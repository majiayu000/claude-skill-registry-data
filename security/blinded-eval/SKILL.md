---
name: blinded-eval
description: >-
  Blinded evaluation of a Skill, rule, or prompt change. The parent designs
  the experiment, isolates candidates in throwaway directories, runs the same
  organic user prompt, and scores artifacts against a held-back rubric.
  Apply when the user invokes /blinded-eval, asks to eval or A/B a skill
  change, or authoring Phase 4 says the change would alter agent behavior.
  Use authoring-skills-and-rules to write the skill; use dissect to audit an
  existing system.
user-invocable: true
disable-model-invocation: true
invocation-type: manual
version: "1.1.0"
author: "Ali Farahat"
tags: ["eval", "skills", "blinding", "subagents", "meta"]
when_to_use: |
  USE WHEN:
  - The user invokes /blinded-eval or asks to eval, A/B, or promote a skill change.
  - authoring-skills-and-rules Phase 4: the draft would change agent behavior.
  DO NOT USE WHEN:
  - The change is a typo, comment, or formatting-only edit.
  - The task is to write the skill (use authoring-skills-and-rules).
  - The user wants a code review of product code (use dissect).
---

# Blinded eval

> **Leading words:** organic prompt, blinding, isolate, artifacts not
> self-report, inconclusive is not a pass.

The parent owns the experiment. Candidates never learn they are in an
evaluation. The judge sees sanitized labels and the rubric, never variant
names. Grade from files written and files opened, never from a candidate's
claims.

Skip this skill for typos. A behavior-changing skill or rule draft is the
trigger.

## Non-negotiables

Copy the first items of the matched steps below into the todo list verbatim.
A step you skip stays with `skip: <reason>`.

1. Frame the variant and write the rubric (3–6 criteria). Hold the rubric
   back from candidates.
2. Isolate each candidate in its own working directory. Plant only organic
   context. Sanitize names — project-shaped, not experiment-shaped.
3. Author one organic user prompt. Same prompt to every candidate.
4. Spawn N candidates as isolated subagents. Inherit the host model unless
   the host exposes distinct model families; then split families across
   candidates. Do not require Cursor arena, cloud workers, or a specific
   slug menu.
5. Spawn one blinded judge. Prefer a different model family when the host
   exposes one. The judge sees outputs labeled A/B/C plus the rubric.
6. Read every candidate artifact yourself. Compare to the judge. Grade
   chain-following from what they wrote and opened, not self-report.
7. Verdict: promote, iterate, or abandon. Inconclusive is not a pass.

Blinding word list and sanitization: [references/blinding.md](references/blinding.md).
Judge prompt template: [references/judge-prompt.md](references/judge-prompt.md).

## Phase A — Frame

State, to the user only:

- Variant under test (what changed, vs what baseline).
- Success predicate (falsifiable).
- Rubric: 3–6 concrete criteria the judge will score. Example scale:
  pass / partial / fail per criterion.

Do not put the rubric, the words `eval`, `rubric`, `candidate`, `baseline`,
or `variant` in any directory, filename, or prompt a candidate will see.

## Phase B — Isolate

One directory per candidate (git worktree or temp dir). Never commit these
trees into the kit repo.

Plant what an organic task would have: a small project skeleton, the skill
folder under test (baseline copy or draft copy), maybe a README. No
sibling skills the candidate would not naturally open.

Sanitize:

- Directory names: `invoice-cli`, `changelog-bot` — not `skill-eval-a`.
- Skill folder inside the plant uses the skill's real name (`authoring-skills-and-rules`), not `variant-b`.

## Phase C — Organic prompt

Write what a user would type. State the goal. Do not ask which skills,
principles, or files they applied. Do not mention other candidates.

Example shape: "This repo needs a skill so agents stop inventing changelog
sections. Write the skill."

## Phase D — Candidates

Spawn N parallel `Task` / equivalent subagents. Minimum useful N is 2 per
variant (baseline vs draft) or 2+2. Give each:

- Absolute working directory.
- The organic prompt only.
- Instruction to write files in that directory and stop. No git commit.

Route bulk to subagents. Keep summaries in this thread, not raw payloads.

If the host cannot spawn isolated subagents, run candidates sequentially in
separate directories and still blind the judge. Say so in the verdict.

## Phase E — Blinded judge

Fill [references/judge-prompt.md](references/judge-prompt.md). Attach each
candidate's written files under labels A, B, C. Never include which model
or which variant produced them. Shuffle label assignment; record the mapping
only in the parent notes.

The judge returns per-label scores against the rubric and a ranking.

## Phase F — Parent synthesis

Read every candidate output end to end. If you disagree with the judge, the
rubric is ambiguous or a model is biased — fix the rubric and re-run, do
not promote on a coin flip.

**Reply contract:**

- Variant under test
- Rubric
- Per-candidate notes (files written, what they actually did)
- Judge verdict
- Your synthesis
- Recommendation: promote / iterate / abandon

Do not promote on self-report. A candidate that claims it followed the skill
but wrote a 600-line SKILL.md with no `references/` fails criterion 3.

## Dogfood rule

This skill is proven by using it on a real draft. Do not eval
`blinded-eval` with itself in a loop.
