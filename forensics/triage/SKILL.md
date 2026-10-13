---
name: triage
description: Evaluate unevaluated beads issues and move each to an intake state — ready-for-agent, human, needs-info, backlog, or a wontfix close. Use to review what needs attention or to triage a specific issue.
disable-model-invocation: true
---

# Triage

Moves filed-but-unevaluated beads issues to a decided state. State vocabulary and the
`ready-for-agent` gate: `.beads/beads.md` → *Intake States*. Commands: the `beads`
skill. This skill decides *when* an issue moves; it does not redefine what states mean.

## Show what needs attention

Present four buckets, oldest first, with counts and a one-line summary per item:

1. `bd list -l needs-triage` — filed, never evaluated
2. `bd list -l idea` — raw captures worth promoting or dropping
3. `bd list -l needs-info` — were the open questions in notes answered since?
4. `bd human list` — waiting on the user to execute

Use the supplied issue or authorized batch. Ask for selection only when the
request did not establish a scope.

## Triage one issue

1. **Gather.** `bd show <id>` including notes. Do not re-ask anything a prior
   `Established:` note already records.
2. **Redundancy check.** Search the codebase for an existing implementation by
   domain concept, not the issue's wording — and report where you looked.
   If it already exists, that is a wontfix close (step 6).
3. **Prior-rejection check.** `bd search "<terms>" --status all` for earlier
   `wontfix:` closes that resemble this. Surface any match before proceeding.
4. **Verify the claim.** For bugs: reproduce it, or record exactly why you could
   not. An unreproduced bug does not pass the gate.
5. **Decide within authority.** Recommend an outcome with evidence. Apply it
   when the user already authorized that decision or bulk triage; otherwise
   obtain the missing approval. An unreproduced bug stays unresolved/needs-info,
   not automatically wontfix.
6. **Apply the outcome** (all writes with `--actor`):

   | Outcome | Commands |
   |---|---|
   | Agent-executable | verify the gate holds, then `bd label add <id> ready-for-agent` (+ `bd update --acceptance` if missing) |
   | User's work | `bd label add <id> human` |
   | Underspecified | `bd label add <id> needs-info` + questions via `--append-notes` |
   | Real, not now | `bd label add <id> backlog` + `bd defer <id> --until …` |
   | Not doing it | `bd close <id> --reason "wontfix: <why>"` |

   Remove the previous state label, and record what was settled:
   `bd update <id> --append-notes "Established: …"` — so the next session resumes
   instead of re-asking.

## Rules

- One state label per issue; never stack them.
- Never promote to `ready-for-agent` past a failing gate — that label is what
  autonomous claiming trusts.
- Analysis-only requests remain read-only. Carry existing triage authority
  through clear items; escalate material ambiguities separately.
