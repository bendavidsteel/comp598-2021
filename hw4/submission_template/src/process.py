import os

import pandas as pd

this_dir_path = os.path.dirname(os.path.abspath(__file__))
data_dir_path = os.path.join(this_dir_path, '..', 'data')
dataset_path = os.path.join(data_dir_path, 'nyc_311_limit_filtered.csv')

df = pd.read_csv(dataset_path, 
                 dtype={'Incident Zip': 'str'})
df['Created Date'] = pd.to_datetime(df['Created Date'], infer_datetime_format=True)
df['Closed Date'] = pd.to_datetime(df['Closed Date'], infer_datetime_format=True)
df['Duration'] = (df['Closed Date'] - df['Created Date']).dt.total_seconds // 3600
df['Month'] = df['Closed Date'].dt.month

df = df[['Incident Zip', 'Month', 'Duration']]

all_df = df.groupby('Month')['Duration'].mean()

zipcodes_df = df.groupby('Month', 'Incident Zip')
