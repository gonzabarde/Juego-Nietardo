// Bloque Jenga — Torre Sabia
// Medidas estándar Jenga: ~7.5 x 2.5 x 1.5 cm (escala 10: 75 x 25 x 15 mm)

BLOCK_L = 75;
BLOCK_W = 25;
BLOCK_H = 15;
MARK_DEPTH = 1.5;
MARK_W = 3;
MARK_GAP = 4;

module bloque_base() {
  cube([BLOCK_L, BLOCK_W, BLOCK_H], center = true);
}

module marca_linea(offset_y) {
  translate([0, offset_y, BLOCK_H/2 - MARK_DEPTH/2])
    cube([BLOCK_L * 0.7, MARK_W, MARK_DEPTH + 0.01], center = true);
}

// Bloque FÁCIL — 1 línea (🍃 hoja)
module bloque_facil() {
  difference() {
    bloque_base();
    marca_linea(0);
  }
}

bloque_facil();

// Exportar: bloque_facil.stl
