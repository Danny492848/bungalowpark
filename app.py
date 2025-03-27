from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from models.models import db, Bungalow, Guest #Importeert Modellen

app = Flask(__name__)

#Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Change this for MySQL/PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session security

db.init_app(app)
migrate = Migrate(app,db) 

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
def booking():
    if request.method == 'POST':
        bungalow_id = request.form.get('bungalow_id')
        week = request.form.get('week')
        return f"Boeking bevestigd voor Bungalow {bungalow_id} in week {week}"

    # Simuleer een lijst van bungalows voor de dropdown
    bungalow_list = [
        {'id': 1, 'name': 'Duinhuis', 'type': 'Luxe', 'capacity': 6, 'price': 750},
        {'id': 2, 'name': 'Strandvilla', 'type': 'Premium', 'capacity': 8, 'price': 950}
    ]
    return render_template('booking.html', bungalows=bungalow_list)

if __name__ == '__main__':
    app.run(debug=True)
