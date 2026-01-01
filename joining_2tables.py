from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:Geetha%402004@localhost/bamul'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    houses = db.relationship('House', backref='owner', lazy=True)
# backref='owner' → house.owner gives the user

# lazy=True → load houses only when needed

class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    house_number = db.Column(db.String(50))
    house_address = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@app.route('/')
def home():
    return "API is running!"

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_with_house(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # If the user has no houses, this list will be empty
    house_data = []
    for house in user.houses:
        house_data.append({
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "house_number": house.house_number,
            "house_address": house.house_address
        })

    return jsonify(house_data)


@app.route('/add_user_house', methods=['POST'])
def add_user_house():
    data = request.get_json()

    # 1. Create the User
    new_user = User(
        name=data.get('name'),
        email=data.get('email')
    )
    db.session.add(new_user)
    db.session.flush() # flush() Sends SQL to DB not permanently
    # 2. Create the House (associated with the user)
    if 'house_number' in data:
        new_house = House(
            house_number=data.get('house_number'),
            house_address=data.get('house_address'),
            user_id=new_user.id
        )
        db.session.add(new_house)

    # 3. Commit both to the database
    db.session.commit()

    return jsonify({"message": "User and House added successfully!"}), 201

@app.route('/update_user_house/<int:user_id>/<int:house_id>', methods=['PUT'])
def update_user_house(user_id, house_id):
    data = request.get_json()

    # 1. Find the User and the specific House
    user = User.query.get(user_id)
    house = House.query.filter_by(id=house_id, user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not house:
        return jsonify({"error": "House not found or does not belong to this user"}), 404

    # 2. Update User fields (if provided in JSON)
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']

    # 3. Update House fields (if provided in JSON)
    if 'house_number' in data:
        house.house_number = data['house_number']
    if 'house_address' in data:
        house.house_address = data['house_address']

    # 4. Commit changes
    try:
        db.session.commit()
        return jsonify({
            "message": "User and House updated successfully!",
            "updated_user": user.name,
            "updated_house": house.house_number
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/delete_user_house/<int:user_id>/<int:house_id>', methods=['DELETE'])
def delete_house(user_id, house_id):
    # 1. Find the user using 'id' (the correct column name)
    user = User.query.get(user_id)
    
    # 2. Find the specific house belonging to that user
    house = House.query.filter_by(id=house_id, user_id=user_id).first()

    # 3. Validations
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not house:
        return jsonify({"error": "House not found for this user"}), 404

    try:
        # 4. Delete the house first, then the user
        db.session.delete(house)
        db.session.delete(user)
        
        # 5. Commit the transaction
        db.session.commit()
        
        return jsonify({
            "message": f"User {user_id} and House {house_id} deleted successfully!"
        }), 200
        
    except Exception as e:
        # Exception → base class of all errors
        # as e → store the error message in variable e
        db.session.rollback()
        # Without rollback ❌:Session becomes broken,Next request fails,Database stays in half-state
        # With rollback ✅:Everything is cancelled,Database is safe,Session is clean
        return jsonify({"error": str(e)}), 500
        # str(e):Converts error object to readable text
if __name__ == '__main__':
    app.run(debug=True)