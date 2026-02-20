from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from collections import Counter
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_la_profe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emociones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(20)) 
    registros = db.relationship('Registro', backref='autor', lazy=True)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emocion = db.Column(db.String(20))
    fecha = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# --- RUTAS ---

@app.route('/')
@login_required
def index():
    if current_user.username == "Armando_Palacios":
        return redirect(url_for('stats'))
    return render_template('index.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('username').strip()
        pass_input = request.form.get('password').strip()

        # PUERTA SECRETA ARMANDO PALACIOS
        if user_input == "Armando_Palacios" and pass_input == "17102009":
            profe = User.query.filter_by(username="Armando_Palacios").first()
            if not profe:
                profe = User(username="Armando_Palacios", password="17102009", curso="ADMIN")
                db.session.add(profe)
                db.session.commit()
            login_user(profe)
            return redirect(url_for('stats'))

        # LOGIN NORMAL ALUMNOS
        user = User.query.filter_by(username=user_input, password=pass_input).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        
        flash("Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        curso = request.form.get('curso')

        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe")
            return redirect(url_for('signup'))

        nuevo = User(username=username, password=password, curso=curso)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/registrar', methods=['POST'])
@login_required
def registrar():
    emo = request.form.get('emocion')
    if emo:
        nuevo = Registro(emocion=emo, user_id=current_user.id)
        db.session.add(nuevo)
        db.session.commit()
    return redirect(url_for('stats'))

@app.route('/stats')
@login_required
def stats():
    if current_user.username == "Armando_Palacios":
        todos = Registro.query.order_by(Registro.fecha.desc()).all()
        total_alumnos = User.query.filter(User.username != "Armando_Palacios").count()
        return render_template('profe.html', registros=todos, total_alumnos=total_alumnos)
    
    mis_registros = Registro.query.filter_by(user_id=current_user.id).all()
    total = len(mis_registros)
    ultima = mis_registros[-1].emocion if total > 0 else "Sin registros"
    frecuente = Counter([r.emocion for r in mis_registros]).most_common(1)[0][0] if total > 0 else "N/A"

    return render_template('stats.html', total_registros=total, emocion_frecuente=frecuente, ultima_emocion=ultima)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)