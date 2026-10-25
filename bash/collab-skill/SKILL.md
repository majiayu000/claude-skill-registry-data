---
name: collab
description: Autonomous implementer/reviewer loop between two coding agents (e.g. Claude Code and Codex CLI) coordinated through the shared `collab` CLI in ~/.collab. Use when the user says "collab implement", "collab review", "collab 1" (implementer) or "collab 0" (reviewer).
---

# collab — autonomous implementer ⇄ reviewer loop

Two agents, running in separate terminals, share one task through the `collab` CLI:
one **implements**, the other **reviews**, and they hand off turns until the reviewer
approves. A request can take several tasks (e.g. the stages of a plan): the pair works through
all of them without the user restarting anything.

**The loop only stops when:**
1. there is a real fault: an agent stops responding, or the CLI fails in a way a retry doesn't fix;
2. everything the user asked for is done (the implementer runs `collab end`);
3. a task is escalated: something outside the task blocks it (see *Escalation*), or the user
   chose *stop* when the round limit (default 4) was reached.

A question only the user can answer is not a stop: ask it with `decide` (see *Decisions for
the user*) and carry on once they pick an option.

## Pick your role

Read the argument from the user's message:

| Argument               | Role            |
|------------------------|-----------------|
| `implement`, `1`       | **implementer** |
| `review`, `0`          | **reviewer**    |

Anything after the role (e.g. `collab implement add dark mode to the tarot app`) is the
task for the implementer. For the reviewer, a task id after the role (e.g.
`collab review dark-mode-20260926-120000`, as `init` prints it) pairs you with that task: join it
with `collab -t <task-id> join`. If the role is missing, ask the user once, then continue on your own.

If you are the implementer and no task was given, first run `collab queue next` from the project
directory. If it shows a queued task, take it (see *Queued tasks*). If the queue is empty
(exit 15), reply only with "Collab implementer ready, what should I build?" and end your turn.
Treat the user's next message as the task and start the implementer loop from step 1.

**Task options** can come with the request, e.g. `/collab implement --plan --check "npm test" add
dark mode`. Pass them straight to `collab init`:

| Option | Meaning |
|---|---|
| `--plan` | the reviewer approves a plan before any code (see *Plan phase*) |
| `--max-rounds N` | review rounds before the user is asked how to go on |
| `--check "CMD"` | must pass before every handoff; `collab submit` runs it |
| `--scope "GLOBS"` | files the task may change (comma-separated); `collab diff` flags the rest |
| `--focus "TEXT"` | what the reviewer should look at hardest |
| `--branch NAME` | work on this branch |
| `--commit` | commit the task's changes when it's DONE (never push) |
| `--phone` | push the moments that need the user to their phone; later tasks of the run keep it |

`collab init` adds a *Task options* section to the brief, so the reviewer sees them too.

## The CLI

`collab` is on PATH. If it isn't, run `node <this skill's folder>/bin/collab.js` instead (the folder that
contains this SKILL.md; its name may be `Collab` or `collab`). Run `collab help` for details.

- **Pin your task:** once `collab init` (implementer) or `collab join` (reviewer) prints the
  task id, pass `-t <task-id>` as the first argument on **every** later call, e.g.
  `collab -t dark-mode-20260926-120000 wait reviewer`. That way a second collab pair started
  elsewhere can never redirect you to its task.
- **Passing messages** (brief, summary, review), depending on your shell:
  - *bash / zsh / Git Bash:* a quoted heredoc on stdin:
    `collab -t <id> submit implementer ready <<'EOF' … EOF`
  - *PowerShell (e.g. Codex on Windows):* prefer **`--file`**. Write the message to a file in
    the scratch folder (see *Files you write*), then run
    `collab -t <id> submit implementer ready --file "<scratch>\msg.md"`. Reuse the same name each
    time; collab keeps its own copy of every message.
    Windows PowerShell 5.1 mangles non-ASCII text piped into programs; in PowerShell 7, piping
    a single-quoted here-string (`@' … '@ | collab …`) also works.
  - `init` and `note` accept `--file` too.
- In PowerShell, read a command's exit code from `$LASTEXITCODE`.
- Exit codes: `0` = OK / your turn, `10` = task finished (DONE, ESCALATED, ABORTED, STALLED),
  `11` = wait timed out and it's still not your turn (just run the same command again),
  `12` = submit refused because a note for you (from the user, or from the other agent) is not
  acknowledged as `Note #N` in your message (see *Notes*),
  `13` = the other agent looks unresponsive (see below),
  `14` = submit refused because the task's `--check` failed, `15` = the queue is empty,
  `16` = the user has to choose and you present it: the other agent asked, or (implementer only)
  the round limit was reached (see *Decisions for the user*), `17` = the project files changed
  since the review (a refused `approve`) or since the approval (`collab verify`), `1` = error.
  For `join --after`, `10` also means the implementer ended the run.
- **Start both agents from the same project folder** when you can. A folder and the folders
  inside it count as one project (e.g. a repo root and a module in it), so tasks and the queue
  are still shared if they differ. But `--check` runs, and `collab diff` paths are shown,
  relative to the folder the task was started from.
- If a submit fails with "task already finished", the user stopped the task: stop looping and
  give them a short report of where you were.

## Files you write

- **Handoff-only files** (message drafts, notes to yourself, command logs) go in the **scratch
  folder**: `init` and `join` print it as `scratch:`, and `collab scratch` prints it any time
  (before `init`, it is a shared drafts folder; use that one for the brief). **Never** put them in
  the project (not even in a plans or docs folder) or in the system temp folder. Collab already
  keeps every brief, summary and review in the task's log, and deletes the scratch folder with
  the task.
- **Deliverable documents** (a plan, an investigation, a verification checklist) are part of
  the work. They go where the brief's `## Deliverables` line says, and nowhere else.

## Project lessons (either role)

A brief may have a *Project lessons* section: things learned in earlier tasks of this project.
Follow them. The user's current instructions and the project's own rules (CLAUDE.md / AGENTS.md)
come first: if a lesson contradicts them or is clearly obsolete, say so with evidence (implementer:
in your summary; reviewer: as a non-blocking item or under `## For the user`) instead of following it.

To record a lesson, add a `## Lessons` section with one bullet each to any `submit` message.
Only for something a *future* task in this project would get wrong without being told: a
convention, a recurring mistake, a non-obvious project fact. Not one-off bugs, and not what
CLAUDE.md / AGENTS.md already say. Usually none; at most 1–2 per task, each under 300 characters.
Collab keeps them in the project's `.collab/lessons.md`. It belongs to the project: commit it with
the task's changes when you commit, but never edit it to record a lesson.

## The other agent looks unresponsive (exit 13)

`wait` returns 13 when the other agent has not handed off for 30 min. While the implementer is
working, it also needs no project file to have changed for 10 min. `join --after` returns 13 when
the implementer has neither started a new task nor ended the run for 30 min. The user already
got a desktop notification.
- **Claude Code:** use the AskUserQuestion tool: "The <other role> has not handed off for
  N min. Stop the task?", with the options **Keep waiting (30 min)** and **Stop the task**.
  On *keep waiting*, run `collab -t <id> snooze 30` (or the minutes the user gives), then go back
  to waiting. On *stop*, run `collab -t <id> abort` (skip this after `join --after`: that task
  is already finished) and give the user a short final report.
- **Codex CLI:** **don't end your turn.** If you ended it, the other agent's handoff would go
  unnoticed until the user spoke to you again. Instead, post a short message: "The <other role>
  has not handed off for N min. I'll keep waiting; interrupt me and say *stop* to end the task."
  Then run `collab -t <id> snooze 30` and go back to waiting. After 2 hours without a handoff, the
  task ends by itself (`STALLED`).

## Notes (the user steering a running task, or the other agent mid-turn)

The user can add a note at any time with `collab note "…"`. Notes show up as
`!!! HUMAN NOTE` entries in your `wait` or `progress` output, or in a refused submit (exit 12).
- A human note **takes priority** over the brief and over the other agent's feedback.
- **Acknowledge every note addressed to you in your next handoff**, as a line `Note #N — what you
  did` (implementer: under `## Review responses`; reviewer: anywhere in the review). The CLI
  refuses a submit (exit 12) that leaves a note for you unacknowledged, even one you were already
  shown: output you discarded (e.g. a `progress` call piped to `/dev/null`) never loses a note.
  A `decide` or `escalate` is never refused for notes; the notes stay pending for your next handoff.
- Implementer: act on it. Reviewer: take it into account, and check that the implementer followed
  earlier notes.
- On exit 12, nothing was submitted. Handle the listed notes, then submit again with your **full,
  updated** message (not just a diff of it).

**Never post a note as the user.** To flag something to the other agent outside a handoff (e.g. a
reviewer's early finding while the implementer is still working), use
`collab -t <id> note --from <your role> "…"`. It goes to the other agent, shown as
`>>> NOTE FROM THE OTHER AGENT` (not from the user), and it must be acknowledged like any note.
A plain `collab note` from an agent's shell is refused. Prefer putting findings in your handoff;
use `--from` only when waiting would waste the other agent's work.

## Progress updates while it's your turn

While you hold the turn, post a one-line status at each real step, so the user (in `collab watch`)
and the waiting agent can see that the pause is normal:

```
collab -t <id> progress "reading the review, 3 items to address"
collab -t <id> progress "running npm test"
collab -t <id> progress "fixing item 2: missing null check in parser.ts"
```

- Post one when your turn starts, before anything long (tests, builds, large reads), and when you
  move to the next item. Typically 3–8 per turn. **Never on a timer**, and never in a loop.
- Keep it short and concrete (under ~80 characters): *what* you're doing, not how you feel.
- It isn't a handoff: it doesn't pass the turn or add a timeline entry. It does count as a sign
  of life, so a long but active turn won't be flagged as unresponsive.
- If its output shows a note (`!!! HUMAN NOTE` or `>>> NOTE FROM THE OTHER AGENT`), handle it like
  any other note and acknowledge it in your next handoff (see *Notes*). Don't send progress output
  to `/dev/null` if you can avoid it: that is where mid-turn notes arrive.
- When `wait` times out (exit 11), its output includes the other agent's latest progress. A
  recent update means the wait is normal, so just keep waiting.

## How to wait (depends on which CLI you are)

Waiting is a blocking shell command, so polling doesn't use model tokens. **Never end your
turn while you are in the loop**, and that includes the reviewer waiting in `collab join` for a
task that doesn't exist yet. Exit 11 from `wait` or `join` only means "not yet": run the same
command again. Keep waiting until you see exit 10 (or 13 or 16, see above). If the user wants
you to stop, they will interrupt you.

- **Claude Code:** run `collab wait <role> --timeout 3300` (or `collab join --timeout 3300`)
  with the Bash tool's `run_in_background: true`. You are re-invoked when it exits. Read its
  output, then act on the exit code.
- **Codex CLI:** run `collab wait <role> --timeout 540` (or `collab join --timeout 540`) in the
  foreground with a shell timeout of at least 600000 ms. On exit 11, run it again immediately.
  Don't stop to ask the user and don't end your turn.
- **If the shell tool stops the command before it exits** (a tool timeout, "command timed out",
  an interrupted or killed process, no exit code), that is not an error in the task. Run the same
  command again, with a `--timeout` below the shell tool's limit (e.g. `--timeout 240` for a
  5-minute limit). The same goes for any exit code other than 0, 10, 13, 16 and the ones listed for
  `submit`: check `collab -t <id> status`, then go back to waiting.

## Implementer loop

1. **Start the task.** Turn the user's request into a brief, then run
   `collab init <short-slug> [--plan] [--max-rounds N]` from the project directory:
   ```
   collab init dark-mode <<'EOF'
   ## Goal
   …
   ## Scope / files likely involved
   …
   ## Acceptance criteria
   - …
   ## Constraints
   (project rules, things not to touch)
   ## Deliverables
   (only if the task produces documents) where they go: the project's convention if it has one
   (CLAUDE.md / AGENTS.md, or an existing folder such as `.agents/plans/<slug>/`), otherwise
   `docs/` in the project folder
   EOF
   ```
   The CLI snapshots every git repo under the project (nested ones too), so `collab diff` later
   shows only what changed during this task. Tell the user the task id and the `reviewer:` command
   `init` printed (e.g. `/collab review <task-id>`, Codex: `$collab review <task-id>`), which pairs
   the reviewer with this task even if another pair is running, and that they can watch live with
   `collab watch` and steer with `collab note "…"`.
   If `init` printed a `phone:` line, pass it on too (a `NEW` one means they must subscribe first).
   If the request has several stages (a staged plan, a list of deliverables) or is too big for
   one review, split it now into **all** its parts (see *Splitting a task*), not just the first
   few. Leave stages out only if the user explicitly asked for a subset.
   In plan mode, go through the *Plan phase* first, then continue at step 2.
2. **Implement.** Follow the project's own rules (CLAUDE.md / AGENTS.md: commits, dev servers
   and so on). If the task has a `--branch`, create or switch to it before changing anything.
   Run the relevant lint, type-check or tests yourself before handing off. If the task has a
   check command, `collab check` runs it while you work; don't run it just before `submit`,
   which runs it again.
3. **Hand off** with `collab submit implementer ready`, using this summary:
   ```
   ## Summary
   what changed and why (2–5 bullets); what the reviewer should check
   ## Files changed
   - path — what changed
   ## Closeout
   Verified: what you checked and how: commands run and their results
   Attempted, blocked: what you tried but couldn't finish, and why (or "none")
   Deferred: what you consciously left for later, and where it is recorded (or "none")
   Not claimed: what this work does not vouch for (or "none")
   ## Review responses          (from round 2 on)
   1. Fixed — …
   2. Declined — reason …
   ## Divergence from plan      (--plan tasks only, when the build departs from the approved plan)
   - what differs from the plan, and why
   ## Decisions taken           (only for judgment calls you made yourself, see *Escalation*)
   - what you chose, the alternatives, and why it is the safe choice
   ```
   `## Closeout` is required, with exactly that heading and all four labels (the CLI refuses a
   `ready` without them; write "none" where nothing applies). Only put under `Verified` what you
   actually ran or checked in this turn.
   **Exit 14** means the task's check failed and nothing was submitted: fix the problem and submit
   again. If the check can't pass for reasons outside the task, escalate.
4. **Wait** with `collab wait implementer`. On exit 0 the output is the reviewer's feedback.
   Address every numbered item, either by fixing it or by declining with a reason, then go back to step 3.
5. On **exit 10**:
   - **DONE:** if the task has `--commit`, first run `collab -t <id> verify`. Only on **exit 0**,
     commit the task's changes (in each repo you changed, on the current branch, with a message
     summarising the task; never push). On exit 17 (files changed after the approval) or 1 (no
     approved tree recorded), don't commit: tell the user, then carry on. Post a one-line status as
     plain text (**don't end your turn**), then run `collab queue next`. If it shows a task, start
     it (see *Queued tasks*) and continue the loop. If the queue is empty (exit 15), check the
     user's original request (and any plan it points to). If some of it is still not done, start
     the next part with `collab init` and continue. Only when **all** of it is done, run
     `collab -t <id> end` with a final report on stdin or `--file`:
     ```
     ## Final report
     what was delivered, task by task; anything left for the user (manual steps, follow-ups)
     ```
     The CLI appends each task's last *Closeout*, the reviewer's *For the user* briefings, every
     answer the user gave and every *Decisions taken* section of the run, and stops the reviewer.
     Then stop, and give the user that report (`collab -t <id> show`), all of it included.
   - **ESCALATED, STALLED or ABORTED:** stop. Give the user a short report and explain what needs
     a decision. **Don't start queued tasks**: the queue waits until the user runs
     `/collab implement` again.

## Queued tasks

The user can queue tasks ahead of time with `collab queue add "…"`. Each queued task belongs to
the project folder it was added from. `collab queue next` shows the first one for the current
folder, with its options.

1. If the output says **CONFIRM FIRST**, ask the user before starting: start, skip, or stop.
   If it also says **HELD**, an earlier part of the same split task didn't get approved. Say so
   in your question.
   (Claude Code: AskUserQuestion; Codex: plain text, then end your turn.) *Skip* runs
   `collab queue skip` and moves on to the next one. *Stop* leaves it queued for later: if the
   last task was approved, run `collab end` as in step 5 of the implementer loop (it lists the
   task under *Left in the queue*), then stop.
2. Turn the task text into a brief as usual, then start it with
   `collab init <short-slug> --from-queue` (brief on stdin or `--file`). This removes the task
   from the queue and applies its options. Pin the new task id with `-t`. For a CONFIRM FIRST
   task, add `--confirmed "<the user's answer>"`. The CLI refuses without it, and records the
   answer in the task's timeline.
3. Tell the user which queued task you started and how many are left, then continue the
   implementer loop from step 2 (or the *Plan phase*).

## Splitting a task (implementer)

Use `collab queue split` when a task from the user is too big to review well in one pass, for
example when it has several independent changes, a refactor followed by a feature on top of it,
or a plan with stages. Split it into every part the request covers, so the pair can work through
all of them. Don't split small tasks. Each part must be something the reviewer can approve on its own, and
it must leave the project working.

Split **right after `collab init`**, before your first `plan` or `ready`. The CLI refuses later
on, refuses to split twice, and refuses to split a task that is already a part. Always use
`queue split`, never a series of `queue add` calls: it keeps the parts in order, at the front of
the queue, with the task's options (`--check`, `--scope`, `--branch`, `--commit`, …).

```
collab -t <id> queue split --reason "3 independent changes; easier to review one by one" <<'EOF'
Part 1: what this task now covers, and its acceptance criteria
=== part ===
Part 2: goal, scope and acceptance criteria, written so it can be started on its own
=== part ===
Part 3: …
EOF
```

- Part 1 stays the current task. The CLI adds a `split` entry to its timeline, so the
  reviewer sees that only part 1 is in scope.
- Parts 2..N are queued next for this project. Each will be its own task with its own review,
  and its brief says which part it is. You start them later through *Queued tasks*, as usual.
- Work you find later (a stage you missed, a follow-up the review uncovered) goes in with
  `collab queue add --first [options] "…"`, repeating the task options it needs.
- Tell the user how you split the work (one line per part). They can edit the queue with
  `collab queue rm` / `move`.
- In plan mode, split before submitting the plan, and make the plan cover part 1 only.

## Plan phase (only for tasks started with `--plan`)

- **Implementer:** explore the code without changing any project files, then run
  `collab submit implementer plan`:
  ```
  ## Approach
  the chosen design and why; alternatives considered
  ## Steps
  1. path — change
  ## Risks / open questions
  ## How it will be verified
  ```
  Then wait. If you get `PLAN_CHANGES`, revise the plan and submit it again with `plan`. A
  `plan` or `ready` identical to your previous one is refused (exit 1, nothing written): it
  usually means writing the message file failed, so write it again before resubmitting.
  Once the status is `IMPLEMENTING`, the plan is approved and you start coding (step 2).
- **Reviewer:** when the status is `PLAN_REVIEW`, judge the plan against the brief and the
  codebase: whether it's the right approach, fits existing patterns, misses a step, carries a
  risk, or is over-engineered. If the implementer split the task, judge the split too. From
  the second plan on, `wait` usually shows only the changes since the plan you reviewed; read
  the whole one with `collab show N` if you no longer have the earlier plan in mind. Use
  `changes` (numbered items) or `approve`. In this phase,
  `approve` starts the implementation; it does **not** end the task.

## Reviewer loop

1. **Join** with `collab -t <task-id> join` if you were given a task id, else `collab join` (it
   only looks at the project of the folder you're in). It blocks until an active task exists,
   then prints the brief. The implementer may take several minutes to write the brief. On exit 11,
   run the same `join` again, as many times as it takes (see *How to wait*). Never end your turn
   with "no active task".
   **Exit 1 with "already has a reviewer"** means another reviewer is working on that task (often
   another pair's), and **"several projects"** means your folder matches more than one active
   task. Don't pick one yourself: stop, show the user the message, and let them restart you with
   the right task id or folder. Use `join --force` only when the user says the earlier reviewer
   of that task is gone.
2. **Wait** with `collab wait reviewer`.
3. **Review** (on exit 0):
   - Treat the implementer's summary as a guide, not proof. Run `collab diff --stat`, then
     `collab diff` (or read the files) to see the real changes. From round 2 on, start with
     `collab diff --since-review` (only what changed since your last review) and open the full
     diff where the new changes touch earlier code. Lockfile patches are left out and binary
     files shown as a size: `collab diff --all` includes lockfiles.
   - Check the summary's `## Closeout`: anything under `Verified` that wasn't actually run or
     checked (a test claimed to pass that doesn't, a check that never ran) is a blocking item.
   - From round 2 on, `wait` recaps the `[blocking]` items of your earlier reviews. Check that
     each one is resolved in intent, not just in wording, and raise it again if it isn't.
   - `wait` also lists the notes you sent since your last review, each with the implementer's
     `Note #N` line. Check each fix in the code, not just the acknowledgement; an unfixed or
     wrongly declined note is a blocking item.
   - In a `--plan` task, `wait` names the approved plan entry (`collab show N`). Review the build
     against it too. A substantive divergence the summary doesn't declare under
     `## Divergence from plan` is blocking; a declared one is judged on its merits.
   - Check them against the brief's acceptance criteria. Look for correctness, edge cases,
     regressions, security, and consistency with the surrounding code and project conventions.
   - You can run read-only checks (lint, type-check, tests). **Don't edit project files**;
     your only output is the review.
   - Stay within the brief's scope. Don't ask for unrelated refactors.
   - A new document outside the brief's `## Deliverables` location, or a handoff draft (brief,
     summary, review copy) written into the project, is a blocking item: it belongs in the
     scratch folder (see *Files you write*).
   - Breaking an applicable *Project lesson* from the brief is a blocking item (see *Project lessons*).
   - Respect the brief's *Task options*. Look hardest at the **review focus**. If `collab diff`
     shows `⚠ OUTSIDE SCOPE`, treat it as blocking unless the change is clearly required. A
     `check passed` line in the summary means the check command succeeded; you can run
     `collab check` yourself too.
   - If the task was split (a `split` entry, or a *Part of a split task* section in the brief),
     review only this part. Don't flag work that belongs to the other parts as missing. If the
     split itself is wrong (a part can't stand on its own, or leaves the project broken), say
     so as a blocking item.
   - If the status is `PLAN_REVIEW`, follow the *Plan phase* rules instead.
4. **Decide:**
   - Blocking issues found → `collab submit reviewer changes`:
     ```
     ## Verdict: changes requested
     1. [blocking] path:line — problem → what to do
     2. [should-fix] …
     ## Nits (optional, non-blocking)
     ## Decisions taken (only for judgment calls you made yourself, see *Escalation*)
     ```
     Then go back to step 2.
   - Nothing blocking → `collab submit reviewer approve` with a short verdict and any nits.
     In the build phase, this ends the task for both agents. There, add a short `## For the user`
     section: the riskiest changes, invariants worth protecting, and what to try to break by hand.
     `collab end` passes it on to the user.
   - The CLI refuses (exit 1) an `approve` that contains a numbered `[blocking]` item, and a
     `changes` without numbered items. Don't restate resolved items as `[blocking]` in an approve.
   - An `approve` covers the files as they were at the implementer's handoff. If they changed
     since (exit 17, the files are listed), look at the listed files. If your review still holds,
     run `collab -t <id> submit reviewer approve --rereviewed` (it covers the files as they were
     when the approve was refused); if the changes matter, submit `changes`. Your own test runs
     can cause this when they leave files behind that git doesn't ignore.
5. On **exit 10** (from `wait`, or from your own `approve`):
   - If the status is **DONE**, the implementer may have more tasks to do. Run
     `collab join --after <id>` (without `-t`; `<id>` is the task that just finished) and wait as
     in *How to wait*:
     - **exit 0:** a new task started. Pin its new id and go to step 2.
     - **exit 10:** with `WORK COMPLETE`, the implementer ended the run; with `TASK FINISHED`, a
       later task ended without approval. Either way, stop and give the user a short final report.
     - **exit 13:** the implementer hasn't started anything new for a long time. Handle it as in
       *The other agent looks unresponsive*, snoozing the task that `join` names.
     - **exit 11:** run the same `join --after` again.
   - Otherwise (ESCALATED, STALLED, ABORTED) stop looping and give the user a short final report.

## Decisions for the user (either role)

When a choice belongs to the user (product behaviour, a trade-off they would want a say in, an
ambiguous requirement), **ask right away** with `decide`. Don't spend review rounds on it. The
task pauses (`DECISION`) and continues as soon as the user picks an option.

1. Write the question with 2–4 numbered options, the recommended one first and marked
   `(Recommended)`, each with its consequence:
   ```
   ## Strip the base snapshot from incidental prompts?
   Context in 2–4 lines: what is at stake, what you found.
   1. Strip it from incidental prompts (Recommended) — nothing stale to drop, replies keep flowing
   2. Keep it and drop stale replies — strictly factual, but some replies vanish
   3. Keep it, check only match/audience/age — rare stale mentions
   ```
2. Submit it with `collab -t <id> submit <role> decide`:
   - **Claude Code:** add `--self`, then ask the user yourself with AskUserQuestion (the options
     from your message; the context goes in the question). Record the answer with
     `collab -t <id> answer <N>` (or `answer "<their own words>"`). The turn is yours again:
     carry on.
   - **Codex CLI:** without `--self`. Then run `collab -t <id> wait <role>` as usual. It returns
     (exit 0) with the user's answer once they have chosen.
3. **Exit 16 from `wait`** means the user has to choose and **you** present it: the other agent
   asked (without `--self`), or you are the implementer and the round limit was reached (see
   *Escalation*). Claude Code: ask the user with AskUserQuestion as in
   step 2, run `collab -t <id> answer …`, then go back to waiting. Codex: post the question and
   options as plain text, tell the user to answer with `collab answer <N>` in any terminal, and
   go back to waiting (**don't end your turn**). If `answer` says no decision is pending, the
   user already answered elsewhere: just go back to waiting.

**One agent presents each decision**, so the user answers in one place: the asker with `--self`,
the implementer for the round limit, otherwise the agent whose `wait` returned 16. If you are not
that agent, **never ask the user about it** (no AskUserQuestion, no plain-text question, no relay):
keep running `wait` until it returns with the answer. If the user mentions the decision in your
thread anyway, tell them to answer it where it was presented or with `collab answer <N | text>`.

The user's answer takes priority, like a human note.

## Escalation (either role)

Don't escalate a disagreement or a technical judgment call. Keep reviewing. If the reviewer
still requests changes once the round limit (default 4) is reached, the CLI asks the user
through the implementer (its `wait` returns 16; the reviewer just keeps waiting): 2 more rounds,
approve as it is, or stop. The task continues with their choice. For a technical choice you can make yourself, pick the safest option (or the one the codebase already
leans towards), carry on, and note it under `## Decisions taken` in your summary or review. The
final report lists these for the user.

Use `collab submit <role> escalate` only when the task **cannot** continue: something outside its
scope is broken, access or credentials are missing, or the next step is destructive or
irreversible and the user hasn't approved it. Give a clear question. After escalating, stop and
report to the user.

## Human controls

- `collab watch`: interactive dashboard: ↑↓ steps in full, ←→ earlier tasks, live progress, timers
- `collab note "…"`: steer a running task (add `--implementer` or `--reviewer` to target one agent).
  Agents use `collab note --from <their role> "…"` (see *Notes*); every note must be acknowledged
  as `Note #N` in the target's next handoff.
- `collab answer <N | text>`: answer a pending decision
- `collab status`, `collab log`, `collab list`, `collab abort` (stops both loops)
- `collab snooze [MIN]`: keep waiting on a slow agent; `collab clean`: delete finished tasks
- `collab queue add [options] "…"`, `collab queue`, `collab queue rm N`: manage the task queue
- `collab queue split [--reason TEXT]`: implementer only, split the current task (see *Splitting a task*)
- `collab lessons [add "…" | rm N]`: the project's lessons; `collab phone [set … | test]`: where `--phone` pushes go
State lives in `~/.collab/tasks/<task-id>/` (`state.json`, `log.md`, `entries/`).
