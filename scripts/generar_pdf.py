#!/usr/bin/env python3
"""Genera el PDF de reglas de Jenga de Cultura General (máx. 1,5 hojas A4)."""

import json
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "datos" / "juego.json").read_text(encoding="utf-8"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT = ROOT / "Jenga_Cultura_General_Reglas.pdf"


class ReglasPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0, 8,
            f"Jenga de Cultura General — Reglas  ·  Pág. {self.page_no()}",
            align="C",
        )


def section(pdf: FPDF, title: str):
    pdf.set_font("DejaVu", "B", 10.5)
    pdf.set_text_color(120, 70, 10)
    pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)


def mc(pdf: FPDF, text: str, h: float = 4.6):
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, h, text)


def main():
    pdf = ReglasPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_B)
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 9, DATA["nombre"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 5, "Juego escolar · Argentina · 2 a 4 jugadores", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 9.5)
    mc(
        pdf,
        "Reinvención educativa de Jenga: cada bloque tiene un color de materia escolar y una "
        "saturación que indica la dificultad (1 a 3). Sacás un bloque, respondés la pregunta "
        "de esa materia y nivel, sumás puntos y colocás el bloque arriba. Gana quien más puntos "
        "tenga cuando caiga la torre.",
    )
    pdf.ln(1)

    section(pdf, "Materias, colores y dificultad")
    pdf.set_font("DejaVu", "", 8.5)
    mc(
        pdf,
        "El color identifica la materia; la saturación (claro → intenso) indica el nivel. "
        "Nivel 1 = 1 pt · Nivel 2 = 2 pts · Nivel 3 = 3 pts.",
    )
    col_w = [38, 22, 18, 18, 18, 18]
    pdf.set_font("DejaVu", "B", 7.5)
    pdf.set_fill_color(240, 240, 240)
    headers = ["Materia", "Color", "Niv.1", "Niv.2", "Niv.3", "Total"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 5, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("DejaVu", "", 7.5)
    for m in DATA["materias"]:
        b = m["bloques"]
        total = sum(b.values())
        pdf.cell(col_w[0], 5, m["nombre"], border=1)
        pdf.cell(col_w[1], 5, m["color_base"].capitalize(), border=1, align="C")
        pdf.cell(col_w[2], 5, str(b["1"]), border=1, align="C")
        pdf.cell(col_w[3], 5, str(b["2"]), border=1, align="C")
        pdf.cell(col_w[4], 5, str(b["3"]), border=1, align="C")
        pdf.cell(col_w[5], 5, str(total), border=1, align="C")
        pdf.ln()
    mc(pdf, "Total: 40 bloques + 1 base (3D) · 60 cartas en papel (4 por materia y nivel) · 1 hoja de puntaje.")
    pdf.ln(0.5)

    section(pdf, "Reglas y puntos")
    pdf.set_font("DejaVu", "", 9)
    mc(
        pdf,
        "• Respuesta correcta: sumás 1, 2 o 3 puntos según el nivel.\n"
        "• Respuesta incorrecta: 0 puntos (igual colocás el bloque).\n"
        "• Torre cae: quien la tiró pierde TODOS sus puntos.\n"
        "• Fin: cuando cae la torre; gana quien más puntos tenga.",
    )
    pdf.ln(0.5)

    section(pdf, "Turno (en orden)")
    for i, step in enumerate([
        "Elegí qué bloque sacar (como Jenga).",
        "Identificá materia (color) y nivel (saturación del color).",
        "Robá 1 carta del mazo de esa materia y nivel.",
        "Respondé antes de colocar el bloque (la lee otro jugador).",
        "Colocás el bloque arriba. Siguiente jugador, sentido horario.",
    ], 1):
        mc(pdf, f"{i}. {step}", 4.4)
    pdf.ln(0.5)

    section(pdf, "Estrategia e impresión 3D")
    pdf.set_font("DejaVu", "", 8.5)
    mc(
        pdf,
        "Podés elegir bloques de materias que dominés o niveles bajos (color claro) para ir seguro, "
        "o arriesgar niveles altos (color intenso) por más puntos con más tensión física.\n\n"
        "Imprimí cada bloque con el color y saturación indicados en datos/juego.json. "
        "Modelo paramétrico en 3d/bloque.scad. Base con el nombre del juego en 3d/base.scad.",
    )
    pdf.ln(0.5)

    section(pdf, "Ejemplos de preguntas (Argentina)")
    pdf.set_font("DejaVu", "", 8)
    ejemplos = []
    for m in DATA["materias"]:
        mid = m["id"]
        for nivel in ("1", "2", "3"):
            card = DATA["preguntas"][mid][nivel][0]
            ejemplos.append(f"{m['nombre']} n{nivel}: {card['q']}")
    mc(pdf, " · ".join(ejemplos[:4]) + "\n" + " · ".join(ejemplos[4:8]))

    pdf.output(str(OUTPUT))
    pages = pdf.page_no()
    print(f"PDF generado: {OUTPUT} ({pages} página(s))")
    if pages > 1.5:
        print("AVISO: supera 1,5 hojas — compactar si hace falta.")


if __name__ == "__main__":
    main()
