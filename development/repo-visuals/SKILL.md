---
name: repo-visuals
description: Create hero visuals — animated GIF, static PNG, or animated SVG — for GitHub repositories. Runs a structured discovery conversation (scan repo → recommend format → propose creative scenarios → agree on a brief), then designs bespoke HTML/SVG, previews it in the browser, and exports. Use when the user asks for a README hero, repo banner, README image, GitHub header, social preview card, repo demo GIF, hero image, OG image, project screenshot, repository showcase, or any "image at the top of the README".
---

# repo-visuals

Turn a repo (GitHub URL, local folder, or free-text brief) into a hero visual that a viewer sees at the top of the README and instantly understands *what this project does and why it's interesting*. The hero may be an **animated GIF**, a **static PNG**, or an **animated SVG** — the skill recommends one based on the repo's identity, the user picks.

The skill's quality comes from the **discovery dialog**, not from templates. Every hero is bespoke.

## Phases

1. **Discovery** — pick operating mode (Auto / Semi-auto / Manual, §1.1a), scan the repo, summarize findings, recommend a format (animated vs static), ask about vibe/audience/hero moment, propose 2–3 scenarios, converge on a brief. Then **Gate A — brief vs README** (§1.8): narrow repo-context check on the brief before any pixels exist. The mode controls *how many* of these the user answers vs. Claude decides silently — it does not skip any of the craft checks.
2. **Build** — write HTML/CSS/JS for the chosen scenario. For static, design one decisive frame; for animated, a loop. No storyboard step. Then **Gate B — rendered HTML vs README** (§2.6): sample keyframes from the HTML, check what's on screen against the repo's own positioning, allow 1 auto-iteration if it fails. Both gates are deliberately narrow — only repo-context fidelity, not aesthetics or craft.
3. **Preview & iterate** — open the HTML in the user's default browser, iterate in text until the user says ship.
4. **Export** — animated GIF → Puppeteer screencast + ffmpeg palette pipeline. Static PNG → Puppeteer `page.screenshot` (with `deviceScaleFactor: 2` for retina crispness). Animated SVG → author the SVG directly (CSS `@keyframes` or SMIL `<animate>` inside the file); no rasterization step — the source *is* the artifact.
5. **Output** — place the hero in the target repo; optionally open a PR that embeds it in the README.

**Dev mode (author-only):** Phase 6 — Evaluate exists but **only runs in dev mode**. Dev mode is for the skill's author iterating on the skill itself; it collects scorecard data and writes run logs under `./evaluations/` in the user's current working directory. Enable it only when the user explicitly says "dev mode" (or sets `REPO_VISUALS_DEV=1`). In every normal run — including Manual, Semi-auto, and Auto — the skill ends after Phase 5. Do not mention Phase 6 to end users.

---

## Phase 1 — Discovery

Discovery runs **before any HTML is written**. Its job: go from a vague ask ("make a hero GIF for my repo") to a specific, committed creative brief.

### 1.1 Activation

Enter discovery mode whenever the user invokes the skill, **unless** they explicitly say "skip discovery, I have the brief ready."

### 1.1a Operating mode (ask first, once per run)

Before anything else — before the scan summary, before any direction questions — ask the user which operating mode they want for this run. Use the `AskUserQuestion` tool so the choice is structured and visible, not buried in free text. Offer three modes; describe each in concrete terms (what gets asked, what gets decided silently) and include pros/cons so the user can pick with open eyes. Default recommendation: **Semi-auto**.

> Note: this "operating mode" is a skill-level concept about how many questions the skill asks. It is distinct from the Claude Code harness's own auto-mode; the two do not replace each other.

Verbatim `AskUserQuestion` shape (Run mode header, three labeled options with pros/cons): `craft/snippets/operating-mode-question.md`. Paste as-is; option text is load-bearing.

Rules that apply to **every** mode regardless of choice (craft non-negotiables):

- **§1.3 inventory count is always collected.** Auto/semi don't skip it.
- **§4.0 scope-match rule is always enforced.** If the hero says "all" or shows a grid, on-screen reality must match the real inventory — regardless of mode.
- **§1.8 Gate A and §1.8b Gate B are always run on the brief.** Gate A covers repo-fidelity, Gate B covers aesthetic-identity match and the wow check. Auto/semi don't skip them before writing HTML.
- **§3.0a / §4.4a render self-critique is always run.** Every rendered HTML preview screenshot and every exported PNG/GIF gets read and bullet-critiqued before being shown to the user. The user is not the QA pass.
- **Any mode can be upgraded mid-run.** If Auto drifts, user can say "stop, switch to semi" and we resume from the nearest decision point. Do not silently re-ask everything; pick up at the next unanswered question.

After the user picks a mode, commit it to memory for the run (e.g. "Mode: Semi-auto") and reference it when deciding whether to ask or decide silently at each subsequent step. In Auto and Semi-auto, make decisions with a brief one-line note ("going with the Product-UI marketing archetype per §1.4c — amplication-shape repo") so the user can redirect if they disagree.

### 1.2 Input triage

User may provide:

- **GitHub URL** → clone shallow, plus use `gh repo view` for stars/topics/languages/releases.
- **Local path** → scan the tree directly.
- **Free-text brief only** → proceed to direction questions immediately.
- **Nothing** → ask first for one of the above.

### 1.3 Scan checklist (collect a lot)

Gather as much as possible before asking the user anything. Goal: Claude should already have an opinion about what this repo is before the vibe conversation starts.

- README (full text) — extract tagline from first paragraph.
- Manifest(s): `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `*.csproj`, etc. — description, keywords, dependencies, entry points.
- File tree (depth 3) + top 10 files by size.
- Language breakdown (LOC per language).
- Existing visuals in repo: `assets/`, `docs/`, `.github/`, `public/`, any `*.png` / `*.gif` / `*.svg` near the root.
- **Brand logo — find it, don't invent it.** Look in this order, stop at the first hit: (1) repo files: `public/`, `assets/`, `.github/`, `docs/` for `logo.*`, `favicon.*`, `icon.*`, `brand.*`; (2) README `<img>` / `srcset` entries near the top (often hosted on the project's domain or GitHub CDN — try `curl` with a browser User-Agent); (3) homepage URL from `package.json` / GitHub repo metadata — fetch `/logo.svg`, `/logo-dark.svg`, `/favicon.svg`, `/favicon.ico`, or the og:image; (4) GitHub social-preview image. Save whatever you find to the working dir alongside `index.html`. If nothing turns up, **do not generate or stylize a substitute mark in any mode.** See §2.4 logo rule for what to do next.
- `LICENSE`, `CHANGELOG.md` — maturity signal.
- Recent git log (last 10 commits) — what's active.
- If GitHub: stars, topics, releases, open issues count.
- If `ast-graph` is available locally and the repo has supported languages: run `scan` + `hotspots` + `symbol` on top-level exports for structural inventory.
- **Count the real inventory** — if the repo exposes a collection (tools, commands, pages, themes, plugins, routes), count them from source (route files, `src/tools/*`, CLI command registrations, etc.). Do not estimate from the README. This number is used later: any hero that says "all", "every", "the whole", or shows a grid meant to represent scope must match this count — or explicitly frame itself as a sample ("10 of 30 shown", scroll affordance, "30+"). An undercount reads as a broken promise.
- **If the repo's product has a visible runtime UI** (CLI tool, TUI, terminal app, IDE plugin, desktop app), collect the *real* UI vocabulary before drafting any hero with that UI in it. Look for: screenshots in `assets/`/`docs/`, GIFs already in the README, source-level UI strings (banner generators, status string constants, hook output messages, prompt formats). **Proactively ask the user for a short screen recording** (`.mov` / `.mp4`) if none are in the repo — extract frames with `ffmpeg -i recording.mov -vf "fps=0.5,scale=1400:-1" frames/f%02d.png` and `Read` multiple keyframes for grounding. A generic terminal mock with invented `npm run typecheck`-style lines is a craft failure even when it looks polished — it doesn't match the real app and viewers who use the tool will spot it. This rule is hard, not soft: if the real UI vocabulary isn't accessible, **flag the gap to the user before drafting** rather than inventing.

Summarize findings back to the user in ~6–10 bullets so they can correct misreadings early. Include the inventory count when one exists. **If the scan finds an existing hero**, branch into §1.3a before continuing to direction questions.

### 1.3a Redesign vs greenfield (only if an existing hero is found)

If the scan surfaced an existing hero, branch into the redesign protocol *before* §1.4. Surface the existing file (path, format, age, README placement), then `AskUserQuestion` the entry mode — **Redesign (carry forward)** / **Fresh (ignore existing)** / **Replace in place** — and follow the matching steps. Full protocol (entry-mode question, critique structure, carry-forward rules, scenario constraints) in `craft/redesign.md`.

### 1.4 Direction questions (after the scan summary)

Ask these as a structured batch, with suggested defaults based on what the scan found so the user can just accept or redirect:

1. **Where will this hero live?** — README top / project website / social posts (Twitter, LinkedIn) / conference slide / internal demo / elsewhere. *This drives dimensions and loop length.*
2. **Output format?** — **animated GIF** / **static image (PNG)** / **animated SVG** / **HTML only (no export)**. Not every repo wants motion; some strong identities read better as one sharp frame; some content (vector UI, type, simple geometry) renders sharper, smaller, and theme-aware as SVG. Scan the repo first and offer a recommendation (see §1.4c), then let the user override. Default: whichever §1.4c recommends. *(MP4/WebM and square social cards are listed in the future-formats appendix.)*
3. **Audience** — working devs / eng leaders / newcomers / prospective contributors / all
4. **Vibe** — minimal, playful, technical, cinematic, retro-terminal, brutalist, polished-SaaS
5. **Energy** — calm & meditative / steady / frenetic & showy
6. **Hero moment** — the single thing a viewer should take away
7. **What NOT to imply** — claims, vibes, or audiences this hero must *avoid* suggesting. A hero can look polished and still say the wrong thing (e.g. implying enterprise-readiness for a hobby project, or "fast" for a tool whose pitch is correctness). Capture explicit don'ts so Gate A (§1.8) has something to check against. Examples: *"don't imply this is production-ready,"* *"don't lead with speed — the pitch is correctness,"* *"avoid AI/ML aesthetics — this is a UI library."*
8. **Hard constraints** — brand colors, existing fonts, imagery to include/avoid, duration cap

### 1.4a Probing when the user doesn't know

Many users will answer "I don't know" to vibe / hero moment / audience. That's normal. Don't force them to guess — extract intent sideways:

- **"Show me a repo whose hero you liked"** — reverse-engineer what they respond to.
- **"What do you wish someone understood about this project in 10 seconds?"** — surfaces the hero moment without asking for it directly.
- **"Who's the person whose opinion about this repo matters most to you?"** — surfaces the audience.
- **"Is this repo a calm/serious tool or a fun/exciting one?"** — a binary that usually works for vibe.

If they still can't articulate, offer Claude's best guess based on the scan and ask them to confirm or push back. Be willing to **commit first, confirm second** — a concrete wrong guess triggers better reactions than another open-ended question.

### 1.4c Format recommendation (animated vs static)

Before asking Q2, form an opinion from the scan. **First consult `craft/reference-gallery.md`** — try to place the target repo in one of the catalogued archetypes (Terminal-demo GIF / Product-UI marketing / Brand-first logo / Banner/promo graphic / Diagram-as-hero) and cite the match by name when recommending. If no clean match, fall back to the heuristics below.

The repo's identity tells you which format fits:

**Lean static (PNG) when:**
- The repo's pitch is a **surface**, not a process — a landing page, a typography choice, an API shape, a single striking screenshot.
- Existing visuals in `assets/` / `docs/` are already static and strong.
- The vibe is brutalist, editorial, documentation-first, or "the screenshot is the product" (design systems, component libs shown in a grid, CLI themes whose appeal is one frame).
- Audience skews toward skim-then-click (social posts shared as preview cards, directory listings).
- README opens with one crisp hero sentence and a screenshot — mirror that, don't animate it.

**Lean animated (GIF) when:**
- There's a **before→after transformation**, a step sequence, or a multi-stage pipeline — the motion *is* the pitch.
- The repo is a tool with visible runtime behavior (CLI output, live reload, computation unfolding).
- The hero moment is "watch this happen," not "see this exists."
- The scan surfaces multiple distinct capabilities worth walking through (then: animated; or: static grid).

**Lean animated SVG when:**
- The hero is **vector-friendly**: typography-led, UI chrome, simple geometric motion, line-art mascots, terminal/code-style heroes without raster screenshots or photographs.
- File-size matters and the content is mostly shapes + text — animated SVG often lands 5–50× smaller than the equivalent GIF and stays crisp at any zoom (no palette banding, no sub-pixel text smear).
- Theme-aware rendering is wanted (light/dark via `<picture>` swap or `prefers-color-scheme` media queries inside the SVG).
- Motion is expressible as property animation (transform, opacity, stroke-dashoffset, path morphs, simple keyframe sequences) — *not* per-frame raster effects, particle systems, blend-mode-heavy compositing, or anything that needed JS timing in the HTML version.
- Hard constraints from GitHub: SVG must be loaded via `<img src="...">` (inline `<svg>` is sanitized out of READMEs); **no `<script>`** survives the sanitizer, so motion is CSS `@keyframes` or SMIL `<animate>` only; no pointer/hover interaction (image embed gets no events); external resources (fonts, fetched images) are blocked, so embed everything.
- **Skip SVG if** the hero needs a real screenshot, photograph, dense gradients (size win evaporates once raster is embedded), or JS-driven scene sequencing.

**Lean HTML-only when:**
- The user will embed on a site they control and wants the live animation.
- The user explicitly wants to iterate further with their own tools.

Present the recommendation forcefully: *"Based on the scan, I'd go **static** — this repo's identity is [X], and motion would add noise not signal. Want me to proceed with static, or would you rather animated?"* Then honor whatever they pick.

**Mascot / character-driven repos** (pixel pet, animal, robot, bespoke creature) are a special case worth flagging at recommendation time:
- Size the mascot as the **visual anchor**: ≥30–35% of the stage's smaller dimension. Smaller, and it gets out-competed by surrounding chrome (terminal windows, taglines, icons) and the hero loses its identity. Real incident: clawd-on-desk landed at 184px-on-500px-tall (~37%) only after two iterations of bumping from an undersized initial 96px.
- Default to **always-present** layout: the mascot sits in its final position from frame 1. Story arc happens via the mascot's own animation/state changes, not via the mascot moving across the frame.
- **Skip cinematic entrances** — jump-in / zoom-in / slide-in / camera-dolly transitions almost always look bad in a small GIF and add no information. If you're tempted to write one, prefer holding the framing and animating the mascot's state instead. The same run had a "pet jumps into terminal + camera zooms" sequence that the user explicitly cut as *"look bad"*; removing it improved the hero.

### 1.5 Scenario proposal

Offer **2–3 concrete scenarios** (two if the viable directions are closely related, three if they diverge meaningfully), each with:

- **Concept** — one line
- **Scene beats** — 3–5 bullets describing what happens second-by-second
- **Vibe anchor** — a visual reference ("think Linear changelog", "think `htop`")
- **Why it suits this repo** — one paragraph grounding it in the scan findings
- **Risk** — one line on what could make this one weaker

Then **Claude's recommendation**: pick one and argue for it forcefully in 1–2 sentences. Frame it as something the user can still redirect.

### 1.6 Convergence signal — "enough info"

Move to the build phase when all six are settled:

- [ ] Chosen scenario (one of the 2–3 proposed, possibly with edits)
- [ ] Vibe locked
- [ ] Hero moment named in one sentence
- [ ] Audience named
- [ ] Hard constraints captured (or confirmed "none")
- [ ] "What NOT to imply" list captured (or confirmed "none") — used by Gate A (§1.8)
- [ ] Output format chosen (animated GIF / static PNG / animated SVG / HTML only)
- [ ] Placement agreed (README / website / social / slide / other)
- [ ] Duration chosen — animated only (typical: 15–25s loop; default 20s); skip for static
- [ ] Dimensions confirmed (see §1.7 — default 1200×675; tailor when the repo spirit calls for it)
- [ ] Real inventory count captured from §1.3 scan (if the repo has a countable collection)
- [ ] Operating mode recorded from §1.1a (Auto / Semi-auto / Manual)
- [ ] Paddings are symmetric — top = bottom, left = right — unless a deliberate asymmetry is named in the brief (§2.4 symmetry rule)
- [ ] Gate A (§1.8) and Gate B (§1.8b) both PASS — repo-fidelity *and* aesthetic-identity + wow have been checked

Write the brief back to the user in a compact block. Wait for **"go"** before writing any HTML — *unless* the mode is **Auto**, in which case proceed directly to Phase 2 with a brief summary line and no wait. In **Semi-auto**, show the brief but proceed after a brief pause unless the user interjects. In **Manual**, wait explicitly for "go".

### 1.7 Dimensions — default with room to tailor

**Default: 1200×675 (16:9).** It's the safe pick when the repo gives no strong signal — GitHub's ~1000px README column renders it at ~560h (comfortable but not dominant), and the skill's capture/eval scripts are calibrated around that width. Start here unless the repo *wants* something else.

**Tailor when the repo's spirit points elsewhere.** Don't force a 16:9 crop onto a project whose identity is clearly another shape. Signals to deviate:
- **Slim banner (e.g. 1200×300 / 1600×400):** one-line wordmark-led brands, docs sites with an existing slim header, terminal-themed repos where the pitch is a single ribbon of text. Banners read as "logo-bar," not "hero scene" — use shorter loops (10–15s) and fewer scenes.
- **Square / portrait (1:1, 4:5):** social-first repos, mobile SDKs, anything whose primary surface is a phone. Don't build these for a README header — they're a separate deliverable.
- **Wider than 16:9 (2:1, 21:9):** data-viz / dashboard / timeline repos whose pitch is lateral scan; spatial tools (maps, CAD, audio waveforms). Only go this wide if the content genuinely fills it — empty wide heroes look lonelier than cramped 16:9 ones.
- **Taller than 16:9 (4:3, 3:2):** repos with dense stacked panels (notebook screenshots, multi-pane IDEs, documentation browsers) where 675h would truncate the story.

**How to decide:** during the scan (§1.3), note the existing hero image's dimensions and the repo's format archetype (from `craft/reference-gallery.md`). If they point toward a non-16:9 shape *and* the brief's hero moment fits that shape, propose the tailored size in the direction-questions batch (§1.4) — show the user the default and the tailored option, cite the reason, let them pick. If nothing argues against 1200×675, don't introduce the choice; just use it.

**Craft rules scale with whatever dimensions are chosen** — the font-size floors, bottom-clearance minimums, and column-density rules later in this document are written around 1200×675 but are expressed as ratios (% of stage height, px relative to canvas width) so they port. When you deviate, recompute: e.g. at 1200×400 the body-text floor is still ~2.5% of stage height × retina headroom, not a fixed 17px.

**The capture pipeline already supports arbitrary dimensions** — `scripts/screenshot.js` and `capture.js` both take `--width` and `--height` flags. Pass whatever the brief locked in; don't hardcode 1200×675 in export commands.

### 1.8 Gate A — brief vs README (repo-context check, pre-render)

Run after the brief block is written, before saying "go" (Auto: silently; Semi-auto: silently, surface only if it triggers a revision; Manual: visible note the user can override).

**Scope of this gate is deliberately narrow: only repo-context fidelity.** A hero can look polished and still say the wrong thing about *this specific repo* — that's what Gate A catches. Aesthetic judgments, AI-design clichés, technical compliance, "is the design generic" — all out of scope. Those belong to taste and craft rules elsewhere in this document, not to a gate that triggers a revision. Keeping the scope narrow is what prevents the gate from drifting into "optimize for pretty" — the failure mode the original Reddit feedback warned about.

**Inputs** (assemble from §1.3 scan + the locked brief):

- README first 40 lines (verbatim).
- Real inventory count and any specific names from §1.3.
- Stated hero moment (one sentence).
- Audience.
- "What NOT to imply" list (§1.4 question 7).

**Critique prompt:**

> You are critiquing a draft creative brief for the repo `<owner/repo>`'s hero visual *before any HTML exists*. Your only job is to check whether the brief faithfully represents this repo's own positioning — not to judge aesthetics, not to suggest design improvements.
>
> **Brief:** `<paste the locked brief>`
>
> **Repo ground truth:** `<README excerpt, inventory count, stated hero moment, audience, "what NOT to imply">`
>
> Answer concretely (cite the brief and the README):
> 1. **Voice match.** Does the brief's on-screen copy use this repo's own README phrasing and terminology, or does it drift into generic marketing voice?
> 2. **Scope honesty.** If the brief implies "all" / "every" / a grid, does it match the real inventory count? If not, is it explicitly framed as a sample?
> 3. **What it implies that it shouldn't.** Walk the "what NOT to imply" list and the README's actual positioning — does the brief accidentally suggest something the repo isn't claiming?
>
> For each, output: `PASS` (with a one-line reason), or `FAIL` (with a one-line reason and a one-line concrete fix). Do not comment on visual style, color, layout, or design quality — those are not what this gate checks.

**What to do with the result:**

- **All PASS** → proceed to Phase 2.
- **Any FAIL** → revise the brief to apply the fixes, re-show the brief block (don't re-run Gate A — one pass is enough). In Manual mode, surface the FAILs to the user and let them decide whether to apply the fix.
- **Auto mode + FAIL** → apply fixes silently, note them in a one-line "tightened brief: [what changed]" before proceeding.

### 1.8b Gate B — aesthetic identity & wow (pre-render)

Run immediately after Gate A passes, on the same locked brief, before saying "go" (Auto: silently; Semi-auto: silently, surface only if it triggers a revision; Manual: visible note the user can override).

**Scope of this gate is deliberately narrow: only aesthetic identity match and wow.** Gate A already verifies that the brief says the right *facts* about the repo. Gate B verifies that the brief picks the right *visual language* for the repo and that the composition has a reason to exist. Anything past those two questions — pixel-level polish, type kerning, exact palette values — belongs to render-time critique (§3.0a / §4.4a), not here.

The two failure modes Gate B catches:

1. **Author's-personal-aesthetic ≠ product's-identity.** A repo by a designer has *two* visual languages around it — the maintainer's personal blog/portfolio aesthetic, and the *product*'s own identity. Heroes belong to the product. Defaulting to the maintainer's personal palette is a real, recurring failure.
   *Example incident:* a hero for `kepano/obsidian-skills` was first drafted in Flexoki cream — kepano's *personal blog* palette. The product is **Obsidian**, whose iconic visual is the dark-purple graph view. The cream draft drew "no wow, doesn't feel like the repo." Fix was to switch to dark + graph-view aesthetic.

2. **No wow anchor.** A brief like "tasteful grid of cards in a muted palette" is generic — there is no specific compositional move that would make a viewer stop scrolling. The brief needs to name *one* concrete visual move that anchors the hero (the product's iconic visual, an unexpected layout, a vivid contrast, a recognizable metaphor).

**Inputs** (assemble from §1.3 scan + the locked brief):

- Author identity *vs* product identity. Are they the same? (e.g., a solo dev's CLI = same; a designer's library for someone else's product = different — use the *product*'s identity.)
- Existing visuals in `assets/` / app screenshots / docs.site — what visual language does the *product* itself use?
- Stated vibe and palette in the brief.
- Stated hero moment and chosen scenario.

**Critique prompt:**

> You are critiquing a draft creative brief for the repo `<owner/repo>`'s hero visual *before any HTML exists*. Your job is to check two things only: aesthetic identity match, and wow anchor. Do not re-check facts, scope, or repo-fidelity — Gate A already did that.
>
> **Brief:** `<paste the locked brief>`
>
> **Identity context:**
> - Repo author / maintainer: `<name>`
> - Author's personal aesthetic (if known from scan — blog, portfolio, prior work): `<one line>`
> - The *product* this repo is for or about: `<name>`
> - Product's iconic visual identity (from app screenshots, docs site, brand): `<one line>`
> - Existing in-repo visuals: `<list or "none">`
>
> Answer concretely:
> 1. **Identity match.** Does the brief's chosen vibe/palette/composition match *the product's* visual identity, or has it drifted into the author's personal aesthetic (or generic AI-design defaults)? If the author and product are the same entity, this question collapses to "does the brief match the maintainer's identity."
> 2. **Wow anchor.** Name the *one specific compositional move* in the brief that would make a viewer stop scrolling. If you can't name one in a single sentence, the brief is generic — flag it.
>
> For each, output: `PASS` (with a one-line reason), or `FAIL` (with a one-line reason and a one-line concrete fix — e.g., "swap Flexoki cream for Obsidian's dark + purple graph-view aesthetic," or "anchor on the product's signature graph visualization on the right half of the canvas").

**What to do with the result:**

- **Both PASS** → proceed to Phase 2.
- **Any FAIL** → revise the brief, re-show the brief block (don't re-run Gate B — one pass is enough). In Manual mode, surface the FAILs to the user and let them decide whether to apply the fix. In Auto/Semi-auto, apply fixes silently with a one-line note ("tightened brief: switched palette from Flexoki cream to Obsidian dark-purple to match product identity").

---

## Phase 2 — Build

Once the brief is locked and the user says "go", write the HTML in **one file** (`index.html` in a working directory for this repo's hero).

### 2.1 Working directory

Default layout — always nest per-repo under a subdirectory named after the target repo (e.g. `last30days-skill`, `my-cli`):

```
<current-dir>/repo-visuals-work/<repo-name>/
  index.html        # the hero animation source (GIF / PNG / HTML formats)
  index.svg         # the hero source when format is animated SVG (single file, self-contained)
  assets/           # any images/SVGs the scenario needs
```

For **animated SVG**, author `index.svg` directly as a single self-contained file — `<style>` block with CSS `@keyframes` (or SMIL `<animate>` elements) inside the SVG, all fonts embedded as `@font-face` data URIs (Google Fonts loads at render time and won't survive GitHub's `<img>` sandbox), no external assets, no `<script>`. Open the file directly in a browser to preview — the same animation that plays locally will play when GitHub embeds it via `<img>`.

Use `repo-visuals-work/<repo-name>/` so the scratch files stay obviously separate from the target repo **and** runs for different repos don't clobber each other. Never write directly into `repo-visuals-work/` — always into the repo-named subfolder. If no obvious repo name, use a short slug derived from the brief.

### 2.2 Re-read the README before writing

Open the target repo's README once more right before writing HTML. Mirror its actual phrasing, headings, and technical terms in the animation's on-screen text. The hero should feel like it was written *by* the repo author, not *for* them.

### 2.2a Consult the craft library

Before writing any scene copy or layout, read:

- `craft/headlines.md` — headline patterns (imperative-plus-invariant, narrative arc), voice rules, anti-patterns.
- `craft/templates/*.html` — full working heroes from past runs, **all upstream-merged** (the maintainers of the target repos accepted them). Read end-to-end to see how a complete scene system is composed (stage + browser chrome + tool-body + rotating hero text + progress indicator + timeline scheduler). Don't copy verbatim — steal patterns. Match by archetype, not by preference ranking.

Every scene needs a headline. A demo without copy delivers no meaning.

### 2.3 Structure of `index.html`

Single self-contained file. No build step. Sections:

1. **Stage** — a fixed container sized to the chosen dimensions (§1.7). Everything absolutely positioned inside. Outside the stage: a subtle page background so the capture crop is unambiguous.
2. **Fonts & tokens** — import fonts at the top (Google Fonts `@import`), define CSS custom properties for the palette (`--bg`, `--accent`, `--text`, `--muted`, etc.) derived from the vibe/constraints.
3. **Scene DOM** — the HTML elements that each scene uses. Build all of them upfront; scenes show/hide via classes.
4. **Timeline object** — a JS `TIMELINE` with named keys (e.g. `scene2Start: 3500`) so pacing is tweakable in one spot. Include `loopPauseAt` so the animation has a clean loop boundary.
5. **Timer helpers** — `schedule(t, fn)` wrapping `setTimeout` into an `animTimers` array, plus a `runLoop()` that clears and restarts. This is what the export pipeline calls to reset to t=0 deterministically.
6. **Scenes** — each scene is a plain function that flips classes / starts tweens. Keep CSS transitions for simple motion; use small rAF-driven tweens for counters or typing effects.

### 2.4 Rules of thumb

- **Durations**: match the chosen loop length (default 20s). Each scene ~3–6s, never so fast the viewer can't read it. Shorter dimensions (banner / slim) naturally want shorter loops — 10–15s.
- **Motion**: use `transform` and `opacity` only — never `top/left/width/height` (janky, expensive).
- **Type**: scale the minimum body size to stage height — ~2.5% of stage height, bumped up for GIF legibility. At 675h that's ~17px; at 300h that's ~14px minimum. Never below 13px.
- **Palette**: pick 4–6 colors. More kills GIF compression *and* looks busy.
- **Loop seam**: the last frame should visually match the first (or transition back smoothly). `runLoop()` is the hard reset if needed.
- **Determinism**: no `Math.random()` without a seed, no `Date.now()`-based logic. Everything must replay identically each capture.
- **Avoid the NY Times / editorial-newspaper theme**: no serif-headline + rule-lines + dateline + column-grid pastiche. It's become a default AI-design shortcut and reads as generic. Pick a visual language that actually suits the repo's domain (terminal, data-viz, spatial, playful, brutalist, neon, etc.) — not a broadsheet aesthetic unless the repo is explicitly about journalism or publishing.
- **No drift-prone claims in on-screen copy.** No version numbers, star counts, download counts, contributor counts, language-floor versions, or release dates as exact values — they go stale fast. Use `<next lower round number>+` ("40+ rules", "6k+ stars") when a number helps the pitch. Full banned/allowed list and soft-cap reasoning in `craft/rules.md`.
- **NEVER invent a logo.** The logo is core brand identity — the maintainer's, not yours to design. The §1.3 scan must look for the real one. Behavior by mode:
  - **Auto mode** → if §1.3 found a logo, **use it.** If §1.3 found nothing, render the hero **wordmark-only** — no mark at all. Do not generate a substitute. Note in the run summary whether a logo was found and used, or skipped.
  - **Semi-auto and Manual modes** → if §1.3 found a logo, use it (you may still confirm with the user that it's the right one before locking the brief). If nothing was found, **STOP and ask the user** before drawing anything. Offer three options: (a) point me to a logo file or URL, (b) proceed wordmark-only, (c) you explicitly want me to create a placeholder mark — and only if (c), describe it first and get confirmation before rendering.
  - A geometric "V"/"X"/initial-letter shape, a gradient pill with the first character, a generic database/cube/lightning glyph — **all of these count as inventing a logo.** Past failure (VeloxDB run): shipped a custom purple "V lightning" mark for a repo whose real logo (a stacked database disc with speed lines) was sitting at `<homepage>/logo-dark.svg` the whole time. Required a follow-up commit and PR push. The fetch step in §1.3 exists to prevent exactly this.
- **No fake app UI.** If the repo's product has a visible runtime UI (CLI/TUI/IDE/desktop app) and the hero contains *any* depiction of it (terminal panel, app window chrome, status bars, banners), every visible UI string and shape must come from the real app — its actual banner, prompt format, status phrases, footer chrome, command output. Invented `npm run typecheck`-style lines, generic `$` shell prompts, made-up status indicators all read as a hollow simulation to anyone who actually uses the tool. Pull real strings from screenshots, repo source (status constants, hook output, banner generators), or — best of all — a screen recording the user provides. If you can't access the real vocabulary, *flag the gap and ask* before drafting; don't invent. This rule cost two prior runs (Terminal.Gui simulated UI, clawd-on-desk v1–v2 fake terminal) and the third (clawd-on-desk v3+) only became authentic after extracting frames from a user-supplied `.mov`. See also §1.3's screen-recording prompt.
- **README-voice over slogan-voice in hero copy.** Default rotating headlines, captions, and overlay text to README-style status-readout shape (colored pip + bold one-word state label + factual phrase, optionally a dim subtitle of concrete context) — not punchy two-line marketing slogans. Anti-patterns: imperative-then-twist ("Walk away. Come back."), "So you don't have to" / "So it just works" patterns, hero-text title pairs in big bold + accent-colored phrase. The user calls these "silly". Status-readout shape (`● thinking · reading your codebase`, `● juggling · 3 subagents in parallel`) feels like the repo's own activity log. See `craft/headlines.md`.
- **Layout discipline (split-stage, anchors, scoping).** The bullets that bite during build:
  - Don't pin a left-column's bottom row flush to the edge — center the column or leave ≥32 px breathing room.
  - Don't let one column run empty while the other fills — match density with secondary content right under the title block, not bottom-pinned 200 px below.
  - Bottom-anchored footer elements need ≥40 px clearance and ≥32 px gap above. If the math doesn't work, shrink stage height — don't just nudge.
  - Scope generic class selectors to a region (`.form .row`, not bare `.row`) so they don't leak into the rest of the stage.
  - On-screen labels must read cold — no cryptic abbreviations a first-time viewer can't decode in two seconds.
  - Symmetry is load-bearing — top-pad = bottom-pad, left-margin = right-margin. When shrinking a right-anchored element, preserve its left-edge position, not its right margin.
  - Full incident write-ups for each in `craft/rules.md`.
- **Preview-vs-export parity.** The HTML the user previews must equal the exported pixel grid: pin the stage at `(0, 0)`, treat `box-shadow` as preview-only, never let content exceed the stage, always pass an explicit `clip` to `page.screenshot()`, and visually diff the export against the HTML before declaring done. Detail in `craft/rules.md`.
- **Retina quality is mandatory.** Capture at 2× always (PNG via `deviceScaleFactor: 2`; GIF via the zoom-fallback in `craft/export.md`). Source font floor on a 1200-wide canvas is ~15.5 px body / ~12.5 px metadata after GitHub's ~0.83× downscale. The own benchmark is "looks like a native MacBook retina screenshot" sitting next to other chrome on the README.
- **Embedding a user- or reviewer-provided asset has its own rulebook.** Loop must equal or cleanly divide the outer loop; keep inner at native resolution; budget palette by keeping outer chrome low-chroma; never silently replace a reviewer's asset. Full version in `craft/rules.md`.

### 2.5 When to stop writing and preview

First preview as soon as:

- All scenes are implemented (even if polish is rough)
- Timing hits the full duration target
- No console errors

Don't polish before first preview. User's reaction on overall shape is more valuable than Claude's local polish loop.

### 2.6 Gate B — rendered HTML vs README (repo-context check, pre-export)

Once `index.html` is ready and §2.5's stop conditions are met, run a **vision-based check on the rendered HTML before any GIF/PNG export.** Same narrow scope as Gate A — only repo-context fidelity (does what's on screen match what the README says about this repo?). Aesthetic, technical, and craft compliance are explicitly out of scope; those are caught by taste and the dev-mode scorecard, not by an iteration-triggering gate.

This catches the brief→pixels gap: the right brief can still produce text that drifted from README phrasing, a scene that undercounts the repo's real inventory, or copy that quietly implies something the "what NOT to imply" list ruled out.

**Why on HTML, not the exported artifact:** an export cycle is expensive (GIF: capture + ffmpeg ~30s+, PNG: Puppeteer ~3s but still wasted if the critique fails). Running the check on Puppeteer screenshots of the HTML keeps it in the same cheap loop as build, so an iteration is "edit HTML, re-screenshot, re-critique" — no encoder in the inner loop.

**Mode interaction:**

| Mode | Gate B behavior |
|---|---|
| **Auto** | Run silently. If FAIL, apply 1 auto-iteration (edit HTML, re-screenshot, re-critique). After 1 retry, proceed regardless and note remaining issues in the hand-off. |
| **Semi-auto** | Run once silently before showing the artifact. If FAIL, apply 1 auto-iteration before the human preview. Surface a one-line "Gate B caught and fixed: [X]" so the user knows. |
| **Manual** | Skip — the human is the critic. Optional: offer to run it as a "second opinion" if the user asks. |

**Capture step** (no ffmpeg):

- Animated: call `scripts/screenshot.js` 4–5 times at evenly-spaced `--seek` values across the loop duration (the script uses `window.seekTo(t)` if exposed by the HTML; otherwise design the HTML to expose it — see §2.3 timeline helpers). Output to `repo-visuals-work/<repo>/critique-frames/`.
- Static: a single `scripts/screenshot.js` call at `deviceScaleFactor: 2`.

**Critique prompt** — narrowed version of §6.3, repo-context only:

> You are checking the rendered hero for `<owner/repo>` against the repo's own positioning. Only judge whether what's on screen matches the README — not whether it looks good, not whether the design is original, not whether type is well-set. Aesthetic and craft judgments are out of scope here.
>
> **Repo ground truth:** `<README first 40 lines, real inventory count, stated hero moment, audience, "what NOT to imply" list>`
>
> For each frame, rate (1–5, default 3, evidence required to move):
> - **Voice match.** Does on-screen text use README phrasing and terminology, or drift to generic marketing voice?
> - **Intent delivery.** Does the hero deliver the *why* a viewer would reach for this repo, grounded in what the README claims — not just *what* the repo does?
>
> Also flag binary issues (PASS/FAIL):
> - **Scope undercount.** Does any "all" / "every" / grid claim match the real inventory? If not, is it explicitly framed as a sample?
> - **Don't-imply violations.** Does anything on screen suggest something from the "what NOT to imply" list?
>
> Cite specific frames in every observation. Do not comment on color, layout, animation polish, or design taste.

**Pass/fail rule (narrowed):**

- **Pass** = Voice match ≥ 3, Intent delivery ≥ 3, no scope undercount, no don't-imply violation.
- **Fail** = any of: Voice match ≤ 2, Intent delivery ≤ 2, scope undercount, don't-imply violation.

Aesthetic / legibility / loop-duration / palette concerns are **not** Gate B's job. They surface in the dev-mode scorecard (§6) and as user-visible feedback in Phase 3, but they don't trigger the retry. This keeps Gate B from manufacturing busywork on artifacts that are visually fine but technically borderline (real incident: the original 28s clawd-on-desk hero would have triggered a Code-row FAIL on loop duration, the resulting fix was perceptually invisible — the gate did nothing useful).

**On fail, exactly one retry:** identify the most-cited concrete repo-context problem from the critique notes (not all of them — that invites whiplash). Edit the HTML to fix that one thing. Re-screenshot. Re-critique. After the retry, proceed to Phase 3 (Semi-auto) or Phase 4 (Auto) regardless of the second result — log remaining issues for the user.

**Why one retry, not many:** the critic and the generator are the same model. More than one auto-iteration risks sycophantic loops or whiplash between two equally-flawed designs. One retry forces a single decisive fix and stops.

---

## Phase 3 — Preview & iterate

Keep this phase conversational. The goal is to converge on a version the user loves before spending time on export.

### 3.0a Render self-critique (before showing the user)

**Do this every time** before presenting any rendered hero artifact (HTML preview screenshot, exported PNG, exported GIF) to the user. Skipping it makes the user the QA pass — that burns trust.

**The procedure:**

1. **Read the rendered file** (use the Read tool on the PNG/GIF, or take a screenshot of the HTML preview) — actually look at it, not just the source.
2. **Write 3–5 honest critique bullets to yourself** before composing the user-facing message. Look specifically for:
   - **Text overflows / wraps** — chips wrapping into the wrong row, headlines breaking awkwardly, labels clipping the stage edge.
   - **Overlapping or colliding elements** — two pieces of copy occupying the same visual zone (e.g. a meta strip stacked on top of a ghost label stacked on top of a graph node label).
   - **Redundant copy across regions** — eyebrow and meta and chips all repeating the same word (e.g. "spec" appearing three times).
   - **Scope-claim mismatches** — image says "all" / shows a grid of N items, real inventory is bigger or smaller.
   - **Color/vibe drift from the locked brief** — the rendered output looks more muted, busier, or more generic than the brief promised.
   - **Wow check** (carry-over from §1.8b) — is there still one anchor move that makes a viewer stop scrolling, or did it get washed out in execution?
3. **Fix anything obvious in the bullets**, re-render, and read it again.
4. **Only then** present to the user, and proactively call out any issues you noticed but chose not to fix yet ("`obsidian-markdown` wraps to two lines in its card — can tighten the type if you want, otherwise leaves it").

**This applies in every operating mode.** Auto and Semi-auto skip *optional questions to the user*, not *quality gates against the artifact*. If anything, Auto's "ship fast" pace makes the self-critique gate more important, not less, because there's no preview round to catch the issues for you.

**Real incidents this prevents:**

- A static PNG shipped with: a `web defuddle` chip wrapping into a second row that overlapped the graph SVG, three competing pieces of text crowding the top-right corner (meta + ghost wikilink + node label), and a "graph view" footnote colliding with the chip row. All three would have been caught by one honest look at the rendered file.
- A first-pass hero shipped with the right facts but no compositional anchor — drew "I don't feel wow when first see it" from the user. Earlier render-time critique combined with §1.8b's wow check would have caught it before the user did.

### 3.1 Open in browser

After writing `index.html`, **give the user the command** to open it themselves (their browser, their timing):

- **Windows**: `start repo-visuals-work/<repo-name>/index.html`
- **macOS**: `open repo-visuals-work/<repo-name>/index.html`
- **Linux**: `xdg-open repo-visuals-work/<repo-name>/index.html`

Tell them to watch **one full loop** (the animation restarts automatically via `runLoop()`).

### 3.2 What to ask after first preview

Keep first-preview questions focused on **shape**, not polish:

- Does the *hero moment* land?
- Does the overall pace feel right (too fast? too slow?)
- Does any scene feel confusing or unnecessary?
- Does the loop seam look clean?

Don't ask about colors/fonts/spacing on the first round. Polish comes after shape is right.

### 3.3 Iteration rhythm

- Each round: Claude edits, user refreshes, one sentence of reaction.
- After shape converges, switch to polish rounds: type hierarchy, color calibration, micro-timing, loop seam.
- If user gives vague feedback ("feels off"), ask **one pointed question** to narrow it — don't guess.
- **Iterate on HTML, not on exports.** During the iteration phase, edit `index.html` and let the user preview via their browser (`open .../index.html`). Do **not** re-run the Puppeteer screenshot / GIF export on every round — it burns time and tokens for no gain since the browser preview is the source of truth for layout and color. Export *once* at the end on the ship signal (and once mid-build only if §3.4 GIF sanity check applies). If the user explicitly asks for a fresh PNG/GIF mid-iteration (e.g. to share a draft externally), that's the only reason to re-export before ship.
- **Style stuck? Invoke `frontend-design` — and offer it proactively.** If the user has gone back-and-forth on *style* (palette, type, overall aesthetic, visual language) for **3+ rounds** without converging — or says something like "still not it" / "try a totally different direction" — stop tweaking in place. In Manual mode, ask the user before invoking. In Semi-auto/Auto, **proactively surface the option** ("we've done 3 style rounds without converging — want me to invoke `frontend-design` for a fresh design pass, or keep iterating?") rather than silently continuing to tweak. Don't wait for the user to remember the option exists; the rule says you suggest it. Pass `frontend-design` the brief, the repo scan summary, the current `index.html`, and a plain-language description of what's not working. Use its output as the new starting point, then return to this iteration loop. Don't invoke it for pacing, timing, or animation-logic feedback — only when the blocker is *visual design quality*.

### 3.4 Mid-build GIF sanity check *(only if GIF is a target output)*

GIF quantization causes specific failures that HTML preview hides: small text blurs, near-identical hues posterize, fine gradients band. If GIF was selected in §1.4, run the export pipeline **once** at ~70% polish so these surface before the final polish rounds. Check:

- Is small text still legible?
- Do any colors posterize badly?
- Does the animation feel the same speed as the HTML?

If problems appear, tune the HTML (bigger type, fewer palette neighbors, simpler gradients) and keep iterating on the preview.

**Skip this section entirely if the output is not a GIF** (MP4/WebM preserve HTML fidelity; static outputs are sampled directly; animated SVG renders identically to the source — no quantization).

**Animated SVG sanity check (replaces the GIF check when SVG is the chosen format):** open the `index.svg` file as `<img src="index.svg">` inside a throwaway `preview.html` (not by opening the SVG directly — that path uses the document context, not the image-embed sandbox GitHub uses). Confirm: animations play, fonts render (if any are embedded), no console errors, no broken external references. If anything renders only when opened directly but not via `<img>`, you've leaked a script tag, an external font URL, or a hover-driven animation — fix in the source, re-test.

### 3.5 Stop signal

Stop iterating when the user says "ship it" (or equivalent). Don't invite more rounds — excess polish is real cost. If Claude thinks there's still a clear improvement available, mention it *once* and let the user decide.

### 3.6 Deliver all the intent, even unstated

The user may not fully know what they want. Keep watching for mismatches between the scan/brief and the HTML behavior:

- Did the README say "fast"? The hero should feel quick, not luxurious.
- Is the audience newcomers? Don't assume they know jargon — the hero's text should echo README phrasing.
- Did the brief say "calm"? Check for accidental frenetic motion (fast cuts, snappy eases).

When you spot a mismatch, flag it proactively ("the README leans 'fast' but the current pacing is slower — intentional, or should we tighten?"). Deliver intent, not just instructions.

**"Reduce" means reduce — directional verbs are load-bearing.** When the user pairs a directional verb (*reduce*, *smaller*, *tighten*, *cut*, *shrink*, *trim*) with a relational clause (*"so A equals B"*, *"to match X"*), treat the directional verb as the binding constraint. If executing the relational clause would violate the direction — e.g., equalizing padding by growing the demo — stop and restate rather than execute. Incident detail in `craft/rules.md`.

---

## Phase 4 — Export

### 4.0 Entry gate — do not skip

Before you export anything, confirm — the exact gate depends on operating mode (§1.1a):

| Gate item | Manual | Semi-auto | Auto |
|---|---|---|---|
| User has **seen the artifact running** (open in browser or rendered screenshot) | required | required | skipped |
| At least **one iteration round** after first look | required | required | skipped |
| **Scope match** — hero claims (*"all"*, *"every"*, grid/list representing the repo) match real inventory from §1.3, or explicitly framed as sample ("10 of 30", "30+", scroll affordance) | **required** | **required** | **required** |
| User has explicitly said ship / go / export | required | required (after 1 preview) | not required |

The scope-match rule is **non-negotiable in every mode** — it's a craft check, not a human-involvement question. The human-in-the-loop items are what modes toggle.

Export is the **last** step, not a midpoint. A capture→encode→evaluate cycle feels productive but burns the user's patience on a draft that wasn't ready. When in doubt between "export this pass" and "one more iteration", prefer the iteration — except in Auto mode, where the point is to deliver a first draft fast and let the user redirect.

### 4.1 Prerequisites (ask before installing)

Check presence, list missing, ask the user before installing:

- **Node.js + `puppeteer`** — via `node --version` and looking for `node_modules/puppeteer`. If missing: `npm install puppeteer` (~170MB Chromium download).
- **`ffmpeg`** — via `ffmpeg -version`. If missing:
  1. Prefer system package manager (`choco install ffmpeg`, `brew install ffmpeg`, `apt install ffmpeg`) — needs admin.
  2. On Windows without admin, download **portable** ffmpeg from `https://github.com/GyanD/codexffmpeg/releases/latest` and extract `ffmpeg.exe` into the skill's `bin/` dir. Do NOT add to PATH; call by absolute path.

Never install silently. Show the plan, ask, then act.

### 4.2 Branch on chosen format

Based on the format decided in §1.4c:

- **Animated GIF** → run the GIF pipeline. Recipe in `craft/export.md`.
- **Static PNG** → run the static pipeline. Recipe in `craft/export.md`.
- **Animated SVG** → no rasterization step. The `index.svg` authored in Phase 2 *is* the artifact. Validate it before hand-off:
  1. Strip any `<script>` tags (sanitizer drops them anyway; cleaner to remove now).
  2. Confirm every font is embedded as `@font-face` data URI — no `https://fonts.googleapis.com/...` imports.
  3. Confirm no external `<image href>` URLs — embed any raster as `data:` URI or rebuild as vector.
  4. Render via `<img src="index.svg">` in a throwaway `preview.html` and visually confirm the animation matches the direct-open preview.
  5. Check file size — target ≤ 200 KB, hard cap 500 KB. Over budget usually means an embedded raster doesn't belong; reconsider format or extract the raster.
  - For terminal/UI demos with **per-character typewriter typing** (cmder-style heroes), hand-authoring the SMIL keyTimes is unmaintainable. Switch to a generator script (`build-svg.js`) that mirrors the HTML's `COMMANDS` data — full ruleset (CSS-vs-SMIL, `calcMode="discrete"`, caret structure, verification protocol) in `craft/svg-animation.md`. Read that file before writing any generator code.
- **HTML only** → skip Phase 4 entirely; the hand-off is `repo-visuals-work/<repo-name>/index.html`.

`scripts/capture.js` (GIF) and `scripts/screenshot.js` (PNG) wrap the recipes; both default to 2× retina and accept `--width` / `--height`. Don't hardcode 1200×675 in invocations — pass what the brief locked in. Animated SVG has no capture script — the file is hand-authored and shipped as-is.

### 4.3 Output file name

- Animated GIF → `repo-visuals-work/<repo-name>/hero.gif`
- Static PNG   → `repo-visuals-work/<repo-name>/hero.png`
- Animated SVG → `repo-visuals-work/<repo-name>/hero.svg` (rename of validated `index.svg`)

Keep in the scratch dir until Phase 5 (Output) moves it.

### 4.4a Render self-critique (post-export)

After every export — PNG, GIF, or otherwise — **re-run §3.0a on the exported file**, not just the HTML preview. The export pipeline can introduce its own failure modes (GIF quantization blurs small text, palette banding, retina vs non-retina rendering differences, ffmpeg seam glitches) that don't show up in the HTML.

The discipline is the same: Read the file, write 3–5 honest critique bullets, fix obvious issues, re-export, then present. Do not show the exported artifact to the user until §3.0a-style critique has run on it.

If the post-export critique surfaces an issue that requires HTML changes (not just an encode tweak), go back to Phase 3 to fix the source — don't try to patch around it in the export step.

---

## Phase 5 — Output

Move `hero.gif` / `hero.png` from the scratch dir into the target repo, update the README, optionally open a PR. Full mechanics in `craft/ship.md`. Decision-tree headlines:

- **Placement.** Infer from convention (`assets/` → `docs/` → `.github/` → default `assets/hero.gif`); ask before creating dirs. Default to **image + README line only** — no `hero.html`, no maintenance docs, unless the reviewer asks, the repo has precedent, or the user opts in. (Premature source-bundling is a top reviewer complaint — see `craft/ship.md` for incident links.)
- **README embed.** Insert at the top by default; replace existing only with confirmation. **Alt text is informational** — convey the stats / positioning the image shows, not just `<repo-name> demo`. **Always use relative paths** — never `raw.githubusercontent.com/...`, even if the rest of the README does (legacy debt; doesn't render in forks/PR previews).
- **Commit & PR.** Branch `docs/add-hero-gif` unless repo convention differs. Co-author footer **default OFF** — only on explicit opt-in. **Provenance footer default ON** for hero PRs — append `> Generated with [repo-visuals](https://github.com/livlign/claude-skills) — happy to iterate on changes.` as the last line of the PR body, and verify it's there in a pre-flight check before `gh pr create`. Skip only when target culture argues against (AI-PR ban in CONTRIBUTING) or it's a non-hero PR. Cannot be retrofitted post-merge — get it right at submission. User-owns-repo → push to origin; doesn't-own → `gh repo fork --clone=false` then `gh pr create --repo <upstream> --head <user>:<branch>`. Not authed correctly → stop and ask.
- **Hand-off.** Report PR URL, file size, placement path, one-line README diff. End with a single-line `SHOWCASE.md` invite — never let it crowd the hero hand-off, never re-surface it.
- **Local-only opt-out.** If no PR wanted, leave the file in `repo-visuals-work/<repo-name>/` and print the path; don't touch the target repo.

Read `craft/ship.md` end-to-end before running this phase the first time on a given repo.

---

## Phase 6 — Evaluate *(dev mode only — skip in normal runs)*

**Gate:** run this phase only when dev mode is active (user said "dev mode" this run, or `REPO_VISUALS_DEV=1`). In every other run — Manual, Semi-auto, Auto — stop after Phase 5. Do not ask user-rating questions, do not write run logs, do not mention this phase.

In dev mode, score the **final artifact** (not the process) across four rater types — User (3 rows), Claude (1 row), Code (auto via `scripts/evaluate.js`), AI (vision pass on extracted keyframes, blind to prior chat). Use the labeled 1–5 scale (`5 / Excellent` style). Skip User rows in Auto mode and flag accordingly.

Write run logs to `./evaluations/runs/<YYYY-MM-DD>-<slug>.md` in the user's working directory (NOT the plugin cache — wiped on `/plugin update`). Curated rolling stats live in `./evaluations/index.md`, edited by the `repo-visuals-retro` meta-skill.

Full criteria tables, the fixed AI-eval prompt (with anchored ground-truth and the "default to 3, lower-by-one if you can name an improvement" protocol), the `AskUserQuestion` shape for User rows, and the scorecard template all live in `craft/evaluate.md`. Read it before running this phase.
