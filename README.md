# 🎓 CRM Educativo - Sistema de Gestión de Clases y Cursos

Un sistema completo de Customer Relationship Management (CRM) diseñado específicamente para instituciones educativas, con gestión de estudiantes, cursos, pagos, asistencia y reportes.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- Registro e inicio de sesión de usuarios
- Diferentes roles: Admin, Profesor, Asistente
- Autenticación JWT segura
- Recuperación de contraseña

### 👥 Gestión de Estudiantes
- Registro completo de estudiantes
- Historial académico
- Estado de pagos
- Asistencia y calificaciones
- Comunicación con padres/tutores

### 📚 Gestión de Cursos
- Crear y editar cursos
- Programar clases
- Asignar profesores
- Gestionar horarios
- Control de capacidad

### 💰 Sistema de Pagos
- Registro de matrículas
- Mensualidades
- Descuentos y becas
- Estados de cuenta
- Recordatorios automáticos

### 📊 Reportes y Analytics
- Dashboard interactivo
- Gráficos de ingresos
- Estadísticas de asistencia
- Reportes de rendimiento
- Exportación de datos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Autenticación**: JWT
- **UI Framework**: Bootstrap 5
- **Gráficos**: Chart.js
- **Iconos**: Font Awesome
- **Containerización**: Docker

## 🚀 Instalación y Configuración

### Opción 1: Usando Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd crm-educativo
```

2. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up --build
```

3. **Acceder a la aplicación**
- URL: http://localhost:5000
- Credenciales por defecto:
  - Email: `admin@crm.edu`
  - Contraseña: `admin123`

### Opción 2: Instalación Local

1. **Requisitos previos**
- Python 3.11+
- pip

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-clave-jwt-aqui
DATABASE_URL=sqlite:///crm_educativo.db
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

## 📁 Estructura del Proyecto

```
crm-educativo/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de base de datos
├── routes.py              # Rutas de la API
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Configuración de Docker Compose
├── Procfile              # Configuración para Railway
├── runtime.txt           # Versión de Python
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard principal
│   └── estudiantes.html  # Gestión de estudiantes
├── static/               # Archivos estáticos
│   ├── css/             # Estilos CSS
│   └── js/              # JavaScript
└── README.md            # Este archivo
```

## 🎨 Diseño y UI/UX

### Tema Educativo
- **Colores principales**: Azul (#1e3a8a), Verde (#059669), Amarillo (#eab308)
- **Diseño responsivo**: Mobile-first approach
- **Iconografía**: Font Awesome con emojis educativos
- **Animaciones**: Transiciones suaves y efectos hover

### Secciones del Sistema
1. **🏠 Dashboard** - Resumen general y estadísticas
2. **👥 Estudiantes** - Gestión completa de estudiantes
3. **📚 Cursos** - Administración de cursos y clases
4. **💰 Finanzas** - Control de pagos y cobros
5. **📊 Reportes** - Analytics y estadísticas
6. **⚙️ Configuración** - Ajustes del sistema

## 🔧 Configuración para Producción

### Variables de Entorno
```bash
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/db

# Seguridad
SECRET_KEY=clave-secreta-muy-segura
JWT_SECRET_KEY=clave-jwt-muy-segura

# Email (opcional)
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-app

# Entorno
FLASK_ENV=production
```

### Despliegue en Railway

1. **Conectar repositorio a Railway**
2. **Configurar variables de entorno**
3. **Deploy automático**

### Despliegue en Heroku

1. **Instalar Heroku CLI**
2. **Crear aplicación**
```bash
heroku create tu-app-name
```

3. **Configurar variables**
```bash
heroku config:set SECRET_KEY=tu-clave
heroku config:set DATABASE_URL=postgresql://...
```

4. **Deploy**
```bash
git push heroku main
```

## 📊 Base de Datos

### Tablas Principales

- **users**: Usuarios del sistema (admin, profesores, asistentes)
- **students**: Información de estudiantes
- **courses**: Cursos disponibles
- **classes**: Clases programadas
- **enrollments**: Matrículas de estudiantes
- **payments**: Registro de pagos
- **attendance**: Control de asistencia
- **grades**: Calificaciones
- **notifications**: Notificaciones del sistema

## 🔐 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Hashing de contraseñas**: bcrypt para encriptación
- **Validación de formularios**: Sanitización de datos
- **CORS configurado**: Control de acceso entre dominios
- **Rate limiting**: Protección contra ataques

## 📱 Responsividad

- **Mobile-first**: Diseño optimizado para móviles
- **Menú hamburguesa**: Navegación adaptativa
- **Tablas responsivas**: Scroll horizontal en móviles
- **Formularios touch-friendly**: Optimizados para pantallas táctiles

## 🚀 Funcionalidades Avanzadas

### Dashboard Interactivo
- Estadísticas en tiempo real
- Gráficos dinámicos con Chart.js
- Actividades recientes
- Próximas clases

### Gestión de Estudiantes
- Búsqueda y filtros avanzados
- Exportación a CSV
- Historial completo
- Comunicación integrada

### Sistema de Pagos
- Múltiples métodos de pago
- Recordatorios automáticos
- Estados de cuenta
- Reportes financieros

### Reportes y Analytics
- Rendimiento por estudiante
- Estadísticas de asistencia
- Proyecciones financieras
- Exportación de datos

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

- **Email**: soporte@crm-educativo.com
- **Documentación**: [docs.crm-educativo.com](https://docs.crm-educativo.com)
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/crm-educativo/issues)

## 🎯 Roadmap

### Versión 2.0
- [ ] App móvil nativa
- [ ] Integración con WhatsApp
- [ ] Sistema de videoconferencias
- [ ] IA para recomendaciones

### Versión 2.1
- [ ] Múltiples idiomas
- [ ] Integración con LMS
- [ ] Sistema de certificados
- [ ] API pública

---

**¡Gracias por usar CRM Educativo! 🎓**

Desarrollado con ❤️ para la comunidad educativa. 