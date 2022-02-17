from numpy import column_stack
import pandas as pd
import part2 as op

class DataSet():  # creates an object with the name of the dataset and its data content
    def __init__(self, name: str, path: str):
        self.__name = name
        self.__data = pd.read_csv(path, "\t")
    @staticmethod
    def read(directory: list):
        collection= {}
        for i in directory:
            collection[i[0]]=DataSet(i[1],i[2])
        return collection
    
    @property
    def name(self) -> str:
        return self.__name
    @property
    def data(self) -> pd.DataFrame:
        return self.__data

class OperationBuilder():  #it stores the list of operations, providing the connection between them and the OperationManager
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

class OperationManager():  # manages requests from the user, providing answers and the title to visualize
    @staticmethod
    def manager(registry: dict, L : list, input : str ="") -> list:
        if (L[0]=='mtd'):
            title = "Metadata"
            collection = {}
            for set in registry.values():
                dim= OperationBuilder.create(L[0],set.data)
                frame = pd.DataFrame(data=[["Rows", dim[0]],["Columns", dim[1]]], columns=["Description", "Data"])
                collection[set.name] = frame
            return[collection, title]
        elif (L[0]=='sm'):
            title = "Semantics"
            return[{registry['gene'].name : pd.DataFrame(OperationBuilder.create(L[0],registry['disease'].data)), registry['disease'].name : pd.DataFrame(OperationBuilder.create(L[0],registry['gene'].data))},title]
        elif(L[0]=='el'):
            title = registry[L[1]].name[:registry[L[1]].name.index(" "):] + " List"
            return [OperationBuilder.create(L[0], registry[L[1]].data, L[2], False, True, True, L[3]), title, input]
        elif(L[0]=='rqc'):
            title = registry[L[1]].name + " Quotes"
            return  [OperationBuilder.create(L[0], registry[L[1]].data, ['sentence'], input, L[2]), title, input]
        elif(L[0] =='t10'):
            if (input == "n"):
                input = ""
                del_rows=['sentence','nsentence']
            title = "Top 10 Associations among Gene and Disease"
            return [OperationBuilder.create(L[0], registry['gene'].data, registry['disease'].data, ["geneid","gene_symbol","diseaseid","disease_name"],del_rows), title, input]
        elif(L[0]=='as'):
            del_rows = []
            print(input)
            s = input[input.rfind(" ")+1:len(input):]
            print(s)
            if (s == "n"):
                input = input[:len(input)-2:]
                del_rows=['sentence','nsentence']
            title ="Correlation between specific " +registry[L[1]].name[:registry[L[1]].name.index(" "):] + " and " + registry[L[2]].name[:registry[L[2]].name.index(" "):]
            return [OperationBuilder.create(L[0], registry[L[1]].data, registry[L[2]].data, L[3], input, L[4], del_rows), title, input]