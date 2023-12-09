import random

class Ball:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 6
        self.speed_y = 6
        self.radius = 10
        self.color = (8, 146, 209)

    def move(self, screen_width, screen_height, has_hit_bat):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        if (self.pos_x <= self.radius or self.pos_x >= screen_width - self.radius):
            self.speed_x = -self.speed_x
        elif (self.pos_y <= self.radius or has_hit_bat):
            self.speed_y = -self.speed_y
        elif (self.pos_y >= screen_height - self.radius):
            self.speed_x = 0
            self.speed_y = 0
            
    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        
    def get_position(self):
        return (self.pos_x, self.pos_y)
            
class Bat:
    
    def __init__(self):
        self.pos_x = self.pos_y = 0
        self.move_speed = 5
        self.width = 150
        self.height = 15
        self.ga_coefficients = [0,0,0]
        self.ga_fitness = []
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        for i in range(len(self.ga_coefficients)):
            self.ga_coefficients[i] = random.randint(0, 99999)
            
    def move(self, x_change):
        self.pos_x += x_change
            
    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_position(self):
        return (self.pos_x, self.pos_y)
            
    def get_rect(self):
        return (self.pos_x, self.pos_y, self.width, self.height)
                
class Config:
    
    def __init__(self, clock, font):
        self.clock = clock
        self.font = font
        self.screen_size = [960, 540]
        self.bg_color = (8, 146, 209)
        self.fps = 60
        self.score = 0
        self.hit_reset_delay = 0
        self.game_running = False