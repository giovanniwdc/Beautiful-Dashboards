import pandas as pd

from scripts.decorators import singleton

READ_CSV_CONFIG={
    "sep":";",
    "decimal":","
}

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

