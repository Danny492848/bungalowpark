from app import app, db
from models.models import BungalowType, Bungalow  # Importeer de modellen

with app.app_context():
    # Verwijder bestaande tabellen (alleen voor ontwikkelomgeving)
    db.drop_all()
    db.create_all()

    # Voeg de bungalow types toe
    bungalow_type_4 = BungalowType(size=4, price_per_week=500)
    bungalow_type_6 = BungalowType(size=6, price_per_week=750)
    bungalow_type_8 = BungalowType(size=8, price_per_week=1000)

    db.session.add(bungalow_type_4)
    db.session.add(bungalow_type_6)
    db.session.add(bungalow_type_8)
    db.session.commit()  # Zorg ervoor dat de types eerst zijn toegevoegd

    # Voeg bungalows toe met de juiste type_id
    bungalow1 = Bungalow(name="Duinroos", type_id=bungalow_type_4.id)
    bungalow2 = Bungalow(name="Zonnestrand", type_id=bungalow_type_4.id)
    bungalow3 = Bungalow(name="Bosrand Lodge", type_id=bungalow_type_6.id)
    bungalow4 = Bungalow(name="Zeezicht Villa", type_id=bungalow_type_6.id)
    bungalow5 = Bungalow(name="Strandpaviljoen", type_id=bungalow_type_8.id)
    bungalow6 = Bungalow(name="Duinenhof", type_id=bungalow_type_8.id)

    db.session.add_all([bungalow1, bungalow2, bungalow3, bungalow4, bungalow5, bungalow6])
    db.session.commit()  # Commit de wijzigingen naar de database

    print("Voorbeelddata toegevoegd succesvol!")
