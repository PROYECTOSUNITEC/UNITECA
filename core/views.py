from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

ROL_COOKIE = "uniteca_rol"

ROLES_CONFIG = {
    "estudiante": {
        "role_key": "estudiante",
        "role_label": "Estudiante",
        "name": "Gabriel Morales",
        "initials": "GM",
        "can_download": False,
        "can_manage": False,
    },
    "academico": {
        "role_key": "academico",
        "role_label": "Personal Académico",
        "name": "Valentina Acevedo",
        "initials": "VA",
        "can_download": True,
        "can_manage": False,
    },
    "admin": {
        "role_key": "admin",
        "role_label": "Administrador",
        "name": "Ricardo Valero",
        "initials": "RV",
        "can_download": True,
        "can_manage": True,
    },
}

ROLE_MATRIX = [
    {
        "name": "Estudiante",
        "key": "estudiante",
        "summary": "Consulta del catálogo general y lectura completa en el visor en línea.",
        "permissions": ["Búsqueda en el catálogo", "Lectura en visor Split-View", "Cita APA 7"],
        "restriction": "Sin descarga local de archivos",
    },
    {
        "name": "Personal Académico",
        "key": "academico",
        "summary": "Docentes, tutores y jurados examinadores con permiso de descarga.",
        "permissions": [
            "Búsqueda y lectura en sala",
            "Descarga del tomo en PDF",
            "Descarga de láminas de defensa",
        ],
        "restriction": "Acceso completo de lectura y descarga",
    },
    {
        "name": "Administrador",
        "key": "admin",
        "summary": "Personal encargado del registro, catalogación y preservación digital.",
        "permissions": [
            "Depósito de nuevos TEG",
            "Edición de fichas bibliográficas",
            "Descarga de todos los ejemplares",
        ],
        "restriction": "Control y gestión del repositorio",
    },
]

CARRERAS_GRUPOS = [
    {
        "grupo": "Ingenierías",
        "carreras": [
            {
                "nombre": "Ingeniería en Información",
                "abrev": "Ing. en Información",
                "color": "#12409A",
                "titulo_otorgado": "Ingeniero(a) en Información",
            },
            {
                "nombre": "Ingeniería en Redes y Comunicaciones",
                "abrev": "Ing. en Redes y Comunicaciones",
                "color": "#1D5B79",
                "titulo_otorgado": "Ingeniero(a) en Redes y Comunicaciones",
            },
            {
                "nombre": "Ingeniería de Producción Industrial",
                "abrev": "Ing. de Producción Industrial",
                "color": "#8E2C24",
                "titulo_otorgado": "Ingeniero(a) de Producción Industrial",
            },
            {
                "nombre": "Ingeniería Eléctrica",
                "abrev": "Ing. Eléctrica",
                "color": "#A97A12",
                "titulo_otorgado": "Ingeniero(a) Electricista",
            },
            {
                "nombre": "Ingeniería Mecánica",
                "abrev": "Ing. Mecánica",
                "color": "#2F5D50",
                "titulo_otorgado": "Ingeniero(a) Mecánico",
            },
        ],
    },
    {
        "grupo": "Licenciaturas",
        "carreras": [
            {
                "nombre": "Licenciatura en Ciencias Administrativas y Gerenciales",
                "abrev": "Lic. Ciencias Administrativas",
                "color": "#5B4B8A",
                "titulo_otorgado": "Licenciado(a) en Ciencias Administrativas y Gerenciales",
            },
            {
                "nombre": "Licenciatura en Contaduría Pública",
                "abrev": "Lic. Contaduría Pública",
                "color": "#6D4C3D",
                "titulo_otorgado": "Licenciado(a) en Contaduría Pública",
            },
        ],
    },
    {
        "grupo": "Técnicos Superiores Universitarios (TSU)",
        "carreras": [
            {
                "nombre": "TSU en Mercadeo",
                "abrev": "TSU Mercadeo",
                "color": "#7A3E65",
                "titulo_otorgado": "Técnico Superior Universitario en Mercadeo",
            },
            {
                "nombre": "TSU en Recursos Humanos",
                "abrev": "TSU Recursos Humanos",
                "color": "#4A6B82",
                "titulo_otorgado": "Técnico Superior Universitario en Recursos Humanos",
            },
            {
                "nombre": "TSU en Logística",
                "abrev": "TSU Logística",
                "color": "#8C5A2B",
                "titulo_otorgado": "Técnico Superior Universitario en Logística",
            },
            {
                "nombre": "TSU en Informática",
                "abrev": "TSU Informática",
                "color": "#1E5194",
                "titulo_otorgado": "Técnico Superior Universitario en Informática",
            },
            {
                "nombre": "TSU en Mecánica",
                "abrev": "TSU Mecánica",
                "color": "#3B695C",
                "titulo_otorgado": "Técnico Superior Universitario en Mecánica",
            },
            {
                "nombre": "TSU en Electricidad",
                "abrev": "TSU Electricidad",
                "color": "#9B7218",
                "titulo_otorgado": "Técnico Superior Universitario en Electricidad",
            },
            {
                "nombre": "TSU en Producción Industrial",
                "abrev": "TSU Producción Industrial",
                "color": "#84352E",
                "titulo_otorgado": "Técnico Superior Universitario en Producción Industrial",
            },
            {
                "nombre": "TSU en Procedimientos y Métodos",
                "abrev": "TSU Procedimientos y Métodos",
                "color": "#525E75",
                "titulo_otorgado": "Técnico Superior Universitario en Procedimientos y Métodos",
            },
        ],
    },
]

CARRERAS = [item for grupo in CARRERAS_GRUPOS for item in grupo["carreras"]]

MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]

MOCK_TEGS = [
    {
        "id": 1,
        "codigo": "TEG-2026-014",
        "signatura": "TEG 621.31 M538s 2026",
        "anio": 2026,
        "fecha_defensa": "15/07/2026",
        "titulo": (
            "Sistema de detección temprana de fallas en transformadores de potencia "
            "mediante aprendizaje profundo"
        ),
        "autores": [
            {"nombre": "Mariana", "apellido": "Méndez"},
            {"nombre": "Alejandro", "apellido": "Rojas"},
        ],
        "tutor": "Dr. Carlos Mendoza",
        "carrera": "Ingeniería Eléctrica",
        "linea": "",
        "palabras_clave": ["aprendizaje profundo", "transformadores", "mantenimiento predictivo"],
        "paginas": 118,
        "laminas": 24,
        "lecturas": 1284,
        "citas": 12,
        "peso_pdf": "14,2 MB",
        "peso_laminas": "8,6 MB",
        "archivo_pdf": "TEG_2026_014_Mendez_Rojas.pdf",
        "archivo_laminas": "Defensa_TEG_2026_014.pdf",
        "mencion": "Publicación",
        "resumen": (
            "Este trabajo desarrolla un modelo neuronal convolucional-recurrente para el "
            "análisis de gases disueltos y perfiles térmicos en subestaciones eléctricas. "
            "Validado con registros históricos de tres subestaciones, el sistema anticipa "
            "fallas incipientes con una exactitud del 94 % y reduce en un 38 % los tiempos "
            "de parada no programada."
        ),
    },
    {
        "id": 2,
        "codigo": "TEG-2026-009",
        "signatura": "TEG 005.8 P126a 2026",
        "anio": 2026,
        "fecha_defensa": "22/05/2026",
        "titulo": (
            "Arquitectura de confianza cero para la protección de repositorios académicos "
            "y activos de investigación"
        ),
        "autores": [{"nombre": "Daniela", "apellido": "Páez"}],
        "tutor": "Dra. Valentina Acevedo",
        "carrera": "Ingeniería en Redes y Comunicaciones",
        "linea": "Ciberseguridad e infraestructura en la nube",
        "palabras_clave": ["ciberseguridad", "confianza cero", "microsegmentación"],
        "paginas": 96,
        "laminas": 18,
        "lecturas": 2107,
        "citas": 21,
        "peso_pdf": "9,8 MB",
        "peso_laminas": "5,4 MB",
        "archivo_pdf": "TEG_2026_009_Paez.pdf",
        "archivo_laminas": "Defensa_TEG_2026_009.pdf",
        "mencion": "Honorífica",
        "resumen": (
            "Se diseña e implementa una arquitectura de seguridad basada en la verificación "
            "continua de identidad y en el control de acceso granular por rol, orientada a "
            "proteger los repositorios universitarios frente a accesos indebidos, fuga de "
            "información y suplantación de credenciales institucionales."
        ),
    },
    {
        "id": 3,
        "codigo": "TEG-2025-041",
        "signatura": "TEG 658.78 S586o 2025",
        "anio": 2025,
        "fecha_defensa": "10/11/2025",
        "titulo": (
            "Optimización heurística de rutas de distribución de última milla en centros "
            "logísticos multipuerto"
        ),
        "autores": [{"nombre": "Luis Fernando", "apellido": "Silva"}],
        "tutor": "MSc. Roberto Linares",
        "carrera": "Ingeniería de Producción Industrial",
        "linea": "Investigación de operaciones y cadena de suministro",
        "palabras_clave": ["cadena de suministro", "heurística", "logística"],
        "paginas": 134,
        "laminas": 22,
        "lecturas": 876,
        "citas": 7,
        "peso_pdf": "16,5 MB",
        "peso_laminas": "7,1 MB",
        "archivo_pdf": "TEG_2025_041_Silva.pdf",
        "archivo_laminas": "Defensa_TEG_2025_041.pdf",
        "mencion": "",
        "resumen": (
            "Se formula un modelo híbrido de recocido simulado y búsqueda tabú para minimizar "
            "el costo operativo de flotas de reparto urbano con ventanas de tiempo estrictas. "
            "La propuesta reduce la distancia total recorrida en un 17 % respecto al esquema "
            "de despacho vigente en la empresa estudiada."
        ),
    },
    {
        "id": 4,
        "codigo": "TEG-2025-028",
        "signatura": "TEG 006.35 V712m 2025",
        "anio": 2025,
        "fecha_defensa": "19/09/2025",
        "titulo": (
            "Motor de indexación semántica para documentos científicos basado en grafos "
            "de conocimiento"
        ),
        "autores": [
            {"nombre": "Sofía", "apellido": "Villamediana"},
            {"nombre": "Javier", "apellido": "Quintero"},
        ],
        "tutor": "Dra. Valentina Acevedo",
        "carrera": "Ingeniería en Información",
        "linea": "Inteligencia artificial e ingeniería del conocimiento",
        "palabras_clave": ["inteligencia artificial", "procesamiento de lenguaje", "grafos"],
        "paginas": 110,
        "laminas": 20,
        "lecturas": 1652,
        "citas": 15,
        "peso_pdf": "11,9 MB",
        "peso_laminas": "6,2 MB",
        "archivo_pdf": "TEG_2025_028_Villamediana_Quintero.pdf",
        "archivo_laminas": "Defensa_TEG_2025_028.pdf",
        "mencion": "Publicación",
        "resumen": (
            "Se construye un flujo de extracción de entidades académicas y relaciones "
            "temáticas que alimenta un grafo de conocimiento, con el fin de acelerar la "
            "recuperación de literatura técnica en bibliotecas universitarias y sugerir "
            "lecturas afines a partir del contenido de cada documento."
        ),
    },
    {
        "id": 5,
        "codigo": "TEG-2024-052",
        "signatura": "TEG 670.42 M313a 2024",
        "anio": 2024,
        "fecha_defensa": "04/12/2024",
        "titulo": (
            "Automatización de celdas de manufactura flexible mediante gemelos digitales "
            "e internet industrial de las cosas"
        ),
        "autores": [{"nombre": "Héctor", "apellido": "Marcano"}],
        "tutor": "Dr. Ernesto Figuera",
        "carrera": "Ingeniería Mecánica",
        "linea": "Automatización industrial y robótica",
        "palabras_clave": ["automatización", "gemelo digital", "manufactura flexible"],
        "paginas": 142,
        "laminas": 26,
        "lecturas": 731,
        "citas": 4,
        "peso_pdf": "19,4 MB",
        "peso_laminas": "10,3 MB",
        "archivo_pdf": "TEG_2024_052_Marcano.pdf",
        "archivo_laminas": "Defensa_TEG_2024_052.pdf",
        "mencion": "",
        "resumen": (
            "Se sincronizan en tiempo real los sensores de una celda de mecanizado con un "
            "entorno virtual tridimensional, lo que permite validar secuencias de operación "
            "antes de su ejecución física en planta y disminuir los tiempos de puesta a punto."
        ),
    },
    {
        "id": 6,
        "codigo": "TEG-2024-019",
        "signatura": "TEG 658.155 C266m 2024",
        "anio": 2024,
        "fecha_defensa": "14/06/2024",
        "titulo": (
            "Modelo de gobernanza financiera y evaluación del riesgo tecnológico en pequeñas "
            "y medianas empresas industriales"
        ),
        "autores": [{"nombre": "Valeria", "apellido": "Cárdenas"}],
        "tutor": "Dra. Beatriz Fonseca",
        "carrera": "Licenciatura en Ciencias Administrativas y Gerenciales",
        "linea": "Gerencia financiera y transformación digital",
        "palabras_clave": ["gobernanza", "riesgo operativo", "finanzas"],
        "paginas": 88,
        "laminas": 16,
        "lecturas": 549,
        "citas": 3,
        "peso_pdf": "7,5 MB",
        "peso_laminas": "4,8 MB",
        "archivo_pdf": "TEG_2024_019_Cardenas.pdf",
        "archivo_laminas": "Defensa_TEG_2024_019.pdf",
        "mencion": "",
        "resumen": (
            "Se propone un conjunto de indicadores clave de riesgo y de retorno de la "
            "inversión tecnológica para empresas manufactureras, junto con un procedimiento "
            "de evaluación periódica adaptado a su estructura de gobierno."
        ),
    },
]

SLIDES_PREVIEW = [
    {"titulo": "Introducción", "subtitulo": "Contexto y objetivos"},
    {"titulo": "Marco metodológico", "subtitulo": "Diseño de la investigación"},
    {"titulo": "Resultados", "subtitulo": "Métricas comparativas"},
    {"titulo": "Conclusiones", "subtitulo": "Aportes y recomendaciones"},
]

CAPITULOS = [
    {"numero": "", "titulo": "Introducción", "pagina": 1},
    {"numero": "I", "titulo": "El problema", "pagina": 4},
    {"numero": "II", "titulo": "Marco teórico", "pagina": 18},
    {"numero": "III", "titulo": "Marco metodológico", "pagina": 42},
    {"numero": "IV", "titulo": "Análisis de resultados", "pagina": 67},
    {"numero": "V", "titulo": "Conclusiones y recomendaciones", "pagina": 98},
    {"numero": "", "titulo": "Referencias", "pagina": 106},
]

CAMPOS_BUSQUEDA = [
    ("todo", "Todo el registro"),
    ("titulo", "Título"),
    ("autor", "Autor"),
    ("tutor", "Tutor"),
    ("clave", "Palabra clave"),
]

ORDENES = [
    ("recientes", "Más recientes"),
    ("leidos", "Más leídos"),
    ("titulo", "Título A–Z"),
]


def _carrera_info(nombre: str) -> dict:
    return next((c for c in CARRERAS if c["nombre"] == nombre), CARRERAS[0])


def _iniciales(nombre: str) -> str:
    return " ".join(f"{parte[0]}." for parte in nombre.split())


def _autores_apa(autores: list) -> str:
    partes = [f"{a['apellido']}, {_iniciales(a['nombre'])}" for a in autores]
    if len(partes) == 1:
        return partes[0]
    return ", ".join(partes[:-1]) + ", & " + partes[-1]


def _fecha_larga(fecha: str) -> str:
    dia, mes, anio = fecha.split("/")
    return f"{int(dia)} de {MESES[int(mes) - 1]} de {anio}"


def _mes_anio(fecha: str) -> str:
    _, mes, anio = fecha.split("/")
    return f"{MESES[int(mes) - 1]} de {anio}"


def _enriquecer(teg: dict) -> dict:
    carrera = _carrera_info(teg["carrera"])
    data = dict(teg)
    data["autor"] = " y ".join(f"{a['nombre']} {a['apellido']}" for a in teg["autores"])
    data["carrera_color"] = carrera["color"]
    data["carrera_abrev"] = carrera["abrev"]
    data["titulo_otorgado"] = carrera["titulo_otorgado"]
    data["fecha_larga"] = _fecha_larga(teg["fecha_defensa"])
    data["mes_anio"] = _mes_anio(teg["fecha_defensa"])
    data["autores_apa"] = _autores_apa(teg["autores"])
    return data


def _get_current_user(request: HttpRequest) -> dict:
    role_key = request.GET.get("rol") or request.COOKIES.get(ROL_COOKIE) or "academico"
    return ROLES_CONFIG.get(role_key.lower(), ROLES_CONFIG["academico"])


def _render(request: HttpRequest, template: str, context: dict) -> HttpResponse:
    response = render(request, template, context)
    role_key = request.GET.get("rol", "").lower()
    if role_key in ROLES_CONFIG:
        response.set_cookie(ROL_COOKIE, role_key, samesite="Lax")
    return response


def _coincide(teg: dict, consulta: str, campo: str) -> bool:
    textos = {
        "titulo": [teg["titulo"]],
        "autor": [teg["autor"]],
        "tutor": [teg["tutor"]],
        "clave": teg["palabras_clave"],
    }
    if campo in textos:
        candidatos = textos[campo]
    else:
        candidatos = [
            teg["titulo"],
            teg["autor"],
            teg["tutor"],
            teg["codigo"],
            teg["signatura"],
            teg["resumen"],
            *teg["palabras_clave"],
        ]
    return any(consulta in texto.lower() for texto in candidatos)


@api_view(["GET"])
def hello_world(request: HttpRequest) -> Response:
    return Response({"message": "Hello, world!", "app": "UNITECA"})


def login_view(request: HttpRequest) -> HttpResponse:
    current_user = _get_current_user(request)
    context = {
        "current_user": current_user,
        "selected_role": current_user["role_key"],
        "role_matrix": ROLE_MATRIX,
    }
    return _render(request, "core/login.html", context)


def dashboard_view(request: HttpRequest) -> HttpResponse:
    current_user = _get_current_user(request)
    consulta = request.GET.get("q", "").strip()
    campo = request.GET.get("campo", "todo").strip()
    carrera_sel = request.GET.get("carrera", "").strip()
    autor = request.GET.get("autor", "").strip()
    desde = request.GET.get("desde", "").strip()
    hasta = request.GET.get("hasta", "").strip()
    mencion = request.GET.get("mencion", "").strip()
    orden = request.GET.get("orden", "recientes").strip()

    todos = [_enriquecer(t) for t in MOCK_TEGS]
    tegs = list(todos)

    if consulta:
        tegs = [t for t in tegs if _coincide(t, consulta.lower(), campo)]
    if carrera_sel:
        tegs = [t for t in tegs if t["carrera"] == carrera_sel]
    if autor:
        tegs = [t for t in tegs if autor.lower() in t["autor"].lower()]
    if desde.isdigit():
        tegs = [t for t in tegs if t["anio"] >= int(desde)]
    if hasta.isdigit():
        tegs = [t for t in tegs if t["anio"] <= int(hasta)]
    if mencion:
        tegs = [t for t in tegs if t["mencion"]]

    if orden == "leidos":
        tegs.sort(key=lambda t: t["lecturas"], reverse=True)
    elif orden == "titulo":
        tegs.sort(key=lambda t: t["titulo"].lower())
    else:
        orden = "recientes"
        tegs.sort(key=lambda t: t["codigo"], reverse=True)

    anios = [t["anio"] for t in todos]

    context = {
        "current_user": current_user,
        "tegs": tegs,
        "total_tegs": len(todos),
        "total_lecturas": sum(t["lecturas"] for t in todos),
        "anio_min": min(anios),
        "anio_max": max(anios),
        "carreras_grupos": CARRERAS_GRUPOS,
        "campos": CAMPOS_BUSQUEDA,
        "ordenes": ORDENES,
        "hay_filtros": bool(consulta or carrera_sel or autor or desde or hasta or mencion),
        "filters": {
            "q": consulta,
            "campo": campo,
            "carrera": carrera_sel,
            "autor": autor,
            "desde": desde,
            "hasta": hasta,
            "mencion": mencion,
            "orden": orden,
        },
    }
    return _render(request, "core/dashboard.html", context)


def detalle_view(request: HttpRequest, teg_id: int) -> HttpResponse:
    current_user = _get_current_user(request)
    base = next((item for item in MOCK_TEGS if item["id"] == teg_id), None)
    if base is None:
        raise Http404("El Trabajo Especial de Grado solicitado no existe.")
    teg = _enriquecer(base)

    otros = [_enriquecer(t) for t in MOCK_TEGS if t["id"] != teg_id]
    otros.sort(key=lambda t: (t["carrera"] != teg["carrera"], -t["lecturas"]))

    context = {
        "current_user": current_user,
        "teg": teg,
        "slides_preview": SLIDES_PREVIEW,
        "capitulos": CAPITULOS,
        "relacionados": otros[:3],
    }
    return _render(request, "core/detalle.html", context)


def upload_view(request: HttpRequest) -> HttpResponse:
    current_user = _get_current_user(request)
    upload_success = False
    submitted_title = ""

    if request.method == "POST":
        upload_success = True
        submitted_title = request.POST.get("titulo", "Nuevo TEG registrado")

    context = {
        "current_user": current_user,
        "carreras_grupos": CARRERAS_GRUPOS,
        "upload_success": upload_success,
        "submitted_title": submitted_title,
    }
    return _render(request, "core/upload.html", context)
