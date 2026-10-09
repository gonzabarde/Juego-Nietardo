# Jenga de Cultura General

Reinvención escolar del Jenga para Argentina: bloques impresos en 3D con un color por materia y un nivel de dificultad grabado, cartas de preguntas y un sistema de puntos. De 2 a 4 jugadores, 20 a 30 minutos.

**45 bloques · 15 pisos · 60 cartas · 5 materias × 3 niveles**

---

## Cómo se juega

1. Armá la torre sobre la base: 15 pisos de 3 bloques, cada piso girado 90° respecto del anterior.
2. En tu turno, sacá un bloque con una sola mano.
3. Mirá qué te tocó: el **color** dice la materia y las **ranuras** dicen el nivel.
4. El jugador de tu izquierda saca una carta de ese mazo y te lee la pregunta.
5. Respondé antes de apoyar el bloque. Si acertás sumás **1, 2 o 3 puntos** según el nivel; si errás **restás 1** (nunca bajás de cero).
6. Colocá el bloque arriba de todo y pasa el turno.

Cuando la torre se cae, termina la partida. **Quien la tiró pierde todos sus puntos.** Gana el que tenga más.

> Reglas completas, variantes y guía de impresión en **[Jenga_Cultura_General_Reglas.pdf](Jenga_Cultura_General_Reglas.pdf)**

---

## Materias y colores

| Materia | Color | Inicial | Nivel 1 · 1 pt | Nivel 2 · 2 pts | Nivel 3 · 3 pts | Bloques |
|---|---|---|---|---|---|---|
| Historia | Rojo | H | `#FFCCCC` | `#FF5555` | `#AA0000` | 9 |
| Geografía | Verde | G | `#CCFFCC` | `#44BB44` | `#006600` | 9 |
| Ciencias Naturales | Azul | C | `#CCE5FF` | `#4499DD` | `#004488` | 9 |
| Lengua y Literatura | Violeta | L | `#E8CCFF` | `#9955CC` | `#551188` | 9 |
| Educación Cívica | Naranja | E | `#FFE5CC` | `#FF8833` | `#BB4400` | 9 |

Cada materia lleva **3 bloques de cada nivel**. El nivel también se lee por las ranuras hundidas en la cara grande, y la materia por la inicial grabada en las dos puntas: el juego funciona aunque lo imprimas todo de un solo color.

---

## Cómo imprimirlo

### Piezas 3D

| Archivo | Qué es | Medidas | Cuántas veces |
|---|---|---|---|
| [`stl/materias/*.3mf`](stl/materias/) | **Un archivo por materia**, con sus 3 niveles y el color adentro | 95 × 75 × 15 mm | **3 veces cada uno** → 45 bloques |
| [`stl/Jenga de Cultura General.stl`](stl/) | Los 15 bloques juntos, sin color (archivo original) | 75 × 25 × 15 mm c/u | 3 veces → 45 bloques |
| [`stl/Base de la torre.stl`](stl/) | Placa que apoya y centra el primer piso | 86 × 86 × 6 mm | 1 vez |
| [`stl/Porta-cartas.stl`](stl/) | Bandeja para los mazos, con el frente en curva | 84 × 112 × 24 mm | 1 vez (o 5, una por materia) |

Los `.3mf` traen el color de cada nivel adentro y vienen ya apoyados sobre la cama; el `.stl` no guarda color y entra parado, hay que acostarlo a mano.

Boquilla 0,4 mm · capa 0,2 mm · relleno 15–20 % · **sin soportes**. Si al armar la torre los pisos quedan desparejos, imprimí los bloques al 99 % de escala.

### Cartas

Cada `cartas.pdf` tiene 2 páginas. Imprimilas **a doble faz, girando por el lado largo**, en papel de 160–200 g. Recortá por las cruces de las esquinas: cada carta queda de **72 × 100 mm**.

---

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| [`Jenga_Cultura_General_Reglas.pdf`](Jenga_Cultura_General_Reglas.pdf) | Manual de reglas completo (4 páginas) |
| [`Hoja_de_Puntaje.pdf`](Hoja_de_Puntaje.pdf) | Planilla para anotar los puntos turno a turno |
| [`datos/Materias_y_Bloques.pdf`](datos/Materias_y_Bloques.pdf) | Colores hex y cantidades para imprimir |
| [`preguntas/`](preguntas/) | Los 15 mazos de cartas |
| [`stl/`](stl/) | Bloques, base y porta-cartas |
| [`informe/INFORME.pdf`](informe/INFORME.pdf) | Informe escolar del trabajo |
| [`presentacion/Informe_del_juego.pdf`](presentacion/) | Informe completo del proyecto en texto, con la prueba de juego para completar |
| [`presentacion/Informe_del_juego.docx`](presentacion/) | El mismo informe en Word, para editarlo a mano |
| [`presentacion/Jenga_de_Cultura_General.pptx`](presentacion/) | Presentación de 8 diapositivas para exponer, con notas del orador |

### Mazos de cartas

```
preguntas/
├── historia/   nivel-1 · nivel-2 · nivel-3
├── geografia/  nivel-1 · nivel-2 · nivel-3
├── ciencias/   nivel-1 · nivel-2 · nivel-3
├── lengua/     nivel-1 · nivel-2 · nivel-3
└── civica/     nivel-1 · nivel-2 · nivel-3
```

15 mazos × 4 cartas = 60 preguntas.

---

## Créditos

Proyecto escolar de impresión 3D. Las 60 preguntas corresponden a contenidos
de secundaria argentina: Historia, Geografía, Ciencias Naturales, Lengua y
Literatura y Educación Cívica.

Jenga es una marca registrada de Pokonobe Associates. Este es un trabajo
escolar sin fines comerciales.
