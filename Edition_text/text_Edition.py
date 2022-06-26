from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import QtCore

class text():
    def __init__(self):
        self.exec_code = ""
        self.index = 0

    def newFileText(self, interface):
        self.clear_all_registers(interface)
        interface.text_code.setPlainText("")
        self.lines_of_exec = 0

    def read_code_file(self, file, text_code):
        with open(file[:-2]+".s", 'rt') as f:
            contenido = f.read()
            text_code.setPlainText(contenido)
    
    def read_execution_code(self, file):
        with open(file[:-2]+".s", 'rt') as f:
                contenido = f.readlines()
        return contenido    

    def save_file(self, file, text_code):
         with open(file, 'wt') as f:
            f.write(text_code.toPlainText()) 

    def get_information_of_response(self, response):
        info = ""
        for i in range(0, len(response), 1):
            dicc = response[i]
            dato = str(dicc['payload']) 
            dato = dato.replace("\\n","")
            dato = dato.replace("\\t","")
            if i>0 and i<len(response)-1:
               info += dato+"\n"
        return info

    def search_line_exec_code(self, response):
        dicc = response[len(response)-1]
        dato2 = ""
        dato = dicc["payload"]

        if "frame" not in dato:
            return self.index+1
        else:
            dato = dato['frame']
            if "line" not in dato:
                return self.index+1
            else:
                dato = dato['line']
                self.index = int(dato)-1
        return self.index

    def put_information_execution(self, response, file, interface):
        if interface.variablesG:
            exec_text = interface.text_ejec_code_2
        else:
            exec_text = interface.text_ejec_code   
        info = ""; i = 0; exec_text.setPlainText(""); enc = False
        index = self.search_line_exec_code(response)
        text = self.read_execution_code(file)
        for line in text:
            line = line.replace("\n","")
            if i != index:
                exec_text.appendPlainText(line)
            else:
                exec_text.appendHtml("<font color = 'yellow'>"+line+"</font>")
                
            i+=1
        exec_text.verticalScrollBar().setValue(index-10)  
       
    def set_global_variables(self, execut, variable, command, interface):
        execut.variables[variable] = command
        self.show_global_variables(execut, interface)
        interface.show_variables_updated()

    def show_global_variables(self, execut, interface):
        keys = execut.variables.keys()
        interface.text_variables.setPlainText("")
        del_keys = []
        s = ""
        for key in keys:
            resp = execut.show_variable_value(execut.variables[key])
            resp = resp[1]['payload']
            if "No symbol" in resp:
                interface.show_variable_not_found()
                del_keys.append(key)
            else: 
                resp = resp.split('=')[1] 
                resp = resp.replace("\n","")
                s += key+" : "+resp+" \n"
        for key in del_keys:
            execut.variables.pop(key)
        interface.text_variables.appendPlainText(s)

    def list_breakpoints(self, gdb):
        breakpoints = ""
        response = gdb.show_list_breakpoints()
        response = response[0];response = response['payload'];response = response['BreakpointTable'];response = response['body']
        for i in range(0, len(response), 1):
            res = response[i]
            breakpoints += "Número de breakpoint: " +res['number']+"\n"
            breakpoints += "Linea: " +res['line']+"\n"
            breakpoints += "Linea en fichero: " +res['original-location']+"\n"
            breakpoints += "\n"
        return breakpoints
            
    def addValuesToRegisters_32_hex(self, gdb, interface):
        respuesta = gdb.show_registers_general()
        enc1 = False
        for i in range(1, len(respuesta), 1):
            dicc = respuesta[i]
            dato = str(dicc['payload'])
            d = dato.split()
            j=0
            if d[0] == 'eax' or d[0] == 'cs':
                if interface.variablesG: 
                    interface.regsV2[d[j]].setText(d[j+1])
                else:
                    interface.regsV1[d[j]].setText(d[j+1])
                enc1 = True
            if enc1 == True:
                if interface.variablesG: 
                    interface.regsV2[d[j]].setText(d[j+1])
                else:
                    interface.regsV1[d[j]].setText(d[j+1])
                if d[j] == 'eip' or d[j] == 'es':
                    enc1 = False

    def addValuesToRegisters_64_hex(self, gdb, interface):
        respuesta = gdb.show_registers_general()
        enc1 = False
        for i in range(1, len(respuesta), 1):
            dicc = respuesta[i]
            dato = str(dicc['payload'])
            d = dato.split()
            j=0
            if d[0] == 'rax' or d[0] == 'cs': 
                enc1 = True
            if enc1 == True:
                d1=d[j]; d2 =d[j]; d2 = d2[1:]; d2 = 'e'+d2; mitad = int(len(d[j+1])/2)
                if interface.variablesG:
                    interface.regsV2[d1].setText(d[j+1][:mitad])
                    interface.regsV2[d2].setText(d[j+1][mitad:])
                    if d1 == 'cs' or d1 == 'ds' or d1 == 'es' or d1 == 'ss':
                        interface.regsV2[d1].setText(d[j+1])
                else:
                    interface.regsV1[d1].setText(d[j+1][:mitad])
                    interface.regsV1[d2].setText(d[j+1][mitad:])
                    if d[0] == 'cs' or d[0] == 'ds' or d[0] == 'es' or d[0] == 'ss':
                        interface.regsV1[d1].setText(d[j+1])
                if d[j] == 'rip' or d[j] == 'es':
                    enc1 = False

    def addValuesToRegisters_32_dec(self, gdb, interface):
        respuesta = gdb.show_registers_general()
        enc1 = False
        for i in range(1, len(respuesta), 1):
            dicc = respuesta[i]
            dato = str(dicc['payload'])
            d = dato.split()
            j=0
            if d[0] == 'eax' or d[0] == 'cs':
                if interface.variablesG: 
                    interface.regsV2[d[j]].setText(d[j+2].replace("\n",""))
                else:
                    interface.regsV1[d[j]].setText(d[j+2].replace("\n",""))
                enc1 = True
            if enc1 == True:
                if interface.variablesG: 
                    interface.regsV2[d[j]].setText(d[j+2].replace("\n",""))
                else:
                    interface.regsV1[d[j]].setText(d[j+2].replace("\n",""))
                if d[j] == 'eip' or d[j] == 'es':
                    enc1 = False

    def addValuesToRegisters_64_dec(self, gdb, interface):
        respuesta = gdb.show_registers_general()
        enc1 = False
        for i in range(1, len(respuesta), 1):
            dicc = respuesta[i]
            dato = str(dicc['payload'])
            d = dato.split()
            j=0
            if d[0] == 'rax' or d[0] == 'cs': 
                enc1 = True
            if enc1 == True:
                d1=d[j]; d2 =d[j]; d2 = d2[1:]; d2 = 'e'+d2; mitad = int(len(d[j+1])/2)
                if interface.variablesG:
                    interface.regsV2[d1].setText(d[j+2][:mitad].replace("\n",""))
                    interface.regsV2[d2].setText(d[j+2][mitad:].replace("\n",""))
                    if d1 == 'cs' or d1 == 'ds' or d1 == 'es' or d1 == 'ss':
                        interface.regsV2[d1].setText(d[j+1])
                else:
                    interface.regsV1[d1].setText(d[j+2][:mitad].replace("\n",""))
                    interface.regsV1[d2].setText(d[j+2][mitad:].replace("\n",""))
                    if d1 == 'cs' or d1 == 'ds' or d1 == 'es' or d1 == 'ss':
                        interface.regsV1[d1].setText(d[j+1])

                if d[j] == 'rip' or d[j] == 'es':
                    enc1 = False
    
    def clear_all_registers(self, interface):
        for i in interface.regsV2: interface.regsV2[i].setText("")
        for i in interface.regsV1: interface.regsV1[i].setText("")

    def check_program_finish(self, response, interface):
        resp = response[len(response)-1]
        resp = resp['payload']
        if "msg" in resp:
            resp = resp['msg']
            if "programa inferior detenido" in resp:
                interface.show_finish_program()
    
    def check_continue_stop_break(self, response):
        resp = response[len(response)-1]['payload']
        if "reason" in resp:
            resp = resp["reason"]
            if resp == "breakpoint-hit":
                return True

    def find_word(self, interface):
        p = interface.text_code.palette()
        q = QColor()
        q.setRgb(46, 52, 54)
        p.setColor(QtGui.QPalette.Highlight, q)
        interface.text_code.setPalette(p)
        h = interface.text_code.toPlainText()
        interface.text_code.setPlainText(h)
        d, ok = QInputDialog.getText(interface, 'Búsqueda de texto', 'Indica la palabra o frase a buscar:')
        if ok and len(d)>0: 
            pattern = d 
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
            cursor = interface.text_code.textCursor()
            regex = QtCore.QRegExp(pattern)
            # Process the displayed document
            pos = 0
            index = regex.indexIn(interface.text_code.toPlainText(), pos)
            while (index != -1):
                # Select the matched text and apply the desired format
                cursor.setPosition(index)
                cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
                cursor.mergeCharFormat(format)
                # Move to the next match
                pos = index + regex.matchedLength()
                index = regex.indexIn(interface.text_code.toPlainText(), pos)

