# 💾 Datei: app.py (komplett überarbeitet – Mood, Verlauf, Favoriten)
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json, os, datetime, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'

USERS_FILE = 'users.json'
HISTORY_FILE = 'history.json'
FAV_FILE = 'favorites.json'

# Sicherstellen, dass JSON-Dateien existieren
def init_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({}, f)

for file in [USERS_FILE, HISTORY_FILE, FAV_FILE]:
    init_file(file)

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_json(USERS_FILE)

        if email in users:
            flash('E-Mail existiert bereits.')
            return redirect(url_for('register'))

        users[email] = {'password': generate_password_hash(password)}
        save_json(USERS_FILE, users)

        flash('Registrierung erfolgreich.')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    users = load_json(USERS_FILE)
    if email in users and check_password_hash(users[email]['password'], password):
        session['user'] = email
        return redirect(url_for('home'))
    flash('Login fehlgeschlagen.')
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', email=session['user'])
    flash('Bitte logge dich ein.')
    return redirect(url_for('index'))

@app.route('/mood', methods=['POST'])
def mood():
    if 'user' not in session:
        flash('Bitte einloggen.')
        return redirect(url_for('index'))

    mood = request.form['mood']
    moods = {
        "happy": {
            "quote": "Lächle, und die Welt lächelt mit dir.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
                "https://open.spotify.com/embed/playlist/1h0CEZCm6IbFTbxThn6Xcs"
            ]
        },
        "sad": {
            "quote": "Auch Regen gehört zum Wachsen dazu.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1"
            ]
        },
        "chill": {
            "quote": "Atme tief durch und lass los.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWSkMjlBZAZ07"
            ]
        },
        "motivated": {
            "quote": "Heute ist dein Tag!",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DXdxcBWuJkbcy"
            ]
        }
    }
    data = moods.get(mood, {})
    quote = data.get("quote")
    spotify = random.choice(data.get("spotify", []))

    # Verlauf speichern
    history = load_json(HISTORY_FILE)
    user_history = history.get(session['user'], [])
    user_history.append({"mood": mood, "timestamp": datetime.datetime.now().isoformat()})
    history[session['user']] = user_history
    save_json(HISTORY_FILE, history)

    # Favorit speichern
    favorites = load_json(FAV_FILE)
    user_favs = favorites.get(session['user'], [])
    user_favs.append({"mood": mood, "quote": quote})
    favorites[session['user']] = user_favs
    save_json(FAV_FILE, favorites)

    return render_template("mood_result.html", mood=mood, quote=quote, spotify=spotify)

@app.route('/load_history')
def load_history():
    if 'user' not in session:
        return jsonify([])
    history = load_json(HISTORY_FILE)
    return jsonify(history.get(session['user'], []))

@app.route('/load_favorites')
def load_favorites():
    if 'user' not in session:
        return jsonify([])
    favorites = load_json(FAV_FILE)
    return jsonify(favorites.get(session['user'], []))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
