---
name: orchestrate
description: "Use when an agent orchestrates other agents on a piece of work, of any kind (a plan, a task swarm, a brainswarm): proposing a run tuned to the work, built on the closest protocol (build-verify, idea-to-outcome, brainstorm, debate, editorial, a project's own), settling it with the person, dispatching each member with its brief and role, watching them, judging their findings and steering a drift. Not for the duties one kind adds (orchestrate-plan for a plan, swarm for a task swarm, brainswarm for a seat swarm), and not for the board they talk on (swarm-board)."
---

# Orchestrate

**This session holds the kind's document, its charter, the briefs and the decisions; members do the work.** A member never edits the kind's document or its charter.

## Propose the run

**Protocols are worked examples, never a menu**: each is a proven way for members to work (its
seats, its phases, what each may do, the phases that repeat and the goal that ends them) and the
rules it learnt. Once the person and you are aligned on the work, however you got there, **propose
one run tuned to it, built on the closest example**.

| Example | When it fits | Kinds | File |
|---|---|---|---|
| build-verify | code changed, then judged in the running product, until it holds | task swarm, plan | `references/protocols/build-verify/protocol.md` |
| idea-to-outcome | a list of ideas, each framed, built, proven live and accepted by the person in turn | task swarm | `references/protocols/idea-to-outcome/protocol.md` |
| brainstorm | options, many and varied, before choosing | brainswarm | `references/protocols/brainstorm/protocol.md` |
| debate | known questions to decide, with sources | brainswarm | `references/protocols/debate/protocol.md` |
| editorial | a text for a given reader: a letter, a proposal, a README | brainswarm | `references/protocols/editorial/protocol.md` |

- **The project's own come first**: its `protocol-<name>` skills in its local skills folder
  (`.claude/skills/` when it has no other), and its older `brainswarm-<name>` skills.
- **Read the closest one's `protocol.md`** before proposing; its other files where it says.
- **Estimate the work first, and size the run from it**: the work cut into tasks of one member's
  context each (`references/tasks.md`), how many can run in the same phase without waiting on
  each other, and how many phases that makes. **The example's recommended seats are the starting point,
  reconsidered against that estimate**: kept when the width matches, changed when it does not, the
  change named in the proposal with its reason; its rounds, verifiers and loop's cap are
  reconsidered the same way. For a brainswarm, the
  estimate is the viewpoints the question needs, one seat each that would catch what the others
  would not. The proposal states it in one line: `≈ 12 tasks, 4 at once, 3 rounds → 4 builders`.
- **The person's number wins**: asked for more seats than proposed, re-cut the work finer so
  every seat has work in the first phase (`references/tasks.md`, *Cutting*), never seats left
  idle; asked for fewer, fold tasks together. When the finer cut costs something (tasks sharing
  files, waiting on each other, too small to be worth a member), say so in one line and go on
  unless they change their mind.
- **The proposal is one message**: `Based on <protocol>, with these changes:`, each change against
  the example with its reason (a seat added, a phase dropped, a cap lowered); then the run as one
  table (each phase, who acts in it, every seat's role and area, the special seats); then the
  loop, when it repeats (`until <goal> · cap <n>`, `<n>`, or `unbounded`); each seat's model and
  effort as a column of the table (Opus for all; `medium` for a seat that thinks, `low` for one
  that carries work out, `references/charter.md`); then the example's own fields. It ends on `Go, or adjust?`
- **The base's rules hold unless the proposal says it drops one**: a verifier walks a copy of the
  data, the judged findings table, a fix task names its ids. Nothing departs from the example
  without being named.
- **The person says go, or adjusts lines**: only what they change is talked through, one point at
  a time, through the `interview` skill, the table shown again after. A task swarm with no
  example is workers on call, taking tasks as they come.
- **Once approved, ask the run's authority** (`references/authority.md`, read then): what the
  person delegates, per role, before any dispatch.
- **The approved proposal is the charter** (`references/charter.md`, read before the first
  proposal), the base named in it and on the board (`open --protocol <base>`).
- **A run worth repeating is kept** as the project's `protocol-<name>` skill, on the person's
  yes: read `references/protocols/new-protocol.md` first; the next proposal builds on it.

**A loop runs as its charter says**: each repeated phase's message names its iteration (`verify
3 of 5`); the judged findings table ends on the goal's state; the goal met closes the loop; at
the cap without it, pause and give the person the choice: one more iteration, a raised cap, or
the close. Never an iteration the charter did not grant.

## Handing the run off

**A run that builds code, or any run longer than a sitting, is handed to an orchestrator of its
own** once the proposal is approved: this session stays with the person and can hold several
runs at once. How, per harness (Claude Code, Codex, Cursor) and when nesting is refused:
`references/handoff.md`, read before the first handoff. A small run (one or two members, or one
the person wants to steer closely) is orchestrated here.

## Dispatch

- **One member per seat**, given its work as tasks (`references/tasks.md`, read before the first task), on a subagent definition carrying the charter's model and effort; the dispatch passes its model, and its effort where the `Agent` tool takes one; otherwise effort is carried by the subagent definition the dispatch names (`effort:` in its frontmatter). A dispatch naming neither inherits the session's level. **When no subagent definition carries the charter's model and effort, say so to the person before dispatching**, naming the nearest one; never dispatch on another level silently.
- **The member's agent follows its seat, never `general-purpose`**: every builder (a task swarm's, a plan's) on the plugin's `swarm-worker`, a brainswarm seat on `brainswarm-seat`, a handed-off run on `orchestrator` (or a fork), any verification (a verifier seat, one pass, the proof of a new verify skill) on `verifier` (`subagent_type: "swarmstorm:<agent>"`). It holds the rules every brief of that kind would otherwise have to repeat.
- **The brief is the only thing sent.** Read `references/brief.md` before the first dispatch.
- **Check blockers before every dispatch.**
- **Every ready member's `Agent` call goes in one message**, each in the background, nothing between them.
- **A member whose kind needs a worktree** gets `isolation: "worktree"`, its own install, and its base named in the brief. On Windows, set `git config core.longpaths true` before the first worktree removal.

## Roles

A member given a role (a seat, an expert) gets it in a few sentences. Read `references/roles.md` before writing a member's role.

## Watching

The completion notification ends a member; it does not tell you the work is healthy. On a swarm board, the board's member states and events replace the digest below (the `swarm-board` skill's orchestrator side). Otherwise, while members work:

- **Every few minutes, run the digest** and look at it: `node <skill-dir>/scripts/watch-agents.mjs <subagents-dir> [--label <id>=<member>] [--forbidden '<regex>']`. One line per live member: calls, idle time, last tool, last words. Never open a transcript whole; it exhausts this session's context. Transcripts live under `<claude home>/projects/<project>/<session id>/subagents/`.
- **Report only what is news**: a stale member (no new call in ten minutes), a `BREACH` of the brief's boundary, work clearly outside the member's document. `--forbidden` is the brief's boundary as a regex anchored on a command's verb, never a path.
- **Steer only a drift from the brief**: one `SendMessage` naming the brief line it left. A member that drifts again is stopped and re-dispatched with the brief amended. Decisions its document leaves to the member are its own.

## Findings

**Weigh every finding a member returns before anything acts on it** (a verifier's, a reviewer's, a worker's): you know the document, its decisions and the inputs, which the member may not. **Findings travel as one table, and your answer is the same table judged**, posted before anything is dispatched; only the rows that stand reach a fix. The table, its ids and the judged columns: `references/findings.md`, read before judging the first one.

## A member that stops on a finding

It is done. Fix the kind's document or the member's; never re-brief it past what it found.
