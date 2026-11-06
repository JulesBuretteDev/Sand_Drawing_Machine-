# Sand Drawing Machine — contexte pour Claude

Table à sable : une bille d'acier, tirée par un aimant sous un bac de sable, trace des motifs (G-code Sandify).
Le propriétaire reprend un projet ancien (v1) pour en faire une v2 propre. Échanges en **français**, cotes en **mm**.

## Où en est le projet

- **v1 (legacy)** : `raspyFiles/` (Python/Flask sur la Pi, envoi de G-code à GRBL, écran TFT sur Arduino) et
  `arduinooo/screen/screen.ino`. Revue détaillée dans `docs/REVIEW_V1.md`. Ce code n'est pas à réutiliser tel quel.
- **v2 (en conception)** : rien n'est encore implémenté côté logiciel. Les décisions sont dans `docs/` :
  - `docs/ARCHITECTURE.md` : architecture logicielle visée (service Python unique sur la Pi, pilote GRBL,
    file de motifs, API web).
  - `docs/MECANIQUE.md` : mécanique CoreXY, cotes, poulies, hauteurs, fixation des pieds TINGBY, poulies imprimées.
  - `docs/HARDWARE.md` : électronique, câblage, réglages GRBL et **procédure de test du montage**.
  - `docs/mecanique/*.py` : calculs paramétriques (source de vérité des cotes) ;
    `docs/mecanique/logement_pied_tingby.scad` : logement des pieds.

## Décisions clés (ne pas les remettre en cause sans que l'utilisateur le demande)

- Gabarit **500 × 500, angles R50** : la machine remplace le plateau d'une desserte IKEA TINGBY.
- **CoreXY**, cadre 2020 V-slot (4 × 400 + coins imprimés), 2 NEMA 17 fixes côté droit, GT2 6 mm,
  renvois dans les coins moteurs. Bac **350 mm** ; courses 343 (X) × 326 (Y).
- Électronique : **Raspberry Pi 4B → USB → Arduino Uno GRBL 1.1 (COREXY) + shield CNC V3 + 2 × TMC2209**
  (mode autonome, 1/16), **bloc 19 V** sur la shield, convertisseur 19 → 5 V pour la Pi.
- Poulies de renvoi imprimées (PETG/ASA) sur bague imprimée ou roulements MR105ZZ ; poulies moteur en alu.

## Travailler avec les cotes

Ne recopie pas de chiffres à la main : modifie les paramètres de `docs/mecanique/plan_corexy.py` ou
`hauteurs.py` et relance-les (`cd docs/mecanique && python3 plan_corexy.py`), puis mets à jour `docs/MECANIQUE.md`.

## Accès à la Raspberry Pi

- Le serveur MCP **pi-hub** (s'il est connecté à la conversation) donne un accès **en lecture** à la Pi :
  état système, écran TFT de la Mega, imprimante 3D. Il ne permet ni commandes shell ni accès au port de l'Uno.
- Pour flasher GRBL et tester la machine, il faut un accès terminal : l'utilisateur clone ce dépôt sur la Pi et
  lance `claude remote-control` dans le dossier ; la conversation peut alors demander l'accès à ce dossier.
- Deux Arduino seront sur la Pi (Mega de l'écran + Uno GRBL) : toujours passer par `/dev/serial/by-id/` et ne pas
  ouvrir le port de la Mega (il est utilisé par le service d'affichage).

## Points ouverts

- Sens de rotation des pieds TINGBY et cote de la gorge du gros pion (voir `docs/MECANIQUE.md`).
- Longueur réelle du corps des moteurs (40 mm supposés), épaisseur du verre, taille de l'aimant.
- Emplacement de l'Uno + shield (≈ 45 mm de haut, trop pour la zone de 30 mm sous le portique).
- Montage électronique **non testé** (voir la procédure dans `docs/HARDWARE.md`).
- Sécurité : une clé API OpenWeather est dans l'historique git (`raspyFiles/MyValues.py`). Elle doit être
  révoquée ; ne jamais remettre de clé dans le code (utiliser un `.env` non versionné).
