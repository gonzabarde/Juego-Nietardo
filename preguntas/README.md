# Carpeta de preguntas

Estructura de cartas para **Jenga de Cultura General**.

```
preguntas/
├── SISTEMA_PUNTOS.json      ← puntos y reglas de puntuación
├── historia/
│   ├── nivel-1/cartas.json  ← 1 punto
│   ├── nivel-2/cartas.json  ← 2 puntos
│   └── nivel-3/cartas.json  ← 3 puntos
├── geografia/
├── ciencias/
├── lengua/
└── civica/
```

## Sistema de puntos

| Nivel | Saturación del color | Puntos si acertás |
|-------|----------------------|-------------------|
| 1 | Clara (pálida) | **1** |
| 2 | Media | **2** |
| 3 | Intensa (oscura) | **3** |

- Respuesta incorrecta: **0 puntos** (igual colocás el bloque).
- Torre cae: quien la tiró **pierde todos sus puntos**.

Detalle completo en `SISTEMA_PUNTOS.json`.

## Formato de cada cartas.json

```json
{
  "materia_id": "historia",
  "materia": "Historia",
  "nivel": 1,
  "puntos": 1,
  "cartas": [
    { "id": 1, "pregunta": "...", "respuesta": "..." }
  ]
}
```

Cada mazo tiene **4 cartas**. Total: **60 cartas** (5 materias × 3 niveles × 4 cartas).
