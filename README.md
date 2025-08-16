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

## 🌐 API Endpoints

Actualmente disponible:

- `GET /` - Health check que retorna el estado de la aplicación

**Respuesta del Health Check:**
```json
{
  "status": "ok",
  "message": "Flowise Backend is running",
  "environment": "development"
}
```

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