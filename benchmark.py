"""Mesures de performance des brute-force.

Ce script est destiné au rapport. Il compare la version naïve et la
version optimisée d'Enigma sur un même message, et imprime les temps
en secondes.

Usage :
	python benchmark.py
"""
from time import perf_counter
from main import (
	chiffrer,
	enigma_chiffrer,
	brute_force_cesar,
	brute_force_enigma,
	brute_force_enigma_optimise,
)


def chronometrer(fonction, *args, repetitions: int = 1):
	"""Mesure le temps moyen d'exécution d'une fonction.

	Lance `fonction(*args)` plusieurs fois et retourne la moyenne
	pour lisser les variations dues à la charge système.
	"""
	temps_total = 0.0
	for _ in range(repetitions):
		tic = perf_counter()
		fonction(*args)
		toc = perf_counter()
		temps_total += (toc - tic)
	return temps_total / repetitions


if __name__ == "__main__":
	# Message de reference (assez long pour que le score soit fiable).
	message_clair = (
		"Bonjour le monde, ceci est un message de test pour le brute-force. "
		"Il contient plusieurs mots francais courants comme le, la, et, de, "
		"qui permettent au score de bien fonctionner sur les candidats."
	)

	# --- Brute-force Cesar ---
	cle_cesar = 7
	message_chiffre_cesar = chiffrer(message_clair, cle_cesar)

	temps_cesar = chronometrer(brute_force_cesar, message_chiffre_cesar, repetitions=10)
	print(f"Brute-force Cesar (26 cles, 10 repetitions)        : {temps_cesar*1000:.2f} ms")

	# --- Brute-force Enigma naif ---
	cles_enigma = (7, 16, 9)
	message_chiffre_enigma = enigma_chiffrer(message_clair, cles_enigma)

	temps_enigma_naif = chronometrer(brute_force_enigma, message_chiffre_enigma, repetitions=3)
	print(f"Brute-force Enigma naif (17576 cles, 3 repetitions): {temps_enigma_naif:.2f} s")

	# --- Brute-force Enigma optimise ---
	temps_enigma_opt = chronometrer(brute_force_enigma_optimise, message_chiffre_enigma, repetitions=3)
	print(f"Brute-force Enigma optimise (echantillon 100 char) : {temps_enigma_opt:.2f} s")

	gain = (1 - temps_enigma_opt / temps_enigma_naif) * 100
	print(f"\nGain de la version optimisee : {gain:.1f} %")