# -*- coding: utf-8 -*-
"""Etapa 2: cuerpo completo del informe (secciones 1 a 7)."""
import copy
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

PATH = "SI886-LAB-04_vargas.docx"
REPO = "https://github.com/AngelVargasGutierrez/PETI-TALLER4"
GRAF = "graficos/S04_diagnostico.png"
ANEXO_A = "evidencias/S04/anexo_A_crehana_pagina.png"

d = docx.Document(PATH)


def find_para(text, style=None):
    for para in d.paragraphs:
        if para.text.strip() == text and (style is None or para.style.name == style):
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
    return add_paragraphs(after_para, items, style="List Bullet")


def delete_paragraph(paragraph):
    p = paragraph._p
    p.getparent().remove(p)


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
# 1. Borrar la pagina "Como se usa esta plantilla"
# =====================================================================
p_iter = d.paragraphs
idx_start = None
for i, para in enumerate(p_iter):
    if para.text.strip() == "Cómo se usa esta plantilla" and para.style.name == "Heading 1":
        idx_start = i
        break
if idx_start is None:
    raise ValueError("No se encontro el heading 'Como se usa esta plantilla'")

idx_end = None
for i in range(idx_start, len(p_iter)):
    if p_iter[i].text.strip() == "Borra esta página antes de entregar.":
        idx_end = i + 1  # incluye el parrafo vacio con el salto de pagina
        break
if idx_end is None:
    raise ValueError("No se encontro el parrafo de cierre de la pagina de instrucciones")

to_delete = p_iter[idx_start:idx_end + 1]
for para in to_delete:
    delete_paragraph(para)

print(f"Eliminados {len(to_delete)} parrafos de la pagina de instrucciones")

d.save(PATH)
print("Etapa 2a (borrar instrucciones) OK")
