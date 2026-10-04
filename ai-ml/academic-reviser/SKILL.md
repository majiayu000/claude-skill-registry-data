---
name: academic-reviser
description: "Self-review, audit, or verify CS/AI/ML paper drafts as a critical peer reviewer. Three-round review (evidence→argument→style) with Verification Status and debt tracking. Use when: reviewing a paper draft before submission, checking evidence compliance of claims, simulating peer reviewer feedback, verifying citation closure and evidence debts, performing cross-section consistency checks. Triggers on: self review, 自查, verification, 审稿, evidence compliance, peer review, 论文审查, draft audit, 验证论文, 检查引用, cross-section review, 审修, draft verification."
---

# Academic Reviser

将此 skill 视为"挑剔审稿人代理"——像 peer reviewer 一样审查草稿，按证据→论证→风格三轮顺序执行。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines non-negotiable rules, bounded assessment, termination conditions, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables, debt types, and Verification Status format.
   - `anti-patterns.md` defines known failure modes, correct alternatives, and self-deception signals.
4. Detect the mode using the manifest's `mode` axis. When input materials are incomplete, declare a Bounded Assessment before proceeding.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

Debt types tracked: `prose_debt`, `section_contract_debt`, `citation_debt`, `evidence_debt`, `figure_debt`, `protocol_debt`, `result_debt`, `rationale_debt`. Schema: `skills/shared/schemas/verification-report.md`.

## Modes

| Mode | Use when |
|---|---|
| `full-section-review` | Complete 3-round review + Verification for a single section |
| `cross-section-review` | Cross-section consistency check |
| `verification-only` | Verdict only, no re-review |
| `targeted-review` | Specific issue (e.g. citation closure only) |
| `targeted-evidence-mode` | Evidence compliance only (orchestrator Step 9.5) |
| `mock-reviewer-package` | Optional pre-submission 3-reviewer package |

## Agent Dispatch

`agents/reviser_agent.md` dispatched by orchestrator at Step 9.5 or Step 9.8. Subagent returns structured review content; must not modify project files or invent reviewer identities, experiments, citations, or unprovided evidence.

## Independent Use

| Input | Mode | Priority | Behavior |
|---|---|---|---|
| Section draft | full-section-review | 2 (path trigger) | Full 3-round review |
| Multiple sections | cross-section-review | 2 (path trigger) | Consistency only |
| "只用 verdict" | verification-only | 1 (explicit) | Verdict only |
| Specific issue | targeted-review | 1 (explicit) | Targeted check |
| Evidence focus | targeted-evidence-mode | 1 (explicit) | Evidence compliance |
| "审稿包" / pre-submission | mock-reviewer-package | 1 (explicit) | Optional reviewer package |

| Scenario | Recommended |
|---|---|
| Just reviewing a draft | This skill (standalone) |
| During paper drafting | academic-paper-writer orchestrator |
| After polishing pass | academic-polishing → this skill |
