---
name: assistant-spike
description: "Answers one observable feasibility question by running a small disposable experiment outside tracked files, then reports a validated, partial, or invalidated verdict and builds no production change. Use when the user asks to spike, try out, or prove whether an approach can work and only execution can settle it, not reading sources, scoring trade-offs, building the real change, or diagnosing a failure."
---

# Feasibility Spike

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](../../tools/progress/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Answer one feasibility question ("can approach X do Y here?") with the least
evidence that settles it. A spike produces a finding, never production code.

## 1. Frame the question

Before building anything, state:

- **Question**: one observable feasibility question.
- **Constraints**: the conditions the answer must hold under (data size, load,
  platform, version, time limit).
- **Decisive observation**: what you would see if the answer is yes, such as
  "p95 under 100 ms over 200 queries at 50k rows".
- **Failure condition**: what you would see that invalidates the idea.

One question is the default. Split into more questions only when no single
decisive observation can answer the user's idea; there is no fixed question
count, question table or alignment pause. Ask the user only about a
constraint you cannot discover and that would change the verdict.

## 2. Inspect first

Check whether source, documentation already in the repository, installed
package source, or existing test output settles the question. If it does,
answer from that evidence with file:line or the output, say that no experiment
was needed, and stop: build no probe and ask for no probe approval. Execute
only when running something adds evidence that reading cannot, for example
timing, resource limits, real parser or runtime behaviour, or an interaction
the source does not determine.

## 3. Plan the smallest probe

Test the **riskiest assumption** first: the one whose failure would invalidate
the idea and that has the least evidence so far. Do not prototype the easy
parts before it. Keep the probe as small as the question allows; hardcode
inputs unless the question is about them.

Choose at least one **control** or limit that makes the decisive case
interpretable, and report which you ran:

- Latency, throughput or memory: the stated load, plus a small baseline or a
  cold versus warm run, so a single fast run is not mistaken for the answer.
- Compatibility or behaviour: a known-good baseline (input, version or
  configuration) through the same harness, so a failure is attributable.
- Capacity or size: the boundary input at and just over the stated limit.
- Rejection or validation: one input that must fail, so a pass is not vacuous.

### Probe location

The probe directory is always a fresh subdirectory, named for this spike, that
does not exist when the plan is written:

- Default: `<session scratch or temp directory>/spike-<id>/`.
- When the probe needs project dependencies or relative paths: a new
  subdirectory under a Git-ignored directory inside the project, with the new
  path confirmed by `git check-ignore <path>` before the plan is presented.

A pre-existing directory is never the probe directory, even if it is empty or
ignored: not the scratch root itself, not `.codex/`, and not any directory that
holds local task state. Do not create a tracked `spikes/` directory, and never
commit probe code.

### Probe plan and its single approval

"Disposable" or "throwaway" never waives an existing boundary. Writing files
and running state-changing scripts need confirmation even in a scratch or
ignored directory, so ask **once**, before writing anything, with a probe plan
that names:

1. the exact probe directory;
2. the files it will create there;
3. the exact commands it will run, ending with the cleanup command that deletes
   only the probe directory (for example `rm -rf <scratch>/spike-<id>`), unless
   the plan states the probe will be kept.

After one approval:

- **Covered**: any file written inside the approved probe directory, including
  files added while iterating; the listed commands; the listed cleanup command.
- **Not covered**: any write outside that directory; any unlisted command.
  Ask again first. A change to the directory or the commands needs a new
  approval.
- **Always separate**: package installs, network or external API calls,
  credentials, real user data and every other item on assistant-workflow's AI
  usage policy confirmation list keep their own confirmation. Production
  systems stay off limits.

This approval is the skill's own chat confirmation only. Host permission
prompts and execution-policy prompts, such as the Codex `rm -rf` prompt rule,
still apply to approved commands; answer them as normal, never treat them as
redundant, and never choose or rewrite a command, including the cleanup
command, to avoid one. Do not substitute `find ... -delete`, a script or another
deletion form for the approved cleanup command.

When the spike runs inside a Workflow task whose boundary excludes execution
(`prepare_only` or progressive discovery), run it only with the user's explicit
authorization for that execution; otherwise report the question and the probe
plan you would run, and run nothing.

## 4. Run

Immediately before the first write, check that the probe directory still does
not exist. If it exists, write nothing and ask again with a new name. Then run
the decisive case and the control. Do not declare success after one
happy-path run; follow surprising results within the approved plan. Finally run
the listed cleanup command, or leave the probe in place if the plan said it is
kept. Every file that existed before the spike must be unchanged afterwards.

Never edit the project's tracked production source, tests or configuration. If
the question can only be answered by changing tracked files, stop and hand off
to Workflow (section 6) instead.

## 5. Verdict

Return exactly one verdict:

- **validated**: the decisive observation occurred under the stated
  constraints and the control behaved as expected.
- **partial**: the decisive observation holds only under named conditions that
  are narrower than the stated constraints, or the control exposed a condition
  the real build must handle (for example a cold first run over the limit).
- **invalidated**: the failure condition occurred, or the decisive observation
  did not, with the reason.

"It works" is not a verdict. Each verdict carries the evidence (commands run
and what was observed, for the decisive case and the control), its limits, the
consequence for a real build, the probe location, and whether the probe was
deleted or kept. A validated spike shows feasibility under the tested
conditions only; never claim production readiness.

## 6. Handoff to Workflow

When the user wants to proceed to a real build, hand off to
`assistant-workflow` in plain prose with: the question, the verdict, the
evidence and its conditions, the limits, the consequence for the real build,
and the probe location and disposal state. State that the finding
**authorizes no production change**. Workflow takes the finding as discovered
context through its existing `constraints` input, or through
`candidate_search_constraints` when Candidate Search runs; its own scope,
verification selection and plan approval apply unchanged. Never copy probe code
into tracked source, and never treat the verdict as plan approval.

### Boundary with Candidate Search, Research and Thinking

Use this skill only when a decisive observation must be produced by execution.
A request to compare or choose between options that reading or scoring
trade-offs can settle stays with assistant-research, assistant-thinking or
Workflow's Candidate Search; this skill never activates or replaces Candidate
Search. When Workflow asks for a spike on a candidate's unverified assumption,
the verdict is evidence for that candidate's Feasibility score and enters
`candidate_search_constraints`. A spike verdict never selects a candidate,
changes an approved plan, or bypasses Workflow's plan-deviation procedure.
