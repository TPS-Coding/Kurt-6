from settings import *
from random import choice, uniform


 
class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        #image
            
        self.image = pygame.Surface(SIZE['paddle'])
        self.image.fill(COLORS['paddle'])

        #rect and movement
        self.rect = self.image.get_frect(center = (POS['player']))
        self.direction = 0 ##initializing at zero  
        self.speed = SPEED['player'] ## speed set from dictionary in settings.py
        self.old_rect = self.rect.copy()


    def move(self,dt):
        self.rect.centery += self.direction * self.speed * dt ## y = v * t (velocity=[speed * direction] * time)

        ## setting boundary conditions
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        ## this calls the functions move() and get_direction(). the overall function update() gets called in main.py when we call self.all_sprites.update()
        self.get_direction()
        self.move(dt)


class Player(Paddle):
    def __init__(self,groups):
        super().__init__(groups)

       
        self.speed = SPEED['player'] ## speed set from dictionary in settings.py



        ## setting boundary conditions
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom

    def get_direction(self):
        ## getting keboyard input to move the paddle
        keys = pygame.key.get_pressed() ### returns a dictionary of keys with True or False values if pressed or not
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) ## int(True) = 1, int(False) = 0, so this returns 1, 0, -1 based on what key is pressed



    
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites):
        super().__init__(groups)

        self.paddle_sprites = paddle_sprites
        ## image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image,COLORS["ball"], (SIZE['ball'][0]/2, SIZE['ball'][1]/2), SIZE['ball'][0]/2) 
        
        ## rect
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 ))
        ## direction here is in 2D (x and y) so it has to set up as a vector. The choice and uniform functions makes the direction somewhat random to start
        self.direction = pygame.Vector2(choice([1,-1]), uniform(0.7, 0.8) * choice([1,-1]))
        self.old_rect = self.rect.copy()
    

    def move(self, dt):
        self.rect.center += self.direction * SPEED["ball"] * dt ## this gives a vector in both x and y

        self.collision("horizontal")


    def wall_collision(self):
        ## y direction
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        
      

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.rect.right >= sprite.rect.left and self.direction.x == 1:
                        self.rect.right = sprite.rect.left

                    if self.rect.left <= sprite.rect.right and self.direction.x == -1:
                        self.rect.left = sprite.rect.right

                    self.direction.x *= -1 ## this needed to be outside the if statement
    
    def update(self,dt):
        self.old_rect = self.rect.copy()
        ## always must include the update function so that the written functions are called
        self.move(dt)
        self.wall_collision()



class Opponenent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)

        self.speed = SPEED['opponent']
        self.rect = self.image.get_frect(center = POS['opponent'])
        self.ball = ball

    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1 ## center not centur