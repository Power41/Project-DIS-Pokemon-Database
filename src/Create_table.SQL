
-- Drop tables if they exist
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS pokemon_cards CASCADE;

-- Create pokemon_cards table if it doesn't exist
CREATE TABLE IF NOT EXISTS pokemon_cards (
    id SERIAL PRIMARY KEY,
    set VARCHAR(50),
    name VARCHAR(100),
    type VARCHAR(50),
    subtypes VARCHAR(50),
    level INTEGER,
    hp INTEGER,
    ability BOOLEAN,
    weakness VARCHAR(50),
    retreatCost INTEGER,
    resistance VARCHAR(50),
    rarity VARCHAR(50)
);

-- Create the users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username)
);

-- Create the favorites table if it doesn't exist
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    pokemon_id INTEGER NOT NULL,
    username VARCHAR(20) NOT NULL,
    CONSTRAINT fk_username FOREIGN KEY(username) REFERENCES users(username)
);









