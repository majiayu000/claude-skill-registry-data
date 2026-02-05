---
name: github-pages-deploy
description: |
  Deploy Docusaurus static site to GitHub Pages for automated CI/CD pipeline.
  Bundled resources: GitHub Actions workflow, docusaurus.config.js deployment block, homepage redirect, i18n scaffolding.
  Use when setting up new Docusaurus project, adding CI/CD, or migrating to automated deployment.
version: 1.3.0
inputs:
  organization:
    description: GitHub username or organization
    required: true
    example: my-org
  repository:
    description: Repository name
    required: true
    example: my-docs
  default_branch:
    description: Default branch name (main or master) - MUST match your repo's default branch
    required: false
    default: "main"
    example: "master"
  node_version:
    description: Node.js version for build (20+ required for Docusaurus 3.9+)
    required: false
    default: "20"
  locales:
    description: Locales to build (comma-separated or "all")
    required: false
    default: "all"
    example: "en,ur"
---

# GitHub Pages Deploy

## Quick Setup

Run this command from your project root to set up deployment:

```bash
# Create workflow directory
mkdir -p .github/workflows

# Create deploy.yml (Node.js 20 required for Docusaurus 3.9+)
# ⚠️ IMPORTANT: Change 'main' to 'master' if your repo uses master branch!
# Check with: git branch --show-current
cat << 'EOF' > .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]  # ⚠️ Change to [master] if your repo uses master branch
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build website (all locales)
        run: npm run build
        env:
          NODE_OPTIONS: --max-old-space-size=4096

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF

echo "✅ Created .github/workflows/deploy.yml"

# Create homepage redirect with useBaseUrl (prevents double-slash 404s)
mkdir -p src/pages
cat << 'EOF' > src/pages/index.js
import React from 'react';
import {Redirect} from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function Home() {
  return <Redirect to={useBaseUrl('/docs')} />;
}
EOF

echo "✅ Created src/pages/index.js (homepage redirect)"

# Create i18n scaffolding for Urdu locale
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current
mkdir -p i18n/ur/docusaurus-theme-classic

cat << 'EOF' > i18n/ur/docusaurus-theme-classic/navbar.json
{
  "title": {
    "message": "عنوان",
    "description": "The title in the navbar"
  }
}
EOF

cat << 'EOF' > i18n/ur/docusaurus-theme-classic/footer.json
{
  "copyright": {
    "message": "کاپی رائٹ © 2025",
    "description": "The footer copyright"
  }
}
EOF

cat << 'EOF' > i18n/ur/code.json
{
  "theme.docs.paginator.previous": {
    "message": "پچھلا",
    "description": "The label used to navigate to the previous doc"
  },
  "theme.docs.paginator.next": {
    "message": "اگلا",
    "description": "The label used to navigate to the next doc"
  }
}
EOF

cat << 'EOF' > i18n/ur/docusaurus-plugin-content-docs/current/intro.md
---
sidebar_position: 1
---

# خوش آمدید

یہ اردو ترجمہ ہے۔
EOF

echo "✅ Created i18n/ur/ scaffolding (Urdu locale)"
echo ""
echo "📝 Now update docusaurus.config.js with your organization and repository names"
echo "⚠️  CRITICAL: baseUrl MUST have BOTH leading AND trailing slashes: '/<repo>/'"
```

## Bundled Resources

### 1. GitHub Actions Workflow (with i18n support)

**File**: `.github/workflows/deploy.yml`

> **⚠️ CRITICAL:** The `branches` value MUST match your repository's default branch. Use `[main]` for repos with main branch, `[master]` for repos with master branch. Mismatch = workflow never triggers!

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]  # ⚠️ Change to [master] if your repo uses master branch
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20  # Required: Docusaurus 3.9+ dropped Node 18 support
          cache: npm

      - name: Install dependencies
        run: npm ci

      # Builds all configured locales (en, ur, etc.)
      # Docusaurus automatically builds all locales defined in docusaurus.config.js
      - name: Build website (all locales)
        run: npm run build
        env:
          NODE_OPTIONS: --max-old-space-size=4096  # Required for i18n/multi-locale builds

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**i18n Notes**:
- Docusaurus builds ALL locales defined in `docusaurus.config.js` by default
- To build specific locale only: `npm run build -- --locale en`
- To build multiple: `npm run build -- --locale en --locale ur`
- `NODE_OPTIONS` increases memory for multi-locale builds (essential for Urdu/RTL)

### 2. Docusaurus Configuration Block

**File**: `docusaurus.config.js` (merge into existing config)

```javascript
const config = {
  // ===========================================
  // GitHub Pages Deployment Configuration
  // ===========================================

  // Replace <organization> with your GitHub username or org name
  url: 'https://<organization>.github.io',

  // ⚠️ CRITICAL: baseUrl MUST have BOTH leading AND trailing slashes!
  // ✅ Correct: '/<repository>/'
  // ❌ Wrong:   '<repository>/'   (missing leading slash → 404 errors)
  // ❌ Wrong:   '/<repository>'   (missing trailing slash → 404 errors)
  // ❌ Wrong:   'repository'      (missing both → 404 errors)
  baseUrl: '/<repository>/',

  // GitHub Pages deployment settings
  organizationName: '<organization>', // GitHub org/user name
  projectName: '<repository>',        // Repository name
  trailingSlash: false,

  // Recommended: Fail build on broken links
  onBrokenLinks: 'throw',

  // Markdown configuration (Docusaurus v3.9+)
  // ⚠️ Use markdown.hooks, NOT root-level onBrokenMarkdownLinks
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // ===========================================
  // i18n Configuration (for multi-locale builds)
  // ===========================================
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
        htmlLang: 'ur-PK',
      },
    },
  },

  // ... rest of your config
};

module.exports = config;
```

### 3. Homepage Redirect

**File**: `src/pages/index.js`

```javascript
import React from 'react';
import {Redirect} from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function Home() {
  return <Redirect to={useBaseUrl('/docs')} />;
}
```

> **⚠️ Important:** Always use `useBaseUrl()` for redirects to prevent double-slash issues with baseUrl.

### 4. RTL Support CSS

**File**: `src/css/custom.css` (add to existing)

```css
/* RTL Support for Urdu */
[dir='rtl'] {
  text-align: right;
}

[dir='rtl'] .navbar__items {
  flex-direction: row-reverse;
}

[dir='rtl'] .pagination-nav {
  flex-direction: row-reverse;
}

/* Code blocks stay LTR */
[dir='rtl'] pre,
[dir='rtl'] code {
  direction: ltr;
  text-align: left;
}
```

### 5. Input Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| `organization` | Yes | - | GitHub username or org | `my-org` |
| `repository` | Yes | - | Repository name | `my-docs` |
| `default_branch` | No | `main` | Default branch (main or master) | `master` |
| `node_version` | No | `20` | Node.js version (20+ required) | `20` |
| `locales` | No | `all` | Locales to build | `en,ur` |

## Usage Instructions

### Step 1: Run Quick Setup

```bash
# Option A: Run the quick setup script above
# Option B: Manually create files from Bundled Resources section
```

### Step 2: Update Docusaurus Config

Replace placeholders in `docusaurus.config.js`:

```javascript
// Before
url: 'https://<organization>.github.io',
baseUrl: '/<repository>/',
organizationName: '<organization>',
projectName: '<repository>',

// After (example)
url: 'https://my-org.github.io',
baseUrl: '/physical-ai-book/',  // ⚠️ MUST have both slashes!
organizationName: 'my-org',
projectName: 'physical-ai-book',
```

### Step 3: Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment", select **Source**: `GitHub Actions`
3. Save changes

### Step 4: Push and Deploy

```bash
git add .
git commit -m "feat: add GitHub Pages deployment with i18n support"
git push origin main
```

The workflow will automatically build all locales and deploy.

## Verification Checklist

- [ ] `.github/workflows/deploy.yml` exists with `node-version: 20`
- [ ] `.github/workflows/deploy.yml` `branches:` matches your default branch (main OR master)
- [ ] `.github/workflows/deploy.yml` has `NODE_OPTIONS: --max-old-space-size=4096`
- [ ] `docusaurus.config.js` has correct `url`, `baseUrl`, `organizationName`, `projectName`
- [ ] `baseUrl` has BOTH leading AND trailing slashes: `'/<repo>/'`
- [ ] `src/pages/index.js` uses `useBaseUrl()` for redirect (not hardcoded path)
- [ ] `markdown.hooks.onBrokenMarkdownLinks` (not root-level config)
- [ ] `docusaurus.config.js` has `i18n` config with all locales
- [ ] `i18n/ur/` directory exists with translated content
- [ ] GitHub Pages is enabled in repository settings
- [ ] Source is set to "GitHub Actions"
- [ ] First deployment completed successfully
- [ ] English site accessible at `https://<org>.github.io/<repo>/`
- [ ] Urdu site accessible at `https://<org>.github.io/<repo>/ur/`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Workflow never runs** | Check `branches: [main]` matches your default branch. Use `[master]` if repo uses master. Run `git branch --show-current` to verify |
| **Build fails on Node version** | Ensure `node-version: 20` in deploy.yml (Docusaurus 3.9+ dropped Node 18 support) |
| **404 on all pages** | Check `baseUrl` has BOTH leading AND trailing slashes: `'/<repo>/'` |
| **404 on homepage** | Create `src/pages/index.js` with redirect using `useBaseUrl()` |
| **Double slashes in URL** | Use `useBaseUrl()` hook, not hardcoded paths like `/docs/intro` |
| **404 on /ur/ locale** | Create `i18n/ur/` folder with translated docs and theme files |
| **Deprecation warnings** | Move `onBrokenMarkdownLinks` to `markdown.hooks` (not root config) |
| **Memory errors (i18n builds)** | Set `NODE_OPTIONS=--max-old-space-size=4096` (essential for multi-locale) |
| **Old content after push** | Workflow triggered on wrong branch. Verify `branches:` in deploy.yml matches your default branch |

### Build Fails

```bash
# Test build locally first
npm run build

# If memory error, increase heap size
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### i18n Build Issues

```bash
# Build specific locale only (for debugging)
npm run build -- --locale en

# Check locale directory exists
ls -la i18n/ur/
```

### Urdu/RTL Not Rendering

- Verify `direction: 'rtl'` in locale config
- Check font imports in `src/css/custom.css`
- Ensure `i18n/ur/` directory has translated content

## Requirements

- **Node.js 20+** (required - Docusaurus 3.9+ dropped Node 18 support)
- Docusaurus 3.9+
- GitHub repository with Pages enabled

## Environment Variables

The workflow includes essential environment variables:

```yaml
env:
  NODE_OPTIONS: --max-old-space-size=4096  # Required for i18n/Urdu builds
```

This is critical for multi-locale builds which consume significantly more memory during compilation.

## Related

- [Docusaurus Deployment Docs](https://docusaurus.io/docs/deployment#deploying-to-github-pages)
- [Docusaurus i18n Docs](https://docusaurus.io/docs/i18n/introduction)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- ADR-001: Deployment Infrastructure Stack
- ADR-003: Translation & Internationalization Approach
