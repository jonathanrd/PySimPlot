

class Pointer:

    # Set all initial values using calculate() on load
    def __init__(self, window, step, offset = 0):
        self.window = window
        self.step = step
        self.iteration = 0
        self.offset = offset
        self.calculate()

    # Read the current parameters and set values
    def calculate(self):
        self.window_lower = self.step * self.iteration + self.offset
        self.window_upper = self.window + self.step * self.iteration  + self.offset

        # Is the window size odd or even? Set correct pointer location
        if (self.window % 2) == 0:
            self.pointer = int((self.window / 2) - 1 + self.step * self.iteration) + self.offset
        else:
            self.pointer = int((self.window - 1) / 2 + self.step * self.iteration) + self.offset

    # Increase the iteration count and recalculate all values
    def increment(self):
        self.iteration += 1
        self.calculate()

    # Reset the iteration count to zero and recalculate all values
    def reset(self):
        self.iteration = 0
        self.calculate()





def compare(sequenceA, sequenceB, gaps = False):
    """Compares two sequences and returns the identity. If gaps is set to True then count a shared gap as identical.

    Args:
        sequenceA (str): The first sequence.
        sequenceA (str): The second sequence.
        gaps (bool): Should gaps count as identical? (Default: False)

    Returns:
        float: identity.

    """


    assert(len(sequenceA) == len(sequenceA)), "Sequence lengths do not match"

    length = len(sequenceA)

    # Initiate counters
    identical  = 0
    gap_length = 0

    # Look at each position in turn
    for base in range(0, length):

        # Deal with gaps (gap in ref and seq to compare)
        if((sequenceA[base] == "-" and sequenceB[base] == "-") and gaps == False) :
              gap_length += 1
              continue

        # Is the base/residue the same?
        if ( sequenceA[base] == sequenceB[base]):

            # Increase the counter
            identical += 1

    # Avoid a divide by zero error
    if (gap_length == length): length += 1

    # Convert the count to a percentage
    identity = identical / (length - gap_length) * 100
    return identity





def main(seqA, seqB, verbose, gaps, window, step):
    sequenceA = seqA["Sequence"]
    sequenceB = seqB["Sequence"]

    offset = seqA["SeqStart"]



    # Verbose output
    if (verbose):
        print("\n\nNow comparing: ",seqA["Name"],"with",seqB["Name"])
        print("\n\n")

    # Initiate an empy dict to hold the identity values
    combined_identities = {}

    # Initiate the pointer class
    pointer = Pointer(window, step, offset)

    # Iterate through the sequences
    # but stop when the window goes past the last base/residue
    while pointer.window_upper <= seqA["SeqEnd"]:

        # Extract the part each sequence to compare
        lower = pointer.window_lower
        upper = pointer.window_upper
        compareA = sequenceA[lower:upper]
        compareB = sequenceB[lower:upper]

        # Compare the sequences and get the % identity
        identity = compare(compareA, compareB, gaps)


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
