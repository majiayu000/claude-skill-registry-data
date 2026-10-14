---
name: slidev-retro-deck
description: >
  Trigger: slidev, slides, presentation, deck, retro console, CRT, terminal
  theme. Build a Slidev presentation with a retro-console visual identity —
  three packaged themes (crt-phosphor, dos-terminal, synthwave-arcade), each
  with day and night schemes — themed Mermaid diagrams, and a mandatory
  PNG-export verification loop that checks every slide for overflow. También
  se activa en castellano: "hazme una presentación con Slidev", "presentación
  estilo consola retro".
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.2.0"
---

# Slidev Retro Deck

Build 16:9 Slidev decks with a retro console identity (scanlines, tube glow, terminal type, blinking cursor) and verify every slide visually before declaring the deck done. Three packaged themes live under `assets/themes/`, each with a **day** (light console) and **night** (dark console) scheme selected per deck via headmatter `colorSchema`:

| Theme | Night | Day | Fonts (headings / body) |
|---|---|---|---|
| `crt-phosphor` | green/amber phosphor on black | phosphor ink on paper-green | VT323 / JetBrains Mono |
| `dos-terminal` | yellow/cyan on Borland blue | navy ink on ivory paper | Silkscreen / IBM Plex Mono |
| `synthwave-arcade` | magenta/cyan neon on deep purple | sunrise pastel arcade | Press Start 2P / Space Mono |

The workflow applies to any Slidev deck; the packaged identity is the retro console.

## Activation

- The user asks for a slide deck or presentation, especially with Slidev or a retro/terminal/Matrix look.
- Create each deck in its own directory (for example `.ai/slides/<deck-name>/`), never inside a managed component tree.

## Workflow

1. **Scaffold** — copy `assets/scaffold/package.json` and `assets/scaffold/pnpm-workspace.yaml` into the deck directory, then install with pnpm. `playwright-chromium` (needed by `slidev export`) only downloads because the workspace file allows its build script. `npm` may be aliased to pnpm in some setups, so prefer explicit pnpm commands. Run `npx slidev slides.md` for a hot-reloading dev server.
2. **Headmatter** — start from `assets/slides-skeleton.md`. Non-obvious facts: the seriph theme maps the `fonts: serif` slot to **headings**, so the display font goes there (each theme's font pair is listed in the skeleton comments and the theme CSS header); `sans`/`mono` carry the body mono font; `colorSchema` picks the scheme — `dark` = night console, `light` = day console, `auto` = system preference plus the UI toggle; `background: none` lets the CSS gradient show through.
3. **Design system** — pick a theme under `assets/themes/` (`crt-phosphor`, `dos-terminal`, `synthwave-arcade`) and copy its `style.css` to the deck root (Slidev auto-loads it). Every theme is token-based: day palette on `:root`, night overrides on `html.dark`, so both schemes come from the same file. Each defines two semantic accents `--accent-a`/`--accent-b`: assign each accent to one topic/domain of the deck and keep the mapping consistent everywhere: text (`.tx-a`/`.tx-b`), borders (`.bd-a`/`.bd-b`), chips, stamps, and diagram nodes.
4. **Stamps** — every slide carries an absolutely positioned top-right badge naming its section/topic, placed right after the slide separator: `<div class="stamp stamp-a">topic</div>`. Slides spanning both topics use `.stamp-both` with one span per accent.
5. **Author credit** — copy `assets/global-bottom.vue` to the deck root; Slidev renders it on every slide, and the theme's `.credit` class pins the handle small and dimmed at the bottom-left. Default handle is `@andresnator`; edit the copied file if the deck belongs to someone else.
6. **Mermaid theming** — copy the chosen theme's `mermaid-setup.ts` to `setup/mermaid.ts`. It must export a plain function; never import `@slidev/types` (not a direct dependency, strict pnpm cannot resolve it, and the resulting vite error renders on the first slide). Each setup carries a day and a night palette and picks one at diagram render time from Slidev's scheme class; a live scheme toggle does not re-render existing diagrams (reload), and exports are always consistent. To accent nodes, tag them in the fence with `class <id> a`, `class <id> b`, or `class <id> aux` — the setup's `themeCSS` styles those classes in the scheme-correct palette. Never use `classDef` in fences: mermaid cannot parse `var()` there, and hardcoded hexes break the day/night switch.
7. **Diagram sizing** — apply the playbook below; wide flows are `flowchart LR`, never `TD`.
8. **Overflow discipline** — mono fonts are wider and taller than proportional ones. Dense slides get per-slide frontmatter `class: text-sm`; footers get `text-xs`; watch the last table row and the final line of any box near the bottom edge.
9. **Verification loop (mandatory)** — never declare the deck done without it:
   1. Parse every mermaid block with `assets/mermaid-check/check.mjs` (install its deps from the sibling `package.json` in a scratch dir): `node check.mjs <deck>/slides.md`.
   2. Export: `npx slidev export slides.md --format png --output slide-export --timeout 90000`.
   3. Visually inspect **every** PNG for clipping, overflow, and legibility; fix and re-export until clean. `--range N` iterates faster but wipes the output directory — always finish with a full export.

## Diagram sizing playbook

Apply in order; stop when the diagram fits as large as possible:

| Lever | How |
|---|---|
| Orientation | `flowchart LR` for pipelines; `TD` overflows 16:9 |
| Scale | fence option `{scale: 0.4–0.6}` — mono fonts need the lower end |
| Spacing | `{scale: X, flowchart: {nodeSpacing: 35, rankSpacing: 36}}` — fence options merge into `mermaid.initialize` |
| Label trim | shorten the widest node label; move the info to a caption under the diagram |
| Width | `.mermaid` in the theme's `style.css` reclaims the slide's side padding via negative margins |
| Composition | diagram-only slides get frontmatter `class: diagram-center` to center vertically |

## Hard rules

- `setup/mermaid.ts` exports a plain function — no `@slidev/types` import.
- No "done" without the full PNG inspection of every slide, in the scheme(s) the deck will actually use.
- One accent = one meaning, everywhere (text, borders, chips, stamps, diagram nodes).
- No color literals in mermaid fences: accent nodes with `class <id> a|b|aux` (styled by the setup's `themeCSS`), never `classDef` — `var()` fails to parse and hexes break the day/night switch.
- Respect each theme's heading type scale — pixel fonts (Silkscreen, Press Start 2P) are far wider than VT323 and overflow at CRT sizes.
- Presenter notes are a trailing `<!-- ... -->` HTML comment inside the slide.
- Keep the `prefers-reduced-motion` guard on the blinking cursor.

## Resources

- `assets/themes/<name>/style.css` — day/night token-based theme (scanlines, glow, stamps, chips, diagram helpers).
- `assets/themes/<name>/mermaid-setup.ts` — matching day/night mermaid palettes for `setup/mermaid.ts`.
- `assets/slides-skeleton.md` — headmatter plus cover, content, and diagram slide examples.
- `assets/global-bottom.vue` — per-slide bottom-left author credit (styled by each theme's `.credit`).
- `assets/scaffold/` — `package.json` and `pnpm-workspace.yaml` templates.
- `assets/mermaid-check/` — parse validator for mermaid blocks.
- `references/troubleshooting.md` — symptom → cause → fix catalog from real failures.
