import pandas as pd

from scripts.decorators import singleton

READ_CSV_CONFIG={
    "sep":";",
    "decimal":","
}

@singleton
class Dataset:
    def __init__(self, path=None):

        self._path = path
        self._data = None
        self.csv_config=READ_CSV_CONFIG

        if path != None:
            self.setData(path)
        
    def getData(self):
        return self._data

    def setData(self, path, **kwargs):
        self._path = path
        self._data = self._opendDataset(path, *kwargs)

    def _opendDataset(self, path):
        try:
            data = pd.read_csv(path)
            return data
        except FileNotFoundError as error:
            print("File path not found!")

@singleton
class DataDict:

    def __init__(self):
        self._data_dict = {}

    def add_dataset(self, name, dataset):
        self._data_dict[name] = dataset
    
    def get_dataset(self, name):
        return self._data_dict[name]

    def __str__(self):
        print(f"Dataset list {self._data_dict.keys()}")

