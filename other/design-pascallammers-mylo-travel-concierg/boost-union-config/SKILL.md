---
name: boost-union-config
description: Configure Moodle Boost Union theme settings and customizations. Use when theming Moodle, configuring layouts, or customizing Boost Union features.
allowed-tools: Read, Write, Grep, Glob
---

# Boost Union Configuration Skill

Configure Boost Union theme settings and grandchild theme development.

## Trigger
- Moodle theme configuration requests
- SCSS customization in theme_cloodle
- Boost Union Flavours or Smart Menus setup

## Server Paths
- **Theme location**: `/opt/cloodle/apps/moodle/public/theme/cloodle/`
- **Boost Union**: `/opt/cloodle/apps/moodle/public/theme/boost_union/`
- **Container**: `docker exec cloodle-dev`

## Actions

### 1. Edit SCSS Variables
Modify `/theme/cloodle/scss/pre.scss` for Bootstrap variable overrides:
```scss
$primary: #6e66cc;
$body-color: #423653;
$font-family-sans-serif: "Outfit", sans-serif;
```

### 2. Add Component Styles
Modify `/theme/cloodle/scss/post.scss` for component refinements:
```scss
.btn-primary {
    border-radius: 500px;
}
```

### 3. Purge Theme Cache
```bash
docker exec cloodle-dev php /workspace/apps/moodle/admin/cli/purge_caches.php
```

## Key Files
| File | Purpose |
|------|---------|
| `version.php` | Theme identification |
| `config.php` | SCSS callbacks |
| `lib.php` | SCSS content functions |
| `scss/pre.scss` | Bootstrap overrides |
| `scss/post.scss` | Component styles |
