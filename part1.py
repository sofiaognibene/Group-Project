from numpy import column_stack
import pandas as pd
from abc import ABC, abstractmethod
import part2_calsses as op
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
    def manager(registry: dict, l : str, input : str):
        L=eval(l)
        if (L[0]=='mtd'):
            pass
        elif(L[0]=='el'):
            title = registry[L[1]].name[:registry[L[1]].name.index(" "):] + " List"
            return [OperationBuilder.create(L[0], registry[L[1]].data, L[2], False, True, True, L[3]), title]
        elif(L[0]=='rqc'):
            title = registry[L[1]].name[:registry[L[1]].name.index(" "):] + "Quotes"
            return  [OperationBuilder.create(L[0], registry[L[1]].data, ['sentence'], input, L[2]), title, input]

def read():
    df_disease = DataSet("Gene Dataset","disease_evidences.tsv")
    df_gene = DataSet("Disease Dataset","gene_evidences.tsv")
    return {"gene" : df_gene, "disease" : df_disease}


'''

class OperationListBuilder:

    @staticmethod
    def build(registry, **kwargs):

        name_parts = kwargs['name'].split()
        brand = name_parts[0]
        model_name = ' '.join(name_parts[1:])

        if brand in registry:
            manufacturer = registry[brand]
        else:
            manufacturer = Manufacturer(brand)
            registry.update({brand: manufacturer})

        characteristics = []
        for key, value in kwargs.items():
            if key != 'name':
                characteristic = ModelCharacteristicBuilder.build(key, value)
                characteristics.append(characteristic)

        model = Model(manufacturer, model_name, characteristics)
        manufacturer.add_model(model)

        return registry


class DatasetReader:

    @staticmethod
    def read(data_path):

        registry = dict()

        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            header = []
            for row in csv_reader:
                if line_count == 0:
                    header = row
                else:
                    item_count = 0
                    representation = dict()
                    for item in row:
                        print(item)
                        representation.update({header[item_count]: item})
                        item_count += 1

                    ModelBuilder.build(registry, **representation)

                line_count += 1

        return registry
'''