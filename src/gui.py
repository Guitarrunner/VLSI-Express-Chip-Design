#IMPORTS
from sys import modules
from tkinter import *
from tkinter import Menu
from tkinter import filedialog

#GUI
root = Tk()
root.title("GUI Mark I")
root.geometry("900x700")

#Functions
def clear():
    text.delete(1.0,END)

def open_txt():
    text.delete(1.0,END)
    text_file = filedialog.askopenfilename(title="Open File")
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
    text_file = open("../temp.v",'w')
    text_file.write(text.get(1.0,END))
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
text = Text(root, width=20,height=15,font=("Helvetica",16));
text.pack(side=TOP, anchor=NW, pady=20, padx=30)
result = Text(root, width=20,height=15,font=("Helvetica",16));

clear_button = Button(root,text="Clear Screan",command=clear)
clear_button.pack(side=BOTTOM, pady=100)

open_button = Button(root,text="Open Text File",command=open_txt)
open_button.pack(side=BOTTOM)

save_button = Button(root,text="Save File",command=save_txt)
save_button.pack(side=BOTTOM)

syntesis_button = Button(root,text="Syntesis File",command=syntesis_txt)
syntesis_button.pack(side=BOTTOM)

#Main Loop
root.mainloop()
