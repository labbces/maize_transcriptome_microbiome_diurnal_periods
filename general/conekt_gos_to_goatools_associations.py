#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Get GO file used in CoNekT Grasses and generates an association file for GOATOOLS")
parser.add_argument('--input', type=str, metavar='Zma_gos.tsv.txt',
                    dest='conekt_go_file',
                    help='The TSV file with the gene, GO term and evidence code',
                    required=True)
parser.add_argument('--output', type=str, metavar='output.txt',
                    dest='output_file',
                    help='Output file with the significant correlations (pairs of OTUs and genes passing the permutation threshold)',
                    required=True)

args = parser.parse_args()

conekt_go_file = args.conekt_go_file
output_file = args.output_file

gene2go = {}

with open(conekt_go_file, 'r') as fin:

    for line in fin:
        gene, go, evidence = line.rstrip().split()
        if gene not in gene2go:
            gene2go[gene] = [go]
        else:
            if go not in gene2go[gene]:
                gene2go[gene].append(go)

output_file_obj = open(output_file, 'w')

for key in gene2go.keys():
    output_file_obj.write(key+"\t"+";".join(gene2go[key])+"\n")

output_file_obj.close()