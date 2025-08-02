# 🚀 Guía de Postman para CRM de Gestión de Clases

## 📋 Configuración Inicial

### 1. **Configurar Variables de Entorno en Postman**

1. Abre Postman
2. Crea una nueva colección llamada "CRM Educativo"
3. Ve a la pestaña "Variables" de la colección
4. Agrega las siguientes variables:

| Variable | Valor Inicial | Valor Actual |
|----------|---------------|--------------|
| `base_url` | `http://localhost:5000` | `https://web-production-668e6.up.railway.app` |
| `token` | (vacío) | (se llenará automáticamente) |

### 2. **Configurar Headers Globales**

En la colección, ve a "Headers" y agrega:
- `Content-Type`: `application/json`

---

## 🔐 Autenticación

### **Login (Obtener Token)**

**POST** `{{base_url}}/api/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "admin@crm.edu",
    "password": "admin123"
}
```

**Respuesta esperada:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "admin@crm.edu",
        "name": "Administrador",
        "role": "admin"
    }
}
```

**Script para guardar token automáticamente:**
```javascript
// En la pestaña "Tests" de la request de login
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.collectionVariables.set("token", response.token);
}
```

### **Registro de Usuario**

**POST** `{{base_url}}/api/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "profesor@crm.edu",
    "password": "profesor123",
    "name": "Juan Pérez",
    "role": "profesor"
}
```

---

## 👥 Gestión de Usuarios

### **Obtener Todos los Usuarios**

**GET** `{{base_url}}/api/users`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Obtener Usuario por ID**

**GET** `{{base_url}}/api/users/1`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nuevo Usuario**

**POST** `{{base_url}}/api/users`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "asistente@crm.edu",
    "password": "asistente123",
    "name": "María García",
    "role": "asistente"
}
```

### **Actualizar Usuario**

**PUT** `{{base_url}}/api/users/1`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "name": "Administrador Actualizado",
    "role": "admin"
}
```

### **Eliminar Usuario**

**DELETE** `{{base_url}}/api/users/2`

**Headers:**
```
Authorization: Bearer {{token}}
```

---

## 👨‍🎓 Gestión de Estudiantes

### **Obtener Todos los Estudiantes**

**GET** `{{base_url}}/api/students`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nuevo Estudiante**

**POST** `{{base_url}}/api/students`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "name": "Ana López",
    "email": "ana.lopez@email.com",
    "phone": "555-0123",
    "parent_phone": "555-0124",
    "address": "Calle Principal 123",
    "birth_date": "2010-05-15",
    "status": "activo"
}
```

### **Actualizar Estudiante**

**PUT** `{{base_url}}/api/students/1`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "name": "Ana López Actualizada",
    "phone": "555-9999",
    "status": "activo"
}
```

---

## 📚 Gestión de Cursos

### **Obtener Todos los Cursos**

**GET** `{{base_url}}/api/courses`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nuevo Curso**

**POST** `{{base_url}}/api/courses`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "name": "Matemáticas Avanzadas",
    "description": "Curso de matemáticas para nivel avanzado",
    "duration": "6 meses",
    "price": 150.00,
    "max_students": 25,
    "teacher_id": 1
}
```

---

## 🏫 Gestión de Clases

### **Obtener Todas las Clases**

**GET** `{{base_url}}/api/classes`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nueva Clase**

**POST** `{{base_url}}/api/classes`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "course_id": 1,
    "teacher_id": 1,
    "schedule": "2024-01-15T10:00:00",
    "room": "Aula 101",
    "status": "programada"
}
```

---

## 💰 Gestión de Pagos

### **Obtener Todos los Pagos**

**GET** `{{base_url}}/api/payments`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nuevo Pago**

**POST** `{{base_url}}/api/payments`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "student_id": 1,
    "amount": 150.00,
    "type": "matricula",
    "date": "2024-01-15",
    "status": "pagado"
}
```

---

## 📊 Gestión de Asistencia

### **Obtener Todas las Asistencias**

**GET** `{{base_url}}/api/attendance`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nueva Asistencia**

**POST** `{{base_url}}/api/attendance`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "student_id": 1,
    "class_id": 1,
    "date": "2024-01-15",
    "status": "presente"
}
```

---

## 📈 Gestión de Calificaciones

### **Obtener Todas las Calificaciones**

**GET** `{{base_url}}/api/grades`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nueva Calificación**

**POST** `{{base_url}}/api/grades`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "student_id": 1,
    "course_id": 1,
    "grade": 85.5,
    "date": "2024-01-15"
}
```

---

## 🔄 Gestión de Matrículas

### **Obtener Todas las Matrículas**

**GET** `{{base_url}}/api/enrollments`

**Headers:**
```
Authorization: Bearer {{token}}
```

### **Crear Nueva Matrícula**

**POST** `{{base_url}}/api/enrollments`

**Headers:**
```
Authorization: Bearer {{token}}
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "student_id": 1,
    "course_id": 1,
    "enrollment_date": "2024-01-15",
    "status": "activo"
}
```

---

## 📝 Scripts Útiles para Postman

### **Script para verificar respuesta exitosa:**
```javascript
// En la pestaña "Tests"
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has data", function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property('data');
});
```

### **Script para mostrar datos en consola:**
```javascript
// En la pestaña "Tests"
console.log("Response:", pm.response.json());
```

---

## 🚀 Flujo de Trabajo Recomendado

1. **Configurar variables de entorno**
2. **Hacer login para obtener token**
3. **Crear usuarios (profesores, asistentes)**
4. **Crear cursos**
5. **Crear estudiantes**
6. **Crear clases**
7. **Registrar matrículas**
8. **Registrar pagos**
9. **Registrar asistencias**
10. **Registrar calificaciones**

---

## ⚠️ Notas Importantes

- **Token**: El token JWT expira en 24 horas
- **Roles**: Solo usuarios con rol 'admin' pueden crear/eliminar usuarios
- **IDs**: Los IDs se generan automáticamente, no los especifiques al crear
- **Fechas**: Usar formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- **Errores**: Revisar la consola de Postman para mensajes de error detallados

---

## 🔗 URLs de Producción

- **Base URL**: `https://web-production-668e6.up.railway.app`
- **Login**: `https://web-production-668e6.up.railway.app/api/auth/login`
- **Dashboard**: `https://web-production-668e6.up.railway.app/dashboard`

¡Con esta guía podrás probar todas las funcionalidades del CRM desde Postman! 🎉 