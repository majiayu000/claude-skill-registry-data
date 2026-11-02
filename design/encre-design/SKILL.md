---
name: encre-design
description: Revue visuelle selon la direction « Encre » du design system de Paul Perigault. À déclencher pour relire ou critiquer un composant, une page ou un graphique SVG (LineChart, BarChart, AreaChart, GaugeChart, KPI, tableau), pour vérifier contraste, typographie et rendu « générique », ou à la demande « revue Encre », « fais-le moins générique », « audit visuel ». Propre au projet, web statique uniquement.
---

# Encre : revue visuelle

Issue : [#134](https://github.com/PaulPerigault/design-system/issues/134). Sources : ADR-0002
(identité), ADR-0007 (données), `packages/tokens`, réponses de Paul (2026-10-29).
« Préférence à valider » = règle sans source écrite, à confirmer par Paul.

## Comment l'utiliser

- Phrase de déclenchement : « revue Encre de `<composant, page ou fichier>` » (ou `/encre-design`).
- Entrée : un composant, une page de `apps/docs`, ou un SVG produit au build.
- Sortie : un rapport au format de la section « Format du rapport », dans `docs/design/`.
- Mesurer avant de juger : aucune remarque de couleur, de taille ou d'espacement sans chiffre.
- Ce skill est un critère de relecture, pas un générateur : il ne change aucun jeton.

## La direction

- Trois adjectifs (Paul) : **précis, posé, lisible**.
- Signature (Paul) : le trait plein d'encre de 2 px sur un fond quasi blanc ou quasi noir, avec
  l'étiquette directe en bout de courbe, sans cadre ni légende décorative.
- L'étiquette directe **ne remplace jamais** la légende accessible : tableau de données lié,
  motifs de trait et marqueurs restent exigés (WCAG 1.4.1).
- L'ancre est le favicon : encre quasi noire `oklch(0.2008 0.0124 270.7)`, blanc, rien d'autre. Le
  fond sombre est cette encre (ADR-0002).
- Une pièce d'ingénierie, pas une illustration : une information par élément, ou l'élément part.

## Interdits

AGENTS.md et ADR-0002 : dégradés, ombres décoratives, flou (`backdrop-filter`), emoji, étiquettes en
majuscules espacées, numéros de section, pastilles de tags, palette Tailwind par défaut, valeurs
arbitraires, vert sur noir, scanlines, glitch, machine à écrire, phrases génériques.

Ajouts de Paul : coins arrondis au-delà de 8 px (hors marque : 14 % du logo et de l'avatar) ;
illustrations génériques et icônes décoratives ; « crème + serif + terracotta » ; palette
arc-en-ciel de graphique (six teintes de saturation égale).

Autres : tout attribut `style` en ligne, toute couleur, taille, espacement, rayon ou durée brute
(les consommateurs ont une CSP stricte, AGENTS.md).

## Couleur et contraste

Seuils (WCAG 2.2 AA, projet) : texte jusqu'à 17 pt (≈ 22,7 px, hors gras) : **4,5:1** ; grands textes
et éléments graphiques porteurs d'information (tracés, barres, marques, anneau de focus, bord de
contrôle) : **3:1** (1.4.3, 1.4.11). Le projet vise plus haut sur le texte : 7:1 texte/fond (ADR-0002).
Calcul sur le sRGB rendu, avec `@paulperigault/tokens/contrast` (`contrastRatio`), jamais sur le L
d'OKLCH.

- Neutres : teinte 270,7, chroma ≤ 0,022. Fond clair `oklch(0.985 0.004 270.7)`, sombre
  `oklch(0.201 0.0124 270.7)`.
- Texte : `--pp-color-fg` (16,8:1 clair, 15,4:1 sombre) ou `--pp-color-muted` (7,8:1 et 9,3:1). Jamais
  une couleur de série pour du texte (ADR-0007).
- Accent : une teinte, `oklch(0.47 0.19 h)` clair, `oklch(0.78 0.1 h)` sombre (6,93:1 et 8,94:1).
  Il est **rare** (Paul) : une série ou une valeur par graphique. Exception : `GaugeChart`, dont
  les zones sont colorées par seuils, avec libellé et valeur écrits.
- Jamais la couleur seule (1.4.1) : icône, libellé, motif ou marqueur en plus. Statuts :
  `--pp-color-status-*` en renfort d'un mot.
- Mesures du 2026-10-29 : `--pp-chart-1..6` contre le fond, clair 6,93 / 3,36 / 17,66 / 3,07 / 8,23 /
  3,45 ; sombre 8,94 / 3,22 / 14,19 / 3,10 / 7,12 / 4,81 (tous ≥ 3:1). Le filet `--pp-color-line`
  (1,35 et 1,54) ne porte aucune donnée : décoratif, jamais pour un texte ni un bord de contrôle.

## Typographie

- Texte : Atkinson Hyperlegible Next (`--pp-font-family-sans`, vérifié dans `tokens.css`).
  Mono (`--pp-font-family-mono`, Atkinson Hyperlegible Mono) seulement pour code, identifiants,
  empreintes et métadonnées (préférence, ADR-0002).
- Échelle 1,25 : `--pp-font-size--1` 0,9 rem, `-0` 1,125 rem (corps, 18 px), `-1` 1,406 rem, `-2`
  1,758 rem, `-3` 2,197 rem, `-4` 2,747 rem. Interligne `--pp-font-line-height-body` 1,55, titres 1,15.
- Graisses : `--pp-font-weight-regular` 400, `-medium` 500, `-semibold` 600, `-bold` 700.
- Planchers (décisions de Paul, 2026-10-29) : le corps ne descend pas sous 18 px ; le texte hors
  graphique, sous 14 px. Texte d'axe et de légende des graphiques : **12 px au moins à 375 px de
  largeur d'écran**, en `--pp-font-size--1` (0,9 rem, 14,4 unités) dans un viewBox de 360 unités
  de large, soit 12,4 px (ADR-0007, point ouvert 3, D-049). Mesure : taille calculée × largeur
  affichée / largeur du viewBox ; sous 12 px à 375 px, ou chevauchement des libellés : à signaler.
- Chiffres de données : `font-variant-numeric: tabular-nums`. Pas de majuscules espacées.

## Forme

- Rayons : `--pp-radius-control` 4 px, `--pp-radius-surface` 8 px. Aucun autre. Barres et marques de
  données à coins droits (ADR-0007).
- Filets : `--pp-size-rule` (1 px). Courbes à 2 `--pp-size-rule`. Focus : `--pp-size-focus-width` 2 px,
  décalage `--pp-size-focus-offset` 2 px, plein.
- Cibles : ≥ `--pp-size-target-min` (1,5 rem = 24 px, 2.5.8) ; contrôles à `--pp-size-control-height`.
- Espacement : `--pp-space-3xs` à `-3xl` (0,25 à 6 rem). Mesure `--pp-size-measure` 36 rem, page
  `--pp-size-page` 72 rem. Propriétés logiques (`inline`, `block`).
- Aucune ombre ni flou. Mouvement : `--pp-duration-fast` 100 ms et `-base` 160 ms, opacité et
  transformations, 0 sous `prefers-reduced-motion: reduce`.

## Visuels de données (ADR-0007)

- Rapport données/encre (Tufte, 1983) : ce qui ne porte pas de donnée disparaît. Pas de cadre, de fond
  de tracé, de grille verticale. Grille horizontale 1 `--pp-size-rule` en `--pp-color-line`, ligne de
  base pleine, 5 graduations au plus, « rondes ».
- Barres depuis zéro, séparées par un espace. Aire : fond à 12 % au plus de la série, trait sur la
  seule courbe supérieure (ni base ni côtés).
- Valeur écrite sur une barre : neutre `--pp-color-fg` ou `--pp-color-bg` choisi par série et par
  thème pour atteindre 4,5:1 contre la barre (`inkOn`, `@paulperigault/dataviz` : 4,78 à 17,66:1),
  liseré de la couleur de la série ; hors de la barre : `--pp-color-fg`, liseré du fond.
- Couleur jamais seule : chaque rang de série a un motif de trait (continu, tirets, points) et un
  marqueur ; barres et aires par motif de remplissage ; légende = marqueur + libellé.
- Palettes dérivées de `--pp-accent-hue` : `--pp-chart-1..6` (catégorielle), 6 séries au plus ;
  au-delà, regrouper. Pas de palette empruntée. Contrôle daltonisme : ΔE00 ≥ 10 par paire.
- Annotations : texte direct, 3 au plus, trait de rappel fin.
- Alternative : `figure` + `figcaption` (résumé chiffré), `svg role="img"` + `title` + `desc`, tableau
  lié avec `th scope`. Une valeur manquante est dite, jamais omise ni mise à 0.
- États : vide = `EmptyState` ; erreur = erreur typée qui fait échouer le build (ou `Alert` + tableau).
  Un graphique statique n'a pas d'état de chargement.
- Budget : 400 nœuds SVG et 10 ko par graphique. Contraste forcé : tracés en `CanvasText`.
- Sobriété par défaut (Paul) : une série en accent, les autres en neutres plus motifs ; la
  personnalité vient de la typographie et du soin des annotations, pas de la décoration.

## Signes d'un rendu générique (propres au projet)

1. Arc-en-ciel de six teintes de même saturation, ou palette Tailwind par défaut.
2. Dégradé, ombre portée, flou, halo autour d'une courbe ou d'un KPI.
3. Coins de plus de 8 px, barres en pilule, icône décorative, illustration de remplissage.
4. Fond crème, serif et terracotta ; ou vert acide sur noir.
5. Cadre autour du tracé, grille dense, quadrillage vertical, légende séparée loin du tracé.
6. Étiquette en majuscules espacées, numéro de section, pastille de tag, emoji.
7. Titre creux (« Aperçu des performances ») au lieu d'un fait chiffré.
8. Couleur seule pour distinguer deux séries ; texte d'axe sous 12 px à 375 px (hors graphique : 14 px).
9. Espacements arbitraires, hors jetons `--pp-space-*`.
10. Valeur d'accent employée partout : plus rien ne ressort.

## Méthode de revue

1. Lire le composant et ses CSS ; lister les jetons réellement utilisés.
2. Produire le SVG au build pour 2 ou 3 jeux représentatifs (court, long, trous, extrêmes).
3. Calculer les contrastes à partir des jetons (`contrastRatio`), clair et sombre : texte contre
   fond, marques contre fond, texte sur zone colorée.
4. Regarder le rendu à 375 et 800 px, en clair et en sombre : texte tronqué ou chevauché, traits
   fins, débordement horizontal, étiquettes illisibles.
5. Comparer à la liste « Signes d'un rendu générique » et aux interdits.
6. Rédiger le rapport. Corriger seulement ce qui se règle en quelques lignes sans toucher un jeton
   partagé (un jeton modifié change tout le système : décision de Paul d'abord).

## Format du rapport

Trois sections, chaque point avec la **mesure** et la **correction proposée** :

- **Critique** : viole un seuil ou une règle (contraste < 3:1 ou 4,5:1, couleur seule, interdit,
  texte tronqué).
- **À améliorer** : lisible mais approximatif (taille proche du plancher, espacement, épaisseur de
  trait, annotation trop longue).
- **Ce qui fonctionne** : à conserver, avec la mesure.

Gravités (Critical, High, Medium, Low) en tête de point. Fin de rapport : liste « à faire » des
points non corrigés, sans ouvrir d'issue.

## Hors périmètre

Aucune règle de plateforme iOS ou macOS : c'est un design system web. Aucun texte ni ressource
tierce n'est copié ici ; les guides externes ne servent que de critères d'inspiration.
