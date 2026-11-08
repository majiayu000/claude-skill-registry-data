---
name: turn-entry-map
kind: pattern
rule: turn-entry
description: Pattern of rule turn-entry. Load when editing the turn map and the hook that serves it — what goes into the map, how it differs from a rule, how the hook stays silent about what is missing and how that is checked. Not for the shape of the handover itself — that is pattern task-flow-handoff.
---
<!-- rt-kit v0.34.0 · patterns/turn-entry-map.md · f32d338c4fa7 · правится надстройкой, не здесь -->

# The turn map and its serving — ready-made code

Pattern of the rule `turn-entry`. What must be true — the law
`docs/constitution/work-conduct.md`.

## When to use

- A state was added to the rule on the course of work — the map fell behind.
- The entry hook is being edited, or the order in which the parts of the entry are put into the
  context.
- The map check turned red.

## What goes into the map and what does not

The map answers the question "what to do", the rule — the question "why". There is one selection
sign: a line the session reads and then takes the next step — into the map; a line that explains
where the requirement came from — into the rule.

| Into the map                                        | Into the rule                                            |
| --------------------------------------------------- | -------------------------------------------------------- |
| the state name and its mandatory action             | why this action is mandatory                             |
| the pattern the state leads to                      | the incident analysis it grew out of                     |
| the four turn exits and what backs each of them     | what happens when a turn is ended otherwise              |
| a line that the rest is a continuation of the turn  | the list of what a turn must not end with, with examples |

An incident analysis never moves into the map: it explains, and an explanation is the rule.

## Serving: first the handover, then the map

The order is not indifferent. The handover says where exactly this work stands, the map — what is
done in such a place in general. Read first, the map answers a question the session has not asked
yet.

```bash
# the handover — by the name of the current branch, not by picking from the directory
handoff="$ROOT/${RT_HANDOFF_DIR:-.claude/handoff}/$(git branch --show-current).md"
[ -r "$handoff" ] && { printf 'HANDOVER OF THE PAST SESSION\n\n'; cat "$handoff"; }

# the map — as its own file, not parsed out of the rule
[ -r "$map" ] && { printf 'TURN MAP\n\n'; cat "$map"; }

exit 0
```

Three things in this piece are mandatory and easily lost:

- **`-r`, not `-f`.** The file may exist and not be readable; `-f` then lets `cat` through, and
  the hook prints a heading over emptiness.
- **`exit 0` at the end and no other exits.** The entry hook refuses nothing: a session without
  part of the context is better than a refused launch.
- **The file name is built from the branch.** Picking "the first one found" in the directory
  serves someone else's handover, and it looks like one's own.

## What it is checked with

```bash
node tools/check-turn-map.mjs   # size, completeness of states both ways, four exits
```

The check compares the state names of the map with the rule's table both ways: a state declared
by the rule and forgotten in the map, and a state left in the map after a rename — both are
divergences.

A live trial of the hook is done on a tree where both parts lie, and is repeated four times: both
parts, without the handover, without the map, without both. The last case must give empty output
and a zero code — a hook that stayed silent with a non-zero code reads as a refused launch.

## Common misses

- **The size limit is assigned by measurement, not by eye.** The first number was chosen as
  "twice the current map" — and the check turned red on its own text in the very first run: a map
  in Cyrillic weighs twice what the line count suggests.
- **Going past the limit means splitting the map, not raising the limit.** Raised once, it is
  raised a second time too, and the map quietly becomes a second copy of the rule.
- **A map parsed out of the rule on the spot breaks silently.** No check sees an edit of the
  table markup, and the map after it arrives empty — and the session never learns of it.
