---
name: task-closure
description: Use when someone asks whether a task is ready to close, wants a closure check, needs to verify a task is genuinely done, or asks to confirm a task can be marked complete.
argument-hint: [task or topic]
allowed-tools: Read, Glob, Grep, Write, Bash(git status), Bash(git log *)
---

## What This Skill Does

Verifies whether a task is genuinely ready to close by checking nine dimensions — requirements, deliverables, validation, assumptions, evidence, approvals, temporary files, unresolved issues, and requester handoff — against actual evidence, never assumption. Returns exactly one verdict: **COMPLETE**, **COMPLETE WITH LIMITATIONS**, **REVIEW REQUIRED**, **BLOCKED**, or **INCOMPLETE**. Never modifies, publishes, or deletes anything without explicit, per-action approval.

## Check-Status Vocabulary

Every check in this skill — the nine dimensions, each traced requirement, and every piece of cited evidence — uses exactly one status, never a different label:

- **Confirmed** — genuine, fresh evidence supports this.
- **Gap Found** — checked, and evidence is missing, contradicts, or fails.
- **Unknown** — could not be determined (no accessible evidence, not confirmable, ambiguous).
- **Not Applicable** — doesn't apply to this task.

Never label anything Confirmed without citing the specific evidence behind it (a file path, a git result, a tool output, an explicit user statement). No exceptions, and no other status labels anywhere in this skill's output.

## Input

`$ARGUMENTS` is the task or topic to check.

If empty, infer the task from what was just completed in the current conversation. If the task can't be identified with reasonable confidence, ask the user directly before proceeding — never guess.

## Step-by-Step Workflow

### Step 1: Identify the Task and Gather Evidence Sources

Restate the task in one line. Then gather everything available across:
- The current conversation (what was requested, done, and said)
- Project files relevant to the task
- `git status` and `git log` (uncommitted changes, unpushed commits, recent relevant commits)
- A matching `output/evidence-packs/<task-slug>/` folder, if one exists — use it directly as the evidence source for the components it covers rather than re-deriving them from conversation
- Any other visible tool output from the conversation (test results, screenshots, build reports)

### Step 2: Requirement-Level Traceability

Do not treat "Requirements" as one lump check. Extract the individual requirements from the original request (as explicitly stated — never invented), list each one separately, and trace each to the specific evidence that satisfies it:

| # | Requirement (as stated) | Evidence | Status |
|---|---|---|---|
| 1 | ... | file / commit / tool-output reference | Confirmed / Gap Found / Unknown / Not Applicable |

The "Requirements" dimension's overall status is the **worst** status among its rows — any single Gap Found or Unknown pulls the whole dimension down. Never average or round up.

### Step 3: Evidence Freshness Check

Before marking anything Confirmed, check whether the evidence is still current relative to the task's present state — not just whether it once existed. Evidence is **stale** if the artifact it describes has changed since the evidence was produced (e.g. a validation run before the last edit to the file it validated, a hash computed before a subsequent change, a screenshot of a since-modified page).

Stale evidence can never support Confirmed. Downgrade the affected check to Gap Found (if the current state is verifiably different) or Unknown (if it can't be re-verified right now) — cite what changed and when, and re-verify against the current state before relying on it.

### Step 4: Run the Nine Dimension Checks

For each dimension, determine status per the vocabulary above, citing evidence and applying the freshness check from Step 3:

1. **Requirements** — per Step 2's traceability table.
2. **Deliverables** — does the actual output exist, at the stated location, matching what was promised?
3. **Validation** — were checks actually performed (not just claimed)? Cite the specific validation run and its result. Never infer a pass from the absence of a reported failure.
4. **Assumptions** — were any assumptions made during the task ever left unconfirmed? List each one; Confirmed only if explicitly resolved with the user.
5. **Evidence** — is there a traceable record for the above (files, logs, an evidence pack, tool output)? Not Applicable only if the task genuinely produced nothing that needs evidence.
6. **Approvals** — were required approvals actually obtained explicitly (never assumed from silence)? Cite the specific approval and when it was given.
7. **Temporary Files** — see Step 5.
8. **Unresolved Issues** — see Step 6.
9. **Requester Handoff** — has the deliverable actually been presented to the requester, in a form they can use, with its location stated clearly?

### Step 5: Temporary-File Handling (Classified)

Actively scan known scratch/temp locations (the session's scratchpad directory, and any disposable directories mentioned in the conversation) via Glob for leftover files. Classify each one found:

- **Disposable** — pure scratch/intermediate work (scratchpad, OS temp dir, or explicitly described as temporary). Safe to flag for deletion.
- **Deliverable-adjacent** — sits inside or near the actual output location (e.g. `output/`) and might be part of the intended deliverable. Never classify as safe to delete without explicit confirmation it isn't part of the output.
- **Unknown** — can't confidently classify. Treat conservatively: never propose deletion, always ask.

The "Temporary Files" dimension is Confirmed only if every Disposable file found has been either already cleaned up or explicitly approved and removed this run (Step 7). Any Disposable file left behind, or any Unknown-classified file, makes this dimension Gap Found.

### Step 6: Unresolved Issues

Scan the conversation, project files, git status, the evidence pack (if any), and other tool results for explicit open questions, TODOs, pending approvals, failed checks, caveats, deferred work, dependencies, or promised follow-ups. List each with its evidence and impact. Then ask via `AskUserQuestion`: "Is there anything else outstanding that isn't captured above?" — options **No, that's everything (Recommended)** / **Yes, there's more** (if yes, gather it as free text).

Never treat silence or missing evidence as confirmation that no unresolved issues exist. If confirmation is unavailable, mark this dimension Unknown, not Confirmed.

### Step 7: Handle Fixable Issues (Approval-Gated)

If a fixable issue was found (most commonly: Disposable temp files to remove), do not act automatically. Ask a specific, scoped question via AskUserQuestion (e.g. "Delete these N disposable files — Recommended" / "Leave them"). Act only on explicit approval, and only on exactly what was approved — never expand scope beyond it. This is the only point in the workflow where this skill may modify or delete anything, and only after this specific gate. Deletion is not in `allowed-tools`, so the delete command itself will separately prompt for permission — an intentional second gate on top of the `AskUserQuestion` approval above.

### Step 8: Verdict Precedence

Evaluate in this exact order; stop at the first rule that applies:

1. **BLOCKED** — any required check can't be completed due to a dependency outside the assistant's or user's immediate control (missing access, waiting on a required decision or action from someone else).
2. **INCOMPLETE** — any core requirement or deliverable check is Gap Found, and it isn't blocked (the work itself remains to be done).
3. **REVIEW REQUIRED** — no core work is missing, but at least one check is Unknown, evidence for a required check is stale and unverified, an approval is still pending, or an unresolved issue needs a human decision.
4. **COMPLETE WITH LIMITATIONS** — every required check is Confirmed or Not Applicable, but one or more disclosed, non-blocking limitations were explicitly documented and accepted.
5. **COMPLETE** — every required check is Confirmed or Not Applicable, with no Unknowns, no stale evidence, no unresolved issues, and no undisclosed limitations anywhere.

### Step 9: Final Decision-Quality Gate

Before reporting the verdict, self-check for internal consistency:

- Does the verdict contradict any individual check's status? (No verdict better than INCOMPLETE is valid while any core check is Gap Found; COMPLETE is invalid while any check is Unknown or stale.)
- Were all nine dimensions actually addressed — none silently skipped?
- Does every Confirmed status have cited evidence attached?
- Does the chosen verdict match the specific precedence rule that triggered it, not a feel-based pick?

If the gate finds an inconsistency, do not report the original verdict — fix the mislabeled check(s) or fall back to the more conservative verdict the corrected labels actually support, and say so explicitly in the report.

### Step 10: Report

Show the full report in chat by default: the requirement-traceability table, all nine dimension statuses with evidence, the temp-file classification, the unresolved-issues list, required next actions, result location(s), and exactly one final verdict with the precedence rule that produced it.

Only save the report to `output/task-closure/<task-slug>-closure-report.md` if the user explicitly asks. Never save automatically.

## Output Format

```
# Task Closure Check: [task name]

## Requirement Traceability
| # | Requirement | Evidence | Status |
|---|---|---|---|
| 1 | ... | ... | ... |

## Dimension Checks
| Dimension | Status | Evidence | Notes |
|---|---|---|---|
| Requirements | ... | ... | ... |
| Deliverables | ... | ... | ... |
| Validation | ... | ... | ... |
| Assumptions | ... | ... | ... |
| Evidence | ... | ... | ... |
| Approvals | ... | ... | ... |
| Temporary Files | ... | ... | ... |
| Unresolved Issues | ... | ... | ... |
| Requester Handoff | ... | ... | ... |

## Temporary Files Found
| File | Classification | Disposition |
|---|---|---|

## Unresolved Issues
- [issue] — [evidence] — [impact]

## Required Next Actions
1. ...

## Decision-Quality Gate: [PASS / corrected — see notes]

## Verdict: [COMPLETE / COMPLETE WITH LIMITATIONS / REVIEW REQUIRED / BLOCKED / INCOMPLETE]
[Which precedence rule triggered this, in one sentence]
```

## Notes

- Never modifies, publishes, or deletes anything without explicit, per-action approval (Step 7) — this applies even when the user has already approved the task's underlying work in general.
- Never claims a check, validation, approval, cleanup, or handoff occurred without citing real evidence — missing or ambiguous evidence is Gap Found or Unknown, never Confirmed.
- Never treats silence as confirmation of anything (approvals, unresolved issues, cleanup).
- `context: fork` is intentionally not used — this skill must inspect the current conversation directly, which a forked subagent cannot see.
- Complements `evidence-pack-builder` (reads its output when present) and pairs naturally with `first-task-mapper` as the opening and closing bookends of a task.
- Chat output by default; a saved file is only ever written after an explicit request, to `output/task-closure/<task-slug>-closure-report.md`.
- Clickable-question convention: Step 6's "anything else outstanding?" check and Step 7's approval-gated fix already use `AskUserQuestion`. Task identification (Input section, when ambiguous) stays free text — genuine content, not a finite menu.
