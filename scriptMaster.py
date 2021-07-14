# Run command:  (INTERFACE) python3 scriptMaster.py -g
#               (TERMINAL) python3 scriptMaster.py sample10.v -l

# Imports
import os
from struct import pack
import vagrant
import sys
from tkinter import Menu
from tkinter import filedialog
import tkinter.messagebox
from pathlib import Path
from fabric.api import *
from tkinter import *

# Global Variables
options = ["-l","-f","-s","-d","-p","-o","-e","-g"]
PROGRAM_NAME = "VLSI"
file_name = None

# Functions
@task
def mytask(command):
    with hide('warnings'):
        run(command)

def createCommand(analysisType,fileName):
    switcher = {
                "-l": ["Style Linter","sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint"],
                "-f": ["Formatter","sudo verible/bazel-bin/verilog/tools/formatter/verible-verilog-format"],
                "-s": ["Parser","sudo verible/bazel-bin/verilog/tools/syntax/verible-verilog-syntax"],
                "-d": ["Lexical Diff","sudo verible/bazel-bin/verilog/tools/diff/verible-verilog-diff"],
                "-p": ["Verible project tool","sudo verible/bazel-bin/verilog/tools/proyect/verible-verilog-project"],
                "-o": ["Code Obfuscator","sudo verible/bazel-bin/verilog/tools/obfuscator/verible-verilog-obfuscate"],
                "-e": ["Source Code Indexer","sudo verible/bazel-bin/verilog/tools/kythe/verible-verilog-kythe-extractor"]
            }

    filePath = " /vagrant_data/utils/" + fileName
    commands = []

    # Command flow
    for analysis in analysisType:
        tool = switcher.get(analysis)
        commands.append([tool[0],tool[1] + filePath + " >> log.txt; cp log.txt /vagrant_data/"])
    return commands

def runCommand(commands):
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
            break
        else:
            execute(mytask,command[1])
    if(Path("log.txt").stat().st_size != 0):
        print("\n[INFO] Exiting Vagrant\n")
        print("[ERROR] The analysis failed at "+ command[0]+", check the log.txt for errors")

    else:
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

        # Summary of errors
        errorList = []
        for i in range(len(txt1)):
            if txt1[i][1] not in errorList:
                errorList.append(txt1[i][1])

        summary = []
        for error in errorList:
            tmp = 0
            for i in range(len(txt1)):
                if txt1[i][1] == error:
                    tmp += 1
            summary.append([tmp,error])

        open("summary.txt","w").close()
        f = open("summary.txt","a")
        for i in range(len(summary)):
            f.write("La regla '" + summary[i][1] + "' se está violando " + str(summary[i][0]) + " veces\n")
        f.close()

        #print("[INFO] Summary created")

        #Overwrite data in log.txt
        errorsCount = 0
        open("log.txt","w").close()
        f = open("log.txt","a")
        for i in range(len(txt1)):
            f.write(txt1[i][0] + txt1[i][1] + "\n")
            errorsCount += 1
        f.close()

        #print("[INFO] Log.txt updated")

        # Errors count
        if errorsCount != 0:
            print("[WARNING] "+ str(errorsCount)+" errors found\n")

# Interface
class Gui:
    def __init__(self,root):
        self.root = root
        self.root.title("VLSI")
        self.root.geometry("1180x670")

        self.new_file_icon = PhotoImage(file='icons/new_file.png')
        self.open_file_icon = PhotoImage(file='icons/open_file.png')
        self.save_file_icon = PhotoImage(file='icons/save.png')
        self.cut_icon = PhotoImage(file='icons/cut.png')
        self.copy_icon = PhotoImage(file='icons/copy.png')
        self.paste_icon = PhotoImage(file='icons/paste.png')
        self.undo_icon = PhotoImage(file='icons/undo.png')
        self.redo_icon = PhotoImage(file='icons/redo.png')
        self.run_icon = PhotoImage(file='icons/run.png')

        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left',
                            image=self.new_file_icon, underline=0, command=self.new_file)
        self.file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                            image=self.open_file_icon, underline=0, command=self.open_file)
        self.file_menu.add_command(label='Save', accelerator='Ctrl+S',
                            compound='left', image=self.save_file_icon, underline=0, command=self.save)
        self.file_menu.add_command(label='Run', accelerator='Ctrl+R',
                            compound='left', image=self.run_icon, underline=0, command=self.save)
        self.file_menu.add_command(
            label='Save as', accelerator='Shift+Ctrl+S', command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', accelerator='Alt+F4', command=self.exit_editor)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',
                            compound='left', image=self.undo_icon, command=self.undo)
        self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',
                            compound='left', image=self.redo_icon, command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X',
                            compound='left', image=self.cut_icon, command=self.cut)
        self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C',
                            compound='left', image=self.copy_icon, command=self.copy)
        self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V',
                            compound='left', image=self.paste_icon, command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Find', underline=0,
                            accelerator='Ctrl+F', command=self.find_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Select All', underline=7,
                            accelerator='Ctrl+A', command=self.select_all)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)


        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.show_line_number = IntVar()
        self.show_line_number.set(1)
        self.view_menu.add_checkbutton(label='Show Line Number', variable=self.show_line_number,
                                command=self.update_line_numbers)
        self.show_cursor_info = IntVar()
        self.show_cursor_info.set(1)
        self.view_menu.add_checkbutton(
            label='Show Cursor Location at Bottom', variable=self.show_cursor_info, command=self.show_cursor_info_bar)
        self.to_highlight_line = BooleanVar()
        self.view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1,
                                offvalue=0, variable=self.to_highlight_line, command=self.toggle_highlight)
        self.themes_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_cascade(label='Themes', menu=self.themes_menu)

        self.color_schemes = {
            'Default': '#000000.#FFFFFF',
            'Greygarious': '#83406A.#D1D4D1',
            'Aquamarine': '#5B8340.#D1E7E0',
            'Bold Beige': '#4B4620.#FFF0E1',
            'Cobalt Blue': '#ffffBB.#3333aa',
            'Olive Green': '#D1E7E0.#5B8340',
            'Night Mode': '#FFFFFF.#000000',
        }

        self.theme_choice = StringVar()
        self.theme_choice.set('Default')
        for k in sorted(self.color_schemes):
            self.themes_menu.add_radiobutton(
                label=k, variable=self.theme_choice, command=self.change_theme)
        self.menu_bar.add_cascade(label='View', menu=self.view_menu)

        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label='About', command=self.display_about_messagebox)
        self.about_menu.add_command(label='Help', command=self.display_help_messagebox)
        self.menu_bar.add_cascade(label='About',  menu=self.about_menu)
        self.root.config(menu=self.menu_bar)

        self.shortcut_bar = Frame(self.root,  height=25, background='DeepSkyBlue2')
        self.shortcut_bar.pack(expand='no', fill='x')

        icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
                'undo', 'redo', 'find_text', 'run')
        for i, icon in enumerate(icons):
            tool_bar_icon = PhotoImage(file='icons/{}.png'.format(icon))
            cmd = eval("self."+icon)
            self.tool_bar = Button(self.shortcut_bar, image=tool_bar_icon, command=cmd)
            self.tool_bar.image = tool_bar_icon
            self.tool_bar.pack(side='left')

        # Content text
        self.line_number_bar = Text(self.root, width=4, padx=3, takefocus=0,  border=0,
                            background='DarkOliveGreen1', state='disabled',  wrap='none')
        self.line_number_bar.pack(side='left',  fill='y')

        self.content_text = Text(self.root, wrap='word', undo=1)
        self.content_text.pack(side='left', ipadx= 100, expand='yes', fill='both')

        self.scroll_bar = Scrollbar(self.content_text)
        self.content_text.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.content_text.yview)
        self.scroll_bar.pack(side='right', fill='y')
        self.cursor_info_bar = Label(self.content_text, text='Line: 1 | Column: 1')
        self.cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

        self.content_text.bind('<KeyPress-F1>', self.display_help_messagebox)
        self.content_text.bind('<Control-N>', self.new_file)
        self.content_text.bind('<Control-n>', self.new_file)
        self.content_text.bind('<Control-O>', self.open_file)
        self.content_text.bind('<Control-o>', self.open_file)
        self.content_text.bind('<Control-R>', self.run)
        self.content_text.bind('<Control-r>', self.run)
        self.content_text.bind('<Control-S>', self.save)
        self.content_text.bind('<Control-s>', self.save)
        self.content_text.bind('<Control-f>', self.find_text)
        self.content_text.bind('<Control-F>', self.find_text)
        self.content_text.bind('<Control-A>', self.select_all)
        self.content_text.bind('<Control-a>', self.select_all)
        self.content_text.bind('<Control-y>', self.redo)
        self.content_text.bind('<Control-Y>', self.redo)
        self.content_text.bind('<Any-KeyPress>', self.on_content_changed)
        self.content_text.tag_configure('active_line', background='ivory2')

        # Result text
        self.result_text = Text(self.root, wrap='word', undo=1)
        self.result_text.pack(side='right', ipadx= 200, expand='yes', fill='both', padx=50)

        self.result_scroll_bar = Scrollbar(self.result_text)
        self.result_text.configure(yscrollcommand=self.result_scroll_bar.set)
        self.result_scroll_bar.config(command=self.result_text.yview)
        self.result_scroll_bar.pack(anchor='ne',fill='y', expand='yes')


        # set up the pop-up menu
        self.popup_menu = Menu(self.content_text)
        for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
            cmd = eval("self."+i)
            self.popup_menu.add_command(label=i, compound='left', command=cmd)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Select All', underline=7, command=self.select_all)
        self.content_text.bind('<Button-3>', self.show_popup_menu)


        # bind right mouse click to show pop up and set focus to text widget on launch
        self.content_text.bind('<Button-3>', self.show_popup_menu)
        self.content_text.focus_set()


    # show pop-up menu
    def show_popup_menu(self,event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)


    def show_cursor_info_bar(self):
        show_cursor_info_checked = self.show_cursor_info.get()
        if show_cursor_info_checked:
            self.cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
        else:
            self.cursor_info_bar.pack_forget()


    def update_cursor_info_bar(self,event=None):
        row, col = self.content_text.index(INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        self.cursor_info_bar.config(text=infotext)


    def change_theme(self,event=None):
        selected_theme = self.theme_choice.get()
        fg_bg_colors = self.color_schemes.get(selected_theme)
        foreground_color, background_color = fg_bg_colors.split('.')
        self.content_text.config(
            background=background_color, fg=foreground_color)
        self.result_text.config(
            background=background_color, fg=foreground_color)


    def update_line_numbers(self,event=None):
        self.line_numbers = self.get_line_numbers()
        self.line_number_bar.config(state='normal')
        self.line_number_bar.delete('1.0', 'end')
        self.line_number_bar.insert('1.0', self.line_numbers)
        self.line_number_bar.config(state='disabled')


    def highlight_line(self,interval=100):
        self.content_text.tag_remove("active_line", 1.0, "end")
        self.content_text.tag_add(
            "active_line", "insert linestart", "insert lineend+1c")
        self.content_text.after(interval, self.toggle_highlight)


    def undo_highlight(self):
        self.content_text.tag_remove("active_line", 1.0, "end")


    def toggle_highlight(self,event=None):
        if self.to_highlight_line.get():
            self.highlight_line()
        else:
            self.undo_highlight()


    def on_content_changed(self,event=None):
        self.update_line_numbers()
        self.update_cursor_info_bar()


    def get_line_numbers(self):
        output = ''
        if self.show_line_number.get():
            row, col = self.content_text.index("end").split('.')
            for i in range(1, int(row)):
                output += str(i) + '\n'
        return output


    def display_about_messagebox(self,event=None):
        tkinter.messagebox.showinfo(
            "About", "{}{}".format(PROGRAM_NAME, "\nText Editor GUI\nHackAnons\nhackanons@yahoo.com"))


    def display_help_messagebox(self,event=None):
        tkinter.messagebox.showinfo(
            "Help", "Help Book: \nText Editor GUI\nHackAnons\nhackanons@yahoo.com",
            icon='question')


    def exit_editor(self,event=None):
        if tkinter.messagebox.askokcancel("Quit?", "Do you want to QUIT for sure?\n Make sure you've saved your current work."):
            self.root.destroy()


    def new_file(self,event=None):
        self.root.title("Untitled")
        global file_name
        file_name = None
        self.content_text.delete(1.0, END)
        self.on_content_changed()

    def run(self,event=None):
        fileName = os.path.basename(file_name)
        command = createCommand(["-l"],fileName)
        runCommand(command)
        dataTreatment()
        with open("log.txt") as _file:
            self.result_text.insert(1.0, _file.read())
        self.on_content_changed()

    def open_file(self,event=None):
        input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            self.root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
            self.content_text.delete(1.0, END)
            with open(file_name) as _file:
                self.content_text.insert(1.0, _file.read())
            self.on_content_changed()


    def write_to_file(self,file_name):
        try:
            content = self.content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            tkinter.messagebox.showwarning("Save", "Could not save the file.")


    def save_as(self,event=None):
        input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if input_file_name:
            global file_name
            file_name = input_file_name
            self.write_to_file(file_name)
            self.root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        return "break"


    def save(self,event=None):
        global file_name
        if not file_name:
            self.save_as()
        else:
            self.write_to_file(file_name)
        return "break"


    def select_all(self,event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"


    def find_text(self,event=None):
        search_toplevel = Toplevel(self.root)
        search_toplevel.title('Find Text')
        search_toplevel.transient(self.root)

        Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')

        search_entry_widget = Entry(
            search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
            row=1, column=1, sticky='e', padx=2, pady=2)
        Button(search_toplevel, text="Find All", underline=0,
            command=lambda: self.search_output(
                search_entry_widget.get(), ignore_case_value.get(),
                self.content_text, search_toplevel, search_entry_widget)
            ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window(self):
        self.content_text.tag_remove('match', '1.0', END)
        self.search_toplevel.destroy()
        self.search_toplevel.protocol('WM_DELETE_WINDOW', self.close_search_window)
        return "break"

    def search_output(self,needle, if_ignore_case, content_text,
                    search_toplevel, search_box):
        content_text.tag_remove('match', '1.0', END)
        matches_found = 0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = content_text.search(needle, start_pos,
                                                nocase=if_ignore_case, stopindex=END)
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(needle))
                content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            content_text.tag_config(
                'match', foreground='red', background='yellow')
        search_box.focus_set()
        search_toplevel.title('{} matches found'.format(matches_found))


    def cut(self):
        self.content_text.event_generate("<<Cut>>")
        self.on_content_changed()
        return "break"


    def copy(self):
        self.content_text.event_generate("<<Copy>>")
        return "break"


    def paste(self):
        self.content_text.event_generate("<<Paste>>")
        self.on_content_changed()
        return "break"


    def undo(self):
        self.content_text.event_generate("<<Undo>>")
        self.on_content_changed()
        return "break"


    def redo(self,event=None):
        self.content_text.event_generate("<<Redo>>")
        self.on_content_changed()
        return 'break'

# Script
if sys.argv[1] == "-g":
    # Start Gui
    root = Tk()
    gui = Gui(root)
    root.mainloop()

elif sys.argv[1] == "-i":
    print("[INFO] You have just entered interactive mode")
    os.system("vagrant ssh")

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
            commands = createCommand(analysisType,fileName)
            runCommand(commands)
            dataTreatment()