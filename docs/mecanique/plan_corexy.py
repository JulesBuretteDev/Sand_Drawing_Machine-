"""Géométrie CoreXY de la table à sable 500 x 500 (vue de dessus).

Repère : origine au coin haut-gauche du contour, X vers la droite, Y vers le bas, en mm.
Lancer `python3 plan_corexy.py` pour afficher courses, poulies, jeux et longueur de courroie.
Les autres scripts (hauteurs.py) importent ce module : modifier un paramètre ici suffit.
"""
import math

# ---------------- Paramètres (modifiables) ----------------
W = 500.0            # contour extérieur
CORNER = 50.0        # coins imprimés (et rayon extérieur)
PROF = 20.0          # profilé 2020
RP = 20 * 2 / (2 * math.pi)   # rayon primitif poulie GT2 20 dents = 6.366
RF = 9.0             # rayon des flasques (poulie Ø18)
WHEEL_R = 12.5       # roues Ø25
WHEEL_OFF = 19.85    # entraxe roue / axe du profilé (V-slot 20 mm)
SE = 30.0            # entraxe des 2 roues d'un chariot d'extrémité (selon X)
SM = 30.0            # entraxe des roues du chariot aimant (selon Y)
PLATE_Y0, PLATE_T = 21.0, 6.0   # plaque verticale des chariots d'extrémité
PLATE_HALF = 26.0    # demi-longueur de cette plaque selon X
MOTOR = 42.3
MA = (W - MOTOR / 2, CORNER + 1 + MOTOR / 2)   # moteur A (collé au coin imprimé haut-droit)
MB = (MA[0], W - MA[1])
Y_OUT, Y_IN = 30.0, 42.0   # lignes de courroie haut (bas = W - ...)
X_L = 28.0                 # ligne de courroie côté gauche
CLR = 2.0                  # jeu mini entre pièces mobiles
WHEEL_END_MARGIN = 1.0     # roue d'extrémité : ne dépasse pas le bout du profilé
BALL = 15.0                # bille
TRAY = 350.0               # bac intérieur
TRAY_MARGIN = 3.0          # bille <-> paroi du bac

# ---------------- Calculs ----------------
# Course du portique (X) : les roues restent sur le profilé de 400 (x 50..450)
gx_min = CORNER + WHEEL_R + WHEEL_END_MARGIN + SE / 2
gx_max = W - CORNER - WHEEL_R - WHEEL_END_MARGIN - SE / 2
x_travel = gx_max - gx_min


def pulleys(gx):
    """Centres des poulies pour un portique en X = gx. Courroie A niveau haut, B niveau bas."""
    return {
        "P1": ("A", "lisse",  (gx + RP, Y_IN + RP), "Chariot ext. haut"),
        "P2": ("B", "dentée", (gx - RP, Y_OUT + RP), "Chariot ext. haut"),
        "P3": ("A", "dentée", (gx - RP, W - Y_OUT - RP), "Chariot ext. bas"),
        "P4": ("B", "lisse",  (gx + RP, W - Y_IN - RP), "Chariot ext. bas"),
        "P5": ("A", "lisse",  (MA[0] - 2 * RP, Y_IN + RP), "Coin moteur A"),
        "P6": ("A", "dentée", (MA[0], Y_OUT + RP), "Coin moteur A"),
        "P7": ("B", "lisse",  (MB[0] - 2 * RP, W - Y_IN - RP), "Coin moteur B"),
        "P8": ("B", "dentée", (MB[0], W - Y_OUT - RP), "Coin moteur B"),
        "P9": ("A+B", "dentée ×2", (X_L + RP, Y_OUT + RP), "Coin haut-gauche"),
        "P10": ("A+B", "dentée ×2", (X_L + RP, W - Y_OUT - RP), "Coin bas-gauche"),
    }


# Course de l'aimant (Y) : chariot aimant bloqué par la poulie la plus intérieure (P1 / P4)
mag_half_y = SM / 2 + WHEEL_R
mag_half_x = WHEEL_OFF + WHEEL_R
p = pulleys(250)
yc_min = p["P1"][2][1] + RF + CLR + mag_half_y
yc_max = p["P4"][2][1] - RF - CLR - mag_half_y
y_travel = yc_max - yc_min

# Vérifications de collisions (en vue de dessus, pire cas)
checks = []
pm = pulleys(gx_max)
checks.append(("P1 (portique à droite) / P5", (pm["P5"][2][0] - RF) - (pm["P1"][2][0] + RF)))
pm0 = pulleys(gx_min)
checks.append(("P2 (portique à gauche) / P9", (pm0["P2"][2][0] - RF) - (pm0["P9"][2][0] + RF)))
checks.append(("Chariot aimant / moteur A (coin haut-droit)", (MA[0] - MOTOR / 2) - (gx_max + mag_half_x)))
checks.append(("Brin vers moteur A / flasque P6", (pulleys(0)["P5"][2][1]) - (pulleys(0)["P6"][2][1] + RF)))
checks.append(("Plaque chariot ext. / coin imprimé (droite)", (W - CORNER) - (gx_max + PLATE_HALF)))
checks.append(("Plaque chariot ext. / coin imprimé (gauche)", (gx_min - PLATE_HALF) - CORNER))
c6 = pulleys(0)["P6"][2]
checks.append(("P6 dans le coin arrondi (paroi restante)", CORNER - (math.dist(c6, (W - CORNER, CORNER)) + RF)))
c9 = pulleys(0)["P9"][2]
checks.append(("P9 dans le coin arrondi (paroi restante)", CORNER - (math.dist(c9, (CORNER, CORNER)) + RF)))


def belt_A_length(gx, yc, clamp=10.0):
    """Longueur de la courroie A (identique à B par symétrie), attaches à yc ± clamp."""
    q = pulleys(gx)
    L = 0.0
    L += (yc - clamp) - q["P1"][2][1]
    L += math.pi / 2 * RP
    L += q["P5"][2][0] - q["P1"][2][0]
    L += math.pi / 2 * RP
    L += MA[1] - q["P5"][2][1]
    L += math.pi * RP                                  # moteur 180°
    L += MA[1] - q["P6"][2][1]
    L += math.pi / 2 * RP
    L += q["P6"][2][0] - q["P9"][2][0]
    L += math.pi / 2 * RP
    L += q["P10"][2][1] - q["P9"][2][1]
    L += math.pi / 2 * RP
    L += q["P3"][2][0] - q["P10"][2][0]
    L += math.pi / 2 * RP
    L += q["P3"][2][1] - (yc + clamp)
    return L


belt_len = belt_A_length(250, 250)

# Bac et zone de dessin (limites logicielles)
tray0 = (W - TRAY) / 2
soft = (tray0 + BALL / 2 + TRAY_MARGIN, W - tray0 - BALL / 2 - TRAY_MARGIN)
lim_x = (max(gx_min, soft[0]), min(gx_max, soft[1]))
lim_y = (max(yc_min, soft[0]), min(yc_max, soft[1]))
draw_x = lim_x[1] - lim_x[0] + BALL
draw_y = lim_y[1] - lim_y[0] + BALL
gantry_len = W - 2 * (PLATE_Y0 + PLATE_T)

if __name__ == "__main__":
    print(f"Course portique X : {x_travel:.1f} ({gx_min:.1f} -> {gx_max:.1f})")
    print(f"Course aimant Y   : {y_travel:.1f} ({yc_min:.1f} -> {yc_max:.1f})")
    print(f"Limites logicielles (bac {TRAY:.0f}) : X {lim_x[0]:.1f}->{lim_x[1]:.1f}  Y {lim_y[0]:.1f}->{lim_y[1]:.1f}")
    print(f"Zone dessinée : {draw_x:.1f} x {draw_y:.1f}")
    print(f"Profilé portique : {gantry_len:.0f}   Courroie : {belt_len:.0f} mm (+ serrage)")
    print("\nPoulies (portique au centre gx=250):")
    for k, (lvl, typ, (x, y), where) in pulleys(250).items():
        print(f"  {k:4s} {lvl:4s} {typ:10s} x={x:7.2f} y={y:7.2f}  {where}")
    print("\nJeux (doivent être > 0):")
    for name, v in checks:
        print(f"  {name:45s} {v:6.2f} mm")
