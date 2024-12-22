from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

DATABASE = 'lost_and_found.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)  # Remove the session variable
    flash('You have logged out successfully!')
    return redirect(url_for('login'))


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image TEXT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        db.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    filter_type = request.args.get('filter', 'All')
    db = get_db()
    if filter_type == 'All':
        items = db.execute('SELECT * FROM items').fetchall()
    else:
        items = db.execute(
            'SELECT * FROM items WHERE status = ?', (filter_type,)).fetchall()
    return render_template('index.html', items=items, filter_type=filter_type)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Handle file upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f'uploads/{filename}'

        db = get_db()
        db.execute('''
            INSERT INTO items (image, title, category, description, location, email, phone, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            image_path,
            request.form['title'],
            request.form['category'],
            request.form['description'],
            request.form['location'],
            request.form['email'],
            request.form['phone'],
            request.form['status']
        ))
        db.commit()
        flash('Item successfully reported!')
        return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        flash('Please login first!')
        return redirect(url_for('login'))

    db = get_db()
    if request.method == 'POST':
        if 'add-item' in request.form:
            # Handle file upload for new item
            image_path = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_path = f'uploads/{filename}'

            db.execute('''INSERT INTO items (image, title, category, description, location, email, phone, status)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                image_path,
                request.form['title'],
                request.form['category'],
                request.form['description'],
                request.form['location'],
                request.form['email'],
                request.form['phone'],
                request.form['status']
            ))
            db.commit()
            flash('Item successfully added!')

        elif 'id' in request.form:
            # Updating an existing item
            item_id = int(request.form['id'])
            item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
            if item:
                image_path = item['image']
                if 'image' in request.files:
                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_path = f'uploads/{filename}'

                db.execute('''UPDATE items SET image = ?, title = ?, category = ?, description = ?, location = ?, email = ?, phone = ?, status = ? WHERE id = ?''', (
                    image_path,
                    request.form['title'],
                    request.form['category'],
                    request.form['description'],
                    request.form['location'],
                    request.form['email'],
                    request.form['phone'],
                    request.form['status'],
                    item_id
                ))
                db.commit()
                flash('Item successfully updated!')

    # Get all items
    items = db.execute('SELECT * FROM items').fetchall()

    # Find similar items (items with the same image)
    image_map = {}
    for item in items:
        image = item['image']
        if image not in image_map:
            image_map[image] = []
        image_map[image].append(item)

    similar_items = []
    for image, grouped_items in image_map.items():
        if len(grouped_items) > 1:
            similar_items.append(grouped_items)

    return render_template('admin.html', items=items, similar_items=similar_items)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if not session.get('admin_logged_in'):
        flash('Please login first!')
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    flash('Item successfully deleted!')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
