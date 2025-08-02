from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='profesor')  # admin, profesor, asistente
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    courses = db.relationship('Course', backref='teacher', lazy=True)
    classes = db.relationship('Class', backref='teacher', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    parent_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='activo')  # activo, inactivo, graduado
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relaciones
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    payments = db.relationship('Payment', backref='student', lazy=True)
    attendance = db.relationship('Attendance', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(50))  # ej: "3 meses", "6 meses"
    price = db.Column(db.Float, nullable=False)
    max_students = db.Column(db.Integer, default=20)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='activo')  # activo, inactivo, completado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    classes = db.relationship('Class', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    schedule = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=60)  # duración en minutos
    room = db.Column(db.String(50))
    status = db.Column(db.String(20), default='programada')  # programada, en_curso, completada, cancelada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    attendance = db.relationship('Attendance', backref='class_session', lazy=True)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='activo')  # activo, completado, cancelado
    final_grade = db.Column(db.Float)
    notes = db.Column(db.Text)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # matricula, mensualidad, material, otro
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pendiente')  # pendiente, pagado, cancelado
    payment_method = db.Column(db.String(50))  # efectivo, tarjeta, transferencia
    reference = db.Column(db.String(100))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='presente')  # presente, ausente, justificado, tardanza
    notes = db.Column(db.Text)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), default='evaluacion')  # evaluacion, tarea, proyecto, final
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float, default=1.0)  # peso de la calificación

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, warning, success, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    user = db.relationship('User', backref='notifications') 