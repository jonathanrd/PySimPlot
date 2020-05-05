#! /usr/bin/env python3

import argparse
import os

my_parser = argparse.ArgumentParser(description='pySimPlot')

# Add the arguments
my_parser.add_argument('-i',
                       metavar='ALIGNMENT',
                       type=str,
                       help='the input alignment file')

my_parser.add_argument('-o',
                       metavar='out.csv',
                       type=str,
                       default = "out.csv",
                       help='the output CSV file')

my_parser.add_argument('-w',
                       metavar='100',
                       type=int,
                       default=100,
                       help='rolling window size')

my_parser.add_argument('-s',
                       metavar='1',
                       type=int,
                       default=1,
                       help='step size')

my_parser.add_argument('--gaps',
                       action='store_true',
                       default=False,
                       help='Default: Off. Turn on to include bases/residues where both sequences contain a gap. Not recommended.')

my_parser.add_argument('-v',
                       action='store_true',
                       help='Verbose. See what\'s happening!')



# Execute the parse_args() method
args = my_parser.parse_args()

inputAlignment = args.i
outputFile     = args.o
window         = args.w
step           = args.s
verbose        = args.v
includegaps    = args.gaps

# Validate inputs
assert(os.path.exists(inputAlignment)), "Can't open input file"




class fasta:
    def __init__(self, file):

        with open(file, "r") as file:
            header = ""
            seq = ""
            self.seqs = []
            line = file.readline()
            while (line):
                line = line.rstrip('\n')
                if ">" in line:
                    if header != "":
                        self.seqs.append({"Name": header[1:], "Sequence": seq})
                        header = ""
                        seq = ""
                    header = line
                else:
                    seq = seq + line
                line = file.readline()
            self.seqs.append({"Name": header[1:], "Sequence": seq})

    def count(self):
        return len(self.seqs)

    def changeReference(self, name):
        # Choose a new reference and add it to top of list.

        # Find the index from a list of dicts
        index = next((index for (index, d) in enumerate(self.seqs) if d["Name"] == name), None)

        # Check that an index number was returned
        assert(isinstance(index, int)), "Selected reference does not exist"

        # Pop the old dict from list and reinsert it at the top
        self.seqs.insert(0, self.seqs.pop(index))





class Pointer:

    # Set all initial values using calculate() on load
    def __init__(self, window, step):
        self.window = window
        self.step = step
        self.iteration = 0
        self.calculate()

    # Read the current parameters and set values
    def calculate(self):
        self.window_lower = self.step * self.iteration
        self.window_upper = self.window + self.step * self.iteration

        # Is the window size odd or even? Set correct pointer location
        if (self.window % 2) == 0:
            self.pointer = int((self.window / 2) - 1 + self.step * self.iteration)
        else:
            self.pointer = int((self.window - 1) / 2 + self.step * self.iteration)

    # Increase the iteration count and recalculate all values
    def increment(self):
        self.iteration += 1
        self.calculate()

    # Reset the iteration count to zero and recalculate all values
    def reset(self):
        self.iteration = 0
        self.calculate()





def compare(sequenceA, sequenceB):
    global args
    includegaps = args.gaps

    length = len(sequenceA)

    # Initiate counters
    sum = 0
    window_adjust = 0

    # Look at each position in turn
    for base in range(0, length):

        # Deal with gaps (gap in ref and seq to compare)
        if((sequenceA[base] == "-" and sequenceB[base] == "-") and includegaps == False):
              window_adjust  += 1
              continue

        # Is the base/residue the same?
        if ( sequenceA[base] == sequenceB[base]):

            # Increase the counter
            sum += 1

    # Avoid a divide by zero error
    if (window_adjust == length): length += 1

    # Convert the count to a percentage
    identity = sum / (length - window_adjust) * 100
    return identity




# Take the Pointer object and extract a windowed sequence
# from the full-length sequence
def extract(pointer, sequence):

    # Get the window boundaries
    lower = pointer.window_lower
    upper = pointer.window_upper
    windowed_sequence = sequence[lower:upper]
    return windowed_sequence


def main(seqA, seqB, verbose):
    sequenceA = seqA["Sequence"]
    sequenceB = seqB["Sequence"]

    # Verbose output
    if (verbose):
        print("\n\nNow comparing: ",seqA["Name"],"with",seqB["Name"])
        print("\n\n")

    # Initiate an empy dict to hold the identity values
    combined_identities = {}

    # Initiate the pointer class
    pointer = Pointer(window,step)

    # Iterate through the sequences
    # but stop when the window goes past the last base/residue
    while pointer.window_upper <= len(sequenceA):

        # Extract the part each sequence to compare
        compareA = extract(pointer, sequenceA)
        compareB = extract(pointer, sequenceB)

        # Compare the sequences and get the % identity
        identity = compare(compareA, compareB)


        # Verbose output
        if (verbose):
            print("Window: ",pointer.window_lower,pointer.window_upper)
            print("A: ",compareA)
            print("B: ",compareB)
            print("Identity: ",round(identity,2),"\n")

        # Add the identity to our array using the pointer position as a key
        combined_identities[pointer.pointer] = identity

        # Increment the pointer and window location
        pointer.increment()

    seqB["Identities"]=combined_identities
    #print(combined_identities)

    pointer.reset()




def csvExport(sequences, outputFile):

    import csv

    # First make the CSV header
    header = ["pointer"]
    for y in range(1,len(sequences.seqs) ):
        header.append(sequences.seqs[y]["Name"])

    # Now read all of the identities
    rows = [sequences.seqs[y]["Identities"].keys()]
    for y in range(1,len(sequences.seqs) ):
        rows.append(sequences.seqs[y]["Identities"].values())
    rows = zip(*rows)

    # Write it to the output file
    with open(outputFile, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)






# Process input alignment (Fasta Formatted)
sequences = fasta(inputAlignment)

# How many sequences were we given?
noOfSequences  = len(sequences.seqs)

# Set the first sequence as the reference sequence
referenceSequence = sequences.seqs[0]

# Run the comparison of each seq to the reference
for x in range(1, noOfSequences):
    main(referenceSequence,sequences.seqs[x], verbose)

# Export everything to CSV
csvExport(sequences, outputFile)
