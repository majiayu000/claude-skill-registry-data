---
name: video-repurpose
description: Transforme une vidéo longue de {{COMPANY_NAME}} (webinar, podcast filmé, interview, live, conférence) en clips sociaux. Transcription horodatée au mot, repérage des candidats, notation sur cinq critères, test « se comprend sans contexte », validation humaine de la liste avant tout montage, coupe au mot, recadrage 9:16 et 1:1, sous-titres et habillage, QA par clip avec qa-video.py, une entrée de calendrier par clip. Appelée par video-production ; le montage passe par video-editing, les sous-titres par captions. Ne publie pas, n'écrit pas les posts d'accompagnement, ne fait jamais dire à quelqu'un ce qu'il n'a pas dit.
---

# video-repurpose : d'une vidéo longue à des clips sociaux

Une vidéo longue contient des moments qui tiennent seuls. Cette skill les trouve, les note, les fait valider, puis les fait monter un par un pour la plateforme visée. Elle est appelée par `video-production`, qui a ouvert le projet (`08-video/projets/<slug>/`, slug daté `AAAA-MM-JJ-<sujet>`), écrit le brief et tient le budget.

## Références à charger

- `08-video/formats.md` : durées, toiles, zones de sécurité, sous-titres, repères du format court.
- `08-video/montage.md` : coupe au mot, respirations, son.
- `08-video/narration.md` : seulement si un carton ou une voix d'introduction s'ajoute au propos d'origine.
- `02-strategy/calendar/calendar.md` et `_templates/inventory.md` : ce qui est prévu, ce qui a déjà été publié.
- `01-brand/voice.md`, `01-brand/droits.md`, `01-brand/divulgation-ia.md`.

## Où se placent les validations

Les trois validations de `video-production` prennent ici cette forme :

- **Concept** (validation 1) : le traitement de la série, une fois les droits et la source vérifiés (section suivante). Il fixe les plateformes et les toiles visées, l'habillage (lower-third, carton de contexte, plan de fin) et la voie des sous-titres, ffmpeg ou designés.
- **Script** (validation 2) : la liste des clips notée et passée au test « se comprend sans contexte » (étape 3). Elle devient `script.md`.
- **Storyboard** (validation 3) : `storyboard.md`, une vignette au vrai cadrage par clip et par toile, avec l'habillage prévu, après le recadrage (étape 5) et avant l'habillage et le montage (étapes 6 et 7). Aucun crédit avant (voix, musique ou cartons générés payants).

Le montage passe ensuite à `video-editing`, storyboard déjà validé : en voie A, `hyperframes:general-video` reçoit `flow: automation` et `storyboard: no` dans `BRIEF.md` (table « Validations et passage de main par filière » de `video-production`).

## Avant de couper : droits et source

- **Droits.** Accord des personnes filmées pour une réutilisation en clips, invités compris : vérifier que l'accord donné pour l'événement couvre des extraits diffusés sur les réseaux, et le noter dans `decisions.md`. Sans accord établi, s'arrêter et le dire.
- **Ce que la source permet.** Y a-t-il une image exploitable, ou seulement du son ? Combien de personnes parlent ? Le son est-il propre ? Sans image, les clips reposent sur un visuel de marque animé par `motion-design` et sur les sous-titres. Un son médiocre se nettoie avant la transcription.
- **Rangement.** La source dans `rushes/`, la notation dans `candidats.md`, les extraits de texte des clips dans `clips/`, les rendus dans `exports/`.

Présenter le traitement de la série (plateformes et toiles visées, habillage, voie des sous-titres, ce que les droits et la source permettent) et **attendre la validation explicite** (validation 1 de `video-production`). Rien ne passe à l'étape 1 avant l'accord : la plateforme retenue fixe la durée des clips à repérer.

## Étape 1 : transcription horodatée au mot

```bash
ffmpeg -i rushes/source.mp4 -vn -ac 1 -ar 16000 rushes/source.wav
whisper-cli -m <modèle> -f rushes/source.wav -l fr -oj -ml 1 -sow -of rushes/transcription
```

- `-ml 1 -sow` : un mot par segment dans `rushes/transcription.json`, au format de whisper-cli (liste `transcription`, début et fin de chaque mot en millisecondes dans `offsets.from` et `offsets.to`). `<modèle>` est le chemin déclaré dans `.env` (`WHISPER_MODEL`).
- Autre voie : `npx hyperframes transcribe rushes/source.wav --model small --language fr -d rushes`, la transcription au mot d'HyperFrames (par le lanceur du plugin quand HyperFrames est installé en plugin). Elle écrit `rushes/transcript.json`, un autre format : un tableau plat de mots `{ "text", "start", "end" }`, en secondes. Jamais sans `--model` ni `--language` : le modèle par défaut, `small.en`, traduit l'audio français en anglais.
- whisper n'identifie pas les intervenants : sur un entretien ou une table ronde, vérifier à l'écoute qui dit quoi avant d'attribuer une phrase.
- Les vrais silences, que la transcription aligne bord à bord : `ffmpeg -i rushes/source.wav -af silencedetect=noise=-30dB:d=0.3 -f null -`.

## Étape 2 : repérer les candidats

- **Unités de sens de 20 à 90 s** : une idée complète, avec son entrée et sa chute. Fourchette de travail, à resserrer selon la plateforme visée (`08-video/formats.md`).
- Repérer les passages où l'intervenant change de ton, donne un exemple précis ou répond franchement à une question : ce sont de bons candidats.
- Lire la transcription en entier avant de choisir.
- Noter chaque candidat dans `candidats.md` : numéro, début et fin, intervenant, première et dernière phrase, sujet.

## Étape 3 : noter

Cinq critères, chacun de 1 à 5 :

1. **Accroche** : les trois premières secondes du clip, seules, donnent-elles envie de rester ?
2. **Autonomie** : le clip se comprend-il sans le reste de la vidéo (test ci-dessous) ?
3. **Valeur pour la persona** : apprend-elle, gagne-t-elle quelque chose (`01-brand/personas.md`) ?
4. **Énergie** : voix, rythme, conviction.
5. **Adéquation à la plateforme** : durée, ton et sujet conformes à la plateforme visée.

Tableau de notation type, dans `candidats.md` (valeurs d'exemple) :

| # | Début | Fin | Durée | Cible | Accroche | Autonomie | Valeur | Énergie | Plateforme | Total | Décision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 00:12:04 | 00:12:51 | 47 s | LinkedIn | 4 | 5 | 4 | 3 | 4 | 20 | retenu |
| 2 | 00:31:10 | 00:32:20 | 70 s | LinkedIn | 2 | 1 | 4 | 4 | 3 | 14 | écarté : commence par « donc », renvoie à la démo |
| 3 | 00:44:30 | 00:45:02 | 32 s | Reels | 5 | 4 | 3 | 5 | 5 | 22 | retenu |

Le total classe, il ne décide pas seul : un clip noté 1 en autonomie est écarté quel que soit son total. Le nombre de clips livrés dépend de ce que la source contient de bon, pas d'un objectif fixé d'avance ; l'ordre de publication se décide à l'étape 9.

### Test « se comprend sans contexte »

Lire la transcription du clip seule, comme quelqu'un qui n'a pas vu la vidéo :

- renvoie-t-elle à un passage antérieur (« comme on l'a vu », « sur ce slide », « pour répondre à ta question ») ?
- commence-t-elle par un connecteur (« donc », « et », « du coup », « comme je disais ») ?
- « il », « ça », « ce truc » : sait-on de qui ou de quoi l'on parle ?
- la dernière phrase conclut-elle, ou le clip coupe-t-il avant la réponse ?

Une réponse oui : élargir le clip (reprendre la phrase d'avant), couper ailleurs, ajouter un carton de contexte d'une ligne, ou écarter. Un carton situe, il ne fait pas dire.

**Validation humaine de la liste avant tout montage.** Présenter les clips retenus (numéro, plateforme, durée, première phrase, note) et les écartés notables avec leur raison, puis attendre. Rien n'est coupé avant l'accord. La liste validée devient le `script.md` du projet : le frontmatter du modèle de `video-production` (`date`, `subject`, `statut`), un titre, puis une ligne par clip (numéro, début, fin, plateforme, première phrase). C'est ce frontmatter qui l'inscrit à l'inventaire à la livraison.

## Étape 4 : couper au mot

- Entrée et sortie de chaque clip sur les horodatages des mots, ajustées sur les vrais silences. Lire ceux de la transcription faite à l'étape 1 : `rushes/transcription.json` (whisper-cli, millisecondes dans `offsets`, à diviser par 1000) ou `rushes/transcript.json` (HyperFrames, secondes dans `start` et `end`). ffmpeg prend les instants en secondes, décimales comprises (`-ss 724.36`).
- Respirations resserrées sans être supprimées ; hésitations et redites retirées seulement quand le sens ne change pas (`08-video/montage.md`).
- Jamais de coupe qui change le sens : le clip dit ce que la personne a dit, dans l'ordre où elle l'a dit.
- Écrire le texte du clip coupé dans `clips/clip-<nn>.txt` : il sert à la QA.

## Étape 5 : recadrer

16:9 vers 9:16, recadrage centré :

```bash
ffmpeg -i clip-03.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p -c:a aac clip-03-9x16.mp4
```

- Sujet décentré : `crop=ih*9/16:ih:<x>:0`, avec `<x>` le bord gauche de la zone gardée, en pixels de la source.
- Intervenant qui se déplace, ou plusieurs intervenants : recadrage suivi, plan par plan. Découper le clip à chaque changement de plan ou de personne qui parle, choisir le cadre de chaque morceau ; l'assemblage se fait au montage.
- 1:1 : `crop=ih:ih,scale=1080:1080`.
- Netteté : depuis une source 1080p, un recadrage 9:16 garde une bande d'environ 608 px de large (1080 × 9/16), agrandie à 1080 px, donc plus douce. Préférer une source 4K quand elle existe.

Écrire `storyboard.md` : pour chaque clip retenu et chaque toile, une vignette au vrai cadrage (image tirée du clip recadré), le cadre choisi plan par plan, l'habillage prévu (lower-third, carton de contexte, plan de fin). → **Validation 3**, avant l'habillage et le montage.

## Étape 6 : sous-titres et habillage

- Sous-titres incrustés sur chaque clip, par la skill `captions` (vitesse de lecture et zones de sécurité : `08-video/formats.md`).
- Habillage par la skill `motion-design` : lower-third au nom et à la fonction de l'intervenant à sa première apparition (rôles `title` et `label` de `frame.md`), carton de contexte s'il a été validé, plan de fin avec un seul appel à l'action.
- Nom et fonction écrits comme la personne les a validés.

## Étape 7 : monter

Assemblage par la skill `video-editing` : coupes, recadrage, sous-titres, habillage, son au niveau de `08-video/montage.md`. Un fichier par clip et par plateforme : `exports/<slug>-clip-<nn>-<plateforme>.mp4`.

## Étape 8 : QA par clip

```bash
python3 08-video/scripts/qa-video.py 08-video/projets/<slug>/exports/<slug>-clip-03-linkedin.mp4 \
  --plateforme linkedin --duree 47 --script 08-video/projets/<slug>/clips/clip-03.txt
```

- `--script` avec le texte du clip : la couverture de la transcription signale une coupe qui a avalé une phrase.
- Puis l'agent `video-reviewer` sur chaque clip, et deux tours de correction au plus, comme dans `video-production`.

## Étape 9 : calendrier

- Une entrée par clip dans `02-strategy/calendar/calendar.md` : plateforme, date visée, statut, vidéo source.
- Espacer les publications selon la cadence du canal, et intercaler d'autres contenus : une série de clips ne se publie pas d'un bloc.
- Anti-répétition : vérifier dans le calendrier et `_templates/inventory.md` qu'un sujet n'a pas déjà été publié récemment, et ne pas publier deux clips sur la même idée la même semaine.

## Checklist avant livraison

- [ ] Accord des personnes filmées couvrant les extraits, noté dans `decisions.md`
- [ ] Liste des clips notée dans `candidats.md`, test « se comprend sans contexte » passé, liste validée par un humain avant tout montage
- [ ] Coupes au mot, sans changement de sens ; texte de chaque clip dans `clips/clip-<nn>.txt`
- [ ] Traitement de la série validé (validation 1) ; `storyboard.md` validé avant l'habillage et le montage (validation 3)
- [ ] Recadrage 9:16 ou 1:1 vérifié plan par plan : visage et zone utile dans le cadre
- [ ] Sous-titres incrustés (`captions`), lower-third au nom et à la fonction validés par la personne
- [ ] `qa-video.py` par clip avec `--script clips/clip-<nn>.txt`, revue `video-reviewer` traitée, revue humaine faite
- [ ] Une entrée de calendrier par clip, publications espacées, aucun doublon de sujet avec l'inventaire

## Ce que cette skill ne fait pas

- Publier : décision humaine.
- Écrire les posts qui accompagnent les clips : `social-content`.
- Faire dire à quelqu'un ce qu'il n'a pas dit : pas de voix de synthèse sur son propos, pas de coupe qui en change le sens.
- Monter ou sous-titrer elle-même : `video-editing` et `captions`.

---

Méthode inspirée d'OpenMontage (calesthio/OpenMontage, AGPLv3), réécrite pour le template : aucun texte ni code repris. Registre : docs/vendored-video.md.
