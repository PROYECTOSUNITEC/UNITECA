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

3. Verifica el endpoint de prueba:

   ```bash
   curl http://localhost:8000/api/hello/
   ```

   Respuesta esperada:

   ```json
   {"message": "Hello, world!", "app": "UNITECA"}
   ```

## Servicios

- `web`: aplicación Django (puerto `8000`).
- `db`: PostgreSQL 17 (puerto `5432`).

## Contribuir

Revisa [CONTRIBUTING.md](CONTRIBUTING.md) antes de aportar cambios.
