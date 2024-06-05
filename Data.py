import pandas as pd
from sqlalchemy import create_engine

# Load CSV data
file_path = r'C:\Users\caspe\OneDrive - University of Copenhagen\DIS\Pokemon\Data\pokemon_first_gen_base.csv'
pokemon_data = pd.read_csv(file_path)

# Create a connection to PostgreSQL with correct credentials
username = 'postgres'  # Erstat med dit PostgreSQL brugernavn
password = '1234'  # Erstat med din PostgreSQL adgangskode
database = 'pokemon_db'
host = 'localhost'
port = '5432'

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

# Convert the ability column to boolean
pokemon_data['ability'] = pokemon_data['ability'].apply(lambda x: True if x == 'Yes' else False)

# Insert data into the PostgreSQL table
pokemon_data.to_sql('pokemon_cards', engine, if_exists='replace', index=False)