---
name: data2story-pro
description: "Use to turn a dataset into a verifiable multimedia blog (a data story / data-driven article / interactive dashboard from a dataset). Orchestrator for the Data Journalist Agent (Data2Story): a 7-team newsroom (14 agents) running detective → scout → analyst → imagineer → editor → copywriter → designer → interaction → hero → cinematographer → programmer → auditor → critic → inspector in sequence. Trigger when the user hands over a dataset (CSV/JSON/folder/path) and wants a published story, blog post, or interactive report built from it. Creates a versioned project folder per run."
argument-hint: [data path | URL | idea]
allowed-tools: Bash(*), Read, Write, Glob, Grep, Skill, Agent, WebSearch, WebFetch
---

# Data Journalist Agent (Data2Story)

Turn **$ARGUMENTS** into a blog. Orchestrates the roles below in sequence.

## Orchestration rituals

Five process rules earned from real runs. Each is one rule + why it exists; follow them across every run regardless of topic.

- **(D1) Candidate-image review loop.** For any hero/cover image of a named person or specific real object, generate **N candidates**, then run a VLM (or human) review and **select** one — never ship the first render. *Why:* text2image of named people intermittently refuses outright and quality varies shot-to-shot, so a single render is a coin-flip; a small candidate pool plus a review step is the only reliable way to land a usable, correctly-identified image.
- **(D2) Audit-before-finalize.** Run the read-only multi-agent audit (provenance / repro / assets / IP lenses) to **find** every defect FIRST, collect them, and only THEN make one editing pass to **fix** them. *Why:* interleaving find-and-fix makes agents edit the same file against a moving target and re-introduce each other's defects; separating the finding phase from the fixing phase prevents that churn.
- **(D3) Single owner of one big file.** Parallel agents may produce data and assets concurrently, but exactly **ONE** agent writes `index.html`. *Why:* the HTML is one indivisible artifact; concurrent edits to it interleave and corrupt it, so it must have a single writer even when everything feeding it is parallel.
- **(D4) Headless-verify-then-defer-render.** Prove everything you can **without** a browser — `node --check` the scripts, recompute a known model output and compare, byte-compare each inline JSON island to its `verify/` file — then hand the final visual/browser sign-off to the **user**. *Why:* deterministic checks catch the failures that don't need eyes cheaply and early, while genuine render correctness needs a real browser this harness can't drive, so the human does that last mile (see also the chart-width-0 class of bug, invisible to node shims).
- **(D5) Verify-coexistence-with-zero-engine-edits.** New interactive features layer **on top of** the frozen Verify engine (the in-page Inspector panel + `verify/` artifacts); never edit the engine to make a feature fit. *Why:* the Verify layer is the paper's coding verifier and a hard gate — editing it to accommodate a feature risks silently breaking provenance, so features adapt to it, not the reverse.

## The 7 teams

The newsroom is **7 teams** (the paper's 7 canonical roles), staffed by **14 agents**. Two teams are a single agent; five are a small team with a **lead** who coordinates one or more members. The folders stay flat and every `Skill <name>` call resolves by the member's frontmatter `name:` — the teams are a coordination overlay, not a folder move. **You (this orchestrator) are the top coordinator across all 7 teams.**

| Team (paper role) | Lead | Members | Kind |
|---|---|---|---|
| **Detective** | Detective | + **Scout** | multi-agent |
| **Analyst** | Analyst | + **Imagineer** | multi-agent |
| **Editor** | Editor | + **Copywriter** | multi-agent |
| **Designer** | Designer | + **Interaction** + **Hero** + **Cinematographer** | multi-agent |
| **Programmer** | Programmer | — | single-lead |
| **Auditor** | Auditor | + **Critic** (+ **Playtester** step) | multi-agent |
| **Inspector** | Inspector | — | single-lead |

Each lead's `SKILL.md` carries a "Team coordination" section describing how it briefs and integrates its members; the member `Skill <name>` calls below are **mirrored** in those sections so a member is never silently skipped. The cross-team checkpoints (the two gates and the Critic revision loop) are **owned by this top orchestrator**, not delegated into any team.

## Setup

Resolve paths before doing anything:

- Never hard-code machine-local paths and never ask the user to export path variables.
- Resolve `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro`)
- Resolve `ARCHIVE_DIR` = the ancestor directory that contains `skills/` (two levels up from `SKILL_DIR`, i.e. `SKILL_DIR/../..`)
- Resolve `DATA2STORY_ROOT` = parent of `ARCHIVE_DIR`
- Commands below use symbolic placeholders such as `ARCHIVE_DIR`; replace them with resolved, quoted paths before running Bash.
- `DATA_NAME` = the dataset folder name (e.g. `pick_a_card`). In URL / IDEA mode it is taken from the `DATA_DIR` that **Stage 0 — Input dispatch (below)** resolves, so run Stage 0 before resolving `PROJECT_DIR`.
- `DATA_DIR` = the validated dataset folder, resolved by **Stage 0 — Input dispatch** below. It originates from one of: the existing path in `$ARGUMENTS` (DATA MODE, path); `find-data`'s output folder (DATA MODE, URL); or `ideation`'s output folder (IDEA MODE). For a bare dataset name with no Stage-0 acquisition, fall back to `DATA2STORY_ROOT/data/{DATA_NAME}`.
- `TIMESTAMP` = current time formatted as `MMDD_HHMM` (e.g. `0401_1618`): `date +%m%d_%H%M` (run in bash)
- `PROJECT_DIR` = `DATA2STORY_ROOT/project/{DATA_NAME}/blog_{MODEL}_{TIMESTAMP}`
- Create `PROJECT_DIR/`, `PROJECT_DIR/assets/`, `PROJECT_DIR/code/` — **after Stage 0 has resolved `DATA_DIR`/`DATA_NAME`** (immediate in path mode; after the Stage-0 acquisition in URL / IDEA mode).
- Write `PROJECT_DIR/run_config.json` = `{"run_profile": "premium"}` or `{"run_profile": "fast"}` from the Stage-0 *Run profile* decision (below). `validate.py`/`generate_viewer.py` read it; absent ⇒ `premium`.

> **Windows:** there is usually no `python3` on PATH — run the `python3 …` commands in this skill as `py` (or `py -3`). Set `PYTHONUTF8=1` (e.g. `$env:PYTHONUTF8=1`) to avoid GBK console errors when scripts print Unicode.

> **Sibling-skill dependency.** This skill requires the sibling skills **`frontend-design-pro/`** and **`dataviz-craft/`** to live under the same `skills/` parent (`ARCHIVE_DIR/skills/`). The Designer/Programmer/Auditor/Critic borrow their component recipes, design tokens, quality rubric, and dataviz craft from them via `../frontend-design-pro/...` and `../dataviz-craft/...` relative paths. **Deploy all three together** — `data2story-pro/` alone is incomplete; a clone missing either sibling will break the design/audit references. **IDEA MODE additionally requires** the sibling skills **`find-data/`** and **`sparring-partner/`** under the same `skills/` parent: Stage 0's `ideation` sub-skill drives `sparring-partner` to converge a topic and `find-data` to acquire a real dataset. A clone missing either of these two can still run DATA MODE (a path or URL), but cannot run IDEA MODE (an empty/free-text idea).

## Stage 0 — Input dispatch (data path · URL · idea)

Classify `$ARGUMENTS` before resolving `DATA_DIR`. This stage decides how `DATA_DIR` is obtained; every later stage (Detective → … → Inspector) is identical regardless of which branch ran. **FIRST match wins:**

1. **Empty / whitespace** → **IDEA MODE** (open by inviting the idea: "what do you want to tell a story about?").
2. **An existing path on disk** (`$ARGUMENTS` resolves to a file or directory) → **DATA MODE**. The current behavior, unchanged: set `DATA_DIR` to that path and proceed into the pipeline.
3. **A data URL** (`$ARGUMENTS` starts with `http://` or `https://`) → **DATA MODE via find-data url-mode**. Run `Skill find-data "<url>"` — it fetches the resource and validates it against the 4 completeness gates, producing a dataset folder. Set `DATA_DIR` to that folder and continue the pipeline.
4. **Otherwise (free-text prose, not a path)** → **IDEA MODE**.

**Ambiguity guard.** If `$ARGUMENTS` LOOKS like a path (contains a slash, a drive letter, or a file extension) but does NOT exist on disk, do **one** quick confirmation question instead of silently treating it as an idea — e.g. "that looks like a path but I can't find it; did you mean a dataset folder, or a topic to research?" — and branch on the answer.

### IDEA MODE

Hand the user's idea to the `ideation` sub-skill, passing the raw `$ARGUMENTS` text verbatim and the resolved `DATA2STORY_ROOT`:

```
Skill ideation "<raw $ARGUMENTS>" <DATA2STORY_ROOT>
```

`ideation` runs the brainstorming dialogue (reusing `sparring-partner`) to converge the vague idea into one concrete data-story topic, then runs `find-data` to acquire a real, validated dataset — with a user checkpoint after each step — and returns exactly one of:

- **`DATA_DIR=<absolute path to the validated dataset folder>`** — success. A `story_brief.json` will sit at `<DATA_DIR>/meta/story_brief.json`. Set `DATA_DIR` and `DATA_NAME` from this folder and proceed into the EXISTING pipeline unchanged (Detective → … → Inspector). Nothing downstream differs.
- **`IDEATION_ABORTED: <reason>`** — the user aborted, or no adequate real dataset could be found. **Halt gracefully** with an honest one-line message that relays the reason. Do NOT run the pipeline, and do NOT fabricate data or a dataset to "succeed".

### Run profile — Fast vs Premium (select ONCE, then commit)

Data2Story ships **two committed profiles**. Resolve the profile **once, here at Stage 0**, and write it to `PROJECT_DIR/run_config.json`; do not revisit it mid-run. A profile is a self-consistent bundle (which stages run AND the matching gate set), **NOT** a pile of per-stage toggles.

- **`premium`** (default) — the full 14-agent newsroom: verified media (Scout), interactive playgrounds (Imagineer + Interaction), an animated cover (Hero), a cinematic scroll (Cinematographer), titling (Copywriter), the Critic revision loop, and the **full runnable verify layer** (in-page panel + runnable Pyodide cells + a reproducible notebook). ~2h40–2h50. The flagship.
- **`fast`** (~15–25 min) — the **7 canonical roles only**: Detective → Analyst → Editor → Designer (charts + static images, no media generation) → Programmer → Auditor → Inspector. Keeps the in-page **traceability** panel (click any claim → its code/source) but NOT the runnable cells / reproducible notebook. Skips Scout, Imagineer, Copywriter, Interaction, Hero, Cinematographer, and the Critic loop. The premium floors (mandatory cinematic / BGM / richness / engagement / runnable-verify / playtest) do not apply.

**Resolve it:**
1. If `$ARGUMENTS` contains **`--fast`** → `fast`; **`--premium`** → `premium`. **Strip the flag** from `$ARGUMENTS` before input dispatch. A headless/automated call with no flag defaults to `premium`.
2. Otherwise (interactive, no flag) → ask **one** `AskUserQuestion`: *"Fast (~15–25 min — charts + static images, traceability only) or Premium (~2h40–2h50 — the full cinematic/interactive flagship)?"*
3. Write the choice to `PROJECT_DIR/run_config.json` as `{"run_profile": "premium"}` or `{"run_profile": "fast"}` right after `PROJECT_DIR` is created (Setup). **`validate.py` and `generate_viewer.py` read this file; absent ⇒ `premium`**, so the default and every automated call is the full flagship.

Each stage heading below is marked **[premium]** when the `fast` profile skips it; unmarked stages run in both.

## Archival

Immediately after creating `PROJECT_DIR`, snapshot the current skills:

```bash
mkdir -p PROJECT_DIR/archival
cp -r ARCHIVE_DIR/skills PROJECT_DIR/archival/skills
```

This preserves the exact skill versions used for this run.

## Tools available

All media tools route through OpenRouter. Set `OPENROUTER_API_KEY` before any generation call.

Media generation is the Designer's job, so the media tools (text2image, text2video, image2video, text2music, embeddings) live under `SKILL_DIR/designer/scripts/openrouter-*/`. The full list — default models and exact `python3 ...` invocations — is in **[`designer/references/tools.json`](designer/references/tools.json)**; full per-tool docs are each tool's own `SKILL.md` under `SKILL_DIR/designer/scripts/openrouter-*/`. Note: `text2music` is for opt-in atmospheric **sound-design / SFX** (un-findable sounds — drones, textures, best-effort foley), NOT the front-of-blog BGM — the BGM must be a **sourced real track** (sourced_bgm, found by the Scout), never AI-composed.

## Pipeline Overview

The pipeline is a single linear sequence that produces a traceable HTML blog from raw data:

```
DATA → Detective → Scout → Analyst → Imagineer → Editor → Copywriter → Designer → Interaction → Hero → Cinematographer → media-purpose + richness + cinematic-supply gates → Programmer → Auditor + Playtester → contract gate → Inspector verify.py (Stage 6.4 → verifier.json) → Critic (bounded loop, <=2 rounds; signature-move pass bar R9 = every dim >=4 AND >=1 dim >=5; re-runs Programmer + Auditor + validate.py + verify.py each round) → Inspector generate_viewer.py (Stage 7, REQUIRED terminal step — MUST exit 0) → final index.html (with the in-page Inspector panel) + verify/ artifacts
```

> **Two profiles (set once at Stage 0).** The sequence above is the **`premium`** flagship. The **`fast`** profile (~15–25 min) runs only the **7 canonical roles** — Detective → Analyst → Editor → Designer (charts + static images) → Programmer → Auditor → Inspector — keeping the in-page **traceability** panel but skipping every stage whose heading is marked **[premium]** (Scout, Imagineer, Copywriter, Interaction, Hero, Cinematographer, the Critic loop) plus the runnable-verify cells + notebook. Its gate set drops the premium floors (cinematic / BGM / richness / engagement / playtest / runnable-verify) to match. Absent `run_config.json` ⇒ `premium`.

> The **Imagineer** (Stage 2.5) fans out candidate interactive concepts; the **Editor** curates them into the hero + supporting set; the **Copywriter** (Stage 3.5) re-titles the masthead + every section title + every figure/photo/table caption to a titling standard that kills the AI-tell patterns (strings only — names, never edits); the **Interaction Engineer** (Stage 4.5) builds that whole SET (not just one centerpiece); the **Hero** (Stage 4.6) crafts the animated cover; the **Cinematographer** (Stage 4.7) consumes that cover as its first scene (`cin_00`); the **Playtester** (a step inside the Auditor team at Stage 6) drives every built playground in a real browser before the contract gate.

> **A run is INCOMPLETE — do NOT present it as finished — if the contract gate (`validate.py`) Section 7 reports any `verify_*` error, OR Section 15 reports any `send_back_open` / `playtest_hard_unresolved`, OR `generate_viewer.py` (Stage 7) exits nonzero.** The verify layer is the paper's coding verifier; it is a hard pipeline gate, not an optional flourish, and "the panel and `verify/` artifacts are mentioned as MANDATORY" is enforced by those deterministic checks, not by prose alone. A left-`open` detected defect (a Section-15 `send_back_open` / `playtest_hard_unresolved`) blocks flagship in the same class as a `verify_*` error.

Run each stage in order. Each stage reads the previous artifact(s) before starting. Do not proceed to the next stage until the current artifact is complete.

> **Model tier (optional).** The mechanical stages — the Programmer's HTML build and the Inspector's scripts (`verify.py`, `generate_viewer.py`) — are deterministic and run fine on a cheaper/faster model; the creative and analytical stages (Detective, Analyst, Editor, Designer, Interaction, Critic) benefit most from a strong model. Spend the budget where judgment matters.

The stages below are grouped under their **team** heading. The stage numbers, Input/Output, What, and `Call` lines are unchanged — run them in the same linear order regardless of grouping.

#### Detective team — context + verified media (lead: Detective; member: Scout)

### Stage 1 — Detective
Input: `DATA_DIR`
Output: `PROJECT_DIR/detective.json`
What: Researches external context — background knowledge, domain history, related findings, why this data matters. Each finding gets a `det_xx` ID.

### Stage 1.5 — Scout [premium]
Input: `DATA_DIR`, `PROJECT_DIR/detective.json`
Output: `PROJECT_DIR/scout.json`, `PROJECT_DIR/assets/scout_*`
What: Sources and **verifies** rich external media the Detective's background pass didn't cover — license-clean music for the front-of-blog BGM, high-value real photos/video of the story's key subjects, and the latest live status (timestamped, display-only). Every asset carries a checked `license` (permits republication) and `identity` (it is what the caption claims) block; each item gets an `sct_xx` ID. The pipeline's **media verifier** — what it passes downstream is legally usable and correctly identified. Skips lightly for abstract/statistical/privacy-sensitive datasets (records why).

Call: `Skill scout DATA_DIR PROJECT_DIR`

#### Analyst team — quantitative analysis + interactive ideation (lead: Analyst; member: Imagineer)

### Stage 2 — Analyst
Input: `DATA_DIR`, `PROJECT_DIR/detective.json`
Output: `PROJECT_DIR/code/*.py`, `PROJECT_DIR/analyst.json`
What: Exhaustive quantitative analysis of the data, informed by detective's context. All code saved to `code/` as runnable scripts. Each finding gets an `ana_xx` ID with `calculation` (file + lines + output) and `data_table` (chart-ready data).

### Stage 2.5 — Imagineer [premium]
Input: `PROJECT_DIR/analyst.json` (+ `client_model`s), `PROJECT_DIR/detective.json` (`topic_profile`), `PROJECT_DIR/editor.md` spine (if already present)
Output: `PROJECT_DIR/imagineer.json`
What: Fans out **many** candidate interactive concepts grounded in the data + narrative — one `img_xx` per concept, each binding a finding (`ana_xx`), an archetype, a reader-action, a `purpose` (INFORM/IMMERSE), and a feasibility/sketch — for the Editor to curate into the hero + supporting set. A deliberate fan-out, not a final selection. `img_` ids are **internal** and never reach the HTML. Gates its breadth off `topic_profile.is_computational`/`is_visual` (fans out little for abstract/statistical data).

Call: `Skill imagineer PROJECT_DIR`

> **Post-Analyst re-confirm `is_computational` (cheap, additive — after the Analyst team, before the Editor).** The `is_computational` flag was first set by the Detective at Stage 1 from the headline's nature, before any numbers existed; the Analyst has now actually computed them, so re-check it cheaply: if `analyst.json` emitted any `client_model`, OR any finding whose nature is a **rate / ranking / aggregate / probability / model output** (i.e. a number the reader could in principle reproduce), **upgrade `topic_profile.is_computational` to `true`** in the resolved profile (the `detective.json`/`scout.json` `topic_profile`) so downstream reads see it. This is a one-way upgrade (never downgrade) that recovers the interaction + runnable-verify flagship levers when an early Detective pass under-classified a chart-led computational topic. Do not reorder stages; this is a single boolean re-confirm between the Analyst team and the Editor.

#### Editor team — narrative + titling (lead: Editor; member: Copywriter)

### Stage 3 — Editor
Input: `PROJECT_DIR/detective.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/imagineer.json`
Output: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`
What: Editorial decisions — which findings matter, what the narrative arc is, what the blog argues. Each section gets an `edt_xx` ID with explicit references to `ana_xx` findings and `det_xx` context. Also **curates** the Imagineer's `img_` concepts into `editor.json.interactives` (the `hero` + ranked `supporting[]`), binding each to a section + a distinct finding + a `purpose` (INFORM/IMMERSE) so the Interaction Engineer builds only what earns its place. No visual design.

### Stage 3.5 — Copywriter [premium]
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/detective.json` (`topic_profile`), `PROJECT_DIR/designer.json` (if already present)
Output: `PROJECT_DIR/copywriter.json`
What: **Names the piece — strings only.** Re-writes the masthead (`headline` + `standfirst` + `kicker`), every section `title`, and every figure/photo/table `caption` to a research-driven titling standard that kills the AI-tell patterns a competent default falls into — above all the **AT1 two-beat** ("Flat statement. Flat counter-statement.", e.g. "Argentina is the favourite. No bookmaker agrees."). Writes `copywriter.json` (masthead + `items{edt_xx:{title}, des_xx:{caption}}`), each string `backs`-ed to a real `ana_*`. **Naming, not editing**: it touches no finding, no number, no `data-*` id, no layout, no body prose, and **reuses the existing `edt_`/`des_` ids (adds none)** — so the Verify layer + provenance graph are untouched; the Programmer renders the masthead + figcaptions from `copywriter.json` verbatim. Runs after the Editor, before the Designer (Editor team).

Call: `Skill copywriter PROJECT_DIR`

#### Designer team — visual brief + interaction + cinematic (lead: Designer; members: Interaction, Cinematographer)

### Stage 4 — Designer
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/analyst.json`
Output: `PROJECT_DIR/designer.json`, `PROJECT_DIR/assets/*`
What: Data-driven creative visual decisions — how to present each point using charts, images, video, audio, maps, interactives, stat callouts, instances, or text-only treatment when appropriate. The media mix should emerge from the dataset's properties, not from a fixed checklist. The page should be **multimedia-rich by default**: borrow the visual language from the shared [`frontend-design-pro`](../frontend-design-pro/) skill and use all five channels (chart, image, video, audio, interactive/map) unless a channel's documented fallback would be fabricated or purely decorative. Each visual gets a `des_xx` ID with `data_source` pointing to `ana_xx` data_tables when data-driven. Generates selected assets. No HTML.

### Stage 4.5 — Interaction Engineer [premium]
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json` (+ `interactives`), `PROJECT_DIR/analyst.json` (+ `client_model`), `PROJECT_DIR/imagineer.json`, `PROJECT_DIR/designer.json`
Output: `PROJECT_DIR/interaction.json`
What: Builds the **curated SET** the Editor approved (`editor.json.interactives`) — the ONE narrative-bound hero `centerpiece` PLUS the ranked `supporting[]` playgrounds, each an explorable that makes the reader PRODUCE a distinct finding to the three-layer-number standard — plus scrollytelling/transition craft, consuming the Analyst's `client_model`. Builds **only** what the Editor curated (nothing more); every element earns its place by binding a distinct finding the reader produces/feels. May reach back into the Editor's spine to confirm the hero. See `interaction/SKILL.md` + the shared `../frontend-design-pro/references/interaction_playbook.json`.

Call: `Skill interaction PROJECT_DIR`

### Stage 4.6 — Hero [premium]
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json` (+ `interactives.hero`), `PROJECT_DIR/scout.json`, `PROJECT_DIR/designer.json`, `PROJECT_DIR/interaction.json`
Output: `PROJECT_DIR/hero.json`, `PROJECT_DIR/assets/teaser.*` (`.webm` + `_web.mp4` + `.jpg` poster)
What: Crafts the **cover** — the single most important detail. The animated hero is the **default**: an auto-selected source ladder (first rung that resolves) keeps the cover moving — Scout real still → `image2video` cinemagraph; recognizable real public figure → `image2video --model kwaivgi/kling-v3.0-std` (Veo/Wan refuse real faces) → ffmpeg Ken-Burns; license-clean stock clip; abstract/atmospheric `text2image` still then animate; and only as the LAST rung, a recorded static poster (`kind:"image"` with a `media_blocker`). Emits `hero.json` (`id:"des_hero_video"`, `kind`, `assets{video_webm,video_mp4,poster}`, `reduced_motion_fallback`, `verify.class_marker:"teaser"`). Reuses the `des_` prefix (no 6th provenance prefix). Runs `optimize_assets.py` (VP9 webm + H.264 mp4 + poster, < 3 MB web budget).

Call: `Skill hero PROJECT_DIR`

### Stage 4.7 — Cinematographer (mandatory) [premium]
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/designer.json`, `PROJECT_DIR/interaction.json`, `PROJECT_DIR/scout.json`
Output: `PROJECT_DIR/cinematographer.json`
What: **Mandatory — every blog ships a cinematic scroll background; there is no `off`/opt-out.** Designs a full-bleed, scroll-driven background + global motion choreography, staging the Designer's visuals and the Interaction centerpiece as scenes. The MODE adapts to the topic, it never turns off: **`photographic`** (primary — a scroll built from the Scout's verified real imagery, each scene a `cin_xx` whose background `media_ref` points at a verified `sct_`/`des_` asset so it stays licensed + identified), **`generative`** (AI-sourced atmosphere when real cover-able imagery is thin), or **`data_driven`** (a chart-spine background — `kind:color|gradient`/chart scenes carrying no `media_ref` — for abstract/statistical data, so a dry topic still gets a tasteful immersive layer instead of an inert column). Mandatory means always-present-AND-tasteful, never force-junk: a tonally-wrong or decorative immersion still caps visual_design at 3 (it does not satisfy the stage). See `cinematographer/SKILL.md`.

Call: `Skill cinematographer PROJECT_DIR`

#### Programmer team — HTML build (single-lead: Programmer)

### Stage 5 — Programmer
Input: `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/designer.json`, `PROJECT_DIR/interaction.json`, `PROJECT_DIR/cinematographer.json`
Output: `PROJECT_DIR/index.html`
What: Implements the final blog in HTML. Applies the theme/accent recorded in `designer.json` `page_rhythm` and borrows component + token recipes from the [`frontend-design-pro`](../frontend-design-pro/) skill. Resolves chart data from analyst.json data_tables (NO raw data access). Tags every element with `data-edt`, `data-ana`, `data-det`, `data-des` (and `data-sct` on scouted media, `data-cin` on cinematic backgrounds) attributes for traceability. The cinematic background is MANDATORY, so `cinematographer.json` `meta.mode` is always one of `photographic` / `generative` / `data_driven` (`cinematic` is the backward-compat alias for `photographic`); the Programmer builds the scroll-driven background layer per its scenes for every blog (see `cinematographer/references/cinematic_recipes.json`). The plain editorial column is built only in the impossible no-scenes pipeline-error case.

#### Auditor team — build/render correctness + content quality (lead: Auditor; members: Critic + Playtester step)

> The two cross-team gates (the **media-purpose gate** and the **contract gate `validate.py`**) and the **Inspector team's `verify.py` (Stage 6.4)** fall between the Auditor (Stage 6) and the Critic (Stage 6.5); they are run by this top orchestrator at the canonical points below, not delegated into the Auditor team.

### Stage 6 — Auditor
Input: `PROJECT_DIR/index.html`
Output: `PROJECT_DIR/index.html` (modified), `PROJECT_DIR/auditor.json`, `PROJECT_DIR/audit/` (render_report.json + screenshots)
What: **Actually renders the page in a real headless browser** (`auditor/scripts/render_capture.js` drives the installed Chrome/Edge via puppeteer-core — no Chromium download; falls back to static analysis if a browser isn't available) to catch render-time defects that source inspection is blind to — blank/0-width charts, broken/404 media, horizontal overflow, dead interactions — measuring every element's true pixel box and capturing console errors. It also runs a **mobile-viewport pass (~390×844)** that re-checks horizontal overflow + screenshots the phone layout (virality is mobile, so mobile overflow is a real defect), and an **asset-weight / performance check** over `assets/` against shared budgets (audio > 3 MB, single image > 600 KB, video > 3 MB, total payload > ~8 MB). Then **2–3 cross-validating vision agents** review the screenshots against `designer.json`/`editor.md` intent (charts / layout / media+interaction lenses; ≥2-agree = high confidence). Fixes layout (incl. mobile overflow) in place; **views each image** to catch a wrong/garbled subject or an AI render faking a specific real object (e.g. a fake trophy); records correctness + oversized-asset problems in `auditor.json.send_backs` for the owning role; re-renders to confirm fixes. Runs automatically after Programmer.

Call: `Skill auditor PROJECT_DIR`

After the Auditor, if `auditor.json.send_backs` is non-empty, route each issue to its `send_back_to` role (Designer re-fetches a real image, regenerates, or **re-encodes/compresses an oversized generated asset**; Scout swaps an **oversized sourced asset** for a lighter still-licensed one; Programmer fixes wiring/markup or a mobile-overflow constraint), then re-run the Programmer (if the HTML changed) and the Auditor — bounded to ≤2 rounds — before the contract gate. Set each routed send-back's `resolution` (`fixed` after a clearing re-run, or `blocker_recorded`+`blocker_reason`); the contract gate asserts none is left `open`.

**Playtester step (inside the Auditor team, Stage 6 — after the render/probe, before the contract gate).** The Auditor team then drives **every built playground** in a real browser (the `auditor/scripts/playtest_drive.js` script, built and documented by the Auditor team) — for each `int_` id in `interaction.json` (`centerpiece` + `supporting[]`) it sets the declared controls, reads the live readout, and checks the playground fires, its in-browser recompute agrees with the published `ana_*` figure, it degrades without JS, and it is keyboard-reachable — writing `PROJECT_DIR/audit/playtest_report.json`. Correctness defects join `auditor.json.send_backs` and route through the Auditor's ≤2-round loop (purpose/abundance defects route to the Critic loop). **Every** hard playtest send-back must end `fixed` (a re-run shows the check PASS) or `blocker_recorded`+reason; an `open`/unmatched/omitted hard playtest fail hard-fails the contract gate (Section 15) — a false-positive call is RECORDED as `blocker_recorded`, never silently dropped or downgraded. (Only referenced here; the step's script + checks are owned by the Auditor team.)

#### Inspector team — traceability verification + viewer (single-lead: Inspector)

> The Inspector team's two scripts run inline at the canonical points, invoked by this top orchestrator: `verify.py` here at Stage 6.4 (after the contract gate, before the Critic) and `generate_viewer.py` at Stage 7 (after the Critic loop settles).

### Stage 6.4 — Inspector: verify.py (sentence → evidence map)
Input: `PROJECT_DIR/index.html`, all JSON files
Output: `PROJECT_DIR/verifier.json`
What: Runs the Inspector's first step — `verify.py` — to produce the sentence→evidence map. Run it **after the contract gate passes (see Handoff rules) and before the Critic**, so `verifier.json` exists when the Critic reads it (the Critic scores `data_method_transparency` against this traceability index). This is only the sentence→evidence pass; the in-page panel injection (`generate_viewer.py`) stays at Stage 7.
```bash
python3 SKILL_DIR/inspector/scripts/verify.py PROJECT_DIR
```

> Back to the **Auditor team**: with `verifier.json` in hand, its content-quality member runs next.

### Stage 6.5 — Critic (quality review + bounded revision loop) [premium]
Input: `PROJECT_DIR/index.html` + all JSON
Output: `PROJECT_DIR/critic.json`
What: Scores the finished article against the 5 quality-rubric dimensions and sends targeted, surgical fixes back to the responsible roles. This is the pipeline's only **content-quality** gate (the Auditor handles build/render correctness, the Inspector only traceability).

Call: `Skill critic PROJECT_DIR`

Then run the **bounded revision loop (max 2 rounds)**:
1. Read `critic.json`. If `overall.pass` is true, proceed to the contract gate + Stage 7. **`overall.pass == true` is the signature-move bar (R9): it means every rubric dimension scored >=4 AND at least one dimension reached >=5 (a signature move). A run that is merely "all >=4 but nothing reached 5" is NOT a pass — `overall.pass` will be false and `overall.tier` will be `"competent"`, not `"flagship"`.**
2. Otherwise, for each failing dimension apply its `suggested_fix` via the `send_back_to` role as a **surgical** edit of that role's artifact only — Editor → `editor.md`/`editor.json`; Designer → `designer.json` (+regenerate only the affected asset); Analyst → the specific finding; Detective → the missing context. Do NOT regenerate the whole pipeline.
3. Re-run the Programmer to re-render only the affected sections into `index.html`, then re-run the Auditor (`Skill auditor PROJECT_DIR`), the contract gate (`validate.py`), and `verify.py` (so `verifier.json` reflects the revised page). The contract gate now also asserts the verify layer (`validate.py` Section 7): if it reports any `verify_*` error, route it to the **Programmer (Step 2.5)** per the contract-gate routing table below and re-run before continuing. Set each routed send-back's `resolution` (`fixed` after a clearing re-run, or `blocker_recorded`+`blocker_reason`); the contract gate asserts none is left `open` (Section 15).
4. Re-run `Skill critic PROJECT_DIR` (increment `overall.round`).
5. Stop when `overall.pass` is true OR after 2 rounds (the loop **never** exceeds 2 rounds and **never** downgrades-then-passes / rounds-up-to-pass); then proceed to build regardless, leaving the final `critic.json` (with any residual issues) in place. A run is `flagship` **only** when `overall.pass == true` (i.e. `overall.tier == "flagship"`). If the loop exits after 2 rounds with `overall.pass == false`, read `critic.json overall.tier` and report **one of two honest terminal sub-states** — in neither case is the build hard-blocked (Stage 7 still runs and the deliverables are still produced), but in neither case may the run be reported as a silent "done" or called flagship:
   - **`overall.tier == "sub_competent"`** (some dimension scored < 4): status **`INCOMPLETE — quality gate not cleared`** (parallel to a contract-gate / verify-layer failure). Surface it explicitly in the final deliverables (see Handoff rules → Final deliverables) and in the run's closing summary, listing each failing dimension and its `send_back_to` role + `suggested_fix`.
   - **`overall.tier == "competent"`** (every dimension scored >= 4 but none reached >= 5 — the signature-move bar R9 was not met within the bounded rounds): status **`COMPETENT — NOT flagship-verified (no signature move reached 5 in N rounds)`** (N = `overall.round`). This is a **sound competent blog**, not a failure: the deliverables still ship and Stage 7 still runs with **NO hard block**. But it must NOT be called flagship, and it must be **surfaced in the closing summary**, naming the highest-leverage lift the Critic recorded (the dimension + `suggested_fix` most likely to reach a signature 5).
   A passing `critic.json` (`overall.pass == true`, `tier == "flagship"`) is required before a run may be called flagship-quality.

> **The Critic runs BEFORE Stage 7 fills the panel islands.** The Critic's PIT-29 verify-layer check (`frontend-design-pro/references/pitfalls.json`) therefore confirms only that the `verify/` FILES exist and the panel SHELL is present (the `#verifyToggle` toggle + the two island `<script>` tags, which are still EMPTY at this point) — it must NOT require the islands to be filled. The deterministic island-filling is checked at Stage 7 by `generate_viewer.py` itself.

### Stage 7 — Inspector: generate_viewer.py (panel injection + redirect)
Input: `PROJECT_DIR/index.html`, the Programmer-authored `PROJECT_DIR/verify/` payloads (`verify_map.json`, `run_cells.json`, the reproducible notebook), `PROJECT_DIR/verifier.json` (from Stage 6.4)
Output: `PROJECT_DIR/index.html` (with the in-page Inspector panel filled), `PROJECT_DIR/verify/cell_registry.json` (derived)
What: Stands up the **in-page Inspector panel** — a click-any-claim drawer embedded in `index.html` whose evidence is byte-identical to the `verify/` artifacts, backed by a reproducible notebook that re-executes the headline numbers from raw data (the notebook is the paper's from-raw-data coding verifier; the panel makes its reproductions one-click in the page). **This whole layer is MANDATORY on every blog.** `verifier.json` was already produced at Stage 6.4; this stage **first runs `inspector/scripts/relocate_unreferenced.py`** (relocating any unreferenced heavy master from `assets/` to a non-shipping `provenance/`, writing the `provenance/_relocated.json` sentinel), then runs the panel + redirect emitter:
```bash
python3 SKILL_DIR/inspector/scripts/generate_viewer.py PROJECT_DIR
```
It fills the panel's two inline JSON islands (`verifyMap`/`runCells`, byte-identical to `verify/verify_map.json` + `verify/run_cells.json` — both **authored by the Programmer**, not by this script), derives `verify/cell_registry.json`, wires the reproducible notebook (`NB_PATH` — the Download-notebook target the reader runs locally; no Colab). The Programmer copies the panel UI verbatim (see the Programmer's `inspector_panel` family) and authors the `verify/` payloads; the runnable `computation` snippets re-execute in-browser via lazy Pyodide. See `inspector/SKILL.md` for details.

**Stage 7 is a REQUIRED terminal step — it MUST exit 0.** It is not optional and the run is not finished until it has run successfully:
- If `generate_viewer.py` **exits nonzero**, read its **stderr**: a complaint about the authored `verify/` payloads or the panel shell (missing/empty islands, a `data-*` id with no `verify_map` entry, a schema-invalid `verify_map.json`/`run_cells.json`) routes to the **Programmer (Step 2.5)** to fix the authored layer; a script-internal failure routes to the **Inspector**. Then **re-run** `generate_viewer.py`.
- Loop fix → re-run until it **exits 0**. **Do NOT present the run as finished while Stage 7 has a nonzero exit** (or while the contract gate's `verify_*` Section-7 errors are unresolved).

> Stage 7 is the **Inspector team's** second script, invoked by the orchestrator once the Critic's bounded revision loop has settled. It closes the linear sequence — and the run is incomplete until it exits 0.

## Traceability: ID flow through the pipeline

```
det_01 ──┐
det_02 ──┤
sct_01 ──┤  (scouted media: verified photo / video / music / live-status, each with license + identity)
         ├──▶ ana_01 (based_on: [det_02]) ──┐
         │    ana_02 (based_on: [])          ├──▶ edt_01 (findings: [ana_01, ana_02], context: [det_01, sct_01]) ──▶ des_01 (section: edt_01, data_source: ana_01, media: sct_01)
         │    ana_03 (based_on: [det_01])    │    edt_02 (findings: [ana_03], context: [det_02])                 ──▶ des_02 (section: edt_02, data_source: ana_03)
         └────────────────────────────────────┘
```

All role outputs key their `items` as a dict `{id: {...}}` (not arrays); detective `sources` are `{url, title, facts}` dicts — `validate.py`/`verify.py` enforce this.

Every value in the final HTML can be traced: `HTML data-des="des_01"` → `designer.json des_01.data_source="ana_01"` → `analyst.json ana_01.calculation.code` → verifiable. Likewise every external media element: `HTML data-sct="sct_01"` → `scout.json sct_01.license` + `sct_01.identity` → a checked license + verified subject. And every cinematic background scene: `HTML data-cin="cin_01"` → `cinematographer.json cin_01.background.media_ref` → the verified `sct_`/`des_` asset behind it. The **Hero cover** is a `des_` item (`hero.json id="des_hero_video"`, reusing `data-des` — no 6th prefix): it surfaces as a SINGLE provenance hit on the `.teaser` overlay (`data-des="des_hero_video"`), and the Cinematographer consumes it as `cin_00` (its continuous backdrop), so the cover routes through the existing `des_`/`cin_` graph with no new tuple. Each interactive (hero + supporting) traces the same way: `HTML data-int="int_NN"` → `interaction.json` `centerpiece` (the hero, a single object) / `supporting[]` (the curated set) → the Analyst `client_model` / `ana_*` it recomputes. The Imagineer's `img_` ids are **internal** (concept ideation only) and **never reach the HTML** — they are added to NO `data-*` tuple/regex; the Editor maps the chosen `img_` concepts onto the `int_` ids the Interaction Engineer builds. `data-play-out="int_NN"` is a **non-provenance** hook (a Playtester readout selector, like `data-backs`) — it is NOT a provenance prefix and is invisible to `validate.py`/`verify.py`.

**Provenance prefix convention (authoritative).** Each producing role tags its atomic ids with a fixed prefix, surfaced in the HTML as `data-<prefix>="<prefix>_NN"`: `det_` Detective · `sct_` Scout · `ana_` Analyst · `edt_` Editor · `des_` Designer · `int_` Interaction (every playground — hero `centerpiece` + each `supporting[]` — via `data-int`) · `cin_` Cinematographer. The Imagineer's `img_` is **internal-only** (never surfaced in HTML, in no tuple/regex), and `data-play-out` is a **non-provenance** hook (not a prefix). This is the single source of truth for the prefix↔role mapping used throughout the pipeline (`validate.py`/`verify.py`, the verify-layer schemas, and each role's `SKILL.md`).

## Handoff rules

- Each artifact must be complete before the next stage starts.
- If an artifact is missing required sections, fix it before proceeding.
- **Media-purpose gate — the Designer team's exit gate (after Designer/Interaction, before Programmer):** every item in `designer.json` must declare a `purpose` — INFORM (carries data/information the prose can't) or IMMERSE (sets mood/aids reading); an item serving neither is decoration and must be cut. Aim for breadth across the five channels (chart, image, video, audio, interactive_or_map), but a channel is used only when an asset in it earns a purpose — for any channel marked `used:false`, confirm a data-grounded reason is recorded in `meta.media_decisions`. Send back to the Designer (before the Programmer) any unpurposed/decorative asset, or a channel skipped for convenience rather than genuine lack of purpose.
  - **Playgrounds too — the primary "earn its place" lever.** This same gate ALSO walks every interactive in `interaction.json` — the `centerpiece` (hero) **and** each `supporting[]` entry. Any playground that declares no `purpose` (INFORM/IMMERSE) or binds a fake/non-existent `finding` (`ana_*`) is decoration and is **CUT here — before the Programmer builds it**, so an unearned widget is never coded in the first place. This pre-build cut is the single most important guard against abundance degrading quality: every supporting playground must independently justify its existence, or it does not survive to Stage 5. Send the cut back to the Interaction Engineer (drop or re-bind the playground) before the Programmer runs.
- **Richness gate — the Designer team's exit gate (the INVERSE of the media-purpose gate; BLOCKS on rich topics):** the media-purpose gate above cuts purposeless ADDITIONS (too much); this gate forbids IMPOVERISHMENT on RICH topics (too little). Trigger: `topic_profile.is_visual == true` **OR** `is_computational == true` (UNION — a genuinely abstract/small/`privacy_sensitive` dataset trips none, each sub-check being capability-gated). On a rich topic, confirm the page is not under-delivered: a **dynamic hero** (`hero.json kind=="video"`, not a bare static still) on a visual topic; a **license-clean topic-asset floor** (≥3 distinct verified images, ≥5 cover-able for cinematic) on a visual non-privacy topic; **substantive verify** (no hollow `cell_registry` cells) on a computational topic. On a topic the classifier marks visual/computational these floors **BLOCK** (`validate.py` Section 12 emits the matching `richness_*` ERRORs — `richness_static_hero`, `richness_asset_floor`, `richness_hollow_verify_cells` — and the contract gate routes the nonzero `validate.py` back to the owning role: hero/scout/programmer), **unless a legitimate blocker is recorded** — a `privacy_sensitive` topic, or a genuinely-failed source ladder / an honest fallback. Route each blocking error back to the named role to enrich, then re-run BEFORE the Programmer re-runs. **Anti-slop:** each required-rich element still earns its place via the media-purpose gate — the floor forbids impoverishment, it NEVER forces a fabricated/decorative asset (which itself caps `visual_design` at 3). It is **NOT** correct to say this gate "never hard-blocks": on a rich topic with no recorded legitimate blocker, an unmet floor blocks (mirror of, and must not collide with, the abstract-topic `missing_engagement_floor`).
- **Mandatory cinematic + BGM gate — orchestrator-owned:** cinematic and BGM are MANDATORY stages — EVERY blog ships a cinematic scroll background (`cinematographer.json` `meta.mode` is one of `photographic` / `generative` / `data_driven` — never `off`/opt-out) AND opens with a fitting real-sourced BGM. Two floor checks: (a) **cinematic missing** — `meta.mode` is absent / not one of the on-modes (no scroll background produced) → send back **to the Cinematographer** to build the immersive layer (photographic if ≥5 cover-able verified images exist, else generative AI atmosphere, else a data_driven chart-spine); (b) **BGM missing or tonally wrong** — no fitting front-of-blog soundtrack on **any** topic (a missing BGM, or a present-but-tonally-WRONG track — e.g. a celebratory anthem on a sober topic) → send back **to the Scout** to source a fitting, license-clean (or demo-gated) real track. The two floors differ in how they block. **BGM is a HARD ERROR on EVERY blog** — there is **NO** privacy exemption and **NO** `audio.used == false` escape hatch: the Scout's classical-recording floor (rung C) is the GUARANTEED terminal rung of the audio source ladder, so a license-clean BGM always exists (a privacy-sensitive topic gets a quiet classical recording, an abstract topic a restrained pensive/ambient track), and `validate.py` emits the `bgm_missing` ERROR on every topic whenever no BGM presence signal is found — "ship no BGM" is never a valid outcome. The legitimate-blocker escape survives ONLY for the **cinematic** background: `cinematic_missing` ERRORs on a visual/computational topic (else warn), and cinematic may fall back to a thin spine or be reduced under under-supply / on a `privacy_sensitive` topic. The contract gate routes the nonzero `validate.py` back to the owning role — Cinematographer / Scout. Mandatory means always-present-AND-tasteful, never force-junk: never satisfy these by bolting on a tonally-wrong/decorative immersion (that still caps `visual_design` at 3).
- **Cinematic-supply gate — orchestrator-owned (the "go-source-more" undersupply send-back; a non-blocking WARN, NOT a hard publish-block):** distinct from the two BLOCKING floors above — here cinematic is already ON (the mandatory floor is satisfied), so an undersupply of cover-able imagery only WARNs, it does not block. When the topic is visual (`topic_profile.is_visual == true`) AND cinematic is ON but the immersion fell back to a non-photographic mode for **under-supply** of real cover-able imagery (`1 <= verified license-clean cover-able image count < 5`), send the run back — **to the Scout** to source ≥5 (ideally a dozen+) license-clean cover-able backgrounds of the story's subjects, then **to the Designer** to register each as a real `des_`/`sct_` item, BEFORE the Cinematographer re-runs so the immersion can UPGRADE to a `photographic` scroll. The **count is the primary signal**; `meta.mode_reason` is only a secondary confirm that the non-photographic mode was supply-driven (not honest restraint). `validate.py` Section 12 front-runs this as the `richness_cinematic_undersupplied` **warning** (a WARN, not an error). Surface an unmet supply gate in the closing summary as **"richness floor not met"**. This send-back never hard-blocks the build (the run still finishes); the ≥5 threshold itself is unchanged.
- **Registration-first cinematic backgrounds — pre-Programmer assertion (after Cinematographer, before Programmer):** since cinematic is mandatory (`meta.mode` ∈ `photographic`/`generative`/`data_driven`/`cinematic`), assert that **every** `cin_*` scene's `background.media_ref` (for `kind` image/video) **already resolves to a registered `sct_` (scout) or `des_` (designer) item** — the cinematic background must be a registered media item BEFORE the Cinematographer references it, not just an entry in a bypass manifest. (A `data_driven` chart-spine scene with `kind` color/gradient carries no `media_ref` and is exempt from this resolution check — it is still a real built scroll layer.) Any image/video `cin_*` whose `media_ref` is missing or dangles (not a current `sct_`/`des_` id) is sent back: to the **Designer/Scout** to register the background as a real `des_`/`sct_` item, then to the **Cinematographer** to point `media_ref` at it. Resolve all `cin_*` references before invoking the Programmer (this front-runs the same check `validate.py` Section 6 enforces, so the dangling reference never reaches the build).
- **Contract gate (hard) — the top orchestrator's cross-team gate, after Programmer/Auditor, before Inspector:** run `python3 SKILL_DIR/inspector/scripts/validate.py PROJECT_DIR`. If it exits nonzero, read `PROJECT_DIR/validation.json` and send each violation back to its owning role to fix (`ana_*` → Analyst, `edt_*` → Editor, `des_*`/instance → Designer, `sct_*`/`media_*` (license/identity) → Scout, `int_`/`data-int` → Interaction (centerpiece spec) or Programmer (its wiring), `cin_*` → Cinematographer, HTML `data-*` → Programmer), then re-run until it reports 0 errors. Do not start the Inspector until `validate.py` passes. (Unlike the media-richness gate above, this is a deterministic hard pass/fail.) The contract gate now ALSO asserts (Section 15) that every `auditor.json`/playtest send-back is resolved — each `auditor.json.send_backs[]` entry must end `fixed` or `blocker_recorded`+`blocker_reason`, and every hard `audit/playtest_report.json` fail must match an auditor resolution — so a left-`open` send-back or an unmatched hard playtest fail is a contract-gate ERROR; and (Section 16) that `assets/` ships no unreferenced heavy master.
  - **Newer contract-gate kinds — routing (validate.py kind → role):**
    - `topic_profile_unresolved` → **Detective** (resolve the `topic_profile` with explicit `is_visual`/`is_computational` booleans), then **Scout** (which writes one into `scout.json` if the Detective's is still absent).
    - `verify_map_kind_keys_missing` / `verify_map_unknown_kind` / `verify_map_entry_malformed` → **Programmer (Step 2.5)** (fix the authored `verify/verify_map.json`).
    - `cinematic_data_driven_not_built` → **Cinematographer** when the `data_driven` mode emitted no real scene; **Programmer** when the scenes exist but the `data-cin` token was never mounted.
    - `des_data_source_scout_dangling` → **Designer** (point `data_source` at a real `scout.<sct_id>` / `scout.live_status`) with the **Scout** (register the `sct_` item or supply the `live_status` entry).
    - `missing_engagement_floor` → **Imagineer** (propose the engagement-floor concept) / **Interaction** (build it) — or record the honest `engagement_blocker`. **It now BLOCKS on a resolved descriptive topic** (`is_visual:false AND is_computational:false`) **unless an honest `engagement_blocker` is recorded** (`privacy_sensitive` topics are auto-exempt) — it is not advisory/soft.
    - `send_back_open` / `send_back_blocker_no_reason` / `send_back_fixed_but_still_failing` (Section 15) → the entry's OWN `send_back_to` role (the Auditor sets it) — resolve it (`fixed` after a clearing re-run, or `blocker_recorded`+`blocker_reason`); a left-`open`, a `blocker_recorded` with no reason, or a "fixed" the re-run still fails is the contract-gate ERROR.
    - `playtest_hard_unresolved` (Section 15) → **Programmer** (or the hard-flagged playground's owner) — a hard `audit/playtest_report.json` fail with no matching `auditor.json` resolution; fix it (then mark the matching send-back `fixed`) or record `blocker_recorded`+reason.
    - `asset_unreferenced_heavy` (Section 16) → **Inspector** (re-run the Stage-7 `relocate_unreferenced.py` so the heavy master moves to `provenance/`) / **Programmer** (if the asset SHOULD be referenced, wire it into `index.html`).
  - **Verify-layer errors (Section 7) all route to the Programmer (Step 2.5).** The contract gate also asserts the verify layer exists and its panel shell is in place; every one of these `validate.py` Section-7 kinds → **Programmer (Step 2.5)** (author/repair the verify layer per `programmer/SKILL.md`): `verify_dir_missing`, `verify_map_missing`, `verify_map_empty`, `verify_map_missing_entry`, `run_cells_missing`, `run_cells_no_runnable`, `notebook_missing`, `panel_shell_missing`. After the Programmer fixes the layer, re-run `validate.py` (and the Programmer if `index.html` changed) until 0 errors. (Section 7 asserts only that the `verify/` files exist + the panel shell is pasted; it does **not** assert the islands are filled — that is Stage 7's `generate_viewer.py` job.)
- **Cross-team checkpoints are orchestrator-owned.** Both gates above, plus the **Critic's bounded revision loop (≤2 rounds, Stage 6.5)** — which re-runs the Programmer and Auditor teams between rounds — are run by this top orchestrator, never delegated into a team. The **Inspector team** owns its two scripts (`verify.py` at Stage 6.4, `generate_viewer.py` at Stage 7); the orchestrator invokes them inline at those canonical points. This keeps each single-lead team self-contained and the cross-team sequence in one hand.
- All generated assets go into `PROJECT_DIR/assets/` only. Superseded/unreferenced masters are relocated to `provenance/` at finalize (kept for traceability, never shipped); `assets/` ships only what the page loads.
- Final deliverables: `PROJECT_DIR/index.html` (with the in-page Inspector panel), `PROJECT_DIR/detective.json`, `PROJECT_DIR/scout.json`, `PROJECT_DIR/analyst.json`, `PROJECT_DIR/code/*.py`, `PROJECT_DIR/imagineer.json`, `PROJECT_DIR/editor.md`, `PROJECT_DIR/editor.json`, `PROJECT_DIR/copywriter.json` (the re-titled masthead + section titles + figure/photo/table captions; strings only — names, never edits), `PROJECT_DIR/designer.json`, `PROJECT_DIR/interaction.json` (now the hero `centerpiece` + the curated `supporting[]` set), `PROJECT_DIR/hero.json` (the animated cover; `kind:"image"` only when every animation rung degraded, with a recorded `media_blocker`), `PROJECT_DIR/cinematographer.json` (mandatory — `meta.mode` is one of `photographic`/`generative`/`data_driven`; never `off`), `PROJECT_DIR/auditor.json`, `PROJECT_DIR/audit/playtest_report.json` (the Playtester's real-browser drive of every playground), `PROJECT_DIR/critic.json`, `PROJECT_DIR/validation.json`, `PROJECT_DIR/verifier.json`, the `PROJECT_DIR/verify/` artifacts (`verify_map.json`, `run_cells.json`, the reproducible notebook, `cell_registry.json`). The Inspector panel + `verify/` artifacts are MANDATORY on every blog — a run that reaches "done" with the contract gate's `verify_*` (Section 7) errors unresolved, or with `generate_viewer.py` (Stage 7) at a nonzero exit, is **INCOMPLETE** and must not be presented as finished. **Likewise, a run whose `critic.json` still has `overall.pass == false` after the bounded 2-round loop must carry one of two explicit terminal statuses (read from `critic.json overall.tier`) in its closing summary:** `tier == "sub_competent"` → **`INCOMPLETE — quality gate not cleared`** (naming the still-failing dimension[s]); `tier == "competent"` → **`COMPETENT — NOT flagship-verified`** (every dimension >= 4 but no signature move reached 5 in the bounded rounds, naming the highest-leverage lift the Critic recorded). In **both** cases the deliverables are produced and Stage 7 still runs (the quality gate does not hard-block the build), but the run must NOT be reported as a silent "done" or called flagship-quality. Only a run with all hard gates clear — including `validate.py` Section 15 reporting no `send_back_open` / `playtest_hard_unresolved` — AND `critic.json overall.pass == true` (`tier == "flagship"`) is a finished flagship.
