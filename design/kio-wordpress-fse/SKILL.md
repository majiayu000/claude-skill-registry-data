---
name: kio-wordpress-fse
description: "Build WordPress Full Site Editing (FSE) block themes, native Gutenberg block patterns, and SSR custom blocks via the S0-S8 workflow. Use for Gutenberg block themes (not legacy classic themes like Flatsome)."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 1.1.0
---

# 🌐 Kio WordPress FSE & Block Theme Pipeline (`kio-wordpress-fse`)

The engineering and verification pipeline for **WordPress Full Site Editing (FSE) Block Themes** from any input source (static HTML, design screenshot mockups, or wireframes).

> **📌 Architecture Scope Note**: This skill specifically targets modern **Gutenberg Block Themes / Full Site Editing (`theme.json`, Block Patterns, and SSR Dynamic Blocks)**. It does **not** apply to legacy Classic Themes built on proprietary page builders (such as *Flatsome / UX Builder*).

---

## 🧭 Standard S0 – S8 Process Matrix

```
S0 Env ──► S1 Analyze ──► S2 Foundation ──► S3 Blocks SSR ──► S4 Editor Parity
                                                                       │
           S8 Delivery ◄── S7 Func QA ◄── S6 Visual QA ◄── S5 Seeding ─┘
```

| Phase | Core Objective | Standard & Deliverables |
|---|---|---|
| **S0 Env** | Port scanning & Docker initialization | Free port in `8080-8999`, `DB_NAME=<project_slug>`, 100% `.env`, Admin `<project_slug>_admin` (strict ban on `admin`), cryptographically random password |
| **S1 Analyze** | Input-source structural decomposition | Generate `docs/build/ui-spec.md` & `docs/build/block-map.md` based on input type (HTML / Visual Image / Wireframe) |
| **S2 Foundation** | Theme architecture & CSS tokens | `theme.json`, Design tokens, SCSS architecture, FSE Header/Footer template parts |
| **S3 Blocks** | Server-Side Rendered (SSR) Blocks | Custom blocks in active theme (`ai-zippy-child` or `<project-slug>`), `save.js` returns `null`, `render.php` handles dynamic SSR output |
| **S4 Editor Parity** | Gutenberg Site Editor Synchronization | 100% of copy, images, links, and icons editable in WP Admin. Zero discrepancy between Gutenberg Editor and Frontend |
| **S5 Seeding** | Media Sideloading & Backend Forms | Sideload images into WP Media Library, secure `wp_mail()` handler with nonces, synchronize WooCommerce core pages |
| **S6 Visual QA** | Multi-device layout verification | Automated Playwright screenshots: Desktop (1440px), Tablet (768px), Mobile (375px). Enforce Anti-Slop |
| **S7 Func QA** | Interactive logic & edge testing | Mini-cart drawer, mobile hamburger navigation, dynamic CTA icons/links, email dispatch, modal dialogs |
| **S8 Delivery** | Executive sign-off report | Generate visual `src/report-<project-name>.html` with live Playwright comparison evidence |

---

## 🎛️ Multi-Source S1 Analysis Engine

The Kio WordPress Pipeline automatically detects input formats and triggers specialized analysis pipelines:

### 1. Source is Converted PDF or HTML (`kio-frontend-craft`)
* **Philosophy**: Literal 1:1 clone. No invented UI.
* Build each WordPress block directly corresponding to sections in `design_spec.md`, reusing clean extracted background images in `images/` and exact HEX colors.

### 2. Source is Static HTML Mockup (Literal Clone)
* Guide: [`references/html-mockup-analysis.md`](references/html-mockup-analysis.md)
* **Philosophy**: Clone 1:1 with surgical precision. Never redesign or simplify; HTML/CSS mockup is ground truth.
* Deconstruct SPA pages, section hierarchies, extract CSS tokens and interactive JS behaviors (sliders, tabs, modals).

### 3. Source is Design Image / Mockup Screenshot (Visual Spec)
* Guide: [`references/image-spec-measurement.md`](references/image-spec-measurement.md)
* **Philosophy**: Quantitative viewport measurements (1440/1920px design width). Never guess.
* Deconstruct Hero vs Content, typographic scale, palette, spacing, and micro-interaction cues (hamburger, cart badge, accordion chevrons).

### 4. Source is Wireframe / Sketch (P-Flow for Existing Sites)
* Guide: [`references/wireframe-page-design.md`](references/wireframe-page-design.md)
* **Philosophy**: Apply existing project design tokens and component libraries to the wireframe layout.
* Fast-track lifecycle: P1 Analyze ➔ P2 Blocks ➔ P3 Editor Parity ➔ P4 Update Page ➔ P5 QA Sync.

### 5. Custom Business Feature (C-Flow)
* Applied when building bespoke Booking systems, CRM workflows, Custom Post Types, or Admin Dashboards.
* Lifecycle: C0 Spec ➔ C1 Backend Plugin ➔ C2 Admin UI ➔ C3 Functional QA ➔ C4 Visual Polish.

---

## 🏗️ 4-Archetype Repository Detection Matrix

Before modifying files, scan the repository root to detect the active architecture:

| Repo Archetype | Signature | PHP / Blocks / Templates Path | SCSS, JS & Build Tooling |
| :--- | :--- | :--- | :--- |
| **🅰️ Model 1: Gutenberg FSE + Vite** | Has `vite.config.child.js`, `src/wp-content/themes/ai-zippy-child/`, `theme.json` | • Blocks: `src/blocks/<slug>/` (`block.json`, `edit.js`, `render.php`)<br>• FSE: `parts/header.html`, `parts/footer.html`, `templates/*.html` | • SCSS: `src/scss/style.scss` + `src/scss/_*.scss`<br>• JS: `src/js/child.js`<br>• Build: **Vite** + `@wordpress/scripts` ➔ `assets/dist/` & `assets/blocks/` |
| **🅱️ Model 2: Classic PHP + Entry-Per-Page** | Root has `template/`, `src/entry/template/`, `webpack.common.js` | • Page Templates: `template/templates/template-<page>.php`<br>• Header/Footer: `template/header.php`, `footer.php`<br>• AJAX/Logic: `template/custom-functions/ajax-*.php`, `lib/` | • Shared: `src/scss/layouts/_common-sections.scss`, `src/entry/app.scss`, `src/utils/*.js`<br>• Per-page: `src/entry/template/<page>.scss` + `<page>.js`<br>• Build: **Webpack** (`yarn build` / `npm run build`) |
| **🅲 Model 3: Elementor Child + Includes** | Has `themes/*-elementor-child/`, `includes/kio_*.php`, `site-structure/` | • PHP Modules: `includes/kio_shortcode.php`, `kio-woo.php`, `kio_acf.php`, `kio_custom.php`<br>• Custom Blocks: `site-structure/blocks/<name>/index.php` | • SCSS: `assets/sass/app.scss`, `assets/sass/page/*.scss`<br>• JS: `assets/js/app.js`<br>• Build: **Webpack** ➔ `assets/dist/css/` & `assets/dist/js/` |
| **🅳 Model 4: Standalone FSE / Custom Theme** | None of the above or Greenfield project | • Create Standalone FSE Theme at `wp-content/themes/<project-slug>/` with `theme.json`, `parts/`, `templates/` | • Driven by theme's `package.json` (`vite` / `webpack` / `@wordpress/scripts`) |

---

## 🛑 15 Non-Negotiable Engineering Rules

1. **Strict Gate Passing**: Never declare a gate passed without fresh terminal output or screenshot evidence.
2. **Centralized CSS**: Never write raw CSS inside `src/blocks/*/style.scss`; consolidate into child theme SCSS for editor parity.
3. **No Theme Media Assets**: All media assets must be sideloaded directly into the WordPress Media Library.
4. **Dual Environment Verification**: Test both Frontend canvas and Gutenberg Admin editor simultaneously.
5. **Responsive Mandatory**: Validate at 375px mobile, 768px tablet, and 1440px desktop.
6. **Environment Variable Security**: All credentials stored in `.env`. Zero secrets in git.
7. **Database Naming**: `DB_NAME` must format project slug into `snake_case`.
8. **Admin Username**: Prohibit `admin`. Must use `<project_slug>_admin` with random >=16 character password.
9. **Visual Report**: Generate `src/report-<project-name>.html` with live side-by-side screenshots.
10. **100% Gutenberg Editable**: Zero hardcoded strings or images in `render.php`. All customizable via block attributes.
11. **Secure Email Forms**: Handle submissions via `wp_mail()`, nonce validation, and AJAX toast notifications.
12. **Customizable CTAs**: All CTA buttons must expose label, URL, and icon picker in Admin.
13. **WooCommerce Mini-Cart**: Flawless drawer opening on initial page load with clean empty states.
14. **WooCommerce Page Synchronization**: `/cart`, `/checkout`, `/my-account` must strictly conform to theme design tokens.
15. **FSE Template Parts**: Header and Footer must be drag-and-drop Template Parts (`parts/header.html`, `parts/footer.html`).
