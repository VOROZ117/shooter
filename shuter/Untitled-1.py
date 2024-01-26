from pygame.sprite import Group 
from pygame import*  
from random import randint  
#звук  
mixer.init()  
mixer.music.load("space.ogg")  
mixer.music.play()  
fire = mixer.Sound("fire.ogg")  
  
class GameSprite(sprite.Sprite):  
  
    def __init__(self, player_image , player_x , player_y, size_x, syze_y, player_speed):  
        sprite.Sprite.__init__(self)  
        self.image = transform.scale(image.load(player_image),(50 , 50))   
        self.speed = player_speed  
        self.rect = self.image.get_rect()  
        self.rect.x = player_x  
        self.rect.y = player_y  
    def reset (self):  
        window.blit(self.image,(self.rect.x , self.rect.y))  
  
class Player(GameSprite):  
    def update(self):  
        keys_pressed = key.get_pressed()  
        if keys_pressed [K_LEFT] and self.rect.x > 5 :  
            self.rect.x -= self.speed    
  
            keys_pressed = key.get_pressed()  
        if keys_pressed [K_RIGHT] and self.rect.x < win_width - 80 :  
            self.rect.x += self.speed  
  
  
    def fire(self):  
        pass  
        bullet = Bullet("bullet.png", self.rect.x, self.rect.y, 15, 20, -15 ) 
        bullets.add(bullet) 
 
class Bullet(GameSprite): 
    def update(self): 
        self.rect.y +=  self.speed 
        #зникає, якщо дійде до краю екрану 
        if self.rect.y < 0: 
            self.kill() 
bullets = sprite.Group() 
#лічильник збитих і пропущених кораблів  
      
score = 0  
 
lost = 0  
class Enemy(GameSprite):  
    def update(self):  
        self.rect.y += self.speed  
        global lost   
  
        if self.rect.y > win_height:  
            self.rect.x = randint(80, win_width - 80)  
            self.rect.y = 0  
            lost = lost + 1  
  
#ігрова сцена  
win_width = 700  
win_height = 500  
window = display.set_mode((win_width, win_height))  
display.set_caption("Shooter Game")  
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))  
#шрифти ы написи  
font.init()  
font2 = font.Font(None, 36)
font1 = font.Font(None , 80)

txt_lose_game = font1.render('YOU LOSE' , True, [255, 0, 0])
txt_win_game = font1.render('YOU WIN' , True, [0, 255, 0])



  
#зображення  
asteroid = 'asteroid.png'  
bullet = 'bullet.png'  
rocket = 'rocket.png'  
ufo = 'ufo.png'  
  
#спайти  
rocket = Player(rocket, 5, win_height - 100, 80, 100, 20)  
monsters = sprite.Group()  
for i in range(1, 6):  
    monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  
    monsters.add(monster)   
  
#змінна гра закінчилась  
  
finish = False  
  
  
#Цикл гри
run = True  
  
while run:  
  
    #подія натискання на кнопку закрити  
      
    for e in event.get():  
        if e.type == QUIT:  
            run = False  
        #подія натискання на пробіл - спрайт стріляє 
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: 
                fire.play() 
                rocket.fire() 
    if not finish:  
  
        window.blit(background, (0, 0))  
          
        #пишемо текст на екрані  
  
        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))  
        window.blit(text, (10, 20))  
  
        text_lost = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))  
        window.blit(text_lost, (10, 50))  
  
        #рухи спрайтів  
  
        rocket.update()  
        monsters.update()  
        bullets.update() 
  
        rocket.reset() 

        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(txt_lose_game, [200,200])
        
        collides = sprite.groupcollide(monsters, bullets, True , True)
        for c in collides:
            monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  
            monsters.add(monster)
            score += 1

        if score == 40:
            finish = True
            window.blit(txt_win_game, [200,200])
            
            score = 0
            lost = 0
        for m in monsters:
            m.kill()
        
        for m in bullets:
            m.kill()
        
        time.delay(3000)
        for i in range(5):
            mon = Enemy('ufo.png', randint (0, win_width-80), 0 , 80, 50, randint(1,5))
            monsters.add(mon)




        monsters.draw(window)  
        bullets.draw(window) 
 
        display.update()  
  
    time.delay(50)