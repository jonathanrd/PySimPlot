


class alignment:
    def __init__(self, file, reference=None):

        # Validate inputs
        import os
        assert(os.path.exists(file)), "Can't open input file"

        # Parse the fasta alignment
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

        # Ensure more than one sequence is provided
        assert (len(self.seqs) > 1), "Less than two sequences provided"

        # Check all parsed sequences are of the same length
        self.checkSequenceLength()

        # If args.r[eference] is specified, changeReference
        if (reference):
            self.changeReference(reference)

        # Trim the reference
        self.setReferenceStartEnd()

        self.reference = self.seqs[0]["Name"]





    def checkSequenceLength(self):
        # Length of first sequence
        referencelength = len(self.seqs[0]["Sequence"])

        # True if all sequences are same length as reference seq
        samelength = all(len(d['Sequence']) == referencelength for d in self.seqs)
        assert(samelength), "Input sequence lengths do not match"


    def changeReference(self, name):
        # Choose a new reference and add it to top of list.

        # Find the index from a list of dicts
        index = next((index for (index, d) in enumerate(self.seqs) if d["Name"] == name), None)

        # Check that an index number was returned
        assert(isinstance(index, int)), "Selected reference does not exist"

        # Pop the old dict from list and reinsert it at the top
        self.seqs.insert(0, self.seqs.pop(index))


    def setReferenceStartEnd(self):

        # Remove all trailing "-" from reference
        # We should also do this from the start but more of a challenge
        startLength        = len(self.seqs[0]["Sequence"])
        trimmedReferenceL  = len(self.seqs[0]["Sequence"].lstrip("-"))
        trimmedReferenceLR = len(self.seqs[0]["Sequence"].lstrip("-").rstrip("-"))

        start = startLength-trimmedReferenceL
        end = trimmedReferenceLR

        self.seqs[0]["SeqStart"] = 0
        self.seqs[0]["SeqEnd"]   = end
