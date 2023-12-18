import pygame
from game_classes import Ball, Bat, Config, StatsSave
from genetic_algo import GeneticPong
from typing import List
import statistics

class Pong:
    
    # Initializing game elements and AI
    def __init__(self, game_config: Config, bat: Bat, ball: Ball, ai: GeneticPong):
        self.config = game_config
        self.bat = bat
        self.ball = ball
        self.screen = pygame.display.set_mode(self.config.screen_size)
        self.ai = ai
        self.stats_saver = StatsSave()
    
    # Run the gamne
    def run(self):
        self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)  
        self.config.game_running = True
        start_time = self.config.timer.get_ticks()
        
        # Game loop
        while self.config.game_running:
        
            # Handling game events, updating display, and AI decisions
            self.config.clock.tick(self.config.fps)
            score_text = game_font.render('Score: ' + str(self.config.score), True, (255, 255, 255))
            players_count_text = game_font.render('Bats Left: ' + str(len(self.ai.bats)), True, (255, 255, 255))
            episode_count_text = game_font.render('Episode Count: ' + str(len(self.ai.episode_winners) + 1), True, (255, 255, 255))
            self.screen.fill(self.config.bg_color)
            self.screen.blit(score_text, (15, 5))
            self.screen.blit(players_count_text, (375, 5))
            self.screen.blit(episode_count_text, (725, 5))
            pygame.draw.circle(self.screen, self.ball.color, self.ball.get_position(), self.ball.radius)
        
            # Draw every bat generated
            for i in range(len(self.ai.bats)):
                pygame.draw.rect(self.screen, self.ai.bats[i].color, self.ai.bats[i].get_rect())
        
            pygame.display.flip()

            ball_hit_bat = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.config.game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.config.game_running = False
            
            acceptable_ai_bats: List[Bat] = []
            
            # Check move to make, update fitness of all remaining bats
            for ai_bat in self.ai.bats:
                bat_move = self.ai.calculate_move([ai_bat.pos_x, self.ball.pos_x, self.ball.pos_y], ai_bat.ga_coefficients)

                if (bat_move == 0 and ai_bat.pos_x >= 0):
                    ai_bat.pos_x -= ai_bat.move_speed
                elif (bat_move == 1 and ai_bat.pos_x + ai_bat.width <= self.config.screen_size[0]):
                    ai_bat.pos_x += ai_bat.move_speed
            
                ai_bat.ga_fitness.append(self.ai.distance(ai_bat.pos_x, ai_bat.pos_y, self.ball.pos_x, self.ball.pos_y))
            
                if (ai_bat.check_collision(ball)):
                    if(self.config.hit_reset_delay <= 0):
                        ball_hit_bat = True
                        self.config.score += 1
                        self.config.hit_reset_delay = 30
                    if ai_bat not in acceptable_ai_bats:
                        acceptable_ai_bats.append(ai_bat)
                
            self.ball.move(self.config.screen_size, ball_hit_bat)
            
            if (self.config.hit_reset_delay > 0):
                self.config.hit_reset_delay -= 1
           
            # Remove the bats that missed the ball 
            if (ball_hit_bat):
                self.ai.current_winners = self.ai.bats = acceptable_ai_bats
            
            # On episode over, reset positions, generate next episode values                
            if(self.ball.pos_y > self.bat.pos_y or self.config.score == self.ai.episode_win_score):
                runtime = (self.config.timer.get_ticks()- start_time) / 1000
                start_time = self.config.timer.get_ticks()                               
                self.ball.reset()
                self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)
                best_bat = self.ai.reset(self.config)
                if best_bat != None:
                    print('---------------------------------------------------------------------------------------')
                    print(f"Episode: {len(self.ai.episode_winners)}")
                    print(f"    Score: {self.config.score}")                
                    print(f"    Coefficients: {best_bat.ga_coefficients}")    
                    print(f"    Best bat fitness: {statistics.mean(best_bat.ga_fitness)}")    
                    print(f"    Runtime: {runtime}")    
                    
                    # Store stats in excel file
                    self.stats_saver.add_values(len(self.ai.episode_winners), self.config.score, best_bat.ga_coefficients[0], best_bat.ga_coefficients[1], best_bat.ga_coefficients[2], statistics.mean(best_bat.ga_fitness), runtime)
                                
                self.config.score = 0                
                                                                                                   
            if (len(self.ai.episode_winners) >= self.ai.episodes):
                game_config.game_running = False
            
                            
if __name__ == "__main__":
    pygame.init()
    game_font = pygame.font.SysFont("goudyoldstyle", 25)
    timer = pygame.time

    game_config = Config(timer, game_font)
    
    pong_genetic_algo = GeneticPong()
    
    # Generate bats according to ai defined count
    for _ in range(pong_genetic_algo.ai_count):
        bat = Bat()
        bat.set_position((game_config.screen_size[0] - bat.width) / 2, game_config.screen_size[1] - bat.height - 20, game_config.screen_size[0])
        pong_genetic_algo.bats.append(bat)
        
    pong_genetic_algo.bat_width = pong_genetic_algo.bats[0].width
    ball = Ball()
    
    pong_game = Pong(game_config, pong_genetic_algo.bats[0], ball, pong_genetic_algo)
    pong_game.run()