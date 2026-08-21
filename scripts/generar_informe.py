#!/usr/bin/env python3
"""Genera el informe escolar en PDF (máx. 1,5 hojas A4)."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "informe" / "INFORME.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class InformePDF(FPDF):
    def setup(self):
        self.add_font("DejaVu", "", FONT)
        self.add_font("DejaVu", "B", FONT_B)
        self.set_auto_page_break(auto=True, margin=12)

    def titulo(self, text: str, size: float = 11):
        self.set_font("DejaVu", "B", size)
        self.set_text_color(100, 60, 10)
        self.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(30, 30, 30)

    def texto(self, text: str, size: float = 9):
        self.set_font("DejaVu", "", size)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, 4.5, text)
        self.ln(1)


def main():
    pdf = InformePDF("P", "mm", "A4")
    pdf.setup()
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 17)
    pdf.cell(0, 9, "Informe — Jenga de Cultura General", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 5, "Proyecto escolar · Argentina · Secundaria · 2 a 4 jugadores", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.ln(2)

    pdf.titulo("1. Introducción", 10)
    pdf.texto(
        "Este trabajo propone una reinvención del juego Jenga integrando preguntas de "
        "cultura general de materias de secundaria y un sistema de puntos. La impresión 3D "
        "tiene función educativa: cada bloque indica materia (color) y dificultad (saturación)."
    )

    pdf.titulo("2. Juego original vs. reinvención", 10)
    cols = [42, 58, 58]
    pdf.set_font("DejaVu", "B", 7.5)
    pdf.set_fill_color(240, 240, 240)
    for h, w in [("Aspecto", cols[0]), ("Jenga original", cols[1]), ("Jenga de Cultura General", cols[2])]:
        pdf.cell(w, 5.5, h, border=1, fill=True, align="C")
    pdf.ln()
    rows = [
        ("Objetivo", "No tirar la torre", "Sumar más puntos"),
        ("Bloques", "Todos iguales", "5 materias × 3 niveles"),
        ("Contenido", "Ninguno", "Preguntas escolares"),
        ("Habilidades", "Destreza manual", "Destreza + conocimiento + estrategia"),
    ]
    pdf.set_font("DejaVu", "", 7.5)
    for row in rows:
        pdf.cell(cols[0], 5.5, row[0], border=1)
        pdf.cell(cols[1], 5.5, row[1], border=1)
        pdf.cell(cols[2], 5.5, row[2], border=1)
        pdf.ln()
    pdf.ln(1)

    pdf.titulo("3. Innovación", 10)
    pdf.texto(
        "El jugador elige qué bloque sacar, combinando tres decisiones: materia (color del bloque), "
        "dificultad (saturación = nivel 1, 2 o 3) y riesgo físico (bloques arriba son más inestables). "
        "No es solo copiar Jenga ni solo trivia: hay que pensar el juego."
    )

    pdf.titulo("4. Componentes y puntos", 10)
    pdf.texto(
        "40 bloques 3D + 1 base · 60 cartas PDF · Reglas y sistema de puntajes en PDF. "
        "Puntos: nivel 1 = 1 pt, nivel 2 = 2 pts, nivel 3 = 3 pts. Respuesta incorrecta: 0. "
        "Si cae la torre, quien la tiró pierde todos sus puntos."
    )

    pdf.titulo("5. Cartas e impresión 3D", 10)
    pdf.texto(
        "Las cartas tienen marco tipo naipe. En el frente: pregunta grande y respuesta en chico "
        "centrada abajo (la ve quien lee la carta). El dorso es decorativo. "
        "Bloques: modelos en 3d/bloque.scad; colores en datos/Materias_y_Bloques.pdf."
    )

    pdf.titulo("6. Prueba de juego (completar en clase)", 10)
    pdf.set_font("DejaVu", "", 8.5)
    campos = [
        "Fecha: _______________________",
        "Jugadores (2-4): _________________________________________________",
        "Duración aproximada: _____________",
        "¿Se entendieron colores y niveles?  Sí / No / Más o menos",
        "¿Funcionó el sistema de puntos?     Sí / No / Más o menos",
        "¿La torre se sintió inestable a tiempo?  Sí / No",
        "Ganador: _______________________",
        "Puntajes finales: J1 _____  J2 _____  J3 _____  J4 _____",
        "Observaciones: ________________________________________________",
    ]
    for c in campos:
        pdf.cell(0, 5.5, c, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.titulo("7. Conclusión", 10)
    pdf.texto(
        "Jenga de Cultura General une equilibrio físico, contenidos de secundaria argentina "
        "y decisiones estratégicas. Cumple la consigna de impresión 3D con bloques "
        "funcionales y material de juego listo para imprimir."
    )

    pdf.output(str(OUTPUT))
    pages = pdf.page_no()
    print(f"Informe generado: {OUTPUT} ({pages} página(s))")
    if pages > 2:
        print("AVISO: supera 1,5 hojas.")


if __name__ == "__main__":
    main()
