import pygame as pg
import precode as pc
import random
from faker import Factory


class Box(pg.sprite.Sprite):
    def __init__(self, image, row, column, isBomb=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image,(int(700/10),int(700/10)))
        self.rect = self.image.get_rect()
        self.isBomb = isBomb 

    
    def setup():
        pass 

    def open():
        pass
    
    def flag():
        pass
    
class Map(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.row = 10
        self.column = 10
        self.boxGroup = pg.sprite.Group()
        self.boxArray = [[object for i in range(self.row)] for i in range(self.column)]
        self.createmap()

    def createmap(self):
        faker = Factory.create()
        for i in range(self.row):
            for j in range (self.column):
                # isBomb = random.choice([True, False])
                isBomb = faker.boolean(chance_of_getting_true = 20)
                box = Box("Images/facingDown.png", i, j, isBomb)
                box.rect.x += (i * int(700/10))
                box.rect.y += (j * int(700/10))
                self.boxGroup.add(box)
                self.boxArray[i][j] = box

    def draw(self, window):
        self.boxGroup.draw(window)
        self.boxGroup.update()

    def onClick(self, mousePos):
        for i in range(self.row):
            for j in range(self.column):
                box = self.boxArray[i][j]
                if box.rect.x < mousePos[0] and box.rect.right > mousePos[0]:
                    if box.rect.y < mousePos[1] and box.rect.bottom > mousePos[1]:
                        self.changeImage(box, i, j)

    def changeImage(self, box, i, j):
        if box.isBomb:
            box.image = pg.image.load("Images/bomb.png")
        else:
            box.image = pg.image.load("Images/0.png")
        box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
        box.rect = box.image.get_rect()
        box.rect.x += (i * int(700/10))
        box.rect.y += (j * int(700/10))


class Main():
    def __init__(self):
        pg.init()
        pg.display.set_caption("Minesweeper")
        screen_dim = [700 , 700]               
        self.window = pg.display.set_mode(screen_dim)
        self.fps = 100
        self.clock = pg.time.Clock()

        self.maping = Map()
        self.main()

    def restart(self):
        print("restarting...")
        self.maping = Map()

    def main(self):
        while True:    
            self.window.fill((200, 20, 20))

            self.maping.draw(self.window)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        exit()
                    if event.key == pg.K_r:
                        self.restart()
                if event.type == pg.MOUSEBUTTONDOWN: 
                    # print(pg.mouse.get_pos())
                    self.maping.onClick(pg.mouse.get_pos())
    
            pg.display.update()                 
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Main();