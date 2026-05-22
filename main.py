"""
MGA802 — Mini-Projet A : Chiffrement de César
Squelette de départ pour votre équipe.
"""
import argparse

def _decaler_lettre(lettre: str, decalage: int) -> str:
    """Décale une lettre de l'alphabet d'un nombre donné de positions.

    Brique de base utilisée par César et Enigma César. La fonction gère
    automatiquement les clés négatives et les clés supérieures à 26 grâce
    à l'opérateur modulo. La casse (majuscule/minuscule) est préservée.
    Les caractères qui ne sont pas des lettres ASCII (espaces, ponctuation,
    chiffres, lettres accentuées) sont retournés inchangés.

    Paramètres :
        lettre (str)   : un seul caractère à décaler.
        decalage (int) : nombre de positions à décaler (peut être négatif).

    Retour :
        str : la lettre décalée, ou le caractère original si non alphabétique.
    """
    # Determiner la base ASCII selon la casse de la lettre.
    if "a" <= lettre <= "z":
        base = ord("a")
    elif "A" <= lettre <= "Z":
        base = ord("A")
    else:
        # Caractere non alphabetique ASCII : on le laisse inchange.
        return lettre

    # Position dans l'alphabet (0 a 25), application du decalage modulo 26.
    position = ord(lettre) - base
    nouvelle_position = (position + decalage) % 26
    return chr(base + nouvelle_position)

def chiffrer(message: str, cle: int) -> str:
	"""Chiffre un message avec le chiffrement de César.

	Chaque lettre de l'alphabet ASCII est décalée de `cle` positions.
	Les caractères non alphabétiques (espaces, ponctuation, accents)
	sont laissés inchangés. La casse est préservée.

	Paramètres :
		message (str) : le texte clair à chiffrer.
		cle (int)     : entier de décalage (positif ou négatif).

	Retour :
		str : le message chiffré.

	Exemples :
		>>> chiffrer("Veni, vidi, vici!", 42)
		'Ludy, lyty, lysy!'
		>>> chiffrer("Veni, vidi, vici!", -42)
		'Foxs, fsns, fsms!'
		>>> chiffrer("Tout pareil.", 0)
		'Tout pareil.'
	"""
	# On applique _decaler_lettre a chaque caractere et on reassemble.
	return "".join(_decaler_lettre(c, cle) for c in message)


def dechiffrer(message: str, cle: int) -> str:
	"""Déchiffre un message chiffré par César.

	Déchiffrer revient à chiffrer avec la clé opposée. On délègue donc
	à `chiffrer` avec `-cle`, ce qui garantit que
	`dechiffrer(chiffrer(m, k), k) == m`.

	Paramètres :
		message (str) : le texte chiffré à déchiffrer.
		cle (int)     : la clé utilisée lors du chiffrement.

	Retour :
		str : le message en clair.

	Exemple :
		>>> dechiffrer("Ludy, lyty, lysy!", 42)
		'Veni, vidi, vici!'
	"""
	return chiffrer(message, -cle)


def enigma_chiffrer(message: str, cles) -> str:
	"""Chiffre un message avec le chiffrement Enigma César (3 clés rotatives).

	La clé est composée de 3 entiers appliqués tour à tour, lettre par lettre :
	position 1 -> cles[0], position 2 -> cles[1], position 3 -> cles[2],
	position 4 -> cles[0], et ainsi de suite. Le compteur de position
	n'avance QUE sur les lettres : les espaces et la ponctuation ne
	consomment pas de clé.

	Paramètres :
		message (str)         : le texte clair à chiffrer.
		cles (tuple ou list)  : exactement 3 entiers (ex. (7, 16, 9)).

	Retour :
		str : le message chiffré.

	Lève :
		ValueError : si `cles` ne contient pas exactement 3 elements.

	Exemple :
		>>> enigma_chiffrer("MAISON", (7, 16, 9))
		'TQRZEW'
	"""
	# Validation : la cle Enigma doit avoir exactement 3 nombres.
	if len(cles) != 3:
		raise ValueError(
			f"La cle Enigma doit contenir exactement 3 nombres, "
			f"{len(cles)} fourni(s)."
		)

	resultat = []
	compteur_lettres = 0
	for caractere in message:
		# Le compteur n'avance que sur les lettres ASCII.
		if ("a" <= caractere <= "z") or ("A" <= caractere <= "Z"):
			cle_courante = cles[compteur_lettres % 3]
			resultat.append(_decaler_lettre(caractere, cle_courante))
			compteur_lettres += 1
		else:
			# Espaces, ponctuation, accents : inchanges, pas de consommation de cle.
			resultat.append(caractere)
	return "".join(resultat)


def _parse_cle(texte: str):
	"""Convertit l'argument --cle en clé utilisable.

	Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
	et la transforme en type Python approprié :
	- César           : un entier, ex. "42" ou "-42"
	- Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9"

	Paramètre :
		texte (str) : la chaîne saisie par l'utilisateur après --cle.

	Retour :
		int : une clé entière pour César
		tuple : un tuple de 3 entiers pour Enigma César

	Exemple :
		_parse_cle("42") → 42 (int)
		_parse_cle("7-16-9") → (7, 16, 9) (tuple)
	"""
	# Vérifier s'il y a un tiret dans la clé (sauf si c'est juste un signe négatif).
	# lstrip("-") enlève tous les tirets au début, pour distinguer :
	#   "-42" (entier négatif, pas de tiret après le signe)
	#   "7-16-9" (trois nombres séparés par des tirets)
	if "-" in texte.lstrip("-"):
		# Si oui, c'est une clé Enigma César : on coupe au niveau du "-" et on convertit en entiers.
		return tuple(int(x) for x in texte.split("-"))
	# Sinon, c'est une clé César simple : on convertit en entier.
	return int(texte)

def main(argv=None):
	"""Point d'entrée principal du programme en ligne de commande.

	Cette fonction :
	1. Parse les arguments saisis par l'utilisateur (action, message, clé)
	2. Convertit la clé en type approprié (int ou tuple)
	3. Appelle la fonction correspondante (chiffrer, dechiffrer ou enigma_chiffrer)
	4. Affiche le résultat

	Paramètre :
		argv (list ou None) : si None, utilise sys.argv (arguments de la console).
		                      si list, utilise les arguments fournis (utile pour les tests).

	Exemples d'utilisation en terminal :
		python main.py chiffrer "Veni, vidi, vici!" --cle 42
		python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
		python main.py enigma "MAISON" --cle 7-16-9
	"""
	# === ÉTAPE 1 : Créer et configurer le parseur d'arguments ===
	# argparse est un module qui aide à gérer les arguments en ligne de commande.
	# ArgumentParser crée un analyseur personnalisé pour notre programme.
	parser = argparse.ArgumentParser(
		description="Mini-Projet A : chiffrement de César / Enigma César.")

	# === ÉTAPE 2 : Définir les arguments attendus ===

	# Argument positionnel "action" : l'opération à effectuer.
	# - Obligatoire (pas de -- devant)
	# - Doit être l'une des valeurs listées dans "choices"
	parser.add_argument(
		"action",
		choices=["chiffrer", "dechiffrer", "enigma"],
		help="Opération à effectuer (chiffrer, dechiffrer ou enigma).")

	# Argument positionnel "message" : le texte à traiter.
	# - Obligatoire
	# - C'est la chaîne que nous allons chiffrer ou déchiffrer
	parser.add_argument(
		"message",
		help="Texte à traiter (mettez-le entre guillemets).")

	# Argument optionnel "--cle" (abréviation "-c") : la clé de chiffrement.
	# - Obligatoire via required=True
	# - Peut être un entier (César) ou trois entiers séparés par des tirets (Enigma César)
	parser.add_argument(
		"-c", "--cle", required=True,
		help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

	# === ÉTAPE 3 : Analyser les arguments ===
	# parse_args() transforme les arguments en un objet "Namespace" avec des attributs.
	# Si argv=None, il lit automatiquement depuis la ligne de commande.
	# Sinon, il utilise la liste fournie.
	args = parser.parse_args(argv)

	# Maintenant, on peut accéder aux arguments via :
	# - args.action (ex. "chiffrer")
	# - args.message (ex. "Veni, vidi, vici!")
	# - args.cle (ex. "42" ou "7-16-9", toujours en chaîne de caractères)

	# === ÉTAPE 4 : Convertir la clé (texte) en type approprié ===
	# _parse_cle() transforme la clé en int (César) ou tuple (Enigma).
	cle = _parse_cle(args.cle)

	# === ÉTAPE 5 : Choisir et exécuter l'opération ===
	# Selon l'action, on appelle la fonction appropriée.
	# (Une fois que chiffrer / dechiffrer / enigma_chiffrer seront implémentées,
	#  ces appels retourneront le résultat du chiffrement/déchiffrement.)

	if args.action == "chiffrer":
		# L'utilisateur veut chiffrer : on appelle chiffrer()
		resultat = chiffrer(args.message, cle)
	elif args.action == "dechiffrer":
		# L'utilisateur veut déchiffrer : on appelle dechiffrer()
		resultat = dechiffrer(args.message, cle)
	else:  # args.action == "enigma"
		# L'utilisateur veut utiliser Enigma César : on appelle enigma_chiffrer()
		resultat = enigma_chiffrer(args.message, cle)

	# === ÉTAPE 6 : Afficher le résultat ===
	# print() affiche le résultat à l'écran pour que l'utilisateur le voie.
	print(resultat)
	
	# TODO : Une fois les fonctions de base implémentées, vous pourrez :
	# - Ajouter des options pour lire/écrire depuis des fichiers
	# - Implémenter le mode brute-force
	# - Ajouter d'autres fonctionnalités


if __name__ == "__main__":
	# Ce bloc s'exécute SEULEMENT si ce fichier est lancé directement depuis le terminal.
	# Exemple : python main.py chiffrer "Veni" --cle 42
	#
	# Il ne s'exécute PAS si on fait "import main" depuis un autre fichier Python.
	# Cela permet d'utiliser le code de main.py dans d'autres projets sans lancer main().
	# 
	# Pour les tests : pytest importe ce fichier mais ne lance pas main()
	# (car __name__ ne vaut pas "__main__" lors d'un import).
	main()

