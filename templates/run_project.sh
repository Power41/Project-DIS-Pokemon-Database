#!/bin/bash

# Trin 1: Opret database, hvis den ikke allerede findes
psql -U postgres -h localhost -tc "SELECT 1 FROM pg_database WHERE datname = 'pokemon_db'" | grep -q 1 || psql -U postgres -h localhost -c "CREATE DATABASE pokemon_db;"

# Trin 2: Slet eksisterende tabeller, hvis de findes, og opret dem på ny # Update path to file
psql -U postgres -d pokemon_db -h localhost <<EOF
DROP TABLE IF EXISTS pokemon_cards;
-- Gentag DROP TABLE for andre tabeller, du vil slette

\i /Users/malthejohansen/Documents/UNI/DIS/Project/Create_table.SQL 
EOF

# Trin 3: Importer data
python /Users/malthejohansen/Documents/UNI/DIS/Project/Data.py # Update path to file

# Trin 4: Kør applikationen
python /Users/malthejohansen/Documents/UNI/DIS/Project/App.py # Update path to file
