---
name: video-editing
description: Montage de rushes pour {{COMPANY_NAME}} (face caméra, interview, capture d'écran, clips générés), du script minuté à l'export par plateforme. Deux voies, un projet HyperFrames (hyperframes:talking-head-recut pour habiller un face caméra, hyperframes:general-video pour un montage libre) ou un plan de montage ffmpeg (découpe, coupe des silences, recadrage 9:16 suivi, concaténation, export normalisé à -14 LUFS). Habillage aux variables de brand.css, doctrine de 08-video/montage.md et 08-video/formats.md, QA par qa-video.py. Appelée par video-production, reel-talking-head et video-repurpose. Ne fait ni le sous-titrage (skill captions) ni la génération de rushes (skill video-generation).
---

# video-editing : monter des rushes pour {{COMPANY_NAME}}

Vous transformez des rushes en vidéo montée, habillée aux couleurs de la marque et exportée aux bons formats. La skill est appelée par `video-production` (point d'entrée de toute demande vidéo), `reel-talking-head` ou `video-repurpose`, qui ont ouvert le projet, tiennent les validations et le budget. Lire `08-video/CLAUDE.md` et `08-video/README.md` (outillage) avant la première production.

## Références à charger avant de commencer

1. `08-video/formats.md` : ratios, durées, zones de sécurité de la plateforme cible.
2. `08-video/montage.md` : coupe, rythme, son, démo produit.
3. `08-video/narration.md` : dès qu'une voix off s'ajoute aux rushes.
4. `01-brand/style-guide.md` : couleurs, police, style, tropes bannis.
5. `01-brand/voice.md` : pour tout texte à l'écran.
6. `03-social-media/<canal>/examples/` : calibrer accroches et ton sur ce qui a déjà marché.

## Étape 1 : le brief

Le projet vit dans `08-video/projets/<slug>/`, créé par `video-production` au cadrage, avec `brief.md` (objectif business, canal, durée, persona, message unique, matière, appel à l'action, budget), `REPRISE.md`, `decisions.md` et `couts.md`. Les rushes sont rangés dans `rushes/`.

Pas de brief validé, pas de montage. Une demande de montage qui arrive sans projet passe d'abord par `video-production`.

## Étape 2 : la structure (le script minuté)

Le script s'écrit dans `08-video/projets/<slug>/script.md`, au format de `video-production` (une ligne par plan, une seule colonne « Voix », celle que `qa-video.py --script` compare à la transcription du rendu). Les règles du format court, actionnables et non décoratives :

- **Accroche en 3 secondes au plus** : la première image pose une tension (question, chiffre surprenant, résultat avant/après, contradiction). Si l'accroche ne tient pas en une phrase lisible à l'arrêt sur image, elle est ratée. Proposer **3 variantes d'accroche**, validation humaine obligatoire.
- **Une coupe toutes les 2 à 4 s** : jamais plus de 4 s sur le même plan sans changement (zoom, plan, texte), règle de `08-video/montage.md`. Les tenues de 4 à 5 s sont des temps forts voulus, réservés aux moments émotionnels : `qa-video.py` les signale en avertissement (`plan-long`, plafond `--max-plan` de 4 s par défaut), à accepter en connaissance de cause. Le rythme se voit dans le tableau minuté.
- **Texte à l'écran en permanence** : la majorité regarde sans le son. Chaque segment a son texte (repris par la skill `captions`).
- **Une idée, une vidéo** : si le script contient « et aussi », couper ; c'est la vidéo suivante.
- **Appel à l'action en fin, une seule action** : commenter, suivre ou cliquer, pas les trois.
- **Boucle** : si possible, la dernière seconde renvoie visuellement à la première (la relecture est un signal fort sur TikTok et Reels).

```markdown
| # | Temps | Image | Voix | Texte à l'écran | Jeu |
|---|---|---|---|---|---|
| 1 | 0:00-0:03 | ... (ACCROCHE) | ... | ... | ... |
| 2 | 0:03-0:08 | ... | ... | ... | ... |
```

## Étape 3 : le montage

Deux voies. La voie A quand la vidéo demande un habillage designé ou un montage de plusieurs sources dans une composition ; la voie B pour un assemblage simple, ou pour préparer les rushes avant la voie A.

### Voie A : projet HyperFrames

Deux workflows du plugin HyperFrames (installé par `/modules`) :

- **`hyperframes:talking-head-recut`** : rushes face caméra, interview ou podcast filmé, habillés de cartes designées calées sur la parole (titres, lower-thirds, chiffres, citations, incrustations). Le workflow ne coupe pas : la séquence passe telle quelle sous l'habillage. Les coupes (silences, redites, aparté final) se font donc avant, par la voie B ou par le script `transcript-cut.mjs` de la skill `hyperframes:media-use`, qui coupe d'après la transcription.
- **`hyperframes:general-video`** : montage libre de rushes. Couper, réordonner, recadrer, remixer, reconstituer une séquence à partir de plusieurs sources (rushes, captures d'écran, clips générés). Chaque plan est un `<video>` placé par `data-start`, `data-duration` et `data-media-start` (skill `hyperframes:hyperframes-core`) ; un zoom ou un recadrage animé passe par les keyframes d'un conteneur intérieur (skill `hyperframes:hyperframes-keyframes`) ; le mixage par la skill `hyperframes:hyperframes-audio`.

Avec `hyperframes:talking-head-recut`, deux réglages du workflow se corrigent, comme le fait la skill `captions` pour `hyperframes:embedded-captions` :

- **Transcription en français.** Son étape 4 (« Transcribe ») lance `npx hyperframes transcribe … --model small.en`, un modèle anglais qui traduit l'audio français en anglais. Passer outre : `npx hyperframes transcribe <audio> -d <dossier de travail> --json --model small --language fr`, ou déposer dans le dossier de travail un `transcript.json` au format du workflow (tableau plat de mots `{ "text", "start", "end" }`, en secondes) tiré de la transcription whisper de la skill `captions`. Relire la transcription comme le demande son étape 5.
- **Style des cartes.** Son étape 7 (« Decide Render Strategy ») fait choisir un groupe de style de cartes (`warm-paper`, `clinical`, `experimental`) ; chaque style apporte ses polices et ses couleurs, et la palette `themeId` pose `--accent-N`, `--bg` et `--text`. Choisir le style le plus proche de la marque (`01-brand/style-guide.md`, profil de goût de `decisions.md`), puis remplacer ses polices et ses couleurs par les variables de `brand.css` (`--accent-N`, `--bg` et `--text` comprises, prises dans les `--brand-*`) : les polices livrées par le workflow (Caveat, Inter, Virgil…) cèdent la place à celles de la marque. Consigner l'exception dans `decisions.md`.

Préparation, dans cet ordre :

1. **Le projet HyperFrames est préparé par `video-production`** (création dans `08-video/projets/<slug>/hyperframes/`, `BRIEF.md` avec `workflow: talking-head-recut` ou `workflow: general-video`) **et `motion-design`** (`frame.md` et `brand.css` générés par `brand-frame.py`). Ne pas les écrire ici.
2. **Rushes copiés dans le dossier du projet HyperFrames** (`hyperframes/assets/`), jamais chargés depuis une URL ni depuis un chemin hors du projet. Les originaux restent dans `rushes/`.
3. **Chaque `<video>` est muet** (`muted`, `playsinline`) ; le son passe par un `<audio>` séparé, qui a un `id` (règles de rendu de `motion-design`).
4. **Validation 3.** L'entretien de `hyperframes:talking-head-recut` ne pose pas les questions de mode de travail : comme pour `hyperframes:motion-graphics`, la validation du storyboard se tient sur `storyboard.md`, avant la passation. Quand `storyboard.md` est déjà validé à l'appel (`reel-talking-head`, `video-repurpose`, `video-documentary`), `hyperframes:general-video` reçoit `flow: automation` et `storyboard: no` dans `BRIEF.md`, pour ne pas rouvrir un second point de contrôle du storyboard. Appelé directement en mode collaboratif (`flow: automation`, `storyboard: yes`), son `STORYBOARD.md` en tient lieu. Table « Validations et passage de main par filière » de `video-production`.
5. **Contrôles** : `npx hyperframes lint`, puis `npx hyperframes check`, puis l'aperçu (`npx hyperframes preview`). Rendu seulement après l'accord de l'humain, depuis le dossier `hyperframes/` :

```bash
npx hyperframes render --quality delivery --output ../exports/<slug>-<plateforme>.mp4
```

Dans une installation en plugin, chaque commande `npx hyperframes` passe par le lanceur du plugin (règle de la skill `hyperframes:hyperframes`).

### Voie B : plan de montage ffmpeg

Produire un **plan de montage** : une suite de commandes ffmpeg commentées dans `08-video/projets/<slug>/montage.sh`, exécutées après validation humaine, depuis le dossier du projet (`cd 08-video/projets/<slug>` depuis la racine du dépôt) : les chemins des commandes ci-dessous en partent. Les fichiers intermédiaires vont dans `rushes/tmp/` (non versionné). Briques types :

```bash
# Découper un segment (sans réencodage si les points tombent sur des images clés)
ffmpeg -ss 00:00:12 -to 00:00:18 -i rushes/plan1.mp4 -c copy rushes/tmp/seg1.mp4

# Recadrer un 16:9 en 9:16 (recadrage centré puis mise à l'échelle)
ffmpeg -i rushes/tmp/seg1.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" rushes/tmp/seg1-vertical.mp4

# Concaténer les segments (rushes/tmp/liste.txt : file 'seg1-vertical.mp4' ..., chemins relatifs à la liste)
ffmpeg -f concat -safe 0 -i rushes/tmp/liste.txt -c:v libx264 -crf 18 -c:a aac rushes/tmp/montage.mp4

# Poser un clip 9:16 sur fond de marque (déclinaison 1:1 LinkedIn)
ffmpeg -i rushes/tmp/montage.mp4 -vf "scale=608:1080,pad=1080:1080:236:0:color={{BRAND_COLOR_DARK}}" rushes/tmp/carre.mp4
```

La couleur du fond se lit dans `01-brand/tokens.json` (la même que `--brand-dark` dans `brand.css`) : ffmpeg ne lit pas les variables CSS.

**Couper les silences.** whisper aligne les mots bord à bord : les vrais silences se mesurent sur le son.

```bash
# 1. Repérer les silences de 0,3 s ou plus sous -30 dB
ffmpeg -i rushes/face.mp4 -af silencedetect=noise=-30dB:d=0.3 -f null - 2> rushes/tmp/silences.txt
grep -E "silence_(start|end)" rushes/tmp/silences.txt

# 2. Garder ce qui se trouve entre la fin d'un silence et le début du suivant ; réencoder pour couper à l'image près
ffmpeg -ss 0 -to 2.08 -i rushes/face.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac rushes/tmp/garde-01.mp4
ffmpeg -ss 2.96 -to 18.40 -i rushes/face.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac rushes/tmp/garde-02.mp4

# 3. Recoller (rushes/tmp/garde.txt : file 'garde-01.mp4', file 'garde-02.mp4' ...)
ffmpeg -f concat -safe 0 -i rushes/tmp/garde.txt -c copy rushes/tmp/sans-silences.mp4
```

- La liste des segments gardés s'écrit dans `montage.sh`, avec pour chacun la phrase qu'il contient : elle se relit avant l'exécution.
- Laisser une marge de chaque côté de la coupe : une respiration se resserre, elle ne se supprime pas (repère de `reel-talking-head` : vers 0,12 s).
- Une coupe ne change jamais le sens : la personne dit ce qu'elle a dit, dans l'ordre où elle l'a dit.

**Recadrer 16:9 en 9:16 en suivant le sujet.** Le recadrage centré coupe un sujet décentré. Choisir l'abscisse du cadre plan par plan :

```bash
# Image du milieu du plan, pour placer le cadre
ffmpeg -ss 4.5 -i rushes/tmp/plan-03.mp4 -frames:v 1 rushes/tmp/plan-03.jpg

# Bord gauche de la zone gardée à 220 px de la source (de 0 à iw - ih*9/16, soit 1312 px pour une source 1920x1080)
ffmpeg -i rushes/tmp/plan-03.mp4 -vf "crop=ih*9/16:ih:220:0,scale=1080:1920" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac rushes/tmp/plan-03-9x16.mp4
```

- Un sujet qui se déplace dans le plan, ou deux personnes qui se répondent : découper le plan à chaque déplacement ou changement de personne qui parle, choisir le cadre de chaque morceau, puis concaténer. Un cadre qui glisse en continu se fait dans la voie A (keyframes sur le conteneur de recadrage).
- Le visage et la zone utile restent dans les zones de sécurité de `08-video/formats.md`.
- Depuis une source 1080p, le recadrage 9:16 garde une bande d'environ 608 px agrandie à 1080 px, donc plus douce : préférer une source 4K quand elle existe.

### Règles de précision (éprouvées en production)

- **Positions en images entières** : un point d'entrée exprimé en secondes peut tomber entre deux images et décaler le plan d'une image. Caler entrées et sorties sur des images entières (à 30 images par seconde, des multiples de 1/30 s) ; sur une voix, une image de décalage s'entend à la couture.
- **Aucun trou entre deux plans** : un plan posé une image trop court laisse un flash de fond au rendu. Dans un projet HyperFrames, `npx hyperframes timeline --json` liste les débuts et fins de chaque plan ; les relire après chaque série de coupes.
- **Zoom et recadrage par une échelle supérieure à 1** : garder 86 % du cadre revient à une échelle de 1/0,86, soit environ 1,163. Un punch-in continu est une échelle interpolée linéairement sur toute la durée du plan.
- **Rushes issus d'un modèle génératif qui refait parler quelqu'un** (synchronisation labiale, image vers vidéo sur une voix) : contrôle de fidélité du texte **avant** de les poser dans le montage, voir la skill `video-generation`, section « Fidélité du texte ». C'est le contrôle le plus important de la chaîne.

### Montage à sources régénérées (voix)

Quand une zone joue l'audio d'un fichier régénéré (phrasé différent de l'original) : **un clip audio continu par zone** (WAV extrait du fichier), jamais les audios liés plan par plan, sinon chaque coupe devient une épissure audible. Couper le son de tous les clips vidéo de la zone, puis recaler sous-titres et effets sonores sur les attaques du fichier régénéré.

## Étape 4 : l'habillage aux couleurs de la marque

Tout élément graphique prend ses valeurs dans les variables de `brand.css` (générées depuis `01-brand/tokens.json` par `brand-frame.py`), jamais en dur :

- **Textes à l'écran** : police `var(--font-display)` ({{BRAND_FONT_PRIMARY}}), couleurs `--brand-light` et `--brand-primary`, ou `--brand-text-on-dark` sur un fond sombre ; jamais plus de 2 niveaux de texte simultanés.
- **Fonds, bandeaux, transitions** : `--brand-dark`, `--brand-primary`, `--brand-gradient` ({{BRAND_GRADIENT}}) ; aucune couleur hors palette.
- **Logo** : plan de fin uniquement (ou discret en zone sûre), depuis `01-brand/assets/`.
- **Interdits** : les tropes bannis ({{BRAND_BANNED_VISUALS}}), les gabarits d'habillage génériques, les emojis en pluie, les effets interdits par `08-video/motion.md`.
- **Zones de sécurité** : aucun texte dans les marges de `08-video/formats.md`, reprises dans `frame.md` (`safe-top`, `safe-bottom`, `safe-left`, `safe-right`).

Les éléments animés (titres, lower-thirds, chiffres, plan de fin) passent par la skill `motion-design`. Dans la voie B, les valeurs se lisent dans `01-brand/tokens.json`.

Sous-titres : déléguer à la skill **`captions`** (transcription, segments, `.srt`, sous-titres incrustés aux couleurs de la marque).

## Étape 5 : l'export par plateforme

Un export par canal cible, nommé `08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4`, aux specs de `08-video/formats.md`. Comme les commandes de la voie B, celle-ci se lance depuis le dossier du projet ; la QA, elle, se lance depuis la racine du dépôt (section suivante).

```bash
cd 08-video/projets/<slug>    # depuis la racine du dépôt
# Export final : H.264 yuv420p, son normalisé à -14 LUFS (crête vraie -1,5 dBTP), AAC 48 kHz, lecture web rapide
ffmpeg -i rushes/tmp/final.mp4 -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart exports/<slug>-<plateforme>.mp4
```

- Un rendu HyperFrames qui n'a que le son hors cible (constat `loudness` de `qa-video.py`) repasse par la même commande avec `-c:v copy` à la place des réglages vidéo : l'image n'est pas réencodée.
- Si `qa-video.py` signale encore `loudness` après ce passage, faire la normalisation en deux passes (mesure, puis application des valeurs mesurées) décrite par la skill `hyperframes:media-use`.
- **Sous-titres incrustés ensuite par ffmpeg** (skill `captions`) : exporter vers `rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4` (rendu HyperFrames compris : `--output ../rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4`) ; c'est l'incrustation qui écrit le livrable `exports/<slug>-<plateforme>.mp4`, celui que contrôlent la QA et la revue.
- Garder le master avant compression (rendu HyperFrames ou `rushes/tmp/final.mp4`) : c'est lui qu'on archive sur le stockage du client, hors git.
- **Un rendu long se surveille en tâche de fond** (sortie du processus, taille du fichier qui grossit), jamais par une boucle d'attente `sleep` au premier plan, que l'environnement d'exécution peut bloquer.

### Avant de livrer

**Transcrire le master final et le comparer au texte attendu** : un master peut provenir d'un état antérieur du montage (même durée, contenu différent). Depuis la racine du dépôt :

```bash
python3 08-video/scripts/qa-video.py 08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4 \
  --plateforme <reels|tiktok|shorts|linkedin> --duree <secondes> --script 08-video/projets/<slug>/script.md
```

Le constat `transcription-couverture` signale un passage du script absent du rendu. Un mot que la transcription déforme sous un effet sonore se vérifie par corrélation d'enveloppe avec la source (au-dessus de 0,9 : fidèle ; méthode dans `video-generation`). Puis l'agent `video-reviewer`, comme le prévoit `video-production` § « QA et revue ».

## Checklist avant livraison

- [ ] Accroche lisible à l'arrêt sur image, validée par un humain
- [ ] Aucun plan de plus de 4 s sans changement, hors tenues de 4 à 5 s voulues (avertissements `plan-long` acceptés)
- [ ] Sous-titres présents (skill `captions`), hors zones de sécurité
- [ ] Habillage 100 % variables de `brand.css` (ou valeurs de `01-brand/tokens.json` en voie B), zéro trope banni
- [ ] Un export conforme par plateforme (`08-video/formats.md`), dans `exports/`
- [ ] `qa-video.py` sans erreur (constats restants acceptés par l'humain)
- [ ] Revue `video-reviewer` traitée
- [ ] Divulgation IA selon `01-brand/divulgation-ia.md` si clips générés ou voix de synthèse : mention en tête du contenu (carton d'ouverture ou première ligne de description)
- [ ] `brand-check` sur le script et les textes à l'écran
- [ ] Statut mis à jour dans le calendrier éditorial

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/video-courte.md` pour le détail sourcé :

1. **Gabarit de script imposé** : accroche 0-3 s, apport de valeur 4-15 s, révélation, puis appel à l'action dans les 5 dernières secondes, avec un temps visuel ou narratif toutes les 5 à 7 secondes.
2. **Jamais de logo, de jingle ni de plan d'installation en ouverture** : 50 à 60 % des abandons ont lieu dans les 3 premières secondes.
3. **Couper 20 à 30 % du script au montage** (intros, transitions, redites) : la complétion bat la durée ; 45 s complétées à 70 % surperforment 15 s complétées à 40 %.
4. **Durées cibles par plateforme** : TikTok 60-180 s (substance) ; Reels 15-30 s (portée) ou 60-90 s (récit) ; Shorts 25-40 s ; LinkedIn moins de 60-90 s, vertical 9:16 ou 4:5, téléversement natif uniquement.
5. **Une déclinaison par plateforme, jamais de republication brute** (un filigrane TikTok sur Reels est sous-distribué) : adapter au minimum l'accroche, les sous-titres, le ratio et le son.
6. **Rendu « créateur », pas corporate** en organique : smartphone, face caméra, imperfections assumées ; tout contenu promotionnel sur TikTok exige le label de contenu commercial natif activé.

## Doctrine de montage

Les règles de coupe, de rythme et de plan sonore (coupes franches, J-cuts et L-cuts, raccord d'échelle d'au moins 20 %, punch-in continu, médiane des plans, silence) sont dans **`08-video/montage.md`** : les charger avant tout montage narratif (face caméra, documentaire, interview). Pour orchestrer la transformation complète d'une vidéo brute de client en reel : skill `reel-talking-head`.

## Ce que cette skill ne fait pas

- Publier : validation humaine, publication par le module social.
- Le sous-titrage : skill `captions`.
- Les visuels fixes : skill `image-generation`.
- Générer des rushes IA : skill `video-generation` ; détourer : skill `video-matting`.
- Choisir la filière, tenir les validations ou le budget : skill `video-production`.
