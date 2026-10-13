---
name: video-generation
description: Génération de rushes vidéo IA pour {{COMPANY_NAME}}, texte vers vidéo ou image vers vidéo, via un MCP multi-modèles (Seedance, Kling, Hailuo, Veo...). Spécification d'un plan en cinq aspects (sujet, mouvement, scène, espace, caméra), prompts en anglais, notes datées par famille de modèles, arbre stock ou génération, grille de choix du fournisseur, discipline de dépense sous le contrat de coût de video-production, et contrôle de fidélité du texte sur tout rush qui fait parler quelqu'un (corrélation d'enveloppe audio). À utiliser pour un plan cinématique, un b-roll animé, une animation de produit, ou régénérer un plan d'un montage. Le montage relève de video-editing, l'orchestration de video-production (et de reel-talking-head pour un reel client).
---

# video-generation : rushes vidéo IA pour {{COMPANY_NAME}}

Vous produisez des **rushes** (jamais le livrable final) via un MCP de génération vidéo multi-modèles (type Magnific/Freepik). La composition et l'assemblage relèvent de `video-editing` ; le projet, les validations et le budget, de `video-production`.

## Avant de générer

1. **Brief et storyboard validés** (`08-video/projets/<slug>/brief.md` et `storyboard.md`, validation 3 de `video-production`) : sujet, mouvement voulu, durée, ratio, audio ou non, référence de départ. Aucun crédit dépensé avant.
2. Style-guide chargé (`01-brand/style-guide.md`) si le rush porte l'identité de la marque.
3. **Stock ou génération ?** Section « Stock ou génération » : réutiliser et chercher avant de générer.
4. **t2v ou i2v ?** Texte vers vidéo pour explorer un concept ; image vers vidéo pour le contrôle et la cohérence (générer d'abord l'image de départ avec `image-generation`, ou partir d'un visuel validé).
5. **Choisir le modèle par le besoin, pas par le prix affiché** : les modèles économiques pour itérer, les modèles les plus complets pour le rendu final validé uniquement (section « Choisir un fournisseur »). Lister le catalogue en session (`video_models_list`) : il évolue en continu, ne jamais figer une liste.

## Spécifier un plan en 5 aspects

Un prompt part d'une ligne validée de `storyboard.md`, pas d'une idée. Cette ligne se déplie en cinq aspects (sujet, mouvement, scène, espace, caméra), chacun répondant à une question de tournage. Un aspect laissé vide est un choix abandonné au modèle.

- **Sujet : que regarde-t-on ?** Le décrire comme on le reconnaît sur la vignette du storyboard : matière, couleur, tenue, objet en main. Un sujet qui revient dans plusieurs plans (le produit, une personne, une mascotte) a sa fiche dans `decisions.md` (sujet « Fiche du sujet »), reprise à l'identique dans chaque prompt de la série. Mieux encore, quand le modèle l'accepte : une image de référence du sujet (image de départ, ou références `character` et `product` du catalogue) plutôt qu'une description seule.
- **Mouvement : que se passe-t-il ?** Le verbe du plan, avec sa vitesse et son effet visible : la pâte monte, la porte s'ouvre, la vapeur se dissipe. Un clip de quelques secondes porte une action, qui commence et s'achève dans sa durée.
- **Scène : où et quand ?** Lieu, époque, saison, heure, météo, et ce qui vit derrière le sujet (passants, feuillage, fumée). Rien de ce qui appartient à la marque : texte, logo, sous-titres et habillage s'ajoutent au montage, aux couleurs de `brand.css`, et le prompt le dit (`no text, no logo`).
- **Espace : d'où le voit-on ?** La valeur de plan de la vignette (gros plan, plan moyen, plan large) et la place du sujet dans la toile de destination : en 9:16, dans la zone utile de `08-video/formats.md`, loin des marges que l'interface des plateformes recouvre. Puis ce qui détache le sujet du fond : arrière-plan flou, objet net au premier plan.
- **Caméra : comment filme-t-on ?** Immobile, ou un seul mouvement nommé (liste ci-dessous) ; l'optique (courte, l'espace s'ouvre ; longue, il se resserre) ; la netteté, et l'endroit où elle se pose.

Le mouvement de caméra se choisit par l'intention, puis s'écrit en anglais dans le prompt :

- s'approcher d'un détail : push-in (`slow push-in`), ou dolly avant (`dolly in`), plus coulé ; s'en éloigner : pull-out (`pull-out`, `dolly out`) ;
- accompagner un geste ou une personne qui marche : travelling latéral (`tracking shot`, `truck left`, `truck right`) ;
- montrer un objet sous plusieurs faces : orbit (`orbit around the subject`) ;
- révéler un lieu en prenant de la hauteur : grue (`crane up`) ;
- donner une présence vivante, documentaire : caméra à l'épaule (`handheld`) ;
- laisser toute la place au geste : plan fixe (`static shot`, `locked-off camera`) ;
- conduire le regard d'un élément à un autre sans bouger la caméra : bascule de point (`rack focus from ... to ...`).

La lumière, par l'effet recherché : chaleur de fin de journée, heure dorée (`golden hour`) ; produit net et rassurant, high key (`high-key lighting`) ; tension ou mystère, low key (`low-key lighting`) ; silhouette détachée du fond, contre-jour (`backlit`, `rim light`) ; intérieur habité, lampes visibles dans l'image (`practical lights`). La palette de la scène reste compatible avec `01-brand/style-guide.md`.

Certains modèles prennent le mouvement de caméra en paramètre (Seedance : `cameraMotion`, avec des valeurs comme `pushIn`, `orbitLeft`, `craneUp`, `handheld`, `static`) : le paramètre se règle en plus du texte, et les deux disent la même chose.

Exemple de prompt complet (image vers vidéo, plan de 6 s), écrit d'une traite :

```text
Late-afternoon pottery workshop, dust floating in warm light from a side window, shelves of unglazed bowls blurred in the background.
Medium close-up at eye level on a potter's hands, navy linen apron, silver ring on the left hand, shaping wet clay on a spinning wheel that sits in the lower third of the frame.
Her thumbs press in and the wall of the bowl rises slowly, then her hands lift away while the bowl keeps turning.
Slow dolly in with a 50 mm lens and shallow depth of field; in the last second the focus shifts from her hands to the rim of the bowl.
Golden hour light, soft backlight on the clay dust. No text, no logo, no watermark.
```

Chaque phrase répond à l'une des cinq questions. La fiche du sujet (`navy linen apron, silver ring on the left hand`) se reprend telle quelle dans les plans suivants de la série.

## Écrire le prompt : le mouvement d'abord, en anglais

Les modèles vidéo sont mieux calibrés en anglais ; le français concerne le contenu à l'écran, pas le prompt technique.

- Décrire **ce qui bouge**, pas ce qui est statique : sujet, action, caméra nommée (`slow push-in`, `handheld`, `orbit`), ambiance.
- Audio natif si le modèle le prend en charge : `"dialogue"`, `SFX:`, `Ambient noise:`.
- Pour du multi-plan, structurer le prompt en sections (déroulé des plans, inventaire des effets, courbe d'énergie).
- Plans destinés à s'insérer dans un montage existant : écrire les **interdits de raccord** (décor, tenue, lumière identiques), sinon le modèle casse la continuité.

## Notes par famille de modèles

Relevé du catalogue Magnific (`video_models_list`, modèles recommandés et recherche « veo ») le 2026-10-12. Ces notes vieillissent vite : lister le catalogue en session avant tout choix, et faire rafraîchir cette section par l'agent `video-model-scout`. Les recommandations citées sont celles que l'agrégateur publie dans son catalogue, pas un test du template.

- **Seedance (ByteDance)**. La 2.5 est en tête des recommandations du catalogue : clips de 4 à 30 s jusqu'en 1080p, son natif, synchronisation labiale, références image, vidéo et audio, mouvement de caméra en paramètre. La 2.0 monte jusqu'en 4K (4 à 15 s). La 2.0 Fast sert aux brouillons (480p ou 720p).
- **Kling 2.5**. Clips muets de 5 ou 10 s, en 720p ou 1080p ; images de début et de fin fixables (en 720p, l'image de départ est exigée et l'image de fin n'est pas admise). Présenté par l'agrégateur comme le meilleur rapport qualité-prix pour un plan muet.
- **MiniMax Hailuo H3 Max et H3 Max Turbo**. Clips de 5 à 15 s en 480p ou 768p, pour explorer vite le mouvement et la mise en scène. Max accepte des références image, vidéo et audio ; Turbo, non.
- **Google Veo 3.1** (et ses versions Fast et Lite). Clips de 4, 6 ou 8 s, formats 16:9 et 9:16 seulement (pas de 1:1), jusqu'en 4K (1080p pour Lite) ; les effets sonores sont une option qui change le coût.

Tendances de ce relevé, sans promesse : le son natif et la synchronisation labiale se répandent ; un clip dépasse rarement 15 s (Seedance 2.5 va jusqu'à 30 s) ; les versions rapides servent aux brouillons, les versions complètes au définitif ; les formats proposés varient d'un modèle à l'autre, d'où le contrôle du ratio avant de choisir. Plusieurs modèles sont marqués bêta dans le catalogue : en tenir compte pour la fiabilité.

## Stock ou génération

Ordre de `video-production` : réutiliser (`01-brand/assets/`, rushes existants), puis le stock, puis générer. Pour chaque plan :

1. **Un fait réel, une preuve, un document** : stock ou archives, jamais un plan généré, qui ne prouve rien. Pour un montage d'archives : skill `video-documentary` (corpus documentaire et ses licences).
2. **Un plan d'ambiance que personne ne doit reconnaître** (une rue, un atelier, des mains au travail) : chercher au stock ; générer seulement si aucun résultat ne tient face à la vignette du storyboard.
3. **Ce qui ne peut pas se filmer** (une idée mise en image, un objet qui n'existe pas encore) : génération.
4. **Le produit réel** : image vers vidéo depuis des visuels validés (`01-brand/assets/`, photos du produit), avec la première et la dernière image fixées pour garder l'identité du produit. Jamais un produit redessiné par le modèle.
5. **Une personne réelle** : tournage, ou génération seulement avec son consentement explicite (section « Garde-fous et divulgation »).

Le stock se cherche par l'outil `stock_search` du MCP Magnific (`content_type: video`, `video_type: footage`, orientation selon la toile), se compare à la vignette du storyboard sur son aperçu, puis se télécharge par `stock_download`. Licence et crédit de chaque plan vérifiés dans `01-brand/droits.md` et notés dans `decisions.md` ; une licence payante passe par le contrat de coût.

## Choisir un fournisseur

Le modèle se choisit plan par plan, sur une grille qualitative, pas sur un classement :

- **Adéquation à la tâche** : durée, format, son, références d'identité ou de produit dont le plan a besoin.
- **Qualité** : jugée sur un échantillon, pas sur la réputation du modèle ni sur la recommandation du catalogue.
- **Contrôle** : images de début et de fin, références, caméra en paramètre.
- **Fiabilité** : modèle en bêta ou non, échecs déjà notés dans `decisions.md`.
- **Coût** : tarif réel de l'échantillon, solde du budget (`couts.md`) et du compte (`account_balance`).
- **Délai** : temps de génération annoncé par le catalogue, au regard de l'échéance du brief.
- **Continuité avec les plans voisins** : les rendus diffèrent d'un modèle à l'autre ; une même séquence garde un même modèle quand c'est possible.

Le choix et sa justification s'écrivent dans `decisions.md` (sujet « Modèle vidéo »), avec les options écartées. **Jamais de changement de fournisseur ou de modèle sans l'annoncer** : un modèle indisponible est un blocage à signaler, pas l'occasion d'en prendre un autre.

## Discipline de dépense : non négociable

Tout appel payant suit le **contrat de coût de `video-production`** (annonce de l'outil, du modèle, de la raison, échantillon ou série, coût estimé, solde ; `couts.md` à jour ; premier usage validé par l'humain). En plus :

- **Itérer là où c'est inclus** (application web du fournisseur si l'abonnement y donne de l'illimité en basse résolution), **produire par le MCP** une fois la direction validée. On valide la *direction* en basse résolution (cadrage, raccord, mouvement), pas le piqué.
- **Un exemplaire avant la série.** La simulation de coût peut échouer sur la génération vidéo : lancer **un** clip pour connaître le tarif réel, puis décider.
- **Générer en 720p et agrandir en local** quand la source d'origine est en basse définition : le 1080p natif n'invente que du détail, pour un multiple du prix.
- Vérifier le solde en direct (`account_balance`) avant toute série.

## Fidélité du texte : le contrôle le plus important de la chaîne

**Un modèle qui refait parler quelqu'un (synchronisation labiale, génération sur une voix) peut lui faire dire autre chose, avec une synchro labiale parfaite.** Pas un artefact visuel : des phrases entières remplacées. Invisible si l'on ne compare pas au texte d'origine, et catastrophique sur un contenu client.

**Le test, avant de poser tout rush dans un montage (local, quelques secondes, gratuit) :** corréler l'enveloppe d'énergie audio du rush avec la voix d'origine (RMS par fenêtres de 10 ms, corrélation avec recherche de décalage) :

- **au-dessus de 0,9** : fidèle, montable (valeurs observées : 0,97 à 0,99) ;
- **sous 0,5** : texte altéré, **ne pas monter** ; confirmer par transcription (valeurs observées : 0,24 à 0,25).

Les valeurs ne sont jamais ambiguës. Un rush globalement infidèle peut garder des segments fidèles : la corrélation glissante les localise. La même mesure sert à vérifier un mot que la transcription du master déforme sous un effet sonore.

**Faire ce contrôle avant le montage, jamais après** : le découvrir après coûte la reconstruction du montage entier.

## Synchronisation labiale

Sur un plan régénéré, la synchronisation native du modèle ne suffit pas : passage séparé, avec l'audio **exactement de la durée du clip** (sinon les mots sont coupés). Comparer les moteurs de synchronisation **à l'image** (bouche recadrée sur 3 instants) : le prix ne prédit pas la qualité.

## Garde-fous et divulgation

- Visage réel : uniquement avec le **consentement explicite** de la personne, obligatoire dès qu'un plan est régénéré ou synchronisé.
- Jamais de logo tiers fabriqué par IA.
- Mention « Vidéo générée par IA » en légende de la publication, jamais sur le média, selon `01-brand/divulgation-ia.md`.
- Chaque rush produit : sidecar `.json` (modèle, prompt, paramètres, `validated`, `ai_disclosure`) à côté du rush dans `08-video/projets/<slug>/rushes/`, et sa ligne de dépense dans `couts.md`.

## Ce que cette skill ne fait pas

- Monter : skill `video-editing` ; orchestrer un projet : `video-production` ; un reel client : `reel-talking-head`.
- Détourer : skill `video-matting`.
- Les visuels fixes : skill `image-generation`.
- Combler un emplacement d'un montage documentaire par un plan généré : `video-documentary` l'interdit.

---

Méthode inspirée d'OpenMontage (calesthio/OpenMontage, AGPLv3), réécrite pour le template : aucun texte ni code repris. Registre : docs/vendored-video.md.
