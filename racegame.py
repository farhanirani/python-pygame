import pygame
import time
from random import randint

pygame.init() # we initialise the pygame  module
# here we initialise the window properties
display_width = 800
display_height = 600
white=(255,255,255)
black = (0,0,0)
red = (200,0,0)
blue = (0,0,255)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
gameDisplay = pygame.display.set_mode((display_width,display_height)) # this will display the game window

clock = pygame.time.Clock() # this will keep track of the fps

pygame.display.set_caption('A bit Racey') # the caption of the game


def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,(thingx,thingy,thingw,thingh))

def carDisplay(x,y): # this function will display the image of the car
    gameDisplay.blit(carImg,(x,y))


def crash(): # this function will display the crash message
    messaage_display('YOU CRASHED')


def dodged_thing(count):
    font = pygame.font.SysFont(None,25)
    text = font.render('DODGED:-'+ str(count),True,green)
    gameDisplay.blit(text,(0,0))
    pygame.display.update()


def messaage_display(text): # this will help in displaying the windows
    largeText = pygame.font.SysFont('/home/ram2510/Desktop/python/pygame/fonts',115)
    textSurf,textRect = text_objects(text,largeText)
    textRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(textSurf,textRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def Button(msg,x,y,w,h,inactive_color,active_color,action = None):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if x+w > mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,active_color,(x,y,w,h))
        if clicked[0]==1 and action!= None:
            if action == 'play':
                game_loop()
            elif action == 'quit':
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(gameDisplay,inactive_color,(x,y,w,h))

    smallText = pygame.font.SysFont('/home/ram2510/Desktop/python/pygame/fonts',25)
    textSurf,textRect = text_objects(msg,smallText)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

def text_objects(text,font):
    textSurf = font.render(text,True,black)
    return textSurf,textSurf.get_rect()


carImg = pygame.image.load('racecar.png').convert_alpha() # this loads the image of the  car and converts it to alpha


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            gameDisplay.fill(white)
            largeText = pygame.font.SysFont('/home/ram2510/Desktop/python/pygame/fonts',115)
            textSurf,textRect = text_objects('A bit RACEY',largeText)
            textRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(textSurf,textRect)
            pygame.draw.rect(gameDisplay,green,(150,450,100,50))
            pygame.draw.rect(gameDisplay,red,(550,450,100,50))
            #def Button(msg,x,y,w,h,inactive_color,active_color):
            Button('GO!',150,450,100,50,green,bright_green,'play')
            Button('QUIT.',550,450,100,50,red,bright_red,'quit')
            pygame.display.update()


def game_loop(): # this is the main game loop
    gameExit = False
    x = (display_width*0.45) # this will help in moving the images
    y = (display_height*0.75)
    thing_x = randint(0,display_width-5)
    thing_y = -600
    thing_y_change = 3
    thing_height = 50
    thing_width = 100
    x_change = 0 # this is the change the user wants
    car_width = 35
    dodged = 0
    while not gameExit: # this will run unil its not true
        for event in pygame.event.get(): # this gets all the event the user puts in the window
            if event.type == pygame.QUIT: # if the user clicks on the x bitton
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: # if the user prsses any key downwards or applies pressure to the keys
                if event.key == pygame.K_LEFT: # if the key pressed is left
                    x_change = -5
                if event.key == pygame.K_RIGHT: # if the key pressed is right
                    x_change = 5

            if event.type == pygame.KEYUP: # if the user releases the key which he/she pressed
                if event.key == pygame.K_LEFT or pygame.K_RIGHT: # any key
                    x_change = 0
        x += x_change # to change the position
        if x>display_width-car_width or x<0: #if the user goes out of the window
            crash() # this will call the crash function

        gameDisplay.fill(white) # this will paint the windows white
        #things(thingx,thingy,thingw,thingh,color)

        things(thing_x,thing_y,thing_width,thing_height,blue)
        thing_y += thing_y_change
        if thing_y>display_width:
            thing_y = 0
            thing_x = randint(0,display_width)
            dodged += 1
            thing_y_change +=1

        carDisplay(x,y) # this will display the car in the x y posotion
        dodged_thing(dodged)
        if y<thing_y + thing_height:
            if x>thing_x and x<thing_x+thing_width or x + car_width >thing_x and x + car_width < thing_x + thing_width:
                crash()

        pygame.display.update() # this will update the screeen
        clock.tick(60) # this will make the whole game_loop in 60 frames per second

game_intro()
game_loop()
pygame.quit() # quit the game
quit() # this quit for python
