---
name: encre-voix
description: Voix écrite du design system de Paul Perigault, en français. À déclencher pour écrire, réécrire ou relire un texte du site de documentation, du README, d'une page d'auteur, d'une description de paquet ou d'un message public du projet ; à la demande « voix Encre », « réécris ce texte », « fais-le moins IA », « accroche de page ». Propre au projet. Complète la revue visuelle `encre-design`.
---

# Encre : voix écrite

Issue : [#135](https://github.com/PaulPerigault/design-system/issues/135). Sources : réponses de Paul
(entretien du 2026-10-29), `.agents/product-marketing.md` (cible, promesse, preuves), ADR-0002,
`AGENTS.md` (règle éditoriale). « Préférence à valider » = règle sans source écrite, à confirmer.
Méthode inspirée des skills `copywriting` et `copy-editing` (niveau utilisateur), adaptée au français :
aucun texte tiers n'est copié ici.

## Comment l'utiliser

- Phrase de déclenchement : « voix Encre de `<fichier ou page>` » (ou `/encre-voix`).
- Avant toute chose, lire `.agents/product-marketing.md`. Y compléter les `[A VERIFIER]` avec Paul,
  ne jamais les remplir de mémoire.
- Entrées : un texte existant (réécriture ou relecture) ou une demande (nouveau texte).
- Sortie : le format de la section « Format de livraison ».
- Ce skill écrit et relit du texte. Il ne change ni composant, ni jeton, ni mise en page : pour le
  rendu, voir `encre-design`.
- Les textes à la première personne gardent `DraftNotice` : Paul les relit et les réécrit (#112).

## Lecteur et promesse

- Lecteur 1 : recruteur ou responsable technique. Il lit vite et juge un niveau d'ingénierie.
- Lecteur 2 : développeur Astro qui hésite à installer. Il veut savoir ce qui est stable.
- Promesse (Paul) : la preuve d'un niveau d'ingénierie élevé tenu par une seule personne. L'outil
  prêt à l'emploi n'est que la preuve concrète : accessibilité, CSP stricte, zéro JavaScript par défaut.
- Un texte sert l'un des deux lecteurs en premier, jamais les deux à égalité. Le dire dans la
  livraison (« lecteur 1 » ou « lecteur 2 »).

## Le ton

- Trois mots (Paul) : **précis, posé, sobre**. Le premier juge est le fait : un lecteur doit pouvoir
  le retrouver dans un fichier, une norme ou une mesure.
- **Une accroche directe en tête de page** (Paul) : une ou deux phrases qui disent ce que la page
  établit et pourquoi la lire. Elle contient un fait ou une conséquence, pas une description de la
  page (« Cette page résume… » ne passe pas).
- Phrases courtes, une idée chacune. Plus de 25 mots : couper (préférence à valider).
- Sujet, verbe concret, complément. Verbe d'action du dépôt : « vérifie », « refuse », « mesure »,
  « échoue », « note ».
- Le ton ne monte pas : ni exclamation, ni question rhétorique, ni formule d'enthousiasme. Le
  texte donne envie par ce qu'il établit.
- Une ou deux phrases qui marquent par page, au plus (en tête, et une dans le corps). Le reste est
  plain et factuel.
- Dire les limites au même niveau que les forces (modèle : page auteur, D-021). Une limite dite
  rend le reste crédible.

## Personne

| Type de texte                                          | Personne                       |
| ------------------------------------------------------ | ------------------------------ |
| Page d'auteur, accueil du site, README, présentation   | « je » (Paul parle)            |
| Documentation technique, composants, API, ADR, journal | neutre : impératif ou 3e pers. |

- « Nous » est interdit : il y a un auteur (Paul), le « nous » serait faux.
- Au « je », parler au présent et dire ce qui est fait : « J'écris les règles une fois dans
  `AGENTS.md`. La CI les vérifie. » Pas d'humilité feinte, pas de bravade.
- Dans la doc technique, ni « je » ni « vous » inutile. L'impératif suffit : « Installer… »,
  « Passer `tone` à… ».
- Les textes au « je » reçoivent `DraftNotice` tant que Paul ne les a pas relus.

## Refus de Paul : à ne pas écrire

**Tournures « faites par IA » :**

- « Il ne s'agit pas de X, mais de Y » et ses variantes (« ce n'est pas X : c'est Y »).
- Triplets négatifs : « sans X, sans Y, sans Z ». Une négation, si elle est vraie et utile.
- Phrase qui s'allonge en virgules : « …, offrant ainsi…, garantissant… ». Couper en deux phrases.
- Ouvertures creuses : « Dans un monde où », « À l'ère de », « Plongeons », « Découvrez »,
  « N'hésitez pas à ».
- Triplets rythmés pour l'effet (trois adjectifs, trois verbes) quand deux faits suffisent.
- Questions suivies de leur réponse (« Le résultat ? Un système… »).

**Superlatifs et adjectifs de vente :** « puissant », « robuste », « performant », « moderne »,
« élégant », « complet », « à la pointe », « de qualité », « véritable », « simplement ». Remplacer
par le fait : « 120 lignes au plus par fichier », pas « un code propre ».

**Mots d'agence :** « solution(s) », « innovant », « écosystème », « boîte à outils », « expérience »,
« accompagner », « levier », « au cœur de », « passionné par », « orienté résultats », « de bout en
bout » employé sans objet. Les anglicismes de vitrine : « seamless », « cutting-edge », « best-in-class ».

**Verbes d'intention** (Paul) : « vise à », « permet de », « a pour objectif », « cherche à »,
« entend ». Ils décrivent un souhait. Écrire ce que la chose fait ou ce que la règle impose :

- « Ce composant permet d'afficher une alerte » → « `Alert` affiche une alerte. »
- « Le projet vise à garantir l'accessibilité » → « L'accessibilité cible WCAG 2.2 AA ; l'e2e la mesure. »

**Chiffres sans source :** voir la section suivante.

Les interdits visuels d'`encre-design` (emoji, majuscules espacées, etc.) valent aussi pour le texte :
aucun emoji, aucun mot en capitales pour l'effet, aucun numéro de section décoratif.

## Preuves

- « Prouvé » seulement si une source l'établit : auteur, année, revue ou norme (`AGENTS.md`). Sinon
  écrire « convention » ou « préférence ».
- Tout chiffre porte sa source : fichier du dépôt, norme ou mesure datée. Dans le texte : « 13
  appareils (`apps/docs/e2e/devices.ts`) ». Une mesure vieille de plusieurs semaines : la redater ou
  la refaire.
- Chiffre ou fait non établi : écrire `[A VERIFIER]` à sa place et le lister en fin de livraison.
  Ne jamais arrondir, estimer ni écrire « plus de », « près de » sans la valeur exacte à côté.
- Accessibilité : cible WCAG 2.2 AA, AAA **partiel**, jamais « conforme AAA » (ADR-0002).
- Comparaison avec un produit tiers nommé : interdite sans source ni mesure (`[A VERIFIER]`).
- Une affirmation que le texte ne peut pas prouver est refusée, avec ce qui la débloquerait :
  « affirmation refusée : "léger" ; à débloquer avec : taille du paquet mesurée par `npm pack --dry-run` ».
- Rien d'inventé sur l'auteur : pas de formation, d'employeur, de date ni de contact non fournis
  (la page auteur le dit déjà).

## Rythme et forme

- Titre de page : un fait ou le sujet nommé, pas un titre creux (« Présentation »).
- Après l'accroche : du plus important au moins important. Un lecteur qui s'arrête après trois
  phrases doit déjà avoir la promesse et une preuve.
- Une section = une idée. Le titre de section dit cette idée.
- Listes : trois à six puces, chacune un fait complet avec sa source. Pas de liste pour trois mots.
- Tableau quand le lecteur compare (paquets, contrôles) ; la source dans une colonne.
- Liens : le libellé dit la destination (« la page preuves »), jamais « cliquez ici ».
- Texte alternatif, `aria-label` et titres : mêmes règles, une phrase courte et factuelle.

## Typographie française

- Apostrophe typographique `’` (majoritaire dans l'accueil, l'architecture, les preuves). La
  page auteur et `utiliser` emploient `'` : à harmoniser dans #123 (préférence à valider).
- Guillemets « » avec espaces insécables ; espace insécable avant `:`, `;`, `?`, `!`.
- Orthographe : « design system » (la page d'accueil écrit « design système » dans un titre :
  à corriger). Écrire « paquet », « jeton » ou « token » : le projet utilise `token` pour le
  paquet et « jeton » dans la prose ; garder un seul des deux par page (préférence à valider).
- Nombres : virgule décimale (6,93:1), espace fine insécable pour les milliers.
- Dates : `2026-10-29` dans les journaux et mesures ; « 29 octobre 2026 » dans la prose courante.

## Méthode (adaptée de copywriting et copy-editing)

1. **Diagnostiquer** : A = page vide ou texte creux (latitude sur l'angle, jamais sur les faits) ;
   B = voix réelle présente (la restaurer, garder le vocabulaire de Paul) ; C = correction ponctuelle
   (ne changer que la ligne demandée). Le dire en une ligne, avec la preuve.
2. **Décomposer** en unités (titre, accroche, chaque section, légendes). Pour chaque unité, deux ou
   trois versions, garder la meilleure, corriger son pire défaut, la figer.
3. **Passer chaque ligne au crible** (trois questions) :
   - Le lecteur peut-il se représenter la chose (un fichier, un test, un chiffre) ?
   - La phrase peut-elle être vraie ou fausse, donc vérifiée ?
   - Un autre projet pourrait-il écrire exactement cette phrase ? Si oui, elle échoue.
     Trois oui : garder. Deux : durcir la faible. Un ou zéro : réécrire depuis les faits, ou `[A VERIFIER]`.
4. **Relire en cinq balayages** : clarté ; voix (liste des refus) ; « et alors ? » (la phrase
   apporte-t-elle une conséquence ?) ; preuve (source ou `[A VERIFIER]`) ; précision (mot générique
   remplacé par le mot exact).
5. **Épreuve de non-modification** : tout changement doit être justifié (plus précis, plus court,
   plus vrai). Sinon, le retirer. En situation B et C, c'est le garde-fou principal.

Non retenus : les balayages « émotion » et « zéro risque » des skills tiers, sans objet ici
(pas de vente, pas de garantie commerciale).

## Format de livraison

Pour chaque texte, dans cet ordre :

1. **Diagnostic** (A, B ou C), lecteur visé (1 ou 2), type de texte (personne : je ou neutre).
2. **Avant** : le texte d'origine, tel quel (absent pour un nouveau texte).
3. **Après** : le texte proposé.
4. **Justification** : une ligne par changement, avec la règle de ce skill qui l'impose.
5. **À vérifier** : la liste des `[A VERIFIER]`, des chiffres à recompter et des affirmations refusées
   avec leur déblocage.
6. **Application** : fichiers à modifier, `DraftNotice` conservé ou non. Ne rien appliquer sans
   que la demande l'inclue.

Les essais de référence (accueil du site et README racine) sont dans `docs/design/voix-essais.md`.

## Hors périmètre

Aucun texte ni ressource tierce n'est copié ici. Pas de rédaction commerciale (offres, prix, appels
à l'achat), pas de texte en anglais, pas de contenu juridique (mentions légales, confidentialité) : un
changement de ces pages demande l'accord explicite de Paul.
