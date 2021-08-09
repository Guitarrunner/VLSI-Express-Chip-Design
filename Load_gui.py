
from tkinter.ttk import Progressbar
from tkinter import *


# Interface
class Gui:
    def __init__(self,root):
        self.root = root
        '''
        # Gets the requested values of the height and widht.
        self.windowWidth = root.winfo_reqwidth()
        self.windowHeight = root.winfo_reqheight()
        print("Width",self.windowWidth,"Height",self.windowHeight)
        
        # Gets both half the screen width/height and window width/height
        self.positionRight = int(root.winfo_screenwidth()/2 - self.windowWidth/2)
        self.positionDown = int(root.winfo_screenheight()/2 - self.windowHeight/2)
        
        # Positions the window in the center of the page.
        
        self.root.geometry("+{}+{}".format(self.positionRight, self.positionDown)) '''
        self.root.geometry("720x380")

        self.background_image=PhotoImage(file = 'Background/GREEN.png')
        self.background_label = Label(master=root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = self.background_image

        self.root.overrideredirect(1)

        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
        self.progress=Progressbar(root,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=720,mode='determinate')

        self.progress.place(x=0,y=360)

        ######## Label
        
        self.l1=Label(root,text='VLSI Express Chip Design',fg='white',bg='#4A4C4B')
        lst1=('Calibri (Body)',18,'bold')
        self.l1.config(font=lst1)
        self.l1.place(x=50,y=80)

        self.botton_icon = PhotoImage(file='icons/Start.png')
    
        #self.tool_bar = Button(self.shortcut_bar, image=botton_icon, command=cmd, )


        a='#249794'
        Frame(root,width=0,height=0,bg=a).place(x=0,y=0)  #249794
        self.b1=Button(root,image=self.botton_icon,command=self.bar,border=0,fg=a,bg='white')
        self.b1.pack(side='bottom', padx=0, pady=30)
        
        
    def new_win(self):
        print('perro1')
        root.destroy()
        import gui
        #q.mainloop()
        
    def bar(self):
        print('perro')
        l4=Label(root,text='Loading...',fg='white',bg='blue')
        lst4=('Calibri (Body)',10)
        l4.config(font=lst4)
        l4.place(x=18,y=210)
        
        import time
        r=0
        for i in range(100):
            self.progress['value']=r
            root.update_idletasks()
            time.sleep(0.03)
            r=r+1
        self.new_win()



root = Tk()
gui = Gui(root)
root.mainloop()