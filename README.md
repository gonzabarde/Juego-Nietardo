# Jenga de Cultura General

Proyecto escolar en PDF — Jenga + materias de secundaria + puntos por dificultad.

## Archivos principales

| Archivo | Contenido |
|---------|-----------|
| `Jenga_Cultura_General_Reglas.pdf` | Reglas del juego |
| `preguntas/SISTEMA_PUNTOS.pdf` | Explicación del sistema de puntajes |
| `datos/Materias_y_Bloques.pdf` | Colores, materias y bloques 3D |
| `informe/INFORME.pdf` | Informe escolar para entregar |
| `3d/Jenga de Cultura General.stl` | Modelo imprimible (Fusion 360) |
| `preguntas/<materia>/nivel-<1|2|3>/cartas.pdf` | Cartas imprimibles |

## Cartas

Cada `cartas.pdf` tiene **2 páginas** (frente + dorso decorativo). En el frente: pregunta grande y respuesta en chico abajo. Imprimir a doble cara y recortar.

## Carpetas

- `preguntas/` — cartas por materia y nivel
- `datos/` — materias y bloques (PDF)
- `3d/` — modelos OpenSCAD, STL e instrucciones Fusion
- `informe/` — informe escolar (`INFORME.pdf`)

## Regenerar PDFs

```bash
python3 scripts/generar_informe.py
python3 scripts/generar_cartas.py
python3 scripts/generar_pdf.py
```
