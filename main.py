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
    
class MenuBox(pg.sprite.Sprite):
    def __init__(self, image, nr):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image,(int(240),int(150)))
        self.rect = self.image.get_rect()
        self.nr = nr

    
class Map(pg.sprite.Sprite): 
    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.screen = screen
        self.row = 10
        self.column = 10
        self.boxGroup = pg.sprite.Group()
        self.boxArray = [[object for i in range(self.row)] for i in range(self.column)]
        self.total = 0
        self.won = False
        self.lose = False
        self.createmap()
        self.setSur()

    def createmap(self):
        faker = Factory.create()
        for i in range(self.row):
            for j in range (self.column):
                isBomb = faker.boolean(chance_of_getting_true = 10)
                if isBomb:
                    self.total += 1
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
                self.flag(box)
        
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
            self.lose = True

        box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
        box.rect = box.image.get_rect()
        box.rect.x += (box.row * int(700/10))
        box.rect.y += (box.column * int(700/10))

    def flag(self, box):
        if box.flag:
            box.image = pg.image.load("Images/facingDown.png")
        else:
            box.image = pg.image.load("Images/flagged.png")
        box.image = pg.transform.scale(box.image,(int(700/10),int(700/10)))
        box.rect = box.image.get_rect()
        box.rect.x += (box.row * int(700/10))
        box.rect.y += (box.column * int(700/10))
        box.flag = True if not box.flag else False 

    def losing(self, x, y):
        font = pg.font.Font(None, 150)
        self.screen.blit(font.render("YOU LOSE", 20, (0, 0, 0)),(110 + x, 200 + y))
        fonte = pg.font.Font(None, 30)
        self.screen.blit(fonte.render("PRESS 'R' TO RESTART", 30, (0, 0, 0)),(260 + y, 360))
        self.screen.blit(fonte.render("PRESS 'Q' or 'Esc' TO QUIT", 30, (0, 0, 0)),(240 + x,390))

        pg.display.update()                 

    
    def winning(self, x, y):
        font = pg.font.Font(None, 150)
        self.screen.blit(font.render("YOU WON", 20, (255, 255, 0)),(110 + x, 200 + y))
        fonte = pg.font.Font(None, 30)
        self.screen.blit(fonte.render("PRESS 'R' TO RESTART", 30, (0, 0, 0)),(260 + y, 360))
        self.screen.blit(fonte.render("PRESS 'Q' or 'Esc' TO QUIT", 30, (0, 0, 0)),(240 + x,390))

        pg.display.update()  

    def unflipped(self):
        left = 0
        for i in range(self.row):
            for j in range(self.column):
                box = self.boxArray[i][j]
                if not box.fliped:
                    left += 1
        if left == self.total:
            self.won = True
    
    def drawBomb(self):
        for i in range(self.row):
            for j in range(self.column):
                box = self.boxArray[i][j]
                if box.isBomb:
                    self.changeImage(box)

class Main():
    def __init__(self):
        pg.init()
        pg.display.set_caption("Minesweeper")
        screen_dim = [700 , 700]               
        self.window = pg.display.set_mode(screen_dim)
        self.fps = 60
        self.clock = pg.time.Clock()

        self.boxGroup = pg.sprite.Group()
        self.boxArray = [ int for i in range(3)]

        self.createMenu()
        self.menuing()

        self.maping = Map(self.window)
        self.main()
    
    def createMenu(self):
        menuBoxSmall = MenuBox("Images/Small.png", 10)
        menuBoxMedium = MenuBox("Images/Medium.png", 20)
        menuBoxBig = MenuBox("Images/Big.png", 50)

        menuBoxMedium.rect.x += 250
        menuBoxBig.rect.x += 500

        menuBoxSmall.rect.y += 100
        menuBoxMedium.rect.y += 200
        menuBoxBig.rect.y += 300

        self.boxArray[0] = menuBoxSmall
        self.boxArray[1] = menuBoxMedium
        self.boxArray[2] = menuBoxBig

        self.boxGroup.add(menuBoxSmall)
        self.boxGroup.add(menuBoxMedium)
        self.boxGroup.add(menuBoxBig)

    def onClickLeft(self, mousePos, boxArray):
        box = self.findBox(mousePos, boxArray)
        if box:
            return box
        
    def findBox(self, mousePos, boxArray):
        for i in range(3):
            box = boxArray[i]
            print(box.nr)
            if box.rect.x < mousePos[0] and box.rect.right > mousePos[0]:
                if box.rect.y < mousePos[1] and box.rect.bottom > mousePos[1]:
                    return box
        
    def restart(self):
        print("restarting...")
        Main()
        # self.maping = Map(self.window)

    def menuing(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        exit()
                if event.type == pg.MOUSEBUTTONDOWN: 
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        return self.onClickLeft(pg.mouse.get_pos(), self.boxArray)

            self.window.fill((255, 255, 255))

            self.boxGroup.draw(self.window)
            self.boxGroup.update()

            pg.display.update()
            self.clock.tick(self.fps)
            

    def main(self):
        while True:
            while not self.maping.won and not self.maping.lose:    

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                            exit()
                        if event.key == pg.K_r:
                            self.restart()
                        if event.key == pg.K_y:
                            self.maping.won = True
                    if event.type == pg.MOUSEBUTTONDOWN: 
                        mouse = pg.mouse.get_pressed()
                        if mouse[0]:
                            self.maping.onClickLeft(pg.mouse.get_pos())
                        if mouse[2]:
                            self.maping.onClickRight(pg.mouse.get_pos())

                self.window.fill((200, 20, 20))

                self.maping.draw(self.window)
                self.maping.unflipped()

                pg.display.update()
                self.clock.tick(self.fps)
            
            while self.maping.won or self.maping.lose: 
                import math
                radius = 10
                for angle in range(0, 360, 10):                      
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                                exit()
                            if event.key == pg.K_r:
                                self.restart()  
                                self.lose = False
                                self.main()      

                    theta = math.radians(angle)
                    x = radius*math.cos(theta)
                    y = radius*math.sin(theta) 

                    self.window.fill((200, 20, 20))
                    self.maping.draw(self.window)
                    if self.maping.lose:
                        self.maping.losing(x, y)
                        self.maping.drawBomb()
                    else:
                        self.maping.winning(x, y)
                    pg.display.update()                 
                    self.clock.tick(self.fps)


if __name__ == "__main__":
    Main();