import os
import pandas as pd

data_dir_path = os.path.join('/', 'home', 'ben', 'projects', 'comp598-2021', 'hw4', 'submission_template', 'data')
dataset_path = os.path.join(data_dir_path, 'nyc_311_limit_2020.csv')
df = pd.read_csv(dataset_path, 
                 names=['Unique Key', 'Created Date', 'Closed Date', 'Agency', 'Agency Name', 'Complaint Type', 'Descriptor', 'Location Type', 'Incident Zip', 'Incident Address', 'Street Name', 'Cross Street 1', 'Cross Street 2', 'Intersection Street 1', 'Intersection Street 2', 'Address Type', 'City', 'Landmark', 'Facility Type', 'Status', 'Due Date', 'Resolution Description', 'Resolution Action Updated Date', 'Community Board', 'BBL', 'Borough', 'X Coordinate (State Plane)', 'Y Coordinate (State Plane)', 'Open Data Channel Type', 'Park Facility Name', 'Park Borough', 'Vehicle Type', 'Taxi Company Borough', 'Taxi Pick Up Location', 'Bridge Highway Name', 'Bridge Highway Direction', 'Road Ramp', 'Bridge Highway Segment', 'Latitude', 'Longitude', 'Location'],
                 dtype={'Incident Zip': 'str'})

# filter cases that weren't open in 2020
df = df[df['Created Date'].dt.year == 2020 | df['Closed Date'].dt.year == 2020]

# filter invalid zip codes
df = df[df['Incident Zip'].notna()]

# filter invalid dates
df = df[df['Created Date'].dt < df['Closed Date'].dt]

new_dataset_path = os.path.join(data_dir_path, 'nyc_311_limit_filtered.csv')
df.to_csv(new_dataset_path)