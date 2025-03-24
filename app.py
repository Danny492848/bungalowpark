from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Homepagina
@app.route('/')
def home():
    return render_template('index.html')

# Bungalows-pagina
@app.route('/bungalows')
def bungalows():
    # Simuleer een lijst van bungalows
    bungalow_list = [
        {'id': 1, 'name': 'Duinhuis', 'type': 'Luxe', 'capacity': 6, 'price': 750},
        {'id': 2, 'name': 'Strandvilla', 'type': 'Premium', 'capacity': 8, 'price': 950}
    ]
    return render_template('bungalows.html', bungalows=bungalow_list)

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
