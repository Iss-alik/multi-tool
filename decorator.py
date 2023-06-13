from wand.image import Image #this libarary need to crop and read images
from PIL import Image as pil #from PIL library import Image to check black pixels

class Entity:
    def __init__(self, src):
        self.src = src

    def play(self):
        return self.sound

class Level(Entity):
    def __init__(self, img):
        self.img = img

    def invert(self):
        img_inverted=self.img #in this section load image and change chanels white and black  
        img_inverted.level(0.6, 0.5, gamma=1)
        return img_inverted

    def contrast(self):
        img_contrast = self.img 
        img_contrast.level(0.4, 1.0, gamma=1.3)
        return img_contrast