import csv
from turtle import pd
import pandas as pd

#1
df_disease = pd.read_csv("disease_evidences.tsv", "\t")
df_gene = pd.read_csv("gene_evidences.tsv", "\t")

#2
shape_disease = df_disease.shape
shape_gene = df_gene.shape

#3
df_duplicates_genes = df_gene.loc[:, ["geneid", "gene_symbol"]].drop_duplicates().sort_values

#4
'''g = "geneid == " + input("geneid: ")
g_sentences = df_gene.query(g)["sentence"]
g_sentence_list = []

for i in g_sentences:
    g_sentence_list.append(i)
print(g_sentence_list)'''

#5
df_duplicates_disease = df_disease.loc[:, ["diseaseid", "disease_name"]].drop_duplicates().sort_values

#6

d = "diseaseid == " + "'" + input("diseaseid: ") + "'"
d_sentences = df_disease.query(d)["sentence"]
d_sentence_list = []

for e in d_sentences:
    d_sentence_list.append(e)
print(d_sentence_list)