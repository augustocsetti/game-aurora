# sprite classes for platform game

import pygame as pg
import time
from os import path
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):

        pg.sprite.Sprite.__init__(self)
        self.game = game
        # used in animation
        self.current_frame = 0
        self.last_update = 0
        self.side = 0
        self.walking = False
        self.jumping = False
        #self.change_door = False

        # character
        self.image = self.game.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (QUARTERSCREEN_X - 180, FLOOR)
        self.pos = vec(self.rect.midbottom)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):

        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.channel1.play(self.game.jump_sound)
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):

        if self.jumping:
            # if it still uping
            if self.vel.y < -2:
                #
                self.vel.y = self.vel.y / 1.5

    def update(self): # movement

        # animation
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        # motion x
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        if self.game.hits_wall_check:
            if self.side == -1 and self.acc.x > 0:
                self.side = 1
                self.game.hits_wall_check = False
                self.pos.x += 5

            elif self.side == 1 and self.acc.x < 0:
                self.side = -1
                self.game.hits_wall_check = False
                self.pos.x += -5


        if self.game.hits_wall_check:
            self.vel.x = 0
            self.acc.x = 0
            self.pos.x += 0

        # condition to stop (to print standing_frames)
        if abs(self.vel.x) < 0.7:
            self.vel.x = 0
            self.walking = False

        # equations of motion x
        if not self.game.hits_wall_check:

            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            #equations of motion x
            self.vel.x += self.acc.x
            self.pos.x += self.vel.x + 0.5 * self.acc.x

        # define self.side
        if self.vel.x > 0:
            self.side = 1
        elif self.vel.x < 0:
            self.side = -1

        # motion y
        # if hits any ceiling stop going up
        if self.game.hits_ceiling_check:
            self.vel.y = 0
            self.pos.y += 5
        else:
        # equations of motion y
            if self.vel.y < 60:
                self.vel.y += self.acc.y
                self.pos.y += self.vel.y + 0.5 * self.acc.y
            else:
                self.vel.y = 60
                self.pos.y += self.vel.y

        self.game.lvl.update_scenario(0)

        self.rect.midbottom = self.pos

    def animate(self):

        # time since pg init
        now = pg.time.get_ticks()
        # condition to walk
        if self.vel.x != 0 and self.jumping == False:
            self.walking = True
            #self.game.channel2.play(self.game.step_sound, loops=-1)
        elif self.vel.x != 0 and self.jumping == True:
            self.walking = True
            self.game.channel2.fadeout(10)
        elif self.vel.x == 0 and self.jumping == False:
            self.walking = False
            #self.game.channel2.fadeout(10)
        # show walking animation
        if self.walking:
            if now - self.last_update > 140:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.walk_frames_l)
                bottom = self.rect.bottom
                # change the image (left or right)
                if self.vel.x > 0:
                    self.image = self.game.walk_frames_r[self.current_frame]
                else:
                    self.image = self.game.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()

                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            # self.last_update to count program time (miliseconds)
            if now - self.last_update > 350:
                self.last_update = now
                # if reach the limit of the list it needs to start again
                self.current_frame = (self.current_frame + 1) % len(self.game.standing_frames)
                # search for the bottom initial and keep it for the next frame
                bottom = self.rect.bottom
                self.image = self.game.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                # relocate image to floor
                self.rect.bottom = bottom

class Lvl_1(pg.sprite.Sprite):
    def __init__(self, game):

        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.window_open = False
        self.get_book = False
        self.item = False
        self.get_item1 = False
        self.get_item2 = False
        self.get_item3 = False
        self.get_item4 = False
        self.get_item5 = False
        self.House_1()

    def House_1(self):

        # cleaning up scenario
        for group in self.game.scenarios:
            group.kill()

        if not self.get_item1:
            item = pg.transform.scale(self.game.item1, (34,15))
            self.item1 = Get_image(self.game, item, QUARTERSCREEN_X - 75, FLOOR_OBJ - 40, True)
            self.game.specials.add(self.item1)

        # loading and organizing images on the screen
        wall1 = Wall(QUARTERSCREEN_X - 300, FLOOR - HOUSE_HEIGHT , WALL_WIDTH, HOUSE_HEIGHT)
        wall2 = Wall(QUARTERSCREEN_X - 8, FLOOR - HOUSE_HEIGHT, WALL_WIDTH, HOUSE_HEIGHT)
        ceiling = Wall(QUARTERSCREEN_X - 300, FLOOR - HOUSE_HEIGHT, 300, WALL_WIDTH)
        floor = Platform(0, FLOOR, WIDTH, 20)

        # setting images scenario (midbottom)
        #img = Get_image(self.game, self.game., x_midbottom, y_midbottom)
        self.game.floor = pg.transform.scale(self.game.floor, (300 - 2*WALL_WIDTH, self.game.floor.get_height()))
        floor_img = Get_image(self.game, self.game.floor, QUARTERSCREEN_X - 150, FLOOR + 71, False)
        door1 = Get_image(self.game, self.game.door_2d, QUARTERSCREEN_X - 3, FLOOR, True)
        background_house = Get_image(self.game, self.game.background_house, QUARTERSCREEN_X - 150, FLOOR, False)
        tv = Get_image(self.game, self.game.tv, QUARTERSCREEN_X - 60, FLOOR_OBJ + 35, True)
        mesa = Get_image(self.game, self.game.table, QUARTERSCREEN_X - 240, FLOOR_OBJ - 3, True)

        if not self.get_book:
            book = pg.transform.scale(self.game.book, (35,35))
            self.book = Get_image(self.game, book, QUARTERSCREEN_X - 250, FLOOR + 40, True)
            self.game.specials.add(self.book)

        self.game.objects_notouch.add(background_house)
        self.game.specials.add()
        self.game.doors.add(door1)
        self.game.platforms.add(floor, floor_img)
        self.game.walls.add(wall1, wall2)
        self.game.ceilings.add(ceiling)
        self.game.door_scenarios.add(tv, mesa)
        self.game.scenarios.add(self.game.objects_notouch, self.game.platforms, self.game.walls, self.game.ceilings, self.game.doors, self.game.specials, self.game.door_scenarios)

        if not self.game.dialog_house_1:

            self.game.scenarios.draw(self.game.screen)
            self.game.screen.blit((self.game.player.image), (self.game.player.rect))
            pg.display.flip()
            time.sleep(1)

            self.game.msg(self.game.place)

    def City_pt_1(self):

        # cleaning up scenario
        for group in self.game.scenarios:
            group.kill()

        wall_end = Wall(-20, 0, 20, HEIGHT)
        floor = Platform(0, FLOOR, WIDTH, 200)
        vazio_new = pg.transform.scale(self.game.vazio, (55, 80))
        self.vazio = Get_image(self.game, vazio_new, (WIDTH * 4) // 8 + 24, FLOOR + 5, True)
        door_sc_new = pg.transform.scale(self.game.vazio, (62, 100))
        door_sc1 = Get_image(self.game, door_sc_new, (WIDTH * 3) // 8 - (self.game.casa_cenario1.get_width()/4) - 10, FLOOR, True)
        door_sc2 = Get_image(self.game, door_sc_new, (WIDTH * 6) // 8 + (self.game.casa_cenario2.get_width()/4) - 30, FLOOR, True)

        # setting images scenario
        door1 = Get_image(self.game, self.game.door_2d, QUARTERSCREEN_X - 10, FLOOR + 5, True)
        house1_img = Get_image(self.game, self.game.house1_img, QUARTERSCREEN_X - 150, FLOOR + 5, True)
        street = Get_image(self.game, self.game.street, WIDTH / 2, HEIGHT, False)
        casa_cenario1 = Get_image(self.game, self.game.casa_cenario1, (WIDTH * 3) // 8, FLOOR + 10, True)
        casa_cenario2 = Get_image(self.game, self.game.casa_cenario2, (WIDTH * 6) // 8 , FLOOR + 4, True)
        placa = Get_image(self.game, self.game.placa, (WIDTH * 4) // 8 + 24, FLOOR + 5, True)

        self.game.objects_notouch.add(street, house1_img, casa_cenario1, casa_cenario2, placa)
        self.game.specials.add(self.vazio)
        self.game.doors.add(door1)
        self.game.platforms.add(floor)
        self.game.walls.add(wall_end)
        self.game.ceilings.add()
        self.game.door_scenarios.add(door_sc1, door_sc2)
        self.game.scenarios.add(self.game.platforms, self.game.walls, self.game.ceilings, self.game.objects_notouch, self.game.doors, self.game.door_scenarios)

    def City_pt_2(self):

        # cleaning up scenario
        for group in self.game.scenarios:
            group.kill()

        if not self.get_item2:
            item = pg.transform.scale(self.game.item2, (20,10))
            self.item2 = Get_image(self.game, item, WIDTH / 2 - 40, FLOOR_OBJ + 6, False)
            self.game.specials.add(self.item2)

        if not self.get_item5:
            item = pg.transform.scale(self.game.item5, (10,15))
            self.item5 = Get_image(self.game, item, WIDTH * (3/4), FLOOR_OBJ - 30, True)
            self.game.specials.add(self.item5)

        # condition to win game
        if not self.game.dialog_city_2:
            wall_end = Wall(WIDTH, 0, WALL_WIDTH, HEIGHT)
            self.game.walls.add(wall_end)
            self.look_someone = Get_image(self.game, self.game.vazio, CENTER_BUILD_X + BUILD_WIDTH / 2 - self.game.vazio.get_width()/2, BUILD_Y - DOOR_WIDTH, True)
            self.game.specials.add(self.look_someone)

        wall_start = Wall(-WALL_WIDTH, BUILD_Y - 300, WALL_WIDTH, -(BUILD_Y - 300) + HEIGHT - 450)
        door_sc_new = pg.transform.scale(self.game.vazio, (40, 100))
        door_sc3 = Get_image(self.game, door_sc_new, (WIDTH * 6) // 8 + 40, FLOOR, True)

        street = Get_image(self.game, self.game.street, WIDTH / 2, HEIGHT, False)
        build = Get_image(self.game, self.game.build, CENTER_BUILD_X, FLOOR, False)
        door = Get_image(self.game, self.game.build_door, CENTER_BUILD_X, FLOOR, False)
        casa_cenario3 = Get_image(self.game, self.game.casa_cenario3, (WIDTH * 6) // 8 , FLOOR + 13, True)
        plat_top_img = pg.transform.scale(self.game.build_plat, (200, DOOR_WIDTH + 10))
        plat_top = Get_image(self.game, plat_top_img, CENTER_BUILD_X + BUILD_WIDTH // 4, BUILD_Y, False)

        windows = []

        x_pos = 1
        y_pos = 0
        for x in range (CENTER_BUILD_X - self.game.build_wall.get_width() // 2 + 71, CENTER_BUILD_X + self.game.build_wall.get_width() // 2, 129):
            for y in range (FLOOR - 272, FLOOR - 2000, - 193):
                if (x_pos, y_pos) != (1,8):
                    win = Get_image(self.game, self.game.build_window_inside, x, y, True)
                    windows.append(win)
                else:
                    if self.window_open == True:
                        window = Get_image(self.game, self.game.build_window_inside_door1, x, y, True)
                    else:
                        window = Get_image(self.game, self.game.build_window_inside_door0, x, y, True)
                y_pos += 1
            x_pos += 1
            y_pos = 1
        x_pos = 1
        y_pos = 1

        plat_win = pg.transform.scale(self.game.build_plat, (65, DOOR_WIDTH))
        plat_window_support = pg.transform.scale(self.game.vazio, (65, DOOR_WIDTH + 50))
        for x in range (CENTER_BUILD_X - self.game.build_wall.get_width() // 2 + 71, CENTER_BUILD_X + self.game.build_wall.get_width() // 2, 129):
            for y in range (FLOOR - BUILD_FRIST_FLOOR - BUILD_TOTAL // 9, FLOOR - self.game.build_wall.get_height(), - BUILD_TOTAL // 9):
                if x_pos == 1 and y_pos == 8:
                    plat_window = Get_image(self.game, plat_win, x, y, False)
                    plat_top_base = Get_image(self.game, plat_window_support, x, y + 50, True)
                y_pos += 1
            x_pos += 1
            y_pos = 1

        # setting images scenario (midbottom)
        self.game.objects_notouch.add(casa_cenario3, build, plat_window, windows)
        self.game.specials.add()
        self.game.doors.add(door, window)
        self.game.platforms.add(street, plat_top, plat_top_base)
        self.game.walls.add(wall_start)
        self.game.ceilings.add()
        self.game.door_scenarios.add(door_sc3)
        self.game.scenarios.add(self.game.objects_notouch, self.game.platforms, self.game.walls, self.game.ceilings, self.game.doors, self.game.specials, self.game.door_scenarios)

        if self.window_open == True and self.game.compass != 0:
            for elem in self.game.scenarios:
                elem.rect.y += self.game.compass

    def Build_1(self):

        for group in self.game.scenarios:
            group.kill()

        if not self.get_item3:
            item = pg.transform.scale(self.game.item3, (60,30))
            self.item3 = Get_image(self.game, item, CENTER_BUILD_X + 100, FLOOR_OBJ - 40, True)
            self.game.specials.add(self.item3)

        floor = Platform(0, FLOOR, WIDTH, 200)
        wall1 = Wall(CENTER_BUILD_X - (self.game.build_wall.get_width() / 2 + WALL_WIDTH / 2), -self.game.build_wall.get_height() + FLOOR, WALL_WIDTH, self.game.build_wall.get_height())
        wall2 = Wall(CENTER_BUILD_X + (self.game.build_wall.get_width() / 2 - WALL_WIDTH / 2), -self.game.build_wall.get_height() + FLOOR, WALL_WIDTH, self.game.build_wall.get_height())
        ceiling = Wall(CENTER_BUILD_X - (self.game.build_wall.get_width() / 2 + WALL_WIDTH / 2),  -self.game.build_wall.get_height() + FLOOR, self.game.build_wall.get_width(), WALL_WIDTH)

        door = Get_image(self.game, self.game.build_door, WIDTH / 4, FLOOR, False)
        build_wall = Get_image(self.game, self.game.build_wall, CENTER_BUILD_X, FLOOR, False)
        floor = pg.transform.scale(self.game.floor, (BUILD_WIDTH, HEIGHT - FLOOR))
        floor_img = Get_image(self.game, floor, CENTER_BUILD_X, HEIGHT, False)

        plat1 = Get_image(self.game, self.game.build_plat, CENTER_BUILD_X, FLOOR - 220, False)
        windows = []
        plats = []

        x_pos = 1
        y_pos = 0
        for x in range (CENTER_BUILD_X - self.game.build_wall.get_width() // 2 + 71, CENTER_BUILD_X + self.game.build_wall.get_width() // 2, 129):
            for y in range (FLOOR - 272, FLOOR - 2000, - 193):
                if (x_pos, y_pos) != (1,8):
                    win = Get_image(self.game, self.game.build_window_inside, x, y, True)
                    windows.append(win)
                else:
                    if self.window_open == True:
                        window = Get_image(self.game, self.game.build_window_inside_door1, x, y, True)
                    else:
                        window = Get_image(self.game, self.game.build_window_inside_door0, x, y, True)
                y_pos += 1
            x_pos += 1
            y_pos = 1

        x_pos = 1
        y_pos = 1
        self.game.build_plat = pg.transform.scale(self.game.build_plat, (60, DOOR_WIDTH + 10))
        for x in range (CENTER_BUILD_X - self.game.build_wall.get_width() // 2 + 71, CENTER_BUILD_X + self.game.build_wall.get_width() // 2, 129):
            for y in range (FLOOR - BUILD_FRIST_FLOOR - BUILD_TOTAL // 9, FLOOR - self.game.build_wall.get_height(), - BUILD_TOTAL // 9):
                if (x_pos, y_pos) not in ((2,1), (1,2), (1,3), (3,3), (2,4), (2,5), (2,6), (1,6), (3,7), (2,8), (3,8)):
                    plat = Get_image(self.game, self.game.build_plat, x, y, False)
                    plats.append(plat)
                y_pos += 1
            x_pos += 1
            y_pos = 1

        self.game.objects_notouch.add(build_wall, door, windows, floor_img)
        self.game.specials.add()
        self.game.doors.add(door, window)
        self.game.platforms.add(floor_img, plat1, plats)
        self.game.walls.add(wall1, wall2)
        self.game.ceilings.add(ceiling)
        self.game.door_scenarios.add()
        self.game.scenarios.add(self.game.objects_notouch, self.game.platforms, self.game.walls, self.game.ceilings, self.game.doors, self.game.specials, self.game.door_scenarios)

        if self.window_open == True and self.game.compass != 0:
            for elem in self.game.scenarios:
                elem.rect.y += self.game.compass
            self.game.player.pos.y -= 14

    def update_scenario(self, keys):

        if keys:

            if keys == pg.K_a and self.game.hits_door_check:
                # house / city
                if self.game.place == 'house_1':
                    self.game.channel1.play(self.game.door_sound)
                    self.game.place = 'city_pt_1'
                    self.game.player.pos.x = QUARTERSCREEN_X + 20
                    self.game.lvl.City_pt_1()
                elif self.game.place == 'city_pt_1':
                    self.game.channel1.play(self.game.door_sound)
                    self.game.place = 'house_1'
                    self.game.player.pos.x = QUARTERSCREEN_X -30
                    self.game.lvl.House_1()
                # city / build base
                if self.game.place == 'city_pt_2' and self.game.player.pos.y > HEIGHT / 2:
                    self.game.channel1.play(self.game.door_sound)
                    self.game.place = 'build_1'
                    self.game.lvl.Build_1()
                elif self.game.place == 'build_1' and self.game.player.pos.y > HEIGHT / 2:
                    self.game.channel1.play(self.game.door_sound)
                    self.game.place = 'city_pt_2'
                    self.game.lvl.City_pt_2()
                # build / city top
                if self.game.place == 'city_pt_2' and self.game.player.pos.y < HEIGHT / 2:
                    self.game.place = 'build_1'
                    self.game.lvl.Build_1()
                elif self.game.place == 'build_1' and self.game.player.pos.y < HEIGHT / 2 and self.window_open == True:
                    self.game.place = 'city_pt_2'
                    self.game.lvl.City_pt_2()

            elif keys == pg.K_a and self.game.hits_door_scenario_check:
                if self.game.place == 'city_pt_1':

                        self.game.walking = False
                        self.game.channel2.fadeout(10)
                        self.game.player.vel.x = 0

                        self.game.dialog_too_small = False
                        self.game.msg('small')

                if self.game.place == 'city_pt_2':

                        self.game.walking = False
                        self.game.channel2.fadeout(10)
                        self.game.player.vel.x = 0

                        self.game.dialog_too_small = False
                        self.game.msg('small')

                # glass breaking
            if keys == pg.K_s and self.game.hits_door_check:
                if self.game.place == 'build_1' and self.window_open == False and self.game.player.pos.y < HEIGHT / 2:
                    self.game.channel1.play(self.game.brokenwindow_sound)
                    self.window_open = True
                    self.game.lvl.Build_1()

        if not keys:

                # city 1 to city 2
            if self.game.place == 'city_pt_1' and self.game.player.rect.left >= WIDTH and self.game.player.vel.x > 0:
                self.game.player.pos.x = 1
                self.game.place = 'city_pt_2'
                self.game.lvl.City_pt_2()
            elif self.game.place == 'city_pt_2' and self.game.player.rect.right < 0 and self.game.player.vel.x < 0:
                self.game.place = 'city_pt_1'
                self.game.player.pos.x = WIDTH - 1
                self.game.lvl.City_pt_1()
                # city 2 to win
            elif self.game.place == 'city_pt_2' and self.game.player.rect.left > WIDTH + 5 and self.game.dialog_city_2 == True:
                self.game.encerramento_check = True
                self.game.playing = False

        self.interact()

    def interact(self):

        # check if player hits a item or place
        hits_special = pg.sprite.spritecollide(self.game.player, self.game.specials, False)
        if hits_special:
            self.game.hits_special_check = True
        else:
            self.game.hits_special_check = False

        keys = pg.key.get_pressed()

        if keys[pg.K_s] and self.game.hits_special_check:

            self.walking = False
            self.game.channel2.fadeout(10)

            if self.game.place == "house_1":

                if pg.Rect.colliderect(self.game.player.rect, self.book): # book

                    self.get_book = True
                    self.game.channel1.play(self.game.item1_sound)
                    self.House_1()

                    self.game.place = 'get_book'
                    book = self.game.book
                    book.set_colorkey(BLACK)
                    book_rect = book.get_rect()
                    book_rect.center = (WIDTH // 2, HEIGHT // 2)
                    self.game.screen.blit(book, book_rect)
                    text1 = ('Você encontrou um livro!')
                    text2 = ('-- Use a tecla "D" quando quiser acessá-lo. --')
                    text3 = ('Pressione "ENTER" para seguir.')
                    self.game.draw_text(text1, 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
                    self.game.draw_text(text2, 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 25)
                    self.game.draw_text(text3, 25, WHITE, WIDTH / 2, HEIGHT * 3 / 4 + 50)
                    pg.display.flip()
                    self.game.wait_for_key()
                    self.game.msg(self.game.place)
                    self.game.place = 'house_1'

                if pg.Rect.colliderect(self.game.player.rect, self.item1) and self.get_book: #IMPORTANTE

                    self.get_item1 = True
                    self.game.channel1.play(self.game.item1_sound)
                    self.House_1()
                    self.msg_item('item1')

            elif self.game.place == "city_pt_1":

                if pg.Rect.colliderect(self.game.player.rect, self.vazio): # jornal

                    self.game.place = 'jornal'
                    jornal = self.game.jornal
                    jornal_rect = jornal.get_rect()
                    jornal_rect.center = (WIDTH // 2, HEIGHT // 2)
                    self.game.screen.blit(jornal, jornal_rect)
                    pg.display.flip()
                    self.game.wait_for_key()
                    self.game.msg(self.game.place)
                    self.game.place = 'city_pt_1'

            elif self.game.place == "city_pt_2":

                if pg.Rect.colliderect(self.game.player.rect, self.item2) and self.get_book: #IMPORTANTE

                    self.get_item2 = True
                    self.game.channel1.play(self.game.item1_sound)
                    self.City_pt_2()
                    self.msg_item('item2')

                elif pg.Rect.colliderect(self.game.player.rect, self.item5) and self.get_book: #IMPORTANTE

                    self.get_item5 = True
                    self.game.channel1.play(self.game.item1_sound)
                    self.City_pt_2()
                    self.msg_item('item5')

            elif self.game.place == "build_1":

                if pg.Rect.colliderect(self.game.player.rect, self.item3) and self.get_book: #IMPORTANTE

                    self.get_item3 = True
                    self.game.channel1.play(self.game.item1_sound)
                    self.Build_1()
                    self.msg_item('item3')


        if self.game.place == "city_pt_2":

            if pg.Rect.colliderect(self.game.player.rect, self.look_someone):

                self.walking = False
                if self.get_item4 == False:
                    self.get_item4 = True
                    self.game.channel1.play(self.game.item1_sound)
                self.game.channel2.fadeout(10)

                self.game.msg(self.game.place)

    def msg_item(self, item):

        if item == 'item1':
            falas = [('A temperatura hoje está bem alta, parece haver algo nesse livro falando sobre isso..')]
        elif item == 'item2':
            falas = [('Nossa, uma barbaridade o que fizeram com a Reserva do Saura, a cidade era bem mais bonita antes da área ser explorada'),
                     ('Vou deixar essa foto no livro.')]
        elif item == 'item3':
            falas = [('Olha só?! Um cartaz da antiga fábrica a pleno vapor. Nessa época nossa cidade era muito movimentada e rica!'),
                     ('Há um bom tempo eu trabalhei aqui na parte de limpeza. Bons tempos e saudade das minhas costas de 30 anos atrás.')]
        elif item == 'item5':
            falas = [('Hmmm, não sei se posso acreditar nesse artigo.. não sei mais o que é real ou falso. Só sei que está muito calor.')]

        for elem in falas:
            self.game.screen.blit(self.game.dialog_box2, self.game.dialog_box_rect2)
            self.game.draw_text(elem, 22, BLACK, WIDTH / 2, 30)
            pg.display.flip()
            self.game.wait_for_key()

    def read_book(self):

        self.walking = False
        self.game.channel2.fadeout(10)

        book = self.game.book_open0
        book_rect = book.get_rect()
        book_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.game.screen.blit(book, book_rect)
        pg.display.flip()

        ok = True
        page = 0
        while ok:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        if page == 0:
                            pass
                        else:
                            page -= 1
                            self.game.channel1.play(self.game.page_sound)
                    if event.key == pg.K_RIGHT:
                        if page == 5:
                            pass
                        else:
                            page += 1
                            self.game.channel1.play(self.game.page_sound)

                    if event.key == pg.K_RETURN or event.key == pg.K_ESCAPE:
                        ok = False

                    if page == 0:
                        book = self.game.book_open0
                        self.item = False

                    elif page == 1:
                        book = self.game.book_open1
                        if self.get_item1:
                            self.item = True
                            item = self.game.item1
                            item_rect = item.get_rect()
                            item_rect.center = ((WIDTH / 2) - (self.game.book_open0.get_width() / 4), HEIGHT // 2)
                        else:
                            self.item = False

                    elif page == 2:
                        book = self.game.book_open2
                        if self.get_item2:
                            self.item = True
                            item = self.game.item2
                            item_rect = item.get_rect()
                            item_rect.center = ((WIDTH / 2) - (self.game.book_open0.get_width() / 4), HEIGHT // 2)
                        else:
                            self.item = False

                    elif page == 3:
                        book = self.game.book_open3
                        if self.get_item3:
                            self.item = True
                            item = self.game.item3
                            item_rect = item.get_rect()
                            item_rect.center = ((WIDTH / 2) - (self.game.book_open0.get_width() / 4), HEIGHT // 2)
                        else:
                            self.item = False

                    elif page == 4:
                        book = self.game.book_open4
                        if self.get_item4:
                            self.item = True
                            item = self.game.item4
                            item_rect = item.get_rect()
                            item_rect.center = ((WIDTH / 2) - (self.game.book_open0.get_width() / 4), HEIGHT // 2)
                        else:
                            self.item = False

                    elif page == 5:
                        book = self.game.book_open5
                        if self.get_item5:
                            self.item = True
                            item = self.game.item5
                            item_rect = item.get_rect()
                            item_rect.center = ((WIDTH / 2) - (self.game.book_open0.get_width() / 4), HEIGHT // 2)
                        else:
                            self.item = False

                    book_rect = book.get_rect()
                    book_rect.center = (WIDTH // 2, HEIGHT // 2)
                    self.game.screen.blit(book, book_rect)
                    if self.item:
                        item.set_colorkey(BLACK)
                        self.game.screen.blit(item, item_rect)

                    pg.display.flip()

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(EBONY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Get_image(pg.sprite.Sprite):
    def __init__(self, game, img, x, y, ck):

        pg.sprite.Sprite.__init__(self)
        self.game = game
        w, h = (img.get_width(), img.get_height())
        self.image = pg.Surface((w, h))
        self.image.blit(img, (0, 0))
        if ck == True:
            self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
