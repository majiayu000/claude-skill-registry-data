---
name: byte-auto
description: "Use the Byte workflow for end-to-end completion of a multi-stage project request."
---

# Byte Auto

Own the requested outcome end to end. Adapt the method to the task instead of
running every Byte skill or producing every Byte OS artifact.

## Outcome Contract

At the start, identify:

- the deliverable or observable result;
- important constraints and evidence already available;
- what completion can be verified now;
- actions that require new authority or user input.

Infer ordinary implementation details. Ask only when a missing choice is both
material and unsafe to infer.

## Adaptive Loop

Repeat as useful:

1. Inspect the current files, runtime, evidence, prior work, and relevant active lessons.
2. Decide the highest-value next action.
3. Research, plan, implement, or review only as needed.
4. Verify in proportion to risk.
5. Repair important failures and reassess completion.
6. Record a reusable lesson when evidence confirms a meaningful mistake or the
   user corrects a requirement misunderstanding.

Do not use a fixed iteration count. A small task may need one pass; a difficult
task may need several. Do not stop merely because a stage or plan finished.

Research is optional unless current external facts affect the result. A written
plan is optional unless it reduces coordination or execution risk. Product specs,
OKRs, role analyses, harnesses, and review documents are optional tools, not gates.

## Completion

Finish when the requested deliverable exists, relevant verification has passed or
its limits are disclosed, and no high-priority in-scope issue remains that can be
safely resolved.

Pause only when progress requires user input, credentials, payment, unavailable
external state, a consequential product decision, or authority for a destructive
or irreversible action. Report the exact blocker and the smallest next action.

## Persistent State

For long or resumable work, keep a concise `.byte-os/STATE.md` or update the
project's existing state mechanism. Record only what a future session needs:
overall outcome and acceptance, remaining work and evidence, current execution
mode, monitor identity when present, and next step. Link detailed logs; update
this record instead of creating a design document per phase.
Do not create a full Byte OS document set by default.

Use `.byte-os/LESSONS.md` as the automatic error notebook. Keep only confirmed,
reusable lessons with the mistake, corrected understanding or evidence, and a
specific prevention rule. Deduplicate recurring mistakes and never store secrets
or routine trial-and-error noise.

## Handoff

Lead with the delivered result. Summarize meaningful changes, verification, and
remaining limits. Do not end with a workflow command when safe in-scope work is
still unfinished.

## Adaptive execution

Define one overall outcome and acceptance criteria first. For the requested
Goal-plus-monitor workflow, follow [adaptive execution](references/long-running-work.md):
use Goals for difficult core work and scheduled checks for routine supervision
and bounded repairs. Continuously update the remaining work and saved monitor;
disable monitoring before returning to a Goal. Keep one concise state document.

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
