# Électronique — table à sable v2

Choix retenu : le **Raspberry Pi 4B** envoie les motifs par **USB** à un **Arduino Uno sous GRBL 1.1**,
équipé d'une **shield CNC V3** et de **2 drivers TMC2209**. Puissance moteurs : **bloc 19 V** sur le bornier de la shield.
(Une variante ESP32 + FluidNC avait été étudiée, puis écartée pour réutiliser ce matériel.)

## Schéma

```
  Bloc 19 V (chargeur portable, ≥ 65 W)
        │
   [interrupteur] ── [fusible 4 A] ── (protection contre l'inversion de polarité)
        │
        ├──────────────► Shield CNC V3 (bornier VMOT 12–36 V)
        │                   ├─ driver X (TMC2209) ──► Moteur A
        │                   ├─ driver Y (TMC2209) ──► Moteur B
        │                   └─ fins de course X- (D9), Y- (D10) · boutons Hold / Resume (A1 / A2)
        │                         ▲ shield enfichée sur l'Arduino Uno (GRBL 1.1, COREXY)
        │                         │ câble USB = données + 5 V de l'Arduino
        └──► Convertisseur 19 V → 5,1 V / 5 A ──► Raspberry Pi 4B (USB-C) (+ LEDs 5 V en option)
```

- Le 19 V de la shield n'alimente **que les drivers**. L'Arduino prend son 5 V par l'USB de la Pi.
- Un seul bloc et une masse commune. Budget : moteurs 10–20 W, Pi 4 5–8 W, LEDs en option : 65 W suffisent.
- ⚠️ La shield CNC n'a pas de protection contre l'inversion de polarité : vérifier au multimètre avant de brancher.
- ⚠️ Ne jamais brancher ni débrancher un moteur sous tension (destruction du driver).
- Ventilateur éventuel en 5 V sur le convertisseur (un ventilateur 12 V ne supporte pas le 19 V).

## TMC2209 sur la shield CNC (mode autonome STEP/DIR)

- 19 V est sous leur maximum de 29 V. Mode silencieux (StealthChop) par défaut, sans UART.
- Micro-pas **1/16** : cavaliers **M0 et M1 mis, M2 retiré**. Sur beaucoup de modules TMC2209, la 3e broche est
  PDN/UART et non MS3 : **ne jamais mettre M2**, et vérifier le brochage du module.
- Pas de retour à l'origine sans capteur (DIAG non câblé sur la shield) : **2 fins de course** sur X- et Y-.
- Régler le **Vref** avant de brancher les moteurs (formule du fabricant), viser environ 0,7–0,8 A. Radiateurs sur les drivers.

## GRBL

- Compiler GRBL 1.1 avec `#define COREXY` dans `config.h`.
- Réglages issus des plans (`docs/MECANIQUE.md`) :

| Réglage | Valeur | Rôle |
|---|---|---|
| `$100`, `$101` | 80 | pas/mm |
| `$110`, `$111` | 3000–6000 | vitesse max (mm/min) |
| `$120`, `$121` | 100–300 | accélération (plus bas = plus silencieux) |
| `$130`, `$131` | 343, 326 | courses X et Y |
| `$20` / `$22` | 1 / 1 | limites logicielles / retour à l'origine |
| `$5` | 0 ou 1 | selon le type de fin de course |

- L'Uno **redémarre à chaque ouverture du port série** : attendre la bannière `Grbl 1.1…` avant d'envoyer.
- Côté Pi, utiliser `/dev/serial/by-id/…` plutôt que `/dev/ttyACM0`.

## La Raspberry Pi existante

- Raspberry Pi 4B déjà en service : service `pi-hub` (serveur MCP lisible depuis les conversations Claude),
  pilotage du ventilateur sur GPIO14, mosquitto (MQTT), apache2.
- Une **Arduino Mega + écran TFT 480 × 320** (contrôleur 0x9488, l'écran de la v1) y est déjà branchée en USB
  et affiche l'état de la Pi. L'Uno GRBL sera un **second** périphérique USB : les distinguer par `/dev/serial/by-id/`.
- Le serveur `pi-hub` ne donne qu'un accès en lecture (état, écran, imprimante 3D). Pour flasher et tester
  la machine, il faut un accès terminal : cloner ce dépôt sur la Pi et y lancer `claude remote-control`.

## Procédure de test du montage (à dérouler avec un accès terminal sur la Pi)

1. **Repérage USB** : `ls -l /dev/serial/by-id/` → identifier l'Uno (et ne pas toucher au port de la Mega).
2. **Firmware** : flasher GRBL 1.1 compilé avec `COREXY` (`arduino-cli` ou `avrdude`), puis vérifier la bannière
   et `$I` en série à 115200 bauds.
3. **Réglages** : appliquer les `$` ci-dessus, puis vérifier avec `$$`.
4. **Alimentation** : 19 V présent au bornier (multimètre), Vref de chaque driver réglé, **moteurs débranchés**
   pendant ces mesures.
5. **Moteurs, l'un après l'autre** : `$X` puis petits déplacements en `G91 G1 X10 F500`. En CoreXY, un
   déplacement en X fait tourner les deux moteurs dans le même sens, un déplacement en Y en sens contraires.
   Si un axe part à l'envers ou si X et Y sont permutés, inverser un moteur (`$3`) ou permuter les connecteurs.
6. **Fins de course** : `?` doit afficher `Pn:X` / `Pn:Y` quand on appuie sur chaque contact. Ensuite seulement,
   `$H`.
7. **Géométrie** : tracer un carré de 300 mm et un cercle de Ø300, mesurer, corriger `$100` / `$101` si besoin.
8. **Silence et chaleur** : vérifier la température des drivers après 15 min de motif.

## Statut

- [x] Choix des composants (Pi 4B, Uno + shield CNC V3, 2 × TMC2209, bloc 19 V)
- [ ] Convertisseur 19 V → 5 V, fusible, interrupteur, protection de polarité
- [ ] GRBL compilé en COREXY et flashé
- [ ] Montage testé (procédure ci-dessus) — non fait : pas encore d'accès terminal à la Pi
