import pygame
import time
import random

pygame.init() ## initail pygame

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height)) ## windows size
pygame.display.set_caption('Dodge') ## title
clock = pygame.time.Clock()

carImg = pygame.image.load('object.png')

def thing_dodged(count):
    font = pygame.font.SysFont('Monaco.ttf', 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (1, 1))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])    

def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.SysFont('Monaco.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    
    time.sleep(3)

    game_loop()

def crash():
    message_display("Game Over!")

def quit_game():
    pygame.quit()
    quit()

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
        
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1 and action:
            action() 
##            if action == 'play':
##                game_loop()
##            elif action == 'quit':
##                pygame.quit()
##                quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.SysFont('Monaco.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont('Monaco.ttf', 115)
        TextSurf, TextRect = text_objects('Dodge', largeText)
        TextRect.center = ((display_width/2), (display_height/3))
        gameDisplay.blit(TextSurf, TextRect)

        button('GO!', 150,450,100,50, green, bright_green, game_loop)
        button('Quit!', 550,450,100,50, red, bright_red, quit_game)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    gameExit = False

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 5
    thing_width = 100
    thing_height = 100

    thing_count = 1
    
    dodged = 0

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -15
                elif event.key == pygame.K_RIGHT:
                    x_change = 15
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
        
        x += x_change
        if x > display_width - car_width or x < 0:
            x -= x_change

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            thing_speed += 0.5
            dodged += 1
            thing_count += 1

        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash()
        
        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car(x, y)
        thing_dodged(dodged)
        
        pygame.display.update() ## reset
        clock.tick(120) ## FPS

game_intro()
game_loop()
pygame.quit()
quit()
