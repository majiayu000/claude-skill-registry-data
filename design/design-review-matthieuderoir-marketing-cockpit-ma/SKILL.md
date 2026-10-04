---
name: design-review
description: Réviser et corriger l'UI des livrables web de {{COMPANY_NAME}} (landing pages, pages statiques, emails HTML riches, dashboards de reporting) — conformité marque, accessibilité WCAG, responsive, performance perçue, formulaires, animations. Utiliser avant toute livraison de code UI, quand l'utilisateur dit « review cette page », « le design fait pas pro », « corrige l'UI », ou en QA finale des skills landing-page / design-system / design-direction. Vendorisée depuis ui-ux-pro-max (MIT, NextLevelBuilder) — voir docs/vendored-design.md.
---

# design-review — revue et correction UI des livrables web

Vous êtes le passage QA design obligatoire avant livraison. Deux modes : **review** (rapport de findings priorisés, sans toucher au code) et **fix** (corrections appliquées, listées et justifiées). Par défaut : review, puis fix sur validation.

## Étape 0 — Charger les design tokens de la marque (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur tout style générique de cette skill.**

1. Lire `01-brand/style-guide.md` : couleurs, police, radius, gradient, interdits visuels (`{{BRAND_BANNED_VISUALS}}`).
2. Lire `01-brand/design-anti-generique.md` : la revue traque aussi les patterns « IA générique » — un livrable conforme aux tokens mais visuellement générique est un 🟠.
3. Si un `design-tokens.md` accompagne le livrable (produit par la skill `design-system`), le charger : c'est le contrat à vérifier.
4. La conformité marque est la **priorité 0** de la revue, avant même l'accessibilité : une page accessible mais hors marque est refusée aussi sûrement qu'une page inaccessible.

Si `01-brand/style-guide.md` est manquant ou contient des `{{...}}`, signaler et limiter la revue aux priorités 1-8 (génériques).

## Format du rapport

Pour chaque finding : `[P{n}-{sévérité}] {fichier}:{ligne} — {problème} → {correction}`. Sévérités : `bloquant` (livraison interdite), `majeur` (corriger avant publication), `mineur` (amélioration). Conclure par un verdict : ✅ livrable / ⚠ corrections majeures requises / ❌ retour en production.

## Grille de revue par priorité

### P0 — Conformité marque (BLOQUANT)

- Couleurs = tokens du style-guide, aucun hex étranger à la marque sur les éléments identitaires (CTA, titres, fonds).
- Police = `{{BRAND_FONT_PRIMARY}}` (+ complément validé). Radius = `{{BRAND_BORDER_RADIUS}}` décliné en échelle cohérente.
- Aucun interdit visuel de `{{BRAND_BANNED_VISUALS}}`.
- Logos : assets officiels de `01-brand/assets/`, proportions et zones de protection respectées — jamais recolorés ou déformés.

### P1 — Accessibilité (CRITIQUE)

- Contraste : texte normal ≥ 4.5:1, texte large (≥ 24 px ou 19 px gras) et composants UI ≥ 3:1. Tester aussi le dark mode s'il existe.
- Focus visible (ring 2-4 px) sur tout élément interactif — ne jamais supprimer `outline` sans remplacement.
- `alt` descriptif sur les images porteuses de sens ; `alt=""` sur le décoratif.
- `aria-label` sur les boutons icône-seul ; ordre de tabulation = ordre visuel ; lien « aller au contenu ».
- Hiérarchie de titres séquentielle (h1→h6, sans saut) ; un seul h1.
- L'information n'est jamais portée par la couleur seule (ajouter icône ou texte).
- `prefers-reduced-motion` respecté : animations réduites/désactivées avec fallback complet.

### P2 — Interaction et cibles (CRITIQUE)

- Cibles tactiles ≥ 44×44 px, espacement ≥ 8 px entre cibles.
- `cursor: pointer` sur le cliquable ; hover n'est jamais le seul chemin vers une interaction.
- Feedback visuel ≤ 100 ms au clic ; boutons désactivés + spinner pendant les opérations async.
- 4 états distincts sur chaque interactif : default / hover / active / disabled (opacité 0.38-0.5 + cursor).
- Confirmation avant toute action destructive.

### P3 — Performance perçue (HAUTE)

- Images : WebP/AVIF, `srcset/sizes`, `loading="lazy"` sous le pli, `width/height` ou `aspect-ratio` déclarés (CLS < 0.1).
- Fonts : `font-display: swap`, précharger uniquement les graisses critiques.
- Espace réservé pour tout contenu async (pas de saut de layout) ; skeleton au-delà de 300 ms de chargement.
- Scripts tiers en `async/defer` ; CSS critique en tête.
- Vidéo : jamais d'autoplay avec son ; click-to-play ou pause hors écran ; compressée.

### P4 — Cohérence de style (HAUTE)

- Un seul style UI sur tout le livrable ; ombres/blur/radius alignés sur ce style (échelle d'élévation unique).
- **Pas d'emoji comme icônes structurelles** : SVG uniquement (Lucide, Heroicons, Phosphor), un seul set, stroke constant (1.5 ou 2 px), filled vs outline discipliné par niveau de hiérarchie.
- Tailles d'icônes tokenisées (sm/md/lg), alignées sur la baseline du texte.
- Un seul CTA primaire par écran ; secondaires visuellement subordonnés.
- Tokens sémantiques partout — aucun hex brut dans les composants.

### P5 — Layout et responsive (HAUTE)

- `<meta name="viewport" content="width=device-width, initial-scale=1">` — jamais de blocage du zoom.
- Aucun scroll horizontal ; tester 320 / 375 / 768 / 1024 / 1440 px.
- Corps ≥ 16 px sur mobile ; mesure 35-60 caractères mobile, 60-75 desktop.
- Échelle d'espacement 4/8 px systématique ; rythme vertical hiérarchisé (ex. 16/24/32/48).
- `max-width` cohérente sur desktop ; échelle z-index définie (10/20/40/100/1000) ; padding compensant les barres fixes/sticky.
- Préférer `min-height: 100dvh` à `100vh` sur mobile ; `max-width: 100%` sur les images ; tableaux → scroll horizontal contenu ou passage en cartes.

### P6 — Typographie et couleur (MOYENNE)

- Line-height 1.5-1.75 pour le corps ; échelle modulaire cohérente ; hiérarchie par la graisse (700/400/500).
- Texte sombre sur fond clair (pas de gris-sur-gris) ; chiffres tabulaires pour données/prix.
- Troncature : préférer le retour à la ligne ; sinon ellipse + accès au texte complet.
- Dark mode : variantes désaturées, jamais une inversion ; contrastes re-testés séparément.

### P7 — Animation (MOYENNE)

- Micro-interactions 150-300 ms ; transitions complexes ≤ 400 ms ; jamais > 500 ms.
- `transform`/`opacity` uniquement — jamais `width/height/top/left` (reflow).
- `ease-out` en entrée, `ease-in` en sortie ; sortie ~60-70 % de la durée d'entrée.
- 1-2 éléments animés max par vue ; chaque animation exprime une relation cause-effet, pas une décoration.
- Stagger de listes 30-50 ms/item ; aucune animation ne bloque l'input utilisateur.

### P8 — Formulaires et feedback (MOYENNE)

- Label visible par champ (jamais placeholder-seul) ; erreur sous le champ concerné, avec cause + correction.
- Validation au blur (pas à la frappe) ; focus auto sur le premier champ invalide après soumission ; `aria-live`/`role="alert"` pour les erreurs.
- Types sémantiques (`email`, `tel`, `url`, `number`) + `autocomplete` ; hauteur d'input ≥ 44 px.
- États submit : loading → succès/erreur ; toasts auto-fermés 3-5 s sans voler le focus.
- États vides utiles (message + action) ; parcours multi-étapes avec indicateur de progression et retour possible.

## Checklist express pré-livraison

À dérouler en dernier passage, dans l'ordre :

- [ ] P0 : tokens marque exacts, aucun interdit visuel, logos officiels
- [ ] Contrastes 4.5:1 / 3:1 vérifiés (light **et** dark)
- [ ] Focus visibles, navigation clavier complète, `alt` et `aria-label` posés
- [ ] Zéro emoji-icône ; un seul set SVG cohérent
- [ ] Testé 320-375 px et desktop ; zéro scroll horizontal ; corps ≥ 16 px
- [ ] `prefers-reduced-motion` respecté ; animations `transform/opacity` 150-300 ms
- [ ] Images dimensionnées + lazy ; pas de saut de layout
- [ ] Formulaires : labels, erreurs claires, feedback submit
- [ ] Un seul CTA primaire par écran

Si le livrable est du contenu marketing en dossier de production, enchaîner avec la skill `brand-check` (fond éditorial) — `design-review` couvre la forme, pas le message.

---

*Source : règles condensées et adaptées de [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) v2.5.0 (`quick-reference.md` + `ux-guidelines.csv`), © 2024 Next Level Builder, licence MIT. Adaptations : recentrage web (règles iOS/Android/React Native/Flutter écartées), ajout de la priorité P0 conformité marque, format de rapport et modes review/fix. Registre : `docs/vendored-design.md`.*
