from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for PostgreSQL connection
username = 'postgres'  # Erstat med dit PostgreSQL brugernavn
password = '1234'  # Erstat med din PostgreSQL adgangskode
database = 'pokemon_db'
host = 'localhost'
port = '5432'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PokemonCard(db.Model):
    __tablename__ = 'pokemon_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    set = db.Column(db.String(50))
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    subtypes = db.Column(db.String(50))
    level = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    ability = db.Column(db.Boolean)
    weakness = db.Column(db.String(50))
    retreatCost = db.Column(db.Integer)
    resistance = db.Column(db.String(50))

@app.route('/')
def index():
    pokemon_cards = PokemonCard.query.all()
    for card in pokemon_cards:
        card.image_url = url_for('static', filename=f'CardN/{card.id}.jpg')
    return render_template('index.html', data=pokemon_cards)

if __name__ == '__main__':
    app.run(debug=True)