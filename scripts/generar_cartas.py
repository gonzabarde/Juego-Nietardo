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

CARD_W = 72
CARD_H = 100
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
    gap_x = 8
    gap_y = 10
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


def scale_w(value: float) -> float:
    return value * (CARD_W / 63)


def scale_h(value: float) -> float:
    return value * (CARD_H / 88)


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
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_xy(x + 5, y + 5)
    pdf.cell(8, 6, label, align="C")
    pdf.set_xy(x + CARD_W - 13, y + CARD_H - scale_h(11))
    pdf.cell(8, 6, str(numero), align="C")


def draw_card_front(pdf: FPDF, x: float, y: float, carta: dict, mazo: dict, rgb: tuple[int, int, int], label: str):
    draw_card_frame(pdf, x, y, rgb, label, carta["id"])

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("DejaVu", "B", 7.5)
    pdf.set_xy(x + 14, y + 5)
    pdf.cell(CARD_W - 28, 6, mazo["materia"][:22], align="C")

    pdf.set_text_color(40, 40, 40)
    pdf.set_font("DejaVu", "B", 8)
    pdf.set_xy(x + 6, y + scale_h(18))
    pdf.cell(CARD_W - 12, 5, f"Nivel {mazo['nivel']} · {mazo['puntos']} pt{'s' if mazo['puntos'] > 1 else ''}", align="C")

    pdf.set_draw_color(*rgb)
    pdf.set_line_width(0.25)
    pdf.rect(x + 8, y + scale_h(28), CARD_W - 16, CARD_H - scale_h(42))

    pdf.set_font("DejaVu", "", 9.5)
    pdf.set_xy(x + 10, y + scale_h(32))
    pdf.multi_cell(CARD_W - 20, 4.8, carta["pregunta"], align="C")

    pdf.set_draw_color(*rgb)
    pdf.set_line_width(0.2)
    pdf.line(x + 10, y + CARD_H - scale_h(17), x + CARD_W - 10, y + CARD_H - scale_h(17))

    pdf.set_font("DejaVu", "", 6)
    pdf.set_text_color(70, 70, 70)
    pdf.set_xy(x + 6, y + CARD_H - scale_h(15))
    pdf.multi_cell(CARD_W - 12, 3, carta["respuesta"], align="C")


def draw_card_back(pdf: FPDF, x: float, y: float, carta: dict, mazo: dict, rgb: tuple[int, int, int], label: str):
    draw_card_frame(pdf, x, y, rgb, label, carta["id"])

    # Dorso decorativo (la respuesta va en chico abajo del frente)
    pdf.set_fill_color(min(255, rgb[0] + 190), min(255, rgb[1] + 190), min(255, rgb[2] + 190))
    pdf.rect(x + 8, y + scale_h(18), CARD_W - 16, CARD_H - scale_h(32), style="F")

    pdf.set_draw_color(*rgb)
    pdf.set_line_width(0.2)
    cx, cy = x + CARD_W / 2, y + CARD_H / 2 - 2
    r = scale_w(14)
    for i in range(-2, 3):
        pdf.line(cx - r, cy + i * 5, cx + r, cy + i * 5)
        pdf.line(cx + i * 5, cy - r, cx + i * 5, cy + r)

    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(*rgb)
    pdf.set_xy(x + 6, y + CARD_H / 2 - 6)
    pdf.cell(CARD_W - 12, 8, label, align="C")


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
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def titulo(text: str, size: float = 16):
        pdf.set_font("DejaVu", "B", size)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")

    def parrafo(text: str, size: float = 10.5):
        pdf.set_font("DejaVu", "", size)
        pdf.set_text_color(45, 45, 45)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 5.5, text)
        pdf.ln(2)

    titulo("Sistema de puntajes", 20)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Jenga de Cultura General · Explicación", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    parrafo(
        "En este juego no alcanza con no tirar la torre: también sumás puntos respondiendo "
        "preguntas de cultura general. Cuanto más difícil el bloque que saques, más puntos "
        "podés ganar… pero también más riesgo de que se caiga la torre."
    )

    titulo("¿Cómo sé cuántos puntos vale un bloque?", 13)
    parrafo(
        "Cada bloque tiene un color de materia (Historia, Geografía, Ciencias, Lengua o "
        "Educación Cívica) y una saturación del color que indica la dificultad:"
    )

    rows = [
        ("Nivel 1", "Color claro / pálido", "Pregunta fácil", "1 punto"),
        ("Nivel 2", "Color medio", "Pregunta media", "2 puntos"),
        ("Nivel 3", "Color intenso / oscuro", "Pregunta difícil", "3 puntos"),
    ]
    pdf.set_font("DejaVu", "B", 9)
    pdf.set_fill_color(245, 240, 230)
    col_w = [22, 42, 52, 28]
    for h, w in zip(["Nivel", "Saturación", "Pregunta", "Puntos"], col_w):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("DejaVu", "", 9)
    for row in rows:
        for val, w in zip(row, col_w):
            pdf.cell(w, 8, val, border=1, align="C" if w < 40 else "L")
        pdf.ln()
    pdf.ln(3)

    titulo("¿Cómo se suman puntos en un turno?", 13)
    parrafo(
        "1. Sacás un bloque y mirás su materia y nivel.\n"
        "2. Robás una carta de ese mazo.\n"
        "3. Si respondés bien → sumás 1, 2 o 3 puntos según el nivel.\n"
        "4. Si respondés mal → no sumás nada (0 puntos), pero igual colocás el bloque arriba.\n"
        "5. Anotás el puntaje y pasa el turno al siguiente jugador."
    )

    titulo("Ejemplo de partida", 13)
    parrafo(
        "Lucas saca un bloque verde claro de Geografía (nivel 1), responde bien → +1 punto.\n"
        "María saca un bloque rojo intenso de Historia (nivel 3), responde bien → +3 puntos.\n"
        "Tomás saca un bloque azul medio de Ciencias (nivel 2), falla → 0 puntos.\n"
        "Al final de varios turnos: Lucas 5 pts, María 8 pts, Tomás 3 pts."
    )

    titulo("Penalización: la torre cae", 13)
    parrafo(
        "La partida termina cuando la torre se cae. El jugador que la tiró pierde "
        "TODOS sus puntos acumulados, no solo una parte. Por ejemplo: si María tenía 8 puntos "
        "y tira la torre, queda en 0. Los demás conservan sus puntos."
    )

    titulo("¿Quién gana?", 13)
    parrafo(
        "Gana quien tenga más puntos después de la caída de la torre. "
        "Pueden jugar de 2 a 4 jugadores. "
        "Conviene anotar los puntos turno a turno en una hoja aparte."
    )

    pdf.set_font("DejaVu", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(
        pdf.epw, 5,
        "Tip estratégico: podés elegir bloques fáciles y seguros para sumar de a poco, "
        "o arriesgar bloques difíciles arriba de la torre para sumar más rápido.",
    )

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
