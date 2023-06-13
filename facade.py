import os
from wand.image import Image
from structural.decorator import *
from structural.adapter import *
import constants

class Start:

    def __init__(self, path, source, format, contrast, sign, operation):
        self.path = path
        self.source = source
        self.format = format
        self.contrast = contrast
        self.operation = operation
        self.sign = sign
    
    def startMutli(self):
        if(not self.source):
            file_list = os.listdir(self.path)
            for self.src in file_list:
                if( (self.src[-4:]==".jpg" or self.src[-4:]==".png") and self.src[:4]!="sign"):
                    
                    #full path to the file 
                    self.file = self.path + "/" + self.src

                    #convert to png
                    self.original = Image(filename=self.file)
                    self.edit_img = self.original.clone()
                    self.edit_img.format = 'png'

                    #comand contrast
                    if(self.contrast):
                        self.level = Level(self.edit_img)
                        self.edit_img = self.level.contrast()

                    operation = Operation(img = self.edit_img, comand= self.operation, src=self.src, format= self.format, sign = self.sign)
                    operation.operr()

        else:
            source_file = self.path

class Operation:
    def __init__(self,img,comand,src,format,sign):
        self.edit_img =img 
        self.comand = comand
        self.src =src
        self.format = format
        self.sign = sign 

        #create inverted image to next steps
        self.clone_img = self.edit_img.clone()
        self.level = Level(self.clone_img)
        self.inverted  = self.level.invert() 

    def operr(self):        
        command = self.comand

        #command slice 
        if(command == 0):
            if(self.src[0]=='w'):
                self.w_slice()
            else:
                self.clone_img_1 = self.edit_img.clone()
                self.clone_img_2 = self.edit_img.clone()
                self.slice()

        #command date
        elif(command == 1):
            pass

        #command square
        elif(command == 2):
            self.clone_img_1 = self.edit_img.clone()
            self.clone_img_2 = self.edit_img.clone()
            self.square()
    
    #function finding coordinets
    @staticmethod
    def go_to(check,x,y,cmd='slice'): 

        while(check[x,y].string<'srgb(250,250,250)'):
            x+=1
    
        while(check[x,y].string >='srgb(250,250,250)' or check[x,y+1].string >='srgb(250,250,250)' or check[x,y+2].string >='srgb(250,250,250)'):
            y-=1

        if(cmd == 'slice'):
            x-=15
            y-=18
        elif(cmd =='sign'):
            y-=12
        elif(cmd == 'square'):
            if(y>constants.MIN_H or y<0):
                y=0
            x-=5
        return x,y 
    
    #function croping picture to 3 strips 
    def slice(self):
        strips = [self.edit_img, self.clone_img_1, self.clone_img_2]
        
        x=80
        y=200

        for i in range(3):
            x,y = self.go_to(check=self.inverted,x=x,y=y)
            strips[i].crop(x,y,width=1858, height=405)
            if(i==0):
                 y=680
            elif(i==1):
               y=1120
            x=0

            #section of image saving 
            self.save = self.src[:-4] + " " + str(i) + '.png'
            self.img_save(to_save = strips[i])

    #function crop weekends strips
    def w_slice(self):
        x=80
        y=250
        x,y = self.go_to(check=self.inverted,x=x,y=y)
        self.edit_img.crop(x,y,width=1860, height=1280)

        self.save = self.src[:-4] + '.png'
        self.img_save(to_save = self.edit_img)
   
   #function change format of stip on square
    def square(self):
        self.w = int(self.clone_img_1.width / 2)
        self.h = self.clone_img_1.height

        x=5
        y=30

        x,y = self.go_to(check=self.inverted, x= x, y=y,cmd = 'square')

        self.clone_img_1.crop(x,y, width = self.w, height = self.h)

        x = self.w
        y = 30

        x,y = self.go_to(check=self.inverted, x= x, y=y, cmd = 'square')
        self.clone_img_2.crop(x,y, width = self.w, height = self.h)
        
        w1 = self.clone_img_1.width
        w2 = self.clone_img_2.width

        self.w_res = min(w1,w2)
        self.h_res = self.clone_img_1.height + self.clone_img_2.height

        self.cntrl_point = self.h
        if(self.w < constants.MIN_SQ_W):
            self.cntrl_point -= 15
            self.h_res -=15
        
        self.res = Image(width=self.w_res,height= self.h_res)
        self.res.composite(image=self.clone_img_1, left=0,top=0)
        self.res.composite(image=self.clone_img_2, left=0,top=self.cntrl_point)

        self.save = self.src[:-4] + '.png'
        self.img_save(to_save = self.res)   

    #function add sign to picture
    def add_sign(self,img="none"):
        if(self.format): #we have two version of sign old and new
            sign = Image(filename='sign.png')
        else:
            sign = Image(filename='sign_old.png') 

        self.clone_img = img.clone()
        self.level = Level(self.clone_img)
        self.inverted_sign  = self.level.invert() 

        x = 5
        y = 30

        x,y=self.go_to(check=self.inverted_sign,x=x,y=y,cmd ='sign')
        if(self.format): #new sign is higher than old on 5 pixels
            y-=5

        self.edit_img = img.composite(sign,x,y)

    def img_save(self, to_save):
        self.save = constants.RES + self.save 
        if(self.sign):
            self.add_sign(img= to_save)
        to_save.save(filename = self.save)