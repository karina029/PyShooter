from pygame import *
from random import *
from time import time as timer
from PyQt5.QtWidgets import *

win_width = 1000
win_height = 700
app = QApplication([])
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
display.set_icon(image.load('shot.jpeg'))
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
final = transform.scale(image.load("final.jpeg"), (win_width, win_height))
win_final = transform.scale(image.load("визнання.jpeg"), (win_width, win_height))
win_secretfinal = transform.scale(image.load("diamonds.jpeg"), (win_width, win_height))
mixer.init()
mixer.music.load("mainmenu.mp3")
mixer.music.play()
mixer.music.set_volume(0.2)


def messagestartgame():
    message = QMessageBox()
    message.setText(
        "Вітаю вас у грі Шутер! Ви будете грати за тілоохоронця, який рятує людей від терроризму. Ваше завдання: вбити ворогів та боса, який з'явиться при необхідній кількості очок, зберігаючи постріли та здоров'я гравця. Якщо здолаєш їх, то врятуєш людей від тероризму, а в іншому випадку терористи підірвуть місто")
    message.setIcon(QMessageBox.Information)
    message.exec()


messagestartgame()
lose_sound = mixer.Sound('lose_sound.mp3')
win_secretsound = mixer.Sound('diamonds.mp3')
win_sound = mixer.Sound('winner_sound.mp3')
gamestart = mixer.Sound("gamestart.mp3")
f = mixer.Sound("пострil.mp3")
f.set_volume(0.1)
gamestart.play()
bullets = ["weapon.png", "granata.png"]


class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_img), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        '''
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
        '''
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed
        '''pos = mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width/2
        self.rect.y = pos[1] - self.rect.height/2'''
        self.reset()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height + 50:
            self.rect.y = - 50
            '''if self.rect.y < win_height:
            #self.rect.y -= 50'''
            self.speed = randint(2, 8)
            global lost
            lost += 1
        self.reset()


class Knife(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < - 100:
            self.kill()
        self.reset()


class Gun(GameSprite):
    def __init__(self, gun_img, knife_img, player, size_x, size_y, fire_speed):
        super().__init__(gun_img, player.rect.x, player.rect.y, size_x, size_y, fire_speed)
        self.player = player
        self.knife_img = knife_img

    def fire(self):
        knife = Knife(self.knife_img, self.rect.centerx - 10, self.rect.y, 20, 40, self.speed)
        Knifes.add(knife)
        f.play()

    def update(self, shift_x=0, shift_y=0):
        self.reset()
        self.rect.x = self.player.rect.x + shift_x
        self.rect.y = self.player.rect.y + shift_y


class Anim(sprite.Sprite):
    def __init__(self, nameAnimFolder, width, height, pos_x, pos_y, countSprite):
        super().__init__()
        self.animation_set = [transform.scale(image.load(f"{nameAnimFolder}/{i}.png"), (width, height)) for i in
                              range(countSprite)]

        self.x = pos_x
        self.y = pos_y
        self.cadr = 0

    def update(self):
        window.blit(self.animation_set[self.cadr], (self.x, self.y))
        self.cadr += 1
        if self.cadr > len(self.animation_set) - 1:
            self.kill()


animsHit = sprite.Group()


class Boss(GameSprite):
    def __init__(self, boss_img, boss_x, boss_y, size_x, size_y, live=5000, fire_speed=10, speed=4):
        super().__init__(boss_img, boss_x, boss_y, size_x, size_y, speed)
        self.live = live
        self.startLife = live
        self.BossIsDead = False
        self.bossKnifes = sprite.Group()
        self.fire_speed = fire_speed
        self.last_time = timer()

    direction = 'right'

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        if self.direction == "left":
            self.rect.x -= self.speed
        if self.rect.x > 700:
            self.direction = "left"
        elif self.rect.x < 0:
            self.direction = "right"
        if self.BossIsDead:
            return
        if self.live <= 0:
            self.BossIsDead = True
            self.rect.y = - 1000
        if self.live > self.startLife * 0.6:
            color_live = (0, 250, 0)
        elif self.live > self.startLife * 0.1:
            color_live = (250, 250, 0)
        else:
            color_live = (200, 0, 0)
        text = font3.render("BOSS: " + str(self.live), True, color_live)
        window.blit(text, (25, 145))

        now_time = timer()
        if now_time - self.last_time > 0.2:
            boss_knife = Knife("boss_knife.png", randint(self.rect.x, self.rect.right), self.rect.top, 60, 60,
                               -self.fire_speed)
            self.bossKnifes.add(boss_knife)
            self.last_time = timer()
        self.bossKnifes.update()
        self.reset()


font.init()
font2 = font.SysFont("Century Gothic", 40)
font3 = font.SysFont("Century Gothic", 30)
win_text = font2.render("Ти врятував світ і люди тобі вдячні!)", True,
                        (255, 255, 255))
win_text2 = font2.render("ТИ заслуговуєш ШАНИ и ПОВАГИ!! YOU ARE WINNER)", True,
                        (255, 255, 255))
win_secretext = font2.render("You saved world and killed terrorist!)", True, (25, 255, 255))
win_secretext2 = font2.render("Amazing! Like your present) U went secret finish", True, (25, 255, 255))
win_secretext3 = font2.render("CONGRATULATIONS! YOU WON!)", True, (25, 255, 255))
lose_text = font2.render("Terrorists killed you... ", True, (60, 200, 90))

lost = 0
score = 0

start_life = 2000
xp = start_life

run = True
clock = time.Clock()
finish = False
player = Player("man.png", win_width / 2, win_height - 100, 80, 120, 10)
gun = Gun('granata.png', 'granata.png', player, 20, 40, 10)
gun1 = Gun('винтовка.png', 'пуля.png', player, 100, 100, 10)
gun2 = Gun('винтовка2.png', 'пуля.png', player, 100, 100, 10)
gun3 = Gun('винтовка3.png', 'пуля.png', player, 100, 100, 10)
boss = Boss("boss.png", 350, -50, 250, 250)
guns = ['granata.png', 'винтовка.png', 'винтовка2.png', 'винтовка3.png']
num_skin = 0
Guns = sprite.Group()
for guns in Guns:
    Guns.add(guns)
Terrorists = sprite.Group()
monsters_img = ["killer.png", "knife_enemy.png", "dangerous.png"]
for i in range(20):
    terrorist = Enemy(choice(monsters_img), randint(0, win_width - 30), -50, 70, 130, randint(1, 5))
    Terrorists.add(terrorist)
Knifes = sprite.Group()
lifes = 5

rel_time = False
num_fire = 20



start_time_game = timer()

#!!!!!!!!!!!!
show_boss = True
#!!!!!!!!!!!!!
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire > 0 and rel_time == False:
                    gun1.fire()
                    num_fire -= 1

                if num_fire <= 0 and rel_time == False:
                    rel_time = True
                    last_time = timer()
            if e.key == K_1:
                num_skin += 1
                gun = Gun(guns[num_skin % len(guns)], 'granata.png', player, 20, 40, 10)
                gun1 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun2 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun3 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
            if e.key == K_2:
                num_skin += 1
                gun = Gun(guns[num_skin % len(guns)], 'granata.png', player, 20, 40, 10)
                gun1 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun2 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun3 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
            if e.key == K_3:
                num_skin += 1
                gun = Gun(guns[num_skin % len(guns)], 'granata.png', player, 20, 40, 10)
                gun1 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun2 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)
                gun3 = Gun(guns[num_skin % len(guns)], 'пуля.png', player, 100, 100, 10)



                '''if xp < 1000:
                                    knifes.fire()'''


    if not finish:
        window.blit(background, (0, 0))
        time = timer()
        player.update()
        gun1.update(-70, -40)
        Terrorists.update()
        Knifes.update()
        animsHit.update()

        collide = sprite.groupcollide(Terrorists, Knifes, True, True)
        for c in collide:
            score += 1
            if xp > 0:
                if score < 70:
                    terrorist = Enemy(choice(monsters_img), randint(0, win_width - 30), -50, 70, 130, randint(1, 5))
                    Terrorists.add(terrorist)

            x, y = c.rect.x, c.rect.y
            hit = Anim("anim", 130, 130, x, y, 49)
            animsHit.add(hit)

        collide = sprite.spritecollide(player, Terrorists, True)
        for c in collide:
            xp -= 100
            if xp > 0:
                if score < 70:
                    terrorist = Enemy(choice(monsters_img), randint(0, win_width - 30), -50, 70, 130, randint(1, 5))
                    Terrorists.add(terrorist)
            x, y = c.rect.x, c.rect.y
            hit = Anim("anim", 130, 130, x, y, 25)
            animsHit.add(hit)

        collide = sprite.groupcollide(Terrorists, Guns, True, True)
        for c in collide:
            score += 1
            if xp > 0:
                if score < 100:
                    terrorist = Enemy(choice(monsters_img), randint(0, win_width - 30), -50, 70, 130, randint(1, 5))
                    Terrorists.add(terrorist)
        color_patrons = (0, 250, 0)
        if num_fire <= 7:
            color_patrons = (250, 250, 0)
        elif num_fire == 3 or num_fire < 3:
            color_patrons = (255, 23, 23)

        text = font3.render("Kill: " + str(score), True, (255, 255, 255))
        window.blit(text, (25, 25))
        text = font3.render("Lost: " + str(lost), True, (233, 28, 0))
        window.blit(text, (25, 50))
        text = font3.render("Lifes: " + str(lifes), True, (233, 28, 0))
        window.blit(text, (650, 50))
        text = font3.render("Patrons: " + str(num_fire), True, color_patrons)
        window.blit(text, (650, 400))
        if lifes < 5:
            color_live = (0, 250, 0)
        elif lifes < 4:
            color_live = (250, 250, 0)
        elif lifes < 3:
            color_live = (200, 0, 0)

        if xp > start_life * 0.6:
            color_xp = (0, 250, 0)
        elif xp > start_life * 0.1:
            color_xp = (250, 250, 0)
        else:
            color_xp = (200, 0, 0)

        text = font3.render("Xp: " + str(xp), True, color_xp)
        window.blit(text, (25, 70))
        if lifes > 0:
            if xp < 0:
                xp = 2000
                lifes -= 1

        if score > 25:
            #!!!!!!!!!!!!!!!!!!!!!!
            if show_boss:
                message = QMessageBox()
                message.setText("Вітаю! Ви пройшли 1 рівень, вбивши 25 ворогів! На тебе чекає бос! Якщо здолаєш його, то врятуєш людей від тероризму, а якщо ні, то терористи підірвуть місто")
                message.setIcon(QMessageBox.Information)
                message.exec()
                show_boss = False
            #!!!!!!!!!!!!!!!!!!!!!!
            boss.update()
            collide = sprite.spritecollide(boss, Knifes, True)
            for c in collide:
                boss.live -= 100
                score += 5
                if num_skin % len(guns) == 0:
                    boss.live -= 50
                if num_skin % len(guns) == 1:
                    boss.live -= 100
                if num_skin % len(guns) == 2:
                    boss.live -= 200
                x, y = c.rect.x - 50, c.rect.y - 50
                hit = Anim("anim", 25, 25, x, y, 49)
                animsHit.add(hit)
            collide = sprite.spritecollide(player, boss.bossKnifes, True)
            for c in collide:
                xp -= 150
                x, y = c.rect.x - 50, c.rect.y - 50
                hit = Anim("anim", 25, 25, x, y, 49)
                animsHit.add(hit)
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                mixer.Sound("realod.mp3").play()
                text = font3.render("Realod ..." + str(3 - int(now_time - last_time)), True, (213, 79, 240))
                window.blit(text, (win_width / 2 - 50, win_height - 100))
            else:
                num_fire = 20
                rel_time = False
        if lifes <= 0:
            mixer.music.stop()
            window.blit(final, (0, 0))
            window.blit(lose_text, (150, 150))
            lose_sound.play()
            finish = True
        if boss.live <= 0:
            mixer.music.stop()
            window.blit(win_final, (0, 0))
            window.blit(win_text, (50, 250))
            window.blit(win_text2, (50, 350))
            win_sound.play()
            finish = True

        if score == 50 and timer() - start_time_game <= 20:
            mixer.music.stop()
            window.blit(win_secretfinal, (0, 0))
            window.blit(win_secretext, (150, 100))
            window.blit(win_secretext2, (20, 150))
            window.blit(win_secretext3, (150, 200))
            win_secretsound.play()
            win_secretsound.set_volume(0.1)
            finish = True

    display.update()
    clock.tick(60)
