from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os, json, re, datetime, random

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'

USERS_FILE = 'users.json'
HISTORY_FILE = 'history.json'
FAVS_FILE = 'favorites.json'

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_json(USERS_FILE)

        if not is_valid_email(email):
            flash('Bitte gib eine gültige E-Mail-Adresse ein.')
            return redirect(url_for('register'))

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
    if 'user' not in session:
        flash('Bitte einloggen.')
        return redirect(url_for('index'))
    return render_template('home.html', email=session['user'])

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
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX1tyCD9QhIWF",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWU0ScTcjJBdj",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWYBO1MoTDhZI",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX9XIFQuFvzM4",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3ZaylsKSCvK",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZKx3oSvn1ka",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWXRqgorJj26U",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWYkaDif7Ztbp"
            ]
        },
        "sad": {
            "quote": "Auch Regen gehört zum Wachsen dazu.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX7gIoKXt0gmx",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWWv6MSZULLBi",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3YSRoSdA634",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX5trt9i14X7j",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWU4EQPjP9ZpS",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWVIiR5qh2MFm",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ"
            ]
        },
        "chill": {
            "quote": "Atme tief durch und lass los.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX889U0CL85jj",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3PIPIT6lEg5",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX6VdMW310YC7",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZqd5JICZI0u",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWXX4UT26fTi1",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWXLeA8Omikj7",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DXbITWG1ZJKYt",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX4H7FFUM2osB",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWUa8ZRTfalHk"
            ]
        },
        "motivated": {
            "quote": "Heute ist dein Tag!",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZjqjZMudx9T",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZKx3oSvn1ka",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZZbwlv3Vmtr",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWYBO1MoTDhZI",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWUVpAXiEPK8P",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX1s9knjP51Oa",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX2aneNMeYHQ8",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWU6QmMWiv7mM"
            ]
        }
    }

    data = moods.get(mood, {})
    quote = data.get("quote", "Bleib motiviert!")
    playlist = random.choice(data.get("spotify", []))

    # Verlauf speichern
    history = load_json(HISTORY_FILE)
    user_history = history.get(session['user'], [])
    user_history.append({
        'mood': mood,
        'timestamp': datetime.datetime.now().isoformat()
    })
    history[session['user']] = user_history
    save_json(HISTORY_FILE, history)

    # Favoriten speichern (nicht doppelt)
    favorites = load_json(FAVS_FILE)
    user_favs = favorites.get(session['user'], [])
    exists = any(f['mood'] == mood and f['quote'] == quote for f in user_favs)
    if not exists:
        user_favs.append({'mood': mood, 'quote': quote})
        favorites[session['user']] = user_favs
        save_json(FAVS_FILE, favorites)

    return render_template("mood_result.html", mood=mood, quote=quote, spotify=playlist)

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
    favorites = load_json(FAVS_FILE)
    return jsonify(favorites.get(session['user'], []))

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'user' not in session:
        return jsonify({'status': 'unauthorized'}), 401

    data = request.get_json()
    mood = data.get('mood')
    quote = data.get('quote')

    favorites = load_json(FAVS_FILE)
    user_favs = favorites.get(session['user'], [])

    new_favs = [f for f in user_favs if not (f['mood'] == mood and f['quote'] == quote)]
    favorites[session['user']] = new_favs
    save_json(FAVS_FILE, favorites)

    return jsonify({'status': 'ok'})

@app.route('/load_users_moods')
def load_users_moods():
    if 'user' not in session:
        return jsonify([])
    history = load_json(HISTORY_FILE)
    result = []
    for user, entries in history.items():
        if entries:
            latest = sorted(entries, key=lambda e: e['timestamp'], reverse=True)[0]
            result.append({
                'email': user,
                'mood': latest['mood'],
                'timestamp': latest['timestamp']
            })
    return jsonify(result)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
