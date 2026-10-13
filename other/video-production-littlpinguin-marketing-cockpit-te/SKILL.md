---
name: video-production
description: Point d'entrée unique de toute demande vidéo pour {{COMPANY_NAME}} (Reel, Short, vidéo LinkedIn, explainer, vidéo produit ou de lancement, motion design, montage de rushes, clips tirés d'une vidéo longue, montage documentaire sur archives, animation à l'encre, 3D, Manim). Cadre l'objectif business, choisit la filière, tient le dossier de projet, les trois validations humaines (concept, script, storyboard), le contrat de coût, le journal de décisions, le contrôle avant rendu, la QA mesurée (qa-video.py, agent video-reviewer) et la livraison ; passe la main aux skills spécialisées et aux workflows HyperFrames par un BRIEF.md. Ne publie pas, ne décide pas la doctrine de marque, n'écrit pas le post qui accompagne la vidéo, ne fait pas de deck (skill slides).
---

# video-production : de la demande au rendu livré

Toute demande vidéo du cockpit entre ici, quelle que soit sa forme : Reel, Short, vidéo LinkedIn, explainer, vidéo produit ou de lancement, motion design, montage de rushes, clips tirés d'une vidéo longue, montage documentaire, animation à l'encre, 3D, Manim. Cette skill tient l'ordre, les validations, le budget et la QA. Chaque étape technique a sa skill, et la construction passe le plus souvent par un workflow HyperFrames.

## Avant tout

1. **Module actif.** `.setup-completed` porte `modules.video.enabled: true`. Sinon, proposer `/modules` et s'arrêter.
2. **HyperFrames présent** pour les filières qui l'utilisent : le plugin `hyperframes@hyperframes`, installé par `/modules`, expose ses skills `hyperframes:*` dans la session. S'il manque, proposer `/modules` (installation) ou `/health-check` (diagnostic). Les capacités facultatives (whisper, Manim, corpus CLIP) sont notées par `/modules` dans `.setup-completed` (`modules.video.capacites`) : une filière qui en dépend le dit avant de commencer.
3. **Objectif business d'abord** (règle (a) du `CLAUDE.md` racine) : notoriété, leads, conversion, rétention ou preuve sociale, avec l'indicateur suivi. Filière, format et durée en découlent, jamais l'inverse.
4. **Contexte.** Lire `02-strategy/calendar/calendar.md` (ce qui est prévu, ce qui est en cours) et `00-intel/` (signaux récents). L'intel est confidentielle : on reformule, aucun fait sur une personne n'en sort.
5. **Marque, jamais de mémoire** : `01-brand/voice.md`, `01-brand/anti-ai-writing-style.md`, `01-brand/style-guide.md`, `01-brand/divulgation-ia.md`, `01-brand/droits.md`, et le catalogue `01-brand/assets/`. Si un fichier manque ou porte encore des `{{...}}`, s'arrêter et proposer `/start-cockpit`.
6. **Doctrine du module**, selon la filière : `08-video/formats.md`, `08-video/montage.md`, `08-video/narration.md`, `08-video/motion.md`, `08-video/documentaire.md`, et `08-video/inspiration.md` pour la recherche de références.
7. **Vidéo de référence, en option.** Si l'humain montre une vidéo qu'il aime, écrire dans `brief.md` ce qu'on garde (rythme, accroche, structure, ton) et ce qu'on change (sujet, traitement, angle). On ne reprend ni ses images, ni sa musique, ni son texte.

## Le projet

Un dossier par vidéo, créé au cadrage et nommé `AAAA-MM-JJ-<sujet>` : la date du cadrage, puis le sujet en minuscules et tirets (`2026-10-12-explainer-reporting`). Ce nom est le `<slug>` de tout le module, exports compris (`<slug>-<plateforme>.mp4`).

```
08-video/projets/<slug>/
├── brief.md        objectif business, canal, durée, persona, message unique, matière, CTA, budget
├── REPRISE.md      état courant et prochaine action, lu en premier par une nouvelle session
├── decisions.md    journal en ajout seul : date, sujet, choix, options écartées, raison
├── couts.md        estimations, dépenses réelles, solde du budget
├── references.md   références d'inspiration retenues (créateur, lien, mécanisme) et planche référence → transposition
├── script.md       script minuté (validé) ; son frontmatter l'inscrit à l'inventaire
├── storyboard.md   plans, vignettes au vrai cadrage, sources de matière (validé)
├── sous-titres/    fichiers .srt relus (skill captions)
├── hyperframes/    racine HyperFrames : BRIEF.md, frame.md, brand.css, STORYBOARD.md, compositions/
├── hyperframes-sous-titres/  projet hyperframes:embedded-captions (skill captions), à part de hyperframes/ ; frames_fg/, frames_bg/ non versionnés
├── rushes/         sources, clips générés, intermédiaires dans rushes/tmp/ (non versionnés)
├── exports/        rendus finaux par plateforme (non versionnés)
└── qa/             rapports de qa-video.py et planches (seul le rapport .md final se versionne)
```

### `brief.md`

```markdown
# Brief : <titre de travail>

- **Objectif business** : <notoriété | leads | conversion | rétention | preuve sociale> ; indicateur suivi : <...>
- **Canal et plateforme** : <Reels | TikTok | Shorts | LinkedIn | site | YouTube> ; toile <1080x1920 | 1080x1350 | 1080x1080 | 1920x1080>
- **Durée visée** : <secondes>
- **Persona** : <persona de 01-brand/personas.md> ; ce qu'elle sait déjà du sujet : <...>
- **Message unique** : <une phrase>
- **Matière disponible** : <rushes, captures, assets de 01-brand/assets/, chiffres sourcés, voix, musique>
- **Appel à l'action** : <une seule action>
- **Budget** : <montant ou crédits> ; outils payants autorisés : <liste, ou aucun>
- **Échéance** : <date> ; entrée du calendrier : <ligne de 02-strategy/calendar/calendar.md>
- **Filière** : <ligne de la table « Choisir la filière »>
- **Vidéo de référence** (si fournie) : on garde <...> ; on change <...>
```

### `REPRISE.md`

```markdown
# Reprise : <slug>

- **État** : <cadrage | concepts | script | storyboard | matière | construction | rendu | QA | livré>
- **Dernière validation** : <validation, date, qui, ce qui a été validé>
- **Prochaine action** : <une action précise>
- **En attente de l'humain** : <question ouverte, ou rien>
- **Fichiers clés** : <chemins>
```

### `decisions.md`

```markdown
# Décisions : <slug>

Journal en ajout seul. Une décision qui change s'ajoute en nouvelle ligne, avec le même sujet ; l'ancienne ligne reste.

| Date | Sujet | Choix | Options écartées | Raison |
|---|---|---|---|---|
| <date> | Filière | <filière> | <autres filières envisagées> | <pourquoi> |
| <date> | Profil de goût | densité <n>, énergie <n>, audace <n> | <...> | <lecture de la vidéo> |
| <date> | Voix | <fournisseur, modèle, voix> | <...> | <échantillon validé le ...> |
```

### `couts.md`

```markdown
# Coûts : <slug>

Budget du projet : <montant ou crédits>

| Date | Outil | Fournisseur | Modèle | Échantillon ou série | Estimé | Réel | Solde |
|---|---|---|---|---|---|---|---|
```

### `script.md`

Un frontmatter, un titre, puis un tableau minuté, une ligne par plan. Le frontmatter est ce que lit `scripts/build-inventory.py` : `date` (la date du cadrage, celle du slug), `subject` (le sujet de la vidéo en 5 à 10 mots, repris tel quel dans la colonne Sujet de l'inventaire) et `statut` (`brouillon`, puis `validé` à la validation 2, `publié` après la publication). Une seule colonne du tableau a un en-tête qui contient « Voix » : c'est le texte dit, celui que `qa-video.py --script` compare à la transcription du rendu ; le frontmatter et le titre ne la gênent pas.

```markdown
---
date: <AAAA-MM-JJ>
subject: <sujet de la vidéo, 5 à 10 mots>
statut: brouillon
---

# Script : <titre de travail>

| # | Temps | Image | Voix | Texte à l'écran | Jeu |
|---|---|---|---|---|---|
| 1 | 0:00-0:03 | <ce qu'on voit> | <texte dit> | <carton> | <intention, pause, mot appuyé> |
```

## Choisir la filière

| Demande | Filière |
|---|---|
| Motion court sans voix (titre animé, chiffre, logo, lower-third, data viz, carte) | `motion-design` → `hyperframes:motion-graphics` |
| Explainer narré sans tournage (article, notes, concept) | `hyperframes:faceless-explainer` |
| Vidéo produit ou lancement depuis une URL, un site, une app | `hyperframes:product-launch-video` |
| Annonce de fonctionnalité depuis un PR (clients SaaS) | `hyperframes:pr-to-video` |
| Clip rythmé sur une musique | `hyperframes:music-to-video` |
| Rushes face caméra → reel | `reel-talking-head` → `video-editing` : `hyperframes:general-video`, la voie ordinaire ; `hyperframes:talking-head-recut` seulement pour poser un habillage designé sur une séquence déjà coupée et étalonnée ; ou tout par ffmpeg |
| Vidéo longue → clips | `video-repurpose` |
| Clips IA ou stock + narration, montage libre | `video-generation` (matière) → `hyperframes:general-video` |
| Montage documentaire sur archives | `video-documentary` |
| Animation à l'encre, personnages, 3D | `motion-design` (références) → `hyperframes:general-video` ou `hyperframes:motion-graphics` |
| Démonstration conceptuelle ou mathématique | `manim-composer` → `manim-ce` → plan vidéo dans HyperFrames |
| Sous-titres seuls | `captions` (ffmpeg, ou `hyperframes:embedded-captions` pour du designé) |
| Présentation, deck | **toujours `slides`**, jamais `hyperframes:slideshow` |

Toute composition animée passe par `motion-design`, qui porte la marque jusqu'à HyperFrames. Une démo produit filmée en capture d'écran suit `08-video/montage.md` § « Démo produit et capture d'écran ». Les skills du projet priment sur celles d'un plugin : si une skill `hyperframes:*` et une skill du template se recouvrent, celle du template décide, et le workflow HyperFrames exécute.

## Étapes et validations

1. **Cadrage.** Objectif business, calendrier et `00-intel/` consultés, filière choisie, dossier du projet créé, `brief.md` écrit, `REPRISE.md` initialisé.
2. **Concepts.** Deux ou trois concepts réellement différents, chacun avec son chemin outillé honnête (ce que les outils disponibles produisent vraiment, pas ce qu'ils promettent), son coût estimé et son risque. En recommander un. Pour les nourrir, chercher des références avec `python3 08-video/scripts/inspiration.py chercher "<mots en anglais>"` (2 à 4 requêtes par concept), les transposer selon `08-video/inspiration.md` (on reprend un mécanisme, jamais un look) et les consigner dans `references.md`. Chaque concept cite ses références avec leur lien et leur créateur, ce qu'on garde et ce qu'on change. Sans réseau ni cache, le dire et continuer sans références.
   → **Validation 1 : choix du concept.**
3. **Script** dans `script.md`, selon `08-video/narration.md` quand il y a une voix. Pour un format court, l'accroche en trois variantes (`08-video/formats.md` § « Format court : repères de production »). Profil de goût et moteur consignés dans `decisions.md` (`08-video/motion.md`). Le débit de la voix se mesure sans dépense, avec la voix locale de Kokoro ou une lecture chronométrée (`08-video/narration.md` § « Calibrer la longueur »).
   → **Validation 2 : script validé.**
4. **Storyboard.** Filières HyperFrames : le plan d'HyperFrames (`hyperframes/STORYBOARD.md`), produit après la passation avec `storyboard: yes` ; ses croquis de mise en page suivent l'accord (voir « Voix et storyboard » plus bas). Autres filières, et `hyperframes:motion-graphics` qui n'en produit pas : `storyboard.md`, un tableau des plans avec des vignettes au vrai cadrage et la source de chaque matière. Dans les deux cas, la revue de singularité de `08-video/motion.md` est faite, et une planche « référence → transposition » (une ligne par scène, dans `references.md`) accompagne le storyboard : `08-video/inspiration.md` § « Transposer dans la marque ».
   → **Validation 3 : storyboard validé. Aucun crédit dépensé avant.**
5. **Matière.** Réutiliser d'abord (`01-brand/assets/`, rushes existants), puis le stock (Magnific `stock_search` et `stock_download`, corpus documentaire), puis générer (`video-generation`, `image-generation`, voix, musique). Un échantillon avant toute série, sous le contrat de coût.
6. **Construction.** HyperFrames ou ffmpeg selon la filière, dans `hyperframes/` ou dans le plan de montage de `video-editing`.
7. **Contrôle avant rendu** (section dédiée).
8. **Rendu, puis QA** : `qa-video.py` et l'agent `video-reviewer`.
9. **Livraison** (section dédiée).

Règles des validations :

- À chaque validation, le tour s'arrête et attend la réponse de l'humain. Présenter ce qui est à valider, la recommandation, et ce que l'accord déclenche.
- Une validation vaut pour une seule étape. Un « ok » sur le concept ne valide pas le script.
- Une pré-autorisation globale (« fais tout », « je te fais confiance jusqu'au rendu ») se consigne dans `decisions.md` avec sa portée exacte : quelles validations elle couvre. Elle ne couvre jamais le premier usage d'un outil payant, un dépassement du budget, ni la revue humaine du rendu final.
- **Aucun crédit dépensé avant le storyboard validé.** Pas d'image, pas de clip, pas de voix ni de musique payante « pour voir ».

### Validations et passage de main par filière

Les trois validations gardent leur objet partout (concept, script ou liste, storyboard) ; leur support et le moment où la main passe changent selon la filière. Une filière qui a validé son `storyboard.md` avant la passation écrit `storyboard: no` dans `BRIEF.md` : le workflow publie alors son plan pour information et continue, sans second point de contrôle du storyboard. Le rendu reste soumis à l'accord de l'humain dans tous les cas.

| Filière | Validation 1 : concept | Validation 2 : script | Validation 3 : storyboard | Passation, champs de `BRIEF.md` |
|---|---|---|---|---|
| Workflows HyperFrames appelés directement (`faceless-explainer`, `product-launch-video`, `pr-to-video`, `music-to-video`, `general-video`) | Étape 2 ci-dessus | `script.md` (étape 3) | Plan du workflow, `hyperframes/STORYBOARD.md`, à son point de contrôle | Après la validation 2 ; `flow: automation`, `storyboard: yes` |
| `reel-talking-head` | Angle et traitement du reel, après l'analyse gratuite de la source (Temps 1) | Script de montage dans `script.md` (Temps 2) | `storyboard.md` aux vignettes au vrai recadrage (Temps 3) | Après la validation 3, par `video-editing` : `general-video` avec `flow: automation`, `storyboard: no` ; `talking-head-recut` sans ces deux champs ; ou ffmpeg |
| `video-repurpose` | Traitement de la série : plateformes, toiles, habillage, sous-titres | Liste des clips notée et validée, devenue `script.md` (étape 3) | `storyboard.md` : vignette au vrai cadrage de chaque clip, habillage prévu (après l'étape 5) | Après la validation 3, par `video-editing` : ffmpeg, ou `general-video` avec `flow: automation`, `storyboard: no` |
| `video-documentary` | Question, thèse, registre (étape 1) | Découpage en emplacements (étape 2), puis narration sur les images retenues (étape 6) | `selections.json` et `storyboard.md` (étape 5) | Après la validation 3 (étape 7) : `general-video` avec `flow: automation`, `storyboard: no` |
| `motion-design` → `hyperframes:motion-graphics` | Étape 2 ci-dessus | `script.md` : cartons, chiffres, temps | `storyboard.md`, avant la passation | Après la validation 3 ; ni `flow` ni `storyboard`, le workflow est autonome par conception |
| Manim (`manim-composer` → `manim-ce`) | Étape 2 ci-dessus | `script.md` | `scenes.md` de `manim-composer`, avec dans `storyboard.md` les plans qui entourent la démonstration | Après la validation 3 : rendu Manim, puis composition par `motion-design` (`general-video` avec `flow: automation`, `storyboard: no`, ou `motion-graphics`) |

## Passer la main à HyperFrames

Pour toute filière HyperFrames : après la validation du script quand le workflow tient lui-même le storyboard, après la validation 3 sinon (table « Validations et passage de main par filière »). Dans une installation en plugin, la skill `hyperframes:hyperframes` fait passer chaque commande `npx hyperframes` par le lanceur du plugin, qui fixe la version du CLI : suivre sa règle pour toutes les commandes de cette section.

**1. Choisir la toile** selon la destination :

| Destination | Toile (`--aspect`, `aspect:`) | Préréglage d'`init` |
|---|---|---|
| Reels, TikTok, Shorts, LinkedIn vertical | `1080x1920` | `portrait` |
| LinkedIn 4:5, l'autre vertical du fil | `1080x1350` | aucun préréglage 4:5 : `portrait`, puis `data-height="1350"` sur la racine de chaque composition (skill `hyperframes:hyperframes-core`) |
| LinkedIn carré (le plus sûr sur ordinateur), fil carré | `1080x1080` | `square` |
| Site, YouTube | `1920x1080` | `landscape` |

**2. Créer le projet HyperFrames** dans un dossier qui n'existe pas encore : `init` refuse un dossier non vide, et le workflow ne relance pas `init` quand `hyperframes.json` existe déjà.

```bash
npx hyperframes init 08-video/projets/<slug>/hyperframes --non-interactive --example=blank \
  --skill=<workflow> --resolution <portrait|square|landscape>
```

**3. Poser la charte de marque** : `frame.md` (le fichier de design qu'HyperFrames lit en premier) et `brand.css`, générés depuis `01-brand/tokens.json`.

```bash
python3 08-video/scripts/brand-frame.py 08-video/projets/<slug>/hyperframes --aspect <toile>
```

**4. Écrire `hyperframes/BRIEF.md`**, qui porte le brief confirmé : le workflow le lit et ne refait pas d'entretien.

```markdown
---
workflow: faceless-explainer
flow: automation
storyboard: yes
message: "La seule chose que la vidéo doit faire passer, en une phrase"
destination: linkedin-feed
aspect: 1080x1080
language: fr
length: 45s
audience: "Persona du brief et ce qu'elle sait déjà du sujet"
angle: concept
narration: yes
voice: ff_siwis
---

## Intent

Ce qu'est la vidéo, pour qui, pourquoi maintenant ; l'objectif business du brief ; le ton, dans les mots de 01-brand/voice.md.

## Assets

- ../script.md : script validé (validation 2), narration à reprendre mot pour mot.
- assets/<fichier> : ce que c'est, où il sert.

## Customizations

- Ce que le concept validé demande en plus, par exemple un compteur animé sur le chiffre clé.

## Notes

- frame.md est généré par 08-video/scripts/brand-frame.py et fait foi : aucun preset de frame-presets, pas de build-frame, aucune recette adoptée, frame.md jamais réécrit.
- VO_MODE : verbatim.
- Voix : celle consignée dans decisions.md ; aucun fournisseur payant sans annonce de coût.
- Rendu seulement après accord explicite, vers ../exports/<slug>-<plateforme>.mp4.
```

`workflow` prend le nom de la filière sans préfixe (`faceless-explainer`, `product-launch-video`, `pr-to-video`, `music-to-video`, `motion-graphics`, `general-video`, `talking-head-recut`). `flow: automation` avec `storyboard: yes` met HyperFrames en mode collaboratif : il s'arrête et attend à ses points de contrôle, ce qui recouvre nos validations. Une filière qui a validé `storyboard.md` avant la passation écrit `storyboard: no` (table « Validations et passage de main par filière »). `motion-graphics` et `talking-head-recut` travaillent sans ces deux champs : leur storyboard se valide avant la passation.

**5. Charger la skill de workflow `hyperframes:<workflow>`.** Elle lit `BRIEF.md` et déroule son storyboard puis la construction. Points de vigilance :

- **Charte.** L'étape de design system des workflows (choix d'un preset dans `frame-presets`, script `build-frame`, recette) se saute : `frame.md` existe et fait foi. Si un `frame.md` a été réécrit, relancer `brand-frame.py`, puis `brand-frame.py --check`.
- **`hyperframes:music-to-video`.** Son étape 3 (« Pick the brand ») copie un preset tel quel dans `frame.md`, et sa porte de contrôle exige que `frame.md` soit une copie conforme d'un preset. Garder le `frame.md` de la marque, remplir le champ `style` du frontmatter de `STORYBOARD.md` (police et palette) depuis `frame.md`, et consigner l'exception dans `decisions.md` : cette condition de la porte est levée par décision, les autres (`validate-plan.mjs` sans erreur, accord sur le plan) restent.
- **Sous-titres.** Sauter l'étape de design system saute aussi la copie de la peau de sous-titres : le script de sous-titres des workflows retombe alors sur sa pastille par défaut (police Roboto, fond noir), hors marque. Exception admise, consignée dans `decisions.md` : copier le seul `caption-skin.html` d'un preset (dossier `frame-presets/` de la skill `hyperframes:hyperframes-creative`) vers `hyperframes/.hyperframes/caption-skin.html` ; le script y injecte les couleurs et les polices de `frame.md` (fichiers de police déposés dans `assets/fonts/`). Sinon, marquer l'étape de sous-titres du workflow comme sautée et sous-titrer avec la skill `captions`, ou `hyperframes:embedded-captions` sur des images filmées.
- **Connexion et médias.** Au départ, le workflow affiche `npx hyperframes auth status` et attend le choix de l'humain : se connecter à HeyGen, ou continuer hors ligne. Connecté, l'étape audio prend la voix chez HeyGen et la musique dans sa bibliothèque. Hors ligne, la voix vient de Kokoro, en local, mais les trois workflows scriptés (`faceless-explainer`, `product-launch-video`, `pr-to-video`) n'ont aucune musique : leur étape audio ne fait que récupérer chez HeyGen. La génération locale de musique (Lyria si une clé Gemini ou Google est présente, sinon MusicGen en local) ne concerne que `hyperframes:general-video` et l'usage direct du moteur. Une vidéo hors ligne qui doit avoir de la musique la reçoit donc à part (voir le contrat de coût). HeyGen et Lyria sont des fournisseurs externes : coût ou quota annoncé avant l'étape audio. Licence de la musique : voir le contrat de coût.
- **Voix et storyboard.** Le point de contrôle du plan (`STORYBOARD.md`) tient lieu de validation 3, et l'étape audio démarre dès qu'il est accepté. Avant de l'accepter : la voix validée est écrite dans le frontmatter de `BRIEF.md` (`voice: ff_siwis` hors ligne, ou l'identifiant de la voix HeyGen retenue si l'humain s'est connecté, car les identifiants changent d'un fournisseur à l'autre), et le coût de la voix et de la musique est annoncé. Vérifier que l'étape audio reçoit bien cette voix (`--voice <id>`) : sans elle, le workflow prend sa voix anglaise par défaut. Une voix payante encore jamais entendue se règle ainsi : accord sur le plan, puis échantillon payant annoncé et validé, et seulement ensuite l'étape audio. Une fois l'échantillon validé, après la validation 3, mettre `voice:` à jour dans `BRIEF.md` avec l'identifiant de la voix retenue, avant de lancer l'étape audio. `hyperframes:motion-graphics` n'a pas de storyboard : la validation 3 se tient sur `storyboard.md` avant de lui passer la main.
- **Rendu.** Jamais automatique. Après `npx hyperframes check` propre et l'aperçu (`npx hyperframes preview`), demander l'accord, puis rendre depuis le dossier `hyperframes/` :

```bash
npx hyperframes render --quality delivery --output ../exports/<slug>-<plateforme>.mp4
```

Rappels : jamais de preset `frame-presets` (hors la peau de sous-titres) dans un projet client ; `frame.md` jamais édité à la main (le modifier, c'est modifier les tokens puis relancer `brand-frame.py`).

## Contrat de coût

Avant tout appel payant (image, clip vidéo, voix, musique, 3D, fournisseur externe d'HyperFrames), annoncer dans la conversation :

- l'outil (nom exact), le fournisseur et le modèle ;
- la raison de ce choix ;
- échantillon ou série ;
- le coût estimé ;
- le solde du budget du projet (`couts.md`) et, quand l'outil le permet, le solde du compte vérifié en direct : outil `account_balance` du MCP Magnific quand il est connecté.

Règles :

- **Un échantillon avant toute série.** Le coût réel de l'échantillon décide de la série.
- **Premier usage d'un outil payant dans un projet** : validation explicite de l'humain, même sous pré-autorisation.
- **Pas de substitution silencieuse.** Jamais changer de fournisseur ou de modèle sans le dire et le consigner dans `decisions.md`. Un modèle indisponible est un blocage, pas l'occasion d'en prendre un autre.
- **`couts.md` à jour** à chaque appel : estimation, dépense réelle, solde du budget.
- **Musique : la licence d'abord, même gratuite.** L'étape audio des workflows HyperFrames choisit seule sa musique, et pas de la même façon selon le workflow. `faceless-explainer`, `product-launch-video` et `pr-to-video` la prennent dans la bibliothèque HeyGen si l'humain est connecté, et n'en ont aucune hors ligne. `hyperframes:general-video` et l'usage direct du moteur la génèrent en local, par Lyria (clé Gemini ou Google) puis par MusicGen. Les poids de MusicGen sont publiés sous licence CC BY-NC 4.0 ([fiche du modèle](https://huggingface.co/facebook/musicgen-small)). Tant que `01-brand/droits.md` n'a pas tranché son usage pour la marque : fournir une piste sous licence établie dans la section `## Assets` de `BRIEF.md`, en précisant qu'elle remplace la musique du workflow ; ou poser `music: none` dans le bloc YAML de tête de `hyperframes/STORYBOARD.md` (la narration reste, seule la musique du workflow est coupée) et ajouter la musique à part, depuis une bibliothèque sous licence ou par Magnific `audio_music_generate` sous ce contrat.

Signaler un blocage en cinq points, puis attendre :

1. Ce qui bloque.
2. Ce qui a été tenté.
3. Les options possibles.
4. La recommandation, avec sa raison.
5. Ce qu'il faut de l'humain : une décision, un accès, une clé, du budget.

## Contrôle avant rendu

- [ ] **Promesse tenue** : une vidéo promise en mouvement a du mouvement réel, pas un diaporama d'images zoomées (`08-video/motion.md`).
- [ ] **Variété** : jamais trois scènes du même type d'affilée.
- [ ] **Narration plus courte que la vidéo** : durée du fichier de voix (`ffprobe -v error -show_entries format=duration -of csv=p=0 <narration.wav>`) inférieure ou égale à la durée de la composition.
- [ ] **Musique assez longue** pour toute la vidéo, ou bouclage prévu sans coupure audible.
- [ ] **Assets tous présents** dans le dossier du projet : `npx hyperframes check` sans requête en échec.
- [ ] **Marque à jour** : `python3 08-video/scripts/brand-frame.py 08-video/projets/<slug>/hyperframes --check` sort 0.
- [ ] **Revue de singularité** répondue dans `decisions.md`.

## QA et revue

```bash
python3 08-video/scripts/qa-video.py 08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4 \
  --plateforme <reels|tiktok|shorts|linkedin> --duree <secondes> --script 08-video/projets/<slug>/script.md
```

- Sans piste son : `--sans-audio`. Sans voix (musique seule) : sans `--script` ; une colonne Voix vide dans `script.md` désactive de toute façon la vérification de couverture. Destination hors des quatre plateformes de `08-video/scripts/plateformes.toml` (site, YouTube) : lancer sans `--plateforme`.
- La QA écrit dans `08-video/projets/<slug>/qa/<nom>/` une image au milieu de chaque plan, une planche contact et `rapport.md`. Code 0 : aucun constat bloquant ; 1 : constats bloquants ; 2 : erreur d'usage ou d'outil.
- Puis dispatcher l'agent `video-reviewer` (lecture seule) avec le rendu, `brief.md`, `script.md` et la plateforme : message et appel à l'action, marque, zones de sécurité, mouvement et variété, sous-titres, divulgation, crédits.
- **Deux tours de correction au plus** sur les constats de la QA et de la revue. Au-delà, remonter à l'humain avec l'état des constats.
- **La revue humaine du rendu final reste obligatoire**, quel que soit le résultat de la QA.

## Livraison

1. **`brand-check`** sur le script et sur l'habillage du rendu.
2. **Divulgation IA** selon `01-brand/divulgation-ia.md` : clips générés, voix de synthèse, musique générée.
3. **Crédits et droits** : `credits.md` du corpus documentaire, licences du stock et de la musique, droit d'embarquer la police, accord des personnes filmées ; vérification dans `01-brand/droits.md`.
4. **Calendrier** : statut de l'entrée dans `02-strategy/calendar/calendar.md` (`idée → brouillon → à-valider → validé → publié`).
5. **Inventaire** : `python3 scripts/build-inventory.py --add 08-video/projets/<slug>/script.md`.
6. **Capitalisation** dans `decisions.md` : prompts, voix et réglages validés, et les échecs avec leur raison, pour qu'ils ne soient pas retentés.
7. **`REPRISE.md`** passé à l'état « livré ».

## Checklist avant livraison

- [ ] Trois validations obtenues (concept, script, storyboard), chacune notée dans `decisions.md` avec sa date
- [ ] Aucun crédit dépensé avant la validation 3 ; chaque appel payant annoncé et inscrit dans `couts.md`
- [ ] Voix validée et consignée ; musique sous licence établie (`01-brand/droits.md`)
- [ ] Contrôle avant rendu coché ; rendu fait après l'accord de l'humain sur l'aperçu
- [ ] `qa-video.py` sans constat bloquant, ou constats restants acceptés par l'humain ; revue `video-reviewer` traitée
- [ ] Revue humaine du rendu final faite
- [ ] Références d'inspiration citées avec lien et créateur ; aucun prompt, visuel ni code de créateur repris (`08-video/inspiration.md`)
- [ ] `brand-check`, divulgation IA, crédits et droits faits
- [ ] Calendrier, inventaire, capitalisation et `REPRISE.md` à jour

## Reprendre une session

1. Lire `REPRISE.md`, puis `decisions.md` (la dernière ligne de chaque sujet fait foi) et `couts.md`.
2. Projet HyperFrames : lire `hyperframes/BRIEF.md` et `hyperframes/STORYBOARD.md` (le mode de travail en cours est dans son frontmatter) ; pour savoir ce qui est construit, `npx hyperframes timeline --json` depuis `hyperframes/`.
3. Reprendre à la prochaine action notée, sans refaire le cadrage ni l'entretien.

## Ce que cette skill ne fait pas

- Publier : la publication reste une décision humaine.
- Décider la doctrine de marque : `01-brand/`.
- Écrire le post qui accompagne la vidéo : `social-content`.
- Faire une présentation ou un deck : `slides`.
- Le détail technique de chaque étape : les skills de la table « Choisir la filière ».

---

Méthode inspirée d'OpenMontage (calesthio/OpenMontage, AGPLv3), réécrite pour le template : aucun texte ni code repris. Registre : docs/vendored-video.md.
