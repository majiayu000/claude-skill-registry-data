---
name: go-embedded-frontend
description: A single-page frontend embedded into a Go binary from internal/server/static/ - HTML boilerplate, Tailwind v4 browser build, the Catppuccin Mocha palette, self-hosted fonts, icons, and PWA files. Use when building or changing the web UI of a Go Web Only or CLI + Web project, laying out static assets, theming a page, choosing which surface a panel or control sits on, or adding PWA support. Triggers on internal/server/static/, index.html, tailwind, @theme, Catppuccin, crust, favicon, manifest.json, sw.js, Lucide, and Font Awesome. Not for templ or htmx server-rendered HTML, and not for a framework SPA built outside the repository.
user-invocable: false
---

# Go Embedded Frontend

**One `index.html` under `internal/server/static/`, styled with the Tailwind browser build and the Catppuccin Mocha palette, with every asset self-hosted.**

The Go server owns how these bytes are served. This covers what goes inside `static/`.

## Layout

```
internal/server/static/
├── index.html          # the single page
├── app.js              # application logic, when it outgrows an inline block
├── manifest.json       # PWA, when enabled
├── sw.js               # PWA, when enabled, served at /sw.js
├── css/
│   ├── inter.css               # @font-face for Inter
│   ├── google-sans.css         # @font-face for Google Sans
│   ├── jetbrains-mono.css      # @font-face for JetBrains Mono
│   ├── github-dark.min.css     # highlight.js theme, when rendering markdown
│   └── devicon.min.css         # when using tech logos
├── fonts/              # woff2 only
├── fontawesome/
│   ├── css/
│   └── webfonts/
├── icons/
│   ├── favicon.ico             # 32x32, legacy browser tabs
│   ├── favicon.png             # 32x32
│   ├── apple-touch-icon.png    # 180x180, iOS home screen
│   ├── icon-192.png            # PWA, Android
│   ├── icon-512.png            # PWA, splash screen
│   └── logo.png                # in-app branding
└── js/                 # tailwind.js, lucide.min.js, and anything else vendored
```

Nothing under `css/`, `js/`, `fonts/`, or `fontawesome/` is committed. A Makefile target downloads them and the release workflow calls the same target, since a downloaded asset in a diff is a binary nobody reviews and a version nobody can trace.

## Assets

Every asset is pinned to an exact version. A floating `@latest` makes two builds of the same commit produce different bytes, and a new major breaks rendering with no diff to point at.

| Asset | Version | Lands at |
|---|---|---|
| Tailwind browser build | `@tailwindcss/browser@4.3.3` | `js/tailwind.js` |
| Lucide | `lucide@1.34.0` | `js/lucide.min.js` |
| Font Awesome | `@fortawesome/fontawesome-free@7.3.1` | `fontawesome/css/`, `fontawesome/webfonts/` |
| Dev Icons | `devicon@2.17.0` | `css/devicon.min.css` |
| Inter | Google Fonts | `css/inter.css`, `fonts/*.woff2` |
| Google Sans | Google Fonts | `css/google-sans.css`, `fonts/*.woff2` |
| JetBrains Mono | Google Fonts | `css/jetbrains-mono.css`, `fonts/*.woff2` |
| JetBrains Mono Nerd Font Mono | nerd-fonts `v3.5.1`, opt-in | `css/jetbrains-mono.css`, `fonts/*.woff2` |
| Chart.js | `chart.js@4.5.1` | `js/chart.umd.js` |

The three fonts are always downloaded, so the asset step is the same everywhere. Everything below them in the table is downloaded when the project uses it. Marked, Highlight.js, and Mermaid are pinned by the skills that own them.

Web fonts are woff2, never ttf. woff2 is roughly half the bytes of the same ttf and every browser here supports it, and Google Fonts already serves woff2.

Only the `latin` and `latin-ext` blocks of each Google Fonts stylesheet are kept. The endpoint declares every subset the family has, twenty-five files for Google Sans, and `//go:embed` compiles all of them into the binary regardless.

Font Awesome's stylesheet references its webfonts by a relative path that does not survive being served from `/static/`, so the asset step rewrites it:

```bash
sed -i.bak 's|../webfonts/|/static/fontawesome/webfonts/|g' fontawesome/css/all.min.css
rm -f fontawesome/css/all.min.css.bak
```

`sed -i.bak` rather than `sed -i ''`, because the empty-argument form is BSD-only and the release workflow runs this on Linux.

## Fonts

| Font | Role | `font-family` |
|---|---|---|
| Inter | body and UI text | `'Inter'` |
| Google Sans | display headings and branding | `'Google Sans'` |
| JetBrains Mono | code and monospace | `'JetBrains Mono'` |

Each has its own `@font-face` stylesheet under `css/`, pointing at local woff2 files. Nothing loads from `fonts.googleapis.com` at run time, since a page fetching a font from a third party leaks every visitor's IP and stops rendering offline.

The mono slot takes the plain family by default. The Nerd Font variant is a patched build Google Fonts does not carry, so it is downloaded as ttf and compressed to woff2, costing two megabytes and ten seconds against sixty kilobytes and half a second. A page earns that only by rendering Nerd Font glyphs: a Powerline separator, a private-use file-type icon, or terminal output carrying them. An icon Lucide or Font Awesome already has is not a reason.

Switching is a Makefile variable, not a page change. The nerd target writes the same `css/jetbrains-mono.css` under the same `JetBrains Mono` family name.

## The Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APP_NAME</title>

    <link rel="icon" type="image/x-icon" href="/static/icons/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png">

    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#11111b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="APP_NAME">

    <link rel="stylesheet" href="/static/css/inter.css">
    <link rel="stylesheet" href="/static/css/google-sans.css">
    <link rel="stylesheet" href="/static/css/jetbrains-mono.css">
    <link rel="stylesheet" href="/static/fontawesome/css/all.min.css">

    <script src="/static/js/lucide.min.js"></script>
    <script src="/static/js/tailwind.js"></script>
    <style>
      /* Catppuccin Mocha */
      :root {
        --ctp-rosewater: #f5e0dc; --ctp-flamingo: #f2cdcd; --ctp-pink: #f5c2e7;
        --ctp-mauve: #cba6f7;     --ctp-red: #f38ba8;      --ctp-maroon: #eba0ac;
        --ctp-peach: #fab387;     --ctp-yellow: #f9e2af;   --ctp-green: #a6e3a1;
        --ctp-teal: #94e2d5;      --ctp-sky: #89dceb;      --ctp-sapphire: #74c7ec;
        --ctp-blue: #89b4fa;      --ctp-lavender: #b4befe; --ctp-text: #cdd6f4;
        --ctp-subtext1: #bac2de;  --ctp-subtext0: #a6adc8; --ctp-overlay2: #9399b2;
        --ctp-overlay1: #7f849c;  --ctp-overlay0: #6c7086; --ctp-surface2: #585b70;
        --ctp-surface1: #45475a;  --ctp-surface0: #313244; --ctp-base: #1e1e2e;
        --ctp-mantle: #181825;    --ctp-crust: #11111b;
      }
    </style>
    <style type="text/tailwindcss">
      @theme {
        --color-rosewater: var(--ctp-rosewater); --color-flamingo: var(--ctp-flamingo);
        --color-pink: var(--ctp-pink);           --color-mauve: var(--ctp-mauve);
        --color-red: var(--ctp-red);             --color-maroon: var(--ctp-maroon);
        --color-peach: var(--ctp-peach);         --color-yellow: var(--ctp-yellow);
        --color-green: var(--ctp-green);         --color-teal: var(--ctp-teal);
        --color-sky: var(--ctp-sky);             --color-sapphire: var(--ctp-sapphire);
        --color-blue: var(--ctp-blue);           --color-lavender: var(--ctp-lavender);
        --color-text: var(--ctp-text);           --color-subtext1: var(--ctp-subtext1);
        --color-subtext0: var(--ctp-subtext0);   --color-overlay2: var(--ctp-overlay2);
        --color-overlay1: var(--ctp-overlay1);   --color-overlay0: var(--ctp-overlay0);
        --color-surface2: var(--ctp-surface2);   --color-surface1: var(--ctp-surface1);
        --color-surface0: var(--ctp-surface0);   --color-base: var(--ctp-base);
        --color-mantle: var(--ctp-mantle);       --color-crust: var(--ctp-crust);

        --font-sans: 'Inter', sans-serif;
        --font-display: 'Google Sans', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
      }
    </style>
</head>
<body class="bg-crust text-subtext0 min-h-screen font-sans">
    <nav class="bg-crust border-b border-surface0 px-4 py-3">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-2">
                <img src="/static/icons/logo.png" alt="Logo" class="w-8 h-8">
                <span class="text-lg font-semibold font-display text-text">APP_NAME</span>
            </div>
        </div>
    </nav>

    <main class="max-w-6xl mx-auto px-4 py-8">
        <h1 class="text-2xl font-bold mb-6 font-display text-text">Page Title</h1>
        <div class="bg-mantle border border-surface0 rounded-xl p-6">
            <input class="w-full bg-surface0 border border-surface1 rounded-lg px-3 py-2 text-text pointer-coarse:text-[16px]">
        </div>
    </main>

    <script src="/static/app.js"></script>
    <script>lucide.createIcons();</script>
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }
    </script>
</body>
</html>
```

The Tailwind v4 browser build reads the `<style type="text/tailwindcss">` block containing `@theme` and rejects a JavaScript config entirely, so the `tailwind.config = {...}` global from v3 produces no CSS and no error.

A `--color-mauve` entry generates `bg-mauve`, `text-mauve`, and a real `var(--color-mauve)` for hand-written CSS. Naming the entries after Catppuccin's own names keeps the class written and the swatch picked identical.

`@theme` maps each name onto a `--ctp-*` variable rather than a literal hex. The utility resolves the variable at paint time, so redefining the `--ctp-*` set under a selector re-themes the page without a second `@theme` or a class change. Opacity modifiers survive it, since v4 emits `color-mix(in oklab, var(--color-mauve) 50%, transparent)` rather than substituting a value.

`@import "tailwindcss";` is omitted, because the browser build injects it when no `@import` appears anywhere in the block. Writing one takes over the whole import graph and drops the base styles unless you add it back yourself.

## Layering

The page is grounded on `crust`, the darkest step, and every surface is raised from there. Grounding on `base` instead leaves the chrome darker than the page it sits on and costs contrast against every text color.

| Role | Token |
|---|---|
| Page ground, and any chrome flush with it such as a sidebar, header, or rail | `crust` |
| A surface that reads as lifted off the page, such as a card, modal, popover, or dropdown | `mantle` |
| A control sitting on either of those, such as an input, chip, button, or hovered row | `surface0` |
| Borders, dividers, and the hover state of a `surface0` control | `surface1` |
| A well recessed inside a `mantle` panel, such as a code block or an embedded preview | `base` |

Adjacent layers step one rung and no more. `crust` to `mantle` is a contrast ratio of 1.07 and `crust` to `surface0` is 1.49, which separates them without drawing a seam. Skipping a rung reads as two unrelated panels rather than one raised off the other.

Text runs the same way. Body copy takes `subtext0`, headings and the one value a row exists to show take `text`, and metadata takes `overlay1`. Defaulting body copy to `text` makes every word shout and leaves nothing louder for a heading to be.

Structure never borrows from the accent ramp. The neutral steps carry it, and an accent marks one thing per view: the active item, the primary action, or a state. Two accents competing means neither is signal.

The tokens are assigned by what a surface does, so a layout this skill has never seen still lands on the right step.

## Theme

Catppuccin Mocha is the default for a new frontend. A project that already has a palette keeps it, since re-theming an existing app is a design decision rather than a convention.

Light and dark switching is added only when it is asked for, by redefining the `--ctp-*` set for Latte.

```html
<style>
  /* Catppuccin Latte, re-slotted so crust stays the page ground */
  :root:not(.dark) {
    --ctp-crust: #eff1f5; --ctp-mantle: #e6e9ef; --ctp-base: #dce0e8;
    --ctp-surface0: #ccd0da; --ctp-surface1: #bcc0cc; --ctp-surface2: #acb0be;
    --ctp-text: #4c4f69; --ctp-subtext0: #5c5f77; --ctp-overlay1: #6c6f85;
    --ctp-blue: #1e66f5; --ctp-mauve: #8839ef;
  }
</style>
```

Latte's ramp runs light to dark, the opposite of Mocha's, so re-slotting keeps `crust` the ground and `mantle` the surface above it in both. The text tokens shift one step too, because Latte's own `subtext0` on its own `base` is 4.37 and body copy has to clear 4.5.

A script in `<head>` sets the class from `localStorage` or `prefers-color-scheme` before the body renders, preventing a flash of the wrong theme.

## Styling Rules

Styling is Tailwind utility classes on the element. Hand-written CSS earns its place only in a case that has no utility form:

- `@font-face` declarations
- scrollbar pseudo-elements, `::selection`, and other pseudo-elements Tailwind does not reach
- a subtree a third party generates, where the classes are not yours to write, such as rendered Markdown, a Mermaid diagram, or an editor widget
- `@media print` rules
- `@keyframes`

Everything else is a class. A hand-written rule that duplicates a utility is a second place a color or a spacing value can drift, and it is invisible to anyone reading the element.

The custom CSS that remains lives in inline `<style>` blocks rather than `css/`, so the asset step can wipe and re-download `css/` without touching anything a person wrote.

An existing project's working CSS is not ripped out to impose this, since the rule governs what you write.

The browser build compiles utility classes at run time, which Tailwind documents as development-only. It is fine for an embedded tool or a dashboard, and an app needing a small payload moves to a build step emitting a static `tailwind.css`.

One `index.html` is the default. Views are shown and hidden client-side, and shared logic moves into `app.js` only once more than one place needs it.

Every form control renders at 16px on a coarse pointer, through `pointer-coarse:text-[16px]` alongside whatever size the design uses. iOS Safari zooms the viewport in when a focused control computes under 16px, and it does not zoom back out on blur.

`text-base` cannot carry it, because the palette defines `--color-base` and Tailwind compiles `text-base` to `color: var(--color-base)` with no font size.

The viewport meta stays `width=device-width, initial-scale=1.0`, since `user-scalable=no` and `maximum-scale=1` suppress the zoom only by taking pinch zoom away from everyone.

## Icons

| Library | Use for |
|---|---|
| Lucide | general UI icons, the default |
| Font Awesome | brand icons, and gaps in Lucide |
| Dev Icons | technology and language logos |

```html
<i data-lucide="settings"></i>
<script>lucide.createIcons();</script>

<i class="fab fa-github"></i>

<i class="devicon-go-original-wordmark"></i>
```

`lucide.createIcons()` runs after any DOM update that inserts an `<i data-lucide>`, since it replaces those elements with inline SVG and does not observe later insertions.

App icons are PNG with transparency, recognizable at 16 pixels, and drawn from the Catppuccin palette so they read on light and dark browser chrome. PWA icons keep their content inside the centre 80%, because the installer rounds the corners off.

## PWA

Add PWA support when the app is used often on a phone, when offline behavior is useful, or when installability was requested. Skip it for an admin dashboard or a developer tool, where an install prompt is noise.

`static/manifest.json`:

```json
{
  "name": "APP_NAME",
  "short_name": "APP_SHORT",
  "description": "APP_DESCRIPTION",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#11111b",
  "theme_color": "#11111b",
  "icons": [
    { "src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

`static/sw.js` is a no-op worker:

```javascript
self.addEventListener('fetch', () => {});
```

It caches nothing, so the app behaves like a normal tab. A caching worker serves stale assets after a deploy and gives users a version they cannot refresh away.

The worker is not what makes the app installable, since the manifest, the two icon sizes, and HTTPS are. It earns its line by controlling the app's pages, which later offline or push behavior needs.

A worker's scope is the directory it is served from, so one served at `/static/sw.js` controls `/static/` and never the app at `/`. It registers without error and reports that narrow scope, so nothing fails loudly enough to notice. A `Service-Worker-Allowed` header on the static mount is the wrong repair, because it widens every file under `/static/` to fix one.

The file stays under `static/` so `//go:embed static` picks it up, and a route at `/sw.js` serves it from the embedded FS through `http.ServeFileFS` with a `text/javascript` content type.

Drop the manifest, the worker, its route, the registration script, and the PWA meta tags together when not building a PWA. The manifest alone is enough to prompt an install, which an app that gains nothing from being installed should not do.
