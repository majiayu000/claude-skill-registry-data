---
name: lottie-design
description: Search, fetch, and integrate free Lottie animations into React, React Native, Vue, Svelte, Angular, Flutter, and Vanilla web projects. Use when the user asks for any Lottie/dotLottie/animation work — loaders, success checkmarks, splash screens, empty states, onboarding, micro-interactions. Triggers on keywords like "lottie", "dotlottie", ".lottie", "animasyon ekle", "splash animation", "loader animation", "success animation", "empty state animation".
---

# Lottie Design Skill

You help the user find free Lottie animations and embed them in their project with framework-correct code. Goal: zero friction — install dep, write component, show code, offer preview, all in one shot.

## When to use this skill

Trigger on any of:
- Explicit keywords: `lottie`, `dotlottie`, `.lottie`, `lottiefiles`
- Animation needs paired with framework: "loading spinner for my React app", "splash animation Flutter", "404 empty state animation"
- User pastes a `lottiefiles.com` URL or `lottie.host` URL

Do NOT trigger for:
- CSS animations / Framer Motion / GSAP requests (different domain)
- SVG sprite work
- User asking you to *author* a Lottie JSON from scratch (out of scope — tell them this skill embeds existing animations only)

## Files in this skill

```
SKILL.md                       this file
catalog.json                   curated metadata (id, title, tags, category, jsonUrl, lottieUrl, source, license, author)
catalog.md                     human-readable category index
templates/
  react.tsx.template           @lottiefiles/dotlottie-react snippet
  react-native.tsx.template    lottie-react-native v7 snippet
  flutter.dart.template        lottie pub.dev v3 snippet
  vanilla.html.template        @lottiefiles/dotlottie-wc snippet
scripts/
  extract-url.js               Node: lottiefiles.com page → lottie.host JSON URL
  generate-preview.js          Node: JSON/lottie URL → standalone preview HTML (auto-opens browser)
  fetch-lottie.sh              bash: page URL → download JSON to disk
docs/
  react.md, react-native.md, flutter.md, vanilla.md, search-strategy.md
preview-template.html          base HTML for live preview
```

## Workflow

### Step 1 — Detect project context (no questions)

Read these files to infer everything before asking the user anything:

- `package.json` → check `dependencies` + `devDependencies` for the framework signal:
  - `react-native` → React Native
  - `next` (with or without `react`) → Next.js (a React variant — emits same React template, but local-mode default path is `public/animations/`)
  - `@angular/core` → Angular
  - `vue` → Vue
  - `svelte` or `@sveltejs/kit` → Svelte
  - `react` only → plain React
- `pubspec.yaml` → Flutter project + `lottie` dep
- `angular.json` → Angular workspace
- `svelte.config.js` → SvelteKit
- `nuxt.config.ts` → Nuxt (Vue variant)
- `tsconfig.json` or any `.ts*` file → TypeScript; otherwise JavaScript
- `index.html` at root with no `package.json` → Vanilla
- Existing components in `src/components/animations/`, `src/components/ui/`, `app/components/`, `lib/widgets/` → use the same convention

Only ask the user if multiple frameworks are present (monorepo) and the request doesn't specify which one.

### Step 2 — Install dep FIRST (before any code)

**Install the framework dep at the very start of the workflow** — do not wait until the end, do not just suggest the command. Run it immediately if it's missing. Confirm only if the project's lockfile / package manager is ambiguous.

| Framework | Install command | Skip if |
|---|---|---|
| React / Next.js | `npm i @lottiefiles/dotlottie-react` (or `pnpm add` / `yarn add` based on lockfile) | already in `package.json` |
| React Native | `npm i lottie-react-native` (Expo: `npx expo install lottie-react-native`) | already in `package.json` |
| Vue / Nuxt | `npm i @lottiefiles/dotlottie-vue` | already in `package.json` |
| Svelte / SvelteKit | `npm i @lottiefiles/dotlottie-svelte` | already in `package.json` |
| Angular | `npm i ngx-lottie lottie-web` + register `provideLottieOptions` in app config | already in `package.json` |
| Flutter | append `lottie: ^3.3.2` to `pubspec.yaml` deps + run `flutter pub get` | already in `pubspec.yaml` |
| Vanilla | none — script tag CDN | always |

Detect the package manager:
- `pnpm-lock.yaml` → `pnpm add`
- `yarn.lock` → `yarn add`
- `bun.lockb` → `bun add`
- `package-lock.json` (or none) → `npm i`

Tell the user one line: `Installing @lottiefiles/dotlottie-react…` then run it. If the install fails, surface the exact error and stop.

### Step 3 — Search for animation

**Search order (stop at first good match):**

1. **Catalog first — semantic ranking.** Read `catalog.json` (140 entries). Use semantic understanding rather than literal tag overlap. For each entry, mentally score relevance to the user's request along four dimensions:

   - **Intent match (weight 0.5)**: does the entry's `title` + `category` + `tags` describe what the user actually wants? Examples: "fintech splash" → onboarding/payment/rocket category; "checkout celebration" → success/confetti; "device offline state" → error/no-internet.
   - **Color match (weight 0.2)**: if user mentions a color (TR/EN/ES/DE/FR/JA), check `dominantColor` against the named-color → hex map in `docs/search-strategy.md`. Score 1.0 if same hue family (within ±30° on HSL hue), 0.5 if within ±60°, 0 otherwise. Skip if user mentioned no color.
   - **Style/duration match (weight 0.15)**: short/snappy (`duration < 1s`) vs. atmospheric (`duration > 3s`) vs. neutral. Match against user phrases: "quick"/"snappy"/"hızlı"/"rapide" → short; "smooth"/"atmospheric"/"yumuşak"/"tranquilo" → long.
   - **Size match (weight 0.15)**: prefer smaller `sizeKb` for production-critical contexts ("loader on landing page", "splash on slow connection"). Penalize entries over 200KB unless user specifically asked for "rich"/"detailed"/"high-fidelity".

   Sum the weighted scores; surface the top 3 entries. If the top entry's score < 0.4, treat it as a catalog miss and proceed to step 2.

   **Pre-translate the query** using the i18n keyword maps in `docs/search-strategy.md` (TR/ES/DE/FR/JA → EN) before scoring.

2. **Catalog miss → LottieFiles search index.** WebFetch `https://lottiefiles.com/free-animations/<topic>` (e.g. `/loading`, `/success`). The index page returns 200 and lists `/free-animation/<slug>` links. Extract 3–5 candidate slugs.

3. **Resolve direct URL** (best-effort). Run `node scripts/extract-url.js https://lottiefiles.com/free-animation/<slug>`. Individual animation pages are often gated by Cloudflare; the script detects this and exits with code `6`. When that happens, tell the user: "Cloudflare blocked auto-resolve. Open `<pageUrl>` in a browser, click **Get URL**, paste the `lottie.host` URL here."

4. **CF blocked or LF down → useAnimations fallback.** Use catalog's `ua-*` entries. For names not in the catalog, URL pattern is `https://raw.githubusercontent.com/useAnimations/react-useanimations/master/src/lib/<camelCaseName>/<camelCaseName>.json`. License is CC-BY 4.0 (attribution required).

### Step 4 — Present options

Show 2–3 options using **AskUserQuestion** with rich preview blocks. Each option must include a `preview` field rendered as a metadata card so the user can compare at a glance. Skip the question and pick the top match if user said "just pick" / "best one" / specific id, or if request is unambiguous (e.g. "default").

**Required option shape**:

- `label` — animation title (max 5 words). Add ` (Recommended)` to the first option if you have a clear top pick.
- `description` — `<category> · <license>` (one line, ≤80 chars).
- `preview` — multi-line metadata block. Use this exact format:

```
ID:        <id>
Color:     <dominantColor> ●
Duration:  <duration>s · <frames> frames
Size:      <sizeKb>KB · <w>×<h>
License:   <license><attribution-flag>
Author:    <author>
Source:    <preview-url>
```

The Color line should include a literal Unicode dot (●) immediately after the hex. If `dominantColor` is null, omit the Color line. Replace `<attribution-flag>` with ` (attribution required)` for CC-BY entries, otherwise empty string.

**Also generate a side-by-side preview gallery** before asking — so the user sees the animations playing while they choose:

```
node scripts/generate-preview.js --gallery <slug> '<item1-json>' '<item2-json>' '<item3-json>'
```

Each `<itemN-json>` is a single-line JSON object: `{"id","title","src","color","duration","frames","sizeKb","license"}`. The script writes `preview-<slug>.html` and auto-opens it in the browser. Mention "Bir browser tab'ı açıldı, animasyonları yan yana karşılaştır." in your message before the AskUserQuestion call.

Use **AskUserQuestion** as the primary picker — it handles the "Other" escape hatch automatically.

### Step 5 — Verify URL reachability

`curl -sI <url>` → must be 200. Prefer dotLottie (`.lottie`) over JSON when both exist.

### Step 5.5 — Asset mode (CDN vs local)

Default: **CDN mode** (`src=<url>`). Skill embeds the URL directly in the component. Pros: zero file footprint, always latest version. Cons: runtime network dependency, can break if CDN deletes the file.

Switch to **local mode** if any of these is true (auto-detect, don't ask):
- User says "local", "offline", "indir", "bundle", "embed", "no CDN", "self-host".
- Project has a `public/animations/` or `src/assets/animations/` directory already populated → use the same convention.
- File `sizeKb < 100` AND the entry's source is `github-mirror` (xvrh) — the mirror is essentially a sample repo, prefer pinning a copy.

To switch to local mode:

```
node scripts/download-asset.js <jsonUrl> <projectRoot> [framework] [--dotlottie]
```

Pass `--dotlottie` to also emit a sibling `.lottie` (ZIP-compressed) — typically **50-80% smaller** than the raw JSON, useful for production bundles. Only adds value when the player supports dotLottie (`@lottiefiles/dotlottie-*` packages, the `<dotlottie-wc>` web component, and `lottie-flutter` v3+; **not** `lottie-react-native` v7 which expects `.json`).

The script downloads the asset to the conventional location for the framework:
- React (Vite/CRA): `src/assets/animations/<name>.json`
- Next.js: `public/animations/<name>.json`
- React Native: `src/assets/animations/<name>.json`
- Flutter: `assets/animations/<name>.json` + auto-patches `pubspec.yaml` asset registration
- Vanilla: `animations/<name>.json`

It prints a JSON summary including `importHint`. Use that hint when filling the template `{{src}}` placeholder.

For React, the `{{src}}` value becomes one of:
- CDN mode:   `"https://lottie.host/<uuid>/<id>.json"`
- Local mode: imported asset → set `{{src}}` to a JSX expression like `{animationData}` and add the import on top:
  ```tsx
  import animationData from '@/assets/animations/<name>.json';
  // then: <DotLottieReact src={animationData} ... />
  ```

For React Native local mode, use `require('./assets/animations/<name>.json')` as the source.
For Flutter local mode, use `Lottie.asset('assets/animations/<name>.json')` instead of `Lottie.network(...)`.
For Vanilla local mode, point `<dotlottie-wc src="animations/<name>.json">` to the relative path.

Always tell the user which mode you used and why, in one line at the top of the success summary.

### Step 6 — Generate code

Read the right template based on framework + TS/JS detection:
- React / Next + TS → `templates/react.tsx.template` (write as `.tsx`)
- React / Next + JS → same template, write as `.jsx` and strip the `interface` line + Props type annotation
- React Native + TS → `templates/react-native.tsx.template` (`.tsx`)
- React Native + JS → same, strip TS bits, write `.jsx`
- Vue / Nuxt → `templates/vue.vue.template` (`.vue`)
- Svelte / SvelteKit → `templates/svelte.svelte.template` (`.svelte`)
- Angular → `templates/angular.ts.template` (`.component.ts`); also need `kebabName` placeholder (e.g. `loading-pulse`)
- Flutter → `templates/flutter.dart.template` (`.dart`)
- Vanilla → `templates/vanilla.html.template` (raw HTML snippet)

**Placeholder fill rules:**
- `{{sourceUrl}}` — original page or repo URL (for license header)
- `{{componentName}}` — PascalCase from animation title (e.g. `SuccessCheckAnimation`, `LoadingPulse`)
- `{{license}}` — entry's `license` field
- `{{attributionNote}}` — for CC-BY entries: ` (attribution required: see footer credit below)`; for Lottie Simple License: empty string
- `{{size}}` — user-specified size or default 200
- `{{author}}` — entry's `author` field (used in attribution string)

**React-specific (CDN vs local mode):**
- CDN mode:
  - `{{importLine}}` → empty string
  - `{{srcExpr}}` → `"<https URL>"`  (note quotes — produces `src={"https://..."}`, equivalent to `src="https://..."`)
- Local mode (after `download-asset.js`):
  - `{{importLine}}` → `import animationData from '<relative-path>';`
  - `{{srcExpr}}` → `animationData`  (no quotes — produces `src={animationData}`)

**React Native, Flutter, Vanilla**: keep using the framework templates as-is. For local mode in those frameworks, swap the URL source for `require(...)` (RN), `Lottie.asset(...)` (Flutter), or relative path (Vanilla).

**Path resolution:**
- Look for an existing animations dir: `src/components/animations/`, `src/components/ui/animations/`, `app/components/animations/`, `lib/widgets/`, `src/lib/components/animations/` (SvelteKit), `src/app/animations/` (Angular)
- If none exists, create:
  - React/RN/Vue/Svelte: `src/components/animations/`
  - Angular: `src/app/animations/`
  - Flutter: `lib/widgets/animations/`
- Filename:
  - React/RN: `{{componentName}}.tsx` or `.jsx`
  - Vue: `{{componentName}}.vue`
  - Svelte: `{{componentName}}.svelte`
  - Angular: `{{kebabName}}.component.ts`
  - Flutter: `{{kebabName}}.dart`
  - Vanilla: print snippet or write to a standalone HTML file

**ALWAYS show the generated code in chat** in a fenced code block right after writing the file. Do not just say "wrote the file." The user must see what landed.

### Step 7 — Attribution string (if CC-BY)

If the chosen entry has `license: "CC-BY-4.0"` (any `ua-*` entry), output a ready-to-paste attribution snippet:

```
Animation "<title>" by <author> (https://useanimations.com), licensed under CC-BY 4.0.
```

Tell the user: "Paste this in your footer / credits / about page. CC-BY requires visible attribution for commercial use."

For `Lottie Simple License`, no attribution string is needed — say so.

### Step 8 — Offer preview

After writing the file, always offer:
> Preview üreteyim mi? `preview-<componentName>.html` browser'da açılır.

If the user agrees, run `node scripts/generate-preview.js <url> <componentName>`. The script auto-opens the file in the default browser (Windows: `start`, macOS: `open`, Linux: `xdg-open`).

### Step 9 — Final summary

**Always start the final message with a branded success line**, then the 3-line summary:

```
🎬 Lottie skill ile <açıklama> başarıyla eklendi.

✅ Installed: <package>
✅ Component: <relative-path>  →  <ComponentName />
✅ License: <license> [+ attribution string if CC-BY]
```

`<açıklama>` examples:
- "loading animasyonu" / "loader animation"
- "success checkmark" / "başarı animasyonu"
- "splash screen rocket" / "splash roket animasyonu"
- "<componentName> component'ı"

Match the language of the user's prompt (TR / EN / ES / DE / FR / JA) — see `docs/search-strategy.md` for keyword maps. If the user's prompt was Turkish, the branded line stays Turkish; if English, English; etc. The 3 ✅ lines stay English (technical labels).

Examples:
- TR: `🎬 Lottie skill ile loading animasyonu başarıyla eklendi.`
- EN: `🎬 Successfully added a loading animation with the Lottie skill.`
- ES: `🎬 Animación de carga añadida con éxito mediante el skill Lottie.`

## Component prop interface (standardized)

All generated components accept a single `size` prop (square — width = height = size) plus optional `className` (web) or `style` (RN/Flutter):

```tsx
<LoadingPulse size={160} />
<SuccessCheck size={120} className="mx-auto" />
```

Default `size` = 200 if not provided. Templates already export this interface.

## Rules

- **No premium animations.** If a URL contains `/premium/` or the page indicates "Pro" / "Paid", skip it and find a free alternative.
- **Always include a license header** in generated files. Format: `// Source: <pageUrl> — <license>`
- **For CC-BY entries always output a separate attribution string** for the user to paste in footer/credits.
- **Prefer dotLottie over JSON** for production (smaller payload).
- **Don't inline JSON > 50KB into source files.** Always use a URL or place under a static assets folder.
- **Auto-install deps** at Step 2 — don't end the workflow with "now run npm i". Run it yourself unless the user explicitly said "don't install".
- **Don't fabricate `lottie.host` URLs.** Only use URLs verified via catalog or `extract-url.js`.
- **License copyleft note**: if the user *modifies* an animation, the modified file must retain the Lottie Simple License. Mention this once if the user asks about editing.

## Catalog notes

- ~48 verified entries across 9 categories (`loader`, `success`, `error`, `empty-state`, `onboarding`, `social-share`, `payment`, `ecommerce`, `character`).
- 38 entries from useAnimations (CC-BY 4.0, attribution required), 10 from LottieFiles community (Lottie Simple License, no attribution required).
- If a catalog entry's URL stops working, fall back to web fetch and update the entry inline (edit `catalog.json`).

See `docs/search-strategy.md` for matching heuristics + i18n keyword map (TR→EN). See `docs/<framework>.md` for advanced per-framework usage (controllers, segments, hover triggers, asset bundling).
