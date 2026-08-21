# AGENTS.md

## Cursor Cloud specific instructions

This repository is the **asset/source repository for a physical board game** ("Jenga de Cultura General"), not a deployable web app. There are **no long-running services** (no backend, frontend, database, or dev server) to start.

### What "running the app" means here

The only executable code is the rules-PDF generator. Regenerating the PDF is the end-to-end flow:

```bash
python3 scripts/generar_pdf.py
```

It reads `datos/juego.json`, `preguntas/SISTEMA_PUNTOS.json`, and every `preguntas/<materia>/nivel-<1|2|3>/cartas.json`, then writes `Jenga_Cultura_General_Reglas.pdf` at the repo root (overwriting the committed copy). Success prints `PDF generado: ... (N página(s))`.

### Non-obvious notes

- The generator hard-codes the DejaVu font paths `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` (and `-Bold`). These fonts are preinstalled on the base image; if a future image lacks them, install `fonts-dejavu-core`.
- The only Python dependency is `fpdf2` (installed by the update script; also pinned in `requirements.txt`).
- There is **no test suite and no configured linter**. For a lightweight sanity check use `python3 -m py_compile scripts/generar_pdf.py` and validate the JSON decks by loading them with `json.load`.
- `3d/bloque.scad` and `3d/base.scad` are OpenSCAD models for 3D-printing the blocks/base. OpenSCAD is **not** installed and is not part of any automated flow — only needed if you intend to render/export STLs.
