import json
import os

class PacModel:
    def __init__(self, data_file = 'info.json'):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.patients = json.load(file)
        else:
            self.patients = []
