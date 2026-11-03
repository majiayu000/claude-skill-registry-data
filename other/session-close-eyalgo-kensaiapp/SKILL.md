---
name: session-close
description: |
  Close a working session by sweeping what it produced onto durable surfaces, so the next session picks it
  up cold rather than out of someone's head. Four gated sweeps in order — uncommitted work, the journey's
  position, findings the session surfaced but must not act on, and durable session-craft. It **routes
  rather than acts**: each sweep names the skill or file that owns the move, and hands off.
  Use when: a session is ending or being handed over, or the owner asks to wrap up or close out. Use it
  even when the tree looks clean — an uncaptured finding and an ambiguously-open station leave no trace in
  `git status`.
  Do not use for: performing the journey moves themselves (shukuba-park, shukuba-retire, nemawashi-unpick,
  nemawashi-retire, nemawashi-drop, tobiishi-seal own those), writing the corrections store (the harness owns that
  mechanism), or a routine mid-session commit.
  Trigger phrases: "let's close", "close the session", "wrap up", "end of session", "prepare for the next
  session", "hand this over", "session-close".
license: MIT
metadata:
  version: "1.6.2"
  category: journey
  risk: safe
  created: "2026-08-25"
  depends-on: shukuba-park, shukuba-retire, nemawashi-unpick, nemawashi-retire, nemawashi-drop, tobiishi-seal
---

# Session Close

## Purpose

**A session ends with residue, and most of it is only in the session.** The repo keeps the files that
were written. What dies at the end of the turn is everything else: which of the dirty files were
deliberate, where the station actually stands versus where its file says it stands, the three things
the session noticed and correctly refused to do, and the correction it earned the hard way.

This skill sweeps that residue onto surfaces that outlive the session. It is a **close-out**, not a
finishing move — it does not decide that work is done, and it never claims a leg was walked.

**It routes; it does not act.** Every move it identifies already has an owner: a journey verb, the
shared commit recipe, the harness's own memory feature. The sweep's job is to *notice* that a move is
owed and hand it to whoever owns it. A close-out that performs the moves itself would be a second
implementation of each one, drifting from the first the day either changes —
`<CORE>/doctrine/governance/single_source.md` is the general form of that rule.

## The four sweeps

Run them in order and stop at each gate. The order is not decorative: an uncommitted tree makes the
journey's real position unreadable, and a journey left mid-step changes which findings are still this
session's to record.

| Sweep | The question it asks | Where the answer goes |
|---|---|---|
| 1. Uncommitted work | What is dirty, and was it meant to be? | A commit through the builder, or a stated reason it stays dirty |
| 2. Journey position | Where does the journey actually stand? | The journey verb that owns the move |
| 3. Loose findings | What did the session surface that is not its work? | A 根回し Nemawashi seed in the owning project's `unpicked/` |
| 4. Session-craft | What did the session learn about how to work? | The corrections store, or named as a graduation candidate |

---

### Sweep 1 — uncommitted work

Read the working tree of every repo and worktree the session touched. Not just the one it started in:
a session that ran with `--add-dir`, or that opened a change worktree, has more than one.

```bash
git -C "<repo>" status --porcelain
```

For each dirty path, decide one of three things and say which:

- **Commit it** — through `<CORE>/doctrine/governance/commit_via_builder.md`, staging that path by name.
- **Leave it, deliberately** — a scratch file, a gitignored artifact, a half-edit the next session will
  finish. Name it and say why, so the next session does not have to guess whether it was abandoned.
- **It is not yours** — another session's work in a shared index. Leave it untouched and name it.

**Never `git add -A` to catch everything.** The shared recipe rules it out at
`<CORE>/doctrine/governance/commit_via_builder.md:52-53`, and the builder's staged-set guard refuses a
commit whose staged set was not declared. On a busy machine the file that gets swept in belongs to
somebody else's session.

> **Gate.** Show the list and what happens to each line before committing anything.

---

### Sweep 2 — journey position

The session's own account of where it got to is the least reliable source available at this moment.
Read the state instead.

```bash
python3 "<CORE>/tools/journey_status.py"
```

It walks every seedbed, station and change folder in the instance and checks the model's four
invariants (`<CORE>/tools/journey_status.py:18-27`) — more than one seed at a seedbed root, more than one
open station, a station open with no active seed, a change folder with no `change_request.md`. A
violation it reports is usually the shape of a session that stopped in the middle.

Then compare where the journey stands against where the session left the work, and route:

| What the session did | The move that is owed | Owner |
|---|---|---|
| Met the station's reached-when | Close it and tick the seed | `shukuba-retire` |
| Worked the station, did not reach it, is setting it down | Park it, seed item left unticked | `shukuba-park` |
| Walked the last item on the seed's checklist | Retire the idea | `nemawashi-retire` |
| Decided the idea is dead — ruled out, superseded, not going to be done | Drop it | `nemawashi-drop` |
| Is setting the active idea down unfinished | Un-pick it back to the pool | `nemawashi-unpick` |
| Left a change open on its branch | Carry it on or seal it | `<CORE>/launchers/chain-development/launcher.sh <project>`, `tobiishi-seal` |
| Worked inside an open station and it is still open | Nothing — the station carries the position | — |

**Six of those moves are seat-gated.** `shukuba-retire` and `nemawashi-retire` halt outside the Scrum Master,
`shukuba-park`, `nemawashi-unpick` and `tobiishi-seal` outside the PM, and `nemawashi-drop` outside the Principal PM,
so for those rows the move that is owed is named and handed to that seat rather than run
from this session — which changes nothing about the gate below, since this sweep never runs any of them.

The last row is the common one, and it is a real answer rather than a gap. An open station whose file
describes where the work stands *is* the continuation record. If the file no longer describes that,
update the station file — that is a station edit, not a close-out invention.

**Do not open a station, and do not pick a seed.** Both are the PM's call
(`<CORE>/docs/michi_agari.md` § *How we work*, steps 1–2). A close-out that picks the next thing has
started the next session on the previous session's judgment.

> **Gate.** Name the move and the skill that owns it. Wait to be told to run it.

---

### Sweep 3 — loose findings

**This is the sweep whose contents have no other home.** A session that stays inside its scope
accumulates things it noticed and correctly refused to do: a defect in a template it was not editing, a
reference that no longer resolves, a capability something obviously wants. In the session they are
obvious. An hour after it ends they are gone.

For each, decide whether it is already on the board — a seed in `unpicked/`, an open station, a line in
a project's docs. Search before writing:

```bash
grep -rn "<the distinguishing phrase>" system/projects/*/journey/ system/nemawashi/
```

If it is not, write **one seed per idea** into the `journey/nemawashi/unpicked/` of the project whose
Agari it serves — not the project the session happened to be working in. A seed states what was found,
why it matters against that Agari, and what a station would have to settle. Keep it terse: a seed is a
working note, not a report.

If no project's Agari covers it, that is itself the finding. Say so rather than filing it somewhere
close.

> **Gate.** List the candidates and where each would land before writing any of them.

---

### Sweep 4 — session-craft

A session sometimes earns a rule about **how to work** — check the tool's actual behaviour before
planning against it; verify a filter by its effect rather than by reading it. That is different from a
rule about the system, and the two live in different stores.

`<CORE>/doctrine/governance/corrections_store.md` owns the split: `<CORE>/doctrine/` holds rules about
the system and its products; the corrections store holds session-craft, how a session conducts itself.
The subjects do not overlap, and neither store is the other's cache.

So for each candidate, do one thing only — **say which store it belongs in, and why**:

- **Session-craft** → the corrections store. **Do not write it here.** The store's format and mechanism
  are the harness's, not kensaiapp's (`corrections_store.md:9-11`), and a skill that writes it becomes a
  second writer of a store it does not own.
- **A rule about the system** → the doctrine file that owns its subject, which is a doctrine edit with
  its own routing through `<CORE>/doctrine/task_map.md`, not a close-out action.
- **Recurred, and a doctrine file owns its subject** → name it as a **graduation candidate** per
  `corrections_store.md` § *Graduation*. Naming is the whole action. Graduation is one act that states
  the rule and deletes the correction in the same breath, and doing half of it at session close leaves
  exactly the copy that section exists to prevent.
- **One incident, once** → it stays a correction, and that is a finished state, not a backlog entry.

> **Gate.** State the routing. Write nothing into either store from this skill.

---

## The close-out summary

End with this, and nothing longer. It is the artifact the next session reads.

```markdown
## Session close — <YYYY-MM-DD>

**Committed:** <sha> — <what> · <sha> — <what>   (or: nothing)

**Journey:** <project> — <where it stands, and the move owed, or "no move owed">

**Seeds written:** <path> — <one line>   (or: none)

**Craft routing:** <candidate> → <store>, <reason>   (or: nothing durable shifted)

## Left open
<Every question this close-out could not answer, and who has to answer it. "none" when there is none —
never omitted, because an absent section reads as "nothing was left open" and a session that ends with
nothing open is the rare case, not the default.>
```

## Anti-patterns

- **Bundling the gates.** Each sweep is shown and confirmed before the next runs. Batched, the owner
  approves a list rather than four decisions, and sweep 3 is the one that quietly empties.
- **Skipping a sweep because it "looks clean."** Sweeps 3 and 4 leave no trace in `git status`. A clean
  tree is evidence about sweep 1 only.
- **Writing a no-op.** If nothing durable shifted, say so. An invented seed or a manufactured correction
  costs more than the empty line it replaced.
- **Performing a journey move because the owning skill is one call away.** The verbs differ in ways that
  matter — park leaves the seed item unticked, retire ticks it — and a close-out reimplementing them
  will get that distinction wrong on the day it counts.
- **Deciding the work is done.** This skill closes a *session*, never a station, an idea, or a change.

## Reference files

- `<CORE>/docs/michi_agari.md` — the journey model and the loop sweep 2 routes against
- `<CORE>/doctrine/governance/corrections_store.md` — the two stores and what moves between them
- `<CORE>/doctrine/governance/commit_via_builder.md` — how sweep 1 commits
- `<CORE>/tools/journey_status.py` — the reader sweep 2 runs
