class PatientView:
    def display_patients(self, patients):
        print("-------")
        print("Buscar:")
        print("-------")
        for patient in patients:
            print("-----")
            print(patient)
            print("-----")

    def display_message(self, message):
        print("-----")
        print(message)
        print("-----")

    def get_patient_info(self):
        name = input("Ingresar nombre del paciente: ")
        last_name = input("Ingrese el apellido del paciente: ")
        age = input("Ingrese la edad del paciente: ")
        id_number = input("Ingrese el numero de identificacion del paciente:  ")
        return {'Nombre': name, 'Apellido': last_name, 'Edad': age, 'Id': id_number}

    def get_search_query(self):
        return input("Ingrese un término de búsqueda: ")

    def get_patient_id(self):
        return input("Ingrese el ID del paciente: ")

    def login(self):
        return input("Ingrese el usuario: "), input("Ingrese la contraseña: ")

    def logout(self):
        input("Presione enter para salir...")

    def show_login_screen(self):
        print("--------------------------------------------")
        print("Bienvenido al sistema manejador de pacientes")
        print("Porfavor ingresar:")

    def show_logout_screen(self):
        print("--------------------------")
        print("Ingresó satisfactoriamente")
        print("--------------------------")

    def show_main_menu(self):
        print("---------------")
        print("Menu Principal:")
        print("1. Agregar paciente")
        print("2. Borrar paciente")
        print("3. Buscar paciente")
        print("4. Salir")