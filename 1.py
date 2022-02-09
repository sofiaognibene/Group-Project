#this should be file 1, right?
'''
I am using visual studio Code
'''
import pandas as pd

df_disease = pd.read_csv("disease_evidences.tsv", "\t")

df_gene = pd.read_csv("gene_evidences.tsv", "\t")
