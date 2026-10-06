# Sand Drawing Machine — Plan d'architecture (v2)

> Document de réflexion pour la reprise du projet. Rien n'est encore implémenté.
> Questions ouvertes : choix de l'écran (option A ou B, §3.6) et techno du front (Svelte ou HTMX, §4).

## 1. Ce qu'on garde de la v1

- Raspberry Pi comme cerveau
- Arduino + GRBL pour les moteurs (fiable, éprouvé)
- Sandify pour créer les motifs
- Écran tactile, capteur PIR, coupure de l'alim USB (`uhubctl`)

Ce qui change surtout, c'est le logiciel : passer de deux scripts séparés à **un seul service**
sur le Raspberry, découpé en modules qui communiquent par des événements.

## 2. Vue d'ensemble

```
┌──────────────────────────────── Raspberry Pi ────────────────────────────────┐
│                                                                              │
│   Navigateur (téléphone / PC)                                                │
│        │  HTTP (REST) + WebSocket (temps réel)                                │
│        ▼                                                                     │
│   ┌────────────┐                                                             │
│   │  API web   │  FastAPI : routes REST + WebSocket                          │
│   └─────┬──────┘                                                             │
│         │                                                                    │
│   ┌─────▼──────────────────── Bus d'événements ─────────────────────────┐    │
│   │  position, état, motif_démarré, capteurs, présence, alarme…         │    │
│   └──┬──────────┬───────────┬────────────┬────────────┬──────────────┬──┘    │
│      │          │           │            │            │              │       │
│ ┌────▼───┐ ┌────▼─────┐ ┌───▼──────┐ ┌───▼──────┐ ┌───▼─────┐ ┌──────▼───┐   │
│ │Pilote  │ │Lecteur / │ │Biblio-   │ │Capteurs  │ │ Écran   │ │Alim. et  │   │
│ │ GRBL   │ │file      │ │thèque    │ │DHT, PIR, │ │         │ │LED       │   │
│ │        │ │d'attente │ │de motifs │ │météo     │ │         │ │          │   │
│ └───┬────┘ └──────────┘ └────┬─────┘ └──────────┘ └───┬─────┘ └────┬─────┘   │
│     │                        │                        │            │         │
│     │                   SQLite + fichiers             │          uhubctl     │
└─────┼─────────────────────────────────────────────────┼──────────────────────┘
      │ USB série (115200)                              │ USB série
┌─────▼──────────┐                              ┌───────▼────────┐
│ Arduino GRBL   │                              │ Arduino écran  │
│ + moteurs      │                              │ TFT tactile    │
└────────────────┘                              └────────────────┘
```

**Principe :** chaque module a un seul rôle et ne connaît pas les autres. Le module GRBL
publie la position, l'interface web et l'écran s'y abonnent (plus de variables globales partagées).

## 3. Les modules

### 3.1 Pilote GRBL (`machine/`)
Le cœur du système, celui qui doit être le plus solide.
- **Envoi du G-code** par comptage de caractères (tampon série GRBL de 128 octets) :
  mouvements fluides, pas de pause entre les lignes, aucune ligne envoyée deux fois.
- **Position en temps réel** : requête `?` ~5 fois/s, publication de la position et de l'état
  (`Idle`, `Run`, `Hold`, `Alarm`).
- **Commandes immédiates** : pause (`!`), reprise (`~`), reset (`Ctrl-X`), override de vitesse (±10 %).
- **Homing** (`$H`), déblocage d'alarme (`$X`), lecture/écriture des réglages `$$`.
- **Simulateur GRBL** en Python, qui répond comme le vrai : développement et tests sur PC sans la table.

### 3.2 Traitement du G-code (`gcode/`)
- **Nettoyage** : suppression des commentaires et lignes vides, rejet des coordonnées hors limites.
- **Mise à l'échelle** : adapter un motif 250×250 à la surface réelle (270×300).
- **Prévisualisation** : extraction du tracé → miniature SVG / affichage navigateur.
- **Estimation** de la durée et de la distance parcourue.
- **Conversion `.thr`** (coordonnées polaires, format Sisyphus) → accès aux motifs de la communauté.

### 3.3 Bibliothèque de motifs (`patterns/`)
- Fichiers sur disque + métadonnées dans SQLite : nom, miniature, durée, catégories, favoris, nb de passages.
- Upload `.gcode` / `.thr` depuis l'interface web.
- **Générateurs intégrés** paramétrables : spirales, rosaces, Lissajous, Hilbert, aléatoire.
- **Effaceurs** : `WiperCircle`, `WiperLine`, `WiperHil4` comme catégorie à part.

### 3.4 Lecteur et file d'attente (`player/`)
- File de motifs : lecture, pause, suivant, arrêt.
- Playlists, aléatoire, répétition.
- **Effaceur automatique** entre deux motifs (optionnel).
- Avancement en %, temps restant, reprise après coupure de courant.

### 3.5 Capteurs et contexte (`sensors/`)
- Température / humidité (conseil : remplacer le DHT11 par un BME280 en I²C).
- PIR (GPIO4) → événements « présence » / « absence ».
- Météo **en cache** (1 requête / 10 min), timeout sur la requête, clé API dans `.env`.

### 3.6 Écran (`display/`)
- **Option A — garder l'Arduino + TFT** avec un vrai protocole : JSON lines (`\n`) dans les deux sens.
  Ex. `{"k":"temp","v":"21.5"}` vers l'écran, `{"btn":"pause"}` depuis l'écran
  → les boutons tactiles peuvent commander la table.
- **Option B — écran tactile branché sur le Pi** (DSI/HDMI) affichant l'interface web en mode kiosque.
  Plus de second Arduino ni de protocole à maintenir.

Recommandation : A pour la v1 (le matériel existe), B si l'électronique est refaite.

### 3.7 Alimentation et ambiance (`power/`)
- Veille écran/moteurs via `uhubctl` selon des règles : absence depuis X minutes, plage horaire de nuit.
- Option : ruban LED adressable (WS2812) autour du sable, effets liés à l'état (dessin, pause, veille).

### 3.8 API et interface web (`api/`, `web/`)
- **REST** : `/patterns`, `/queue`, `/machine/{home,pause,resume,stop,jog}`, `/settings`, `/sensors`.
- **WebSocket** `/ws` : position, état et capteurs en direct.
- **Pages** :
  - Tableau de bord : dessin en direct de la bille et de sa trace, motif en cours, avancement, contrôles.
  - Bibliothèque : grille de miniatures, recherche, upload.
  - File d'attente et playlists.
  - Commande manuelle : jog, homing, console G-code.
  - Réglages : limites de la table, vitesses, ports, plages horaires.
- Utilisable sur téléphone, installable (PWA).

## 4. Choix techniques

| Sujet | Recommandation | Pourquoi |
|---|---|---|
| Langage | Python 3.11+ | Continuité avec la v1, `fullcontrol` reste utilisable |
| Serveur web | FastAPI + uvicorn | Asynchrone, WebSocket intégré, doc d'API automatique |
| Port série | `pyserial-asyncio` | S'intègre à la boucle asynchrone, sans threads |
| Configuration | `pydantic-settings` + `.env` + `config.yaml` | Plus de clé ni de port en dur |
| Stockage | SQLite (SQLModel) | Rien à installer, suffisant |
| Interface web | Svelte, ou HTMX + Alpine (plus léger) | Le canevas temps réel demande un peu de JS |
| Ports série | `/dev/serial/by-id/...` | Plus de détection qui teste tous les ports et reset les Arduino |
| Démarrage | Service `systemd` | Lancement au boot, redémarrage auto |
| Qualité | `pytest` (+ simulateur GRBL), `ruff`, `logging` | Tests sans la table |

## 5. Organisation du dépôt

```
sand-table/
├── README.md                 # présentation, photos, câblage, installation
├── docs/                     # architecture, câblage, protocole écran
├── hardware/                 # modèles 3D (STL/STEP), schémas, liste des pièces
├── firmware/
│   ├── grbl/                 # réglages $$ sauvegardés et notes
│   └── display/              # sketch écran (protocole JSON lines)
├── server/
│   ├── pyproject.toml
│   ├── sandtable/
│   │   ├── main.py           # démarrage, création des modules
│   │   ├── config.py
│   │   ├── events.py         # bus d'événements
│   │   ├── machine/          # pilote GRBL + simulateur
│   │   ├── gcode/            # nettoyage, mise à l'échelle, aperçu, conversion .thr
│   │   ├── patterns/         # bibliothèque + générateurs
│   │   ├── player/           # file d'attente, playlists
│   │   ├── sensors/
│   │   ├── display/
│   │   ├── power/
│   │   └── api/              # REST + WebSocket
│   └── tests/
├── web/                      # interface web
├── patterns/                 # fichiers .gcode actuels
└── deploy/                   # service systemd, script d'installation
```

## 6. Fonctionnalités par priorité

**Essentiel (v1)**
- Lancer un motif depuis le téléphone : pause, reprise, arrêt
- Homing, gestion des alarmes, commande manuelle
- Position en direct sur l'interface
- Bibliothèque avec miniatures et upload
- File d'attente avec effaceur automatique

**Confort**
- Playlists, aléatoire, mode « dessine en continu »
- Plages horaires (silence la nuit), veille en cas d'absence
- Override de vitesse, estimation du temps restant
- Écran TFT : motif en cours + boutons de commande
- Éclairage LED

**Bonus**
- Dessin libre au doigt sur le téléphone, reproduit par la table
- Écriture de texte (polices Hershey à un seul trait)
- Mode horloge : la table dessine l'heure toutes les heures
- Motifs selon la météo
- Image → tracé continu
- Intégration Home Assistant
- Statistiques : distance parcourue, motifs les plus joués

## 7. Feuille de route

1. **Socle** : nouvelle organisation du dépôt, configuration, simulateur GRBL, pilote GRBL fiable, tests.
   → jouer un motif proprement en ligne de commande.
2. **Lecteur et API** : file d'attente, bibliothèque, REST + WebSocket.
3. **Interface web** : tableau de bord temps réel, bibliothèque, commandes.
4. **Contexte** : capteurs, présence, veille, nouveau protocole écran.
5. **Bonus**, au choix.
