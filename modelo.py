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

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.patients, file, indent=4)

    def add_patient(self, patient:dict): 
        if not any(p['id'] == patient['id'] for p in self.patients):
            self.patients.append(patient)
            self.save_data()
            return True
        return False

    def delete_patient(self, patient_id:str):
        initLen = len(self.pets)
        self.patients = [p for p in self.patient if p['id'] != patient_id]
        self.save_data()
        if initLen == len(self.patients):
            return 0
        else:
            return 1

    def search_patients(self, initName:str):
        pass 