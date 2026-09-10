# -*- coding: utf-8 -*-
"""
MV01_diagnostico_declaraciones.py
SI-886 Planeamiento Estrategico de TI -- Taller 04 (UPT)
Aplica los instrumentos de la teoria (5 componentes, 7 defectos y 3 pruebas
de calidad de la mision; 5 atributos de la vision) sobre las declaraciones
literales de una empresa real, y emite el veredicto segun la regla del taller.

Nota de origen: la carpeta de la semana compartida con el estudiante no
incluia el archivo original ../HERRAMIENTAS/SEMANA-04/MV01_diagnostico_declaraciones.py
ni 1-TEORIA.md. Este script es una reconstruccion propia que aplica, de forma
literal, los 5 componentes y las 3 pruebas de calidad tal como los describe
3-TALLER.md, y una lista de 7 defectos tecnicos con respaldo bibliografico
estandar de la literatura de planeamiento estrategico (Bart, 1997; David, F.,
Strategic Management), dado que el listado exacto del docente no estaba
disponible. Se recomienda verificar la terminologia exacta contra 1-TEORIA.md
antes de la entrega final.
"""

import sys
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class _Tee(io.TextIOBase):
    """Escribe en consola y en un archivo UTF-8 al mismo tiempo, evitando
    que la codificacion de la consola de Windows (cp1252) corrompa las
    tildes al redirigir la salida con '>' o 'tee'."""

    def __init__(self, *streams):
        self._streams = streams

    def write(self, s):
        for st in self._streams:
            st.write(s)
        return len(s)

    def flush(self):
        for st in self._streams:
            st.flush()

# =====================================================================
# 1. DATOS DE LA EMPRESA (editados con los datos reales de Crehana)
# =====================================================================
EMPRESA = "Crehana"
FUENTE_URL = "https://www.crehana.com/sobre-nosotros/"
FECHA_CONSULTA = "10/09/2026"

MISION_TEXTO = "Nuestra misión es construir equipos listos para el futuro"
VISION_TEXTO = None  # La empresa no publica una vision formal (hallazgo)
DECLARACION_IMPACTO = "Impulsamos equipos. Potenciamos culturas. Transformamos resultados."

COMPETIDORES = ["Buk", "Runa HR", "Platzi para Empresas"]

# =====================================================================
# 2. LOS CINCO COMPONENTES DE LA MISION
# =====================================================================
COMPONENTES = {
    "Que hacemos":        {"presente": False, "fragmento": "(ausente) no se identifica un verbo ni una actividad concreta: no menciona plataforma, software ni capacitacion"},
    "Para quien":         {"presente": False, "fragmento": "(ausente) no menciona 'empresas', 'equipos de Recursos Humanos' ni 'America Latina' dentro de la propia oracion de mision"},
    "Como nos distingue": {"presente": False, "fragmento": "(ausente) no hay ningun elemento que la diferencie de un competidor del mismo rubro"},
    "Para que":           {"presente": True,  "fragmento": "'construir equipos listos para el futuro' -- presente mas es un valor vago, sin definir que significa 'listos'"},
    "Con que compromiso": {"presente": False, "fragmento": "(ausente) no hay referencia a principios, etica ni forma de operar"},
}

# =====================================================================
# 3. LOS SIETE DEFECTOS TECNICOS
# =====================================================================
DEFECTOS = {
    "Generalidad excesiva": {
        "aplica": True,
        "evidencia": "La frase podria pertenecer a cualquier empresa de software, banco o consultora: no contiene ningun termino propio del sector de gestion de talento.",
    },
    "Ausencia de destinatario explicito": {
        "aplica": True,
        "evidencia": "No nombra 'empresas', 'clientes' ni 'equipos de RR.HH.' -- estos datos solo aparecen en otras secciones de la pagina, no en la oracion de mision.",
    },
    "Ausencia de elemento distintivo": {
        "aplica": True,
        "evidencia": "No explica por que Crehana, y no Buk o Runa HR, deberia 'construir equipos listos para el futuro'.",
    },
    "Confusion con eslogan publicitario": {
        "aplica": True,
        "evidencia": "Comparte el mismo registro corto y aspiracional que la linea de cierre de marketing de la propia pagina: 'Impulsamos equipos. Potenciamos culturas. Transformamos resultados.'",
    },
    "Sobrepromesa sin sustento medible": {
        "aplica": True,
        "evidencia": "'Listos para el futuro' no define ninguna metrica ni plazo que permita verificar si la promesa se cumple.",
    },
    "Ausencia de compromiso o principios": {
        "aplica": True,
        "evidencia": "No hay mencion a etica, calidad de datos, privacidad ni ningun otro principio que rija como se ejecuta la mision.",
    },
    "Ausencia de actividad concreta identificable": {
        "aplica": True,
        "evidencia": "No hay verbo de accion operativo (no dice 'desarrollamos software', 'capacitamos' ni 'conectamos datos'): 'construir equipos' describe un resultado, no una actividad.",
    },
}

# =====================================================================
# 4. LAS TRES PRUEBAS DE CALIDAD
# =====================================================================
def prueba_sustitucion():
    resultados = []
    for competidor in COMPETIDORES:
        variante = f"La mision de {competidor} es construir equipos listos para el futuro"
        resultados.append((competidor, variante, True))  # True = sigue sonando creible
    supera = not any(r[2] for r in resultados)  # supera solo si NINGUNA variante es creible
    return resultados, supera

def prueba_decision():
    pregunta = "¿Esta declaracion permite decidir si Crehana deberia lanzar un modulo de nomina (payroll)?"
    respuesta = "No. La frase es demasiado abstracta para orientar ninguna decision concreta de producto, mercado o inversion."
    supera = False
    return pregunta, respuesta, supera

def prueba_reconocimiento():
    pregunta = "Mostrada sin el logotipo, ¿un tercero podria identificar que pertenece a Crehana?"
    respuesta = "No. La oracion no contiene 'talento', 'Recursos Humanos', 'LATAM' ni ningun otro rasgo propio de la marca."
    supera = False
    return pregunta, respuesta, supera

# =====================================================================
# 5. LOS CINCO ATRIBUTOS DE LA VISION (aplicados a la declaracion de
#    impacto disponible, dado que la empresa no publica una vision formal)
# =====================================================================
ATRIBUTOS_VISION = {
    "Temporalmente acotada": {
        "cumple": False,
        "evidencia": "No declara ningun ano ni horizonte temporal.",
    },
    "Verificable": {
        "cumple": False,
        "evidencia": "No contiene ninguna cifra objetivo (ni de empresas, ni de paises, ni de ingresos).",
    },
    "Ambiciosa pero alcanzable": {
        "cumple": None,
        "evidencia": "No se puede evaluar: al no declarar una meta concreta, no hay nada que contrastar contra el tamano real de la empresa (+1200 empresas cliente en LATAM, 10 anios de trayectoria).",
    },
    "Especifica del negocio": {
        "cumple": False,
        "evidencia": "'Impulsamos equipos. Potenciamos culturas. Transformamos resultados.' podria pertenecer a cualquier empresa de consultoria o de recursos humanos.",
    },
    "Movilizadora": {
        "cumple": False,
        "evidencia": "No permite decidir, por si sola, ninguna inversion o prioridad concreta de la funcion de TI.",
    },
}

# =====================================================================
# 6. LOGICA DE VEREDICTO (segun la regla literal del taller)
# =====================================================================
def veredicto_mision(n_componentes, hay_defectos, pruebas_superadas):
    if n_componentes <= 3:
        return "SE REFORMULA", "porta 3 componentes o menos"
    if n_componentes == 5 and pruebas_superadas == 3:
        return "SE CONSERVA", "porta los 5 componentes y supera las 3 pruebas"
    return "SE AJUSTA", "porta 4 componentes, o tiene algun defecto senalable"

# =====================================================================
# 7. IMPRESION DEL DIAGNOSTICO
# =====================================================================
def main():
    salida_path = "../evidencias/S04/diagnostico.txt"
    archivo = open(salida_path, "w", encoding="utf-8")
    original_stdout = sys.stdout
    sys.stdout = _Tee(original_stdout, archivo)

    print("=" * 78)
    print(f"DIAGNOSTICO DE DECLARACIONES INSTITUCIONALES -- {EMPRESA}")
    print(f"Fuente: {FUENTE_URL}  |  Fecha de consulta: {FECHA_CONSULTA}")
    print("=" * 78)

    print("\nMISION VIGENTE (texto literal):")
    print(f'  "{MISION_TEXTO}"')

    print("\n--- 1. LOS CINCO COMPONENTES ---")
    n_presentes = 0
    for nombre, datos in COMPONENTES.items():
        marca = "[X]" if datos["presente"] else "[ ]"
        if datos["presente"]:
            n_presentes += 1
        print(f"  {marca} {nombre}: {datos['fragmento']}")
    print(f"\n  Componentes presentes: {n_presentes} / 5")

    print("\n--- 2. LOS SIETE DEFECTOS TECNICOS ---")
    n_defectos = 0
    for nombre, datos in DEFECTOS.items():
        if datos["aplica"]:
            n_defectos += 1
            print(f"  [DEFECTO] {nombre}")
            print(f"      Evidencia: {datos['evidencia']}")
    print(f"\n  Defectos identificados: {n_defectos} / 7")

    print("\n--- 3. LAS TRES PRUEBAS DE CALIDAD ---")
    resultados_sust, supera_sust = prueba_sustitucion()
    print("  a) Prueba de sustitucion (con tres competidores reales):")
    for competidor, variante, sigue_creible in resultados_sust:
        estado = "sigue sonando creible -> FALLA" if sigue_creible else "deja de sonar creible -> supera"
        print(f'       "{variante}"  --  {estado}')
    print(f"     Resultado: {'SUPERA' if supera_sust else 'NO SUPERA'} la prueba de sustitucion")

    pregunta_d, respuesta_d, supera_d = prueba_decision()
    print(f"\n  b) Prueba de la decision:")
    print(f"     Pregunta: {pregunta_d}")
    print(f"     Respuesta: {respuesta_d}")
    print(f"     Resultado: {'SUPERA' if supera_d else 'NO SUPERA'} la prueba de la decision")

    pregunta_r, respuesta_r, supera_r = prueba_reconocimiento()
    print(f"\n  c) Prueba del reconocimiento:")
    print(f"     Pregunta: {pregunta_r}")
    print(f"     Respuesta: {respuesta_r}")
    print(f"     Resultado: {'SUPERA' if supera_r else 'NO SUPERA'} la prueba del reconocimiento")

    pruebas_superadas = sum([supera_sust, supera_d, supera_r])
    print(f"\n  Pruebas superadas: {pruebas_superadas} / 3")

    veredicto, regla = veredicto_mision(n_presentes, n_defectos > 0, pruebas_superadas)
    print("\n--- VEREDICTO DE LA MISION ---")
    print(f"  {veredicto}  (regla aplicada: {regla})")

    print("\n" + "=" * 78)
    print(f"VISION -- la empresa NO publica una declaracion de vision formal")
    print(f'Declaracion de impacto disponible (sustituta, no es una vision declarada):')
    print(f'  "{DECLARACION_IMPACTO}"')
    print("=" * 78)

    print("\n--- 4. LOS CINCO ATRIBUTOS DE LA VISION (evaluados sobre la declaracion de impacto) ---")
    n_cumple = 0
    for nombre, datos in ATRIBUTOS_VISION.items():
        if datos["cumple"] is True:
            marca = "[X]"
            n_cumple += 1
        elif datos["cumple"] is False:
            marca = "[ ]"
        else:
            marca = "[?]"
        print(f"  {marca} {nombre}: {datos['evidencia']}")
    print(f"\n  Atributos que cumple: {n_cumple} / 5 (mas 1 no evaluable por ausencia de meta)")

    print("\n--- VEREDICTO DE LA VISION ---")
    print("  NO EVALUABLE COMO VISION -- no existe una declaracion de vision publicada.")
    print("  Hallazgo formal: la ausencia de vision publicada es, en si misma, un defecto")
    print("  de gobierno de la identidad estrategica de la empresa.")

    # ------------------------------------------------------------
    # Grafico de resumen
    # ------------------------------------------------------------
    categorias = ["Componentes\npresentes\n(de 5)", "Defectos\nidentificados\n(de 7)",
                  "Pruebas\nsuperadas\n(de 3)", "Atributos de\nvision cumplidos\n(de 5)"]
    valores = [n_presentes, n_defectos, pruebas_superadas, n_cumple]
    maximos = [5, 7, 3, 5]
    colores = ["#2f6f4f" if v > 0 else "#b23b3b" for v in valores]
    colores[1] = "#b23b3b" if n_defectos > 0 else "#2f6f4f"  # mas defectos = peor

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(categorias, valores, color=["#2f6f4f", "#b23b3b", "#b23b3b", "#b23b3b"])
    for i, (v, m) in enumerate(zip(valores, maximos)):
        ax.text(i, v + 0.12, f"{v} / {m}", ha="center", fontweight="bold")
    ax.set_ylim(0, 7.5)
    ax.set_ylabel("Cantidad")
    ax.set_title(f"Diagnostico de declaraciones institucionales -- {EMPRESA}\n"
                 f"Veredicto de la mision: {veredicto}", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("../graficos/S04_diagnostico.png", dpi=150)
    print("\nGrafico guardado en: graficos/S04_diagnostico.png")

    sys.stdout = original_stdout
    archivo.close()
    print(f"Salida completa guardada en UTF-8 en: {salida_path}")


if __name__ == "__main__":
    main()
