import time
import pygame
import random
import os

# we set up the screen size and the fps
screen_width = 640
screen_height = 480
fps = 30

# we initialise the snake body here 
segment_width = 15
segment_height = 15 
segement_margin = 3
# we set the initial speed
x_change = segment_width + segement_margin
y_change = 0

# here we initialise the windows
pygame.init()
pygame.mixer.init() # we will use this for sound
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('SNAKE hiss')
clock = pygame.time.Clock()

# we initialise all the assests
gameFld = os.path.dirname(__file__)
sound = os.path.join(gameFld,"snake_sound")
images = os.path.join(gameFld,"snake_images")

# we load all the graphics here
background = pygame.image.load(os.path.join(images,"BACKGRND.png")).convert()
background_image = pygame.transform.scale(background,(640,480))
background_rect = background_image.get_rect()
apple1 = pygame.image.load(os.path.join(images,"apple.png")).convert()

# we load all the sounds here
pygame.mixer.music.load(os.path.join(sound,"back_music.mp3"))
bite_sound = pygame.mixer.Sound(os.path.join(sound,'bite_sound.wav'))
pygame.mixer.music.set_volume(1)


font_name = pygame.font.match_font('Arial')
# we create a function to draw text
def text(surface,text,size,x,y):
    font = pygame.font.SysFont(font_name,size)
    text_surface = font.render(text,True,red)
    text_rect = text_surface.get_rect()
    text_rect.midtop =(x,y)
    surface.blit(text_surface,text_rect)


# we create all the sprite classes
# we create the snake segment sprite first
class Segment(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([segment_width,segment_height])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# we create the apple object here
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(apple1,(25,25))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(30,screen_width-30)
        self.rect.y = random.randrange(30,screen_height-30)

def main_menu(surf):
    menu = pygame.image.load(os.path.join(images,"main_menu.png")).convert()
    menu_image = pygame.transform.scale(menu,(screen_width,screen_height),screen)
    surf.blit(menu_image,(0,0))
    pygame.display.update()
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                break
            if ev.key == pygame.K_q:
                quit()

def end_menu(surf):
    menu = pygame.image.load(os.path.join(images,"end.png")).convert()
    menu_image = pygame.transform.scale(menu,(screen_width,screen_height),screen)
    surf.blit(menu_image,(0,0))
    pygame.display.update()
    time.sleep(3)

# we creare the function for sprites so that we can manage all the sprites
all_sprites = pygame.sprite.Group()
segment_group = pygame.sprite.Group()
snake_segment = [] # we create this list to store all thhe segments
for  i in range(0,2):
    x = 250 - (segment_width+ segement_margin)*i
    y= 30
    segments =Segment(x,y)
    snake_segment.append(segments)
    all_sprites.add(segments)
    segment_group.add(segments)
apple_group = pygame.sprite.Group()
apple =Apple()
apple_group.add(apple)
all_sprites.add(apple)


# game loop 
pygame.mixer.music.play(loops = -1)
running = True
main = True
while running:
    if main:
        main_menu(screen)
        main = False
    # we tweak the fps here
    clock.tick(fps)

    # we keep track of all the events here
    for event in pygame.event.get():
        # if the user wishes to quit
        if event.type == pygame.QUIT:
            running = False

        # we set the movent all the segments
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_change = (segment_height + segement_margin)*-1
                x_change=0
            if event.key == pygame.K_DOWN:
                y_change = (segment_height + segement_margin)
                x_change= 0
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segement_margin)*-1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segement_margin)
                y_change = 0
    
    

    # we remove the last element of the snake segment 
    old_segment = snake_segment.pop()
    segment_group.remove(old_segment)
    all_sprites.remove(old_segment)

    # we add the new element on the top of the snake
    x = snake_segment[0].rect.x + x_change
    y = snake_segment[0].rect.y + y_change
    segment = Segment(x,y)
    snake_segment.insert(0,segment)
    all_sprites.add(segment)
    # here we detect collison between apple group and snake sprite and make changes
    
    eat_coll = pygame.sprite.spritecollide(snake_segment[0],apple_group,True) 
    if eat_coll:
        x = snake_segment[-1].rect.x - x_change
        y = snake_segment[-1].rect.y - y_change
        segment = Segment(x,y)
        snake_segment.insert(-1,segment)
        segment_group.add(segment)
        apple_group.remove(apple)
        apple = Apple()
        apple_group.add(apple)
        all_sprites.add(apple)
        bite_sound.play()
    
    # we will end the game if snake collides
    if snake_segment[0].rect.x < 0 - segment_width or snake_segment[0].rect.x > screen_width + segment_width:
        end_menu(screen)
        running = False

    if snake_segment[0].rect.y < 0 - segment_height or snake_segment[0].rect.y > screen_height + segment_height:
        end_menu(screen)
        running = False

    
    # here we fill the background

    screen.blit(background_image,background_rect)
    all_sprites.draw(screen)
    
    # we will update the screen

    pygame.display.update()

text(screen,"YOU DIED",118,screen_width/2,screen_height/2)
time.sleep(3)
    
pygame.quit()