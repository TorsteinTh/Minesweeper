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
        self.row = row
        self.column = column
        self.isBomb = isBomb 
        self.sur = 0
        self.fliped = False
        self.flag = False
    
class Map(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.row = 10
        self.column = 10
        self.boxGroup = pg.sprite.Group()
        self.boxArray = [[object for i in range(self.row)] for i in range(self.column)]
        self.win = 0
        self.createmap()
        self.setSur()

    def createmap(self):
        faker = Factory.create()
        for i in range(self.row):
            for j in range (self.column):
                isBomb = faker.boolean(chance_of_getting_true = 10)
                if isBomb:
                    self.win += 1
                box = Box("Images/facingDown.png", i, j, isBomb)
                box.rect.x += (i * int(700/10))
                box.rect.y += (j * int(700/10))
                self.boxGroup.add(box)
                self.boxArray[i][j] = box

    def draw(self, window):
        self.boxGroup.draw(window)
        self.boxGroup.update()

    def findBox(self, mousePos):
        for i in range(self.row):
            for j in range(self.column):
                box = self.boxArray[i][j]
                if box.rect.x < mousePos[0] and box.rect.right > mousePos[0]:
                    if box.rect.y < mousePos[1] and box.rect.bottom > mousePos[1]:
                        return box

    def onClickLeft(self, mousePos):
        box = self.findBox(mousePos)
        if box:
            if not box.flag:
                self.changeImage(box)
            if box.sur == 0 and not box.flag:
                self.emptySur(box)
            if not box.flag:
                box.fliped = True

    def onClickRight(self, mousePos):
        box = self.findBox(mousePos)
        if box:
            if not box.fliped:
                if not box.flag:
                    self.flag(box)
                else:
                    self.unflag(box)
        
    def emptySur(self, box):
        for i in range(-1,2):
            for j in range(-1,2):
                rowing = box.row + i
                columning = box.column + j
                if rowing not in range(self.row):
                    continue
                if columning not in range(self.column):
                    continue
                tmpBox = self.boxArray[rowing][columning]

                if tmpBox is box: 
                    continue

                if tmpBox.isBomb == False and tmpBox.fliped == False and not tmpBox.flag:
                    self.changeImage(tmpBox)

                if tmpBox.sur == 0 and tmpBox.fliped == False and not tmpBox.flag:
                    tmpBox.fliped = True
                    self.emptySur(tmpBox)

                if tmpBox.fliped == False and not tmpBox.flag:
                    tmpBox.fliped = True

    def setSur(self):
        for i in range(self.row):
            for j in range(self.column):
                self.checkSur(self.boxArray[i][j])

    def checkSur(self, box):
        tmpSur = 0
        for i in range(-1,2):
            for j in range(-1,2):
                rowing = box.row + i
                columning = box.column + j
                if rowing not in range(self.row):
                    continue
                if columning not in range(self.column):
                    continue

                tmpBox = self.boxArray[rowing][columning]
                if tmpBox.isBomb:
                    tmpSur+=1
        box.sur = tmpSur

    def changeImage(self, box):
        if box.sur == 0:
            box.image = pg.image.load("Images/0.png")
        elif box.sur == 1:
            box.image = pg.image.load("Images/1.png")
        elif box.sur == 2:
            box.image = pg.image.load("Images/2.png")
        elif box.sur == 3:
            box.image = pg.image.load("Images/3.png")
        elif box.sur == 4:
            box.image = pg.image.load("Images/4.png")
        elif box.sur == 5:
            box.image = pg.image.load("Images/5.png")
        elif box.sur == 6:
            box.image = pg.image.load("Images/6.png")
        elif box.sur == 7:
            box.image = pg.image.load("Images/7.png")
        elif box.sur == 8:
            box.image = pg.image.load("Images/8.png")

        if box.isBomb:
            box.image = pg.image.load("Images/bomb.png")

        box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
        box.rect = box.image.get_rect()
        box.rect.x += (box.row * int(700/10))
        box.rect.y += (box.column * int(700/10))

    def flag(self, box):
        box.image = pg.image.load("Images/flagged.png")
        box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
        box.rect = box.image.get_rect()
        box.rect.x += (box.row * int(700/10))
        box.rect.y += (box.column * int(700/10))
        box.flag = True if not box.flag else False 

    def unflag(self, box):
            box.image = pg.image.load("Images/facingDown.png")
            box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
            box.rect = box.image.get_rect()
            box.rect.x += (box.row * int(700/10))
            box.rect.y += (box.column * int(700/10))
            box.flag = True if not box.flag else False 


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
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        self.maping.onClickLeft(pg.mouse.get_pos())
                    if mouse[2]:
                        self.maping.onClickRight(pg.mouse.get_pos())

            pg.display.update()                 
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Main();