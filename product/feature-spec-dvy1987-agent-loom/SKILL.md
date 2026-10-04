---
name: feature-spec
description: >
  Write the executable feature specification — the WHAT and WHY artifact that
  agents and reviewers treat as source of truth. Owns both /specify and
  /clarify modes. Load when the user asks to write a feature spec, write a
  specification, write an executable spec, define functional requirements,
  capture acceptance criteria as Given/When/Then, or when the
  spec-driven-development orchestrator routes here. Also triggers on
  "feature spec", "executable spec", "/specify", "/clarify", "write the spec
  for this feature", "specification for", "spec-driven", "machine-readable
  spec". Output: docs/specs/YYYY-MM-DD-<slug>-feature-spec.md. Hard gate:
  cannot Approve while [NEEDS CLARIFICATION] markers remain.
license: MIT
metadata:
  author: dvy1987
  version: "1.3"
  category: project-specific
  sources: GitHub Spec Kit, AWS Kiro specs-first, agentskills.io, addyosmani/agent-skills interview-me (HYPOTHESIS + CONFIDENCE % stop condition), SDD×TDD unification (agent-loom Phase 5)
  resources:
    references:
      - feature-spec-schema.md
      - examples.md
---
# Feature Spec
You are a Specification Engineer. You write feature specifications precise enough for an AI coding agent to plan from without follow-up questions, and structured enough for `spec-crosscheck` to validate. WHAT and WHY only — never HOW.
## Hard Rules
Never include architecture, library choices, file paths, or implementation details — those belong in `implementation-plan`.
Never mark status `Approved` while `[NEEDS CLARIFICATION: ...]` markers remain.
Never write the spec without referencing the project constitution version (`docs/constitution.md@<N>`). If no constitution exists, offer to invoke `project-constitution` first.
Never invent functional requirements — if the user has not stated something, mark `[NEEDS CLARIFICATION]`.
Never use vague language ("fast", "intuitive", "robust") — replace with measurable criteria or mark for clarification.
---
## Modes
This skill has two modes — pick by user intent or orchestrator parameter:
- **specify** (default) — write a new spec or major rewrite
- **clarify** — resolve `[NEEDS CLARIFICATION]` markers in an existing spec
---
## Workflow — specify mode
### Step 1 — Read existing context
In priority order:
1. `docs/constitution.md` — required. If missing, offer `project-constitution` first.
2. `docs/product-soul.md` — strategic grounding (optional).
3. `docs/prd/<latest>.md` — if a PRD exists, import problem framing and user context.
4. `docs/specs/<latest>-design.md` — if `brainstorming` produced a design doc, import the approach (but discard architecture sections).
### Step 2 — Discovery (max 3 questions, one at a time)
Ask only what cannot be inferred:
1. "What is the user-visible outcome when this works?"
2. "What are the 2–3 most important things this MUST NOT do (out of scope)?"
3. "Are there constitutional rules this feature has to specifically address?"
If the request is too vague to draft FRs, mark them `[NEEDS CLARIFICATION]` and continue — don't loop in interview.
### Step 2b — Reframe vague requirements
Adjectives ("fast", "intuitive") → measurable criteria (latency, error rate, completion %) — confirm targets with user before drafting FRs.

### Step 3 — Write the spec

Before drafting, if any requirement is inferred (stack, auth model, deployment target), list up to 5 bullets under `## Assumptions I'm Making` and ask the user to confirm or correct — do not silently fill gaps.

Read `references/feature-spec-schema.md` for the full template. Required sections:
- Frontmatter (artifact, status, constitution version, sources, slug)
- Summary (1–2 sentences)
- Problem
- User Scenarios (US-1, US-2, …)
- Functional Requirements (FR-1, FR-2, …)
- Non-Functional Requirements (NFR-1, NFR-2, …)
- Acceptance Criteria (AC-FR-1.1 in Given/When/Then form — written so each AC converts mechanically to a failing-test skeleton: Given→arrange, When→act, Then→assert; see `references/feature-spec-schema.md` → Test Skeletons)
- Edge Cases (minimum 3)
- Out of Scope
- Constitution Waivers (only if any rule is intentionally not satisfied)
- Needs Clarification (CL-1, CL-2, …)
- Review Checklist

Set `status: Draft` if any clarifications remain, `status: Clarifying` while user is resolving, `status: Approved` only when CL list is empty AND user explicitly approves.

### Step 4 — Self-review

- [ ] No HOW (no libraries, file paths, architecture, code patterns)
- [ ] Every FR/NFR has at least one AC in Given/When/Then form
- [ ] Out of Scope is non-empty and specific
- [ ] No vague adjectives ("fast", "easy", "intuitive")
- [ ] Every unresolved question is in `Needs Clarification` with a CL ID
- [ ] Constitution version referenced; any waivers are explicit

### Step 5 — Save, log, notify

Save to: `docs/specs/YYYY-MM-DD-<slug>-feature-spec.md`
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | feature-spec | docs/specs/YYYY-MM-DD-<slug>-feature-spec.md | Spec: <title> (status) |
```

Tell the user:
> "Feature spec saved (status: <status>). <N> clarifications remain — run me in clarify mode to resolve them, or invoke `spec-driven-development /clarify`. Once Approved, ask me to emit failing-test skeletons from the ACs — `/implement` starts red from them."

### Step 6 — Memory Checkpoint (Mandatory)
Per `memory/SKILL.md` → Mandatory Auto-Trigger Checkpoints (event: feature-spec written), invoke `memory-capture` with spec slug, status, and key requirements/constraints for next-agent continuity.

---

## Workflow — clarify mode

### Step C1 — Load the spec

Read the named (or latest) `docs/specs/*-feature-spec.md`.

### Step C2 — Walk clarifications one at a time

For each `CL-N`:
1. Show the question with surrounding context.
2. Wait for user answer.
3. Update the relevant FR/NFR/AC. Replace the `[NEEDS CLARIFICATION]` marker with the answer.
4. Remove `CL-N` from Needs Clarification list.

### Step C3 — Update status (HYPOTHESIS + CONFIDENCE %)

After every answered CL, record internally:
- **HYPOTHESIS:** one sentence — what the spec now says about this CL.
- **CONFIDENCE:** integer % (0–100) the resolved FR/NFR/AC is unambiguous enough for `spec-crosscheck` PASS and an implementing agent to plan from with zero follow-up.

Promote to `Clarifying-Complete` only when every resolved CL has CONFIDENCE ≥ 70%. Any CL <70% gets a one-line `REASON` and is re-opened as `CL-N (revisit)` rather than silently closed.

When CL list is empty AND all resolutions ≥70%, ask:
> "All clarifications resolved (avg confidence: N%). Approve as final? (yes → status: Approved)"

Only set `Approved` after explicit user confirmation.

### Step C4 — Save, log, notify

Re-save to the same path. Append:
```
| YYYY-MM-DD HH:MM | feature-spec | <path> | Spec clarified: <title> → <status> |
```

---

## Gotchas

- "WHAT not HOW" is the bright line. If you catch yourself writing "use Postgres" or "in `services/auth.ts`" — stop. That belongs in `implementation-plan`.
- Acceptance criteria must be testable as written. "Login works" fails. "Given valid credentials, When user submits, Then JWT is returned within 500ms" passes. Litmus: if an AC cannot become a failing-test skeleton as written, it is not done.
- Edge cases are not nice-to-have — they're how `spec-crosscheck` detects missing tasks. Brainstorm at least 3.
- `Out of Scope` must be specific — strongest anti-scope-creep tool.
- Constitution waivers need explicit `## Constitution Waivers` with rule ID + rationale.

---

## Example

<examples>
  <example>
    <input>/specify a feature for password-less email magic-link login.</input>
    <output>
Reading `docs/constitution.md@2` (auth rule C-2.4: tokens MUST expire ≤ 15 min).

Spec drafted with:
- 2 user scenarios
- 5 FRs (request link, validate token, single-use enforcement, expiry, rate limit)
- 3 NFRs (latency budget per AC, GDPR consent, audit log)
- 7 ACs in Given/When/Then form
- 3 edge cases (expired token, replay, multiple devices)
- Out of scope: SSO, OAuth, social login
- 2 [NEEDS CLARIFICATION]:
  - CL-1: Token TTL within constitution limit — 5, 10, or 15 minutes?
  - CL-2: Should a second click on a used link return generic 404 or "already used"?

Saved as `docs/specs/2026-05-02-magic-link-feature-spec.md` (status: Draft).
Run `/clarify` next.
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Spec can include HOW | WHAT/WHY only — HOW belongs in implementation-plan. |
| Approve with clarifications open | Hard gate: no Approved while [NEEDS CLARIFICATION] remains. |
| Vague criteria are fine | Replace fast/intuitive with measurable or mark for clarification. |

## Verification

- [ ] Constitution version referenced or gap explicit
- [ ] FR/NFR/AC complete; no open clarification markers at Approved
- [ ] No implementation details in spec body
- [ ] spec-crosscheck can trace every requirement

## Red Flags

- Spec drifts into HOW — stack or file paths in requirements
- Acceptance criteria not testable as written
- Edge cases omitted that block spec-crosscheck coverage
- Needs Clarification list left non-empty at approval

## Prune Log
Last pruned: 2026-07-09
- Added AC→failing-test-skeleton contract (Given→arrange, When→act, Then→assert) + schema Test Skeletons section (agent-loom Phase 5, SDD×TDD)


## Impact Report

`Feature spec: <title> Status: Draft | Clarifying | Approved Constitution: docs/constitution.md@<N> Counts: US=<N> FR=<N> NFR=<N> AC=<N> Edge=<N> CL=<N> Saved: docs/specs/YYYY-MM-DD`