from pygame import *

init()
back= (200,255,255)
win_width=700
win_height=500
GREEN = (0,255,0)
window = display.set_mode((win_width,win_height))
window.fill(back)
display.set_caption('Моя первая игра')
picture = transform.scale(image.load('background1.jpg'), (700,500))



class GameSprite(sprite.Sprite): 
    def __init__(self,filename, width, height, x, y): 
        super().__init__() 
        self.image = transform.scale(image.load(filename), (width, height)) 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
        self.rect = Rect(x, y, width, height) 
 
    def reset(self): 
        window.blit(self.image,(self.rect.x, self.rect.y)) 
 
class Player(GameSprite): 
    def __init__(self, filename, width, height, x,y, x_speed, y_speed): 
        super().__init__(filename, width, height, x, y) 
        self.x_speed = x_speed 
        self.y_speed = y_speed 
    def update(self): 
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        platforms_touched = sprite.spritecollide(self, barriers, False) 
        if self.x_speed>0:
            for p in platforms_touched:
                self.rect.right=min(self.rect.left,p.rect.left)
        elif self.x_speed<0:
            for p in platforms_touched:
                self.rect.left=max(self.rect.left,p.rect.right)
        self.rect.y += self.y_speed
        if self.y_speed>0:
            for p in platforms_touched:
                self.rect.bottom=min(self.rect.bottom,p.rect.top)
        elif self.y_speed<0:
            for p in platforms_touched:
                self.rect.top=max(self.rect.top,p.rect.bottom)
        if self.rect.x<0:
            self.rect.x += 5
        elif self.rect.y<0:
            self.rect.y += 10
        elif self.rect.x>660:
            self.rect.x-=5
        elif self.rect.y>460:
            self.rect.y-=10
    def fire(self):
        bullet = Bullet('cobweb.png',20 ,20, self.rect.right, self.rect.centery, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, filename, width, height, x,y, speed): 
        super().__init__(filename, width, height, x, y) 
        self.speed = speed
    def update(self):
        if self.rect.x <= 490:
            self.rect.x += self.speed
            self.direction = 'right'
        elif self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
class Bullet(GameSprite):
    def __init__(self, filename, width, height, x,y, speed): 
        super().__init__(filename, width, height, x, y) 
        self.speed = speed
    def update(self):
        self.rect.x+=self.speed
        if self.rect.x>680:
            self.kill()

player = Player('spiderman.png', 50,50,100,400, 0,0)
wall1= GameSprite('wall.png', 250,40, 200,200)
wall2= GameSprite('wall.png', 40,350, 450,120)
wall3= GameSprite('wall.png', 200,40, 10,350)
final = GameSprite('finish.png',50,50,550,400)
enemy = Enemy('ghost.png', 50,50,650,200,2)


bullets = sprite.Group()
barriers = sprite.Group()
barriers.add(wall1)
barriers.add(wall2)
barriers.add(wall3)

enemies = sprite.Group()
enemies.add(enemy)

run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run= False #break
        if e.type == KEYDOWN: 
            if e.key == K_RIGHT: 
                player.x_speed=5 
            if e.key == K_LEFT: 
                player.x_speed=-5 
            if e.key == K_UP: 
                player.y_speed=-5 
            if e.key == K_DOWN: 
                player.y_speed=5 
            if e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP: 
            if e.key == K_RIGHT: 
                player.x_speed=0 
            if e.key == K_LEFT: 
                player.x_speed=0 
            if e.key == K_UP: 
                player.y_speed=0 
            if e.key == K_DOWN: 
                player.y_speed=0 
    #K_UP K_DOWN
    window.blit(picture, (0,0))
    if sprite.collide_rect(player,final):
        finish = True
        win.reset()
    if sprite.collide_rect(player,enemy):
        finish = True
        lose.reset()
    sprite.groupcollide(bullets,barriers,True,False)
    sprite.groupcollide(bullets,enemies,True, True)

    if not(finish):
        bullets.draw(window)
        barriers.draw(window)
        enemies.draw(window)
        enemies.update()
        bullets.update()
        player.reset()
        wall1.reset()
        player.update()
        wall2.reset()
        wall3.reset()
        final.reset()
    display.update()
