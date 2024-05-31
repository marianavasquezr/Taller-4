from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from controlador import userController, PatientController

import sys

class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        self.userController = userController()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('imgs/hospital.png'))
        self.setup()
        
    def setup(self):
        self.salir_2.clicked.connect(self.saliendo)  
        self.minimizar.clicked.connect(self.minimizator)
        self.ingreso.clicked.connect(self.login)  
        self.pw.setEchoMode(QLineEdit.Password)
        
    def login(self):
        usuario = self.user.text()
        password = self.pw.text()
        existe = self.userController.log_in(usuario, password)
        if isinstance(existe, tuple):
            self.PatientView = PatientView()
            self.PatientView.show()
            self.close()
            
        elif existe == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No existe un usuario con los datos ingresados")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        
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
        super().__init__()
        loadUi('patient.ui', self)
        
        self.patientController = PatientController()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('imgs/hospital.png'))
        self.setup()
        
    def setup(self):
        validator = QtGui.QIntValidator(1, 9999999, self)
        self.salir_2.clicked.connect(self.saliendo)  
        self.minimizar.clicked.connect(self.minimizator)
        self.tableView.verticalHeader().setVisible(False)
        self.ingreso.clicked.connect(self.newPet)
        self.busqueda.clicked.connect(self.filterPatients)
        self.id.setValidator(validator)
        self.buscar.setValidator(validator)
        self.edad.setValidator(validator)
        self.readPatients()
        self.tableUpdate()
        
    def readPets(self):
        self.listaPaciente = self.PatientController.getPac()
        
    def filterPatients(self):
        buscar = self.buscar.text()
        self.listaPaciente = self.PatientController.getPac(buscar)
        self.tableUpdate()
        
    def newPatient(self):
        id = self.id.text()
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        edad = self.edad.text()
        if not id or not nombre or not apellido or not edad:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Debe ingresar todos los datos")
            msgBox.setWindowTitle('Datos faltantes')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            pac = {'id':id, 'nombre':nombre, 'apellido': apellido, 'edad': edad}
            isUnique = self.PatientController.newPac(pac)
            if not isUnique:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("La id ya existe")
                msgBox.setWindowTitle('Id repetida')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            else:
                self.readPacs()
                self.tableUpdate()
                self.id.setText('')
                self.nombre.setText('')
                self.raza.setText('')
                self.edad.setText('')
            
                        
    def tableUpdate(self):
        self.tableView.setRowCount(len(self.listaPaciente)) 
        self.tableView.setColumnCount(5) # 5 siempre
        columnas = ["ID", "Nombre", "Edad", "Apellido", "Eliminar"]
        columnLayout = ['id','nombre','edad','apellido']
        self.tableView.setHorizontalHeaderLabels(columnas)
        for row, paciente in enumerate(self.listaPaciente):
            for column in range(4):
                item = QTableWidgetItem(paciente[columnLayout[column]])
                self.tableView.setItem(row, column, item)
            
            btn = QPushButton('Borrar', self)
            btn.clicked.connect(lambda ch, r=row: self.Eliminar(r))
            self.tableView.setCellWidget(row, 4, btn)
                
        self.tableView.setColumnWidth(0, 80)  
        self.tableView.setColumnWidth(1, 110)  
        self.tableView.setColumnWidth(2, 60)  
        self.tableView.setColumnWidth(3, 60)  
        self.tableView.setColumnWidth(4, 60)  

    def Eliminar(self, row):
        id = self.tableView.item(row, 0).text()
        deleted = self.PatientController.delPac(id)
        if not deleted:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        self.readPac()
        self.tableUpdate()
    
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
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
