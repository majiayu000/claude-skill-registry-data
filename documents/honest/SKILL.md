---
name: honest
description: Produce an honest, defensible ground-truth read of the current repo — how mature the codebase really is, how far along each feature actually is, and what can be safely claimed about it externally. Reads CHANGELOG, architecture/technical docs, and recent git history; never modifies the repo. Offers an Express (10–15 min) or Deep (30–40 min) scan. Trigger when the user says "baseline", "where do we actually stand", "what's the real state of this repo", "honest assessment of the codebase", "maturity assessment", "ground truth", "what's real vs aspirational here", "I inherited this repo", "assess the feature list", or "what can we honestly say about this" — and proactively before the user describes project status to a stakeholder, board, or sales without having verified it first.
---

# Baseline

Establish the honest current state of a project, in plain language, with every claim traceable to evidence. A baseline answers one question for two different readers at once: *where does this actually stand right now — and what can we safely say about it?*

The deliverable is a single Markdown file with two firewalled halves: a **plain-language technical status** (for a PM or an exec) and a **defensible positioning section** (the safe marketing spin). Honesty is the whole point — an inflated baseline is worse than no baseline, because it gets repeated in a sales call or a board deck where being wrong has consequences.

## How this differs from the sibling skills

- **baseline** (orientation) — "Where does this project actually stand, in ground truth?" Run once on entering or re-entering a repo, or before describing status externally.
- **snapshot** (session re-entry) — "Where was I when I stopped?" Saves one working session so you can resume it.
- **take-a-step-back / blast-radius / bottom-line** (decision moments) — challenge, size, or compress a specific choice.

Baseline is upstream of all of them: it's the map you draw before deciding anything.

## Two readers, one document

The output serves a human and a machine simultaneously, so its shape is deliberate:

- A **PM / exec** reads the prose: the bottom line, the maturity call, what's solid, what's thin.
- A **downstream LLM** reads the front-matter and the status table to build on the project without re-deriving its state.

Keep both honest by keeping them separate. Technical status and positioning never blur into each other — see the firewall rule below.

## The maturity ladder (least jargon possible)

Rate the codebase overall, and each material feature, on this five-rung scale. Use the plain word as the label; avoid "MVP", "production-grade", "TRL", and similar.

| Rating | What it means in plain words |
|---|---|
| **Just an idea** | Described somewhere (README, docs, a ticket) but no working code backs it. |
| **Partly built** | Code exists but is incomplete, not wired up, or not reachable by a user. |
| **Works** | Does its job in normal use. Thin or no tests; edge cases unproven. |
| **Solid** | Handles errors and edge cases, has tests, and is in real use. |
| **Proven** | Battle-tested in production over time — stable, monitored, depended on. |

The overall rating is **not** an average. A product is only as mature as its weakest load-bearing feature: if auth is "Partly built", the product is not "Solid" no matter how polished the dashboard is. Say so explicitly.

## Evidence grade (so the rating itself is defensible)

The maturity word is the claim; the evidence grade is how much to trust it. Tag every rating with one — this reuses the same FACT / PATTERN / HYPOTHESIS vocabulary as the finding schema, so it stays consistent across the toolchain.

- **Confirmed (FACT)** — directly observed. The test passed, the code path exists and is exercised, the CHANGELOG entry has a matching commit.
- **Likely (PATTERN)** — multiple indirect signals agree, but nothing was run or directly verified. Recent commits, sensible file structure, corroborating docs.
- **Unverified (HYPOTHESIS)** — claimed or inferred only. README says it exists but no code was found; tests couldn't be run; signal is ambiguous.

This grade is what makes the positioning section safe. **The spin may only draw on Confirmed and Likely features. Anything Unverified goes on the "Don't say yet" list — never into a claim.**

## Depth setting

Ask the operator which scan they want before starting (or honor it if they already said). Be honest about what each can and can't conclude.

### Express scan — ~10–15 min, read-only, no code executed
Inspects:
- `README`, `CHANGELOG`, and any `docs/` or architecture/technical files
- Dependency manifest (`package.json`, `pyproject.toml`, `go.mod`, etc.) and lockfile age
- Directory / module structure
- Recent git history: `git log` for recency, authorship spread, and churn
- Test **presence** (do test files/dirs exist?) — not test results

Ceiling: ratings are mostly **Likely** and **Unverified**. Express can tell you what *appears* to exist; it cannot confirm anything *works*. Say this in the output.

### Deep scan — ~30–40 min, read-only by default
Everything Express does, plus:
- Read the key source files behind each claimed feature (stated-vs-evidenced check)
- Census of `TODO` / `FIXME` / `HACK` and obvious dead/orphaned code
- Dependency staleness and known-deprecated packages
- Rough test coverage of the load-bearing paths
- **Optionally run the test suite or build — but only after asking.** Executing has side effects (DB migrations, network calls, slow runs); never run anything without explicit go-ahead. If declined, note that test results stayed Unverified.

Ceiling: ratings can reach **Confirmed** where something was actually read or run.

## Read-only, always

This skill never stages, commits, edits, or deletes anything. Git access is inspection only — same principle as snapshot. The single exception is *running* tests/build in Deep mode, which requires the operator's explicit yes and still writes nothing to the repo's tracked files.

## The honesty traps — explicit Don'ts

These are the ways a maturity read goes wrong. Guard against each:

- **Don't treat docs or README as evidence of maturity.** A feature described in prose with no code behind it is *Just an idea (Unverified)* — not a feature. Stated ≠ evidenced.
- **Don't read commit volume as maturity.** Heavy churn often means firefighting, not robustness. Volume is a signal about *activity*, never about *quality*.
- **Don't read recency as health, or staleness as abandonment.** A file untouched for 18 months may be stable or dead — both are *Likely/Unverified*, never asserted as fact.
- **Don't let the spin exceed the evidence grade.** "Thin test coverage" never becomes "enterprise-grade reliability." Reframe within the truth, never beyond it.
- **Don't invent market or competitor claims** in the positioning section. The repo is the only source; comparisons it can't support don't belong.
- **Don't average away a weak load-bearing feature** into a flattering overall rating.

## Output file

- File name: `HONEST.md`
- Location: project root / current working directory if one exists (Claude Code or working inside a repo). In Claude.ai with no project filesystem, write to `/mnt/user-data/outputs/HONEST.md` and present it for download.
- **Preserve history, keep the live file clean.** If `HONEST.md` already exists, rename the old one to `HONEST-<YYYY-MM-DD>.md` first, then write the fresh one. This lets the operator see maturity drift over time without bloating the file the downstream LLM reads.
- Always stamp it: timestamp, repo, branch, commit SHA, depth mode, and actual scan duration — so any reader instantly knows how fresh and how deep the read is.

## Output format

```markdown
---
baseline_version: 1
generated: <YYYY-MM-DD HH:MM local>
repo: <name or path>
branch: <branch>
commit: <short sha — first line of message>
scan_depth: express | deep
scan_duration: <minutes>
overall_maturity: <rating> (<Confirmed|Likely|Unverified>)
---

# Project Baseline — <repo>  ·  <date>  ·  <depth> scan

## 1. Bottom line
<3–4 plain sentences: what this project is, how far along it really is, and the
 single biggest gap between what's claimed and what's actually backed by code.>

## 2. Technical status (plain language)
**Overall maturity:** <rating> — <one line on why> · confidence: <grade>

### Feature status
| Feature | Maturity | Confidence | What that's based on |
|---|---|---|---|
| <feature> | Works | Likely | recent commits + endpoint exists; no tests run |
| ... | | | |

### What's solid
- <the things genuinely safe to rely on>

### What's thin or risky
- <gaps, fragile spots, load-bearing features below "Solid">

### What I could not verify
- <honesty section — anything the chosen depth couldn't confirm. Mandatory; if
  empty in a Deep scan, say so. In an Express scan this is usually substantial.>

## 3. Defensible positioning  ⚠️ NOT technical truth
> The claims below are framing for external use. Each is graded. Do not reuse them
> without their grade, and never present a "Say with care" or "Don't say yet" item
> as a confirmed capability.

**Say now** — Confirmed; safe in a sales call, deck, or audit:
- <claim> ← <feature(s) it rests on>

**Say with care** — Likely; true today but hedge the wording ("in active use",
"available in beta", "supported for core flows"):
- <claim> ← <feature(s)>

**Don't say yet** — Unverified; would not survive scrutiny. The red-flag list:
- <thing it's tempting to claim but can't currently defend>

## 4. How this baseline was built
- Depth: <express | deep> · Duration: <mins>
- Sources read: <CHANGELOG, README, docs/, manifests, git log, source files...>
- Commands run: <read-only list; tests run? yes/no/declined>
- Skipped / out of scope: <what wasn't looked at and why>
```

## Conversational framing

Open with one plain sentence before launching the scan — never drop straight into a structured dump. Match it to the stakes: a quick orientation read is light ("Let me get an honest read on where this repo actually stands — Express or Deep?"); a baseline headed for a board deck warrants naming that the spin section will be conservative on purpose. Close the same way: a sentence pointing at the one thing that most changes the picture, before the file link.

## Scaling and scope

- **Default scope** is the repo root. For a monorepo, ask whether to baseline the whole tree or one service/package, and stamp the scope in the output.
- **Express** when the operator needs orientation fast or is early in a repo. **Deep** before anything load-bearing — a stakeholder update, a go/no-go, a release claim, an acquisition or due-diligence read.
- If the repo is tiny or single-purpose, collapse the feature table into a short list — don't manufacture structure that isn't there.

## Example (abridged, Express scan)

> Here's an honest read on where this repo stands after a 12-minute Express scan — no code was run, so anything about reliability is "likely", not "confirmed".
>
> **Bottom line:** A working cross-sell engine with a polished dashboard, but the holdout-testing logic that the whole value prop rests on is only partly built. The README presents holdout testing as a shipped feature; the code shows a scaffold with a TODO where the lift calculation should be.
>
> **Overall maturity:** Partly built — Likely. (The dashboard is "Works", but the load-bearing measurement feature isn't there yet, so the product can't rate higher.)
>
> **Say now (Confirmed):** "Live cross-sell recommendations with a real-time dashboard." ← endpoints exist, dashboard renders.
> **Say with care (Likely):** "AOV-lift measurement in active development." ← scaffold present, not functional.
> **Don't say yet (Unverified):** "Proven AOV lift via holdout testing." ← the calculation isn't implemented; claiming proven lift would not survive a single technical question.
>
> The one thing that changes this picture: whether that holdout calculation is finished. Want me to run a Deep scan on just that module?

## What success looks like

The operator can hand the technical half to an engineer and the positioning half to sales, and **neither one catches the document lying.** Every maturity word traces to a grade; every external claim traces to a Confirmed or Likely feature; and the things that can't yet be defended are named plainly rather than quietly rounded up.