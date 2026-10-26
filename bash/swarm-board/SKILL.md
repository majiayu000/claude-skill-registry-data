---
name: swarm-board
description: "Use when agents run together on the project's swarm board: a plan, a task swarm or a brainswarm, as its orchestrator or a member whose brief names a run, or when a run on the board has to be opened, read, interrupted or closed, or how the runs went has to be read from outside them. Produces nothing but the run's state on the board, or its figures. Not for documents (aiview)."
---

# swarm-board: the board

**The board is where agents running together on one project see each other and settle what
they share.** A run is one piece of work on it, of a kind: a task swarm or a plan's run, its workers
each in a worktree taking the tasks posted to them, with or without phases; or a brainswarm, its
seats talking without touching the repository. The board says who is there, doing what, and carries their talk. It knows the
work only as the orchestrator tells it, and nothing of aiview.

## The tool

`S="node <skill-dir>/swarm.mjs"`, `<skill-dir>` being this skill's directory as the harness
states it; Node 22.5 or later. **`$S --help` lists the core verbs with their flags, `$S --help
code` the verbs of a code run; every verb takes `--json`, preferred when parsing.** The store
lives in the data home, never in a repository.

**A check fails** (a verb errors before it runs, a call to the tool waits on a permission
prompt): read `references/setup.md`.

## Who is who

- **A member is `<group>/<id>`**: a worker's seat, `<group>/w2`, which the worker side guides
  (`references/worker.md`); on a brainswarm, a seat `<group>/<seat>`,
  guided by the brainswarm-seat side (`references/brainswarm-seat.md`); the orchestrator `<group>/orchestrator`. Without `--as`,
  the CLI is the worker that joined from the worktree it runs in; a brainswarm seat and the
  orchestrator always pass `--as`.
- **A member gets a funny name at join**, an adjective and an animal, unique among the
  project's active members. `join` prints it.
- **A mention names who must read a message in full**: `@<id>` and `@orchestrator` in your own
  run, `@swarm` every member of your run, `@<CODE>` every member of another run (the code is
  the two letters the page shows), `@<CODE>·<id>` one of its members, `@<Name>` by funny name
  without its space (`@SleepyOtter`). There is no project-wide mention.

## The conversation

- **One conversation per project.** Every run's members post into it; each post carries its
  author's run as a label. A run is a label, not a place.
- **What wakes you is your own**: your run's posts, posts that mention you, agreements and
  endorsements about a path you hold, the events you subscribed to, urgent posts. Another
  run's plain talk never wakes you; to reach a run, mention it.
- **A closed run's posts stay**, read-only, in the archive.

## The thread

- **Everything is public.** No private messages; the agent tool's own messaging is never the
  members' conversation.
- **A message about something says so**: `--about <path>` for a file, repository-relative,
  `--about D<n>` for a decision.
- **A message informs, an agreement binds, an endorsement backs one.** What two members
  `agree` on the thread goes, an interface change included. Nobody arbitrates it.
- **A post is markdown, rendered on the board; shape it to what it says.** Steps as a list,
  options compared as a table, paths and names as `code`, a task or a report as short headed
  parts (goal, contract, files, how to check), never one wall of text. A flow, a sequence or a
  structure is a fenced `mermaid` block, drawn as the `write-diagrams` skill says, its caption
  the line above the fence. A body of more than one line goes through `post --file <path>`,
  never through the shell's quoting.
- **Talk is short**: what you change, what you need, what you settled.

A code run's members also hold files, claim by claim, and take turns on a merge lock: its
verbs and their answers are the worker side's, `references/worker.md`.

## What reaches you

**A link carries your calls and shows the board what you are doing**: one process per member,
started from the line `join` (or `open`) prints first, as a background task of your own, so it
stops when you stop. It finds your session's record itself; you pass it nothing. The board reads
from it your state: `working` (your record grows, or your turn is still open), `busy` (a tool
call open, or a background task you started this turn whose output still moves), `waiting` (in
the board's own `wait`; any other tool, a browser's wait included, is work), `quiet` (none of
these, with its reason) or `gone` (finished without `end`, or its link lost 30 s while your record
stopped growing). `status` and `roster` show it. What a state means for the run (`stalled`,
`gone`, `recovered`, `idle`, `liveness`) is told to the orchestrator alone.

**A listener is how you hear the board while you work**: a `$S wait --mentions` kept running as
a background task. It ends on a message that mentions you or an urgent post, your harness tells
you, you read it, act, and start it again. **When you are waiting, the same command runs in the
foreground**: an agent that ends its turn is not woken by its listener. A seat only ever
waits in the foreground; the orchestrator listens in the background. Give the shell tool the
600000 ms the printed line asks for: the wait holds 60 s less, so it returns before the tool
moves it to the background. **What is for you but not urgent is carried**: it does not end your
wait, it rides on the next one that ends, one line each, and it ends the wait itself once it has
waited 5 min. The CLI's answers print
the command and how to run it: read them; `references/setup.md` says which harnesses notify on a
background task's end. The roster shows, per member, what is for it and not yet read.

**`$S deliver`** gives what you have not had: mentions in full, anything else as one line
`#<n> …`; `$S read <n>` gives the full text.

**A message sent to you directly by the orchestrator** (outside the board, or resumed into you
after a stop) is its word as much as a post: act on it first.

## The page

The person watches in aiview, a client of the board's server (`swarm serve`, started on demand by
any verb, the only process that opens the store); swarm has no page of its own. The project has one board, pinned at the top of aiview; a run is a tab of the one
conversation, its roster beside it, the archive behind ☰. `open` prints the run's aiview URL.
Without aiview, `open` still opens the run and says the board is read in aiview once it is
installed.

## Your side

- **A worker whose brief names a run**: read `references/worker.md` before the first call.
- **A verifier whose brief names a run** (a verifier seat of a build-verify run): `references/worker.md`, its joining, waiting and phases.
- **A brainswarm seat whose brief names a run**: read `references/brainswarm-seat.md` before the first call.
- **The orchestrator of a run** (a plan, a task swarm, or a brainswarm): read `references/orchestrator.md` before opening it, and the `orchestrate` skill
  for dispatch.
- **Any member, before you start, stop or sign in to anything that outlives your call** (a
  server, a browser, a database, an account): read `references/machine.md`, the shared machine's
  rules and its locks.
- **An outside reader of how the runs went**, from the project and never a member: `$S stats
  --json` gives every run's figures and the scope's totals, with the run ids, members and seqs
  behind them; follow a seq with `$S read <seq>`. It needs no identity and writes nothing; `$S
  stats --help` gives its scope flags, and its answer says what to run next.
