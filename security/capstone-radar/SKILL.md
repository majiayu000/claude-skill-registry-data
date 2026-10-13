---
name: capstone-radar
description: 'Unified A-F grading and ship/no-ship decisions for the 6-skill radar family (5 companions + capstone). Aggregates handoffs from data-model, ui-path, roundtrip, time-bomb, and ui-enhancer; owns 5 grep-reliable domains; tracks velocity; celebrates improvements. Triggers: "capstone radar", "can I ship", "grade codebase", "/capstone-radar".'
version: 3.2.0  # axis-split grading + staleness decay + dependency graph + tier awareness + hygiene backlog + time-bomb consumption + impact-based organization
author: Terry Nyberg
license: Apache-2.0
inherits: radar-suite-core.md
---

# Capstone Radar

Capstone Radar is the **aggregator + gap filler** for the 6-skill radar family (5 companions + capstone). It consumes findings from 5 companion skills, runs its own scans for 5 domains the companions don't cover, grades everything on one unified scale, and makes the ship/no-ship decision.

It does NOT:
- Re-scan domains already covered by companion skills
- Dispatch Axiom auditor agents
- Produce separate reports for domains companions already cover

## Usage

| Command | Description |
|---------|-------------|
| `/capstone-radar` | Full analysis — checks everything and reads companion handoffs |
| `/capstone-radar quick` | Quick check — own domains only, ignores companion results |
| `/capstone-radar report` | No scanning, re-grade from existing handoff files only |
| `/capstone-radar diff` | Compare against previous audit — show resolved/new issues |
| `--trust-all` | Override staleness decay -- treat all companion handoffs as Fresh |
| `--show-suppressed` | Show findings suppressed by known-intentional entries |

---

## Diff Command

**Audit comparison** — compare current codebase against a previous audit to show what changed.

### Usage

```
/capstone-radar diff
/capstone-radar diff 2026-03-15
```

### How It Works

1. **Find previous audit** — Read the most recent (or specified date) `.agents/research/*-capstone-audit.md`
2. **Parse previous findings** — Extract all issues from the GRADES_YAML block and findings tables
3. **Re-check each finding:**
   - Read the file at the reported line number
   - Check if the problematic pattern still exists
   - Classify as: ✅ RESOLVED, 🔴 STILL OPEN, 📁 FILE CHANGED
4. **Scan for new issues** — Quick grep scan for new violations not in previous report
5. **Output diff summary**

### Output Format

```
Audit Diff: 2026-03-15 → 2026-03-29

Summary:
  ✅ Resolved: 8 issues fixed since last audit
  🔴 Still Open: 3 issues remain
  🆕 New: 2 new issues detected
  📁 Changed: 4 files modified (may need re-verification)

Grade Trend:
  Overall: B [83] → B+ [87] ↑
  Code Hygiene: B- → A- ↑
  Security Basics: A → A (stable)
  Test Health: C → C+ ↑

Resolved Issues:
| # | Finding | Was | File | Resolved By |
|---|---------|-----|------|-------------|
| 1 | TODO marker in production | 🟡 HIGH | CloudSyncManager.swift:142 | Commit abc123 |

Still Open:
| # | Finding | Urgency | File | Age |
|---|---------|---------|------|-----|
| 1 | Force unwrap in error path | 🟡 HIGH | BackupManager.swift:89 | 14 days |

New Issues:
| # | Finding | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
```

### When to Use

- **Pre-release check** — "What's changed since our last audit?"
- **Progress tracking** — Verify issues are being resolved over time
- **Regression detection** — Catch new issues introduced since last audit

### Velocity Tracking

If 3+ previous audits exist, show trend line:
```
Grade Velocity (last 5 audits):
  Build 21: C+ [78]
  Build 22: B- [80]
  Build 23: B  [84]
  Build 24: B+ [87]
  Build 25: B+ [88] ← current

Trend: Improving (+2.5 pts/build avg)
Projection: A- by Build 28 at current rate
```

---

## Skill Introduction (MANDATORY — run before anything else)

On first invocation, ask the user three questions in a single `AskUserQuestion` call:

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "Which audit mode?"**
- **Full (Recommended)** — Full analysis — checks everything and reads findings from other audits you've run
- **Quick** — Quick check — only looks at its own areas, ignores other audit results
- **Report only** — No scanning, just re-grade from existing handoff files

**Question 3: "Include user impact explanations?"**
- **No (default)** — Table only. Findings speak for themselves.
- **Yes** — After the table, each finding gets a 3-line explanation: what's wrong, the fix, and how a user experiences it before/after.

Can also be toggled mid-session with `--explain` / `--no-explain`. See `radar-suite-core.md § Experience-Level Output Rules` for format and rules.

**Experience-adapted explanations for Capstone Radar:**

- **Beginner**: "Capstone Radar is the final check before your app goes to the App Store. It combines results from 5 other audit tools (if you've run them) with its own security, testing, and code quality checks, then gives your whole app a letter grade and tells you if it's safe to ship. Think of it as the building inspector who reviews all the specialist reports plus checks the things no one else covered."

- **Intermediate**: "Capstone Radar aggregates findings from 5 companion skills (data-model-radar, ui-path-radar, roundtrip-radar, ui-enhancer-radar, time-bomb-radar) and adds its own scans for security, test health, code hygiene, dependencies, and build health. It grades 11 weighted inputs on one scale (5 own + 5 consumed + 1 cross-domain synthesis), tracks trends across runs, and makes a ship/no-ship recommendation."

- **Experienced**: "Aggregator + gap filler for the radar family. Consumes 5 companion handoffs, owns 5 grep-reliable domains, unified A-F grading across 11 weighted inputs, velocity tracking, risk heatmap, ship/no-ship decision."

- **Senior/Expert**: "5 owned + 5 consumed + 1 cross-domain = 11 weighted domains. Velocity. Heatmap. Ship/no-ship."

Store the experience level as `USER_EXPERIENCE` and apply to ALL output for the session.

---

## Shared Patterns

See `radar-suite-core.md` for: Tier System, Pipeline UX Enhancements, Table Format, Plain Language Communication, Work Receipts, Contradiction Detection, Finding Classification, Audit Methodology, Context Exhaustion, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Implementation Sort Algorithm, short_title requirement.

## Tier Awareness (MANDATORY -- read before any scanning)

Read `.radar-suite/session-prefs.yaml` for the `tier` field. Capstone behavior adapts based on the active tier:

### Tier 3 (Full Pipeline)

All 5 companion skills are expected. If a handoff is missing, treat it as an error (not "not audited"):

```
ERROR: data-model-radar handoff missing. Full pipeline requires all 5 companions.
Options: [Re-run data-model-radar / Continue without it (grade will be partial)]
```

Before starting own scans, emit the **Pre-Capstone Summary** (see `radar-suite-core.md` Pipeline UX Enhancements #5):
- Read all 5 handoff files
- Emit the consolidated findings table (skill, count, critical/high/medium/low breakdown)
- Show top findings by urgency with `RS-NNN (short_title)`
- Ask: "Review summary before capstone grading? [Enter to continue / Review details]"

### Tier 2 (Targeted Pipeline)

Read `tier_skills` from session prefs to know which skills were in the subset. Only expect handoffs for those skills. For skills not in the subset:
- Mark as "not in scope" (not "not audited")
- Grade is scoped to audited domains only
- Emit: "Partial audit: [N] of 5 skills ran. Grade reflects audited domains only. Missing coverage: [list of excluded skills]."

Weight redistribution: redistribute missing domain weights proportionally to audited domains (same as existing missing-handoff logic).

### Tier 1 / No Tier / Standalone

Existing behavior. Missing handoffs show "Not audited -- run [skill-name] for coverage."

---

## Pre-Scan Startup (MANDATORY — before Step 1)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here. (Note: companion findings already excluded at the companion level; capstone only filters its own domain scans through this protocol.)

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

3. **Experience-level auto-apply (capstone-radar local):** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply all output rules from `radar-suite-core.md § Experience-Level Output Rules`.

---

## Step 1: Project Metrics

Collect:

1. **File counts** — `Glob pattern="**/*.swift"` (exclude Tests, Pods, .build, DerivedData)
2. **LOC estimate** — file count x 150, or `wc -l` for accuracy
3. **Architecture** — detect MVVM/MVC/TCA by scanning for ViewModel, Controller, Reducer
4. **Persistence layer** — SwiftData, Core Data, GRDB, UserDefaults, Realm
5. **Test infrastructure** — Swift Testing vs XCTest, unit test count, UI test count
6. **Build number** — read from CLAUDE.md (search for "Current Version" or build number), or from Info.plist
7. **Team detection** — `git shortlog -sn --no-merges | wc -l`. Store as `TEAM_SIZE`.

Ensure output directories exist: `mkdir -p .agents/research .agents/ui-audit`

Print one-line summary:
```
Project: {files} Swift files (~{loc} LOC) | {arch} | {persistence} | Tests: {unit}/{ui} | Build: {number} | Contributors: {count}
```

---

## Step 2: Previous Audit Check

```
Glob pattern=".agents/research/*-capstone-audit.md"
Glob pattern=".agents/research/*-codebase-audit.md"
```

If previous reports exist, parse ALL `GRADES_YAML` HTML comment blocks for velocity tracking. Build an array of dated snapshots sorted by date. Store as `HISTORY`.

---

## Step 3: Companion Handoff Consumption (Tier-Aware)

Read the unified ledger and handoff files. **Which files to read depends on the active tier** (see Tier Awareness above). In Tier 2, read only handoffs for skills listed in `tier_skills`. In Tier 3, read all 5. In Tier 1/standalone, read whatever exists.

```
Read .radar-suite/ledger.yaml (if exists) — unified cross-skill finding store
Read .agents/ui-audit/data-model-radar-handoff.yaml (if exists)
Read .radar-suite/time-bomb-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-path-radar-handoff.yaml (if exists)
Read .agents/ui-audit/roundtrip-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-enhancer-radar-handoff.yaml (if exists)
```

**Ledger integration:** When the ledger exists, use it as the primary source of cross-skill findings. Handoff YAMLs provide per-skill detail (serialization coverage, cross-cutting patterns) that the ledger doesn't store. Capstone should reference findings by RS-NNN ID when available.

For each handoff found:
1. Parse `for_capstone_radar.blockers[]` — extract `finding` and `urgency` (CRITICAL or HIGH)
2. **Backward compat:** Also accept `for_release_ready_radar.blockers[]` key
3. Parse companion-specific extras:
   - data-model-radar: `serialization_coverage` (model field coverage stats)
   - roundtrip-radar: `cross_cutting_patterns[]` (patterns affecting multiple workflows)
4. Record which companions were found vs missing

**Score consumed domains:** Start at 95 (generous baseline — companion ran a full audit and only escalated the worst items). Deduct:
- Per CRITICAL blocker: **-15**
- Per HIGH blocker: **-8**
- Floor at 0

**Missing handoffs (tier-dependent messaging):**
- **Tier 3:** "ERROR: [skill] handoff missing. Full pipeline requires all 5 companions." (see Tier Awareness)
- **Tier 2:** If skill was in `tier_skills`, treat as error. If not, mark "Not in scope" (expected absence).
- **Tier 1 / standalone:** "Not audited -- run [skill-name] for coverage."

In all cases, weight is redistributed proportionally to audited domains.

Print companion status:
```
Companions: data-model-radar [found/missing] | ui-path-radar [found/missing] | roundtrip-radar [found/missing] | time-bomb-radar [found/missing] | ui-enhancer-radar [found/missing]
```

**Skip this step if mode = Quick.**

### Companion Handoff Quality Assessment

When a companion handoff is found, check its `audit_depth` and `_verified` flags (if present):

- `audit_depth: full` + all targets `_verified: true` → Full credit (start at 95, deduct per blocker)
- `audit_depth: partial` or some targets `_verified: false` → Reduced credit (start at 85, deduct per blocker). Note in report: "Partial audit — [domain] grade is provisional."
- No depth/verified flags (older handoff format) → Treat as partial. Note: "Handoff from older skill version — depth not verified."

**Do not give full credit for unverified companion work.** A handoff that says "backup verified, CSV not checked" should not produce an A for the Model Layer domain. The unverified targets represent unknown risk.

### Companion Handoff Staleness Decay

After assessing quality, calculate staleness for each companion handoff:

```
staleness_score = (days_since_handoff * 0.3) + (commits_since_handoff * 0.1)
```

Where:
- `days_since_handoff` = calendar days since the handoff's `timestamp` field
- `commits_since_handoff` = output of `git rev-list --count <handoff_commit>..HEAD` (use `git log --oneline --since="<timestamp>"` if commit hash unavailable)

| Score | Label | Behavior |
|-------|-------|----------|
| 0-2 | Fresh | Full trust -- use handoff as-is |
| 2-5 | Aging | Trust grades, but spot-check HIGH findings (read the file, verify pattern still exists) |
| 5-10 | Stale | Downgrade companion grades by one letter. Spot-check all CRITICAL + HIGH findings. |
| 10+ | Expired | Ignore handoff entirely. Recommend re-running the companion skill. |

**Freshness summary** (print in companion status output):
```
Companion freshness:
  data-model-radar: Fresh (1 day, 3 commits)
  ui-path-radar: Aging (8 days, 12 commits)
  roundtrip-radar: Stale (22 days, 47 commits) — grades downgraded by one letter
  time-bomb-radar: Fresh (2 days, 5 commits)
  ui-enhancer-radar: Expired (35 days, 89 commits) — handoff ignored, re-run recommended
```

**Spot-check protocol** (for Aging and Stale handoffs):
1. Read the finding's file at the cited line range
2. Check if the pattern still exists (grep the finding's work receipt pattern if available)
3. If pattern gone → mark finding as `possibly-resolved (stale handoff)` and exclude from grade calculation
4. If pattern still present → mark as `re-verified` and keep the finding

**`--trust-all` flag:** Overrides staleness calculation. All companions treated as Fresh regardless of age. Use when you know nothing has changed since the last audit.

**Stale/Expired companions** are flagged in the "Next Steps" section of the report.

---

## Step 3.5: Axis Classification Consumption (MANDATORY — after companion handoffs, before risk-ranking)

> **New in v1.1 (axis framework).** Every companion handoff now includes an `axis_summary` block and every finding includes an `axis` field. Capstone splits findings by axis before grading: only axis_1 findings count toward the A-F grade. axis_2 and axis_3 findings land in a separate Hygiene Backlog section.

### What to read

For each companion handoff found in Step 3, read:

1. **`axis_summary`** (top-level block) — counts by axis
2. **`checks_performed`** (top-level block) — what the companion scanned
3. **`axis`** (per-finding field) — classification for each finding
4. **`before_after_experience.audience`** (per-finding field) — surface in the report

### What to do

1. **Split findings by axis into two buckets:**
   - **fix_before_shipping** — all findings where `axis == axis_1_bug`
   - **hygiene_backlog** — all findings where `axis in (axis_2_scatter, axis_3_dead_code, axis_3_smelly)`

2. **Verify schema gate compliance.** For each finding in either bucket, confirm it has:
   - A non-empty `better_approach` field
   - A file:line citation matching regex `[A-Za-z0-9_/+.-]+\.swift:\d+` in the `better_approach` body
   - A `pattern_citation_lookup` entry in `verification_log`
   - A `before_after_experience` with `audience` set

   Findings failing the gate are still displayed but are tagged `coaching incomplete` and excluded from the top-10 prioritized list. This makes bad coaching visible rather than silently dropped.

3. **Aggregate `checks_performed`** across all companions into a single "Audit Coverage" block:
   ```
   Audit Coverage:
     source_roots: Sources/
     files scanned: 588 (ui-path), 588 (roundtrip), 120 (capstone own)
     patterns ran: reachability_trace, whole_file_scan, branch_enumeration, pattern_citation_lookup
     patterns skipped: source_root_introspection (single-root project)
   ```

4. **Count `rejected_no_citation`** across all handoffs. If any radar rejected findings at the gate, surface this prominently — it means the radar had candidate findings it could not coach.

### Grade impact rule (CRITICAL)

**Only axis_1_bug findings affect the A-F grade.** axis_2 and axis_3 findings are NOT counted for grading. The grade cap rules from `radar-suite-core.md` apply only to axis_1 findings:

- CRITICAL axis_1 findings cap grade at C
- HIGH axis_1 findings cap grade at B+

A codebase with 0 axis_1 findings but 50 axis_2 findings can still grade A. Hygiene debt does not block shipping.

### Backward compatibility

Handoffs from older radar versions (pre-v1.1) lack the `axis_summary` block and the per-finding `axis` field. For these:

1. Treat all findings as `axis_1_bug` (the pre-v1.1 default behavior)
2. Note in the "Audit Coverage" section: `"ui-enhancer-radar handoff is pre-axis (v1.0.x); all findings counted as axis_1"`
3. Do not retroactively infer axis; old handoffs are preserved as-is

---

## Step 3.6: Risk-Ranking (MANDATORY — before own domain scans)

Before running grep patterns, determine where to go deep vs quick. The default behavior is to run all grep patterns with equal effort — but some domains have more risk than others based on context.

### Check These Signals

**Signal 1: Prior findings.**
Read `HISTORY` from Step 2. If previous audits scored a domain below B, go deep on verification for that domain this time. Also check memory for known issues (e.g., prior session found test health concerns → verify test patterns more carefully).

**Signal 2: Companion handoff gaps.**
If a companion handoff flagged issues that touch an owned domain (e.g., data-model-radar found security-relevant patterns), escalate that owned domain to deep verification.

**Signal 3: Codebase size signals.**
If Step 1 found >500 Swift files, Security Basics grep will produce many candidates. Plan for heavier verification time on that domain. If test-to-source ratio is below 0.2, Test Health needs deep investigation, not just file counting.

### Risk-Ranking Output

Before Step 4, print:

```
Risk Ranking for Own Domains:
  DEEP VERIFY:
    - [domain] (reason: [signal])
    - [domain] (reason: [signal])
  STANDARD:
    - [domain]
    - [domain]
  LOW RISK:
    - [domain]
```

**Deep verify** means: read every grep candidate in context (20+ lines), classify each as CONFIRMED/FALSE_POSITIVE/INTENTIONAL. Don't report counts — report classified findings.

**Standard** means: read a sample of grep candidates (top 5 per pattern), classify those, extrapolate. Label as `(sampled)` in the report.

**Low risk** means: report counts with spot-check of top 3 candidates. Label as `(spot-checked)` in the report.

---

## Step 4: Own Domain Scans

Run grep-based scans for the 5 domains capstone owns. Apply Verification Rule (Step 5) to every hit. **Follow the risk-ranking from Step 3.6** — deep-verify domains go first and get full candidate classification.

### Shared Grep Patterns

**Code Hygiene** `grep-sufficient`:
```
Grep pattern="// TODO|// FIXME|// HACK|// XXX" glob="**/*.swift" output_mode="count"
Grep pattern="as!" glob="**/*.swift"
Grep pattern="try!" glob="**/*.swift"
```
Also check file sizes: `Glob pattern="**/*.swift"` then read line counts for files that appear large. Flag files >1000 lines.

**Test Health** `grep-sufficient`:
```
Grep pattern="import Testing" glob="**/*Test*.swift" output_mode="count"
Grep pattern="import XCTest" glob="**/*Test*.swift" output_mode="count"
Grep pattern="Thread\.sleep|sleep\(" glob="**/*Test*.swift"
Glob pattern="**/*Tests.swift"
Glob pattern="**/*Test.swift"
```
Calculate test-to-source ratio: test files / (total swift files - test files).

**Security Basics** `grep-sufficient`:
```
Grep pattern="(api[_-]?key|secret[_-]?key|password|token)\s*[:=]\s*[\"'][^\"']+[\"']" glob="**/*.swift" -i
Grep pattern="UserDefaults.*\.(password|token|secret|apiKey)" glob="**/*.swift" -i
Grep pattern="http://(?!localhost|127\.0\.0\.1)" glob="**/*.swift"
```

**Dependency Health** `grep-sufficient`:
```bash
stat -f "%Sm" -t "%Y-%m-%d" Package.resolved 2>/dev/null || echo "no Package.resolved"
```
```
Grep pattern="\.exact\(|\.upToNextMajor\(|\.upToNextMinor\(|from:" path="Package.swift" output_mode="content"
```
Count packages in Package.resolved.

**Build Health** `grep-sufficient`:
```bash
find . -name "*.xcscheme" -not -path "*/.build/*" | wc -l
```
```
Grep pattern="targets?:" path="Package.swift" output_mode="content"
```

### Verification Template (MANDATORY for own domain scans)

Before grading each owned domain, produce this table:

```
| Pattern | Grep Run? | Hits | Classified | Confirmed | False Positive | Receipt |
|---------|-----------|------|------------|-----------|----------------|---------|
| TODO/FIXME | ? | | | | | |
| try! | ? | | | | | |
| as! | ? | | | | | |
| hardcoded secrets | ? | | | | | |
| http:// URLs | ? | | | | | |
```

Rules:
- Every pattern in the scan list must appear in this table
- `?` means the grep wasn't run yet — cannot grade until all are filled
- Hits ≠ Findings. Every hit must be classified (Confirmed / False Positive / Intentional)
- The grade comes from Confirmed count, not Hits count
- If Hits > 0 but Classified = 0, the domain was not actually audited

### Per-Domain Scoring

Start at **100 points**. Deduct per CONFIRMED finding:

| Severity | HIGH Conf | MED Conf | LOW Conf |
|----------|-----------|----------|----------|
| CRITICAL | -15 | -10 | -3 |
| HIGH | -8 | -5 | -1 |
| MEDIUM | -3 | -2 | 0 |
| LOW | -1 | -1 | 0 |

---

## Step 5: Verification Rule

Grep patterns produce candidates, NOT confirmed issues. Before reporting:

1. **Read the flagged file** — minimum 20 lines of context
2. **Check structural context** — pattern may be safe in its actual scope
3. **Classify:** CONFIRMED, FALSE_POSITIVE, or INTENTIONAL
4. **Never report grep counts as issue counts** — classify each hit
5. **Only CONFIRMED findings appear in the report**

**Common false positives:**
- `try!` in test setup code — acceptable in tests
- `http://` in XML namespaces or comments — not an endpoint
- `sleep()` in test helpers for async settling — may be intentional
- `TODO` markers that reference completed work — stale comments
- `as!` in exhaustive switch cases — compiler-guaranteed safe
- Hardcoded "password" in UI label strings — not a credential

---

## Step 6: Cross-Domain Correlation

### 6.1 Risk Heatmap by File

Collect ALL file paths from ALL findings (own 5 domains + companion handoffs). Count domain appearances per file. Report files appearing in **3+ domains**:

```
Risk Heatmap — Files with findings in 3+ domains:
  {file1}  — {domain1}, {domain2}, {domain3} ({N} domains)
  {file2}  — {domain1}, {domain2}, {domain3} ({N} domains)

These {N} files account for {X}% of all findings.
```

### 6.2 Team Enrichment

If `TEAM_SIZE` > 1:
- For each heatmap file, run `git log --format="%an" --since="30 days ago" -- {file} | sort -u` to find recent contributors
- Add ownership info: `{file} — {N} domains, {M} contributors this month, {owner or "no clear owner"}`

### 6.3 Cross-Cutting Patterns

If roundtrip-radar handoff includes `cross_cutting_patterns[]`, incorporate them. Flag patterns that affect 3+ workflows.

---

## Step 6.5: Dependency Graph Construction

Build a dependency graph across ALL findings (own + companion) for `--sort implement` ordering.

### Input

Scan all findings for `depends_on` and `enables` fields. These may be populated by individual skills (within-skill dependencies) or inferred here (cross-skill dependencies).

### Auto-Inference Rules (cross-skill)

Apply these rules to infer dependencies that individual skills could not see:

1. **Requires/provides:** If Finding A's description says "requires X" (e.g., "requires Codable conformance") and Finding B adds X (e.g., "add Codable to Item"), then B `enables` A.
2. **Structural before behavioral:** If two findings touch the same file and one is structural (model change, protocol addition, enum case) while the other is behavioral (UI update, export logic, validation), the structural finding `enables` the behavioral one.
3. **Type/protocol reference:** If a finding references a type or protocol that another finding introduces, the introducing finding is a dependency.

### Algorithm

1. **Build DAG:** Create directed edges from each `depends_on` entry and each `enables` entry. Auto-inferred edges are marked `inferred: true`.
2. **Topological sort:** Order findings so dependencies come before dependents. Within a topological level, break ties by urgency (descending).
3. **Cycle detection:** If the graph contains cycles:
   - Warn the user: "Cycle detected: RS-014 → RS-016 → RS-014 — falling back to urgency sort for these items"
   - Remove cycle members from the DAG and sort them by urgency instead
   - Non-cycle findings remain topologically sorted
4. **Output dependency chains** in the report:
   ```
   Fix RS-014 first (enables RS-015, RS-016)
   Fix RS-003 and RS-007 (independent, parallel-safe)
   ```

### When to Use

This graph is consulted when the user selects `--sort implement`. It also informs the "relationship-aware reporting" in Step 10 (root cause findings first, symptoms indented beneath).

---

## Step 7: Grading

### Domain Weights

The 11 weighted inputs sum to 100%. Cross-Domain Risk is a synthesized domain derived from the heatmap in Step 6.1 — not a separately-audited area.

| Domain | Source | Weight |
|--------|--------|--------|
| Code Hygiene | Own scan | 10% |
| Test Health | Own scan | 15% |
| Security Basics | Own scan | 15% |
| Dependency Health | Own scan | 5% |
| Build Health | Own scan | 5% |
| Model Layer | data-model-radar handoff | 10% |
| Navigation/UX | ui-path-radar handoff | 10% |
| Data Safety | roundtrip-radar handoff | 10% |
| Time Bombs | time-bomb-radar handoff | 5% |
| Visual Quality | ui-enhancer-radar handoff | 10% |
| Cross-Domain Risk | Correlation analysis (synthesized) | 5% |

**Why these weights:** Data Safety dropped from 15% → 10% to make room for Time Bombs (5%) — both domains are about data integrity across time, so the combined 15% allocation matches the prior single-domain weight for Data Safety alone. A cascade-delete crash from time-bomb is functionally equivalent to a round-trip data loss from roundtrip-radar for shipping decisions; splitting them at 10/5 lets the grade distinguish active-flow bugs (roundtrip) from aged-data bugs (time-bomb) without overweighting the combined area.

**Weight redistribution:** When domains are unaudited (missing companion handoff), divide their total weight proportionally among audited domains. Example: if Data Safety (10%) and Visual Quality (10%) are missing, remaining 80% becomes 100%. Code Hygiene's 10% becomes 10/80 = 12.5%.

### Grade Honesty Rules

**1. Label the scope.** The overall grade line must state how many domains were audited:
```
Overall: B+ [87] (6/11 weighted inputs audited — 5 companion domains missing)
```
Not just `Overall: B+ [87]`.

**2. Label the depth.** Each owned domain grade must state its verification depth:
```
Code Hygiene: A [96] (deep-verified — all candidates classified)
Test Health: A [94] (sampled — top 5 per pattern classified)
Build Health: A+ [100] (spot-checked — 3 candidates verified)
```

**3. Distinguish hygiene from quality.** The 5 owned domains are surface hygiene checks. They catch "did you leave a hardcoded password" but NOT "does the backup restore lose 7 fields." When companion domains are missing, add this disclaimer:
```
Note: This grade covers hygiene domains only. Logic bugs, data safety,
navigation issues, and visual quality are not assessed without companion
skill handoffs. Prior audits found [N] bugs in unaudited domains.
```
Check `HISTORY` for the count of prior findings in unaudited domains. If no history, say "unknown number of bugs may exist."

**4. Partial companion credit.** When a companion handoff has `audit_depth: partial` or `_verified: false` on some targets, the consumed domain grade is provisional. Mark it:
```
Model Layer: B+ [88] (provisional — companion audit was partial)
```

### Cross-Domain Risk Scoring

Start at 100. Deduct:
- **-5** per file appearing in 3+ domains (from risk heatmap)
- **-3** per cross-cutting pattern affecting 3+ workflows
- **-5** per correlated domain pair (e.g., security finding + test gap in same file)

### Grade Scale

| Grade | Score | Grade | Score | Grade | Score |
|-------|-------|-------|-------|-------|-------|
| A+ | 97-100 | B+ | 87-89 | C+ | 77-79 |
| A | 93-96 | B | 83-86 | C | 73-76 |
| A- | 90-92 | B- | 80-82 | C- | 70-72 |
| | | D+ | 67-69 | D | 63-66 |
| | | D- | 60-62 | F | 0-59 |
| **I** | **n/a** | | | | |

### Incomplete (I) Grade

Overrides the numeric score for ship-blocking, irreversible risks:

| Trigger | Source |
|---------|--------|
| Hardcoded production credentials | Security Basics (own) |
| Unencrypted secrets in UserDefaults/plist | Security Basics (own) |
| CRITICAL blocker from any companion | Companion handoff |
| Confirmed data loss/corruption path | Companion or own |

If ANY domain is Incomplete, overall grade is `I (Incomplete)`.

### Overall Grade

Weighted average using domain weights (after redistribution), mapped to grade scale.

---

## Step 8: Velocity + Regressions

### Velocity Tracking

If `HISTORY` has previous snapshots, compare current grades to each:

```
Velocity — Grade Over Time:
  Code Hygiene:     C  -> B- -> B+  (3 audits, improving)
  Security Basics:  A  -> A  -> A   (stable)
  Test Health:      C  -> C  -> C+  (3 audits, slowly improving)

  Overall: B -> B+ (trending up)
```

If 3+ data points, add projection: "At this rate, you'll hit overall A- by [estimate]."

### Build-Over-Build Comparison

If current and previous audits have build numbers:

```
Build {prev} -> Build {current}:
  New issues: {N}
  Resolved: {N}
  Grade: {prev_grade} -> {current_grade}
```

### Celebrate Improvements

Diff current vs previous audit. Highlight domains that improved by >=1 letter grade OR >=10 points:

```
Improvements since last audit:
  Code Hygiene: B- -> A- (resolved 8 TODO markers)
  Test Health: C -> B- (added 12 test files)
  Data Safety: D+ -> B (roundtrip-radar found and fixed 6 data loss bugs)
```

Always show improvements BEFORE findings. Positive reinforcement matters.

### Regressions Tied to Git History

For each finding NOT present in the previous audit:

```
REGRESSION: {finding description}
  File: {file:line}
  Introduced: commit {hash} "{message}" ({date})
```

If `TEAM_SIZE` > 1, also show author and reviewer (if from a PR):
```
  Author: {name}
  PR: #{number} (if detectable from commit message)
```

Run `git log -1 --format="%H %s %an %ai" -- {file}` for each regression file.

---

## Step 9: Ship Recommendation

> **⚠️ Grades are NECESSARY, NOT SUFFICIENT.** The companion skills + own scans
> read source code; they are blind to the "compiles + passes tests + looks fine in
> the simulator, but bombs on the real surface" bug class — dead code never called,
> CloudKit **production-only** failures, and **platform-parity** gaps (works on iOS,
> broken on macOS). A clean unified grade does NOT prove the app actually works for
> a real user. Before issuing SHIP, confirm a **manual real-surface smoke test** has
> been run since the last code change: every feature once on **macOS + a real iOS
> device + a real iCloud/Production account**. If it hasn't, label the result
> "SHIP — pending real-surface smoke test" and make that the top blocker. (Origin:
> a B-grade SHIP would have shipped empty CloudKit shares to every user, 2026-06-08.)

| Recommendation | Criteria |
|----------------|----------|
| **SHIP** | No CRITICALs, <=2 HIGHs, overall B- or above, no Incompletes, **AND real-surface smoke test confirmed done** |
| **CONDITIONAL SHIP** | No CRITICALs, 3-5 HIGHs, overall C+ or above, no Incompletes |
| **DO NOT SHIP** | Any Incomplete, OR any CRITICAL, OR >5 HIGHs, OR overall C or below |
| **SHIP — pending smoke test** | Grade qualifies but the manual macOS + real-device + real-iCloud smoke test isn't confirmed since the last change |

Any Incomplete = automatic **DO NOT SHIP** — no exceptions.

Format:

```
## Ship Recommendation: [SHIP / CONDITIONAL SHIP / DO NOT SHIP]

### Blockers (must fix before release)
1. [Issue] — LOE: Xh | File: path:line

### Advisories (fix soon after release)
1. [Issue] — LOE: Xh | File: path:line

**Estimated total blocker LOE:** X hours
```

### Companion Coverage Notice

If any companion skills were not run:

```
Coverage gaps — these domains were NOT audited:
  Model Layer: Run data-model-radar for coverage
  Data Safety: Run roundtrip-radar for coverage
  Time Bombs: Run time-bomb-radar for coverage
  Navigation/UX: Run ui-path-radar for coverage
  Visual Quality: Run ui-enhancer-radar for coverage

Ship recommendation is based on {N}/11 weighted inputs. Run missing companions for full confidence.
```

---

## Step 10: Output + Follow-up

### Write Report

**Before writing:** Per the Artifact Lifecycle rules in `radar-suite-core.md` (Class 3: Dated Snapshot), list any existing `.agents/research/*-capstone-audit.md` files. Move them to `.agents/research/archive/superseded/` (create the directory if missing) before writing the new snapshot. Only ONE live capstone audit file exists at the top level at any time.

Write to `.agents/research/YYYY-MM-DD-capstone-audit.md`. Write sections as generated.

**Report sections:**

1. **Header** — date, build number, mode, companions found/missing
2. **Project metrics** — files, LOC, architecture, persistence, tests, contributors
3. **Grade summary line** — `**Overall: B+** (CodeHygiene A- [91] | Security A [95] | ...)`
4. **GRADES_YAML** — machine-readable in HTML comment:

```html
<!-- GRADES_YAML
build: 25
date: 2026-03-23
overall: 87
code_hygiene: 92
test_health: 78
security_basics: 95
dependency_health: 88
build_health: 90
model_layer: 85
navigation_ux: null
data_safety: 72
visual_quality: null
cross_domain_risk: 80
-->
```

`null` = domain not audited. Previous reports with old 13-category format are still parseable for velocity — map old domain names where possible, ignore the rest.

5. **Improvements** (if previous audit exists) — celebrate what got better
6. **Velocity chart** (if 2+ previous audits) — grade trends per domain
7. **Ship recommendation** — SHIP / CONDITIONAL / DO NOT SHIP with blockers
8. **Companion coverage notice** (if any missing)
9. **Risk heatmap** — files in 3+ domains
10. **Per-domain sections** — grade, score trail, strengths, CONFIRMED issues with Issue Rating Tables
11. **Regressions** — new issues traced to commits
12. **Test coverage gaps** — untested source files, especially those appearing in findings
13. **Top 10 prioritized issues** — composite: `(Urgency x 3) + (Risk x 2) + (ROI x 2) + (1/LOE)` (axis_1 only)
14. **Fix Before Shipping** — axis_1_bug findings with full coaching (see below)
14a. **Hygiene Backlog** — axis_2 and axis_3 findings (see below)
14b. **Audit Coverage** — what was checked across all radars (see below)
15. **Impact-organized findings** — all findings grouped by impact category (see below)
16. **Next steps** — which companion radars to run for unaudited domains

### Axis-Split Output Format (v1.1)

**Section 14 — Fix Before Shipping (axis_1 only)**

This section lists every axis_1_bug finding from all companion handoffs plus capstone's own scans. The A-F grade reflects ONLY this section. Format:

```markdown
## Fix Before Shipping

> Audience legend: 👤 end_user | 👓 code_reader | 🔧 future_maintainer
> All findings in this section are user-facing bugs that should be fixed before release.

### #1 — CSV import freezes main thread on large files
**Source:** roundtrip-radar | **Axis:** axis_1_bug | **Audience:** 👤 end_user
**File:** Sources/Features/ImportExport/ImportCSVView.swift:142

**Before:** User taps Import CSV, app freezes 10-30s with no feedback, some users force-quit thinking the app crashed.
**After:** User sees progress bar with row count, can cancel mid-import, UI stays responsive.

**Current approach:** Import call runs synchronously on @MainActor from onTapGesture. CPU-bound parsing loop blocks main thread.
**Minimum fix:** Wrap in Task { @MainActor in ... }, move parsing to Task.detached(priority: .userInitiated), add progress overlay + cancel button.
**Better approach:** Follow the pattern at Sources/Managers/CloudSyncManager.swift:104-112 which shows both the @MainActor bridge and Task.detached in adjacent lines. Extract an AsyncImportOperation type if there are 2+ similar imports.
**Tradeoffs:** Apply when the operation is >200ms or involves file I/O on large inputs. Don't apply for <50ms operations.

| Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort |
|---------|-----------|--------------|-----|--------------|------------|
| 🔴 CRITICAL | 🟢 Medium | 🔴 Critical | 🟠 Excellent | ⚪ 1 file | Small |
```

Each finding in this section displays the full coaching schema. The rating table is **10-column** (capstone adds the Source column to the standard 9 — see § Issue Rating Format below).

**Section 14a — Hygiene Backlog (axis_2 + axis_3)**

This section does NOT affect the grade. It is a separate list organized by axis sub-type:

```markdown
## Hygiene Backlog

> Audience legend: 👤 end_user | 👓 code_reader | 🔧 future_maintainer
> These findings do not block shipping. Fix opportunistically when touching the affected files.

### Scatter (axis_2) — correct code, reorganize for clarity

#### S1 — Empty states handled 500 lines apart in LegacyWishesView.swift
**Source:** ui-path-radar | **Axis:** axis_2_scatter | **Audience:** 👓 code_reader
**File:** Sources/Features/LegacyWishes/Views/LegacyWishesView.swift:120,480,640
**Severity:** rolling_hygiene

**Before:** Developer reading the file has to scroll between 3 regions to trace state machine.
**After:** Single enum ViewState at top of file, single switch at top of body.

**Better approach:** Follow pattern at Sources/Views/Navigation/NavigationTypes.swift:21 (String-backed enum with per-case computed properties).

### Dead Code (axis_3_dead_code) — unreachable branches

#### D1 — Unreachable empty-state branch in SomeListView.swift
**Source:** ui-path-radar | **Axis:** axis_3_dead_code | **Audience:** 🔧 future_maintainer
**File:** Sources/Views/SomeListView.swift:NNN
**Severity:** backlog_hygiene

**Before:** Future developer assumes the branch handles empty collections, wastes time tracing it.
**After:** Branch deleted, comment at upstream filter site documents why downstream views don't see empty.

### Smelly (axis_3_smelly) — reachable but poorly justified

[similar format]
```

Hygiene findings use a simpler format (no 10-column rating table) since they don't block shipping and don't need severity ranking. Each finding still includes its coaching and file:line citation.

**Section 14b — Audit Coverage**

```markdown
## Audit Coverage

Source roots scanned: Sources/
Files scanned across radars:
  - ui-path-radar: 588 Swift files
  - roundtrip-radar: 588 Swift files (20 workflows traced)
  - capstone-radar own domains: 120 files

Patterns executed:
  - reachability_trace: 42 traces (3 findings reclassified from axis_1 to axis_3_dead_code)
  - whole_file_scan: 18 scans (2 findings reclassified from axis_1 to axis_2_scatter)
  - branch_enumeration: 8 #if blocks enumerated
  - pattern_citation_lookup: 57 lookups (47 hits, 10 generic fallbacks)
  - source_root_introspection: 1 (single-root project confirmed)

Patterns skipped: none

Findings rejected at schema gate: 0
  (If >0: "3 findings dropped for missing citation — listed under 'Coaching Incomplete' below")
```

This section answers "what was checked" so a clean audit run is not ambiguous.

### Impact-Based Finding Organization (v3.0)

When the unified ledger (`.radar-suite/ledger.yaml`) exists, section 14 presents ALL findings in a single 10-column table (the standard 9 plus a Source column showing provenance). The table is sorted by impact category (Crash Risk → Data Loss → UX Broken → UX Degraded → Polish → Hygiene), then by Urgency within each category:

```markdown
| # | Finding | Source | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
|---|---------|--------|---------|-----------|--------------|-----|--------------|------------|--------|
| | **Crash Risk** | | | | | | | | |
| 1 | Cascade delete on archived items | time-bomb | 🔴 CRITICAL | ... | ... | ... | ... | ... |
| 2 | Force unwrap on nil photo data | roundtrip | 🟡 HIGH | ... | ... | ... | ... | ... |
| | **Data Loss** | | | | | | | |
| 3 | CSV export drops Room and UPC | roundtrip | 🟡 HIGH | ... | ... | ... | ... | ... |
| 4 | InsuranceProfile not in backup | data-model | 🟡 HIGH | ... | ... | ... | ... | ... |
| | **UX Broken** | | | | | | | |
| 5 | Settings > Export has no back button | ui-path | 🟡 HIGH | ... | ... | ... | ... | ... |
```

Category separator rows (bold text, empty rating columns) divide the table visually without breaking the single-table rule. The Source column replaces the old `(skill-name)` suffix that was appended to finding text.

### Relationship-Aware Reporting (v3.0)

When the ledger contains finding relationships, the impact-organized report groups related findings:

```
## Crash Risk (2 findings)
RS-002 [CRITICAL] Cascade delete on archived items (time-bomb-radar)
  └─ symptom: RS-014 [HIGH] Force unwrap on nil photo data (roundtrip-radar)
     Fix RS-002 first — RS-014 may resolve automatically.
```

**Root cause findings** are always listed first in their impact group. Symptoms are indented beneath their root cause with a note that fixing the root cause may resolve them.

**Auto-inference:** On capstone startup, scan ledger for relationship patterns per the Finding Relationships protocol in `radar-suite-core.md`. Create links automatically and present for user confirmation.

### Fix Batching Options (v3.0)

After the impact-organized findings, offer fix organization:

```
How would you like to organize fixes?
1. **By crash risk (Recommended)** — highest severity first across all skills
2. **By blast radius** — smallest changes first for quick wins
3. **By user journey** — group findings affecting the same workflow
4. **By skill** — fix all data-model issues, then time-bomb, etc. (legacy)
```

### Test Coverage Gap Analysis

Map test files against source files:

1. Glob `**/*Tests.swift` and `**/*Test.swift`
2. Extract tested type names from test file names (e.g., `ItemViewModelTests.swift` → `ItemViewModel`)
3. Compare against source files
4. Flag untested files that ALSO appear in findings (high risk + no tests = worst combination)

```
Test Coverage Gaps:
  {type} ({N} files, 0 tests) — appears in {domain} findings
  {type} ({N} files, 0 tests) — HIGH risk (companion flagged data issues)
```

### Issue Rating Format

Capstone-radar uses a **10-column table** with a Source column added to the standard 9. This is the only skill that adds Source -- it's the aggregator, so provenance matters. All other radar skills use the standard 9-column table.

| # | Finding | Source | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
|---|---------|--------|---------|-----------|--------------|-----|--------------|------------|--------|
| 1 | CSV export drops Room and UPC | roundtrip | 🟡 HIGH | ⚪ Low | 🟡 High | 🟠 Excellent | 🟢 2 files | Small |
| 2 | InsuranceProfile not in backup | data-model | 🟡 HIGH | ⚪ Low | 🟡 High | 🟢 Good | 🟢 3 files | Medium |
| 3 | TODO marker in production path | capstone | 🟢 MEDIUM | ⚪ Low | 🟢 Medium | 🟠 Excellent | ⚪ 1 file | Trivial |

**Source column values:** Use short names -- `capstone`, `data-model`, `ui-path`, `roundtrip`, `ui-enhancer`, `time-bomb`. For findings from capstone's own scans, use `capstone`.

**Single table rule still applies.** The Source column eliminates the need for separate tables per companion skill. ALL findings -- from own scans and all companion handoffs -- go into ONE table. The impact-based organization (v3.0) groups rows by impact category within this single table; the Source column shows where each finding originated.

**Blast Radius:** Always include the number of files the fix touches (e.g., `3 files`, `1 file`). Count by grepping for callers/references before rating.

### Indicator Scale

| Indicator | General meaning | ROI meaning |
|-----------|----------------|-------------|
| CRITICAL | Critical / high concern | Poor return |
| HIGH | High / notable | Marginal return |
| MEDIUM | Medium / moderate | Good return |
| LOW | Low / negligible | — |
| PASS | Pass / positive | Excellent return |

### Time-Boxed Fix List

After the ship decision, ask: "How much time do you have for fixes?"

Sort findings by (grade impact / fix effort). Output a prioritized list that fits the time budget:

```
You have {N} hours. Here are the {M} fixes that move your grade the most:
1. {fix} ({domain} {old_grade} -> {new_grade}) — {effort}, {files} file(s)
2. {fix} ({domain} {old_grade} -> {new_grade}) — {effort}, {files} file(s)
...
```

**Every fix includes tests.** When listing fix effort, include test writing time. A "Small" fix that needs tests is "Small + tests." When the user applies fixes (directly or via companion skills), verify tests were added. Untested fixes are unverified fixes.

### Write Handoff

Write `.agents/ui-audit/capstone-radar-handoff.yaml`:

```yaml
source: capstone-radar
date: <ISO 8601>
project: <project name>
build: <build number>
recommendation: "ship" | "conditional" | "no-ship"
overall_grade: "<letter grade>"
overall_score: <numeric>

# File timestamps — enables staleness detection by consuming skills
file_timestamps:
  <file path>: "<ISO 8601 mod date>"
  # one entry per unique file referenced in findings

for_roundtrip_radar:
  priority_workflows:
    - domain: "<e.g., Data Safety>"
      grade: "<letter>"
      reason: "<why this domain scored low>"
      group_hint: "<optional, e.g. 'data_safety', 'error_handling'>"

for_ui_path_radar:
  priority_areas:
    - domain: "<e.g., Navigation/UX>"
      grade: "<letter>"
      reason: "<specific issues found>"
      group_hint: "<optional batching suggestion>"

for_ui_enhancer_radar:
  priority_views:
    - domain: "<e.g., Visual Quality>"
      grade: "<letter>"
      reason: "<specific gaps>"
      group_hint: "<optional batching suggestion>"

for_data_model_radar:
  priority_models:
    - domain: "<e.g., Model Layer>"
      grade: "<letter>"
      reason: "<specific model issues>"
      group_hint: "<optional batching suggestion>"

for_time_bomb_radar:
  priority_targets:
    - domain: "<e.g., Time Bombs>"
      grade: "<letter>"
      reason: "<specific aged-data risk patterns>"
      group_hint: "<optional, e.g. 'cascade_delete', 'cache_expiry', 'background_accumulation'>"
```

### File Timestamps

For each unique file path referenced across all findings, record its modification date:

```bash
stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "<file path>"
```

Enables consuming skills to detect **staleness** — if a file changed after the audit, affected findings may need re-verification.

### Group Hints

Optional field for batching related issues. Common hints:
- `security_basics` — secrets, credentials, http URLs
- `test_health` — missing tests, test gaps
- `code_hygiene` — TODOs, force unwraps, large files
- `build_health` — scheme issues, dependency problems

**Automatic:** This file is always written so other audit skills can pick up where this one left off. No user action needed.

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, capstone is the LAST phase of an audit and is responsible for final cleanup:
1. List files in `.radar-suite/` and `.agents/research/`.
2. Move any stale single-use handoffs (`RESUME_PHASE_*.md`, `RESUME_*.md` except `NEXT_STEPS.md`, `*-v[0-9]*.md`) to `.radar-suite/archive/superseded/`.
3. Verify only ONE live `*-capstone-audit.md` exists at the top of `.agents/research/`; older ones must already be in `archive/superseded/` from the Step 10 "Write Report" archive rule.
4. On successful completion, delete `.radar-suite/checkpoint.yaml` per the Checkpoint & Resume rule.
5. Write `.radar-suite/NEXT_STEPS.md` (overwrite, no dates, no phase numbers in filename) containing the post-capstone fix session prompt. This is the ONLY single-use handoff file capstone is allowed to create.
6. Confirm Class 1 persistent-state files (`ledger.yaml`, `session-prefs.yaml`) are in-place rewrites — not dated or versioned.

This prevents `.radar-suite/` from accumulating stale prose artifacts across runs.

### Write to Unified Ledger (MANDATORY)

After writing the handoff YAML, also write findings to `.radar-suite/ledger.yaml` following the Ledger Write Rules in `radar-suite-core.md`:

1. Read existing ledger (or initialize if missing)
2. Record this session (timestamp, skill name, build)
3. For each finding: check for duplicates, assign RS-NNN ID if new, set `impact_category`, compute `file_hash`
4. Write updated ledger

**Capstone-specific ledger behavior:**
- Capstone primarily aggregates findings from companion skills -- most findings should already be in the ledger
- New findings discovered during capstone's own analysis (e.g., cross-domain contradictions) get new RS-NNN IDs
- Capstone updates `impact_category` if its cross-skill view reveals a more accurate classification
- Capstone does NOT overwrite companion skill findings -- it only adds or updates

### Bug-Echo Handoff Prompt (Open → Fixed transitions)

After writing the ledger, capstone walks each finding whose status changed from `open` to `fixed` during this session and applies the Bug-Echo Handoff protocol from `radar-suite-core.md`. Summary of the per-transition decision:

1. Read finding's `pathway` field.
   - Empty → set `bug_echo_status: none`, skip prompt.
   - Non-empty → continue.
2. Check session flag `bug_echo_suppress_session` in `.radar-suite/session-prefs.yaml`.
   - True → set `bug_echo_status: suppressed`, skip prompt.
   - False → emit prompt (see core spec for exact format).
3. On user response:
   - **Yes:** print manual invocation hint with seed (RS-NNN + pathway + fix-site). Set `bug_echo_status: pending`. When user returns results, write `echo_result` and update `bug_echo_status: completed`. Render `**Echo:** <result>` in the Detail block of the impact-organized report.
   - **No:** set `bug_echo_status: declined`. Render `**Echo:** declined` in Detail block.
   - **Skip all:** set session flag `bug_echo_suppress_session: true`. Set this finding's `bug_echo_status: suppressed`. Subsequent Fixed transitions this session skip silently.

**When to walk Fixed transitions:** Capstone walks them at Step 10 (Output + Follow-up), after the ledger write completes and after the impact-organized report is rendered. This ensures the prompts come after the user has seen the grade and report — not interleaved with grading output.

**Findings already at `completed`/`declined`/`none`/`suppressed`:** Skip. The protocol fires once per Open → Fixed transition.

**Pathway-empty findings:** Companion radars are responsible for filling `pathway` at finding-emission time (see "Discipline" subsection in core spec). Capstone does NOT backfill missing pathways — that would require capstone to understand each domain's anti-pattern shapes, which it does not.

### Follow-up Options

After presenting the report, offer:

- **Run missing companions** — list which companion radars would improve coverage
- **Plan blockers only** — create implementation plan for CRITICAL + HIGH items
- **Plan all items** — comprehensive roadmap
- **No plan needed**

---

## Permission Modes

### Normal Mode
- Read any file without asking.
- Write report to `.agents/research/` without asking.
- Run bash commands (git log, stat, find) without asking.

### Hands-Free Mode
**Guarantees no blocking prompts.** Only uses Read, Grep, Glob. No Bash, no Edit, no Write. When complete:
```
Hands-free audit complete. Analysis ready.
  Deferred: Report file writing, git history analysis.
  Reply to continue with supervised steps.
```

---

## Experience-Level Adaptation

Adjust ALL output (grades, findings, recommendations, domain summaries) based on `USER_EXPERIENCE`:

- **Beginner**: Explain what each grade means and why it matters. Define terms. Use analogies for severity.
- **Intermediate**: Standard terminology, explain non-obvious findings.
- **Experienced** (default): Concise grades + key findings. No definitions. Focus on what needs action.
- **Senior/Expert**: Grades + file:line references only. Skip domain descriptions. Just the data.

---

## Step Progress Banner (CRITICAL — BLOCKING requirement)

**After EVERY step and EVERY commit, your NEXT output MUST be the progress banner followed by the next-step `AskUserQuestion`. Do not output anything else first. Do not leave a blank prompt.**

The skill has **10 numbered top-level steps** (the user-facing structure). Three steps have substep refinements (3 has substeps 3.5 and 3.6; 6 has substep 6.5). Substeps print using substep notation so the `/10` denominator stays stable.

**Banner template (top-level step completion):**

```
Step [N] of 10 complete: [step name]

Next: Step [N+1] — [step name] (~[time estimate])
```

**Banner template (substep completion):**

```
Step [N] (substep [.5/.6]) of 10 complete: [substep name]

Next: Step [N] (substep [next]) — [substep name] (~[time estimate])
   or → Step [N+1] if this was the last substep
```

Step time estimates:
| Step | Name | Est. Time |
|------|------|-----------|
| 1 | Project Metrics | ~1 min |
| 2 | Previous Audit Check | ~1 min |
| 3 (with substeps 3.5/3.6) | Companion Handoff Consumption + Axis Classification + Risk-Ranking | ~3-4 min total |
| 4 | Own Domain Scans | ~3-5 min |
| 5 | Verification | ~2-5 min |
| 6 (with substep 6.5) | Cross-Domain Correlation + Dependency Graph Construction | ~3-4 min total |
| 7 | Grading | ~1 min |
| 8 | Velocity + Regressions | ~2 min |
| 9 | Ship Recommendation | ~1 min |
| 10 | Output + Follow-up | ~3 min |

---

## Companion Skills (6-Skill Family — 5 companions + capstone)

| Skill | Unique Role |
|-------|-------------|
| data-model-radar | Are your @Model definitions correct? |
| ui-path-radar | Can users reach every feature? |
| roundtrip-radar | Does data survive the full journey? |
| time-bomb-radar | Will this code crash after 30+ days of aged data? |
| ui-enhancer-radar | Does it look and feel right? |
| **capstone-radar** (this skill) | Can you ship? Unified grade + decision. |

**Recommended audit order:**
1. data-model-radar (foundation — model layer)
2. ui-path-radar (navigation paths)
3. roundtrip-radar (active data flows)
4. time-bomb-radar (aged data flows — chains from roundtrip findings)
5. ui-enhancer-radar (visual quality)
6. capstone-radar (unified grade + ship decision)

Capstone is both the **entry point** ("what should I audit?") and the **exit point** ("can I ship?"). The other radars are the deep work in between.

---

## End Reminder

After every step/commit: print progress banner → `AskUserQuestion` → never blank prompt.

**Grade honesty:** State N/11 weighted inputs audited (5 own + 5 companion + 1 synthesized). State verification depth (deep/sampled/spot-checked). No clean A+ from surface greps alone.

**Risk-ranking:** Produce Step 3.6 risk-ranking table before Step 4. Verify riskiest domains first.
