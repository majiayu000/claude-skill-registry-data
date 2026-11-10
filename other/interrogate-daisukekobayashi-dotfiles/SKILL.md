---
name: interrogate
description: Use only when the user explicitly invokes interrogate for independent reviews of a change or design. Synthesize evidence and disagreements without editing the target.
license: MIT
disable-model-invocation: true
---

# Interrogate

Run only when the user explicitly invokes `interrogate`, such as `$interrogate`
in Codex or `/interrogate` in Claude Code. A generic review request or a
reference from another skill does not activate this workflow.

Return an evidence-based review verdict. Reviewers and the parent must not edit
files, run mutating checks, publish reviews, resolve threads, or fix findings.

## Freeze the review target

Resolve the requested files, design, branch, worktree, commit, or PR. Inspect
repository instructions and current state. Identify the base and relevant
committed, staged, unstaged, and untracked changes without switching branches
or updating refs. Do not infer that an empty committed diff means no local work.

State the intended behavior from the request/specification and identify the
revision or working-tree state being reviewed. If writers are active, wait for
a stable handoff or report that the review cannot cover a stable target.
Do not claim old findings cover a later revision.

## Prepare one review brief

Read the review criteria in available `change-review` and `change-adversarial-review`
skills as references. Reuse their supported defect and failure-path criteria
without invoking those explicit-only workflows or duplicating their operation
steps. If unavailable, use this minimal lens: correctness and regressions,
trust/data boundaries, lifecycle and partial failure, compatibility, and
whether evidence exercises the changed behavior.

Give every reviewer the same intent, scope, baseline, context pointers, criteria,
and read-only restriction. Request concrete findings with a trigger, failure
path, impact, source location, and uncertainty. Ask for coverage gaps as well.
Do not show the parent's suspected findings or another reviewer's answer.

## Obtain independent reviews

Use two reviewers by default when delegation is available and permitted.
Choose distinct available models when useful and permitted; never assume a
model family or send code to a new external service. Otherwise use independent
same-model runs and disclose the reduced diversity. Do not ask reviewers to
spawn more reviewers.

If subagents are unavailable or forbidden, perform a single review and label
that limitation. Sequential reasoning by the same agent is not independent
multi-model evidence. Report missing or failed reviewers instead of silently
counting them as a clean verdict.

## Judge the findings

Read each report and trace consequential findings back to the target.
Deduplicate by failure mechanism. Agreement increases attention, not truth:
one well-supported finding can outweigh a consensus with no evidence.
Investigate disagreements and distinguish unsupported speculation from
unresolved uncertainty.

Classify material findings as Act on / Consider / Dismissed, with the evidence
and reason. A proposed fix stays a recommendation. If a claim needs execution
that could mutate state, mark that verification pending. The user can explicitly
invoke [blast-radius](../blast-radius/SKILL.md) for scoped experiments.

Return the target, verdict, material findings, reviewer/model coverage,
disagreements that matter, and residual risk. A clean review means no supported
material finding in the covered scope, not proof that the change is safe.
After an upstream writer changes the target, reassess review applicability.

## Source

Adapted from Lauren Tan's [pstack interrogate](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/interrogate/SKILL.md).
Local changes: reuse existing review criteria, evidence over voting, strict
read-only behavior, bounded reviewers, and honest fallback coverage. See [LICENSE](LICENSE).
