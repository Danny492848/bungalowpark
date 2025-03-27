from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from models.models import db, Bungalow, Guest #Importeert Modellen
import bcrypt
app = Flask(__name__)

#Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Change this for MySQL/PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session security

db.init_app(app)
migrate = Migrate(app,db) 

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Dit is de route waar gebruikers heen gaan als ze niet zijn ingelogd

# Zorg ervoor dat Flask-Login de gebruiker kan laden op basis van het ID
@login_manager.user_loader
def load_user(user_id):
    return Guest.query.get(int(user_id))

# Registratie route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Maak een nieuwe gebruiker
        new_user = Guest(username=username)
        new_user.set_password(password)  # Wachtwoord wordt gehashed voor het opslaan

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Stuur de gebruiker naar de loginpagina

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Guest.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Controleer of het wachtwoord klopt
            login_user(user)
            return redirect(url_for('booking'))  # Stuur de gebruiker naar de boekingspagina
        
        return "Fout wachtwoord of gebruikersnaam", 401

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))  # Stuur de gebruiker terug naar de loginpagina

#Flask Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Guest.query.get(int(user_id))




# Homepagina
@app.route('/')
def home():
    return render_template('index.html')

# Bungalows-pagina
@app.route('/bungalows')
def bungalows():
    bungalows = Bungalow.query.all()  # Get all bungalows from the database
    return render_template('bungalows.html', bungalows=bungalows)  # Pass them to the template

# Boekingspagina
@app.route('/booking', methods=['GET', 'POST'])
@login_required  # Zorgt ervoor dat je ingelogd moet zijn om de pagina te bekijken
def booking():
    if request.method == 'POST':
        bungalow_id = request.form.get('bungalow_id')
        week = request.form.get('week')

        # Maak een nieuwe boeking voor de ingelogde gebruiker
        new_booking = Booking(guest_id=current_user.id, bungalow_id=bungalow_id, week=week)
        
        db.session.add(new_booking)
        db.session.commit()

        return f"Boeking bevestigd voor Bungalow {bungalow_id} in week {week}"

    # Haal alle bungalows op uit de database
    bungalows = Bungalow.query.all()

    return render_template('booking.html', bungalows=bungalows)



if __name__ == '__main__':
    app.run(debug=True)
