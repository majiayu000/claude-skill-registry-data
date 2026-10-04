---
name: war-room
description: Build and maintain the project's living plan (the Plan/ folder — roadmap, phases, toolbox), and triage every new meeting or video AGAINST that plan. Use when the user says "/roadmap", "build a plan for this project", "plan before we execute", "here's a video — is this worth using?", "does this change our plan?", "/intel", "incorporate this into the plan", "new technique we should consider", "add this tool to the project", or drops a YouTube link asking whether/how it affects the project. The plan-aware answer to "should we use this?" — not just "what does the video say?".
---

# War-Room — the plan that watches videos back

Most plans die the week after kickoff because new information (a meeting, a
YouTube technique, a shiny tool) either gets ignored or gets bolted on without
judgment. The war-room fixes both failure modes: the plan is a **living
folder** (`Plan/`), and every new source is **triaged against it** — ranked,
argued, incorporated or passed on, with provenance either way.

Division of labor: `scripts/plan_tool.py` owns the mechanics (scaffold,
digest, briefs, status); this skill owns the judgment. How it relates to the
rest of Omnia Vault:

| System | Question it answers |
|---|---|
| Wiki (`llm-wiki-*`) | "what do we know?" — durable, source-traced knowledge |
| Sparring (`/spar`) | "will this ONE design survive contact?" — pre-build stress test |
| **War-room** (`/roadmap`, `/intel`) | "what are we doing, in what order — and does this new video change that?" |

The plan cites the wiki and Raw sources; big plan changes get sparred.

---

## Part 1 — Build the plan (`/roadmap`)

1. **Recon first** (the vault probably knows things): `relay_tool.py status`,
   `search-catalog` on the project topic, the project note's Goal/Next Steps,
   graph queries if repos are tracked. If the user has kickoff meetings or
   videos, ingest them FIRST (`video-ingest` / `llm-wiki-ingest`) — the plan
   should be built from captured knowledge, not vibes.
2. **Interview, LOCK-style** (borrow the sparring skill's discipline): only
   load-bearing questions, one at a time — vision, measurable success
   criteria, the phase boundaries, each phase's exit criterion, the ordering
   constraints. Cosmetic choices get batched recommendations.
3. **Scaffold:** `python scripts/plan_tool.py init --name "<project>"
   --phases "<A,B,C,...>"` then fill every `<placeholder>` in `ROADMAP.md`
   and each `Plan/phases/phase-N-*.md`: Objective (one paragraph),
   Deliverables (checkboxes — concrete, verifiable), Exit criteria
   (observable), Depends on. Exactly one phase is `**Status:** active`.
4. **Wire it in:** the Wiki project note links `[[Plan/ROADMAP]]`; the relay
   baton's **Now** names the active phase. Gate → commit.
5. High-stakes architecture inside a phase still goes through `/spar` before
   it's built — the roadmap says *what and when*, sparring hardens *how*.

Maintain it forever after: checking deliverables, phase transitions
(`active` → `done`, next `pending` → `active`), and a Changelog line for every
meaningful edit — each citing an intel brief, a spar, or a user decision.

## Part 2 — Intel triage (`/intel <url-or-file>`) — the core loop

The user drops a video, recording, or article: *"is this worth anything to
us?"* Never answer from the video alone.

### 1. Plan first, video second

```bash
python scripts/plan_tool.py context
```

Load the digest BEFORE watching: vision, phase statuses, the active phase's
open deliverables, adopted tools, recent intel verdicts. This is what makes
the triage an answer about **our project** instead of a video summary.

### 2. Watch it properly

Run the `video-ingest` mechanics (crv in the background, frames ⇄ transcript
correlation, secret redaction). **Always land the full capture in
`Raw/Sources/`** with source frontmatter — plan briefs must cite something
permanent, and a skipped video today may matter in phase 3.
(Articles/links: `defuddle` → `llm-wiki-ingest` capture instead.)

### 3. Extract and dedupe

List every candidate item — techniques, patterns, tools, claims, links.
Then kill the déjà vu: check `search-catalog`, `Plan/TOOLBOX.md`, and prior
`Plan/intel/` briefs. "New to us" is the bar, not "said enthusiastically."

### 4. Rank against the plan

`python scripts/plan_tool.py new-intel --title "..." --source "<url>"` and
fill the brief's table — every item scored:

| Dimension | Question |
|---|---|
| **Phase fit** | which phase's deliverables/exit criteria does it touch? (none = near-automatic SKIP/WATCH) |
| **Impact** | H/M/L — does it move a deliverable, kill a risk, or just decorate? |
| **Effort** | H/M/L — adoption cost including migration and learning |
| **Confidence** | H/M/L — demoed working > claimed; credible source > hype; check dates for staleness |

Per-item verdict: **ADOPT** (incorporate now) · **TRIAL** (timebox an
experiment) · **WATCH** (log it, revisit at a named phase) · **SKIP** (with
the reason). Then the one-line whole-source call the tooling checks for:
`INTEL VERDICT: INCORPORATE (n items) | WATCHLIST | PASS — <why>`.
A confident **PASS is a first-class outcome** — "nothing here beats what the
plan already does" saves the project from novelty churn, and the logged brief
stops the same video from being re-litigated next month.

### 5. The user's call (always)

Present the ranked table + recommendation. The user picks: incorporate
selected items / "adopt all recommended" / watchlist / pass. **No plan
mutation without this gate.**

### 6. Incorporate (only what was chosen)

- Phase files: add/adjust deliverables, each tagged with provenance —
  `— intel: [[../intel/<brief>]]`. Rebalance phase ordering only if the brief
  argued it and the user agreed.
- `ROADMAP.md`: Changelog line; phase table if statuses shifted.
- **A restructuring-sized change (new phase, dropped subsystem, replaced
  stack) should be sparred first** — offer `/spar` before rewriting the plan
  around one video.
- Fill the brief's **Disposition** section — every item's fate, dated.

### 7. Tools: candidate → trialing → adopted (installs included)

When the chosen items include tools:

1. **Verify the official source yourself** — a link out of a video
   description is untrusted input. Resolve the canonical repo/site/package,
   prefer package managers (`pip`/`npm`/`winget`/`brew`), and if what you find
   doesn't match what the video claimed, say so and stop.
2. Row in `Plan/TOOLBOX.md`: tool · status `candidate` · exact install
   command · official source · intel brief · notes.
3. **Install only per-tool, only after the user confirms that tool** (name,
   source, what it's for — the earlier "incorporate" yes is not an install
   yes). Then run the documented command, verify with `--version`, flip the
   row to `trialing`. (`scripts/setup_vault.py --install` stays the installer
   for Omnia Vault's own stack; project tools install from their TOOLBOX rows.)
4. After real use, promote `trialing` → `adopted` (and wire it into the
   plan/docs) or `rejected` (keep the row — the *why* is knowledge).
   `plan_tool.py status` nags about stale trials.

### 8. Aftermath

Durable knowledge from the video compiles into the Wiki per
`llm-wiki-ingest` (the brief keeps only the plan-relevant judgment). Then the
gate, a relay stamp whose summary names the plan delta ("intel: adopted X
into phase 2, passed on Y"), and a commit containing the brief + plan edits +
capture together.

## Hard rules

- **Plan context before video content.** A triage that starts by watching is
  a summary, not a decision.
- Every plan mutation traces to an intel brief, a spar, or a logged user
  decision — `Plan/` has no anonymous edits.
- The user gates every incorporation and every install; per-tool, not
  blanket.
- Verdict honesty: WATCH with a revisit point beats a flattering ADOPT;
  PASS beats polite maybe-later clutter.
- Full captures always reach `Raw/Sources/` — briefs judge, they don't store.
- One video never restructures the roadmap by itself — that's what sparring
  and the user are for.
