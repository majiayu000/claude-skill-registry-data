---
name: byte-do
description: Choose and execute the useful Byte capabilities for a mixed product or project request. Use when the user explicitly invokes $byte-do or asks Byte to select the workflow; focused requests should use the matching skill.
---

# Byte Do

Act as the adaptive front door to the Byte skills. Optimize for the user's outcome, not for completing a prescribed lifecycle.

## Operating Principles

- Follow explicit user intent, scope, and stopping instructions first.
- Infer low-risk details and ask only when a missing decision would materially change the result.
- Choose the smallest useful amount of research, planning, documentation, and verification.
- Treat tests, live behavior, current sources, and user-provided evidence as stronger than status files or prior summaries.
- Preserve user work and make consequential or irreversible actions explicit.
- State assumptions and remaining limits honestly.
- Learn from confirmed mistakes and corrected requirement misunderstandings.
- Use subagents only when explicitly requested and supported. Use ordinary task state unless Goal mode is requested.

## Capability Choice

Honor an explicit `$byte-*` selection. Otherwise use only the capabilities that
materially help the requested result: discussion, ideation, research, planning,
implementation, review, autonomous completion, status inspection, or parking a
future item.

Act directly when ordinary reasoning is enough. Do not load another Byte skill
merely because it exists, announce an internal route by default, or force named
stages. Combine capabilities naturally when the outcome genuinely needs them.

## State

`.byte-os/` is optional. Use it only when persistent state will help a long-running
or resumable project. Prefer a small `STATE.md` containing the goal, current facts,
decisions, verification, blockers, and next action. Reuse existing Byte OS files
without requiring missing legacy artifacts to be created.

Interpret older Byte OS artifacts as ordinary project evidence. Live repository
and runtime evidence remains authoritative.

## Lessons Notebook

Before related work, read active entries in `.byte-os/LESSONS.md` when it exists
and apply relevant prevention rules.

After the user corrects a requirement misunderstanding, or direct evidence
confirms a meaningful mistake, create or update `.byte-os/LESSONS.md`. Record a
lesson only when it is likely to prevent future error. Do not record routine
exploration failures, trivial slips, vague self-criticism, duplicates, secrets,
or sensitive user data.

Use a concise entry:

```markdown
## <date> — <lesson title>
- Context:
- Mistake or misunderstanding:
- Correct understanding and evidence:
- Prevention rule:
- Status: active
```

If the same mistake recurs, update the existing entry with recurrence evidence
instead of creating another. Mark a lesson `superseded` when later evidence
invalidates it. This notebook is the one Byte OS artifact that may be created on
demand even when no other persistent state is needed, unless the user asks for
discussion only or no file changes.

## Response

Lead with the result. Mention routing, artifacts, or next commands only when they
help the user understand or continue the work. Do not emit a fixed status template.

## Adaptive execution

For the requested combined workflow, use
[adaptive execution](references/long-running-work.md): one overall outcome,
Goals for hard core work, and evolving scheduled checks for routine follow-up.
Choose from live evidence; do not create a new Goal after every finished job.

## Source And Updates

Canonical repository: [elan6666/your-bytedance-skills](https://github.com/elan6666/your-bytedance-skills). Use its current `main` branch when checking for or installing updates.
