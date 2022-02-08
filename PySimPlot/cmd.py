# -*- coding: utf-8 -*-
from . import alignment
from . import similarity
from . import export
from . import plot




import argparse


my_parser = argparse.ArgumentParser(description='PySimPlot')

# Add the arguments
my_parser.add_argument('-i',
                       metavar='aligned.fasta',
                       type=str,
                       help='Input alignment file in FASTA format',
                       required = True)

my_parser.add_argument('-o',
                       metavar='simplot.csv',
                       type=str,
                       default = "simplot.csv",
                       help='Output CSV filename')

my_parser.add_argument('-w',
                       metavar='100',
                       type=int,
                       default=100,
                       help='Rolling window size. Default: 100')

my_parser.add_argument('-s',
                       metavar='1',
                       type=int,
                       default=1,
                       help='Step size. Default: 1')

my_parser.add_argument('-r',
                       metavar="Name",
                       type=str,
                       default=False,
                       help='Select a new reference sequence using the FASTA header value.')


my_parser.add_argument('--gaps',
                       action='store_true',
                       default=False,
                       help='Default: Off. Turn on to include bases/residues where both sequences contain a gap. Not recommended.')

my_parser.add_argument('-v',
                       action='store_true',
                       help='Verbose')




def main():
    # Execute the parse_args() method
    args = my_parser.parse_args()

    inputAlignment = args.i
    outputFile     = args.o
    window         = args.w
    step           = args.s
    verbose        = args.v
    includegaps    = args.gaps
    reference      = args.r






    # Process input alignment (Fasta Formatted)
    sequences = alignment.alignment(inputAlignment, reference)

    # How many sequences were we given?
    noOfSequences  = len(sequences.seqs)

    # Set the first sequence as the reference sequence
    referenceSequence = sequences.seqs[0]


    # Run the comparison of each seq to the reference
    for x in range(1, noOfSequences):
        similarity.main(referenceSequence,sequences.seqs[x], verbose, includegaps, window, step)

    # Export everything to CSV
    plot.single(sequences, window)

    if outputFile:
        export.csv(sequences,window, outputFile)
