---
name: arena
description: Use only when the user explicitly invokes arena to compare independent solutions to the same design or implementation problem, then synthesize and verify a result.
license: MIT
disable-model-invocation: true
---

# Arena

Run only when the user explicitly invokes `arena`, such as `$arena` in Codex
or `/arena` in Claude Code. A generic comparison request or a reference from
another skill does not activate this workflow.

Compare alternatives to one problem. Different slices of a task are ordinary
delegation, not an arena.

## Frame before delegating

Define the requested artifact, fixed input/revision, scope, real constraints,
and observable acceptance criteria before seeing candidates. Include the current
approach as a baseline when it is a viable option. Agree a bounded time or work
budget appropriate to the task.

Use two candidates by default; increase only for distinct useful approaches.
Use different available models when supported and permitted, without hardcoded
model IDs or new services. Same-model independent runs are valid, but report
the reduced diversity.

## Isolate candidates

Give each worker the same problem and constraints, its permitted output
location, and a request for an artifact plus rationale. Keep candidates from
reading each other's output until their attempts finish. Carry user/repository
instructions and approval limits into every brief. Do not delegate further
fan-out by default.

Design candidates can return sketches without file edits. File-writing
candidates need separate temporary directories or isolated worktrees from the
same baseline; do not copy secrets or unrelated dirty work. If isolating a real
checkout requires additional approval, obtain it before that operation. Never
reset, stash, switch, or clean the user's checkout to make room for a candidate.

Isolate runtime state as well as files: ports, data directories, caches that
cannot be shared safely, and external write targets. Use available runtime
isolation guidance. If isolation cannot be established, use read-only sketches.

When delegation is unavailable or forbidden, compare sequential alternatives and
label them as one-agent exploration. Do not claim independent review.

## Judge and synthesize

Wait until writers have finished before reading or testing their outputs.
Read every completed candidate and compare each acceptance criterion. When
available and useful, use an independent read-only judge after candidate output
is stable, with the same rubric and anonymous candidate labels.

Verify consequential claims instead of selecting by confidence or vote. Report
failed candidates and missing checks; with fewer than two usable alternatives,
the comparison is incomplete.

Choose a base and incorporate only improvements that preserve one coherent
design. Apply changes to the target checkout only when implementation is
authorized, after inspecting its current diff and preserving unrelated work.
Do not merge branches or rewrite history as an implicit synthesis step.

Use [prove-it-works](../prove-it-works/SKILL.md) on the synthesized result.
Evidence from an individual candidate does not validate the combined result.

## Deliver

Return the selected artifact or design, comparison criteria, reasons for the
choice, useful ideas adopted or rejected, candidate failures, and verification
limits. Keep task-specific comparison state temporary; promote only requested
durable decisions. Stop owned processes; retain evidence and honor approval
requirements before removing worktrees or branches.

## Source

Adapted from Lauren Tan's [pstack arena](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/arena/SKILL.md).
Local changes: bounded fan-out, runtime capability detection, preserved approval
boundaries, and explicit isolation/fallback behavior. See [LICENSE](LICENSE).
