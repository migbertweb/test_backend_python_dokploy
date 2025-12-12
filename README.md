# 📝 FastAPI Task Manager

Un backend moderno y robusto para la gestión de tareas, construido con FastAPI, Python 3.11+, SQLAlchemy y PostgreSQL.

**Autor:** Migbert Yanez  
**GitHub:** [https://github.com/migbertweb](https://github.com/migbertweb)  
**Licencia:** GPL-3.0

---

## 🚀 Características

- **Gestión de Tareas (CRUD)**: Crear, leer, actualizar y eliminar tareas.
- **Autenticación Segura (JWT)**: Login de usuarios y protección de rutas.
- **Rate Limiting**: Protección contra abuso de API (usando `slowapi`).
- **Logging**: Registro detallado de peticiones.
- **Base de Datos Asíncrona**: SQLAlchemy + AsyncPG para alto rendimiento.
- **Dockerizado**: Incluye `Dockerfile` multistage optimizado.
- **Validación de Datos**: Schemas fuertes con Pydantic.

## 🛠️ Tecnologías

- Python 3.11
- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy (Async)
- Pydantic
- JWT (JSON Web Tokens)
- Bases de datos soportadas (Driver requerido):
  - PostgreSQL (asyncpg - Default)
  - SQLite (aiosqlite)
  - MariaDB/MySQL (aiomysql)

---

## 🔄 Cambiar Base de Datos

El proyecto está configurado por defecto para usar **PostgreSQL**. Si deseas cambiar a **SQLite** o **MariaDB**, sigue estos pasos:

### Para usar SQLite

1. Agrega el driver en `requirements.txt`:
   ```text
   aiosqlite
   ```
2. Modifica la variable `DATABASE_URL` en tu archivo `.env` o en `app/database.py`:
   ```python
   DATABASE_URL="sqlite+aiosqlite:///./sql_app.db"
   ```
   _Nota: Para SQLite el archivo de base de datos se creará en el directorio local._

### Para usar MariaDB / MySQL

1. Agrega el driver en `requirements.txt`:
   ```text
   aiomysql
   ```
2. Modifica la variable `DATABASE_URL` en tu archivo `.env` o en `app/database.py`:
   ```python
   DATABASE_URL="mysql+aiomysql://usuario:password@localhost/nombre_db"
   ```

---

## 📦 Instalación y Ejecución

### Opción 1: Usando Docker (Recomendado)

1. **Construir la imagen:**

   ```bash
   docker build -t fastapi-tasks .
   ```

2. **Ejecutar el contenedor:**
   ```bash
   docker run -d -p 8000:8000 --env-file .env fastapi-tasks
   ```

### Opción 2: Ejecución Local

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/migbertweb/fastapi-tasks.git
   cd fastapi-tasks
   ```

2. **Crear entorno virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno:**
   Crea un archivo `.env` en la raíz (para local) o configúralas en tu plataforma de despliegue (Dokploy/Railway).

   | Variable                      | Descripción                     | Valor por defecto / Ejemplo              | Requerido |
   | :---------------------------- | :------------------------------ | :--------------------------------------- | :-------- |
   | `DATABASE_URL`                | String de conexión a PostgreSQL | `postgresql+asyncpg://user:pass@host/db` | ✅ Sí     |
   | `SECRET_KEY`                  | Llave para firmar tokens JWT    | `generar_con_openssl_rand_hex_32`        | ✅ Sí     |
   | `ALGORITHM`                   | Algoritmo de encriptación JWT   | `HS256`                                  | ❌ No     |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos   | `30`                                     | ❌ No     |

5. **Iniciar el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Opción 3: Despliegue en Dokploy

1. **Crear Proyecto**: En tu panel de Dokploy, crea un nuevo proyecto.
2. **Crear Servicio**: Selecciona "Application" y elige GitHub como fuente.
3. **Seleccionar Repositorio**: Elige el repositorio `fastapi-tasks`.
4. **Configuración de Build**:
   - **Build Type**: Dockerfile (Dokploy detectará automáticamente el `Dockerfile`) o Nixpacks (gracias al `railpack.json`).
   - Se recomienda usar **Dockerfile** para este proyecto ya que está optimizado multi-etapa.
5. **Variables de Entorno**:
   - En la pestaña "Environment", añade `DATABASE_URL` y cualquier otra variable necesaria (ej. `SECRET_KEY`).
6. **Desplegar**: Haz clic en "Deploy". Dokploy construirá la imagen y lanzará el contenedor.

---

## 🔑 Uso de la API

La documentación interactiva está disponible en: `http://localhost:8000/docs`

### Flujo de Autenticación

1. **Registro:** `POST /users/`
   - Crea un nuevo usuario.
2. **Login:** `POST /token`
   - Envía `username` (email) y `password`.
   - Recibe un `access_token`.
3. **Usar Token:**
   - Envía el token en el header `Authorization: Bearer <tu_token>` para acceder a las rutas de tareas `/tasks/`.

---

## 📄 Estructura del Proyecto

```
.
├── app
│   ├── main.py      # Punto de entrada y rutas
│   ├── models.py    # Modelos de base de datos
│   ├── schemas.py   # Schemas Pydantic
│   ├── crud.py      # Operaciones de base de datos
│   ├── auth.py      # Lógica de autenticación
│   ├── deps.py      # Dependencias (Current User)
│   └── database.py  # Conexión a DB
├── Dockerfile       # Configuración Docker
├── railpack.json    # Configuración Railpack
└── requirements.txt # Dependencias
```

---

## 📜 Licencia

Este proyecto está bajo la Licencia **GPL-3.0**. Consulta el archivo `LICENSE` para más detalles.
