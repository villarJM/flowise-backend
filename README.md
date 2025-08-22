# Flowise Backend

## Descripción General

Flowise Backend es una aplicación Flask diseñada para la gestión de proyectos y seguimiento de tiempo. El sistema permite a los usuarios registrar tiempo trabajado en diferentes proyectos, generar reportes diarios y semanales, y gestionar horarios de trabajo.

## 🚀 Inicio Rápido

### Desarrollo
```bash
# Clonar el repositorio
git clone <repository-url>
cd flowise-backend

# Ejecutar con Docker
docker-compose -f docker-compose.dev.yml up --build

# La aplicación estará disponible en http://localhost:8000
```

### Producción
```bash
# Ejecutar en modo producción
docker-compose up --build
```

## 📋 Comandos de Configuración Utilizados

### Configuración Inicial de Docker
```bash
# Construir y levantar contenedores en modo desarrollo
docker-compose -f docker-compose.dev.yml up --build -d

# Verificar estado de contenedores
docker ps

# Detener contenedores
docker-compose -f docker-compose.dev.yml down

# Reiniciar contenedor específico
docker restart flowise_server_dev
```

### Configuración de Base de Datos
```bash
# Conectar a PostgreSQL desde el contenedor
docker exec -it flowise_db_dev psql -U postgres -d flowise_dev

# Crear usuario con privilegios
docker exec -it flowise_db_dev psql -U postgres -d flowise_dev -c "CREATE USER flowise_user WITH PASSWORD 'flowise1124'; GRANT ALL PRIVILEGES ON DATABASE flowise_dev TO flowise_user; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flowise_user; GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flowise_user;"

# Listar tablas en PostgreSQL
docker exec -it flowise_db_dev psql -U postgres -d flowise_dev -c "\dt"

# Conectar con el usuario creado
docker exec -it flowise_db_dev psql -U flowise_user -d flowise_dev

# Verificar variables de entorno en el contenedor
docker exec -it flowise_server_dev env | grep -E '(DATABASE_URL|POSTGRES_)'
```

### Migraciones de Base de Datos
```bash
# Ejecutar migraciones (crear tablas)
docker exec -it flowise_server_dev flask db upgrade

# Generar nueva migración
docker exec -it flowise_server_dev flask db migrate -m "Initial migration with all models"

# Inicializar repositorio de migraciones (solo primera vez)
docker exec -it flowise_server_dev flask db init
```

### Ejecución del Servidor
```bash
# Ejecutar servidor Flask manualmente
docker exec -it flowise_server_dev python run.py

# Verificar salud del servidor
curl http://localhost:8000/health
```

### Comandos de Depuración
```bash
# Ver logs de contenedor específico
docker logs flowise_server_dev
docker logs flowise_db_dev

# Acceder al shell del contenedor
docker exec -it flowise_server_dev /bin/bash
docker exec -it flowise_db_dev /bin/bash

# Verificar procesos en puerto específico
lsof -i :8000
```

## 🛠️ Tecnologías

- **Framework**: Flask 3.1.1
- **Base de Datos**: PostgreSQL 17
- **ORM**: SQLAlchemy con Flask-SQLAlchemy 3.1.1
- **Migraciones**: Flask-Migrate 4.1.0
- **Contenedores**: Docker y Docker Compose
- **Variables de Entorno**: python-dotenv 1.1.1
- **Driver de BD**: psycopg2-binary 2.9.10

## 📁 Estructura del Proyecto

```
flowise-backend/
├── app/
│   ├── __init__.py          # Factory de aplicación Flask
│   ├── config.py            # Configuraciones por ambiente
│   ├── models/              # Modelos de datos SQLAlchemy
│   ├── routes/              # Rutas y endpoints API
│   ├── services/            # Lógica de negocio
│   ├── repositories/        # Capa de acceso a datos
│   ├── schemas/             # Esquemas de validación
│   └── utils/               # Utilidades generales
├── migrations/              # Migraciones de base de datos
├── docker-compose.yml       # Configuración Docker producción
├── docker-compose.dev.yml   # Configuración Docker desarrollo
├── Dockerfile               # Imagen Docker de la aplicación
├── requirements.txt         # Dependencias Python
└── run.py                   # Punto de entrada de la aplicación
```

## 🗄️ Modelos de Datos

El sistema incluye los siguientes modelos principales:

- **UserModel**: Gestión de usuarios y autenticación
- **ProjectModel**: Información de proyectos
- **TimeEntryModel**: Registro de tiempo trabajado
- **WorkScheduleModel**: Horarios de trabajo programados
- **DailyReportModel**: Reportes diarios de tiempo
- **WeeklyReport**: Reportes semanales consolidados
- **ProjectCommentModel**: Comentarios en proyectos
- **AuthProviderModel**: Proveedores de autenticación externos
- **UserProjectModel**: Relación usuarios-proyectos

## ⚙️ Configuración

### Variables de Entorno

El proyecto utiliza archivos `.env` para diferentes ambientes y carga automáticamente el archivo correcto según la variable `FLASK_ENV`:

- `.env.dev` - Configuración de desarrollo (por defecto)
- `.env.prod` - Configuración de producción
- `.env.test` - Configuración de testing

#### Selección Automática de Ambiente

El sistema determina qué archivo `.env` cargar basándose en la variable de entorno `FLASK_ENV`:

```bash
# Desarrollo (por defecto)
export FLASK_ENV=development  # Carga .env.dev

# Producción
export FLASK_ENV=production   # Carga .env.prod

# Testing
export FLASK_ENV=testing      # Carga .env.test
```

#### Configuración Dinámica

Además del archivo `.env`, puedes configurar:

- `PORT`: Puerto del servidor (por defecto: 8000)
- `HOST`: Host del servidor (por defecto: 0.0.0.0)

**Ejemplo de configuración (.env.dev):**
```env
FLASK_ENV=development
PORT=8000
HOST=0.0.0.0
POSTGRES_USER=flowise_user
POSTGRES_PASSWORD=flowise_password
POSTGRES_DB=flowise_dev
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=dev_secret_key
JWT_SECRET_KEY=dev_jwt_secret_key
```

### Ambientes Soportados

1. **Development**: Base de datos SQLite por defecto, debug habilitado
2. **Production**: PostgreSQL, debug deshabilitado
3. **Testing**: Base de datos en memoria

## 🐳 Docker

### Características Docker

- **Imagen base**: Python 3.13.2-slim
- **Usuario no privilegiado**: appuser (UID: 10001)
- **Puerto expuesto**: 8000
- **Volúmenes persistentes**: Datos de PostgreSQL
- **Redes aisladas**: Separación entre desarrollo y producción
- **Health checks**: Verificación de estado de PostgreSQL

### Comandos Docker

```bash
# Desarrollo (con hot reload)
docker-compose -f docker-compose.dev.yml up --build

# Producción
docker-compose up --build

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f

# Acceder al contenedor
docker-compose exec server bash
```

## 🔄 Migraciones

El proyecto utiliza Flask-Migrate (Alembic) para gestionar cambios en la base de datos:

```bash
# Generar nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir migración
flask db downgrade
```

## 🔐 Módulo de Autenticación

### Arquitectura del Módulo Auth

El sistema de autenticación sigue una arquitectura en capas:

```
auth_routes.py → auth_service.py → auth_repository.py → user_model.py
     ↓               ↓                    ↓               ↓
  Endpoints      Lógica de         Acceso a Datos    Modelo de BD
                 Negocio
```

### Componentes Principales

#### 1. **AuthRoutes** (`/app/routes/auth_routes.py`)
- **POST /auth/login** - Autenticación de usuarios
- **POST /auth/register** - Registro de nuevos usuarios
- Validación de Content-Type (application/json)
- Manejo de errores con códigos HTTP apropiados

#### 2. **AuthService** (`/app/services/auth_service.py`)
- `login_user()` - Validación de credenciales
- `register_user()` - Creación de usuarios con validaciones
- `hash_password()` - Encriptación con bcrypt
- `check_password()` - Verificación de contraseñas
- `is_password_strong()` - Validación de fortaleza de contraseña

#### 3. **AuthRepository** (`/app/repositories/auth_repository.py`)
- `create_user()` - Persistencia de usuarios en BD
- `get_user_by_email()` - Búsqueda por email

#### 4. **UserModel** (`/app/models/user_model.py`)
- Modelo SQLAlchemy para tabla `users`
- Campos: id, name, last_name, email, password, role, company
- Timestamps automáticos (created_at, updated_at)

#### 5. **UserRegisterSchema** (`/app/schemas/user_register_schema.py`)
- Validación con Marshmallow
- Email válido requerido
- Contraseña mínimo 8 caracteres

### Seguridad Implementada

#### Encriptación de Contraseñas
- **Algoritmo**: bcrypt con salt automático
- **Verificación**: Comparación segura con hash almacenado

#### Validación de Contraseñas Fuertes
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 número
- Al menos 1 carácter especial (!@#$%^&*()_+-=[]{}|;:,.<>?)

#### Validaciones de Negocio
- Email único en el sistema
- Formato de email válido
- Usuario existente para login
- Contraseña correcta para autenticación

### Manejo de Errores

#### Excepciones Personalizadas
- `ValidationError` (400) - Datos inválidos
- `NotFoundException` (404) - Usuario no encontrado
- `AuthenticationError` (401) - Credenciales incorrectas
- `AuthorizationError` (403) - Permisos insuficientes

#### Respuestas de Error
```json
{
  "message": "Descripción del error",
  "status": 400,
  "data": {
    "field": ["Error específico del campo"]
  }
}
```

### Endpoints de Autenticación

#### POST /auth/login
**Request:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "status": 200,
  "data": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "name": "Usuario",
    "role": "user"
  }
}
```

**Errores Comunes:**
- 400: Datos inválidos o cuerpo vacío
- 401: Contraseña incorrecta
- 404: Usuario no encontrado
- 415: Content-Type incorrecto

#### POST /auth/register
**Request:**
```json
{
  "email": "nuevo@ejemplo.com",
  "password": "MiContraseña123!"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "status": 201,
  "data": {
    "email": "nuevo@ejemplo.com"
  }
}
```

**Errores Comunes:**
- 400: Contraseña débil o datos inválidos
- 409: Email ya registrado
- 415: Content-Type incorrecto
- 422: Errores de validación de esquema

### Utilidades de Respuesta

#### ResponseUtils (`/app/core/utils/response_utils.py`)
- `create_response(message, status_code, data=None)`
- Formato estándar para todas las respuestas API
- Estructura consistente con message, status y data opcional

### Pendientes de Implementación

- [ ] **JWT Tokens** - Autenticación stateless
- [ ] **Refresh Tokens** - Renovación de sesiones
- [ ] **Rate Limiting** - Protección contra ataques de fuerza bruta
- [ ] **Email Verification** - Verificación de cuentas
- [ ] **Password Reset** - Recuperación de contraseñas
- [ ] **OAuth Integration** - Login con proveedores externos
- [ ] **Session Management** - Gestión de sesiones activas
- [ ] **Audit Logging** - Registro de eventos de autenticación

## 🌐 API Endpoints

Actualmente disponible:

- `GET /` - Health check que retorna el estado de la aplicación
- `POST /auth/login` - Autenticación de usuarios
- `POST /auth/register` - Registro de nuevos usuarios

**Respuesta del Health Check:**
```json
{
  "status": "ok",
  "message": "Flowise Backend is running",
  "environment": "development"
}
```

## 📊 Códigos de Estado HTTP

La API utiliza los siguientes códigos de estado HTTP estándar:

### Respuestas Exitosas (2xx)
- **200 OK** - Solicitud exitosa, datos retornados
- **201 Created** - Recurso creado exitosamente
- **204 No Content** - Operación exitosa sin contenido de respuesta

### Errores del Cliente (4xx)
- **400 Bad Request** - Datos de entrada inválidos o malformados
- **401 Unauthorized** - Autenticación requerida o token inválido
- **403 Forbidden** - Permisos insuficientes para acceder al recurso
- **404 Not Found** - Recurso no encontrado
- **409 Conflict** - Conflicto con el estado actual del recurso
- **422 Unprocessable Entity** - Errores de validación de datos
- **429 Too Many Requests** - Límite de velocidad excedido

### Errores del Servidor (5xx)
- **500 Internal Server Error** - Error interno del servidor
- **502 Bad Gateway** - Error de gateway o proxy
- **503 Service Unavailable** - Servicio temporalmente no disponible
- **504 Gateway Timeout** - Timeout del gateway o proxy

### Uso por Endpoint
- **GET /health** → 200 (servicio activo) | 503 (servicio no disponible)
- **POST /auth/login** → 200 (login exitoso) | 401 (credenciales inválidas)
- **GET /projects** → 200 (lista de proyectos) | 401 (no autenticado)
- **POST /projects** → 201 (proyecto creado) | 400 (datos inválidos) | 422 (validación fallida)
- **PUT /projects/{id}** → 200 (actualizado) | 404 (no encontrado) | 403 (sin permisos)
- **DELETE /projects/{id}** → 204 (eliminado) | 404 (no encontrado) | 409 (conflicto)

## 🏗️ Estado del Proyecto

### ✅ Implementado
- Modelos de datos completos
- Configuración multi-ambiente
- Dockerización completa
- Sistema de migraciones
- Health check básico

### 🔄 En Desarrollo
- Rutas y endpoints API
- Servicios de lógica de negocio
- Repositorios de acceso a datos
- Esquemas de validación
- Sistema de autenticación
- Middleware de autorización
- Documentación de API (Swagger/OpenAPI)
- Tests unitarios e integración
- Logging y monitoreo

## 🎯 Próximos Pasos

1. **Implementar autenticación JWT**
2. **Crear endpoints CRUD para cada modelo**
3. **Desarrollar lógica de negocio en servicios**
4. **Implementar validación de datos con esquemas**
5. **Agregar tests automatizados**
6. **Configurar logging y monitoreo**
7. **Documentar API con Swagger**
8. **Implementar middleware de seguridad**

## 📚 Documentación Adicional

- [Guía de Servicios AWS](./SERVICIOS.md)
- [Guía Docker](./README.Docker.md)

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

## 📞 Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.

---

**Nota**: Este proyecto está en desarrollo activo. Las funcionalidades pueden cambiar sin previo aviso.