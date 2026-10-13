---
name: roundtrip-radar
description: 'Per-journey code audit tracing data through complete user flows for bugs, data safety, performance, and round-trip completeness. Discovers workflows, audits each end-to-end, rolls up cross-cutting issues, and supports natural-language flow tracing. Triggers: "roundtrip audit", "trace user journey", "/roundtrip-radar".'
version: 2.1.0  # axis classification protocol + named bug-class guides (Collection Narrowing, Bridge Parity)
author: Terry Nyberg
license: Apache-2.0
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
inherits: radar-suite-core.md
---

# Roundtrip Radar

This skill audits application workflows for bugs, data-safety issues, performance
problems, and data round-trip completeness. It operates in three primary steps
plus two targeted entry points:

- **Step 0** — Discover all workflows (run once, or when workflows change)
- **Step 1** — Deep audit one workflow at a time (one prompt per workflow)
- **Step 2** — Roll-up cross-cutting patterns across all audited workflows
- **Trace** — Audit a specific user journey described in natural language (see § Trace Command)
- **Diff** — Compare findings against the previous audit's ledger entries (see § Diff Command)

## Usage

| Command | Description |
|---------|-------------|
| `/roundtrip-radar` | Start with Step 0 (discover), then prompt for Step 1 |
| `/roundtrip-radar discover` | Run Step 0 only — find all workflows |
| `/roundtrip-radar [WORKFLOW]` | Run Step 1 for a specific workflow |
| `/roundtrip-radar rollup` | Run Step 2 — cross-cutting analysis |
| `/roundtrip-radar trace "A → B → C"` | Trace a specific user flow path (see below) |
| `/roundtrip-radar diff` | Compare findings against previous audit |
| `--show-suppressed` | Show findings suppressed by known-intentional entries |
| `--accept-intentional` | Mark current finding as known-intentional (not a bug) |

---

## Trace Command

**Targeted flow tracing** — trace a specific user journey described in natural language.

### Usage

```
/roundtrip-radar trace "Dashboard → Add Item → Photo → Save"
/roundtrip-radar trace "Settings, Export, CSV, Email"
```

### How It Works

1. **Parse the path** — Split on `→`, `->`, or `,` into discrete steps
2. **Identify code locations** — For each step, search for:
   - View names matching the step
   - Sheet triggers, navigation actions
   - Button labels, action handlers
3. **Trace step by step** — For each transition:
   - File and line number
   - State changes (sheet presentations, navigation, @State mutations)
   - Data transformations (what model fields are read/written)
4. **Check for issues at each step:**
   - Is data preserved between steps? (Round-trip completeness)
   - Are collections preserved or silently narrowed? (Collection narrowing)
   - Are there error paths that lose context? (Error handling)
   - Is the user's intent preserved? (Data safety)
   - Are there race conditions? (Concurrency)
5. **Output** — Issue Rating Table for findings + step-by-step trace with receipts

### Output Format

```
Trace: Dashboard → Add Item → Photo → Save

| Step | Action | File | Lines | Data In | Data Out | Finding |
|------|--------|------|-------|---------|----------|---------|
| 1 | Dashboard tap "Add" | DashboardView.swift | 142-145 | — | activeSheet = .addItem | ok |
| 2 | Add Item sheet presents | AddItemView.swift | 1-50 | Item.draft | item.title, item.category | ok |
| 3 | Photo picker | PhotoPicker.swift | 23-89 | item.id | PhotoAttachment | ⚠️ orientation lost |
| 4 | Save item | ItemViewModel.swift | 112-134 | item + attachments | modelContext.save() | ok |

Issues Found:
| # | Finding | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
```

### When to Use

- **Debugging a specific user report** — "When I add a photo and save, the orientation is wrong"
- **Verifying a fix** — Trace the exact path to confirm data flows correctly
- **Pre-release spot check** — Trace critical paths without a full audit

---

## Diff Command

**Compare findings against the previous roundtrip-radar audit** — surface what regressed, what got fixed, and what's new since the last run.

### Usage

```
/roundtrip-radar diff
/roundtrip-radar diff --since 2026-04-01
/roundtrip-radar diff --workflow Backup
```

### Source of Truth

The diff reads from `.radar-suite/ledger.yaml` — the only authoritative cross-session store of roundtrip-radar findings. Per-workflow handoff YAMLs (`.agents/ui-audit/roundtrip-radar-handoff.yaml`) are overwritten each run, so they cannot serve as a diff baseline.

The "previous audit" is defined as **the most recent ledger session entry with `skill: roundtrip-radar`** that is strictly older than the current session. If no prior session exists, the diff command MUST refuse with:

> "No prior roundtrip-radar audit found in `.radar-suite/ledger.yaml`. Run a workflow audit first to establish a baseline."

Do not invent a baseline. Do not fall back to memory or `.agents/research/` markdown reports.

### How It Works

1. **Identify the baseline session** — read `.radar-suite/ledger.yaml`, find the most recent prior session entry with `skill: roundtrip-radar`. With `--since YYYY-MM-DD`, use the latest entry on or after that date instead.
2. **Identify the current session** — either the in-progress session (if the user just ran an audit and is asking for the diff) or the most recent completed session.
3. **Bucket every finding** from the union of baseline + current into one of four categories by RS-NNN ID:
   - **Fixed** — present in baseline with `status: open`, present in current with `status: fixed`
   - **Regressed** — present in baseline with `status: fixed`, present in current with `status: open` (also flag if `file_hash` changed since the fix, per the Regression Detection protocol in `radar-suite-core.md`)
   - **New** — RS-NNN ID is in current but not baseline
   - **Persistent** — present in both with the same status (open or deferred)
4. **Apply optional filters:** `--workflow [NAME]` restricts to findings whose `workflow` field matches.

### Output Format

```
Diff: 2026-04-15 → 2026-05-12 (27 days, 4 sessions)

✅ Fixed (3)
| RS-NNN | short_title | Workflow | Fixed in |
|--------|-------------|----------|----------|
| RS-042 | Backup drops attachment storage | Backup | 2026-04-22 |
...

🔴 Regressed (1)
| RS-NNN | short_title | Workflow | Was fixed | file_hash changed? |
|--------|-------------|----------|-----------|--------------------|
| RS-019 | CSV import loses Room field | CSV Import | 2026-04-18 | yes (CSVImportManager.swift) |

🆕 New (5)
| RS-NNN | short_title | Workflow | Urgency |
|--------|-------------|----------|---------|

📌 Persistent (12)
[collapsed by default; pass --verbose to expand]
```

### When to Use

- **Pre-PR review** — confirm the changes in this PR didn't reintroduce any previously-fixed bug
- **Post-release retrospective** — what got fixed this release cycle, what slipped
- **Suspecting a regression** — `--workflow [NAME]` narrows to one user journey

### Refusal cases

- No prior ledger session: refuse with the message above
- `--since` date is in the future: refuse with "Date is in the future; no audits to compare"
- `--workflow [NAME]` matches no findings in either baseline or current: print "No findings in workflow [NAME] across either session" (not a refusal — a legitimate empty result)

---

## Skill Introduction (MANDATORY — run before anything else)

**This section replaces `radar-suite-core.md § Session Setup` for the roundtrip-radar entry point.** Do NOT also run core's 4-question Session Setup — its questions are consolidated below. All four setup questions go in ONE `AskUserQuestion` call on first invocation. Step 1's per-workflow flow reuses these answers and never re-asks them.

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "How should fixes be handled?"**
- **Auto-fix safe items (Recommended)** — Apply isolated, low-blast-radius fixes automatically. Present cross-cutting fixes and design decisions for approval first.
- **Review first** — Present all findings with ratings, then ask before making any changes. Fixes still happen — you just approve each wave first.
- **Batch mode** — Approve all fixes in each wave at once.

**IMPORTANT:** All three modes lead to fixes. "Review first" means the user sees the plan before code changes — it does NOT mean "skip fixes and jump to handoff." After presenting findings, ALWAYS offer to fix them regardless of which mode was selected. (Exception: Hands-Free mode overrides this — see Question 4.)

**Question 3: "How should results be delivered?"**
- **Display only (Recommended)** — Show findings in the conversation. No file written.
- **Report only** — Write findings to `.agents/research/[DATE]-[WORKFLOW]-audit.md`. Minimal conversation output. **Before writing**, per Artifact Lifecycle (Class 3) in `radar-suite-core.md`, archive any existing `.agents/research/*-[WORKFLOW]-audit.md` matching the same workflow to `.agents/research/archive/superseded/`.
- **Display and report** — Show findings in the conversation AND write to file.

**Question 4: "Will you be stepping away during the audit?"**
- **I'll be here (Recommended)** — Normal mode. Permission prompts may appear for writes/edits.
- **Run the full analysis without stopping to ask — no code changes** — Hands-Free mode. Restricts to read-only tools (Read, Grep, Glob). No Bash, no Edit, no Write — nothing that triggers a permission prompt. **Hands-Free overrides Question 2:** all fixes are deferred regardless of `FIX_MODE`. The progress banner still prints, but the `AskUserQuestion` next-wave prompt is suppressed; the skill emits the "audit complete through Step N" completion message instead (see Hands-Free Mode below).
- **Pre-approved** — You have already configured Claude Code permissions for this session (see Permission Setup below). Run at full speed without restriction.

Store as: `USER_EXPERIENCE`, `FIX_MODE`, `DELIVERY`, `PRESENCE_MODE`. Apply to ALL output for session, per `radar-suite-core.md § Experience-Level Output Rules`. Also persist to `.radar-suite/session-prefs.yaml` per `radar-suite-core.md § Session Persistence`.

**Question 5 (optional follow-up): "Would you like a brief explanation of what this skill does?"**
- **No, let's go (Recommended)** — Skip explanation, proceed to audit.
- **Yes, explain it** — Show a 3-5 sentence explanation adapted to the user's experience level (see below), then proceed.

**Experience-adapted explanations for Roundtrip Radar:**

- **Beginner**: "Roundtrip Radar follows your data through complete user journeys — like tracking a package from warehouse to doorstep and back. For example, it checks: if you create an item, back it up, delete it, and restore — does everything come back exactly? It finds bugs where data gets lost, corrupted, or silently dropped along the way. It audits one workflow at a time (backup, add item, sync, etc.) so nothing gets missed."

- **Intermediate**: "Roundtrip Radar audits individual workflows end-to-end for data safety, error handling, concurrency, and round-trip completeness. It traces data through create → modify → export → import cycles, checks transaction boundaries, verifies error recovery paths, and identifies where data is silently lost. Works one workflow at a time to stay thorough."

- **Experienced**: "Per-workflow code audit: data safety, error handling, concurrency, performance, contract mismatches, and round-trip completeness. Discovers workflows, audits each with issue rating tables and fix plans, then rolls up cross-cutting patterns."

- **Senior/Expert**: "Workflow-scoped audit: data safety + error paths + concurrency + round-trip completeness. Rating tables + fix plans + cross-workflow rollup."

Store the experience level as `USER_EXPERIENCE` and apply to ALL output for the session.

**User impact explanations:** Can be toggled at any time with `--explain` / `--no-explain`. When enabled, each finding gets a 3-line companion explanation (what's wrong, fix, user experience before/after). See the shared rating system doc for format and rules. Store as `EXPLAIN_FINDINGS` (default: false).

**Experience-level auto-apply:** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply all output rules from Experience-Level Output Rules table in `radar-suite-core.md`.

**Subsequent workflows:** Do NOT re-ask the full setup questions. Instead, show a one-line reminder before each workflow:
```
Using: [Experienced] mode, [Auto-fix safe items], [Display only], [I'll be here]. Type "adjust" to change, or press Enter to continue.
```
The four bracketed values map to `USER_EXPERIENCE`, `FIX_MODE`, `DELIVERY`, `PRESENCE_MODE` set during the Skill Introduction. If the user types "adjust", re-ask only the question(s) they want to change. Users may want to adjust experience level after a few workflows (beginner explanations may feel too simple, expert too terse).

---

## Shared Patterns

See `radar-suite-core.md` for: Tier System, Pipeline UX Enhancements, Table Format, Plain Language Communication, Work Receipts, Contradiction Detection, Finding Classification, Audit Methodology, Context Exhaustion, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Implementation Sort Algorithm, short_title requirement.

## Axis Classification Protocol (MANDATORY — before emitting any finding)

Every roundtrip-radar finding must be classified on the 3-axis framework and pass the schema gate in `radar-suite-core.md` before emission. The framework is defined in `skills/radar-suite-axis-classification/SKILL.md`.

### Roundtrip-specific axis mapping

roundtrip-radar's findings are organized by what part of the round-trip path is broken. Each finding category maps to a default axis, with reclassification rules based on verification checks.

| Finding category | Default axis | Reclassification rule |
|---|---|---|
| Data loss on cancel | axis_1_bug | Stays axis_1 (user-facing data loss) |
| Data loss on error | axis_1_bug | Stays axis_1 |
| Missing feedback after save | axis_1_bug | Stays axis_1 |
| Field written but not read | axis_3_smelly | Reclassify to axis_1_bug ONLY if a user feature depends on the field (check feature flags and view usage) |
| Field read but not written | axis_3_smelly | Reclassify to axis_1_bug if feature claims the field is set |
| Field exists but unwired end-to-end | axis_3_smelly | Reclassify to axis_1_bug if a user action should write it |
| Round-trip path opaque (cannot be traced from UI to persistence) | axis_2_scatter | Stays axis_2 — data flow is correct but impossible to verify |
| Inconsistent serialization across paths (CSV, backup, CloudKit) | axis_1_bug | Stays axis_1 — ONE path loses user data |
| Serialization paths duplicated across multiple managers | axis_2_scatter | Stays axis_2 — correct but hard to maintain |
| Serialization call reaches a dead branch (e.g., guard always true) | axis_3_dead_code | Stays axis_3 |
| CloudKit sharing contract violation (write dropped or identity withheld server-side) | axis_1_bug | Stays axis_1 — the trace terminates at the server boundary by construction, not from opacity, so the full-path rule's axis_2_scatter fallback does NOT apply (see § Full-path verification rule, external-boundary clause). Reclassify to axis_3_smelly only if no user-visible surface consumes the affected permission or identity |

### Full-path verification rule (roundtrip-specific)

**Every finding must cite the full roundtrip path in its `verification_log`.** The path is the sequence of file:line hops from UI entry point to persistence and back to UI. If the path cannot be traced end-to-end, the finding is `axis_2_scatter` regardless of its category (the data flow is opaque even if correct).

Example `verification_log` for a roundtrip finding:
```yaml
verification_log:
  - check: full_path_trace
    path:
      - ImportCSVView.swift:142 (user taps Import)
      - CSVImportManager.swift:420 (parse loop)
      - Item.swift:58 (Item init with room: nil  ← MISSING FIELD)
      - ModelContext (save)
      - ItemListView.swift:84 (Query fetches items)
      - ItemRowView.swift:29 (displays room, which is nil)
    result: "path traced end-to-end; room field is dropped at CSVImportManager.swift:420 and displayed as nil downstream"
  - check: pattern_citation_lookup
    result: "found existing round-trip pattern at Sources/Managers/BackupManager.swift:NNN which correctly serializes room"
```

**External-boundary exception.** A path that reaches an external system (a sync server, a payment
processor, a third-party API), and resumes on the other side, is **traced — not opaque**. The
`axis_2_scatter` fallback above applies to paths that cannot be followed *within the codebase*,
not to paths that leave it. Mark the crossing explicitly and keep the finding's category axis:

```yaml
verification_log:
  - check: full_path_trace
    path:
      - FamilySharingView.swift:NNN (owner sets Member Access to Viewer)
      - FamilySharingManager.swift:NNN (participant.permission = ckPermission)
      - [SERVER BOUNDARY: CKShare save succeeds; server discards the write]
      - FamilySharingView.swift:NNN (participant still renders as Editor)
    result: "path traced to the server boundary and resumed on the read side; terminates at an
             external system, NOT from opacity — axis_1_bug stands. Confidence: needs-runtime
             (2-account round-trip required to observe the server's actual behavior)"
```

Distinguish this from a genuine gap: a `[SERVER BOUNDARY]` marker asserts you traced the code up
to the call and picked the path back up after it. If you could not find the read side either, that
is opacity — use `[GAP: ...]` and take `axis_2_scatter`.

If any hop cannot be found (e.g., "no persistence call in this workflow"), the path entry documents the gap:
```yaml
path:
  - AddItemView.swift:120 (user taps Save)
  - AddItemViewModel.swift:85 (validate inputs)
  - [GAP: no modelContext.insert found for this workflow in scope]
result: "round-trip path INCOMPLETE; finding classified as axis_2_scatter (opaque flow)"
```

### Required checks before emission

1. **Full-path trace** (MANDATORY for every finding) — walk UI → manager → model → persistence → UI. Log every hop.
2. **Pattern citation lookup** (MANDATORY) — find an existing correct round-trip pattern in the same codebase and cite it by file:line in `better_approach`.
3. **Whole-file scan** (MANDATORY when claiming a field is "not serialized") — scan the ENTIRE serializer file (CSV import/export, backup encode/decode, CloudKit mapper) for the field name. If found, it IS serialized — the finding is probably about a different code path (reclassify as axis_2_scatter if the serialization is scattered).
4. **Multi-path comparison** (MANDATORY for serialization findings) — a field may be serialized in one path (backup) but not another (CSV). Check ALL known serialization paths before claiming "missing." Stuffolio has at least 4: CSV export, CSV import, backup (JSON), CloudKit (CKRecordMapper).

### Schema gate

Per `radar-suite-core.md`, a finding is REJECTED if:
- `axis` field is missing
- `before_after_experience` is missing or incomplete
- `better_approach` lacks a file:line citation matching the pattern shape
- `verification_log` lacks a `pattern_citation_lookup` entry

Rejected findings are NOT silently dropped: downgrade confidence to `possible`, mark as `coaching incomplete`, and increment `rejected_no_citation` in the handoff's `axis_summary`.

### Axis summary block

At the end of every roundtrip-radar handoff:
```yaml
axis_summary:
  axis_1_bug: [count]              # data loss, missing feedback, broken serialization paths
  axis_2_scatter: [count]          # opaque flows, duplicated serialization
  axis_3_dead_code: [count]        # unreachable serialization branches
  axis_3_smelly: [count]           # unwired fields with no user feature dependency
  rejected_no_citation: [count]
```

---

## Pre-Scan Startup (MANDATORY — before any workflow scan)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here.

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

---

## Step 0: Workflow Discovery

Run first if workflows are unknown or have changed.

Scan the codebase and identify all user-facing workflows.

### What Counts as a Workflow

A workflow is a multi-step user action that:
- Spans 2+ screens or states (not a single tap)
- Involves data creation, modification, deletion, or transfer
- Has a distinct entry point and completion state

### How to Find Them

1. Search for navigation entry points:
   - `.sheet`, `.fullScreenCover`, `.navigationDestination`
   - `NavigationLink`, `TabView` tabs
   - Button actions that trigger multi-step flows
2. Search for data operations:
   - `modelContext.insert`, `modelContext.delete`, `context.save`
   - Import/export, backup/restore, sync operations
   - API calls, file I/O
3. Search for state machines:
   - Enums with cases like `.idle`, `.processing`, `.complete`
   - Multi-step `@State` progressions
   - `isProcessing`, `isImporting`, `isSaving` patterns

### Output

List each workflow with:

| # | Workflow | Entry Point | Key Files | Complexity | Data Risk |
|---|----------|-------------|-----------|------------|-----------|
| 1 | [Name] | [Where user starts it] | [2-4 main files] | Low/Med/High | None/Read/Write/Delete |

### Complexity Criteria

- **Low** — 1-2 files, linear flow, no branching
- **Medium** — 3-4 files, some branching, error handling
- **High** — 5+ files, async operations, multiple outcomes, data transformation

### Data Risk Criteria

- **None** — Display only
- **Read** — Fetches but doesn't modify
- **Write** — Creates or updates data
- **Delete** — Removes data or replaces state

### Priority Recommendation

After listing all workflows, recommend which to audit first based on:
- High complexity + Write/Delete data risk = audit first
- Medium complexity + Write risk = audit second
- Everything else = audit if time permits

Do NOT write a report file. Output the table directly.

---

## Step 1: Per-Workflow Audit

**One workflow per prompt.** Run as a separate agent or conversation per workflow
to prevent context exhaustion.

Audit the **[WORKFLOW NAME]** workflow for bugs, data-safety issues,
performance problems, and data round-trip completeness.

### Before Starting (First Workflow Only)

All setup questions were captured during the Skill Introduction call (`USER_EXPERIENCE`, `FIX_MODE`, `DELIVERY`, `PRESENCE_MODE`). Do NOT re-ask any of them. Show the one-line settings reminder from § Skill Introduction and proceed to the audit.

If any of the four variables is missing for some reason (e.g., session-prefs file deleted mid-session), re-run the full Skill Introduction call before continuing — never partially re-ask, since the questions are interdependent (Question 4 overrides Question 2).

### Permission Modes

#### Normal Mode
- Read any file without asking.
- Edit files listed in "Files to Read" and their corresponding test files freely.
- For files outside that list, edit only if directly required by a P0-P1 fix.
  Note which external files were changed in your output.
- Build and run tests without asking.
- If a fix breaks the build, restore the original code and document the
  finding as "Documented" instead of "Fixed".

#### Hands-Free Mode
**Guarantees no blocking prompts.** The skill will ONLY use these tools:
- `Read` — read file contents
- `Grep` — search file contents
- `Glob` — find files by pattern

It will NOT use:
- `Bash` — no shell commands (grep via Grep tool instead)
- `Edit` / `Write` — no file modifications
- `AskUserQuestion` — no interactive prompts

**Precedence rules (load-bearing — Hands-Free wins all ties):**

1. **Hands-Free overrides `FIX_MODE`.** Even if Question 2 was answered `Auto-fix safe items` or `Batch mode`, no fixes are applied in Hands-Free mode. All findings are emitted with `Status: Deferred (hands-free)` in the Issue Rating table. The Fix Plan is still produced (so the user can act on it on return), but no Wave 1-5 fix application runs.
2. **Hands-Free suppresses the next-wave `AskUserQuestion`.** The "BLOCKING — progress banner + next-wave prompt" rule under § Progress Banner applies in Normal and Pre-Approved modes only. In Hands-Free mode, the progress banner still prints (so the user can see what was audited), but the `AskUserQuestion` call is omitted and replaced by the completion message below.
3. **Hands-Free does not suppress handoff writes.** Writing `.agents/ui-audit/roundtrip-radar-handoff.yaml` and `.radar-suite/ledger.yaml` uses `Edit`/`Write` — which Hands-Free forbids. To resolve: in Hands-Free mode, the skill emits the handoff and ledger content **inline in the conversation as fenced YAML blocks** so the user can persist them on return. Inline emission does not count as a write.

When the audit completes (or hits a step that needs restricted tools), it prints:
```
⏱ Hands-free audit complete through Step [N].
  Steps requiring action: [list]
  Findings deferred: [count] (no fixes applied — Hands-Free mode)
  Handoff YAML + ledger entries: emitted inline above; copy to .agents/ui-audit/ and .radar-suite/ when you return
  Reply to continue with supervised steps.
```

#### Pre-Approved Mode
Full speed, no restrictions. Assumes you've set up permissions. See below.

### Permission Setup (for unattended runs)

To avoid permission prompts during audits, pre-allow these read-only patterns in your Claude Code settings. These are **safe to auto-approve** — they cannot modify your codebase:

```
# Already safe by default (no setup needed):
Read, Grep, Glob — always auto-approved

# Add these for unattended Bash scans:
Bash(find:*)
Bash(wc:*)
Bash(stat:*)
```

**Do NOT auto-approve** (keep these prompted — they modify state):
```
Edit, Write — file modifications
Bash(rm:*), Bash(git:*) — destructive operations
```

> **Tip:** Hands-free mode can complete workflow discovery (Step 0) and the full per-workflow audit (Step 1) read-only. Only fix application needs write access.

### Freshness

Base all findings on current source code only. Do not read or reference
files in `.agents/`, `scratch/`, or prior audit reports. Ignore cached
findings from auto-memory or previous sessions. Every finding must come
from scanning the actual codebase as it exists now.

### Context Budget

If context is running low, prioritize in this order:
1. Finish verifying Suspects
2. Complete any in-progress fixes
3. Emit the Fix Plan for what you've found so far
4. Skip remaining exploratory checks

Never start a new check you can't finish.

### Experience-Level Adaptation

Adjust ALL output based on the user's experience level:

- **Beginner**: Plain language, real-world analogies, define terms on first use ("a model context — the database connection SwiftUI uses to save data"). Explain why each finding matters. Use compact 4-column tables with prose explanations below.
- **Intermediate**: Standard SwiftUI terminology without defining basics, but explain non-obvious patterns (e.g., why a `Task.sleep` workaround indicates a broken refresh path). Full 9-column tables with brief descriptions.
- **Experienced** (default): Concise findings, no definitions. "Missing `modelContext.save()` after batch delete in `BulkEditViewModel.swift:142`". Full tables, terse text.
- **Senior/Expert**: Minimal prose. File:line + one-line description only. Findings table IS the output. Skip design principle citations and category explanations.

### Fix Threshold

- **Fix:** Data loss, data corruption, crashes, infinite loops, broken user flows (P0-P1)
- **Document only:** Performance, UI polish, code style, missing features (P2+)
- **Defer with explanation:** P0-P1 issues that require multi-file migration,
  schema changes, or affect core models used outside this workflow.
  Mark as "P1 - Deferred (reason)" in the table.

### Suspects (verify these first, then explore beyond)

[One per line. Include file name, approximate line, and the specific question to answer.]

Example:
- `BackupDataSheet.swift ~line 351`: `decryptAndRestore(replaceExisting: false)`
  — is the user's replace choice preserved through the password prompt?

[If no suspects: "No prior suspects — full exploratory audit."]

### Recent Changes (verify these are correct)

[One per line. Include file, what changed, and what to verify.]

Example:
- `CloudSyncManager.swift`: Added `maxRetries=3` retry limit
  — verify counter resets on all terminal paths (success, non-retryable errors)

[If none: "None"]

### Files to Read

- **Must read:** [2-4 files central to this workflow]
- **Read if relevant:** [1-2 supporting files, with the condition that makes them relevant]
- **Skip:** [files that look related but are low-value]
- **Tests:** Find by searching `Tests/` for `[WORKFLOW_KEYWORD]`

### What to Check

1. **Data safety** `enumerate-required` — destructive operations, transaction boundaries, edge cases
2. **Error handling** `mixed` — missing catches, silent failures, user-facing error messages
3. **Concurrency** `mixed` — `@MainActor` compliance, Task isolation, ModelContext thread safety
4. **Performance** `grep-sufficient` — `@Query` without predicates, O(n²) loops, main-thread blocking
5. **Contract mismatches** `grep-sufficient` — constants vs hardcoded strings, keys defined in one file but consumed in another
6. **Round-trip completeness** `enumerate-required` — does data survive a full create → export → import/restore cycle?
7. **Interruption paths** `enumerate-required` — dismiss mid-operation, app backgrounding, rotation, cancel
8. **Collection narrowing** `enumerate-required` — collections silently reduced to single elements at handoff points (see detection guide below)
9. **Tests** `enumerate-required` — update broken tests, add tests for P0-P1 fixes where logic is testable
10. **Bridge parity** `enumerate-required` — multiple consumers of the same model type must read the same fields (see detection guide below)
11. **CloudKit production-only failures** `mixed` — code that works in Dev/simulator but fails for real users in Production (see detection guide below)
12. **Dead writers** `grep-sufficient` — a function that does real work (sync/save/write/upload) but has ZERO callers, so a feature compiles + looks done while silently doing nothing (see detection guide below)

### Verification Template (MANDATORY per workflow)

Before grading a workflow, produce this table showing what was actually traced:

```
| Step | Action | File Read | Lines | Receipt | Finding |
|------|--------|-----------|-------|---------|---------|
| 1. Create | [what happens] | [file:line] | [range] | [evidence] | [ok / issue] |
| 2. Save | [what happens] | [file:line] | [range] | [evidence] | [ok / issue] |
| 3. Export | [what happens] | [file:line] | [range] | [evidence] | [ok / issue] |
| 4. Import | [what happens] | [file:line] | [range] | [evidence] | [ok / issue] |
```

Rules:
- Every step in the workflow must have a File Read entry
- Steps without a file read cannot produce findings tagged "verified"
- The table IS the audit — the findings are just a summary of what the table reveals

### Collection Narrowing Detection Guide

**What it is:** A `[T]` (array) enters a handoff point but only a `T` (single element) exits -- silently discarding the rest. The flow works, types are correct, and the user gets a result -- but with degraded quality because most of the input data was dropped.

**Why it matters:** This bug class is invisible to type checking, navigation audits, and UX flow audits. The flow completes successfully with no errors. Only the *quantity* of data is wrong, which degrades results without any signal to the user.

**Detection patterns:**

| Pattern | Code Signature | Likely Bug? |
|---------|---------------|-------------|
| Array-to-first | `array.first` or `array[0]` passed where `[T]` is accepted | Yes -- receiver can handle the full array |
| Init narrowing | `init(item: T)` called by a site holding `[T]` when `init(items: [T])` exists | Yes -- wrong init chosen |
| Wrapper narrowing | Class/struct stores `T` but is created from `[T]` context | Yes -- wrapper designed for single item, not updated for multi |
| Loop-break narrowing | `for item in items { ...; break }` or `if let first = items.first` without processing rest | Maybe -- check if intentional (preview thumbnail) |

**Distinguish intentional from accidental:**

- **Accidental (flag it):** The *receiving* function/init accepts `[T]` but the caller passes `.first`. The API was designed for multiple items.
- **Accidental (flag it):** A wrapper class stores single `T` but is created in a context where `[T]` is available and the downstream service accepts `[T]`.
- **Intentional (skip it):** The receiver only accepts `T` and there's no `[T]` alternative. Example: displaying a single thumbnail preview from an array.
- **Intentional (skip it):** The narrowing is guarded by UI that shows the user only one item is being used (e.g., "Using first photo as cover image").

**How to check during a workflow audit:**

1. At each handoff point in the Verification Template, note the **cardinality** of data passed:
   - `[4 images]` → `[4 images]` = ok
   - `[4 images]` → `[1 image]` = flag as collection narrowing
2. When a function receives an array, trace what it passes downstream -- does the full array reach the endpoint?
3. When an init accepts single `T`, check if a multi-item init exists on the same type
4. In the Verification Template, add a "Cardinality" note to the Receipt column when collections are involved

**Origin:** Found in Stuffolio Apr 2026 -- user selected 4 photos for AI analysis, but `AIAnalysisTask` only accepted first image, and Stuff Scout sheet passed `productImages?.first` to a view that had a multi-image init. Flow worked, types were correct, results were degraded.

### Bridge Parity Detection Guide

**What it is:** Multiple functions consume the same model type but read different subsets of its fields -- one was updated when new fields were added, the others were not. The outdated consumer silently drops data.

**Why it matters:** This bug class is invisible to single-path tracing. Each consumer works correctly in isolation -- types match, no crashes, no errors. The bug only appears when you compare consumers against each other and notice one reads fewer fields. It survives code review because reviewers follow one path at a time.

**Detection method -- relative comparison, not absolute counting:**

1. **Enumerate all consumers** of a given model type. A "consumer" is any function that reads fields from the type to build output (notes, prefill data, export, display). Search for:
   - Functions with parameters of the type (`func build(_ session: ScoutSession)`)
   - Functions that access properties of the type (`session.aboutItem`, `session.historicalContext`)
   - Bridge structs with `init(from:)` or conversion methods (`toItem()`, `toPrefillData()`)

2. **For each consumer, record which fields it reads.** Build a field-access matrix:

   ```
   | Field            | ConsumerA | ConsumerB | ConsumerC |
   |------------------|-----------|-----------|-----------|
   | era              | ✓         | ✓         | ✓         |
   | aboutItem        | ✓         | ✓         | ✓         |
   | historicalContext | ✓         |           | ✓         |
   | collectorNotes   | ✓         |           | ✓         |
   | researchTips     | ✓         |           | ✓         |
   ```

3. **Flag asymmetries.** If N consumers exist and one reads strictly fewer fields than the others, it is the outlier. The comparison is relative -- you do not need to know the "correct" field count. The mismatch itself is the finding.

**Ranking the finding:**

| Signal | Confidence |
|--------|------------|
| One consumer reads < 50% of fields that others read | Almost certain bug -- flag immediately |
| One consumer misses 1-2 fields that all others include | Probable bug -- verify with git blame (was the field added after this consumer was written?) |
| Consumers read different but overlapping sets (no strict subset) | Possible intentional -- different consumers may legitimately need different fields (e.g., summary view vs. detail export). Check if the omitted fields are relevant to the consumer's purpose. |

**Distinguish intentional from accidental:**

- **Accidental (flag it):** Two consumers serve the same purpose (e.g., both build "notes" text from scout data) but one includes 3 more sections. The simpler one was written first and never updated.
- **Accidental (flag it):** A consumer was copied from another and trimmed, but the trimming removed fields that matter for its context.
- **Intentional (skip it):** A summary consumer intentionally shows only key fields (e.g., a list row shows title + era but not full historical context). The consumer's purpose justifies the subset.
- **Intentional (skip it):** A consumer explicitly documents why fields are excluded (comment or design doc).

**How to check during a workflow audit:**

1. When you encounter a bridge or conversion function, search for OTHER functions that consume the same source type
2. Build the field-access matrix for all consumers found
3. If an asymmetry exists, add a "Bridge Parity" note to the Verification Template Receipt column
4. In the Issue Rating table, tag bridge parity findings as `verified` (you read the code of all consumers) with blast radius = number of consumers that need updating

**Cross-cutting accumulator integration:** After finding a bridge parity issue, add the model type to the cross-cutting pattern accumulator. In subsequent workflows, automatically check any new consumer of that type against the established field matrix.

**Origin:** Found in Stuffolio Apr 2026 -- `ScoutSession` had 3 consumers building notes. `ScoutMergeView` and `StuffScoutBridge` included all 6 narrative fields. `ExistingItemScoutFlow.buildNotesFromScout()` included only 3. The outlier was written before the other fields were added and never updated. No type error, no crash, no test failure -- users simply lost Historical Context, Collector Notes, and Research Tips when saving via that code path.

### CloudKit Production-Only Failure Detection Guide

**What it is:** CloudKit code that works in the Development environment (debug builds, simulator) but fails for real users in Production. The simulator masks the bug because Development is permissive; Production is strict. The flow "works on my machine" and ships broken.

**Why it matters:** Invisible to the compiler, unit tests, and any simulator run. Only real users on the Production CloudKit environment hit it — typically as a SILENT empty result (no crash, no error), so it reads as "feature does nothing" rather than "feature errored."

**Detection patterns:**

| Pattern | Code Signature | Production Failure |
|---------|---------------|---------------------|
| `recordName` not queryable | `CKQuery(recordType:, predicate: NSPredicate(value: true))` then `records(matching:)` | A fetch-all query forces a sort on the system `recordName` field, NOT queryable by default in the **Production** schema (it IS in Development → masks it). Throws "Field 'recordName' is not marked queryable" → caught → silent empty result. **DURABLE FIX: enumerate the zone via `CKFetchRecordZoneChangesOperation` (no index needed) — BUT only on CUSTOM zones, not the default zone.** Default-zone code must mark `recordName` queryable in the Dashboard or migrate to a custom zone. |
| Type assumed to exist | `CKRecord(recordType: "Foo")` written where `Foo` may not be in the deployed Prod schema | **Production does NOT auto-create record types on write; Development DOES.** A type exercised only in Dev is absent in Prod until "Deploy Schema Changes" is run. Write fails silently for real users. Verify every written type is in the Prod schema. |
| Partial-failure swallow | `case .partialFailure: ... return []` | Discards the records that DID succeed → blanks the whole list on one bad record. Collect per-record successes instead (zone enumeration does this naturally). |
| `try?` hides prod error | `try? await db.records(...)` / `try? await container.accountStatus()` | Collapses a prod-only failure (or `.couldNotDetermine`/`.temporarilyUnavailable`) into nil → treated as "empty" or "not signed in." Use do/catch + surface to Sentry. |

**Distinguish:** flag the read paths a beneficiary/recipient hits FIRST (highest impact — silent empty UI for the receiver). Owner-side and sync paths are lower but still real.

**Origin:** Stuffolio 2026-06-08 — Legacy Wishes beneficiaries silently received empty shares (3 stacked causes: schema never deployed to Prod, the data-sync writer was never called, and the reads used `CKQuery(predicate:true)` which failed "not queryable" in Prod). The core inventory pull (`CloudSyncManager`) used the same query on the default zone — works ONLY because that one index happens to be deployed; a regression would silently empty every user's inventory on a new device.

### CloudKit Sharing Contract Detection Guide

**What it is:** CloudKit **sharing** code where the Swift is locally correct — it compiles, the
value is assigned, no error is thrown — but the CloudKit server silently refuses the write or
withholds the data. Distinct from the Production-Only guide above: that one is about
**schema/query** failures (a type or index missing in Prod). This one is about **server-side
contracts on `CKShare`** that hold in every environment, Development included, so no amount of
Dev testing surfaces them.

**Why it matters:** These fail *successfully*. `try await db.save(share)` returns without
throwing, the local object shows the new value, and the owner's UI confirms a change that never
landed. Because the source reads correct, a static audit reports the subsystem CLEAN — which is
worse than a missed bug, since "no finding" is indistinguishable from "verified safe." Four
sharing bugs shipped past clean audits on one codebase before this axis existed.

**The contract underneath all four patterns:** a recipient who joins a share by tapping an
invite **link** (while `publicPermission != .none`) is a CloudKit **public participant**
(`role == .publicUser`). Apple's rule (CKShare.h): *"In order to modify the list of
participants, a share must have publicPermission set to CKShareParticipantPermissionNone."*
Public and private participants cannot be mixed on one share. So **link-only invites and
per-member roles are mutually exclusive** — a design choice most codebases make implicitly, in
one line, without recording that they made it.

**Detection patterns:**

| Pattern | Code Signature | Server-Side Failure |
|---------|---------------|---------------------|
| Per-participant permission write | `participant.permission = .readWrite` / `.readOnly` on a share whose `publicPermission != .none` | **Silently discarded.** The server governs a link-joined member's access by share-level `publicPermission` only. The save succeeds, no error, and the participant's own fresh fetch still returns the old value. Fix: write `publicPermission` (household-wide), or move to `publicPermission = .none` + invited private participants. |
| Nil-only guard on CloudKit identity | ANY nil-only guard over an identity read — `?? "Unknown"`, `if let name = identity.nameComponents?.formatted()`, `guard let ... else` | **Guard never fires.** For a public participant the server withholds identity and `formatted()` returns an **EMPTY STRING, not nil** — it binds successfully and sails through into UI interpolation (`"Export 's Items"`, `"'s Household"`) or into a key (`"name:"`). Fix: fall through on **emptiness**, not nil, and degrade name → email → placeholder. ⚠️ **Match on the nil-only *semantics*, not the `??` spelling** — an `if let`/`guard let` over the same expression is the identical defect and is easy to miss when grepping for `??`. |
| Identity read with no both-absent branch | A name→email fallback chain with a single terminal placeholder, rendered into possessives or list rows | CloudKit can withhold **both** identity and email, so every member collapses to the same literal placeholder — the household reads as belonging to a person named "Unknown" and no member is distinguishable. An emptiness-aware helper is necessary but **not sufficient**; the both-absent case needs its own UI treatment. |
| Permission displayed from the wrong field | UI binds a role chip / edit gate to `participant.permission` | **UI lie.** Effective access is the **higher** of `publicPermission` and any individual grant. Reading the per-participant field reproduces the dropped-write bug as a display that contradicts what the user can actually do. |

**Two traps that ride along with the fix:**

1. **Never write `publicPermission = .none` to mean "view only."** It stops the invite link
   resolving and drops pending participants. `.readOnly` is the view-only value.
2. **A "heal" that force-restores `.readWrite`** will silently re-promote a deliberately
   view-only household on the next invite handout. Heal only the unjoinable `.none` case.

**Detection method:**

1. Grep for `CKShare` / `publicPermission` / `\.permission =` / `participant`. **Zero hits for
   `publicPermission` alongside nonzero hits for `participant.permission =` is itself the
   finding** — it means the code manages per-member roles on a share whose join mode was never
   considered.
2. For every CloudKit identity read, check the guard: nil-handling alone is insufficient; require an
   emptiness test. This check is mechanical and has the highest hit rate of the four. **Grep all
   three spellings** — `?? `, `if let`, and `guard let` — over `nameComponents`, `formatted()`,
   `lookupInfo`, and `userIdentity`. Searching only for `??` misses the binding forms.
   ⚠️ **Identity-as-KEY is a separate sweep from identity-as-DISPLAY.** A codebase that fixed its
   display helper may still mint identity keys through an uncorrected fallback chain; the display
   fix does not propagate to it. Check both, in both directions.
3. Trace which field the **UI** reads for role/permission display, independently of which field
   the **writer** sets. A mismatch between them is the "UI lie" pattern.
4. **Before diagnosing any of this, grep the repo for a sibling manager that already solved
   it.** These bugs recur per-manager; the fix usually already exists elsewhere in the same
   codebase and was simply never propagated.

**Confidence and verdict:** every finding here is `needs-runtime` at best from static reading —
the server's behavior cannot be observed by grep, so never emit one as `verified`. Record in the
`verification_log` what a 2-account round-trip would show, so the finding names its own missing
evidence rather than reading as a confirmed bug. The
diagnostic signature of a real dropped write: the save succeeds, and the participant's own fresh
server fetch still returns the old permission — immediately, after force-quit, and after a long
wait. A 15-minute wait ruling out propagation lag is the tell. Confirm in 30 seconds by logging
`participant.role.rawValue` on a freshly fetched share: `.publicUser` makes the diagnosis
certain.

⚠️ **Do not blame the read path first.** In the canonical incident the entire participant read
chain was correct and faithfully reporting the server's true state; suspecting a stale cache
burned a full session. Verify whether the OWNER'S OWN next fetch reflects the change — that
isolates save-side from read-side in one step.

⚠️ **A blank member name is NOT a failed join.** It reads like one on-device. Check
`Status: Accepted` and whether shared items actually arrive.

**Origin:** Stuffolio, four defects over six weeks, one root cause. 2026-07-05 — a legacy
share's "Allow Family Input" was switched ON and the recipient stayed View Only. 2026-08-05 — an
owner→viewer permission change never reached the participant, ever; it cost a full session, and
the fix already existed in a sibling manager in the same repo. 2026-08-05 and 08-07 — the same
empty-string defect logged twice from two devices; member rows rendered nameless and a button
read "Export 's Items". 2026-08-14 — every identity collapsed to the literal "Unknown" because
CloudKit withheld both identity and email; the emptiness-aware helper was working correctly and
still produced an unusable screen. Each shipped past an audit that reported CloudKit clean,
because each one's Swift reads correct.

### Dead Writer Detection Guide

**What it is:** A function whose name implies it does important work (sync/upload/save/persist/write/send/submit/schedule/export/backup) but has ZERO call sites in production code. The feature compiles, looks done, and silently does nothing — because the UI action calls a *different* function (often a stub), or the wiring was simply forgotten.

**Why it matters:** The inverse of an unreachable view — here a live READ path depends on a WRITE that nothing performs. Invisible to the compiler (the function is valid) and to tests (nobody tests a function nobody calls). The user-facing symptom is a feature that "doesn't work" with no error.

**Detection method:**

1. Find functions named with a does-real-work verb: `func (sync|upload|save|persist|write|send|submit|push|commit|schedule|export|backup)[A-Z]...`. Scan Managers, Services, AI/network layers, **and Models** (model methods can be writers too).
2. For each, grep the whole source tree for call sites (`\bfuncName\(`), excluding the definition and tests.
3. **Zero callers = candidate.** Then judge: genuinely dead (delete it) vs. forgotten wiring (a user-facing feature depends on it — wire it). The dangerous case is when a live read path consumes the state this writer was supposed to produce.
4. Watch for grep-blind invocation (dynamic dispatch, `#selector`, protocol witness, public API) before declaring dead.

**Mechanical version:** a build-script grep — find `func (sync|upload|save|persist|write|send|submit|push|commit|schedule|export|backup)[A-Z]...` declarations, then grep the tree for call sites; zero callers (excluding the definition + tests) = candidate. Emit `file:line: warning:`, bypass via a `// orphan-ok: <reason>` comment on the declaration.

**Origin:** Stuffolio 2026-06-08 — `syncLegacyDataToCloudKit` uploaded share data but had ZERO callers (beneficiaries got empty shares; `createShare` wrote only an empty root). Same pattern in `InsuranceProfile.scheduleItem` — the only writer of `scheduledItemIDs`, never wired to UI, so the coverage-alert exclusion that reads `isItemScheduled` was permanently inert → users got un-silenceable high-value alerts.

### Issue Rating Criteria

For every finding, use this table format sorted by Urgency (descending), then ROI:

| # | Finding | Confidence | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
|---|---------|------------|---------|-----------|--------------|-----|--------------|------------|--------|

#### Column Definitions

| Column | Meaning |
|--------|---------|
| Confidence | `verified` (code read + confirmed), `probable` (agent reported, not independently verified), `needs-runtime` (requires running the app to confirm) |
| Urgency | How time-sensitive — must it be fixed before release? |
| Risk: Fix | What could break when making the change |
| Risk: No Fix | Cost of leaving it — crash, data loss, user-visible bug |
| ROI | Return on effort (inverted — 🟠 = excellent, 🔴 = poor) |
| Blast Radius | Number of files the fix touches (e.g., `🟢 3 files`, `⚪ 1 file`). Do not use `<br>` tags. Count by grepping for callers/references before rating. |
| Fix Effort | Trivial / Small / Medium / Large |
| Status | Fixed / Documented / Deferred (reason) |

#### Finding Dependencies and Fingerprints

When creating findings, populate these optional fields where relationships are obvious:

- **`depends_on`/`enables`:** Workflow findings often chain -- a data loss at step 2 enables a corrupt display at step 5. If one fix must come before another, populate with finding IDs.
- **`pattern_fingerprint`/`grep_pattern`/`exclusion_pattern`:** Assign fingerprints for generalizable anti-patterns (e.g., `silent_data_narrowing`, `missing_error_recovery`, `unguarded_concurrent_write`).

#### Indicator Scale

| Indicator | General meaning | ROI meaning |
|-----------|----------------|-------------|
| 🔴 | Critical / high concern | Poor return — reconsider |
| 🟡 | High / notable | Marginal return |
| 🟢 | Medium / moderate | Good return |
| ⚪ | Low / negligible | — |
| 🟠 | Pass / positive | Excellent return |

#### Urgency Scale

- 🔴 CRITICAL — pre-launch blocker OR data loss / crash risk
- 🟡 HIGH — user-visible or stability risk; fix before release
- 🟢 MEDIUM — real issue; acceptable to schedule
- ⚪ LOW — nice-to-have; minimal impact

Do not use prose for ratings. Every finding gets a row in this table.

### Output

#### Fix Plan

After all findings, generate a Fix Plan grouped into these sections:

**1. Safe fixes (contained, only touching one or two files)**
Changes contained within the audited files. No behavioral changes outside the workflow.

| # | Finding | Files Changed | Urgency | ROI | Fix Effort |
|---|---------|---------------|---------|-----|------------|

**2. Cross-cutting fixes (touch shared code)**
Changes that affect models, protocols, or utilities used by other features.
Review for unintended side effects before approving.

| # | Finding | Files Changed | Urgency | ROI | Fix Effort | Side Effects |
|---|---------|---------------|---------|-----|------------|--------------|

**3. Requires design decision**
Multiple valid approaches. Needs user input before proceeding.

| # | Finding | Options | Urgency |
|---|---------|---------|---------|

**4. Deferred (no action needed now)**
Documented for future reference. No plan step generated.

| # | Finding | Urgency | Why Deferred |
|---|---------|---------|--------------|

**5. Shared utility extraction**
When multiple code paths duplicate the same logic, extract to a shared utility.

| # | Finding | Proposed Utility | Files Affected |
|---|---------|------------------|----------------|

**6. Out of scope**
Issues discovered here that belong to a different workflow.
List them with the affected workflow name so they can be fed into that workflow's audit.

| # | Finding | Affected Workflow | Urgency |
|---|---------|-------------------|---------|

#### Verification (auto-fix mode only)

After applying Safe fixes:
1. Build the project — if it fails, revert and move the fix to Cross-Cutting
2. Run tests touching modified files — if any fail, fix the test or revert the code fix
3. Report pass/fail counts in the Fix Plan output

#### Then

- If user chose **Auto-fix safe items**: apply Section 1 fixes, run Verification,
  then present Sections 2-3 for approval.
- If user chose **Review first**: present all sections for approval,
  then ask if the user wants to proceed with fixes.

#### Delivery

- If user chose **Display only**: output all tables in the conversation.
- If user chose **Report only**: write all tables to
  `.agents/research/[DATE]-[WORKFLOW]-audit.md`. Show only a one-line summary
  in the conversation (e.g., "Audit complete: 3 critical, 5 high, 2 medium.
  Report written to .agents/research/2026-03-06-backup-audit.md").
- If user chose **Display and report**: output all tables in the conversation
  AND write to file.

#### Deferred Items Registry

After each workflow audit, append deferred findings to `.agents/research/roundtrip-radar-deferred.md`. This accumulates across workflows so Step 2 rollup can consume them without re-reading all audit output.

Format:
```markdown
## [Workflow Name] — [Date]
| # | Finding | Urgency | Why Deferred |
|---|---------|---------|--------------|
| 1 | ... | 🟡 HIGH | Needs design decision |
```

---

## Fix Application Workflow

After presenting the Fix Plan, apply fixes in **waves**. Each wave is a phase from the Fix Plan. After each wave (including commits), **always** print the progress banner and auto-prompt for the next wave.

### Waves

| Wave | Fix Plan Section | Est. Time | Description |
|------|-----------------|-----------|-------------|
| 1 — Quick fixes | Safe fixes + tests | ~10-15 min | Small, contained fixes (one or two files each). Applied automatically. Tests written for each fix. |
| 2 — Shared code fixes | Cross-cutting fixes + tests | ~15-25 min | Fixes that touch code used by other features. Presented for your review first. Tests written for each fix. |
| 3 — Your call | Design decisions | ~5-15 min | Multiple valid approaches. You pick the direction for each item. |
| 4 — Same bug elsewhere | Pattern Sweep | ~5 min | Search the whole codebase for the same bugs found in this workflow. |
| 5 — Wrap up | Build + Test + Commit | ~5 min | Build both platforms, run tests, stage, commit. |

**Every fix must have a test.** Do not move to the next wave until tests for the current wave's fixes are written and compiling. The test verifies the fix works; without it, the fix is unverified code.

Skip empty waves (e.g., if no design decisions, go straight from Wave 2 to Wave 4).

If a "cross-cutting fix" turns out to need a design decision during implementation, reclassify it — ask the user via `AskUserQuestion` with the options, don't proceed without input.

### Wave 4: Pattern Sweep (after fixes, before commit)

After fixing findings in a workflow, scan the entire codebase for the same anti-pattern. This catches all instances at once instead of rediscovering them workflow-by-workflow.

For each pattern found and fixed in this workflow:
1. Build a grep query (e.g., `Double(` for raw price parsing, `hashValue` for unstable IDs)
2. Search all Sources/ files
3. Report: "Pattern X found in N additional files: [list]"
4. If fixes are trivial and isolated, apply them now. Otherwise, note for the next workflow.

### Progress Banner (CRITICAL — BLOCKING requirement)

**This is a BLOCKING requirement in Normal and Pre-Approved modes.** After EVERY wave and EVERY commit, your NEXT output MUST be the progress banner followed by the next-wave `AskUserQuestion`. Do not output anything else first. Do not wait for user input. Do not leave a blank prompt.

**Hands-Free mode exception:** In Hands-Free mode, the progress banner still prints, but the next-wave `AskUserQuestion` call is suppressed (per the Hands-Free Mode precedence rules above). Replace the AskUserQuestion with the Hands-Free completion message instead.

After completing each wave, **always** print:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Fix batch [N] of [total] complete: [plain description]
   [X] findings fixed, [Y] remaining, [Z] deferred

⏱  Next: Batch [N+1] — [plain description] (~[time estimate])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately ask: "Ready for the next batch?" with options:
- **Proceed (Recommended)** — Start the next batch of fixes
- **Commit first** — Commit current changes before continuing
- **Stop here** — End for now, resume later
- **Explain more** — Describe what the next batch will do before starting

### Between Workflows (MANDATORY transition)

After committing all fixes for a workflow, follow this exact sequence:

1. Print the **Workflow-Level Scorecard**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Roundtrip Radar Progress
   Workflows: [N]/[total] | Fixed: [X] | Deferred: [Y] | Patterns: [Z]
   Last: [workflow name] ([N] fixed)
   Next: [workflow name] (~[time estimate])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. Immediately ask: "Ready for the next workflow?" with options:
   - **Proceed (Recommended)** — Audit the next highest-priority workflow
   - **Stop here** — End session, save progress to memory
   - **Final rollup (Step 2)** — Cross-cutting analysis across all audited workflows

3. If user proceeds, show the one-line settings reminder (see Skill Introduction) then start the audit. Do NOT re-ask the 4 setup questions.

**Never leave the user with a blank prompt between workflows.**

### Pipeline Mode Behavior (Tier 2/3)

When running inside a Tier 2 or Tier 3 pipeline (detected via `tier` field in `.radar-suite/session-prefs.yaml`):

1. **On skill start:** Emit the pipeline-level progress banner (see `radar-suite-core.md` Pipeline UX Enhancements #1). If this is the first skill in the pipeline OR `experience_level` is Beginner/Intermediate, also emit the audit-only statement.
2. **On skill completion:** Emit a per-skill mini rating table marked "PRELIMINARY" (see Pipeline UX Enhancements #2). Then emit the pipeline-level progress banner showing this skill as complete.
3. **Within-skill workflow banners** (above) are still emitted normally in addition to the pipeline-level banners.

### short_title Requirement (v2.1)

Every finding MUST include a `short_title` field (max 8 words). This is the human-scannable label used in pipeline banners, pre-capstone summaries, and ledger output.

Example: `short_title: "Backup drops attachment external storage"`

All finding ID references in output (tables, banners, summaries) use the format: `RS-NNN (short_title)`.

---

## Step 2: Roll-Up

Run after all per-workflow audits are complete.

### Data Sources (read these — do NOT ask the user to paste)

1. `.agents/research/roundtrip-radar-deferred.md` — the accumulator written by every per-workflow audit (see § Deferred Items Registry). Contains every deferred finding across the session.
2. `.radar-suite/ledger.yaml` — filter to entries where `skill: roundtrip-radar` AND the session timestamp is in this rollup's scope (default: all sessions since the last `Step 2 rollup` ledger entry, or all sessions if none).
3. Each per-workflow handoff's `axis_summary` block — load from the in-memory session state for the current run.

Identify cross-cutting patterns across the loaded entries.

### Output

1. List any pattern that appears in 2+ workflows (e.g., `@Query` without predicates, hash-based IDs)
2. For each pattern, state which workflows are affected and whether a shared fix exists
3. Rank the top 5 remaining deferred items by impact using the Issue Rating table format

Deliver results according to the user's output preference from Step 1.

---

## Cross-Skill Handoff

Roundtrip Radar complements **data-model-radar** (model layer), **ui-path-radar** (navigation paths), **ui-enhancer-radar** (visual quality), and **capstone-radar** (ship readiness). Findings from one skill inform the others.

### On Completion — Write Handoff

After completing a workflow audit (or Step 2 rollup), write/update `.agents/ui-audit/roundtrip-radar-handoff.yaml`:

```yaml
source: roundtrip-radar
date: <ISO 8601>
project: <project name>
workflows_audited: <count>

# File timestamps — enables staleness detection by consuming skills
# If a file changed after the audit, affected issues may need re-verification
file_timestamps:
  <file path>: "<ISO 8601 mod date>"
  # one entry per unique file referenced in issues

for_ui_path_radar:
  # Data issues that may have navigation/entry-point implications
  suspects:
    - entry_point: "<button/link that triggers this workflow>"
      finding: "<data safety issue found>"
      file: "<file:line>"
      question: "<does the UI reflect this data issue?>"
      group_hint: "<optional, e.g. 'data_loss', 'silent_failure'>"

for_ui_enhancer_radar:
  # Dead code, orphaned UI, or views with broken data backing
  suspects:
    - view: "<view file>"
      finding: "<data issue that affects this view>"
      action: "verify data binding or remove dead UI"
      group_hint: "<optional batching suggestion>"

for_capstone_radar:
  # Critical/high findings that affect ship readiness
  blockers:
    - finding: "<description>"
      urgency: "<CRITICAL|HIGH>"
      workflow: "<workflow name>"
      group_hint: "<optional batching suggestion>"

cross_cutting_patterns:
  # Patterns found across multiple workflows — useful for all skills
  - pattern: "<e.g., Double() price parsing>"
    workflows_affected: ["Backup", "Edit Item", "CSV Import"]
    status: "fixed" | "deferred"
    group_hint: "<optional, e.g. 'price_parsing', 'id_handling'>"
  # Example: collection narrowing pattern
  # - pattern: "array.first passed to multi-item API"
  #   workflows_affected: ["Add Item (Photo)", "Stuff Scout"]
  #   status: "fixed"
  #   group_hint: "collection_narrowing"
  # Example: bridge parity pattern
  # - pattern: "ScoutSession consumed by 3 functions, 1 reads 3/6 fields"
  #   workflows_affected: ["Stuff Scout", "Add Item (Photo)"]
  #   status: "fixed"
  #   group_hint: "bridge_parity"
```

### File Timestamps

For each unique file path referenced across all issues, record its modification date at audit time:

```bash
# Get file mod date (macOS)
stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "<file path>"
```

This enables consuming skills to detect **staleness** — if a file changed after the audit, affected issues may need re-verification before acting on them.

### Group Hints

Optional field suggesting how consuming skills might batch related issues:
- Issues with the same `group_hint` are candidates for a single fix task
- Consuming skills are free to ignore hints and group differently
- Common hints: `data_loss`, `silent_failure`, `round_trip_gap`, `error_handling`, `concurrency`, `collection_narrowing`, `bridge_parity`

**Automatic:** This file is always written so other audit skills can pick up where this one left off. No user action needed.

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, before returning from this skill:
1. List files in `.radar-suite/` (and `.agents/research/` if used).
2. Move any stale single-use handoffs (`RESUME_PHASE_*.md`, `RESUME_*.md` except `NEXT_STEPS.md`, `*-v[0-9]*.md`) to `.radar-suite/archive/superseded/`.
3. Confirm Class 1 persistent-state files (`ledger.yaml`, `session-prefs.yaml`) are in-place rewrites — not dated or versioned.
4. Confirm Class 2 handoff files are overwrites, not appends.

This prevents `.radar-suite/` from accumulating stale prose artifacts across runs.

### Write to Unified Ledger (MANDATORY)

After writing the handoff YAML, also write findings to `.radar-suite/ledger.yaml` following the Ledger Write Rules in `radar-suite-core.md`:

1. Read existing ledger (or initialize if missing)
2. Record this session (timestamp, skill name, build)
3. For each finding: check for duplicates, assign RS-NNN ID if new, set `impact_category`, compute `file_hash`
4. Write updated ledger

**Impact category mapping for roundtrip-radar findings:**
- Data loss on round-trip (fields dropped, values corrupted) → `data-loss`
- Silent failure (error swallowed, operation appears to succeed but doesn't) → `data-loss`
- Crash on workflow completion → `crash`
- Workflow dead end or broken promise → `ux-broken`
- Degraded workflow (works but lossy or confusing) → `ux-degraded`
- Cross-cutting patterns (e.g., price parsing) → classify per finding

### On Startup — Read Ledger & Handoffs (MANDATORY)

Before Step 0 (or Step 1 if skipping discovery), read the unified ledger and ALL companion handoff YAMLs:

```
Read .radar-suite/ledger.yaml (if exists) — check for existing findings to avoid duplicates
Read .agents/ui-audit/data-model-radar-handoff.yaml (if exists)
Read .radar-suite/time-bomb-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-path-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-enhancer-radar-handoff.yaml (if exists)
Read .agents/ui-audit/capstone-radar-handoff.yaml (if exists)
```

**Ledger check:** If the ledger contains findings for workflows you're about to audit, note their RS-NNN IDs. When you find the same issue, update the existing finding instead of creating a new one.

**Regression check:** For any `fixed` findings in the ledger whose `file_hash` no longer matches the current file, flag for re-verification per the Regression Detection protocol in `radar-suite-core.md`.

**Parse `for_roundtrip_radar` sections.** Each companion can direct findings to this skill. Look for:
- `for_roundtrip_radar.suspects[]` — workflows or data paths another skill flagged as potentially broken
- `for_roundtrip_radar.priority_workflows[]` — workflows another skill wants audited first

If found, incorporate as **priority targets** in workflow selection. These are not pre-confirmed findings — verify each one independently.

**What each companion provides:**
- data-model-radar — model gaps that may cause data loss in specific workflows
- ui-path-radar — dead ends and broken promises suggest workflows to prioritize
- ui-enhancer-radar — visual issues in views that may have data backing problems
- capstone-radar — priority workflows from ship readiness grading

**Specific incorporation rules:**
- Dead-end buttons from ui-path-radar → check the workflow behind that button
- Orphaned views from ui-path-radar → verify the data path exists
- Views flagged by ui-enhancer → check if the data binding is correct before suggesting visual changes
- Model gaps from data-model-radar → trace through the workflow that creates/edits that model

If not found, proceed normally.

---

## End Reminder

After every wave/commit/workflow: print progress banner → `AskUserQuestion` → never blank prompt.
