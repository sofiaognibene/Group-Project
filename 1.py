#this should be file 1, right?
'''
I am using visual studio Code
'''
import pandas as pd

df_disease = pd.read_csv("disease_evidences.tsv", "\t")

df_gene = pd.read_csv("gene_evidences.tsv", "\t")
'''with open("disease_evidences.tsv") as disease_evidences:
    read_disease_evidences = csv.reader(disease_evidences, delimiter = "\t")
    line_count = 0
    for row in read_disease_evidences:
        diseaseid = row[0]
        sentence = row[1]
        nsentence = row[2]
        pmid = row[3]
        disease_name = row[4]
        disease_type = row[5]
    #print(diseaseid + "\t" + sentence + "\t" + nsentence + "\t" + pmid + "\t" + disease_name + "\t" + disease_type)

with open("gene_evidences.tsv") as gene_evidences:
    read_gene_evidences = csv.reader(gene_evidences, delimiter = "\t")
    line_count = 0
    for row in read_gene_evidences:
        geneid = row[0]
        sentence = row[1]
        nsentence = row[2]
        pmid = row[3]
        gene_symbol = row[4]
        organism = row[5]
    #print(geneid + "\t" + sentence + "\t" + nsentence + "\t" + pmid + "\t" + gene_symbol + "\t" + organism)'''
