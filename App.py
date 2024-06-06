from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__, static_url_path='/static')

# Configuration for PostgreSQL connection
username = 'postgres'  # Erstat med dit PostgreSQL brugernavn
password = '1234'  # Erstat med din PostgreSQL adgangskode
database = 'pokemon_db'
host = 'localhost'
port = '5432'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{database}'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Specify the table name
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

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

@app.route('/')
@login_required
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
@login_required
def pokemon_detail(id):
    pokemon = PokemonCard.query.get_or_404(id)
    pokemon.image_url = url_for('static', filename=f'images/{pokemon.id}.jpg')
    return render_template('pokemon_detail.html', pokemon=pokemon)



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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
