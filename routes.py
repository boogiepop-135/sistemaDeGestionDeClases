from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import app, bcrypt, mail
from models import db, User, Student, Course, Class, Enrollment, Payment, Attendance, Grade, Notification
from datetime import datetime, timedelta
import json

# ==================== AUTENTICACIÓN ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    # Crear nuevo usuario
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        name=data['name'],
        role=data.get('role', 'profesor')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Crear token de acceso
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'access_token': access_token,
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt for email: {data.get('email') if data else 'No data'}")
        
        # Validar campos requeridos
        if not data or 'email' not in data or 'password' not in data:
            print("Missing required fields")
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        print(f"User found: {user is not None}")
        
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            # Verificar que el usuario esté activo
            if hasattr(user, 'is_active') and not user.is_active:
                print("User is inactive")
                return jsonify({'error': 'Usuario inactivo'}), 401
                
            access_token = create_access_token(identity=user.id)
            print(f"Token created for user {user.id}: {access_token[:20]}...")
            
            response_data = {
                'message': 'Login exitoso',
                'token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role
                }
            }
            print(f"Login successful for user: {user.name}")
            print(f"Returning response with status 200")
            response = jsonify(response_data)
            response.headers.add('Access-Control-Allow-Origin', 'https://web-production-668e6.up.railway.app')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
        
        print("Invalid credentials")
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        print(f"Profile request for user_id: {user_id}")
        
        user = User.query.get(user_id)
        print(f"User found: {user is not None}")
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        response_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }
        print(f"Profile returned for user: {user.name}")
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in get_profile: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """Endpoint de prueba para verificar que la API esté funcionando"""
    try:
        # Crear un token de prueba
        test_token = create_access_token(identity=1)
        print(f"Test token created: {test_token[:20]}...")
        
        response = jsonify({
            'message': 'API funcionando correctamente',
            'timestamp': datetime.now().isoformat(),
            'status': 'ok',
            'version': '1.0.0',
            'test_token_created': True,
            'jwt_secret_set': bool(app.config.get('JWT_SECRET_KEY')),
            'jwt_secret_length': len(app.config.get('JWT_SECRET_KEY', ''))
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    except Exception as e:
        print(f"Error in test_api: {e}")
        response = jsonify({
            'message': 'Error en API',
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor esté funcionando"""
    try:
        # Verificar que la base de datos esté accesible
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'message': 'Servidor funcionando correctamente',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'server': 'running'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Error en el servidor',
            'timestamp': datetime.now().isoformat(),
            'database': 'disconnected',
            'server': 'running',
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def server_status():
    """Endpoint simple para verificar que el servidor esté respondiendo"""
    response = jsonify({
        'status': 'online',
        'message': 'Servidor en línea',
        'timestamp': datetime.now().isoformat(),
        'jwt_secret_set': bool(app.config.get('JWT_SECRET_KEY')),
        'jwt_secret_length': len(app.config.get('JWT_SECRET_KEY', ''))
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verificar si el token es válido y obtener información del usuario"""
    try:
        print("Verifying token...")
        print(f"JWT Secret Key: {app.config.get('JWT_SECRET_KEY', 'NOT SET')[:10]}...")
        user_id = get_jwt_identity()
        print(f"User ID from token: {user_id}")
        user = User.query.get(user_id)
        print(f"User found: {user is not None}")
        
        if not user:
            print("User not found in database")
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        print(f"Token verification successful for user: {user.name}")
        response = jsonify({
            'valid': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role
            }
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    except Exception as e:
        print(f"Error in token verification: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        response = jsonify({'error': 'Token inválido'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 401

# ==================== USUARIOS ====================

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        current_user = User.query.get(get_jwt_identity())
        
        if not current_user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Solo superadmin y admin pueden ver usuarios
        if current_user.role not in ['superadmin', 'admin']:
            return jsonify({'error': 'No tienes permisos para ver usuarios'}), 403
        
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'email': u.email,
            'name': u.name,
            'role': u.role,
            'is_active': u.is_active if hasattr(u, 'is_active') else True,
            'created_at': u.created_at.isoformat()
        } for u in users])
    except Exception as e:
        print(f"Error en get_users: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = User.query.get(get_jwt_identity())
    
    # Solo superadmin puede crear usuarios
    if current_user.role != 'superadmin':
        return jsonify({'error': 'Solo el superadmin puede crear usuarios'}), 403
    
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    # Crear nuevo usuario
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        email=data['email'],
        password_hash=hashed_password,
        name=data['name'],
        role=data['role']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuario creado exitosamente',
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role
        }
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    
    # Solo superadmin puede actualizar usuarios
    if current_user.role != 'superadmin':
        return jsonify({'error': 'Solo el superadmin puede actualizar usuarios'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.is_active = data.get('is_active', user.is_active)
    
    if data.get('password'):
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    db.session.commit()
    
    return jsonify({'message': 'Usuario actualizado exitosamente'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    
    # Solo superadmin puede eliminar usuarios
    if current_user.role != 'superadmin':
        return jsonify({'error': 'Solo el superadmin puede eliminar usuarios'}), 403
    
    # No permitir eliminar el propio usuario
    if current_user.id == user_id:
        return jsonify({'error': 'No puedes eliminar tu propia cuenta'}), 400
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario eliminado exitosamente'})

# ==================== ESTUDIANTES ====================

@app.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'email': s.email,
        'phone': s.phone,
        'parent_phone': s.parent_phone,
        'status': s.status,
        'enrollment_date': s.enrollment_date.isoformat() if s.enrollment_date else None
    } for s in students])

@app.route('/api/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json()
    
    new_student = Student(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        parent_phone=data.get('parent_phone'),
        address=data.get('address'),
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data.get('birth_date') else None,
        status=data.get('status', 'activo'),
        notes=data.get('notes')
    )
    
    db.session.add(new_student)
    db.session.commit()
    
    return jsonify({
        'message': 'Estudiante creado exitosamente',
        'student': {
            'id': new_student.id,
            'name': new_student.name,
            'email': new_student.email
        }
    }), 201

@app.route('/api/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'phone': student.phone,
        'parent_phone': student.parent_phone,
        'address': student.address,
        'birth_date': student.birth_date.isoformat() if student.birth_date else None,
        'status': student.status,
        'enrollment_date': student.enrollment_date.isoformat(),
        'notes': student.notes
    })

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    
    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    student.phone = data.get('phone', student.phone)
    student.parent_phone = data.get('parent_phone', student.parent_phone)
    student.address = data.get('address', student.address)
    student.status = data.get('status', student.status)
    student.notes = data.get('notes', student.notes)
    
    if data.get('birth_date'):
        student.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({'message': 'Estudiante actualizado exitosamente'})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({'message': 'Estudiante eliminado exitosamente'})

# ==================== CURSOS ====================

@app.route('/api/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'duration': c.duration,
        'price': c.price,
        'max_students': c.max_students,
        'teacher_id': c.teacher_id,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in courses])

@app.route('/api/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    
    new_course = Course(
        name=data['name'],
        description=data.get('description'),
        duration=data.get('duration'),
        price=data['price'],
        max_students=data.get('max_students', 20),
        teacher_id=data['teacher_id'],
        status=data.get('status', 'activo')
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    return jsonify({
        'message': 'Curso creado exitosamente',
        'course': {
            'id': new_course.id,
            'name': new_course.name,
            'price': new_course.price
        }
    }), 201

@app.route('/api/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'duration': course.duration,
        'price': course.price,
        'max_students': course.max_students,
        'teacher_id': course.teacher_id,
        'status': course.status,
        'created_at': course.created_at.isoformat()
    })

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    course.duration = data.get('duration', course.duration)
    course.price = data.get('price', course.price)
    course.max_students = data.get('max_students', course.max_students)
    course.teacher_id = data.get('teacher_id', course.teacher_id)
    course.status = data.get('status', course.status)
    
    db.session.commit()
    
    return jsonify({'message': 'Curso actualizado exitosamente'})

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Curso eliminado exitosamente'})

# ==================== CLASES ====================

@app.route('/api/classes', methods=['GET'])
@jwt_required()
def get_classes():
    classes = Class.query.all()
    return jsonify([{
        'id': c.id,
        'course_id': c.course_id,
        'teacher_id': c.teacher_id,
        'title': c.title,
        'description': c.description,
        'schedule': c.schedule.isoformat(),
        'duration': c.duration,
        'room': c.room,
        'status': c.status
    } for c in classes])

@app.route('/api/classes', methods=['POST'])
@jwt_required()
def create_class():
    data = request.get_json()
    
    new_class = Class(
        course_id=data['course_id'],
        teacher_id=data['teacher_id'],
        title=data['title'],
        description=data.get('description'),
        schedule=datetime.fromisoformat(data['schedule']),
        duration=data.get('duration', 60),
        room=data.get('room'),
        status=data.get('status', 'programada')
    )
    
    db.session.add(new_class)
    db.session.commit()
    
    return jsonify({
        'message': 'Clase creada exitosamente',
        'class': {
            'id': new_class.id,
            'title': new_class.title,
            'schedule': new_class.schedule.isoformat()
        }
    }), 201

# ==================== MATRÍCULAS ====================

@app.route('/api/enrollments', methods=['GET'])
@jwt_required()
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([{
        'id': e.id,
        'student_id': e.student_id,
        'course_id': e.course_id,
        'enrollment_date': e.enrollment_date.isoformat(),
        'status': e.status,
        'final_grade': e.final_grade
    } for e in enrollments])

@app.route('/api/enrollments', methods=['POST'])
@jwt_required()
def create_enrollment():
    data = request.get_json()
    
    new_enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id'],
        status=data.get('status', 'activo')
    )
    
    db.session.add(new_enrollment)
    db.session.commit()
    
    return jsonify({
        'message': 'Matrícula creada exitosamente',
        'enrollment': {
            'id': new_enrollment.id,
            'student_id': new_enrollment.student_id,
            'course_id': new_enrollment.course_id
        }
    }), 201

# ==================== PAGOS ====================

@app.route('/api/payments', methods=['GET'])
@jwt_required()
def get_payments():
    payments = Payment.query.all()
    return jsonify([{
        'id': p.id,
        'student_id': p.student_id,
        'amount': p.amount,
        'type': p.type,
        'description': p.description,
        'date': p.date.isoformat(),
        'status': p.status,
        'payment_method': p.payment_method
    } for p in payments])

@app.route('/api/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    
    new_payment = Payment(
        student_id=data['student_id'],
        amount=data['amount'],
        type=data['type'],
        description=data.get('description'),
        status=data.get('status', 'pendiente'),
        payment_method=data.get('payment_method'),
        reference=data.get('reference')
    )
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({
        'message': 'Pago registrado exitosamente',
        'payment': {
            'id': new_payment.id,
            'amount': new_payment.amount,
            'type': new_payment.type
        }
    }), 201

# ==================== ASISTENCIA ====================

@app.route('/api/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    attendance = Attendance.query.all()
    return jsonify([{
        'id': a.id,
        'student_id': a.student_id,
        'class_id': a.class_id,
        'date': a.date.isoformat(),
        'status': a.status,
        'notes': a.notes
    } for a in attendance])

@app.route('/api/attendance', methods=['POST'])
@jwt_required()
def create_attendance():
    data = request.get_json()
    
    new_attendance = Attendance(
        student_id=data['student_id'],
        class_id=data['class_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        status=data.get('status', 'presente'),
        notes=data.get('notes')
    )
    
    db.session.add(new_attendance)
    db.session.commit()
    
    return jsonify({
        'message': 'Asistencia registrada exitosamente',
        'attendance': {
            'id': new_attendance.id,
            'student_id': new_attendance.student_id,
            'status': new_attendance.status
        }
    }), 201

# ==================== CALIFICACIONES ====================

@app.route('/api/grades', methods=['GET'])
@jwt_required()
def get_grades():
    grades = Grade.query.all()
    return jsonify([{
        'id': g.id,
        'student_id': g.student_id,
        'course_id': g.course_id,
        'grade': g.grade,
        'type': g.type,
        'description': g.description,
        'date': g.date.isoformat(),
        'weight': g.weight
    } for g in grades])

@app.route('/api/grades', methods=['POST'])
@jwt_required()
def create_grade():
    data = request.get_json()
    
    new_grade = Grade(
        student_id=data['student_id'],
        course_id=data['course_id'],
        grade=data['grade'],
        type=data.get('type', 'evaluacion'),
        description=data.get('description'),
        weight=data.get('weight', 1.0)
    )
    
    db.session.add(new_grade)
    db.session.commit()
    
    return jsonify({
        'message': 'Calificación registrada exitosamente',
        'grade': {
            'id': new_grade.id,
            'student_id': new_grade.student_id,
            'grade': new_grade.grade
        }
    }), 201

# ==================== DASHBOARD ====================

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    # Estadísticas generales
    total_students = Student.query.filter_by(status='activo').count()
    total_courses = Course.query.filter_by(status='activo').count()
    total_classes = Class.query.filter_by(status='programada').count()
    
    # Ingresos del mes actual
    current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_payments = Payment.query.filter(
        Payment.date >= current_month,
        Payment.status == 'pagado'
    ).all()
    monthly_income = sum(p.amount for p in monthly_payments)
    
    # Asistencia promedio
    attendance_records = Attendance.query.all()
    if attendance_records:
        present_count = sum(1 for a in attendance_records if a.status == 'presente')
        attendance_rate = (present_count / len(attendance_records)) * 100
    else:
        attendance_rate = 0
    
    return jsonify({
        'total_students': total_students,
        'total_courses': total_courses,
        'total_classes': total_classes,
        'monthly_income': monthly_income,
        'attendance_rate': round(attendance_rate, 2)
    })

@app.route('/api/dashboard/recent-activities', methods=['GET'])
@jwt_required()
def get_recent_activities():
    # Actividades recientes
    recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.date.desc()).limit(5).all()
    
    activities = []
    
    for enrollment in recent_enrollments:
        student = Student.query.get(enrollment.student_id)
        course = Course.query.get(enrollment.course_id)
        activities.append({
            'type': 'enrollment',
            'message': f'{student.name} se matriculó en {course.name}',
            'date': enrollment.enrollment_date.isoformat()
        })
    
    for payment in recent_payments:
        student = Student.query.get(payment.student_id)
        activities.append({
            'type': 'payment',
            'message': f'{student.name} realizó un pago de ${payment.amount}',
            'date': payment.date.isoformat()
        })
    
    # Ordenar por fecha
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    return jsonify(activities[:10])

# ==================== REPORTES ====================

@app.route('/api/reports/student-performance', methods=['GET'])
@jwt_required()
def get_student_performance():
    students = Student.query.all()
    performance_data = []
    
    for student in students:
        grades = Grade.query.filter_by(student_id=student.id).all()
        if grades:
            avg_grade = sum(g.grade for g in grades) / len(grades)
        else:
            avg_grade = 0
        
        attendance_records = Attendance.query.filter_by(student_id=student.id).all()
        if attendance_records:
            present_count = sum(1 for a in attendance_records if a.status == 'presente')
            attendance_rate = (present_count / len(attendance_records)) * 100
        else:
            attendance_rate = 0
        
        performance_data.append({
            'student_id': student.id,
            'student_name': student.name,
            'average_grade': round(avg_grade, 2),
            'attendance_rate': round(attendance_rate, 2)
        })
    
    return jsonify(performance_data)

@app.route('/api/reports/financial', methods=['GET'])
@jwt_required()
def get_financial_report():
    # Reporte financiero
    payments = Payment.query.filter_by(status='pagado').all()
    
    total_income = sum(p.amount for p in payments)
    
    # Ingresos por tipo
    income_by_type = {}
    for payment in payments:
        if payment.type not in income_by_type:
            income_by_type[payment.type] = 0
        income_by_type[payment.type] += payment.amount
    
    # Ingresos por mes (últimos 6 meses)
    monthly_income = {}
    for i in range(6):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_payments = [p for p in payments if month_start <= p.date <= month_end]
        monthly_income[month_start.strftime('%Y-%m')] = sum(p.amount for p in month_payments)
    
    return jsonify({
        'total_income': total_income,
        'income_by_type': income_by_type,
        'monthly_income': monthly_income
    }) 