---
name: slides
description: Présentations HTML standalone projetables pour {{COMPANY_NAME}} (pitchs, comités, kickoffs, readouts, webinars). Qualité éditoriale (barre Monocle / Bloomberg viz / MIT Tech Review print), 01-brand/ comme source unique de vérité, cadre 1920×1080 scalé responsive, navigation triple (drag bar + overview + quick-jump) + plein écran, QA Playwright obligatoire avant livraison, export PDF propre (rastérisation canvas des textes en gradient si la marque en utilise). À utiliser pour toute demande de présentation, deck, slides projetées ou partagées. Pas pour un carrousel LinkedIn PDF 1080×1350 (→ `carousel`) ni pour une image unique (→ `image-generation`).
---

# slides — decks HTML éditoriaux pour {{COMPANY_NAME}}

Tu génères des présentations `.html` autonomes, projetées en réunion, exportées en PDF ou hébergées sur une URL statique. La barre de qualité : *Monocle × Bloomberg viz × MIT Tech Review print* — retenue, hairlines, blanc généreux, une idée par slide. Bannir les tropes « startup IA 2025 » (bento grids, orbes glassy, gradients radiaux empilés, copy pseudo-percutante).

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant le moindre plan de slides :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie slides (pas de point final sur les titres, plancher de tailles), assets, réutilisation.
2. Charger `01-brand/voice.md` + `01-brand/style-guide.md` — voix, vocabulaire, tokens visuels.
3. Consulter `01-brand/assets/index.md` avant d'envisager le moindre visuel : un asset existant se réutilise, il ne se régénère pas.
4. Charger `01-brand/design-anti-generique.md` — doctrine design anti-générique : marqueurs du look IA interdits par défaut, contrastes typographiques, checklist de pré-livraison (la marque prime là où elle a un avis).

**Ne jamais produire sans.** Si un de ces fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`.

## Où vit le travail

Tous les fichiers slides vivent sous `06-graphic-design/presentations/` :

```
06-graphic-design/presentations/
├── decks/                  ← decks générés (un .html par deck)
├── briefs/                 ← briefs par deck (intention, audience, décision, sources)
├── templates/
│   ├── base.html           ← squelette (chrome, nav, mode print, hooks QA)
│   ├── components.md       ← catalogue de composants + guide de sélection
│   └── components/         ← layouts de slides prêts à coller
├── scripts/
│   ├── qa.py               ← check Playwright overflow (obligatoire)
│   ├── serve.sh            ← serveur statique local :5173
│   ├── export-pdf.sh       ← export PDF 1920×1080 propre
│   └── export_pdf.py       ← worker Chromium headless
├── docs/
│   ├── design-system.md    ← principes, anti-patterns, échelle typo
│   ├── engine-parity.md    ← liste CANONIQUE des features du moteur + règle de parité
│   ├── pdf-export.md       ← rastérisation du texte en gradient expliquée
│   └── hosting.md          ← Netlify Drop, S3, GitHub Pages, etc.
└── tokens.css              ← variables CSS slides, dérivées de 01-brand/
```

**Base technique** : le starter `templates/base.html` embarque le **moteur complet** (parité avec `_examples/deck-catalogue/catalogue.html`, voir `docs/engine-parity.md`) : plein écran, overview groupée, export PDF, folios auto, hooks de pattern. Partir du starter (ou du deck approuvé le plus récent dans `decks/` pour ses compositions) — mais le moteur, lui, ne se réécrit jamais : il se reprend tel quel et `qa.py` vérifie sa présence.

## Quand invoquer cette skill

- « Fais-moi un deck pour [audience] sur [sujet] »
- « Construis une présentation pour pitcher [projet] à [interlocuteurs] »
- « Transforme ce brief / cette transcription / ce doc stratégie en slides »
- « Refais [deck précédent] dans le même style »
- Tout livrable projeté ou partagé en deck

Carrousel LinkedIn PDF → `carousel`. Infographie statique, post social, bannière → `image-generation`.

## Prérequis — confirmer avant de démarrer

1. **Setup marque complet.** `.setup-completed` existe à la racine ; `01-brand/style-guide.md`, `01-brand/voice.md` et `tokens.css` ne contiennent plus de `{{...}}`.
2. **Matière source claire.** Soit l'utilisateur fournit brief / transcription / mémo, soit tu passes par `superpowers:brainstorming`. Jamais de HTML sur un brief verbal flou.
3. **Le plan de slides est approuvé.** Rédiger une liste numérotée (eyebrow + headline par slide, 10-24 au total) et obtenir un accord explicite avant de générer le HTML. C'est LE moment de correction le moins cher.

## Procédure (8 phases)

### Phase 1 — Préparation

1. Lire toute la matière source : brief dans `briefs/`, transcriptions dans `_sources/transcriptions/`, rapports cités dans `_sources/reports/`.
2. Identifier audience, décision à obtenir, format (projeté live vs lecture autonome).
3. Choisir un arc émotionnel façon Duarte : alternance douleur ↔ espoir (ou contexte → douleur → promesse → stratégie → exécution → KPIs → engagement). Mapper chaque temps sur une intention de slide.
4. Couper à 10-24 slides, « une idée = une slide ». Insérer 3-4 slides « respiration » (un gros chiffre + une phrase courte) entre les slides denses.

### Phase 2 — Direction artistique

5. Choisir une métaphore visuelle fil rouge alignée marque et sujet : un motif récurrent (marqueur visuel, watermark ambient, animation discrète) qui ancre le récit. Chaque deck invente ses propres compositions — ne pas recopier la grille du deck précédent.
6. Confirmer le système typographique depuis `tokens.css` : paire de contraste (ex. graisse 200 vs 700/900), tailles display vs body, captions mono. **Si `01-brand/style-guide.md` est maigre**, invoquer `ui-ux-pro-max` pour poser style + couleurs + fonts cohérents avant d'aller plus loin.
7. Verrouiller la grille : cadre 1920×1080, chrome inset 36×60, padding slide 80×120. Grille de fond optionnelle (dust-grid ~96px avec mask radial) si la marque s'y prête.
8. Principes d'animation : easing lent (0.8-1.1s `cubic-bezier(0.16, 1, 0.3, 1)`), stagger 0.08-0.12s, pas de springs bondissants, pas de cuts rapides. **Mascottes et motifs de marque FIXES** : pas d'animation de flottement — seules les transitions reveal d'entrée sont autorisées.

### Phase 3 — Composants

9. Décider quels patterns de `templates/components.md` tu réutilises. Construire tout nouveau composant en isolation, le tester à 1920×1080, puis l'intégrer. **Quand un temps de slide n'entre dans aucun composant documenté**, invoquer `frontend-design` pour en concevoir un. Pour des références plus riches, les outils 21st.dev (`mcp__magic__21st_magic_component_builder` / `inspiration` / `refiner`) — traiter leur sortie comme inspiration : retravailler la géométrie au cadre 1920×1080, respecter la safe-zone du chrome, ré-appliquer les tokens. Jamais de composant généré collé tel quel.
10. Tester le tout premier composant via Playwright avant d'en ajouter d'autres — attrape tôt les bugs d'échelle et de typo.
11. **Icônes = Lucide en SVG inline** (`stroke-width: 1.75`, `stroke: var(--brand-primary)`, `fill: none`) dans une pastille de fill léger. Plus net que des icônes générées.
12. **Eyebrows : souvent en trop.** Le tag-meta du chrome (haut-gauche) suffit pour le contexte ; ne poser un eyebrow au-dessus d'un titre que s'il apporte une information.

### Phase 4 — Assets

13. **Logo de marque** : inline en `<symbol id="brand-logo">` depuis `01-brand/assets/`. Toujours `fill="currentColor"` sur les paths internes — le shadow DOM du `<use>` ne reçoit PAS `fill: url(#gradient)` ; piloter la couleur via `color:` sur le wrapper.
14. **Illustrations / photos de marque** : d'abord `01-brand/assets/index.md` (catalogue), puis `06-graphic-design/outputs/` (visuels déjà produits par `image-generation`). SVG inlinés ; rasters en chemins relatifs.
15. **Captures produit réelles** : si la marque a un produit, préférer de vraies captures soignées à toute illustration générique. Les référencer dans le brief.
16. **Co-branding** : logo partenaire monochrome foncé sur fond sombre → `filter: brightness(0) invert(1)` pour le passer en blanc.
17. **Logos d'outils tiers** (au besoin), ordre de tentative : (a) `cdn.simpleicons.org/<slug>/<hex-sans-#>`, (b) `api.iconify.design/logos/<slug>.svg` ou `api.iconify.design/simple-icons/<slug>.svg?color=<hex>`, (c) WebFetch du site officiel + extraction du SVG inline, (d) fallback PNG `google.com/s2/favicons?domain=<domaine>&sz=256`. Sauvegarder sous `01-brand/assets/<slug>.<ext>` et référencer en relatif. Re-vérifier les URLs à chaque projet — elles dérivent.

### Phase 5 — Contenu

18. Écrire la copy sous la doctrine de l'étape 0. Liste de vocabulaire interdit non négociable ; filtre anti-style-IA intégral (parallélismes négatifs, vocabulaire IA mort, règle de trois automatique).
19. **Jamais de point final sur un titre.** Jamais de tiret cadratin (`—`) dans le contenu visible : `–`, virgule ou reformulation.
20. Chaque affirmation est adossée à un chiffre, une date ou une source nommée. Croiser avec `01-brand/messaging-framework.md` — ne jamais publier un chiffre qui n'y est pas ou qui n'est pas dans `_sources/reports/`.
21. Vérifier slogans et formules signature : uniquement les versions validées de `01-brand/voice.md`.
22. Baseline footer : `{{COMPANY_NAME}} · {{COMPANY_WEBSITE}}` en signature bottom du chrome sur chaque slide hors hero (déjà câblé dans `base.html`).

### Phase 6 — Navigation

23. La navigation triple est câblée dans `templates/base.html` : drag-bar horizontale, overview panel (`O` / `Esc`, **groupée par familles** via `data-family` : ouverture, editorial, dataviz, schema, tableau, preuve, conclusion), quick-jump clavier (chiffres + Enter). Plus les classiques ←/→/Espace/Page↑↓/Home/End, molette debouncée 700ms, swipe tactile. **Mode plein écran** : bouton `⛶` + raccourci `F` (Fullscreen API avec fallback `webkit`) → `body.presenting` masque la nav, `fit()` tourne sans réserve ni cap, et la nav réapparaît quand le pointeur passe à moins de 90 px du bas (`nav-peek`). **Folios auto-numérotés** : le moteur injecte `NN / TOTAL` dans chaque `.nav-num` depuis `SLIDE_COUNT` — laisser les spans vides, ne jamais coder un folio en dur. **Ne pas retirer ni réimplémenter** — la liste canonique des features est `docs/engine-parity.md`.
24. Centrage du cadre : `transform: translate(-50%, calc(-50% + ${yShift}px)) scale(${scale})` avec `yShift = -(24 + nav.offsetHeight)/2`. `place-items: center` ne fonctionne PAS avec `transform: scale()` — la boîte de layout reste 1920×1080.

### Phase 7 — QA Playwright (NON NÉGOCIABLE)

25. Exécuter `python scripts/qa.py decks/<deck>.html` depuis `06-graphic-design/presentations/`. Doit retourner `All slides clean`. Le script vérifie :
    - **Parité moteur** (`docs/engine-parity.md`) : présence mécanique des marqueurs du moteur (`body.presenting`, `nav-peek`, `SLIDE_COUNT`, export PDF, `--brand-pattern`…). Échec = une feature du moteur manque ; la porter depuis `templates/base.html` ou le catalogue, jamais la réécrire.
    - Aucun élément ne déborde du cadre 1920×1080.
    - Écart contenu bas / chrome bas ≥ 16px sur chaque slide.
26. Re-tester à 1366×768 et 1024×600 pour confirmer le scaling responsive. Inspecter visuellement chaque screenshot.
27. **Insertion / suppression de slide** : aucune renumérotation manuelle — les folios `NN / TOTAL`, le compteur de la nav et l'overview se recalculent depuis `SLIDE_COUNT` (JS). Vérifier seulement que la nouvelle slide porte `data-family`, `data-eyebrow`, `data-heading` et un `.nav-num` vide. `qa.py` détecte le nombre de slides automatiquement.

### Phase 8 — Brand-check + livraison

28. **Brand-check obligatoire** avant livraison (5 points : vocabulaire / ton / preuve / audience / visuel). Les decks passent la même porte que le social, l'email et le web. Le hook PostToolUse rappelle ; ne pas le contourner.
29. Garder `v1` intact pendant l'itération. Révision → `v2` à côté. Une fois approuvé, supprimer `v1` si souhaité.
30. Confirmer que l'utilisateur a prévisualisé le deck (`./scripts/serve.sh` puis `http://localhost:5173/decks/<deck>.html`) avant d'annoncer terminé.

## Lisibilité typographique (règle de présentation)

Plancher : **aucun texte de contenu sous ~18-20px** sur le cadre 1920×1080 (équivalent 18pt minimum en projection ; corps idéal 20-24pt). Seuls les labels mono du chrome (folio, signature, tag-meta) restent à 12-14px. Captions et notes ≥ 15px.

**Éviter l'espace vide** sur les slides « titre + contenu » : centrer le **bloc entier** (titre + contenu ensemble), pas titre collé en haut + contenu centré (qui crée un trou au milieu). Pattern : `.plate.vcenter { justify-content: center } .plate.vcenter .body-wrap { flex: 0 0 auto }`.

## Pièges typographiques (patterns déjà résolus)

| Symptôme | Cause | Fix |
|---|---|---|
| Descendantes `g` `j` `p` `q` (et `%` `O` `9`) coupées sur display | `background-clip: text` ne peint que dans la boîte de l'inline-block, dont la hauteur = line-height ; en display serré les descendantes sortent de la boîte | `line-height ≥ 1.1` sur les titres texte, `letter-spacing: -0.025em` max, et sur le span en gradient : `padding: 0.22em 0.08em; margin: -0.22em -0.08em; overflow: visible` |
| Texte en gradient rendu différemment après `transform: scale()` | `-webkit-background-clip: text` + rendu sub-pixel | `display: inline-block; transform: translateZ(0); -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision` |
| Halos colorés autour du texte en gradient en PDF/print | `background-clip: text` + `display: inline-block` clippent mal en print | En `@media print`, remplacer le gradient par un aplat `var(--brand-primary-deep)` — ou rastériser (voir export PDF) |
| Chiffre + unité qui passent sur 2 lignes | `display: block` ou colonne de grille trop étroite | `display: inline-flex; align-items: baseline; white-space: nowrap`, élargir la colonne |
| Logo invisible après embed | `fill: url(#grad)` ne traverse pas le shadow DOM du `<use>` | `fill="currentColor"` dans le `<symbol>`, `color:` sur le wrapper (slide sombre : `color: var(--brand-light)`) |
| Élément qui déborde sur le chrome bas | Composant trop haut, padding-bottom trop court | Audit Playwright, réduire font-sizes / paddings / gaps ; jamais de padding-bottom de slide < 110px |

## CRITIQUE — zone de sécurité du chrome bas

Le chrome bas (marque + signature) est à `inset: 36px` du cadre ; son contenu occupe y ≈ 1014 → 1044 dans le cadre natif 1080.

**Règle dure** : aucun élément de contenu ne dépasse y=1000. Le script QA vérifie `chrome_row.top - lowest_content_bottom ≥ 16px` sur chaque slide.

**Slides typiquement à risque** : KPIs avec gros chiffres, tableaux comparatifs denses, timelines/roadmaps, combos section-head + grille dense + footer-bar.

**Fix en cas d'overlap** :
1. Réduire les font-sizes display (chiffres, totaux).
2. Réduire paddings/gaps des grilles.
3. Réduire le `margin-top` des section-heads.
4. Si le contenu est conceptuellement trop dense → couper en deux slides. « Une idée = une slide » est la discipline qui garde le layout calme.

## CRITIQUE — export PDF et textes en gradient

Chromium a un bug documenté dans son pipeline PDF avec `background-clip: text` + `linear-gradient` : des lignes d'artefacts colorés apparaissent aux bords des inline-blocks multi-lignes. **Aucune combinaison CSS ne le corrige** (testés : `box-decoration-break: clone`, `display: inline`, `isolation: isolate`, resets padding/margin — tous échouent).

**Deux régimes selon l'identité de marque :**

- **La marque titre en couleur solide (pas de gradient sur texte)** — cas le plus simple : laisser `GRADIENT_TEXT_SELECTORS = []` dans `templates/base.html` et le PDF imprime le texte nativement. Il suffit d'activer le mode print (`__enablePrintMode()` ajoute `body.printing-pdf`) puis `window.print()`. Export headless : `page.evaluate("__enablePrintMode()")` puis `page.pdf(prefer_css_page_size=True, print_background=True)` ; vérifier une page par slide (compter `/Type /Page`) et un poids plausible.
- **La marque utilise du texte en gradient** ({{BRAND_GRADIENT}} sur heros / big numbers) : la solution câblée dans `base.html` — avant `window.print()`, parcourir chaque sélecteur de texte-gradient, rendre l'élément dans un `<canvas>` avec le même gradient, remplacer le DOM par des `<img>` PNG, restaurer sur `afterprint`. Sélecteurs à maintenir dans la constante :

```js
const GRADIENT_TEXT_SELECTORS = [
  '.gradient-text',
  '.hero-num',
  '.bigquote em',
  // + tout nouveau sélecteur qui utilise background-clip: text
];
```

Si tu ajoutes un composant à texte-gradient, **ajoute son sélecteur à cette liste**, sinon le PDF montrera des artefacts sur cet élément.

Autres règles print déjà câblées :

- `*` : `-webkit-print-color-adjust: exact` (force gradients / fonds)
- `.stage-frame` : `transform: none` en print (annule le scaling)
- `.slide` : `page-break-before: always` à partir de la slide 2 (évite la page blanche finale)
- `.reveal` : `opacity: 1; transform: none` (saute les animations)
- aurora / dust-grid : `display: none` en print (blurs et gradients 1px rendent mal)
- `*` : `box-shadow: none; text-shadow: none` (banding / halos en print)

Détail complet : `06-graphic-design/presentations/docs/pdf-export.md`.

## Règles brand-strict (toujours)

- **Uniquement** les custom properties de `tokens.css`. Aucun hex en dur dans le deck.
- **Uniquement** les familles de fonts déclarées dans `tokens.css` (miroir de `01-brand/style-guide.md`). Fonts en **local** (woff2 dans `01-brand/assets/fonts/`) si la marque les fournit — pas de CDN dans un livrable.
- Logo dans le chrome bas-droite de chaque slide via `<use href="#brand-logo">` ; watermark ambient possible sur les slides hero.
- Border-radius : {{BRAND_BORDER_RADIUS}} — jamais 0 sauf hairlines techniques (ou exigence de marque explicite).
- Alterner fonds clairs et sombres pour le rythme. Un deck de 20 slides ne doit pas être 20 fonds identiques.
- Mascotte / motif de marque : 1 par slide maximum hors hero ; jamais sur un fond qui l'écrase.
- Les chiffres en héros : display énorme, gradient ou aplat ; texte secondaire petit. Retenue partout.
- Gradient réservé aux titres d'impact (hero, big numbers de slides respiration) — jamais sur les titres standards, sauf si la charte l'exige.
- Interdits : bento grids, glassmorphism gratuit, photos stock, copy pseudo-percutante, et tout ce qui figure dans `{{BRAND_BANNED_VISUALS}}`.

## Vie graphique de la marque

Un deck vivant porte le motif de la marque — jamais de la décoration générique.

1. **Recenser les patterns/motifs reconnaissables de la marque** dans `01-brand/assets/index.md` et `01-brand/style-guide.md` (trames, lignes signature, emblèmes, textures) avant la direction artistique.
2. **S'ils existent, les décliner** plutôt qu'en inventer :
   - **backgrounds à faible opacité** (filigrane ~.05 sur fonds clairs, ~.07 sur fonds sombres) sur les slides de rythme : cover, intercalaires, silences ;
   - **éléments d'angle discrets** sur les slides éditoriales (motif en coin, tracé encre sur fond clair, jamais dans la zone du cartouche ni sous le contenu) ;
   - **filets / ornements typographiques** dérivés du logo-mark (citations, respirations).
3. **Varier les fonds entre familles de slides** (clair, teinté, sombre, texturé) au lieu d'un fond unique : même motif partout, seuls la couleur du tracé et le dosage changent — la variété reste cohérente.
4. **Si la marque n'a aucun motif** : en générer un avec la skill `image-generation` (ou le brandkit) à partir des éléments d'identité existants, et le faire **valider par l'humain** avant tout usage. Jamais décoratif gratuit — toujours issu de la marque.
5. Le motif reste sous tout (`z-index` en dessous du contenu, du chrome et du cartouche), à opacité faible, et la QA Playwright se re-passe après chaque ajout.

Référence exécutée : `_examples/deck-catalogue/catalogue.html` — hooks `--brand-pattern` / `--brand-pattern-light` / `--corner-motif` dans le `:root`, classes `.motif` / `.texture` / `.corner` / `.filet-orn` (doc complète dans son README, section « Vie graphique de la marque »). Le starter `templates/base.html` et `tokens.css` embarquent les mêmes hooks avec un motif placeholder neutre : le remplacer par le motif réel de la marque avant livraison.

**Rappel descendantes de titres** : `line-height ≥ 1.1` sur tous les niveaux de titres texte, jamais de clip. Sur un titre en `background-clip: text` (texte en dégradé), la zone peinte s'arrête à la boîte de l'inline-block : compensation `padding: 0.22em 0.08em; margin: -0.22em -0.08em; overflow: visible` obligatoire, sinon le bas des g / j / p / q disparaît (voir le tableau des pièges).

## Modes de livraison

Trois modes ; défaut = (A). Ne jamais imposer un stack lourd.

**A. Présentation locale**

```
cd 06-graphic-design/presentations
./scripts/serve.sh
```

Serveur statique sur `http://localhost:5173`. Ouvrir le deck : `→` avance, `O` overview, `F` plein écran, `P` impression PDF.

**B. Export PDF**

```
cd 06-graphic-design/presentations
./scripts/export-pdf.sh decks/<deck>.html
```

PDF 1920×1080 propre (une slide par page) via Chromium headless. Voir la section export PDF ci-dessus.

**C. Partage en ligne**

Le deck est un fichier HTML unique, assets inlinés ou en chemins relatifs. Déposer le dossier (ou juste `decks/` + `01-brand/assets/`) sur n'importe quel hébergeur statique. Voir `docs/hosting.md`.

## Livrable final

Un seul fichier : `06-graphic-design/presentations/decks/<sujet>-<date>-<version>.html`, plus les éventuels logos tiers référencés en relatif. Autonome (s'ouvre dans Chrome sans serveur), partageable via `./scripts/serve.sh`, exportable en PDF, hébergeable en statique.

Après livraison : mettre à jour l'entrée du calendrier éditorial (`02-strategy/calendar/calendar.md` — statut + chemin du deck) et indexer le deck dans `_templates/inventory.md` (skill `inventory`, type `deck`).

## Personnalisation par marque

{{SLIDES_SPECIFIC_RULES}}

## Skills associées

- `brand-check` — 5 points obligatoires avant livraison
- `carousel` — carrousel LinkedIn PDF 1080×1350 (pas cette skill)
- `image-generation` — quand le deck a besoin d'un visuel absent de `01-brand/assets/`
- `frontend-design` / `ui-ux-pro-max` — nouveau composant ou identité visuelle encore faible
- `superpowers:brainstorming` — point d'entrée quand l'utilisateur part d'une page blanche
