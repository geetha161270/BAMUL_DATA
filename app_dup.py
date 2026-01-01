from flask import Flask, render_template, request
# render_template:-Used to show HTML pages (index.html).
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# UPDATED: Changed 'bamul' to 'bamul_db' to match your MySQL terminal
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Geetha%402004@localhost/bamul_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Connects Flask app to database
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()
# Flask needs application context to access config & DB.
@app.route('/')
# when user opens,flask loads
def index():
    return render_template('index.html')

# Ensure this route matches exactly what you type in Postman/HTML
@app.route('/signup', methods=['POST'])
# accepts POST requests and matches HTML form
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or len(password) < 6:
        return "<h3>Invalid Credentials: Password must be at least 6 characters.</h3>", 400

    try:
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f"<h1>Welcome to BAMUL DATABASE, {name}!</h1>"
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)