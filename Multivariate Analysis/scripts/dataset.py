import pandas as pd

from scripts.decorators import singleton

@singleton
class Dataset:
    def __init__(self, path=None):

        self._path = path
        self._data = None

        if path != None:
            self.setData(path)
        
    def getData(self):
        return self._data

    def setData(self, path):
        self._path = path
        self._data = self._opendDataset(path)

    def _opendDataset(self, path):
        try:
            data = pd.read_csv(path)
            return data
        except FileNotFoundError as error:
            print("File path not found!")
