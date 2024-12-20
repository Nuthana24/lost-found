from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample data structure
items = []

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_image_hash(image_path):
    """Calculate a hash for the image."""
    hash_md5 = hashlib.md5()
    try:
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except FileNotFoundError:
        return None
    return hash_md5.hexdigest()

@app.route('/')
def index():
    filter_type = request.args.get('filter', 'All')
    if filter_type == 'All':
        filtered_items = items
    else:
        filtered_items = [item for item in items if item['status'] == filter_type]
    return render_template('index.html', items=filtered_items, filter_type=filter_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Successfully logged out!')
    return redirect(url_for('login'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if not session.get('admin_logged_in'):
        flash('Please login first!')
        return redirect(url_for('login'))
    
    global items
    # Find and remove the item
    items = [item for item in items if item['id'] != item_id]
    flash('Item successfully deleted!')
    return redirect(url_for('admin'))

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

        item = {
            'id': len(items) + 1,
            'image': image_path,
            'title': request.form['title'],
            'category': request.form['category'],
            'description': request.form['description'],
            'location': request.form['location'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'status': request.form['status']
        }
        items.append(item)
        flash('Item successfully reported!')
        return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        flash('Please login first!')
        return redirect(url_for('login'))

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

            new_item = {
                'id': len(items) + 1,
                'image': image_path,
                'title': request.form['title'],
                'category': request.form['category'],
                'description': request.form['description'],
                'location': request.form['location'],
                'email': request.form['email'],
                'phone': request.form['phone'],
                'status': request.form['status']
            }
            items.append(new_item)
            flash('Item successfully added!')
        elif 'id' in request.form:
            # Handle editing existing item
            item_id = int(request.form['id'])
            item = next((i for i in items if i['id'] == item_id), None)
            if item:
                # Handle file upload for edited item
                if 'image' in request.files:
                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        item['image'] = f'uploads/{filename}'

                item.update({
                    'title': request.form['title'],
                    'category': request.form['category'],
                    'description': request.form['description'],
                    'location': request.form['location'],
                    'email': request.form['email'],
                    'phone': request.form['phone'],
                    'status': request.form['status']
                })
                flash('Item successfully updated!')

    # Compare images and find identical ones
    image_hash_map = {}
    similar_items = []
    for item in items:
        if item['image']:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(item['image']))
            image_hash = calculate_image_hash(image_path)
            if image_hash:
                if image_hash in image_hash_map:
                    similar_items.append((image_hash_map[image_hash], item))
                else:
                    image_hash_map[image_hash] = item

    return render_template('admin.html', items=items, similar_items=similar_items)



if __name__ == '__main__':
    app.run(debug=True)