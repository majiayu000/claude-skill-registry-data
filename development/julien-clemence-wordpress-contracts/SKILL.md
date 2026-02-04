---
name: julien-clemence-wordpress-contracts
description: Development contracts for clemencefouquet.fr WordPress theme. Enforces rules for Gutenberg blocks, patterns, header, and footer. Use when creating or modifying theme components.
allowed-tools: Read, Write, Edit, Bash
---

# WordPress Development Contracts - clemencefouquet.fr

Contracts for consistent, accessible, and maintainable code in the Clémence Fouquet WordPress theme.

## Quick Reference

| Contract | Purpose |
|----------|---------|
| [Block](#1-block-contract) | Gutenberg blocks structure |
| [Pattern](#2-pattern-contract) | Block patterns composition |
| [Header](#3-header-contract) | Header accessibility & glassmorphisme |
| [Footer](#4-footer-contract) | Footer grid & legal |

**Resources**: [tokens.md](references/tokens.md) | [checklists.md](references/checklists.md) | [code-examples.md](references/code-examples.md)

---

# 1. Block Contract

## Structure obligatoire

```
blocks/block-name/
├── block.json     # Metadata (OBLIGATOIRE)
├── edit.js        # Composant éditeur React
├── render.php     # Rendu dynamique serveur
├── style.css      # Styles front-end
└── index.js       # Point d'entrée
```

## Règles fondamentales

### block.json requis
- `name`: Namespace unique (`clemence/card`)
- `title`, `category`, `attributes`, `supports`

### Attributs typés
```json
{ "title": { "type": "string", "default": "" } }
```

### CSS avec tokens
```css
.c-card {
  background: var(--wp--preset--color--white);
  padding: var(--wp--preset--spacing--50);
}
```
> Voir [references/tokens.md](references/tokens.md) pour tous les tokens

### PHP échappé
```php
<div <?php echo get_block_wrapper_attributes(['class' => 'c-card']); ?>>
  <h3><?php echo esc_html($title); ?></h3>
</div>
```
- `esc_html()` pour texte, `esc_attr()` pour attributs, `esc_url()` pour URLs

### JS imports WordPress
```javascript
import { useBlockProps, RichText } from '@wordpress/block-editor';
```

> Exemples complets: [references/code-examples.md](references/code-examples.md)
> Checklist: [references/checklists.md](references/checklists.md#checklist-bloc-gutenberg)

---

# 2. Pattern Contract

## Règle fondamentale

> **Un pattern = composition de blocs existants**
> **JAMAIS de CSS additionnel**

## Header obligatoire

```php
<?php
/**
 * Title: Hero Violet Organique
 * Slug: clemence/hero-violet-organic
 * Categories: clemence-sections
 * Keywords: hero, banner, organic
 */
?>
```

## Règles

| Faire | Ne pas faire |
|-------|--------------|
| `<!-- wp:heading -->` | `<div class="custom">` |
| `{"textColor":"violet-500"}` | `{"style":{"color":"#5b2e7f"}}` |
| Presets theme.json | Valeurs hardcodées |

> Exemple complet: [references/code-examples.md](references/code-examples.md#pattern---exemple-complet)
> Checklist: [references/checklists.md](references/checklists.md#checklist-pattern)

---

# 3. Header Contract

## Structure HTML

```html
<header class="l-header">
  <a href="#main-content" class="l-header__skip">Aller au contenu</a>
  <div class="l-header__logo"><!-- wp:site-logo --></div>
  <nav class="l-header__nav" aria-label="Navigation principale">...</nav>
  <button class="l-header__toggle" aria-controls="mobile-nav" aria-expanded="false">
    <span class="l-header__toggle-icon"></span>
  </button>
</header>
<div id="mobile-nav" class="l-mobile-nav" aria-hidden="true">...</div>
```

## Glassmorphisme

```css
@layer components {
  .l-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
  }
}
```

## Accessibilité obligatoire

- **Skip link** en premier élément
- **aria-controls/aria-expanded** sur toggle
- **Escape** ferme le menu
- **Touch targets** 44x44px minimum

> JavaScript complet: [references/code-examples.md](references/code-examples.md#header---javascript-complet)
> Checklist: [references/checklists.md](references/checklists.md#checklist-header)

---

# 4. Footer Contract

## Structure HTML

```html
<footer class="l-footer">
  <div class="l-footer__wave"><svg>...</svg></div>
  <div class="l-footer__grid">
    <div class="l-footer__col">
      <h2>À propos</h2>
      <p>...</p>
    </div>
    <div class="l-footer__col">
      <h2>Navigation</h2>
      <nav aria-label="Navigation footer"><ul>...</ul></nav>
    </div>
    <div class="l-footer__col">
      <h2>Contact</h2>
      <address><a href="mailto:contact@clemencefouquet.fr">...</a></address>
    </div>
    <div class="l-footer__col">
      <h2>Suivez-moi</h2>
      <ul class="l-footer__social">
        <li><a href="#" aria-label="LinkedIn"><svg>...</svg></a></li>
      </ul>
    </div>
  </div>
  <div class="l-footer__legal">
    <p>&copy; 2025 Clémence Fouquet</p>
    <nav aria-label="Liens légaux"><a href="/mentions-legales">Mentions légales</a></nav>
  </div>
</footer>
```

## Règles CSS

- Fond: `var(--wp--preset--color--violet-700)`
- Texte: `white` ou `beige-100`
- Grid: 1→2→4 colonnes responsive
- Police minimum: 14px

> CSS complet: [references/code-examples.md](references/code-examples.md#footer---css-complet)
> Checklist: [references/checklists.md](references/checklists.md#checklist-footer)

---

# Anti-patterns communs

| Ne pas faire | Faire |
|--------------|-------|
| `!important` | Augmenter spécificité ou `@layer` |
| `#id-selector` | `.l-class-selector` |
| `color: #5b2e7f` | `var(--wp--preset--color--violet-500)` |
| `.a .b .c .d` (4 niveaux) | `.l-a__d` (2 niveaux max) |

---

# Skill Chaining

## Input Expected
- Projet WordPress avec thème FSE
- Theme.json configuré avec tokens
- Structure `/blocks/`, `/patterns/`, `/parts/`

## Output Produced
- Blocs/patterns/composants conformes aux contracts
- Code accessible WCAG AA
- CSS maintenable avec @layer et BEM

## Skills Required Before
- **julien-clemence-wordpress-tooling**: Pour setup linters et architecture CSS

## Compatible Skills After
- **julien-clemence-wordpress-remote**: Pour déployer sur VPS
- **julien-wordpress-structure-validator**: Pour valider la structure

## Tools Used
- `Read` - Lire theme.json, fichiers existants
- `Write` - Créer blocks, patterns
- `Edit` - Modifier composants existants
- `Bash` - Commandes npm/build
