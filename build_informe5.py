# -*- coding: utf-8 -*-
"""Etapa 5: Secciones 3 a 7."""
import copy
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

PATH = "SI886-LAB-04_vargas.docx"
REPO = "https://github.com/AngelVargasGutierrez/PETI-TALLER4"
GRAF = "graficos/S04_diagnostico.png"

d = docx.Document(PATH)


def find_para(text, style=None, contains=False):
    for para in d.paragraphs:
        t = para.text.strip()
        ok = (text in t) if contains else (t == text)
        if ok and (style is None or para.style.name == style):
            return para
    raise ValueError(f"No se encontro parrafo: {text!r}")


def insert_paragraph_after(paragraph, text="", style=None):
    new_p = copy.deepcopy(paragraph._p)
    for child in list(new_p):
        new_p.remove(child)
    paragraph._p.addnext(new_p)
    from docx.text.paragraph import Paragraph
    new_para = Paragraph(new_p, paragraph._parent)
    if style:
        new_para.style = style
    if text:
        new_para.add_run(text)
    return new_para


def add_paragraphs(after_para, items, style=None):
    cur = after_para
    for it in items:
        cur = insert_paragraph_after(cur, it, style=style)
    return cur


def add_bullets(after_para, items):
    return add_paragraphs(after_para, [f"•  {it}" for it in items], style="Compact")


def add_image_paragraph(after_para, img_path, width_in=5.5, caption=None):
    cur = insert_paragraph_after(after_para, "")
    cur.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cur.add_run()
    run.add_picture(img_path, width=Inches(width_in))
    if caption:
        cur2 = insert_paragraph_after(cur, caption)
        cur2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in cur2.runs:
            r.italic = True
            r.font.size = Pt(9)
        return cur2
    return cur


# =====================================================================
# SECCION 3 -- RESULTADOS
# =====================================================================
h3 = find_para("3. Resultados", style="Heading 1")
h3_note = find_para("Si algo no se logró, explícalo aquí. Un resultado no alcanzado y "
                     "bien explicado vale más que uno declarado sin evidencia.")
cur = add_paragraphs(h3_note, [
    "Los tres resultados que se califican (registro de las declaraciones, diagnóstico "
    "de la misión y visión de TI derivada) se lograron en su totalidad y están "
    "enlazados con su evidencia verificable en GitHub. El único resultado logrado de "
    "forma parcial es el número 9 (métricas implícitas de la visión): al no existir una "
    "visión formal, no hay métricas propias que documentar; esta ausencia se registró "
    "honestamente como hallazgo, en vez de inventar cifras que la empresa no declara.",
])

tabla_resultados = d.tables[1]  # header + 8 filas ya existentes
filas_datos = [
    ["1", "Empresa del sector tecnológico elegida, con su actividad y su país", "Sí",
     f"{REPO}/blob/main/02_identidad/MV01_declaraciones.md"],
    ["2", "Misión y visión transcritas literalmente, con dirección y fecha de consulta",
     "Sí (misión) — Hallazgo: la empresa no publica visión (documentado)",
     f"{REPO}/blob/main/02_identidad/MV01_declaraciones.md"],
    ["3", "Los cinco componentes de la misión, cada uno con su fragmento literal", "Sí",
     f"{REPO}/blob/main/02_identidad/2.1_mision.md"],
    ["4", "Los siete defectos revisados, señalados con su nombre técnico y su prueba",
     "Sí (3/7 aplican; 2 no aplican; 2 no evaluables con información pública)",
     f"{REPO}/blob/main/evidencias/S04/diagnostico.txt"],
    ["5", "Prueba de sustitución ejecutada con tres competidores reales", "Sí",
     f"{REPO}/blob/main/evidencias/S04/diagnostico.txt"],
    ["6", "Prueba de la decisión y prueba del reconocimiento respondidas", "Sí",
     f"{REPO}/blob/main/02_identidad/2.1_mision.md"],
    ["7", "Veredicto de la misión y de la visión, con la regla que lo produce", "Sí",
     f"{REPO}/blob/main/evidencias/S04/diagnostico.txt"],
    ["8", "Los cinco atributos de la visión evaluados con su evidencia", "Sí",
     f"{REPO}/blob/main/02_identidad/2.2_vision.md"],
]
for i, fila_datos in enumerate(filas_datos):
    row = tabla_resultados.rows[i + 1]
    for c, val in enumerate(fila_datos):
        row.cells[c].text = val

filas_adicionales = [
    ["9", "Métricas implícitas de la visión con su línea base y su fuente",
     "Parcial — documentado el hallazgo de ausencia de visión, con las cifras reales "
     "disponibles como línea base",
     f"{REPO}/blob/main/02_identidad/2.2_vision.md"],
    ["10", "Versión propuesta de la misión, con la constancia de que adoptarla decide "
     "la empresa", "Sí", f"{REPO}/blob/main/02_identidad/2.1_mision.md"],
    ["11", "Visión de TI derivada con la estructura de la teoría", "Sí",
     f"{REPO}/blob/main/02_identidad/2.2_vision.md"],
    ["12", "Tabla de derivación con estado actual y estado objetivo por capacidad", "Sí",
     f"{REPO}/blob/main/02_identidad/2.2_vision.md"],
    ["13", "Etiqueta v0.4 en Git", "Sí", f"{REPO}/tree/v0.4"],
]
for fila_datos in filas_adicionales:
    row = tabla_resultados.add_row()
    for c, val in enumerate(fila_datos):
        row.cells[c].text = val

cur_after_table = find_para("3. Resultados", style="Heading 1")
# insertar grafico despues del cierre de la tabla: localizamos el ultimo parrafo
# del documento que sigue a la tabla (python-docx no vincula tablas a parrafos
# directamente; se añade el grafico dentro del propio cuerpo, tras el heading 4)


# =====================================================================
# SECCION 4 -- CONCLUSIONES
# =====================================================================
h4 = find_para("Mínimo tres. Una conclusión no resume lo que hiciste. Dice lo que "
               "aprendiste y se sostiene en la evidencia de la sección 3.")
add_bullets(h4, [
    "Una misión que sobrevive a la prueba de sustitución con competidores reales, como "
    "ocurrió con la de Crehana frente a Buk, Runa HR y Platzi para Empresas, no ha "
    "servido nunca para rechazar nada: cualquier decisión de TI que se apoye en ella "
    "hereda esa misma incapacidad de discriminar entre alternativas de inversión.",
    "Nombrar el defecto con su término técnico y probarlo con evidencia textual — y no "
    "con una impresión como «es muy general» — es lo único que sostiene una "
    "recomendación ante la alta dirección: de los siete defectos evaluados sobre la "
    "misión de Crehana, tres aplicaban con evidencia directa (intercambiable, "
    "confunde misión con visión, omite al destinatario) y dos no pudieron evaluarse "
    "por falta de acceso a información interna de la empresa — se documentó esa "
    "limitación con honestidad en vez de forzar un veredicto sin evidencia.",
    "La ausencia de una visión formal no es un vacío neutro: obliga a construir "
    "cualquier plan de TI sobre datos sueltos (como los más de 1200 clientes y los 10 "
    "años de trayectoria que sí publica la empresa) en lugar de sobre una meta "
    "declarada, lo que deja a la función de TI sin un criterio objetivo de "
    "priorización de inversiones.",
    "Derivar la visión de TI directamente de fragmentos textuales verificables — y no "
    "de una idea del equipo — es lo único que permite trazar cada capacidad de TI de "
    "la Sección 2.2.4 hasta su origen concreto en lo que la empresa realmente declara, "
    "insumo que después ordena el portafolio de proyectos del PETI.",
])

# =====================================================================
# SECCION 5 -- CUESTIONARIO
# =====================================================================
h5 = find_para("Copia cada pregunta de la guía de la semana y respóndela debajo.")
add_paragraphs(h5, [
    "3-TALLER.md no incluye, para esta semana, una sección de cuestionario "
    "independiente: las preguntas del laboratorio están integradas dentro de los "
    "pasos del procedimiento (Sección 2). Se reproducen y responden a continuación "
    "por completitud.",
])
add_bullets(h5, [
    "Pregunta (Paso B): ¿la misión vigente supera las tres pruebas de calidad? "
    "Respuesta: no. No supera ninguna de las tres — ni la de sustitución, ni la de la "
    "decisión, ni la del reconocimiento.",
    "Pregunta (Paso A/C): ¿la empresa publica una visión institucional? Respuesta: no. "
    "Esa ausencia se documenta como hallazgo formal en la Sección 2.2.1.",
    "Pregunta de transferencia (Paso F): ¿qué riesgo correría una organización real si "
    "esto se hiciera mal? Respuesta: financiaría capacidades de TI indistinguibles de "
    "las de cualquier competidor y sin métrica que verifique el retorno de la "
    "inversión, y perdería el criterio objetivo para priorizar qué proyecto emprender "
    "primero.",
])

# =====================================================================
# SECCION 6 -- REFERENCIAS
# =====================================================================
h6 = find_para("Normas técnicas, marcos profesionales, documentación oficial y "
               "bibliografía indexada, en formato APA. No se admiten wikis abiertas "
               "ni sitios sin autoría verificable.", contains=True)
add_paragraphs(h6, [
    "Crehana. (2026). Sobre nosotros. https://www.crehana.com/sobre-nosotros/ "
    "(consultado el 10 de septiembre de 2026).",
    "González Millán, J. (2020). Manual práctico de planeación estratégica. Ediciones "
    "Díaz de Santos. https://elibro.net/es/lc/bibliotecaupt/titulos/129291",
    "García Sánchez, E. y Valencia Velazco, M. L. Planeación estratégica: teoría y "
    "práctica. Trillas.",
    "Rodríguez Bermúdez, J. R. (2015). Planificación y dirección estratégica de "
    "sistemas de información. Editorial UOC. "
    "https://elibro.net/es/lc/bibliotecaupt/titulos/57875",
    "Collins, J. y Porras, J. (1996). Building your company's vision. Harvard Business "
    "Review, 74(5), 65–77.",
    "Bart, C. K. (1997). Sex, lies, and mission statements. Business Horizons, 40(6), "
    "9–18.",
    "CEPLAN. Guía para el Planeamiento Institucional — formulación de la misión "
    "institucional. https://www.gob.pe/ceplan",
    "Resolución de Secretaría de Gobierno Digital 005-2018-PCM/SEGDI — Anexo I. "
    "https://cdn.www.gob.pe/uploads/document/file/356863/Anexo_I_Lineamientos_PGD.pdf",
])

# =====================================================================
# SECCION 7 -- ANEXOS
# =====================================================================
h7 = find_para("Capturas completas, archivos de configuración y salidas extensas. "
               "Cada anexo lleva su letra y su título, y se menciona en el cuerpo del "
               "informe.", contains=True)
cur = add_paragraphs(h7, [
    f"Anexo A — captura de la página oficial de Crehana, con la dirección y la fecha "
    f"visibles (incluida en el cuerpo del informe, Paso A, y en "
    f"{REPO}/blob/main/evidencias/S04/anexo_A_crehana_pagina.png).",
    f"Anexo B — salida completa del diagnóstico: {REPO}/blob/main/evidencias/S04/diagnostico.txt",
    f"Anexo C — gráfico del diagnóstico (incluido en el cuerpo del informe, Paso B, y "
    f"en {REPO}/blob/main/graficos/S04_diagnostico.png).",
    f"Anexo D — Secciones 2.1 y 2.2 del PETI en formato versionable: "
    f"{REPO}/blob/main/02_identidad/2.1_mision.md y "
    f"{REPO}/blob/main/02_identidad/2.2_vision.md",
    f"Repositorio completo del taller (rama fusionada, etiquetas v0.4 y taller-04): {REPO}",
])

d.save(PATH)
print("Secciones 3-7 OK")
