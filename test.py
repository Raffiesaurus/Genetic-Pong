import openpyxl
import os 
import datetime
import matplotlib.pyplot as plt 
import pandas as pd

time = datetime.datetime.now()

print(str(time).replace(' ', '_').split('.')[0])

with open('best_coeffs.txt') as f:
    lines = f.readlines()
    print(float(lines[0].split('\n')[0]))
    
file = pd.read_excel(r'stats\data_2023_12_13_20_42_13.xlsx') 
episode = file['Episode'] 
score = file['Score'] 
coeff1 = file['Coeff_bat_x']
coeff2 = file['Coeff_ball_x']
coeff3 = file['Coeff_ball_y']
fitness = file['Mean Fitness']
runtime = file['Runtime']

print(coeff1.iat[-1])
print(coeff2.iat[-1])
print(coeff3.iat[-1])

plt.rcParams['figure.figsize'] = [5, 3]
plt.subplots_adjust(bottom=0.2)
plt.xlabel("Episode") 

plt.title("Score vs Episode")
plt.plot(episode, score)
plt.plot(episode[27], score[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Score") 
plt.show() 

plt.title("Coefficient - Bat X Position vs Episode")
plt.plot(episode, coeff1)
plt.plot(episode[27], coeff1[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Coefficient - Bat X Position") 
plt.show()

plt.title("Coefficient - Ball X Position vs Episode")
plt.plot(episode, coeff2)
plt.plot(episode[27], coeff2[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Coefficient - Ball X Position") 
plt.show()

plt.title("Coefficient - Ball Y Position vs Episode")
plt.plot(episode, coeff3)
plt.plot(episode[27], coeff3[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Coefficient - Ball Y Position") 
plt.show()

plt.title("Fitness Value vs Episode")
plt.plot(episode, fitness)
plt.plot(episode[27], fitness[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Fitness Value") 
plt.show()

plt.title("Runtime (in seconds) vs Episode")
plt.plot(episode, runtime)
plt.plot(episode[27], runtime[27], color = 'blue', marker = '*', markersize = 10, markerfacecolor="tab:red", markeredgecolor="tab:red", label = "Maximum score obtained")
plt.legend()
plt.ylabel("Runtime (in seconds)") 
plt.show()
