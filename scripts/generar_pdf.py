#!/usr/bin/env python3
"""Genera el PDF de reglas de Torre Sabia (máx. 1,5 hojas A4)."""

from fpdf import FPDF

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT = "/workspace/Torre_Sabia_Reglas.pdf"


class ReglasPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Torre Sabia — Reglas del juego  ·  Pág. {self.page_no()}", align="C")


def main():
    pdf = ReglasPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_B)
    pdf.add_page()

    # Título
    pdf.set_font("DejaVu", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Torre Sabia", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, "Conocimiento en equilibrio", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    body = 10
    pdf.set_font("DejaVu", "", body)
    pdf.set_text_color(30, 30, 30)

    pdf.multi_cell(
        0,
        5,
        "Torre Sabia es una reinvención educativa de Jenga: cada bloque indica la dificultad de una "
        "pregunta de cultura general. Sacás un bloque, respondés antes de colocarlo arriba y sumás puntos. "
        "Gana quien más puntos tenga cuando caiga la torre.",
    )
    pdf.ln(2)

    section(pdf, "Componentes")
    pdf.set_font("DejaVu", "", 9.5)
    rows = [
        ("Bloques fáciles (1 rayita)", "14", "Impresión 3D"),
        ("Bloques medios (2 rayitas)", "14", "Impresión 3D"),
        ("Bloques difíciles (3 rayitas)", "12", "Impresión 3D"),
        ("Base", "1", "Impresión 3D"),
        ("Mazo Fácil / Medio / Difícil", "20 c/u", "Cartas en papel"),
        ("Hoja de puntaje", "1", "Papel"),
    ]
    col_w = [75, 18, 35]
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("DejaVu", "B", 9)
    pdf.cell(col_w[0], 6, "Pieza", border=1, fill=True)
    pdf.cell(col_w[1], 6, "Cant.", border=1, fill=True, align="C")
    pdf.cell(col_w[2], 6, "Material", border=1, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 9)
    for row in rows:
        pdf.cell(col_w[0], 5.5, row[0], border=1)
        pdf.cell(col_w[1], 5.5, row[1], border=1, align="C")
        pdf.cell(col_w[2], 5.5, row[2], border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    section(pdf, "Sistema de puntos")
    pdf.set_font("DejaVu", "", 9.5)
    pdf.multi_cell(
        0,
        5,
        "Fácil = 1 pt  ·  Medio = 2 pts  ·  Difícil = 3 pts\n"
        "Respuesta incorrecta: 0 puntos (igual colocás el bloque).\n"
        "Si la torre cae: quien la tiró pierde 5 puntos.",
    )
    pdf.ln(1)

    section(pdf, "Mecánica de un turno")
    steps = [
        "Elegí qué bloque sacar (como en Jenga).",
        "Mirá su dificultad (color o marcas en relieve).",
        "Robá 1 carta del mazo correspondiente.",
        "Respondé la pregunta (la lee otro jugador) antes de colocar el bloque.",
        "Acertás → sumás puntos. Fallás → 0 puntos.",
        "Colocás el bloque arriba de la torre.",
        "Siguiente jugador, sentido horario.",
    ]
    pdf.set_font("DejaVu", "", 9.5)
    x0 = pdf.l_margin
    w = pdf.epw
    for i, step in enumerate(steps, 1):
        pdf.set_x(x0)
        pdf.multi_cell(w, 5, f"{i}. {step}")

    pdf.ln(1)
    section(pdf, "Fin de la partida y estrategia")
    pdf.set_font("DejaVu", "", 9.5)
    pdf.multi_cell(
        0,
        5,
        "Se juega hasta que cae la torre. Se suman los puntos finales; quien la tiró resta 5. "
        "Gana quien más puntos tenga.\n\n"
        "La estrategia une riesgo físico e intelectual: un bloque fácil abajo da pregunta fácil y poco "
        "riesgo (1 pt); un bloque difícil arriba puede dar 3 pts pero aumenta la chance de que se caiga.",
    )
    pdf.ln(1)

    section(pdf, "Impresión 3D y ejemplos de preguntas")
    pdf.set_font("DejaVu", "", 9.5)
    pdf.multi_cell(
        0,
        5,
        "Los bloques se diferencian por líneas en relieve (1, 2 o 3). La base puede llevar el nombre "
        "«Torre Sabia» o un diseño de torre de libros. Modelos en la carpeta 3d/.\n\n"
        "Fácil: ¿Cuál es la capital de Argentina?  ·  Medio: ¿En qué año llegó el hombre a la Luna?  ·  "
        "Difícil: ¿Cuál es la capital de Australia?",
    )

    pdf.output(OUTPUT)
    print(f"PDF generado: {OUTPUT} ({pdf.page_no()} página(s))")


def section(pdf: FPDF, title: str):
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(140, 100, 20)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)


if __name__ == "__main__":
    main()
