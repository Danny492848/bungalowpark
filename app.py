from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from models.models import db, Bungalow, Booking, Guest #Importeert Modellen
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check of gebruiker al bestaat
        existing_user = Guest.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is al in gebruik!", "danger")
            return redirect(url_for('register'))

        # Nieuwe gebruiker aanmaken
        new_user = Guest(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account succesvol aangemaakt! Je kunt nu inloggen.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Zoek gebruiker in database
        user = Guest.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for('home'))
        else:
            flash("Ongeldige login!", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Uitgelogd!", "info")
    return redirect(url_for('home'))

#Flask Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Guest.query.get(int(user_id))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash("Je hebt geen toegang tot deze pagina.", "danger")
        return redirect(url_for('home'))  # Redirect naar de homepagina als je geen admin bent

    # Haal alle bungalows op voor weergave
    bungalows = Bungalow.query.all()

    if request.method == 'POST':
        bungalow_id = request.form.get('bungalow_id')
        new_name = request.form.get('new_name')
        new_price = request.form.get('new_price')

        bungalow = Bungalow.query.get(bungalow_id)
        if bungalow:
            bungalow.name = new_name
            bungalow.bungalow_type.price_per_week = new_price  # Wijzig de prijs van het bijbehorende BungalowType
            db.session.commit()

            flash(f"Bungalow '{bungalow.name}' succesvol bijgewerkt!", "success")
        else:
            flash("Bungalow niet gevonden!", "danger")

    return render_template('admin.html', bungalows=bungalows)


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
@login_required
def booking():
    if request.method == 'POST':
        bungalow_id = request.form['bungalow_id']
        week_str = request.form['week']  # e.g. "2025-W14"

        # Convert to integer format: 202514
        try:
            year, week = map(int, week_str.split("-W"))
            week_int = int(f"{year}{week:02d}")
        except ValueError:
            flash("Ongeldig weekformaat!", "danger")
            return redirect(url_for('booking') + "#modal")

        # Check if already booked
        existing_booking = Booking.query.filter_by(bungalow_id=bungalow_id, week=week_int).first()
        if existing_booking:
            flash("Deze bungalow is al geboekt voor deze week!", "danger")
            return redirect(url_for('booking') + "#modal")

        # Create new booking
        new_booking = Booking(
            guest_id=current_user.id,
            bungalow_id=bungalow_id,
            week=week_int
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('confirmation'))

    # GET request: show booking form
    selected_bungalow_id = request.args.get('bungalow_id', type=int)
    bungalows = Bungalow.query.all()
    return render_template('booking.html', bungalows=bungalows, selected_bungalow_id=selected_bungalow_id)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        return redirect(url_for('home'))  # Alleen admin toegang

    # Haal alle boekingen op
    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/admin/edit_booking/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Haal alle gebruikers op voor de dropdown
    users = Guest.query.all()
    
    if request.method == 'POST':
        # Verwerk de veranderingen in de boeking
        new_user_id = request.form.get('user_id')
        new_user = Guest.query.get(new_user_id)
        
        if new_user:
            booking.user_id = new_user.id
            db.session.commit()
            flash("Boeking succesvol aangepast!", "success")
        else:
            flash("Gebruiker niet gevonden.", "error")
        
        # Optioneel: Verwijder de boeking
        if 'delete_booking' in request.form:
            db.session.delete(booking)
            db.session.commit()
            flash("Boeking succesvol verwijderd!", "success")
            return redirect(url_for('admin'))  # Ga terug naar het admin paneel

    return render_template('edit_booking.html',bungalow=bungalows, booking=booking, users=users)


if __name__ == '__main__':
    app.run(debug=True)
