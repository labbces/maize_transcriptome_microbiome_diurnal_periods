#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Generates a TXT file to be used in Krona from a file with OTUs and their respective taxonomy (GTDB)")
parser.add_argument('--input', type=str, metavar='gtdb_taxonomy.tsv',
                    dest='gtdb_taxonomy_file',
                    help='The TSV file OTU, GTDB taxonomy path and confidence value (first two columns are used)',
                    required=True)
parser.add_argument('--output', type=str, metavar='krona.txt',
                    dest='krona_txt_file',
                    help='Output file with the TXT file to be used in Krona',
                    required=True)

args = parser.parse_args()

gtdb_taxonomy_file = args.gtdb_taxonomy_file
krona_txt_file = args.krona_txt_file

otu_taxonomy_dict = {}

with open(gtdb_taxonomy_file, 'r') as infile:
    for line in infile:
        columns = line.strip().split('\t')
        if len(columns) < 2:
            print(f"Error: line with less than 2 columns: {line}")
            exit(1)
        otu = columns[0]
        taxonomy = columns[1]
        taxonomy_list = taxonomy.split(';')
        
        domain_found = False
        phylum_found = False
        class_found = False
        
        otu_taxonomy_dict[otu] = {}

        for taxon_rank in taxonomy_list:
            if taxon_rank.startswith('d__'):
                domain = taxon_rank.split('__')[1]
                if domain == 'Bacteria':
                    domain_found = True
                    otu_taxonomy_dict[otu]['domain'] = domain
                else:
                    print(f"Error: domain different from Bacteria: {domain}")
                    exit(1)
        
        for taxon_rank in taxonomy_list:
            if taxon_rank.startswith('p__'):
                phylum_found = True
                phylum = taxon_rank.split('__')[1]
                otu_taxonomy_dict[otu]['phylum'] = phylum
        
        for taxon_rank in taxonomy_list:
            if taxon_rank.startswith('c__'):
                class_found = True
                taxon_class = taxon_rank.split('__')[1]
                otu_taxonomy_dict[otu]['class'] = taxon_class
        
        if not domain_found:
            otu_taxonomy_dict[otu]['domain'] = 'Unclassified'

        if not phylum_found:
            otu_taxonomy_dict[otu]['phylum'] = 'Unclassified'
        
        if not class_found:
            otu_taxonomy_dict[otu]['class'] = 'Unclassified'

count_class = {}
class2phylum = {}
unclass2phylum = {}
class2domain = {}

for otu in otu_taxonomy_dict.keys():
    # Treating unclassified classes
    if otu_taxonomy_dict[otu]['class'] == 'Unclassified':
        if otu_taxonomy_dict[otu]['domain']+"\t"+otu_taxonomy_dict[otu]['phylum']+"\tUnclassified" in unclass2phylum.keys():
            unclass2phylum[otu_taxonomy_dict[otu]['domain']+"\t"+otu_taxonomy_dict[otu]['phylum']+"\tUnclassified"] += 1
        else:
            unclass2phylum[otu_taxonomy_dict[otu]['domain']+"\t"+otu_taxonomy_dict[otu]['phylum']+"\tUnclassified"] = 1
        continue

    # Treating classified classes
    elif otu_taxonomy_dict[otu]['class'] in count_class.keys():
        count_class[otu_taxonomy_dict[otu]['class']] += 1
    else:
        count_class[otu_taxonomy_dict[otu]['class']] = 1
    
    if otu_taxonomy_dict[otu]['class'] in class2phylum.keys():
        if otu_taxonomy_dict[otu]['class'] and otu_taxonomy_dict[otu]['phylum']:
            if otu_taxonomy_dict[otu]['phylum'] != class2phylum[otu_taxonomy_dict[otu]['class']]:
                print(f"Error: class {otu_taxonomy_dict[otu]['class']} has more than one phylum ({class2phylum[otu_taxonomy_dict[otu]['class']]})")
                exit(1)
    else:
        if otu_taxonomy_dict[otu]['phylum']:
            class2phylum[otu_taxonomy_dict[otu]['class']] = otu_taxonomy_dict[otu]['phylum']
    
    if otu_taxonomy_dict[otu]['class'] in class2domain.keys():
        if otu_taxonomy_dict[otu]['class'] and otu_taxonomy_dict[otu]['domain']:
            if otu_taxonomy_dict[otu]['domain'] != class2domain[otu_taxonomy_dict[otu]['class']]:
                print(f"Error: class {otu_taxonomy_dict[otu]['class']} has more than one domain ({class2domain[otu_taxonomy_dict[otu]['class']]})")
                exit(1)
    else:
        if otu_taxonomy_dict[otu]['domain']:
            class2domain[otu_taxonomy_dict[otu]['class']] = otu_taxonomy_dict[otu]['domain']

with open(krona_txt_file, 'w') as outfile:
    for taxon_class in count_class.keys():
        outfile.write(f'{count_class[taxon_class]}\t{class2domain[taxon_class]}\t{class2phylum[taxon_class]}\t{taxon_class}\n')
    for unclass in unclass2phylum.keys():
        outfile.write(f'{unclass2phylum[unclass]}\t{unclass}\n')