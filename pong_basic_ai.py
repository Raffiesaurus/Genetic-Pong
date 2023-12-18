import pygame
from game_classes import Ball, Bat, Config

class Pong:
    
    # Initialize the game with configurations, bat, and ball
    def __init__(self, game_config: Config, bat: Bat, ball: Ball):
        self.config = game_config
        self.bat = bat
        self.ball = ball
        self.screen = pygame.display.set_mode(self.config.screen_size)
    
    # Run the game
    def run(self):
        self.ball.set_position(self.config.screen_size[0] / 2, self.config.screen_size[1] / 2)
        self.bat.set_position((self.config.screen_size[0] - self.bat.width) / 2, self.config.screen_size[1] - self.bat.height - 20, self.config.screen_size[0])
        
        self.config.game_running = True
        
        # Game loop
        while self.config.game_running:
            
            # Handling events and updating the display
            self.config.clock.tick(self.config.fps)  
            score_text = game_font.render('Score: ' + str(self.config.score), True, (255, 255, 255))  
            self.screen.fill(self.config.bg_color)  
            self.screen.blit(score_text, (10, 5)) 
            pygame.draw.circle(self.screen, self.ball.color, self.ball.get_position(), self.ball.radius)
            pygame.draw.rect(self.screen, self.bat.color, self.bat.get_rect())  
            pygame.display.flip()  
            
            ball_hit_bat = False 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.config.game_running = False  # Quit the game on window close

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.config.game_running = False  # Quit the game on ESC key press
            
            # Move the bat towards the ball's x-position
            if (self.bat.pos_x + (self.bat.width / 2) > self.ball.pos_x and self.bat.pos_x >= 0):
                self.bat.pos_x -= self.bat.move_speed
                
            if (self.bat.pos_x + (self.bat.width / 2) < self.ball.pos_x and self.bat.pos_x + self.bat.width <= self.config.screen_size[0]):
                self.bat.pos_x += self.bat.move_speed
            
            if (self.bat.check_collision(ball)):
                if(self.config.hit_reset_delay <= 0):
                    ball_hit_bat = True  
                    self.config.score += 1  
                    self.config.hit_reset_delay = 30  # Set delay for bat collision
            
            self.ball.move(self.config.screen_size, ball_hit_bat) 
            
            if (self.config.hit_reset_delay > 0):
                self.config.hit_reset_delay -= 1  # Reduce delay
            
            if (self.ball.speed_x == 0 and self.ball.speed_y == 0):
                game_config.game_running = False  # End game when ball stops
            
if __name__ == "__main__":
    pygame.init() 
    game_font = pygame.font.SysFont("goudyoldstyle", 25)
    timer = pygame.time
    game_config = Config(timer, game_font)
    bat = Bat()
    ball = Ball()
    
    pong_game = Pong(game_config, bat, ball)
    pong_game.run()
    
    print('Final score: ', game_config.score)