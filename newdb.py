from app import app, db
from models.models import Guest

with app.app_context():
    # Verwijder bestaande tabellen (alleen voor ontwikkelomgeving)
    db.drop_all()
    db.create_all()

    # Voeg een admin-gebruiker toe
    admin_user = Guest(username="admin", email="admin@example.com", is_admin=True)
    admin_user.set_password("admin123")  # Wachtwoord voor admin
    db.session.add(admin_user)

    db.session.commit()
    print("Admin gebruiker toegevoegd!")
