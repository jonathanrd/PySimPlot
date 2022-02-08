

def exportcsv(sequences, outputFile):

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
