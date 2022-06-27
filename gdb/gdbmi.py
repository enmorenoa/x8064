import os
from pprint import pprint
import subprocess
import Edition_text.text_Edition as text_Edition
from pygdbmi import *
from pygdbmi.gdbcontroller import GdbController
import pygdbmi


class gdb():
    def __init__(self):
        self.gdb = GdbController()
        self.tty = "" 
        self.terminal = ""
        self.gdb.time_to_check_for_additional_output_sec = 1
        self.texts = text_Edition.text()
        self.mode32bits = False
        self.variables = {}
        self.open_terminal()
        #self.get_pid_terminal()
        self.compilation=''
        self.response = ""

    def open_terminal(self):
        os.system("xterm -e 'gdbserver --multi localhost:4343' &")
        pass

    def check_terminal(self, interface):
        response = self.gdb.write('target extended-remote localhost:4343')
        msg = 'ps ax | grep gdb'
        resp = subprocess.getoutput(msg)
        resp = resp.split('\n')
        pts = ""
        for line in resp:
            if "Ss" in line:
                pts = line
        if (len(pts.split())) > 1:
            pts = pts.split()[1]
            self.tty = "/dev/"+pts
            self.get_pid_terminal()
        else:
            interface.show_message_dependencies()    
        
    def get_pid_terminal(self):
        self.terminal = subprocess.getoutput('ps -ft '+self.tty)
        self.terminal = self.terminal.split()
        for a in self.terminal:
            if a.isdigit():
                self.terminal = a
                break

    def kill_terminal(self):
        os.system("kill -9 "+self.terminal)

    def change_terminal(self, number):
        self.tty = "/dev/pts/"+str(number)
        self.gdb.write("-inferior-tty-set "+self.tty)
        self.get_pid_terminal()
    
    def open_file(self, file, text_code, interface): 
        self.texts.read_code_file(file, text_code)

    def compile_file(self, file, interface, texts):
        texts.save_file(file, interface.text_code)
        res = ""
        if self.mode32bits:   
            comp = 'gcc -m32 -gstabs+ '+self.compilation+' '+file+' '+' -o '+file[:-2]
            res = subprocess.getoutput(comp)
        else: 
            comp = 'gcc -gstabs+ '+self.compilation+' '+file+' '+' -o '+file[:-2]
            res = subprocess.getoutput(comp)
        if len(res) > 0: 
            if "warning" in res:
                interface.show_message_warning(res)
                interface.show_message_success()
                interface.isCompiled = True
                return True
            elif "Aviso:" in res and "Error" not in res: 
                interface.show_message_warning(res)
                interface.show_message_success()
                interface.isCompiled = True
                return True
            elif "Error" in res:
                interface.show_message_error(res)
                return False
            elif "error" in res:
                interface.show_message_error(res)
                return False
        else:
            interface.show_message_success()
            interface.isCompiled = True
            return True

    def add_information_execution(self, interface):
        self.texts.put_information_execution(self.response, interface.archive, interface)
        if interface.hexadecimal:
            if self.mode32bits == True: self.texts.addValuesToRegisters_32_hex(self, interface)
            if self.mode32bits == False: self.texts.addValuesToRegisters_64_hex(self, interface)
        else:
            if self.mode32bits == True: self.texts.addValuesToRegisters_32_dec(self, interface)
            if self.mode32bits == False: self.texts.addValuesToRegisters_64_dec(self, interface)
        if interface.variablesG:
            self.texts.show_global_variables(self, interface)

    def start_archive(self, file, interface):
        self.gdb.write('kill')
        self.delete_global_variables()
        self.response = self.gdb.write('set remote exec-file '+str(file[:-2]))
        self.response = self.gdb.write('-file-exec-and-symbols '+str(file[:-2]))
        self.response = self.gdb.write('-break-insert main')            
        self.response = self.gdb.write('-exec-run', raise_error_on_timeout=False, timeout_sec=60)
        self.gdb.write("record")

    def next_instruction(self, interface): 
        self.response = self.gdb.write("-exec-next", raise_error_on_timeout=False, timeout_sec=60)
        self.add_information_execution(interface)
        self.texts.check_program_finish(self.response, interface)
        return self.response

    def reverse_instruction(self, interface): 
        self.response = self.gdb.write('-exec-next --reverse', raise_error_on_timeout=False, timeout_sec=60)
        self.add_information_execution(interface)
        return self.response

    def continue_execution(self, interface): 
        self.response = self.gdb.write("-exec-continue", raise_error_on_timeout=False, timeout_sec=60)
        self.add_information_execution(interface)
        if self.texts.check_continue_stop_break(self.response):
            interface.show_reached_break()
        else:
            self.texts.check_program_finish(self.response, interface)
            self.next_instruction(interface)
        return self.response
        
    def stop_program(self): return self.gdb.write("kill")

    def activate_mode_32_bits(self): 
        if self.mode32bits == False: 
            self.mode32bits = True

    def activate_mode_64_bits(self): 
        if self.mode32bits == True: 
            self.mode32bits = False

    def get_mode_execution(self):
        return self.mode32bits
            
    def show_variable_value(self, variable): return self.gdb.write("p "+variable, raise_error_on_timeout=False, timeout_sec=60)     

    def set_a_breakpoint(self, line): return self.gdb.write("-break-insert "+line, raise_error_on_timeout=False, timeout_sec=60)
    
    def delete_a_breakpoint(self, line): return self.gdb.write("-break-delete "+line, raise_error_on_timeout=False, timeout_sec=60)

    def delete_all_breakpoints(self): return self.gdb.write("delete", raise_error_on_timeout=False, timeout_sec=60)

    def delete_global_variables(self): return self.variables.clear()

    def show_registers_general(self): return self.gdb.write("info reg", raise_error_on_timeout=False, timeout_sec=60)

    def show_registers_dec(self): return self.gdb.write("p/d $al")

    def show_variables(self): return self.gdb.write("info variables")

    def show_arguments_code(self): return self.gdb.write("info args")

    def show_local_variables(self): return self.gdb.write("info local")

    def show_info_stack_1(self): return self.gdb.write("info frame")

    def show_info_stack_2(self): return self.gdb.write("info stack")

    def show_info_state_memory(self): return self.gdb.write("info proc mappings")
    
    def show_list_breakpoints(self): return self.gdb.write("-break-list")
        
    def exit_gdb(self): return self.gdb.exit()
