# UNITECA — guía para asistentes de IA

Sistema de gestión bibliotecaria en Django + Django REST Framework + PostgreSQL 17, corriendo en Docker (ver `README.md`).

## Reglas de trabajo

- No hagas commit ni push directo a `main` o `development`. Todo cambio va en una rama propia creada desde `development` (ver `CONTRIBUTING.md`).
- No edites migraciones (`*/migrations/*.py`) a mano; generarlas con `python manage.py makemigrations`.
- No subas ni edites `.env`, credenciales o secretos. Usa `.env.example` como referencia.
- No borres ni reescribas datos de la base de datos (`docker compose down -v`, `DROP`, `TRUNCATE`, etc.) sin confirmarlo antes conmigo.
- No agregues dependencias nuevas en `requirements.txt` sin que lo pida explícitamente.
- Antes de un cambio en el esquema de datos o en `docker-compose.yml`, avísame qué vas a cambiar y por qué.
- Sigue el estilo ya presente en el proyecto (Django/DRF estándar); no introduzcas otro framework o patrón sin preguntar.
