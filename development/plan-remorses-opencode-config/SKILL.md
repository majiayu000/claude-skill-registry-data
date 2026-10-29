---
name: plan
description: >
  Plan work that spans several tasks or sessions as a checklist file where every box names
  its evidence, then execute it task by task with clean pickup between sessions. Adapted
  from the pstack multi-phase plan playbook. Records user corrections and design calls as
  decision files in plans/decisions/ (adapted from tRPC vNext), so later agents keep the
  same choices. Use when asked to plan, write a plan, break work into tasks or phases, or
  continue, resume or pick up a plan in a new session. Also use when the user corrects an
  approach in a repo that has plans/decisions/.
---

# plan

A plan is a checklist one agent runs box by box and the user audits from the evidence.
State that must outlive a session goes in the plan file and in git, never in chat context.
Do not rely on compaction.

Choices that must outlive the plan go in **decision files**. The plan is deleted when
done; decisions stay, so an agent that refactors the code a year later keeps the same
philosophy.

```
plans/
  <slug>.md              active plan, deleted when done
  archive/<slug>.md      dropped plans
  decisions/<topic>.md   one file per decided topic, permanent
```

## When to plan

- **Skip it** when the change is one or two files with an obvious approach. Say so and do
  the work.
- **Design first, plan last.** Settle open questions with throwaway prototypes in a scratch
  folder, not with debate. Never review an abstract plan with no code behind it:
  reviewers invent risks that never happen.
- **Read every relevant file before writing the plan.** Never plan to "explore" later.
- **Ask the user only product or preference calls** no experiment can settle. Give options
  and a default.
- **The plan is the deliverable.** Do not implement until the user says go.

## Write the plan

Path: `plans/<slug>.md` at the repo root (not under `docs/`), unless the user names one.

- **One active plan per repo.** Before creating a new plan, finish the current one or
  archive it: move it to `plans/archive/<slug>.md` with a one-line status at the top.
- **Reference it in AGENTS.md** while active, so every new session reads it without the
  user mentioning it. Edit the non-generated source (check the first lines for a
  "generated" notice). Near the top:

```markdown
Active plan: `plans/<slug>.md`. Read it before starting work.
Decisions: `plans/decisions/`. Search them before designing or refactoring.
```

The `Decisions:` line is permanent. Add it with the first decision file and keep it after
the plan is done.

One task is one session-sized unit that ends in a state you can check. Order tasks so the
sequence proves itself:

- riskiest unknown first
- subtraction (delete dead code, old paths) before additions
- verification harness and baseline capture before the change it measures
- shared types and scaffold before features

````markdown
# <Goal> plan

<Under 10 lines: what changes, for whom, the done check for the whole plan, task ids in order.>

## How to read this

One box is one unit of work. Check a box only when its evidence exists: a command output,
a file, a screenshot, a log line, a commit SHA. Write the evidence next to the box.
Tests alone are not verification. Each task is verified on the real artifact.

## Task 1: <verb phrase>

**Depends on.** None.

**Files.**
- [ ] Edit `<path>`
- [ ] Delete `<path>`

**Build.**
- [ ] <one change, naming the symbol and file>

**You see.**
- [ ] <one observable result: exact output, screen state or log line>

**Verify.**
- [ ] Run `<command>`. Pass when <predicate>.
- [ ] <drive the real surface: CLI command, playwriter, tuistory, HTTP call>. Pass when <predicate>.

**Progress.** <empty until a session stops mid-task>

## Task 2: <verb phrase>

**Depends on.** Task 1.
...

## Done

- [ ] Every box above is checked with evidence.
- [ ] <whole-goal check on the real artifact>

## Appendix A. Prototype evidence
<each open question a prototype settled, with the scratch path and what it showed>

## Appendix B. Decisions
<a link to each `plans/decisions/<topic>.md` this plan made or depends on>

## Appendix C. Risks
<each risk, the task it lands in, what to watch>
````

Every placeholder gets filled. A box you cannot write a pass predicate for is not scoped
yet.

## Record decisions

A decision is a choice a later agent could undo by accident. Write one when:

- **the user corrects you** ("use an object param, not positional args"). Write it before
  you continue the work.
- the user answers an open question or picks an option.
- you make a non-obvious call that shapes code beyond one file (WebSocket over HTTP, one
  error class for client and server).

Skip it for local choices that the code alone explains.

**One file per topic:** `plans/decisions/<topic>.md`, kebab-case, named by topic. No dates
or numbers in the name (parallel sessions pick the same number) and no index file (every
change would edit it, and parallel sessions conflict).

```markdown
# Object params for public functions (human)

- User, 2026-10-20: "use an object with named args, not a list of arguments".
- Every exported function with 2+ params takes one object: `createClient({ url, token })`.
- Why: call sites read without checking the signature; adding an option is not breaking.
- Lost: short positional calls like `createClient(url, token)`.
- Open: none.
- Lives in: `src/client.ts`, `src/server.ts`.
```

- **Title marker says who decided.** `(human)`: the user decided. Never reverse it without
  asking. `(human asked)`: the user set the outcome, the agent chose the details. The
  details can change. `(agent)`: a judgement call, open to revision with a good reason.
  An `(agent)` bullet inside a `(human)` file marks one agent detail.
- **Quote the user verbatim** with the date. Write "User", never their name.
- **Why, Lost, Open, Lives in** are short bullets. Lost names the alternatives given up.
  Lives in names the files that implement it, so a refactor finds them.
- **Show code** when the decision is about API shape.
- **Changing a decision edits its file. Reversing one rewrites or deletes it.** Do not
  keep superseded text. Git holds the history: `git log -p -- plans/decisions/<topic>.md`.
- **Commit the decision with the code** that implements it.

Precedence: **decisions > plan > memory.** Before designing or refactoring, search them:
`rg -n '<topic>' plans/decisions/`. If the work shows a decision is wrong (too slow, awkward
API), do not silently diverge. Show the evidence (benchmark, code sample) and ask, then
edit the decision file.

## Execute a task

Each session starts with pickup:

1. Read the plan file, the decision files its Appendix B links, `git log` since the plan
   was written, and `git status`.
2. Name the resume point: the first task with unchecked boxes whose dependencies are done.
   Do not redo checked boxes. The plan is authoritative.
3. Re-check inherited claims only on the real artifact, never by trusting a prior summary.

Then work the task:

- Verify each box before starting the next. Check it and write the evidence inline.
- If reality contradicts the plan, edit the plan first (task, order, or a new task), then
  continue. The plan file is the single source of state.
- When the user corrects you, write or edit the decision file first, then update the plan
  tasks it affects, then continue.
- Commit at the end of each task so the next session starts clean.

## Run tasks in parallel

- Only tasks with no dependency between them and no shared files run in parallel.
- Give each parallel session its own worktree or branch. One writer per file.
- One coordinator owns the plan file. Parallel sessions report back (status, what they ran,
  evidence, deviations). The coordinator checks the boxes after reviewing the real output.
- Each session brief stands alone: the plan path, the task id, and "do only this task".
  In Kimaki:

```bash
kimaki send --channel <channel_id> --prompt 'Read plans/<slug>.md. Do only Task 3. Report evidence for each box.' --agent <agent> --wait
```

## Stop mid-task

On pause, user going offline, or a context window close to full:

1. Finish or back out of the current box. Start nothing new.
2. Commit as one `wip:` commit. If the tree is broken, say so in the commit body.
3. Fill the task's **Progress** field: what is done, what is verified, the next step, key
   files, gotchas.

The next session resumes from the plan, not from chat history. In Kimaki, read the old
session only if the plan is missing context: `kimaki session read <id> > ./tmp/s.md`.

## Finish

1. Every box is checked with evidence.
2. Run the whole-goal check from **Done** on the real artifact.
3. Move any durable knowledge (architecture, gotchas) into code comments, `docs/*.md` or
   AGENTS.md. Check every decision file the plan made: Lives in paths are correct and
   Open bullets are still true.
4. Delete the plan file and remove the `Active plan:` line from AGENTS.md. Keep
   `plans/decisions/` and the `Decisions:` line.

If the plan is dropped instead, archive it (see **Write the plan**) and remove the
`Active plan:` line too. Decisions it made stay unless the user reverses them.
