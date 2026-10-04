---
name: design-system
description: Générer ou compléter un système de design web pour {{COMPANY_NAME}} — palette sémantique, pairing typographique, style UI, échelles d'espacement et tokens CSS — toujours sous contrainte des tokens de marque 01-brand. Utiliser quand un livrable web (landing page, page statique, dashboard de reporting, email HTML riche) a besoin d'un système de composants cohérent, quand il faut choisir un style visuel, une palette ou une typographie, ou quand une autre skill (landing-page, design-direction) demande les tokens. Vendorisée depuis ui-ux-pro-max (MIT, NextLevelBuilder) — voir docs/vendored-design.md.
---

# design-system — système de design web sous contrainte de marque

Vous produisez des systèmes de design complets : tokens sémantiques, style UI, palette, typographie, échelles. Les données de référence (styles, palettes, pairings) sont condensées dans `references/` — elles servent de bibliothèque de fallback, jamais de source prioritaire.

## Étape 0 — Charger les design tokens de la marque (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur tout style générique de cette skill.**

1. Lire `01-brand/style-guide.md` : couleurs, police, radius, gradient, style d'illustration, interdits visuels.
2. Lire `01-brand/checklist-pre-composition.md` si présent (règles anti-style-IA) et `01-brand/design-anti-generique.md` (doctrine design anti-générique — elle gouverne les dimensions libres, jamais celles verrouillées par la marque).
3. Classer chaque dimension du système en deux catégories :
   - **Verrouillée par la marque** — le style-guide fournit une valeur (ex. couleur primaire, police). On l'utilise telle quelle. Interdiction de la remplacer par une valeur des références de cette skill.
   - **Libre** — le style-guide est muet (ex. couleur `muted`, échelle d'espacement, style des états d'interaction). C'est le seul espace où les références de cette skill s'appliquent.

Si `01-brand/style-guide.md` est manquant ou contient des `{{...}}` : s'arrêter et proposer `/start-cockpit`. Ne jamais générer un système 100 % générique pour un projet configuré.

## Étape 1 — Qualifier le besoin

Extraire du brief :
- **Type de livrable** : landing page, page produit, dashboard de reporting, page événement, espace client…
- **Type de produit / secteur** : SaaS, service B2B, agence, e-commerce, formation, communauté… (sert à choisir palette et style de fallback dans `references/`)
- **Tonalité** : sobre, premium, énergique, éditorial, technique…
- **Contraintes** : dark mode requis, contrainte de performance, audience accessibilité renforcée.

## Étape 2 — Composer le système

Ordre de résolution pour **chaque token** : `01-brand/style-guide.md` → dérivation depuis la marque (teintes, opacités) → `references/` de cette skill → défaut neutre. Documenter la provenance de chaque valeur dans le livrable.

1. **Style UI** — choisir dans `references/styles.md` le style compatible avec la marque ET le type de produit. Vérifier la colonne « Ne pas utiliser pour ». Un seul style par site ; pas de mélange flat/glassmorphism aléatoire.
2. **Palette sémantique** — construire les 12 rôles à partir de la marque :

   | Rôle | Source |
   |---|---|
   | `--primary` / `--on-primary` | `{{BRAND_COLOR_PRIMARY}}` + contraste calculé |
   | `--accent` / `--on-accent` | `{{BRAND_COLOR_ACCENT}}` (CTA) |
   | `--background` / `--foreground` | `{{BRAND_COLOR_LIGHT}}` / `{{BRAND_COLOR_DARK}}` |
   | `--card` / `--card-foreground` | dérivés du background (élévation) |
   | `--muted` / `--muted-foreground` | dérivés neutres (texte secondaire ≥ 4.5:1) |
   | `--border`, `--ring`, `--destructive` | dérivés ou `references/palettes.md` |

   Si la marque ne fournit que 2-3 couleurs, compléter les rôles manquants par dérivation (jamais en remplaçant les couleurs fournies). `references/palettes.md` sert uniquement de calibration (quel niveau de saturation pour tel secteur) ou de fallback si la marque n'a pas de couleurs du tout.
3. **Typographie** — `{{BRAND_FONT_PRIMARY}}` est la police de référence. Décider de son rôle (display, body ou les deux) et compléter si besoin avec un pairing de `references/typographie.md` compatible. Échelle type : 12 / 14 / 16 / 18 / 24 / 32 / 48 px, body ≥ 16 px, line-height 1.5–1.75.
4. **Espacement et rythme** — échelle 4/8 px (4, 8, 12, 16, 24, 32, 48, 64). Radius : `{{BRAND_BORDER_RADIUS}}` partout, décliné en échelle (sm/md/lg) cohérente.
5. **Effets et états** — ombres/blur/gradients alignés sur le style choisi (étape 2.1) et le `{{BRAND_GRADIENT}}` éventuel. Chaque interactif a 4 états : default, hover, active/pressed, disabled. Transitions 150–300 ms, `transform`/`opacity` uniquement.
6. **Dark mode** (si demandé) — variantes désaturées/éclaircies, jamais une simple inversion. Re-vérifier les contrastes séparément.

## Étape 3 — Livrer les tokens

Livrer un bloc `:root` CSS prêt à coller, précédé d'un tableau récapitulatif (token, valeur, provenance : marque / dérivé / référence). Exemple de squelette :

```css
:root {
  /* Marque — 01-brand/style-guide.md (ne pas modifier) */
  --primary: {{BRAND_COLOR_PRIMARY}};
  --accent: {{BRAND_COLOR_ACCENT}};
  --background: {{BRAND_COLOR_LIGHT}};
  --foreground: {{BRAND_COLOR_DARK}};
  --radius: {{BRAND_BORDER_RADIUS}};
  --font-sans: '{{BRAND_FONT_PRIMARY}}', system-ui, sans-serif;
  /* Dérivés + fallbacks références (documenter chaque choix) */
  --muted: …; --muted-foreground: …; --border: …; --ring: …;
  --space-1: 4px; --space-2: 8px; --space-3: 16px; --space-4: 24px; --space-5: 48px;
}
```

Si le livrable appartient à un dossier de production (`05-web-content/`, `06-graphic-design/`, `11-reporting/`), enregistrer le système à côté du livrable (ex. `05-web-content/landing-pages/<slug>/design-tokens.md`) pour réutilisation.

## Garde-fous (non négociables)

- **Contraste** : texte normal ≥ 4.5:1, texte large et composants UI ≥ 3:1 (WCAG AA). Vérifier chaque paire fond/texte du système.
- **Pas d'emoji comme icônes structurelles** : SVG uniquement (Lucide, Heroicons, Phosphor), un seul set par projet, stroke cohérent.
- **Tokens sémantiques, pas de hex brut** dans les composants.
- **Un seul CTA primaire par écran** ; les actions secondaires sont visuellement subordonnées.
- **Interdits visuels de la marque** (`{{BRAND_BANNED_VISUALS}}`) : ils l'emportent sur toute recommandation des références. Si un style de `references/styles.md` entre en conflit avec un interdit, écarter le style.
- Passer le résultat par la skill `design-review` avant toute livraison de code UI.

## Références embarquées

| Fichier | Contenu | Usage |
|---|---|---|
| `references/styles.md` | ~20 styles UI web (quand, jamais, effets, mots-clés CSS) | Choix du style — étape 2.1 |
| `references/palettes.md` | ~28 palettes sémantiques par type de produit (WCAG-ajustées) | Calibration / fallback couleur — étape 2.2 |
| `references/typographie.md` | ~24 pairings Google Fonts par tonalité | Complément typo — étape 2.3 |

---

*Source : données condensées et adaptées de [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) v2.5.0, © 2024 Next Level Builder, licence MIT. Adaptations : recentrage web marketing (mobile natif, Flutter, SwiftUI, BI exclus), priorité absolue aux tokens 01-brand, suppression de la dépendance aux scripts Python. Registre : `docs/vendored-design.md`.*
