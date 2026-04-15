from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Esto permite que tu JavaScript hable con Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
db = SQLAlchemy(app)

# Modelo de la base de datos
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default="pending")

with app.app_context():
    db.create_all()

@app.route('/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([{"id": h.id, "name": h.name, "status": h.status} for h in habits])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    
    
    
    @app.route('/')
def index():
    return render_template('index.html')

@app.route('/habits', methods=['POST'])
def add_habit():
    data = request.json
    new_habit = Habit(name=data['name'])
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({"message": "Habit created"}), 201