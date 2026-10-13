---
name: data-model-radar
description: 'Audits SwiftData/Core Data model layer for field completeness, serialization gaps, relationship integrity, semantic ambiguity, dead fields, and migration safety. Finds model-layer bugs that manifest as workflow bugs. Triggers: "audit models", "model radar", "/data-model-radar".'
version: 2.3.0  # Domain 3a/3b cross-context mutation and stale object checks
author: Terry Nyberg
license: Apache-2.0
allowed-tools: [Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion]
inherits: radar-suite-core.md
metadata:
  tier: execution
  category: analysis
---

# Data Model Radar

> Audits the @Model layer for completeness, consistency, and round-trip integrity. Finds model-layer bugs before they manifest as workflow bugs.

**Anti-shortcut rule:** Do not claim a domain is "clean" without evidence. Every domain grade must cite specific files read and patterns checked. "No dead fields detected from structural analysis" without grepping is a failing grade for the auditor, not a passing grade for the model.

## Quick Commands

| Command | Description |
|---------|-------------|
| `/data-model-radar` | Full audit across all model-layer domains (9 numbered + 2 sub-domains under Domain 3 + Domain 8 delegated to time-bomb-radar) |
| `/data-model-radar [ModelName]` | Audit a single model in depth |
| `/data-model-radar models` | Show all models with risk ranking (no audit, discovery only) |
| `/data-model-radar serialization` | Domain 2 only — backup/export coverage |
| `/data-model-radar relationships` | Domain 3 only — cascade rules, orphan risk |
| `/data-model-radar migration` | Domain 6 only — schema version safety |
| `/data-model-radar dead-fields` | Domain 5 only — unused model fields |
| `/data-model-radar time-bombs` | Domain 8 only — deferred operations on aged data |
| `/data-model-radar status` | Show audit progress |
| `--show-suppressed` | Show findings suppressed by known-intentional entries |
| `--accept-intentional` | Mark current finding as known-intentional (not a bug) |

## Overview

Data Model Radar audits the foundation your app is built on — the data models. Every UI bug, every sync failure, every round-trip data loss traces back to a model-layer decision. This skill finds those issues at the source instead of waiting for them to surface in workflows.

| Domain | What It Finds | Est. Time |
|--------|--------------|-----------|
| **1. Field Completeness** | Missing fields, enum gaps, semantic holes | ~3-5 min |
| **1.5 Computed Properties** | Business logic bugs in computed properties (nil chains, fallback defaults, currency math) | ~5-10 min |
| **2. Serialization Coverage** | Backup/export fields that don't round-trip | ~10-20 min |
| **3. Relationship Integrity** | Cascade rules, inverse relationships, orphan risk | ~3-5 min |
| **3a. Cross-Context Mutation** | @Model param mutated in a manager's own context = crash | ~3-5 min |
| **3b. Stale Object After Cross-Context Save** | Manager saves in own context; caller's @Model reference goes stale | ~3-5 min |
| **4. Semantic Clarity** | nil vs zero ambiguity, missing type distinctions | ~2-3 min |
| **5. Field Usage Mapping** | Dead fields (no UI reads), phantom fields (UI shows, model doesn't store) | ~10-20 min |
| **6. Migration Safety** | Schema versions, VersionedSchema coverage, migration plan gaps | ~5-10 min |
| **7. Cross-Model Consistency** | Identifier strategy, naming conventions, shared pattern violations | ~3-5 min |
| **7.5 Near-Duplicate Detection** | Models sharing 70%+ fields that should be consolidated | ~3-5 min |
| **8. Time Bombs** (delegated to time-bomb-radar) | Deferred operations on aged data — cascade deletes, cache expiry, scheduled side effects | ~5-10 min |

---

## Skill Introduction (MANDATORY — run before anything else)

**This section replaces `radar-suite-core.md § Session Setup` for the data-model-radar entry point.** Do NOT also run core's 4-question Session Setup — its questions are consolidated below. Other radar-suite skills entered via their own SKILL.md files have their own equivalent sections.

On first invocation, ask the user all four setup questions in a single `AskUserQuestion` call:

**Question 1: "What's your experience level with Swift/SwiftUI?"**
- **Beginner** — New to Swift. Plain language, analogies, define terms on first use.
- **Intermediate** — Comfortable with SwiftUI basics. Standard terms, explain non-obvious patterns.
- **Experienced (Recommended)** — Fluent with SwiftUI. Concise findings, no definitions.
- **Senior/Expert** — Deep expertise. Terse, file:line only, skip explanations.

**Question 2: "Table format?"**
- **Full tables (Recommended)** — 8-column Issue Rating Tables
- **Compact tables** — 3-column with details below

**Question 3: "Fix handling?"**
- **Auto-fix safe items (Recommended)** — Apply isolated, low-blast-radius fixes automatically. Present cross-cutting fixes and design decisions for approval first.
- **Review first** — Present all findings with ratings, then ask before making any changes. Fixes still happen — you just approve each wave first.
- **Batch mode** — Approve all fixes in each wave at once.

**IMPORTANT:** All three fix modes lead to fixes. "Review first" means the user sees the plan before code changes — it does NOT mean "skip fixes and jump to handoff." After presenting findings, ALWAYS offer to fix them regardless of which mode was selected.

**Question 4: "Would you like a brief explanation of what this skill does?"**
- **No, let's go (Recommended)** — Skip explanation, proceed to audit.
- **Yes, explain it** — Show a 3-5 sentence explanation adapted to the user's experience level (see below), then proceed.

Store as: `USER_EXPERIENCE`, `TABLE_FORMAT`, `FIX_MODE`. Apply to ALL output for session, per `radar-suite-core.md § Experience-Level Output Rules`. Also persist these to `.radar-suite/session-prefs.yaml` per `radar-suite-core.md § Session Persistence`.

**Experience-adapted explanations for Data Model Radar:**

- **Beginner**: "Data Model Radar checks the blueprints your app is built on — the data models that define what an 'item' or 'warranty' or 'photo' looks like in the database. Think of it like inspecting a building's foundation before checking the rooms. If the blueprint says a house has 10 rooms but only 8 have doors, people can't reach 2 rooms. Similarly, if your Item model has 47 fields but your backup only saves 40, those 7 fields are lost forever when someone restores from backup. This skill finds those gaps."

- **Intermediate**: "Data Model Radar audits your @Model classes for field completeness (missing enums, semantic holes), serialization coverage (backup/export round-trip gaps), relationship integrity (cascade rules, orphan risk), nil-vs-zero ambiguity, dead fields (defined but never read), migration safety (schema versions), and cross-model consistency. It finds model-layer bugs that would otherwise surface as workflow bugs across multiple features."

- **Experienced**: "Audits @Model layer across 9 numbered domains (1, 1.5, 2, 3, 4, 5, 6, 7, 7.5) plus 2 sub-domains (3a cross-context mutation, 3b stale object) plus Domain 8 (time bombs, delegated to time-bomb-radar). Covers field completeness, computed properties, serialization coverage, relationship integrity, cross-context safety, semantic clarity, usage mapping, migration safety, cross-model consistency, near-duplicate detection. Outputs issue rating tables with fix plans. Findings feed roundtrip-radar as suspects."

- **Senior/Expert**: "Model audit: fields → computed → serialization → relationships (+3a/3b cross-context) → semantics → usage → migration → consistency → near-dupes → time-bombs (delegated). Rating tables + fix plans."

Store the experience level as `USER_EXPERIENCE` and apply to ALL output for the session.

**User impact explanations:** Can be toggled at any time with `--explain` / `--no-explain`. When enabled, each finding gets a 3-line companion explanation (what's wrong, fix, user experience before/after). See the shared rating system doc for format and rules. Store as `EXPLAIN_FINDINGS` (default: false).

**Subsequent models (if auditing multiple):** Show one-line reminder:
```
Using: [Beginner] mode, [Auto-fix] or [Review first], [Display only]. Type "adjust" to change, or press Enter to continue.
```

---

## Shared Patterns

See `radar-suite-core.md` for: Rules Summary, Tier System, Pipeline UX Enhancements, Table Format, Rating Table Gate, Plain Language Communication, Work Receipts, Contradiction Detection, Finding Classification, Audit Methodology, Context Exhaustion, Progress Banner, Issue Rating Tables, Handoff YAML schema, Known-Intentional Suppression, Pattern Reintroduction Detection, Experience-Level Output Rules, Implementation Sort Algorithm, short_title requirement.

## Pre-Scan Startup (MANDATORY — before any domain scan)

1. **Known-intentional suppression:** Run the protocol in `radar-suite-core.md § Known-Intentional Suppression`. Core owns this — do not restate the steps here.

2. **Pattern reintroduction detection:** Run the protocol in `radar-suite-core.md § Pattern Reintroduction Detection`. Core owns this.

3. **Experience-level auto-apply (data-model-radar local):** If `USER_EXPERIENCE` = Beginner, auto-set `EXPLAIN_FINDINGS = true` and default sort to `impact`. If Senior/Expert, default sort to `effort`. Apply output rules from `radar-suite-core.md § Experience-Level Output Rules`.

---

## Audit Depth

Each domain can be run at two depths:

| Depth | When to Use | What It Does |
|-------|-------------|-------------|
| **Quick** | Triage, low-risk models, <10 fields | Structural analysis — read the model, check patterns, report what's visible |
| **Deep** | High-risk models, >20 fields, multiple serialization targets | Grep every field, read every serialization target, verify every claim |

**Default:** Deep for models with Risk = High. Quick for Low risk. Ask for Medium risk.

**The difference matters.** A quick audit of Domain 5 says "no obvious dead fields." A deep audit greps each of the 55 fields and proves it. Quick audits must label their grades with `(quick)` so the handoff distinguishes verified from unverified.

---

## Risk-Ranking (MANDATORY — before any verification)

**Do not start verifying until you have ranked where to go deep.** The default behavior is to verify whatever is easiest to read (usually backup code) and skip what's harder (CSV import, CloudKit mapping). Risk-ranking inverts this: verify riskiest first, not easiest first.

### Six Signals (Check in Order)

**Signal 1: Prior findings exist.**
Before choosing depth, check:
- Memory files for prior audit results mentioning this model
- `.agents/ui-audit/*-handoff.yaml` for companion skill findings
- `.agents/research/*-audit.md` for previous capstone/codebase audit notes

If prior sessions found CSV import loses fields, go deep on CSV — not backup. This is the strongest signal and the cheapest to collect.

**Signal 2: Asymmetry between input and output.**
Count fields on both sides of any serialization target. If export writes 27 columns but import reads 11, the 16-field gap is where data loss hides. Go deep on the smaller side (the reader, not the writer).

**Signal 3: Recently changed code.**
```bash
git log --since="3 months ago" -p -- Sources/Models/{Model}.swift | grep "^+.*var " | head -20
```
New fields are most likely to be missing from serialization structs. Cross-reference these against backup/CSV/CloudKit code.

**Signal 4: Multiple systems touch the same data.**
Count how many systems read/write each field. A field serialized across backup + CSV + CloudKit + UI = 4 consumers = high risk. A field only in one view = low risk.

**Signal 5: Money, identity, and relationships.**
Fields with `InCents`/`Price`/`Value`/`Cost`, identity fields (`cloudSyncID`, `ownerUserRecordID`), and `@Relationship` properties have higher consequences when gaps exist.

**Signal 6: The "looks clean" feeling (meta-signal).**
When you feel confident about a domain without having produced its required artifact — that IS the signal to stop and do the work. Confidence without evidence is the #1 predictor of shallow work.

### Risk-Ranking Output

Before starting Domain 1, produce a risk-ranking table:

```
Risk Ranking for [Model]:
  GO DEEP:
    1. CSV import (Signal 2: 27 export vs 11 import — 16-field asymmetry)
    2. Price fields (Signal 5: 6 currency fields across 3 serialization targets)
    3. Fields added since Build 24 (Signal 3: 4 new fields in last 3 months)
  QUICK OK:
    4. Backup (Signal 1: prior audit found full coverage)
    5. Relationship integrity (low change rate, all cascade)
  NOT APPLICABLE:
    6. CloudKit (no CKRecord mapping code found)
```

This table determines where time is spent. Domains that touch "GO DEEP" items get deep verification. Domains that only touch "QUICK OK" items can use quick verification (labeled accordingly).

---

## Step 0: Model Discovery

Scan the codebase and identify all data models. This step runs automatically before any audit and is also available standalone via `/data-model-radar models`.

### How to Find Them

**IMPORTANT:** Models can live anywhere under Sources/, not just Sources/Models/. Scan the full tree.

1. Search for `@Model` classes across ALL of Sources/: `Grep pattern="@Model" glob="**/*.swift" path="Sources/"`
2. Search for Core Data entities if applicable: `Glob pattern="**/*.xcdatamodeld"`
3. Search for Codable structs used in serialization: backup structs, export structs
4. Search for relationship models: `Grep pattern="@Relationship" glob="**/*.swift" path="Sources/"`
5. Check for recently changed models: `git log --since="3 months ago" --name-only --diff-filter=M -- "Sources/**/*.swift"` (note: `**` not just `Sources/Models/`)

**Common locations missed if only checking Sources/Models/:**
- `Sources/Features/*/` (feature-specific models like ScoutBookmark, ScoutRecentScan)
- `Sources/Data/` or `Sources/Database/`
- Root of `Sources/` itself

### Risk Criteria

| Risk | Criteria |
|------|----------|
| **High** | Many fields (>20) + multiple serialization targets + external sync or externalStorage |
| **Medium** | Moderate fields (10-20) + some serialization |
| **Low** | Simple model (<10 fields), local only, cache/ephemeral |

**Risk boosters** (promote a model one level):
- Has `@Attribute(.externalStorage)` on any field (delete/sync crash risk)
- Changed in the last 3 months (new fields may be missing from serialization)
- Has prior findings in `.radar-suite/ledger.yaml`
- Is referenced by 3+ other models (hub model, high blast radius)

### Output: Risk-Ranked Model Inventory

Present models grouped by risk level, sorted within each group by field count descending. Include recently-changed indicator and prior finding count.

```
Found [N] @Model classes. Ranked by audit priority:

HIGH RISK (recommend auditing first)
  1. Item              — 88 fields, 10 rels, Backup+CSV+CloudKit, changed 3d ago
  2. ExtendedWarranty  — 43 fields, 1 rel, Backup+CloudKit
  3. RMARecord         — 41 fields, 1 rel, Backup, changed 2w ago

MEDIUM RISK
  4. DonationRecord    — 30 fields, 0 rels, Backup+CSV, externalStorage ⚠
  5. MaintenanceTask   — 28 fields, 1 rel, Backup
  6. ScoutBookmark     — 25 fields, 0 rels, Backup, externalStorage ⚠
  ...

LOW RISK (cache/ephemeral, audit only if time permits)
  18. AIResponseCache  — 14 fields, cache only, externalStorage ⚠
  ...

[N] models with prior findings: [list RS-NNN IDs if any]
```

Mark externalStorage models with ⚠ since they have elevated delete/sync crash risk.

### Standalone Command: `/data-model-radar models`

When invoked with the `models` argument, run ONLY Step 0 (discovery) and present the risk-ranked inventory. Do not start any audit. Do not ask setup questions. This is a read-only browse command.

After presenting the inventory, offer:
```
Options:
1. Audit a specific model — pick from the list above
2. Audit all High Risk models — deep audit of [N] models (~[time])
3. Full audit — all [N] models across 7 domains (~[time])
4. Done — exit without auditing
```

### Model Selection Menu (when user chooses "Audit a specific model")

When the user selects a single-model audit (either from the interactive menu or via `/data-model-radar [ModelName]`), **always run Step 0 first** to present the risk-ranked inventory before asking which model. Do NOT ask the user to name a model blind.

**Exception:** If the user provided a model name directly (e.g., `/data-model-radar Item`), skip the selection menu and audit that model immediately. The user already knows what they want.

After presenting the inventory, ask:
```
Which model to deep-audit? (enter number, model name, or "all high")
```

The `AskUserQuestion` options should list the top 4 models by risk as selectable options, with "Other" allowing any model name.

### Recently Changed Fields (Deep mode)

For high-risk models, identify fields most likely to have serialization gaps:
```bash
git log --since="3 months ago" -p -- Sources/Models/Item.swift | grep "^+.*var " | head -20
```

Fields added recently are highest risk -- they may not have been added to backup/CSV/CloudKit structs yet. **Audit these first in Domain 2.**

---

## Step 1: Per-Model Audit

Audit one model at a time across all 9 numbered domains (1, 1.5, 2, 3, 4, 5, 6, 7, 7.5) plus the 2 sub-domains under Domain 3 (3a, 3b) plus Domain 8 (delegated to time-bomb-radar).

### Before Starting (First Model Only)

`FIX_MODE` was already captured during the Skill Introduction setup call. Confirm the remaining per-session preferences in one `AskUserQuestion`:

- Delivery: Display only / Report / Both
- Presence: Normal / Hands-free / Pre-approved

If `FIX_MODE` has not been set for some reason (e.g. session-prefs file deleted mid-session), re-ask Question 3 from § Skill Introduction before proceeding.

### Domain 1: Field Completeness `enumerate-required`

**What to check:**
- Are there fields that *should* exist based on how the model is used?
  - Grep for hardcoded strings/enums that could be model fields (e.g., `"inherited"` string where an `acquisitionType` enum should exist)
  - Check if sibling models have fields this model lacks (e.g., all models have `cloudSyncID` except one)
- Are enums complete? Check every `switch` statement — are there `default` cases hiding missing enum values?
- Are optional fields appropriately optional? (Should `warrantyMonths` really be non-optional with default 12?)

**Output per finding:** What field is missing, why it should exist, which code paths would use it.

### Domain 1.5: Computed Property Correctness `mixed`

Models often embed business logic in computed properties (e.g., `effectiveReplacementCostInCents`, `isNearingEndOfLife`, `warrantyStatus`). A wrong computation is a model-layer bug that affects every view consuming it.

**What to check:**

- **Nil propagation chains:** Computed properties that chain optional fields. Does `effectiveReplacementCostInCents` correctly fall back from `replacementCostInCents` to `priceInCents` to `0`? Does the fallback chain match business intent?
- **Fallback default correctness:** When a computed property returns a default for nil input, is the default appropriate? Returning `0` for a missing price may be wrong if downstream code interprets `0` as "free" rather than "unknown."
- **Stale input assumptions:** Properties like `isReplacementCostStale` that use `assetAge > 2.0` embed a threshold. Is the threshold reasonable? Is it documented? Could it be a user-configurable setting?
- **Circular dependencies:** Property A reads property B which reads property A. SwiftData models can create subtle cycles through relationship traversal.
- **Calendar/date correctness:** Properties computing durations (`assetAge`, `daysRemaining`) that use hardcoded values like `365.25` instead of `Calendar` APIs. Check for leap year handling, timezone assumptions.
- **Currency computation safety:** Properties combining `*InCents` fields. Verify they handle nil correctly and don't accidentally mix dollars and cents.

**Method (Deep):**
1. Grep the model file and its extensions for `var.*:.*{` (computed properties with getters)
2. For each computed property that involves arithmetic, date math, or chained optionals, read the implementation
3. Check: are the inputs always available when this property is accessed? What happens when they're nil?
4. For currency computations, verify consistent units (all cents, no mixed dollars/cents)

**Method (Quick):**
1. List computed properties from the model file
2. Check only currency and date computations
3. Label grade as `(quick)`

**Output per finding:** The property, what it computes, what's wrong, and a concrete example of incorrect output.

### Domain 2: Serialization Coverage `enumerate-required`

**MANDATORY CHECKLIST — verify each target explicitly:**

For the model being audited, check ALL applicable serialization targets. Do not skip any.

- [ ] **Backup struct** — Read the `BackupXxx` struct. Diff every model field against backup fields. List gaps.
- [ ] **CSV export** — Find the CSV export code (e.g., `CSVExportManager`, `ExportManager`). Read it. List which model fields map to CSV columns and which don't.
- [ ] **CSV import** — Find the CSV import code (e.g., `CSVImportManager`). Read it. List which CSV columns map back to model fields. The export→import gap is where data loss hides.
- [ ] **CloudKit sync** — Find CKRecord mapping code (e.g., `CloudSyncManager`, `SharedZoneSyncManager`). List synced fields.
- [ ] **JSON API** — If the model receives data from an API, check the response mapping.

**Do not report a target as "covered" without reading the actual code.** "Backup looks complete" without reading BackupItem is not verification.

**Method:**
1. Read the model — list all stored properties (exclude `@Transient` computed properties)
2. Read each serialization struct/function listed above
3. Diff: model fields NOT in serialization = potential gap
4. For each gap, classify using the Intentional Exclusion Framework below

### Intentional Exclusion Framework

Not every serialization gap is a bug. Some fields are intentionally excluded from certain targets. Before reporting a gap as a finding, classify it:

| Classification | Meaning | Action | Example |
|---------------|---------|--------|---------|
| **Gap (report)** | Field carries user data that would be lost on round-trip | Report as finding | `purchasePrice` missing from CSV import |
| **Intentional: format mismatch** | Field type doesn't fit the target format | Document, don't report | `priceHistoryData` (JSON blob) excluded from CSV |
| **Intentional: internal metadata** | Field is sync/system infrastructure, not user data | Document, don't report | `cloudSyncID`, `cloudKitRecordID` excluded from CSV |
| **Intentional: relationship data** | Nested objects that need their own serialization | Document, note if the child model IS serialized | `attachments` excluded from CSV (binary data) |
| **Intentional: scope boundary** | Target intentionally covers a subset | Document, don't report | SharedZone CloudKit syncs 22 fields (household subset) |

**How to classify:**
- **User data test:** If this field were lost during export-import, would the user notice? If yes, it's a gap. If no (sync IDs, internal timestamps), it's intentional.
- **Format test:** Could this field reasonably be represented in the target format? JSON blobs and binary data can't go in CSV. That's a format mismatch, not a gap.
- **Subset test:** Does the target explicitly define a subset? (e.g., SharedZone syncs "household-visible" fields only.) If the exclusion matches the subset definition, it's intentional scope.

**Output:** In the Domain 2 coverage table, add an `Exclusion` column for fields not in a target:

```
| Field | Model | Backup | CSV Export | CSV Import | CloudKit | Exclusion Reason |
|-------|:-----:|:------:|:---------:|:----------:|:--------:|-----------------|
| cloudSyncID | yes | yes | no | no | yes | Internal metadata |
| priceHistoryData | yes | yes | no | no | yes | Format mismatch (JSON blob) |
| attachments | yes | yes | no | no | yes | Relationship data (binary) |
```

**Grade impact:** Intentional exclusions do NOT lower the domain grade. Only unclassified gaps or gaps classified as "report" lower the grade.

**Output:** Side-by-side coverage table:

```
| Field | Model | Backup | CSV Export | CSV Import | CloudKit |
|-------|:-----:|:------:|:---------:|:----------:|:--------:|
| title | yes | yes | yes | yes | yes |
| cloudSyncID | yes | yes | no | no | yes |
| documents | yes | no | no | no | yes |
```

Mark fields not checked with `?` instead of yes/no. The table must be honest about what was verified.

### Verification Template (MANDATORY for Domain 2)

Before grading serialization coverage, produce this pre-populated table. Read the model file first to get all stored properties, then fill in each cell by reading the actual serialization code.

```
| Field | Model | Backup | CSV Export | CSV Import | CloudKit | Receipt |
|-------|:-----:|:------:|:---------:|:----------:|:--------:|---------|
| [field1] | yes | ? | ? | ? | ? | (fill after reading each target) |
| [field2] | yes | ? | ? | ? | ? | |
```

Rules:
- `yes` = confirmed by reading the code (include file:line in Receipt column)
- `no` = confirmed absent by reading the code
- `?` = not yet checked
- A domain grade CANNOT be produced while any cell contains `?` for a target you claimed to check
- If you skip a target (e.g., don't read CloudKit), mark the entire column as `not checked` — don't fill in `?` and then grade as if you checked it

### Domain 3: Relationship Integrity `mixed`

**What to check:**
- Every `@Relationship` has a correct `deleteRule` (`.cascade`, `.nullify`, `.deny`, `.noAction`)
- Every `@Relationship` has an `inverse` specified
- Cascade chains don't create unexpected data loss (deleting Item cascades to Photos, which is correct — but does it also cascade to SharedZone records?)
- Orphan risk: can child objects exist without a parent? (e.g., PhotoAttachment with `item: Item? = nil`)
- Circular relationships: A → B → A

**Method:**
1. Grep for all `@Relationship` declarations
2. For each, verify: deleteRule, inverse, optional vs required
3. Build a relationship graph and check for orphan paths

#### 3a: Cross-Context Mutation `mixed`

**The problem:** A manager or service class creates its own `ModelContext` (via `makeContext()`, `ModelContext(container)`, or similar), then receives `@Model` objects as parameters and mutates them or sets relationships on them. SwiftData forbids relating or mutating objects across different contexts. This crashes at runtime with "attempting to relate model with model context to destination model from destination's model context."

**Why static audits miss it:** Every line of code is valid Swift. The bug is the *relationship* between where the object was created (caller's context) and where the mutation happens (method's own context). No single file is wrong in isolation.

**How to find them:**

```
Grep pattern="ModelContext\(|makeContext\(\)" glob="**/*.swift" output_mode="files_with_matches"
```

For each file that creates its own context, check every method that:
1. Receives `@Model` parameters (any `@Model` type as a function argument)
2. Mutates those parameters (sets properties, assigns relationships) OR deletes them
3. Saves via the method's own context, not the caller's

**False positive filter:** Methods that re-fetch the passed-in object by `persistentModelID` before mutation are safe. Example:
```swift
let localObject = context.model(for: passedObject.persistentModelID) as? MyModel
```

**Classification:**

| Behavior | Rating |
|---|---|
| Receives @Model param, creates own context, mutates param directly | BOMB (crash) |
| Receives @Model param, creates own context, re-fetches by ID before mutation | Safe |
| Receives @Model param, uses caller's context (passed as parameter) | Safe |
| Creates own context, only reads/queries (no mutation of passed-in objects) | Safe |

#### 3b: Stale Object After Cross-Context Save `mixed`

**The problem:** A manager method saves changes in its own `ModelContext`, but the caller passed in an `@Model` object and expects it to reflect the saved changes. The caller's copy belongs to a different context and won't see the update. The UI shows stale data until the user navigates away and back. Not a crash, but frequently reported as "my data disappeared" or "save didn't work."

**How to find them:**

Same grep as 3a. For each method that creates its own context and receives `@Model` parameters, check if:
1. The method modifies data related to the passed-in object (even if it doesn't mutate the object directly)
2. The method returns success or the updated object, implying the caller can trust the passed-in reference
3. The caller's context never learns about the save

**Classification:**

| Behavior | Rating |
|---|---|
| Saves in own context, caller assumes passed-in object is updated | Risky (stale UI) |
| Saves in own context, caller re-fetches after call returns | Safe |
| Uses caller's context for save | Safe |

### Domain 4: Semantic Clarity `enumerate-required`

**What to check:**
- **nil vs zero:** For every `Int?` field, is there UI or documentation that distinguishes "not set" from "zero"? (e.g., `priceInCents: Int?` — nil = not entered, 0 = free. But does the UI show this difference?)
- **Missing type distinctions:** Are there fields where a single type carries multiple meanings? (e.g., `priceInCents` used for both new and used purchases — should there be separate fields?)
- **Boolean ambiguity:** `isEstimatedPrice` — does `false` mean "confirmed exact" or "user never set this flag"?
- **String fields that should be enums:** Fields like `disposalMethodRaw: String` — is the enum complete? Are there raw strings in the codebase that don't match any enum case?

### Domain 5: Field Usage Mapping `mixed`

**What to check:**
- **Dead fields:** Model properties that are never read in any view, ViewModel, or manager. Set during creation but never displayed or used in calculations.
- **Phantom fields:** Values shown in the UI that are computed on-the-fly and never stored. If the computation inputs change, the displayed value changes retroactively (e.g., donation FMV recalculated from condition).
- **Write-only fields:** Set by the user but never read back (data goes in but nothing comes out).
- **Form-only fields:** Editable in a form/sheet and correctly serialized, but never displayed in any read-only detail view. The user enters data that vanishes from view after saving. Data is preserved (not lost), but the user must re-enter edit mode to see it. This is a UX degradation, not data loss, but frequently reported as "my data disappeared." To detect: when grepping for a field's consumers, classify each hit as `form` (read to populate edit state), `detail` (read for display in a read-only view), `serialization` (backup/CSV/CloudKit), or `compute` (consumed by a computed property). A field with `form` + `serialization` consumers but zero `detail` consumers is a form-only field.
- **Read-only fields:** Displayed but never settable by the user (may be intentional for computed fields, but worth flagging if the user might want to override).

**Method (Deep — required for High-risk models):**

For models with >20 fields, use a **stratified sampling strategy** instead of grepping all fields:

1. **All recently added fields** (from git log in Step 0) — highest risk for being unwired
2. **All currency fields** (`*InCents`, `*Price*`, `*Value*`, `*Cost*`) — money = high risk
3. **All optional fields** (`var x: Type? = nil`) — more likely to be dead than required fields
4. **All fields with "raw" suffix** (`*Raw`) — enum storage, check if enum is used anywhere
5. **Random sample of remaining fields** (5-10) to spot-check

For each sampled field:
```
Grep pattern="\.fieldName" glob="**/*.swift" path="Sources/" output_mode="files_with_matches"
```

Flag: 0 read hits in Sources/ (excluding the model file itself and Tests/) = dead field candidate.

**MANDATORY verification before reporting any dead field:**
1. **Confirm the field exists.** Grep the model file itself for `var fieldName`. If the field doesn't exist in the model, it was hallucinated. Do NOT report hallucinated fields.
2. **Check extension files.** Grep for `extension ModelName` across Sources/ and read any matches. A field may appear "dead" because its consumer is in `Model+Extension.swift`, not the main model file. See Extension Discovery below.
3. **Check backup/serialization code.** A field that exists only in the model and backup is "backed up but not displayed," which is different from "dead." Classify correctly.
4. **Read one suspected consumer.** If the field name appears in a file, read the relevant lines to confirm it's actually reading this model's field (not a different type with the same property name).

Only after all 4 checks pass with 0 consumers should a field be reported as dead.

### Extension Discovery (MANDATORY before declaring fields dead)

Models often split logic across multiple files via extensions (e.g., `Item+Warranty.swift`, `Item+Maintenance.swift`). A field consumer in an extension file is invisible if only the main model file is read.

**Before running field usage grep for any model, discover all extension files:**

```
Grep pattern="extension ModelName" glob="**/*.swift" path="Sources/" output_mode="files_with_matches"
```

Also check for naming convention files:
```
Glob pattern="**/ModelName+*.swift" path="Sources/"
```

**Include all discovered extension files** in the "exclude self" list when counting consumer files. A field referenced only in the model file AND its extensions is not dead if the extension provides computed properties consumed by views.

**Example:** `Item.swift` has extensions in `Item+Warranty.swift`, `Item+Maintenance.swift`, `Item+Extensions.swift`, `Item+PriceWatch.swift`, `Item+Rating.swift`, `Item+Timeline.swift`, `Item+Accessible.swift`. A field like `warrantyMonths` may only appear in `Item.swift` and `Item+Warranty.swift`, but `Item+Warranty.swift` provides computed properties like `expirationDate` that ARE consumed by views. The field is not dead.

**Method (Quick — for Low-risk models):**
1. List all stored properties
2. Check for obvious dead patterns: fields with no corresponding UI label, fields added but never referenced in any view
3. Label grade as `(quick)` — not fully verified

### Domain 6: Migration Safety `enumerate-required`

**What to check (Deep — read the actual schema files):**
1. **Read the VersionedSchema file** — `Glob pattern="**/*Schema*.swift"` or `**/*Migration*.swift"`
2. **Verify the latest schema version includes all current model fields.** Diff the schema's model definition against the actual model. Any field in the model but not in the latest schema version = migration gap.
3. Does a `SchemaMigrationPlan` exist with proper stage ordering?
4. Are there fields added without migration? (SwiftData handles simple additions automatically, but relationship changes or type changes need explicit migration)
5. Has the model changed since the last migration version? Compare timestamps: `git log -1 --format="%ai" -- Sources/Models/Item.swift` vs `git log -1 --format="%ai" -- Sources/Models/AppSchema.swift`
6. Are there `@Attribute` modifiers that affect storage (`.externalStorage`, `.unique`) — are these in the migration plan?

**Do not say "migration infrastructure exists" without reading the schema file.** That's the same as saying "backup exists" without reading BackupItem.

**CloudKit schema is a SEPARATE migration surface from SwiftData (often missed):**
The SwiftData `VersionedSchema` checks above do NOT cover raw-CloudKit sync. If the app syncs via manual `CKDatabase`/`CKRecord` (i.e. SwiftData's `cloudKitDatabase: .none`), the CloudKit Production schema is its own thing that the simulator never validates. Check:
1. **Does the Production CloudKit schema contain every record type the app writes?** Production does NOT auto-create record types on write — Development DOES. A type exercised only in Dev is absent in Prod until "Deploy Schema Changes" is run in the Dashboard → writes fail silently for real users. Enumerate every `CKRecord(recordType: "X")` and confirm `X` is deployed to Prod.
2. **Any `CKQuery(predicate: NSPredicate(value: true))` fetch-all?** It sorts on the system `recordName` field, which is NOT queryable by default in the Prod schema (it IS in Dev → masks the bug). In Prod it throws "Field 'recordName' is not marked queryable" → silent empty read. Durable fix: enumerate the zone via `CKFetchRecordZoneChangesOperation` (no index needed, custom zones only) OR mark `recordName` queryable in the Dashboard.
3. **CloudKit "Deploy Schema Changes" is irreversible** — additive (new types/indexes/fields) is safe; deleting/retyping a live field or migrating zones is Bucket-B-class (schedule a spike, don't do reactively). Reviewing the deploy diff is mandatory.

**Origin:** Stuffolio 2026-06-08 — Legacy Wishes sharing types were never deployed to Prod + reads used `CKQuery(predicate:true)`; beneficiaries silently saw empty shares. The simulator (Dev environment) showed it working the whole time.

### Domain 7: Cross-Model Consistency `enumerate-required`

**Minimum model requirement:** This domain requires reading at least 3 models to be meaningful. When auditing a single model, this domain outputs one of:

- **If 3+ models are being audited this session:** Full cross-model comparison.
- **If single model audit:** Read 2-3 additional model files (pick the highest-relationship models from Step 0) to compare patterns, then grade. Label as `(partial — N models compared)`.

**What to check:**
- **Identifier strategy:** Do all models use the same approach? (Some use `cloudSyncID`, some use `persistentModelID.hashValue`, some use UUID — should be consistent)
- **Timestamp conventions:** `timestamp`, `createdAt`, `date` — same concept, different names across models?
- **Naming patterns:** `priceInCents` vs `deductibleInCents` vs `fairMarketValue` (not in cents?) — consistent currency representation?
- **Shared protocol conformances:** Do models that should be `Sendable` all conform? Do models with `cloudSyncID` all use it the same way?

### Domain 7.5: Near-Duplicate Model Detection `mixed`

Detect models that share a high percentage of fields and methods, indicating they should be consolidated via a shared protocol or base pattern.

**When to run:**
- **3+ models audited this session:** Always run. Compare all audited models pairwise.
- **Single model audit:** Check the model's field list against all other models discovered in Step 0. Use a lightweight comparison (field name overlap) rather than deep reading.

**How to detect:**

1. For each pair of models (A, B), compute field overlap:
   ```
   shared_fields = fields_in_A ∩ fields_in_B (by name AND type)
   overlap_ratio = shared_fields / min(fields_in_A, fields_in_B)
   ```
2. Flag pairs with `overlap_ratio >= 0.70` (70%+ shared fields)

3. For flagged pairs, also check method duplication:
   - Grep both files for `func ` declarations
   - Compare method signatures (name + parameter types)
   - Flag if 50%+ of methods also overlap

**What to look for beyond field overlap:**
- **Duplicated init logic:** Both models have `init(from session:)` that copies the same fields
- **Duplicated computed properties:** Same property names with same logic
- **Duplicated static methods:** `generateThumbnail()`, helper functions copy-pasted
- **Conversion methods between them:** `modelA.toModelB()` that manually copies every field (fragile, breaks when fields are added to one but not the other)

**Classification:**

| Overlap | Recommendation |
|---------|---------------|
| 90%+ fields, 50%+ methods | Extract shared protocol with default implementations |
| 70-89% fields | Consider shared protocol for common fields; document why they diverge |
| 50-69% fields | Note the similarity; likely intentional domain separation |
| <50% fields | Not duplicates, skip |

**Output per finding:** The two models, overlap percentage, list of shared fields, list of duplicated methods, and recommended consolidation approach.

**Example finding:**
```
ScoutBookmark and ScoutRecentScan share 90% of fields (20/22) and 6 identical
computed properties. Both have duplicated init(from:), toSession(), and
generateThumbnail() methods. Recommend extracting ScoutIdentifiable protocol.
```

### Domain 8: Time Bomb Audit

**Delegated to `/time-bomb-radar`** -- a standalone skill in the radar-suite family.

When running a full data-model-radar audit, invoke `/time-bomb-radar` after completing Domains 1-7. Its findings feed into the data-model-radar handoff under `for_capstone_radar.blockers[]`.

When running data-model-radar standalone (not as part of a full suite run), note in the handoff that Domain 8 was not run and recommend `/time-bomb-radar` as a follow-up.

---

## Domain Scoring Rubric

Every domain produces a letter grade. Use this rubric so grades are consistent across sessions, models, and auditors.

### Grade Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 95-100 | No findings. All checks verified with evidence. |
| A- | 90-94 | Minor observations only (hygiene, documentation). No functional gaps. |
| B+ | 85-89 | 1-2 LOW findings. No data loss or crash risk. |
| B | 80-84 | 1 MEDIUM finding or 3+ LOW findings. |
| B- | 75-79 | 2-3 MEDIUM findings. Functional gaps exist but workarounds available. |
| C+ | 70-74 | 1 HIGH finding or 4+ MEDIUM findings. |
| C | 65-69 | 2+ HIGH findings. Significant gaps affecting data integrity. |
| C- | 60-64 | Multiple HIGH findings with user-visible impact. |
| D | 50-59 | CRITICAL finding present. Ship blocker. |
| F | <50 | Multiple CRITICAL findings or fundamental design flaw. |

### Per-Domain Scoring Rules

**Domain 1 (Field Completeness):**
- Start at A. Deduct per missing field by severity: missing enum case = -3, missing field that would prevent a workflow = -10, missing optional convenience field = -1.

**Domain 1.5 (Computed Property Correctness):**
- Start at A. Deduct per incorrect computation: wrong fallback default = -5, nil propagation crash risk = -10, stale threshold = -2, currency unit mismatch = -15.

**Domain 2 (Serialization Coverage):**
- Start at A. Deduct per unintentional gap: field missing from backup = -10, field missing from CSV = -5, field missing from CloudKit = -5. Intentional exclusions (per framework) do NOT deduct.
- Quick-depth audits cap at B+ (unverified targets may hide gaps).

**Domain 3 (Relationship Integrity):**
- Start at A. Deduct: missing inverse = -10, wrong delete rule = -15, orphan risk = -5, undocumented cascade to externalStorage = -20, cross-context mutation (3a) = -20 (crash), stale object after cross-context save (3b) = -10 (silent bug).

**Domain 4 (Semantic Clarity):**
- Start at A. Deduct: nil-vs-zero ambiguity with no distinguishing flag = -5, string field that should be enum = -3, boolean with ambiguous false = -2.

**Domain 5 (Field Usage Mapping):**
- Start at A. Deduct per dead field: dead field with no serialization = -2, dead field that IS serialized (wasted backup space) = -3, phantom field = -5, write-only field = -3.
- Quick-depth audits cap at B+ (stratified sampling may miss dead fields).

**Domain 6 (Migration Safety):**
- Start at A. Deduct: no VersionedSchema at all = -15, schema version behind model = -10, missing migration stage for type change = -20, no migration needed (additive only, correct single-version state) = 0.

**Domain 7 (Cross-Model Consistency):**
- Start at A. Deduct: inconsistent identifier strategy = -5, inconsistent currency representation = -5, inconsistent timestamp naming = -3, missing shared protocol conformance = -3.
- Partial comparisons (single model audit) cap at A- (can't fully verify without reading all models).

**Domain 7.5 (Near-Duplicate Detection):**
- Start at A. Deduct: 90%+ overlap without shared protocol = -5, duplicated methods = -3 each, fragile conversion method = -3.

**Domain 8 (Time Bombs — delegated):**
- Not graded by data-model-radar. Findings from `/time-bomb-radar` flow directly to `for_capstone_radar.blockers[]` in the handoff and do NOT enter this skill's weighted-average model grade. Domain 8 is therefore absent from the weight table below by design.

### Evidence Requirement

**Every grade must include an Evidence block:**
```
**Evidence:** Read [files read with line ranges]. Verified [what was checked].
[What was NOT checked, if anything].
**Confidence:** [verified | quick | partial]
```

A grade without evidence is not a grade. It's a guess. Downgrade to `needs-verification` if evidence is absent.

### Overall Model Grade

The overall model grade is the **weighted average** of domain grades:

| Domain | Weight | Rationale |
|--------|--------|-----------|
| 1. Field Completeness | 10% | Foundation, but gaps are usually LOW severity |
| 1.5 Computed Properties | 10% | Business logic correctness — one wrong computation affects every view that consumes the property, so equal weight to Domain 1 is intentional |
| 2. Serialization Coverage | 25% | Data loss is the highest-impact model bug |
| 3. Relationship Integrity | 15% | Cascade/orphan bugs cause crashes. 3a/3b deductions roll into Domain 3's score per § Per-Domain Scoring Rules — they do NOT get their own weight rows |
| 4. Semantic Clarity | 5% | Important but rarely causes data loss |
| 5. Field Usage Mapping | 10% | Dead fields are hygiene, not crashes |
| 6. Migration Safety | 15% | Wrong migration = app won't launch |
| 7. Cross-Model Consistency | 5% | Consistency aids maintenance |
| 7.5 Near-Duplicate Detection | 5% | Code hygiene |

**Sub-domain treatment:** Domains 3a and 3b are scored *within* Domain 3 (their deductions appear in Domain 3's "Per-Domain Scoring Rules" entry). Domain 8 is excluded entirely — see "Domain 8 (Time Bombs — delegated)" above. The 9 weight rows sum to 100%.

Convert letter grades to numeric (A=97, A-=92, B+=87, B=82, B-=77, C+=72, C=67, C-=62, D=55, F=40), compute weighted average, convert back to letter.

---

## Issue Rating Criteria

For every finding, use this table format sorted by Urgency (descending), then ROI:

| # | Finding | Confidence | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort | Status |
|---|---------|------------|---------|-----------|--------------|-----|--------------|------------|--------|

### Column Definitions

| Column | Meaning |
|--------|---------|
| Confidence | `verified` (code read + confirmed), `probable` (structural analysis, not independently verified), `needs-runtime` (requires running the app to confirm) |
| Urgency | CRITICAL / HIGH / MEDIUM / LOW |
| Risk: Fix | What could break when making the change |
| Risk: No Fix | Cost of leaving it — data loss, crash, user-visible bug |
| ROI | Excellent / Good / Marginal / Poor |
| Blast Radius | Number of files the fix touches (e.g., `3 files`, `1 file`). Count by grepping for callers/references before rating. |
| Fix Effort | Trivial / Small / Medium / Large |
| Status | Fixed / Documented / Deferred (reason) |

### Finding Dependencies and Fingerprints

When creating findings, populate these optional fields where relationships are obvious:

- **`depends_on`/`enables`:** If one finding must be fixed before another (e.g., "add Codable conformance" enables "serialize to JSON backup"), populate these fields with finding IDs. Common in data-model-radar: structural changes (new field, new enum case) enable serialization/UI fixes.
- **`pattern_fingerprint`/`grep_pattern`/`exclusion_pattern`:** If the anti-pattern is generalizable, assign a fingerprint so it can be detected if reintroduced elsewhere. Example: `missing_backup_field` with `grep_pattern: "case .backup"` and exclusion checking for the field name.

---

## Fix Plan

Group findings into:

**1. Safe fixes (isolated, low blast radius)**

**2. Cross-cutting fixes (touch shared code)**

**3. Schema changes (require migration)**
Changes that add/modify/remove model fields. These need:
- VersionedSchema update
- SchemaMigrationPlan stage
- Backup format update (if field should be serialized)
- Testing on real device with existing data

| # | Finding | Migration Required | Backward Compatible | Fix Effort |
|---|---------|-------------------|--------------------:|------------|

**4. Shared utility extraction**
When multiple models duplicate the same pattern, extract to a shared protocol or utility.

**5. Design decisions (need user input)**

**6. Deferred**

---

## Fix Application Workflow

Apply fixes in **waves** with progress tracking.

### Wave Scaling

Scale the number of waves to finding severity:

- **All findings LOW/MEDIUM, no schema changes:** Collapse to 1 wave (safe fixes) + commit. Skip waves 2-4.
- **Mixed severity, no schema changes:** 2 waves (safe + cross-cutting) + commit.
- **Schema changes present:** Full 5-wave workflow.

### Waves (Full)

| Wave | Section | Est. Time | Description |
|------|---------|-----------|-------------|
| 1 | Safe fixes + tests | ~10-15 min | No schema changes, isolated. Write tests for each fix. |
| 2 | Cross-cutting fixes + tests | ~15-25 min | Touch shared code. Write tests for each fix. |
| 3 | Schema changes + tests | ~20-35 min | Model + migration + backup + tests on real data. |
| 4 | Pattern Sweep | ~5 min | Scan codebase for patterns found. |
| 5 | Build + Test + Commit | ~5 min | Build both platforms, run tests, stage, commit. |

**Every fix must have a test.** Do not move to the next wave until tests for the current wave's fixes are written and compiling. The test verifies the fix works; without it, the fix is unverified code.

### Progress Banner (CRITICAL — BLOCKING requirement)

**After EVERY wave and EVERY commit, your NEXT output MUST be the progress banner followed by the next-wave `AskUserQuestion`. Do not output anything else first. Do not leave a blank prompt.**

After completing each wave, **always** print:

```
Step [N] of [total] complete: [plain description of what was done]
   [X] issues fixed, [Y] remaining, [Z] deferred

Next: [plain description of what comes next] (~[time estimate])
```

Then immediately ask using `AskUserQuestion`:
- **"Continue to next step (Recommended)"** — proceed with the next batch of fixes
- **"Show me what was fixed"** — review the changes before continuing
- **"Stop here"** — defer remaining fixes
- **"Explain more"** — describe what the next step involves and why

### Between Models

After all waves for a model, print scorecard and prompt for next model:

```
Progress: [N] of [total] models checked | [X] issues fixed | [Y] deferred
   Just finished: [model name] — [one-line summary of what was found]
   Next up: [model name] (~[time estimate])
```

Then ask: "Ready to check the next model?" with options including **"Explain more"** — what this model is and why it matters.

### Pipeline Mode Behavior (Tier 2/3)

When running inside a Tier 2 or Tier 3 pipeline (detected via `tier` field in `.radar-suite/session-prefs.yaml`):

1. **On skill start:** Emit the pipeline-level progress banner (see `radar-suite-core.md` Pipeline UX Enhancements #1). If this is the first skill in the pipeline OR `experience_level` is Beginner/Intermediate, also emit the audit-only statement.
2. **On skill completion:** Emit a per-skill mini rating table marked "PRELIMINARY" (see Pipeline UX Enhancements #2). Then emit the pipeline-level progress banner showing this skill as complete.
3. **Within-skill phase banners** (above) are still emitted normally in addition to the pipeline-level banners.

### short_title Requirement (v2.1)

Every finding MUST include a `short_title` field (max 8 words). This is the human-scannable label used in pipeline banners, pre-capstone summaries, and ledger output.

Example: `short_title: "CSV export drops Room column"`

All finding ID references in output (tables, banners, summaries) use the format: `RS-NNN (short_title)`.

---

## Cross-Skill Handoff

Data Model Radar is the **foundation layer** of the radar family. Run it first — its findings feed every other skill.

### On Completion — Write Handoff

After auditing models, write `.agents/ui-audit/data-model-radar-handoff.yaml`:

```yaml
source: data-model-radar
date: <ISO 8601>
project: <project name>
models_audited: <count>
audit_depth: <full | partial | quick>
domains_verified: [1, "1.5", 2, 3, "3a", "3b", 4, 5, 6, 7, "7.5"]  # quote any non-integer entries to keep YAML valid
domains_at_quick_depth: []
domains_skipped: []

# File timestamps — enables staleness detection by consuming skills
file_timestamps:
  <file path>: "<ISO 8601 mod date>"
  # one entry per unique file referenced in issues

for_roundtrip_radar:
  # Serialization gaps = workflow-specific data loss
  suspects:
    - workflow: "<affected workflow>"
      finding: "<e.g., DocumentAttachment not in BackupItem>"
      model: "<model name>"
      field: "<field name>"
      group_hint: "<optional, e.g. 'backup_gaps', 'csv_gaps', 'cloudkit_gaps'>"

for_ui_path_radar:
  # Dead fields may indicate dead UI paths
  suspects:
    - view: "<view that might reference this field>"
      finding: "<e.g., field exists but no UI reads it>"
      group_hint: "<optional batching suggestion>"
  # Form-only fields: user enters data that vanishes from detail view
  form_only_fields:
    - model: "<model name>"
      field: "<field name>"
      form_view: "<form that edits this field>"
      detail_view: "<expected detail view that should display it>"
      group_hint: "form_to_detail_gap"

for_ui_enhancer_radar:
  # Semantic ambiguity affects how fields should be displayed
  suspects:
    - view: "<view displaying this field>"
      finding: "<e.g., nil vs 0 not distinguished in UI>"
      group_hint: "<optional batching suggestion>"

for_capstone_radar:
  # Model-layer blockers
  blockers:
    - finding: "<description>"
      urgency: "<CRITICAL|HIGH>"
      domain: "Data Safety"
      group_hint: "<optional batching suggestion>"

serialization_coverage:
  # Summary table for roundtrip-radar to reference
  # Only include targets that were ACTUALLY READ AND VERIFIED
  - model: "Item"
    total_fields: 47
    backup_coverage: 40
    backup_verified: true
    csv_export_coverage: 27
    csv_export_verified: true
    csv_import_coverage: 11
    csv_import_verified: true
    cloudkit_verified: false
    missing_from_backup: ["field1", "field2"]
    missing_from_csv_export: ["field3", "field4"]
```

### File Timestamps

For each unique file path referenced across all issues, record its modification date:

```bash
stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "<file path>"
```

Enables consuming skills to detect **staleness** — if a model file changed after the audit, serialization coverage data may be stale.

### Group Hints

Optional field for batching related issues. Common hints:
- `backup_gaps` — fields missing from backup
- `csv_gaps` — fields missing from CSV export/import
- `cloudkit_gaps` — fields missing from CloudKit sync
- `dead_fields` — model fields with no UI reads
- `semantic_ambiguity` — nil vs zero not distinguished

**Honesty rule:** The handoff must distinguish "verified clean" from "not checked." Use `_verified: true/false` for each serialization target. Capstone-radar uses these flags to determine how much credit to give.

### End-of-Run Directory Cleanup (MANDATORY)

Per the Artifact Lifecycle rules in `radar-suite-core.md`, before returning from this skill:
1. List files in `.radar-suite/` (and `.agents/ui-audit/` or equivalent if used).
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

**Impact category mapping for data-model-radar findings:**
- Domain 2 serialization gaps → `data-loss`
- Domain 3 cascade/orphan risk → `crash` (if cascade to external storage) or `data-loss`
- Domain 3a cross-context mutation → `crash`
- Domain 3b stale object after cross-context save → `ux-degraded`
- Domain 5 dead fields → `hygiene`
- Domain 6 migration gaps → `crash` (if breaking) or `data-loss`
- Domain 1/4/7 → classify per finding (usually `hygiene` or `ux-degraded`)

### On Startup — Read Ledger & Handoffs (MANDATORY)

Before starting Step 1, read the unified ledger and ALL companion handoff YAMLs:

```
Read .radar-suite/ledger.yaml (if exists) — check for existing findings to avoid duplicates
Read .agents/ui-audit/roundtrip-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-path-radar-handoff.yaml (if exists)
Read .agents/ui-audit/ui-enhancer-radar-handoff.yaml (if exists)
Read .agents/ui-audit/capstone-radar-handoff.yaml (if exists)
```

**Ledger check:** If the ledger contains findings for files you're about to audit, note their RS-NNN IDs. When you find the same issue, update the existing finding instead of creating a new one.

**Regression check:** For any `fixed` findings in the ledger whose `file_hash` no longer matches the current file, flag for re-verification per the Regression Detection protocol in `radar-suite-core.md`.

**Parse `for_data_model_radar` sections.** Each companion can direct findings to this skill. Look for:
- `for_data_model_radar.suspects[]` — models or fields another skill flagged as potentially wrong
- `for_data_model_radar.priority_models[]` — models another skill wants audited first

If found, incorporate as **priority targets** in the model audit order. These are not pre-confirmed findings — verify each one independently. If not found, proceed normally.

**What each companion provides:**
- roundtrip-radar — workflow-specific data issues that trace to model gaps
- ui-path-radar — dead UI that may indicate dead model fields
- ui-enhancer-radar — visual issues that may trace to missing/wrong model fields
- capstone-radar — priority models from ship readiness grading

**Automatic:** This file is always written so other audit skills can pick up where this one left off. No user action needed.

---

## Step 2: Cross-Model Rollup

After auditing all high-risk models, identify patterns across models:

1. Shared serialization gaps (e.g., "3 models missing from backup")
2. Inconsistent identifier strategies
3. Naming convention violations
4. Missing shared protocols
5. Top 5 deferred items ranked by impact

---

## Domain Grade Evidence Requirements

Every domain grade MUST cite what was actually done. Use this format after each domain:

```
**Evidence:** Read BackupItem (BackupManager.swift:32-340). Diffed 55 model fields against 55 backup fields.
Verified toItem() restore at line 342-546. CSV export NOT checked (CSVExportManager not read).
**Confidence:** verified (backup), not-checked (CSV, CloudKit)
```

A grade without evidence is not a grade — it's a guess.

---

## End Reminder

After every step: print progress banner → `AskUserQuestion` → never blank prompt.

**Anti-shortcut:** Domain 2 (Serialization) and Domain 5 (Field Usage) require actual grep verification. No "looks complete" without evidence.
