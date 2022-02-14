import pandas as pd
from abc import ABC, abstractmethod
import part2_calsses as op

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
            return operation(*args)
        else:
            return None
df_disease = pd.read_csv("disease_evidences.tsv", "\t")
df_gene = pd.read_csv("gene_evidences.tsv", "\t")


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