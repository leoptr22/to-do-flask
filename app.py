from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla "Tarea"
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200))
    completada = db.Column(db.Boolean, default=False)

# Crear la base de datos (ejecutar solo una vez)
with app.app_context():
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def index():
    tareas = Tarea.query.all()  # Obtener todas las tareas
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nueva_tarea = Tarea(contenido=request.form['contenido'], completada=False)
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/completar/<int:id>')
def completar(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.completada = not tarea.completada  # Alternar estado
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)