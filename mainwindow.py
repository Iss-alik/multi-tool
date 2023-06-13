from tkinter import *
from tkinter import filedialog as fd
from creational.singleton import Singleton
from structural.facade import Start

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
        self.entery = Entry(width=50)
        self.entery.place(x= 50, y=60)

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

        #Format work section
        self.label = Label(text="Format")
        self.label.place(x=250, y=100)  

        self.format = BooleanVar(value=0)
        self.radio = Radiobutton(text = 'new', variable=self.format, value=0)
        self.radio.place(x= 250, y=120)

        self.radio= Radiobutton(text = 'old', variable=self.format, value=1)
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

        self.radio= Radiobutton(text = 'Nothing', variable=self.operation, value=3)
        self.radio.place(x= 50, y=240)

        #button to start 
        self.button = Button(self, text="Go", command=self.go_Multi)
        self.button.place(x= 50, y=280)

    def browse(self):
        radio = self.source.get()

        if(radio == 0):
            cur_direktory = fd.askdirectory()
            self.path = cur_direktory

        elif(radio == 1):
            cur_file = fd.askopenfilename()
            self.path = cur_file

    def go_Multi(self):
        go = Start(path=self.path, source=self.source.get(), format = self.format, 
        contrast= self.contrast.get(), sign= self.sign.get(), operation=self.operation.get())
        go.startMutli()

    
