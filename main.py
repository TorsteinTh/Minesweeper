import pygame as pg
import precode as pc


class Box():
    def __init__(self):
        self.visible: True 
    
    def setup():
        pass 

    def draw():
        pass

    def open():
        pass
    
    def flag():
        pass
    
class Main():
    def __init__(self):

        self.main()

    def restart(self):
        print("restarting...")

    def main(self):
        pg.display.set_caption("Minesweeper")
        screen_dim = [700 , 700]               
        pg.init()
        window = pg.display.set_mode(screen_dim)
        fps = 100
        clock = pg.time.Clock()

        while True:    
            window.fill((30, 10, 50))
            pg.display.update()                 
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        exit()
                    if event.key == pg.K_r:
                        self.restart()
                if event.type == pg.MOUSEBUTTONDOWN: 
                    print(pg.mouse.get_pos())


if __name__ == "__main__":
    Main();