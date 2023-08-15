import csv
import pandas as pd

class CSVWorker:

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode

    def is_csv_file(self):
        return self.filename.lower().endswith('.csv')

    def read_csv(self):
        if not self.is_csv_file():
            raise ValueError("The file is not a CSV file.")

        return pd.read_csv(self.filename)

    def write_csv(self, data):
        if not self.is_csv_file():
            raise ValueError("The file is not a CSV file.")

        data_frame = pd.DataFrame(data)
        data_frame.to_csv(self.filename, index=False)