import json
import os

class PatientModel:
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
        initLen = len(self.patients)
        self.patients = [p for p in self.patient if p['id'] != patient_id]
        self.save_data()
        if initLen == len(self.patients):
            return 0
        else:
            return 1

    def get_patient_by_id(self, patient_id):
        for patient in self.patients:
            if patient['id'] == patient_id:
                return patient
        return None

    def search_patients(self, query):
        results = []
        for patient in self.patients:
            if patient['name'].lower().startswith(query.lower()):
                results.append(patient)
        return results
class UserModel:

    def __init__(self, users_file = 'usuarios.json'):
        self.users_file = users_file
        self.load()
        
    def load(self):
        try:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []
            print("No se encontró información")

    def exists(self, user:str, pw:str):
        try:
            for i in self.users:
                if i['usuario'] == user and i['contrasena'] == pw:
                    return (1, f'{user} bienvenido')
            return 0
        except TypeError:
            return 2