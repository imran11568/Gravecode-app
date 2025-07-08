from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
UPLOAD_FOLDER = 'upload_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            dod TEXT,
            bio TEXT,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        dod = request.form['dod']
        bio = request.form['bio']
        image = request.files['image']
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('profiles.db')
        c = conn.cursor()
        c.execute("INSERT INTO profiles (name, dob, dod, bio, image) VALUES (?, ?, ?, ?, ?)",
                  (name, dob, dod, bio, filename))
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return redirect(url_for('view', profile_id=new_id))
    return render_template('create.html')

@app.route('/profile/<int:profile_id>')
def view(profile_id):
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE id=?", (profile_id,))
    profile = c.fetchone()
    conn.close()
    return render_template('profile.html', profile=profile)

@app.route('/')
def home():
    return redirect(url_for('create'))

if __name__ == '__main__':
    app.run(debug=True)
