---
name: klassci-user-tutorial
description: >
  Génère un tutoriel utilisateur illustré pour une fonctionnalité KLASSCI (personnel d'école :
  secrétariat, coordination, comptabilité, enseignants), avec de VRAIES captures d'écran annotées
  et un PDF soigné. Utiliser quand on demande un "tuto", "guide utilisateur", "mode d'emploi",
  "pas à pas", "expliquer à une directrice/secrétaire comment faire", ou de répondre à un utilisateur
  qui ne sait pas où cliquer dans KLASSCI.
argument-hint: "[fonctionnalité] [--tenant presentation]"
---

# KLASSCI — Tutoriel utilisateur illustré

Produit un guide pas à pas pour le personnel d'une école, à partir de **vraies captures d'écran
annotées** de l'application, assemblées en **PDF de qualité** via `editorial-pdf`.

## ⛔ Règle d'or (non négociable)

**JAMAIS de reconstruction de l'interface en HTML/SVG.** Aucune maquette « dessinée à la main ».
Chaque image du tutoriel est une **capture d'écran RÉELLE** de KLASSCI, prise dans le navigateur sur
un tenant, puis annotée (numéros, flèches, cadres) par-dessus l'image réelle. Une capture réelle mal
cadrée vaut mieux qu'une belle maquette fausse : l'utilisateur doit reconnaître exactement son écran.

## Ce dont on a besoin avant de commencer

1. **La fonctionnalité** à documenter (ex : « saisie des présences des étudiants de tronc commun »).
2. **L'audience** (secrétaire, comptable, coordinateur, enseignant, directrice) — dicte le ton et le
   vocabulaire (voir la réponse-type dans [references/presences-absences-workflow.md](references/presences-absences-workflow.md)).
3. **Le tenant** où capturer. Défaut : `presentation` (login `superadmin` / `Bonjour@123`, pas de
   protection anti-bot LWS → capture simple). Pour un tenant prod, appliquer la recette de bypass LWS
   du skill `klassci-test-e2e` (non-headless + spoof User-Agent).

Si l'un de ces points manque et n'est pas déductible, le demander en une question courte.

## Workflow

### 1. Cartographier le parcours réel
Naviguer soi-même dans l'app (voir étape 3) pour relever le **chemin de menu exact** (fil d'Ariane,
ex : `Présence & Absences › Gestion des présences › Présences étudiants › Marquer présences`) et la
**suite d'étapes** que l'utilisateur devra reproduire. Ne jamais deviner un libellé de menu : le lire
à l'écran. Couvrir aussi les **variantes** (ex : présences par séance ET saisie manuelle des heures
pour régulariser une période passée — cf. la référence présences).

### 2. Rédiger le plan du tuto
Une étape = un écran = une capture annotée. Lister : titre d'étape, action utilisateur, ce qu'on
marque sur la capture (le bouton à cliquer, le champ à remplir). Rédiger la prose côté utilisateur
(pas de jargon technique), au ton de l'audience.

### 3. Capturer les VRAIES captures (dev-browser)
Utiliser `dev-browser` (comme `visual-check` / `klassci-test-e2e`). Recette de login + capture — voir
[references/screenshot-capture.md](references/screenshot-capture.md) pour le script complet, la recette
de bypass LWS des tenants prod, et le cadrage (pleine page vs zone ciblée). Une capture PNG par étape,
nommée `etapeN-description.png`, dans un dossier de travail dédié.

### 4. Annoter + assembler en HTML
Partir du template [assets/tutorial-template.html](assets/tutorial-template.html) : il embarque chaque
capture réelle via `file://` et pose PAR-DESSUS des **overlays d'annotation** (badges numérotés, flèches,
cadres de surbrillance) positionnés en `%` sur l'image. On n'édite jamais l'image source ; on superpose
en CSS. Charte KLASSCI (bleu `#0453cb`, monochrome). Une section = une étape.

### 5. Générer le PDF via editorial-pdf
Invoquer le skill `editorial-pdf` sur le HTML assemblé (Chrome headless → PDF A4 portrait). Suivre son
pipeline (boilerplate, commande Chrome, vérif visuelle de chaque page). Le PDF est le livrable.

### 6. Vérifier
Relire chaque page du PDF : capture nette, annotation bien placée sur le bon élément, texte lisible,
aucun chevauchement. Corriger le positionnement `%` des overlays si une flèche tombe à côté.

## Anti-patterns à bloquer

1. ❌ Reconstruire l'UI en HTML/SVG « qui ressemble à » l'écran (interdit absolu).
2. ❌ Screenshot non authentifié → on capture la page de login au lieu de l'écran réel.
3. ❌ Deviner un libellé de menu au lieu de le lire à l'écran.
4. ❌ Oublier les variantes d'un flux (ex : présences = par séance ET saisie manuelle des heures).
5. ❌ Livrer le HTML au lieu du PDF final (le livrable est le PDF `editorial-pdf`).
6. ❌ Annoter en modifiant l'image source (toujours overlay CSS par-dessus la capture intacte).

## Références

- [references/screenshot-capture.md](references/screenshot-capture.md) — recette dev-browser (login,
  bypass LWS, cadrage, nommage).
- [references/presences-absences-workflow.md](references/presences-absences-workflow.md) — exemple
  complet présences/absences (par séance + saisie manuelle des heures) + réponse-type au personnel.
- [assets/tutorial-template.html](assets/tutorial-template.html) — template HTML captures annotées
  (charte KLASSCI, prêt pour editorial-pdf).
