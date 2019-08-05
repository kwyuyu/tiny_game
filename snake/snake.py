import pygame
import time
import random

pygame.init()

display_width = 600
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
bright_blue = (0,0,255)
blue = (0,0,200)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

# object related
def square(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])

def food(position, button_height, cube):
    while True:
        food_x = random.randrange(0, display_width / cube) * cube
        food_y = random.randrange(int(button_height / cube), display_height / cube) * cube
        if [food_x, food_y] not in position:
            break
        
    return food_x, food_y

# text realated
def text_object(text, font, color):
    textSurface = font.render(text, True, color)

    return textSurface, textSurface.get_rect()

def message_display(text, size, color, x, y, w, h):
    largeText = pygame.font.SysFont('Monaco.ttf', size)
    TextSurf, TextRect = text_object(text, largeText, color)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)

# button related
def RESET_button(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    message_display(msg, 15, white, x, y, w, h)

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    message_display(msg, 15, black, x, y, w, h)

# persistent move
def move(action, cube):
    if action == 1 or action == 3:
        change = -cube
    elif action == 2 or action == 4:
        change = cube
        
    return change

# game related
def loop(repeat):
    while repeat:
        repeat = main()

def crash_wall():
    message_display('Game Over!', 75, red, 0, 0, display_width, display_height)
    pygame.display.update()
    time.sleep(3)
    
    return True
    
def main():
    gameExit = False

    cube = 20
    action = 0
    init_snake_length = 3
    button_height = 2 * cube
    snake_x_change = 0
    snake_y_change = 0
    key = 1
    speed = 0.1
    position = []
    
    snake_x = random.randrange(int((display_width / cube) * 0.25), int((display_width / cube) * 0.75)) * cube
    snake_y = random.randrange(int((display_height / cube) * 0.25), int((display_height / cube) * 0.75)) * cube

    for n in range(init_snake_length):
        position.append([snake_x + cube * n, snake_y])

    food_x, food_y = food(position, button_height, cube)
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and action != 4:
                    snake_x_change = -cube
                    snake_y_change = 0
                    action = 3
                    key = 0
                elif event.key == pygame.K_RIGHT and action != 3:
                    if action == 0:
                        position.reverse()
                        snake_x += (init_snake_length - 1) * cube
                    snake_x_change = cube
                    snake_y_change = 0
                    action = 4
                    key = 0
                elif event.key == pygame.K_UP and action != 2:
                    snake_y_change = -cube
                    snake_x_change = 0
                    action = 1
                    key = 0
                elif event.key == pygame.K_DOWN and action != 1:
                    snake_y_change = cube
                    snake_x_change = 0
                    action = 2
                    key = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_DOWN:
                    key = 1
                    
        if key == 1:
            if action == 1 or action == 2:
                snake_y_change = move(action, cube)
                snake_x_change = 0
            elif action == 3 or action == 4:
                snake_x_change = move(action, cube)
                snake_y_change = 0
        
        snake_x += snake_x_change
        snake_y += snake_y_change

        ## crash the wall
        if snake_x < 0 or snake_x + cube > display_width or snake_y < button_height or snake_y + cube > display_height:
            if crash_wall():
                break
        elif action != 0 and [snake_x, snake_y] in position:
            if crash_wall():
                break
        
        ## eat food
        if food_x == snake_x and food_y == snake_y:
            food_x, food_y = food(position, button_height, cube)
        else:
            if len(position) > 1 and action != 0:
                position.pop()
                
        if action != 0:
            position.insert(0, [snake_x, snake_y])

        gameDisplay.fill(white)
        
        for x, y in position:
            square(x, y, cube, cube, black) # snake

        square(food_x, food_y, cube, cube, red) # food

        # reset the map
        if RESET_button('RESET', 5, 5, 50, 25, blue, bright_blue):
            break
        
        pygame.display.update()
        clock.tick(120)

        time.sleep(speed)

    return True





loop(True)








