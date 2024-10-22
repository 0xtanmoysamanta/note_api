from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a more secure key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])  # Hash the password in a real app
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:  # Validate hashed password in a real app
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/notes', methods=['GET', 'POST'])
@jwt_required()
def manage_notes():
    current_user_id = get_jwt_identity()
    if request.method == 'POST':
        data = request.json
        new_note = Note(title=data['title'], content=data['content'], user_id=current_user_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"msg": "Note created"}), 201
    else:
        notes = Note.query.filter_by(user_id=current_user_id).all()
        return jsonify([{"id": note.id, "title": note.title, "content": note.content} for note in notes])

@app.route('/notes/<int:note_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_note(note_id):
    current_user_id = get_jwt_identity()
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user_id:
        return jsonify({"msg": "Not authorized"}), 403

    if request.method == 'PUT':
        data = request.json
        note.title = data['title']
        note.content = data['content']
        db.session.commit()
        return jsonify({"msg": "Note updated"})

    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({"msg": "Note deleted"})

if __name__ == '__main__':
    app.run(debug=True)
