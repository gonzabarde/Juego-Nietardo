// Base Torre Sabia — torre de libros / plataforma
BASE_L = 90;
BASE_W = 90;
BASE_H = 8;
RIM = 3;

module base_torre_sabia() {
  difference() {
    // Plataforma principal
    cube([BASE_L, BASE_W, BASE_H]);

    // Borde interior (reborde para que no resbale la torre)
    translate([RIM, RIM, BASE_H - 2])
      cube([BASE_L - 2*RIM, BASE_W - 2*RIM, 3]);

    // Texto "TORRE SABIA" (simplificado como surco)
    translate([BASE_L/2, BASE_W/2, BASE_H - 1])
      linear_extrude(height = 1.5)
        text("TORRE SABIA", size = 6, halign = "center", valign = "center",
             font = " Liberation Sans:style=Bold");
  }

  // Detalle: "libros" en los bordes
  for (i = [0:3]) {
    translate([10 + i * 20, 5, BASE_H])
      cube([15, 8, 4 + i]);
    translate([10 + i * 20, BASE_W - 13, BASE_H])
      cube([15, 8, 3 + (3-i)]);
  }
}

base_torre_sabia();
