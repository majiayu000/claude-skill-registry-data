---
name: reveal-js-architect
version: 1.0.2
description: reveal.js 6.0.1 presentation architecture — section/fragment structure, HTML vs Markdown-mode authoring, theming, plugin config, Reveal.initialize() options, vanilla setup, React extension via @revealjs/react 0.2.1. Use when building, structuring, or reviewing a reveal.js deck.
---

# Reveal.js Architect

Targets **reveal.js 6.0.1** (vanilla) with an extension for **@revealjs/react 0.2.1**. Produces actual reveal.js source (HTML/JS deck scaffold or Markdown-mode slides) — never a slide-spec document; for that, see [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md) (unrelated output format, not a dependency). Full project skeletons in [RECIPES.md](RECIPES.md); pinned versions in [STACK.md](STACK.md).

## 1. Scope & output

- **Output is real reveal.js source** — `index.html` + `<section>` markup, or Markdown-mode slides, plus any `main.js` config. Never a slide-spec `.md` document.
- **Vanilla is the default target.** Reach for the React extension (§9) only when the deck already lives inside a React app or needs component-driven slide content (data-fetched slides, shared design-system components).
- **This skill does not write slide copy for the user.** It structures decks; content (titles, bullets) comes from the user or from a spec produced by [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md).

## 2. Interview-first protocol

**Never scaffold a deck without finishing the interview.** Ask in order; wait for each answer:

1. **Topic + slide count/duration** — what's the deck about, how long is the talk.
2. **Vanilla or React?** — plain HTML/JS project, or embedded in an existing React app via `@revealjs/react`.
3. **Authoring mode** — HTML `<section>` markup, or Markdown-mode (`data-markdown`)? See §4 for the trade-off.
4. **Theme** — a built-in theme (§5), or a custom CSS override.
5. **Plugins needed** — syntax highlighting, speaker notes, math, zoom, search (§6).
6. **Delivery** — static HTML file opened directly, or a bundler-based project (npm + Vite)?

## 3. Deck structure conventions

- **Horizontal `<section>` = new topic; nested vertical `<section>` = a sub-point of the same topic.** Don't nest vertical slides more than one level deep — audiences lose the "back" direction.
- **One idea per slide**, same discipline as [demo-presentation-architect §3](../../personal/demo-presentation-architect/SKILL.md) — split rather than cram.
- **Fragments (`class="fragment"`) reveal progressively within a slide** — use for build-up bullets or step-by-step diagrams, not as a substitute for splitting a slide.
- **Speaker notes** go in `<aside class="notes">` inside each section — visible only in speaker view (`S` key), never on the audience-facing screen.
- **`data-transition` overrides per-slide** when a specific slide needs a different transition than the deck default — use sparingly, inconsistent transitions read as sloppy.
- **Never set `position`, `overflow`, or `display` directly on `<section>`.** reveal.js owns those properties on slide elements to drive its stacking and transition system (e.g. `position: absolute` on non-present slides, toggling `display` via the `.present` class). Custom CSS that overrides them breaks navigation silently — slides go blank on advance with no console error. Style content *inside* the section (a wrapper `<div>`), never the section itself.
- **Make content fit by default; treat `overflow-y: auto` as a fallback, not a strategy.** For a live talk, a presenter forced to scroll mid-slide is a UX failure. When a slide is too dense, first tighten typography/spacing or split the slide (§3 "one idea per slide") — reach for internal scroll only as a defensive catch for unexpectedly long content, not as the default answer to "it doesn't fit."

## 4. Content authoring mode

- **HTML sections** — full control over markup, required when a slide embeds custom components, tables with rowspan/colspan, or fine-grained fragment ordering.
- **Markdown-mode (`data-markdown`)** — faster to author, easier to diff/review, preferred for text-heavy decks (bullets, code blocks, quotes). Separate slides within one block with `---`, vertical slides with `--`.
- **Don't mix modes within one deck** unless one section genuinely needs HTML control the rest doesn't — pick a default per deck and stay consistent.
- **External Markdown files** (`data-markdown="slides.md"`) keep content in version control separate from the shell; prefer this for long text-heavy decks over inline `<script type="text/template">`.

## 5. Theming & assets

- **Start from a built-in theme** (`black`, `white`, `league`, `sky`, `night`, `serif`, `simple`, `solarized`, `moon`, `beige`, `blood`, `dracula`) — never build from scratch unless brand requirements demand it.
- **Custom overrides go in a separate stylesheet loaded after the theme**, not by editing the theme file in place — keeps upgrades painless.
- **Images and media live alongside the deck**, referenced with relative paths; large video/audio should be lazy-loaded via `data-src` and `data-lazy-load` conventions to keep initial load fast.
- **Watch compounding `em` on nested elements that each set their own `font-size`.** If a dense region (a wide table, a sidebar) shrinks via `font-size: 0.4em` and a generic deck-wide rule sets a child element's `font-size` in `em` too (e.g. `p { font-size: 0.55em }`), the two multiply rather than add — `0.4 × 0.55 ≈ 0.22em`, far smaller than either value alone suggests. When nesting a shrunk region inside deck-wide `em` typography, size the inner region in `rem` or a fixed unit, or explicitly reset the child's `font-size` to `1em`.

## 6. Plugins

Standard plugin set, loaded and registered in `Reveal.initialize({ plugins: [...] })`:

- **`RevealHighlight`** — syntax-highlighted code blocks; pair with `<pre><code data-line-numbers>` for line-focus during a talk.
- **`RevealNotes`** — enables the speaker-notes view (`S` key); always include if `<aside class="notes">` is used anywhere.
- **`RevealMarkdown`** — required whenever any slide uses `data-markdown`.
- **`RevealMath`** (KaTeX flavor preferred over MathJax for load speed) — only when the deck has actual formulas.
- **`RevealZoom`** — Alt/Option-click zoom into any element; low cost, safe default to include.
- **`RevealSearch`** — only for long reference decks the audience will navigate themselves, not for live-talk decks.

Don't register a plugin the deck doesn't use — each one adds a script tag and init cost.

## 7. Config conventions

- **Sane defaults to keep**: `hash: true` (deep-linkable slides), `controls: true`, `progress: true`, `center: true` unless the deck's layouts are top-aligned by design.
- **`transition`** — `slide` is the safe default; reserve `fade`/`zoom`/`convex` for decks where the transition itself carries meaning (rare).
- **`width`/`height`** — leave at defaults (1280×720) unless the deck targets a specific screen ratio; reveal.js auto-scales via its `viewDistance` and CSS scaling, don't hardcode pixel layouts inside slides.
- **`<section>` only ever gets `width: 100%` from reveal.js — never `height`.** Slide height is intrinsic (fits content), so any inner wrapper using `height: 100%` resolves against nothing and collapses to content size — backgrounds don't cover the canvas, and `flex: 1; overflow-y: auto` panels have no real box to scroll within. If a slide's layout needs a fixed canvas height (full-bleed background, scrollable body panel), set it in **px on the inner wrapper**, matching `Reveal.initialize({ height })` exactly (e.g. a `--slide-height: 720px` custom property) — never `%` and never on `<section>` itself.
- **`slideNumber`** — enable for reference/training decks the audience revisits; skip for live pitch decks where it's visual clutter.
- **If the theme's background isn't pure white, override `.reveal-viewport { background-color: ... }` to match it.** When the window's aspect ratio doesn't match the configured `width`/`height`, reveal.js letterboxes with `.reveal-viewport`'s own background — white by default in `reveal.css` — not the theme's. On a non-white theme this shows as an ugly border around the logical canvas.

## 8. Vanilla setup

CDN link for a single-file deck, or an npm + Vite project for anything version-controlled and multi-file. Full project skeleton (folder tree, `package.json`, `main.js` with plugin registration) in [RECIPES § Vanilla project skeleton](RECIPES.md#vanilla-project-skeleton).

## 9. React extension (@revealjs/react)

- **Use when** the deck lives inside an existing React app, or slides need live component state (charts fed by app data, shared design-system components) rather than static markup.
- **`<Reveal>` wraps `<Slide>` children** — each `<Slide>` maps to a `<section>`; fragments become a `<Fragment>` component, not the `class="fragment"` attribute.
- **Reveal's imperative API (`Reveal.initialize`, plugin registration) is wrapped by the library's own hooks/props** — don't reach into the vanilla API directly except for edge cases the wrapper doesn't expose.
- **Don't reach for this extension by default** — see [react-architect](../react-architect/SKILL.md) for general React conventions; this section only covers the reveal.js-specific integration surface. Full component skeleton in [RECIPES § React project skeleton](RECIPES.md#react-project-skeleton).

## 10. Anti-patterns & review checklist

- Wall-of-text slides (no fragment/split discipline) — same failure mode as [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md) flags for spec decks.
- Mixing HTML and Markdown-mode within one deck without a reason.
- Registering plugins that aren't used anywhere in the deck.
- Speaker notes that duplicate on-slide text instead of adding presenter-only context.
- Hardcoded pixel layouts fighting reveal.js's auto-scaling instead of using its centering/sizing config.
- Custom CSS setting `position`, `overflow`, or `display` on `<section>` — silently breaks the stacking/transition system (blank slides on advance, no console error).
- An inner wrapper using `height: 100%` (or `flex: 1` inside it) to fill the slide — `<section>` never has a set height, so this collapses to content size instead of the canvas. Use a fixed px height matching `Reveal.initialize({ height })`.
- `overflow-y: auto` used as the primary fix for a slide that doesn't fit, instead of tightening typography/spacing or splitting the slide — forces the presenter to scroll mid-talk.
- Nested `em` font-sizing where a shrunk region (table, sidebar) and a deck-wide child rule both use `em` — the values multiply, producing unexpectedly tiny text.
- Non-white theme with no `.reveal-viewport` background override — letterboxing shows the default white viewport background instead of the theme's.
- React extension reached for out of habit when a static vanilla deck would do.

Before handing off: every slide has a clear single idea, plugins list matches what's actually used, transitions are consistent unless a specific slide has a stated reason to diverge, and speaker notes (if any) are present only where they add value.
