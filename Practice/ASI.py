from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database functions
def create_database():
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assets')
    assets = cursor.fetchall()
    conn.close()
    return render_template('index.html', assets=assets)

@app.route('/add', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        number = request.form['NO.']
        active = request.form['Active']
        inactive = request.form['Inactive']
        operating = request.form['Operating']
        consolidated = request.form['Consolidated']

        conn = sqlite3.connect('assets.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO assets (number, active, inactive, operating, consolidated) VALUES (?, ?, ?)', (number, active, inactive, operating, consolidated))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        number = request.form['NO.']
        active = request.form['Active']
        inactive = request.form['Inactive']
        operating = request.form['Operating']
        consolidated = request.form['Consolidated']
        cursor.execute('UPDATE assets SET number=?, active=?, inactive=?, operating=?, consolidated=? WHERE id=?', (number, active, inactive, operating, consolidated, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM assets WHERE id=?', (id,))
    asset = cursor.fetchone()
    conn.close()
    return render_template('edit.html', asset=asset)

@app.route('/delete/<int:id>')
def delete_asset(id):
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM assets WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)