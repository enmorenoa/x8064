from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os

class global_var_dialog(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        vars = os.path.abspath(os.getcwd()+"/interface/diag_variable.ui")
        uic.loadUi(vars, self)
        type_list = ["int","vector_de_enteros","char","cadena_de_texto","None"]
        self.type_var.addItems(type_list)
        self.type_var.setCurrentIndex(4)
        self.variables.setReadOnly(True)
        self.size_var.setReadOnly(True)
        self.type_selected = ""
        self.name_selected = "None"
        self.size_selected = "None"
        self.variables.setPlaceholderText("Selecciona primero un tipo correcto.")
        self.size_var.setPlaceholderText("Selecciona primero un tipo correcto.")
        """PONER AQUI LAS CONEXIONES DE LOS BOTONES"""
        self.type_var.currentIndexChanged.connect(self.get_type_selected)

    def get_type_selected(self):
        self.type_selected = self.type_var.currentText()
        if self.type_selected != "None":
            if self.type_selected == "int":
                self.variables.setPlaceholderText("Ej: num")
                self.size_var.setPlaceholderText("Para un entero no hay que especificar tamaño.")
            elif self.type_selected == "char":
                self.variables.setPlaceholderText("Ej: letra")
                self.size_var.setPlaceholderText("Para un único caracter no hay que especificar tamaño.")
            elif self.type_selected == "vector_de_enteros":
                self.variables.setPlaceholderText("Ej: vector")
                self.size_var.setPlaceholderText("Ej: 10, donde 10 es el número de elementos del vector.") 
            elif self.type_selected == "cadena_de_texto":
                self.variables.setPlaceholderText("Ej: cadena")
                self.size_var.setPlaceholderText("Ej: 22, donde 22 es el número de caracteres que tiene la cadena.")                
            self.variables.setReadOnly(False)
            if self.type_selected == "vector_de_enteros" or self.type_selected == "cadena_de_texto": 
                self.size_var.setReadOnly(False)
            else:
                self.size_var.setText("")
                self.size_var.setReadOnly(True)
        else:
            self.variables.setPlaceholderText("Selecciona primero un tipo correcto.")
            self.size_var.setPlaceholderText("Selecciona primero un tipo correcto.")


    