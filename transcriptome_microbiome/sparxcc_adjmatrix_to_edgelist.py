#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Get correlated pairs from SparXCC output matrix\
                                 ($cor object from R list generated in SparXCC)")
parser.add_argument('--input', type=str, metavar='SparXCC_output.txt',
                    dest='sparxcc_matrix_file',
                    help='The file with the cross-correlation matrix output from SparXCC',
                    required=True)
parser.add_argument('--cor_threshold', type=float, metavar='0.0',
                    dest='cor_threshold', default=0,
                    help='The threshold for the correlation coefficient to consider significant (default: 0).\
                        Any correlation value greater than or equal to the positive threshold or less than or\
                            equal to the negative threshold will be considered significant.',
                    required=False)
parser.add_argument('--output', type=str, metavar='output.txt',
                    dest='output_file',
                    help='Output file with the significant correlations (if --cor_threshold is passed,\
                    that threshold is considered)',
                    required=True)

args = parser.parse_args()

sparxcc_matrix = args.sparxcc_matrix_file
output_file = args.output_file
correlation_threshold = args.cor_threshold

output_file_obj = open(output_file, 'w')

output_file_obj.write("OTU\tGene\tCorrelationCoefficient\n")

with open(sparxcc_matrix, 'r') as fin:

    colnames = fin.readline().rstrip().split()
    halfmatrix = int(len(colnames) / 2)
    gene_names = [n.replace('cor.','').replace('"', '') for n in colnames[:halfmatrix]]

    for line in fin:
        otu_name, *line_fields = line.rstrip().split()
        otu_name = otu_name.replace('"', '')

        # Retrieve the correlation matrix, the m value and the boolean matrix
        correlations_matrix = line_fields[:halfmatrix]
        m_value = line_fields[halfmatrix]
        m_boolean_matrix = line_fields[halfmatrix + 1:]

        # Get significant correlations
        for i, val in enumerate(m_boolean_matrix):
            if val == 'TRUE' and abs(float(correlations_matrix[i])) >= correlation_threshold:
                output_file_obj.write(otu_name+"\t"+gene_names[i]+"\t"+correlations_matrix[i]+"\n")

output_file_obj.close()