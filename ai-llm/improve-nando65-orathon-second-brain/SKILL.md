---
name: improve
description: Turn one recurring pain point into one measurable, bounded workflow improvement.
argument-hint: "[problem or workflow]"
---

# Improve

Read `SYSTEM.md`, current objectives, source registry, decision journal, relevant captures, and recent healthchecks.

The goal is one useful improvement per run, not a broad transformation plan.

## Step 1 — Select one problem

Prefer a problem that is:
- repeated,
- expensive in time or errors,
- tied to a current objective,
- and narrow enough to test.

If the user already supplied a specific problem, use it unless evidence shows a prerequisite is missing.

## Step 2 — Define the before and after

Capture:
- current process,
- current pain or failure mode,
- desired output,
- one measurable success signal,
- who reviews or owns the result.

## Step 3 — Simplify before automating

Ask:
- Can any step be removed?
- Can inputs be standardized?
- Can a deterministic rule solve part of it?
- Which parts genuinely need language-model reasoning?
- Which decisions should remain human-owned?

## Step 4 — Map the workflow

Write:
- trigger,
- inputs and authoritative sources,
- ordered operations,
- decisions/branches,
- output destination,
- error path,
- privacy or permission constraints.

## Step 5 — Choose the smallest implementation

Use the least complex option that meets the goal:

1. checklist or template,
2. reusable prompt,
3. deterministic script,
4. AI-assisted workflow with review,
5. multi-step agent only when the earlier options are insufficient.

## Step 6 — Define acceptance

Before building, specify:
- sample input,
- expected output,
- what must never happen,
- how a human will verify quality,
- what evidence is required before increasing autonomy.

## Deliver

Record the decision in `journal/decisions.md`.

Then create or update one artifact under `workflows/` that implements the chosen approach. Preserve unrelated files.

End with:
- what changed,
- how to test it,
- what evidence would justify the next iteration.
