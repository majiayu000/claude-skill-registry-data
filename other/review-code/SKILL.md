---
name: review-code
description: Audits a whole codebase in bounded waves of independent parallel auditors, publishes every verified finding ranked by severity, and applies only safe, in-scope repairs. Use when invoked explicitly for a codebase health review.
disable-model-invocation: true
---

# review-code

Review this codebase in bounded evidence-driven waves, publish the full report, and autonomously apply only safe, authorized improvements.

The task is the text given with this invocation.

---

## Bound the audit

Read applicable instructions, repository status, architecture, entry points, manifests, tests, configuration, and recent history. Preserve all staged, unstaged, untracked, and concurrent user work. Do not stash, reset, overwrite, or include unrelated changes.

Define the wave boundary before dispatch: subsystem, risk surface, or representative slice. Large repositories require multiple bounded waves; do not claim every line was reviewed when it was not.

## Adaptive audit panel

Scale each wave by scope:

- trivial: direct review or 1 specialist;
- modest: 2-3 auditors;
- normal: 4-7 auditors;
- broad, cross-system, or high-risk: 8-12+ auditors.

Orthogonality and independence matter more than reaching a count. Choose relevant lenses from correctness, security, data integrity, architecture/API, error handling, tests, complexity, dead code, dependencies, performance, operations, documentation, and consistency. Launch independent auditors concurrently; never permit nested agents.

Tiers: auditors run on your default model; the verification of candidate findings runs on your strongest model. Pin the model on every agent; an unpinned agent inherits whatever the session runs on.

Each finding must include severity, confidence, file and line, violated invariant, triggering conditions, concrete consequence, blast radius, evidence, and smallest credible remedy. Verify every candidate against code, callers, tests, and history. Deduplicate by root cause and discard invalid or purely subjective findings.

## Full report and ordering

Publish every verified finding from the audited waves, including findings not selected for automatic repair. Sort deterministically by:

1. severity descending;
2. blast radius descending;
3. confidence descending;
4. repair effort ascending.

Correctness and security defects are must-fix when the repair is within current authorization and does not require a product decision. For maintainability, consistency, performance polish, docs, low severity, and nits, use an ROI gate: repair only when expected impact multiplied by confidence clearly exceeds effort and regression/churn risk. Do not blindly fix every nit.

Any finding whose remedy intentionally changes externally observable behavior, product policy, public contracts, data meaning, or architecture is a handoff to a goal loop such as `sergio-loop`, or to `investigate`; report the evidence and proposed acceptance criteria, but do not implement it under this skill.

## Bounded repair waves

1. Select the highest-priority independent fixes that pass the authorization and ROI gates.
2. Assign non-overlapping ownership and launch independent work concurrently; integrate serially.
3. Run focused tests and relevant lint, type-check, build, and security checks.
4. Use a separate reviewer lane to validate fixes and identify regressions. Authors do not approve their own work.
5. Re-rank the remaining verified backlog before the next wave.

Stop after at most 25 audit/repair rounds. Stop with `NO_PROGRESS` after 3 consecutive rounds with no verified risk reduction, the same unresolved failure, or only below-gate polish remaining. Do not weaken tests, bypass hooks, or create speculative scaffolding to continue.

## Output

```text
## Codebase Health Report: [repository]
### Coverage
- [waves, subsystems, exclusions, evidence]
### Findings
- [severity] [file:line] [consequence] [blast radius] [confidence] [effort] [disposition]
### Prioritized actions
1. [ordered action and rationale]
### Applied repair waves
- [round] [files, findings fixed, verification]
### Behavior-changing handoffs
- [goal-loop or investigate brief with acceptance criteria]
### Remaining backlog
- [must-fix blocked items, below-ROI items, unresolved evidence]
### Terminal state
[COMPLETE | NO_PROGRESS | ROUND_LIMIT | BLOCKED]
```
