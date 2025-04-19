from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os, re, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dein_geheimer_schluessel'

USERS_FILE = 'users.json'
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

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
        users = load_users()

        if not is_valid_email(email):
            flash('Bitte gib eine gültige E-Mail-Adresse ein.')
            return redirect(url_for('register'))

        if email in users:
            flash('E-Mail existiert bereits.')
            return redirect(url_for('register'))

        users[email] = {'password': generate_password_hash(password)}
        save_users(users)

        flash('Registrierung erfolgreich. Jetzt einloggen.')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    users = load_users()
    if email in users and check_password_hash(users[email]['password'], password):
        session['user'] = email
        return redirect(url_for('home'))
    else:
        flash('Login fehlgeschlagen.')
        return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', email=session['user'])
    else:
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
                "https://open.spotify.com/embed/playlist/1h0CEZCm6IbFTbxThn6Xcs",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWYBO1MoTDhZI"
            ]
        },
        "sad": {
            "quote": "Auch Regen gehört zum Wachsen dazu.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWVV27DiNWxkR",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX3YSRoSdA634"
            ]
        },
        "chill": {
            "quote": "Atme tief durch und lass los.",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX4WYpdgoIcn6",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWSkMjlBZAZ07",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWTkIwO2HDifB"
            ]
        },
        "motivated": {
            "quote": "Heute ist dein Tag!",
            "spotify": [
                "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DXdxcBWuJkbcy",
                "https://open.spotify.com/embed/playlist/37i9dQZF1DWZjqjZMudx9T"
            ]
        }
    }
    data = moods.get(mood, {})
    quote = data.get("quote")
    spotify_list = data.get("spotify", [])
    spotify = random.choice(spotify_list) if spotify_list else ""

    return render_template("mood_result.html", mood=mood, quote=quote, spotify=spotify)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
