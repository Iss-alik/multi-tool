import os
from wand.image import Image
from structural.decorator import *
from structural.adapter import *
import constants
import datetime

class Start:

    def __init__(self, path, source, strip, contrast, sign, operation, date):
        self.path = path
        self.source = source
        self.strip = strip
        self.contrast = contrast
        self.operation = operation
        self.sign = sign
        self.date = date
    
    def startMutli(self):
        in_date = Operation()
        in_date.give_date(date = self.date)

        if(not self.source):
            file_list = os.listdir(self.path)
            file_list.sort()
            for self.src in file_list:
                if( (self.src[-4:]==".jpg" or self.src[-4:]==".png" or self.src[-4:]==".gif") and self.src[:4]!="sign"):
                    
                    #full path to the file 
                    self.file = self.path + "/" + self.src
                    self.pret_start()

                    operation = Operation(img = self.edit_img, comand= self.operation, src=self.src, strip= self.strip, sign = self.sign)
                    operation.operr()

        else:
            self.file = self.path

            self.pret_start()

            lst = self.file.split(sep="/")
            self.src = lst[-1]

            operation = Operation(img = self.edit_img, comand= self.operation, src=self.src, strip= self.strip, sign = self.sign)
            operation.operr()

    def pret_start(self):
        #convert to png
        self.original = Image(filename=self.file)
        self.edit_img = self.original.clone()
        self.edit_img.format = 'png'

        #comand contrast
        if(self.contrast):
            self.level = Level(self.edit_img)
            self.edit_img = self.level.contrast()
class Operation:
    
    cur_date = "nothing"

    def __init__(self,img = "none",comand = "none",src = "none",strip = "none",sign="none"):
        self.edit_img =img 
        self.comand = comand
        self.src =src
        self.strip = strip
        self.sign = sign 

        if(img != "none"):
            #create inverted image to next steps
            self.clone_lv = self.edit_img.clone()
            self.level = Level(self.clone_lv)
            self.inverted  = self.level.invert() 

    @classmethod
    def give_date(cls, date):
        Operation.cur_date = date
    
    def operr(self):        
        command = self.comand

        #command slice 
        if(command == 0):
            if(self.src[0]=='w'):
                self.clone_1 = self.edit_img.clone()
                self.w_slice()
            else:
                self.clone_1 = self.edit_img.clone()
                self.clone_2 = self.edit_img.clone()
                self.slice()

        #command date
        elif(command == 1):
            self.date()

        #command square
        elif(command == 2):
            self.clone_1 = self.edit_img.clone()
            self.clone_2 = self.edit_img.clone()
            self.square()

        #command acomics
        elif(command == 3 and self.strip):
            self.clone_1 = self.edit_img.clone()
            self.acomics()

        else:
            self.img_save(to_save=self.edit_img)
    
    #function finding coordinets
    @staticmethod
    def go_to(check,x,y,cmd='slice'): 

        while(check[x,y].string<'srgb(250,250,250)'):
            x+=1
    
        while( (check[x,y-1].string >= 'srgb(250,250,250)' or check[x+1,y-1].string >= 'srgb(250,250,250)' ) and y>0):
            y-=1

        if(cmd == 'slice'):
            x-=15
            y-=18
        elif(cmd =='sign_new'):
            y-=15
        elif(cmd == 'square'):
            y=0
            if(x>=5):
                x-=5
            else:
                x=0
        return x,y 
    
    #function croping picture to 3 strips 
    def slice(self):
        strips = [self.edit_img, self.clone_1, self.clone_2]
        
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
            self.img_save(to_save = strips[i], special_arg=True, i=i)

    #function crop weekends strips
    def w_slice(self):
        x=constants.W_GO_X
        y=constants.W_GO_Y
        x,y = self.go_to(check=self.inverted,x=x,y=y)
        self.edit_img.crop(x,y,width=1860, height=1280)

        self.img_save(to_save = self.edit_img)
   
   #function change format of stip on square
    def square(self):
        self.w = int(self.clone_1.width / 2)
        self.h = self.clone_1.height

        x=constants.GO_X
        y=constants.GO_Y

        x,y = self.go_to(check=self.inverted, x= x, y=y,cmd = 'square')

        self.clone_1.crop(x,y, width = self.w, height = self.h)

        x = self.w
        y = constants.GO_Y

        x,y = self.go_to(check=self.inverted, x= x, y=y, cmd = 'square')
        self.clone_2.crop(x,y, width = self.w, height = self.h)
        
        w1 = self.clone_1.width
        w2 = self.clone_2.width

        self.w_res = min(w1,w2)
        self.h_res = self.clone_1.height + self.clone_2.height

        self.cntrl_point = self.h
        if(self.w < constants.MIN_SQ_W):
            self.cntrl_point -= 15
            self.h_res -=15
        
        self.res = Image(width=self.w_res,height= self.h_res, background="white")
        self.res.composite(image=self.clone_2, left=0,top=self.cntrl_point)
        self.res.composite(image=self.clone_1, left=0,top=0)

        self.img_save(to_save = self.res)   

    #function add sign to picture
    def add_sign(self,img="none"):
        if(self.strip): #we have two version of sign old and new
            sign = Image(filename='sign.png')
        else:
            sign = Image(filename='sign_old.png') 

        self.clone_lv = img.clone()
        self.level = Level(self.clone_lv)
        self.inverted_sign  = self.level.invert() 

        x = constants.GO_X
        y = constants.GO_Y

        if(self.strip):
            x,y=self.go_to(check=self.inverted_sign,x=x,y=y,cmd ='sign_new')

        else:
            x,y=self.go_to(check=self.inverted_sign,x=x,y=y,cmd ='sign_old')
        
        if(self.strip):
            img.composite(sign,x,y)
            signed = img 
        else:
            w = img.width
            h = 200

            signed = Image(width = w, height= h, background="white")
            
            signed.composite(image=img, left=0,top = constants.SIGN_OLD_S + constants.SIGN_OLD_H - y)  
            signed.composite(image=sign, left=x,top = constants.SIGN_OLD_S)
        
        return (signed)

    #adopting new strips to acomics format
    def acomics(self):
        h = self.clone_1.height
        if(h<1000):
            self.clone_1.resize(constants.ACOM_X, constants.ACOM_Y)
        else:
            self.clone_1.resize(constants.ACOM_X, constants.ACOM_W_Y)
        self.sign = False
        self.img_save(to_save = self.clone_1)

    def img_save(self, to_save, special_arg = False, i=False):
        if(special_arg):
            self.save = self.src[:-4] + " " + str(i) + '.png'
        else:
            self.save = self.src[:-4] + '.png'
        self.save = constants.RES + self.save

        if(self.sign):
            to_save = self.add_sign(img= to_save)
        to_save.save(filename = self.save)

    def date(self):
        self.src = "pe" + Operation.cur_date +".png"
        self.img_save(to_save = self.edit_img)

        lst = Operation.cur_date.split(sep= "-")
        year = int(lst[0])
        month = int(lst[1])
        day = int(lst[2])

        D = datetime.date(year, month, day)
        delta = datetime.timedelta(days=1)
        D = D + delta

        year = str(D.year)
        month = self.add_zero(date = D.month)
        day = self.add_zero(date = D.day)
       
        Operation.cur_date = year + "-" + month + "-" + day

    @staticmethod
    def add_zero(date):
        if(date<10):
            date = "0" + str(date)
        return str(date)
#улучшить дату