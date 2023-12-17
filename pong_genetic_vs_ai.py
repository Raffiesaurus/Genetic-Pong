import pygame
from game_classes import PvPBall, Bat, Config
from genetic_algo import GeneticPong
import pandas as pd

class Pong:
    
    def __init__(self, game_config: Config, genetic_bat: Bat, basic_ai_bat: Bat, ball: PvPBall):
        self.config = game_config
        self.genetic_bat = genetic_bat
        self.basic_ai_bat = basic_ai_bat
        self.ball = ball
        self.screen = pygame.display.set_mode(self.config.screen_size)

    
    def run(self):
        self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)
        self.genetic_bat.set_position((self.config.screen_size[0] - genetic_bat.width) / 2, self.config.screen_size[1] - genetic_bat.height - 20, self.config.screen_size[0])
        self.basic_ai_bat.set_position((self.config.screen_size[0] - genetic_bat.width) / 2, genetic_bat.height, self.config.screen_size[0])
        
        self.config.game_running = True
        self.ga = GeneticPong()
        
        while self.config.game_running:
            self.config.clock.tick(self.config.fps)
            score_text = game_font.render('Score: ' + str(self.config.score), True, (255, 255, 255))
            opp_score_text = game_font.render('Genetic Score: ' + str(self.config.opp_score), True, (255, 255, 255))
            self.screen.fill(self.config.bg_color)
            pygame.draw.circle(self.screen, self.ball.color, self.ball.get_position(), self.ball.radius)
            pygame.draw.rect(self.screen, self.genetic_bat.color, self.genetic_bat.get_rect())
            pygame.draw.rect(self.screen, self.basic_ai_bat.color, self.basic_ai_bat.get_rect())
            self.screen.blit(score_text, (10, 5))
            self.screen.blit(opp_score_text, (750, 500))
            pygame.display.flip()

            ball_hit_bat = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.config.game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.config.game_running = False

            if (self.basic_ai_bat.pos_x + (self.basic_ai_bat.width / 2) > self.ball.pos_x and self.basic_ai_bat.pos_x >= 0) :
                self.basic_ai_bat.pos_x -= self.basic_ai_bat.move_speed
                
            if (self.basic_ai_bat.pos_x + (self.basic_ai_bat.width / 2) < self.ball.pos_x and self.basic_ai_bat.pos_x + self.basic_ai_bat.width <= self.config.screen_size[0]) :
                self.basic_ai_bat.pos_x += self.basic_ai_bat.move_speed
            
            inputs = [self.genetic_bat.pos_x, self.ball.pos_x, self.ball.pos_y]
            bat_move = self.ga.calculate_move(inputs, self.genetic_bat.ga_coefficients)

            if (bat_move == 0 and self.genetic_bat.pos_x >= 0):
                self.genetic_bat.pos_x -= self.genetic_bat.move_speed
            elif (bat_move == 1 and self.genetic_bat.pos_x + self.genetic_bat.width <= self.config.screen_size[0]):
                self.genetic_bat.pos_x += self.genetic_bat.move_speed
            
            if (self.genetic_bat.check_collision(ball)):
                if(self.config.hit_reset_delay <= 0):
                    ball_hit_bat = True
                    self.config.hit_reset_delay = 5
                    
            elif((self.basic_ai_bat.pos_y + (self.basic_ai_bat.height * 2)) >= (self.ball.pos_y + self.ball.radius)) and ((self.basic_ai_bat.pos_x <= self.ball.pos_x) and ((self.basic_ai_bat.pos_x + self.basic_ai_bat.width) >= self.ball.pos_x)):
                if(self.config.hit_reset_delay <= 0):
                    ball_hit_bat = True
                    self.config.hit_reset_delay = 5
            
            self.ball.move(self.config.screen_size, ball_hit_bat)
            
            if (self.config.hit_reset_delay > 0):
                self.config.hit_reset_delay -= 1
                
            if (self.ball.pos_y >= self.config.screen_size[1] - self.ball.radius):
                self.ball.speed_x = 0
                self.ball.speed_y = 0
                self.config.score += 1
                self.ball.reset()
                self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)
 
            elif (self.ball.pos_y <= 0):
                self.ball.speed_x = 0
                self.ball.speed_y = 0
                self.config.opp_score += 1
                self.ball.reset()
                self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)

            if (self.config.score == 5 or  self.config.opp_score == 5):
                game_config.game_running = False
            
if __name__ == "__main__":
    pygame.init()
    game_font = pygame.font.SysFont("goudyoldstyle", 25)
    timer = pygame.time
    game_config = Config(timer, game_font)
    genetic_bat = Bat()
    basic_ai_bat = Bat()
    ball = PvPBall()
    
    file = pd.read_excel(r'stats\data_2023_12_13_20_42_13.xlsx') 
    genetic_bat.set_coefficients(file['Coeff_bat_x'].iat[-1], file['Coeff_ball_x'].iat[-1], file['Coeff_ball_y'].iat[-1])
    genetic_bat.set_color(255,0,0)
    
    basic_ai_bat.set_color(255,255,0)
    
    pong_game = Pong(game_config, genetic_bat, basic_ai_bat, ball)
    pong_game.run()