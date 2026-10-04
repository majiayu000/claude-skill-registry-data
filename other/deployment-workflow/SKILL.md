---
name: Deployment Workflow
description: Use when deploying WordPress themes to skyyrose.co, verifying deployments, checking CSP headers, validating console errors, or performing rollbacks. Triggers on keywords like "deploy", "upload", "production", "staging", "rollback", "verify deployment".
version: 1.0.0
---

# Deployment Workflow

Expert guidance for deploying WordPress themes to skyyrose.co (WordPress.com managed hosting) with comprehensive verification and rollback capabilities.

## When to Use This Skill

Apply when:
- Deploying theme updates to production
- Verifying deployment success
- Checking Content Security Policy headers
- Monitoring console errors post-deployment
- Performing rollbacks after failed deployments
- Creating deployment packages

## SkyyRose Deployment Configuration

```json
{
  "site": {
    "url": "https://skyyrose.co",
    "adminUrl": "https://wordpress.com",
    "theme": "skyyrose-2025",
    "themeDir": "/Users/coreyfoster/DevSkyy/wordpress-theme/skyyrose-2025"
  },
  "verification": {
    "cspRequirements": [
      "'unsafe-inline'",
      "stats.wp.com",
      "widgets.wp.com",
      "cdn.babylonjs.com",
      "cdn.jsdelivr.net",
      "cdn.elementor.com"
    ],
    "consoleErrorThreshold": 10,
    "performanceTargets": {
      "LCP": 2.5,
      "FID": 100,
      "CLS": 0.1
    }
  }
}
```

## Pre-Deployment Checklist

Before deploying, verify:

### 1. Theme File Integrity
```bash
# Check all required files present
required_files=(
  "style.css"
  "functions.php"
  "index.php"
  "header.php"
  "footer.php"
  "inc/security-hardening.php"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Missing required file: $file"
    exit 1
  fi
done
```

### 2. PHP Syntax Validation
```bash
# Validate all PHP files
find . -name "*.php" -exec php -l {} \; | grep -v "No syntax errors"
```

### 3. CSP Configuration Check
```php
// Verify inc/security-hardening.php contains:
// - 'unsafe-inline' for scripts and styles
// - Whitelisted WordPress.com domains
// - Whitelisted 3D library CDNs

grep -q "'unsafe-inline'" inc/security-hardening.php || echo "WARNING: Missing 'unsafe-inline'"
```

### 4. Asset Verification
```bash
# Verify self-hosted fonts are served — skyyrose.co self-hosts fonts (zero Google-Fonts CDN)
# (JS/CDN delivery is out of scope for this font check — the theme's enqueue is the source of truth for JS loading)
base="https://skyyrose.co/wp-content/themes/skyyrose-flagship/assets"
urls=(
  "$base/css/fonts.css"
  "$base/fonts/archivo-latin.woff2"
  "$base/fonts/hanken-grotesk-latin.woff2"
)

for url in "${urls[@]}"; do
  curl -sI "$url" 2>&1 | grep -q "200" || echo "ERROR: $url not accessible"
done
```

## Deployment Process

### Step 1: Create Deployment Package

```bash
#!/bin/bash
# scripts/create-deployment-package.sh

THEME_DIR="/Users/coreyfoster/DevSkyy/wordpress-theme/skyyrose-2025"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PACKAGE_NAME="skyyrose-2025-deploy-${TIMESTAMP}.zip"

cd "$THEME_DIR/.."

# Create ZIP excluding unnecessary files
zip -r "$PACKAGE_NAME" skyyrose-2025 \
  -x "*.DS_Store" \
  -x "*node_modules/*" \
  -x "*.git/*" \
  -x "*.backup" \
  -x "*_bak*" \
  -x "*.log"

echo "Deployment package created: $PACKAGE_NAME"
echo "Size: $(du -h $PACKAGE_NAME | cut -f1)"
```

### Step 2: Upload to WordPress.com

**Semi-Automated Process:**

1. **Open WordPress Admin:**
   ```bash
   open "https://wordpress.com/themes/skyyrose.co"
   ```

2. **User Actions:**
   - Click "Add New Theme"
   - Click "Upload Theme"
   - Select ZIP file: `skyyrose-2025-deploy-[timestamp].zip`
   - Click "Install Now"
   - **CRITICAL:** Click "Replace current with uploaded" (not "Activate as new theme")
   - Click "Activate"

3. **Clear Caches:**
   ```bash
   open "https://wordpress.com/settings/performance/skyyrose.co"
   # User clicks "Clear all caches"
   ```

### Step 3: Post-Deployment Verification

#### A. CSP Header Verification
```bash
# Check CSP headers match requirements
curl -I "https://skyyrose.co/?nocache=1" 2>&1 | grep "content-security-policy"

# Should contain:
# - script-src ... 'unsafe-inline' 'unsafe-eval'
# - style-src ... 'unsafe-inline'
# - Whitelisted domains (stats.wp.com, cdn.babylonjs.com, etc.)
```

#### B. Console Error Check
```javascript
// scripts/check-console-errors.js
const puppeteer = require('puppeteer');

async function checkConsoleErrors() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });

  await page.goto('https://skyyrose.co/?nocache=1', {
    waitUntil: 'networkidle2'
  });

  await page.waitForTimeout(5000);

  console.log(`Total console errors: ${errors.length}`);
  if (errors.length > 10) {
    console.log('WARNING: Excessive console errors detected');
    errors.slice(0, 10).forEach(err => console.log(`  - ${err}`));
  }

  await browser.close();
  return errors.length;
}

checkConsoleErrors();
```

#### C. CSS Loading Verification
```bash
# Verify style.css loads successfully
curl -I "https://skyyrose.co/wp-content/themes/skyyrose-flagship/style.css" 2>&1 | grep "200 OK"
```

#### D. Performance Check
```bash
# Run Lighthouse audit
npx lighthouse https://skyyrose.co \
  --only-categories=performance \
  --output=json \
  --output-path=./lighthouse-report.json \
  --chrome-flags="--headless"

# Check Core Web Vitals
cat lighthouse-report.json | jq '.audits."largest-contentful-paint".numericValue'
cat lighthouse-report.json | jq '.audits."first-input-delay".numericValue'
cat lighthouse-report.json | jq '.audits."cumulative-layout-shift".numericValue'
```

## Verification Criteria

### Success Indicators
- ✅ CSP headers include 'unsafe-inline' and whitelisted domains
- ✅ Console errors < 10 (down from 107+)
- ✅ All CSS/JS assets return 200 OK
- ✅ 3D scenes load without errors
- ✅ Elementor editor functional
- ✅ LCP < 2.5s, FID < 100ms, CLS < 0.1

### Failure Indicators
- ❌ Old CSP still present (nonce-based)
- ❌ Console errors > 50
- ❌ 404 errors on CSS/JS
- ❌ 3D scenes fail to render
- ❌ Elementor editor broken

## Rollback Procedure

If deployment fails verification:

### Option 1: WordPress.com Backup Restore
```bash
# Guide user to restore
open "https://wordpress.com/backup/skyyrose.co"

echo "
ROLLBACK STEPS:
1. Find today's backup (before deployment)
2. Click 'Restore'
3. Wait for restoration to complete
4. Verify site is back to previous state
"
```

### Option 2: Re-upload Previous Version
```bash
# Find previous deployment package
ls -lt ../skyyrose-2025-deploy-*.zip | head -2

# Upload the second most recent (previous version)
echo "Upload this file to rollback: [previous-version].zip"
open "https://wordpress.com/themes/skyyrose.co"
```

## Troubleshooting

### Issue: CSP Headers Not Updated

**Symptoms:**
- Old nonce-based CSP still present
- Console errors not reduced

**Solution:**
1. Verify theme file actually uploaded (check file modification date)
2. Deactivate theme, activate Twenty Twenty-Four, then reactivate SkyyRose 2025
3. Clear WordPress.com Batcache (wait 5-10 minutes)
4. Try adding `?nocache=1` to URL

### Issue: Console Errors Not Reduced

**Symptoms:**
- Still seeing 100+ console errors
- CSP violations persist

**Solution:**
1. Check CSP headers with curl
2. Verify `inc/security-hardening.php` contains updated CSP
3. Hard refresh browser (Cmd+Shift+R)
4. Test in incognito window
5. Check browser console for specific blocked resources

### Issue: CSS Not Loading

**Symptoms:**
- Site appears unstyled
- Plain HTML with no formatting

**Solution:**
1. Check `style.css` returns 200 OK
2. Verify CSP allows `style-src 'self'`
3. Clear all caches (WordPress.com + browser)
4. Check for PHP fatal errors in theme files

## WordPress.com Specific Considerations

### Batcache (Edge Cache)
- WordPress.com uses aggressive edge caching
- Headers may be cached for 5-10 minutes
- Use `?nocache=1` parameter to bypass
- Clear cache via Performance settings

### Session Management
- WordPress.com manages sessions at platform level
- Do not implement custom session handling
- Avoid `session_start()` in theme code

### File Permissions
- No FTP/SSH access
- All changes via WordPress.com admin UI
- Cannot edit files directly on server

### CDN Requirements
- External resources must use HTTPS
- CDN URLs must be whitelisted in CSP
- Test CDN availability before deployment

## Deployment Frequency

**Recommended schedule:**
- **Major updates:** Weekly (Mondays, off-peak hours)
- **Bug fixes:** As needed (test in staging first)
- **Security patches:** Immediately
- **Performance optimizations:** Bi-weekly

## Monitoring Post-Deployment

**First 24 hours:**
- Monitor error logs
- Check Analytics for traffic drops
- Watch user feedback channels
- Verify Core Web Vitals in Search Console

**First week:**
- Review conversion rates
- Check bounce rates
- Monitor page load times
- Verify Elementor widgets functioning

## References

See `references/` directory for:
- `wordpress-com-deployment.md` - WordPress.com specific guidance
- `csp-verification.md` - CSP header validation
- `rollback-procedures.md` - Detailed rollback steps

## Examples

See `examples/` directory for:
- `deployment-script.sh` - Complete deployment automation
- `verify-deployment.js` - Post-deployment verification
- `rollback.sh` - Automated rollback procedure

## Scripts

See `scripts/` directory for:
- `create-deployment-package.sh` - Build deployment ZIP
- `verify-deployment.sh` - Post-deployment checks
- `check-csp-headers.sh` - CSP validation
- `rollback.sh` - Rollback to previous version
