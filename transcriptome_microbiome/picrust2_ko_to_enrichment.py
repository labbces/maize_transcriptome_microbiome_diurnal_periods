#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Generates a TERM2GENE file to be used in the enricher function (clusterProfiler)")
parser.add_argument('--input', type=str, metavar='KO_predicted.tsv (matrix file with KO abundance per ASV/OTU)',
                    dest='picrust_ko_file',
                    help='The file with KO abundance per ASV/OTU',
                    required=True)
parser.add_argument('--output', type=str, metavar='output.txt',
                    dest='output_file',
                    help='Output file with the term2gene mapping to be used in the enricher function',
                    required=True)

args = parser.parse_args()

picrust_ko_file = args.picrust_ko_file
term2gene_file = args.output_file

ko2otus = {}
ko_predicted_line_count = 0

with open(picrust_ko_file, 'r') as infile:
    ko_ids = infile.readline().strip().split('\t')
    ko_ids = ko_ids[1:]
    for line in infile:
        columns = line.strip().split('\t')
        otu = columns[0]
        kos = columns[1:]
        for i, ko in enumerate(kos):
            if int(ko) > 0:
                if ko_ids[i] not in ko2otus.keys():
                    ko2otus[ko_ids[i]] = [otu]
                else:
                    if otu not in ko2otus[ko_ids[i]]:
                        ko2otus[ko_ids[i]].append(otu)
        ko_predicted_line_count += 1

print(f"{len(ko2otus.keys())} KOs found in {picrust_ko_file}")

with open(term2gene_file, 'w') as outfile:
    for ko in ko2otus.keys():
        for otu in ko2otus[ko]:
            outfile.write(f"{ko}\t{otu}\n")

