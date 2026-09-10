# -*- coding: utf-8 -*-
"""Etapa 6: limpieza de textos instructivos residuales de la plantilla."""
import docx

PATH = "SI886-LAB-04_vargas.docx"
d = docx.Document(PATH)

TEXTOS_A_BORRAR = [
    "Reglas de uso del laboratorio y de alcance que se respetaron durante el trabajo.",
    "Si algo no se logró, explícalo aquí. Un resultado no alcanzado y bien explicado "
    "vale más que uno declarado sin evidencia.",
    "Mínimo tres. Una conclusión no resume lo que hiciste. Dice lo que aprendiste y se "
    "sostiene en la evidencia de la sección 3.",
    "Copia cada pregunta de la guía de la semana y respóndela debajo.",
    "Normas técnicas, marcos profesionales, documentación oficial y bibliografía "
    "indexada, en formato APA. No se admiten wikis abiertas ni sitios sin autoría "
    "verificable.",
    "Capturas completas, archivos de configuración y salidas extensas. Cada anexo "
    "lleva su letra y su título, y se menciona en el cuerpo del informe.",
]

borrados = 0
for para in list(d.paragraphs):
    if para.text.strip() in TEXTOS_A_BORRAR:
        p = para._p
        p.getparent().remove(p)
        borrados += 1

print(f"Parrafos instructivos eliminados: {borrados}")
d.save(PATH)
print("Etapa 6 (limpieza) OK")
