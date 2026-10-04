---
name: spec-drift-check
description: Audits a WP brief for drift against current code — extracts claims, verifies each, emits PROCEED/STOP verdict. Use when starting a new WP, before consuming a spec as binding, or when a doc references paths/lines/functions.
when_to_use: Stage 0 of any new WP implementation; before consuming a WP YAML, plan doc, or memory entry as binding; anytime a spec references file paths, line numbers, or function names the next action depends on.
argument-hint: "<spec-path> [<additional-context>]"
arguments: spec_path
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - Write
disallowed-tools:
  - Edit
version: 1.0.1
author: "Ashay Kubal @ Qball Inc."
---

# spec-drift-check

Audits a Work Package brief (or any spec document) for drift against the current code state. The skill extracts every verifiable factual claim from the subject spec — file paths, line refs, function and type names, constants, sequence-of-events claims, dependency claims, state claims — verifies each against current code via Grep / Read / Bash, categorizes findings (CONFIRMED, drift variants, AC re-interpretation, GAP) at LOW / MEDIUM / HIGH severity, rewrites the implementation plan based on findings, and emits a structured verdict (PROCEED, PROCEED_ADJUSTED, STOP_USER_APPROVAL). The verified plan supersedes the original spec for the rest of the work package.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|----------------------|
| Pre-WP verification | "Run spec drift check on the P10.16 brief", "Verify this brief before I start the WP" |
| Drift audit | "Check for drift between the spec and current state", "Audit this brief for stale claims" |
| Claim verification | "Extract claims from this brief and verify them", "Are the file refs in this doc still valid?" |

**DO NOT use for:**
- Implementing a brief (use the relevant implementer skill / agent — this skill is verification only)
- General code review or PR review (use `code-review`)
- Test audit (use `test-audit`)
- Debugging issues (use `issue-debugging`)

**This skill is READ-ONLY with respect to the subject spec.** It does NOT modify the input brief or any code referenced by it. The skill DOES write its own outputs — verification log under `$PROJECT_DIR/logs/spec-verify-*.md` and diagnostic YAML under `$PROJECT_DIR/logs/diagnostics/` — those are not "modifications" of the subject. To FIX issues found in the subject spec, the user invokes a separate skill (manual edits, `fix-bug`, or an implementer agent). The skill's value is the audit + adjusted plan, not the fix. The frontmatter lists `Edit` under `disallowed-tools`, which removes it from the available tool pool while the skill runs, preventing accidental subject-spec modification at the permission layer.

This skill follows the **Reviewer** archetype with the `standalone`, `multi-source`, and `pipeline-stage` sub-patterns. It runs in **Main Context Orchestration** (no sub-agent fork) by deliberate design — the verifier needs to read across the full claimed scope and the orchestrator must absorb the verdict directly to make scope-expansion decisions.

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Step 1 guide** | `references/step-1-claim-extraction.md` | **REQUIRED** | Before Stage 1 |
| **Step 2 guide** | `references/step-2-verification-methods.md` | **REQUIRED** | Before Stage 2 |
| **Step 3 guide** | `references/step-3-categorization.md` | **REQUIRED** | Before Stage 3 |
| **Step 4 guide** | `references/step-4-plan-adjustment.md` | **REQUIRED** | Before Stage 4 |
| **Step 5 guide** | `references/step-5-log-template.md` | **REQUIRED** | Before Stage 5 |
| **Step 6 guide** | `references/step-6-decision-matrix.md` | **REQUIRED** | Before Stage 6 |
| **Anti-patterns** | `references/anti-patterns.md` | **REQUIRED** | Throughout |
| **Output template** | `references/output-template.md` | **REQUIRED** | When writing the verification log |
| **Findings schema** | `templates/findings-output.yaml` | **REQUIRED** | When emitting structured YAML output |

---

## Usage

```
/spec-drift-check <spec-path> [<additional-context>]
```

**Arguments:**
- `<spec-path>` — Required. Path to the brief or spec document to audit (e.g., `plans/task-briefs/P10.16-statusline-lock-cleanup-observability.md`).
- `<additional-context>` — Optional. Free-text context the orchestrator should consider (e.g., "WP was authored 5 sessions ago", "previous attempt blocked at AC-3").

**Examples:**
- `/spec-drift-check plans/task-briefs/P10.16-statusline-lock-cleanup-observability.md`
- `/spec-drift-check plans/task-briefs/P10.18-spec-drift-check-skill.md "drafted in S119; verify before implementing"`

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping. Skipping items violates SC1-SC3 (Skill Compliance Rules in Rules.md).**

This skill is a read-only Reviewer using Main Context Orchestration. The subject artifact MUST NOT be modified. Findings MUST be severity-classified per the rubric. Follow every item in order:

- [ ] **Stage 0 — Pre-Flight**: Subject spec file exists and is readable
- [ ] **Stage 0 — Pre-Flight**: All 8 reference docs loaded into context
- [ ] **Stage 1 — Claim Extraction**: Every concrete factual claim in the spec extracted to numbered checklist (per references/step-1-claim-extraction.md)
- [ ] **Stage 2 — Verification**: Each claim verified against current code via Grep/Read/Bash (per references/step-2-verification-methods.md). MUST grep + verbatim quote, NOT recall
- [ ] **Stage 3 — Categorization**: Each finding categorized (CONFIRMED / DRIFT-line-ref / DRIFT-wrong-file / DRIFT-missing-scope / DRIFT-undeclared-scope / AC-reinterpretation / GAP) with LOW/MEDIUM/HIGH severity (per references/step-3-categorization.md)
- [ ] **Stage 4 — Plan Adjustment**: Implementation plan rewritten based on findings (per references/step-4-plan-adjustment.md)
- [ ] **Stage 5 — Log**: Verification log written to `$PROJECT_DIR/logs/spec-verify-{session}-{topic}.md` (per references/step-5-log-template.md)
- [ ] **Stage 6 — Decide**: Verdict emitted (PROCEED / PROCEED_ADJUSTED / STOP_USER_APPROVAL) per finding mix (references/step-6-decision-matrix.md)
- [ ] **Stage 7 — Bind**: Verified plan SUPERSEDES original spec for rest of WP
- [ ] **READ-ONLY enforced (subject spec)**: Subject spec MUST NOT be modified at any point during review. Skill outputs (verification log + diagnostic YAML) are NOT modifications of the subject — those are deliverables the skill writes to `$PROJECT_DIR/logs/`. `Edit` is listed under `disallowed-tools` (and absent from `allowed-tools`) to enforce subject-read-only at the permission layer
- [ ] **Main Context Orchestration**: Do NOT spawn sub-agents for the verification work — verifier needs full claimed scope; orchestrator needs verdict directly
- [ ] **Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/spec-drift-check-{YYYYMMDD-HHMMSS}.yaml`
- [ ] **Findings + verdict presented to user via AskUserQuestion if STOP_USER_APPROVAL**

---

## Workflow

The skill executes the canonical 7-step methodology developed by clear-Claude (CLEAR framework). Each stage has a dedicated reference doc with full procedure detail; the summaries below are orchestration only.

### Stage 0 — Pre-Flight

Verify `<spec-path>` exists and is readable. Load all 8 reference docs (`references/step-1-claim-extraction.md` through `references/output-template.md` plus `references/anti-patterns.md`) and `templates/findings-output.yaml`. STOP if the spec is missing or malformed.

### Stage 1 — Claim Extraction

Read the spec end-to-end. Enumerate every concrete factual claim into a numbered checklist, in priority order (load-bearing first). Cover: file paths, line refs, function/method/class/type names, constants/schema versions/enum values, sequence-of-events claims, dependency claims, state claims. See `references/step-1-claim-extraction.md` for full claim taxonomy and the checklist scaffold.

### Stage 2 — Verification

For each claim from Stage 1, run the matching verification recipe (Grep / Read at offset / `git log --grep` / source-of-truth artifact read). MUST grep + verbatim quote rather than recall — recall hallucinates. Capture the actual current state alongside the claim. See `references/step-2-verification-methods.md` for per-claim-type recipes.

### Stage 3 — Categorization

For each verified claim, assign a category (CONFIRMED / DRIFT — line-ref / DRIFT — wrong file / DRIFT — missing scope / DRIFT — undeclared scope / AC re-interpretation / GAP) and a severity (LOW / MEDIUM / HIGH). Severity drives the verdict and the plan adjustment. See `references/step-3-categorization.md` for the category table and severity decision tree.

### Stage 4 — Plan Adjustment

Rewrite the spec's plan section based on the findings: drop deliverables that are now no-ops, add deliverables for undeclared-scope HIGHs, re-target paths for wrong-file DRIFTs, resolve AC re-interpretations explicitly with rationale, re-estimate the token budget if scope changed. See `references/step-4-plan-adjustment.md` for the rewrite procedure and a before/after example.

### Stage 5 — Log

Write the verification log to `$PROJECT_DIR/logs/spec-verify-{session}-{topic}.md` using the canonical YAML schema (findings, ac_reinterpretations, adjusted_plan, verification_checklist, proceed_decision, roi). See `references/step-5-log-template.md` for the full template and field-by-field guidance; `references/output-template.md` is the schema reference.

### Stage 6 — Decide

Emit a verdict from the finding mix per the decision matrix:
- All CONFIRMED → **PROCEED**
- Only LOW + MEDIUM → **PROCEED_ADJUSTED**
- Any HIGH → **STOP_USER_APPROVAL**

When STOP_USER_APPROVAL fires, surface the HIGH findings + proposed adjusted scope to the user via AskUserQuestion before any implementation. See `references/step-6-decision-matrix.md` for the AskUserQuestion template.

### Stage 7 — Bind

The verified plan in the log SUPERSEDES the original spec for the rest of this WP. Implementation work follows the verified plan; deviations require explicit user approval. The implementer is expected to consume the log, not the original spec.

---

## Sub-Patterns Documented

This skill exhibits three sub-patterns from the Reviewer archetype's catalog. Sub-patterns are additive — all three apply.

### `standalone`

> **Definition**: Reviewer is invoked directly by the user as a primary action.
>
> **When to use**: The review is the user's goal — they're auditing something specifically.

**How it shapes this skill**:
- User-facing CLI invocation (`/spec-drift-check <spec-path>`).
- Verdict is presented prominently; STOP_USER_APPROVAL surfaces via AskUserQuestion.
- The verification log is a deliverable the implementer (or next session) consumes — written to `$PROJECT_DIR/logs/spec-verify-{session}-{topic}.md`.

### `multi-source`

> **Definition**: Reviewer reads multiple prior artifacts (logs, prior-stage outputs, external context) and synthesizes a verdict ACROSS all of them.
>
> **When to use**: The review's value is the cross-artifact analysis (gap detection, consistency check, holistic verdict).

**How it shapes this skill**:
- Stage 0 Pre-Flight explicitly loads ALL inputs (the subject spec + every claim's referenced source-of-truth artifact). Lazy loading would miss cross-artifact inconsistency.
- Findings include cross-references between sources (e.g., "D-04: Spec claims `active_tasks.yaml` shows P10.18 status=in_progress, but actual yaml shows status=pending").
- Verdict reflects holistic judgment across spec + code + state artifacts, not per-source pass/fail.

### `pipeline-stage`

> **Definition**: Reviewer operates as a single stage within a larger orchestrating Pipeline skill.
>
> **When to use**: The review is one step in a multi-stage workflow (audit → adjust → implement, or scan → classify → report).

**How it shapes this skill**:
- Once **SD1** ships (per `P10.20-drift-enforcement-bundle.md`), this skill is mandated as **Stage 0** of every WP implementation flow. SD1's binding contract: orchestrator must invoke `/spec-drift-check <brief>` before any implementation work, and consume the resulting verification log (not the original spec) for the rest of the WP.
- The verification log at `$PROJECT_DIR/logs/spec-verify-{session}-{topic}.md` is the **canonical machine-readable output** the next stage reads. Schema is locked in `references/output-template.md` so downstream consumers can parse it deterministically.
- When invoked as a pipeline stage (vs user-direct via `standalone`), the verdict still surfaces to the user via AskUserQuestion when STOP_USER_APPROVAL fires — the user is the explicit decision point on scope-changing HIGH findings, not the orchestrator. The pipeline does NOT auto-proceed past a STOP verdict.
- The downstream stage (implementer or implementer agent) is contractually expected to read `proceed_decision`, `adjusted_plan`, and `verification_checklist` from the log; deviations from the verified plan require fresh user approval.
- See `references/step-6-decision-matrix.md` for the orchestrator-vs-user decision boundary in pipeline-stage mode.

---

## Severity Rubric

Full rubric: `references/step-3-categorization.md`. Compact summary:

| Severity | Definition | Verdict Implication |
|----------|------------|---------------------|
| **CRITICAL** | Reserved — escalates to HIGH for verdict purposes | STOP_USER_APPROVAL |
| **HIGH** | Wrong-file DRIFT, undeclared-scope DRIFT, GAP — scope-changing or block-level | STOP_USER_APPROVAL |
| **MEDIUM** | Missing-scope DRIFT, AC re-interpretation — adjustable without scope expansion | PROCEED_ADJUSTED |
| **LOW** | Line-ref DRIFT — file correct, line off | PROCEED_ADJUSTED (doc fix in implementation comments) |

Do NOT invent severities. Each finding maps to exactly one tier.

---

## Verdict Decision Matrix

Full matrix: `references/step-6-decision-matrix.md`. Compact summary:

| Finding mix | Verdict |
|-------------|---------|
| All CONFIRMED | **PROCEED** with original plan |
| Only LOW + MEDIUM findings | **PROCEED_ADJUSTED** with adjusted plan; flag in summary |
| Any HIGH finding (esp. scope changes) | **STOP_USER_APPROVAL** — surface to user via AskUserQuestion before implementing |

---

## Anti-Patterns

Full catalog (with examples + remediation): `references/anti-patterns.md`. Five anti-patterns:

- Skipping Step 1 — embedded claims missed, drift caught late
- Verifying after implementation starts — drift caught late = wasted work
- Treating handoff/memory as immutable truth — they are snapshots in time
- Recalling claims rather than grep-quoting verbatim — recall hallucinates
- Auto-applying drift fixes without user sign-off when scope changes (HIGH)

---

## Anti-Thought Trap

If you find yourself thinking "I'll just spawn a sub-agent to do this faster" — STOP. That violates the Main Context Orchestration design intent. The verifier must read across the entire claimed scope and the orchestrator must absorb the verdict directly to make scope-expansion decisions. Sub-agent fork would force a context split.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Subject spec file not found | Report path; STOP — no audit possible |
| Subject spec file unreadable / parse error | Report; STOP — do NOT proceed on malformed input |
| Reference doc missing | Report which `references/*.md` is missing; STOP — cannot audit without methodology |
| Modification accidentally made to subject spec | Revert immediately via git; report violation; STOP |
| Verification command (Grep/Read/Bash) fails | Note in finding as `verification_error`; do NOT auto-classify as CONFIRMED |
| Log write fails | Retry once; if still failing, surface to user — do NOT silently drop the log |

---

## Token Budget

| Stage | Bound | Notes |
|-------|-------|-------|
| Stage 1 (Claim extraction) | Bounded by **spec size**, not project size | One full read of the subject spec; enumeration is linear in claim count |
| Stage 2 (Verification) | **Per-claim grep / read** — efficient | Each claim runs one or two targeted commands; no full-project scans |
| Stage 3-4 (Categorize + adjust) | Bounded by **finding count** | Single pass over Stage 2 output |
| Stage 5 (Log) | Bounded by **finding count** | Single Write call |
| Stage 6-7 (Decide + bind) | Constant | Verdict + handoff to next action |

The ROI section in the log captures actual cost vs estimated savings. Initial runs may show negative ROI; aggregate ROI across many invocations is what matters.

---

## Output Format

The verification log is written to `$PROJECT_DIR/logs/spec-verify-{session}-{topic}.md`. Compact YAML schema preview (full schema + field docs in `references/output-template.md`; YAML template in `templates/findings-output.yaml`):

```yaml
findings:
  - id: D-01
    category: drift-line-ref | drift-wrong-file | drift-missing-scope | drift-undeclared-scope | ac-reinterpretation | gap | confirmed
    severity: LOW | MEDIUM | HIGH
    spec_claim: "<verbatim quote from spec>"
    actual_state: "<what current code/state shows>"
    resolution: "<doc fix | plan adjustment | scope expansion | ask user>"

ac_reinterpretations:
  - ac: AC-N
    ambiguity: "<what's unclear>"
    resolution: "<chosen interpretation + rationale>"

adjusted_plan:
  deliverables: [...]
  estimated_token_delta: "+5K | -10K | 0"

verification_checklist:
  - "<item 1 for implementer to confirm at end>"

proceed_decision: PROCEED | PROCEED_ADJUSTED | STOP_USER_APPROVAL

roi:
  spent_tokens_estimate: "~5K"
  estimated_savings: "~15-25K"
  net: positive | break-even | negative
```
