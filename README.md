# Mini-Projet A — Chiffrement de César & Enigma César

Mini-projet du cours MGA802 (ÉTS, été 2026). Un programme Python qui chiffre et déchiffre des messages selon deux algorithmes — le chiffrement de César et une version simplifiée d'Enigma à trois clés rotatives — avec un mode brute-force pour casser un chiffré dont on ignore la clé.

## Équipe

- Yann Bouroullec — interface, fichiers, CLI, mode interactif
- Théo Malavieille — fonctions de chiffrement César et Enigma
- Pierre-Jean Tulasne — brute-force et mesures de performance

## Ce que le programme fait

Deux chiffrements :

- **César** décale chaque lettre du message d'un nombre constant de positions. La clé est un entier (positif, négatif, peu importe, on s'en sort avec un modulo).
- **Enigma César** utilise trois clés `(a, b, c)` appliquées tour à tour, lettre par lettre. Plus dur à casser que César parce qu'il faut deviner les trois nombres au lieu d'un seul.

Deux façons de l'utiliser :

- Une **ligne de commande** avec argparse (options `--fichier`, `--sortie`, `--brute-force`).
- Un **menu interactif** qui se lance quand on exécute `main.py` sans aucun argument.

## Installation

Python 3.14 et `pytest` pour les tests. C'est tout.

```bash
git clone <url-du-depot>
cd <nom-du-projet>
pip install -r requirements.txt
```

## Utilisation

### Mode interactif

Le plus simple. Tu lances :

```bash
python main.py
```

Et tu suis le menu (chiffrer ou déchiffrer, César ou Enigma, message au clavier ou depuis un fichier).

### Ligne de commande

**Chiffrer et déchiffrer en César :**

```bash
python main.py chiffrer   "Veni, vidi, vici!" --cle 42
python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
```

**Enigma César** (trois entiers séparés par des tirets) :

```bash
python main.py enigma "MAISON" --cle 7-16-9
```

**Lire un fichier au lieu de saisir le message** :

```bash
python main.py chiffrer --cle 42 --fichier message.txt
```

**Écrire le résultat dans un fichier** :

```bash
python main.py chiffrer "Veni, vidi, vici!" --cle 42 --sortie chiffre.txt
```

**Retrouver la clé toute seule** (brute-force) :

```bash
python main.py chiffrer "Ivuqvby sl tvukl, jljp lza bu tlzzhnl..." --brute-force
python main.py enigma   "QXJUNHA WO QYFCXV PMRTW..."                --brute-force
```

Le programme affiche le top 3 des candidats classés par ressemblance au français, puis imprime le meilleur.

Pour voir toutes les options : `python main.py -h`.

## Choix de conception

Quelques décisions à connaître :

- Les fichiers sont lus et écrits en **UTF-8**.
- Les **lettres accentuées** (é, à, ç, ñ...) ne sont pas décalées, elles restent telles quelles dans le message chiffré. On ne décale que `a-z` et `A-Z`. La casse est préservée.
- Dans Enigma, le **compteur de position n'avance que sur les lettres**. Un espace ou une virgule ne consomme pas de clé. Donc `chiffrer("MA SON", (7,16,9))` applique les clés `7, 16, 9, 7, 16` aux 5 lettres `M, A, S, O, N`, comme si l'espace n'existait pas.
- Le **modulo 26** sur les clés gère tout : `42` est équivalent à `16`, `-42` à `10`, et `1000` à `12`. Pas besoin de borner l'entrée utilisateur.
- Le **brute-force évalue la "francité"** d'un candidat en comptant les mots français courants (`le`, `la`, `et`, `de`, `est`...). C'est rudimentaire mais ça suffit pour des textes français de taille normale. Ça ne marche pas sur du latin (Veni, vidi, vici), du texte très court, ou autre chose que du français — limite assumée et discutée dans le rapport.

## Tests

11 tests unitaires dans `tests/test_caesar.py`. Pour les lancer :

```bash
pytest -v
```

Ils couvrent : chiffrement César avec clés positives, négatives, nulles et géantes, chiffrement Enigma, round-trip (chiffrer puis déchiffrer doit redonner le message d'origine), conservation des accents et de la casse, rejet d'une clé Enigma qui n'a pas exactement 3 nombres, et validation du brute-force sur César et Enigma.

Pour les mesures de performance, le script `benchmark.py` chronomètre le brute-force César, le brute-force Enigma naïf et la version Enigma optimisée :

```bash
python benchmark.py
```

## Structure

```
.
├── main.py            # toutes les fonctions, l'interface CLI, le mode interactif
├── benchmark.py       # mesures de performance
├── tests/
│   └── test_caesar.py # 11 tests unitaires
├── message.txt        # fichier d'exemple pour tester --fichier
├── requirements.txt
├── README.md
└── .editorconfig
```

Dans `main.py` les fonctions sont groupées en quatre sections :

1. Brique de base : `_decaler_lettre`.
2. Chiffrements : `chiffrer`, `dechiffrer`, `enigma_chiffrer`, `enigma_dechiffrer`.
3. Fichiers et interface : `lire_fichier`, `ecrire_fichier`, `mode_interactif`.
4. Brute-force : `score_francais`, `brute_force_cesar`, `brute_force_enigma`, `brute_force_enigma_optimise`.

## Méthode de travail

On a suivi le workflow Git du cours : une branche par fonctionnalité (`feat/chiffrement`, `feat/brute-force`, `feat/interface`), une Pull Request pour chaque, et merge dans `main` seulement après revue par un autre coéquipier. On a aussi fait tourner les rôles pour que personne ne teste son propre code.