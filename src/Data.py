import pandas as pd
from sqlalchemy import create_engine

# Configuration for PostgreSQL connection
username = 'postgres'
password = '1234'
database = 'pokemon_db'
host = 'localhost'
port = '5432'

# Database connection
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

# Load data from CSV file
pokemon_data = pd.read_csv('Your-file-directory/tmp/Project_data.csv')

pokemon_data['ability'] = pokemon_data['ability'].apply(lambda x: True if x == 'Yes' else False)

# Load data into the pokemon_cards table
pokemon_data.to_sql('pokemon_cards', engine, if_exists='replace', index=False)

print("Data loaded successfully")


