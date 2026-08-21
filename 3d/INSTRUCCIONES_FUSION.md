# Instrucciones para Fusion 360 — Colores y letras de bloques

Usá este documento como prompt para Claude (o seguí los pasos manualmente).

---

## Prompt para Claude en Fusion

```
Tengo prismas rectangulares tipo Jenga (75 × 25 × 15 mm) en Fusion 360.
Necesito que a cada bloque le asignes:

1. COLOR con saturación según materia y dificultad (ver tabla abajo).
2. LETRA de la materia en las DOS caras más chicas del prisma (25 × 15 mm).
   Esas son las caras de los extremos cortos (no las de 75 × 25 ni las de 75 × 15).

Letras por materia:
- Historia → H
- Geografía → G
- Ciencias Naturales → C
- Lengua y Literatura → L
- Educación Cívica → E

La letra va en relieve o grabada, centrada, en AMBAS caras chicas (simétrico).

Además, en la cara superior grande (75 × 25) van rayitas en relieve:
- Nivel 1 → 1 rayita
- Nivel 2 → 2 rayitas
- Nivel 3 → 3 rayitas

---

TABLA COMPLETA — 40 BLOQUES

| # | Materia            | Letra | Nivel | Puntos | Color HEX | Cantidad |
|---|--------------------|-------|-------|--------|-----------|----------|
| 1 | Historia           | H     | 1     | 1      | #FFCCCC   | 3        |
| 2 | Historia           | H     | 2     | 2      | #FF5555   | 3        |
| 3 | Historia           | H     | 3     | 3      | #AA0000   | 2        |
| 4 | Geografía          | G     | 1     | 1      | #CCFFCC   | 3        |
| 5 | Geografía          | G     | 2     | 2      | #44BB44   | 3        |
| 6 | Geografía          | G     | 3     | 3      | #006600   | 2        |
| 7 | Ciencias Naturales | C     | 1     | 1      | #CCE5FF   | 3        |
| 8 | Ciencias Naturales | C     | 2     | 2      | #4499DD   | 3        |
| 9 | Ciencias Naturales | C     | 3     | 3      | #004488   | 2        |
|10 | Lengua y Literatura| L     | 1     | 1      | #E8CCFF   | 3        |
|11 | Lengua y Literatura| L     | 2     | 2      | #9955CC   | 3        |
|12 | Lengua y Literatura| L     | 3     | 3      | #551188   | 2        |
|13 | Educación Cívica   | E     | 1     | 1      | #FFE5CC   | 3        |
|14 | Educación Cívica   | E     | 2     | 2      | #FF8833   | 3        |
|15 | Educación Cívica   | E     | 3     | 3      | #BB4400   | 2        |

TOTAL: 40 bloques (8 por materia).

---

CÓMO APLICAR EN FUSION 360

Colores:
- Seleccionar cuerpo → Appearance → Physical Material o Appearance
- New → pegar HEX de la tabla
- Aplicar a los bloques según cantidad de la tabla

Letra en caras chicas (25 × 15):
- Crear Sketch sobre cada cara pequeña del extremo
- Text (T) → escribir H/G/C/L/E → centrar
- Extrude → Cut o New Body en relieve 0.5–1 mm
- Repetir en la cara opuesta (misma letra)

Rayitas en cara grande (75 × 25):
- Sketch líneas paralelas al borde largo
- Extrude cut 1–1.5 mm de profundidad
- 1, 2 o 3 líneas según nivel

Organización:
- Renombrar componentes: ej. "Historia_N1_01", "Geografia_N2_02"
- Agrupar por materia en el browser

Si tengo menos de 40 bloques, duplicar según la columna Cantidad hasta completar 40.
```

---

## Guía visual rápida

```
        ┌──────────────── 75 mm ────────────────┐
        │         cara grande (75×25)          │  ← rayitas (1/2/3)
   15mm │                                      │ 15mm
        │         cara grande opuesta          │
        └──────────────────────────────────────┘
       25mm                                    25mm
        ↑                                        ↑
   cara chica                                 cara chica
   (25×15) LETRA                              (25×15) LETRA
      H/G/C/L/E                                  H/G/C/L/E
```

---

## Resumen para no confundirse

- **5 materias** → 5 letras (H, G, C, L, E)
- **3 saturaciones por materia** → 3 tonos del mismo color
- **15 tipos de bloque** distintos (materia + nivel)
- **40 bloques** en total + 1 base

Referencia: `datos/Materias_y_Bloques.pdf`
