from modelo import *
#Estas clases se encargan de manejar la lógica de negocio y de interacción con los modelos correspondientes 
class UserController:
    def __init__(self, user_model:object = UserModel()):
        #Inicializa la clase con una instancia del modelo UserModel
        self.user_model = user_model #permite que el controlador pueda interactuar con el modelo
        
    def log_in(self, username:str, password:str):
        #Llama al método exists del modelo de usuario (UserModel) para verificar si el usuario y la contraseña proporcionados son correctos
        result = self.user_model.exists(username, password)
        return result 
    
class PatientController:
    def __init__(self, pac_model = PatientModel()):
        #Inicializa la clase con una instancia del modelo PatientModel
        self.pac_model = pac_model

    def newPac(self, data:dict):
        #Llama al método add_patient del modelo de pacientes (PatientModel) para añadir un nuevo paciente con los datos proporcionados
        return self.pac_model.add_patient(data) #True si se añadio 
    
    def getPac(self, initName:str = ''):
        #Llama al método search_patients del PatientModel para buscar pacientes cuyos nombres comiencen con la cadena proporcionada
        #Devuelve la lista de pacientes encontrados
        return self.pac_model.search_patients(initName)
    
    def delPac(self, id:str):
        #Llama al método delete_patient del modelo de pacientes (PatientModel) para eliminar un paciente con el ID proporcionado
        return self.pac_model.delete_patient(id) #1 si se elimino 0 si no se encontro