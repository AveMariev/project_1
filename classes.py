import pygame


class SuperDeb:
    
    def __init__(self):
        self.inter = Interface()
        self.game = Game()
        self.font_end = pygame.font.SysFont('Arial', 40, bold=True)
        self.interf = True
        self.time_to_choose = True 
        self.game_choice = False
        self.single_game = False 
        self.game_over = False
    
    def interface(self, sc):
        if not self.inter.game_level:
            if self.game_choice:
                self.inter.show_game_but(self.sc)
            if self.interf:
                self.sc = sc    
                self.inter.show(self.sc)
        else:
            self.time_to_choose = False
    
    def game_choose(self):
        self.interf = False
        self.game_choice = True
         
    def take_pos(self, pos, AVE):
        if self.game_choice:
            self.inter.take_answer_to_game_but(pos)        
        if self.interf:
            self.inter.take_answer(pos, AVE)
        
    def lose(self):
        self.game_over = True
        self.render_end = self.font_end.render('ВЫ ПРОИГРАЛИ', 1, pygame.Color('Purple'))
        self.sc.blit(self.render_end, (430, 800 // 2))
    
    def win(self):
        self.game_over = True
        self.render_end = self.font_end.render('ВЫ ВЫИГРАЛИ', 1, pygame.Color('Purple'))
        self.sc.blit(self.render_end, (430, 800 // 2))


class Interface:
    
    def __init__(self):
        self.sprites = pygame.sprite.Group()      
        self.game_level = 0    
        
    def show(self, sc):
        self.sc = sc
        play_single = Button(330, 250, 'images/single_player.bmp', self.sprites)
        play_versus = Button(330, 500, 'images/vs_bot.bmp', self.sprites)
        
        sc.blit(play_single.surf, play_single.rect)
        sc.blit(play_versus.surf, play_versus.rect)
        
    def show_game_but(self, sc):
        game_level_one = Button(330, 50, 'images/easy_hard.bmp', self.sprites)
        game_level_two = Button(330, 300, 'images/hard.bmp', self.sprites)
        game_level_three = Button(330, 550, 'images/very_hard.bmp', self.sprites)
        
        sc.blit(game_level_one.surf, game_level_one.rect)
        sc.blit(game_level_two.surf, game_level_two.rect)
        sc.blit(game_level_three.surf, game_level_three.rect)
    
    def take_answer_to_game_but(self, pos):
        if 330 < pos[0] < 830:
            if 50 < pos[1] < 200:
                self.game_level = 1
            elif 300 < pos[1] < 450:
                self.game_level = 2
            elif 550 < pos[1] < 700:
                self.game_level = 3
            
    
    def take_answer(self, pos, AVE):
        self.AVE = AVE
        if 330 < pos[0] < 830:
            if 250 < pos[1] < 400:
                self.AVE.game_choose()
                for i in self.sprites:
                    i.kill()
            elif 500 < pos[1] < 650:               
                self.AVE.game.start(self.sc) 
                self.AVE.interf = False
                self.AVE.time_to_choose = False
                for i in self.sprites:
                    i.kill()                 
    

class Game:
    
    def __init__(self):
        self.multi = False
    
    def start(self, sc):
        self.multi = True
        
    def move(self, plate, ball):
        if plate.rect.center > ball.rect.center:
            plate.move(Left=True)
        elif plate.rect.center < ball.rect.center:
            plate.move(Right=True)


class Button(pygame.sprite.Sprite):
    
    def __init__(self, x, y, pic, sprites):
        super().__init__(sprites)
        self.surf = pygame.image.load(pic)
        self.surf.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(x, y, 500, 150)


class Block(pygame.sprite.Sprite):
    
    def __init__(self, x, y, posx, posy, color, all_sprites):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(posx, posy, x, y)
        self.surf = pygame.Surface((x, y))
        self.surf.fill(color)
    
    def update(self, sc):
        sc.blit(self.surf, self.rect)
    

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, radius, x, y, all_sprites, speed):
        super().__init__(all_sprites)
        self.image = pygame.image.load(
                    'images/ball.png').convert_alpha()      
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(x, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.speed = speed
        self.dx = 1
        self.dy = -1
    
    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
                
    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy 
    
    def change_direction(self, OX=False, OY=False):
        if OX:
            self.dx *= -1
        if OY:
            self.dy *= -1
    
    def check_some_fckn_shit(self, other):
        if self.dx > 0:
            delta_x = self.rect.right - other.rect.left
        else:
            delta_x = other.rect.right - self.rect.left
        if self.dy > 0:
            delta_y = self.rect.bottom - other.rect.top
        else:
            delta_y = other.rect.bottom - self.rect.top
        if self.rect.center < other.rect.center:
            self.dx = -1 
        else:
            self.dx = 1
        if delta_x > delta_y:
            self.dy *= -1
            
    def collide(self, other):
        self.check_some_fckn_shit(other)
    
    def collide_block(self, other):
        self.check_some_fckn_shit(other)
    
    def update(self, sc):
        sc.blit(self.image, self.rect)    
    

class Plate(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed, all_sprites, pos):
        super().__init__(all_sprites)
        self.image = pygame.image.load(
                    'images/player.png').convert_alpha() 
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(pos[0], pos[1], x, y)      
        self.speed = speed  
    
    def move(self, Right=False, Left=False):
        if Left:
            self.rect.x -= self.speed
        elif Right:
            self.rect.x += self.speed
            
    def fast_move(self, Right=False, Left=False):
        if Left:
            self.rect.x -= self.speed * 2
        elif Right:
            self.rect.x += self.speed * 2    
    
    def update(self, sc):
        sc.blit(self.image, self.rect)