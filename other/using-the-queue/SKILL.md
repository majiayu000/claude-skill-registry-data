---
name: using-the-queue
description: "Use to track your committed work or see who is doing what - 'what is on my plate', 'promote a backlog bead', 'assign work', 'nothing pending'. Also run it before concluding you are done, to reconcile committed work against the queue."
---

# Using the Thrum Queue

## Overview

`thrum queue` is a per-agent, local-only, daemon-resident list of the work an
agent has committed to. One queue per `agent_id`; you EDIT your own, anyone may
READ any queue. It is not beads and not a message inbox - beads is the shared
backlog of what COULD be done; the queue is the private, short-lived list of
what an agent IS doing right now, and it is gone when the agent is deleted.

**One rule governs everything else: the queue never crosses agents by itself.**
You only ever write your OWN queue. Assigning, handing off, and cross-box status
all travel as MESSAGES; the receiving agent adds the work to its own queue. No
command writes another agent's queue.

## When to Use

- You need a task list of what you are actively working on.
- Someone messaged you an assignment and you want it tracked as committed work.
- You are promoting a backlog item (a bead / thrum-issue) into active work.
- You are a coordinator/orchestrator routing work and want to record who you
  handed a bundle to.
- You need to see what another agent is working on or how loaded it is.
- You are moving a task between pending / in_progress / blocked / done, or
  clearing finished work out.

## Mental Model

- **Bundle** = one unit of committed work (the only top-level record). Carries a
  title, optional backlog `refs`, a status, a priority, and provenance.
- **Item** = a short checklist entry EMBEDDED inside a bundle. Items are never
  standalone and never linked across bundles. There is no nesting - a bundle
  holds items, nothing deeper.
- **`title` carries the whole content** - there is no body field (40 KB cap).
- **Local-only**: `.thrum/var/queue/<agent>.jsonl`, projected to SQLite, rebuilt
  on cold boot, included in `thrum backup`. Never peer-synced.

## Who-is-doing-what (read this if that is your goal)

Three distinct fields, do not conflate them:

- **`assigned_by`** - provenance: which agent assigned this to me. Auto-filled
  when a bundle/item is created with `--from-message` (from the message author).
  Answers "who gave me this."
- **`assigned_to`** - routing metadata I put on MY OWN bundle via
  `thrum queue assign`. It is informational only. **It does NOT write the
  named agent's queue and does NOT hand the work off.** Answers "who I intend
  this for." The actual handoff is a separate `thrum send`; that agent runs
  `thrum queue add --from-message` to pull it into its own queue.
- **`thrum queue list --agent <id>` / `show <id> --agent <id>`** - read another
  agent's queue directly. Answers "what is agent X working on / how loaded is
  it." Read-only, no permission gate.

## Quick Reference

| Command | Does |
|---|---|
| `thrum queue add --title "..."` | Create a bundle in your queue; the title may be the single quoted argument instead (`thrum queue add "..."`), not both |
| `thrum queue add --from-message <msg_id>` | Special case: lift ONE specific message you received (content->title, author->assigned_by, refs->refs). Use the exact msg-id you're acting on - never head-1 of the inbox |
| `thrum queue add --title "..." --ref bead:<id>` | Promote a backlog item into active work |
| `thrum queue list [--status <s>] [--stage <s>] [--agent <id>] [--assigned <id>]` | List your queue (or another agent's); `--status`/`--stage` AND-combine when both given; `--assigned` filters to bundles assigned to that agent |
| `thrum queue show <bundle-id> [--agent <id>]` | Full detail for one bundle |
| `thrum queue start <bundle-id>` | -> in_progress (clears block_reason) |
| `thrum queue block <bundle-id> [--reason "..."]` | -> blocked (records the reason; `--reason` required) |
| `thrum queue done <bundle-id>` | -> done (TEMPORARY waypoint, not deleted; `start` reopens it; clears block_reason) |
| `thrum queue wait <bundle-id> [--reason "..."]` | -> waiting (alias for `queue update --status=waiting`; `--reason` optional) |
| `thrum queue ready <bundle-id>` | -> ready (alias for `queue update --status=ready`) |
| `thrum queue update <bundle-id> [flags]` | General partial update: `--status`, `--stage`, `--reason` (status_reason), `--title`, `--ref` (repeatable, replaces existing refs), `--priority`, `--assigned-by`, `--assigned-to-remove` - at least one required; `--status=blocked` requires `--reason` |
| `thrum queue drop <bundle-id>` | DELETE bundle + all its items, any status. This is the normal close-out: drop a bundle in the same turn its work lands |
| `thrum queue assign <bundle-id> <agent-id>...` | Append agent(s) to assigned_to (routing metadata only) |
| `thrum queue unassign <bundle-id> <agent-id>...` | Remove agent(s) from assigned_to (clears a stale assignee) |
| `thrum queue note <bundle-id> --stdin` (or `--body-file <f>`) | Append a dated progress note (append-only; shown by `show`, last note previewed by `list`) |
| `thrum queue item add <bundle-id> --title "..."` | Add one embedded item |
| `thrum queue item batch-add <bundle-id> --title "..." --title "..."` | Add several items in one call (shared --ref/--priority) |
| `thrum queue item start/block/done <bundle-id> <item-id>` | Item-level status (start/done clear the item's block_reason) |
| `thrum queue item update <bundle-id> <item-id> [flags]` | Partial item update: `--title`, `--assigned-by`, `--ref` (repeatable, replaces existing refs), `--priority` - at least one required |

Without a Pro licence (`not entitled` / `requires a license`), skip this write and track it in the message thread instead.

Optional: `--ref <type>:<value>` (repeatable), `--priority N` (higher sorts
first), and `--from-message` (special case, below). `add` / `item add` require at
least one of `--title` or `--from-message`; explicit `--title` wins over
`--from-message`. **`--title` is the normal way to add work.**

### Status and stage: two independent axes

A bundle carries two orthogonal fields, both settable via `queue update`:

- **`status`** - `pending`, `in_progress`, `waiting`, `ready`, `blocked`,
  `done`. Says whether the owning agent can or must act now. `start` / `block`
  / `done` / `wait` / `ready` are all just `queue update --status=<x>` under a
  short name; `wait` and `ready` are exact aliases with no independent
  behavior of their own.
- **`stage`** - `intake`, `planning`, `dispatched`, `implementation`,
  `integration`, `review`, `rework`, `gate`, `merge`, `deploy`,
  `verification`, `cleanup`. Says where the bundle sits in its workflow,
  independent of status. Optional; never set on items, bundle-only. Set/read
  via `queue update --stage <s>` / `queue list --stage <s>` / `queue show`.

`status_reason` (set via `--reason` on `update`/`block`/`wait`) is the
general reason field; `--status=blocked` requires it, `wait` accepts it
optionally, other transitions clear it.

## Common Flows

**Add work you're taking on (the normal case):**
```
thrum queue add --title "Ship the X migration"
```

**Promote a backlog bead into active work:**
```
thrum queue add --title "Ship the X migration" --ref bead:thrum-abc12 --priority 5
```

**Lift a SPECIFIC message you received** (special case - mainly an
orchestrator/agent taking a dispatch it was handed):
```
thrum queue add --from-message <msg_id>
```
Copies the message's content into the bundle title, its author into
`assigned_by`, its refs into `refs`, then discards the message ID. 🔴 Pass the
EXACT id of the assignment you are acting on, matched to its sender - NEVER pipe
`inbox --unread | head -1`, which grabs whatever is newest (often a monitor
alert or an unrelated message) and stores it as your title. For anything you
create yourself, use `--title`.

**Hand work to another agent** (two steps, in this order - there is no one-shot):
```
thrum queue assign <bundle-id> @impl_foo      # record intent on YOUR bundle
thrum send --to @impl_foo --stdin <<'EOF'      # actually route it
Assigned you <bundle>: <what + refs>. Add it with: thrum queue add --from-message <this msg id>
EOF
```

Assign at dispatch so `thrum queue list` shows `-> agent` and flags unassigned in-progress bundles;
remove a stale assignee with `thrum queue unassign <bundle-id> <agent-id>`.
The other half of a load check is the role-filtered roster: `thrum team --all --role <role> --compact`;
only live rows (◍) count, not ☓ retired or ☾ sleeping.

Without a Pro licence (`not entitled` / `requires a license`), skip this write and track it in the message thread instead.

**See what an agent has on its plate:**
```
thrum queue list --agent @impl_foo --status in_progress
```

**Finish vs discard:** `done` is a WAYPOINT, not a resting place - it marks a
bundle done and KEEPS it visible (`start` reopens it), but it is not where
finished work should live. `drop` DELETES it and every item inside, regardless
of status. When the work lands, `drop` it in the same turn (`done` first is
optional). A finished bundle is never kept: its history lives in git and the
bead, not in the queue.

**Close on a TRIGGER, not a reminder.** The moment a bundle's branch merges into
trunk, OR its last referenced bead closes, `done` + `drop` it in that same turn -
closure is part of the merge/close act, exactly as `add` is part of dispatch. A
bundle whose branch is an ancestor of trunk, or whose beads are all closed, is
completed-but-open rot; do not leave it for "later". `add` has a natural trigger
(dispatch) and gets done reliably; the close has no trigger unless you make the
merge/close BE the trigger.

**Reconcile is a bounded sweep, not a review.** At session start / breakpoint,
close only the bundles a check proves done, and skip the rest. Two checks only:
- branch is an ancestor of trunk (`git merge-base --is-ancestor <tip> origin/<trunk>`) -> `done` + `drop`
- every `bead:` ref is closed (`bd show <id>`) -> `done` + `drop`

Do NOT read each bundle's full history - the sweep is those two checks against
merged/closed state, nothing more.

## Identity-field mutation: queue vs. state (two intentional shapes)

`queue update` / `queue item update` and `state set` handle identity-field
mutation differently. This is an intentional two-shape convention chosen per
domain, not an inconsistency - do not "fix" one to match the other.

**`queue.update` / `queue.item.update`**: wrapped by `RejectIdentityKeysHandler`, which returns a typed
`*queue.ErrImmutableField` error (`queue: cannot modify immutable field %q`) if a raw identity key (`id`, `agent_id`,
`created_at` for bundles; `id`, `created_at` for items) appears in the wire payload at all - checked BEFORE decode,
fail-closed. Note: `QueueUpdateRequest`/ `QueueItemUpdateRequest` have no JSON fields for these identity keys anyway, so
this wrapper is defense-in-depth, not load-bearing on its own.

**`state.set`**: no reject path at all, and that is by design, per field:
- **Kind/Scope** are the addressing key - a different `(Kind,Scope)` pair
  addresses a DIFFERENT record, so setting them isn't a mutation attempt and
  there's nothing to reject.
- **Class** is derived server-side from the kind registry; no wire field
  exists for a caller to even attempt to set it.
- **CreatedAt** is server-stamped once at creation (on the fleet tier it's
  actually derived from `UpdatedAt` at read time rather than stored
  independently); not client-spoofable, and `StateSetRequest` has no field to
  smuggle it through.
- **EstablishedBy** is influenceable only via `CallerAgentID` on a
  non-peercred transport (browser/WS, unit tests) - but that is a general,
  already-documented property of the RPC layer (identity trust depends on
  transport), not something unique to `state.set`, and it is explicitly out
  of scope per the project's security model: "Thrum does not attempt
  to prevent agent identity forgery" is an owner ruling, stated as
  [INTENDED] and permanent, not tracked as debt.

**The convention, stated plainly:** queue rejects raw identity keys at the
wire as defense-in-depth (even though its request types don't have those
fields anyway); state has no reject path because its identity/system-derived
fields are either addressing semantics (not a mutation) or server-derived/
unspoofable (nothing to reject). Two different but each internally-consistent
shapes, chosen by domain, not an oversight.

Non-goal: fail-closed reject-symmetry for `state.set` (mirroring queue's
`RejectIdentityKeysHandler`) is a possible future non-security hardening
preference, not built here - out of scope per the project's security model.

## Common Mistakes

- **Treating `add`/`done` as the work itself.** The queue *tracks* your work; it
  does not perform it. `add` is not dispatching — the dispatch is the
  `thrum send` / merge / deploy the bundle *mirrors*. `done` means the tracked
  work actually landed, not "I'm finished thinking about it." Marking bundles
  `done` when nothing was dispatched or deployed is a false record, exactly like
  filing a bead and calling the bug fixed — and it inflates the queue while
  little actually ships. Verify the thing landed before `done` (branch merged /
  bead closed / deploy confirmed); otherwise it is still `in_progress` or
  `blocked`.
- **Piping a guessed id into `--from-message` (e.g. `inbox --unread | head -1`).**
  That grabs whatever is newest - often a monitor alert or an unrelated message -
  and stores it as your bundle title. `--from-message` takes the EXACT id of the
  assignment you are lifting, matched to its sender; for anything self-created use
  `--title`.
- **Expecting `assign` to put work in the other agent's queue.** It does not -
  it only tags your own bundle. Always follow it with a `thrum send`; the
  recipient adds it themselves via `--from-message` (with that message's exact id).
- **Leaving done bundles to pile up.** `done` never removes anything - the
  bundle stays, and only `drop` deletes it. Drop each bundle the turn its work
  lands; a queue full of undropped done bundles is the primary rot mode.
- **Reaching for a `remove`/item-`drop` verb.** Removal (of a bundle and every item inside it) happens only at the
  bundle level via `drop` - there is no finer-grained delete. Renaming/re-titling is NOT in this category:
  `queue update --title` and `queue item update --title` are the supported post-create edit path for a bundle's or
  item's title (and other fields - stage, refs, priority, assigned-by).
- **Trying to edit another agent's queue.** Impossible by design - you only
  write your own. Cross-agent work is messaging plus the recipient's own `add`.
- **Treating the queue as durable/shared history.** It is local, private, and
  deleted with the agent. Anything that must survive belongs in beads or a
  committed doc, referenced from the bundle via `--ref`.
