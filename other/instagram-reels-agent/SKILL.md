---
name: instagram-reels-agent
description: "Instagram Reels idea-and-script factory inside a multi-channel content factory. UNLIKE the other channels, it does NOT drain one idea per run — it analyses the WHOLE shared ../raw-ideas/ library (immutable) and produces a ranked reel-map.md of reel candidates of three kinds: Direct (1 idea → 1 reel), Combo (several related ideas summarised into 1 reel), and Pattern (a new reel theme derived from patterns ACROSS ideas, not present in any single file). Then it scripts the top unproduced candidate end-to-end: Reel Strategist (picks faceless vs on-camera + format) → N Scriptwriters → Editor → Cover Designer (/image-gen-agent), writing a publish-ready shooting script into ./instagram-reels/. Source ideas NEVER move. Use when user says /instagram-reels-agent, 'suggest reels', 'what reels can I make', 'script a reel about X', 'process my reels', or when invoked via /loop. Always trigger this skill."
trigger: /instagram-reels-agent
extends: x-growth-agent
---

# /instagram-reels-agent

An Instagram Reels factory. It answers two questions every run:

1. **"What reels should I make?"** — by mining the *entire* shared idea library for reel candidates (not just one idea).
2. **"Give me a script to start with."** — by scripting the top candidate into a publish-ready shooting script + cover frame.

This is the Instagram sibling of `x-growth-agent` and `linkedin-growth-agent`. The factory mechanics are shared (immutable `../raw-ideas/`, per-channel `TODO.md` ledger, save-every-handoff, no emojis, strip company/tool names, never invent stats, read-only cross-channel signal). **Where this file is silent, the X skill's structure applies; where it speaks, Instagram wins.**

**Default scriptwriter angles per reel: 3 (Demo/how-to · Hot-take/POV · Story/build-in-public). Override with `/instagram-reels-agent 2` to drop the third angle. Max 3.**

---

## The ONE big difference: this channel mines the whole library, it does not drain a queue

LinkedIn and X each pick the **oldest single unconsumed idea** and turn it into one post. **Instagram does not.** A reel is often *more* than one idea, and the best reels frequently come from patterns that live *between* ideas. So this skill runs a **mapping pass over the full library** and emits three kinds of reel candidates:

| Reel type | Sources | Example |
|-----------|---------|---------|
| **Direct** | exactly 1 raw idea | `001-claude-vs-codex.md` → "I tested Claude vs Codex on the same task" |
| **Combo** | 2-N related raw ideas, summarised into one reel | `build-your-first-agents-team.md` + `run-your-own-agent-agency-with-paperclip.md` → "Build an AI agent team in 60 seconds" |
| **Pattern** | a theme that recurs ACROSS many ideas; not any single file | several tool/agent ideas → "5 signs you're building AI agents the hard way" — a NEW angle the library implies but never states |

Because a reel can draw on many ideas — and one idea can fuel several reels — **ideas are never "used up."** There is no subtractive queue. Instead the ledger tracks **produced reels** (each listing its source ideas), and the map flags **coverage gaps** (ideas with no reel yet) as priorities.

---

## What makes Instagram different from X / LinkedIn (read first)

| Dimension | X / LinkedIn | Instagram Reels (this skill) |
|-----------|--------------|------------------------------|
| **Output unit** | one text post | **a shooting script for a short video** — hook + timed beats + on-screen text + spoken/VO lines + visual cues + caption + cover frame |
| **Consumption** | drain oldest 1 idea | **map the whole library**, then script ONE chosen candidate (Direct/Combo/Pattern) |
| **Selection** | filename order | **reel-worthiness score** (visual potential, hook, demoability, length-fit) — the map ranks; top unproduced wins |
| **Style** | n/a | **per-reel: faceless (text+VO+B-roll) OR on-camera (talking head)** — the Strategist decides |
| **Length** | char limit | **time budget.** 7-15s for max reach; 20-40s talking-head; up to 60-90s for tutorials. Retention is the metric. |
| **Hook** | first ~7 words | **first 1-2 seconds** — on-screen text + spoken line + a visual that stops the thumb. No slow intros, no "hey guys". |
| **Hashtags** | none (X) / 3-5 (LI) | **3-5 relevant** — IG discovery still benefits from targeted tags. Niche > broad. Still no emojis. |
| **Image** | in-stream graphic | **cover frame** — 1080×1920 (9:16) reel cover + a 1080×1350 (4:5) grid-safe variant |
| **Audio** | n/a | every script names an **audio approach**: trending-audio (reach) vs original voiceover (clarity/evergreen) |

Everything else (immutable library, save-every-handoff, no emojis, strip company/tool names, never invent stats) is identical to the other channels.

---

## Project folder layout (canonical)

```
content-factory/
├── raw-ideas/                                  ← SHARED, immutable, read-only from this skill
├── instagram.agent.md                          ← daily /loop prompt (calls this skill)
└── instagram-reels/                            ← Instagram channel folder (this skill writes here)
    ├── README.md
    ├── CLAUDE.md
    ├── PLAYBOOK.md                             ← Reels craft baseline (read every run)
    ├── reel-map.md                            ← living board of reel candidates (refreshed every run)
    ├── TODO.md                                ← In Progress + Produced + Parked
    └── reels/                                  ← one folder per scripted reel
        └── <reel-slug>-<YYYYMMDD>/
            ├── 00-reel-brief.md                   ← chosen candidate + sources + cross-channel signal
            ├── 01-reel-plan.md                    ← Strategist: style + format + beat skeleton + angles
            ├── 02a-script-demo.md
            ├── 02b-script-hottake.md
            ├── 02c-script-story.md                (if N=3)
            ├── 03-editor-verdict.json
            ├── 02-revised-script.md               (if revision round)
            ├── 03-editor-verdict-final.json       (if revision round)
            ├── cover-1.svg                        ← 9:16 reel cover
            ├── cover-2.svg                        ← 4:5 grid-safe cover
            ├── exports/
            │   ├── cover-1.png
            │   └── cover-2.png
            └── reel-script.md                     ← 👈 THE DELIVERABLE (publish-ready shooting script)
```

**`../raw-ideas/` is immutable.** Never move, rename, or delete files in it.

**Bootstrap on first run:** if `./instagram-reels/` is missing its scaffold (`TODO.md`, `reel-map.md`, `reels/`, `PLAYBOOK.md`), create it (templates below) and continue. If `../raw-ideas/` doesn't exist, create it, tell the user where to drop ideas, and exit.

---

## Run modes

**Mode A — Map + script (default; loop or bare `/instagram-reels-agent`).**
Refresh the reel-map over the whole library, then script the top unproduced candidate. Produces the menu AND one dish.

**Mode B — Map only (`/instagram-reels-agent map` or "suggest reels", "what reels can I make").**
Only refresh and print `reel-map.md`. Script nothing. The user picks later.

**Mode C — Script a specific reel (`/instagram-reels-agent <reel id or topic>`).**
Skip selection. If the argument matches a candidate id in `reel-map.md`, script that. If it's free text, treat it as a new ad-hoc reel topic (and, like X Mode B, persist it as a new `../raw-ideas/<NNN>-<slug>.md` so other channels can also use it), then script it.

**N parsing:** a leading small integer (`/instagram-reels-agent 2 ...`) sets N script angles. Otherwise N=3. Max 3.

---

## Step 1 — Refresh the reel map (the Scout / Pattern-Miner)

Runs in **every** mode. One agent reads the **entire** library and produces the ranked board.

1. List `../raw-ideas/` (non-recursive; accept `.md` and `.txt`). Read **every** file (minus frontmatter). Drop any file whose frontmatter declares `channels: [...]` without `"instagram"` (or `"reels"`).
2. Read `./instagram-reels/TODO.md` **Produced** + **Parked** sections, and the existing `reel-map.md` if present, so you don't re-propose what's already shipped or parked.
3. **Read `./instagram-reels/PLAYBOOK.md`** — score every candidate against what Reels reward (hook in 1-2s, retention, visual/demoable, save/share triggers).
4. **Cross-channel signal (READ-ONLY).** Open `../linkedin-posts/TODO.md` and `../x-posts/TODO.md` (+ any `performance.md`) to see which topics already resonated elsewhere. Boost candidates whose topic performed on another channel. **Never write to those folders.** (Sanctioned by project CLAUDE.md rule 3.)
5. Generate candidates of all three types:
   - **Direct** — for each reel-worthy single idea (prioritise coverage gaps: ideas with no produced reel yet).
   - **Combo** — cluster related ideas (same tool family, same theme) into summarising reels. State which files merge and the unifying angle.
   - **Pattern** — step back: what recurring themes, contradictions, or progressions appear ACROSS the library? Coin NEW reel angles the ideas collectively imply but none states alone. This is the highest-leverage output — be genuinely creative, but every pattern must be grounded in ≥2 real source files (cite them). Never invent facts not in the sources.
6. Score each candidate 0-10 on **reel-worthiness** and tag the likely **style** (faceless/on-camera) and **format** (demo/talking-head/text-B-roll/listicle).
7. Write `./instagram-reels/reel-map.md` (template below), ranked within each section. Print `[HANDOFF: REEL MAP]` and the board.

> The reel-map is a **content deliverable** (the suggestions the user asked for), regenerated each run — not a hidden state file. It is the Instagram analogue of the X Fit Gate: reel-worthiness scoring happens here, so there is no separate gate file.

**If Mode B (map only):** stop here after printing the board.

---

## Step 2 — Pick the reel to script

- **Mode A:** pick the **highest reel-worthiness candidate not already in Produced / In Progress**. Ties → prefer Direct that closes a coverage gap, then Combo, then Pattern. State the pick and its score.
- **Mode C:** the user named it — use that candidate (or the ad-hoc topic).
- Derive `<reel-slug>` (kebab, no numeric prefix). Create `./instagram-reels/reels/<reel-slug>-<YYYYMMDD>/`. If that folder exists (same-day re-run), append `-2`, `-3`.
- Move the reel to **In Progress** in `TODO.md`.
- Write `00-reel-brief.md`: chosen candidate, type (Direct/Combo/Pattern), **list of source idea filenames**, the cross-channel signal, and the recommended style/format/hook lean. Print `[HANDOFF: REEL BRIEF]`.

---

## Pipeline overview (production)

```
reel-map refresh (Scout)        → reel-map.md
   ↓ pick top unproduced
Reel Brief                      → 00-reel-brief.md   (sources + cross-channel signal)
   ↓
Reel Strategist (once)         → 01-reel-plan.md     (STYLE: faceless|on-camera · FORMAT · beats · angles)
   ↓
Scriptwriters × N (parallel)   → 02a..02c-script-*.md
   ↓
Editor                         → 03-editor-verdict.json
   ↓ if needs_revision AND round < 2
Scriptwriter (winner)          → 02-revised-script.md
   ↓
Editor (final)                 → 03-editor-verdict-final.json
   ↓
Cover Designer (/image-gen-agent ×2) → cover-1.svg (9:16), cover-2.svg (4:5)
   ↓
[DELIVERABLE]                  → reel-script.md
   ↓
DO NOT touch ../raw-ideas/      (immutable, shared)
TODO.md: In Progress → Produced (list source ideas + folder link); refresh reel-map coverage
```

Max revision rounds: **2**.

---

## Reel Strategist (runs once)

**Job:** turn the chosen candidate into a production plan. **Read `./instagram-reels/PLAYBOOK.md` + `00-reel-brief.md` first.**

Decide and state, at the top of the plan:

1. **STYLE** — `FACELESS` (text-on-screen + voiceover + screen-recording/B-roll) or `ON-CAMERA` (talking head + B-roll overlays). Choose from the content: demos/screens → faceless; opinions/story → on-camera often wins trust. State the one-line rationale.
2. **FORMAT** — one of: `talking-head`, `screen-demo`, `text-B-roll`, `listicle`. 
3. **LENGTH** target in seconds (7-15 reach / 20-40 talking-head / up to 90 tutorial) + why.
4. **AUDIO** approach — trending-audio (reach, faceless/text reels) vs original voiceover (clarity, evergreen). 

Print `[HANDOFF: REEL STRATEGIST]` AND save `01-reel-plan.md`:

```
## Style & Format
Style: <FACELESS | ON-CAMERA> — <why>
Format: <talking-head | screen-demo | text-B-roll | listicle>
Length: <Ns> — <why>
Audio: <trending | original VO> — <why>

## Core Insight
<the one "so what" in a sentence>

## Target Viewer
<who is scrolling — be specific>

## Hook (0-2s)
<the scroll-stopper concept: the on-screen line + the visual that earns the first 2 seconds>

## Beat Skeleton
1. Hook (0-2s) — <beat>
2. <beat> (~Xs)
3. <beat>
... (3-6 beats; each must hold retention into the next)
Payoff/CTA — <the close: follow/save/comment reason>

## Caption direction
<first-line hook for the caption + the CTA>

## Hashtags
<3-5 relevant niche tags, or fewer — never spammy. e.g. #aiengineering #buildinpublic>

## Cover Brief
<2-5 words / one number / one contrast for the cover frame + 1 tagline>

## Sources
<list the raw-idea filenames this reel draws from — Direct: 1, Combo/Pattern: several>

## Angle Assignments
Each scriptwriter writes a FULL shooting script in the chosen STYLE/FORMAT, but on a different angle:
  - **Angle 1 — Demo / how-to (always):** show the thing working / the steps. Save-bait. Lead with the payoff, prove it fast.
  - **Angle 2 — Hot-take / POV (always):** a sharp, defensible opinion the idea supports. Comment + share bait. Real position, never manufactured outrage.
  - **Angle 3 — Story / build-in-public (at N=3):** a concrete first-person moment ("I tried X, here's what happened"). Relatability → comments.
When N=2, use Angles 1 and 2. The Strategist MAY swap an angle if the idea can't support it (state the swap + reason).
```

---

## Scriptwriters (N instances, run in parallel)

Run all N at once. Each gets the plan + its angle + the STYLE/FORMAT/LENGTH decision. **Read `./instagram-reels/PLAYBOOK.md` first.**

**Rules for every Reel Scriptwriter:**
- Write a complete **shooting script** in the Strategist's STYLE and FORMAT, hitting the LENGTH target.
- **Hook owns the first 1-2 seconds.** On-screen text + the spoken/VO line + a concrete visual. No "hey guys", no logo intro, no slow build.
- Structure as **timed beats**. For each beat give: `[t]` timestamp, **On-screen** text overlay, **Spoken/VO** line (or `[to camera]` line if on-camera), **Visual** (what's on screen / B-roll / screen-recording).
- Every beat must **earn the next second** — open loops, fast cuts, payoff withheld just enough.
- Land a clear **payoff** and a **CTA** that gives a reason to follow/save/comment. CTA must be **public-shareable** (no "DM me to try the internal tool").
- Write the **caption**: a hook first line (visible before "more"), short body, CTA, then **3-5 relevant hashtags**.
- Name the **audio** (trending vs original VO) consistent with the plan.
- Never invent stats, quotes, or claims not in the source idea(s). **Strip company/tool names — keep the lesson.** No emojis unless Altaf asks.

Each prints its block AND writes its file (`02a-script-demo.md`, `02b-script-hottake.md`, `02c-script-story.md`; rename suffix if the Strategist swapped an angle):

```
[HANDOFF: SCRIPTWRITER — <Angle Name>]

Style: <FACELESS | ON-CAMERA>   Format: <...>   Target: <Ns>

### Shooting script
[0-2s] HOOK
  On-screen: <text overlay>
  Spoken/VO: <line>
  Visual: <what's shown>

[2-Xs] <beat name>
  On-screen: <...>
  Spoken/VO: <...>
  Visual: <...>

... (continue through payoff + CTA)

### Caption
<hook first line>
<body>
<CTA>
<#tag #tag #tag>

### Audio
<trending: describe the vibe to search for | original VO>

### On-screen text (consolidated overlay list)
- <overlay 1>
- <overlay 2>

---
Angle: <name>   Est. length: <Ns>   Beats: <count>
```

**On revision round** (winner only): `[HANDOFF: SCRIPTWRITER — REVISED <Angle>]`, save `02-revised-script.md` with a `Changes made:` list.

---

## Editor

**Read `./instagram-reels/PLAYBOOK.md` and score against it.** Round 1: score all variants, pick winner, decide revision. Round 2: final verdict.

Print `[HANDOFF: EDITOR]` — valid JSON only → `03-editor-verdict.json` (round 1) / `03-editor-verdict-final.json` (round 2):

```json
{
  "round": 1,
  "style": "FACELESS | ON-CAMERA",
  "format": "talking-head | screen-demo | text-B-roll | listicle",
  "variants_reviewed": ["A", "B", "C"],
  "status": "approved | needs_revision",
  "winner": "A | B | C",
  "why_winner": "<1-2 sentences>",
  "scores": {
    "A": { "hook_1_2s": 9, "retention_arc": 8, "payoff": 8, "clarity": 9, "cta_strength": 7, "avg": 8.2 },
    "B": { "hook_1_2s": 8, "retention_arc": 7, "payoff": 9, "clarity": 8, "cta_strength": 8, "avg": 8.0 }
  },
  "length_check": { "A": "pass (~24s)", "B": "pass", "C": "long (~75s) — trim" },
  "runner_up_notes": { "B": "<what the winner should borrow>" },
  "issues": [
    {
      "type": "weak_hook | slow_open | no_payoff | over_length | off_plan | missing_cta | jargon | inauthentic | non_shareable_cta | wrong_style",
      "severity": "high | medium | low",
      "description": "<exact problem in the WINNER>",
      "action": "<exact fix>"
    }
  ]
}
```

**Hard fails (always `needs_revision` if present in the winner):** a hook that doesn't land in the first 1-2s (`weak_hook`/`slow_open`), no clear payoff (`no_payoff`), or a non-shareable CTA (`non_shareable_cta`).

**Decision logic:** `approved` → Cover Designer · `needs_revision` AND round < 2 → revise winner · round = 2 → output best available, list unresolved issues.

---

## Cover Designer (runs once, after the script is locked)

**Job:** generate TWO cover frames by invoking `/image-gen-agent` once with `Variations: 2`, `Channel: instagram`. Pass dimensions explicitly (the image agent may not know IG formats):

```
[IMAGE BRIEF]
Channel: instagram
Variations: 2
Dimensions: explicit — cover-1 = 1080×1920 (9:16 reel cover), cover-2 = 1080×1350 (4:5 grid-safe). Different style each.
Style hint: <reason from content>
Final script: <paste the winning shooting script's hook + core>
Stats:
  - <label>: <value>   (from plan Cover Brief; qualitative contrast pairs if no numbers)
Winning angle: <from editor verdict>
Tagline: <from 01-reel-plan.md Cover Brief>
Author: Altaf Shaikh
Handle: @teachmebro
Domain: <e.g. "AI Engineering">
Output path: ./instagram-reels/reels/<reel-slug>-<YYYYMMDD>/cover
```

The image-gen-agent emits `[IMAGE REASONING]`, then writes `cover-1.svg`, `cover-2.svg` (+ `exports/*.png`). Do NOT write SVG inline — always delegate. **Then proceed to Step N.**

---

## Step N — Finalize and update the ledger

**Mandatory every production run.**

1. Write `reel-script.md` (template below) — the deliverable.
2. **DO NOT touch `../raw-ideas/`.**
3. Update `./instagram-reels/TODO.md`: remove from **In Progress**; prepend a **Produced** line listing the reel folder, its **type**, and **all source idea filenames**.
4. Refresh `reel-map.md` so the produced candidate is marked ✅ (and coverage updated).
5. Print the final summary block.

---

## `reel-map.md` template

```markdown
# Instagram Reel Map

Living board of reel candidates mined from the whole `../raw-ideas/` library. Refreshed every run. Ranked by reel-worthiness. ✅ = already produced (see TODO.md Produced).

_Last refreshed: <YYYY-MM-DD> · Library size: <N ideas> · Coverage: <X>/<N> ideas have ≥1 reel_

## Direct reels (1 idea → 1 reel)
| # | Reel-worthiness | Reel idea (working title) | Source | Style | Status |
|---|-----------------|---------------------------|--------|-------|--------|
| 1 | 9 | <title> | <NNN-slug.md> | faceless | ⬜ |

## Combo reels (several ideas → 1 reel)
| # | Reel-worthiness | Reel idea | Sources (merged) | Angle | Status |
|---|-----------------|-----------|------------------|-------|--------|
| 1 | 8 | <title> | <a.md> + <b.md> | <unifying angle> | ⬜ |

## Pattern reels (derived across the library — not in any single file)
| # | Reel-worthiness | Reel idea | Grounded in | The pattern | Status |
|---|-----------------|-----------|-------------|-------------|--------|
| 1 | 9 | <title> | <a.md>, <b.md>, <c.md> | <the recurring theme/contradiction the library implies> | ⬜ |

## Coverage gaps (ideas with no reel yet)
- <NNN-slug.md> — <why it's hard / what angle it needs>
```

---

## `TODO.md` template

```markdown
# Instagram Reels — Status

Instagram does NOT drain a queue — it mines the whole library. The live menu of reel ideas lives in [`reel-map.md`](./reel-map.md). This file tracks what's been scripted. An idea can fuel several reels, so ideas are never "used up"; we track produced reels (with their source ideas) and coverage.

**Reel map:** [`reel-map.md`](./reel-map.md) — last refreshed <YYYY-MM-DD>

## In Progress
_(none)_

## Produced
- [x] [reels/<reel-slug>-<YYYYMMDD>/reel-script.md](./reels/<reel-slug>-<YYYYMMDD>/reel-script.md) — <Direct|Combo|Pattern> — sources: <a.md, b.md> — <YYYY-MM-DD>

## Parked (reel ideas judged not worth producing)
- [ ] <working title> — <one-line reason> — <YYYY-MM-DD>
```

Refresh nothing destructively: append to **Produced** and **Parked**; never delete unless the user asks to re-make a reel.

---

## `reel-script.md` template (THE DELIVERABLE)

```markdown
# <Reel working title>

**Type:** <Direct | Combo | Pattern>
**Source idea(s):** <links to ../../../raw-ideas/<file>.md for each source>
**Generated:** <YYYY-MM-DD>  ·  **Style:** <FACELESS | ON-CAMERA>  ·  **Format:** <...>  ·  **Target length:** <Ns>  ·  **Rounds:** <1|2>

## Variation Scores (Round 1)

| Variant | Angle | Hook(1-2s) | Retention | Payoff | Clarity | CTA | Avg |
|---------|-------|-----------|-----------|--------|---------|-----|-----|
| A | Demo | 9 | 8 | 8 | 9 | 7 | 8.2 |

**Winner:** Variant <X> — <why>

---

## Shooting Script (shoot this)

| Time | On-screen text | Spoken / VO | Visual |
|------|----------------|-------------|--------|
| 0-2s | <hook overlay> | <hook line> | <visual> |
| ... | ... | ... | ... |

## Caption
<hook first line>
<body>
<CTA>

**Hashtags:** <#tag #tag #tag>

## Audio
<trending vibe to search for | original voiceover>

## Cover frames

| File | Format | Style | Carries |
|------|--------|-------|---------|
| [cover-1.svg](./cover-1.svg) | 1080×1920 (9:16) | <style> | <elements> |
| [cover-2.svg](./cover-2.svg) | 1080×1350 (4:5) | <style> | <elements> |

**Exported PNGs:** `exports/cover-1.png` · `exports/cover-2.png`

---

**Unresolved issues:** <list or "none">
```

---

## Conversation output (every run)

**Map only (Mode B):**
```
Instagram reel map refreshed → ./instagram-reels/reel-map.md
Candidates: <D> direct · <C> combo · <P> pattern. Top pick: <title> (<score>).
Run /instagram-reels-agent to script it, or name one.
```

**Empty library:**
```
No raw ideas to mine for reels. Drop files into ../raw-ideas/ and re-run.
```

**Scripted a reel (Mode A / C):**
```
Channel: Instagram Reels
Reel: <title>  (<Direct|Combo|Pattern>)
Sources: <a.md, b.md>
Style: <FACELESS|ON-CAMERA> · Format: <...> · Length: ~<Ns>
Folder: ./instagram-reels/reels/<reel-slug>-<YYYYMMDD>/
Deliverable: .../reel-script.md
Covers: cover-1.svg (9:16) · cover-2.svg (4:5)  → exports/*.png
Map: ./instagram-reels/reel-map.md (refreshed)
```

---

## Loop integration (`/loop`)

Wrapped by `../instagram.agent.md`. Each firing: refresh the reel-map over the full library, script the top unproduced candidate (Mode A), update TODO + map. No-ops gracefully if the library is empty or every candidate is produced/parked.

---

## Shared rules (all agents)

Same shared rules as `x-growth-agent` / `linkedin-growth-agent`, plus the Instagram specifics: mine the whole library (don't drain a queue), reel-worthiness selection, per-reel faceless/on-camera decision, hook in the first 1-2s, 3-5 relevant hashtags, name an audio approach. Never write outside `./instagram-reels/` (except Mode C may write ONE new file to `../raw-ideas/`, and every run appends one row to `./runs/instagram.md`). Never move, rename, or delete anything in `../raw-ideas/`. Read-only cross-channel signal from LinkedIn/X is allowed; writes there are forbidden.

---

## Run log (heartbeat) — write this on EVERY run

**The last action of every run, on every path, including early exits.** Full contract: `runs/README.md` at the repo root.

Append ONE row to `./runs/instagram.md` (repo root, not the channel folder). Newest at the bottom:

```
| <YYYY-MM-DD> | <outcome> | <one short line, no trailing period> | <link to reel folder or —> |
```

`<outcome>` is exactly one of `produced` · `skipped` · `blocked` · `error`.

| Path through the run | Outcome |
|---|---|
| Scripted a reel and opened a PR | `produced` |
| Every map candidate is already produced or parked, or the library is empty | `skipped` |
| A gate stopped the run on purpose | `blocked` |
| The run failed. Put the failure in `Detail` | `error` |

A run that **only** refreshed `reel-map.md` without scripting anything is `skipped`, with a Detail saying the map was refreshed and how many candidates it now holds. That is a real, useful outcome and it should be visible.

**Committing the row:**

- **Scripted a reel** → include `runs/instagram.md` in the same content branch and commit.
- **Produced nothing** → commit this one file alone and push straight to the fork's `main`:

  ```bash
  git add runs/instagram.md
  git commit -m "runs: instagram <YYYY-MM-DD> <outcome>"
  git pull --rebase origin main && git push origin main
  ```

  The ONE exception to "never push to main directly." It must never carry any other file. If the push fails, say so and finish the run anyway.

Why this is mandatory for THIS channel in particular: Instagram produced nothing and opened zero PRs between 2026-06-28 and 2026-08-15, with `reel-map.md` stale the whole time, and nobody noticed. `skipped` is a healthy outcome. A missing row is not.
