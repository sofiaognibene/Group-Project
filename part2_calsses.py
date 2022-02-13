from abc import ABC, abstractmethod
import pandas as pd


# to be tested!!!!


class Operation(ABC):
    def __init__(self, data: pd.DataFrame, description: str):
        self.__data = data
        self.__description = description

    @abstractmethod
    def execute(self):
        pass

    @property
    def description(self) -> str:
        return self.__description


# 1/2
'''
shape_disease = df_disease.shape
shape_gene = df_gene.shape
'''


class Dimensions(Operation):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data, "html?")

    def execute(self) -> tuple:
        return self.__data.shape


# 3/5
'''
df_duplicates_genes = df_gene.loc[:, ["geneid", "gene_symbol"]].drop_duplicates().sort_values
df_duplicates_disease = df_disease.loc[:, ["diseaseid", "disease_name"]].drop_duplicates().sort_values
'''


class RetriveColumns(Operation):
    def __init__(self, data: pd.DataFrame, columns: list[str], repetitions: bool = True, sort: bool = False,
                 ascending: bool = True, sorter: str = ""):
        super().__init__(data, "html?")
        self.__columns = columns
        self.__repetitions = repetitions
        self.__sort = sort
        self.__ascending = ascending
        self.__sorter = sorter

    def execute(self) -> pd.DataFrame:
        if not self.__repetitions:
            a = self.__data.loc[:, self.__columns].drop_duplicates()
        else:
            a = self.__data.loc[:, self.__columns]
        if self.__sort:
            return a.sort_values(by=self.__sorter, ascending=self.__ascending)
        else:
            return a


# 4/6
'''g = "geneid == " + input("geneid: ")
g_sentences = df_gene.query(g)["sentence"]
g_sentence_list = []

for i in g_sentences:
    g_sentence_list.append(i)
print(g_sentence_list)'''


class RetrieveColumnCondition(Operation):
    def __init__(self, data: pd.DataFrame, columns: list[str], input: str, options: list[str]):
        super().__init__(data, "html?")
        self.__columns = columns
        self.__input = input
        self.__options = options

    def execute(self) -> pd.DataFrame:
        q = ""  # this shit is needed if we do not provide in input the type of research that we want to do
        for x in self.__options:
            q += x + " == " + self.__input + " or "
        q = q[:-4:]
        return self.__data.query(q).loc[:, self.__columns]


# 7. Record the 10-top most frequent distinct association between genes and diseases.
'''
df_merge = df_gene.merge(df_disease)
merge_loc = df_merge.loc[:, ["gene_symbol", "disease_name"]]
top_10 = merge_loc.groupby(merge_loc.columns.tolist()).size().reset_index().rename(columns={0: 'counts'}). \
             sort_values('counts', ascending=False).iloc[0:10]
'''


class Merger(Operation):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame):
        super().__init__(data, "html?")
        self.__data2 = data2

    def execute(self) -> pd.DataFrame:
        return self.__data.merge(self.__data2)


class Top10(Operation):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: list[str]):
        super().__init__(data, "html?")
        self.__data2 = data2
        self.__columns = columns

    def execute(self) -> pd.DataFrame:
        output = Merger(self.__data, self.__data2)
        output_loc = RetriveColumns(data=output, columns=self.__columns)
        return output_loc.groupby(output_loc.columns.tolist()).size().reset_index().rename(
            columns={0: 'counts'}).sort_values('counts', ascending=False).iloc[0:10]


# the first step merges the two dataframes based on the pmid and sentence
# next, we select the columns we are interested in
# finally, we select the first 10 elements in a descending-ordered list based on a new column, which is
# 'counts', that counts the number of gene-disease associations we obtained with the groupby function

# 8 / 9
'''gene = "geneid ==" + input("geneid: ")
query_gene = df_gene.query(gene)["pmid"]

gene_disease = []

for a in query_gene:
    query_disease = "pmid ==" + str(a)
    query = df_disease.query(query_disease).loc[:, ["diseaseid", "disease_name"]].drop_duplicates()
    gene_disease.append(query)

gd_final = pd.concat(gene_disease)
print(gd_final)'''


class Correlation(Operation):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: list[str], input: str, options: list[str]):
        super().__init__(data, "html?")
        self.__data2 = data2
        self.__columns = columns
        self.__input = input
        self.__options = options

    def execute(self) -> pd.DataFrame:
        return RetrieveColumnCondition(Merger(self.__data, self.__data2), self.__columns, self.__input,
                                       self.__options).drop_duplicates()


# 1
df_disease = pd.read_csv("disease_evidences.tsv", "\t")
df_gene = pd.read_csv("gene_evidences.tsv", "\t")
