---
name: tailwind-v3-to-v4-migration
version: 0.0.2
description: >-
  Migrate a project from Tailwind CSS v3 to v4 safely and completely. Runs the official
  `@tailwindcss/upgrade` codemod, then drives the judgment it can't: reconciling dependencies and
  PostCSS/Vite/CLI plumbing, porting JS config to CSS-first `@theme` (or keeping it via `@config`),
  auditing the v4 changed-defaults that silently alter appearance
  (border/ring/placeholder/cursor/dialog/hover) and applying compat shims, sweeping for
  renamed/removed utilities, and proving the migration is a visual no-op. Framework-agnostic
  (Next.js, Vite, Tailwind CLI, plain PostCSS; Vue/Svelte/Astro/CSS-module caveats). USE FOR: upgrading Tailwind 3 to 4, "tailwind v4
  migration", `@tailwind` directives error, `@tailwindcss/postcss` setup, tailwind.config.js to CSS
  @theme, shadow-sm/rounded/ring/outline-none renames, bg-gradient-to to bg-linear-to. Activate only
  when an existing Tailwind v3 install is being upgraded. DO NOT USE FOR: a fresh v4 setup with no v3
  present, downgrading v4 to v3, or non-Tailwind CSS.
license: MIT
compatibility: >-
  The upgrade tool requires Node.js 20+. Works best in a git repo (run in a branch, review the
  diff). A way to view the app in a browser (or a screenshot/visual-regression harness) is needed
  for the verification step.
---

# tailwind-v3-to-v4-migration

Upgrade a codebase from Tailwind CSS v3 to v4. The codemod does ~80% of the mechanical work; this
skill supplies the 20% of judgment where migrations actually break — changed defaults, config
porting, plugin/animation swaps, and proving nothing moved.

## When to use

- Upgrading any project from Tailwind v3.x to v4.x.
- Build errors after a partial upgrade: `@tailwind` directives unknown, missing `@tailwindcss/postcss`,
  `Cannot apply unknown utility class`, `tailwind.config` no longer picked up.
- Converting `tailwind.config.{js,ts}` to CSS-first `@theme`.

Skip if: the project is already on v4; you need to *downgrade*; or you are building a brand-new design
system rather than migrating one. Note v4 targets **Safari 16.4+, Chrome 111+, Firefox 128+** —
if you must support older browsers, stay on v3.4 (flag this to the operator before proceeding).

## The one idea that makes this safe

**A correct migration is a visual no-op.** Every renamed utility is a pure alias — `shadow-sm`→
`shadow-xs`, `rounded`→`rounded-sm`, `ring`→`ring-3`, `outline-none`→`outline-hidden` all compile to
the *same* CSS as before. So what changes pixels is almost entirely v4's **changed defaults** (Step 3);
the few non-default exceptions — the `space-x/y-*` & `divide-*` selector change, gradient-variant
preservation, and `container` config removal — are flagged in Step 4. Rename mechanically, neutralize
the changed defaults, fix those few exceptions, and the rendered output is identical. That is also how
you verify success (Step 5): capture the UI before, prove it's unchanged after.

## Procedure

Always work on a branch. Run the steps in order; do not skip Step 0 or Step 3.

### Step 0 — Pre-flight & baseline (do not skip)

1. Confirm Node 20+ (`node -v`) and that the working tree is clean. Create a branch (e.g. `tailwind-v4`).
2. **Inventory** every Tailwind entry point — there may be more than one: each CSS file with
   `@tailwind`/`@import "tailwindcss"`, every `tailwind.config.*`, every `postcss.config.*`, the
   bundler config (next/vite/webpack), and `package.json`. Monorepos: do this per package.
3. Record the current setup: `darkMode` value, custom `theme.extend`, `plugins`, the package
   manager (npm/yarn/pnpm/bun), and two easy-to-miss config options that need special handling later:
   **`prefix`** (v4 changes `tw-flex`→`tw:flex`) and **`theme.container`** (`center`/`padding` are gone
   in v4 — recreate via `@utility container`).
4. **Capture a baseline of how the app looks now** so you can prove the migration changed nothing:
   a screenshot set or a visual-regression run on v3 (see `references/05-verification-playwright.md`),
   or at minimum a list of key pages to eyeball. Confirm the project builds green on v3 first.

### Step 1 — Run the official upgrade tool

```bash
npx @tailwindcss/upgrade@latest          # clean git tree required…
npx @tailwindcss/upgrade@latest --force  # …or pass --force if untracked/uncommitted files exist
```

The tool refuses to run on a dirty tree (so you can review its diff). Commit/stash unrelated changes,
or use `--force`. It updates dependencies, migrates the config to CSS where it can, rewrites
`@tailwind` directives, and codemods most renamed/removed utilities in templates. **Review the full
diff** — it is a starting point, not the finish line. If it errors (offline, exotic setup, unsupported
config), fall back to the manual path in `references/01-breaking-changes.md` +
`references/02-css-first-config.md` and continue. **Monorepos:** run the tool once per package root and
confirm `tailwindcss` resolves to 4.x in *every* package's `node_modules` — a half-migrated workspace
compiles some packages against v3.

### Step 2 — Reconcile dependencies & build plumbing

Verify the tool did these; finish any it missed (`references/04-framework-setups.md` for your stack):

- **Deps:** remove `tailwindcss@3`; add `tailwindcss@^4`. Remove `autoprefixer` and `postcss-import`
  (v4 does prefixing + import inlining itself).
- **PostCSS:** `postcss.config.*` → `{ plugins: { '@tailwindcss/postcss': {} } }` (add the
  `@tailwindcss/postcss` dep). **Vite:** prefer `@tailwindcss/vite` over PostCSS. **CLI:** `npx
  tailwindcss` → `npx @tailwindcss/cli`.
- **CSS entry:** `@tailwind base/components/utilities;` → `@import "tailwindcss";`.
- **Plugins:** delete now-built-in ones (`@tailwindcss/container-queries`, `@tailwindcss/aspect-ratio`,
  line-clamp) — and remove their dead `theme`/usage. **`@tailwindcss/typography` stays** but is loaded
  in CSS via `@plugin "@tailwindcss/typography";` and must be bumped to a v4-compatible release (≥0.5.16).
- **`container` customization:** if v3 set `theme.container.center`/`padding`, those options are gone —
  recreate as `@utility container { margin-inline: auto; padding-inline: 2rem; }` or every `container`
  loses its centering/padding silently.
- Reinstall with the project's package manager so the lockfile updates; the `tailwindcss` version must
  resolve to 4.x.

### Step 3 — Changed-defaults audit + compat shims (the parity killers)

These changed defaults are the main thing that moves pixels (see Step 4 for the few non-default
exceptions). Walk the checklist; for each "relied on", paste the shim into your main CSS (after
`@import "tailwindcss";`). Full rationale in `references/03-compat-shims.md`.

- [ ] **Border/divide color** is now `currentColor` (was `gray-200`). If you use bare `border`/`divide`
      without a color anywhere, add:
  ```css
  @layer base {
    *, ::after, ::before, ::backdrop, ::file-selector-button {
      border-color: var(--color-gray-200, currentColor);
    }
  }
  ```
- [ ] **Ring** is now 1px / `currentColor` (was 3px / `blue-500`). Replace bare `ring`→`ring-3`; if you
      relied on the blue default add `ring-blue-500`. (Compat-only escape: `@theme { --default-ring-width:
      3px; --default-ring-color: var(--color-blue-500); }`.)
- [ ] **Placeholder** is now current text @ 50% (was `gray-400`). To keep v3 look:
  ```css
  @layer base { input::placeholder, textarea::placeholder { color: var(--color-gray-400); } }
  ```
- [ ] **Buttons** now use `cursor: default` (was `pointer`):
  ```css
  @layer base { button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; } }
  ```
- [ ] **`<dialog>`** margins are reset (was centered): `@layer base { dialog { margin: auto; } }` if needed.
- [ ] **Hover** now applies only on `(hover: hover)` devices. If your UI depends on tap-to-hover, add
      `@custom-variant hover (&:hover);`.
- [ ] **Dark mode:** if v3 used `darkMode: 'class'` (or a custom selector), add
      `@custom-variant dark (&:is(.dark, .dark *));`. If it used `'media'`, v4's default already matches —
      **do nothing** (adding the class variant would *break* media-driven dark mode).

> **Two of these are invisible to a screenshot harness:** the **button-cursor** and **hover-on-tap**
> shims change behavior, not painted pixels, so visual parity (Step 5) can't confirm them. Decide them
> by reasoning about the markup (do real `<button>`s / touch interactions rely on the v3 default?), not
> by the pixel diff. Same for `outline-none`→`outline-hidden` (the difference only shows in forced-colors mode).

### Step 4 — Residual sweep (catch what the codemod missed)

Grep, then fix each real hit against the tables in `references/01-breaking-changes.md` (which cover the
mechanical rewrites: `*-opacity-*`→`/<n>`, `flex-shrink/grow`→`shrink/grow`, `bg-gradient-to`→
`bg-linear-to`, arbitrary `bg-[--x]`→`bg-(--x)`, `!flex`→`flex!`, `theme()`→`var(--…)`, etc.):

```bash
grep -rEn '@tailwind |bg-gradient-to-|flex-shrink-|flex-grow-|overflow-ellipsis|decoration-slice|decoration-clone|[a-z]+-opacity-[0-9]|outline-none' src
grep -rEn '\b(shadow|rounded|blur|drop-shadow|backdrop-blur)(["'"'"'`[:space:]])' src   # bare scales — review, don't blind-replace
grep -rEn 'transition(-colors)?\b' src    # if paired with a focus-state outline-* color → set outline-color unconditionally
# only if v3 used a prefix (Step 0): grep -rEn '\bPFX-[a-z]' src   # PFX-flex → PFX:flex
```

Three judgment calls the tables don't make for you:

- **Order bare renames after explicit ones:** `shadow-sm`→`shadow-xs` *before* bare `shadow`→`shadow-sm`
  (same for rounded/blur/drop-shadow/backdrop-blur); word-boundary the bare form so `rounded-md`/
  `shadow-lg` are untouched. The grep is noisy — `blur`/`shadow` collide with `placeholder="blur"` and
  prose; fix only real class lists.
- **`space-x/y-*` & `divide-x/y-*`** selectors changed to `:not(:last-child)` (no shim). If a list/inline
  layout shifts, move it to flex/grid + `gap`.
- **Gradients** now *preserve* stops across variants — add `via-none` to reset a 3-stop in a state.

### Step 5 — Verify (build + browser parity)

1. `build`, `lint`, `typecheck`, and unit tests must pass.
2. **Prove the visual no-op:** re-run the baseline from Step 0 and confirm zero unintended diffs. Pay
   special attention to: borders, focus rings, placeholders, dark mode, and any `prose` (typography)
   content. Any diff maps to a missed Step 3 shim or Step 4 rename — fix it, don't accept it.
3. **Check the screenshot-invisible changes by hand:** button cursor, hover-on-touch, and forced-colors
   outline behavior (see the Step 3 note) — confirm these in a real browser, since no pixel diff will.

## Decision points

- **Port JS config to CSS, or keep it?** Default: port `theme.extend` to a CSS `@theme {}` block
  (nested objects → flat vars: `colors.brand.500`→`--color-brand-500`, `boxShadow.card`→`--shadow-card`,
  `fontFamily.sans`→`--font-sans`; use `@theme inline` for `hsl(var(--x))` references). **Keep the JS
  file via `@config "../tailwind.config.js";`** when it carries plugin theming that's hard to express in
  CSS — the classic case is **`@tailwindcss/typography` `theme.extend.typography` customization**
  (custom `prose-*` modifiers). `@config` is officially supported v4 usage. `corePlugins`, `safelist`,
  `separator` are NOT supported in JS config under v4 (safelist → `@source inline(...)`). Note:
  Tailwind's **default** theme tokens (e.g. `--color-gray-200`, `--color-gray-400`) stay available even
  when you keep a JS config via `@config`, so the Step 3 compat shims that reference them still resolve.
  See `references/02-css-first-config.md`.
- **CSS directive order:** `@import "tailwindcss";` must come first; place `@config "…";` and any
  `@theme { … }` block after it.
- **Custom `@layer utilities`/`@layer components` classes** → convert to `@utility name { … }`.
- **Animation libs:** `tailwindcss-animate` (v3) → `tw-animate-css` (`@import "tw-animate-css";`),
  utility names unchanged.
- **Scoped styles** (Vue/Svelte/Astro `<style>`, CSS modules) lose theme access → add
  `@reference "../app.css";` or use raw CSS vars. **No Sass/Less/Stylus** with v4.

## Manual fallback (no codemod)

deps → `postcss.config` → `@import "tailwindcss";` → port theme to `@theme` (or `@config`) → Step 3
shims → Step 4 sweep → Step 5 verify. Exhaustive tables: `references/01-breaking-changes.md`,
`references/02-css-first-config.md`, `references/03-compat-shims.md`.

## References

- `references/00-official-upgrade-guide.md` — the **official** Tailwind v3→v4 upgrade guide, verbatim
  (source of truth; everything below distills it). https://tailwindcss.com/docs/upgrade-guide
- `references/01-breaking-changes.md` — complete renamed / removed / syntax-change tables.
- `references/02-css-first-config.md` — JS theme → `@theme`; `@config` fallback; plugins; `@utility`.
- `references/03-compat-shims.md` — every changed default + its copy-paste shim and when it's needed.
- `references/04-framework-setups.md` — Next.js, Vite, CLI, PostCSS, Astro, Vue, Svelte, CSS modules.
- `references/05-verification-playwright.md` — capture-baseline-then-assert visual-parity recipe.
- `references/06-gotchas.md` — rename ordering, typography prose port, gradient `via-none`, hover-on-tap, monorepos.
