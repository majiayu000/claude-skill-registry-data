---
name: change-review
description: Use when reviewing a branch, pull request, or work-in-progress diff since a fixed point for conformance to the repository's standards and fidelity to the originating spec or issue, reported as two separate axes.
license: MIT
---

# Change Review

## Purpose

Review the diff between `HEAD` and a fixed point on two separate axes and report them side by side:

- **Standards**: does the change follow this repository's documented standards and the owning skill's change contract?
- **Spec**: does the change do what the originating issue, spec, or ticket asked, no less and no more?

A change can pass one axis and fail the other. Code that follows every convention but builds the wrong thing passes Standards and fails Spec; code that does exactly what was asked but breaks the repository's contracts passes Spec and fails Standards. Keeping the axes apart stops one from hiding the other.

## Activate when

- reviewing a branch, pull request, or local work before handing it off
- a request says "review since `main`", "review this PR", or "review my changes"
- an implementation loop finishes and the diff is ready to commit or merge
- an agent reviews another agent's change

## Boundary ownership

| Concern | Primary skill |
|---|---|
| Standards and spec review of a whole diff | change-review |
| Whether the diff could be smaller or simpler | stack-minimality-review |
| RuboCop findings and cop configuration | rubocop |
| Rails structure and framework best-practice review | rails-architecture |
| Security threat modelling of the change | rails-security-engineering |
| Correctness of one behavior under a failing test | ruby-debugging |

Compose the narrow reviewers as secondary skills when the diff touches their area; this skill reports their findings under the Standards axis without re-ranking them.

## Repository inspection

1. **Pin the fixed point.** Use the commit, branch, tag, or ref the user gave; ask when none was given. Confirm it resolves with `git rev-parse <fixed-point>` and that `git diff <fixed-point>...HEAD` is not empty before reviewing.
2. **Collect the change.** Record the three-dot diff (against the merge-base) and `git log <fixed-point>..HEAD --oneline`.
3. **Find the spec**, in this order: issue or PR references in commit messages (`#123`, `Closes #45`); a path the user passed; a spec under `docs/`, `specs/`, or the repository's planning location matching the branch or feature; otherwise ask. If there is none, the Spec axis reports "no spec available".
4. **Find the standards**: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, coding-standards documents, `.rubocop.yml` and other linter configuration, and the `## <Domain> changes` section of each skill that owns a touched boundary (route with `skill-manifest.yml` and `router/ROUTING.md`).
5. **Check what tooling already enforces**: RuboCop, type checks, and CI checks. Do not re-report what a configured tool catches; report instead whether the tool was run and passed.

## Decision rules

1. Review the two axes as separate passes with separate notes. When the agent can run sub-agents, give each axis its own sub-agent with the diff command and its sources; otherwise finish the Standards pass, then start the Spec pass without editing the Standards notes.
2. **Standards axis**: report each place the diff breaks a documented standard, citing the file and rule, and each code smell from the baseline, quoting the hunk. A documented standard is a hard finding; a smell is always a judgement call, labelled as such ("possible Feature Envy").
3. The repository overrides the baseline: when a documented standard endorses something the baseline would flag, drop the smell.
4. **Spec axis**: report requirements that are missing or partial, behavior the spec did not ask for (scope creep), and requirements that look implemented but wrong. Quote the spec line for each.
5. Keep each axis report under about 400 words, ordered by severity within the axis.
6. Report; do not fix. The author or a follow-up implementation step applies changes.

## Always-critical findings

These patterns are hard Standards findings with critical severity in every repository. Rule 3 never downgrades them: a repository convention cannot make them safe. Each finding quotes the hunk and cites the real `file:line` from the diff, never a representative location.

- `params.permit!`, or mass assignment from unfiltered `params` (`rails-action-controller`).
- `html_safe`, `raw`, or `<%==` applied to content a user can influence (`rails-security-engineering`). Confirm the data flow; a string literal or already-sanitized output is not a finding.
- SQL built by string interpolation or concatenation of external input, in `where`, `order`, `find_by_sql`, `select`, `joins`, or `connection.execute` (`rails-security-engineering`).
- Disabling forgery protection (`skip_forgery_protection`, `protect_from_forgery with: :null_session` on session-authenticated controllers) to make a request work (`rails-security-engineering`).
- `constantize`, `safe_constantize`, `send`, or `public_send` with a value taken from request input (`rails-security-engineering`).

Business logic in a controller is a design smell. It is reported as a smell, not as an always-critical finding.

## Critical invariants

- Never merge or re-rank findings across axes; name the worst finding within each axis, never one overall winner.
- Never report a smell as a violation; only a documented standard or a skill change contract produces a hard finding.
- Never claim a test, linter, or CI run passed unless its output was observed in this review.
- Authentication and authorization findings stay separate even when one hunk touches both.

## References

Load only when needed; the reference is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| running the Standards axis on a diff with Ruby or Rails code | [references/smell-baseline.md](references/smell-baseline.md) | Baseline code smells with Ruby signs and fixes; how the repository overrides them | `rubocop-review`, `rails-best-practice-review` |

## Reference example

Pin the range, then report the two axes separately:

```bash
git rev-parse --verify main
git diff --stat main...HEAD
git log main..HEAD --oneline
```

```text
## Standards
- app/models/invoice.rb:42 — breaks rails-active-record change contract: update_all
  skips callbacks and the audit event without an explicit bypass note. (hard)
- app/services/refund_builder.rb:10-31 — possible Feature Envy: reads six
  Invoice attributes to compute a value Invoice could own. (judgement)
- RuboCop: `bundle exec rubocop` run, no offenses.

## Spec
- Missing: "partial refunds must keep the original tax split" (issue #214, line 9);
  RefundBuilder refunds tax proportionally only for full refunds.
- Scope creep: adds a CSV export of refunds; not requested in #214.

Standards: 2 findings, worst is the update_all contract breach.
Spec: 2 findings, worst is the missing partial-refund tax split.
```

## Agent review checklist

- [ ] fixed point resolves and the diff is not empty
- [ ] spec located, or "no spec available" stated
- [ ] standards sources listed, including the owning skills' change contracts
- [ ] tool-enforced rules left to the tools, and tool runs reported only when observed
- [ ] every hard Standards finding cites a file and rule
- [ ] every smell labelled as a judgement call
- [ ] every Spec finding quotes the spec line
- [ ] axes reported separately, each with its own worst finding

## Failure modes

- blending the two axes into one ranked list, so a clean Standards pass hides a Spec failure
- reporting smells as hard violations, or reporting a smell the repository's standards endorse
- reviewing without a pinned range, or against a two-dot diff that includes unrelated base-branch changes
- skipping the Spec axis silently when no spec was found
- repeating RuboCop output instead of reporting whether RuboCop ran
- rewriting the code during review instead of reporting

## Verification

The review is complete when both axis reports exist (or the Spec axis states that no spec exists), every finding points to a file and line or a spec line, and any tool or test result cited was run during the review with its output available.

## Source foundation

The two-axis review, the fixed-point range, spec discovery order, and the code-smell baseline as labelled judgement calls are adapted, in this repository's words and with Ruby examples, from the `code-review` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). The smell catalogue follows Martin Fowler, *Refactoring* (2nd edition), chapter 3. The Standards axis adds this repository's skill change contracts and RuboCop baseline.
