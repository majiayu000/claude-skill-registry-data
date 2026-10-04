---
name: carousel
description: Génère un carrousel LinkedIn pour {{COMPANY_NAME}} — PDF document multipage 1080×1350 portrait, qualité graphiste expert, brand-strict. Codifie l'échelle typographique, l'échelle d'espacement, le pipeline d'export Playwright avec rastérisation des gradients, et tous les anti-patterns appris en production. À utiliser dès que l'utilisateur demande « carrousel LinkedIn », « slides LinkedIn », « post carrousel » ou similaire. Ne pas confondre les formats — carrousel LinkedIn multipage (cette skill) ≠ présentation projetée 1920×1080 (→ `slides`) ≠ visuel image unique (→ `image-generation`).
---

# carousel — carrousels LinkedIn brand-strict {{COMPANY_NAME}}

Tu construis des carrousels LinkedIn sous forme de PDFs multipages 1080×1350 portrait. Résultat attendu : **niveau graphiste expert**, pas un gabarit générique. Cette skill codifie tout ce qui a été appris en production pour qu'aucune règle ne soit redécouverte.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant le moindre plan de slides :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie carrousels (pas de point final sur les titres, plancher 22px), assets, réutilisation.
2. Charger `01-brand/voice.md` + `01-brand/style-guide.md` — voix, vocabulaire, tokens visuels.
3. Consulter **`01-brand/assets/index.md`** et **lister les assets pertinents** AVANT d'improviser un visuel. Un asset existant se réutilise, il ne se régénère pas. Ne jamais se fier au nom brut d'un fichier : se fier à sa fiche dans l'index.
4. Consulter `_templates/inventory.md` + les carrousels passés de `06-graphic-design/outputs/` : repartir du plus récent validé, pas de zéro.
5. Charger `01-brand/design-anti-generique.md` — doctrine design anti-générique : marqueurs du look IA interdits par défaut (emojis-icônes, excès d'animation, faible densité), checklist de pré-livraison.

**Ne jamais produire sans.** La copy des slides (hook, titres, légendes, finale) passe le filtre anti-style-IA intégral : aucun parallélisme négatif (« pas X, mais Y »), aucun mot IA mort, pas de tiret cadratin, pas de hype. Court, spécifique, une vraie position.

## Quand l'utiliser

- L'utilisateur demande un carrousel LinkedIn / des slides LinkedIn / un post carrousel
- Tu illustres un post LinkedIn long-format avec un PDF document attaché
- Livrable final = PDF prêt à uploader (LinkedIn → « Add a document »)

Présentation projetée en réunion (1920×1080, navigation interactive HTML) → `slides`. Visuel isolé (image carrée, hero web) → `image-generation`.

## Workflow obligatoire

1. **Brief court** : audience LinkedIn, message-clé, copy du post (fournie par l'utilisateur), nombre de slides (8-10 typique).
2. **Plan de slides** : 1 hook + 1 plot twist + actes/preuves + manifeste + CTA. Une ligne par slide.
3. **Brief visuel écrit, validé AVANT construction.** Pour chaque slide : layout, texte, quel bloc porte le gradient (si la marque en a un), et :
   - **3a. Passe catalogue** — parcourir `01-brand/assets/index.md` et **assigner un visuel porteur de sens** à chaque slide (scène, icône, emblème, portrait), avec chemin exact + placement (coin alterné gauche/droite). Si une slide reste sans visuel, le justifier (data brute, manifeste typographique). Une slide « toute en texte » par défaut est un défaut, pas un choix.
   - **3b. Rythme (anti-monotonie)** — planifier la cadence : une **pause visuelle** (gros chiffre ou mot-clé sur fond contrasté, bascule de fond) toutes les 2-3 slides ; varier intensité et compositions. Jamais 8 slides au même gabarit.
4. **Construction** : HTML standalone dans `06-graphic-design/outputs/carrousel-<slug>-<date>/index.html`, à partir de `06-graphic-design/templates/carousel-base.html` (s'il n'existe pas encore, le créer depuis le carrousel validé le plus récent et le référencer dans `_templates/inventory.md`). Tokens CSS en tête (palette, typo, espacement, fonts locales).
5. **Export PDF** : `python3 06-graphic-design/scripts/export-carousel-pdf.py <html> <pdf>` (Playwright headless 1080×1350, rastérisation des gradients — voir plus bas). Créer le script à la première utilisation s'il manque.
6. **Vérification visuelle** : lire le PDF page par page (outil Read). Vérifier contre la checklist anti-patterns. Itérer.
7. **Brand-check + calendrier** : `brand-check` sur la copy du post + du carrousel ; mettre à jour le statut dans `02-strategy/calendar/calendar.md` (et {{EDITORIAL_CALENDAR_TOOL}} si configuré).

## Format LinkedIn

- **Dimensions** : 1080×1350 px (4:5 portrait) — l'optimum du feed mobile LinkedIn (~80% du trafic).
- **Livraison** : PDF document multipage, max 100 MB, max 20 pages (limites LinkedIn).
- **Rendu mobile** : min lisible **22px** source (≈ 8pt physique). Toute taille en dessous → corriger.

## Échelle typographique STRICTE — non négociable

À déclarer en tête du `<style>` (tokens + commentaire). **Aucune taille hors échelle.** Toujours déclarer `font-size` explicitement à chaque niveau hiérarchique (les héritages silencieux ont déjà produit des labels à 16px).

| Rôle | Taille | Line-height | Letter-spacing | Usage |
|---|---|---|---|---|
| `.h-xxl` | 168px | 0.92 | -0.025em | Hook cover (1 slide max par deck) |
| `.h-xl` | 124px | 0.94 | -0.022em | Titres d'impact, plot twists |
| `.h-l` | 88px | 0.98 | -0.018em | Titres standard |
| `.h-m` | 64px | 1.02 | -0.012em | Sous-titres |
| `.h-sub` | 56px | 1.06 | -0.010em | Valeurs, headers tertiaires |
| `.num` | ~300px | 0.90 | -0.03em | Chiffre héros (1 par slide data) |
| `.lede` | 36px | 1.36 | 0 | Premier paragraphe |
| `.body-l` | 30px | 1.42 | 0 | Texte principal |
| `.body-m` | 28px | 1.42 | 0 | Texte secondaire |
| `.caption` | 24px | 1.35 | 0 | Légendes, labels |
| `.eyebrow` | 24px | 1.20 | 0.10em CAPS | Meta uppercase (parcimonieux — souvent à retirer) |
| `.footer` | 22px | — | 0.01em | Baseline footer |

**Seuil absolu : 22px.**

## Échelle d'espacement STRICTE

```css
:root {
  --sp-3xs:   8px;  /* micro (label ↔ valeur) */
  --sp-2xs:  16px;  /* très petit (gap boutons) */
  --sp-xs:   24px;  /* petit (lignes connexes) */
  --sp-sm:   32px;  /* normal (eyebrow → titre) */
  --sp-md:   48px;  /* confortable (blocs voisins) */
  --sp-lg:   64px;  /* généreux (titre → contenu) */
  --sp-xl:   80px;  /* section (contenu → caption) */
  --sp-2xl: 100px;  /* hero (gaps verticaux des slides centrées) */
}
```

**Seuil minimum : `--sp-md` (48px)** pour tout gap entre deux blocs sémantiquement distincts. Aucune valeur hardcodée hors barème.

## Palette et typographie de marque

Tokens dérivés de `01-brand/style-guide.md` — jamais de hex en dur hors des tokens :

- Couleurs : `{{BRAND_COLOR_PRIMARY}}` / `{{BRAND_COLOR_ACCENT}}` / `{{BRAND_COLOR_DARK}}` / `{{BRAND_COLOR_LIGHT}}` ; gradient signature : `{{BRAND_GRADIENT}}`.
- Police : `{{BRAND_FONT_PRIMARY}}`, chargée en **local** (`@font-face` sur les woff2 de `01-brand/assets/fonts/`) — jamais de CDN Google Fonts dans un livrable (Chrome headless capture avant le chargement de la webfont → texte en Helvetica).
- Border-radius : {{BRAND_BORDER_RADIUS}}.
- Interdits visuels : {{BRAND_BANNED_VISUALS}}, tropes « IA » (dégradé violet→néon, cerveau-circuit, robot), glassmorphism, photos stock.

## Le logo : règle absolue

On n'écrit **jamais** le nom de la marque au clavier dans un visuel quand un logo existe. On insère **toujours le vrai logo** (SVG inline, ids dédupliqués) depuis `01-brand/assets/`. Vaut pour les titres et la signature de slide.

## Export PDF — règles critiques (apprises en production)

Chromium rend mal certaines constructions CSS dans son pipeline PDF. Ces règles sont non négociables :

1. **Texte en gradient** (`background-clip: text`) : rendu en rectangle plein ou avec artefacts en PDF. Contournement câblé dans `export-carousel-pdf.py` : chaque élément à gradient est **rastérisé par screenshot Playwright (DPR×2)** puis remplacé par un `<img>` aux dimensions exactes avant `page.pdf()`.
   **Conséquence design** : le gradient ne s'applique qu'à des **blocs autonomes occupant leurs propres lignes** (un titre entier, une ligne dédiée, un `.num`). **Jamais un `<span>` gradient au milieu d'une phrase qui peut wrapper** — la rastérisation casserait le flux inline. Un mot-clé en gradient = sa propre ligne de titre (c'est aussi un meilleur design).
2. **`box-shadow` flou interdit** : Chromium le rend en **rectangle gris plein** à l'export. Pour détacher une carte claire du fond : `border: 1px solid rgba(0,0,0,.12)` fin.
3. **Halo/glow en élément séparé interdit** (div alpha + border-radius) : rastérisé en **bande grise rectangulaire**. Cuire l'ambiance dans le `background` de la slide (radial-gradients alpha très faibles ~.05, sous un éventuel grain qui les dither).
4. **Élément DOM à fond gradient** (bouton CTA pill, badge, cadre) : rasterisé avec bords crénelés au zoom. Le rendre en **SVG vecteur** (gradient en `<linearGradient>` + texte vecteur).
5. **SVG à `fill="url(#pattern)"` ou image embarquée** : rendu tronqué dans certains lecteurs (LinkedIn mobile). **Pré-rastériser en PNG** (Playwright, `omit_background`).
6. **Rotation d'un cadre photo** : jamais `transform: rotate()` CSS sur un div (rasterisation → bords en escalier) ; incliner par une rotation **vecteur à l'intérieur du SVG** (`<g transform="rotate(…)">`), photo en `<image>` embarqué pleine résolution.
7. **Photos** : copies redimensionnées à **~1800-2400px sur le grand côté, qualité ~92** dans `outputs/.../photos/` — jamais les originaux pleine résolution (PDF trop lourd) ni sous 2000px (flou au zoom : `page.pdf` embarque la résolution source telle quelle). Vérifier avec `pdfimages -list <pdf>`.
8. **Zone basse ~12% de la slide** : la barre du lecteur PDF mobile LinkedIn la recouvre. Aucun contenu critique (visage, tampon, CTA) dans cette zone ; un élément peut y déborder de façon sacrificielle, pas son point focal.

Recette minimale du script d'export (à créer dans `06-graphic-design/scripts/export-carousel-pdf.py` si absent) : Playwright Chromium headless, viewport 1080×1350, `device_scale_factor=2` ; screenshot de chaque élément `[data-raster]` (ou classe gradient) et remplacement DOM par `<img>` ; puis `page.pdf(width="1080px", height="1350px", print_background=True, prefer_css_page_size=True)` avec `page-break-after` câblé sur chaque `.page`.

## Précision graphique — grille de repère OBLIGATOIRE

Les alignements comptent autant que le contenu. Jamais « à l'œil » :

- **Overlay de grille activable** dans le HTML (lignes horizontales tous les 50px + numéros + axe central vertical) pour MESURER puis positionner ; le retirer pour le livrable final.
- Un titre posé dans une forme conteneur doit être **centré dans la masse de la forme** (jamais calé en haut) : mesurer le vide au-dessus et en dessous, égaliser.
- **Aucun mot orphelin** en fin de bloc (titre, lede, CTA) : contrôler explicitement les sauts de ligne (lignes de titre voulues, lede en liste de lignes, `white-space: nowrap` sur les noms propres).
- **Aucun mot composé coupé** en fin de ligne : tiret insécable U+2011.
- Vérifier à la grille, **slide par slide**, avant livraison : centrages, marges, alternance gauche/droite, débordements, chevauchements.

## Anti-uniformité — grammaires visuelles

Un carrousel ne doit pas ressembler au précédent. Choisir/inventer une **grammaire visuelle** selon le type de contenu, puis la varier :

- **Famille « portrait / humain »** : titres centrés, forme de marque conteneur sur cover/finale, visuels de coin, finale chaleureuse. Pour les portraits, témoignages.
- **Famille « thèse / données »** : grille cassée, aligné à gauche, cover plein cadre + filet, slides data en split-screen (chiffre héros ↔ caption), finale CTA plein cadre. Pour les posts marché/data.
- **Famille « photo / carnet »** : portée par de vraies photos (cadres de marque en SVG vecteur, alternance gauche/droite, fil conducteur graphique entre les slides).

Même palette pour toutes ; ce qui change = composition, alignement, traitement des données/photos. Pour un nouveau sujet, repartir de la famille adaptée et **inventer des compositions propres**.

## Anti-patterns UX LinkedIn (à retirer systématiquement)

1. **Pas de folio « 01 / 10 »** — LinkedIn affiche son propre indicateur de progression.
2. **Footer = le domaine seul** (ex. `{{COMPANY_WEBSITE}}`) — pas de « Marque · domaine » redondant. Et jamais footer domaine + bouton CTA domaine sur la même slide : sur la finale, l'URL vit dans le CTA.
3. **Pas d'eyebrow « Acte 1 / Acte 2 »** — les titres parlent d'eux-mêmes.
4. **Pas de point final sur les titres** (`.h-*`, punchlines, CTA courts). Les paragraphes (`.lede`, `.body-*`) gardent leur ponctuation.
5. **Pas de tiret cadratin (`—`)** — `–` ou reformuler.
6. **Pas d'emoji Unicode** (💡, ✅, ✨…) — icône de marque depuis `01-brand/assets/` ou générée via `image-generation`.
7. **Pas de label sous les visuels expressifs** (portraits, mascottes) — ils se lisent d'eux-mêmes.
8. **Flèche de progression → (droite)** sur le hook, jamais ↓ (le carrousel se lit en swipe horizontal).
9. Pas de taille hors échelle, pas de gap < 48px entre blocs distincts, pas de forme abstraite improvisée quand un asset de marque existe.

## Journalisation obligatoire

Chaque carrousel laisse trois traces :

- **Brief** : `06-graphic-design/briefs/<date>-carrousel-<slug>.md` (audience, copy du post, plan de slides + passe catalogue + rythme, validation).
- **Source + export** : `06-graphic-design/outputs/carrousel-<slug>-<date>/index.html` et `exports/<slug>.pdf`.
- **Calendrier** : statut mis à jour dans `02-strategy/calendar/calendar.md` (+ {{EDITORIAL_CALENDAR_TOOL}} si configuré).

Les assets contextuels générés restent en staging dans `outputs/` ; ils ne migrent vers `01-brand/assets/` (avec fiche `index.md`) qu'après validation humaine.

## Personnalisation par marque

{{CAROUSEL_SPECIFIC_RULES}}

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/social-linkedin.md` pour le détail sourcé :

1. Le carrousel/document est le **format n°1 sur LinkedIn en 2026** : 3,71 % d'engagement vs 1,80 % pour la vidéo (Metricool, 673 k posts) ; +278 % vs vidéo (Buffer, 2 M posts). L'assumer dans les recommandations de mix.
2. **Slide 1 = hook autonome lisible dans le feed** — elle doit fonctionner seule, avant tout swipe et sans le texte du post.
3. **Optimiser chaque slide pour le swipe** : tension, question ouverte ou série numérotée qui donne envie d'ouvrir la suivante — les swipes et saves comptent dans l'engagement « invisible » qui monte (+14 %).
4. **Juger la performance sur impressions, swipes et saves**, pas sur les likes (en baisse structurelle de −13 %).

## Skills associées

- `slides` — présentations projetées 1920×1080 (pas pour LinkedIn)
- `image-generation` — génération d'icônes / illustrations brand-compliant (consulte d'abord `01-brand/assets/index.md`)
- `social-content` — copy du post qui accompagne le carrousel
- `copy-editing` — relecture de la copy
- `brand-check` — validation finale obligatoire
