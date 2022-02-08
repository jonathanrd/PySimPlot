PySimPlot
=========

PySimPlot takes an alignment of two or more sequences (nucleotide or amino acid) in fasta format and then calculates the identity between them within a rolling window. The resulting data are returned plotted and optionally saved as a csv file for you to format with Excel etc.

This software is inspired by [SimPlot](https://sray.med.som.jhmi.edu/SCRoftware/SimPlot/) from Stuart Ray.

Example Usage:

    clustalo -i sequences.fasta -o aligned.fasta
    pysimplot -i aligned.fasta -o data.csv


![Example similarity plot](https://jonathanrd.com/public/screenshot.png)
