---
name: hugo-architect
version: 1.0.0
description: Hugo 0.161 static-site architectural standards — project layout, front matter conventions, template hierarchy, Hugo Modules over submodules, Page Bundles, asset pipeline via Hugo Pipes, i18n, render hooks, deployment targets. Extended edition required. Use when scaffolding, reviewing, or auditing a Hugo site or theme.
---

# Hugo Architecture

Targets **Hugo Extended 0.161** (Go-templated static-site generator). Theme styling integrates with [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md); Go template syntax overlaps with [go-architect](../../languages/go-architect/SKILL.md); deploy pipelines follow [ci-cd-architect](../../infra/ci-cd-architect/SKILL.md). Concrete skeletons in [RECIPES.md](RECIPES.md); pinned versions in [STACK.md](STACK.md).

## 1. Project layout & content organization

- **Standard top-level folders** — `content/`, `layouts/`, `assets/`, `static/`, `data/`, `i18n/`, `archetypes/`, `themes/` (if not module-mounted), `hugo.toml`. Skeleton in [RECIPES § Project tree](RECIPES.md#project-tree).
- **`content/` mirrors the URL structure.** Section folders (`content/posts/`, `content/docs/`) become URL prefixes; taxonomies are inferred from front matter, not folder names.
- **`assets/` for processed files; `static/` for pass-through.** Anything that needs fingerprinting, minification, transpilation, or image processing belongs in `assets/` and goes through Hugo Pipes. Truly static files (`robots.txt`, `favicon.ico`, prebuilt PDFs) go in `static/`.
- **`data/` for structured site data** — JSON/YAML/TOML files queryable via `site.Data.<file>`. Use for author lists, sponsor logos, redirect maps; do **not** use for content (that belongs in `content/`).
- **`archetypes/` define `hugo new` templates** — one per content section, with sensible front-matter defaults.
- **One repository per site by default.** Multi-site monorepos are an exception; reach for them only when ownership and deploy targets align.

## 2. Front matter conventions

- **TOML front matter** is the default (`+++` delimiters). Matches `hugo.toml` config syntax — one parser to learn. YAML is acceptable for theme authors who must support broader ecosystems; pick one per repo and don't mix.
- **Required fields on every page** — `title`, `date`, `draft` (default `false` once published). Drafts are excluded from production builds.
- **Taxonomies are arrays** — `tags = ["x", "y"]`, never comma-separated strings. Taxonomies auto-generate listing pages.
- **`slug` only when the title is unstable.** Otherwise let Hugo derive from the filename — stable URLs survive title edits.
- **`weight` for manual ordering** — lower = earlier. Reserve for navigation menus and curated lists; chronological content uses `date`.
- **Custom params under `[params]`** — never at the top level. `params` is the supported namespace for site-specific extensions; top-level keys collide with future Hugo additions.

## 3. Template hierarchy

Hugo's lookup order resolves templates from most-specific to most-generic. Internalize the order; don't memorize it — the [Hugo template lookup docs](https://gohugo.io/templates/lookup-order/) are the source of truth.

- **`baseof.html`** is the single shell template. Every other template extends it via `{{ define "main" }}`.
- **`single.html`** renders one page; **`list.html`** renders section/taxonomy listings; **`home.html`** is the site root.
- **`partials/`** are reusable fragments — header, footer, SEO meta. Pass an explicit context; never rely on the global scope.
- **`shortcodes/`** are content-callable partials — invoke from Markdown with `{{< name >}}`. Use for figures, callouts, embeds; do **not** use to inject styling.
- **Type/section overrides** — `layouts/posts/single.html` beats `layouts/_default/single.html`. The `_default/` folder is the fallback, not the convention.

Skeletons in [RECIPES § Template hierarchy](RECIPES.md#template-hierarchy).

## 4. Hugo Modules over git submodules

- **Themes and shared layouts ship as Hugo Modules** — Go-module-backed, versioned via SemVer tags. `hugo mod get` resolves; `go.mod` records.
- **Why not git submodules?** Submodules pin to commits with no version semantics, require `git submodule update --init` after every clone, and break on theme repo reorganizations. Modules give SemVer + automatic dependency resolution.
- **`hugo.toml [module]` block** declares imports, mounts, and replacements. Mount overrides let you patch a single template without forking the theme.
- **Vendor for reproducibility** — `hugo mod vendor` writes `_vendor/`; commit it for hermetic builds (mirrors Go's `vendor/` discipline per [go-architect](../../languages/go-architect/SKILL.md)).

Skeleton in [RECIPES § Hugo Module setup](RECIPES.md#hugo-module-setup).

## 5. Page Bundles over flat content

- **Page Bundle = `index.md` + co-located assets** in a folder. `content/posts/launch-day/index.md` plus `cover.jpg`, `diagram.svg` in the same folder.
- **Two bundle types:**
  - **Leaf bundle** (`index.md`) — a single page; resources are bundle-local.
  - **Branch bundle** (`_index.md`) — a section page; child pages are independent.
- **Why bundles?** Page resources (`resources.Get`, `.Resources.GetMatch`) are scoped to the bundle, image processing works on co-located files, and content + assets move together.
- **Flat `content/posts/foo.md` is acceptable** for text-only posts with no images. Reach for bundles the moment you have a cover image or inline diagram.

## 6. Asset pipeline (Hugo Pipes)

Hugo Pipes is the built-in asset pipeline — no Webpack, no Vite. Extended edition required for Sass/SCSS.

- **Source files in `assets/`** — invoke via `resources.Get "css/app.scss"`.
- **Standard chain** — `toCSS` (or `js.Build`) → `postCSS` (optional, for Tailwind/autoprefixer) → `minify` → `fingerprint` → render `<link>` / `<script>` with `Permalink` + `Data.Integrity` (SRI).
- **Fingerprinting is mandatory in production** — long-cache headers + immutable URLs. Build with `--minify` and rely on the fingerprint for cache busting.
- **Image processing** — `.Resize`, `.Fit`, `.Fill`, `.Filter`. Pair with `srcset` for responsive images. WebP/AVIF output via format conversion. Use `q=` for JPEG quality; don't blow the byte budget.
- **PostCSS lives outside Hugo** — `postcss.config.js` + `package.json`. Hugo invokes the binary; keep the toolchain pinned via [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md).

Skeleton in [RECIPES § Asset pipeline chain](RECIPES.md#asset-pipeline-chain).

## 7. Performance budget

- **Build time target** — under 10s for sites under 1k pages; under 60s for sites under 10k pages. Beyond that, profile (`hugo --templateMetrics`) and audit the slowest partial/shortcode.
- **Per-page weight** — under 100 KB transferred (HTML + CSS + JS + critical fonts) for content pages. Images load lazily via `loading="lazy"` and `srcset`.
- **No JS by default.** Add JS only where it earns its place (search, comments, interactive widgets). Hugo's strength is shipping HTML; don't undermine it.
- **Tailwind via PostCSS with `content` globbing** — production builds purge unused classes. Without purging, Tailwind ships ~3 MB CSS.
- **Critical CSS inline for above-the-fold** when Lighthouse flags it; fingerprinted external CSS for the rest.

## 8. i18n & multilingual

- **`[languages]` block in `hugo.toml`** — one entry per language, with `weight`, `languageName`, `contentDir`, `languageDirection`.
- **Translation strategies** — by filename (`post.en.md` + `post.es.md`) or by content directory (`content/en/` + `content/es/`). Pick one per site; filename mode is simpler, directory mode scales better past three languages.
- **`i18n/<lang>.toml`** for UI strings — invoke via `{{ i18n "key" }}`. Don't hardcode strings in templates.
- **Translation linking** — Hugo auto-links translations by `translationKey` (front matter) when filenames diverge.
- **Default language has no URL prefix** unless `defaultContentLanguageInSubdir = true`. Decide early — changing later breaks every existing URL.

## 9. Render hooks & Markdown extensions

- **Goldmark is the Markdown parser.** Render hooks override individual element rendering — `render-link.html`, `render-image.html`, `render-codeblock-<lang>.html`, `render-heading.html`.
- **Use render hooks for** — auto-linking internal references, lazy-loading images, syntax-highlighting code blocks via Chroma, adding anchor links to headings.
- **Markdown extensions enabled by default** — tables, strikethrough, footnotes, definition lists, task lists, typographer. Configure under `[markup.goldmark]`.
- **`unsafe = true`** allows raw HTML in Markdown. Enable only when content authors are trusted; otherwise it's an XSS vector.
- **Shortcodes for structured content** that Markdown can't express cleanly — figure with caption, video embed, alert box. Don't reach for shortcodes when a render hook would do.

Skeleton in [RECIPES § Render hook examples](RECIPES.md#render-hook-examples).

## 10. Deployment targets

- **Static-host CDN is the default** — Cloudflare Pages, Netlify, GitHub Pages, S3 + CloudFront. Build in CI, push the `public/` folder.
- **Cloudflare Pages** — first-class Hugo support, native integration with `wrangler.toml`. Free tier is generous.
- **GitHub Pages** — fine for personal sites and docs. `peaceiris/actions-hugo` is the standard workflow action. Custom domains require a CNAME file in `static/`.
- **S3 + CloudFront** — when you need infrastructure control or are inside an AWS-only org. Pair with OAI/OAC for private bucket + CloudFront-only access.
- **`baseURL` must match the deploy domain** — relative URLs break otherwise. Use `--baseURL` in CI to inject per-environment.
- **CI pipeline** — see [ci-cd-architect](../../infra/ci-cd-architect/SKILL.md). Standard stages: install Hugo Extended → `hugo --minify` → upload `public/`.

Skeleton in [RECIPES § GitHub Pages deploy workflow](RECIPES.md#github-pages-deploy-workflow).

## 11. Out of scope

- **CMS / authoring UI** — Hugo is a build tool. For non-technical authoring, layer Decap CMS, Tina, or Sanity on top; or move to Astro/Next.js if dynamic features outweigh build-step simplicity.
- **Dynamic features at runtime** — comments, search, forms. These need a third-party service (Disqus, Algolia, Formspree, Cloudflare Workers) — Hugo only emits static HTML.
- **Themes you author from scratch** — covered at a high level here; deep theme development is its own discipline and would need a `hugo-theme-architect` skill if demand emerges.
- **Markdown content conventions** — front-matter linting, heading hierarchy, image alt-text discipline belong to a separate authoring guide; this skill enforces site structure, not content style.

## 12. Cross-skill ties

- [go-architect](../../languages/go-architect/SKILL.md) — Hugo's template language is Go's `text/template` + `html/template`; same syntax, same gotchas.
- [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) — design tokens, accessibility, four-state UI discipline apply to Hugo themes the same way as React/Next.
- [ci-cd-architect](../../infra/ci-cd-architect/SKILL.md) — deploy pipelines for the built `public/` artifact.
- [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md) — `mise` or `proto` for pinning the Hugo binary version; `Task` / `just` for the local build commands.

---

_Adapted from the [Hugo documentation](https://gohugo.io/documentation/) (v0.161)._
