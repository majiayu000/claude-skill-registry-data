---
name: video-documentary
description: Montage documentaire sur archives libres pour {{COMPANY_NAME}}, un essai filmé au service d'une thèse, à partir d'images d'Internet Archive, Wikimedia Commons, NASA, Pexels ou Pixabay. Brief thématique et thèse, découpage en emplacements validé, corpus constitué et filtré par licence (corpus.py build), index et recherche CLIP (corpus.py index et search), sélection validée sur les images clés (selections.json), narration, montage dans hyperframes:general-video avec un étalonnage commun, crédits générés (corpus.py credits) et QA. Appelée par video-production ; ne comble pas un trou par un clip généré, n'élargit jamais une licence sans décision humaine, ne publie pas.
---

# video-documentary : un essai filmé sur archives libres

Un montage documentaire défend une thèse avec des images réelles : des archives qui montrent que quelque chose a eu lieu, rapprochées pour faire naître un sens. Cette skill conduit le film du brief thématique aux crédits. Elle est appelée par `video-production`, qui a ouvert le projet (`08-video/projets/<slug>/`, slug daté `AAAA-MM-JJ-<sujet>`, `script.md` au modèle de `video-production` avec son frontmatter `date`, `subject`, `statut`), écrit le brief et tient les validations.

## Références à charger

- `08-video/documentaire.md`, en premier : ton, emplacements, règles de sélection, étalonnage, licences, outillage.
- `08-video/narration.md` si le film a une voix ; `08-video/montage.md` pour la coupe et le son ; `08-video/motion.md` pour les cartons de date et de source.
- `01-brand/droits.md` et `01-brand/divulgation-ia.md`.

## Prérequis

- **ffmpeg et ffprobe** : conversion des archives en mp4, mesure des durées, images clés.
- **Recherche CLIP**, facultative : `pip install -r 08-video/requirements-corpus.txt` (open_clip, torch, pillow ; les poids du modèle se téléchargent au premier lancement). `/modules` note cette capacité dans `.setup-completed` (`modules.video.capacites.corpus`). Sans elle, la sélection se fait à l'œil (`08-video/documentaire.md` § « Outillage »).
- **Clés gratuites**, facultatives : `PEXELS_API_KEY` et `PIXABAY_API_KEY` dans `.env`. Sans elles, les sources Internet Archive, Wikimedia Commons et NASA restent disponibles.
- **HyperFrames** pour le montage (plugin installé par `/modules`).

## Où se placent les validations

Les trois validations de `video-production` prennent ici cette forme :

- **Concept** (validation 1) : la question du film, la thèse, le registre (étape 1).
- **Script** (validation 2) : le découpage en emplacements, avant `corpus.py build` (étape 2) ; puis, si le film a une voix, la narration écrite sur les images retenues, avant toute génération de voix (étape 6).
- **Storyboard** (validation 3) : la sélection validée dans `selections.json`, avec `storyboard.md` (ordre des plans, durées, cartons), à la fin de l'étape 5, avant le montage (étape 7).

Constituer et indexer le corpus ne coûte aucun crédit. Une voix ou une musique payante reste sous le contrat de coût de `video-production`, et jamais avant la validation 3.

## Étape 1 : brief thématique et thèse

Dans `brief.md` : la question du film en une ligne, la thèse que le spectateur doit pouvoir formuler à la fin, le registre du film, la durée, la destination et sa toile, avec ou sans voix, la musique envisagée et sa licence. → **Validation 1.**

## Étape 2 : découper en emplacements

Écrire `08-video/corpus/themes/<nom>.toml` sur le modèle de `08-video/corpus/themes/exemple-savoir-faire.toml` : le champ `nom`, sources, nombre de résultats par requête, durée maximale d'un clip, et pour chaque emplacement un `id`, une `description` en langage visuel (sujet, action, cadre, époque, lumière ; en anglais pour la recherche CLIP) et deux ou trois `requetes` en anglais. Laisser les licences par défaut. Le dossier du corpus (`08-video/corpus/<nom>/`), et donc le `<nom>` de toutes les commandes qui suivent, vient du champ `nom` du thème, pas du nom du fichier (qui ne sert que si le champ manque) : en copiant le thème d'exemple, remplacer `nom = "savoir-faire"` par le nom du nouveau corpus, sinon ses clips rejoignent ceux de l'exemple. → **Validation humaine du découpage**, avant toute recherche.

## Étape 3 : constituer le corpus

```bash
python3 08-video/scripts/corpus.py build 08-video/corpus/themes/<nom>.toml
python3 08-video/scripts/corpus.py list <nom>
```

- `build` cherche chaque requête dans chaque source, écarte les licences hors du défaut et les clips trop longs, télécharge le reste dans `08-video/corpus/<nom>/clips/` avec une fiche par clip. Lire son rapport : clips téléchargés, déjà présents, écartés pour licence ou pour durée, sources ignorées, erreurs.
- Relancer `build` reprend sans retélécharger. Un emplacement trop pauvre se nourrit de nouvelles requêtes dans le thème, puis d'un nouveau `build`.
- `list` donne l'inventaire : nombre de clips, licences, durée totale, index présent ou non.

## Étape 4 : indexer

```bash
python3 08-video/scripts/corpus.py index <nom>
```

Extrait les images clés de chaque clip (une après chaque changement de plan, au moins une toutes les 3 s) dans `08-video/corpus/<nom>/images/` et construit l'index CLIP. Sans les dépendances facultatives, la commande sort en code 2 et affiche la commande d'installation.

## Étape 5 : chercher et sélectionner

```bash
python3 08-video/scripts/corpus.py search <nom> --emplacement <id>
python3 08-video/scripts/corpus.py search <nom> "<description libre, en anglais>" --top 5
```

- La forme `--emplacement` cherche avec la description de l'emplacement et écrit les meilleurs résultats (5 par défaut, réglable par `--top`) dans `08-video/corpus/<nom>/selections.json` : clip, instant de l'image la plus proche, score, image clé. La forme libre affiche seulement les résultats.
- Relancer `--emplacement` sur un même emplacement remplace sa sélection : le faire avant la validation, jamais après.
- **Planche des images retenues** : pour chaque emplacement, réunir les images clés citées par `selections.json` (champ `image`, dans `08-video/corpus/<nom>/images/`), les regarder, et appliquer les règles de sélection de `08-video/documentaire.md` : ni contresens ni anachronisme, date et contexte vérifiés sur la fiche du clip, pas de visage de particulier sans droit.
- Ne garder dans `selections.json` que les clips choisis, avec leur instant. Les écartés notables vont dans `decisions.md` avec leur raison.
- **Sans open_clip** : pas d'index ni d'images clés extraites par l'outil. Sélection à l'œil, sur une planche par clip faite avec ffmpeg, puis `selections.json` écrit à la main (format et commande dans `08-video/documentaire.md` § « Outillage »).

Écrire `storyboard.md` : l'ordre des plans, la durée de chacun, le passage du clip retenu, les cartons de date et de source. → **Validation humaine de `selections.json` et du storyboard (validation 3).**

## Étape 6 : narration

Si le film a une voix : script minuté selon `08-video/narration.md`, écrit sur les images retenues. La voix oriente, l'archive prouve : ne pas décrire ce que l'image montre déjà. Validation du texte, puis échantillon de voix validé, avant toute génération complète. Sans voix, la musique et les cartons portent le film : la thèse doit rester lisible.

## Étape 7 : monter dans `hyperframes:general-video`

- Passation selon `video-production` § « Passer la main à HyperFrames », avec `workflow: general-video`, `flow: automation` et `storyboard: no` dans `BRIEF.md` : la sélection et le storyboard sont déjà validés (validation 3), le workflow publie son plan pour information sans rouvrir de point de contrôle du storyboard. Le rendu reste soumis à l'accord.
- Copier les seuls clips retenus dans `hyperframes/assets/` : tous les médias restent dans le dossier du projet.
- Chaque archive devient un plan `<video>` muet, avec `data-start`, `data-duration` et `data-media-start` (le point d'entrée dans le clip) ; le son passe par des `<audio>` séparés.
- **Étalonnage commun** : le parti retenu dans `08-video/documentaire.md` (noir et blanc assumé, grain commun ou table de correspondance commune), appliqué à tous les plans, jamais clip par clip. Les traitements d'image d'HyperFrames sont décrits par la skill `hyperframes:media-use`.
- **Date et source à l'écran** quand l'archive porte un fait : rôle `label` de `frame.md`, discret, en zone sûre.
- **Montage par temps forts** : les plans qui portent la thèse restent plus longtemps à l'écran ; coupes franches de `08-video/montage.md` ; un silence sur le moment le plus fort.
- Rendu seulement après l'accord de l'humain sur l'aperçu.

## Étape 8 : crédits

```bash
python3 08-video/scripts/corpus.py credits <nom> --selection 08-video/corpus/<nom>/selections.json
```

Écrit `08-video/corpus/<nom>/credits.md`, une ligne par clip retenu (titre, auteur, source et page, licence, mention d'attribution obligatoire). Le reprendre au générique, ou dans la légende de publication si la vidéo n'en a pas, et le copier dans `08-video/projets/<slug>/` : le dossier du corpus n'est pas versionné. Ajouter les crédits de la musique et de la police si leur licence le demande.

## Étape 9 : QA

```bash
python3 08-video/scripts/qa-video.py 08-video/projets/<slug>/exports/<slug>-<plateforme>.mp4 \
  --plateforme <reels|tiktok|shorts|linkedin> --duree <secondes> --script 08-video/projets/<slug>/script.md
```

- Sans piste son : `--sans-audio`. Sans voix (musique seule) : sans `--script` ; une colonne Voix vide dans `script.md` désactive de toute façon la vérification de couverture. Destination site ou YouTube : sans `--plateforme`.
- Un film contemplatif tient des plans longs à dessein : relever `--max-plan` (ou `0` pour couper ce contrôle) et noter la raison dans `decisions.md`.
- Puis l'agent `video-reviewer`, deux tours de correction au plus, et la revue humaine du rendu final (`video-production` § « QA et revue »).

## Coûts

Les sources du corpus sont gratuites. Ce qui se dépense : le temps de téléchargement et d'indexation (le premier `index` télécharge en plus les poids du modèle), la place disque du corpus, et, s'il y en a, la voix et la musique payantes, sous le contrat de coût de `video-production`.

## Checklist avant livraison

- [ ] Question du film, thèse et registre validés (validation 1)
- [ ] Découpage en emplacements validé avant `corpus.py build` ; descriptions et requêtes en anglais
- [ ] `selections.json` réduit aux clips choisis et validé sur la planche des images clés, avec `storyboard.md` (validation 3)
- [ ] Aucun contresens ni anachronisme ; date et source à l'écran quand l'archive porte un fait ; aucun visage de particulier sans droit
- [ ] Un seul parti d'étalonnage pour tout le film ; aucun agrandissement par IA ni colorisation non déclarés
- [ ] Licences du défaut, ou élargissement consigné dans `decisions.md` ; musique sous licence établie
- [ ] `credits.md` produit par `corpus.py credits --selection`, repris au générique ou en légende, copié dans le projet
- [ ] `qa-video.py` et `video-reviewer` passés ; revue humaine du rendu final faite

## Ce que cette skill ne fait pas

- Combler un emplacement vide par un clip généré : chercher d'autres requêtes, changer l'emplacement, ou poser la question à l'humain.
- Élargir les licences admises sans décision humaine consignée dans `decisions.md`.
- Agrandir par IA ou coloriser une archive sans le déclarer.
- Publier.

---

Méthode inspirée d'OpenMontage (calesthio/OpenMontage, AGPLv3), réécrite pour le template : aucun texte ni code repris. Registre : docs/vendored-video.md.
