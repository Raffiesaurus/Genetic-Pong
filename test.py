import pandas as pd
import openpyxl
import os 
import datetime

time = datetime.datetime.now()

print(str(time).replace(' ', '_').split('.')[0])

with open('best_coeffs.txt') as f:
    lines = f.readlines()
    print(float(lines[0].split('\n')[0]))