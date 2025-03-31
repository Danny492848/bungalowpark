from app import app, db
from models.models import BungalowType, Bungalow  # Importeer de modellen

with app.app_context():
    db.create_all()  # Zorg ervoor dat de tabellen worden aangemaakt

    # Voeg bungalowtypes toe
    bungalow_type_4 = BungalowType.query.filter_by(size=4).first()
    if not bungalow_type_4:
        bungalow_type_4 = BungalowType(size=4, price_per_week=500)
        db.session.add(bungalow_type_4)

    bungalow_type_6 = BungalowType.query.filter_by(size=6).first()
    if not bungalow_type_6:
        bungalow_type_6 = BungalowType(size=6, price_per_week=750)
        db.session.add(bungalow_type_6)

    bungalow_type_8 = BungalowType.query.filter_by(size=8).first()
    if not bungalow_type_8:
        bungalow_type_8 = BungalowType(size=8, price_per_week=1000)
        db.session.add(bungalow_type_8)

    db.session.commit()

    # Voeg bungalows toe zonder duplicaten
    bungalows = [
        {"name": "Duinroos", "type_id": bungalow_type_4.id},
        {"name": "Zonnestrand", "type_id": bungalow_type_4.id},
        {"name": "Bosrand Lodge", "type_id": bungalow_type_6.id},
        {"name": "Zeezicht Villa", "type_id": bungalow_type_6.id},
        {"name": "Strandpaviljoen", "type_id": bungalow_type_8.id},
        {"name": "Duinenhof", "type_id": bungalow_type_8.id}
    ]

    for bungalow_data in bungalows:
        bungalow = Bungalow.query.filter_by(name=bungalow_data["name"]).first()
        if not bungalow:
            bungalow = Bungalow(name=bungalow_data["name"], type_id=bungalow_data["type_id"])
            db.session.add(bungalow)

    db.session.commit()
    print("Voorbeelddata toegevoegd succesvol!")
