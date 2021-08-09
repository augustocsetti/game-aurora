# Desenvolvido por Augusto
# Rodando em Python 3.6

import pygame as pg
import time
from os import path
from settings import *
from sprites import *

class Game:
        def __init__(self): # initialize game window, etc.

            pg.init()
            pg.mixer.init()
            self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
            pg.mouse.set_visible(False)
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
            self.running = True
            self.death = False
            self.load_data()

        def load_data(self): # load files/img

            # build img files
            self.dir = path.dirname(__file__)
            self.img_dir = path.join(self.dir, 'img')
            self.snd_dir = path.join(self.dir, 'snd')

                # background
            self.background = pg.image.load(path.join(self.img_dir, "background0.png")).convert()
            self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
            self.background_rect = self.background.get_rect()
            self.logo = pg.image.load(path.join(self.img_dir, "logo_aurora.png")).convert()
            self.logo.set_colorkey(BLACK)
            self.logo_rect = self.logo.get_rect()
            self.heart = pg.image.load(path.join(self.img_dir, "heart.png")).convert()
            self.heart.set_colorkey(BLACK)
            self.heart = pg.transform.scale(self.heart, (50, 50))
            self.heart_rect = self.background.get_rect()
            self.vazio = pg.image.load(path.join(self.img_dir, "vazio.png")).convert() # size: (100, 100)
            self.die = pg.image.load(path.join(self.img_dir, "die.png")).convert()
            self.die_rect = self.die.get_rect()
            self.encerramento = pg.image.load(path.join(self.img_dir, "encerramento.png")).convert()
            self.encerramento_rect = self.die.get_rect()
            self.gameover = pg.image.load(path.join(self.img_dir, "gameover.png")).convert()
            self.gameover_rect = self.gameover.get_rect()

                # msg
            self.dialog_box = pg.image.load(path.join(self.img_dir, "balao_fala.png")).convert()
            self.dialog_box_rect = self.dialog_box.get_rect()
            self.dialog_box_rect = (0, 3)
            self.dialog_box2 = pg.image.load(path.join(self.img_dir, "balao_fala2.png")).convert()
            self.dialog_box_rect2 = self.dialog_box2.get_rect()
            self.dialog_box_rect2 = (0, 3)

                # player
                    # stand
            self.standing_frames = [pg.image.load(path.join(self.img_dir, "personagem1-1.png")).convert()]
            for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
                    # right
            self.walk_frames_r = [pg.image.load(path.join(self.img_dir, "personagem1-r1.png")).convert(),
                                  pg.image.load(path.join(self.img_dir, "personagem1-r2.png")).convert(),
                                  pg.image.load(path.join(self.img_dir, "personagem1-r3.png")).convert()]
            for frame in self.walk_frames_r:
                frame.set_colorkey(BLACK)
                    # left
            self.walk_frames_l = []
            for frame in self.walk_frames_r:
                self.walk_frames_l.append(pg.transform.flip(frame, True, False))

                # Lvl_1: house_1

            self.background_house = pg.image.load(path.join(self.img_dir, "parede1.png")).convert()
            self.background_house = pg.transform.scale(self.background_house, (300, HOUSE_HEIGHT))
            self.door_2d = pg.image.load(path.join(self.img_dir, "door_house_0.png")).convert()
            self.door_2d = pg.transform.scale(self.door_2d, (DOOR_WIDTH, DOOR_HEIGHT))
            self.floor = pg.image.load(path.join(self.img_dir, "floor.png")).convert()
            self.tv = pg.image.load(path.join(self.img_dir, "tv.png")).convert()
            self.book = pg.image.load(path.join(self.img_dir, "book.png")).convert()
            self.table = pg.image.load(path.join(self.img_dir, "mesa.png")).convert()
            self.table = pg.transform.scale(self.table, (60, 60))

                # book

            self.book_open0 = pg.image.load(path.join(self.img_dir, "book_open0.png")).convert()
            self.book_open1 = pg.image.load(path.join(self.img_dir, "book_open1.png")).convert()
            self.book_open2 = pg.image.load(path.join(self.img_dir, "book_open2.png")).convert()
            self.book_open3 = pg.image.load(path.join(self.img_dir, "book_open3.png")).convert()
            self.book_open4 = pg.image.load(path.join(self.img_dir, "book_open4.png")).convert()
            self.book_open5 = pg.image.load(path.join(self.img_dir, "book_open5.png")).convert()

                # item

            self.item1 = pg.image.load(path.join(self.img_dir, "termometro.png")).convert()
            self.item2 = pg.image.load(path.join(self.img_dir, "desmatamento.png")).convert()
            self.item2 = pg.transform.scale(self.item2, (350, 250))
            self.item3 = pg.image.load(path.join(self.img_dir, "fabrica.jpg")).convert()
            self.item3 = pg.transform.scale(self.item3, (380, 220))
            self.item4 = pg.image.load(path.join(self.img_dir, "item4.png")).convert()
            self.item4 = pg.transform.scale(self.item4, (380, 275))
            self.item5 = pg.image.load(path.join(self.img_dir, "artigo.png"))

                # Lvl_1: city_pt_1

            self.house1_img = pg.image.load(path.join(self.img_dir, "house1-1.png")).convert()
            self.house1_img = pg.transform.scale(self.house1_img, (300, HOUSE_HEIGHT))
            self.street = pg.image.load(path.join(self.img_dir, "street.png")).convert()
            self.street = pg.transform.scale(self.street, (WIDTH, HEIGHT - FLOOR))
            self.casa_cenario1 = pg.image.load(path.join(self.img_dir, "casa_cenario1.png")).convert()
            self.casa_cenario2 = pg.image.load(path.join(self.img_dir, "casa_cenario2.png")).convert()
            self.casa_cenario3 = pg.image.load(path.join(self.img_dir, "casa_cenario3.png")).convert()
            self.placa = pg.image.load(path.join(self.img_dir, "placa.png")).convert()
            self.placa = pg.transform.scale(self.placa, (45, 63))
            self.jornal = pg.image.load(path.join(self.img_dir, "jornal.png")).convert()
            self.jornal = pg.transform.scale(self.jornal, (HEIGHT - 50, HEIGHT - 50))

                # Lvl_1: city_pt_2

            self.build = pg.image.load(path.join(self.img_dir, "build.jpg")).convert()
            self.build_door = pg.image.load(path.join(self.img_dir, "build_door.jpg")).convert()
            #self.car = pg.image.load(path.join(self.img_dir, "carro.png")).convert()

                # Lvl_1: build_1
            self.build_window_inside = pg.image.load(path.join(self.img_dir, "build_window_inside.png")).convert()
            self.build_window_inside_door0 = pg.image.load(path.join(self.img_dir, "build_window_inside_door0.png")).convert()
            self.build_window_inside_door1 = pg.image.load(path.join(self.img_dir, "build_window_inside_door1.png")).convert()
            self.build_wall = pg.image.load(path.join(self.img_dir, "build_wall.jpg")).convert()
            self.build_plat = pg.image.load(path.join(self.img_dir, "plat_build.png")).convert()
            self.build_plat = pg.transform.scale(self.build_plat, (70, DOOR_WIDTH + 8))

            # load sounds
            self.channel1 = pg.mixer.Channel(0)
            self.channel2 = pg.mixer.Channel(1)

            self.ss_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Background Growl.ogg'))
            pg.mixer.music.load(path.join(self.snd_dir, 'Kim Lightyear - And Then We Left.ogg'))
            self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump5.wav'))
            self.step_sound = pg.mixer.Sound(path.join(self.snd_dir, 'sfx_step_grass_l.wav'))
            self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Death.ogg'))
            self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Hit.ogg'))
            self.door_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Door.ogg'))
            self.brokenwindow_sound = pg.mixer.Sound(path.join(self.snd_dir, 'glass_breaking.ogg'))
            self.the_end_sound = pg.mixer.Sound(path.join(self.snd_dir, 'the_end.ogg'))
            self.page_sound = pg.mixer.Sound(path.join(self.snd_dir, 'BookFlip2.ogg'))
            self.item1_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Menu2A.ogg'))
            self.open_sound = pg.mixer.Sound(path.join(self.snd_dir, 'awesomeness.ogg'))

        def show_start_screen(self): # game splash/start screen

            self.logo_rect = (50, 50)
            self.screen.blit(self.background, self.background_rect)
            self.screen.blit(self.logo, self.logo_rect)

            self.draw_text("Pressione ENTER para iniciar", 36, WHITE, WIDTH / 2, HEIGHT - 100)
            self.channel1.play(self.open_sound, loops=-1)
            pg.display.flip()
            self.wait_for_key()
            self.channel1.fadeout(200)

        def new(self): # start a new Game

            if not self.death:
                self.encerramento_check = False

                # condition used in colisions with walls and ceilings
                self.hits_wall_check = False
                self.hits_ceiling_check = False
                self.hits_special_check = False
                self.hits_door_check = False
                self.hits_door_scenario_check = False

                self.compass = 0
                self.hurt = False

                # dialogues
                self.dialog_intro = False #ATENÇÃO
                self.dialog_house_1 = False #ATENÇÃO
                self.dialog_jornal = False
                self.dialog_city_1 = False #ATENÇÃO
                self.dialog_city_2 = False #ATENÇÃO
                self.dialog_too_small = True
                self.dialog = ''

                # group with all sprites
                self.all_sprites = pg.sprite.Group()
                self.scenarios = pg.sprite.Group()

                # groups with interactives objects
                self.objects_notouch = pg.sprite.Group()
                self.doors = pg.sprite.Group()
                self.specials = pg.sprite.Group()
                self.door_scenarios = pg.sprite.Group()

                # groups to scenarios (walls, ceilings and platforms)
                self.platforms = pg.sprite.Group()
                self.walls = pg.sprite.Group()
                self.ceilings = pg.sprite.Group()

                # initialize intro
                if not self.dialog_intro:
                    self.place = 'intro'
                    self.msg(self.place)

                # call objects in scenario and initialize player
                pg.mixer.music.play(loops=-1)
                self.place = 'house_1'
                self.player = Player(self)
                self.lvl = Lvl_1(self)
                self.life_point = 3

                self.scenarios.add(self.objects_notouch, self.doors, self.platforms, self.walls, self.ceilings, self.specials)
                self.all_sprites.add(self.player, self.scenarios, self.lvl)
            self.death = False
            self.run()

        def run(self): # game loop

            self.playing = True
            while self.playing:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
            pg.mixer.music.fadeout(500)

        def events(self): # game loop - events

            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.playing:
                            self.playing = False
                        self.running = False
                    if event.key == pg.K_UP:
                        self.player.jump()
                    if event.key == pg.K_d and self.lvl.get_book:
                        self.lvl.read_book()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.player.jump_cut()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_a or event.key == pg.K_s:
                        self.lvl.update_scenario(event.key)

        def update (self): # game loop - update

            self.all_sprites.update()

            # check if player hits a platform - only it falling
            if self.player.vel.y > 0:
                hits_plat = pg.sprite.spritecollide(self.player, self.platforms, False)
                if hits_plat:
                    # condition to choise which platform go on (the lower)
                    lowest = hits_plat[0]
                    for hit in hits_plat:
                        # only stay if foot is uper
                        if hit.rect.bottom < lowest.rect.centery:
                            lowest = hit
                    # DIE
                    if self.player.vel.y > 30 and self.player.vel.y < 40:
                        self.channel1.play(self.hit_sound)
                        self.life_point -= 1
                        self.hurt = True
                    elif self.player.vel.y >= 45 and self.player.vel.y < 55:
                        self.channel1.play(self.hit_sound)
                        self.life_point -= 2
                        self.hurt = True
                    elif self.player.vel.y >= 60:
                        self.channel1.play(self.death_sound)
                        self.life_point -= 3
                        self.hurt = True
                    if self.life_point <= 0:
                        self.channel1.play(self.death_sound)
                        time.sleep(0.5)
                        self.playing = False

                    if self.hurt:
                        self.screen.blit(self.die, self.die_rect)
                        self.hurt = False

                        pg.display.flip()

                    if self.player.pos.y < hits_plat[0].rect.bottom:
                        self.player.pos.y = hits_plat[0].rect.top + 8
                        self.player.vel.y = 0
                        self.player.jumping = False

            self.hits_ceiling_check = False

            # check if player hits a wall
            hits_wall = pg.sprite.spritecollide(self.player, self.walls, False)
            if hits_wall:
                self.hits_wall_check = True
            else:
                self.hits_wall_check = False

            # check if player hits a ceiling
            hits_ceiling = pg.sprite.spritecollide(self.player, self.ceilings, False)
            if hits_ceiling:
                self.hits_ceiling_check = True
            else:
                self.hits_ceiling_check = False

            # check if player hits a door
            hits_door = pg.sprite.spritecollide(self.player, self.doors, False)
            if hits_door:
                self.hits_door_check = True
            else:
                self.hits_door_check = False

            # check if player hits a scenario's door
            hits_door_scenario = pg.sprite.spritecollide(self.player, self.door_scenarios, False)
            if hits_door_scenario:
                self.hits_door_scenario_check = True
            else:
                self.hits_door_scenario_check = False

            # if the player reaches top 1/4 of screen
            if self.player.rect.top <= HEIGHT / 4:
                self.player.pos.y += max(abs(self.player.vel.y), 10)
                self.compass += max(abs(self.player.vel.y), 10)
                for elem in self.scenarios:
                    elem.rect.y += max(abs(self.player.vel.y), 10)

            # if the player reaches top 3/4 of screen
            if self.player.rect.bottom > HEIGHT / 2 and self.compass != 0:
                if self.compass > 0:
                    self.player.pos.y -= max(abs(self.player.vel.y), 20)
                    self.compass -= max(abs(self.player.vel.y), 20)
                    for elem in self.scenarios:
                        elem.rect.y -= max(abs(self.player.vel.y), 20)
                else:
                    for elem in self.scenarios:
                        elem.rect.y -= self.compass
                    self.compass = 0

        def draw(self): # game loop - draw

            self.screen.fill(BLACK)

            if self.place == 'house_1':
                self.screen.fill(BLACK)
            elif self.place == 'city_pt_1':
                self.screen.blit(self.background, self.background_rect)
            elif self.place == 'city_pt_2':
                self.screen.blit(self.background, self.background_rect)
            elif self.place == 'build_1':
                self.screen.fill(BLACK)

            self.scenarios.draw(self.screen)

            # life points
            x = WIDTH // 20
            c = 1
            while c <= self.life_point:
                if c == 1:
                    self.heart_rect = (x, HEIGHT // 10)
                    self.screen.blit(self.heart, self.heart_rect)
                if c == 2:
                    x += 50
                    self.heart_rect = (x, HEIGHT // 10)
                    self.screen.blit(self.heart, self.heart_rect)
                if c == 3:
                    x += 50
                    self.heart_rect = (x, HEIGHT // 10)
                    self.screen.blit(self.heart, self.heart_rect)
                c += 1

            self.screen.blit((self.player.image), (self.player.rect))
            self.screen.blit(self.heart, self.heart_rect)

            pg.display.flip()

            if not self.dialog_city_1 and self.place == 'city_pt_1':

                self.screen.blit((self.player.image), (self.player.rect))
                self.screen.blit(self.heart, self.heart_rect)

                pg.display.flip()

                self.walking = False
                self.channel2.fadeout(10)
                self.player.vel.x = 0
                time.sleep(2) #ATENÇÃO
                self.msg(self.place)

        def msg(self, place):

            # dialogue intro
            #soundvoicesandnoises
            if place == 'intro':
                self.screen.fill(BLACK)
                #APAGARself.channel1.play(self.intro_sound, loops=-1)
                pg.display.flip()
                time.sleep(3) #ATENÇÃO
            while not self.dialog_intro and place == 'intro':
                self.screen.fill(BLACK)
                falas = [('Olá, seja bem vinda(o)!'),
                         ('Nesta aventura você controlorá as ações de Dona Aurora, uma pobre senhora que está tendo um dia bem atípico.'),
                         ('Sua tarefa é ajudá-la a encontrar o que procura e entender o que está acontecendo.'),
                         ('Tenham uma boa sorte.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_intro = True

                self.screen.fill(BLACK)
                pg.display.flip()
                time.sleep(4) #ATENÇÃO

            # dialogue house_1
            while not self.dialog_house_1 and place == 'house_1':
                falas = [('Ah, Deus...'),
                        ('Que dor! Minhas costas estão me matando..'),
                        ('Ué?!'),
                        ('Onde está meu filho, Lavi?! Ele saiu ontem a tarde e ainda não voltou..'),
                        ('Bom.. vou lá fora para ver como está o tempo e se aquele pestinha está por perto..'),
                        ('-- Use a tecla "A" para abrir portas. --'),
                        ('-- "S" para interagir com o cenário. --')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_house_1 = True

            # dialogue house_1
            if place == 'get_book':
                falas = [('Hm, não é esse o livro que eu estava pensando, mas com certeza o Lavi também vai gostar de saber seu conteúdo.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

            # dialogue city 1
            while not self.dialog_city_1 and place == 'city_pt_1':
                falas = [('Nossa..'),
                        ('O que aconteceu aqui? A cidade está tão deserta e suja'),
                        ('também nem sinal do Lavi, onde será que ele se meteu?!'),
                        ('Hmm.. vou dar uma olhada naquele jornal.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_city_1 = True

            # dialogue newspapper
            while not self.dialog_jornal and place == 'jornal':

                falas = [('Não há mais volta?! \'haha\' Os jovens hoje em dia são tão dramáticos, aiai..'),
                        ('Mas o clima está realmente estranho hoje.. tão abafado e tudo parece morto, sinto uma tristeza de final de domingo'),
                        ('Estou começando a ficar preocupada com Lavi.. onde foi que aquele demoninho se meteu..'),
                        ('Talvez esteja no terraço da fábrica.. lembro que quando ela funcionava, meu Lavi gostava de subir até lá.'),
                        ('Antes de ir é bom eu pegar o livro que ele gosta de ler comigo.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_jornal = True

            # dialogue build
            while not self.dialog_city_2 and place == 'city_pt_2':

                falas = [('Porco dio! Ele também não está aqui.'),
                        ('E a cidade está realmente uma bagunça, até onde dá para ver só tem sujeira..'),
                        ('Vou anotar isso que estou percebendo, para depois fazer uma reclamação. Naquele livro que tenho têm coisas que se referem a isso.'),
                        ('Não consigo mais ver nem o lago e a reserva onde eu ia namorar na minha juventude \'hehe\' Bons tempos...'),
                        ('Bom, não vou desistir de meu pobre Lavi, é bom eu descer logo e seguir procurando..'),
                        ('Garanto que ele está com sede. Até eu estou com esse tempo raro que faz hoje.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_city_2 = True

            # dialogue too small
            while not self.dialog_too_small and place == 'small':
                self.channel1.play(self.door_sound)
                falas = [('Lavi não deve ter entrado aqui, esse lugar parece estar lacrado.')]

                for elem in falas:
                    self.screen.blit(self.dialog_box2, self.dialog_box_rect2)
                    self.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
                    pg.display.flip()
                    self.wait_for_key()

                self.dialog_too_small = True

        def show_gameover_screen(self): # game over/continue

            if not self.running:
                return

            self.walking = False
            self.channel2.fadeout(10)
            self.player.vel.x = 0
            self.channel1.play(self.the_end_sound, loops=-1)

            # win
            if self.encerramento_check:
                self.screen.blit(self.encerramento, self.encerramento_rect)
                pg.display.flip()
                self.wait_for_key()
                self.running = False
                self.channel1.fadeout(200)

            # game over
            else:
                self.screen.blit(self.gameover, self.gameover_rect)
                pg.display.flip()
                self.wait_for_key()
                self.channel1.fadeout(200)

                pg.mixer.music.play(loops=-1)
                self.life_point = 3
                self.playing = True
                self.running = True
                self.death = True
                self.player.vel.y = 0

        def wait_for_key(self):

            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        self.running = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.playing = False
                            self.running = False
                            waiting = False
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_RETURN:
                            waiting = False

        def draw_text(self, text, size, color, x, y):

            font = pg.font.Font(pg.font.match_font('lunchds.ttf'), size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x, y)
            self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover_screen()

pg.quit()
