# -*- coding: utf-8 -*-
"""Etapa 7: corrige el orden de la nota introductoria en la seccion 5 (Cuestionario)."""
import copy
import docx

PATH = "SI886-LAB-04_vargas.docx"
d = docx.Document(PATH)

NOTA = ("3-TALLER.md no incluye, para esta semana, una sección de cuestionario "
        "independiente: las preguntas del laboratorio están integradas dentro de los "
        "pasos del procedimiento (Sección 2). Se reproducen y responden a "
        "continuación por completitud.")

paras = d.paragraphs
idx_heading = None
idx_nota = None
for i, para in enumerate(paras):
    if para.text.strip() == "5. Cuestionario" and para.style.name == "Heading 1":
        idx_heading = i
    if para.text.strip() == NOTA:
        idx_nota = i

if idx_heading is None or idx_nota is None:
    raise ValueError(f"No encontrado: heading={idx_heading} nota={idx_nota}")

nota_p = paras[idx_nota]._p
heading_p = paras[idx_heading]._p

# mover el elemento XML de la nota a justo despues del heading
nota_p.getparent().remove(nota_p)
heading_p.addnext(nota_p)

d.save(PATH)
print("Orden corregido en Seccion 5.")
