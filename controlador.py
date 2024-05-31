from modelo import *

class UserController:
    def __init__(self, user_model:object = UserModel()):
        self.user_model = user_model
        
    def log_in(self, username:str, password:str):
        result = self.user_model.exists(username, password)
        return result
    
class PatientController:
    def __init__(self, pac_model = PatientModel()):
        self.vet_model = pac_model

    def newPac(self, data:dict):
        return self.vet_model.add_pac(data)
    
    def getPac(self, initName:str = ''):
        return self.vet_model.search_pacs(initName)
    
    def delPac(self, id:str):
        return self.vet_model.delete_pac(id)