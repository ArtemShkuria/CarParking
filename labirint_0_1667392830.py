from pygame import *

mixer.init()
mixer.music.load("minecraft.ogg")
mixer.music.play(-1)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed       

    
    def update(self): 
        if car.rect.x <= win_width-80 and car.x_speed > 0 or car.rect.x >= 0 and car.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if car.rect.y <= win_height-80 and car.y_speed > 0 or car.rect.y >= 0 and car.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)


class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 240:
            self.side = "right"
        if self.rect.x >= win_width - 450:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed               
 

win_width = 1500
win_height = 900
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load('asphalt.jpg'),(1500,900))
black = (105, 105, 105)

barriers = sprite.Group()
car2 = sprite.Group()

barriers.add(GameSprite('bebra.png', 170, 350, 300, 70))
barriers.add(GameSprite('bebra2.png', 450, 350, 70, 400))
barriers.add(GameSprite('bebra2.png', 1250, -40, 70, 450))
barriers.add(GameSprite('bebra2.png', 1250, 550, 70, 450))
barriers.add(GameSprite('bebra2.png', 170, 750, 65, 400))
barriers.add(GameSprite('bebra2.png', 970, 550, 80, 250))
barriers.add(GameSprite('bebra2.png', 170, 160, 70, 400))
barriers.add(GameSprite('bebra.png', 170, 130, 350, 70))
barriers.add(GameSprite('bebra.png', 950, 130, 350, 70))
barriers.add(GameSprite('bebra.png', 380, 130, 350, 70))
barriers.add(GameSprite('bebra.png', 955, 340, 350, 70))
barriers.add(GameSprite('bebra.png', 170, 730, 350, 70))
barriers.add(GameSprite('bebra.png', 700, 730, 305, 70))
barriers.add(GameSprite('bebra.png', 730, 340, 350, 70))
barriers.add(GameSprite('bebra2.png', 700, 350, 70, 400))
 
car = Player('car.png', 5, win_height - 150, 150, 50, 0, 0)
car_2 = Enemy('car2.png', win_width - 550, 240, 180, 60, 20)
final_sprite = GameSprite('diamond.png', win_width - 170, win_height - 150, 150, 120)

car2.add(car_2)

finish = False 
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                car.x_speed = -20
            elif e.key == K_RIGHT:
                car.x_speed = 20
            elif e.key == K_UP:
                car.y_speed = -20
            elif e.key == K_DOWN:
                car.y_speed = 20
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                car.x_speed = 0
            elif e.key == K_RIGHT:
                car.x_speed = 0
            elif e.key == K_UP:
                car.y_speed = 0
            elif e.key == K_DOWN:
                car.y_speed = 0
    if not finish:
        window.blit(back,(0,0))
        barriers.draw(window) 
        car2.draw(window)  
        car.reset()
        final_sprite.reset()
        car.update()
        car2.update()

        if sprite.spritecollide(car, car2, False):
                finish = True
                img = image.load('game-over_1.png')
                d = img.get_width() // img.get_height()
                window.fill((255, 255, 255))
                window.blit(transform.scale(img, (win_height * d, win_height)), (300, 0))

        if sprite.collide_rect(car, final_sprite):
                finish = True
                img = image.load('thumb.png')
                window.fill((255, 255, 255))
                window.blit(transform.scale(img, (win_width, win_height)), (-100, 0))

        time.delay(30)
        display.update()