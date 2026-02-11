from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from flask_mail import Message
import sqlite3

auth_bp = Blueprint('auth', __name__)

def init_db():
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL,
            rol TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        from database import get_connection
        conn = get_connection()

        c = conn.cursor()
        c.execute("SELECT id, usuario, password, rol FROM usuarios WHERE usuario = ?", (usuario,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['usuario'] = user[1]
            session['rol'] = user[3]
            flash(f" Bienvenido {user[1]}", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(" Usuario o contraseña incorrectos.", "danger")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()    
    return redirect(url_for('auth.login'))


@auth_bp.route('/solicitud_recuperacion', methods=['GET', 'POST'])
def solicitud_recuperacion():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        motivo = request.form.get('motivo')
        destino = "brandonperez1209@gmail.com"

        msg = Message(
            subject=" Solicitud de Restablecimiento de Contraseña",
            sender='brandonperez1209@gmail.com',
            recipients=[destino]
        )
        msg.body = f"""
        Se ha recibido una solicitud de restablecimiento de contraseña.

        👤 Nombre del trabajador: {nombre}
        📝 Motivo: {motivo}
        
        Ingresar a la pagina el usuario administrador:
        usuario: admin
        contraseña: admin123
        """
        current_app.extensions['mail'].send(msg)
        flash('Tu solicitud fue enviada correctamente', 'success')
        return redirect(url_for('auth.login'))

        
    return render_template('solicitud_recuperacion.html')

