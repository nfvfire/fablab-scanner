import os
import glob
import json
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from datetime import datetime

# Define paths
json_dir = '/opt/scanner/Stats_Openlabs/'
xlsx_dir = '/mnt/synology/OpenLab/'

# Find latest JSON file in directory
latest_file = max(glob.glob(os.path.join(json_dir, '*.json')), key=os.path.getctime)

# Load JSON file
with open(latest_file, 'r') as f:
    data = json.load(f)

# Extract date from filename and format it
date = os.path.basename(latest_file).replace('.json', '')
date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')

# Create DataFrame from JSON
df = pd.json_normalize(data)
df = df.rename(columns={'code': 'CARTE', 'age': 'AGE', 'city': 'COMMUNE', 'time': 'HORAIRE',
                        'time_dif': 'DUREE', 'gone': 'PARTI ?', 'name': 'PRENOM', 'surname': 'NOM',
                        'email': 'EMAIL'})

# Format time column
df['HORAIRE'] = df['HORAIRE'].apply(lambda x: f'{x[0]:02}:{x[1]:02}')

# Create Excel file
wb = Workbook()
ws = wb.active

# Write DataFrame to sheet
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Save Excel file
filename = f'{date}.xlsx'
wb.save(os.path.join(xlsx_dir, filename))
