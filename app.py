from flask import Flask, render_template, redirect, request, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session management

# Dummy credentials for demonstration purposes
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Report page route
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        description = request.form.get('description')
        print(f"Lost product: {product_name}, Description: {description}")
        return render_template('report.html', message="Report submitted successfully.")
    return render_template('report.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Save login status in session
            return redirect(url_for('admin'))  # Redirect to admin panel
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# Admin panel route
@app.route('/admin')
def admin():
    if 'logged_in' not in session or not session['logged_in']:
        flash('You need to log in to access the admin panel.', 'danger')
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    return render_template('admin.html')  # Admin dashboard page

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))  # Redirect to login page

# Home route (optional)
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login page by default

if __name__ == '__main__':
    app.run(debug=True)
