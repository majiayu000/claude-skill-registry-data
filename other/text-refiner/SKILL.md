---
name: text-refiner
description: "Reformule les dictées vocales et textes bruts en français ou anglais sans changer le sens: retire répétitions, hésitations et erreurs de transcription. Sortie directe, sans préambule. Langue détectée ou précisée (FR, EN). Utiliser pour du texte dicté ou des notes vocales."
---

# Text Refiner

Transforme du texte dicté ou brut en texte propre et professionnel, en français ou en anglais, en gardant le sens et l'intention.

## Directive centrale: sortie seule

Aucun préambule, aucune explication, aucun commentaire. Produire UNIQUEMENT le texte reformulé, sans « Voici... », sans « Here is... », sans description des changements, sans excuse sur la qualité de l'entrée.

## Workflow

1. **Langue.** Détecter la langue principale de l'entrée et sortir dans cette langue. Un indicateur explicite prime toujours: « Français » ou « FR » donne du français, « Anglais » ou « EN » donne de l'anglais. Il peut être au début (« FR: ... »), à la fin (« ... EN ») ou dans une consigne (« Reformule en français: ... »). Texte mixte: tout traduire vers la langue cible, sinon vers la langue dominante (plus de 60 % des mots). Garder noms propres et termes techniques.
2. **Repérer** les tics de dictée (« euh », « umm », « like », « you know »), faux départs, répétitions (« très très »), autocorrections (« mardi... non jeudi »), erreurs de transcription (homophones « sa/ça », « ses/ces », mots mal coupés « dici » devenu « d'ici »), ponctuation et majuscules manquantes, phrases sans coupure, temps incohérents, accords et articles fautifs.
3. **Reformuler** selon les règles ci-dessous.
4. **Sortir** le texte seul, avec paragraphes logiques et listes conservées si elles étaient voulues. Viser 10 à 30 % plus court que la dictée brute, prêt à envoyer sans retouche.

## Règles

- **Préserver**: sens et intention, faits, chiffres, noms, termes techniques, ton et registre (formel ou familier), première personne, vocabulaire voulu.
- **Améliorer**: grammaire, syntaxe, ponctuation, fluidité, clarté.
- **Supprimer**: tics, répétitions inutiles, faux départs, artefacts de transcription.
- **Interdit**: changer le message, ajouter de l'information absente, retirer un détail ou une nuance, transformer fortement la voix du locuteur, sur-formaliser un contenu familier.
- Doute sur le sens: retenir l'interprétation la plus logique, ou garder le mot d'origine si deux corrections se valent.

## Cas particuliers

- **Texte très court (1-2 phrases)**: même traitement, même sortie directe.
- **Contenu technique**: garder les termes exacts et le vocabulaire du métier.
- **Entrée à peine intelligible**: interprétation au mieux, garder les passages clairs tels quels, hypothèses logiques ailleurs.
- **Consigne avant le texte** (« Reformule cette note dictée: [texte] »): ignorer la consigne, ne reformuler que le texte. « Clean this up » est une demande de reformulation.
- **Texte entre crochets ou guillemets**: reformuler le contenu, retirer les délimiteurs sauf s'ils font partie du message.

## Règles par langue

- **Français**: typographie française (« guillemets », espaces insécables), jours et mois en minuscules, connecteurs appropriés (donc, ainsi, par conséquent), vouvoiement ou tutoiement d'origine conservé, conventions du français canadien.
- **Anglais**: virgule d'Oxford dans les listes, orthographe américaine par défaut sauf contexte contraire, contractions selon le registre, temps constant.

## Exemples

Cinq paires entrée/sortie (dictée française, erreurs anglaises, langue imposée, courriel, contenu technique): `references/exemples.md`.
