#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Generates a TERM2GENE file to be used in the enricher function (clusterProfiler) for KEGG pathways")
parser.add_argument('--otu_ko_association', type=str, metavar='otus_ko.txt',
                    dest='otu_ko_file',
                    help='The file with KOs associated with OTU/ASV (TERM2GENE output from picrust2_ko_to_enrichment.py)',
                    required=True)
parser.add_argument('--ko_map_association', type=str, metavar='ko',
                    dest='ko_map_file',
                    help='The file with KOs associated with KEGG pathways (from https://rest.kegg.jp/link/pathway/ko)',
                    required=True)
parser.add_argument('--output', type=str, metavar='output.txt',
                    dest='output_file',
                    help='Output file with the term2gene mapping to be used in the enricher function',
                    required=True)

args = parser.parse_args()

otu_ko_file = args.otu_ko_file
ko_map_file = args.ko_map_file
term2gene_file = args.output_file

kos2pathways = {}
otu2kos = {}
otu2pathways = {}

with open(ko_map_file, 'r') as infile:
    for line in infile:
        columns = line.strip().split('\t')
        ko = columns[0]
        ko = ko.replace('ko:', '')
        pathway = columns[1]
        pathway = pathway.replace('path:', '')
        if ko not in kos2pathways.keys():
            kos2pathways[ko] = [pathway]
        else:
            kos2pathways[ko].append(pathway)

with open(otu_ko_file, 'r') as infile:
    for line in infile:
        columns = line.strip().split('\t')
        ko = columns[0]
        otu = columns[1]
        if otu not in otu2kos.keys():
            otu2kos[otu] = [ko]
        else:
            otu2kos[otu].append(ko)

for otu in otu2kos.keys():
    for ko in otu2kos[otu]:
        if ko in kos2pathways.keys():
            for pathway in kos2pathways[ko]:
                if otu not in otu2pathways.keys():
                    otu2pathways[otu] = [pathway]
                else:
                    otu2pathways[otu].append(pathway)

with open(term2gene_file, 'w') as outfile:
    for otu in otu2pathways.keys():
        for pathway in otu2pathways[otu]:
            outfile.write(f"{pathway}\t{otu}\n")