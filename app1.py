import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_mail import Mail


from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.registros_routes import registros_bp
from routes.usuarios_routes import usuarios_bp
from routes.historial_routes import historial_bp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db') 

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Crea la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(registros_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(historial_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/health')
def health():
    return "OK"

@app.route('/test')
def test():
    return "HTTPS funciona"
