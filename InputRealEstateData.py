import csv
import numpy as np
import pandas as pd
import json

file_path = './keyword.json'

def getJsonInfo():
    with open(file_path, 'r') as file:
        data = json.load(file)
        array = data['지역정보']
        return array