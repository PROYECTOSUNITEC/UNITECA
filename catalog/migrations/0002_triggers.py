from django.db import migrations

INCREMENTAR_VISTAS_FORWARD = """
CREATE FUNCTION incrementar_vistas_documento() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE documentos
    SET vistas_contador = vistas_contador + 1
    WHERE id = NEW.documento_id;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_incrementar_vistas
    AFTER INSERT ON historial_consultas
    FOR EACH ROW EXECUTE FUNCTION incrementar_vistas_documento();
"""

INCREMENTAR_VISTAS_REVERSE = """
DROP TRIGGER IF EXISTS trg_incrementar_vistas ON historial_consultas;
DROP FUNCTION IF EXISTS incrementar_vistas_documento();
"""

VALIDAR_TUTOR_FORWARD = """
CREATE FUNCTION validar_autor_no_sea_tutor() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM documento_autores
        WHERE documento_id = NEW.documento_id
          AND usuario_id = NEW.tutor_id
    ) THEN
        RAISE EXCEPTION 'Error de validación: El usuario (ID: %) ya está asignado como autor de este documento y no puede ser tutor de su propio trabajo.', NEW.tutor_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validar_tutor
    BEFORE INSERT OR UPDATE ON documento_tutores
    FOR EACH ROW EXECUTE FUNCTION validar_autor_no_sea_tutor();
"""

VALIDAR_TUTOR_REVERSE = """
DROP TRIGGER IF EXISTS trg_validar_tutor ON documento_tutores;
DROP FUNCTION IF EXISTS validar_autor_no_sea_tutor();
"""


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(INCREMENTAR_VISTAS_FORWARD, reverse_sql=INCREMENTAR_VISTAS_REVERSE),
        migrations.RunSQL(VALIDAR_TUTOR_FORWARD, reverse_sql=VALIDAR_TUTOR_REVERSE),
    ]
