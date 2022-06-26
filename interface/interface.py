from gdb import gdbmi
from Edition_text import text_Edition
from interface import dicc_of_regs, enum_To_TextEditors
from interface import variables_dialog
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import subprocess
import sys
import os

class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        app = os.path.abspath(os.getcwd()+"/interface/interfaz.ui")

        uic.loadUi(app, self)
        
        """ATRIBUTOS"""
        self.archive = ""
        self.directory = ""
        self.execut = gdbmi.gdb()
        self.editors = text_Edition.text()
        self.var_dialog = variables_dialog.global_var_dialog()
        self.listOfRegisters = self.findChildren(QLineEdit)
        self.regsV1 = dicc_of_regs.reg_dicc().get_dicc_of_regs_vista1(self)
        self.regsV2 = dicc_of_regs.reg_dicc().get_dicc_of_regs_vista2(self)
        self.setWindowIcon(QIcon(os.path.abspath(os.getcwd()+"/assert/icons/terminal.png")))
        self.mode_exect = ""
        self.start_program = False
        self.isCompiled = False
        self.menuEjecuci_n.setEnabled(False)
        self.menuPuntos_de_ruptura.setEnabled(False)
        self.variablesG = False
        self.hexadecimal = True
        self.variable_name = ""
        self.variable_type = ""

        """CONEXION DE LOS BOTONES"""
        self.botonN_2.clicked.connect(self.newFile)
        self.botonA_2.clicked.connect(self.openFile)
        self.botonG_2.clicked.connect(self.saveFile)
        self.botonE.clicked.connect(self.start_ejecution)
        self.botonNX.clicked.connect(self.next_line)
        self.botonNX_2.clicked.connect(self.next_line)
        self.botonC.clicked.connect(self.continue_execution)
        self.botonC_2.clicked.connect(self.continue_execution)
        self.boton32.clicked.connect(self.activate_32_bits)
        self.boton64.clicked.connect(self.activate_64_bits)
        self.boton_Comp.clicked.connect(self.compile_file)
        self.botonRestart.clicked.connect(self.restart_ejecution)
        self.botonRestart_2.clicked.connect(self.restart_ejecution)
        self.botonPararVolver.clicked.connect(self.stop_execution)
        self.botonPararVolver_2.clicked.connect(self.stop_execution)
        self.botonAtras.clicked.connect(self.reverse_line)
        self.botonAtras_2.clicked.connect(self.reverse_line)
        self.botonSetV.clicked.connect(self.set_global_variable)
        self.botonSetV_2.clicked.connect(self.set_global_variable)
        self.botonShowV.clicked.connect(self.show_global_variables)
        self.botonShowEjec.clicked.connect(self.show_execution_window)
        self.var_dialog.send.clicked.connect(self.get_variable_name_and_type_selected)
        self.var_dialog.cancel.clicked.connect(self.close_var_diag)

        """CONEXION DE LAS ACCIONES DEL MENU BAR"""
        self.actionNuevo_Archivo.triggered.connect(self.newFile)
        self.actionAbrir_archivo.triggered.connect(self.openFile)
        self.actionGuardar.triggered.connect(self.saveFile)
        self.actionGuardarComo.triggered.connect(self.saveFileAs)
        self.actionSalir_2.triggered.connect(self.exit_8086)
        self.actionEjecutar.triggered.connect(self.start_ejecution)
        self.actionSiguiente_l_nea.triggered.connect(self.next_line)
        self.actionContinuar.triggered.connect(self.continue_execution)
        self.actionDirectorio_de_proyectos.triggered.connect(self.change_directory)
        self.actionModo_32_bits_2.triggered.connect(self.activate_32_bits)
        self.actionModo_64_bits_2.triggered.connect(self.activate_64_bits)
        self.actionPoner_punto_de_ruptura.triggered.connect(self.set_breakpoint)
        self.actionEliminar_punto_de_ruptura.triggered.connect(self.delete_breakpoint)
        self.actionEliminar_todos_los_puntos_de_ruptura.triggered.connect(self.delete_all_breakpoints)
        self.actionMostrar_puntos_de_rupturas_actuales.triggered.connect(self.list_breakpoints)
        self.actionVer_c_digos_ascii_2.triggered.connect(self.show_ascii_codes)
        self.actionVista_c_digo.triggered.connect(self.show_code_window)
        self.actionVista_ejecuci_n.triggered.connect(self.show_execution_window)
        self.actionCortar.triggered.connect(self.text_code.cut)
        self.actionCopiar.triggered.connect(self.text_code.copy)
        self.actionPegar.triggered.connect(self.text_code.paste)
        self.actionSeleccionar_todo.triggered.connect(self.text_code.selectAll)
        self.actionDeshacer.triggered.connect(self.text_code.undo)
        self.actionRehacer.triggered.connect(self.text_code.redo) 
        self.actionB_squeda.triggered.connect(self.find_word)
        self.actionCambiar_modo_de_ejecuci_n_por_defecto.triggered.connect(self.change_mode_execution)
        self.actionRetroceder_l_nea.triggered.connect(self.reverse_line)
        self.action_Reiniciar.triggered.connect(self.restart_ejecution)
        self.actionParar_y_volver_al_c_digo.triggered.connect(self.stop_execution)
        self.actionOpciones_de_compilaci_n.triggered.connect(self.compilation_options)
        self.actionLimpiar_las_opciones_a_adidas.triggered.connect(self.clean_option_compilation)
        self.actionMostrar_Registros_en_decimal.triggered.connect(self.set_registers_to_decimal)
        self.actionMostrar_Registros_en_hexadecimal.triggered.connect(self.set_registers_to_hexadecimal)
        self.actionRestaurar_configuraci_n_por_defecto.triggered.connect(self.set_configuration_default)

        """HACER QUE LOS TEXTOS TENGAN NUMERACION"""  
        self.text_code.lineNumberArea = enum_To_TextEditors.LineNumberArea(self)
        self.text_ejec_code.lineNumberArea = enum_To_TextEditors.LineNumberAreaExec(self)
        self.text_ejec_code_2.lineNumberArea = enum_To_TextEditors.LineNumberAreaExec_2(self)

        self.text_code.updateRequest.connect(self.text_code.lineNumberArea.updateLineNumberArea)
        self.text_ejec_code.updateRequest.connect(self.text_ejec_code.lineNumberArea.updateLineNumberAreaExec)
        self.text_ejec_code_2.updateRequest.connect(self.text_ejec_code_2.lineNumberArea.updateLineNumberAreaExec)

        self.text_ejec_code.lineNumberArea.updateLineNumberAreaWidthExec()
        self.text_ejec_code_2.lineNumberArea.updateLineNumberAreaWidthExec()
        self.text_code.lineNumberArea.updateLineNumberAreaWidth()

        """PONER TODOS LOS ELEMENTOS NECESARIOS EN MODO LECTURA"""
        self.mode_read_only()
        self.load_configuration()
        self.show_code_window()        

    """EVENTOS"""
    def mode_read_only(self):
        self.text_ejec_code.setReadOnly(True)
        self.text_ejec_code_2.setReadOnly(True)
        self.text_variables.setReadOnly(True)
        [reg.setReadOnly(True) for reg in self.listOfRegisters]

    def load_configuration(self):
        with open(os.getcwd()+"/Configuration/Configuration.txt", 'rt') as f:
            direct = f.readline(); direct = direct.replace("\n", "").split(" ")
            if direct[1] == "DEFAULT":
                self.directory = os.path.abspath(os.getcwd()+"/code_proyects/")
            else:
                self.directory = direct[1]
            exec = f.readline(); exec = exec.replace("\n", "").split(" ")
            self.mode_exect = exec[1]
            if exec[1] == "32": self.activate_32_bits()
            elif exec[1] == "64": self.activate_64_bits()

    def disable_botons(self):
        self.botonNX.setEnabled(False)
        self.botonAtras.setEnabled(False)
        self.botonC.setEnabled(False)
        self.botonSetV.setEnabled(False)
        self.botonNX_2.setEnabled(False)
        self.botonAtras_2.setEnabled(False)
        self.botonC_2.setEnabled(False)
        self.botonSetV_2.setEnabled(False)

    def activate_botons(self):
        self.botonNX.setEnabled(True)
        self.botonAtras.setEnabled(True)
        self.botonC.setEnabled(True)
        self.botonSetV.setEnabled(True)
        self.botonNX_2.setEnabled(True)
        self.botonAtras_2.setEnabled(True)
        self.botonC_2.setEnabled(True)
        self.botonSetV_2.setEnabled(True)

    def get_variable_name_and_type_selected(self):
        self.var_dialog.close()
        resp = ""
        type_selected = self.var_dialog.type_var.currentText()
        self.variable_name = self.var_dialog.variables.text()
        self.variable_size = self.var_dialog.size_var.text()
        if(len(self.variable_name)>0):
            if type_selected == "int":
                resp = "(int) "+self.variable_name
            elif type_selected == "char":
                resp = "(char) "+self.variable_name
            elif type_selected == "vector_de_enteros":
                resp = "(int["+str(self.variable_size)+"]) "+self.variable_name
            elif type_selected == "cadena_de_texto":
                resp = "(char["+str(self.variable_size)+"]) "+self.variable_name 
            self.editors.set_global_variables(self.execut, self.variable_name, resp, self)
            self.var_dialog.variables.setText("")
            self.var_dialog.size_var.setText("")
            self.var_dialog.size_var.setReadOnly(True)
            self.var_dialog.variables.setReadOnly(True)
            self.var_dialog.type_var.setCurrentIndex(4)
        else:
            self.show_diag_error()

    def newFile(self):
        self.actionVista_ejecuci_n.setEnabled(False)
        self.menuEjecuci_n.setEnabled(False)
        self.menuPuntos_de_ruptura.setEnabled(False)
        self.execut.stop_program()
        self.editors.newFileText(self)
        self.archive = ""
        self.variablesG = False
        self.show_code_window()
        self.show_new_file_message()
    
    def openFile(self):
        self.actionVista_ejecuci_n.setEnabled(False)
        self.menuEjecuci_n.setEnabled(False)
        self.menuPuntos_de_ruptura.setEnabled(False)
        self.execut.stop_program()
        self.execut.delete_all_breakpoints()
        self.isCompiled = False
        filetypes = "Archivos de código (*.c *.s);;Todos los archivos(*.*)"
        archive = QFileDialog.getOpenFileName(self, 'Abrir archivo', self.directory, filetypes)
        if archive[0]:
            self.archive = archive[0]
            self.execut.open_file(self.archive, self.text_code, self)
            self.show_code_window()

    def saveFile(self):
        if len(self.archive)>0: 
            self.editors.save_file(self.archive, self.text_code)
        else: 
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        archive, _ = QFileDialog.getSaveFileName(self, 'Guardar archivo...', self.directory)
        if len(archive)>0:
            self.archive = archive
            self.editors.save_file(self.archive, self.text_code)

    def compile_file(self):
        if len(self.archive) > 0: 
            self.saveFile()
            return self.execut.compile_file(self.archive, self, self.editors)

    def start_ejecution(self): 
        if self.isCompiled:
            self.variablesG = False 
            self.editors.clear_all_registers(self)
            self.execut.delete_all_breakpoints()
            self.execut.start_archive(self.archive, self)
            self.actionVista_ejecuci_n.setEnabled(True)
            self.menuEjecuci_n.setEnabled(True)
            self.menuPuntos_de_ruptura.setEnabled(True)
            self.show_execution_window()
            self.execut.add_information_execution(self)
            self.isCompiled = False
            self.editors.start_finish = False
            self.activate_botons()
        else:
            if self.compile_file(): 
                self.start_ejecution()

    def restart_ejecution(self):
        self.variablesG = False
        self.editors.clear_all_registers(self)
        self.execut.delete_all_breakpoints()
        self.execut.start_archive(self.archive, self)
        self.actionVista_ejecuci_n.setEnabled(True)
        self.menuEjecuci_n.setEnabled(True)
        self.menuPuntos_de_ruptura.setEnabled(True)
        self.editors.start_finish = False
        self.show_execution_window()
        self.execut.add_information_execution(self)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ejecución')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('El programa ha sido reiniciado.')
        reply = msgBox.exec()
        self.activate_botons()

    def next_line(self):
        self.execut.next_instruction(self)

    def reverse_line(self):
        self.execut.reverse_instruction(self)

    def continue_execution(self):
        self.execut.continue_execution(self)

    def stop_execution(self):
        self.execut.delete_all_breakpoints()
        self.execut.stop_program()
        self.show_code_window()
        self.actionVista_ejecuci_n.setEnabled(False)
        self.menuEjecuci_n.setEnabled(False)
        self.menuPuntos_de_ruptura.setEnabled(False)
        self.show_code_window()       

    def activate_32_bits(self):
        self.boton32.setEnabled(False)
        self.boton64.setEnabled(True)
        self.execut.activate_mode_32_bits()
        if self.start_program:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Modo de ejecución')
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('EJECUCIÓN EN MODO 32-BITS')
            reply = msgBox.exec()

    def activate_64_bits(self):
        self.boton32.setEnabled(True)
        self.boton64.setEnabled(False)
        self.execut.activate_mode_64_bits()
        if self.start_program:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Modo de ejecución')
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('EJECUCIÓN EN MODO 64-BITS')
            reply = msgBox.exec()

    def change_mode_execution(self):
        d, ok = QInputDialog.getText(self, 'Tipo de arquitectura', 'Opción "32" para establecer 32 bits y Opción "64" para establecer 64 bits:')
        if ok and len(d)>0: 
            self.mode_exect = d
            with open("./Configuration/Configuration.txt", 'wt') as f:
                f.write("DIRECTORIO: " + self.directory + "\n")
                f.write("EXECUTION: " + self.mode_exect + "\n")

    def compilation_options(self):
        d, ok = QInputDialog.getText(self, 'Opciones de compilación', 'Añadir la nueva opción para compilar los ficheros, ej: -fPie')
        if ok and len(d)>0:
            self.execut.compilation += " "+d+" "  

    def close_var_diag(self):
        self.var_dialog.close()

    def set_configuration_default(self):
        with open("./Configuration/Configuration.txt", 'wt') as f:
            f.write("DIRECTORIO: DEFAULT\n")
            f.write("EXECUTION: 32\n" )
        self.show_configuration_default()

    def set_breakpoint(self):
        d, ok = QInputDialog.getText(self, 'Puntos de ruptura', 'Linea para establecer el nuevo punto de ruptura:')
        if ok and len(d)>0: 
            self.execut.set_a_breakpoint(d)
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Punto de ruptura')
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText('Punto de ruptura establecido en la linea '+d+' .')
            reply = msgBox.exec()

    def delete_breakpoint(self):
        number = ""
        d, ok = QInputDialog.getText(self, 'Puntos de ruptura', 'Número de breakpoint que se desea eliminar:')
        if ok and len(d) > 0: 
            number = d
            self.execut.delete_a_breakpoint(number)
            self.show_break_deleted(number)

    def delete_all_breakpoints(self):
        self.execut.delete_all_breakpoints()
        self.show_all_breaks_deleted()
    
    def list_breakpoints(self):
        breakpoints = self.editors.list_breakpoints(self.execut)
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Punto de ruptura')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Puntos de ruptura actuales: \n'+breakpoints)
        reply = msgBox.exec()

    def find_word(self):
        self.editors.find_word(self)

    def clean_option_compilation(self):
        self.execut.compilation = ""
        self.show_option_comp_clean()

    def resizeEvent(self, event):
        cr = self.contentsRect()
        self.text_code.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))
        self.text_ejec_code.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))
        self.text_ejec_code_2.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))

    def change_directory(self):
        self.directory = QFileDialog.getExistingDirectory(self, "Cambiar directorio", self.directory)
        if len(self.directory) > 0:
            with open("./Configuration/Configuration.txt", 'wt') as f:
                f.write("DIRECTORIO: " + self.directory + "\n")
                f.write("EXECUTION: " + self.mode_exect + "\n")
            self.show_directory_changed()

    def set_global_variable(self):
        self.var_dialog.show()

    def set_registers_to_decimal(self):
        self.hexadecimal = False
        self.execut.add_information_execution(self)
        self.show_registers()

    def show_variable_not_found(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Variables Globales')
        msgBox.setIcon(QMessageBox.Warning)        
        msgBox.setText('Variable introducida no encontrada.')
        reply = msgBox.exec()  

    def show_variables_updated(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Variables Globales')
        msgBox.setIcon(QMessageBox.Information)        
        msgBox.setText('Las variables globales han sido actualizadas.')
        reply = msgBox.exec()              

    def show_option_comp_clean(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Opciones de compilación')
        msgBox.setIcon(QMessageBox.Warning)        
        msgBox.setText('Se han eliminado todas las opciones de compilación establecidas.')
        reply = msgBox.exec()

    def set_registers_to_hexadecimal(self):
        self.hexadecimal = True
        self.execut.add_information_execution(self)
        self.show_registers()

    def show_diag_error(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Variables Globales')
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText('Introduce un nombre de variable válido.')
        reply = msgBox.exec()        

    def show_registers(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Consola Entrada/Salida')
        msgBox.setIcon(QMessageBox.Warning)
        if self.hexadecimal:
            msgBox.setText('Se han cambiado los registros a hexadecimal.')
        else:
            msgBox.setText('Se han cambiado los registros a decimal.')
        reply = msgBox.exec()

    def show_configuration_default(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Configuración')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Se ha restablecido la configuración por defecto.')
        reply = msgBox.exec() 

    def show_console_changed(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Consola Entrada/Salida')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Se ha cambiado a la consola con identificador '+self.execut.tty+' .')
        reply = msgBox.exec()         

    def show_directory_changed(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Directorio de trabajo')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Se ha cambiado el directorio de proyectos cuya nueva ruta es '+self.directory+" .")
        reply = msgBox.exec()        

    def show_reached_break(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ejecución')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Se ha alcanzado un punto de ruptura.')
        reply = msgBox.exec()

    def show_new_file_message(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Nuevo archivo')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Iniciado nuevo archivo.')
        reply = msgBox.exec()
    
    def show_break_deleted(self, number):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Puntos de ruptura')
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText('Punto de ruptura número '+number+' eliminado.')
        reply = msgBox.exec()

    def show_all_breaks_deleted(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Puntos de ruptura')
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText('Todos los puntos de ruptura han sido eliminados.')
        reply = msgBox.exec()

    def show_global_variables(self):
        self.variablesG = True
        self.show_global_variables_window()
        self.execut.add_information_execution(self)

    def show_global_variables_window(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_code_window(self):
        self.stackedWidget.setCurrentIndex(1)
        self.actionVista_ejecuci_n.setEnabled(False)   

    def show_message_dependencies(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('x8064')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Se le recuerda al usuario que para que el programa funcione correctamente, es necesario instalar las dependencias primero.')
        reply = msgBox.exec()

    def show_execution_window(self):
        self.variablesG = False
        self.execut.add_information_execution(self)
        self.stackedWidget.setCurrentIndex(0)

    def show_ascii_codes(self):
        pix = QPixmap(); pix.load(os.path.abspath(os.getcwd()+"/assert/image_codes_ascii/ascii_codes.png"))
        item = QtWidgets.QGraphicsPixmapItem(pix); scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.graphicsView.showMaximized(); self.graphicsView.setScene(scene)
        self.stackedWidget.setCurrentIndex(2)

    def show_finish_program(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Fin de ejecución')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('EL PROGRAMA HA FINALIZADO.')
        reply = msgBox.exec()
        self.execut.stop_program()
        self.disable_botons()

    def show_message_error(self, res):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Error')
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText('Error: \n'+res)
        reply = msgBox.exec()

    def show_message_warning(self, res):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Warning')
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText('Warning: \n'+res)
        reply = msgBox.exec()  

    def show_message_success(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Compilación')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Programa compilado con éxito.')
        reply = msgBox.exec()

    def show_message_execution(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Modo de ejecución')
        msgBox.setIcon(QMessageBox.Information)
        mode = ""
        if self.execut.get_mode_execution(): mode = "Modo de ejecución: Ensamblador 32 bits"
        else: mode = "Modo de ejecución: Ensamblador 64 bits"
        msgBox.setText('EJECUCIÓN ACTUAL: \n'+mode)
        reply = msgBox.exec()
        self.start_program = True
        self.execut.check_terminal(self)

    def get_interface_object(self):
        return self

    def kill_terminal(self):
        self.execut.kill_terminal()

    def close_variablesG(self):
        self.var_dialog.close()

    def exit_8086(self):
        self.execut.exit_gdb()
        self.close()

class Main():
    def __init__(self):
        self.GUI = ""

    def main(self):
        app = QApplication(sys.argv)
        self.GUI = Interface()
        self.GUI.show()
        self.GUI.show_message_execution()
        app.aboutToQuit.connect(self.killAll)
        sys.exit(app.exec_())

    def killAll(self):
       self.GUI.close_variablesG()
       self.GUI.kill_terminal()
    
    

