---
name: staged-review-flow
version: "1.3.0"
user-invocable: false
description: "Shared review-stage flow for PDCA hosts: full decision review, code-design review for code-affecting solutions, Standards∥Spec dual-axis verdicts (no cross-axis merge rank), binary pass/fail, bounded auto optimization, design summary, and verification-report honesty composed with completion-evidence-discipline. Used by PDCA workflows. Triggers — 「阶段审查流程」「方案审查编排」「审查闭环」「验证报告诚实」「双轴审查」 / staged review flow, dual-axis review, verification honesty. Do NOT use as a standalone task workflow."
dependencies:
  - solution-review
  - code-design-review
  - completion-evidence-discipline
---

# Staged Review Flow

> Internal shared skill. Referencing workflows keep stage numbers, artifact destinations, and intentional divergences; this skill is the single source of truth for review and verification-report flow.
>
> **Prerequisite check:** verify each declared dependency is available when this skill is loaded. If one is missing, stop and print `npx skills add FuDesign2008/open-skills -g --skill '*' --yes`; do not silently reduce the review.

## Placeholder contracts

| Placeholder | Meaning | Referencing workflow supplies |
|---|---|---|
| `{next-stage}` | The stage entered after a passed review | Number and name |
| `{artifact-sink}` | Where review records or the design summary are persisted | Host-specific path or artifact |
| `{extra-dimensions}` | Additional host-only dimensions | Required checks and their sink |
| `{batch-overcap-behavior}` | Action after the automatic three-round limit in batch contexts | Host-specific behavior, or `N/A` |

Never hardcode a host workflow's stage numbers, OpenSpec paths, Jira state transitions, or batch policy.

## Review contract

1. Always load and run the complete `solution-review` framework: all core dimensions and strategic dimensions at the depth determined by reversibility. For code-affecting solutions, the strategic dimensions that carry long-term cost (cost-vs-value, team cognitive fit) run at least at standard depth, regardless of reversibility classification.
2. When the solution affects code — writing or modifying source files, including scripts and generated config code — also load and run `code-design-review` Layer A/B/C according to its applicability rules.
3. Apply `{extra-dimensions}` after the shared reviews. These checks supplement, never replace, `solution-review`.
4. Keep **two axes** separate in the report (labels MAY vary; meaning MUST NOT):
   - **Standards** — design / quality / smell / security fitness (`solution-review` strategic+core quality aspects and `code-design-review` when applicable).
   - **Spec** — fit to the chosen solution, ticket, or OpenSpec delta / stated requirements.
   Axes MAY run in parallel (e.g. separate subagents). **MUST NOT** merge both into one undifferentiated ranked list; a pass on one axis MUST NOT hide a fail on the other.
5. Aggregate blocking criteria into a binary overall result:
   - **Pass:** no blocking issues remain on **either** axis (and `{extra-dimensions}`).
   - **Fail:** at least one blocking issue remains on any axis.
6. Write the review record and passed design summary to `{artifact-sink}`.

## Review loop and gates

- In automatic mode, on failure optimize the solution, record the optimization, and rerun the full review. The initial review plus at most two optimized re-reviews is a three-round limit.
- At the limit, pause for the user unless `{batch-overcap-behavior}` specifies the host's batch handling.
- In manual mode, present the review report and wait for the user to approve, revise, or reselect the solution. Do not advance without an explicit user decision.
- A pass enters `{next-stage}`. A fail remains in solution optimization or returns to solution selection as directed by the user.

## Design summary

After a passed review, emit a structured design summary with goals, non-goals, decisions, risks and mitigations, and open questions. It is part of the review output, not a separate mandatory file, unless `{artifact-sink}` requires persistence.

## Verification-report honesty

Every verification result must disclose its execution state:

- **Executed:** include the command or action and a concise output/result summary.
- **Pending:** name the precise manual action still required.

Do not report designed scenarios or inferred correctness as completed verification. Browser or other unavailable manual interactions remain pending with actionable instructions.

**Compose with `completion-evidence-discipline`:** an **Executed** / pass claim is valid only when backed by fresh evidence from the **current turn** per that skill's Iron Law. Load `completion-evidence-discipline` at verification time; do not paste its prose into hosts.

## Integration guide

Referencing workflows must:

1. Declare `staged-review-flow` in frontmatter dependencies and perform their normal dependency gate (transitively requires `completion-evidence-discipline`).
2. At the review stage, load this skill and map all placeholders using numbers and names where applicable.
3. Keep only host orchestration: stage exit wording, `{extra-dimensions}`, `{artifact-sink}`, and `{batch-overcap-behavior}`.
4. Point their verification stage to this skill's honesty rule **and** `completion-evidence-discipline` in at most one or two sentences.

Do not duplicate binary tables, blocking lists, three-round loop prose, design-summary templates, dual-axis definitions, or verification-honesty blocks in hosts.
