---
name: aid-triage
description: >
  Suggest which AID entry point fits the work you are describing. Use this skill when you
  know what you want to change but not which skill to reach for. Give it one short free-form
  description; it infers the work type, judges the scope, and names the single best entry --
  the matching verb-and-artifact shortcut for a known single change type, or the full path
  via `/aid-describe` for broad or ambiguous work. It reads the shortcut catalog to resolve
  its suggestion to a canonical, non-alias name. It suggests only: no interview, no
  scaffold, no work folder, and nothing written.
allowed-tools: Read Glob Grep
argument-hint: "[description]  -- what you want to do; I'll point you at the right entry"
---

# Route to the Right Entry

For the "I don't know which path or skill fits" case. Takes a short free-form
description and suggests where to go next -- a specific direct-entry shortcut
(`/aid-fix`, `/aid-create-api`, ...) for a known, single change, or the full
path (`/aid-describe`) for anything broad, multi-activity, or ambiguous.

This skill is largely the **extraction** of `/aid-describe`'s former TRIAGE
routing logic into a standalone router, so the routing capability
`/aid-describe` used to provide is preserved here, relocated (see
`references/state-suggest.md` for the reflect-back turn this was extracted
from).

## Agents Involved

`/aid-triage` is a **single-turn, suggest-only** skill -- it runs entirely
inline, with no subagent dispatch. NFR-8 (no over-engineering): the
reflect-back turn is a one-shot conversational exchange, not a multi-turn
interview, so no dedicated agent, work folder, or `STATE.md` is warranted.
Because the skill produces no graded artifact (it writes nothing to disk),
there is no runtime `aid-reviewer` gate either -- unlike the retired
aid-describe lite-path review step, FR-11's per-document grading does not apply here. The skill
itself is graded at build time by `aid-reviewer` like any other shipped
skill.

## Pre-flight

Check that a free-form description was supplied (as the invocation argument,
or -- if omitted -- ask for it in the INTAKE turn below; either is fine, the
description is always captured before CLASSIFY runs).

No `.aid/` workspace check is required -- `/aid-triage` never reads or writes
work state; it only reads the installed catalog.

## Arguments

| Argument | Effect |
|----------|--------|
| `[description]` | A short free-form description of what you want to do. If omitted, INTAKE asks for it. |

---

## State Machine

`/aid-triage` is **stateless across invocations** -- there is no `STATE.md`,
no work folder, and therefore no state to resume. Every invocation starts
fresh at INTAKE and runs straight through to HALT in one pass.

```
[● INTAKE ] -> [ CLASSIFY ] -> [ SUGGEST ] -> [ HALT ]
```

> **State-machine chaining:** Each `/aid-triage` invocation drives the state
> machine until it hits a natural pause point per
> `.aid/runtime/templates/state-machine-chaining.md`. Every state here is
> either mechanical or an inline question; only HALT stops the run.

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| INTAKE | inline (below) | inline | CHAIN -> CLASSIFY |
| CLASSIFY | `references/state-classify.md` | inline | CHAIN -> SUGGEST |
| SUGGEST | `references/state-suggest.md` | inline | CHAIN -> HALT |
| HALT | inline (below) | inline | -> halt |

---

## State: INTAKE

Capture one short free-form description in a single turn -- no adaptive
loop, no scaffold. If the invocation already carried a `[description]`
argument, use it directly and skip the prompt below.

```
In a sentence or two -- what do you want to build, change, or fix?

Suggested: For example: "fix the login crash on special characters" or
           "add a /orders REST endpoint."
Why: A short description is enough to tell whether this is a single,
     well-scoped change (I can point you straight at a shortcut) or
     something broader (better handled by the full /aid-describe interview).

[1] Use the form above and share yours
[2] Your answer: ___
```

Wait for the answer. Record it internally as `{description}`.

**Advance:** **CHAIN** -> [State: CLASSIFY] (continue inline).

---

## State: HALT

Print the recommended invocation the user should type next, then **STOP**.
`/aid-triage` never invokes another skill on the user's behalf -- it
suggests; the user runs the command. No file is written; no `.aid/works/work-*/`
folder is created; no `STATE.md` exists for this skill.

**Shortcut suggested:**
```
-> Suggested next step:

    /{name} "{description}"

Run that command to start -- it goes straight to the flattened Lite work
for {intent}.
```

**Full path suggested:**
```
-> Suggested next step:

    /aid-describe

Run that command to start the full requirements interview.
```

---

## Constraints

- **Suggest-only (FR-13).** No interview, no scaffold, no work folder, no
  `STATE.md` is ever created by this skill.
- **Write-free.** `allowed-tools` is `Read Glob Grep` only -- no `Write`,
  no `Edit`. This skill cannot write anything even if instructed to.
- **Canonical names only (Step 3 catalog match).** When the suggestion comes
  from Step 3's shortcut-catalog semantic match (Cases A/B/C), it is always a
  canonical catalog `name` (`alias_of: null`); an alias row is never
  suggested directly there -- see `references/state-classify.md`.
  **Case D (the QUESTION route)** hard-routes to `/aid-ask`, the canonical
  Q&A row -- Step 0 short-circuits past Step 3 entirely, so this constraint
  applies only to Cases A/B/C; see `references/state-suggest.md` Case D.
- **Conservative default.** Anything short of one confident, single-match
  suggestion routes to the full path (`/aid-describe`) -- mirrors the
  conservative default that aid-describe's former TRIAGE state used before
  extraction.
