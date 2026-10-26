---
name: rite-seal
description: Decide GO/NO-GO for an active feature; $rite-ship owns commit, push, tag, and close.
argument-hint: "[feature-slug] [--full]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/candidate-integrity.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md","devrites-lib/reference/standards/verification-methods.md","rite-seal/reference/phase-contract.md","rite-seal/reference/final-evidence.md","rite-seal/reference/go-no-go.md","rite-seal/reference/risk-and-rollback.md","rite-seal/reference/seal-template.md","rite-seal/reference/output.md","rite-seal/reference/anti-patterns.md"],"triggers":{"agents":["devrites-lib/reference/standards/agents.md"],"browser":["devrites-lib/reference/standards/browser-proof-checklist.md"],"code-review":["devrites-lib/reference/standards/code-review.md"],"deprecation":["devrites-lib/reference/standards/deprecation.md"],"documentation":["devrites-lib/reference/standards/documentation.md"],"dod":["devrites-lib/reference/standards/definition-of-done.md"],"observability":["devrites-lib/reference/standards/observability.md"],"principles":["devrites-lib/reference/standards/principles.md"],"security":["devrites-lib/reference/standards/security.md"],"testing":["devrites-lib/reference/standards/testing.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md","touched-files.md","review.md","seal.md"],"workspaceByRole":{"code-reviewer":["spec.md","plan.md","tasks.md","test-plan.md","architecture.md","decisions.md","state.md","evidence.md","touched-files.md","review.md"],"devex-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md","devex.md","review.md"],"doubt-reviewer":["spec.md","plan.md","tasks.md","state.md","decisions.md","review.md"],"frontend-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md","review.md"],"performance-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md","review.md"],"proof-runner":["spec.md","test-plan.md","tasks.md","gates.md","evidence.md","state.md"],"security-auditor":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md","review.md"],"simplifier-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","review.md"],"spec-reviewer":["brief.md","spec.md","decision-coverage.md","questions.md","decisions.md","assumptions.md","state.md","review.md"],"test-analyst":["spec.md","tasks.md","test-plan.md","state.md","evidence.md","review.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .agents/skills <slug> --phase seal` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# $rite-seal: GO / NO-GO

Verify final candidate in `seal.md`; `$rite-ship` owns authorized irreversible
actions and close-out.

## Authority

Read [`core.md`](../devrites-lib/reference/standards/core.md) plus only
final-diff-relevant standards: agents, code-review, testing, browser-proof-checklist,
security, principles, documentation, observability, deprecation,
definition-of-done, and [`verification-methods.md`](../devrites-lib/reference/standards/verification-methods.md)
for coverage-denominator and evidence-status judgment.
Load [`final-evidence.md`](reference/final-evidence.md) and
[`go-no-go.md`](reference/go-no-go.md) for proof and verdict safety.
Follow the shared
[`candidate-integrity.md`](../devrites-lib/reference/candidate-integrity.md) for
the reviewed digest and artifact bindings.

The host runs/reconciles named read-only reviewers; engine checks invariants.
**Standard** is default; **Full** broadens conditional axes per
[`devrites-lib/reference/orchestration-profiles.md`](../devrites-lib/reference/orchestration-profiles.md).

## Gate

| State | Verdict |
|---|---|
| Acceptance proven, deterministic checks pass, no unresolved drift or human gate, `Critical == 0`, `Important == 0` | **GO** |
| Same, but `Important > 0` | Ask `Important findings remain. Proceed to seal? [y/N]`; default **N**. Only a human answers `y`; unattended (AFK/autocomplete) keeps **N** and stops for a human if Important remains |
| `Critical > 0` | **NO-GO** |
| Any acceptance criterion, resolved prohibition, or declared key link lacks proof | **NO-GO** |
| `gates status` is not `all-met` — an unmet, stale, unapproved, or abandoned ledger gate remains | **NO-GO** |
| Evidence is stale, or native diff review plus the exact test analyst finds weakened tests | **NO-GO: Critical** |
| Any exact required reviewer account is missing or silent | **NO-GO** |
| Any deferred finding (`touched-files.md` `## Review trail`, `eng-review.md` `## Deferred findings`) lacks a `review.md` verdict | **NO-GO** |
| Any `gate: validating` question remains open | **NO-GO** |
| Material UI acceptance lacks or fails required browser proof | **NO-GO** |
| Unresolved drift, unsafe migration/removal, or unapproved principle violation remains | **NO-GO** |
| `check regression` reports an unblessed loss vs the recorded progress baseline | **NO-GO** |
| `check windows` reports a deferral marker the change introduced without a `windows.md` waiver | **NO-GO** |

A judgment-only criterion needs the human eye; AFK records a validating question
(`slice: seal`) and stops. Autocomplete never auto-picks it; only a human answers.

## Workflow

Follow [`reference/phase-contract.md`](reference/phase-contract.md)
([`risk-and-rollback.md`](reference/risk-and-rollback.md),
[`seal-template.md`](reference/seal-template.md),
[`anti-patterns.md`](reference/anti-patterns.md)):

1. read workspace and final diff;
2. recheck the canonical candidate/bindings and approved repository/CI proof;
3. admit every valid same-candidate Review account; dispatch remaining required exact roles under
   `../devrites-lib/reference/parallel-dispatch.md` in one wave, proof-runner included, on the same frozen candidate,
   code review through its § Engineering lanes;
4. reconcile their read-only verdicts against source and immutable evidence;
5. draft GO/NO-GO `seal.md` with acceptance, tests, decisions, and seven roster accounts plus proof-runner and doubt-reviewer
   (each engineering lane its own account);
6. write exactly one candidate binding, then run
   `devrites-engine check seal <slug>` for structure and identity, never semantics,
   and, when that check reports a stale readiness-input binding, run
   `devrites-engine check drift <slug>` before returning to Vet so the repair
   starts at the named changed, missing, or added input,
   and `devrites-engine check regression <slug>` to confirm no recorded progress
   fact was lost since the last checkpoint — `BLOCKED` is NO-GO; `unproven`
   (no baseline) does not block — plus two separate runs of `devrites-engine check windows <slug>`,
   one with `--base <release-base>` and one with `--worktree` (the only mode that scans
   untracked files; never pass both flags in one command, the last one wins) so each deferral marker the feature diff introduced
   carries a `windows.md` waiver row ([`windows.md`](../devrites-lib/reference/standards/windows.md));
   unwaived hits are NO-GO. The engine already refuses a `gates.md` ledger
   that is malformed, unmet,
   stale, unapproved, or abandoned — a seal-side `gates status` reading anything
   but `all-met` means Prove's evidence is not current; return there, never
   attest past it. Before the Seal wave, run `devrites-engine gates reverify <slug>
   --transcripts` on the frozen candidate, so every gate has a transcript bound to
   this digest for the proof runner. It likewise refuses a malformed `notes.md` or any anchor
   graded other than `exact`: `devrites-engine note check <slug> --repair`
   re-anchors `moved` notes; `stale`/`ambiguous`/`lost` ones are corrected or
   removed before GO. Repeat each `note: unexecuted driver` line `check seal` prints in the GO/NO-GO reply.

Corrections return through affected Prove/Review before restarting Seal under
[evidence validity](../devrites-lib/reference/candidate-integrity.md#evidence-validity).

Only repository scripts/CI authorize commands; never guess.

## On GO

Set `state.md` `Next step: $rite-ship` and stop. A GO is a verdict, not
authorization to perform an irreversible action.

## Output

Use [`reference/output.md`](reference/output.md).
