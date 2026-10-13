---
name: constitute-check
description: "Memory-bank governance audit — checks whether T0 laws/current state, T1 supporting context, T2 execution mirrors, adapter freshness, and T3 archive indexes align. Read-only by default; may record adapter_state.yaml only after explicit approval."
argument-hint: "[optional: 'full' for verbose report, or a specific principle number]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion
model: haiku
context: |
  !echo "=== Memory Bank Status ===" && echo "T0: $(ls memory_bank/t0_core/ 2>/dev/null | wc -l) files" && echo "T1: $(ls memory_bank/t1_axioms/ 2>/dev/null | wc -l) files" && echo "T2: $(ls memory_bank/t2_execution/ 2>/dev/null | wc -l) files" && echo "T3: $(ls memory_bank/t3_archive/ 2>/dev/null | wc -l) files" && echo "Review mode: $(cat production/review-mode.txt 2>/dev/null || echo 'not set')"
---

## User Guide

- When to use: Memory-bank governance audit — checks whether T0 laws/current state, T1 supporting context, T2 execution mirrors, adapter freshness, and T3 archive indexes align. The audit is read-only by default.
- Inputs: Command arguments: `/constitute-check [optional: 'full' for verbose report, or a specific principle number]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: A T0-T3 health report plus live and recorded adapter freshness. Write only the approved adapter-state record described below.
- Memory-bank writes: At most `memory_bank/t2_execution/adapter_state.yaml`, and only after showing the exact YAML draft and receiving explicit approval. No other file may be written.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Purpose before Governance Audit

Apply the purpose rule to skills, independent agent/role definitions, native
configuration containing instruction bodies and their exclusive references/overlays.
A Target's development-only role stays local-only even without invoking a skill;
TOML, developer_instructions fields and native loading give no exception. Real
product-use agents follow actual product rules. Independent configuration must be
independent of development instructions/role packages and carry no such body;
a native loader of developer roles is not an independent configuration consumer.

Read `standards/skill-purpose.md` before domain/audit routing. Identify the actual
project and whether the request uses its delivered functions or develops/governs
it. This CDD governance audit is a local-only Target development template; complete
platform copies, bespoke prompts and exclusive overlays do not change that role.
Independent product-use tasks use their real capabilities, without requiring a
Memory Bank. Purpose review and Git eligibility remain separate from freshness.

## Phase 0: Domain Routing

Detect the project domain before checking constitution compliance:
- `design/cdd/game-concept.md` -> **[Game]** verify principles against player fantasy, core loop, game pillars, playtest evidence, and game-specific CDDs.
- `design/cdd/product-concept.md` -> **[Product]** verify principles against user promise, JTBD, target workflows, product modules, API/CLI contracts, and product-specific CDDs.
- If neither exists, check only the constitution and report that domain-specific validation is pending.

Do not remove game constitution examples. Product checks are an added validation path.
# Constitution Check — T0-T3 Memory Health Audit

This skill is read-only by default. Its only write exception is an explicitly
approved refresh of `memory_bank/t2_execution/adapter_state.yaml`; every other
project file remains read-only.

This skill checks the health of a project's memory-bank governance plane:
whether T0 laws/current state exist, whether T1 supporting context is present,
whether T2 execution mirrors exist when the project has been initialized, and
whether T3 archive indexes exist once evidence is produced. It is lightweight —
not a full 4-gate CDD audit. For a complete project scan, use
`/project-stage-detect`.

---

## Step 1: Verify Constitution Exists

Check for the minimum memory-bank artifacts:

| Artifact | Required? | How to check |
|----------|-----------|--------------|
| `memory_bank/t0_core/basic_law_index.md` | **Yes** | Read if exists |
| `memory_bank/t0_core/active_context.md` | **Yes** | Read if exists |
| `memory_bank/t0_core/current_state.md` | **Yes** | Read if exists |
| `memory_bank/t1_axioms/tech_context.md` | **Yes** | Read if exists |
| `memory_bank/t1_axioms/system_patterns.md` | **Yes** | Read if exists |
| `memory_bank/t1_axioms/behavior_context.md` | **Yes** | Read if exists |
| `memory_bank/t1_axioms/architecture_context.md` | Recommended | Read if exists |
| `memory_bank/t1_axioms/ux_accessibility_context.md` | Recommended | Read if exists |
| `memory_bank/t1_axioms/qa_context.md` | Recommended | Read if exists |
| `memory_bank/t1_axioms/knowledge_graph.md` | Recommended | Read if exists |
| `memory_bank/t1_axioms/module_support_map.yaml` | Recommended | Read if exists |
| `memory_bank/t2_execution/workflow_contract.md` | Recommended | Read if exists |
| `memory_bank/t2_execution/current_roadmap.md` | Recommended | Read if exists |
| `memory_bank/t2_execution/framework_contract.md` | Recommended | Read if exists |
| `memory_bank/t2_execution/adapter_state.yaml` | Recommended | Read if exists |
| `memory_bank/t3_archive/README.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/gate_runs/README.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/release_evidence/README.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/reviews/README.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/reviews/review-index.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/sprint_snapshots/README.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/sprint_snapshots/story-closure-index.md` | Recommended | Read if exists |
| `memory_bank/t3_archive/amendments/README.md` | Recommended | Read if exists |
| `memory_bank/README.md` | Recommended | Read if exists |

If `basic_law_index.md` is missing: "No constitution detected. Run `/constitute`
to establish one." Stop here — nothing else to check.

If `basic_law_index.md` exists but older projects only have T0/T1 files, report
`NEEDS ATTENTION` with a migration recommendation. Do not mark old T0/T1-only
projects `CRITICAL` unless a required T0 file or `tech_context.md` is missing.

If `memory_bank/t0_core/knowledge_graph.md` exists, report it as a deprecated compatibility path. The canonical path is now
`memory_bank/t1_axioms/knowledge_graph.md`.

---

## Step 2: Read the Constitution

Read `memory_bank/t0_core/basic_law_index.md` and extract:
- Core thesis (Support ID: BL-01)
- All laws/ principles (Support IDs: BL-02 through BL-06)
- Each law's current-state requirement

Read `memory_bank/t0_core/active_context.md` and extract:
- Current working state (State A-E)
- Module status summaries
- Active risks and open decisions

Read `memory_bank/t0_core/current_state.md` when present and extract:
- Current phase
- Current blocker
- Next command
- Stage source

Read `memory_bank/t1_axioms/tech_context.md` and extract:
- Language, framework, platform
- Performance budgets
- External dependencies

Read T2 files when present:
- `memory_bank/t2_execution/workflow_contract.md`
- `memory_bank/t2_execution/current_roadmap.md`
- `memory_bank/t2_execution/framework_contract.md`
- `memory_bank/t2_execution/adapter_state.yaml`

Read T3 indexes when present:
- `memory_bank/t3_archive/qa_evidence_index.md`
- `memory_bank/t3_archive/gate_runs/`
- `memory_bank/t3_archive/release_evidence/`
- `memory_bank/t3_archive/reviews/`
- `memory_bank/t3_archive/reviews/review-index.md`
- `memory_bank/t3_archive/sprint_snapshots/`
- `memory_bank/t3_archive/sprint_snapshots/story-closure-index.md`
- `memory_bank/t3_archive/amendments/`

---

## Step 3: Adapter Freshness Check

For the submission boundary, inspect actual diffs, the Git index and intended
publication contents under the governing Source/Target rules. Local maintenance
files, including ignored session logs, may stay inside or outside the repository;
location/presence alone is not a finding. `.gitignore` does not exclude tracked
content. Preserve business QA and required neutral inputs; this audit does not
authorize moving/deleting files, untracking or changing log locations.
Read `standards/skill-purpose.md` and classify full skill bodies/references first.
Developer skills/exclusive overlays and references stay local-only even when bespoke
or fully projected. Split mixed content; verify actual delivered functions/user tasks
for use claims and real independent readers for configuration. Test/release names,
paths or overlay labels give no exception. Business code/tests/QA/documents keep
their own rules. This check does not untrack or change them.
Check required local inputs and Target Git candidates separately. In a target, reusable
templates, generic standards/workflow originals and skill-testing definitions stay local-only;
locally readable ignored inputs are not missing Git deliverables and do not become
Git candidates merely because a workflow requires them.

First read `memory_bank/t2_execution/framework_contract.md` when it exists.
Its project/Source binding section records the actual project role, sole Source,
installed revision and runtime, exact installed paths, required neutral inputs
and project-owned customizations. Unknown values remain unconfigured.

If that control-plane file is absent or lacks a binding, use only existing
project-owned documentation/configuration selected by the project's governing
instructions and defining those same fields and their owners. Do not invent a
configuration path/schema, restore a maintenance profile/lock, or create the
Memory Bank for this audit. Without a documented binding, report its affected
scope as Unknown/NOT AVAILABLE and continue independent installed-input checks;
no freshness state write is available. A local manifest or copied script alone
does not establish that this is the CDD Source library.

For a consumer, directly read the selected installed entries and their actual
required references. Report missing/unread originals with their affected scope.
These observations work offline and need no local maintenance toolkit. They do
not establish live Source freshness. A consumer freshness comparison must bind
its exact installed allowlist against the actual sole Source revision/expected
outputs and approved project differences; a Source-only check is insufficient.

If the Source is unavailable, the binding is unresolved, or no valid comparison
covers the consumer's installed files, report `Live adapter freshness: NOT AVAILABLE`
with the exact limitation. Preserve any recorded state and continue
independent constitution/installed-input checks. Do not add general source
mirrors/checkers to consumer Git delivery or label an uninitialized record fresh.

Use only an actually available, authorized read-only comparison that covers the
applicable owner and exact installed paths. Without such a comparison, keep
NOT AVAILABLE and continue at Step 4 without offering a state write. A missing
optional checker does not hide a failed comparison that actually ran.

For an applicable comparison, bind the actual owner, Source revision, full input
identities, complete compared paths, approved project differences, result and
verification time. A consumer comparison must include its installed allowlist;
a Source-library result alone is insufficient. Record the real comparison
method without inventing an invocation. Missing, malformed or mismatched evidence
is INVALID or NOT AVAILABLE for its affected scope; preserve recorded state and
offer no state write. Valid evidence may establish fresh/stale only for its
declared scope. Evidence used with the existing adapter-state schema must include
`schema_version: 1`, a `status` of `fresh` or `stale`, full 64-character
lowercase hexadecimal `manifest_digest` and `source_digest`, ISO-8601 UTC
`checked_at`, the actual `checked_commit`, `counts` and `check_command`.
Validate all fields and complete input scope; record the actual comparison method
in `check_command`, never a fabricated invocation. Missing, malformed or
scope-mismatched fields are INVALID and offer no state write. Manual observations
that do not supply this valid record remain separate from CURRENT/OUTDATED and
the optional YAML-record branch below.

Compare an applicable valid live result with
`memory_bank/t2_execution/adapter_state.yaml`:

| Recorded state | Meaning |
|----------------|---------|
| `MISSING` | The memory bank exists but the adapter-state template was not initialized |
| `UNINITIALIZED` | The deterministic template exists and has no recorded evidence |
| `CURRENT` | Applicable checked owner/scope, recorded status and both digests match the live result |
| `OUTDATED` | A prior record exists but status or either digest differs |
| `UNVERIFIED` | A prior record exists but no applicable live comparison is available |

Report both values separately: `Live adapter freshness: FRESH/STALE/INVALID/NOT AVAILABLE`
and `Recorded adapter state: CURRENT/OUTDATED/UNINITIALIZED/MISSING/UNVERIFIED`. Include
all non-zero counts and drift paths. A clean `checked_commit` is contextual;
the two digests are the authoritative identity of the checked inputs.

### Optional approved state record

Only for a valid live result covering the actual checked owner/inputs, prepare
the complete YAML draft with this field order and actual live values. Use its
actual portable check description; do not store host-specific paths in a target
project. No unavailable or Source-only consumer check is recordable:

```yaml
schema_version: 1
status: fresh
manifest_version: 2
manifest_digest: "[live manifest_digest]"
source_digest: "[live source_digest]"
checked_commit: "[live checked_commit]"
checked_at: "[live checked_at]"
check_command: "[actual live portable check command/description]"
```

Use `stale` instead of `fresh` when the live check reports drift. Show the
entire draft. Reuse existing matching authority for this exact record; otherwise
ask exactly:

`May I write this adapter freshness record to memory_bank/t2_execution/adapter_state.yaml?`

If approved, write only that file. If declined, leave the repository unchanged
and state that the report was read-only. Never create `memory_bank/` from this
skill; when the control plane or `framework_contract.md` is missing, recommend
`/constitute`.

## Step 4: Alignment Check

For each constitutional principle, check alignment with the codebase:

### 3a: Principle → Code Alignment

For each law in `basic_law_index.md`, perform a quick alignment scan:

1. Read the law's current-state requirement
2. Check whether the codebase respects it
3. Flag violations or uncertainties

Example checks:
- Law requires "no function over 20 lines" → grep for functions, check length
- Law requires "API stability: no breaking changes" → check for deprecation markers
- Law requires "all public APIs documented" → check docstring coverage in `src/`
- Law requires "tests before merge" → check test file count vs source file count

For each law, produce one of:
- **ALIGNED** — evidence found that the law is being followed
- **CONCERN** — potential violation or insufficient evidence
- **UNABLE TO CHECK** — law is abstract or can't be auto-verified (e.g., "prioritize user experience")

### 3b: Tech Context → Reality Check

Compare `tech_context.md` against actual project state:
- Is the declared language actually used? (Glob `src/**` for language files)
- Are declared dependencies actually in the project? (Check config files)
- Are performance budgets plausible given the codebase size?

---

## Step 5: Gap Detection

Identify what's missing or stale:

| Gap | Detection |
|-----|-----------|
| **Missing T0 current state** | `memory_bank/t0_core/current_state.md` does not exist |
| **Missing T1 required docs** | `tech_context.md`, `system_patterns.md`, or `behavior_context.md` missing |
| **Missing T1 recommended docs** | `architecture_context.md`, `ux_accessibility_context.md`, `qa_context.md`, `knowledge_graph.md`, or `module_support_map.yaml` missing |
| **Deprecated knowledge graph path** | `memory_bank/t0_core/knowledge_graph.md` exists |
| **Missing T2 workflow contract** | `memory_bank/t2_execution/workflow_contract.md` does not exist |
| **Missing T2 current roadmap** | Project has roadmap evidence but `memory_bank/t2_execution/current_roadmap.md` is missing |
| **Missing framework contract** | `memory_bank/t2_execution/framework_contract.md` does not exist |
| **Missing adapter state** | `memory_bank/t2_execution/adapter_state.yaml` does not exist |
| **Uninitialized adapter state** | State exists with `status: uninitialized`; only valid applicable live evidence can initialize the record |
| **Unavailable live comparison** | Exact Source/binding/check evidence unavailable; preserve recorded state and continue independent checks |
| **Stale adapters** | Valid live comparison evidence reports `status: stale` or non-zero stale/missing/extra/invalid counts |
| **Outdated adapter record** | Recorded status or digests differ from the live result |
| **Missing T3 archive README** | `memory_bank/t3_archive/README.md` does not exist |
| **Missing T3 gate archive** | Gate evidence exists but `memory_bank/t3_archive/gate_runs/README.md` is missing |
| **Missing QA evidence index** | QA evidence exists but `memory_bank/t3_archive/qa_evidence_index.md` is missing |
| **Missing release evidence archive** | Release evidence exists but `memory_bank/t3_archive/release_evidence/README.md` is missing |
| **Missing review index** | Review artifacts exist but `memory_bank/t3_archive/reviews/review-index.md` is missing |
| **Missing story closure index** | Completed stories exist but `memory_bank/t3_archive/sprint_snapshots/story-closure-index.md` is missing |
| **Missing README** | `memory_bank/README.md` does not exist |
| **Stale tech context** | Tech context mentions old versions or unused dependencies |
| **Drifted principles** | Law says X, code does Y |
| **No review mode set** | `production/review-mode.txt` does not exist |

---

## Step 6: Present Report

Keep it concise. Use this format:

```
## Memory Bank Health: [Project Name]

**Core thesis:** [from BL-01, one line]
**Constitution established:** [date from active_context.md or file timestamp]
**Current phase:** [from current_state.md or production/stage.txt]

### T0 Current Truth
- Laws: [present/missing/stale]
- Active context: [present/missing/stale]
- Current state: [present/missing/stale]

### T1 Supporting Context
- Tech context: [present/missing/stale]
- System patterns: [present/missing/stale]
- Behavior context: [present/missing/stale]
- Recommended context: [summary]

### T2 Execution Control
- Workflow contract: [present/missing]
- Current roadmap: [present/missing/not started]
- Framework contract: [present/missing]
- Live adapter freshness: [fresh/stale/invalid/not available]
- Installed inputs: [observed complete / affected missing or unread paths]
- Recorded adapter state: [current/outdated/uninitialized/missing/unverified]

### T3 Archive Indexes
- Archive README: [present/missing]
- QA evidence index: [present/missing/not applicable yet]
- Release evidence: [present/missing/not applicable yet]

### Principles (N/M aligned)
- [Support ID]: ALIGNED — [brief evidence]
- [Support ID]: ALIGNED — [brief evidence]
- [Support ID]: CONCERN — [what's wrong, suggestion]

### ✓ Tech Stack
- Language: [X] ✓
- Framework: [Y] ✓
- Platform: [Z] ✓
- [Any concerns]

### → Gaps
- [Gap 1 — with concrete fix, e.g. "Run /constitute-check for a read-only audit; updates need separate authority"]
- [Gap 2]

### → Recommendations
1. [Highest priority action]
2. [Secondary action]

---
**Overall:** [HEALTHY / NEEDS ATTENTION / CRITICAL]
```

**Severity levels:**
- **HEALTHY**: Required T0/T1 artifacts present, T2/T3 indexes appropriate for stage, all checkable laws ALIGNED
- **NEEDS ATTENTION**: Old T0/T1-only memory bank, stale/uninitialized/outdated adapter state, 1-2 CONCERNs, or missing recommended T1/T2/T3 indexes
- **CRITICAL**: Missing `basic_law_index.md`, missing required T0/T1 files, 3+ CONCERNs, or stale constitution

If verbosity argument is `full`, add a detailed per-law analysis section with
the specific evidence found for each alignment check.

---

## Edge Cases

- **No constitution**: "No constitution detected. Run `/constitute` to establish your project's governing principles." Stop.
- **Old T0/T1-only memory bank**: "Your constitution exists, but the T2/T3 governance control plane is not initialized. Run `/constitute` to refresh the memory-bank skeleton." Continue with `NEEDS ATTENTION`.
- **Missing adapter templates in an older memory bank**: Recommend `/constitute` to initialize both framework files; do not create the control plane from this audit.
- **Unavailable Source/comparison**: Report NOT AVAILABLE and any historical recorded state separately; preserve it. Complete installed-input and constitution observations offline without requiring Source trees or tools.
- **Stale live check**: Report every drift class for the actual compared owner/paths and offer to record `status: stale`; regeneration remains a separate, explicitly requested action.
- **Invalid comparison evidence**: Report `INVALID`, preserve any prior state file, and do not write partial or fabricated values.
- **Constitution exists but is very old**: Note the date — "Your constitution was established [N months] ago. Much may have changed. Consider running `/constitute` to refresh it."
- **Path D project (existing code, new constitution)**: Flag likely drift — "Your constitution was recently established. Some existing code may not yet align. This is normal for brownfield adoption — prioritize alignment iteratively."
- **All laws are abstract (can't auto-check)**: "Your principles are abstract — they can't be automatically verified. Consider adding falsifiable current-state requirements to each law for future audits."

---

## Collaborative Protocol

- **Read-only by default.** The sole exception is an exact adapter-state YAML record after explicit approval.
- **No hidden writes.** Running the comparison, declining the draft, or encountering invalid comparison evidence must leave the repository unchanged.
- **Be honest.** Don't sugarcoat drift or gaps.
- **Be specific.** Every gap must come with a concrete fix suggestion.
- **One primary recommendation.** The user should leave knowing exactly one thing to do next.
