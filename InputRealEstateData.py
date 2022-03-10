import csv
import numpy as np
import pandas as pd
import json

file_path = './keyword.json'

with open(file_path, 'r') as file:
    data = json.load(file)
    array = data['지역정보']
    
    print(array[0]['지역명'])
    print(array[0]['파일경로'])

    