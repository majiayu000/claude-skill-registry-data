---
name: eos-insights
description: Periodic cross-corpus reflection on EmptyOS development — where the system is heading. Aggregates a 30-day (or custom) window of the ARTIFACT corpus — git log, devlogs and _next/ track briefs, the app/plugin inventory, dark flags, the deferred-feature readiness recheck, trace-miner error clusters, KB-gap output — into a standalone AI-authored report. Surfaces build velocity per track, growing vs dormant apps, flags built-but-never-enabled, top friction signatures, and candidate rules / skills / lessons, as PROPOSALS only. Use when the user says "eos insights", "what is the system becoming", "dev trends", "what have I been building", "system reflection", or "where is EmptyOS drifting". NOT Claude Code's own /insights (that reads conversation history; this reads artifacts), NOT one session's log (use eos-session-wrapup), and NOT a point-in-time code-health scan (use eos-architecture-review, eos-bug-audit, eos-kb-audit or eos-simplify — this synthesises trends over their outputs).
---

# EmptyOS Insights

A "knowledgeable engineering manager reading the whole project" report. Reflect on a window of EmptyOS development across every artifact source, surface the trends no single audit sees, and write a durable report — proposing, never auto-applying. This is the EmptyOS self-audit-loop (`.claude/rules/self-audit-loops.md`) turned into a periodic synthesis, and the system-side analogue of Claude Code's `/insights`.

## When to use

- User says "eos insights", "what is the system becoming", "dev trends", "what have I been building", "system reflection", "where is EmptyOS drifting"
- Monthly / milestone step-back over EmptyOS development

Do **NOT** use this for:
- One dev session's housekeeping → `/eos-session-wrapup`.
- A point-in-time code-health scan → `/eos-architecture-review`, `/eos-bug-audit`, `/eos-kb-audit`, `/eos-simplify`.
- How *you* use Claude Code (conversation history, tool usage) → that's Claude Code's built-in `/insights`, a different corpus.
- Personal life → `/eos-life-insights`.

The line: this skill is the **aggregator** the codebase was missing — it reads *across* sources and *over time*, and it reads the *outputs* of `trace-miner` / `kb-gap-miner` rather than re-mining.

## Pre-flight

Mostly read-only static + git + scripts. A couple of enrichments hit the daemon — only then:

- **Daemon up** (optional, for `eos app list` proxy / miner endpoints) — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9000/` → `200`. If down, read manifests + script output directly; never restart the daemon (`.claude/rules/daemon-handling.md`).
- **SDK/script shell is safe** — `scripts/check_dark_flags.py`, `scripts/kb_claim_audit.py`, `scripts/kb_link_audit.py` are pure file I/O (no kernel boot), safe to run while the daemon is up.
- **Vault root** — `[notes] path` in `emptyos.toml` (read it from there; don't hardcode the path).

## Vocabulary

- **Window** — default last 30 days from today; custom on request.
- **Artifact corpus** — git history + devlog notes + manifests + dark-flag state + miner output + KB. NOT the conversation history.
- **Track** — a work lane named in `{vault}/10_Projects/emptyos/log/_next/_index.md`, each with a `_next/<track>.md` on-deck brief, last-touched date.
- **Report path** — `{vault}/30_Resources/EmptyOS/insights/outputs/YYYY-MM-DD-eos.md` (today). `outputs/` ⇒ AI-authored (`.claude/rules/authorship-boundary.md`); set `author: ai` explicitly.

## Process

### Step 0 — Read the prior scorecard (the loop closes here)

Before gathering anything, read what the *last* run proposed:

```bash
python scripts/insights_ledger.py scorecard eos
```

A proposal **recurring** across reports without being acted on is a stronger signal than a fresh one. Carry still-relevant ones forward, note any you can see were acted on, drop the stale. This is what makes the skill a *loop*, not a one-shot. `(no prior ledger …)` on the first run is fine.

### Step 1 — Deep-research loop (read, don't just count)

Apply the **deep-research method** (`.claude/rules/deep-research.md`) to the EmptyOS artifact corpus — the four passes below are that method's moves 2–5 (the v1 failure mode was **tabulating without reading**; statistics dressed as insight):

**1a — First pass (breadth).** The cheap inventory:
- git: `git log --since="30 days ago" --pretty=format:"%h %ad %s" --date=short`; `git log --since="30 days ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -30` (hot files); commit-type split; per-`apps/<group>`/`emptyos/`/`engines/` churn.
- `{vault}/10_Projects/emptyos/log/_next/_index.md` (tracks + last-touched).
- `apps/**/manifest.toml` + `plugins/*/manifest.toml` crossed with git churn (dormant).
- `python scripts/check_dark_flags.py` (dark-flag inventory; STALE = dark >90d).
- `docs/DEFERRED-WORK.md` — the deferred-feature registry: each `deferred` row's trigger + `Added` age (the "is it ready to build/deploy yet?" recheck input).
- `trace-miner` top issues by score (`data/apps/trace-miner/issues.json`) — aggregate, do NOT re-mine.
- `python scripts/kb_claim_audit.py` + `kb_link_audit.py` (+ kb-gap-miner output).
- `python scripts/check_gap_freshness.py` + `python scripts/insights_ledger.py scorecard gap` — market gap-analysis registry coverage (stale/unanalyzed apps, gaps recurring unaddressed → surface as candidates for a `/eos-app-gap-analysis` run or promotion).

**1b — Gap pick.** Name the **3-5 load-bearing or uncertain claims** — the ones a decision hangs on ("is `engineering-pilot` actually stalled?", "is the boot-import failure real and *current*?", "are the dormant tracks dead or just parked?"). These, not the easy counts, are what to deepen.

**1c — Deep-read (the part v1 skipped).** For each gap claim, READ the primary sources — don't infer from counts:
- the actual *body* of ~5 relevant `{vault}/10_Projects/emptyos/log/YYYY-MM-DD.md` session logs;
- the top friction **samples** in `data/apps/trace-miner/issues.json` + the matching lines in `data/daemon.err.log` (confirm a friction is real-and-CURRENT, not a stale artifact);
- the actual feature code / manifest behind the oldest dark-flags before calling one "ship" or "cut".
- for each `deferred` row in `docs/DEFERRED-WORK.md`, a cheap readiness check (judgment, not regex — triggers are prose): did a consumer/caller appear (grep), does the named engine/app now exist, did a blocking dependency land, or has it aged past `Added` while the need recurs in friction / KB-gap signals?
**Triangulate** — every headline claim rests on ≥2 independent sources (a stall = quiet git churn AND a parked devlog note, not one alone).

**1d — Adversarial pass (kill overconfidence).** Before writing, try to **refute** each top finding ("the dormant track is dead, not parked — prove it isn't"; "the healthy feat:fix ratio hides revert churn — check"). Test each heuristic against 3 known-healthy cases (`.claude/rules/audits.md`). Drop or downgrade anything that doesn't survive; a claim you couldn't verify is graded `inferred`, never asserted as fact.

### Step 2 — Synthesize the report

**Forecast, don't just describe.** Thoroughness = a quantitative spine + narrative, not prose alone (the Claude `/insights` standard).

**Quantitative spine (required):**
- A `## Stats` section right after Headline — a 2-col `Metric | Value` table (commits, files changed, lines +/−, tests touched, net-new KB, dark-flags soaking/ON). The renderer turns it into the stat-tile row.
- **≥3 chartable distributions** — emit each as a 2-col `Label | Value` table (the renderer auto-draws a bar chart): commit-type split (feat/fix/refactor…), per-area churn, dark-flag status, friction-kind. Slice the corpus several ways.
- **Copyable artifacts** — for each rule/skill/KB proposal, put the exact paste-ready text in a fenced ``` block (the renderer adds a copy button).

Sections (markdown `##` — keep these names so the renderer themes them right):

1. **Headline** — one paragraph: "what the system is becoming" (becomes the hero box). Lead with the *trajectory* finding, not the biggest number.
2. **Trend (vs prior window)** — this 30d vs the prior 30d (commits, dormant count, dark-flag backlog) and a read of the *previous* insights report's deltas (find it: prior `…-eos.md` in the outputs dir). Trend, not snapshot — this fixes the v1 "still photo" gap.
3. **Build velocity per track** — lanes that moved/quieted, last-touched dates. Include a `Label | Value` table (e.g. area → touches) so the renderer draws a bar chart.
4. **Trajectory vs goals** — the strategic layer v1 skipped: does where effort *actually went* match stated priorities (engineering-pilot / monetization, energy×software, NIW — per the project/career memories)? Surface **divergence** (e.g. heavy self-tooling investment while a revenue-relevant track went dormant). Wheel-for-the-codebase: over-feeding occupational/intellectual self-improvement vs shipping/financial.
5. **Growing vs dormant** — gaining vs losing attention; *parked* vs *truly dead* (decided by the 1c deep-read, not the count alone).
6. **Dark-flags never flipped on** — built-but-unadopted, STALE called out, each a "ship it / cut it / still cooking?" prompt.
7. **Top friction signatures** — ranked AFTER flooring noise (auth-probe etc.); code-bug vs external; each confirmed real-and-current from the 1c read.
8. **KB growth + gaps** — net new, broken-link/claim count, top unanswered clusters.
9. **Deferred-feature readiness (proposals)** — walk `docs/DEFERRED-WORK.md`'s `deferred` rows; for any whose trigger now shows signs of being met (per the 1c readiness check), surface a *Candidate to promote: `<feature>` — trigger may be met because `<signal>`*. **PROPOSAL ONLY** — never flip a row's Status or build/enable anything; the human edits the row (`deferred → triggered`). Omit the section if nothing looks ready.
10. **Suggested next steps (proposals)** — candidate **CLAUDE.md rules / skills / KB lessons**, each with a rationale. **PROPOSALS ONLY.**

**Evidence grading** — tag every non-trivial finding with how it was derived: `[counted]` (a tally), `[read-verified]` (confirmed against a primary source in 1c), `[inferred]` (a judgment that survived 1d but isn't directly evidenced). The grade is the honesty signal that separates this from v1's statistics-dressed-as-insight.

### Step 3 — Write the report

Block-style YAML tags:

```markdown
---
author: ai
tags:
  - insights
lens: eos
period: 30d
as_of: YYYY-MM-DD
lifecycle: snapshot
---
```

Write to `{vault}/30_Resources/EmptyOS/insights/outputs/YYYY-MM-DD-eos.md`.

Section-heading discipline (the renderer themes cards by keyword in the `##` title): a leading `## Headline` section becomes the amber hero box; titles containing *friction/error/bug* → red, *dark-flag/dormant/stale/backlog* → amber, *proposal/next step/suggested* → blue, *kb/velocity/growing/win/health* → green, else neutral. Keep the section names in this skill (Headline, Build velocity per track, Growing vs dormant, Dark-flags…, Top friction…, KB growth…, Suggested next steps) so the themes land right.

### Step 3b — Render the HTML view

```bash
python scripts/render_insights_html.py "{vault}/30_Resources/EmptyOS/insights/outputs/YYYY-MM-DD-eos.md"
```

This writes a styled `…-eos.html` sibling (the Claude-Code-`/insights`-style report: hero + TOC + stat tiles + themed cards + tables). The markdown stays the vault-native source of truth; the HTML is a generated view. `scripts/render_insights_html.py` is pure stdlib (no kernel boot) — safe to run anytime. Add `--open` to pop it in the browser. Give the user the `file:///…/YYYY-MM-DD-eos.html` URL.

### Step 4 — Feedback-loop posture (load-bearing)

eos-insights **surfaces** rule/skill/KB proposals; it does **NOT** auto-write rules, skills, or KB notes. The human decides whether a later session acts on any of them (`.claude/rules/proposed-action.md`, `.claude/rules/self-audit-loops.md`, "with you, not for you"). This is the EmptyOS-correct version of the [yahav10/claude-insights] "insights → auto-generate skills/rules" loop — propose, don't auto-apply. If the user picks a proposal, that's a separate explicit action in a follow-up turn.

**Record the proposals** so the next run's Step-0 scorecard can grade them:

```bash
python scripts/insights_ledger.py record eos --from "{vault}/30_Resources/EmptyOS/insights/outputs/YYYY-MM-DD-eos.md"
```

This closes the loop. State lives under `data/apps/insights/` (telemetry, gitignored), never the vault.

### Step 5 — Report to chat

1. Top 3-4 trends (a velocity line, the standout dormant area, the most painful friction signature).
2. The report paths — both the `.md` and the `file:///…/YYYY-MM-DD-eos.html` view.
3. Which 1-2 proposals look highest-leverage, and the one EmptyOS gap this run bumped into (e.g. no machine-readable "track last-touched", trace-miner output not queryable offline) — fed forward per the self-audit-loop.

## Deep-research mode (comprehensive run)

For a thorough run — or when the user asks to "go deep" / "comprehensive" — execute the 1a–1d loop as a multi-agent **Workflow** instead of serially:

- **Phase 1** parallel deep-readers (one each: git, devlog bodies, dark-flags+code, friction+`daemon.err.log`, KB) → structured findings.
- **Phase 2** dedup by `sig_hash` (`emptyos/sdk/miner_state.py`).
- **Phase 3** independent **adversarial verifiers** that try to refute each top finding (majority-refute → drop).
- **Phase 4** synthesize + write report + ledger-record.

This is `emptyos/sdk/deep_loop.py`'s gap→deepen→merge realized as fan-out. The Workflow tool needs **explicit user opt-in** (it spawns many agents) — don't launch it unprompted; the serial 1a–1d loop is the default.

**Do NOT use the `explore` app for insights.** It is web-only (`ask_web` over DuckDuckGo/arxiv/etc.) — the wrong corpus. Insights analyzes the codebase and vault; asking the web "why did velocity drop" hallucinates. The deep-research engine here is the multi-agent Workflow over *internal* sources, not `explore`.

## Cross-references

- `.claude/skills/eos-life-insights/SKILL.md` — the personal-vault sibling.
- `scripts/insights_ledger.py` — the prediction ledger (Step 0 scorecard + Step 4 record).
- `emptyos/sdk/deep_loop.py` / `emptyos/sdk/miner_state.py` — deepen pattern + dedup/score primitives.
- `.claude/skills/eos-session-wrapup/SKILL.md` — single-session log; eos-insights aggregates over many.
- `.claude/rules/self-audit-loops.md` — the umbrella pattern (turn EmptyOS's tools on EmptyOS); this is its periodic-synthesis instance.
- `.claude/rules/proposed-action.md` — propose, don't auto-apply (the Step 4 rule).
- `apps/extension/dev/trace-miner/` + `apps/extension/dev/kb-gap-miner/` — friction + KB-gap outputs aggregated here.
- `scripts/check_dark_flags.py`, `scripts/kb_claim_audit.py`, `scripts/kb_link_audit.py` — pure inputs (safe to shell).
- `docs/DEFERRED-WORK.md` — the deferred-feature registry; the §9 readiness recheck reads it and proposes promotions (the periodic "has a trigger fired?" pass lives here).
- `{vault}/10_Projects/emptyos/log/_next/_index.md` — track index + last-touched.
- `project_feature_pipeline_flag_default_dark` (memory) — why a long-dark flag is a signal.
- `.claude/rules/authorship-boundary.md` — `author: ai` + `outputs/`.

## When NOT to use

- One session → `/eos-session-wrapup`.
- A focused code-quality pass → the one-off audit skills.
- The window has almost no commits/devlog (quiet period) → say so and skip; thin data makes a step-back report misleading (the `/insights` "skews on intensive sessions / variable between runs" failure mode).

[yahav10/claude-insights]: https://github.com/yahav10/claude-insights
