from numpy import column_stack
import pandas as pd
import part2 as op

class DataSet():
    def __init__(self, name: str, path: str):
        self.__name = name
        self.__data = pd.read_csv(path, "\t")
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def data(self) -> pd.DataFrame:
        return self.__data

class OperationBuilder():
    operations_dict = {
        'mtd': op.Dimensions,
        'sm': op.Labels,
        'el': op.RetrieveColumns,
        'rqc': op.RetrieveColumnCondition,
        't10': op.Top10,
        'as': op.Associations,
    }

    @staticmethod
    def create(operation_name: str, *args) -> op.Operation:

        operation = OperationBuilder.operations_dict[operation_name]

        if operation:
            return operation(*args).execute()
        else:
            return None

class OperationManager():
    @staticmethod
    def manager(registry: dict, l : str, input : str =""):
        L=eval(l)
        if (L=='mtd'):
            title = "Metadata"
            collection = {}
            for set in registry.values():
                dim= OperationBuilder.create(L,set.data)
                frame = pd.DataFrame(data=[["Rows", dim[0]],["Columns", dim[1]]], columns=["Description", "Data"])
                collection[set.name] = frame
            return[collection, title]
        elif (L=='sm'):
            title = "Semantics"
            return[{registry['gene'].name : pd.DataFrame(OperationBuilder.create(L,registry['disease'].data)), registry['disease'].name : pd.DataFrame(OperationBuilder.create(L,registry['gene'].data))},title]
        elif(L[0]=='el'):
            title = registry[L[1]].name[:registry[L[1]].name.index(" "):] + " List"
            return [OperationBuilder.create(L[0], registry[L[1]].data, L[2], False, True, True, L[3]), title, input]
        elif(L[0]=='rqc'):
            title = registry[L[1]].name + " Quotes"
            return  [OperationBuilder.create(L[0], registry[L[1]].data, ['sentence'], input, L[2]), title, input]
        elif(L =='t10'):
            title = "Top 10 Associations among Gene and Disease"
            return [OperationBuilder.create(L, registry['gene'].data, registry['disease'].data, ["geneid","gene_symbol","diseaseid","disease_name"]), title, input]
        elif(L[0]=='as'):
            title ="Correlation between specific " +registry[L[1]].name[:registry[L[1]].name.index(" "):] + " and " + registry[L[2]].name[:registry[L[2]].name.index(" "):]
            return [OperationBuilder.create(L[0], registry[L[1]].data, registry[L[2]].data, L[3], input, L[4]), title, input]

def read():
    df_disease = DataSet("Disease Dataset","disease_evidences.tsv")
    df_gene = DataSet("Gene Dataset","gene_evidences.tsv")
    return {"gene" : df_gene, "disease" : df_disease}