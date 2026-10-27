---
name: deliver-change
description: Coordinate a development task from a stronger brief through implementation and verification, with optional adversarial Codex review. Use when asked to deliver a change using deepen-task and verify-change or to run this combined workflow. Codex review is off unless explicitly requested. For verification alone, use verify-change; for a standalone review, use codex-review.
---

# Deliver Change

Carry out the requested development task and hand off the result with
evidence. Coordinate the existing skills without replacing their methods
or treating a successful check as an independent review.

## Invocation and dependencies

- `deliver-change <task>`: deepen the approach, implement, and verify.
- `deliver-change --review <task>`: also run adversarial codex-review.
- `deliver-change --no-review <task>`: explicitly omit that optional stage.

These are skill invocation conventions, not a new executable CLI. A clear
natural-language request for Codex review also opts in. A routine request
to inspect the work does not silently enable a separate model run. Honor
an explicit opt-out; clarify contradictory review instructions if needed.
Keep required project reviews visible even when this optional stage is off.

Locate and read `deepen-task` and `verify-change` through skill discovery,
or their sibling directories beside this skill in an Inkstone installation.
Locate and read `codex-review` only when opted in. Resolve resources from
each skill's actual installed directory, not the target repository's cwd.
If a dependency is unavailable, name the missing stage and continue useful
independent work; do not silently replace it or claim it ran. If review was
requested but cannot run, keep it explicitly incomplete in the handoff.

## Establish the task and authority

Work in the user's target repository. Read its guidance and inspect its
initial state. Read its review, ownership and approval policy where
available; if it cannot be read, record the policy as unknown rather than
assuming that none applies. Record the starting commit and existing local changes, then
identify the task's paths, acceptance criteria, and relevant constraints.
Preserve unrelated edits throughout implementation and review.

The task supplies the authority: implement when implementation is requested,
or stop at a plan when the user asked for a plan. Calling the wrapper alone
does not add authority to publish, merge, deploy, file issues, change global
settings, or alter approval rules. Complete explicitly authorized delivery
steps without asking for the same permission again.

For a plan-only request, deliver the plan and state that implementation,
runtime verification, and code review were not run. A review flag does not
turn a plan into code or authorize reviewing unrelated existing changes.

## Frame and implement

Apply `deepen-task` to the consequential uncertainties: missing expert work,
primary evidence, useful methods, and what would demonstrate success. Keep
this brief for straightforward fixes. Preserve the requested outcome and
artifact; do not end with a rewritten prompt when the user asked for work.

Implement within the agreed scope using the project's conventions. Apply
`verify-change` during the work, selecting meaningful checks against the
acceptance criteria rather than waiting for the end to invent tests.
Follow its three-attempt checkpoint on each repeatedly failing behavior:
diagnose or change strategy, then continue authorized repairs. The checkpoint
does not end the task or start an adversarial review loop.

Before handoff, refresh evidence affected by edits. Keep passed, failed,
blocked, and not-run checks distinct, and retain the tested code identity.
If optional review is off, proceed directly to the final handoff.

## Optional adversarial review

Use `codex-review` as a separate stage. Pass a concrete task scope through
its resolver and echo the resolved scope before review. Check that it covers
the intended changes rather than relying on bare auto-detection, which can
select only a dirty diff or the last commit. Account for task-owned new
files: untracked files are absent from an ordinary git diff. Stage or commit
them only under existing authority; otherwise report the coverage gap and
resolve the scope before claiming a complete review. Do not silently include
unrelated pre-existing edits to make a scope convenient.

Preserve the reviewer's isolation: provide the resolved diff commands and
the selected review guidance, not the implementation conversation, author
rationale, verification narrative, or expected findings. Keep the evidence
handoff for the user separate. Report the actual reviewer backend and
model. Compare the actual reviewer and author models/vendors before calling the
review cross-model or cross-vendor; the CLI name does not establish independence.
A same-model fresh-context fallback is not a cross-model review.

Triage every finding using codex-review's dispositions. Fix accepted,
in-scope defects when that falls within the user's existing implementation
authority; do not introduce another approval question for an already
authorized repair. Preserve any narrower instructions, such as review-only.
Keep pre-existing defects outside this change and do not create issues or
publish artifacts merely because a dependency lists those possible actions.

After repairs, rerun affected verification and record which code state the
review covered. Use a focused re-review of changed code when the user or
project requires it, or when a consequential repair warrants it. A review
of the earlier state does not automatically cover new edits. Do not run
repeated full-scope reviews by default or confuse the implementation
three-attempt checkpoint with a review-round policy.

## Final handoff

Report the implemented outcome, tested code state, meaningful evidence,
remaining gaps, and recovery notes for consequential changes. Name any
change to CI workflows or owner-designated sensitive paths as needing a
human decision. Add optional
review status: not requested, incomplete, or completed, with reviewer
backend, reviewed state, finding dispositions, and any later edits it
does not cover. Keep the report proportionate to the change.

If the user requested a PR, merge, or deployment, complete that authorized
step after the applicable checks and project requirements are satisfied.
Otherwise finish with the requested artifact and handoff. Never equate the
wrapper's completion with a blanket safety claim or merge approval.
