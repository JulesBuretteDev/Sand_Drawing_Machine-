// Logement des pieds IKEA TINGBY, à intégrer dans les coins imprimés de la table à sable.
//
// Principe (notice IKEA AA-2544065-2, étape 1) : chaque pied porte 2 pions vissés dans son bout.
//  - petit pion (tête Ø10, 10 de haut) = PIVOT, dans un trou rond ;
//  - gros pion (tête Ø12,5, 15 de haut) = VERROU, dans une rainure en arc : on l'enfonce dans le
//    trou d'entrée, puis on tourne le pied de 45° autour du pivot ; une lèvre vient se loger dans
//    une gorge du gros pion et bloque le pied.
//
// REPÈRE : on regarde la face de dessous du plateau (table retournée).
//   origine = angle formé par les deux bords droits du plateau, X et Y le long de ces bords, Z vers soi.
//   La matière est en Z < 0.
//
// Cotes relevées sur la table : pions sur la diagonale du pied, à 8 mm (pivot) et 29 mm (verrou)
// de la pointe du pied. La pointe du pied est le centre de l'arrondi R50 du coin, soit (50 ; 50).
// Cotes encore À CONFIRMER : SENS de rotation, profondeur et hauteur de la gorge (lèvre).
// Fichier non compilé dans l'environnement de rédaction : vérifier l'aperçu dans OpenSCAD.

// ---------- Pions (mesurés) ----------
PIV_TETE_D  = 10;    // petit pion : Ø des collerettes
PIV_GORGE_D = 8;     // petit pion : Ø au fond des gorges
PIV_TETE_H  = 10;    // petit pion : hauteur de la tête
VER_TETE_D  = 12.5;  // gros pion : Ø des collerettes
VER_GORGE_D = 9;     // gros pion : Ø au fond des gorges
VER_TETE_H  = 15;    // gros pion : hauteur de la tête

// ---------- Implantation (mesurée) ----------
POINTE    = [50, 50];  // pointe du pied = centre de l'arrondi R50
DIST_PIV  = 8;         // pointe -> centre du petit pion
DIST_VER  = 29;        // pointe -> centre du gros pion
DIRECTION = 225;       // la diagonale part de la pointe vers l'angle arrondi

// ---------- À confirmer ----------
SENS     = 1;     // +1 : le pied se pose tourné de +45° (trou d'entrée à 270°), -1 : à 180°
ROTATION = 45;
LEVRE_Z0 = 4;     // profondeur du haut de la lèvre (= début de la gorge du gros pion, depuis le bout du pied)
LEVRE_H  = 2.5;   // épaisseur de la lèvre (< hauteur de la gorge)

// ---------- Impression ----------
JEU    = 0.4;     // jeu sur les diamètres
JEU_Z  = 0.8;     // garde en profondeur
EP_EPROUVETTE = VER_TETE_H + JEU_Z + 3;
$fn = 96;

A = DIST_VER - DIST_PIV;                                     // entraxe = rayon de la rainure (21)
PIV = POINTE + DIST_PIV * [cos(DIRECTION), sin(DIRECTION)];  // (44,34 ; 44,34)
LARGE  = VER_TETE_D + JEU;    // passage des collerettes
ETROIT = VER_GORGE_D + JEU;   // lèvre : passe dans la gorge, pas les collerettes
PROF   = VER_TETE_H + JEU_Z;

echo(str("Pivot en ", PIV, " ; verrou en ", POINTE + DIST_VER * [cos(DIRECTION), sin(DIRECTION)], " ; entraxe ", A));

// Profil (r, z) de la rainure, z positif vers l'intérieur de la matière
module profil_rainure() {
    polygon([
        [A - LARGE / 2, -0.01], [A + LARGE / 2, -0.01],
        [A + LARGE / 2, LEVRE_Z0], [A + ETROIT / 2, LEVRE_Z0],
        [A + ETROIT / 2, LEVRE_Z0 + LEVRE_H], [A + LARGE / 2, LEVRE_Z0 + LEVRE_H],
        [A + LARGE / 2, PROF], [A - LARGE / 2, PROF],
        [A - LARGE / 2, LEVRE_Z0 + LEVRE_H], [A - ETROIT / 2, LEVRE_Z0 + LEVRE_H],
        [A - ETROIT / 2, LEVRE_Z0], [A - LARGE / 2, LEVRE_Z0]
    ]);
}

module logement_tingby() {
    a_entree = DIRECTION + SENS * ROTATION;
    a_debut = min(DIRECTION, a_entree);
    mirror([0, 0, 1])
    translate([PIV[0], PIV[1], 0]) {
        // trou du pivot (petit pion)
        translate([0, 0, -0.01]) cylinder(d = PIV_TETE_D + JEU, h = PIV_TETE_H + JEU_Z + 0.01);
        // rainure en arc avec lèvre
        rotate([0, 0, a_debut]) rotate_extrude(angle = ROTATION) profil_rainure();
        // bout de la rainure (position verrouillée)
        rotate([0, 0, DIRECTION]) translate([A, 0, 0]) {
            translate([0, 0, -0.01]) cylinder(d = LARGE, h = LEVRE_Z0 + 0.01);
            translate([0, 0, LEVRE_Z0 - 0.01]) cylinder(d = ETROIT, h = LEVRE_H + 0.02);
            translate([0, 0, LEVRE_Z0 + LEVRE_H]) cylinder(d = LARGE, h = PROF - LEVRE_Z0 - LEVRE_H);
        }
        // trou d'entrée sur toute la profondeur
        rotate([0, 0, a_entree]) translate([A, 0, -0.01]) cylinder(d = LARGE, h = PROF + 0.01);
    }
}

// Éprouvette : imprimer face de dessous sur le plateau, puis tester avec un vrai pied
module eprouvette() {
    difference() {
        translate([0, 0, -EP_EPROUVETTE]) cube([60, 60, EP_EPROUVETTE]);
        logement_tingby();
    }
}

// Les 4 logements sur un plateau de 500 x 500 (pieds identiques tournés de 90°)
module quatre_logements(cote = 500) {
    for (i = [0 : 3])
        translate([cote / 2, cote / 2, 0]) rotate([0, 0, 90 * i])
            translate([-cote / 2, -cote / 2, 0]) logement_tingby();
}

eprouvette();
