---
name: x-growth-agent
description: "Daily-loop X (Twitter) post factory inside a multi-channel content factory. Reads ideas from a SHARED ../raw-ideas/ library (immutable) and writes X-specific outputs into ./x-posts/. Each run picks the oldest unconsumed idea (queue = ls raw-ideas/ minus this channel's TODO.md Done section), runs a pipeline (Strategist decides single-tweet vs thread → N Copywriters → Editor) + an Image Designer, saves every handoff to a per-post folder, and updates TODO.md. The source idea NEVER moves — it stays in the shared library so other channels (LinkedIn, blog, presentation) can also consume it. If no unconsumed ideas exist for X, the run exits quietly. Use when user says /x-growth-agent, 'write a tweet', 'draft a thread about X', 'process my X ideas', or when invoked via /loop. Always trigger this skill."
trigger: /x-growth-agent
extends: linkedin-growth-agent
---

# /x-growth-agent

A daily-loop X (Twitter) post factory. The user keeps dropping raw ideas into a shared folder; each invocation processes ONE new idea end-to-end (or no-ops if there are none).

This is the X sibling of `linkedin-growth-agent`. The shape is the same — compute queue, pick oldest, run a writer pipeline, generate images, finalize TODO.md — but the platform rules differ. Where this file is silent, the LinkedIn skill's structure applies; where it speaks, X wins.

**Default variations per post: 3 (one per X-native angle — see Angle Assignments). Override with `/x-growth-agent 2` to drop the contrarian angle for this run. Max 3.**

---

## What makes X different from LinkedIn (read first)

| Dimension | LinkedIn | X (this skill) |
|-----------|----------|----------------|
| **Output unit** | One long-form post | **Single tweet by default; thread only when the idea genuinely breaks into sections** (Strategist decides) |
| **Length** | ~1300 chars, line-break heavy | **280 chars HARD per tweet.** Single tweet ≤ 280. Each thread tweet ≤ 280. |
| **Hashtags** | 3–5 niche tags | **None by default.** Hashtags suppress reach and read as spam on X. At most 1, only if it's a real live community tag. |
| **Links** | Link in first comment | **Link in a reply, never the main tweet** (X downranks tweets with external links). |
| **Hook** | First line, room to breathe | First ~7 words decide the scroll. Front-load the payload. No "a thread 🧵" preamble. |
| **Tone** | Professional-personal | Sharper, faster, more conversational. Punchy beats polished. |
| **Image dims** | Portrait 1080×1350 | **Landscape 1600×900 (16:9, in-stream default) and Square 1080×1080.** No portrait. |

Everything else (immutable `../raw-ideas/`, one-idea-per-run, save-every-handoff, no emojis, strip company/tool names, never invent stats) is identical to LinkedIn — see `.claude/skills/linkedin-growth-agent/SKILL.md` for the shared rules.

---

## Project folder layout (canonical)

```
content-factory/                            ← project root
├── raw-ideas/                              ← SHARED, immutable, read-only from this skill
│   ├── 001-<slug>.md
│   └── 002-<slug>.md
├── x.agent.md                              ← daily /loop prompt (calls this skill)
└── x-posts/                                ← X channel folder (this skill writes here)
    ├── README.md
    ├── CLAUDE.md
    ├── PLAYBOOK.md                         ← X best-practices; the craft baseline (read every run)
    ├── TODO.md                             ← Queue + In Progress + Done sections
    └── posts/                              ← one folder per generated post
        └── <slug>-<YYYYMMDD>/
            ├── 00-x-fit.md                     ← X Fit Gate verdict + LinkedIn cross-channel signal
            ├── 01-post-plan.md
            ├── 02a-draft-<angle>.md
            ├── 02b-draft-<angle>.md
            ├── 02c-draft-<angle>.md            (if N=3)
            ├── 03-editor-verdict.json
            ├── 02-revised-draft.md             (if revision round)
            ├── 03-editor-verdict-final.json    (if revision round)
            ├── impact-1.svg
            ├── impact-2.svg
            ├── exports/
            │   ├── impact-1.png
            │   └── impact-2.png
            └── final-post.md
```

**`../raw-ideas/` is immutable.** Never move, rename, or delete files in it. Consumption is tracked in `./x-posts/TODO.md` Done section.

**Bootstrap on first run:** if `./x-posts/` is missing its scaffold (`TODO.md`, `posts/`), create it (templates below) and continue. If `../raw-ideas/` doesn't exist, create it, tell the user where to drop ideas, and exit.

> **No performance loop on X — read the PLAYBOOK instead.** This channel runs on a free X account with no analytics export, so there is no Agent 0, no `performance/` folder, and no `performance.md`. In its place, **`./x-posts/PLAYBOOK.md` encodes X's known rules of the game** (hooks, reach suppressors, thread craft, the rookie-mistake checklist). Every agent in this pipeline reads it: the Strategist before planning, the Copywriters while writing, the Editor while scoring. It is the craft baseline that keeps us from naive mistakes. (The base `performance-marketing-agent` still serves other channels; X simply doesn't use it.)

---

## Step 0 — Compute the queue and pick the idea

Identical mechanics to LinkedIn, but the channel token is `"x"`.

**Mode A — Loop / autonomous run** (no idea content in args, or invoked via `/loop`):

1. List files in `../raw-ideas/` (relative to `./x-posts/`). Accept `.md` and `.txt`.
2. Read `./x-posts/TODO.md`. Extract filenames in the **Done**, **In Progress**, and **Skipped (not a fit for X)** sections.
3. Compute the X queue:
   ```
   queue = (files in ../raw-ideas/) MINUS (Done) MINUS (In Progress) MINUS (Skipped)
   ```
4. Filter: drop any file whose frontmatter declares `channels: [...]` without `"x"` in the list.
5. If queue is empty → print `No new X ideas. Skipping.`, write the run-log row with outcome `skipped` (see **Run log** below), and exit. **Generate nothing.**
6. Otherwise pick the **oldest by filename sort** (lexical — `001-` before `002-`).
7. Read the chosen file. Its content (minus frontmatter) is the **candidate raw idea**.
8. Derive `<slug>` from the filename (strip extension AND numeric prefix, kebab-case).
9. **Do NOT create the post folder or move to In Progress yet.** First run **Step 0.5 — the X Fit Gate** on this candidate. Only an idea that PASSES the gate becomes the run's idea.

**Mode B — Direct invocation with content in args** (`/x-growth-agent <idea text>`):

1. Treat args as the raw idea.
2. Derive `<slug>` from the first 3–5 meaningful words.
3. Find the next numeric prefix in `../raw-ideas/` and write the idea to `../raw-ideas/<NNN>-<slug>.md` so other channels can also consume it. Then continue.

**N parsing:** if args start with a small integer (`/x-growth-agent 2 ...`), that's N. Otherwise N=3 (the default). Max N=3.

(Folder creation + In Progress move happen at the end of Step 0.5, only for an idea that passes the gate. For **Mode B** — direct invocation — the user explicitly asked for this topic, so run the gate in advisory mode: surface the fit verdict but DO NOT auto-skip; proceed to generate regardless.)

---

## Step 0.5 — X Fit Gate + Cross-Channel Signal (runs before every generation)

Not every idea that works on LinkedIn works on X. **Before committing to generate, critically judge whether this topic is worth an X post** — and borrow signal from the LinkedIn channel, since X has no analytics of its own.

### A. Cross-channel signal (READ-ONLY from LinkedIn)

The X channel may **read** the LinkedIn channel for advisory signal. It must NEVER write there, move files, or alter LinkedIn state. (This is the one sanctioned cross-channel read — see project CLAUDE.md rule 3.)

1. Open `../linkedin-posts/TODO.md`. Look for this idea's **source filename** in the **Done** section.
   - **Not found** → LinkedIn hasn't published it. No cross-channel signal; judge on X-fit alone (Part B).
   - **Found** → note the linked post folder. Continue.
2. Open that LinkedIn post folder (`../linkedin-posts/posts/<slug>-<date>/`). Read `final-post.md` (the winning angle/hook) and, if present, `performance.md`.
   - **`performance.md` has metrics AND an `## Agent Verdict`** → analytics were synced. Extract the real signal: engagement level, the hook/angle that won, what the verdict said to replicate or drop.
   - **`performance.md` missing or has no verdict** → published but **analytics not yet synced**. Treat as a weak positive (it was worth publishing somewhere) but no performance data to lean on.

### B. X-fit critical analysis

Score the idea against what X rewards (use `./x-posts/PLAYBOOK.md` — the follow-reasons in §11 and the reach mechanics in §5). Ask honestly:

- Is there a **punchy, quotable claim** or a sharp contrast in here? (X lives on the screenshot-able line.)
- Can it land a clear **follow-reason** — TIL / FIRED-UP / LOL / HMM / FINALLY?
- Is there a **defensible contrarian take** or a **relatable build-in-public moment**?
- Can the core land in **≤280 chars** (single) or a tight thread — without needing long-form nuance to not be misread?
- Is it **too inside-baseball, too caveated, or too dependent on a link/visual** to work as fast-scroll text?

### C. Verdict → `worth_posting: yes | borderline | no`

Print `[HANDOFF: X FIT GATE]` AND (only if the verdict is `yes`/`borderline`) save it to the post folder as `00-x-fit.md`. Format:

```
## X Fit Verdict
worth_posting: <yes | borderline | no>
fit_score: <0–10>

## Why
<2–4 sentences: what makes this land (or not) on X specifically>

## Cross-channel signal (LinkedIn)
Published on LinkedIn: <yes + folder | no>
Analytics synced: <yes — summary of performance | no | n/a>
Winning angle there: <angle/hook, or n/a>
Implication for X: <one line — e.g. "strong LinkedIn comment-rate → lead with the same contrast on X" or "no signal yet, judge on merits">

## Recommended X angle lean
<which of the 3 angles to weight, and the candidate hook line(s)>
```

**Acting on the verdict:**

- **`yes` / `borderline`** → this is the run's idea. NOW create the post folder `./x-posts/posts/<slug>-<YYYYMMDD>/`, write `00-x-fit.md` into it, move the idea to **In Progress** in TODO.md, and proceed to the Strategist (which reads `00-x-fit.md`).
- **`no`** → do NOT generate. Add the idea to the **Skipped (not a fit for X)** section of `./x-posts/TODO.md` with a one-line reason and date. Then return to Step 0 and evaluate the **next** oldest queued idea. Repeat until an idea passes or the queue is exhausted (if exhausted → print `No X-worthy ideas in the queue right now. Skipping.`, write the run-log row with outcome `skipped`, and exit).
- **Mode B (direct invocation):** advisory only — print the verdict but always proceed, even on `no` (the user explicitly asked for this topic).

A `no` is not permanent: the user can move an idea out of **Skipped** back to the queue any time, and direct invocation always overrides the gate.

---

## Pipeline overview

```
[Queue pick: oldest unconsumed idea]
    ↓
X Fit Gate (Step 0.5)       → 00-x-fit.md   (reads LinkedIn signal READ-ONLY; verdict yes/borderline/no)
    ↓ no  → log to Skipped, try next idea        ↓ yes/borderline
                                            (create folder, In Progress)
    ↓
Strategist (once)           → 01-post-plan.md  (reads 00-x-fit.md; decides SINGLE vs THREAD)
    ↓
Copywriters × N (parallel)  → 02a..02c-draft-*.md   (all write in the chosen format)
    ↓
Editor                      → 03-editor-verdict.json
    ↓ if needs_revision AND round < 2
Copywriter (winner)         → 02-revised-draft.md
    ↓
Editor (final verdict)      → 03-editor-verdict-final.json
    ↓
Image Designer (/image-gen-agent × 2) → impact-1.svg, impact-2.svg
    ↓
[FINAL OUTPUT]              → final-post.md
    ↓
DO NOT touch ../raw-ideas/  (immutable, shared)
Update ./x-posts/TODO.md: move filename from In Progress → Done with link to post folder
```

Max revision rounds: **2**.

---

## Strategist (runs once)

**Job:** Analyze the raw idea → decide the FORMAT → produce a master plan AND define N distinct angles.

**Before planning, read `./x-posts/PLAYBOOK.md` AND `00-x-fit.md`** (the gate's verdict for this idea). The playbook is the craft baseline; `00-x-fit.md` carries the cross-channel signal and the recommended angle lean — let it bias which angle to weight and the candidate hook. There is no analytics tracker to read on X.

### Format decision (X-specific, do this FIRST)

Decide **SINGLE** or **THREAD** and state the verdict + rationale at the top of the plan.

- **Default to SINGLE.** A single tweet is the right unit unless the idea structurally demands more.
- Choose **THREAD** only when the idea genuinely breaks into **≥3 distinct sections** — sequential steps, a numbered list, a multi-part argument, or a before→after→lesson arc that loses meaning when compressed. If you can land the payload in one ≤280-char tweet without gutting it, do that.
- A thread must earn every tweet. 3–7 tweets. No filler. Tweet 1 is a standalone hook that works even if no one expands the thread.

Print `[HANDOFF: STRATEGIST]` AND save to `01-post-plan.md`:

```
## Format Decision
<SINGLE | THREAD> — <one-line rationale: why this idea fits this format; if THREAD, how many tweets and the section breakdown>

## Core Insight
<the central idea in one sentence — the "so what">

## Target Audience
<who specifically — be precise>

## Structure
SINGLE → the one beat the tweet must land.
THREAD → tweet-by-tweet outline:
  1. <hook tweet>
  2. <beat>
  3. <beat>
  ... (3–7 total)

## CTA / Reply hook
<the close. For X, the primary CTA is engagement (a question or a take that invites replies). If the idea has a link, it goes in a REPLY, never the main tweet — note the reply text here.>

## Tone
<punchy | contrarian | tactical | story | analytical>

## Hashtags
None — unless one real community tag genuinely helps. State it or write "none".

## Image Brief
<2–5 numbers/data points or contrast pairs the image should carry · 1 tagline>

## Angle Assignments
X is its own platform — these angles are X-native, not LinkedIn carry-overs. Each targets a DIFFERENT X engagement signal so the three drafts can't collapse into the same tweet. Angles 1 and 2 must read as clearly different posts.

  - **Angle 1 — Viral / reach play (always):** engineered for reposts + bookmarks. One pattern-interrupt or bold, quotable claim that stops the scroll and begs to be screenshotted/re-shared. Sharpest possible hook; strip everything that isn't the punch.
  - **Angle 2 — Build-in-public / story play (always):** a concrete first-person moment — what you did, what happened, what surprised you. Curiosity gap up front, authentic and specific. Targets replies through relatability ("same thing happened to me").
  - **Angle 3 — Contrarian / debate play (at N=3):** a clear, defensible stance against a common belief in the space, framed to invite civil disagreement. Targets replies + quote-tweets — the conversation play. Must be a REAL position drawn from the idea, never manufactured outrage or engagement bait.

When N=2, use Angles 1 and 2 (the two most reliably distinct). When N=3, add Angle 3.

If the idea genuinely can't support a defensible contrarian take, the Strategist MAY swap Angle 3 for a **Tactical/how-to play** (lead with the practical payoff, then the steps — targets bookmarks) or a **Data/proof-point play** (open on the hardest number). State the swap and the one-line reason.
```

---

## Copywriters (N instances, run in parallel)

Run all N simultaneously. Each receives the plan + its assigned angle + the FORMAT decision.

**Read `./x-posts/PLAYBOOK.md` first** — it's the craft baseline every draft must respect (hooks, character economy, reach suppressors, voice). The rules below are the enforced subset; the playbook is the full picture.

**Rules for every X Copywriter:**
- Write in the format the Strategist chose (SINGLE or THREAD).
- **Hard 280-char limit per tweet.** Count characters. A single tweet over 280 is invalid. Each thread tweet over 280 is invalid.
- First ~7 words carry the hook. No "a thread:", no "🧵", no "In this post". Open on the payload.
- Short, declarative lines. Cut every word that isn't load-bearing.
- **No hashtags** unless the plan explicitly named one real community tag.
- **No link in the main tweet/first tweet.** If there's a link, it goes in the reply-hook line (label it `Reply:`).
- For THREAD: number tweets `1/`, `2/`, … (or `1/n`). Each tweet must read as a coherent unit. The last tweet lands the CTA / invites replies.
- End on the CTA from the plan — for X this is usually a question or a take that invites replies, not a "DM me".
- **CTA must be public-shareable** — never offer DM access to internal/proprietary tools.
- Never add ideas not in the plan. Never invent stats, quotes, or claims. Strip company/tool names — keep the lesson.
- No emojis unless Altaf explicitly asks.
- No em dashes (—). Use a comma, a colon, a full stop, or rewrite as two sentences instead.

Each Copywriter prints its block AND writes its file. File naming `02<x>-draft-<angle-slug>.md`:
- Angle 1 → `02a-draft-viral.md`
- Angle 2 → `02b-draft-story.md`
- Angle 3 → `02c-draft-contrarian.md` (or `02c-draft-tactical.md` / `02c-draft-data.md` if the Strategist swapped Angle 3)

Block format:
```
[HANDOFF: COPYWRITER — <Angle Name>]

Format: <SINGLE | THREAD>

<the tweet, OR the numbered thread — paste-ready>

Reply: <reply-hook text with link, if any — else "none">

---
Angle: <angle name>
Hook: <exact first line>
Char counts: <single: N>  OR  <thread: t1=N, t2=N, ...>  (all must be ≤280)
```

**On revision round** (winner only): print `[HANDOFF: COPYWRITER — REVISED <Angle>]`, save to `02-revised-draft.md` with a `Changes made:` list.

---

## Editor

**Read `./x-posts/PLAYBOOK.md` §9 (the rookie-mistake checklist) and score against it.** The Editor is the gate that catches playbook violations before anything ships.

**Round 1:** score every variant, pick the winner, decide on revision.
**Round 2:** final verdict on the revised draft.

Print `[HANDOFF: EDITOR]` — valid JSON only. Save to `03-editor-verdict.json` (round 1) or `03-editor-verdict-final.json` (round 2):

```json
{
  "round": 1,
  "format": "SINGLE | THREAD",
  "variants_reviewed": ["A", "B", "C"],
  "status": "approved | needs_revision",
  "winner": "A | B | C",
  "why_winner": "<1-2 sentences>",
  "scores": {
    "A": { "hook_strength": 9, "scroll_stop": 8, "conciseness": 9, "authenticity": 8, "cta_clarity": 7, "avg": 8.2 },
    "B": { "hook_strength": 7, "scroll_stop": 7, "conciseness": 8, "authenticity": 9, "cta_clarity": 8, "avg": 7.8 },
    "C": { "hook_strength": 8, "scroll_stop": 8, "conciseness": 8, "authenticity": 8, "cta_clarity": 9, "avg": 8.2 }
  },
  "char_check": { "A": "pass | FAIL (t3=291)", "B": "pass", "C": "pass" },
  "runner_up_notes": { "B": "<what the winner should borrow>" },
  "issues": [
    {
      "type": "weak_hook | over_limit | buries_payload | off_plan | missing_cta | jargon | inauthentic | wrong_format | non_shareable_cta | link_in_main_tweet | has_hashtags",
      "severity": "high | medium | low",
      "description": "<exact problem in the WINNER draft>",
      "action": "<exact fix instruction>"
    }
  ]
}
```

**Hard fails (always `needs_revision` if present in the winner):** any tweet over 280 chars (`over_limit`), a link in the main/first tweet (`link_in_main_tweet`), or unrequested hashtags (`has_hashtags`).

**Decision logic:**
- `approved` → Image Designer
- `needs_revision` AND round < 2 → loop winner through one Copywriter
- round = 2 → output best available, list unresolved issues

---

## Image Designer (runs once, after final post is locked)

**Job:** Generate TWO distinct image variations by invoking `/image-gen-agent` once with `Variations: 2`. Pass `Channel: x` so it uses X formats and styles.

**X dimensions (no portrait):** the image agent should choose between **Landscape 1600×900 (16:9)** — the in-stream default — and **Square 1080×1080 (1:1)** — quote-card. The two variations must differ in BOTH dimension and style.

```
[IMAGE BRIEF]
Channel: x
Variations: 2
Dimensions: reason   ← X options only: 1600×900 (16:9) or 1080×1080 (1:1)
Style hint: reason
Final post: <paste the full final tweet/thread text>
Stats:
  - <label>: <value>
  (from final post + 01-post-plan.md Image Brief; use qualitative contrast pairs if no numbers)
Winning angle: <angle name from editor verdict>
Tagline: <from Image Brief in 01-post-plan.md>
Author: Altaf Shaikh
Handle: @teachmebro
Domain: <e.g. "AI Engineering">
Output path: ./x-posts/posts/<slug>-<YYYYMMDD>/impact
```

The image-gen-agent emits an `[IMAGE REASONING]` block, then generates `impact-1.svg` and `impact-2.svg` (+ `exports/*.png`). Do NOT write SVG inline. Always delegate.

**After image generation, the pipeline is NOT done — immediately proceed to Step N.**

---

## Step N — Finalize and update the queue

**Mandatory every run. Never skip.**

1. **Write `final-post.md`** (template below).
2. **DO NOT touch `../raw-ideas/`.** Immutable, shared.
3. **Update `./x-posts/TODO.md`:** remove from In Progress; prepend a Done line with source filename, post-folder link, date.
4. **Print the final output block.**

---

## `TODO.md` template

```markdown
# X — Queue & Status

This is the X channel's consumption ledger. Raw ideas live in `../raw-ideas/` (shared across all channels). Queue = files in `../raw-ideas/` MINUS the filenames listed under **Done** below.

## Queue (unprocessed for X)
- [ ] <NNN>-<slug>.md — <one-line preview>

## In Progress
- [ ] <NNN>-<slug>.md — started <YYYY-MM-DD>

## Done
- [x] <NNN>-<slug>.md → [posts/<slug>-<YYYYMMDD>/final-post.md](./posts/<slug>-<YYYYMMDD>/final-post.md) — <YYYY-MM-DD>

## Skipped (not a fit for X)
- [ ] <NNN>-<slug>.md — <one-line reason from the Fit Gate> — <YYYY-MM-DD>
```

Regenerate the Queue section each run. Append to Done and Skipped; never delete entries from either unless the user asks to re-run or re-queue an idea. The Skipped section is how the gate's `no` verdicts are remembered so they aren't re-evaluated every run.

---

## `final-post.md` template

```markdown
# <slug>

**Source idea:** [../../../raw-ideas/<NNN>-<slug>.md](../../../raw-ideas/<NNN>-<slug>.md)
**Generated:** <YYYY-MM-DD>
**Format:** <SINGLE | THREAD>  ·  **Rounds:** <1 or 2>  ·  **Revised:** <yes/no>

## Variation Scores (Round 1)

| Variant | Angle | Hook | Scroll-stop | Conciseness | Authenticity | CTA | Avg |
|---------|-------|------|-------------|-------------|--------------|-----|-----|
| A       | Viral | 9 | 8 | 9 | 8 | 7 | 8.2 |
| B       | Story | 7 | 7 | 8 | 9 | 8 | 7.8 |
| C       | Contrarian | 8 | 8 | 8 | 8 | 9 | 8.2 |

**Winner:** Variant <X> — <why_winner>

---

## Final Post

<SINGLE → the one tweet, paste-ready (≤280 chars)>
<THREAD → numbered tweets 1/ 2/ 3/ …, each ≤280, paste-ready>

**Reply (post after the main tweet):** <reply-hook text + link, or "none">

---

## Images

| File | Format | Style | Carries |
|------|--------|-------|---------|
| [impact-1.svg](./impact-1.svg) | <W>×<H> (<16:9 Landscape \| 1:1 Square>) | <style name> | <stats/elements> |
| [impact-2.svg](./impact-2.svg) | <W>×<H> (<16:9 Landscape \| 1:1 Square>) | <style name> | <stats/elements> |

**Exported PNGs:** `exports/impact-1.png` · `exports/impact-2.png`

---

**Unresolved issues:** <list or "none">
```

---

## Conversation output (every run)

**No-op (empty queue):**
```
No new X ideas. Skipping.
```

**No-op (queue had ideas, but none passed the Fit Gate):**
```
No X-worthy ideas in the queue right now. Skipping.
Skipped this run: <filename(s)> — see TODO.md "Skipped" for reasons.
```

**Processed an idea:**
```
Channel: X
Processed: <NNN>-<slug>.md
Format: <SINGLE | THREAD>
Post folder: ./x-posts/posts/<slug>-<YYYYMMDD>/
Final post: ./x-posts/posts/<slug>-<YYYYMMDD>/final-post.md
Images (SVG): impact-1.svg · impact-2.svg
Images (PNG): exports/impact-1.png · exports/impact-2.png
Queue remaining (X): <N> idea(s)
```

---

## Loop integration (`/loop`)

Wrapped by `../x.agent.md`:
```
/loop 1d <paste x.agent.md prompt>
```
Each firing: computes X queue (`../raw-ideas/` MINUS TODO.md Done + In Progress), processes ONE idea if non-empty, no-ops silently if empty, never re-processes a Done filename, respects `channels:` frontmatter. Other channels keep independent queues against the same shared library.

---

## Shared rules (all agents)

Identical to `linkedin-growth-agent`'s shared-rules section — plus the X-specific hard rules: 280-char ceiling per tweet, no hashtags by default, links only in replies, hook in the first ~7 words. Never write outside `./x-posts/` (except Mode B may write ONE new file to `../raw-ideas/`, and every run appends one row to `./runs/x.md`). Never move, rename, or delete anything in `../raw-ideas/`.

---

## Run log (heartbeat) — write this on EVERY run

**The last action of every run, on every path, including early exits.** Full contract: `runs/README.md` at the repo root.

Append ONE row to `./runs/x.md` (repo root, not the channel folder). Newest at the bottom:

```
| <YYYY-MM-DD> | <outcome> | <one short line, no trailing period> | <link to post folder or —> |
```

`<outcome>` is exactly one of `produced` · `skipped` · `blocked` · `error`.

| Path through the run | Outcome |
|---|---|
| Generated a post or thread and opened a PR | `produced` |
| Empty queue, every candidate already in flight, or the X Fit Gate rejected everything left | `skipped` |
| A gate stopped the run on purpose | `blocked` |
| The run failed. Put the failure in `Detail` | `error` |

When the Fit Gate sends an idea to **Skipped**, that is still an outcome worth logging: use `skipped` with a Detail like `fit gate rejected 3 ideas, queue exhausted`.

**Committing the row:**

- **Produced a post** → include `runs/x.md` in the same content branch and commit.
- **Produced nothing** → commit this one file alone and push straight to the fork's `main`:

  ```bash
  git add runs/x.md
  git commit -m "runs: x <YYYY-MM-DD> <outcome>"
  git pull --rebase origin main && git push origin main
  ```

  The ONE exception to "never push to main directly." It must never carry any other file. If the push fails, say so and finish the run anyway.

Why this is mandatory for THIS channel in particular: X produced nothing and opened zero PRs between 2026-06-30 and 2026-08-15, and nobody noticed, because a quiet exit and a dead routine look identical from outside. `skipped` is a healthy outcome. A missing row is not.
