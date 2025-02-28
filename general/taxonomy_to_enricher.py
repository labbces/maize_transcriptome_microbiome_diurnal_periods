#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Generates a TERM2GENE file to be used in the enricher function (clusterProfiler)")
parser.add_argument('--input', type=str, metavar='gtdb_taxonomy.tsv',
                    dest='gtdb_taxonomy_file',
                    help='The TSV file with OTU, GTDB taxonomy path and confidence value (first two columns are used)',
                    required=True)
parser.add_argument('--output', type=str, metavar='term2gene.txt',
                    dest='term2gene_file',
                    help='Output file with the term2gene mapping to be used in the enricher function.',
                    required=True)
parser.add_argument('--rank', type=str, metavar='g',
                    dest='taxon_rank',
                    help='Rank to be used in the term2gene file (default: g). Alternatives: f (family), c (class), p (phylum), o (order)',
                    required=True)

args = parser.parse_args()

gtdb_taxonomy_file = args.gtdb_taxonomy_file
term2gene_file = args.term2gene_file
taxon_rank = args.taxon_rank

if taxon_rank not in ['g', 'c', 'p', 'o', 'f']:
    print(f"Error: taxon rank {taxon_rank} not recognized.")
    exit(1)

otu_taxonomy_dict = {}

taxon2otus = {}
taxon2otus['Unclassified'] = []

with open(gtdb_taxonomy_file, 'r') as infile:
    for line in infile:
        
        rank_found = False

        columns = line.strip().split('\t')
        if len(columns) < 2:
            print(f"Error: line with less than 2 columns: {line}")
            exit(1)
        otu = columns[0]
        taxonomy = columns[1]
        taxonomy_list = taxonomy.split(';')
        
        for taxon_field in taxonomy_list:
            if taxon_field.startswith(taxon_rank + '__'):
                otu_taxon = taxon_field.split('__')[1]
                if otu_taxon not in taxon2otus.keys():
                    taxon2otus[otu_taxon] = [otu]
                else:
                    taxon2otus[otu_taxon].append(otu)
                rank_found = True
        
        if not rank_found:
            taxon2otus['Unclassified'].append(otu)

with open(term2gene_file, 'w') as outfile:
    for taxon in taxon2otus.keys():
        for otu in taxon2otus[taxon]:
            outfile.write(f"{taxon}\t{otu}\n")