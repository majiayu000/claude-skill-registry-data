---
name: frontend-design
description: Design frontend pro — palettes, typographie, layout, responsive. Injecté dans le Coder pour les tâches web (landing, portfolio, doc, app, visualizer).
---

# Skill : Frontend Design Pro (condensé)

Fais des choix **délibérés et spécifiques**, jamais génériques. **Distingue d'abord la
nature de l'interface** — ce n'est pas le même design.

## ⚠️ ÉTAPE 0 (OBLIGATOIRE) — Quelle interface construis-tu ?

Avant d'écrire une ligne de CSS, classe la tâche dans UNE de ces 2 catégories. Le design
en dépend totalement :

| Nature | Exemples | Layout | Titre h1 |
|--------|----------|--------|----------|
| **APP / TOOL** (défaut) | visualiseur d'algorithme, calculatrice, éditeur, dashboard, jeu, todo, visualizer, converter | **empilé vertical, centré**, une seule colonne, contenu dans une **card** (surface + box-shadow + border-radius) | **1.5rem–2rem** (lisible, discret) |
| **LANDING / PAGE** | landing page, portfolio, page de doc, site vitrine | sections, hero autorisé, macro-layout | 2.5rem–3rem max |

**Quand tu hésites → APP/TOOL** (le défaut sûr). Un visualiseur, un éditeur, un outil, un
jeu, une calculatrice = APP. Réserve les grands titres et le layout en colonnes aux
véritables landing pages.

**Contre-exemple à éviter** (bug observé) : un « Bubble Sort Visualizer » traité comme une
landing page → `h1` à 3.5rem/4rem énorme + layout row à 1024px = page illisible. Un
visualiseur est une **APP** : titre ~1.75rem, tout empilé verticalement dans une card.

## Système de tokens (à définir AVANT de coder, en :root)
**Palette — 4 à 6 hex nommés, fort contraste, un seul accent signature :**
```css
:root{ --bg:#0b1020; --surface:#121a33; --text:#e6ebff; --muted:#94a0c4; --accent:#6c8cff; --accent-2:#39e6c4; }
```
**Typo — 2 rôles, stack système (pas de CDN) :**
```css
--font-display:"Segoe UI",system-ui,sans-serif; /* titres 700/800 */
--font-body:system-ui,-apple-system,sans-serif;  /* corps 400/500 */
```
**Règle de COMPLÉTUDE (non négociable) :** chaque `var(--x)` que tu ÉCRIS doit être
DÉCLARÉE dans le `:root` ci-dessus — une var référencée mais jamais définie rend la
propriété INVALIDE à l'exécution (police serif par défaut, couleurs transparentes).
Un fallback se met DANS les parenthèses : `var(--font-body, system-ui)` — jamais
`var(--font-body), system-ui` (ça ne protège de rien).

## Typographie — fourchettes (NE JAMAIS dépasser le max)
**APP/TOOL (défaut) :** `h1` 1.5–2rem · `h2` 1.25–1.5rem · corps 1rem · lead 1.1rem ·
interlignage 1.6.
**LANDING/PAGE seulement :** `h1` 2.5–3rem (hero) · `h2` 1.5–2rem · lead 1.25rem.

**Garde anti-titre-géant :** un `h1` > 3rem est INTERDIT sauf hero unique d'une landing
page. Sur une app, un `h1` à 3.5rem/4rem est un BUG — le titre ne doit pas dominer
l'écran au point d'écraser le contenu fonctionnel.

## Layout
- **APP/TOOL** : tout dans une **card** centrée (`.container { max-width: ~900px; margin:
  0 auto; background: var(--surface); padding: 2rem; border-radius: 12px; box-shadow: 0 4px
  30px rgba(0,0,0,.5) }`). Vertical, empilé. **NE FAIS PAS de layout `row` à 1024px** pour
  une app — cela casse la lisibilité (titre à gauche, viz à droite = illisible). Reste en
  une colonne à toutes les résolutions.
- **LANDING/PAGE** : CSS Grid pour macro-layouts (sections, grille features), Flexbox pour
  alignement local. Mobile-first : 1 colonne défaut, media queries (min-width: 640px,
  1024px).
- **Une seule signature mémorable** (ex: dégradé animé subtil sur le hero d'une landing),
  pas un saupoudrage d'effets. Une app n'a pas besoin de signature flashy — la clarté prime.
- Animations subtiles : `transition: transform .2s`, apparition au scroll via
  IntersectionObserver.

## Visualiseurs d'algorithmes — plancher d'effets (F-124, non négociable)
La sobriété vaut pour le CHROME (card, titres, contrôles). Dans un visualiseur, les éléments
animés SONT le produit : le spec de l'Architecte est un PLANCHER — complète-le, jamais aplats.
- **Règle de REMPLISSAGE (F-164, quantitative)** : les éléments de données (barres,
  colonnes, points) doivent REMPLIR la largeur de leur conteneur — `flex: 1` par
  élément dans un conteneur flex (ou largeur calculée `calc()`). INTERDIT : un
  `width: Npx` ou `max-width: Npx` FIXE sur ces éléments (barres de 10-30 px dans
  un board de 800 px = la moitié de l'écran vide). Un board à moitié vide est un
  BUG visuel, même avec 0 erreur console.
- `comparing` : accent dédié + glow (`box-shadow: 0 0 12px var(--accent)`) + `scaleY(1.06)`.
- `sorted` : dégradé distinct (ex. `linear-gradient(180deg,var(--accent-2),var(--accent))`),
  appliqué PROGRESSIVEMENT (position par position), pas toutes les barres d'un coup.
- swaps : `transition: height .25s cubic-bezier(.34,1.56,.64,1)` — jamais de saut sec.
- Compteurs en pills (`border-radius:999px`, `tabular-nums`) ; fond de scène : grille ou
  vignette subtile. Interdit : toutes les barres en UN aplat monochrome (bug run #12).

## Finition (non négociable)
Responsive mobile · focus clavier visible (`:focus-visible`) · `prefers-reduced-motion`
respecté · contraste WCAG AA · sémantique HTML5 (`<header><nav><main><section><article><footer>`,
un seul `<h1>`).

Concentre ton audace sur UN élément, garde le reste discipliné. La copy est un matériau de
design, pas de la décoration.
