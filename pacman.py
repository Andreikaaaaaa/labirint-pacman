from pygame import*
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
    def __init__(self, player_image, player_x, player_y, size_x, size_y,speedx,speedy):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speedx = speedx
        self.speedy = speedy
    def update(self):
        if pacman.rect.x <= winw - 80 and pacman.speedx > 0 or pacman.rect.x >= 0 and pacman.speedx <0:
            self.rect.x += self.speedx
        platforms = sprite.spritecollide(self, bariers, False)
        if self.speedx  > 0:
            for platform in platforms:
                self.rect.right = min(self.rect.right, platform.rect.left)
        elif self.speedx < 0:
            for platform in platforms:
                self.rect.left = max(self.rect.left, platform.rect.right)
        if pacman.rect.y <= winw - 80 and pacman.speedy > 0 or pacman.rect.y >= 0 and pacman.speedy <0:

           self.rect.y += self.speedy      
        platforms = sprite.spritecollide(self, bariers, False)
        if self.speedy  > 0:
            for platform in platforms:
                self.rect.bottom = min(self.rect.bottom, platform.rect.top)
        elif self.speedy < 0:
            for platform in platforms:
                self.rect.top = max(self.rect.top, platform.rect.bottom)
            
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.right,self.rect.centery,15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    direction = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y,speedx,):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speedx = speedx
    def update(self):
        if self.rect.x <= 420:
            self.direction = 'right'
        if self.rect.x >= winw-85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speedx
        else:
            self.rect.x += self.speedx 
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speedx):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speedx = speedx
    def update(self):
        self.rect.x += self.speedx
        if self.rect.x > winw + 10:
            self.kill()
    
winw = 700
winh = 500
window = display.set_mode((winw,winh))
display.set_caption('okno')
background = (255,255,255)
pacman = Player('pacman.png',5,winh-80,80,80,0,0)  
wall = GameSprite('wall.png',winw/2-winw/3,winh/2,300,50)
wall2 = GameSprite('wall.png',370,100,50,400)
ghost = Enemy('ghost.png',winw-80,180,50,50,5)
run = True
finalghost = GameSprite('ghost2.png',winw-85,winh-100,50,50)
finish = False
bullets = sprite.Group()
bariers = sprite.Group()
monsters = sprite.Group()
monsters.add(ghost)
bariers.add(wall)
bariers.add(wall2)
font.init()
while run:
    time.delay(50)
   
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN: 
            if e.key == K_a:
                pacman.speedx = -5
            elif e.key == K_d:
                pacman.speedx = 5
            elif e.key == K_w:
                pacman.speedy = -5
            elif e.key == K_s:
                pacman.speedy = 5
            elif e.key == K_SPACE:
                pacman.fire()
        elif e.type == KEYUP:
            if e.key == K_a:
                pacman.speedx = 0
            elif e.key == K_d:
                pacman.speedx = 0
            elif e.key == K_w:
                pacman.speedy = 0
            elif e.key == K_s:
                pacman.speedy = 0
    if not finish:
        window.fill(background)
        finalghost.reset()
        pacman.update()
        pacman.reset()
        bullets.update()
        bullets.draw(window) 
        bariers.draw(window) 
        sprite.groupcollide(monsters, bullets,True,True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets,bariers,True,False)
        if sprite.collide_rect(pacman,finalghost):
            finish = True
            Win = font.SysFont('Arial',40).render('YOU WIN',True,(0,0,0))
            window.blit(Win,(100,100))
            image = transform.scale(image.load('usaflag.jpg'), (100,100))
            window.blit(image,(150,150))
        if sprite.collide_rect(pacman,ghost):
            finish = True
            Lose = font.SysFont('Arial',40).render('YOU LOSE',True,(0,0,0))
            window.blit(Lose,(100,100))
            image = transform.scale(image.load('canadaflag.png'), (140,140))
            window.blit(image,(150,150))
    display.update()
