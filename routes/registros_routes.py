from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime


registros_bp = Blueprint('registros', __name__, url_prefix='/registros')

@registros_bp.route('/', methods=['GET', 'POST'])
def registros():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    tipo = None
    descripcion = None
    subcategorias = ""

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')

        subcategorias_lista = [
            request.form.get('subcategoria'),
            request.form.get('subcategoria1'),
            request.form.get('subcategoria2'),
            request.form.get('subcategoria3'),
            request.form.get('subcategoria4')
        ]

        subcategorias_lista = [s for s in subcategorias_lista if s]
        subcategorias = ", ".join(subcategorias_lista)

        if not tipo or not descripcion:
            flash("Debes completar todos los campos obligatorios", "warning")
            conn.close()
            return redirect(url_for('registros.registros'))

        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        c.execute("""
            INSERT INTO registros (usuario, tipo, subcategoria, descripcion, fecha, hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session['usuario'], tipo, subcategorias, descripcion, fecha, hora))

        conn.commit()

    c.execute("SELECT fecha, hora, usuario, tipo, subcategoria, descripcion FROM registros ORDER BY id DESC")
    registros = c.fetchall()
    conn.close()

    return render_template(
        'registros.html',
        registros=registros,
        usuario=session['usuario'],
        rol=session['rol']
    )

@registros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(id):
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    if session.get('rol') != 'Administrador':
        flash('No tienes permisos para eliminar registros.', 'danger')
        return redirect(url_for('historial.historial'))

    from database import get_connection
    conn = get_connection()

    c = conn.cursor()
    c.execute("DELETE FROM registros WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Registro eliminado correctamente.', 'success')
    return redirect(url_for('historial.historial'))
