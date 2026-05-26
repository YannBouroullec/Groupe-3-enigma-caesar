"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""

import sys
import pytest  # <-- AJOUTÉ : Nécessaire pour détecter les levées de ValueError
from pathlib import Path

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))

# AJOUTÉ : On importe toutes les fonctions nécessaires au banc de test
from main import (  # noqa: E402
	chiffrer, 
	dechiffrer, 
	enigma_chiffrer, 
	enigma_dechiffrer, 
	brute_force_cesar, 
	brute_force_enigma_optimise
)

# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("MAISON", (7, 16, 9)) == "TQRZEW"


# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg


def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("Tout pareil.", 0) == "Tout pareil."


# TODO : ajoutez vos propres tests ci-dessous
#  - test pour les majuscules
#  - test pour les caractères spéciaux (accents, ponctuation)
#  - test pour les très grandes clés (positives et négatives)
#  - test pour le brute-force (César ET Enigma César)
#  - test que enigma_chiffrer rejette une clé qui n'a pas 3 nombres


# =====================================================================
# TESTS BONUS ADDITIONNELS (Couverture des cas limites)
# =====================================================================

def test_cesar_casse_melangee():
	"""Vérifie que la casse est préservée lors du chiffrement/déchiffrement."""
	message_original = "Hello World, Python est Super !"
	cle = 7
	chiffre = chiffrer(message_original, cle)
	assert chiffre != message_original
	assert dechiffrer(chiffre, cle) == message_original

def test_cesar_caracteres_speciaux_et_accents():
	"""Vérifie que les accents, la ponctuation et les chiffres restent inchangés."""
	message_original = "Montréal, élection en 2026 : un succès !"
	cle = 13
	chiffre = chiffrer(message_original, cle)
	assert "é" in chiffre
	assert "è" in chiffre
	assert ":" in chiffre
	assert "2026" in chiffre
	assert dechiffrer(chiffre, cle) == message_original

def test_cesar_cas_limites():
	"""Vérifie le comportement avec une chaîne vide, une clé nulle ou des clés géantes."""
	assert chiffrer("", 10) == ""
	assert chiffrer("Message Inchangé", 0) == "Message Inchangé"
	assert chiffrer("ABC", 55) == "DEF"
	assert chiffrer("ABC", -23) == "DEF"

def test_enigma_rejet_cle_invalide():
	"""Vérifie qu'une ValueError est bien levée si la clé n'a pas 3 nombres."""
	with pytest.raises(ValueError):
		enigma_chiffrer("MAISON", (7, 16))
	with pytest.raises(ValueError):
		enigma_dechiffrer("TQRZEW", [1, 2, 3, 4])

def test_brute_force_cesar_conforme():
	"""Vérifie que le brute-force César retrouve la bonne clé sur du français."""
	message_clair = "Le chat est sur la table et mange du poisson de manière très calme."
	cle_secrete = 14
	message_chiffre = chiffrer(message_clair, cle_secrete)
	candidats = brute_force_cesar(message_chiffre, top_n=3)
	assert candidats[0][1] == cle_secrete
	assert candidats[0][2] == message_clair

def test_brute_force_enigma_optimise_conforme():
	"""Vérifie que le brute-force Enigma optimisé identifie le triplet de clés."""
	message_clair = "Bonjour tout le monde ceci est un message secret avec plusieurs mots courants."
	cles_secretes = (3, 8, 12)
	message_chiffre = enigma_chiffrer(message_clair, cles_secretes)
	candidats = brute_force_enigma_optimise(message_chiffre, top_n=1)
	assert candidats[0][1] == cles_secretes
	assert candidats[0][2] == message_clair