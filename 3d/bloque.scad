// Bloque Jenga — Jenga de Cultura General
// Medidas estándar: 75 x 25 x 15 mm
// Cambiar MATERIA y NIVEL antes de exportar cada STL
// NIVEL 1 = color claro | 2 = medio | 3 = intenso (ver datos/Materias_y_Bloques.pdf)

BLOCK_L = 75;
BLOCK_W = 25;
BLOCK_H = 15;
MARK_DEPTH = 1.2;
MARK_W = 2.5;

// historia | geografia | ciencias | lengua | civica
MATERIA = "historia";
NIVEL = 1;  // 1, 2 o 3

module bloque_base() {
  cube([BLOCK_L, BLOCK_W, BLOCK_H], center = true);
}

// Marca en relieve: cantidad de rayitas = nivel de dificultad
module marca_nivel(n) {
  gap = 4;
  start = -(n - 1) * gap / 2;
  for (i = [0 : n - 1]) {
    translate([0, start + i * gap, BLOCK_H/2 - MARK_DEPTH/2])
      cube([BLOCK_L * 0.65, MARK_W, MARK_DEPTH + 0.01], center = true);
  }
}

// Símbolo de materia (inicial en relieve)
module marca_materia() {
  letras = [
    ["historia", "H"],
    ["geografia", "G"],
    ["ciencias", "C"],
    ["lengua", "L"],
    ["civica", "E"]
  ];
  letra = "M";
  for (par = letras)
    if (par[0] == MATERIA) letra = par[1];
  translate([-BLOCK_L/2 + 8, 0, BLOCK_H/2 - 0.5])
    linear_extrude(height = 1)
      text(letra, size = 7, halign = "center", valign = "center",
           font = "Liberation Sans:style=Bold");
}

difference() {
  union() {
    bloque_base();
    marca_materia();
  }
  marca_nivel(NIVEL);
}

// Exportar: bloque_MATERIA_nNIVEL.stl
