#python progrom to display and store of signup,login and dashboard page in database
from flask import Flask, render_template, request, redirect, url_for, session
# redirect:-Sends user to another page
# url_for:-Finds route URL by function name
#session:-Stores user login info
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'geetha_secret_key' # Required for sessions

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Geetha%402004@localhost/bamul_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('signup'))

# --- SIGN UP ROUTE ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or len(password) < 6:
            return "Invalid Credentials: Password must be 6+ chars", 400

        try:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) # Redirect to login after success
        except:
            db.session.rollback()
            return "Email already exists!", 400
            
    return render_template('signup.html')

# --- LOGIN ROUTE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password", 401

    return render_template('login.html')

# --- DASHBOARD ROUTE ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', name=session['user_name'])
    return redirect(url_for('login'))

# --- LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.clear() # Ends the session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)