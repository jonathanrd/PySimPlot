# pySimPlot

pySimPlot takes an alignment of two or more sequences (nucleotide or amino acid) in fasta format and then calculates the % identity between them within a rolling window. The resulting data are returned in csv format for you to format with Excel etc.

[See the blog post for details!](https://jonathanrd.com/20-05-02-writing-a-simplot-clone-in-python/)


## Usage

Download the script either directly or by cloning this Git repo. Run using -h for a list of all available options.

```bash
./pySimPlot.py -h
```

An example alignment is provided. To run using this example type the following. Note: the -v flag is useful to double check that everything is running as it should.

```bash
./pySimPlot.py -i example.ali -o plot.csv -v
```
