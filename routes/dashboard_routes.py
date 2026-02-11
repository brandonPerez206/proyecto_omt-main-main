from flask import Blueprint, render_template, redirect, url_for, session
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    from database import get_connection
    conn = get_connection()

    c = conn.cursor()
    c.execute("SELECT id, fecha, hora, usuario, tipo, subcategoria, descripcion FROM registros ORDER BY id DESC LIMIT 10")
    ultimos = c.fetchall()
    conn.close()

    return render_template('dashboard.html', ultimos=ultimos, usuario=session['usuario'], rol=session['rol'])
