from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default="pending")

# Crear la base de datos
with app.app_context():
    db.create_all()

# --- RUTAS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([{"id": h.id, "name": h.name, "status": h.status} for h in habits])

@app.route('/habits', methods=['POST'])
def add_habit():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_habit = Habit(name=data['name'])
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({"id": new_habit.id, "name": new_habit.name, "status": new_habit.status}), 201



@app.route('/habits/<int:id>/complete', methods=['PUT'])
def complete_habit(id):
    habit = Habit.query.get_or_404(id)
    habit.status = "completed"
    db.session.commit()
    return jsonify({"message": "Habit updated successfully"})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)