from tkinter import *
from tkinter import filedialog as fd
from creational.singleton import Singleton
from structural.facade import *

class Window(Tk, Singleton):
    def __init__(self):
        super().__init__()
    
        #Source document section
        self.source = BooleanVar(value=0)

        self.radio = Radiobutton(text = 'Folder', variable=self.source, value=0)
        self.radio.place(x= 50, y=20)

        self.radio= Radiobutton(text = 'File', variable=self.source, value=1)
        self.radio.place(x= 100, y=20)

        #Path section
        self.path = Entry(width=50)
        self.path.place(x= 50, y=60)

        self.button = Button(self, text="Browse", command=self.browse)
        self.button.place(x= 350, y=60)

        #Decorate section
        self.label = Label(text="Decoration")
        self.label.place(x=50, y=100)  

        self.contrast = IntVar(value=0)
        self.sign = IntVar(value=0)

        self.check = Checkbutton(self, text = 'contrast', variable=self.contrast)
        self.check.place(x= 50, y=120)

        self.check =Checkbutton(self, text = 'sign', variable=self.sign)
        self.check.place(x= 50, y=140)

        #Strip work section
        self.label = Label(text="Strip")
        self.label.place(x=250, y=100)  

        self.strip= BooleanVar(value=1)
        self.radio = Radiobutton(text = 'new', variable=self.strip, value=1)
        self.radio.place(x= 250, y=120)

        self.radio= Radiobutton(text = 'old', variable=self.strip, value=0)
        self.radio.place(x= 250, y=140)

        #Operation section
        self.label = Label(text="Operation")
        self.label.place(x=50, y=160)  

        self.operation = IntVar(value=0)

        self.radio = Radiobutton(text = 'Slice', variable=self.operation, value=0)
        self.radio.place(x= 50, y=180)

        self.radio= Radiobutton(text = 'Date', variable=self.operation, value=1)
        self.radio.place(x= 50, y=200)

        self.radio= Radiobutton(text = 'Square', variable=self.operation, value=2)
        self.radio.place(x= 50, y=220)

        self.radio= Radiobutton(text = 'acomics', variable=self.operation, value=3)
        self.radio.place(x= 50, y=240)

        self.radio= Radiobutton(text = 'Nothing', variable=self.operation, value=4)
        self.radio.place(x= 50, y=260)

        #Data section
        self.date = Entry(width=15)
        self.date.insert(0,"YYYY-MM-DD")
        self.date.place(x= 250, y=200)

        self.label = Label(text="Date")
        self.label.place(x=250, y=170)  

        #button to start 
        self.button = Button(self, text="Go", command=self.go_Multi)
        self.button.place(x= 50, y=300)

    def browse(self):
        radio = self.source.get()

        if(radio == 0):
            cur_direktory = fd.askdirectory()
            self.path.delete(first=0, last=END)
            self.path.insert(0,cur_direktory)

        elif(radio == 1):
            cur_file = fd.askopenfilename()
            self.path.delete(first=0, last=END)
            self.path.insert(0,cur_file)

    def go_Multi(self):
        go = Start(path=self.path.get(), source=self.source.get(), strip = self.strip.get(), 
        contrast= self.contrast.get(), sign= self.sign.get(), operation=self.operation.get(), date = self.date.get())
        go.startMutli()

    
