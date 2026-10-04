---
description: "Map an unfamiliar repository (or area within one) so you know where to start."
---

# /recon

Map an unfamiliar repository (or area within one) so you know where to start. Output is a **descriptive lay-of-the-land**, not a critique. Use this *before* `/tackle-issues`, `/bug-hunt`, or `/project-audit` — it produces the orientation those skills assume.

Unlike `/project-audit` (rates the project) or `/swarm-audit` (audits a specific document), `/recon` answers **"what is this repo and where do I start?"** in a single short sweep.

## Arguments

- `$ARGUMENTS` - Optional configuration. Space-separated tokens:
  - First positional: focus area (file path, directory, or quoted topic). Defaults to whole repo.
  - `scouts=N` — Number of scout agents (default: 3, min: 2, max: 5)
  - `output=DIR` — Output directory (default: `docs/recon/`). Pass `output=-` to print to stdout only.
  - `depth=quick|standard|deep` — How thoroughly scouts read (default: `standard`)

Examples:
```
/recon
/recon src/auth
/recon "the websocket protocol" scouts=4
/recon scouts=2 depth=quick output=-
/recon src/payments scouts=5 depth=deep
```

## Instructions

### 1. Parse Arguments

```
TARGET     = first positional (path, dir, or quoted topic) — default: repo root
SCOUT_COUNT = extract from scouts=N (default: 3, clamp 2-5)
OUTPUT_DIR  = extract from output=DIR (default: docs/recon/, "-" means stdout)
DEPTH       = extract from depth=X (default: standard)
```

### 2. Quick Profile Scan

Before launching scouts, do a 30-second sweep yourself so each scout starts with a shared baseline:

- Read `README.md`, `CLAUDE.md` (if present), `package.json` / `Cargo.toml` / `go.mod` / equivalent
- `ls` the root and the target directory (if not root)
- Note the primary language(s), framework(s), and any obvious conventions

Build a short **shared briefing** (5-10 lines max) that every scout will receive. Do NOT do exhaustive exploration here — the scouts will do that. Just enough to coordinate.

### 3. Select Scout Panel

Always include the first two. Add more from the extended roster based on the target.

#### Core Scouts (always included)

| Scout | Nickname | Lens | Personality |
|-------|----------|------|-------------|
| Mapmaker | "Cartographer" | Tech stack, entry points, build system, directory layout, top-level architecture | Methodical surveyor who answers "what is this and how is it organized?" Reads package files, configs, and top-level directory structure. Identifies the 3-5 most important files. |
| Flow Tracer | "Pathfinder" | End-to-end traces of 2-3 major flows (request handling, auth, primary user action) | Detective who follows the wire from input to output. Picks the most important flows and walks them step-by-step, naming each handler and transformation. |

#### Extended Roster (pick based on target)

| Scout | Nickname | Lens | When to Include |
|-------|----------|------|-----------------|
| Risk Spotter | "Bloodhound" | High-churn files (git log), large/complex files, code smell concentrations — where bugs are most likely to live | Always useful unless `depth=quick`. Surfaces the hotspots that feed into `/bug-hunt` later. |
| Convention Reader | "Scribe" | Code style, test conventions, CI setup, attribution policies in CLAUDE.md, commit-message format, branching rules | Include when the repo will be edited by future agents. Captures the implicit rules so they aren't violated. |
| Domain Sniffer | "Native" | Domain vocabulary, key data models, business logic location | Include when target is a feature area rather than the whole repo, or when domain terminology is heavy. |
| Template Critic | "Auditor" | Generic template structure, `{{CUSTOMIZE: ...}}` marker placement and density across `generic/*.md` files | Reconning `generic/`, `deploy.sh`, or `sync.sh` |

#### Selection Algorithm

```
1. Start with the 2 core scouts
2. If SCOUT_COUNT >= 3 and DEPTH != quick: add Bloodhound
3. If SCOUT_COUNT >= 4: add Scribe
4. If SCOUT_COUNT >= 5 OR target is a specific area: add Native
5. Clamp to SCOUT_COUNT
```

State the selected panel to the user **before** launching.

### 4. Launch Scouts

Launch ALL scouts in parallel using the Agent tool. Each scout receives:

1. The shared briefing from step 2
2. The TARGET and DEPTH
3. Their persona, lens, and a strict output template (below)
4. Instructions to read actual files, not guess from names

**Scout prompt template:**

```
You are "{NICKNAME}" — {PERSONALITY}

You are reconning the following target so a future engineer (or agent) can start work without re-doing your exploration:

## Target
{TARGET}

## Shared Briefing (already known)
{BRIEFING}

## Your Scope: {LENS}

You MUST read actual files. Do not infer from filenames alone.

## Output (use these exact sections)

### One-Line Summary
A single sentence answering: from your lens, what is the most important thing to know about this target?

### Key Findings (5-10 bullets)
Each bullet:
- One concise statement (what you found)
- File:line reference where applicable
- Why it matters in one phrase

If a scout has more than 10 genuinely-distinct findings, return the strongest 10 and note the surplus under Open Questions. Caps are soft — quality beats count, but artificial trimming hurts the synthesis step.

### Worth Reading First
2-4 files a new contributor should open before touching anything, with one-line justification each.

### Open Questions
Things you could not determine from the code — gaps that need a human or further investigation.

## Rules
- Be descriptive, not evaluative. Do NOT rate, grade, or recommend fixes. This is recon, not audit.
- Be specific. "It uses some kind of router" is useless. "src/router.ts:24 — express router mounted at /api/v1, registers 12 routes" is useful.
- Stay in your lens. If you stray into other scouts' territory, you waste tokens.
- Depth = {DEPTH}: quick = ~5 files read; standard = ~15-25 (or ~10-15 for small/single-package repos); deep = ~30-50 across modules. For Pathfinder specifically: a single major flow in a god-class can consume 10+ reads on its own — adjust the file count budget toward flow completeness rather than file count. If you hit budget mid-flow, finish the current step then list the remaining trace under Open Questions rather than producing partial steps.
```

**Run scouts as foreground Agent calls.** If SCOUT_COUNT > 4, batch: first 4 in parallel, then the rest.

### 5. Synthesize the Map

After all scouts return, write **one map document** that combines them into a coherent orientation guide. Do NOT just concatenate scout outputs — synthesize.

#### Required Sections

**a. Header**
```markdown
# Recon: {TARGET}

**Date:** {today}
**Scouts:** {nicknames, comma-separated}
**Depth:** {DEPTH}
```

**b. TL;DR (3-5 lines)**
The single paragraph a new contributor reads to know "what is this?"

**c. Tech Stack**
| Layer | Choice | Where to find it |
|---|---|---|
| Language | TypeScript | package.json |
| Framework | Next.js 14 | next.config.js |
| ... | ... | ... |

**d. Entry Points**
Table of the 3-7 files that matter most, in reading order. Pulled from Cartographer + Pathfinder.

| # | File | Why |
|---|---|---|
| 1 | src/index.ts | Main entry; bootstraps the app |
| ... | ... | ... |

**e. Major Flows**
Walkthroughs of 2-3 important flows (from Pathfinder). For each:
- **Flow name**
- 4-12 numbered steps: `file:line — what happens` (long flows in god-classes legitimately need more steps; don't truncate a real flow to hit the lower bound)
- Pitfalls or non-obvious behavior worth knowing

**f. Hotspots**
(Only if Bloodhound was on the panel.) Risk-ranked table of files most likely to contain bugs or change frequently.

| Risk | File | Signal |
|---|---|---|
| High | src/payments/charge.ts | 47 commits in last 90 days; 412 LOC; no tests |
| ... | ... | ... |

**g. Conventions Cheat-Sheet**
(Only if Scribe was on the panel.) Bullet list of project conventions a future agent must follow: attribution policy, commit format, test location, lint rules, etc.

**h. Open Questions**
Deduplicated list of things scouts could not determine. Each item is a question someone could answer with a follow-up dig.

**i. Where to Go Next**
Three concrete suggestions, e.g.:
- "Run `/bug-hunt src/payments` — Hotspots flagged this as the highest-risk module."
- "Read entry points 1-3 before any code change."
- "Resolve open question #2 before touching auth."

### 6. Write or Print Output

If `output=-`, print the synthesized map to stdout. Otherwise write to:

```
${OUTPUT_DIR}/<slugified-target>-<YYYYMMDD>.md
```

Create the directory if needed. Do NOT also write individual scout reports — recon is intentionally lightweight. Scout outputs live only in your synthesis.

### 7. Commit (only if files were written)

**Stage explicit paths.** `git status --short` first, then `git add` the synthesis file you just
wrote, **by name**. Never `git add -A`, `git add .`, `git add -u`, `git add <dir>/`, or
`git commit -a`. A trailing-slash directory add is a bulk add: the working copy is shared with
concurrent sessions, so `${OUTPUT_DIR}/` may also hold a stale report from another run or a file
that is not yours. `-u` is not the safe one: it restages every *tracked* file whose worktree copy
differs, including files a clean/smudge filter rewrote without you touching them — that is how
`git add -u` turned a tracked 21KB `.docx` into a git-lfs pointer and committed it as an edit.

```bash
git status --short "${OUTPUT_DIR}"
git add "${OUTPUT_DIR}/<slugified-target>-<YYYYMMDD>.md"   # name the file you wrote
git commit -m "docs: recon of <target> (<N> scouts)"
```

Do NOT push. Do NOT commit if `output=-`.

### 8. Report to User

Output a concise summary:

```markdown
## Recon Complete: {target}

**Scouts:** {nicknames}
**Output:** {path or "stdout"}

### TL;DR
{the 3-5 line summary from the map}

### Top 3 Things to Read First
1. ...
2. ...
3. ...

### Recommended Next Step
{single concrete next action, usually from "Where to Go Next"}
```

## Configuration

### Depth Levels

| Level | Files Read per Scout | Use When |
|:------|:--------------------:|:---------|
| quick | ~5 | Just need a quick orientation; large repo, short on time |
| standard | ~15-25 (large/monorepo) or ~10-15 (small/single-package) | Default; entering a new repo or feature area |
| deep | ~30-50 across modules | Preparing for a major change; will run `/project-audit` next |

**Budget guidance:** these are per-scout file-read budgets, not hard caps. Pathfinder in particular may legitimately spend 10+ reads on a single major flow when the codebase has god-classes (e.g., a 6000-line server room). When budget runs out mid-flow, scouts should finish the current step and list the remaining trace under Open Questions rather than producing partial step descriptions.

### Scout Behavior Rules

- Scouts MUST be descriptive, not evaluative. No ratings. No "this is bad." That is what `/project-audit` and `/bug-hunt` are for.
- Scouts MUST cite `file:line` for any concrete claim.
- Scouts MUST stay in their lens — if Cartographer starts tracing flows, you'll get duplicate work.
- Scouts SHOULD list open questions rather than guess. Better to flag a gap than fabricate.
- For monorepos, Cartographer should produce a per-package summary, not just a root summary.

## Why Not Use /project-audit Instead?

| Need | Use |
|---|---|
| "What is this repo?" | `/recon` |
| "Where do I start?" | `/recon` |
| "Is this codebase healthy?" | `/project-audit` |
| "What should we ship next?" | `/project-audit` |
| "Find bugs to file as issues" | `/bug-hunt` |
| "Audit this RFC" | `/swarm-audit` |
| "Review this PR" | `/agentic-audit` |

`/recon` is the orientation layer. The others assume orientation already exists.

## Examples

```
/recon                                  # whole repo, 3 scouts, standard depth
/recon src/auth                         # focus on auth module
/recon "the websocket protocol" scouts=4 depth=deep
/recon scouts=2 depth=quick output=-    # print-only quick sweep
/recon . scouts=5                       # full panel including Native + Scribe
/recon packages/server scouts=4         # monorepo subpackage with extra scout for size
```
