import json
import os

class PatientModel:
    #se encarga de manejar la logica relacionada con el paciente 
    def __init__(self, data_file = 'info.json'):
        #inicializa la clase con el archivo json que contiene la informacion de los pacientes y carga la informacion con el metodo load data
        self.data_file = data_file
        self.load_data()


    def load_data(self):
        #este metodo se encarga de cargar los datos desde el archivo y almacenarlos en el contenedor self.patients
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.patients = json.load(file)
        else:
            self.patients = []

    def save_data(self):
        #guarda los datos actuales del contenedor en el archivo
        with open(self.data_file, 'w') as file:
            json.dump(self.patients, file, indent=4)

    def add_patient(self, patient:dict): 
        #añade un paciente nuevo a la lista si no existe otro con el mismo ID
        #guarda los datos y devuelve un true si el paciente fue añadido y un false si no lo fue
        if not any(p['id'] == patient['id'] for p in self.patients):
            self.patients.append(patient)
            self.save_data()
            return True
        return False

    def delete_patient(self, patient_id:str):
        #elimina un paciente por su ID
        #retorna 1 si el paciente se elimino y 0 si el paciente no se encontro
        initLen = len(self.patients)
        self.patients = [p for p in self.patients if p['id'] != patient_id]
        self.save_data()
        if initLen == len(self.patients):
            return 0
        else:
            return 1

    def get_patient_by_id(self, patient_id):
        #Busca un paciente por su ID y lo devuelve si lo encuentra, de lo contrario, devuelve None.
        for patient in self.patients:
            if patient['id'] == patient_id:
                return patient
        return None

    def search_patients(self, query):
        #Busca pacientes cuyos nombres comiencen con la cadena de consulta query.
        #lo que hace es filtrar la lista de pacientes y devolver solo aquellos cuyos nombres comiencen con la cadena proporcionada.
        results = []
        for patient in self.patients:
            if patient['nombre'].lower().startswith(query.lower()):
                results.append(patient)
        return results
class UserModel:
    #se encarga de manejar la logica relacionada con el usuario
    def __init__(self, users_file = 'usuarios.json'):
        #inicializa la clase con el archivo json que contiene la informacion de los pacientes y carga la informacion con el metodo load data
        self.users_file = users_file
        self.load()
        
    def load(self):
        #Carga los datos desde el archivo y los almacena en el contenedor self.users
        #Si el archivo no se encuentra, inicializa self.users como una lista vacía y muestra un mensaje.
        try:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []
            print("No se encontró información")

    def exists(self, user:str, pw:str):
        #Verifica si existe un usuario con el nombre de usuario y la contraseña proporcionados
        try:
            for i in self.users:
                if i['usuario'] == user and i['contrasena'] == pw:
                    return (1, f'{user} bienvenido') #si coinciden
            return 0
        except TypeError:
            return 2 #otro tipo de error 