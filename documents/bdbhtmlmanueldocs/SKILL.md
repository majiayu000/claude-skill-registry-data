---
name: bdbhtmlmanueldocs
description: Use when authoritative design system, standalone HTML template, and automated GitHub Pages live hosting workflow for creating neutral, enterprise-grade developer documentation and user manuals in the official Google Antigravity / BDB OS aesthetic ...
category: bdb-core
risk: safe
date_added: "2026-08-18"
---

# 🌐 BDB HTML Manual & Live Documentation System (`bdbhtmlmanueldocs`)

This skill codifies the complete specification for building and deploying **neutral, enterprise-grade developer documentation and bilingual user manuals** in the official Google Antigravity / BDB OS aesthetic, complete with automated GitHub Pages live hosting.

---

## 🎯 Core Design Philosophy (Anti-Slop & Neutrality)

1. **Restrained, Professional Aesthetic:**
   - Deep matte charcoal surfaces (`#0f1117`, `#161922`) with subtle crisp borders (`#232733`).
   - High-contrast neutral typography (`#f0f3f6` headers, `#9aa1b2` body).
   - Zero loud rainbow gradients or toy-like cartoon icons.
2. **3-Column Doc Architecture:**
   - **Left Sidebar (260px):** Sticky navigation tree with version badges (`v1.1.0`) and soft pill active highlights.
   - **Center Main (860px max):** Breadcrumbs navigation, title lead, neutral platform tables with action pills (`.pill-btn`), interactive pre-flight checklists, and syntax-highlighted copyable terminal blocks.
   - **Right Sidebar (220px):** "On this page" dynamic Table of Contents tracking active scroll position in real-time.
3. **Zero External Dependencies:**
   - 100% self-contained single-file HTML5 with inlined CSS, vector SVGs, and lightweight vanilla JS.
   - 100% offline-ready, instant load, zero CDN failure risk.
4. **Bilingual Parity (DE / EN):**
   - Native segmented toggle (`DE / EN`) with instant content morphing and `localStorage` persistence.

---

## ⚡ The Live Documentation GitHub Hosting Trick (CI/CD Recipe)

Follow this exact procedure to host any documentation live at `https://<owner>.github.io/<repo>/` in under 60 seconds with automated push-to-deploy:

### 1. Workspace Directory Setup
Place the documentation files at the root of the `docs/` folder:
```bash
docs/
├── index.html          # Main standalone bilingual manual (or symlink)
├── .nojekyll           # Bypasses Jekyll processing to serve raw HTML/CSS assets
└── ...
```

### 2. GitHub Actions Deployment Workflow
Create `.github/workflows/deploy-docs.yml`:
```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - '.github/workflows/deploy-docs.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'docs/'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3. Switch GitHub Pages Build Type via CLI (One-Liner)
To activate GitHub Actions-based Pages deployment programmatically without opening the browser:
```bash
gh api -X PUT repos/<owner>/<repo>/pages -f build_type=workflow
```

### 4. Trigger & Verify Live URL
```bash
gh workflow run deploy-docs.yml
gh run watch --exit-status
```
The documentation is now live at `https://<owner>.github.io/<repo>/`.

### 5. README.md Badge & Header Link
Add the live documentation badge and banner to the top of `README.md`:
```markdown
[![Documentation](https://img.shields.io/badge/Docs-Live%20Manual-blue?style=flat-square&logo=github)](https://<owner>.github.io/<repo>/)

> 🌐 **Live User Manual & Interactive Guide:** [https://<owner>.github.io/<repo>/](https://<owner>.github.io/<repo>/)
```

---

## 🎨 DTCG Design Tokens

```css
:root {
  /* Layout */
  --header-height: 60px;
  --sidebar-left-width: 260px;
  --sidebar-right-width: 220px;
  --content-max-width: 860px;

  /* Matte Dark Theme */
  --bg-header: #0f1117;
  --bg-body: #0f1117;
  --bg-sidebar: #0f1117;
  --bg-surface: #161922;
  --bg-surface-elevated: #1e222d;
  --bg-card: #161922;
  --bg-table-header: #1c202a;
  
  --border-subtle: #232733;
  --border-strong: #323847;
  
  --text-primary: #f0f3f6;
  --text-secondary: #9aa1b2;
  --text-muted: #656d81;
  --text-link: #58a6ff;
  
  --accent-blue: #3b82f6;
  --accent-blue-subtle: rgba(59, 130, 246, 0.12);
  --accent-pill: #252b38;
  --accent-pill-hover: #32394a;
  
  --success: #3fb950;
  --warning: #d29922;
  --danger: #f85149;
  
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Google Sans", Inter, Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

[data-theme="light"] {
  --bg-header: #ffffff;
  --bg-body: #ffffff;
  --bg-sidebar: #f8fafc;
  --bg-surface: #f1f5f9;
  --bg-surface-elevated: #e2e8f0;
  --bg-card: #ffffff;
  --bg-table-header: #f8fafc;
  --border-subtle: #e2e8f0;
  --border-strong: #cbd5e1;
  
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-link: #2563eb;
  
  --accent-blue: #2563eb;
  --accent-blue-subtle: rgba(37, 99, 235, 0.08);
  --accent-pill: #e2e8f0;
  --accent-pill-hover: #cbd5e1;
}
```

---

## 📁 Turnkey Template Location

Agents can read and duplicate the full standalone template file:
- `~/.agents/skills/bdbhtmlmanueldocs/templates/docs_template.html`

## 1. Overview
This skill provides domain-specific logic and rules for its respective BDB pipeline component to ensure standardization across multi-agent workflows.

## 2. When to Use
- Use when specifically requested by the user or triggered by an orchestration agent.
- Use when the current task aligns with the skill's domain.
- Exclude when standard tool execution is sufficient.

## 3. Core Process
1. Read the provided context and ensure preconditions are met.
2. Run the required script or tool and confirm the state change.
3. Verify exit codes, file modifications, or DB counts to guarantee success before reporting completion.

## 4. Common Rationalizations
| Rationalization | Reality |
|---|---|
| "The code change was small, so I skipped updating OpenWiki docs." | Every state change must be reflected in the relevant system records. |
| "The ingest script exited without an error, so the memB index must be updated." | Silent failures happen; explicit verification of the side effect is mandatory. |
| "I'll let the /startcycle proceed without a defined rollback path." | Proceeding without a rollback path corrupts the workflow integrity and safety. |
| "I trust the cached agent registry instead of rescanning after a skill change." | Caches stale out quickly; explicit rescans prevent ghost failures. |

## 5. Red Flags
- Bypassing the verification step after a script execution.
- Proceeding to the next pipeline stage without confirming the previous stage's side effects.
- Ignoring domain-specific constraints listed in this skill.

## 6. Verification
- [ ] Verified script exit codes are explicitly checked.
- [ ] Confirmed target files or database records reflect the expected change.
- [ ] Ensured no silent failures were ignored before reporting success.
