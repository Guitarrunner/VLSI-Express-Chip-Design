# Run command:  (INTERFACE) python3 scriptMaster.py -g
#               (TERMINAL) python3 scriptMaster.py sample10.v -l

# Imports
import os
from struct import pack
import vagrant
import sys
import os
from tkinter import Menu
from tkinter import filedialog
from pathlib import Path
from fabric.api import *
from tkinter import *

# Global Variables
options = ["-l","-f","-s","-d","-p","-o","-e","-g"]

# Functions
@task
def mytask(command):
    with hide('warnings'):
        run(command)

def runCommand(analysisType,fileName):
    switcher = {
                "-l": "sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint",
                "-f": "sudo verible/bazel-bin/verilog/tools/formatter/verible-verilog-format",
                "-s": "sudo verible/bazel-bin/verilog/tools/syntax/verible-verilog-syntax",
                "-d": "sudo verible/bazel-bin/verilog/tools/diff/verible-verilog-diff",
                "-p": "sudo verible/bazel-bin/verilog/tools/proyect/verible-verilog-project",
                "-o": "sudo verible/bazel-bin/verilog/tools/obfuscator/verible-verilog-obfuscate",
                "-e": "sudo verible/bazel-bin/verilog/tools/kythe/verible-verilog-kythe-extractor"
            }

    filePath = " /vagrant_data/utils/" + fileName
    commands = []

    # Command flow
    for analysis in analysisType:
        commands.append(switcher.get(analysis) + filePath + " >> log.txt; cp log.txt /vagrant_data/")

    # Vagrant connection
    print("[INFO] Starting Vagrant\n")
    v = vagrant.Vagrant()
    v.up()
    env.hosts = [v.user_hostname_port()]
    env.key_filename = v.keyfile()
    env.warn_only = True

    # Run work flow
    execute(mytask,"echo -n > log.txt; cp log.txt /vagrant_data/")
    for command in commands:
        if(Path("log.txt").stat().st_size != 0):
            print("\n[ERROR] The analysis failed at one point, check the log.txt for errors")
            break
        else:
            execute(mytask,command)
    print("\n[INFO] Exiting Vagrant\n")

def inputValidation():
    operations = []
    for i in range(2,len(sys.argv)):
        if sys.argv[i] not in options:
            print("[ERROR] The type of analysis " + sys.argv[i] + " does not correspond to a valid one.")
            return -1
        else:
            operations.append(sys.argv[i])
    return operations
    

def dataTreatment():
    # Data treatment
        txt = Path('log.txt').read_text()
        txt1=txt.split('\n')
        txt1=txt1[:-1]

        for i in range(len(txt1)):
            cutter_twopoint = txt1[i].find(":")
            txt1[i]=txt1[i][cutter_twopoint+1:]
            cutter_twopoint = txt1[i].find(": ")
            cutter_parenthesis = 0
            if txt1[i].find(" [") != -1:
                cutter_parenthesis =  txt1[i].find(" [")
            if txt1[i].find(" (syntax-error)")!=-1:
                cutter_parenthesis = txt1[i].find(" (syntax-error)")
            
            temp = txt1[i][cutter_twopoint+1:cutter_parenthesis]
            txt1[i]= [txt1[i][:cutter_twopoint],temp]

        # Update log.txt
        open("log.txt","w").close()
        f = open("log.txt","a")
        for i in range(len(txt1)):
            f.write(txt1[i][0] + txt1[i][1] + "\n")
        f.close()

# Interface
class Gui:
    def __init__(self,root):
        self.root = root
        self.root.title("VLSI")
        self.root.geometry("1180x670")

        # Text Input
        self.text = Text(root, width=30,height=20,font=("Helvetica",16));
        self.text.grid(row=0,column=0,pady=20, padx=20)
        self.result = Text(root, width=40,height=20,font=("Helvetica",16));
        self.result.grid(row=0,column=6,pady=20)
        self.ghost = Text (root,width=30, height=20,font=("Helvetica",16)); 

        # Buttons
        self.clear_button = Button(root,text="Clear Screen",command=self.clear)
        self.clear_button.grid(row=2,column=0,pady=20)

        self.open_button = Button(root,text="Open Text File",command=self.open_txt)
        self.open_button.grid(row=2,column=1,pady=20)

        self.save_button = Button(root,text="Save File",command=self.save_txt)
        self.save_button.grid(row=2, column=2, pady=20)

        self.syntesis_button = Button(root,text="Run",command=self.syntesis_txt)
        self.syntesis_button.grid(row=2, column=3 , pady=20)

    # Gui Functions
    def clear(self):
        self.text.delete(1.0,END)
        self.result.delete(1.0,END)

    def open_txt(self):
        self.result.delete(1.0,END)
        self.text.delete(1.0,END)
        text_file = filedialog.askopenfilename(title="Open File")
        fileName = text_file
        self.ghost.insert(END,text_file) 
        print(text_file)
        modules = open(text_file,'r')
        self.text.insert(END,modules.read())
        modules.close()

    def save_txt(self):
        #text_file = filedialog.askopenfilename(title="Open File")
        text_file = filedialog.asksaveasfilename(defaultextension=".v",title="Save File")
        text_file = open(text_file,'w')
        text_file.write(self.text.get(1.0,END))
        text_file.close()

    def syntesis_txt(self):
        fileName = self.ghost.get(1.0,END)
        head, tail = os.path.split(fileName)
        tail = tail[:-1]
        runCommand(["-l"],tail)

        dataTreatment()

        text_file= open("log.txt",'r')
        self.result.insert(END,text_file.read())
        text_file.close()

# Script
if sys.argv[1] == "-g":
    # Start Gui
    root = Tk()
    gui = Gui(root)
    root.mainloop()
elif sys.argv[1] == "-i":
    print("[INFO] Enter interactive mode")

else:
    # Validations from terminal
    if not(os.path.exists('./utils/'+sys.argv[1])):
        print("[ERROR] The indicated file cannot be found.")
    else:
        # Operations Validation
        analysisType = inputValidation()
        if analysisType != -1:

            # Command Preparation
            fileName = sys.argv[1]
            runCommand(analysisType,fileName)
            dataTreatment()