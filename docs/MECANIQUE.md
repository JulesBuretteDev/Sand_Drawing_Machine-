# Mécanique — table à sable CoreXY (v2)

Toutes les cotes viennent des scripts de `docs/mecanique/` : modifier un paramètre dans
`plan_corexy.py` ou `hauteurs.py`, puis relancer le script, plutôt que de recopier des chiffres à la main.

```bash
cd docs/mecanique
python3 plan_corexy.py   # courses, poulies, jeux, longueur de courroie
python3 hauteurs.py      # empilement en hauteur
```

Page de présentation avec schémas cotés (vue de dessus, coupe, détail) :
https://claude.ai/artifact/Y4cmRfSZdFkh9AjhLu9zWr (privée, à partager depuis son menu).

## Cadre et implantation

- La machine remplace le plateau d'une **desserte IKEA TINGBY 50 × 50** (art. 202.959.30) : gabarit
  **500 × 500, angles R50**. Les pieds (quart de cylindre R50, 5 cm) restent ceux de la TINGBY.
- Cadre en **profilés 2020 V-slot** : 4 × 400 mm entre 4 **coins imprimés** de 50 × 50 R50.
- Repère des plans : origine au coin haut-gauche, X vers la droite, Y vers le bas (vue de dessus).

## Cinématique CoreXY

- 2 NEMA 17 fixes sur le profilé droit, collés aux coins imprimés (centres en (478,9 ; 72,2) et (478,9 ; 427,9)).
- 2 courroies **GT2 6 mm**, une par niveau (A en haut, B environ 10 mm plus bas), poulies 20 dents.
- Chaque courroie fait **un demi-tour sur sa poulie moteur** grâce à 2 poulies de renvoi dans le coin moteur :
  les brins horizontaux passent à **30 et 42 mm** du bord.
- Cinématique : `A = X + Y`, `B = X − Y`. **80 pas/mm** (GT2 20T, micro-pas 1/16).

| Résultat | Valeur |
|---|---|
| Course du portique (X) | **343,0** mm (axe du portique de 78,5 à 421,5) |
| Course de l'aimant (Y) | **326,3** mm (de 86,9 à 413,1) |
| Bac à sable (intérieur) | **350 × 350**, centré |
| Limites logicielles (bille Ø15, 3 mm de marge) | X 85,5 → 414,5 · Y 86,9 → 413,1 |
| Zone dessinée | ≈ 344 × 341 mm |
| Profilé du portique | **446 mm** entre les plaques des chariots d'extrémité |
| Longueur de chaque courroie | ≈ 1,83 m + serrage → acheter 2 × 2 m |

### Poulies (centres, portique au milieu X = 250)

| Rep. | Courroie | Type | X | Y | Fixée sur |
|---|---|---|---|---|---|
| P1 | A | lisse | X + 6,4 | 48,4 | chariot d'extrémité haut (patte venant du haut) |
| P2 | B | dentée | X − 6,4 | 36,4 | chariot d'extrémité haut (support sur le portique) |
| P3 | A | dentée | X − 6,4 | 463,6 | chariot d'extrémité bas |
| P4 | B | lisse | X + 6,4 | 451,6 | chariot d'extrémité bas |
| P5 | A | lisse | 466,1 | 48,4 | coin moteur A |
| P6 | A | dentée | 478,9 | 36,4 | coin moteur A |
| P7 | B | lisse | 466,1 | 451,6 | coin moteur B |
| P8 | B | dentée | 478,9 | 463,6 | coin moteur B |
| P9 | A + B | 2 dentées superposées | 34,4 | 36,4 | coin haut-gauche |
| P10 | A + B | 2 dentées superposées | 34,4 | 463,6 | coin bas-gauche |

Jeux minimaux vérifiés (pire cas) : 2,5 mm entre la plaque d'un chariot d'extrémité et le coin imprimé,
3,0 mm entre le brin qui descend au moteur A et la flasque de P6, 3,85 mm entre le chariot aimant et le moteur A.

### Chariots (hypothèses du calcul)

- **Chariots d'extrémité** : plaque verticale de 6 mm côté intérieur, roues V Ø25 sur les faces haut et bas du
  profilé (entraxe 30). Les roues ne peuvent pas aller sur la face extérieure : c'est le bord de la table.
- **Chariot aimant** : 4 roues Ø25 de part et d'autre du portique, environ 64,7 × 55 mm.

## Hauteurs (Z = 0 sous la plaque de fond)

Épaisseur totale **≈ 134,5 mm hors pieds** (au lieu de 36). Détail avec `python3 hauteurs.py`.
Repères : cadre surélevé de 25 mm (roues basses des chariots d'extrémité), portique 40 → 60,
courroie B 64,5 → 70,5, courroie A 74,5 → 80,5, aimant Ø20 × 10 à 5 mm de la bille, verre 128,5 → 134,5.

- Moteurs montés **axe vers le bas** : la poulie est à la hauteur de sa courroie. Le corps du moteur A
  (40 mm supposés) fixe la hauteur du verre ; moteurs de 34 mm = −6 mm.
- **Électronique sous le portique : 30 mm de haut au maximum.** ⚠️ Un Arduino Uno avec shield CNC et
  radiateurs sur les TMC2209 fait environ 45 mm : à placer ailleurs (boîtier sous la table) ou remonter le
  portique (`GANTRY_BOTTOM` dans `hauteurs.py`). Sortir toute l'électronique de la table ramène le plateau
  à environ 106 mm.
- Fond du bac : plaque pleine amagnétique de 3 mm posée sur des tasseaux le long des parois.
- Point serré : des parois d'habillage de 4 mm ne laissent qu'environ 1 mm avec les roues hautes des
  chariots d'extrémité.

## Poulies imprimées

- Matière : **PETG ou ASA** (pas de PLA sous tension permanente), 100 % de remplissage ou 5 parois.
- **Une poulie ne tourne jamais directement sur le filetage d'une vis.** Les vis disponibles sont filetées sur
  toute la longueur, d'où deux montages :
  1. **Bague imprimée fixe** (palier lisse) : alésage Ø5,2 (vis M5), extérieur Ø8, collerettes Ø11–12 ;
     alésage de la poulie Ø8,3–8,4 ; bague en PLA ou nylon, poulie en PETG ; graisse silicone ou PTFE.
  2. **Roulements MR105ZZ (5 × 10 × 4)**, environ 5 € les 10 : solution définitive, même logement de poulie.
- Les poulies dentées 20T laissent environ 1 mm de paroi autour d'un roulement : trop fragile à imprimer.
  Prendre du 30T, ou des poulies lisses Ø18–20 même côté dents. **Changer un diamètre change les plans** :
  modifier `RP` et `RF` dans `plan_corexy.py`.
- **Poulies moteur : à acheter en alu** (GT2 20T, alésage 5 mm, vis de serrage sur le méplat).
- Fixation : appui des deux côtés (vis traversant deux plaques) dans les coins imprimés ; insert fileté à chaud
  ou écrou prisonnier dans le plastique ; écrou marteau M5 dans les rainures du 2020 ; écrou frein.

## Fixation des pieds TINGBY

Notice officielle AA-2544065-2. Chaque pied porte **2 pions vissés** dans son bout :

| | Gros pion = verrou | Petit pion = pivot |
|---|---|---|
| Tête | Ø12,5, gorges Ø9, 15 de haut | Ø10, gorges Ø8, 10 de haut |
| Tige vissée dans le pied | Ø7,5 × 40 | Ø6 × 30 |
| Distance à la pointe du pied | 29 mm | 8 mm |

- La pointe du pied est le centre de l'arrondi R50 du coin, au point (50 ; 50). Les pions sont sur la diagonale.
  Le **pivot** est en (44,34 ; 44,34) et le **verrou bloqué** en (29,49 ; 29,49) (repère : face de dessous,
  origine à l'angle des bords droits). Entraxe 21 mm.
- Dans le plateau : un trou rond pour le pivot, et une **rainure en arc** de rayon 21 sur 45° pour le verrou
  (trou d'entrée Ø12,9, lèvre de 9,4 qui se loge dans une gorge du gros pion).
- Logement paramétrique et éprouvette d'essai : `docs/mecanique/logement_pied_tingby.scad`.
- **À confirmer** : le sens de rotation pour bloquer (vu de dessous), la profondeur et la hauteur de la gorge
  du gros pion la plus proche du pied (`LEVRE_Z0`, `LEVRE_H`).
