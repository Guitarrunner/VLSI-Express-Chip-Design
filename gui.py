#IMPORTS
#import os
import os
from sys import modules
from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from pathlib import Path

#GUI
root = Tk()
root.title("GUI Mark I")
root.geometry("1100x650")

#Functions
def clear():
    text.delete(1.0,END)

def open_txt():
    result.delete(1.0,END)
    text.delete(1.0,END)
    text_file = filedialog.askopenfilename(title="Open File")
    fileName = text_file
    ghost.insert(END,text_file) 
    print(text_file)
    modules = open(text_file,'r')
    text.insert(END,modules.read())
    modules.close()

def save_txt():
    #text_file = filedialog.askopenfilename(title="Open File")
    text_file = filedialog.asksaveasfilename(defaultextension=".v",title="Save File")
    text_file = open(text_file,'w')
    text_file.write(text.get(1.0,END))
    text_file.close()

def syntesis_txt():
    scriptLine = 'python run.py '
    fileName = ghost.get(1.0,END)
    head, tail = os.path.split(fileName)
    os.system(scriptLine+tail) 
    text_file= open("log.txt",'r')
    result.insert(END,text_file.read())
    text_file.close()

#Top Menu
menu = Menu(root)

menu_file = Menu(menu,tearoff=0)
menu_file.add_command(label="New File")
menu_file.add_command(label="Save")

menu_run = Menu(menu,tearoff=0)
menu_run.add_command(label="Run")

menu.add_cascade(label="File", menu=menu_file)
menu.add_cascade(label="Run", menu=menu_run)
root.config(menu=menu)

#Text Input
text = Text(root, width=30,height=20,font=("Helvetica",16));
text.grid(row=0,column=0,pady=20, padx=20)
result = Text(root, width=30,height=20,font=("Helvetica",16));
result.grid(row=0,column=5,pady=20)
ghost = Text (root,width=30, height=20,font=("Helvetica",16)); 

clear_button = Button(root,text="Clear Screen",command=clear)
clear_button.grid(row=5,column=1,pady=20)

open_button = Button(root,text="Open Text File",command=open_txt)
open_button.grid(row=5,column=2,pady=20)

save_button = Button(root,text="Save File",command=save_txt)
save_button.grid(row=5, column=3, pady=20)

syntesis_button = Button(root,text="Syntesis File",command=syntesis_txt)
syntesis_button.grid(row=5, column=4 , pady=20)


#Main Loop
root.mainloop()
