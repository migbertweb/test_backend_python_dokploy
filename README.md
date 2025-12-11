# Backend de Tareas con FastAPI y Nixpacks 🚀

Esta es una aplicación backend simple para gestionar tareas, construida con FastAPI y configurada para ser desplegada fácilmente usando **Nixpacks** en plataformas como Dokploy.

## Características

- 🚀 **FastAPI**: Alto rendimiento y fácil de usar.
- 🗄️ **PostgreSQL**: Persistencia de datos robusta (vía SQLAlchemy Async).
- 📦 **Nixpacks**: Construcción automática y optimizada de contenedores.
- 🐳 **Docker**: Lista para despliegue en contenedores.

## Variables de Entorno

Para que la aplicación funcione correctamente, necesitas configurar la siguiente variable de entorno. En Dokploy, esto se hace en la sección de "Environment Variables" de tu aplicación.

| Variable       | Descripción                                   | Ejemplo                                                    |
| -------------- | --------------------------------------------- | ---------------------------------------------------------- |
| `DATABASE_URL` | URL de conexión a la base de datos PostgreSQL | `postgresql+asyncpg://usuario:password@host:5432/nombredb` |

> **Nota**: Asegúrate de usar el driver `asyncpg` en la URL de conexión (e.g., `postgresql+asyncpg://...`).

### Archivo .env

Para desarrollo local o para sobrescribir la configuración por defecto, crea un archivo `.env` en la raíz del proyecto. Hemos creado uno de ejemplo apuntando a tu servidor remoto:

```env
DATABASE_URL=postgresql+asyncpg://user:password@37.27.243.58/dbname
```

## Desarrollo Local

1. **Crear un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # .\venv\Scripts\activate  # En Windows
   ```

2. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```
   La API estará disponible en `http://localhost:8000`.
   Puedes ver la documentación interactiva en `http://localhost:8000/docs`.

## Despliegue en Dokploy (vía Nixpacks)

Esta configuración utiliza **Nixpacks** para construir la imagen Docker de manera eficiente y sin configuración compleja.

### Paso 1: Configuración en Dokploy

1.  Asegúrate de que tu proyecto en Dokploy esté configurado para usar **Nixpacks**.
2.  Nixpacks detectará automáticamente `requirements.txt` y `nixpacks.toml`.

### Paso 2: Despliegue

Simplemente haz push de tus cambios a tu repositorio. Dokploy (con Nixpacks habilitado) se encargará de:

1.  Detectar que es una aplicación Python.
2.  Instalar las dependencias de `requirements.txt`.
3.  Usar el comando de inicio definido en `nixpacks.toml`: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

No necesitas construir imágenes manualmente ni configurar Dockerfiles complejos.

## Endpoints (Probando con Postman)

- `POST /tasks/`: Crear tarea.
  ```json
  {
    "title": "Aprender Nix",
    "description": "Estudiar flakes y dockerTools"
  }
  ```
- `GET /tasks/`: Listar tareas.
- `GET /tasks/{id}`: Ver tarea.
- `PUT /tasks/{id}`: Actualizar tarea.
- `DELETE /tasks/{id}`: Borrar tarea.
