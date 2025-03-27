from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
db = SQLAlchemy()

# Guest Model (Users)
class Guest(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def check_password(self, password):
        # Controleer of het ingevoerde wachtwoord overeenkomt met het gehashte wachtwoord
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        # Zet het gehashte wachtwoord voor een nieuwe gebruiker
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
# Bungalow Type Model
class BungalowType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)  # 4, 6, or 8 persons
    price_per_week = db.Column(db.Float, nullable=False)

# Bungalow Model
class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('bungalow_type.id'), nullable=False)
    bungalow_type = db.relationship('BungalowType', backref='bungalows')

# Booking Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)  # Stores week number (1-52)
    guest = db.relationship('Guest', backref='bookings')
    bungalow = db.relationship('Bungalow', backref='bookings')
