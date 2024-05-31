from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from controlador import UserController, PatientController

import sys

class Login(QDialog):
    def __init__(self):
        #Inicializa la clase, carga la interfaz de usuario desde un archivo .ui y crea una instancia de UserController.
        super().__init__()
        loadUi('login.ui', self)
        self.userController = UserController()
        self.setWindowFlags(Qt.FramelessWindowHint) #Configura la ventana para que no tenga bordes
        self.setup() #Metodo que configura las instancias y la interfaz
        
    def setup(self):
        #Conecta los botones de la interfaz a sus respectivos métodos
        self.salir_2.clicked.connect(self.saliendo)  
        self.minimizar.clicked.connect(self.minimizator)
        self.ingreso.clicked.connect(self.login)  
        self.pw.setEchoMode(QLineEdit.Password) #configura el campo pw para que oculte la contraseña (puntos)
        
    def login(self):
        #Obtiene el nombre de usuario y la contraseña de los campos de entrada.
        usuario = self.user.text()
        password = self.pw.text()
        #Verifica las credenciales llamando al método log_in del UserController.
        existe = self.userController.log_in(usuario, password)
        if isinstance(existe, tuple):
            #Si las credenciales son correctas, muestra la ventana de PatientView y cierra la ventana de inicio de sesión.+
            self.PatientView = PatientView()
            self.PatientView.show()
            self.close()
            
        elif existe == 0:
            #si no existe muestra un mensaje 
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No existe un usuario con los datos ingresados")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    #Implementan la funcionalidad de arrastrar y minimizar la ventana
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def saliendo(self):
        sys.exit(app.exec_())   
        
    def minimizator(self):
        self.showMinimized()
        
        
class PatientView(QDialog):
    def __init__(self):
        #Inicializa la clase, carga la interfaz de usuario desde un archivo .ui y crea una instancia de PatientController
        super().__init__()
        loadUi('patient.ui', self)
        
        self.patientController = PatientController()
        self.setWindowFlags(Qt.FramelessWindowHint) #ventana sin bordes
        self.setup()
        
    def setup(self):
        #Configura los eventos y validadores para los campos de entrada
        #Conecta los botones a sus respectivos métodos
        validator = QtGui.QIntValidator(1, 9999999, self)
        self.salir_2.clicked.connect(self.saliendo)  
        self.minimizar.clicked.connect(self.minimizator)
        self.tableView.verticalHeader().setVisible(False) #Oculta el encabezado vertical de la tabla que contiene los indices de las filas
        self.ingreso.clicked.connect(self.newPatient)
        self.busqueda.clicked.connect(self.filterPatients)
        self.id.setValidator(validator)
        self.edad.setValidator(validator)
        self.readPatients()
        self.tableUpdate()
        #Llama a readPatients y tableUpdate para cargar y mostrar los datos iniciales
        
    def readPatients(self):
        #carga todos los pacientes.
        self.listaPaciente = self.patientController.getPac()
        
    def filterPatients(self):
        #filtra los pacientes basados en el texto de búsqueda y actualiza la tabla
        buscar = self.buscar.text()
        self.listaPaciente = self.patientController.getPac(buscar)
        self.tableUpdate()
        
    def newPatient(self):
        #Añade un nuevo paciente después de verificar que todos los campos estén completos
        id = self.id.text()
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        edad = self.edad.text()
        if not id or not nombre or not apellido or not edad:
            #Muestra un mensaje de advertencia si falta algún dato o si el ID ya existe.
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Debe ingresar todos los datos")
            msgBox.setWindowTitle('Datos faltantes')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            pac = {'id':id, 'nombre':nombre, 'apellido': apellido, 'edad': edad}
            isUnique = self.patientController.newPac(pac)
            if not isUnique:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("La id ya existe")
                msgBox.setWindowTitle('Id repetida')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            else:
                #Actualiza la tabla después de añadir un nuevo paciente.
                self.readPatients()
                self.tableUpdate()
                self.id.setText('')
                self.nombre.setText('')
                self.apellido.setText('')
                self.edad.setText('')
            
                        
    def tableUpdate(self):
        #Actualiza la tabla con los datos de los pacientes.
        self.tableView.setRowCount(len(self.listaPaciente)) 
        self.tableView.setColumnCount(5) # 5 siempre
        columnas = ["ID", "Nombre", "Apellido", "Edad", "Eliminar"]
        columnLayout = ['id','nombre','apellido','edad']
        self.tableView.setHorizontalHeaderLabels(columnas)
        for row, paciente in enumerate(self.listaPaciente):
            for column in range(4):
                item = QTableWidgetItem(paciente[columnLayout[column]])
                self.tableView.setItem(row, column, item)
            #Añade un botón "Borrar" en cada fila para eliminar pacientes.
            btn = QPushButton('Borrar', self)
            btn.clicked.connect(lambda ch, r=row: self.Eliminar(r))
            self.tableView.setCellWidget(row, 4, btn)
                
        self.tableView.setColumnWidth(0, 80)  
        self.tableView.setColumnWidth(1, 110)  
        self.tableView.setColumnWidth(2, 60)  
        self.tableView.setColumnWidth(3, 60)  
        self.tableView.setColumnWidth(4, 60)  

    def Eliminar(self, row):
        #Elimina un paciente basándose en el ID de la fila seleccionada
        id = self.tableView.item(row, 0).text()
        deleted = self.patientController.delPac(id)
        if not deleted:
            #Muestra un mensaje de advertencia si no se pudo eliminar el paciente
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        #Actualiza la tabla después de eliminar un paciente
        self.readPatients()
        self.tableUpdate()

    #Implementan la funcionalidad de arrastrar y minimizar la ventana 
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def saliendo(self):
        sys.exit(app.exec_())   
        
    def minimizator(self):
        self.showMinimized()
            
if __name__ == "__main__":
    #Crea y ejecuta la aplicación, mostrando la ventana de inicio de sesión
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
