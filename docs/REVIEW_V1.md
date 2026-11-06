# Revue du code v1

> Constat sur le code existant, servant de base à la v2 (voir `ARCHITECTURE.md`). Rien n'a été corrigé.

## À traiter en priorité

1. **Clé API OpenWeather en clair** (`raspyFiles/MyValues.py:9`), présente dans l'historique git
   d'un dépôt public → **à révoquer**, puis à placer dans une variable d'environnement.
2. **Trop d'appels à l'API météo** : `getWeather()` appelle `getWeatherFromWeb()` deux fois, chaque
   seconde (~170 000 requêtes/jour). `requests.get` sans `timeout`. Le DHT11 est aussi lu deux fois.
3. **Flask `debug=True` sur `0.0.0.0`** : le débogueur Werkzeug permet d'exécuter du code depuis le réseau
   local. Le reloader exécute `main.py` deux fois (uhubctl, port série et thread écran en double).

## Bugs

- `main.py` `/toggle` : deux `if` successifs au lieu d'un `elif` → l'écran se rallume aussitôt.
  Après `turnArdOff()`, le port série n'est pas rouvert par `turnArdOn()`.
- `testSand.py` `addSteps("G1 X0 Y0 F2500")` : une chaîne passée à `extend` ajoute les caractères un par
  un → en quittant, la table reçoit `"G"`.
- `testSand.py` `trySending()` : si le `ok` arrive après le timeout, la ligne est renvoyée (mouvement
  doublé). Commentaires `;` et lignes vides envoyés tels quels.
- `wait_for_movement_completion` : `cleaned_line != '$X' or '$$'` est toujours vrai.
- `sendValuesToArduino` : `while len(read_all()) == 0` bloque indéfiniment si l'Arduino ne répond pas.
- `screen.ino` `barMenu()` : `for (int k; …)` → `k` non initialisé.
- `screen.ino` `swiping()` : pour un petit glissement les deux `if` sont vrais → le menu recule puis avance.
- `screen.ino` protocole série sans séparateur : deux messages arrivés ensemble sont fusionnés.
  20 `String` sur un Uno (2 Ko de RAM) avec la lib TFT : risqué.
- `index.html` : `<form>` dans `<head>`, route `/envoyer_commande` inexistante, `top`/`left` inversés (X/Y).

## Organisation du dépôt

- Pas de `.gitignore` → `__pycache__/*.pyc` commités.
- README : dossier `3DFiles` mentionné mais absent ; pas de câblage, `requirements.txt` ni installation ;
  coquilles (« artuino », « patern », « raspiFiles »).
- `find_port()` ouvre tous les ports série pour les tester (reset des Arduino) →
  préférer `/dev/serial/by-id/...`.
