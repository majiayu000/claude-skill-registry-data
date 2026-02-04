---
name: julien-clemence-wordpress-remote
description: Remote management for clemencefouquet.fr on Hostinger VPS. Covers site architecture, WP-CLI commands, and image uploads via Docker.
allowed-tools: Bash, Read, Grep
---

# WordPress Remote Management - clemencefouquet.fr

Remote management for the Clémence Fouquet WordPress site on Hostinger VPS via Docker.

## Quick Reference

| Section | Purpose |
|---------|---------|
| [Infrastructure](#infrastructure) | Server details |
| [WP-CLI](#wp-cli-quick-commands) | Common commands |
| [Image Upload](#image-upload) | Upload workflow |

**Resources**: [wpcli-commands.md](references/wpcli-commands.md) | [image-upload.md](references/image-upload.md)

---

# Infrastructure

| Component | Value |
|-----------|-------|
| Site | https://clemencefouquet.fr |
| Hosting | Hostinger VPS |
| IP | 69.62.108.82 |
| SSH Host | srv759970 |
| Container | wordpress-clemence |
| SSH User | automation |

## Site Structure

| Page | Slug | Template |
|------|------|----------|
| Accueil | `/` | `page-accueil.html` |
| Services | `/services` | `page.html` |
| À propos | `/a-propos` | `page.html` |
| Contact | `/contact` | `page.html` |
| Mentions légales | `/mentions-legales` | `page.html` |

## Theme Structure

```
clemence-theme/
├── style.css, functions.php, theme.json
├── templates/     # index.html, page.html, page-accueil.html
├── parts/         # header.html, footer.html
├── patterns/      # Block patterns
└── assets/        # css/, js/, svg/
```

---

# WP-CLI Quick Commands

## Configuration

```bash
SSH_HOST="srv759970"
CONTAINER="wordpress-clemence"
```

## Pattern

```bash
ssh $SSH_HOST "docker exec $CONTAINER wp <command> --allow-root"
```

## Essential Commands

```bash
# Pages
ssh $SSH_HOST "docker exec $CONTAINER wp post list --post_type=page --allow-root"
ssh $SSH_HOST "docker exec $CONTAINER wp post create --post_type=page --post_title='New' --post_status=publish --allow-root"

# Options
ssh $SSH_HOST "docker exec $CONTAINER wp option get siteurl --allow-root"

# Cache
ssh $SSH_HOST "docker exec $CONTAINER wp cache flush --allow-root"

# Plugins
ssh $SSH_HOST "docker exec $CONTAINER wp plugin update --all --allow-root"

# DB
ssh $SSH_HOST "docker exec $CONTAINER wp db export - --allow-root" > backup.sql
```

> Commandes complètes: [references/wpcli-commands.md](references/wpcli-commands.md)

---

# Image Upload

## Quick Upload

```bash
# 1. Upload
scp "./image.png" automation@69.62.108.82:/tmp/image.png

# 2. Copy with permissions
ssh automation@69.62.108.82 "
  YEAR=\$(date +%Y) && MONTH=\$(date +%m) && \
  docker exec wordpress-clemence mkdir -p /var/www/html/wp-content/uploads/\$YEAR/\$MONTH && \
  docker cp /tmp/image.png wordpress-clemence:/var/www/html/wp-content/uploads/\$YEAR/\$MONTH/ && \
  docker exec -u root wordpress-clemence chown www-data:www-data /var/www/html/wp-content/uploads/\$YEAR/\$MONTH/image.png
"
```

**IMPORTANT**: Utiliser `-u root` pour chown.

## MIME Types

| Extension | MIME Type |
|-----------|-----------|
| PNG | `image/png` |
| JPG | `image/jpeg` |
| SVG | `image/svg+xml` |
| WebP | `image/webp` |

> Workflow complet: [references/image-upload.md](references/image-upload.md)

---

# Troubleshooting

## Permission denied
```bash
ssh $SSH_HOST "docker exec $CONTAINER chown -R www-data:www-data /var/www/html/wp-content"
```

## WP-CLI timeout
```bash
ssh $SSH_HOST "docker exec -e WP_CLI_TIMEOUT=300 $CONTAINER wp ..."
```

## Image not in media library
Execute database registration steps in [references/image-upload.md](references/image-upload.md#step-4-register-in-media-library)

---

# Skill Chaining

## Input Expected
- Accès SSH au VPS (srv759970)
- Container Docker wordpress-clemence running
- Credentials dans `.env` (pour uploads DB)

## Output Produced
- Pages/posts créés/modifiés
- Images uploadées
- Options WordPress mises à jour
- Backups SQL

## Skills Required Before
- **julien-clemence-wordpress-tooling**: Pour workflows Git/deploy

## Compatible Skills After
- **julien-clemence-wordpress-contracts**: Pour créer du contenu conforme
- **julien-wordpress-structure-validator**: Pour valider le thème

## Tools Used
- `Bash` - SSH commands, docker exec, scp
- `Read` - Lire configs, .env
- `Grep` - Rechercher dans logs/output
