import pygame
import random
from game_classes import Ball, Bat, Config

class Pong:
    
    def __init__(self, game_config: Config, bat: Bat, ball: Ball):
        self.config = game_config
        self.bat = bat
        self.ball = ball
        self.screen = pygame.display.set_mode(self.config.screen_size)
    
    
    def run(self):
        self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)
        self.bat.set_position((self.config.screen_size[0] - bat.width) / 2, self.config.screen_size[1] - bat.height - 20)
        
        self.config.game_running = True
        
        move_multiplier = 1
        move_left = move_right = False
        
        while self.config.game_running:
            clock.tick(self.config.fps)
            self.screen.fill(self.config.bg_color)
            score_text = game_font.render('Score: ' + str(self.config.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 5))
            pygame.draw.circle(self.screen, self.ball.color, self.ball.get_position(), self.ball.radius)
            pygame.draw.rect(self.screen, self.bat.color, self.bat.get_rect())
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.config.game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        move_left = True       
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        move_right = True
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        move_left = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        move_right = False
                
                if move_left:
                    move_multiplier = -1
                elif move_right:
                    move_multiplier = 1
                else:
                    move_multiplier = 0

            self.bat.move(self.bat.move_speed * move_multiplier)  

if __name__ == "__main__":
    pygame.init()
    game_font = pygame.font.SysFont("goudyoldstyle", 25)
    clock = pygame.time.Clock()
    game_config = Config(clock, game_font)
    bat = Bat()
    ball = Ball()
    
    pong_game = Pong(game_config, bat, ball)
    pong_game.run()