# Guía de contribución

Gracias por tu interés en aportar a UNITECA. Sigue estos pasos para contribuir correctamente.

## Flujo de trabajo

1. **Copia el repositorio** (fork o clon, según el acceso que tengas) en tu cuenta o máquina local.

   ```bash
   git clone <url-de-tu-copia>
   cd UNITECA
   ```

2. **Parte siempre desde la rama `development`**. Esta rama contiene el estado integrado más reciente del proyecto; no se trabaja directamente sobre `main`.

   ```bash
   git checkout development
   git pull origin development
   ```

3. **Crea una rama propia** para tu cambio, a partir de `development`:

   ```bash
   git checkout -b tipo/nombre-descriptivo
   ```

   Ejemplos de prefijos sugeridos: `feature/`, `fix/`, `chore/`, `docs/`.

4. **Desarrolla y haz commits** pequeños y descriptivos en tu rama.

5. **Sube tu rama** y abre un Pull Request **hacia `development`** (no hacia `main`).

   ```bash
   git push origin tipo/nombre-descriptivo
   ```

6. Espera revisión y atiende los comentarios antes del merge.

## Reglas generales

- `main` refleja únicamente versiones estables/liberadas del proyecto.
- Todo el desarrollo activo ocurre en ramas creadas a partir de `development`.
- No se hace commit directo sobre `development` ni `main`.
- Mantén tus ramas actualizadas con `development` antes de abrir el PR.
