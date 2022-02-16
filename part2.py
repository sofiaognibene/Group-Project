from abc import ABC, abstractmethod
from heapq import merge
import pandas as pd

class Operation(ABC):
    def __init__(self, data: pd.DataFrame, description: str):
        self._data = data
        self._description = description

    @abstractmethod
    def execute(self):
        pass

    @property
    def description(self) -> str:
        return self._description

class Dimensions(Operation):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data, "html?")

    def execute(self) -> tuple:
        return self._data.shape

class Labels(Operation):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data, "html?")
    def execute(self) -> list:
        return self._data.columns.values

class RetrieveColumns(Operation):
    def __init__(self, data: pd.DataFrame, columns: 'list[str]', repetitions: bool = True, sort: bool = False,
                 ascending: bool = True, sorter: str = ""):
        super().__init__(data, "It selects specific columns, eventually deleting repetitions and ordering them.")
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
    def __init__(self, data: pd.DataFrame, columns: 'list[str]', input: str, options: 'list[str]'):
        super().__init__(data, "html?")
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
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame):
        super().__init__(data, "Merger")
        self.__data2 = data2

    def execute(self) -> pd.DataFrame:
        return self._data.merge(self.__data2)

class Top10(Operation):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: 'list[str]'):
        super().__init__(data, "html?")
        self.__data2 = data2
        self.__columns = columns

    def execute(self) -> pd.DataFrame:
        output = Merger(self._data, self.__data2).execute()
        output_loc = RetrieveColumns(data=output, columns=self.__columns).execute()
        return output_loc.groupby(output_loc.columns.tolist()).size().reset_index().rename(
            columns={0: 'counts'}).sort_values('counts', ascending=False).iloc[0:10]

class Associations(RetrieveColumnCondition):
    def __init__(self, data: pd.DataFrame, data2: pd.DataFrame, columns: 'list[str]', input: str, options: 'list[str]'):
        super().__init__(Merger(data, data2).execute(), columns, input, options)
        self._description = "<hmtl>"

    def execute(self) -> pd.DataFrame:
        return super().execute().drop_duplicates()