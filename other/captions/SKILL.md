---
name: captions
description: Sous-titrage vidéo pour {{COMPANY_NAME}}. Transcription (whisper local, transcription au mot d'HyperFrames ou API), relecture, découpage en segments lisibles, fichier .srt propre, sous-titres incrustés aux couleurs de la marque via ffmpeg (.srt ou .ass, karaoké mot à mot), et sous-titres designés par HyperFrames (hyperframes:embedded-captions sur un face caméra, peau de sous-titres dans un workflow). Règles de lisibilité et zones de sécurité de 08-video/formats.md. À utiliser dès qu'une vidéo doit être sous-titrée (Reels, TikTok, Shorts, LinkedIn, webinaire, interview). Le montage relève de video-editing, l'orchestration de video-production.
---

# captions : sous-titrage aux couleurs de la marque

Vous produisez, pour chaque vidéo, deux livrables : un **`.srt`** propre dans `08-video/projets/<slug>/sous-titres/`, et une version aux **sous-titres incrustés**, conforme aux règles de `08-video/formats.md` (lisibilité, zones de sécurité) et à la marque (`01-brand/style-guide.md`, `frame.md` du projet).

**Noms des fichiers.** Le livrable que contrôlent `qa-video.py` et l'agent `video-reviewer` est `08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4`. Quand les sous-titres s'incrustent par ffmpeg, le montage sans sous-titres attend dans `08-video/projets/<slug>/rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4`, et c'est l'incrustation qui écrit le livrable dans `exports/`. Dans les commandes ci-dessous, `<nom>` vaut `<slug>-<plateforme>` (ou `<slug>-clip-<nn>-<plateforme>` pour un clip de `video-repurpose`).

## Étape 1 : transcription

### Option A : whisper local (gratuit, privé, recommandé)

```bash
# Son en mono 16 kHz, puis whisper-cli (brew install whisper-cpp) avec le modèle déclaré dans .env (WHISPER_MODEL)
ffmpeg -i 08-video/projets/<slug>/rushes/tmp/<nom>-sans-sous-titres.mp4 -vn -ac 1 -ar 16000 08-video/projets/<slug>/rushes/tmp/<nom>.wav
whisper-cli -m <modèle> -f 08-video/projets/<slug>/rushes/tmp/<nom>.wav -l fr -osrt \
  -of 08-video/projets/<slug>/sous-titres/<nom>
```

- `<modèle>` est le chemin du modèle ggml renseigné dans `.env` (`WHISPER_MODEL`), le même que lit `qa-video.py`.
- Timings au mot, pour le karaoké et les coupes : ajouter `-ml 1 -sow -oj` (un mot par segment, sortie JSON).
- Autre voie locale : `npx hyperframes transcribe <vidéo> --model small --language fr`, la transcription au mot d'HyperFrames (skill `hyperframes:media-use`), par le lanceur du plugin quand HyperFrames est installé en plugin. Toujours un modèle multilingue (sans suffixe `.en`) et la langue : le modèle par défaut, `small.en`, traduit l'audio français en anglais. `medium` ou `large-v3` pour un son bruité ou une musique sous la voix.

### Option B : API de transcription

Sans calcul local possible : une API de transcription (par exemple l'API Whisper d'OpenAI, `model=whisper-1`, sortie `srt`). Clé dans `.env`, jamais en dur. La vidéo part alors chez un tiers : vérifier que le contenu n'est pas confidentiel avant l'envoi.

### Relecture obligatoire

La transcription brute contient toujours des erreurs : noms propres, marque ({{COMPANY_NAME}}), vocabulaire métier, chiffres. Relire intégralement et corriger avant toute incrustation : un chiffre faux incrusté est une faute publique. Vérifier aussi le vocabulaire banni de `01-brand/voice.md` si le texte affiché est retouché.

Les homophones se corrigent dans le texte affiché (la transcription écrit ce qu'elle entend, « qu'il dit » pour « qui le dit ») ; l'audio, lui, est juste.

## Étape 2 : découpage en segments lisibles

whisper produit des segments trop longs pour du vertical. Redécouper le `.srt` :

- **42 caractères par ligne au plus, 2 lignes au plus** ; en 9:16, viser plutôt **25 caractères, 1 ligne** (gros et centré).
- **1 à 3 s par segment**, synchronisé sur le rythme de parole ; jamais un segment à cheval sur une coupe.
- **Vitesse de lecture** : 12 à 15 caractères par seconde, espaces et ponctuation compris (`08-video/formats.md` § « Texte à l'écran », avec sa source). Contrôle : caractères du segment divisés par sa durée.
- Couper aux frontières naturelles (groupes de sens), pas au milieu d'un groupe nominal.
- Ponctuation minimale : pas de point final sur chaque segment ; garder `?` et `!`, qui portent le ton.
- Mots-clés en MAJUSCULES avec parcimonie (un par segment au plus) pour l'emphase.

```srt
1
00:00:00,000 --> 00:00:01,800
Vous perdez 3 heures par semaine

2
00:00:01,800 --> 00:00:03,200
sur VOS reportings ?
```

## Étape 3 : livrable 1, le `.srt`

- Nommage : `08-video/projets/<slug>/sous-titres/<nom>.srt`, même nom que le livrable vidéo.
- Encodage UTF-8, timecodes `HH:MM:SS,mmm`, numérotation continue.
- Usage : téléversement YouTube (indexation, traduction automatique), archivage, réédition.

## Étape 4 : livrable 2, incrustation par ffmpeg

Les sous-titres incrustés reprennent les valeurs de la marque : police `{{BRAND_FONT_PRIMARY}}`, couleurs lues dans `01-brand/tokens.json` (les mêmes que `--brand-light`, `--brand-dark` et `--brand-accent` de `brand.css`).

**Vérifier d'abord que l'ffmpeg de la machine embarque libass** : `ffmpeg -filters | grep subtitles`. Certaines builds n'ont ni `subtitles`, ni `ass`, ni `drawtext`. Dans ce cas, installer une build qui les embarque, ou passer par la voie HyperFrames (section suivante) ; ne jamais promettre une incrustation avant ce contrôle.

### Méthode simple : filtre `subtitles` avec style forcé

```bash
# Police et couleurs de marque. Les couleurs ASS s'écrivent &HAABBGGRR& (ordre bleu, vert, rouge inversé) :
# convertir {{BRAND_COLOR_LIGHT}} et {{BRAND_COLOR_DARK}} avant de remplir PrimaryColour et OutlineColour.
# MarginV=110 place les sous-titres au-dessus de la zone basse de sécurité en 1080x1920 (formats.md).
ffmpeg -i 08-video/projets/<slug>/rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4 \
  -vf "subtitles=08-video/projets/<slug>/sous-titres/<slug>-<plateforme>.srt:force_style='FontName={{BRAND_FONT_PRIMARY}},FontSize=15,Bold=1,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=110'" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart \
  08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4
```

Le son, déjà normalisé à l'export du montage (`video-editing`, étape 5), est recopié tel quel (`-c:a copy`).

Prérequis : la police `{{BRAND_FONT_PRIMARY}}` installée sur la machine, sinon libass prend une police de secours sans prévenir (vérifier à l'image). `FontSize` s'exprime relativement à la résolution de la piste ASS : contrôler le rendu sur une image avant l'incrustation complète :

```bash
# Contrôle visuel rapide : une image sous-titrée à t = 2 s, avec le même filtre que ci-dessus
ffmpeg -i 08-video/projets/<slug>/rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4 \
  -vf "subtitles=08-video/projets/<slug>/sous-titres/<slug>-<plateforme>.srt:force_style='...'" \
  -ss 2 -frames:v 1 08-video/projets/<slug>/rushes/tmp/controle.png
```

### Méthode fine : fichier `.ass` (style par segment, positions, karaoké)

Pour un style au segment près (mot surligné, changement de couleur, position variable), convertir en `.ass` et éditer le bloc `[V4+ Styles]` :

```bash
ffmpeg -i 08-video/projets/<slug>/sous-titres/<nom>.srt 08-video/projets/<slug>/sous-titres/<nom>.ass
# éditer les styles, puis :
ffmpeg -i 08-video/projets/<slug>/rushes/tmp/<nom>-sans-sous-titres.mp4 \
  -vf "ass=08-video/projets/<slug>/sous-titres/<nom>.ass" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart \
  08-video/projets/<slug>/exports/<nom>.mp4
```

C'est la voie ffmpeg du karaoké (section « Karaoké mot à mot »). À réserver aux vidéos à fort enjeu : le coût d'édition est réel.

## Sous-titres designés (HyperFrames)

Deux cas, selon ce qu'on sous-titre. Le plugin HyperFrames est installé par `/modules` ; ses commandes passent par le lanceur du plugin (skill `hyperframes:hyperframes`).

### Une vidéo face caméra : `hyperframes:embedded-captions`

- **Pour** une vidéo face caméra à un seul sujet. Le workflow ajoute les sous-titres sans toucher à l'image, et fait en local la transcription et le détourage du sujet.
- **Où** : dans le dossier de la vidéo, toujours `08-video/projets/<slug>/hyperframes-sous-titres/`, jamais `hyperframes/` (réservé à la composition du projet, avec son `frame.md` et son `brand.css`, même quand elle n'existe pas encore). Le workflow initialise ce projet lui-même (`init` avec `--skill=embedded-captions`). La vidéo d'entrée est le montage sans sous-titres (`rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4`) ; le fichier final du workflow (`final.mp4`, ou `final_fx.mp4` pour une identité à thème) se copie vers `exports/<slug>-<plateforme>.mp4`, le livrable contrôlé. Les images de détourage (`frames_fg/`, `frames_bg/`), les caches (`.media/`) et les rendus ne sont pas versionnés.
- **Refus** : plusieurs intervenants, plans coupés, pas de parole, sous-titres déjà incrustés dans la source. Un montage avec des coupes franches se découpe plan par plan avant, ou se sous-titre par la voie ffmpeg.
- **Le style** se choisit dans le catalogue d'identités du workflow. Par défaut, le rail discret `anchor` : un sous-titre fidèle en bas de l'image, et au plus un mot fort promu derrière le sujet au temps fort. Présenter deux ou trois identités proches de la marque (`01-brand/style-guide.md`, profil de goût de `decisions.md`), en recommander une, laisser l'humain choisir, et consigner le choix dans `decisions.md`.
- **Police et couleurs** : la cible reste celle de `frame.md`. Les identités du catalogue fixent leur propre typographie et leur palette (certaines prennent l'accent dans l'image), et le workflow ne les repeint pas. Si la charte doit être tenue à la lettre, préférer la voie ffmpeg de cette skill, avec la police et les couleurs de la marque. L'écart accepté se consigne dans `decisions.md`.
- Relecture de la transcription du workflow comme à l'étape 1 : un mot inventé incrusté reste une faute publique.

### Une composition HyperFrames : la peau de sous-titres

Dans les workflows narrés scriptés (`hyperframes:faceless-explainer`, `hyperframes:product-launch-video`, `hyperframes:pr-to-video`), les sous-titres sont une piste de la composition, calée sur les timings au mot de la voix. Ils prennent la police et les couleurs de `frame.md` par la peau de sous-titres, seule exception admise aux presets d'HyperFrames : `video-production` § « Passer la main à HyperFrames », point « Sous-titres ». Sans cette peau, marquer l'étape de sous-titres du workflow comme sautée et sous-titrer le rendu avec cette skill. Dans `hyperframes:general-video`, la piste de sous-titres s'écrit dans la composition : elle prend les variables de `brand.css`, comme le reste de l'habillage.

## Karaoké mot à mot

Un groupe de 3 à 5 mots visible, le mot prononcé coloré :

1. **Transcrire avec les timings au mot** : `whisper-cli ... -ml 1 -sow -oj` (étape 1). Un découpage automatique en groupes de 1 ou 2 mots aux timings approximatifs ne convient pas.
2. **Regrouper en groupes de 3 à 5 mots**, coupés aux frontières de sens, sans groupe à cheval sur une coupe.
3. **Mot actif** en `--brand-accent` ({{BRAND_COLOR_ACCENT}}), fond `--brand-dark` semi-opaque, groupe centré vers 65 % de la hauteur, dans la zone utile de `08-video/formats.md`.
4. **Réalisation** :
   - dans une composition HyperFrames, une piste de sous-titres pilotée par les timings : rendu vectoriel, corrigible au mot près, qui suit les changements de montage à chaque nouveau rendu ;
   - par ffmpeg, un `.ass` avec une ligne `Dialogue` par mot actif : le groupe entier, le mot courant recoloré par une balise `{\c&HBBGGRR&}`.
5. Si le montage insère une ouverture avant le début de la parole (cold open), **décaler toute la grille** d'autant et reconstituer à la main les sous-titres de cette ouverture.

## Règles de placement (rappel de `08-video/formats.md`)

- 9:16 (1080 × 1920) : centrés, au-dessus de la marge basse de 420 px (`MarginV` de 100 à 130 dans la méthode ffmpeg), jamais dans la colonne d'icônes à droite (160 px).
- 1:1 et 16:9 (LinkedIn) : centrés bas, dans la marge de titre de 5 % de chaque dimension.
- Dans un projet HyperFrames, les marges se lisent dans `frame.md` (`safe-top`, `safe-bottom`, `safe-left`, `safe-right`).
- Contraste : liseré (`Outline`) ou bandeau `--brand-dark` systématique ; le fond vidéo change, le sous-titre doit rester lisible sur chaque plan.

## Checklist avant livraison

- [ ] Transcription relue à 100 % (noms, chiffres, vocabulaire de marque, homophones)
- [ ] Segments : 1 ligne de 25 caractères au plus en 9:16 (2 × 42 au plus ailleurs), 1 à 3 s, 15 caractères par seconde au plus, pas de segment à cheval sur une coupe
- [ ] `.srt` livré dans `08-video/projets/<slug>/sous-titres/<nom>.srt` (UTF-8)
- [ ] Incrustation : police `{{BRAND_FONT_PRIMARY}}`, couleurs de la marque, hors zones de sécurité ; identité `hyperframes:embedded-captions` choisie par l'humain et consignée, le cas échéant
- [ ] Contrôle visuel sur au moins 3 images (début, milieu, fin), ou sur la planche de `qa-video.py`
- [ ] Pour YouTube : incrustation **et** `.srt` fournis

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/video-courte.md` pour le détail sourcé :

1. **Sous-titres incrustés sur 100 % des vidéos livrées** : environ 85 % des vidéos sociales sont regardées sans le son (jusqu'à 92 % sur mobile), et les sous-titres augmentent jusqu'à 80 % la probabilité de finir la vidéo.
2. **Test de validation avant livraison : la vidéo se comprend-elle entièrement en muet ?** Aucune information clé portée uniquement par la bande-son ; texte à l'écran pour les informations essentielles.
3. **Placement : gros, centrés, dans la zone sûre** (éviter le tiers bas recouvert par l'interface des plateformes), 1 ou 2 lignes au plus, mots-clés mis en évidence.

## Ce que cette skill ne fait pas

- Le montage : skill `video-editing`.
- Traduire les sous-titres sans validation d'un locuteur natif.
- Publier.
