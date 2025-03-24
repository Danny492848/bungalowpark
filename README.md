📂 bungalowpark/ (hoofddirectory)
├── 📂 static/ (CSS, JavaScript, afbeeldingen)
│ ├── style.css (eigen CSS bovenop Bootstrap)
│ ├── script.js (eventuele JavaScript-functionaliteit)
│ ├── 📂 img/ (afbeeldingen voor de site)
│
├── 📂 templates/ (HTML-pagina’s, gebruikt Jinja2)
│ ├── base.html (hoofdsjabloon met Bootstrap)
│ ├── index.html (homepagina)
│ ├── bungalows.html (overzicht van bungalows)
│ ├── booking.html (reserveringspagina)
│
├── 📂 routes/ (verschillende functionaliteiten)
│ ├── auth.py (inloggen/registreren)
│ ├── bookings.py (reserveringen beheren)
│ ├── bungalows.py (lijst van huisjes tonen)
│
├── 📂 models/ (database-tabellen met SQLAlchemy)
│ ├── models.py (database-modellen zoals User, Booking, Bungalow)
│
├── app.py (hoofdscript om Flask-app te starten)
├── config.py (instellingen, zoals database-configuratie)
├── requirements.txt (lijst met benodigde Python-pakketten en versies)
├── README.md (uitleg over het project en installatie-instructies)