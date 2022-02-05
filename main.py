from CONSTANTS import *

def player_move():     
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if player_plate.rect.x < 1110:
            if AVE.inter.game_level != 2:
                if keys[pygame.K_LSHIFT]:
                    player_plate.fast_move(Right=True)
                else:
                    player_plate.move(Right = True)
    elif keys[pygame.K_LEFT]:
        if player_plate.rect.x > 0:
            if AVE.inter.game_level != 2:
                if keys[pygame.K_LSHIFT]:
                    player_plate.fast_move(Left=True)
                else:
                    player_plate.move(Left = True)

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
wall_image = pygame.image.load('images/wall.jpg').convert()

clock = pygame.time.Clock()

AVE = SuperDeb()

all_sprites = pygame.sprite.Group()
all_blocks =  pygame.sprite.Group()

player_plate = Plate(100, 50, 15, all_sprites, (550, 700))
bot_plate = Plate(100, 50, 15, all_sprites, (550, 100))
ball = Ball(25, WIDTH // 2, HEIGHT // 2, all_sprites, 10)

for i in range(4):
    for j in range(10):
        Block(100, 50, 20 * j + 100 * j, 10 * i + 50 * i, choice(color_list), all_blocks)

while True:
    pos = 0
    sc.blit(wall_image, (0, 0))
    AVE.interface(sc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
    
    if AVE.time_to_choose:
        pygame.display.update()
        if pos:
            AVE.take_pos(pos, AVE)
    
    if AVE.inter.game_level and not AVE.game_over:
        if AVE.inter.game_level == 3:
            ball.speed = 15
        bot_plate.kill()
        ball.move()
        if ball.rect.center[0] < ball.radius or ball.rect.center[0] > WIDTH - ball.radius:
            ball.change_direction(OX=True)
        if ball.rect.center[1] < ball.radius:
            ball.change_direction(OY=True)
            
        if ball.rect.colliderect(player_plate) and ball.dy > 0:
            ball.collide(player_plate)
        
        if pygame.sprite.spritecollideany(ball, all_blocks):
            ball.collide_block(pygame.sprite.spritecollideany(ball, all_blocks))
            pygame.sprite.spritecollideany(ball, all_blocks).kill()
    
        if ball.rect.bottom > 1200:
            AVE.lose()
        
        if not len(all_blocks):
            AVE.win()
                   
        player_move()
        
        for i in all_sprites:
            i.update(sc)
        for i in all_blocks:
            i.update(sc)
        
        pygame.display.update()
        clock.tick(FPS)
        
    elif AVE.game.multi and not AVE.game_over:
        player_move()
        ball.move()
        AVE.game.move(bot_plate, ball)
            
        if ball.rect.center[0] < ball.radius or ball.rect.center[0] > WIDTH - ball.radius:
            ball.change_direction(OX=True)
            
        if ball.rect.center[1] < ball.radius:
            AVE.win()
        if ball.rect.bottom > 1200:
            AVE.lose()       
            
        if ball.rect.colliderect(bot_plate) and ball.dy < 0:
            ball.collide(bot_plate)      
        
        if ball.rect.colliderect(player_plate) and ball.dy > 0:
            ball.collide(player_plate)           
            
        for i in all_sprites:
            i.update(sc)       
            
        pygame.display.update()
        clock.tick(FPS)