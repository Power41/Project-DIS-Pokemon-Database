CREATE TABLE pokemon_cards (
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
    resistance VARCHAR(50)
);