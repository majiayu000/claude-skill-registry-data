---
name: encre-mobile
description: Revue mobile du design system de Paul Perigault. À charger pour relire ou écrire un composant, une page, une mise en page, un graphique, une feuille d'impression, un `viewport`, une cible tactile, une animation, un test de matrice (`apps/docs/e2e/`) ; à la demande « revue mobile », « mobile Encre », « ça tient à 375 px ? », « réseau lent ». Propre au projet, web statique.
---

# Encre : revue mobile

Issue : [#178](https://github.com/PaulPerigault/design-system/issues/178). Sources du dépôt :
`AGENTS.md`, `apps/docs/e2e/devices.ts`, `apps/docs/e2e/matrix/`, `packages/css/src/base.css`,
`packages/css/src/print.css`, D-049. Sources externes : section « Sources ». Ce skill est de la
méthode, pas une preuve : « prouvé » seulement si une source l'établit ; sinon « convention » ou
« préférence ».

## Principe (préférence de Paul)

La majorité du trafic web est mobile (affirmation de Paul, sans source citée ici : ne pas la
chiffrer). Tout se juge donc d'abord à 375 px, sur réseau lent et processeur modeste ; le bureau
vient ensuite. Le réseau et le processeur se **mesurent** : ce skill ne pose aucun seuil bloquant.

## Comment l'utiliser

- Phrase de déclenchement : « revue mobile de `<page, composant ou PR>` » (ou `/encre-mobile`).
- Rendre d'abord à 375 px, puis 320 px, puis le reste ; lire le code ensuite, citer `fichier:ligne`.
- Sortie : trois sections (Bloquant, À améliorer, Ce qui tient), niveau de preuve en fin de point.
- Il ne remplace ni `axe`, ni les tests `e2e/matrix/` : il dit quoi regarder en plus.

## Cibles tactiles

- WCAG 2.5.8 (AA) : cible d'au moins 24 × 24 px CSS, sauf espacement suffisant, cible équivalente,
  cible en ligne dans un texte, contrôle natif non modifié, présentation essentielle (norme).
- WCAG 2.5.5 (AAA) : 44 × 44 px CSS, mêmes types d'exceptions (norme, niveau AAA).
- Règle du dépôt : cibles ≥ `--pp-target-min` (1,5 rem, `base.tokens.json`) ; contrôles principaux
  44 px (`targets.spec.ts` : convention, 2.5.5 est AAA). Un composant dimensionne ses cibles
  lui-même ou dit, dans sa page, que l'appelant doit le faire (exemple : `Cluster`).
- Relire : un lien seul dans un bloc, un bouton d'icône, une case, une pagination, un bouton de
  fermeture ; mesurer avec `getBoundingClientRect`, pas à l'œil.

## Texte et reflow

- Texte ≥ 12 px à 375 px, y compris axes et légendes de graphiques (D-049, décision de Paul) ;
  14 px reste le plancher hors graphique. Vérifier la taille calculée, pas la déclarée.
- Reflow, WCAG 1.4.10 (AA) : contenu défilant verticalement lisible à 320 px CSS de large sans
  défilement horizontal ; exemptions : tableaux de données, cartes, vidéos (norme).
- `layout.spec.ts` mesure `scrollWidth - innerWidth` sur la matrice. À 320 px (hors matrice) :
  rendre à la main, un défilement horizontal de la page est une erreur.
- Propriétés logiques (`inline`, `block`), pas de largeur fixe en pixels, pas de `100vw` seul.

## Viewport et zoom

- Valeur du dépôt : `width=device-width, initial-scale=1` (`DocsLayout.astro`). Rien d'autre.
- Jamais `user-scalable=no`, ni `maximum-scale` qui bloque le zoom : MDN les signale comme barrière
  pour la basse vision (WCAG 1.4.4 exige 200 %) ; MDN recommande de ne rien limiter.
- Relire : toute balise `meta name="viewport"` ajoutée, tout `touch-action` qui coupe le pincement.

## Appareils (13 configurations, `devices.ts`)

- Téléphones, portrait : `360x800`, `375x667`, `393x852`, `430x932` (4).
- Mêmes téléphones en paysage : `…-paysage` (4).
- Tablette : `tablette-820x1180` (1). Bureaux : `1280x800`, `1440x900`, `1920x1080` (3).
- `360x800-mouvement-reduit` : le plus petit téléphone avec `reducedMotion: 'reduce'` (1).
- Tactile : contexte mobile, densité 3 (2 pour la tablette). Chaque entrée est un projet
  Playwright `matrice-<nom>`. Régression visuelle : 360, 820 et 1440 seulement (`VISUAL_PROJECTS`).
- CI : une PR qui touche le rendu lance `chromium`, `matrice-375x667` et `matrice-bureau-1280x800` ;
  la matrice entière tourne chaque lundi et à la demande (`ci.yml`, D-029). Un doute de mise en page : lancer
  `npm run e2e -- --project=matrice-360x800`.

## Réseau lent et processeur bridé (MESURE seulement)

- Lighthouse mobile : réseau simulé « Slow 4G » (latence 150 ms, 1,6 Mb/s descendant, 750 kb/s
  montant) et processeur ralenti 4 fois par défaut (doc Lighthouse).
- DevTools, panneau Performance : réglages de capture, réseau et CPU ; le ralentissement est relatif
  à la machine, une calibration donne un préréglage de téléphone modeste (doc Chrome).
- Core Web Vitals au 75e centile, mobile et bureau séparés : LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1
  (web.dev). Ce sont des **cibles de terrain**. Écart : `perf.spec.ts` les assertit déjà en e2e
  (360 × 800, CPU ×4, Slow 4G) ; en revue, les lire comme une mesure, pas un motif de refus.
- Un chiffre labo n'est pas un chiffre terrain : le site statique n'a pas de mesure de terrain ;
  écrire « mesuré en labo, bridé, le <date> » et jamais « rapide ».
- Rapport : valeur, outil, réglage de bridage, date. Aucun échec de CI, aucune fonctionnalité retirée
  pour gagner une mesure (voir `encre-greenops`).

## Mouvement réduit, contraste forcé, impression

- `prefers-reduced-motion` : valeurs `no-preference` et `reduce` ; MDN conseille l'animation par
  défaut puis son remplacement dans un bloc `reduce`, placé après. Dans le dépôt : `base.css` ne
  lisse le défilement que sous `no-preference` et coupe durées et délais d'animation et de
  transition sous `reduce`. Tester avec `360x800-mouvement-reduit`.
- `forced-colors: active` : couleurs et contours forcés par le système (`CanvasText`, `Canvas`),
  ombres forcées à `none`, fond-image coupé sauf `url()` (MDN). Ne rien porter par une ombre ou une
  couleur seule : prévoir une bordure. Les graphiques et `Alert` le font déjà : suivre leur modèle.
- Impression : `packages/css/src/print.css`. Relire à l'aperçu : liens lisibles, aucun fond requis,
  pas de coupure au milieu d'un graphique.

## Checklist vérifiable

1. 375 px : aucun défilement horizontal, texte ≥ 12 px (graphique) ou 14 px (reste).
2. 320 px : reflow sans perte ni défilement horizontal (tableaux exemptés).
3. Cibles ≥ 24 px mesurées, contrôles principaux ≥ 44 px.
4. `viewport` inchangé ; zoom 200 % lisible.
5. Matrice : `layout`, `targets`, `focus`, `axe` verts sur les projets concernés.
6. Mouvement réduit : aucune animation restante ; contraste forcé : rien d'invisible.
7. Impression : aperçu relu.
8. Mesure bridée notée (valeur, réglage, date), sans seuil bloquant.

## Sources

Consultées le 2026-10-30. Niveaux : norme, convention, préférence. Texte paraphrasé, jamais copié.

| Source                                           | URL                                                                                               | Niveau     |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ---------- |
| WCAG 2.2, 2.5.8 Target Size (Minimum)            | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html                              | norme      |
| WCAG 2.2, 2.5.5 Target Size (Enhanced)           | https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html                             | norme      |
| WCAG 2.2, 1.4.10 Reflow                          | https://www.w3.org/WAI/WCAG22/Understanding/reflow.html                                           | norme      |
| web.dev, Core Web Vitals                         | https://web.dev/articles/vitals                                                                   | convention |
| web.dev, Interaction to Next Paint               | https://web.dev/articles/inp                                                                      | convention |
| Lighthouse, bridage (`docs/throttling.md`)       | https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md                           | convention |
| Chrome DevTools, référence Performance (bridage) | https://developer.chrome.com/docs/devtools/performance/reference                                  | convention |
| MDN, `prefers-reduced-motion`                    | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion | convention |
| MDN, `forced-colors`                             | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors          | convention |
| MDN, `meta name="viewport"`                      | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport           | convention |

« Norme » : spécification du W3C. « Convention » : documentation d'éditeur ou de praticiens, non
normative. Le seuil de 44 px, le plancher de 12 px et la règle « mesure sans blocage » sont des
choix du dépôt (convention ou préférence), pas des preuves. Aucune étude n'est citée.
