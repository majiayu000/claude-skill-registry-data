---
name: Infrastructure
description: This skill activates when users discuss WordPress.com platform specifics, hosting differences, deployment workflows, server configuration, or infrastructure decisions. Provides guidance on WordPress.com vs self-hosted infrastructure and platform-specific patterns.
---

# WordPress Infrastructure

Navigate WordPress.com platform specifics, hosting options, and deployment workflows.

## When This Activates

- "WordPress.com", "self-hosted", "hosting", "deployment"
- "SFTP", "SSH", "platform restrictions", "CDN"
- "staging", "production", "environment", "server"
- User asks about WordPress hosting differences
- Discussing infrastructure or deployment

---

## WordPress.com vs Self-Hosted

### Feature Comparison

| Feature | WordPress.com | Self-Hosted |
|---------|---------------|-------------|
| **Root Access** | ❌ No | ✅ Yes |
| **SSH/SFTP** | ⚠️ SFTP only | ✅ Full SSH |
| **Plugin Install** | ⚠️ Limited (Business+) | ✅ Any plugin |
| **Theme Upload** | ✅ Yes (Premium+) | ✅ Yes |
| **Server Config** | ❌ No control | ✅ Full control |
| **.htaccess** | ❌ No access | ✅ Yes |
| **wp-config.php** | ⚠️ Platform managed | ✅ Full control |
| **CDN** | ✅ Built-in | ⚠️ Configure manually |
| **Security** | ✅ Platform managed | ⚠️ Your responsibility |
| **Updates** | ✅ Automatic | ⚠️ Manual (or auto) |
| **CSP Headers** | ❌ Platform controlled | ✅ Full control |
| **Cost** | $25+/mo | $5-50/mo |

### When to Choose Which

**WordPress.com** (Managed):
- Simple blogs, portfolios
- No technical team
- Want automatic updates/security
- Standard WordPress features sufficient

**Self-Hosted**:
- Need custom plugins/themes
- Require server-level control
- Advanced features (3D, custom CDNs)
- Full CSP/header control

**SkyyRose Reality**: Requires self-hosted for 3D viewers, custom CSP

---

## WordPress.com Platform Specifics

### REST API Access

```javascript
// WordPress.com uses different API URL pattern
// NOT /wp-json/, USE index.php?rest_route=

const WP_COM_API_BASE = 'https://skyyrose.co/index.php?rest_route=';

// Fetch posts
const response = await fetch(`${WP_COM_API_BASE}/wp/v2/posts`);

// WooCommerce products
const products = await fetch(`${WP_COM_API_BASE}/wc/v3/products`, {
  headers: {
    'Authorization': `Basic ${btoa(`${consumerKey}:${consumerSecret}`)}`,
  },
});
```

### SFTP Deployment

```bash
# WordPress.com SFTP credentials
# Host: sftp.wp.com
# Port: 22
# Username: site.wordpress.com
# Password: (from hosting settings)

# Deploy using lftp
lftp -c "
set sftp:auto-confirm yes
open -u USERNAME,PASSWORD sftp://sftp.wp.com:22
mirror --reverse --delete --verbose \
  local-theme-dir/ \
  /htdocs/wp-content/themes/theme-name/
bye
"
```

### Platform Restrictions

```php
// ❌ Cannot modify on WordPress.com:
// - Nginx configuration
// - PHP settings (php.ini)
// - Server-level CSP headers
// - Database access (except via plugin)
// - Cron jobs (except WP-Cron)
// - Custom server software

// ✅ Can modify:
// - Theme files (via SFTP or upload)
// - Plugin files (Business+ plan)
// - wp-config.php constants (some)
// - Database via plugins (WP-CLI, Adminer)
```

### Cache Management

```javascript
// WordPress.com cache clearing
// No direct cache API, use query parameters

// Bust cache on specific URL
const url = 'https://skyyrose.co/products/?nocache=1';

// Or increment version parameter
const url = 'https://skyyrose.co/products/?v=' + Date.now();
```

---

## Self-Hosted WordPress Infrastructure

### Recommended Stack

**Option 1: Traditional (LAMP/LEMP)**
```
Linux (Ubuntu 22.04 LTS)
Nginx or Apache
MySQL 8.0 or MariaDB 10.6
PHP 8.1+ (with OPcache, APCu)
```

**Option 2: Modern (Containerized)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  wordpress:
    image: wordpress:6.4-php8.2-fpm-alpine
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: skyyrose
      WORDPRESS_DB_USER: skyy
      WORDPRESS_DB_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./wordpress:/var/www/html
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: skyyrose
      MYSQL_USER: skyy
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./wordpress:/var/www/html
    depends_on:
      - wordpress

volumes:
  db_data:
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name skyyrose.co;
    root /var/www/html;
    index index.php;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # CSP header (full control on self-hosted)
    add_header Content-Security-Policy "
        default-src 'self';
        script-src 'self' 'unsafe-inline' https://cdn.babylonjs.com https://cdn.jsdelivr.net;
        style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
        font-src 'self' data: https://fonts.gstatic.com;
        img-src 'self' data: https: blob:;
        connect-src 'self' https://api.skyyrose.co;
        frame-src 'self';
        object-src 'none';
    " always;

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;

    # PHP handling
    location ~ \.php$ {
        fastcgi_pass wordpress:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # Static assets cache
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Block access to sensitive files
    location ~ /\.(git|env|htaccess) {
        deny all;
    }
}
```

---

## Deployment Workflows

### CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Create theme ZIP
        run: |
          cd wordpress-theme/skyyrose-2025
          zip -r ../../skyyrose-2025.zip . \
            -x "*.git*" "node_modules/*" ".env*" "*.log"

      - name: Deploy via SFTP
        uses: SamKirkland/FTP-Deploy-Action@4.3.0
        with:
          server: ${{ secrets.SFTP_HOST }}
          username: ${{ secrets.SFTP_USERNAME }}
          password: ${{ secrets.SFTP_PASSWORD }}
          protocol: sftp
          port: 22
          local-dir: ./wordpress-theme/skyyrose-2025/
          server-dir: /htdocs/wp-content/themes/skyyrose-2025/

      - name: Clear Cache
        run: |
          curl -X PURGE "https://skyyrose.co/"
          curl -X PURGE "https://skyyrose.co/shop/"
```

### Manual Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

THEME_NAME="skyyrose-2025"
THEME_DIR="wordpress-theme/${THEME_NAME}"
DEPLOY_DIR="/tmp/${THEME_NAME}-deploy"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ZIP_NAME="${THEME_NAME}-${TIMESTAMP}.zip"

echo "=== WordPress Theme Deployment ==="
echo "Theme: ${THEME_NAME}"
echo "Timestamp: ${TIMESTAMP}"
echo

# 1. Clean previous build
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# 2. Copy theme files (exclude dev files)
echo "Copying theme files..."
rsync -av --progress \
  --exclude=".git*" \
  --exclude="node_modules" \
  --exclude=".env*" \
  --exclude="*.log" \
  --exclude="*.map" \
  "$THEME_DIR/" "$DEPLOY_DIR/"

# 3. Build assets
echo "Building assets..."
cd "$DEPLOY_DIR"
npm ci --production
npm run build

# 4. Remove dev dependencies
rm -rf node_modules package*.json

# 5. Create ZIP
echo "Creating deployment package..."
cd /tmp
zip -r "$ZIP_NAME" "$THEME_NAME"

# 6. Upload via SFTP
echo "Uploading to server..."
lftp -c "
set sftp:auto-confirm yes
open -u $SFTP_USER,$SFTP_PASS sftp://$SFTP_HOST:$SFTP_PORT
put -O /htdocs/wp-content/themes/ $ZIP_NAME
bye
"

# 7. Extract on server (requires WP-CLI or plugin)
echo "Extracting theme on server..."
# SSH command or REST API call to extract

echo "✅ Deployment complete!"
echo "ZIP: /tmp/$ZIP_NAME"
```

---

## Staging Environment

### Setup Staging Site

```bash
# 1. Clone production database
mysqldump -u prod_user -p prod_db > staging_backup.sql
mysql -u staging_user -p staging_db < staging_backup.sql

# 2. Update URLs in database
wp search-replace 'https://skyyrose.co' 'https://staging.skyyrose.co' --all-tables

# 3. Copy uploads directory
rsync -avz prod_server:/var/www/html/wp-content/uploads/ \
  staging_server:/var/www/html/wp-content/uploads/

# 4. Set staging constants
# In wp-config.php
define('WP_ENVIRONMENT_TYPE', 'staging');
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

### Prevent Indexing on Staging

```php
// functions.php
if (defined('WP_ENVIRONMENT_TYPE') && WP_ENVIRONMENT_TYPE === 'staging') {
    // Disable search engine indexing
    add_filter('pre_option_blog_public', '__return_zero');

    // Add noindex meta tag
    add_action('wp_head', function() {
        echo '<meta name="robots" content="noindex,nofollow">';
    }, 1);

    // Block search engines in robots.txt
    add_filter('robots_txt', function($output) {
        return "User-agent: *\nDisallow: /\n";
    });
}
```

---

## Environment Management

```php
// wp-config.php - Environment detection
if (file_exists(__DIR__ . '/.env')) {
    // Load environment-specific config
    $env = parse_ini_file(__DIR__ . '/.env');
    define('WP_ENVIRONMENT_TYPE', $env['ENVIRONMENT'] ?? 'production');
}

// Environment-specific settings
switch (WP_ENVIRONMENT_TYPE) {
    case 'local':
    case 'development':
        define('WP_DEBUG', true);
        define('WP_DEBUG_LOG', true);
        define('WP_DEBUG_DISPLAY', true);
        define('SCRIPT_DEBUG', true);
        break;

    case 'staging':
        define('WP_DEBUG', true);
        define('WP_DEBUG_LOG', true);
        define('WP_DEBUG_DISPLAY', false);
        break;

    case 'production':
        define('WP_DEBUG', false);
        define('WP_DEBUG_LOG', false);
        define('WP_DEBUG_DISPLAY', false);
        define('DISALLOW_FILE_EDIT', true);
        break;
}

// Environment-specific database
$db_config = [
    'local' => [
        'host' => 'localhost',
        'name' => 'skyyrose_local',
        'user' => 'root',
        'pass' => 'root',
    ],
    'staging' => [
        'host' => 'staging-db.skyyrose.co',
        'name' => 'skyyrose_staging',
        'user' => getenv('DB_USER'),
        'pass' => getenv('DB_PASSWORD'),
    ],
    'production' => [
        'host' => 'prod-db.skyyrose.co',
        'name' => 'skyyrose_prod',
        'user' => getenv('DB_USER'),
        'pass' => getenv('DB_PASSWORD'),
    ],
];

$db = $db_config[WP_ENVIRONMENT_TYPE] ?? $db_config['production'];

define('DB_NAME', $db['name']);
define('DB_USER', $db['user']);
define('DB_PASSWORD', $db['pass']);
define('DB_HOST', $db['host']);
```

---

## CDN Configuration

### Cloudflare Setup

```php
// Use Cloudflare for static assets
function skyyrose_cdn_url($url) {
    if (defined('WP_ENVIRONMENT_TYPE') && WP_ENVIRONMENT_TYPE === 'production') {
        $cdn_url = 'https://cdn.skyyrose.co';
        $site_url = 'https://skyyrose.co';

        // Only CDN for static assets
        if (preg_match('/\.(jpg|jpeg|png|gif|css|js|svg|woff2)$/', $url)) {
            return str_replace($site_url, $cdn_url, $url);
        }
    }

    return $url;
}
add_filter('wp_get_attachment_url', 'skyyrose_cdn_url');
add_filter('wp_get_attachment_image_src', 'skyyrose_cdn_url');
```

---

## Monitoring & Logging

```php
// Centralized error logging
function skyyrose_log_error($message, $context = []) {
    if (defined('WP_DEBUG_LOG') && WP_DEBUG_LOG) {
        $log_message = sprintf(
            '[%s] %s | Context: %s',
            date('Y-m-d H:i:s'),
            $message,
            wp_json_encode($context)
        );

        error_log($log_message);

        // Send to external monitoring (production only)
        if (WP_ENVIRONMENT_TYPE === 'production') {
            // Send to Sentry, LogRocket, etc.
        }
    }
}

// Use throughout theme/plugins
try {
    $result = risky_operation();
} catch (Exception $e) {
    skyyrose_log_error('Risky operation failed', [
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
    ]);
}
```

---

## Backup Strategy

```bash
# Automated daily backups
#!/bin/bash
# /etc/cron.daily/wordpress-backup

BACKUP_DIR="/backups/skyyrose"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RETENTION_DAYS=30

# 1. Database backup
mysqldump -u $DB_USER -p$DB_PASS skyyrose_prod | \
  gzip > "$BACKUP_DIR/db-$TIMESTAMP.sql.gz"

# 2. Files backup (wp-content only)
tar -czf "$BACKUP_DIR/files-$TIMESTAMP.tar.gz" \
  /var/www/html/wp-content/uploads \
  /var/www/html/wp-content/themes/skyyrose-2025

# 3. Upload to S3 (or similar)
aws s3 cp "$BACKUP_DIR/db-$TIMESTAMP.sql.gz" \
  s3://skyyrose-backups/database/

aws s3 cp "$BACKUP_DIR/files-$TIMESTAMP.tar.gz" \
  s3://skyyrose-backups/files/

# 4. Clean old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup complete: $TIMESTAMP"
```

---

## SkyyRose Infrastructure Decision

**Current**: WordPress.com (restricted)
**Required**: Self-hosted for:
- Custom CSP headers (3D CDNs)
- Server-level control
- Advanced Elementor features
- Full plugin flexibility

**Migration Path**: See `wordpress-theme/ACTUAL-FIX.md`

---

## When User Asks About Infrastructure

1. **Identify requirements**: What features needed?
2. **Platform choice**: WordPress.com vs self-hosted?
3. **Hosting recommendation**: Based on scale and budget
4. **Deployment workflow**: CI/CD vs manual?
5. **Environment setup**: Local, staging, production
6. **Monitoring**: Logging, backups, alerts

Always consider trade-offs: convenience vs. control, cost vs. features.
