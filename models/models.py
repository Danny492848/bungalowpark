from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class BungalowType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)  # 4, 6 of 8 personen
    weekly_price = db.Column(db.Float, nullable=False)

class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)  # bijvoorbeeld 4, 6 of 8 personen
    price_per_week = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Bungalow {self.name}>'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
