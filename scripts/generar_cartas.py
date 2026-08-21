#!/usr/bin/env python3
"""Genera todos los PDFs del proyecto (reglas, cartas, puntos, materias)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
spec = importlib.util.spec_from_file_location("datos_embebidos", SCRIPTS / "datos_embebidos.py")
_datos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_datos)
MATERIAS = _datos.MATERIAS
MAZOS = _datos.MAZOS
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_I = FONT  # DejaVu Sans Oblique no disponible en este sistema

CARD_W = 63
CARD_H = 88
CARD_R = 4  # esquinas redondeadas


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def load_materias() -> list[dict]:
    return MATERIAS


def load_mazo(materia_id: str, nivel: int) -> dict:
    return MAZOS[f"{materia_id}/{nivel}"]


class BasePDF(FPDF):
    def setup_fonts(self):
        self.add_font("DejaVu", "", FONT)
        self.add_font("DejaVu", "B", FONT_B)
        self.add_font("DejaVu", "I", FONT)


def card_positions() -> list[tuple[float, float]]:
    gap_x = 10
    gap_y = 12
    total_w = CARD_W * 2 + gap_x
    total_h = CARD_H * 2 + gap_y
    ox = (210 - total_w) / 2
    oy = (297 - total_h) / 2
    return [
        (ox, oy),
        (ox + CARD_W + gap_x, oy),
        (ox, oy + CARD_H + gap_y),
        (ox + CARD_W + gap_x, oy + CARD_H + gap_y),
    ]


def draw_card_frame(pdf: FPDF, x: float, y: float, rgb: tuple[int, int, int], label: str, numero: int):
    """Marco tipo carta: doble borde, esquinas redondeadas y adornos en las puntas."""
    # Sombra
    pdf.set_fill_color(220, 220, 220)
    pdf.rect(x + 1.2, y + 1.2, CARD_W, CARD_H, style="F")

    # Fondo blanco interior
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*rgb)
    pdf.set_line_width(0.8)
    pdf.rect(x, y, CARD_W, CARD_H, style="FD")

    # Borde interior (marco característico)
    pdf.set_line_width(0.35)
    pdf.set_draw_color(max(0, rgb[0] - 30), max(0, rgb[1] - 30), max(0, rgb[2] - 30))
    pdf.rect(x + 2.5, y + 2.5, CARD_W - 5, CARD_H - 5)

    # Líneas decorativas en esquinas (estilo carta)
    for dx, dy in [(4, 4), (CARD_W - 4, 4), (4, CARD_H - 4), (CARD_W - 4, CARD_H - 4)]:
        pdf.set_draw_color(*rgb)
        pdf.line(x + dx - 2, y + dy, x + dx + 2, y + dy)
        pdf.line(x + dx, y + dy - 2, x + dx, y + dy + 2)

    # Banda superior de color
    pdf.set_fill_color(*rgb)
    pdf.rect(x + 3, y + 3, CARD_W - 6, 11, style="F")

    # Inicial en esquinas (como naipe)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_xy(x + 5, y + 5)
    pdf.cell(8, 6, label, align="C")
    pdf.set_xy(x + CARD_W - 13, y + CARD_H - 11)
    pdf.cell(8, 6, str(numero), align="C")


def draw_card_front(pdf: FPDF, x: float, y: float, carta: dict, mazo: dict, rgb: tuple[int, int, int], label: str):
    draw_card_frame(pdf, x, y, rgb, label, carta["id"])

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 6.5)
    pdf.set_xy(x + 14, y + 5)
    pdf.cell(CARD_W - 28, 6, mazo["materia"][:22], align="C")

    pdf.set_text_color(40, 40, 40)
    pdf.set_font("DejaVu", "B", 7)
    pdf.set_xy(x + 6, y + 18)
    pdf.cell(CARD_W - 12, 5, f"Nivel {mazo['nivel']} · {mazo['puntos']} pt{'s' if mazo['puntos'] > 1 else ''}", align="C")

    # Área central con marco ovalado implícito
    pdf.set_draw_color(*rgb)
    pdf.set_line_width(0.25)
    pdf.rect(x + 8, y + 28, CARD_W - 16, CARD_H - 42)

    pdf.set_font("DejaVu", "", 8.2)
    pdf.set_xy(x + 10, y + 32)
    pdf.multi_cell(CARD_W - 20, 4.2, carta["pregunta"], align="C")

    pdf.set_font("DejaVu", "I", 6)
    pdf.set_text_color(120, 120, 120)
    pdf.set_xy(x + 6, y + CARD_H - 9)
    pdf.cell(CARD_W - 12, 4, "Jenga de Cultura General", align="C")


def draw_card_back(pdf: FPDF, x: float, y: float, carta: dict, mazo: dict, rgb: tuple[int, int, int], label: str):
    draw_card_frame(pdf, x, y, rgb, label, carta["id"])

    pdf.set_fill_color(min(255, rgb[0] + 180), min(255, rgb[1] + 180), min(255, rgb[2] + 180))
    pdf.rect(x + 8, y + 18, CARD_W - 16, CARD_H - 32, style="F")

    pdf.set_text_color(*rgb)
    pdf.set_font("DejaVu", "B", 8)
    pdf.set_xy(x + 8, y + 22)
    pdf.cell(CARD_W - 16, 5, "RESPUESTA", align="C")

    pdf.set_text_color(30, 30, 30)
    pdf.set_font("DejaVu", "", 8)
    pdf.set_xy(x + 10, y + 30)
    pdf.multi_cell(CARD_W - 20, 4.2, carta["respuesta"], align="C")

    pdf.set_font("DejaVu", "I", 6)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(x + 6, y + CARD_H - 9)
    pdf.cell(CARD_W - 12, 4, f"{mazo['materia']} · N{mazo['nivel']}", align="C")


def materia_label(materia_id: str) -> str:
    return {
        "historia": "H",
        "geografia": "G",
        "ciencias": "C",
        "lengua": "L",
        "civica": "E",
    }[materia_id]


def generar_mazo_pdf(materia: dict, nivel: int):
    mazo = load_mazo(materia["id"], nivel)
    rgb = hex_rgb(materia["hex_niveles"][nivel - 1])
    label = materia_label(materia["id"])

    out_dir = ROOT / "preguntas" / materia["id"] / f"nivel-{nivel}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "cartas.pdf"

    pdf = BasePDF("P", "mm", "A4")
    pdf.setup_fonts()
    pdf.set_auto_page_break(False)

    positions = card_positions()
    # Página frentes
    pdf.add_page()
    for carta, (px, py) in zip(mazo["cartas"], positions):
        draw_card_front(pdf, px, py, carta, mazo, rgb, label)

    # Página dorso (orden espejado para impresión a doble cara)
    pdf.add_page()
    mirror = [positions[1], positions[0], positions[3], positions[2]]
    for carta, (px, py) in zip(mazo["cartas"], mirror):
        draw_card_back(pdf, px, py, carta, mazo, rgb, label)

    pdf.output(str(out_path))
    return out_path


def generar_sistema_puntos_pdf():
    out = ROOT / "preguntas" / "SISTEMA_PUNTOS.pdf"
    pdf = BasePDF("P", "mm", "A4")
    pdf.setup_fonts()
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 12, "Sistema de puntos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 8, "Jenga de Cultura General", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    rows = [
        ("1", "Clara (color pálido)", "1 punto"),
        ("2", "Media", "2 puntos"),
        ("3", "Intensa (color oscuro)", "3 puntos"),
    ]
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    for h, w in [("Nivel", 25), ("Saturación del bloque", 90), ("Puntos si acertás", 55)]:
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("DejaVu", "", 10)
    for row in rows:
        pdf.cell(25, 8, row[0], border=1, align="C")
        pdf.cell(90, 8, row[1], border=1)
        pdf.cell(55, 8, row[2], border=1, align="C")
        pdf.ln()

    pdf.ln(8)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, "Reglas adicionales", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 10)
    for line in [
        "• Respuesta incorrecta: 0 puntos (igual colocás el bloque).",
        "• Torre cae: quien la tiró pierde TODOS sus puntos.",
        "• Jugadores: de 2 a 4.",
        "• Gana quien más puntos tenga al final de la partida.",
    ]:
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out))
    return out


def generar_materias_pdf(materias: list[dict]):
    out = ROOT / "datos" / "Materias_y_Bloques.pdf"
    pdf = BasePDF("P", "mm", "A4")
    pdf.setup_fonts()
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 12, "Materias y bloques 3D", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("DejaVu", "B", 9)
    cols = [40, 22, 18, 18, 18, 18, 28]
    headers = ["Materia", "Color", "Niv.1", "Niv.2", "Niv.3", "Total", "Hex niveles"]
    for h, w in zip(headers, cols):
        pdf.cell(w, 7, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("DejaVu", "", 8)
    for m in materias:
        b = m["bloques"]
        total = sum(b.values())
        pdf.cell(cols[0], 7, m["nombre"], border=1)
        pdf.cell(cols[1], 7, m["color_base"], border=1, align="C")
        pdf.cell(cols[2], 7, str(b["1"]), border=1, align="C")
        pdf.cell(cols[3], 7, str(b["2"]), border=1, align="C")
        pdf.cell(cols[4], 7, str(b["3"]), border=1, align="C")
        pdf.cell(cols[5], 7, str(total), border=1, align="C")
        pdf.cell(cols[6], 7, " / ".join(m["hex_niveles"]), border=1)
        pdf.ln()

    pdf.ln(6)
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(
        0, 5,
        "Total: 40 bloques + 1 base. Cada materia usa su color con 3 niveles de saturación "
        "para indicar la dificultad de la pregunta. Modelos en carpeta 3d/.",
    )
    pdf.output(str(out))
    return out


def generar_reglas_pdf():
    import importlib.util
    spec = importlib.util.spec_from_file_location("generar_pdf", ROOT / "scripts" / "generar_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


def eliminar_json():
    for p in ROOT.rglob("*.json"):
        if ".git" not in p.parts and "scripts" not in p.parts:
            p.unlink()
            print("Eliminado:", p.relative_to(ROOT))


def main():
    materias = load_materias()
    print("Generando cartas PDF...")
    for m in materias:
        for nivel in (1, 2, 3):
            path = generar_mazo_pdf(m, nivel)
            print(" ", path.relative_to(ROOT))

    print("Generando SISTEMA_PUNTOS.pdf...")
    generar_sistema_puntos_pdf()

    print("Generando Materias_y_Bloques.pdf...")
    generar_materias_pdf(materias)

    print("Generando reglas...")
    generar_reglas_pdf()

    print("Eliminando archivos JSON...")
    eliminar_json()

    readme = ROOT / "preguntas" / "README.md"
    if readme.exists():
        readme.unlink()

    print("Listo.")


if __name__ == "__main__":
    main()
