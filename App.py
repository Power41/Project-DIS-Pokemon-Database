from flask import Flask, render_template, request, url_for
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
    rarity = db.Column(db.String(50))
    # description = db.Column(db.String(500))  # Commented out for now

@app.route('/')
def index():
    query = PokemonCard.query
    
    start_letters = request.args.get('start_letters', '')
    set_ = request.args.get('set', '')
    type_ = request.args.get('type', '')
    subtypes = request.args.get('subtypes', '')
    level = request.args.get('level', '')
    hp = request.args.get('hp', '')
    retreat_cost = request.args.get('retreat_cost', '')
    ability = request.args.get('ability', '')
    weakness = request.args.get('weakness', '')
    resistance = request.args.get('resistance', '')
    rarity = request.args.get('rarity', '')

    if start_letters:
        query = query.filter(PokemonCard.name.ilike(f'{start_letters}%'))
    if set_:
        query = query.filter(PokemonCard.set.ilike(f'{set_}%'))
    if type_:
        query = query.filter(PokemonCard.type.ilike(f'{type_}%'))
    if subtypes:
        query = query.filter(PokemonCard.subtypes.ilike(f'{subtypes}%'))
    if level:
        query = query.filter(PokemonCard.level == level)
    if hp:
        query = query.filter(PokemonCard.hp == hp)
    if retreat_cost:
        query = query.filter(PokemonCard.retreatCost == retreat_cost)
    if ability:
        query = query.filter(PokemonCard.ability == (ability.lower() == 'yes'))
    if weakness:
        query = query.filter(PokemonCard.weakness.ilike(f'{weakness}%'))
    if resistance:
        query = query.filter(PokemonCard.resistance.ilike(f'{resistance}%'))
    if rarity:
        query = query.filter(PokemonCard.rarity.ilike(f'{rarity}%'))

    pokemon_cards = query.all()

    for card in pokemon_cards:
        card.image_url = url_for('static', filename=f'CardN/{card.id}.jpg')
    
    filters = {
        'start_letters': start_letters,
        'set': set_,
        'type': type_,
        'subtypes': subtypes,
        'level': level,
        'hp': hp,
        'retreat_cost': retreat_cost,
        'ability': ability,
        'weakness': weakness,
        'resistance': resistance,
        'rarity': rarity
    }

    return render_template('index.html', data=pokemon_cards, filters=filters)

@app.route('/pokemon/<int:id>')
def pokemon_detail(id):
    pokemon = PokemonCard.query.get_or_404(id)
    pokemon.image_url = url_for('static', filename=f'CardN/{pokemon.id}.jpg')
    return render_template('pokemon_detail.html', pokemon=pokemon)

if __name__ == '__main__':
    app.run(debug=True)
