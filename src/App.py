from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__, static_url_path='/static')

# Configuration for PostgreSQL connection
username = 'postgres'  # Replace with your PostgreSQL username
password = '1234'  # Replace with your PostgreSQL password
database = 'pokemon_db' # Name of the database (Database should be created before running the script)
host = 'localhost'
port = '5432'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{database}'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

################################################################################################
# Database Models #

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Specify the table name
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed password

    def get_id(self):
        return self.username

# Pokemon Cards Table
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

# Favorites Table
class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False)

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

################################################################################################
# Helper functions to retrieve distinct values
def get_all_sets():
    sets = db.session.query(PokemonCard.set).distinct().all()
    return [s[0] for s in sets]

def get_all_types():
    types = db.session.query(PokemonCard.type).distinct().all()
    return [t[0] for t in types]

def get_all_subtypes():
    subtypes = db.session.query(PokemonCard.subtypes).distinct().all()
    return [st[0] for st in subtypes]

def get_all_weaknesses():
    weaknesses = db.session.query(PokemonCard.weakness).filter(PokemonCard.weakness != '').distinct().all()
    return [w[0] for w in weaknesses]

def get_all_resistances():
    resistances = db.session.query(PokemonCard.resistance).filter(PokemonCard.resistance != '').distinct().all()
    return [r[0] for r in resistances]

def get_all_rarities():
    rarities = db.session.query(PokemonCard.rarity).distinct().all()
    return [r[0] for r in rarities]

def get_filtered_data(filters):
    query = db.session.query(PokemonCard)
    
    if filters['start_letters']:
        query = query.filter(PokemonCard.name.ilike(f"{filters['start_letters']}%"))
    
    if filters['set']:
        query = query.filter(PokemonCard.set == filters['set'])
    
    if filters['type']:
        query = query.filter(PokemonCard.type == filters['type'])
    
    if filters['subtypes']:
        query = query.filter(PokemonCard.subtypes == filters['subtypes'])
    
    if filters['ability']:
        query = query.filter(PokemonCard.ability == (filters['ability'] == 'True'))
    
    if filters['weakness']:
        if filters['weakness'] == 'None':
            query = query.filter((PokemonCard.weakness == '') | (PokemonCard.weakness == None))
        else:
            query = query.filter(PokemonCard.weakness == filters['weakness'])
    
    if filters['resistance']:
        if filters['resistance'] == 'None':
            query = query.filter((PokemonCard.resistance == '') | (PokemonCard.resistance == None))
        else:
            query = query.filter(PokemonCard.resistance == filters['resistance'])
    
    if filters['rarity']:
        query = query.filter(PokemonCard.rarity == filters['rarity'])

    if filters['hp']:
        query = query.filter(PokemonCard.hp >= int(filters['hp']))
    
    if filters['level']:
        query = query.filter(PokemonCard.level >= int(filters['level']))
    
    if filters['retreat_cost']:
        query = query.filter(PokemonCard.retreatCost >= int(filters['retreat_cost']))
    
    return query.all()
###########################################################################################################

# Login Manager
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# Routes
@app.route('/')
@login_required
def index():
    sets = get_all_sets()
    types = get_all_types()
    subtypes = get_all_subtypes()
    weaknesses = get_all_weaknesses()
    resistances = get_all_resistances()
    rarities = get_all_rarities()

    filters = {
        'start_letters': request.args.get('start_letters', ''),
        'set': request.args.get('set', ''),
        'type': request.args.get('type', ''),
        'subtypes': request.args.get('subtypes', ''),
        'ability': request.args.get('ability', ''),
        'weakness': request.args.get('weakness', ''),
        'resistance': request.args.get('resistance', ''),
        'rarity': request.args.get('rarity', ''),
        'hp': request.args.get('hp', ''),
        'level': request.args.get('level', ''),
        'retreat_cost': request.args.get('retreat_cost', '')
    }

    data = get_filtered_data(filters)

    return render_template('index.html', sets=sets, types=types, subtypes=subtypes, weaknesses=weaknesses, resistances=resistances, rarities=rarities, filters=filters, data=data)

# Route for Pokemon details
@app.route('/pokemon/<int:id>', methods=['GET', 'POST'])
@login_required
def pokemon_detail(id):
    pokemon = PokemonCard.query.get_or_404(id)
    pokemon.image_url = url_for('static', filename=f'images/{pokemon.id}.jpg')

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            favorite = Favorite(pokemon_id=pokemon.id, username=current_user.username)
            db.session.add(favorite)
            db.session.commit()
            flash('Added to favorites!', 'success')
        elif action == 'remove':
            favorite = Favorite.query.filter_by(pokemon_id=pokemon.id, username=current_user.username).first()
            if favorite:
                db.session.delete(favorite)
                db.session.commit()
                flash('Removed from favorites!', 'success')

    is_favorite = Favorite.query.filter_by(pokemon_id=pokemon.id, username=current_user.username).first() is not None

    return render_template('pokemon_detail.html', pokemon=pokemon, is_favorite=is_favorite)


# Route for favorites
@app.route('/profile')
@login_required
def profile():
    favorites = Favorite.query.filter_by(username=current_user.username).all()
    favorite_pokemons = []
    for fav in favorites:
        pokemon = PokemonCard.query.get(fav.pokemon_id)
        if pokemon:
            favorite_pokemons.append(pokemon)
    return render_template('profile.html', favorites=favorite_pokemons)

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        print(f"Registered user: {user.username}, {user.password}")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(f"Attempting login for: {form.username.data}")
        
        if user:
            print(f"Found user: {user.username}")
            stored_password = user.password.strip()
            entered_password = form.password.data.strip()
            print(f"Stored password: '{stored_password}'")
            print(f"Entered password: '{entered_password}'")
            
            if stored_password == entered_password:
                login_user(user, remember=True)
                print(f"Login successful for: {user.username}")
                print(f"Current user: {current_user.username}")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Incorrect password.', 'incorrect_password')
                print(f"Login failed for: {form.username.data}, Incorrect password")
        else:
            flash('Username not found.', 'username_not_found')
            print(f"Login failed: user not found for {form.username.data}")
    
    print(f"Current user authenticated: {current_user.is_authenticated}")
    return render_template('login.html', title='Login', form=form)

# Route for logout
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)














