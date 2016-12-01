#PROJECT 4 
import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 600
Y_MAX = 800

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

#---------------------------------------------------------------------

class EndGame(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Win(EndGame):
    def __init__(self):
        EndGame.__init__(self, "touchdown.png", (150, 150))


class Lost(EndGame):
    def __init__(self):
        EndGame.__init__(self, "gameover.png", (122, 120))

#---------------------------------------------------------------------

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location 
#----------------------------------------------------------------------

class FootballSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(FootballSprite, self).__init__()
        self.image = pygame.image.load("football.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-25)

    def update(self):
        x, y = self.rect.center
        y -= 20
        self.rect.center = x, y
        if y <= 0:
            self.kill()
#---------------------------------------------------------------------

class OSU_Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(OSU_Player, self).__init__()
        self.image = pygame.image.load("enemy_sprite2.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(4, 10)

        self.add(groups)
        self.playergrunt_sound = pygame.mixer.Sound("male_grunt.wav")
        self.playergrunt_sound.set_volume(0.4)


    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            self.velocity = random.randint(3, 6)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y

    def kill(self):
        x, y = self.rect.center
        if pygame.mixer.get_init():
            self.playergrunt_sound.play(maxtime=1000)
            #Explosion(x, y)
        super(OSU_Player, self).kill()

#-------------------------------------------------------------
class StatusSprite(pygame.sprite.Sprite):
    def __init__(self, mich_player, groups):
        super(StatusSprite, self).__init__()
        self.image = pygame.Surface((X_MAX, 30))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = 0, Y_MAX

        default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(default_font, 25)

        self.mich_player = mich_player
        self.add(groups)

    def update(self):
        score = self.font.render("Score : {} Health : {}".format(
            self.mich_player.score, self.mich_player.health), True, (0, 200, 0))
        self.image.fill((255, 255, 255))
        self.image.blit(score, (0, 0))
#------------------------------------------------------------------------------

class Mich_Player(pygame.sprite.Sprite):
    def __init__(self, groups, weapon_groups):
        super(Mich_Player, self).__init__()
        self.image = pygame.image.load("michplayer2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0
        self.firing = self.shot = False
        self.health = 10
        self.score = 0

        self.groups = [groups, weapon_groups]

        self.mega = 1

        self.autopilot = False
        self.in_position = False
        self.velocity = 2

    def reset(self):
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0

    def update(self):
        x, y = self.rect.center
    

        if (x >= 0) and (x <= X_MAX): #{ 

            if not self.autopilot:
                # Handle movement
                self.rect.center = x + self.dx, y + self.dy

                # Handle firing
                if self.firing:
                    self.shot = FootballSprite(x, y)
                    self.shot.add(self.groups)

                if self.health < 0:
                    self.kill()

            else:
                if not self.in_position:
                    if x != X_MAX/2:
                        x += (abs(X_MAX/2 - x)/(X_MAX/2 - x)) * 2
                    if y != Y_MAX - 100:
                        y += (abs(Y_MAX - 100 - y)/(Y_MAX - 100 - y)) * 2

                    if x == X_MAX/2 and y == Y_MAX - 100:
                        self.in_position = True
                else:
                    y -= self.velocity
                    self.velocity *= 1.5
                    if y <= 0:
                        y = -30
                self.rect.center = x, y

        else: #} #{
            if x < 0:
                x = 0
            else:
                x = X_MAX
            self.rect.center = x, y

        #}


    def steer(self, direction, operation):
        v = 10
        if operation == START:
            if direction in (UP, DOWN):
                self.dy = {UP: -v,
                           DOWN: v}[direction]

            if direction in (LEFT, RIGHT):
                self.dx = {LEFT: -v,
                           RIGHT: v}[direction]

        if operation == STOP:
            if direction in (UP, DOWN):
                self.dy = 0
            if direction in (LEFT, RIGHT):
                self.dx = 0

    def shoot(self, operation):
        if operation == START:
            self.firing = True
        if operation == STOP:
            self.firing = False



def main():
    BackGround = Background('bgfield.png', [0,0])
    game_over = False
    game_won = False
    winning_score = 800
    total_tries = 3

    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
    osu_players = pygame.sprite.Group()
    weapon_fire = pygame.sprite.Group()

    empty = pygame.Surface((X_MAX, Y_MAX))
    empty.set_alpha(0)
    clock = pygame.time.Clock()


    mich_player = Mich_Player(everything, weapon_fire)
    mich_player.add(everything)

    status = StatusSprite(mich_player, everything)

    deadtimer = 30
    credits_timer = 250
    playcount = 0

    for i in range(10):
        pos = random.randint(0, X_MAX)
        OSU_Player(pos, [everything, osu_players])

    # # Get some music
    # if pygame.mixer.get_init():
    #     pygame.mixer.music.load("DST-AngryMod.mp3")
    #     pygame.mixer.music.set_volume(0.8)
    #     pygame.mixer.music.play(-1)

    while True:
        screen.fill([0, 0, 0])
        screen.blit(BackGround.image, BackGround.rect)
        clock.tick(30)
        # Check for input
        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            if not game_over:
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        mich_player.steer(DOWN, START)
                    if event.key == K_LEFT:
                        mich_player.steer(LEFT, START)
                    if event.key == K_RIGHT:
                        mich_player.steer(RIGHT, START)
                    if event.key == K_UP:
                        mich_player.steer(UP, START)
                    if event.key == K_LCTRL: 
                        mich_player.shoot(START)
                    if event.key == K_RETURN:
                        if mich_player.mega:
                            mich_player.mega -= 1
                            for i in osu_players:
                                i.kill()

                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        mich_player.steer(DOWN, STOP)
                    if event.key == K_LEFT:
                        mich_player.steer(LEFT, STOP)
                    if event.key == K_RIGHT:
                        mich_player.steer(RIGHT, STOP)
                    if event.key == K_UP:
                        mich_player.steer(UP, STOP)
                    if event.key == K_LCTRL:
                        mich_player.shoot(STOP)

        # Check for impact
        hit_mich_players = pygame.sprite.spritecollide(mich_player, osu_players, True)
        for i in hit_mich_players:
            mich_player.health -= 15
        if mich_player.health < 0:
            if playcount < total_tries:
                mich_player.health = 10
                playcount +=1 
                #mich_player.reset()
                #for i in osu_players:
                    #i.kill()
            else:
                #touchdown = Touchdown(300,300)
                #screen.blit(touchdown.image, touchdown.rect)
                if deadtimer:
                    deadtimer -= 1
                else:
                    lost = Lost()
                    screen.blit(lost.image, lost.rect)

                    lose_sound = pygame.mixer.Sound("crowd_boo.wav")
                    lose_sound.set_volume(0.4)
                    lose_sound.play(maxtime=2500)
                    for i in osu_players:
                        i.kill()
                    game_over = True
                    

        # Check for successful attacks
        hit_mich_players = pygame.sprite.groupcollide(
            osu_players, weapon_fire, True, True)
        for k, v in hit_mich_players.items():
            k.kill()
            for i in v:
                i.kill()
                mich_player.score += 10

        if len(osu_players) < 20 and not game_over:
            pos = random.randint(0, X_MAX)
            OSU_Player(pos, [everything, osu_players])

        if mich_player.rect.center[1] < 130 or game_won == True: #check for touchdown
            game_won = True
            win = Win()
            screen.blit(win.image, win.rect)

            td_sound = pygame.mixer.Sound("football_crowd.wav")
            td_sound.set_volume(0.4)
            td_sound.play(maxtime=1000)


            game_over = True
            for i in osu_players:
                i.kill()

            mich_player.autopilot = True
            mich_player.shoot(STOP)


        # Check for game over
        if mich_player.score > winning_score:
            game_over = True
            for i in osu_players:
                i.kill()

            mich_player.autopilot = True
            mich_player.shoot(STOP)


            if credits_timer:
                credits_timer -= 1
            else:
                sys.exit()

        # Update sprites
        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
