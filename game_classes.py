import random
import pandas as pd
import pygame
import datetime

class Ball:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 5.5
        self.speed_y = 5.5
        self.radius = 10
        self.color = (8, 146, 209)

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        
    def get_position(self):
        return (self.pos_x, self.pos_y)
    
    def move(self, screen_size, has_hit_bat):
        self.pos_x -= self.speed_x
        self.pos_y -= self.speed_y
                
        if (self.pos_x <= self.radius or self.pos_x >= screen_size[0] - self.radius):
            self.speed_x = -self.speed_x
        
        if (self.pos_y <= self.radius or has_hit_bat):
            self.speed_y = -self.speed_y
        
        if (self.pos_y >= screen_size[1] - self.radius):
            self.speed_x = 0
            self.speed_y = 0
            
    def reset(self):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 5.5
        self.speed_y = 5.5
        
class PvPBall:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 4
        self.speed_y = 4
        self.radius = 10
        self.color = (8, 146, 209)

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        
    def get_position(self):
        return (self.pos_x, self.pos_y)
    
    def move(self, screen_size, has_hit_bat):
        self.pos_x -= self.speed_x
        self.pos_y -= self.speed_y
                
        if (self.pos_x <= self.radius or self.pos_x >= screen_size[0] - self.radius):
            self.speed_x = -self.speed_x
        
        if (has_hit_bat):
            self.speed_y = -self.speed_y
            self.speed_x += (self.speed_x * 0.01)
            self.speed_y += (self.speed_y * 0.01)
            
    def reset(self):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 4
        self.speed_y = 4

    
class Bat:
    
    def __init__(self):
        self.pos_x = self.pos_y = 0
        self.move_speed = 5
        self.width = 150
        self.height = 15
        self.ga_fitness = []
        self.ga_coefficients = [random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000)]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def set_position(self, x, y, screen_width):
        self.pos_x = x
        self.pos_y = y
        
        if self.pos_x < 0:
            self.pos_x = 0
        
        if self.pos_x + self.width > screen_width:
            self.pos_x = screen_width - self.width

    def set_coefficients(self, bat_x, ball_x, ball_y):
        self.ga_coefficients[0] = bat_x
        self.ga_coefficients[1] = ball_x
        self.ga_coefficients[2] = ball_y
        
    def set_color(self, r, g, b):
        self.color = (r, g, b)

    def get_position(self):
        return (self.pos_x, self.pos_y)
            
    def get_rect(self):
        return (self.pos_x, self.pos_y, self.width, self.height)
    
    def move(self, x_change, screen_width):
        self.pos_x += x_change
        
        if self.pos_x < 0:
            self.pos_x = 0
        
        if self.pos_x + self.width > screen_width:
            self.pos_x = screen_width - self.width
            
    def check_collision(self, ball: Ball):
        if((self.pos_y - (self.height / 2)) <= (ball.pos_y + ball.radius)) and ((self.pos_x <= ball.pos_x) and ((self.pos_x + self.width) >= ball.pos_x)):
            return True
        else:
            return False
                
class Config:
    
    def __init__(self, timer: pygame.time, font):
        self.timer: pygame.time = timer
        self.clock: pygame.time.Clock = self.timer.Clock()
        self.font = font
        self.screen_size = [960, 540]
        self.bg_color = (0, 0, 0)
        self.fps = 60
        self.score = 0
        self.opp_score = 0
        self.hit_reset_delay = 0
        self.game_running = False

class StatsSave:
    
    def __init__(self) -> None:    
        self.file_path = r"stats\data_"+(str(datetime.datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').split('.')[0])+r".xlsx"
        print(self.file_path)
        self.sheet_columns = ['Episode', 'Score', 'Coeff_bat_x', 'Coeff_ball_x', 'Coeff_ball_y', 'Mean Fitness', 'Runtime']

        self.sheet_data_values = []

        self.data_episode = 0
        self.data_score = 0
        self.data_coeff_bat_x = 0
        self.data_coeff_ball_x = 0
        self.data_coeff_ball_y = 0
        self.data_mean_fitness = 0
        self.data_runtime = 0
            
    def add_values(self, episode, score, coeff_bat_x, coeff_ball_x, coeff_ball_y, mean_fitness, runtime):
        self.data_episode = episode
        self.data_score = score
        self.data_coeff_bat_x = coeff_bat_x
        self.data_coeff_ball_x = coeff_ball_x
        self.data_coeff_ball_y = coeff_ball_y
        self.data_mean_fitness = mean_fitness
        self.data_runtime = runtime
        self.write_to_file()

    def write_to_file(self):
        
        self.sheet_data_values.append([self.data_episode, self.data_score, self.data_coeff_bat_x, self.data_coeff_ball_x, self.data_coeff_ball_y, self.data_mean_fitness, self.data_runtime])
        
        self.sheet_data = pd.DataFrame(self.sheet_data_values, columns = self.sheet_columns)
        
        self.sheet_data.to_excel(self.file_path, index = False)