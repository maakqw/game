import time
import pygame as pg
from ctypes import windll
pg.init()
pg.mixer.init()

try:
    windll.user32.SetProcessDPIAware()  # Windows
except:
    pass

WIN = pg.display.set_mode((1920, 1080))

pg.display.set_caption("")

clock = pg.time.Clock()
run = 1

keys = pg.key.get_pressed()

game_phase = "menu"

escape_counter = 0
transition_counter = 0

transition_active = 0

def check_escape():
    global escape_counter
    if keys[pg.K_ESCAPE]:
        if escape_counter >= 10:
            escape_counter = 0
            return 1
        else:
            return 0
    else:
        return 0

def image(path, width = None, height = None):
    u = pg.image.load(path)
    if width is None or height is None:
        return u
    else:
        return pg.transform.scale(u, (width, height))

exit_img = image("images/exit-button.png")
button_exit = pg.Rect(1840 , 40, 40, 40)

play = image("images/play-button.png", 140, 40)
button_play = pg.Rect(890,490,140,40)

back = image("images/continue-button.png", 140, 40)
button_continue = pg.Rect(890, 490, 140, 40)

main_menu = image("images/menu-button.png", 140,40)
button_menu = pg.Rect(890, 550, 140, 40)

resume = image("images/resume-button.png")
button_resume = pg.Rect(40, 40, 40, 40)

pause_image = image("images/pause-button.png")
button_pause = pg.Rect(40, 40, 40, 40)

background = image("images/background.png", 1920,1080)

darkmode = image("images/darkmode.png", 1920,1080)

click_sound = pg.mixer.Sound('sounds/click.mp3')

def menu():
    global run, game_phase
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click_sound.play()
            if button_exit.collidepoint(event.pos):
                time.sleep(0.33)
                run = 0
            elif button_play.collidepoint(event.pos):
                game_phase = "transition"

    play.set_alpha(255)

    WIN.blit(background, (0,0))

    WIN.blit(darkmode, (0, 0))

    WIN.blit(exit_img, (1840 , 40))
    WIN.blit(play, (890, 490))

def transition():
    global transition_counter, run, game_phase, transition_active

    transition_active = 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click_sound.play()
            if button_exit.collidepoint(event.pos):
                time.sleep(0.33)
                run = 0

    play.set_alpha(255 - transition_counter)
    darkmode.set_alpha(255 - transition_counter)
    pause_image.set_alpha(transition_counter)

    if transition_counter >= 255:
        transition_active = 0
        game_phase = "game"

    WIN.blit(background, (0,0))
    WIN.blit(darkmode, (0,0))
    WIN.blit(play, (890, 490))
    WIN.blit(pause_image, (40, 40))
    WIN.blit(exit_img, (1840 , 40))


def game():
    global run, game_phase, keys

    keys = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click_sound.play()
            if button_pause.collidepoint(event.pos):
                game_phase = "pause"
            elif button_exit.collidepoint(event.pos):
                time.sleep(0.33)
                run = 0

    if check_escape():
        game_phase = "pause"

    WIN.blit(background, (0,0))

    WIN.blit(exit_img, (1840 , 40))
    WIN.blit(pause_image, (40, 40))

def pause():
    global run, game_phase, keys

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click_sound.play()
            if button_continue.collidepoint(event.pos) or button_resume.collidepoint(event.pos):
                game_phase = "game"
            elif button_menu.collidepoint(event.pos):
                game_phase = "menu"
            elif button_exit.collidepoint(event.pos):
                time.sleep(0.33)
                run = 0

    if check_escape():
        game_phase = "game"

    WIN.blit(background, (0,0))

    WIN.blit(darkmode, (0,0))

    WIN.blit(exit_img, (1840 , 40))
    WIN.blit(back,(890, 490))
    WIN.blit(main_menu, (890,550))
    WIN.blit(resume, (40 ,40))

while run:
    clock.tick(60)
    WIN.fill((0,0,0))

    if transition_active:
        transition_counter += 8

    escape_counter += 1
    if escape_counter > 1000:
        escape_counter = 10

    keys = pg.key.get_pressed()

    match game_phase:
        case "menu":
            menu()
        case "game":
            game()
        case "pause":
            pause()
        case "transition":
            transition()

    print(game_phase)

    pg.display.flip()


pg.quit()