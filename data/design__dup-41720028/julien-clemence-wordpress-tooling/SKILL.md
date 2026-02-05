---
name: julien-clemence-wordpress-tooling
description: Build tools, CSS architecture, and Git workflows for clemencefouquet.fr WordPress theme. Covers linting, @layer CSS, and sync between Laragon/Git/VPS.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# WordPress Tooling - clemencefouquet.fr

Build tools, CSS architecture, and deployment workflows for the Clémence Fouquet WordPress theme.

## Quick Reference

| Section | Purpose |
|---------|---------|
| [Build Tools](#1-build-tools) | Linting setup |
| [CSS Architecture](#2-css-architecture) | @layer and tokens |
| [Git Workflows](#3-git-workflows) | Sync and deploy |

**Resources**: [linter-configs.md](references/linter-configs.md) | [git-workflows.md](references/git-workflows.md)

---

# 1. Build Tools

## Stack

| Outil | Usage |
|-------|-------|
| `@wordpress/scripts` | Build JS/CSS |
| `Stylelint` | Lint CSS |
| `ESLint` | Lint JS |
| `PHPCS` | Lint PHP |

## Installation rapide

```bash
npm init -y
npm install --save-dev @wordpress/scripts stylelint stylelint-config-standard @wordpress/eslint-plugin

composer require --dev squizlabs/php_codesniffer wp-coding-standards/wpcs
```

## Commandes

```bash
npm run lint          # Lint tout
npm run lint:css:fix  # Fix CSS
npm run build         # Production
```

> Configs complètes: [references/linter-configs.md](references/linter-configs.md)

---

# 2. CSS Architecture

## Règles NON NÉGOCIABLES

| Règle | Interdit | Correct |
|-------|----------|---------|
| !important | `color: red !important` | Augmenter spécificité |
| ID selectors | `#header` | `.l-header` |
| Hardcoded values | `#5b2e7f` | `var(--wp--preset--color--violet-500)` |
| Deep nesting | `.a .b .c .d` | `.l-a__d` (max 2 niveaux) |

## CSS Layers

```css
@layer reset, base, blocks, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
}

@layer components {
  .l-header { backdrop-filter: blur(10px); }
}
```

| Layer | Contenu |
|-------|---------|
| `reset` | Box-sizing, normalize |
| `base` | Styles HTML elements |
| `blocks` | Blocs Gutenberg custom |
| `components` | `.l-header`, `.c-card` |
| `utilities` | `.u-hidden`, `.u-flex` |

## WordPress Overrides (CRITIQUE)

**CSS hors @layer bat TOUJOURS CSS dans @layer**. WordPress génère CSS sans @layer.

```css
/* HORS @layer - pour battre WordPress */
body .alignfull,
html body .alignfull {
  max-width: none;
  width: 100vw;
}

/* DANS @layer - nos styles custom */
@layer components {
  .l-header { /* ... */ }
}
```

```php
// Priorité 20 pour charger après WordPress (défaut 10)
add_action('wp_enqueue_scripts', 'clemence_enqueue_assets', 20);
```

## Tokens theme.json

```css
/* Couleurs */
var(--wp--preset--color--violet-500)    /* #5b2e7f */
var(--wp--preset--color--orange-500)    /* #f89420 */

/* Espacements */
var(--wp--preset--spacing--50)          /* 24px */
var(--wp--preset--spacing--70)          /* 48px */

/* Typo */
var(--wp--preset--font-family--fraunces)
var(--wp--preset--font-size--large)
```

## Commandes utiles

```bash
grep -rn '!important' assets/css/           # Trouver !important
grep -oE '#[0-9a-fA-F]{3,6}' assets/css/*.css | wc -l  # Compter couleurs hardcodées
```

---

# 3. Git Workflows

## Workflow: Local → Production

```
Laragon → Git commit → GitHub push → VPS deploy
```

### Quick deploy

```bash
# 1. Sync et commit
robocopy "$LOCAL_THEME" "$PROJECT_THEME" /MIR /XD .git
git add . && git commit -m "feat(header): update styles"
git push origin main

# 2. Deploy
tar -czf /tmp/theme.tar.gz . && scp /tmp/theme.tar.gz srv759970:/tmp/
ssh srv759970 "docker cp /tmp/theme.tar.gz wordpress-clemence:/tmp/ && \
  docker exec wordpress-clemence bash -c 'cd /var/www/html/wp-content/themes/clemence-theme && tar -xzf /tmp/theme.tar.gz'"
```

## Workflow: Production → Local (Sync Clémence)

```
VPS Gutenberg → Backup → Git commit → Laragon sync
```

### Quick sync

```bash
# 1. Backup obligatoire
ssh srv759970 "docker exec wordpress-clemence wp db export /tmp/backup.sql --allow-root"

# 2. Export thème
ssh srv759970 "docker exec wordpress-clemence tar -czf /tmp/theme.tar.gz -C /var/www/html/wp-content/themes clemence-theme"
scp srv759970:/tmp/theme.tar.gz ./backups/

# 3. Commit
git checkout -b content-sync/$(date +%Y%m%d)
git add . && git commit -m "sync: Import modifications Clémence"
```

> Workflows détaillés: [references/git-workflows.md](references/git-workflows.md)

## Commit format

```
feat(header): réduire espacement logo-navigation

- Gap réduit de 2rem à 1rem
- Test mobile OK

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Types: `feat`, `fix`, `refactor`, `style`, `sync`
Scopes: `header`, `footer`, `hero`, `css`, `deploy`

---

# Skill Chaining

## Input Expected
- Projet WordPress theme FSE
- Accès SSH au VPS (srv759970)
- Node.js et Composer installés

## Output Produced
- Configs linters prêtes (`.stylelintrc.json`, etc.)
- Architecture CSS avec @layer
- Workflows Git configurés

## Skills Required Before
- Aucun (skill de setup)

## Compatible Skills After
- **julien-clemence-wordpress-contracts**: Utilise les tokens et conventions CSS
- **julien-clemence-wordpress-remote**: Utilise les workflows de déploiement

## Tools Used
- `Read` - Lire configs existantes
- `Write` - Créer configs linters
- `Edit` - Modifier package.json, functions.php
- `Bash` - npm install, git commands
- `Grep` - Rechercher !important, couleurs hardcodées
- `Glob` - Trouver fichiers CSS/JS
