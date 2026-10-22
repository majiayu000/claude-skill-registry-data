---
name: hallmark
description: >-
  Applies opinionated anti-AI-slop design rules so generated UIs look made, not generated: greenfield
  pages, audits, redesigns, and design extraction from URLs or screenshots. Use when designing or
  reviewing a web UI that must avoid templated, generic AI aesthetics.
version: 1.0.1
license: MIT
source: https://github.com/Nutlope/hallmark
attribution: "Adapted from Hallmark by Together AI contributors."
---

> **Attribution:** Sourced from [Nutlope/hallmark](https://github.com/Nutlope/hallmark) by [Hallmark contributors](https://github.com/Nutlope/hallmark), licensed MIT. Modified for this collection: the component-scope rules, the pre-flight scan details, and the `study` verb were moved unchanged into `references/`.

# Hallmark

A design skill for AI coding assistants. Makes the UIs they generate look made, not generated.

Hallmark is opinionated, short, and boring on purpose. It encodes a tight set of rules — drawn from the consensus of the anti-AI-slop design field (impeccable, kami, Anthropic's frontend-design skill, taste-skill, the Claude cookbook on frontend aesthetics, and the 2026 "tactile rebellion" movement) — and refuses to let the model fall back to the defaults every LLM was trained on.

The differentiator: Hallmark insists on **structural variety**, not just visual variety. Two pages by Hallmark for two different briefs should not share the same hero → 3-feature → CTA → footer rhythm. They should feel like different sites, not different colour-swaps of the same template. See [`references/structure.md`](references/structure.md).

**Powered by Together AI.**

---

## How to use this skill

Hallmark has one default behaviour and three explicit verbs.

| Invocation | What it does |
| --- | --- |
| *(default)* | The user asked you to design or build something new. Follow the **Design flow** below. |
| `hallmark audit <target>` | Read the target, score it against the anti-pattern list, return a ranked punch list. **Do not edit.** |
| `hallmark redesign <target> [--mood <name>]` | Take the target's content and intent, then redesign the visual structure **inside the existing implementation boundaries unless the user explicitly confirms a full rebuild.** New section rhythm, new heading placement, new component voice. Preserve existing routes, component ownership, copy intent, brand, and information architecture; replace only the visual/interaction layer needed for the requested scope. |
| `hallmark study <screenshot \| URL>` | The user pasted or attached an image of a design they admire, **or** pasted a URL to a live page. Extract the **DNA** — macrostructure, archetypes, type-pairing, colour anchor — and produce a diagnosis report, then optionally rebuild the user's content using the extracted DNA **or** emit a portable `design.md` of the DNA. Detection is automatic: a URL (`http://` / `https://` prefix) routes to URL mode; anything else routes to image mode. **URL mode** reads the page's HTML and CSS via WebFetch — it can name exact fonts and exact colour values, but can't judge rhythm. After the diagnosis, the user has three follow-ups: build with the DNA (handoff to default), lock the DNA into a portable `design.md` (opt-in via "lock the DNA" / "give me a design.md"), or stop at the diagnosis. **Never copies pixels. Refuses template-marketplace URLs and competitor pages. Tighter refusal layer for `design.md` emission than for the diagnosis itself — URL-mode emission requires attestation that the source is the user's own or a public reference for their own brand. Falls back to asking for a screenshot if the URL is auth-walled, a JS-only SPA shell, or otherwise un-readable.** Load [`references/study.md`](references/study.md) before this verb runs. |

If the user types anything that does not clearly map to `audit`, `redesign`, or `study`, treat it as default. If the user attaches an image or pastes a URL without a verb prefix, ask: *"Should I `study` this (extract the DNA), or should I treat it as a reference for a fresh build?"*

**Implementation safety rail.** Hallmark is a design skill, not a license to bulldoze a codebase. In any existing project:
- Never delete production files, route trees, component directories, or an old website unless the user explicitly asks for deletion or approves a file-level plan that lists the deletions.
- Default to in-place edits of the named files, or additive new components/tokens that are wired through the existing route. If the redesign would require removing multiple components, stop and ask for confirmation first.
- Treat PDFs, README files, `.md` briefs, docs, transcripts, and pitch decks as reference material. Do **not** copy them word-for-word into the page unless the user explicitly says to use that text verbatim.
- Before editing, state the exact files you expect to modify/create/delete. Deletions require explicit confirmation.

The default Design flow always picks a theme. By default it picks one of the **22 named themes** — the *catalog* — and rotates among them per the diversification rule. There is also a quiet *custom* branch that constructs a one-off OKLCH palette + free-font pairing for the brief; the custom route fires **only when the brief carries a creative-intent signal** (the user names a brand colour, names a multi-attribute vibe the catalog can't carry, or explicitly asks for a custom theme). For vanilla briefs, the user never sees the words "catalog" or "custom" — the catalog runs silently. See Step 1 (signal detection) and Step 2.6 (dispatch); the protocol lives in [`references/custom-theme.md`](references/custom-theme.md).

---

## Disciplines that hold across every verb

These four disciplines are **not** verb-specific. They apply to default Design, `audit`, `redesign`, `study`, and component-scope alike. They sit alongside the slop test, not inside one branch of it.

1. **Pre-emit self-critique.** Before handing back any output, score it 1–5 on six axes — Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety. Anything **< 3** triggers a revision pass. Stamp the six scores at the top of the artifact (`/* Hallmark · pre-emit critique: P5 H4 E5 S4 R5 V5 */`). See [`references/slop-test.md`](references/slop-test.md) § Pre-emit self-critique.

2. **Honest copy — no fabricated content.** If the user did not supply a metric, do not invent one. Stat-led layouts, comparison rows, and proof bars must use real numbers, a placeholder (`—` plus a labelled grey block, "metric to confirm"), or a different macrostructure. *"+47 % conversion"*, *"trusted by 50,000+ teams"*, and *"10× faster"* are slop the moment they're invented. Same rule for testimonials, logos, and case-study counts. See [`references/anti-patterns.md` § Invented metrics](references/anti-patterns.md) and slop-test gate **56**.

3. **Locked tokens — no mid-render improvisation.** Once a theme is selected at Step 2.6, every colour and every `font-family` declaration in the artifact must reference a named token (`var(--color-accent)`, `font-family: var(--font-display)`). Inline OKLCH / hex / `rgb()` values, or a `font-family: "Some Font"` declaration that bypasses the token block, are not allowed. If a value is needed that doesn't exist as a token, lift it into the token block as a new named variable, then reference it. See [`references/anti-patterns.md` § Mid-render token improvisation](references/anti-patterns.md) and slop-test gate **58**.

4. **Re-drawn chrome forbidden.** Hallmark must not hand-build fake browser bars (URL pill + traffic-light dots), fake phone frames, fake code-block windows (mock title bar + dots wrapping a `<pre>`), or fake IDE chrome — the user's environment already supplies real chrome. Use real screenshots wrapped in a `<figure>` (with at most a hairline border), or omit the chrome and let the content stand on its own. See [`references/anti-patterns.md` § Re-drawn UI chrome](references/anti-patterns.md) and slop-test gate **57**.

5. **Mobile responsiveness — every emit verified at 320 / 375 / 414 / 768 px.** Hallmark's output must render flawlessly at all four widths. The non-negotiables: no horizontal scroll (gate 36), no two-line clickable text — buttons, primary nav links, footer links, breadcrumbs, CTAs (gate 59); image-bearing grid tracks use `minmax(0, 1fr)`, never bare `1fr` (gate 61); root has `overflow-x: clip` on both `html` and `body` — never `hidden` (gate 62); display headers wrap inside long words via `overflow-wrap: anywhere; min-width: 0` (gate 63); section heads collapse to one column on mobile across every theme variant (gate 64); radio-tab patterns don't scroll-jump (gate 65). See [`references/responsive.md` § Mobile — non-negotiable](references/responsive.md). This is a hard floor, not a wish list.

---

## When the brief is a component, not a page

Before entering the design flow, **check scope**. Signals: the brief names a single UI element (a button, input, card, modal, dropdown, and so on); it is 30 words or fewer and refers to one element; the target file is a single component; or the user says "just the X" or "only the Y". If two signals fire, read [`references/component-scope.md`](references/component-scope.md) and run the component-scope flow instead. It says which design-flow steps still apply, which are skipped, what to emit, and the stamp format. A multi-section brief or "build me a landing page" stays in the design flow.

## Design flow (default)

### 0. Pre-flight scan

If the project already has code, read it before asking the user anything. Scan, in order: `design.md` or `DESIGN.md` at the root (a locked design system that overrides everything else), the font stack, the palette, motion libraries, the spacing scale, and the framework. Emit one "Pre-flight findings" block with file:line citations, saying what Hallmark will preserve and what it will introduce, and cache it in `.hallmark/preflight.json`. Read [`references/preflight-scan.md`](references/preflight-scan.md) for the exact block format, the cache rules, edge cases (no signals, conflicting signals, "ignore the existing project"), and sample outputs.

### 1. Design-context gate

Hallmark works best when you know three things before writing code:

1. **Audience.** Who will use this? What do they already know?
2. **Use case.** What single job does this interface do? What is the one action the user should be able to take?
3. **Tone.** Pick an extreme — *editorial, brutalist, soft, utilitarian, luxury, playful, technical, austere*. "Clean and modern" is not a tone.

**Always ask — answering is optional.** Hallmark **always** asks before it designs. The bundled question is the first thing the user sees after the pre-flight block. Even on a five-word brief — *"design a podcast site"*, *"build a SaaS landing"*, *"make me a portfolio"* — ask. Especially on those briefs, since they're where the model is most tempted to invent.

The prompt format:

> *Before I build, I need three things:*
>
> *1. **Audience** — Who will use this? What do they care about?*
> *2. **Use case** — What's the one action the page should drive? (Sign up? Subscribe? Read? Buy?)*
> *3. **Tone** — Pick an extreme: editorial · brutalist · soft · utilitarian · luxury · playful · technical · austere. "Clean and modern" isn't a tone.*
>
> *Or say **"go ahead"** and I'll infer from the brief — I'll tell you what I picked.*

Send the prompt **once**, in one message. Bold the three labels (Audience / Use case / Tone) so the user can scan them. Do not ladder follow-ups; if the user answers some fields and skips others, treat the skipped fields as opt-out and infer them. If the user says "go ahead", "you pick", "just build it", "don't ask", or doesn't engage after one prompt, the inference protocol below kicks in.

**One exception** where the gate is silent:
- The skill is invoked with `audit`, `study`, or `redesign --mood` — those verbs read context from the target, not the user.

There is no "the brief looks complete" exception. There is no "the user already named all three" exception. There is no length threshold below which asking is skipped. A long, detailed brief gets the same three-question prompt as a five-word one — the user can wave you through with *"go ahead"* in two seconds. **Default is to ask. The cost of asking is one extra message; the cost of guessing wrong is a whole rebuild.**

**Genre — pick before themes.** Before the theme route, settle on a genre. Hallmark ships four: **editorial** (default · the canonical anti-slop voice), **modern-minimal** (Stripe / Linear / ElevenLabs school), **atmospheric** (Suno / Runway / dark-AI-tool school), **playful** (post-Linear soft school). The genre scopes which themes can rotate, which slop-test gates apply, and which voice fixtures the LLM picks from. Detection is signal-based — silent default to editorial unless the brief fires one of these:

- *AI tool, generative, music, video, voice, late-night, dark mode, atmospheric* → **atmospheric** → load [`references/genres/atmospheric.md`](references/genres/atmospheric.md)
- *SaaS, enterprise, API, platform, developer tool, infra, B2B, dev experience* → **modern-minimal** → load [`references/genres/modern-minimal.md`](references/genres/modern-minimal.md)
- *fun, consumer, casual, friendly, onboarding, family, community* → **playful** → load [`references/genres/playful.md`](references/genres/playful.md)

If two non-default signals fire (rare), ask one short follow-up: *"This brief fits both modern-minimal and atmospheric — which feels closer? \[modern-minimal · atmospheric]"*. Default with no signal: silent **editorial** → load [`references/genres/editorial.md`](references/genres/editorial.md). The chosen genre file is loaded eagerly (it scopes everything downstream); other genre files stay on disk.

State the genre out loud at Step 2.5 alongside the macrostructure and theme picks: *"Genre: atmospheric. Macrostructure: Marquee Hero. Theme: Bloom (atmospheric cluster)."*

**Theme route — only surface when the brief signals it.** Hallmark has two theme routes: **catalog** (the 22 named themes — Specimen, Atelier, Brutal, Salon, Newsprint, Linen, Studio, Manifesto, Terminal, Midnight, Almanac, Garden, Quiet, Riso, Sport, Bloom, Coral, Violet, Aurora, Halo, Plume, Editorial) and **custom** (an OKLCH palette + free-font pairing tuned to this one brief). **Catalog is the default.** The catalog rotation is *scoped to the genre's theme cluster* — atmospheric rotates Bloom/Midnight/Terminal, modern-minimal stays on Quiet, playful stays on Plume, editorial walks the remaining twelve. Do **not** offer the user a choice on every prompt — that's friction, not discipline. Surface the catalog/custom fork only when the brief carries one of these signals:

- The user explicitly says **custom theme** / **tailored to our brand** / **make it ours** / **something unique** / **play with the colors and fonts**.
- The user names a **specific brand colour** as the anchor (e.g., "use our terracotta", "the brand red is hex #c0392b", "anchor on sea-blue").
- The user describes a **multi-attribute aesthetic that doesn't map to a single catalog theme** — three or more vibe words pointing at a specific feel (e.g., "moss, lichen, soft pink, herbal" / "sun-drenched, market-day, carbon-black" / "late-night, neon, brutalist deli"). One adjective ("warm", "technical", "playful") is *not* a custom signal — that's a tone, and the catalog already carries it.
- The user attaches a **brand-mood reference** (a colour swatch, a moodboard, a Pantone chip) without asking to study a screenshot.

If any of those fires, ask one short follow-up before picking: *"This brief reads like a custom palette would fit better than the catalog. Want me to construct a custom OKLCH palette + free-font pairing tuned to <one-line summary of the vibe>, or stay on the catalog for variety + speed?"* Wait for the user to say custom (or catalog). Default is still catalog — silence routes to catalog, not custom.

If none of the signals fires, **proceed with catalog silently. Do not mention the fork.** Most briefs don't need a custom theme — the catalog's 22 themes plus the rotation rule already deliver structural variety. See Step 2.6 for the dispatch.

**If the user opts out or skips fields** (says "go ahead", "you pick", "skip", "just build it", "don't ask", answers some fields and leaves others blank, or simply doesn't engage with the question after one prompt):

- Infer audience, use case, and tone from the brief, the domain, and any visible context (filename, framework, surrounding code is fair game *now* — only because the user delegated).
- **State the inferences in one sentence at the top of your reply** — *"Going with: audience = X · use = Y · tone = Z. If any of those is wrong, tell me and I'll redirect."*
- Stamp them in the CSS comment alongside the macrostructure (Step 4 below). The stamp is now the durable record.
- Pick a **non-default** macrostructure — Specimen-fall-through is still banned, even on inferred briefs.

**Do not skip the inference disclosure.** The opt-out is a courtesy to lazy users, not an excuse for the skill to be opaque. If the user can't see what was inferred, they can't redirect when it's wrong.

Once the three are settled (asked or inferred), restate them in one sentence and proceed.

### 2. Pick a macrostructure FIRST

Before loading any visual ruleset, **read the slim index at [`references/macrostructures.md`](references/macrostructures.md) and pick one of the twenty-one named macrostructures.** The index is one-line-per-macro; pick a name, then **load ONLY that one per-macro file** from `references/macrostructures/` (e.g. `references/macrostructures/05-workbench.md`). Do not load the whole catalogue — that's ~37 KB of dead weight for a single pick. Each macrostructure is a complete page-shape — heading placement, body composition, divider language, button voice, image treatment, reveal — bundled as a single named choice. Picking one named macrostructure is faster and more varied than choosing six independent axes from scratch.

**Diversification rule (mandatory).** Before you pick:

1. Look in the target codebase for an existing `/* Hallmark · macrostructure: <name> · ... */` stamp at the top of any CSS file. If you find one, your pick must be a *different* macrostructure.
2. If you have produced any other Hallmark output for this user in this session, your pick must be a different macrostructure than the last one.
3. **The Specimen macrostructure (numbered left-margin labels + huge serif + asymmetric spans + typographic CTA) is no longer a default.** Reach for it only when the brief is explicitly editorial, foundry-adjacent, or the user has named it.

**Theme-diversification rule (mandatory).** Picking a different macrostructure isn't enough on its own — two consecutive Hallmark outputs can share a theme even if their structures differ, and the result reads as repetition. Two consecutive themes must differ on **at least one** of three axes:

- **Paper band** — dark (L < 30 %) / mid (30–85 %) / light (> 85 %), per the theme's `--color-paper` lightness
- **Display style** — italic-serif (Specimen, Studio, Atelier) / roman-serif (Newsprint, Salon, Linen) / geometric-sans (Plume, Manifesto) / mono (Terminal) / display-condensed-italic (Sport) / display-heavy (Brutal) / system-native (Quiet) / risograph-bold (Riso)
- **Accent hue** — warm (red / orange / amber: 10–60°) / cool (blue / indigo / cyan: 200–300°) / neutral (no chromatic accent: Quiet) / chromatic-other (green: Studio · sage: Garden · phosphor: Terminal)

If the previous output was Specimen (light · italic-serif · warm), the next can be Studio (light · italic-serif · chromatic-green) — the *accent hue* differs. But the next can't be Salon (light · roman-serif · warm) which only differs on display style and shares both paper band and accent — pick a more distant theme.

The per-theme axis values live as comments at the top of each theme's tokens block in [`site/css/tokens.css`](site/css/tokens.css). When in doubt, name your candidate theme out loud and identify its three axis values; if two of three match the previous output, redirect.

**State your pick.** Before writing any code, say "Macrostructure: <name>. Theme: <name>. Differs from the last on: <axes>." in plain text. This is a deliberate accountability step — picking on the page (not in your head) prevents the default-attractor sameness that kept the skill emitting Specimen output.

If the brief is genuinely vague (no theme, no tone), do **not** default. Offer the user three macrostructures from *categorically different* groups (e.g. one grid-led like Bento, one document-led like Long Document, one poster-led like Manifesto). Three concrete choices, not seven abstract tones.

The macrostructure picks five of the six structural axes for you; you only need to pick the reveal yourself. The deeper axis catalogue is still in [`references/structure.md`](references/structure.md) when you need to deviate from the macrostructure's defaults.

**Pick a nav archetype (N1–N10) and a footer archetype (Ft1–Ft8) at this step.** They are not optional chrome; they are part of the page's structural fingerprint. Read the slim index at [`references/component-cookbook.md`](references/component-cookbook.md) and the routing tables at its bottom — the genre's default plus the acceptable alternates. Then **load ONLY the picked archetype files** from `references/components/` (e.g. `components/n5-floating-pill.md` + `components/ft5-statement.md`). A typical build loads 5–7 archetype files total (1 hero + 1 section head + 1–2 features + 1 CTA + 1 footer + 1 nav). Do not load the cookbook end-to-end — that's ~55 KB of archetypes you won't use. State both picks alongside the macrostructure: *"Macrostructure: Marquee Hero. Nav: N5 Floating pill. Footer: Ft5 Statement. Theme: Bloom."*

**Default away from N1 and Ft3.** N1 (wordmark + 4–5 inline links + button-right at full width) and Ft3 (4 columns of links + social row + tiny copyright) are the most-recognised AI fingerprints. Reach for N5–N9 and Ft1/Ft2/Ft4/Ft5/Ft6/Ft7/Ft8 by default; reach for N1 only when the page genuinely has 2 destinations and the genre allows it; reach for Ft3 only on a genuine docs root or hub.

**Diversification extends to nav + footer.** Across consecutive Hallmark runs in the same project session (per `.hallmark/log.json`), no two outputs should share the same nav archetype OR the same footer archetype. If the previous run used N5 + Ft5, the next picks N6/N7/N8/N9 + Ft1/Ft2/Ft4/Ft6/Ft7/Ft8 from the routing tables. The nav and footer picks are recorded in the macrostructure stamp at Step 6.

### 2.5. Check project memory

If the project has a `.hallmark/log.json` file (created by previous Hallmark runs), **read it before** picking the macrostructure or theme. The schema is a JSON array, newest entry first:

```json
[
  { "date": "2026-04-30", "macrostructure": "Bento Grid",   "theme": "Linen",   "enrichment": "E1 clipped-edge",  "brief": "Tracejam · SaaS observability" },
  { "date": "2026-04-28", "macrostructure": "Long Document","theme": "Linen",   "enrichment": "E5 hand-built SVG", "brief": "Maple Street Bread · bakery" },
  { "date": "2026-04-25", "macrostructure": "Manifesto",    "theme": "Manifesto","enrichment": "none",            "brief": "Meridian · studio manifesto" }
]
```

Use the **last 3–5 entries** to inform diversification:
- Your macrostructure pick must not match any of the last three.
- Your theme pick must differ from the last on at least one axis (see the theme-diversification rule above).
- Your enrichment pick should not be the same enrichment archetype as the last (`E1 clipped` twice in a row reads as templated, even with different content).

If the file doesn't exist, this is the first Hallmark run for this project — no constraint, but **you'll create the file in Step 6**.

If the project has a CSS stamp but no `log.json`, infer one entry from the stamp and proceed.

**State the rotation in plain text before picking.** This is the user's accountability line for diversification — picking on the page (not in your head) is what keeps the skill from drifting back into Bento-Grid-by-default. The format:

> *"Last 5 builds: Bento Grid (Tracejam) · Bento Grid (Foundry) · Long Document (Maple) · Manifesto (Meridian) · Quote-Led (Tide). Bento Grid used 2 of 5 — picking from {Marquee Hero, Stat-Led, Workbench, Letter} this time. I'll go with Marquee Hero."*

Then the theme rotation, on the next line:

> *"Last 3 themes: Linen · Plain · Salon. Picking from {Newsprint, Atelier, Studio, Garden} — Newsprint differs on display style and accent hue."*

**Three sample shapes** to imitate:

- **First-time** (no `log.json`, fresh project): no rotation block at all — just the macrostructure pick. *"This is the first Hallmark run for this project. Picking Long Document — fits the Coffeebox brief's editorial tone."*
- **Mature project** (5+ entries in `log.json`): the format above — frequency count, exclusion list, pick.
- **User overrode last run** ("use Bento Grid again, I want the same shape"): *"Last build was Bento Grid (you requested it). You've asked for it again — I'll pick different knob values. Knob deltas: tiles=8 (was 6), accent=full-bleed (was corner-only), spans=irregular (was even). Same archetype, different fingerprint."*

The rotation block keeps the user inside the discipline without making them read the rules. Skip it and the user starts thinking the diversification is theatre.

### 2.6. Theme route — studied-DNA, catalog, or custom

By the time you reach this step, one of four things is true:

0. **A `study` diagnosis was emitted earlier in this conversation and the user is asking to build from it** (phrases: *"build it"*, *"make it"*, *"use this DNA"*, *"build with this"* — immediately following the diagnosis) → theme route is **studied-DNA**. **Skip catalog/custom dispatch entirely.** The studied paper OKLCH, accent OKLCH, type roles (with named candidates), macrostructure, and nav/footer archetypes from the diagnosis become the locked system for this build. Diversification is suspended — you're following an external DNA, not rotating the catalog. The Step 6 stamp records `theme: studied-DNA (source: <URL or image>)` plus the actual OKLCH/font values inline. **If the user later pivots with phrases like *"use Linen instead"* / *"ignore the DNA"* / *"rotate to a different theme"*,** route back to the normal dispatch below and resume diversification. Continue to Step 3.
1. **The user named custom** (because they said so, or because Step 1's signal detection fired and they confirmed) → load [`references/custom-theme.md`](references/custom-theme.md), ask the **one** follow-up (vibe in 4–8 words + optional anchor colour), construct the OKLCH palette + free-font pairing, compute the three axis values (paper-band / display-style / accent-hue), then continue to Step 3.
2. **The user named catalog** (or implicitly accepted it by not naming custom) → pick one of the 22 named themes per the diversification rule above. Existing flow — continue to Step 3.
3. **Neither was discussed** (Step 1's signals didn't fire — vanilla brief) → default to **catalog**. Do not pause. Do not ask. Continue to Step 3.

**Custom is a quiet branch, not a default question.** Most briefs route to catalog and the user never sees the words "catalog" or "custom." The 22 named themes plus the rotation rule already deliver structural variety; the fork is reserved for when the brief specifically asks for a tuned look the catalog can't carry.

A custom theme is a **complete** OKLCH palette + font pairing tuned to the brief — not a one-off colour swap, not an excuse to bypass the rules. Every constraint in [`color.md`](references/color.md), [`typography.md`](references/typography.md), and [`anti-patterns.md`](references/anti-patterns.md) still applies. The 65 slop-test gates fire unchanged. The Step 5 preview block surfaces the palette + pairing in plain text **before** any code is emitted, so the user can redirect.

The diversification rule is theme-route-blind: a custom run that follows another custom (or a catalog) must differ on at least one of the three axes from the previous entry, same as catalog-vs-catalog. Custom entries record their three axes explicitly into `.hallmark/log.json` (see [`custom-theme.md`](references/custom-theme.md) § F).

### 3. Load the visual ruleset

The non-negotiables live in [`references/`](references/). **Be precise about what to load when. Discipline matters — over-eager loading is the largest avoidable cost of running Hallmark.**

**Always-load (eager — 1 file):**
- The genre file picked in Step 1 — [`genres/editorial.md`](references/genres/editorial.md), [`genres/modern-minimal.md`](references/genres/modern-minimal.md), [`genres/atmospheric.md`](references/genres/atmospheric.md), or [`genres/playful.md`](references/genres/playful.md). Scopes everything downstream.

**Index-then-pick (read the slim index, then load only the picks):**
- [`macrostructures.md`](references/macrostructures.md) — slim index of the 21 macros. Pick one name from the index, then load ONLY `references/macrostructures/<NN-slug>.md` for that pick. **Never load the whole index plus more than one per-macro file in a single build.** ~30 lines per per-macro file vs. 660 lines for the old monolith.
- [`component-cookbook.md`](references/component-cookbook.md) — slim index of 46 component archetypes (9 heroes, 5 section heads, 6 features, 4 CTAs, 4 testimonials, 8 footers, 10 navs) + the nav + footer routing tables at the bottom. Pick your archetype codes (H#, S#, F#, C#, T#, Ft#, N#) from the index, then load ONLY the matching `references/components/<code>-<slug>.md` files. A typical build loads 5–7 archetype files. **Loading the cookbook end-to-end or pre-loading more than one archetype per category is the single biggest token waste in the skill — don't.**

**Load-per-build (universal rules — load every build):**
- [`typography.md`](references/typography.md) — fonts, scale, pairing, weights, measure, hero headline sizing
- [`color.md`](references/color.md) — OKLCH, palette construction, accent discipline
- [`layout-and-space.md`](references/layout-and-space.md) — 4 pt scale, grid-breaks, asymmetry, depth
- [`motion.md`](references/motion.md) — durations, easings, what to animate, reduced-motion
- [`copy.md`](references/copy.md) — verbs, labels, error structure, link text
- [`anti-patterns.md`](references/anti-patterns.md) — the named tells you must not emit

**Load-conditionally (only when the page actually needs it — be honest, do not pre-load "for safety"):**
- [`microinteractions.md`](references/microinteractions.md) — load whenever the output has *any* interactive element (buttons, inputs, modals, tabs, dropdowns, toasts, drag handles, copy buttons). That is most pages.
- [`interaction-and-states.md`](references/interaction-and-states.md) — load when the page has stateful UI (forms, command palettes, optimistic updates).
- [`responsive.md`](references/responsive.md) — load when mobile is in scope.
- [`structure.md`](references/structure.md) — load only when deviating from a named macrostructure.
- [`hero-enrichment.md`](references/hero-enrichment.md) — **do NOT load at Step 4 unless the image-need check in the next paragraph returns YES.** Most builds are typography-only and never touch this file. The decision is one quick read of the brief, not a defensive auto-load.
- [`custom-craft.md`](references/custom-craft.md) — load only when an enrichment archetype requires construction (CSS art, SVG, declarative animation, etc.).
- [`assets.md`](references/assets.md) — load only when an enrichment archetype needs an external asset (icons, illustration, photography, Lottie).
- [`custom-theme.md`](references/custom-theme.md) — load only when Step 2.6 routes to custom. The full custom branch (palette construction, font pairing, axis computation) lives there; SKILL.md only carries the dispatch.
- [`design-md.md`](references/design-md.md) — load only when the user explicitly asks Hallmark to lock the system into a portable file (phrases: *"lock the system"*, *"give me a design.md"*, *"make this portable"*, etc.). Opt-in; never fires on a vanilla build.
- [`preview-examples.md`](references/preview-examples.md) — load only if you need a worked example of the Step 5 preview block format. The bullet list in Step 5 itself is normally enough; reach for the file only when picking unusual macrostructures / custom themes.

**Load-at-the-end (Step 7 only):**
- [`slop-test.md`](references/slop-test.md) — **strictly Step 7, after Build.** The 66 gates are a post-emit check, not a pre-emit reference. Pre-loading slop-test.md costs ~7K tokens for nothing — the gates inform fixes, not generation. If a gate fails at Step 7, fix and re-test; do not consult the file earlier "to know what to avoid" — that's what `anti-patterns.md` is for.
- [`contract.md`](references/contract.md) — load at handoff time for output-contract + scope rules.
- [`export-formats.md`](references/export-formats.md) — load at Step 6 only when the project warrants multi-format exports (i.e. has a `design.md`). Single-page builds emit `tokens.css` from the in-memory token state and don't need this file.

**Verb-specific:**
- [`verbs/audit.md`](references/verbs/audit.md), [`verbs/redesign.md`](references/verbs/redesign.md) — load only when that verb runs.
- [`study.md`](references/study.md) — load only when `hallmark study` runs.

**Human-only (do NOT auto-load):**
- [`docs/recipes.md`](docs/recipes.md) — eight worked briefs for human readers.
- [`docs/study-examples.md`](docs/study-examples.md) — three worked DNA-extractions for human readers.

### 4. Decide on hero enrichment

Most pages don't need it. The strongest hero is often a typographic one. **Reach for [`hero-enrichment.md`](references/hero-enrichment.md) only when the brief points there** — a SaaS / dev-tool brief wants a demo video or mockup; a bakery / café / atelier brief wants a hand-built illustration; a manifesto wants nothing.

**First — does the brief need imagery at all?** Run the image-need table at [`hero-enrichment.md` § Image-need detection](references/hero-enrichment.md). Default is typography-only. If the brief signals "needs photographic content" (e-commerce, team, food, travel) AND the user hasn't supplied real assets, use the placeholder strategy in [`assets.md` § Placeholder strategy](references/assets.md). If the brief allows non-photographic imagery (SaaS landing, manifesto, agency splash, editorial-led), prefer the [`imagery-kit.md`](references/imagery-kit.md) over photo placeholders. **Never ship invented stock photos as if they were the final design.**

Eyeball the brief or ask one short question. State the decision in one sentence (e.g., *"Enrichment: E1 Clipped-Edge Demo Video, Tier-A CSS-art mockup."* or *"Enrichment: none — typography only."*). The decision goes into the macrostructure stamp at Step 6.

**The enrichment hierarchy is non-negotiable.** Reach for the highest tier you can ship: typography only → Tier A pure CSS art → Tier B hand-built SVG → Tier C generated still (Nanobanana / Recraft) → Tier D library + customisation → **Tier E Lottie is last resort**, only for complex character motion that hand-build can't reach. Reaching for Lottie when CSS would have built it is the new tell.

When an enrichment archetype requires construction, also load [`custom-craft.md`](references/custom-craft.md). When it requires an external asset, load [`assets.md`](references/assets.md).

### 5. Preview

Before emitting any code, output a tight summary of what you're about to ship. This is the user's TL;DR — they should be able to scan it in five seconds and tell you to redirect *before* you write 500 lines of CSS that don't match their intent.

**Format** (Markdown bullets, not ASCII boxes — they render reliably across every chat client and terminal):

```markdown
**Hallmark · v1.0.0**

- **Macrostructure** · Stat-Led
- **Theme** · Plain (#fff paper · cool greys · ink-blue accent)
- **Enrichment** · none (typography only)
- **Sections** · Hero · Logos · Stats · Features · Testimonials · Pricing · FAQ · CTA · Footer
- **Motion** · counter · pricing-lift · pulse-once
- **Slop test** · 69 / 69 ✓ (run after Build)
- **Diversification** · differs from Linen on display style + accent hue
```

**Six required bullets, one optional, plus a CTA line:**

1. **Macrostructure** — the named pick from [`macrostructures.md`](references/macrostructures.md).
2. **Theme** — for catalog: name + one-line palette summary (paper colour band · accent hue · display style). For custom: `custom (vibe: "<4–8 words>" · paper oklch(<L%> <C> <H>) · accent oklch(<L%> <C> <H>) <one-word hue label> · <display face> + <body face>)`.
3. **Enrichment** — the chosen archetype + tier, or *none (typography only)*.
4. **Sections** — section names separated by ` · `, in DOM order.
5. **Motion** — microinteraction primitives separated by ` · `, or *none — typography only*. Always under three primitives per the [`microinteractions.md`](references/microinteractions.md) hard rules.
6. **Slop test** — `69 / 69 ✓` if all gates pass, or `N / 69 — fails: <gate numbers>` if any are open. Run the slop test BEFORE writing this row; the slop test is Step 7.
7. **Diversification** *(optional, only when `.hallmark/log.json` has prior entries)* — what axes differ vs the previous run.

**Then one quiet CTA line, italicised, after the bullets:**

> *System portable? Say `lock the system` to extract this build's tokens + voice into a `design.md`.*

Skip the CTA line when (a) the build is component-scope, or (b) `design.md` already exists at the project root (the system is already locked). See [`design-md.md`](references/design-md.md) for the full opt-in flow.

Four worked sample preview blocks (Long Document, Bento Grid, Manifesto, Custom) live in [`references/preview-examples.md`](references/preview-examples.md) — load that file only if the bullet-list spec above isn't scaffolding enough on its own. Most builds don't need it.

If any slop-test gate fails when you reach Step 7, return to the relevant Build step, fix it, and **re-emit the preview block** with the corrected slop-test row. The preview is the durable summary; it's wrong to ship if it lies.

### 6. Build

Emit code that satisfies the tone and structural fingerprint. Match the complexity of the code to the ambition of the tone — a brutalist page needs raw, heavy CSS; an austere page needs restraint.

Always:

- **Hero headline — match font-size to copy length.** When you write the headline yourself (no user-supplied copy), aim for **≤ 7 words and ≤ 50 chars** from the start. For longer headlines, apply the size-by-length brackets in [`typography.md § Hero headline sizing`](references/typography.md): 21–50 chars use `--text-display`; 51–90 chars cap at `--text-display-s`; > 90 chars rewrite shorter or cap at `--text-4xl`. Aggressive-display themes (Brutal, Riso, Manifesto) auto-step down one rung past 50 chars — their 6.5–9rem ceiling is for short statements only.
- **Section tags / eyebrows — default OFF.** Do NOT emit `01 · THE TOUR`, `02 / FEATURES`, `Chapter Three`, or any uppercase mono-cap section number / kicker / label unless either (a) the user explicitly asked for chapter / step / section numbering, OR (b) the macrostructure is Long Document, Manifesto, or Catalogue numbered AND the content is genuinely ordinal. Cap at 1–2 per page even then. **When a tag IS used, always stack vertical — tag above, heading directly underneath in the same column.** The tag-left / heading-right two-column pattern (a.k.a. hanging header, left-margin label) is banned outright — it is the single most reliable templated-editorial tell, and slop-test gate **66** auto-fails it.
- Use OKLCH for every colour. Declare tokens as CSS custom properties at `:root`.
- Use a 4pt spacing scale with semantic names (`--space-sm`, `--space-md`, …).
- Pick a distinctive display face and a refined body face. Pairings, not single-font pages — *unless* the single-font choice IS the design (a true terminal-aesthetic page is monospace-only on purpose; that's allowed).
- Design every interactive element for its full eight states (see [`interaction-and-states.md`](references/interaction-and-states.md)).
- Animate `transform` and `opacity` only — never layout properties.
- Use the three named easings (`--ease-out`, `--ease-in`, `--ease-in-out`) — never the browser default `ease`, never bounce/overshoot on UI state.
- Support `prefers-reduced-motion: reduce`. Spatial motion collapses to ≤150ms opacity crossfade.
- Include `:focus-visible` with a visible ring at ≥3:1 contrast. **Never animate the ring's appearance** — it must show instantly on focus.
- For each interaction in the output (button, input, modal, toast, drag, copy, etc.), apply the recipe in [`microinteractions.md`](references/microinteractions.md). Pick *silent success* over celebratory toasts. Pick *optimistic update + Undo* over confirmation dialogs. Pick *delay 800ms* on hover tooltips and *0ms* on focus tooltips.
- Cut motion before adding it. Most pages have too much, not too little. If removing an animation wouldn't lose the user information, remove it.
- **Stamp the output.** The first non-empty line of the produced CSS file (or the top of `<style>` if inline) MUST be a comment of the form: `/* Hallmark · macrostructure: <name> · tone: <tone> · anchor hue: <hue> */`. This stamp is the durable record of what you chose. The next time Hallmark runs in this project, it reads the stamp and picks a *different* macrostructure. **For custom themes**, the stamp also carries the vibe, paper + accent OKLCH values, the chosen display + body fonts, and the three diversification axes — the full multi-line format is in [`custom-theme.md`](references/custom-theme.md) § E. **For studied-DNA builds** (Step 2.6 Condition 0 routed here from a `study` diagnosis), the stamp's `theme:` field is `studied-DNA (source: <URL or "image">)` followed by the paper OKLCH, accent OKLCH, and display + body fonts pulled directly from the diagnosis — not a catalog theme name. Diversification stays suspended for the run; the log entry below records `theme: studied-DNA` so Step 2.5 on the next run knows not to rotate against it.
- **Append to project memory.** After you write the stamp, update (or create) `.hallmark/log.json` at the project root. Append a new entry at the **front** of the array: `{ "date": "<YYYY-MM-DD>", "macrostructure": "<name>", "theme": "<name>", "enrichment": "<E# name or 'none'>", "brief": "<one-line summary>" }`. **Custom entries** also carry `"theme": "custom"` plus `"theme_axes": "<paper-band> / <display-style> / <accent-hue>"` and an optional `"vibe": "<4–8 words>"` — see [`custom-theme.md`](references/custom-theme.md) § F. Trim the file to the last 20 entries (rotate the oldest off). Create `.hallmark/` and the file if they don't exist; respect any existing `.gitignore` (the user may or may not want this committed). This file is what Step 2.5 reads on the next run.
- **Always emit `tokens.css`.** After writing the page CSS, also write `tokens.css` at the project root containing every `--color-*`, `--font-*`, `--space-*`, `--text-*`, `--ease-*`, `--dur-*`, `--rule-*`, and `--radius-*` token used in the build. The page CSS imports `tokens.css` (or, on framework projects, the project's existing entry-point includes it) — the page CSS must reference tokens by name, never inline raw values. Even single-page builds get a `tokens.css`. This is what makes the design system portable to the next project. Load [`export-formats.md`](references/export-formats.md) at this point only when the project warrants additional formats — see below.
- **Multi-format exports on `design.md` projects.** If a `design.md` exists at the project root (a system-managed project), append all four export formats — `tokens.css`, Tailwind v4 `@theme`, DTCG `tokens.json`, shadcn/ui CSS variables — into `design.md`'s `## Exports` section. Load [`export-formats.md`](references/export-formats.md) for the canonical mapping from Hallmark tokens to each format. Single-page projects skip this step (they get only `tokens.css`).
- **Opt-in `design.md` (lock-the-system flow).** If the user explicitly asks Hallmark to lock the build's design system into a portable file (phrases: *"lock the system"*, *"give me a design.md"*, *"make this portable"*, etc.), load [`design-md.md`](references/design-md.md) and follow it. Page-scope only; component-scope skips. **The default verb does NOT auto-emit `design.md`** — users iterate freely first, then ask for it once the system is settled. If `design.md` already exists, refresh its `## Exports` section instead of overwriting. The Step 5 preview block carries a one-line CTA surfacing this option after every page-build.

### 7. The slop test

Before handing back, run the output through the 69-gate slop test in [`references/slop-test.md`](references/slop-test.md). Every answer must be **no**. Load that file at this step (not earlier — it isn't needed until handoff). The active genre matters: some gates are universal, some are genre-scoped (atmospheric loosens the radial-bloom gate; modern-minimal loosens the zero-chroma neutral gate; etc.). The full per-genre overrides are listed inline in `slop-test.md`.

Run the slop test BEFORE writing the Slop test row in the Step 5 preview block — that row reflects the actual outcome of this step.

If any gate fails, fix it. Do not ship slop.

---

## `hallmark audit`

Load [`references/verbs/audit.md`](references/verbs/audit.md) and follow it.

---

## `hallmark redesign`

Load [`references/verbs/redesign.md`](references/verbs/redesign.md) and follow it.

---

## `hallmark study`

Load [`references/verbs/study.md`](references/verbs/study.md) and follow it. It also requires [`references/study.md`](references/study.md). `study` extracts a reference design's structure, not its pixels.

## Output contract & scope

Load [`references/contract.md`](references/contract.md) once, at handoff time, for the full output contract and scope-of-skill rules.
