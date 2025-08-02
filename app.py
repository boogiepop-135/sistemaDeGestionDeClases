from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crm_educativo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'

# Configuración de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')

# Importar modelos primero
from models import db

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
CORS(app)

# Configurar manejo de errores JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token expirado',
        'message': 'El token ha expirado. Por favor, inicia sesión nuevamente.'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'Token inválido',
        'message': 'El token proporcionado es inválido.'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'Token requerido',
        'message': 'Se requiere un token de autenticación.'
    }), 401

# Importar rutas después de inicializar db
from routes import *

# Crear tablas
with app.app_context():
    db.create_all()
    
    # Crear usuario superadmin por defecto si no existe
    superadmin_user = User.query.filter_by(email='levi@crm.edu').first()
    if not superadmin_user:
        hashed_password = bcrypt.generate_password_hash('Leaguejinx1310-').decode('utf-8')
        superadmin_user = User(
            email='levi@crm.edu',
            password_hash=hashed_password,
            name='Levi Villarreal',
            role='superadmin'
        )
        db.session.add(superadmin_user)
        db.session.commit()
    
    # Crear usuario admin por defecto si no existe
    admin_user = User.query.filter_by(email='admin@crm.edu').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(
            email='admin@crm.edu',
            password_hash=hashed_password,
            name='Administrador',
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/estudiantes')
def estudiantes():
    return render_template('estudiantes.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/finanzas')
def finanzas():
    return render_template('finanzas.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/configuracion')
def configuracion():
    return render_template('configuracion.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 