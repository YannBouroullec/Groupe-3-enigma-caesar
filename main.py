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


def enigma_dechiffrer(message: str, cles) -> str:
	"""Déchiffre un message chiffré par Enigma César.

	Comme pour César, déchiffrer revient à chiffrer avec les clés opposées.
	On garantit ainsi que
	`enigma_dechiffrer(enigma_chiffrer(m, k), k) == m`.

	Paramètres :
		message (str)        : le texte chiffré à déchiffrer.
		cles (tuple ou list) : les 3 entiers utilisés lors du chiffrement.

	Retour :
		str : le message en clair.

	Exemple :
		>>> enigma_dechiffrer("TQRZEW", (7, 16, 9))
		'MAISON'
	"""
	# Inverser chaque cle revient a dechiffrer.
	cles_inversees = tuple(-c for c in cles)
	return enigma_chiffrer(message, cles_inversees)

def lire_fichier(chemin: str) -> str:
	"""Lit le contenu d'un fichier texte (encodage UTF-8).

	Affiche un message d'erreur clair si le fichier est introuvable
	ou illisible, et relance l'exception pour que l'appelant puisse
	décider quoi faire (sortir du programme, demander un autre nom...).

	Paramètre :
		chemin (str) : chemin vers le fichier à lire (relatif ou absolu).

	Retour :
		str : contenu intégral du fichier.

	Lève :
		FileNotFoundError : si le fichier n'existe pas.
		PermissionError   : si le fichier n'est pas lisible.
	"""
	try:
		with open(chemin, "r", encoding="utf-8") as f:
			return f.read()
	except FileNotFoundError:
		print(f"Erreur : le fichier '{chemin}' est introuvable.")
		raise
	except PermissionError:
		print(f"Erreur : permission refusee pour lire '{chemin}'.")
		raise


def ecrire_fichier(chemin: str, contenu: str) -> None:
	"""Écrit du texte dans un fichier (encodage UTF-8).

	Crée le fichier s'il n'existe pas, écrase son contenu s'il existe déjà.
	Affiche un message d'erreur clair en cas de problème d'écriture.

	Paramètres :
		chemin (str)  : chemin du fichier à écrire.
		contenu (str) : texte à écrire.

	Lève :
		PermissionError : si le fichier ne peut pas être écrit.
	"""
	try:
		with open(chemin, "w", encoding="utf-8") as f:
			f.write(contenu)
	except PermissionError:
		print(f"Erreur : permission refusee pour ecrire dans '{chemin}'.")
		raise

def mode_interactif() -> None:
	"""Lance un menu console guidé pour l'utilisateur.

	Activé quand le programme est lancé sans arguments en ligne de commande.
	L'utilisateur choisit l'opération, saisit son message et sa clé,
	et le résultat est affiché. Aucune connaissance d'argparse requise.
	"""
	print("=" * 50)
	print("  Mini-Projet A : Chiffrement de Cesar / Enigma")
	print("=" * 50)
	print()
	print("Que souhaitez-vous faire ?")
	print("  1. Chiffrer un message (Cesar)")
	print("  2. Dechiffrer un message (Cesar)")
	print("  3. Chiffrer un message (Enigma Cesar)")
	print("  4. Dechiffrer un message (Enigma Cesar)")
	print("  0. Quitter")
	print()

	choix = input("Votre choix : ").strip()
	if choix == "0":
		print("Au revoir.")
		return

	if choix not in ("1", "2", "3", "4"):
		print(f"Erreur : choix '{choix}' invalide.")
		return

	# Saisie du message (au clavier ou depuis un fichier).
	source = input("Lire le message depuis un fichier ? (o/N) : ").strip().lower()
	if source == "o":
		chemin = input("Chemin du fichier : ").strip()
		try:
			message = lire_fichier(chemin)
		except (FileNotFoundError, PermissionError):
			return
	else:
		message = input("Message : ")

	# Saisie de la cle, format different selon Cesar ou Enigma.
	if choix in ("1", "2"):
		texte_cle = input("Cle (entier, ex. 42 ou -42) : ").strip()
	else:
		texte_cle = input("Cle Enigma (3 entiers separes par '-', ex. 7-16-9) : ").strip()

	try:
		cle = _parse_cle(texte_cle)
	except ValueError:
		print(f"Erreur : cle '{texte_cle}' invalide.")
		return

	# Execution de l'operation choisie.
	try:
		if choix == "1":
			resultat = chiffrer(message, cle)
		elif choix == "2":
			resultat = dechiffrer(message, cle)
		elif choix == "3":
			resultat = enigma_chiffrer(message, cle)
		else:  # choix == "4"
			resultat = enigma_dechiffrer(message, cle)
	except ValueError as erreur:
		print(f"Erreur : {erreur}")
		return

	print()
	print("Resultat :")
	print(resultat)


# Liste des mots français les plus fréquents.
# Utilisée par score_francais pour évaluer la "francité" d'un texte.
# Source : mots les plus fréquents de la langue française (articles, prépositions, auxiliaires).
_MOTS_FRANCAIS_COURANTS = (
	"le", "la", "les", "un", "une", "des",
	"de", "du", "et", "ou", "a", "au", "aux",
	"est", "sont", "etait", "ete",
	"que", "qui", "quoi", "dont",
	"je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
	"ce", "cet", "cette", "ces",
	"mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
	"pas", "ne", "plus", "tres", "bien",
	"dans", "sur", "pour", "par", "avec", "sans",
	"mais", "donc", "car",
)


def score_francais(texte: str) -> int:
	"""Évalue à quel point un texte ressemble à du français.

	On découpe le texte en mots (en minuscules) et on compte combien
	d'entre eux figurent dans une liste de mots français très fréquents.
	Plus le score est élevé, plus le texte est probablement du français.

	Cette fonction est volontairement simple : pas de regex, pas de NLP,
	juste du comptage. Elle est utilisée pour classer les candidats
	produits par le brute-force.

	Paramètre :
		texte (str) : le texte à évaluer.

	Retour :
		int : nombre de mots courants trouvés (>= 0).

	Exemple :
		>>> score_francais("le chat est sur la table")
		4  # "le", "est", "sur", "la"
	"""
	# On passe en minuscules et on remplace la ponctuation par des espaces
	# pour que "Bonjour," et "Bonjour" soient traites pareil.
	texte_propre = texte.lower()
	for ponctuation in ".,;:!?\"'()[]{}":
		texte_propre = texte_propre.replace(ponctuation, " ")

	# Comptage : on parcourt chaque mot et on regarde s'il est dans la liste.
	mots_du_texte = texte_propre.split()
	score = sum(1 for mot in mots_du_texte if mot in _MOTS_FRANCAIS_COURANTS)
	return score


def brute_force_cesar(message_chiffre: str, top_n: int = 3):
	"""Tente de déchiffrer un message César en testant toutes les clés.

	Le chiffrement de César n'a que 26 clés possibles (0 à 25). On les
	teste toutes, on évalue chaque résultat avec score_francais, et on
	retourne les `top_n` meilleurs candidats triés par score décroissant.

	Le premier élément de la liste retournée est la meilleure proposition
	automatique. Les suivants permettent à l'utilisateur de choisir si
	l'automatique se trompe (rare avec un texte français de taille raisonnable).

	Paramètres :
		message_chiffre (str) : le texte chiffré à casser.
		top_n (int)           : nombre de candidats à retourner (3 par défaut).

	Retour :
		list de tuples (score, cle, message_dechiffre), trié du meilleur au pire.

	Exemple :
		>>> resultats = brute_force_cesar("Ludy, lyty, lysy!")
		>>> resultats[0][1]  # la clé trouvée
		42
	"""
	candidats = []
	# 26 cles possibles : 0, 1, 2, ..., 25.
	# Une cle de 42 est equivalente a une cle de 42 % 26 = 16, donc
	# tester 0 a 25 couvre toutes les possibilites.
	for cle in range(26):
		essai = dechiffrer(message_chiffre, cle)
		score = score_francais(essai)
		candidats.append((score, cle, essai))

	# Tri par score decroissant : le meilleur candidat en premier.
	candidats.sort(key=lambda c: c[0], reverse=True)
	return candidats[:top_n]


def brute_force_enigma(message_chiffre: str, top_n: int = 3):
	"""Tente de déchiffrer un message Enigma César en testant toutes les clés.

	Enigma César a 26³ = 17 576 combinaisons de clés possibles. On les
	teste toutes (version naïve), on évalue chaque résultat avec
	score_francais, et on retourne les `top_n` meilleurs candidats.

	Cette version est volontairement simple pour servir de référence
	dans le rapport de performance. Voir brute_force_enigma_optimise
	pour une version plus rapide.

	Paramètres :
		message_chiffre (str) : le texte chiffré à casser.
		top_n (int)           : nombre de candidats à retourner.

	Retour :
		list de tuples (score, cles, message_dechiffre), trié du meilleur au pire.
		`cles` est un tuple (a, b, c).
	"""
	candidats = []
	# Trois boucles imbriquees : 26 * 26 * 26 = 17 576 essais.
	for a in range(26):
		for b in range(26):
			for c in range(26):
				cles = (a, b, c)
				essai = enigma_dechiffrer(message_chiffre, cles)
				score = score_francais(essai)
				candidats.append((score, cles, essai))

	# Tri par score decroissant.
	candidats.sort(key=lambda candidat: candidat[0], reverse=True)
	return candidats[:top_n]


def brute_force_enigma_optimise(message_chiffre: str, top_n: int = 3, taille_echantillon: int = 100):
	"""Version optimisée du brute-force Enigma : ne score que le début du texte.

	L'idée : pour un texte de plusieurs centaines de caractères, scorer
	intégralement chacun des 17 576 candidats est coûteux. En pratique,
	les ~100 premiers caractères suffisent à départager les bonnes clés
	des mauvaises (un vrai texte français y aura plusieurs mots courants ;
	un texte aléatoire n'en aura aucun).

	On déchiffre quand même le message complet une fois la meilleure clé
	identifiée, pour que l'utilisateur reçoive le texte intégral.

	Paramètres :
		message_chiffre (str)     : le texte chiffré à casser.
		top_n (int)               : nombre de candidats à retourner.
		taille_echantillon (int)  : nombre de caractères évalués par essai.

	Retour :
		list de tuples (score, cles, message_dechiffre_complet).
	"""
	# Echantillon = les N premiers caracteres du message chiffre.
	echantillon = message_chiffre[:taille_echantillon]

	candidats = []
	for a in range(26):
		for b in range(26):
			for c in range(26):
				cles = (a, b, c)
				# On dechiffre uniquement l'echantillon pour gagner du temps.
				essai_court = enigma_dechiffrer(echantillon, cles)
				score = score_francais(essai_court)
				candidats.append((score, cles))

	candidats.sort(key=lambda candidat: candidat[0], reverse=True)

	# Pour les top_n meilleurs, on dechiffre le message complet.
	resultats = []
	for score, cles in candidats[:top_n]:
		message_complet = enigma_dechiffrer(message_chiffre, cles)
		resultats.append((score, cles, message_complet))
	return resultats


def _parse_cle(texte: str):
	"""Convertit l'argument --cle en clé utilisable.

	Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
	et la transforme en type Python approprié :
	- César           : un entier, ex. "42" ou "-42"
	- Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9"

	Paramètre :
		texte (str) : la chaîne saisie par l'utilisateur après --cle.

	Retour :
		int   : une clé entière pour César.
		tuple : un tuple de 3 entiers pour Enigma César.

	Lève :
		ValueError : si la chaine n'est ni un entier valide,
		             ni un triplet valide d'entiers separes par "-".

	Exemple :
		_parse_cle("42") → 42 (int)
		_parse_cle("7-16-9") → (7, 16, 9) (tuple)
	"""
	# Verifier s'il y a un tiret dans la cle (sauf si c'est juste un signe negatif).
	# lstrip("-") enleve tous les tirets au debut, pour distinguer :
	#   "-42" (entier negatif, pas de tiret apres le signe)
	#   "7-16-9" (trois nombres separes par des tirets)
	if "-" in texte.lstrip("-"):
		# Cle Enigma : on coupe au "-" et on convertit en entiers.
		morceaux = texte.split("-")
		if len(morceaux) != 3:
			raise ValueError(
				f"La cle Enigma doit contenir exactement 3 nombres separes par '-', "
				f"{len(morceaux)} fourni(s) dans '{texte}'."
			)
		try:
			return tuple(int(x) for x in morceaux)
		except ValueError:
			raise ValueError(f"La cle Enigma '{texte}' contient un element non entier.")
	# Cle Cesar simple : on convertit en entier.
	try:
		return int(texte)
	except ValueError:
		raise ValueError(f"La cle '{texte}' n'est pas un entier valide.")

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
	
	# Argument optionnel "--fichier" (abreviation "-f") : lit le message depuis un fichier.
	# Si fourni, le contenu du fichier remplace l'argument "message".
	parser.add_argument(
		"-f", "--fichier",
		help="Chemin d'un fichier texte a chiffrer/dechiffrer (UTF-8).")

	# Argument optionnel "--sortie" (abreviation "-o") : ecrit le resultat dans un fichier.
	# Si non fourni, le resultat est affiche dans la console (comportement par defaut).
	parser.add_argument(
		"-o", "--sortie",
		help="Chemin du fichier de sortie (sinon affichage console).")
	
	# Argument optionnel "--brute-force" (abreviation "-b") : tente de casser le chiffrement.
	# Quand active, la cle n'est pas necessaire (on la cherche).
	parser.add_argument(
		"-b", "--brute-force", action="store_true",
		help="Mode brute-force : retrouve la cle automatiquement (top 3 candidats).")

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
		"-c", "--cle", required=False,
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
	# Si on est en mode brute-force, on n'a pas besoin de cle ; sinon elle est obligatoire.
	if args.brute_force:
		cle = None
	else:
		if args.cle is None:
			parser.error("l'argument --cle est obligatoire (sauf en mode --brute-force).")
		cle = _parse_cle(args.cle)

	# Si --fichier est fourni, on lit le message depuis le fichier
	# au lieu d'utiliser l'argument "message" de la ligne de commande.
	if args.fichier:
		try:
			args.message = lire_fichier(args.fichier)
		except (FileNotFoundError, PermissionError):
			# lire_fichier a deja affiche un message d'erreur clair.
			return  # On sort proprement, sans pile d'erreur visible a l'utilisateur.

	# === ÉTAPE 5 : Choisir et exécuter l'opération ===
	# Selon l'action, on appelle la fonction appropriée.
	# (Une fois que chiffrer / dechiffrer / enigma_chiffrer seront implémentées,
	#  ces appels retourneront le résultat du chiffrement/déchiffrement.)

	# Branchement vers la bonne fonction selon l'action et le mode.
	if args.brute_force:
		# Mode brute-force : on cherche la cle au lieu d'en utiliser une.
		if args.action == "enigma":
			candidats = brute_force_enigma_optimise(args.message)
		else:
			# Pour "chiffrer" et "dechiffrer", on utilise brute_force_cesar.
			candidats = brute_force_cesar(args.message)

		# Affichage du top 3 : score, cle, debut du message.
		print("Top 3 des candidats (score, cle, debut du texte) :")
		for score, cle_trouvee, texte in candidats:
			extrait = texte[:60].replace("\n", " ")
			print(f"  score={score:3d}  cle={cle_trouvee}  texte='{extrait}...'")
		# Le premier candidat est la meilleure proposition.
		resultat = candidats[0][2]
	elif args.action == "chiffrer":
		resultat = chiffrer(args.message, cle)
	elif args.action == "dechiffrer":
		resultat = dechiffrer(args.message, cle)
	else:  # args.action == "enigma"
		resultat = enigma_chiffrer(args.message, cle)

	# === ÉTAPE 6 : Afficher le résultat ===
	# print() affiche le résultat à l'écran pour que l'utilisateur le voie.
	# Si --sortie est fourni, on ecrit dans le fichier ; sinon on affiche.
	if args.sortie:
		try:
			ecrire_fichier(args.sortie, resultat)
			print(f"Resultat ecrit dans '{args.sortie}'.")
		except PermissionError:
			return
	else:
		print(resultat)
	
	# TODO : Une fois les fonctions de base implémentées, vous pourrez :
	# - Ajouter des options pour lire/écrire depuis des fichiers
	# - Implémenter le mode brute-force
	# - Ajouter d'autres fonctionnalités


if __name__ == "__main__":
	# Si aucun argument fourni en ligne de commande, lancer le mode interactif.
	# sys.argv[0] est toujours le nom du script ; les vrais arguments commencent a sys.argv[1].
	import sys
	if len(sys.argv) == 1:
		mode_interactif()
	else:
		main()

