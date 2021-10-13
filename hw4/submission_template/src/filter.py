import os
import pandas as pd

data_dir_path = os.path.join('/', 'home', 'ben', 'projects', 'comp598-2021', 'hw4', 'submission_template', 'data')
dataset_path = os.path.join(data_dir_path, 'nyc_311_limit_slim.csv')
df = pd.read_csv(dataset_path, 
                 dtype={'Incident Zip': 'str'})

# filter cases that weren't open in 2020
df = df[df['Created Date'].str.contains('/2020') | df['Closed Date'].str.contains('/2020')]

# filter invalid zip codes
df = df[df['Incident Zip'].notna()]

# filter invalid dates
df['Created Date'] = pd.to_datetime(df['Created Date'], filter='%m/%d/%Y %I:%M:%S %p')
df['Closed Date'] = pd.to_datetime(df['Closed Date'], filter='%m/%d/%Y %I:%M:%S %p')
df = df[df['Created Date'] < df['Closed Date']]

new_dataset_path = os.path.join(data_dir_path, 'nyc_311_limit_filtered.csv')
df.to_csv(new_dataset_path)