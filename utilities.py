import csv
import pandas as pd
from const import END_YEAR, MID_YEAR, START_YEAR

dt_cases = r"main_data.csv"

# Read the CSV file and populate the cases list
cases = []
with open(dt_cases, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cases.append(row)

def attribute_extraction(param, data):
    output = set()
    for i in data:
        output.add(i[param])
    return sorted(output)

def count_param(param):
    keys = attribute_extraction(param, cases)
    outputdict = {}
    for key in keys:
        accumulated_cases = []
        for case in cases:
            if key == case[param]:
                accumulated_cases.append(case)
        outputdict[key] = len(accumulated_cases)
    return outputdict