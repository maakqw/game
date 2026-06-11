import time

import pygame as pg
pg.init()
pg.mixer.init()

WIN = pg.display.set_mode((1920,1080))
pg.display.set_caption("")

clock = pg.time.Clock()
run = 1

def image(path, width = None, height = None):
    u = pg.image.load(path)
    if width is None or height is None:
        return u
    else:
        return pg.transform.scale(u, (width, height))

exit = image("images/exit-button.png")
button_exit = pg.Rect(1650, 140, 40, 40)

click_sound = pg.mixer.Sound('sounds/click.mp3')

while run:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click_sound.play()
            if button_exit.collidepoint(event.pos):
                time.sleep(0.33)
                run = 0


    #WIN.fill((255,255,255))
    WIN.blit(exit, (1650, 140))

    pg.display.flip()


pg.quit()