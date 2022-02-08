# -*- coding: utf-8 -*-
from . import alignment
from . import similarity
from . import exportcsv




import argparse


my_parser = argparse.ArgumentParser(description='PySimPlot')

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

my_parser.add_argument('-r',
                       metavar="REFERENCE",
                       type=str,
                       default=False,
                       help='Select a new reference sequence by name.')


my_parser.add_argument('--gaps',
                       action='store_true',
                       default=False,
                       help='Default: Off. Turn on to include bases/residues where both sequences contain a gap. Not recommended.')

my_parser.add_argument('-v',
                       action='store_true',
                       help='Verbose. See what\'s happening!')




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
        maina(referenceSequence,sequences.seqs[x], verbose)

    # Export everything to CSV
    exportcsv(sequences, outputFile)
