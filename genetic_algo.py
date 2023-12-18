from game_classes import Bat, Config
import math
import random
from typing import List
import statistics

# Represents the genetic algorithm to solve the game
class GeneticPong:
    
    # Initializing parameters and lists
    def __init__(self):
        self.episodes = 300
        self.episode_win_score = 300
        self.ai_count = 30
        self.episode_winners: List[Bat] = []
        self.current_winners: List[Bat] = []
        self.bat_width = 0
        self.bats: List[Bat] = []
        self.should_mutate = True
        
    # Calculate distance between bat and ball
    def distance(self, bat_pos_x, bat_pos_y, ball_pos_x, ball_pos_y):
        distance_x = abs(bat_pos_x + (self.bat_width / 2) - ball_pos_x)
        distance_y = abs(bat_pos_y - ball_pos_y)
        return math.sqrt(distance_x**2 + distance_y**2)
                
    # Calculate bat's move depending on current frame values and bat's coefficients
    def calculate_move(self, input_values, value_coefficients):
        moves = []
        for i in range(len(input_values)):
            moves.append(input_values[i] * value_coefficients[i])
        move = moves.index(max(moves))
        return move
    
    # Resetting and evolving the population of bats for next episode
    def reset(self, game_config: Config):
        best_bat = None
        
        # Selection process
        
        # If only one bat survived, it is the best bat
        if (len(self.current_winners) == 1):
            best_bat = self.current_winners[0]
            self.episode_winners.append(best_bat)
            
        # If more than one bat survived, best bat is the bat that has the least mean of fitness value
        elif (len(self.current_winners) > 1):
            best_bat = self.current_winners[0]
            for winner in self.current_winners:
                winner_fitness = statistics.mean(winner.ga_fitness)
                best_fitness = statistics.mean(best_bat.ga_fitness)
                if winner_fitness < best_fitness:
                    best_bat = winner
            self.episode_winners.append(best_bat)
        
        # If no bat survived, best bat is taken from previous episode
        else:
            if(len(self.episode_winners) >= 1):
                best_bat = self.episode_winners[-1:]
        
        # Crossover and mutation process
        self.bats = []
        for _ in range(self.ai_count):
            bat = Bat()
            bat.set_position((game_config.screen_size[0] - bat.width) / 2, game_config.screen_size[1] - bat.height - 20, game_config.screen_size[0])
            if(best_bat == None):                        
                self.bats.append(bat)
            else:
                if self.should_mutate:
                    # Mutate bat coefficients based on a chance
                    if(random.randint(1, 10) <= 5):
                        for i in range (len(bat.ga_coefficients)):
                            bat.ga_coefficients[i] = best_bat.ga_coefficients[i] + random.uniform(-10, 10)
                    else:
                        bat.ga_coefficients = best_bat.ga_coefficients
                    self.bats.append(bat)
                else:
                    bat.ga_coefficients = best_bat.ga_coefficients
                    self.bats.append(bat)

        # Checking if this bat is the best bat so far
        for old_bat in self.episode_winners:
            old_fitness = statistics.mean(old_bat.ga_fitness)
            best_fitness = statistics.mean(best_bat.ga_fitness)
            if old_fitness < best_fitness:
                best_bat = old_bat
                
        return best_bat