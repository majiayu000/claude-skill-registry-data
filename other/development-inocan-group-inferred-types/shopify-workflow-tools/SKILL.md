---
name: Shopify Workflow & Tools
description: Shopify CLI commands, development workflow, and essential tools for theme development
---

# Shopify Workflow & Tools

## Shopify CLI Commands

### Initialize a New Theme
```bash
# Clone the Dawn reference theme
shopify theme init

# Clone a specific theme
shopify theme init --clone-url https://github.com/Shopify/dawn.git
```

### Development Server
```bash
# Start local development server with hot-reload
shopify theme dev --store=example.myshopify.com

# Development server options
shopify theme dev --store=example.myshopify.com --port=9293
shopify theme dev --store=example.myshopify.com --theme-editor-sync
```

**Features:**
- Hot-reload for CSS and sections
- Live preview at `http://127.0.0.1:9292`
- Syncs with theme editor changes
- Chrome browser recommended

### Push Theme to Shopify
```bash
# Push as unpublished theme (recommended first push)
shopify theme push --unpublished

# Push to specific theme
shopify theme push --theme=THEME_ID

# Push with development flag
shopify theme push --development
```

### Pull Theme from Shopify
```bash
# Pull published theme
shopify theme pull

# Pull specific theme
shopify theme pull --theme=THEME_ID

# Pull only specific files
shopify theme pull --only=templates/*.json,sections/*.liquid
```

### Publish Theme
```bash
# Publish theme
shopify theme publish --theme=THEME_ID

# List all themes
shopify theme list
```

### Delete Theme
```bash
shopify theme delete --theme=THEME_ID
```

### Check Theme for Issues
```bash
# Run theme check
shopify theme check

# Auto-fix issues
shopify theme check --auto-correct
```

## Development Workflow

### 1. Initial Setup
```bash
# Clone starter theme
shopify theme init

# Navigate to theme directory
cd your-theme-name

# Install dependencies (if using package.json)
npm install

# Start development
shopify theme dev --store=your-store.myshopify.com
```

### 2. Local Development
```bash
# Start dev server
shopify theme dev --store=example.myshopify.com

# Open browser to http://127.0.0.1:9292
# Make changes to Liquid, CSS, JavaScript
# See changes instantly (hot-reload for CSS/sections)
```

### 3. Testing & Validation
```bash
# Check for theme issues
shopify theme check

# Fix auto-fixable issues
shopify theme check --auto-correct
```

### 4. Deploy to Shopify
```bash
# First deployment (as unpublished)
shopify theme push --unpublished

# Or push to development theme
shopify theme push --development

# Verify in Shopify admin
# Theme Library > View theme
```

### 5. Publishing
```bash
# List themes to get THEME_ID
shopify theme list

# Publish theme
shopify theme publish --theme=THEME_ID
```

## Theme Check

Shopify's official linting tool for themes.

### Install
```bash
npm install -g @shopify/theme-check
```

### Usage
```bash
# Run checks
theme-check .

# Auto-fix issues
theme-check . --auto-correct

# Check specific files
theme-check sections/header.liquid
```

### Common Checks
- **Liquid syntax errors**
- **Performance issues**
- **Accessibility problems**
- **Deprecated tags/filters**
- **Missing translations**
- **Asset optimization**

### Integration with VS Code
Install the "Shopify Liquid" extension for:
- Real-time linting
- Syntax highlighting
- Autocomplete
- Hover documentation

## File Structure

### Required Files
```
your-theme/
├── config/
│   ├── settings_schema.json    # Global theme settings (required)
│   └── settings_data.json      # Theme setting values (auto-generated)
├── layout/
│   └── theme.liquid             # Base layout (required)
├── templates/
│   ├── index.json               # Homepage template (required)
│   ├── product.json             # Product page template
│   ├── collection.json          # Collection page template
│   └── 404.liquid               # 404 page
├── sections/
│   └── *.liquid                 # Reusable sections
├── snippets/
│   └── *.liquid                 # Reusable code fragments
├── assets/
│   └── *.*                      # CSS, JS, images, fonts
└── locales/
    └── en.default.json          # Default language (required)
```

## Environment Best Practices

### Development Stores
- Free for Partners
- Sandbox for testing
- No impact on production
- Can transfer to client

```bash
# Create development store
# Visit partners.shopify.com
# Stores > Add store > Development store
```

### Theme Environments
- **Development**: `shopify theme dev` or `--development` flag
- **Staging/Preview**: `--unpublished` flag
- **Production**: Published theme

### Version Control
```bash
# Initialize git
git init

# Add .gitignore
echo "config/settings_data.json" >> .gitignore
echo "node_modules/" >> .gitignore
echo ".DS_Store" >> .gitignore

# Commit theme
git add .
git commit -m "Initial theme commit"
```

**Important**: `.gitignore` should exclude:
- `config/settings_data.json` (store-specific)
- `node_modules/` (dependencies)
- `.DS_Store` (macOS files)

## Debugging Techniques

### Liquid Debugging
```liquid
{%- comment -%}
  Debug output using assign and display
{%- endcomment -%}

{%- assign debug = true -%}

{%- if debug -%}
  <pre>
    Product: {{ product | json }}
    Cart: {{ cart | json }}
  </pre>
{%- endif -%}
```

### Console Logging
```liquid
{% javascript %}
  console.log('Product data:', {{ product | json }});
  console.log('Settings:', {{ section.settings | json }});
{% endjavascript %}
```

### Theme Check Output
```bash
# Verbose output
shopify theme check --verbose

# Output to file
shopify theme check > check-results.txt
```

## Performance Optimization

### Image Optimization
```liquid
{%- # Use appropriate image sizes -%}
<img
  srcset="
    {{ image | image_url: width: 400 }} 400w,
    {{ image | image_url: width: 800 }} 800w,
    {{ image | image_url: width: 1200 }} 1200w
  "
  sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
  src="{{ image | image_url: width: 800 }}"
  loading="lazy"
>
```

### Asset Loading
```liquid
{%- # Defer non-critical JavaScript -%}
<script src="{{ 'theme.js' | asset_url }}" defer></script>

{%- # Preload critical assets -%}
<link rel="preload" href="{{ 'theme.css' | asset_url }}" as="style">
```

### Minimize Liquid Logic
```liquid
{%- # Good - assign complex logic to variable -%}
{%- liquid
  assign is_on_sale = false
  if product.compare_at_price > product.price
    assign is_on_sale = true
  endif
-%}

{%- if is_on_sale -%}
  <span>On Sale</span>
{%- endif -%}

{%- # Bad - inline complex logic -%}
{% if product.compare_at_price > product.price %}
  <span>On Sale</span>
{% endif %}
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy Theme

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Shopify CLI
        run: npm install -g @shopify/cli @shopify/theme
      - name: Push theme
        run: shopify theme push --development
        env:
          SHOPIFY_CLI_THEME_TOKEN: ${{ secrets.SHOPIFY_CLI_THEME_TOKEN }}
```

## Common Commands Reference

```bash
# Authentication
shopify auth login

# Theme commands
shopify theme list                    # List all themes
shopify theme info                    # Show theme info
shopify theme dev                     # Start dev server
shopify theme push                    # Push theme
shopify theme pull                    # Pull theme
shopify theme publish                 # Publish theme
shopify theme delete                  # Delete theme
shopify theme check                   # Check theme for issues
shopify theme package                 # Package theme as .zip

# Theme check
theme-check .                         # Run checks
theme-check . --auto-correct          # Fix issues
theme-check . --config=.theme-check.yml  # Use custom config

# Help
shopify theme --help                  # Show help
shopify theme dev --help              # Show dev command help
```

## Troubleshooting

### Development Server Not Starting
```bash
# Check if port is in use
lsof -i :9292

# Use different port
shopify theme dev --port=9293
```

### Authentication Issues
```bash
# Re-authenticate
shopify auth logout
shopify auth login
```

### Theme Push Conflicts
```bash
# Force push (caution: overwrites remote)
shopify theme push --force

# Pull first, then push
shopify theme pull
shopify theme push
```

### Hot Reload Not Working
- Ensure using Chrome browser
- Check file paths are correct
- Restart dev server
- Clear browser cache

## Best Practices

1. **Use development stores** for testing
2. **Push unpublished first** before publishing
3. **Run theme check** before deploying
4. **Use version control** (Git)
5. **Exclude settings_data.json** from Git
6. **Test on multiple devices** before publishing
7. **Keep CLI updated**: `npm update -g @shopify/cli`
8. **Use theme editor sync** during development
9. **Document custom features** in README
10. **Follow Shopify theme requirements** for Theme Store

Use these tools and workflows to build, test, and deploy Shopify themes efficiently.
