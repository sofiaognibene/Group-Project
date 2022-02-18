from abc import ABC, abstractmethod
from heapq import merge
from pydoc import doc
import pandas as pd

class Operation(ABC):
    '''
    Abstract class parent of all the operations. Its only attribute is data, a pd.Dataframe.
    '''
    def __init__(self, data: pd.DataFrame):
        self._data = data

    @abstractmethod
    def execute(self):
        pass


class Dimensions(Operation):
    '''
    Its method execute uses pd.shape function to return the dimensions of its attribute data.
    '''
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def execute(self) -> tuple:
        return self._data.shape

class Labels(Operation):
    '''
    Its method execute returns the head of its attribute data.
    '''
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
    def execute(self) -> list:
        return self._data.columns.values

class RetrieveColumns(Operation):
    '''
    Its method execute returns specific columns of the dataframe stored in the attribute data.
    Therefore, this class requires, in addition to the dataframe, the list of columns to return, if repetitions must be included, if it must be sorted and how.
    '''
    def __init__(self, data: pd.DataFrame, columns: 'list[str]', repetitions: bool = True, sort: bool = False,
                 ascending: bool = True, sorter: str = ""):
        super().__init__(data)
        self.__columns = columns
        self.__repetitions = repetitions
        self.__sort = sort
        self.__ascending = ascending
        self.__sorter = sorter

    def execute(self) -> pd.DataFrame:
        if not self.__repetitions:
            a = self._data.loc[:, self.__columns].drop_duplicates()
        else:
            a = self._data.loc[:, self.__columns]
        if self.__sort:
            return a.sort_values(by=self.__sorter, ascending=self.__ascending)
        else:
            return a

class RetrieveColumnCondition(Operation):
    '''
    Its method execute returns specific columns of the dataframe stored in the attribute data under specific conditions.
    Therefore, this class requires, in addition to the dataframe, the list of columns to return, the condition in the form of input and the columns where we are looking for that input.
    It uses the query function.
    '''
    def __init__(self, data: pd.DataFrame, columns: 'list[str]', input: str, options: 'list[str]'):
        super().__init__(data)
        self._columns = columns
        self._input = input
        self._options = options

    def execute(self) -> pd.DataFrame:
        q = ""
        if self._input.isdigit():
            for x in self._options:
                q += x + " == " + self._input + " or "
        else:
            for x in self._options:
                q += x + " == " + "'"+ self._input + "'"+ " or "
        q = q[:-4:]
        return self._data.query(q).loc[:, self._columns]

class Merger(Operation):
    '''
    Taking as attributes two pd.DataFrame, its execute method returs their merging, using the merge function.
    '''
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, del_rows: 'list[str]' = []):
        super().__init__(data)
        self.__data2 = data2
        self.__to_del = del_rows

    def execute(self) -> pd.DataFrame:
        self._data = self._data.drop(columns = self.__to_del)
        self.__data2= self.__data2.drop(columns = self.__to_del)
        print(self._data.columns.values)
        return self._data.merge(self.__data2)

class Top10(Operation):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: 'list[str]', del_rows: 'list[str]' = []):
        super().__init__(data)
        self.__data2 = data2
        self.__columns = columns
        self.__to_del = del_rows

    def execute(self) -> pd.DataFrame:
        output = Merger(self._data, self.__data2, self.__to_del).execute()
        output_loc = RetrieveColumns(data=output, columns=self.__columns).execute()
        return output_loc.groupby(output_loc.columns.tolist(), as_index=False).size().\
            sort_values('size', ascending=False).iloc[0:10]

class Associations(RetrieveColumnCondition):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: 'list[str]', input: str, options: 'list[str]', del_rows: 'list[str]' = []):
        super().__init__(Merger(data, data2, del_rows).execute(), columns, input, options)

    def execute(self) -> pd.DataFrame:
        return super().execute().drop_duplicates()