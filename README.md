# UNITECA

Sistema de gestión bibliotecaria desarrollado con Django, Django REST Framework y PostgreSQL.

## Requisitos

- Docker
- Docker Compose

## Levantar el proyecto

1. Copia el archivo de variables de entorno de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Levanta los servicios:

   ```bash
   docker compose up --build
   ```

3. Aplica las migraciones (crean el esquema y cargan roles/categorías/líneas de investigación base):

   ```bash
   docker compose exec web python manage.py migrate
   ```

4. Verifica el endpoint de prueba:

   ```bash
   curl http://localhost:8000/api/hello/
   ```

   Respuesta esperada:

   ```json
   {"message": "Hello, world!", "app": "UNITECA"}
   ```

## Servicios

- `web`: aplicación Django (puerto `8000`).
- `db`: PostgreSQL 17 (puerto `5432`, o `POSTGRES_PORT_HOST` si lo cambiaste en `.env`).
- `minio`: almacenamiento de objetos S3-compatible para los archivos de los trabajos (API en `9000`, consola en `9001`, o los puertos que definas en `.env`). El bucket `documentos` se crea automáticamente al levantar el contenedor.

## Modelo de datos

El esquema (`accounts` y `catalog`) está basado en `database_uniteca_v1.sql`: usuarios con roles, categorías y líneas de investigación, documentos (tesis/trabajos) con autores y tutores, historial de consultas, búsqueda de texto completo en español y los triggers originales:

- `trg_incrementar_vistas`: incrementa el contador de vistas de un documento al registrarse una consulta.
- `trg_validar_tutor`: impide que un autor sea tutor de su propio trabajo.

`accounts.Usuario` es el modelo de autenticación de Django (`AUTH_USER_MODEL`); usa email como usuario.

## API

- `GET/POST /api/documentos/`, `GET/PUT/PATCH/DELETE /api/documentos/<id>/`: gestión de trabajos. El campo `archivo` se sube directamente a MinIO.
- `GET /api/categorias/`, `GET /api/lineas/`: catálogos de referencia.

> Nota: las URLs firmadas de `archivo` apuntan al host interno `minio:9000` (la red de Docker Compose). Para abrirlas desde el navegador en desarrollo, agrega `127.0.0.1 minio` a tu archivo `hosts` o cambia `MINIO_ENDPOINT` según tu entorno.

## Contribuir

Revisa [CONTRIBUTING.md](CONTRIBUTING.md) antes de aportar cambios.
