---
name: julien-wordpress-structure-validator
description: This skill validates WordPress FSE (Full Site Editing) theme structure including templates hierarchy, page associations, theme.json configuration, block styles, featured images usage, file permissions, and UpdraftPlus backup configuration. Use when auditing a WordPress site, after creating/modifying templates, before production deployment, or when troubleshooting backup issues.
triggers:
  - wordpress validation
  - validate wordpress
  - wordpress audit
  - wordpress fse
  - theme.json validation
  - wordpress templates
  - wp structure
  - updraftplus
  - wordpress backup
  - valider wordpress
  - audit wordpress
---

# WordPress Structure Validator

Comprehensive validation tool for WordPress Full Site Editing (FSE) themes.

## When to Use This Skill

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "WordPress Structure Validator" activated
```

Use this skill to validate WordPress site structure in these scenarios:

- After creating or modifying WordPress templates
- Before deploying to production
- When diagnosing structural issues
- During quality audits or code reviews
- After content migration
- When onboarding to an existing WordPress project

## What This Skill Validates

1. **Template Hierarchy**
   - Correct template naming conventions
   - Required templates present (index.html minimum)
   - Template associations with pages
   - Orphaned templates detection

2. **Theme Configuration**
   - theme.json syntax and structure
   - Color palette definitions
   - Typography settings
   - Spacing scale

3. **Block Styles**
   - Registered block styles in functions.php
   - CSS/inline-style definitions
   - Naming conventions
   - Unused styles detection

4. **Content Structure**
   - Featured images defined for all pages
   - Page associations with templates
   - Homepage configuration (front_page_id)
   - Template assignments via _wp_page_template metakey

5. **File Permissions** (Docker/VPS context)
   - Theme files owned by www-data:www-data
   - Correct permissions (644 for files, 755 for directories)
   - Writable uploads directory

6. **UpdraftPlus Backup Configuration**
   - Plugin installed and activated
   - FS_METHOD set to 'direct' in wp-config.php
   - Backup directory permissions (775, www-data:www-data)
   - Write access verification
   - Backup schedule configuration
   - Remote storage setup

## Validation Workflow

### Step 1: Template Validation

Run the template validator script:

```bash
bash scripts/validate_templates.sh <theme-path>
```

This checks:
- index.html presence (required)
- Template naming conventions (page-{slug}.html, single-{type}.html)
- WordPress block syntax (<!-- wp:... -->)
- Unclosed blocks

See `references/wordpress-template-hierarchy.md` for complete hierarchy documentation.

### Step 2: Theme.json Validation

Validate the theme configuration:

```bash
python scripts/check_theme_json.py <path/to/theme.json>
```

Validates:
- JSON syntax
- Required fields (version, settings)
- Color palette structure
- Typography definitions
- Spacing scale

### Step 3: Block Styles Validation

Check functions.php for registered block styles:

```bash
bash scripts/check_block_styles.sh <theme-path>
```

Detects:
- Registered block styles
- Inline CSS definitions
- Orphaned styles (registered but not used)
- Naming convention compliance

### Step 4: Content & Database Checks

For WordPress installations, verify page associations:

```bash
# Check pages without featured images
wp post list --post_type=page --format=json --allow-root | jq '.[] | select(.featured_image == null)'

# Check template assignments
wp db query "SELECT p.ID, p.post_title, pm.meta_value as template FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id AND pm.meta_key = '_wp_page_template' WHERE p.post_type = 'page' AND p.post_status = 'publish';" --allow-root
```

### Step 5: File Permissions Check (Docker)

For Docker/VPS deployments:

```bash
# Check theme files ownership
docker exec <container> ls -la /var/www/html/wp-content/themes/<theme-name>/

# Fix permissions if needed
docker exec <container> chown -R www-data:www-data /var/www/html/wp-content/themes/<theme-name>/
docker exec <container> find /var/www/html/wp-content/themes/<theme-name>/ -type f -exec chmod 644 {} \;
docker exec <container> find /var/www/html/wp-content/themes/<theme-name>/ -type d -exec chmod 755 {} \;
```

### Step 6: UpdraftPlus Backup Check

Validate backup plugin configuration:

```bash
bash scripts/check_updraftplus.sh <container-name>
```

Checks:
- UpdraftPlus installation and activation
- FS_METHOD configuration in wp-config.php
- Backup directory permissions
- Write access test
- Backup schedule and remote storage

**Common Issues Fixed**:
- Missing FS_METHOD → WordPress asks for FTP credentials
- Wrong permissions → Backups fail silently
- No remote storage → Backups lost if server fails

### Step 7: Generate Report

Use the report template to document findings:

```bash
cp assets/validation-report-template.md validation-report-$(date +%Y%m%d).md
# Edit with validation results
```

## Best Practices Checked

Refer to `references/fse-best-practices.md` for complete guidelines. Key checks include:

1. **Templates**
   - Homepage uses `front-page.html` or `page-{slug}.html` (not generic `page.html`)
   - Minimum required: `index.html` (fallback)
   - No Featured Image in homepage template if content already includes one

2. **Theme.json**
   - Valid JSON schema (WordPress version 2 or 3)
   - Complete color palette with semantic names
   - Contrast ratios meet WCAG AA (4.5:1 minimum)

3. **Block Styles**
   - Registered in functions.php with `register_block_style()`
   - Clear, semantic naming (e.g., 'violet-title', 'hero-section')
   - Inline styles for simple CSS, separate files for complex styles

4. **Content**
   - All pages have Featured Images (SEO/social sharing)
   - Homepage properly configured (Settings > Reading)
   - No orphaned pages or templates

5. **File Organization**
   - CSS in `assets/css/`
   - JavaScript in `assets/js/`
   - Templates in `templates/`
   - Template parts in `parts/`

## Common Issues & Fixes

### Issue: "index.html missing"
**Fix**: Create minimal fallback template:
```html
<!-- wp:template-part {"slug":"header"} /-->
<!-- wp:group {"tagName":"main"} -->
<main class="wp-block-group">
    <!-- wp:post-content /-->
</main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer"} /-->
```

### Issue: "theme.json invalid"
**Fix**: Validate JSON syntax with `jsonlint` or use WordPress schema validator.

### Issue: "Featured Image not set"
**Fix**:
```bash
# Set featured image for page
wp post meta update <page-id> _thumbnail_id <image-id> --allow-root
```

### Issue: "Permission denied on uploads"
**Fix**:
```bash
docker exec <container> chown -R www-data:www-data /var/www/html/wp-content/uploads/
docker exec <container> chmod -R 755 /var/www/html/wp-content/uploads/
```

## Output & Reporting

After validation, the skill generates a markdown report (`validation-report-YYYYMMDD.md`) containing:

- Summary of validations (passed/warnings/errors)
- Detailed findings by category
- List of templates found
- Recommendations for fixes
- Links to relevant documentation

See `assets/validation-report-template.md` for the report format.

## References

- `references/wordpress-template-hierarchy.md` - Complete WordPress template hierarchy
- `references/fse-best-practices.md` - FSE development best practices

## Scripts

- `scripts/validate_templates.sh` - Template structure validator
- `scripts/check_theme_json.py` - Theme.json validator
- `scripts/check_block_styles.sh` - Block styles analyzer
