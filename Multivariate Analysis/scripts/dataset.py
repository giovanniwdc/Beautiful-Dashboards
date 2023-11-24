import pandas as pd

from scripts.decorators import singleton

@singleton
class Dataset():

    def __init__(self, path):

        self._path = path
        
        if path != None:
            self._opendDataset(path)
        
    def getData(self):
        return self._data

    def setData(self, path):
        self._path = path
        self._opendDataset(path)

    def _opendDataset(self, path):

        try:
            data = pd.read_csv(path)
            self._data = data
        except FileNotFoundError as error:
            print("File path not found!")
        self._data = dataset
