---
name: radar-suite
description: 'Unified entry point for the 6-skill radar family (5 companions + capstone). Routes to individual skills, runs targeted (Tier 2) or full (Tier 3) audit sequences, owns the unified ledger, and provides cross-skill operations (status, verify, ledger, link, deferred, fresh/no-fresh). Triggers: "radar suite", "full audit", "run all radars", "/radar-suite".'
version: 3.0.0  # time-bomb integration + Fresh Scan Check + Stale-Deferred Check + Link command + Verify command + impact-based ledger filtering
author: Terry Nyberg
license: Apache-2.0
inherits: radar-suite-core.md
---

# Radar Suite — Unified Entry Point

> Single command to run any radar skill or the full audit sequence.

## Quick Commands

### Tier Selection (see `radar-suite-core.md` Tier System for full spec)

| Command | Tier | Description |
|---------|------|-------------|
| `/radar-suite` | 1 | Interactive menu (default: single skill) |
| `/radar-suite [skill]` | 1 | Run specific skill (data-model, time-bomb, roundtrip, ui-path, ui-enhancer, capstone) |
| `/radar-suite --skills dmr,tbr` | 2 | Targeted: run 2-3 skills with cross-skill handoffs |
| `/radar-suite --changed` | 2 | Targeted: auto-select skills from git diff |
| `/radar-suite --changed --since YYYY-MM-DD` | 2 | Targeted: auto-select from changes since date |
| `/radar-suite --scope [path]` | 2 | Targeted: restrict audit to a directory subtree |
| `/radar-suite --full` | 3 | Full pipeline: all 6 skills + capstone + UX enhancements |
| `/radar-suite full` | 3 | Alias for `--full` (backward compatible) |

### State Flags (combine with any command above)

| Flag | Description |
|---------|-------------|
| `--fresh` | Archive prior `ledger.yaml` and `known-intentional.yaml` before this run; treat the codebase as never-before-audited. See "Fresh Scan Check" section. |
| `--no-fresh` | Skip the fresh-scan prompt; always continue with existing state. Useful for scripted/CI runs. |

### Management Commands

| Command | Description |
|---------|-------------|
| `/radar-suite status` | Show audit progress across all skills |
| `/radar-suite resume` | Resume from last checkpoint |
| `/radar-suite ledger` | View unified finding ledger with optional filters |
| `/radar-suite ledger --open` | Show open findings only |
| `/radar-suite ledger --deferred` | Show deferred findings only |
| `/radar-suite ledger --impact crash` | Filter by impact category (crash, data-loss, ux-broken, ux-degraded, polish, hygiene) |
| `/radar-suite ledger --skill [name]` | Filter by source skill |
| `/radar-suite deferred` | Generate DEFERRED.md from ledger |
| `/radar-suite verify` | Re-verify all fixed findings |
| `/radar-suite verify RS-NNN` | Re-verify a single finding |
| `/radar-suite verify --changed` | Re-verify only findings in changed files |
| `/radar-suite link RS-NNN --root-cause-of RS-NNN [RS-NNN...]` | Link findings as root cause/symptom |
| `/radar-suite link RS-NNN --duplicate-of RS-NNN` | Mark finding as duplicate |
| `/radar-suite link RS-NNN --supersedes RS-NNN` | Mark finding as superseding another |
| `/radar-suite bug-echo RS-NNN` | Manually trigger the Bug-Echo Handoff prompt for a finding (bypasses Open→Fixed gate). See Bug-Echo Handoff in `radar-suite-core.md`. |

## Available Skills

| Skill | Purpose | Est. Time |
|-------|---------|-----------|
| **data-model-radar** | Audit @Model layer for completeness, serialization, relationships | ~30-60 min |
| **time-bomb-radar** | Find deferred operations that crash on aged data | ~15-25 min |
| **roundtrip-radar** | Trace user workflows end-to-end for data safety | ~20-40 min |
| **ui-path-radar** | Find dead ends, broken promises, navigation issues | ~15-30 min |
| **ui-enhancer-radar** | Visual UI audit with design intent interview | ~20-45 min |
| **capstone-radar** | Aggregate grades, ship/no-ship decision | ~15-30 min |

### Count vocabulary used throughout this spec

To prevent ambiguity, this document uses three distinct counts:

| Term | Meaning | Skills included |
|------|---------|-----------------|
| **5 companions** | The audit skills that capstone consumes | data-model + time-bomb + roundtrip + ui-path + ui-enhancer |
| **6 skills** / **the family** | All audit + aggregation skills | 5 companions + capstone |
| **2-5 skills** (used in `--skills` validation) | Subset accepted by Tier 2 routing | Any 2-5 of the 5 companions (capstone excluded — runs after) |

Throughout the rest of this spec, references to "5 companions" or "5 skills" mean companion-only (audit skills before capstone aggregates them). References to "6 skills" mean the complete family. References to "5-skill" (without "companion") elsewhere in this document are historical drift and should read "6-skill" — see capstone-radar's matching framing.

---

## Session Setup (MANDATORY -- runs before anything else)

On EVERY `/radar-suite` invocation, check `.radar-suite/session-prefs.yaml`:

**If file exists AND has `experience_level` set:** Show stored preferences and ask `[Enter to continue] or type "change" to adjust settings.` Then proceed to Stale-Deferred Check, then Interactive Menu.

**If file does not exist OR `experience_level` is missing:** Run full setup below before presenting the menu, fix timing, or any audit work. Do NOT skip this. Do NOT jump to exploration.

### Setup Questions (single AskUserQuestion, 4 questions)

**Q1 — Experience level?**
- **Experienced (Recommended)** -- Concise, no definitions
- **Senior/Expert** -- Terse, file:line only
- **Intermediate** -- Standard terms, explain non-obvious
- **Beginner** -- Plain language, define terms

**Q2 — Table format?**
- **Full tables (Recommended)** -- 9-column Issue Rating Tables at every decision point
- **Compact tables** -- 3-column with details below
- **No tables** -- Skip rating tables entirely (findings listed as text)

**Q3 — Fix handling?**
- **Auto-fix safe items (Recommended)** -- Apply isolated, low-blast-radius fixes automatically
- **Review first** -- Present all findings, approve each wave
- **Batch mode** -- Approve all fixes in each wave at once

**Q4 — Explain what this skill does?**
- **No, let's go (Recommended)** -- Skip explanation
- **Yes, briefly** -- 3-5 sentence explanation

Store answers in `.radar-suite/session-prefs.yaml` as `experience_level`, `table_format`, `fix_mode` (3 of the 4 questions — Q4's explain toggle is a one-time per-session choice and is NOT persisted). The `fix_timing` key is added later by the Fix Timing section below (after the Interactive Menu); see § Fix Timing for its values. See `radar-suite-core.md` for experience-level output rules.

#### session-prefs.yaml schema (consolidated reference)

The full set of keys radar-suite writes to `.radar-suite/session-prefs.yaml`:

| Key | Source | Values |
|---|---|---|
| `experience_level` | Q1 above | `beginner` / `intermediate` / `experienced` / `senior` |
| `table_format` | Q2 above | `full` / `compact` / `none` |
| `fix_mode` | Q3 above | `auto` / `review` / `batch` |
| `fix_timing` | § Fix Timing below | `recommended` / `all_per_skill` / `all_after_capstone` |
| `tier` | Menu routing / `--full` / `--skills` | `1` / `2` / `3` |
| `tier_skills` | `--skills` invocation | Array of abbreviations (only when `tier: 2`) |
| `dippy_check` | `radar-suite-core.md § Environment Pre-flight` | Object with `path_has_spaces`, `dippy_installed`, `checked_on` |
| `last_skill` / `last_session` | Updated on session end | Skill name / ISO 8601 timestamp |
| `accepted_risks` | User opt-in per finding | Array of RS-NNN IDs |

### Execution Order

The invocation flow is strictly:
1. **Session Setup** (this section) -- configure or confirm preferences
2. **Write Execution Rules Memory** -- write/update the auto-generated memory (see below)
3. **Fresh Scan Check** -- offer to archive prior state and start clean
4. **Stale-Deferred Check** -- check for overdue findings
5. **Fix Timing** -- ask when fixes should be applied (fresh audits only)
6. **Interactive Menu** -- choose what to audit
7. **Skill execution** -- run the selected skill(s)

Never skip steps 1-5. Never start exploration or scanning before completing them.

### Write Execution Rules Memory (MANDATORY -- after session setup)

After session setup completes (step 1), write or update a memory file that captures the cross-cutting rules most commonly violated during long sessions. This memory survives context compression and is re-loaded from disk on every session.

**File:** Write to the project's auto-memory directory (the same location used by the `auto memory` system). The file name is `radar_suite_execution_rules.md`.

**Content (write exactly this, substituting session prefs):**

```markdown
---
name: Radar Suite execution rules
description: Auto-generated rules for radar-suite display and behavior. Re-read before every AskUserQuestion.
type: feedback
---
1. 9-column table at every decision point: #, Finding, Urgency, Risk:Fix, Risk:No Fix, ROI, Blast Radius, Fix Effort, Status. Omit Status on first display only. Include on every re-display. Skip if TABLE_FORMAT = none.
2. Finding IDs always include short_title: RS-NNN (short description), never bare RS-NNN.
3. Progress banner after every wave, phase, or commit. Never leave a blank prompt. Always follow with the rating table (per rule 1), then AskUserQuestion.
4. Recommend fixing over deferring when effort <= Medium and finding is in scope.
5. Session prefs: experience=[USER_EXPERIENCE], tables=[TABLE_FORMAT], fixes=[FIX_MODE]. Re-read .radar-suite/session-prefs.yaml if unsure.
6. Enumerate-then-verify: any domain grade must cite files read and patterns checked. "Looks clean" without grep is a failing grade for the auditor.
```

**Rules:**
- Substitute `[USER_EXPERIENCE]`, `[TABLE_FORMAT]`, `[FIX_MODE]` with actual values from session-prefs.yaml
- If the file already exists, overwrite it (prefs may have changed)
- Add an entry to MEMORY.md if not already present: `- [Radar Suite execution rules](radar_suite_execution_rules.md) -- auto-generated display and behavior rules`
- Do NOT ask the user for permission to write this file; it is part of session setup

---

## State Read Protocols (meta-skill level)

Radar-suite reads `.radar-suite/ledger.yaml` (Stale-Deferred Check, Ledger command, Verify command), `.radar-suite/known-intentional.yaml` (Fresh Scan Check), and `.radar-suite/{skill}-handoff.yaml` files (Status command, Tier 3 pipeline orchestration) but **does NOT itself scan source code or generate findings**. The Known-Intentional Suppression and Pattern Reintroduction Detection protocols from `radar-suite-core.md` apply within each invoked companion skill, not at the meta-orchestrator level.

The meta-skill's one cross-session integrity check is the **Stale-Deferred Check** below, which fires on every invocation regardless of which command follows.

The meta-skill's one state-mutation operation outside delegated skill runs is the **Fresh Scan Check** (archive `ledger.yaml` + `known-intentional.yaml`). All other state changes happen inside the delegated companion skills.

---

## Interactive Menu

On invocation without arguments, present:

```
Radar Suite — What would you like to audit?

SINGLE SKILL (Tier 1 — quick, focused)
  1. Data models     — @Model layer gaps and inconsistencies (~30-60 min)
  2. Time bombs      — Deferred operations that crash on aged data (~15-25 min)
  3. User workflows  — Data through complete user journeys (~20-40 min)
  4. Navigation paths — Dead ends and broken navigation (~15-30 min)
  5. UI polish       — Visual audit of specific views (~20-45 min)

TARGETED (Tier 2 — 2-3 skills with cross-skill handoffs)
  6. Auto-select from changes — skills chosen by git diff
  7. Pick skills              — choose 2-3 skills manually

FULL PIPELINE (Tier 3 — all skills + capstone)
  8. Full audit — all 6 skills in sequence (~2.5-4 hours)

OTHER
  9. Release readiness — Capstone only (aggregate existing findings)
  10. Resume / Status / Ledger
```

**Menu routing:**
- Options 1-5: Set `tier: 1` in session prefs, invoke the single skill directly.
- Option 6: Run `--changed` auto-selection logic (see below).
- Option 7: Ask user to pick 2-3 skills using abbreviations (dmr, tbr, rtr, upr, uer). Set `tier: 2`.
- Option 8: Set `tier: 3`, run Full Audit Sequence.
- Option 9: Invoke capstone-radar standalone (Tier 1).
- Option 10: Sub-menu for resume, status, and ledger commands.

---

## Fix Timing (MANDATORY — ask during session setup)

Before starting any audit, ask the user when fixes should be applied. Use `AskUserQuestion` with this question:

**"When should findings be fixed?"**

| Option | Description |
|--------|-------------|
| **Fix recommended after each skill (Recommended)** | After each skill completes, fix findings that are high urgency + low effort + small blast radius. Defer the rest to a post-capstone fix session. Best balance of momentum and thoroughness. |
| **Fix all after each skill** | Fix every finding before moving to the next skill. Thorough but slower — you may fix issues that capstone would deprioritize. |
| **Fix all after capstone** | Run all 5 companion skills first (data-model, time-bomb, roundtrip, ui-path, ui-enhancer) for the complete picture, then run capstone-radar to aggregate, then fix everything in one focused session using the capstone report as a punch list. Fastest audit but largest fix backlog. |

### Fix-Now Recommendation Logic

When the user selects "Fix recommended after each skill," the skill determines which findings to fix immediately vs. defer using these rules:

**Fix now** (all three must be true):
- `urgency >= HIGH`
- `fix_effort` is `trivial` or `small`
- `blast_radius <= 2 files`

**Defer to post-capstone:**
- Everything else — medium+ effort, 3+ file blast radius, or medium/low urgency
- Findings that require design decisions (multiple valid approaches)
- Findings where the full audit picture might change the recommended fix

### Post-Capstone Fix Session

After capstone-radar completes, **always present the deferred findings** as a fix backlog:

1. Read all handoff YAMLs for deferred findings
2. Present a unified table sorted by urgency, grouped by source skill
3. Ask: "Ready to fix deferred findings?" with options:
   - **Fix all now** — Work through the backlog in waves
   - **Fix critical/high only** — Skip medium/low for a later session
   - **Save for later** — Write the backlog to `Deferred.md` with ratings

This ensures **no finding is silently dropped**. Every deferred item either gets fixed or explicitly saved.

### Persist Fix Timing Choice

Save the user's choice in `.radar-suite/session-prefs.yaml` as `fix_timing: recommended | all_per_skill | all_after_capstone`. Each individual skill reads this to know whether to enter fix mode after scanning.

---

## Fresh Scan Check (MANDATORY -- runs before Stale-Deferred Check)

After session setup completes and the execution rules memory is written, but before the Stale-Deferred Check reads `.radar-suite/ledger.yaml`, offer the user the option to archive prior radar-suite state and run from a clean slate.

### When to ask

**Skip the question entirely if:**
- `.radar-suite/ledger.yaml` does not exist (this is already a fresh project — nothing to archive)
- The invocation includes the `--fresh` flag (decision already made; go straight to archiving)
- The invocation includes the `--no-fresh` flag (explicit opt-out)

**Otherwise, ask** via a single AskUserQuestion:

```
Question (header: "Fresh scan"): "Run from a clean slate? Your current ledger has [N] open findings, [M] deferred, [K] fixed, plus [P] entries in known-intentional.yaml."

Options:
- "No, keep existing state (Recommended)" — continue normally; prior findings, accepted risks, and known-intentional suppressions remain in effect
- "Yes, archive and start fresh" — move ledger.yaml + known-intentional.yaml to .radar-suite/archive/, then run as if this were a brand-new project
- "Show me what's in the ledger first" — display a summary, then re-ask
```

Populate the counts by reading the existing `ledger.yaml` and `known-intentional.yaml` if they exist. If a count is zero, omit that fragment from the question text.

### What "Yes, archive and start fresh" does

When the user opts in, perform these operations atomically before any other step proceeds:

1. **Compute timestamp:** `STAMP=$(date +%Y-%m-%d-%H%M%S)`
2. **Ensure archive directory exists:** `mkdir -p .radar-suite/archive/`
3. **Move (do not copy, do not delete) the affected files:**
   - `.radar-suite/ledger.yaml` → `.radar-suite/archive/ledger-pre-fresh-${STAMP}.yaml`
   - `.radar-suite/known-intentional.yaml` → `.radar-suite/archive/known-intentional-pre-fresh-${STAMP}.yaml`
4. **Do NOT touch:**
   - `.radar-suite/session-prefs.yaml` — user's preferences are not audit data and stay in effect
   - `.radar-suite/checkpoint.yaml` — separate concern (resume vs. fresh are different operations)
   - `.radar-suite/{skill}-handoff.yaml` — within-run pipeline files, not cross-run state. Will be overwritten naturally.
   - `.radar-suite/archive/*` — the archive itself stays untouched
5. **Confirm to the user** with a one-line banner:
   ```
   ✓ Archived prior state to .radar-suite/archive/ledger-pre-fresh-2026-04-30-061500.yaml and known-intentional-pre-fresh-2026-04-30-061500.yaml. Starting fresh.
   ```
6. **Continue to Stale-Deferred Check.** It will now find an empty ledger and skip naturally (no overdue findings to surface).

### What "Show me what's in the ledger first" does

Render a compact summary:

```
Current radar-suite state:
  Open findings:        [N]   ← will be re-derived from scratch on a fresh scan
  Deferred findings:    [M]   ← will need to be re-deferred manually
  Fixed findings:       [K]   ← reintroduction detection will be lost; fingerprints reset
  Accepted risks:       [A]   ← will need to be re-accepted
  Known-intentional:    [P]   ← will need to be re-confirmed; expect more false positives initially

Archive location on archive: .radar-suite/archive/ledger-pre-fresh-YYYY-MM-DD-HHMMSS.yaml
```

Then re-ask the original question (without the "Show me" option this time, to prevent loops).

### CLI flags

Both flags work on any invocation, regardless of which command follows:

| Flag | Effect |
|---|---|
| `/radar-suite --fresh [...]` | Skip the question. Always archive and start fresh. Useful for power users and scripted runs. |
| `/radar-suite --no-fresh [...]` | Skip the question. Always keep existing state. Useful when you want to make sure no archive happens (e.g., in a git pre-commit hook). |

If both flags are passed, `--no-fresh` wins. Log a one-line warning.

### What this does NOT do

- It does **not** delete data. `archive/` is permanent unless the user manually clears it.
- It does **not** affect other Claude Code state (auto-memory, session checkpoint, conversation history).
- It does **not** propagate retroactively. Findings already in the current conversation context but not yet written to the ledger are not affected.

### Restore path

If a user changes their mind after a fresh scan, they can restore the prior state by hand:

```bash
mv .radar-suite/archive/ledger-pre-fresh-YYYY-MM-DD-HHMMSS.yaml .radar-suite/ledger.yaml
mv .radar-suite/archive/known-intentional-pre-fresh-YYYY-MM-DD-HHMMSS.yaml .radar-suite/known-intentional.yaml
```

This is intentionally a manual operation — automating "undo a fresh scan" inside radar-suite would create a confusing two-history-streams problem. The archive is the source of truth; mv is the API.

---

## Stale-Deferred Check (v3.0 — MANDATORY on every invocation)

At every `/radar-suite` invocation (any command), read `.radar-suite/ledger.yaml` and check for deferred findings past their `review_by` date:

```
⚠️ 3 deferred findings are past their review date:
  RS-002 [CRITICAL] Cascade delete crash — review by Apr 8 (overdue 7 days)
  RS-011 [MEDIUM] DonationRecord FMV — review by Apr 10 (overdue 5 days)
  RS-019 [LOW] Spacing in SettingsView — review by Apr 12 (overdue 3 days)

Review now? [Yes / Snooze 7 days / Dismiss]
```

**On "Yes":** Present each overdue finding with options: Fix now, Re-defer (with new review date), Accept risk, Dismiss.

**On "Snooze":** Update `review_by` to today + 7 days for all overdue findings.

**On "Dismiss":** Proceed without reviewing. The check will fire again next invocation.

---

## DEFERRED.md Generation (v3.0)

`/radar-suite deferred` generates a markdown file from the ledger:

```markdown
# Deferred Findings

Auto-generated from .radar-suite/ledger.yaml. Do not edit directly.
Generated: 2026-04-08

| ID | Finding | Impact | Severity | Release Gate | Review By | Age |
|----|---------|--------|----------|-------------|-----------|-----|
| RS-002 | Cascade delete crash | crash | CRITICAL | pre-release | Apr 8 ⚠️ OVERDUE | 30d |
| RS-011 | DonationRecord FMV | data-loss | MEDIUM | post-release | Apr 10 | 28d |
| RS-019 | Spacing in SettingsView | polish | LOW | next-major | May 8 | 14d |
```

**Overdue items** are marked with ⚠️ OVERDUE.

**Age** is calculated from `discovered` date.

The file is written to the project root as `DEFERRED.md` (or `.radar-suite/DEFERRED.md` if the project root is not appropriate).

---

## Link Command (v3.0)

`/radar-suite link` creates relationships between findings in the ledger.

### Syntax

```
/radar-suite link RS-002 --root-cause-of RS-003 RS-004 RS-005
/radar-suite link RS-009 --duplicate-of RS-007
/radar-suite link RS-015 --supersedes RS-001
/radar-suite link RS-010 --symptom-of RS-002
```

### Behavior

1. Read the ledger
2. Validate that all referenced RS-NNN IDs exist
3. Create bidirectional relationships (root_cause ↔ symptom_of, duplicate_of is one-way)
4. Append history entries to all affected findings
5. Write the updated ledger

### Fix Cascade

When linking `--root-cause-of`, the system records the relationship so that when the root cause is later marked `fixed`, all symptoms automatically move to `pending_recheck`. See Finding Relationships in `radar-suite-core.md`.

---

## Verify Command (v3.0)

`/radar-suite verify` re-verifies fixed findings to catch regressions.

### How It Works

1. Read `.radar-suite/ledger.yaml`
2. Filter findings with status `fixed`
3. For each:
   - Compute current file hash (`shasum -a 256`)
   - Compare against `fixed.file_hash_at_fix`
   - If hash matches: file unchanged, skip (still fixed)
   - If hash differs: re-run `fixed.verification_pattern`
     - Pattern returns no match → confirmed still fixed (update hash)
     - Pattern matches → **regression detected** (reopen finding)

### Known-Intentional Cleanup

As part of verification, also check `.radar-suite/known-intentional.yaml` for orphaned entries:
1. For each entry, verify the `file` path still exists (glob match)
2. If the file has been deleted, flag the entry as orphaned
3. Report orphaned entries so the user can clean them up

```
Orphaned known-intentional entries:
  KI-003: Sources/Old/RemovedFile.swift — file no longer exists
  KI-007: Sources/Legacy/*.swift — no matching files

Options:
1. **Remove orphaned entries (Recommended)**
2. **Keep all** — leave for manual review
```

### Output

```
═══════════════════════════════════════════════
  RADAR SUITE VERIFY — [N] fixed findings checked
═══════════════════════════════════════════════

✓ RS-001 CSVManager.swift — still fixed (file unchanged)
✓ RS-003 BackupManager.swift — still fixed (re-verified)
✗ RS-014 PhotoManager.swift — REGRESSION DETECTED (force unwrap returned)
⚠ RS-019 SafeDeletionManager.swift — needs manual review (no grep pattern)

Summary: [N] confirmed, [N] regressions, [N] need manual review

Options:
1. **Fix regressions now (Recommended)** — address the [N] reopened findings
2. **Show regression details** — see what changed in each file
3. **Done** — exit verification
```

---

## Tier 2: Targeted Pipeline Routing

### Manual Selection (`--skills`)

When `--skills` is provided:

1. Parse comma-separated abbreviations using the table in `radar-suite-core.md` (dmr, tbr, rtr, upr, uer).
2. Validate: must be 2-5 skills. If 1, redirect to Tier 1 with a note. If all 5, auto-upgrade to Tier 3. **`--skills` accepts only the 5 companion skills**; capstone-radar is the aggregator and runs automatically at the end of Tier 3 (via `--full`) or standalone via menu option 9. Attempting to include capstone in `--skills` returns: `"capstone-radar runs after the companion skills; use --full for the complete pipeline or invoke capstone standalone via menu option 9."`
3. Set `tier: 2` and `tier_skills: [abbreviations]` in `.radar-suite/session-prefs.yaml`.
4. Execute in standard pipeline order (dmr, tbr, rtr, upr, uer) regardless of argument order.
5. Write handoff YAMLs between skills. Each skill reads handoffs from prior skills in the subset.
6. Emit pipeline-level progress banner between skills (see `radar-suite-core.md` Pipeline UX Enhancements).
7. On each skill completion, emit a per-skill mini rating table marked "PRELIMINARY".
8. Skip capstone. A partial capstone is misleading; the user can run capstone standalone later.

### Auto-Selection (`--changed`)

1. Run `git diff --name-only` against the base branch (default: `main`). If `--since YYYY-MM-DD` is provided, use `git diff --name-only HEAD@{YYYY-MM-DD}` instead.
2. Apply the auto-selection heuristic table from `radar-suite-core.md` to map changed file patterns to skill abbreviations.
3. Deduplicate the resulting skill list.
4. Route based on count:
   - **0 skills:** "No radar-relevant changes detected. Run a specific skill or full audit?"
   - **1 skill:** Run as Tier 1. Inform user: "Only [skill] is relevant to your changes."
   - **2-3 skills:** Run as Tier 2 (follow Manual Selection steps 3-8 above).
   - **4+ skills:** Suggest Tier 3: "4+ skills triggered by your changes. Run full audit? [Yes / No, run these N skills]"
5. Show the user which skills were selected and why before starting: "Changes in [file list] triggered: [skill list]."

### Scope Restriction (`--scope`)

When `--scope [path]` is provided, restrict all skill scans to files within the specified directory subtree. This narrows the audit without changing tier behavior. Can be combined with `--skills` or `--changed`.

---

## Full Audit Sequence (Tier 3)

Triggered by `/radar-suite --full`, `/radar-suite full`, or menu option 8. Sets `tier: 3` in session prefs.

Execute the 6 skills in this order:

1. **data-model-radar** -- Foundation layer, feeds model/relationship info to others
2. **time-bomb-radar** -- Uses data-model findings to check deferred operations on aged data
3. **roundtrip-radar** -- Uses data-model + time-bomb findings to focus on high-risk workflows
4. **ui-path-radar** -- Navigation audit, independent of data layer
5. **ui-enhancer-radar** -- Visual audit, runs on specific views
6. **capstone-radar** -- Aggregates all findings, produces final grade

After step 6 completes, run the **Post-Capstone Fix Session** (see § Fix Timing above for the workflow). This is a phase, not a skill — it operates on findings already discovered by steps 1-6 and is governed by the `fix_timing` preference (`recommended` / `all_per_skill` / `all_after_capstone`). Findings deferred from per-skill fixes during the audit are presented here as a unified backlog.

### Tier 3 Pipeline UX (MANDATORY)

Apply all 6 pipeline UX enhancements from `radar-suite-core.md`:

1. **Pipeline-level progress banner** at every skill transition (start and completion).
2. **Per-skill mini rating tables** on each skill completion, marked "PRELIMINARY".
3. **Audit-only statement** at pipeline start and each transition (Senior/Expert: first time only).
4. **Per-phase duration estimates** in the pipeline banner.
5. **Pre-capstone summary** emitted by capstone before its own scans (consolidated findings table from all 5 companions).
6. **Finding IDs always include short_title** in parentheses (e.g., `RS-002 (cascade delete crash)`).

**Between skills:** Write handoff YAML, emit pipeline-level progress banner, present fixes per fix timing preference, ask to continue or pause.

**On pause:** Save checkpoint so user can resume later.

---

## Status Command

Show audit progress across all skills:

```
Radar Suite Status:
Fix timing: Fix recommended after each skill

| Skill | Last Run | Findings | Fixed | Deferred |
|-------|----------|----------|-------|----------|
| data-model-radar | 2 days ago | 12 | 10 | 2 |
| time-bomb-radar | 2 days ago | 3 | 2 | 1 |
| roundtrip-radar | 2 days ago | 8 | 6 | 2 |
| ui-path-radar | not run | — | — | — |
| ui-enhancer-radar | not run | — | — | — |
| capstone-radar | not run | — | — | — |

Deferred backlog: 4 findings awaiting post-capstone fix session
Next recommended: ui-path-radar
```

---

## Ledger Command

`/radar-suite ledger` displays findings from `.radar-suite/ledger.yaml` -- the unified cross-skill finding store.

### Filters

| Flag | Description |
|------|-------------|
| `--open` | Show open findings only |
| `--deferred` | Show deferred findings only |
| `--fixed` | Show fixed findings only |
| `--accepted` | Show accepted findings only |
| `--impact [category]` | Filter by impact category: crash, data-loss, ux-broken, ux-degraded, polish, hygiene |
| `--skill [name]` | Filter by source skill (e.g., roundtrip-radar) |
| `--severity [level]` | Filter by severity: CRITICAL, HIGH, MEDIUM, LOW |

### Output Format

```
═══════════════════════════════════════════════
  RADAR SUITE LEDGER — [N] findings ([N] open, [N] fixed, [N] deferred)
  Last session: [skill] on [date]
═══════════════════════════════════════════════

CRASH RISK ([N] findings)
  RS-002 [CRITICAL] Cascade delete on archived items (time-bomb-radar) — open
  RS-014 [HIGH] Force unwrap on nil photo data (roundtrip-radar) — fixed 2026-04-10

DATA LOSS ([N] findings)
  RS-001 [HIGH] CSV export drops Room and UPC (roundtrip-radar) — open
  RS-007 [HIGH] InsuranceProfile not in backup (data-model-radar) — deferred (review by May 8)

UX BROKEN ([N] findings)
  RS-009 [HIGH] Settings > Export has no back button (ui-path-radar) — fixed 2026-04-09

POLISH ([N] findings)
  ...

Options:
1. **Filter** — apply additional filters
2. **Details [RS-NNN]** — show full finding details with history
3. **Fix [RS-NNN]** — mark a finding as fixed
4. **Defer [RS-NNN]** — defer a finding with reason and review date
5. **Done** — exit ledger view
```

### Finding Details

`/radar-suite ledger RS-001` shows full details:

```
RS-001 [HIGH] CSV export drops Room and UPC columns on import
  Status: open
  Impact: data-loss
  Source: roundtrip-radar (also flagged by: data-model-radar)
  File: Sources/Managers/CSVManager.swift:142
  Confidence: verified
  Evidence: grep confirmed importCSV reads 25 fields, exportCSV writes 27
  Discovered: 2026-04-08
  Related: RS-007, RS-011

  History:
    2026-04-08 discovered by roundtrip-radar
    2026-04-08 also flagged by data-model-radar
```

### No Ledger

If `.radar-suite/ledger.yaml` doesn't exist:

```
No finding ledger found. Run an audit skill to create one.
Recommended: /radar-suite full (run all skills) or /radar-suite data-model (start with foundation)
```

---

## Handoff Flow

Each skill writes `.radar-suite/[skill]-handoff.yaml` on completion.

Capstone-radar reads all handoffs to:
1. Aggregate findings
2. Detect cross-skill patterns
3. Produce unified grades
4. Make ship/no-ship recommendation

---

## Shared Patterns

See `radar-suite-core.md` for: Experience-Level Output Rules, Session Persistence, Checkpoint & Resume, Accepted Risks, Wave-Based Fix Presentation, Table Format, Issue Rating Tables, Unified Finding Ledger Protocol.
