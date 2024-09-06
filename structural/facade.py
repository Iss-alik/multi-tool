import os
from wand.image import Image
from structural.decorator import *
import constants
import datetime

class Start:

    # Инициализация класса 
    def __init__(self, path, folder, format, contrast, sign, operation, date):
        self.path = path
        self.folder = folder
        self.format = format
        self.contrast = contrast
        self.operation = operation
        self.sign = sign
        self.date = date
    
    # Подготовка перед основыми работами 
    def pret_start(self):

        # Сначала конвертируем изображение в png
        self.original = Image(filename=self.file) # Создаём экзапляр класса Image который ялвяется частью wand
        self.edit_img = self.original.clone() # Делаем клона с которым дальше будет вестись основная работа 
        self.edit_img.format = 'png' # Меняем формат клона

        # Затем если стоит галочка на контраст то выполняется
        if(self.contrast):
            self.level = Level(self.edit_img) # Создаём экзампляр класса Level и отправляем сразу экзампляр класса Image
            self.edit_img = self.level.contrast() # Делаем операцию contrast (логика в decorator)

    # Основная логика здесь
    def start_multi(self):

        # Инициальзуертся экзампляр класса Operation() через который мы в переменую класса передадим начальную дату
        initial_date = Operation()
        initial_date.give_date(date = self.date) # С помощью функции give_date() отправляем дату с которой будет начинаться нумерация

        # Тип запуска для папки
        if(self.folder):

            # Источник отсылает к папке
            file_list = os.listdir(self.path)
            file_list.sort() # Сортируем что бы не было потом проблем с нумерацией 

            # Пробигаемся по всем файлам в папке
            for self.file_name in file_list:

                # Если он принадлжеит одному из этих типов то работаем
                if(self.file_name.endswith('jpg') or self.file_name.endswith('png') or self.file_name.endswith('gif')):
                    
                    # Прописываем полный путь к файлу, что бы wand не тупил в pret_start
                    self.file = self.path + "/" + self.file_name
                    self.pret_start()

                    operation = Operation(img = self.edit_img, command= self.operation, file_name=self.file_name, format= self.format, sign = self.sign)
                    operation.operr()

        # Тип запуска для одиночного файла
        else:

            # Путь сразу указывает на файл
            self.file = self.path

            self.pret_start()

            # Достаём имя файла 
            lst = self.file.split(sep="/")
            self.file_name = lst[-1]

            operation = Operation(img = self.edit_img, command= self.operation, file_name=self.file_name, format= self.format, sign = self.sign)
            operation.operr()

class Operation:
    # Переменая хронящая последнию дату 
    cur_date = "nothing"

    # Инициализация класса 
    def __init__(self,img = "none",command = "none",file_name = "none",format = "none",sign="none"):
        self.edit_img =img # edit_img - изображение отправленое на обработку
        self.command = command
        self.file_name =file_name
        self.format = format
        self.sign = sign 

        # Если было передано изображение тогда создаем "перевернутое" изображение 
        if(img != "none"):
            self.level = Level(self.edit_img) # Создаём экзампляр класса Level и отправляем сразу экзампляр класса Image
            self.inverted  = self.level.invert() # Делаем операцию invert (логика в decorator)

    @classmethod # Меняем переменую класса, присвоивая ей веденую дату 
    def give_date(cls, date):
        Operation.cur_date = date
    
    def operr(self):        
        command = self.command # Достаем команду из свойств экзампляра класса 

        # Режим стрипы
        if(command == 'slice'):

            # Если файл начинается на 'w' (weekend), то это воскресный стрип 
            if(self.file_name[0]=='w'):
                self.clone_1 = self.edit_img.clone() # Создаем клон с которым будем работать
                self.w_slice() # Используем функцию w_slice

            else:
                self.clone_1 = self.edit_img.clone() # Создаем три клона = три изображения с котрыми будем работать 
                self.clone_2 = self.edit_img.clone()
                self.clone_3 = self.edit_img.clone()
                self.slice() # Используем функцию slice

        # Раставляем даты
        elif(command == 'date'):
            self.date() # Используем функцию date

        # Режим на квадраты
        elif(command == 'square'):
            self.clone_1 = self.edit_img.clone() # Создаем клоны с которыми будем работать
            self.clone_2 = self.edit_img.clone()
            self.square() # Используем функцию square

        # Форматируем под формат акомикса
        elif(command == 'acomics' and self.format):
            self.clone_1 = self.edit_img.clone() # Создаем клон с которым будем работать
            self.acomics() # Используем функцию acomics

        # Если же ничего не выбрано, просто отпрявляем на сохранение edit_img
        else:
            self.img_save(to_save=self.edit_img)
    
    # Статистический метод определяющий высоту и ширину стрипа
    @staticmethod
    def w_and_h(inverte, x, y, weekend = False): # inverte - "перевернутое" изображение; x, y - кординаты левого верхнего угла стрипа
        marker = 0

        # Присваиваем маркеру ширину изображения, то есть перетаскивае маркер в правый конец изображения 
        marker = inverte.width - 2 #-2 что бы маркер была меньше ширины и не выдавло ошибок
        while(inverte[marker, y+10].string < constants.WHITE_PIXEL): # Двигаем маркер на лево пока не наткнемся на белый пискель
            marker-=2

        w = marker - x # отнимаем от полученого маркера начальную кооринату, получая тем самым ширину стрипа  

        # Если стрип не воскресный
        if(not weekend):
            h = int((inverte.height - 3*y)/3) # Примерно расчитываем высоту стрипа, отнимая от высоты изображения 
                # тройной пробел (растояние от стрипа до стрипа на странице книги, примерно равное растоянию от у=0 до первого стрипа)
                # а потом делим на три, потому что три стрипа
            
            marker = h + y +10 # Переносим маркер вниз на растояние равное сумме высоты стрипа, пробела и 10
            # то есть поподаем под первый стрип на картинке

            while (inverte[x+15, marker].string < constants.WHITE_PIXEL ): # Двигаем маркер в верх пока не наткнемся на белый пискель
                marker-=2
            h = marker - y # Отнимаем от полученого маркера начальную кооринату, получая тем самым высоту стрипа 

        # Если стрип воскресный
        else:
            marker = inverte.height # Отправляем маркер в почти самый вниз, что бы избежать нижней черной полосы 
            while( (inverte[x + 20, marker-1].string <= constants.WHITE_PIXEL ) and marker>0): # Двигаем маркер в верх пока не наткнемся на белый пискель
                marker-=3
            h = marker - y # Отнимаем от полученого маркера начальную кооринату, получая тем самым высоту стрипа 

        w+=30 # Плюсуем что бы невелировать возможные ошибки и просчеты
        h+=40
        return w,h # Возвращаем ширину и высоту стрипа

    # Статистический метод определяющий координаты левого верхнего угла стрипа
    @staticmethod
    def upper_left(inverte, mark_x, mark_y, x=0, y=0): # inverte - "перевернутое" изображение; x, y - начальные кординаты поиска

        while(inverte[x,mark_y].string < constants.WHITE_PIXEL): # Двигаем х на право пока не наткнемся на белый пискель
            x+=2
    
        # Двигаем у в вниз пока не наткнемся на белый пискель
        while(inverte[mark_x,y].string < constants.WHITE_PIXEL): 
            y+=2

        return x,y 
    
    # Метод разрезает картинку на 3 стрипа
    def slice(self):
        strips = [self.clone_1, self.clone_2, self.clone_3] # Массив хранящий клоны изображения отправленого на обработку
        
        mark_x = constants.GO_X # Задаем начальные координаты поиска для функции upper_left
        mark_y = constants.GO_Y

        x,y = self.upper_left(inverte = self.inverted, mark_x = mark_x, mark_y = mark_y) # Определяем координаты левого верхнего угла первого стрипа
        space = y # Пробел - растояние от стрипа до стрипа на странице книги, примерно равное растоянию от у=0 до первого стрипа
        w,h = self.w_and_h(inverte = self.inverted, x = x, y = y) # Высчитываем высоту и ширину стрипов на примере первого стрипа на странице

        for i in range(3):
            if(i != 0): # Мы уже нашли угол для первого стрипа когда считали высоту и ширину 
                x,y = self.upper_left(inverte = self.inverted, mark_x = mark_x, mark_y = mark_y, y = y) # Определяем координаты левого верхнего угла стрипа

            x-=15 # Поправка на ошибку 
            y-=20

            strips[i].crop(x,y,width=w, height=h) # Вырезаем прямоугольник верхний левый угол которого находится на координате (х,у)
            # а ширина и высота равны w и h
            
            # Меняем х и у для следующих upper_left
            if(i==0):
                mark_y= 2*space + h # 2*space + h примерно там находится левый верхний угол второго стрипа
                # Потом с помощью upper_left находим точную координату
                y = space + h
                
            elif(i==1): # Тоже самое только чуточку другая формула
               mark_y= int(strips[i+1].height - space - 0.7*h) # Что бы передвинуть маркер чуть ниже левого верхнего угла третьего стрипа
               y = strips[i+1].height - space - h
        
            # Отправляем изображение на сохранение
            self.img_save(to_save = strips[i], special_arg=True, i=i)

    # Метод разрезает картинку на один воскренсый стрип
    def w_slice(self):
        mark_x=constants.W_GO_X # Задаем начальные координаты поиска для функции upper_left
        mark_y=constants.W_GO_Y

        x,y = self.upper_left(inverte=self.inverted, mark_x = mark_x, mark_y = mark_y) # Определяем координаты левого верхнего угла стрипа
        w,h = self.w_and_h(inverte= self.inverted, x =x, y=y, weekend= True) # Определяем высоту и ширину стрипа

        x-=15 # Поправка на ошибку
        y-=20

        self.edit_img.crop(x,y,width=w, height=h) # Вырезаем прямоугольник верхний левый угол которого находится на координате (х,у)
         # а ширина и высота равны w и h

        self.img_save(to_save = self.edit_img) # Отправляем изображение на сохраниене 
   
    # Метод режит стрип на квадрат
    def square(self):        
        w = int(self.clone_1.width / 2) 
        h = self.clone_1.height

        mark_x=constants.GO_X
        mark_y=constants.GO_Y
        x,y = self.upper_left(inverte=self.inverted, mark_x= mark_x, mark_y= mark_y)


        self.clone_1.crop(x, 0, width = w, height = h)

        self.clone_2.crop(w, 0, width = w, height = h)

        self.level = Level(self.clone_2)
        inverted_clone_2 = self.level.invert()

        x, y = self.upper_left(inverte = inverted_clone_2, mark_x= mark_x, mark_y= mark_y)

        self.clone_2.crop(x,y, width = w, height = h)
        
        w1 = self.clone_1.width
        w2 = self.clone_2.width

        w_res = min(w1,w2)
        h_res = self.clone_1.height + self.clone_2.height

        cntrl_point = h
        
        res = Image(width=w_res + 5, height= h_res, background="white")
        res.composite(image=self.clone_2, left=5, top=cntrl_point)
        res.composite(image=self.clone_1, left=5, top=0)

        self.img_save(to_save = res)   

    #function add sign to picture
    def add_sign(self,img="none"):
        if(self.format): #we have two version of sign old and new
            sign = Image(filename='sign.png')
            sign_height = constants.SIGN_NEW_H
        else:
            sign = Image(filename='sign_old.png') 
            sign_height = constants.SIGN_OLD_H

        self.level = Level(img)
        self.inverted_sign  = self.level.invert() 

        mark_x = 150
        mark_y = 360


        x,y=self.upper_left(inverte=self.inverted_sign, mark_x= mark_x, mark_y= mark_y)
        if(y < sign_height):
            w = img.width
            h = img.height
            h += sign_height + constants.SIGN_SPACE

            #Молодец это уже другое дело 
            signed = Image(width = w, height= h, background="white")
            
            signed.composite(image=img, left=0,top = constants.SIGN_SPACE + sign_height - y )  
            signed.composite(image=sign, left=x,top = constants.SIGN_SPACE)

        
        else:
            y -= sign_height
            img.composite(sign,x,y)
            signed = img 
        
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
            self.save = self.file_name[:-4] + " " + str(i) + '.png'
        else:
            self.save = self.file_name[:-4] + '.png'
        self.save = constants.RES + self.save

        if(self.sign):
            to_save = self.add_sign(img= to_save)
        to_save.save(filename = self.save)

    def date(self):
        self.file_name = "pe" + Operation.cur_date +".png"
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
