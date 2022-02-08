

def single(sequences, window):
    import matplotlib.pyplot as plt

    #plt.rcParams['toolbar'] = 'none'


    # Get the headers
    header = ["pointer"]
    print(len(sequences.seqs))
    for y in range(1,len(sequences.seqs) ):
        header.append(sequences.seqs[y]["Name"])

    # Now read all of the identities
    for y in range(1,len(sequences.seqs) ):
        ident = sequences.seqs[y]["Identities"].values()
        x = range(0+int(window/2),len(ident)+int(window/2))
        plt.plot(x, ident, label=header[y])

    # Set the title
    reference = sequences.seqs[0]["Name"]
    plt.title(f"Similarity plot using {reference} as reference.")

    plt.legend()
    plt.xlabel("Position")
    plt.ylabel("Identity (%)")



    plt.show()
