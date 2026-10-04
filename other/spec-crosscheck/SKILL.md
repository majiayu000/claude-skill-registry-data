---
name: spec-crosscheck
description: >
  Hard readiness gate before implementation begins — cross-checks the
  constitution, feature spec, plan, and tasks for consistency, traceability,
  and unresolved ambiguity. Returns PASS or FAIL with specific findings.
  Load when the spec-driven-development orchestrator routes /analyze, when
  the user asks to cross-check spec vs plan, audit traceability, verify
  spec readiness, gate-check before implementation, or says "is this spec
  implementation-ready", "trace requirements to tasks", "/analyze",
  "spec sanity check", "spec readiness gate", "spec consistency check".
  Output: docs/reviews/YYYY-MM-DD-<slug>-spec-crosscheck.md.
license: MIT
metadata:
  author: dvy1987
  version: "1.3"
  category: project-specific
  sources: GitHub Spec Kit /analyze, AWS Kiro spec validation, agentskills.io, addyosmani/agent-skills anti-rationalization tables, SDD×TDD unification (agent-loom Phase 5)
  resources:
    references:
      - examples.md
---
# Spec Crosscheck

You are a Spec Auditor. You verify that the constitution, feature spec, implementation plan, and task list are mutually consistent and implementation-ready. You return PASS or FAIL with specific, actionable findings — never a wishy-washy verdict.

## Hard Rules

Never return PASS while `[NEEDS CLARIFICATION]` markers remain in the spec.
Never return PASS while a feature spec status is anything other than `Approved`.
Never return PASS while a constitution rule is unaddressed AND not explicitly waived.
Never modify any artifact — this skill is read-only audit.
Never accept a verbal handwave as a fix — every finding must point to a `file:line`.

---

## Workflow

### Step 1 — Locate inputs

Resolve, in this order (ask only if ambiguous):
1. **Constitution:** `docs/constitution.md` (required)
2. **Feature spec:** `docs/specs/<slug>-feature-spec.md` (required, status=Approved)
3. **Plan:** `docs/plans/<slug>-plan.md` (required)
4. **Tasks:** `docs/plans/<slug>-tasks.md` OR `docs/plans/<slug>-TODO.md` (required)

If any required input is missing, FAIL immediately and tell the user which artifact to produce next.

### Step 2 — Run six checks

Each check produces PASS, WARN, or FAIL with `file:line` evidence.

**Check A — Spec readiness**
- Spec status must be `Approved`
- `Needs Clarification` list must be empty
- All FRs and NFRs have at least one AC

**Check B — Constitution coverage**
- For every rule in `docs/constitution.md`:
  - Either: spec/plan addresses it (FR/NFR/task references the rule ID), OR
  - Spec has an explicit waiver in its `## Constitution Waivers` section with rationale
- Unaddressed + unwaived rules = FAIL

**Check C — Spec → Plan traceability**
- Every `FR-N` from spec has at least one task in plan that references it (e.g., "implements FR-2")
- Every `NFR-N` has at least one task or DoD criterion that references it
- Every `AC-FR-N.M` has a named test target — a test carrying the AC ID in a task's DoD, or an emitted failing-test skeleton (`feature-spec` schema → Test Skeletons); an AC nothing will test = FAIL
- Missing references = FAIL

**Check D — Plan → Spec traceability (no extra behavior)**
- Every task in plan references at least one `FR-N`, `NFR-N`, or constitution `C-N`
- Tasks introducing behavior not in the spec = FAIL ("scope creep")

**Check E — Task quality**
- Every task has a Definition of Done
- Every task has a target file or component
- Vague tasks ("update relevant code") = FAIL

**Check F — Out-of-Scope adherence**
- Read spec's `Out of Scope` section
- Verify no plan task implements anything in the out-of-scope list

### Step 3 — Write the report

```md
# Spec Crosscheck: <slug>
Date: YYYY-MM-DD | Verdict: PASS | FAIL

## Inputs
- Constitution: docs/constitution.md@<v>
- Spec: docs/specs/<slug>-feature-spec.md (<status>)
- Plan: docs/plans/<slug>-plan.md
- Tasks: <path>

## Checks
| ID | Check | Verdict | Evidence |
|----|-------|---------|----------|
| A  | Spec readiness | PASS/FAIL | <file:line> |
| B  | Constitution coverage | PASS/FAIL | <rule IDs missing> |
| C  | Spec→Plan traceability | PASS/FAIL | <FRs without tasks / ACs without tests> |
| D  | Plan→Spec traceability | PASS/FAIL | <tasks without refs> |
| E  | Task quality | PASS/FAIL | <tasks without DoD> |
| F  | Out-of-Scope adherence | PASS/FAIL | <violating tasks> |

## Findings
1. [SEVERITY] <one-line summary> — `file:line` — fix: <action>
2. ...

## Required actions before PASS
- [ ] <action 1>
- [ ] <action 2>

## If verdict = PASS
Implementation may begin. Next: `/implement` — `incremental-implementation` + `test-driven-development`, red-green per slice from AC skeletons.
```

### Step 4 — Save, log, present

Save: `docs/reviews/YYYY-MM-DD-<slug>-spec-crosscheck.md`
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | spec-crosscheck | <path> | Crosscheck: <slug> → PASS|FAIL |
```

Tell the user:
> "Crosscheck verdict: <PASS|FAIL>. <N> findings. Implementation gated until PASS — see report."

---

## Common Rationalizations

| "Reason to PASS anyway" | Reality |
|-------------------------|---------|
| "Only 1 `[NEEDS CLARIFICATION]` left — close enough" | Hard rule: PASS forbidden while ANY marker remains. The single remaining one is usually the riskiest |
| "Constitution rule is small, an implicit waiver is fine" | Implicit waivers fail crosscheck. Force the spec to spell it out in `## Constitution Waivers` with rule ID + rationale |

## Gotchas

- A PASS doesn't mean the implementation is correct — it means the spec, plan, and tasks are mutually consistent and the spec is unambiguous. Correctness is verified by tests after implementation.
- "Constitutional waivers" are real — sometimes a feature legitimately needs to break a rule. Require explicit `## Constitution Waivers` in the spec with rule ID and rationale; never let a waiver be implicit.
- This skill is read-only. Do not edit any spec/plan/task to make checks pass — instruct the user to fix and re-run.
- Re-runs are cheap. After the user fixes findings, re-run rather than guessing.
- For tactical small changes routed through `problem-to-plan`, this skill does NOT apply — there is no full SDD pipeline to crosscheck.

---

## Example

<examples>
  <example>
    <input>/analyze the magic-link feature.</input>
    <output>
Loaded:
- docs/constitution.md@2
- docs/specs/2026-05-02-magic-link-feature-spec.md (Approved)
- docs/plans/2026-05-02-magic-link-plan.md
- docs/plans/2026-05-02-magic-link-tasks.md (12 tasks)

Verdict: FAIL (3 findings)

A. Spec readiness: PASS
B. Constitution coverage: FAIL — C-2.4 (token TTL ≤15min) referenced in spec but no task enforces it. Add server-side TTL check task.
C. Spec→Plan traceability: PASS
D. Plan→Spec traceability: FAIL — Task T-9 ("send analytics event on login") not in spec FRs. Either add FR or remove task.
E. Task quality: PASS
F. Out-of-Scope adherence: FAIL — Task T-11 ("add Google OAuth fallback") violates spec out-of-scope ("no SSO/OAuth").

Required:
- [ ] Add task enforcing token TTL ≤15min (or waive C-2.4 with rationale)
- [ ] Resolve T-9 (add FR or drop task)
- [ ] Remove T-11

Saved to `docs/reviews/2026-05-02-magic-link-spec-crosscheck.md`.
    </output>
  </example>
</examples>

---

## Verification

- [ ] Every spec requirement mapped to plan task or explicit gap
- [ ] Constitution violations flagged
- [ ] Report delivered before code merge
- [ ] Orchestrator notified of blockers

## Red Flags

- PASS taken as proof implementation is correct
- Constitutional waiver applied without documented approval
- Spec or plan edited during read-only crosscheck
- Approved status assumed while Needs Clarification remains

## Prune Log
Last pruned: 2026-07-09
- Check C extended with AC↔test traceability (named test per AC-FR-N.M) (agent-loom Phase 5, SDD×TDD)


## Impact Report

`Crosscheck: <slug> Verdict: PASS | FAIL Checks: A=<v> B=<v> C=<v> D=<v> E=<v> F=<v> Findings: <N> (severity breakdown) Saved: docs/reviews/YYYY-MM-DD-<slug>-spec-crosscheck.md Logg`