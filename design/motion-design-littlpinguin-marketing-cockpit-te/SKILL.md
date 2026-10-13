---
name: motion-design
description: Passerelle entre la marque de {{COMPANY_NAME}} et HyperFrames pour tout ce qui est animé dans une vidéo, titres, chiffres, data visualisation, habillages, lower-thirds, logos animés, transitions de marque, 3D, personnages, animation à l'encre, insertion d'un rendu Manim. Génère la charte du projet (frame.md et brand.css par brand-frame.py), applique le profil de goût et la revue de singularité de 08-video/motion.md, choisit le workflow HyperFrames, filtre les blocs du registre par la marque et tient les règles de rendu. Références 3D, personnages et encre chargées à la demande. Appelée par video-production ; ne choisit pas la filière, ne tient pas les validations, n'écrit pas le script, ne monte pas de rushes.
---

# motion-design : la marque dans chaque image animée

Cette skill porte la marque jusqu'à HyperFrames pour tout ce qui bouge : titres, chiffres, data visualisation, habillages, lower-thirds, logos animés, transitions de marque, scènes 3D, personnages, animation à l'encre, plan Manim inséré. Elle est appelée par `video-production`, qui a choisi la filière, tient les validations et le budget. Ici, on décide comment la marque se voit et comment la composition se construit sans casser le rendu.

## Références à charger

- `01-brand/style-guide.md` : palette, polices, style d'illustration, tropes bannis.
- `01-brand/design-anti-generique.md` : marqueurs du look générique et méthode pour s'en écarter.
- `08-video/motion.md` : principes, profil de goût, revue de singularité, choix du moteur, repères typographiques, interdits.
- La skill `design-taste` : mêmes curseurs côté web, pour une campagne qui a aussi une landing.
- `08-video/inspiration.md` : chercher des vidéos de référence (`08-video/scripts/inspiration.py`), en extraire le mécanisme et le transposer dans la marque, sans reprendre ni look, ni prompt, ni code d'un créateur.
- Selon le besoin, une des références de cette skill (section « Références »).

Si `01-brand/style-guide.md` manque ou porte encore des `{{...}}`, s'arrêter et proposer `/start-cockpit`.

## Charte du projet

La charte d'un projet HyperFrames se génère, elle ne s'écrit pas :

```bash
python3 08-video/scripts/brand-frame.py 08-video/projets/<slug>/hyperframes --aspect <1080x1920|1080x1350|1080x1080|1920x1080>
python3 08-video/scripts/brand-frame.py 08-video/projets/<slug>/hyperframes --check
```

- Le premier appel écrit `frame.md` et `brand.css` à la racine du projet. Sans `--aspect`, la toile d'un `frame.md` existant est gardée (défaut `1080x1920`).
- `--check` n'écrit rien et sort 1 si l'un des deux fichiers ne correspond plus à `01-brand/tokens.json`. On relance alors sans `--check`.
- `--exemple` part de la palette neutre du template, pour essayer le module avant `/brand-discover` ; jamais pour un projet client.

**`frame.md`** est le fichier de design qu'HyperFrames lit en premier, et son frontmatter fait foi :

- `colors` : `primary`, `accent`, `dark`, `light`, `white`, et les dérivés hexadécimaux de `brand.css` (`primary-deep`, `text-on-dark`, `accent-on-dark`, `on-accent`) ;
- `typography` : les rôles `display`, `headline`, `title`, `body`, `stat` et `label`, avec famille, taille de départ en px, graisse et interlignage ;
- `spacing` : les zones de sécurité de la toile (`safe-top`, `safe-bottom`, `safe-left`, `safe-right`) et l'espacement de base (`gap`) ;
- `components` : `cta` (fond accent, texte `on-accent`), `badge`, `card`, `gradient` (le dégradé de la marque), `logo` (plan de fin uniquement, ou discret en zone sûre) ;
- un corps fixe : sources de la charte, toile et marges, règles de composition, à faire et à ne pas faire.

**`brand.css`** donne les mêmes valeurs en variables CSS. Le lier dans chaque composition (`<link rel="stylesheet" href="brand.css">`) et n'écrire aucune couleur, police ni rayon en dur :

| Variable | Usage |
|---|---|
| `--brand-primary`, `--brand-primary-deep`, `--brand-primary-soft` | Couleur principale, sa version profonde, sa teinte légère (transparente) |
| `--brand-accent`, `--brand-accent-soft` | Accent, réservé à l'élément qui doit attirer l'œil ; sa teinte légère |
| `--brand-dark`, `--brand-light`, `--brand-white` | Fonds sombre et clair, blanc |
| `--brand-text-on-dark`, `--brand-accent-on-dark` | Texte et accent posés sur un fond sombre |
| `--brand-on-accent` | Texte posé sur l'accent (bouton, pastille) |
| `--brand-gradient`, `--brand-gradient-vertical` | Le seul dégradé autorisé, horizontal ou vertical |
| `--font-display`, `--font-mono` | Police de la marque ; police mono des mentions (`label`) |
| `--radius-card`, `--radius-cta`, `--radius-badge` | Rayons des cartes, boutons et pastilles |

**Police.** HyperFrames rend sans réglage les polices qu'il embarque ; une autre police nommée déclenche l'avertissement de lint `font_family_without_font_face` et peut dépendre du réseau au rendu. Quand la police de marque n'est pas embarquée, déposer ses fichiers dans le projet (`assets/fonts/`, avec un nom de fichier qui commence par le nom de la famille, ce que cherche aussi le script de sous-titres des workflows) et les déclarer par `@font-face`, après avoir vérifié dans `01-brand/droits.md` que sa licence autorise l'embarquement et le rendu vidéo. Sous-titres aux couleurs de la marque dans un workflow HyperFrames : `video-production` § « Passer la main à HyperFrames ».

Ne jamais éditer `frame.md` ni `brand.css` à la main : changer les tokens, puis relancer `brand-frame.py`.

## Profil de goût et revue de singularité

Méthode dans `08-video/motion.md` :

1. Une phrase de lecture de la vidéo, puis les trois curseurs notés de 1 à 5 (densité, énergie du mouvement, audace), consignés dans `decisions.md` du projet avec leur justification. Si la campagne a une landing, partir des curseurs de `design-taste` et les ramener à l'échelle vidéo.
2. La revue de singularité, avant de présenter le storyboard puis avant le rendu : reconnaissable sans le logo ? produisible telle quelle pour un concurrent ? quel plan ne ressemble à aucun gabarit ? Réponses écrites dans `decisions.md`.

## Choisir le workflow HyperFrames

- **`hyperframes:motion-graphics`** : une pièce courte, sans voix, où le mouvement est le message (titre animé, chiffre, logo, lower-third, carte, graphique). Sa fiche de route la situe en général sous 10 s. Elle travaille en autonomie, sans storyboard : la validation du storyboard se fait avant, sur `storyboard.md` (`video-production`).
- **`hyperframes:general-video`** : composition libre en plusieurs scènes, narrée ou non, et tout ce qui dépasse une pièce courte (encre, 3D, personnages, montage d'archives, plan Manim inséré).
- **Blocs prêts à l'emploi** : avant d'écrire un effet à la main, chercher dans le registre avec la skill `hyperframes:hyperframes-registry` (`npx hyperframes catalog --query "<effet décrit en anglais>"`, le catalogue est indexé en anglais ; puis `npx hyperframes add <nom>`). Un bloc s'insère dans la composition, il ne la remplace pas. Le filtrer par la marque : ses couleurs et polices remplacées par les variables de `brand.css`, et refusé s'il relève des interdits de `08-video/motion.md` (glitch, flash, zoom de transition, particules décoratives).

Le passage de la main à HyperFrames (création du projet, `BRIEF.md`, rendu) est décrit dans `video-production` § « Passer la main à HyperFrames ».

## Règles de rendu (pièges connus)

HyperFrames rend une composition image par image : chaque image doit pouvoir se recalculer à partir de son seul instant. D'où ces règles, tirées de la documentation des skills `hyperframes:hyperframes-core` et `hyperframes:hyperframes-cli`. Dans une installation en plugin, chaque commande `npx hyperframes` passe par le lanceur du plugin (règle de la skill `hyperframes:hyperframes`).

- **Une timeline par composition.** Une seule `gsap.timeline({ paused: true })`, enregistrée sur `window.__timelines["<id>"]` avec l'`id` du `data-composition-id` de la racine, et seulement à la fin de sa construction : une timeline enregistrée vide donne une vidéo blanche. Pas de `tl.play()`.
- **Polices d'abord.** Construire la scène dans `document.fonts.ready.then(...)`, sinon les premières images partent avec la police de secours.
- **Durée sur la racine.** `data-duration` sur l'élément racine fixe la durée du rendu. Il est obligatoire dès qu'un moteur autre que GSAP anime la scène (Three.js, encre) : ces moteurs n'annoncent pas de durée.
- **Moteurs autres que GSAP.** Écouter l'événement `hf-seek` (`event.detail.time`) et dessiner exactement cet instant ; aucune boucle libre (`requestAnimationFrame`, `setAnimationLoop`).
- **Déterminisme.** Ni horloge (`Date.now()`, `performance.now()`), ni hasard non semé (`Math.random()`), ni `setTimeout` ou `setInterval` pour l'état visuel, ni répétition infinie (`repeat: -1`) : un nombre fini de répétitions. Un hasard voulu passe par une graine.
- **Visibilité des clips.** Ne jamais animer `visibility`, `display` ou `autoAlpha` sur un élément `class="clip"` : HyperFrames gère son apparition. Animer un enfant.
- **Transformations.** Pas de `transform` CSS de départ sur une propriété que GSAP anime : poser l'état de départ dans `gsap.fromTo`.
- **Médias.** Tous les médias copiés dans le dossier du projet (`assets/`), jamais chargés depuis une URL au rendu. Une `<video>` est muette (`muted`, `playsinline`) ; le son passe par un `<audio>` séparé, qui a un `id`.
- **Contrôles.** `npx hyperframes lint` après la première passe et après chaque changement de structure, puis `npx hyperframes check` avant tout rendu (`validate` en est l'ancien nom, gardé pour compatibilité). Une erreur de lint coupe les contrôles de mise en page et de contraste de `check` : la corriger d'abord.
- **Rendu.** Seulement après l'accord de l'humain sur l'aperçu, depuis le dossier du projet : `npx hyperframes render --quality delivery --output ../exports/<slug>-<plateforme>.mp4`, le livrable que contrôlent la QA et la revue. Si les sous-titres s'incrustent ensuite par ffmpeg, rendre vers `../rushes/tmp/<slug>-<plateforme>-sans-sous-titres.mp4` (skill `video-editing`, étape 5).
- **Moteur.** Jamais de changement de moteur en silence (`08-video/motion.md` § « Choisir le moteur »).

## Références

Charger seulement celle dont la vidéo a besoin :

- `references/3d.md` : un objet à montrer sous plusieurs angles, un espace à parcourir. Maquette puis production, plan de caméra, sources d'assets et licences, rendu par l'adaptateur Three.js.
- `references/personnages.md` : un récit porté par un personnage, une mascotte. Fiche, rig, poses, actions ; Lottie, marionnette SVG ou silhouette à l'encre.
- `references/encre.md` : le style dessiné à la main du moteur `08-video/lib/ink-theater/`. Installation, squelette de composition, couleurs de marque, clips de mouvement.
- **Manim** : pour une démonstration conceptuelle ou mathématique, `manim-composer` planifie la scène, puis `manim-ce` écrit le code. Le rendu MP4 entre comme un plan `<video>` de la composition HyperFrames, qui garde l'habillage de marque.

## Checklist avant livraison

- [ ] `frame.md` et `brand.css` générés par `brand-frame.py` ; `--check` sort 0
- [ ] Aucune couleur, police ni rayon en dur : uniquement les variables de `brand.css`
- [ ] Police de marque embarquée par `@font-face` si besoin, droits vérifiés dans `01-brand/droits.md`
- [ ] Profil de goût et revue de singularité consignés dans `decisions.md`
- [ ] Aucun preset `frame-presets` (hors la peau de sous-titres), aucun effet interdit par `08-video/motion.md`, blocs du registre repeints aux couleurs de la marque
- [ ] Si la pièce s'inspire de vidéos de référence : mécanisme transposé selon `08-video/inspiration.md`, créateurs cités, rien de leur look ni de leur prompt repris
- [ ] Logo seulement au plan de fin, ou discret en zone sûre
- [ ] `npx hyperframes lint` et `npx hyperframes check` propres
- [ ] Rendu fait après accord, puis QA et revue par `video-production`

## Ce que cette skill ne fait pas

- Choisir la filière, tenir les validations ou le budget : `video-production`.
- Écrire le script ou diriger la voix : `08-video/narration.md`, par `video-production`.
- Monter des rushes : `video-editing`.
- Générer la matière (images, clips, voix, musique) : `image-generation`, `video-generation`.
- Faire un deck : `slides`.
- Publier.

---

Méthode inspirée d'OpenMontage (calesthio/OpenMontage, AGPLv3), réécrite pour le template : aucun texte ni code repris. Registre : docs/vendored-video.md.
