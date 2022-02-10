import csv
from turtle import pd
import pandas as pd
import numpy
from pyparsing import col

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
'''d = "diseaseid == " + "'" + input("diseaseid: ") + "'"
d_sentences = df_disease.query(d)["sentence"]
d_sentence_list = []

for e in d_sentences:
    d_sentence_list.append(e)
print(d_sentence_list)'''

#7. Record the 10-top most frequent distinct association between genes and diseases.

df_merge = df_gene.merge(df_disease)
merge_loc = df_merge.loc[:, ["gene_symbol", "disease_name"]]
top_10 = merge_loc.groupby(merge_loc.columns.tolist()).size().reset_index().rename(columns={0:'counts'}).\
    sort_values('counts', ascending= False).iloc[0:10]

#the first step merges the two dataframes based on the pmid, since it is the only element in common
#next, we select the columns we are interested in
#finally, we select the first 10 elements in a descending-ordered list based on a new column, which is
#'counts', that counts the number of gene-disease associations we obtained with the groupby function

#8
'''gene = "geneid ==" + input("geneid: ")
query_gene = df_gene.query(gene)["pmid"]

gene_disease = []

for a in query_gene:
    query_disease = "pmid ==" + str(a)
    query = df_disease.query(query_disease).loc[:, ["diseaseid", "disease_name"]].drop_duplicates()
    gene_disease.append(query)

gd_final = pd.concat(gene_disease)
print(gd_final)'''

#9
'''disease = "diseaseid ==" + "'" + input("diseaseid: ") + "'"
query_disease = df_disease.query(disease)["pmid"]

disease_gene = []

for z in query_disease:
    query_gene = "pmid ==" + str(z)
    g_query = df_gene.query(query_gene).loc[:, ["geneid"]].drop_duplicates()
    disease_gene.append(g_query)

dg_final = pd.concat(disease_gene)
print(dg_final)'''