"""Empilement en hauteur (Z) de la table à sable, coupe par l'axe du portique.

Z = 0 sous la plaque de fond. Reprend la géométrie de plan_corexy.py.
Lancer `python3 hauteurs.py` pour afficher le tableau des hauteurs.
"""
from plan_corexy import PROF, WHEEL_OFF, WHEEL_R, BALL

# ---------------- Paramètres de hauteur (modifiables) ----------------
BASE_T = 6.0          # plaque de fond
WALL_T = 4.0          # parois d'habillage
MOTOR_L = 40.0        # longueur du corps des NEMA 17 (à confirmer)
PULLEY_H = 9.0        # hauteur entre flasques d'une poulie (courroie de 6)
GANTRY_BOTTOM = 40.0  # place libre sous le portique (électronique)
SUPPORT_T = 3.0       # support imprimé sous P2/P4
BELT_GAP = 10.0       # entraxe vertical courroie B -> courroie A
BRACKET_T = 4.0       # patte moteur
PLATE_M_T = 5.0       # plaque du chariot aimant
MAG_H, MAG_D = 10.0, 20.0   # aimant néodyme Ø20 x 10
MAG_GAP = 2.0         # aimant <-> dessous du bac
TRAY_T = 3.0          # fond du bac (plaque pleine, amagnétique)
SAND = 5.0
GLASS_T = 6.0
GLASS_GAP = 8.0       # bille <-> verre

Z = {}
Z["base"] = (0.0, BASE_T)
# roue basse d'un chariot d'extrémité : point le plus bas à 2,5 mm au-dessus de la plaque
frame_axis = BASE_T + 2.5 + WHEEL_OFF + WHEEL_R
Z["frame"] = (frame_axis - PROF / 2, frame_axis + PROF / 2)
Z["wheel_lo"] = (frame_axis - WHEEL_OFF - WHEEL_R, frame_axis - WHEEL_OFF + WHEEL_R)
Z["wheel_hi"] = (frame_axis + WHEEL_OFF - WHEEL_R, frame_axis + WHEEL_OFF + WHEEL_R)
Z["gantry"] = (GANTRY_BOTTOM, GANTRY_BOTTOM + PROF)
gt = Z["gantry"][1]
zB = gt + SUPPORT_T + PULLEY_H / 2           # axe courroie B
zA = zB + BELT_GAP                           # axe courroie A
Z["belt_B"] = (zB - 3, zB + 3)
Z["belt_A"] = (zA - 3, zA + 3)
Z["pul_B"] = (zB - PULLEY_H / 2, zB + PULLEY_H / 2)
Z["pul_A"] = (zA - PULLEY_H / 2, zA + PULLEY_H / 2)
Z["mwheel"] = (gt - PROF / 2 - 5, gt - PROF / 2 + 5)
Z["mplate"] = (Z["pul_A"][1] + 1.5, Z["pul_A"][1] + 1.5 + PLATE_M_T)
Z["magnet"] = (Z["mplate"][1] + 2, Z["mplate"][1] + 2 + MAG_H)
Z["tray"] = (Z["magnet"][1] + MAG_GAP, Z["magnet"][1] + MAG_GAP + TRAY_T)
Z["sand"] = (Z["tray"][1], Z["tray"][1] + SAND)
Z["ball"] = (Z["tray"][1], Z["tray"][1] + BALL)
Z["eplate"] = (BASE_T + 6, Z["pul_A"][1] + 4.5)      # plaque chariot ext. + patte haute
Z["motorA"] = (Z["pul_A"][1] + 0.5 + BRACKET_T, Z["pul_A"][1] + 0.5 + BRACKET_T + MOTOR_L)
Z["motorB"] = (Z["pul_B"][1] + 0.5 + BRACKET_T, Z["pul_B"][1] + 0.5 + BRACKET_T + MOTOR_L)
glass0 = max(Z["ball"][1] + GLASS_GAP, Z["motorA"][1] + 2)
Z["glass"] = (glass0, glass0 + GLASS_T)
Z["wall"] = (BASE_T, glass0)
Z["ledge"] = (Z["tray"][0] - 6, Z["tray"][0])
Z["elec"] = (BASE_T, GANTRY_BOTTOM - 4)
TOTAL = Z["glass"][1]

LABELS = [
    ("Plaque de fond", "base"), ("Profilés du cadre 2020 (surélevés)", "frame"),
    ("Roues basses des chariots d'extrémité", "wheel_lo"), ("Roues hautes des chariots d'extrémité", "wheel_hi"),
    ("Zone électronique (sous le portique)", "elec"), ("Portique 2020", "gantry"),
    ("Roues du chariot aimant", "mwheel"), ("Courroie B", "belt_B"), ("Courroie A", "belt_A"),
    ("Plaque du chariot aimant", "mplate"), ("Aimant Ø20 x 10", "magnet"), ("Fond du bac", "tray"),
    ("Sable", "sand"), ("Bille Ø15", "ball"), ("Moteur B (axe vers le bas)", "motorB"),
    ("Moteur A (axe vers le bas)", "motorA"), ("Verre trempé", "glass"),
]

if __name__ == "__main__":
    for name, k in LABELS:
        a, b = Z[k]
        print(f"{name:42s} {a:6.1f} -> {b:6.1f}")
    print(f"\nÉpaisseur totale (hors pieds) : {TOTAL:.1f} mm")
