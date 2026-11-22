---
name: hill-climb
description: Reach any goal that a command can score (faster, fewer bugs, an audit, "make X stable", a port, a UI, a text) in small steps, keeping wins and undoing losses, across one or many repos. Use for "hill climb", "/hill-climb", "climb this", "keep going until it passes", or to resume or report on a climb.
---

# Hill climb

You work toward a goal in many small steps. A check scores each step with no
human in the loop. `scripts/climb.py` keeps the score: you edit code, it runs
the check, commits a win or undoes a loss, and writes the log. Never write a
score down yourself, and never decide a step "basically" passed.

Any goal fits, because every goal becomes the same thing: a command that
prints a number. Faster is a time or a count. "Audit billing" or "make
roles stable" is the number of failing tests, one test per finding. A port
is the number of outputs that match. A UI is a judge's score. Pick the
number, and the rest of this skill is the same for every goal.

What the script gives you that working without it does not:

- **No lost wins and no silent breaks.** Every kept step passed the check
  and the guards. Every failed idea is undone in every repo, so the branch
  only holds proven steps.
- **A score you can't fool.** The check is locked, so no step can weaken a
  test to pass. The report quotes measured numbers, not your opinion.
- **It survives compaction and restarts.** The card, the log, the notes,
  and the last check output are on disk. `status` shows them in one call.
- **The next climb starts faster.** `init` saves the check as a kit that
  any repo can reuse.

It adds seconds a step, not minutes: `try` runs the check you would run
anyway. Never skip it because a goal "feels too open" or spans repos. Both
fit, as shown in step 2.

**Small goal? Read only this.** For a goal you can finish in under an hour:

1. Write the check before `init`, and the reference it compares with:
   - Fix or audit: tests that fail today, from the spec or the bug report.
     Score with `--score '<failure count regex>' --direction min --target 0`.
     Guard with the tests that pass today, kept in their own files, so a
     fix can't break old behavior and a crash can't pass as fewer failures.
   - Faster or smaller: a script that times or counts the work on fresh
     random input. Copy the old code as the reference, and add a guard that
     compares the new output with it. Score with `--direction min --target
     <N>x --runs 3`, and add `--paired` when it is a timer.
   - Anything else: whatever prints how close you are as a number.
2. `init <name> --goal "..." --check "<command>" --lock <check files>`.
   `init` commits the new check files as the first step on the climb
   branch. Add a `--check` and a `--repo` for each other repo the work
   touches.
3. Change, `try`, repeat. Review the whole diff yourself. Then the report.

Skip the card, helpers, and holdout when the goal is this small. Use the
rest of this file when the goal is big, slow, or noisy.

Your order of work:

1. Know the goal.
2. Build a check that scores it with no human. This matters most.
3. Get the tools, compute, and reference material the climb needs.
4. When progress slows, find what slows it and fix that.

I start a climb and leave. I don't read the thread while it works. I come
back when it asks me something or when it is done. Work for that:

- Don't stop to give updates. The only messages I read are the card, a
  question I must answer, and the report.
- Ask with the harness's question tool (`AskUserQuestion` in Claude Code,
  `request_user_input` in Codex), so the thread shows it needs me. Without
  one, end the turn with the question.
- Keep the state on disk (`status`, `notes.md`), not in chat.

Wall-clock time is the cost I care about. Finish as fast as the goal
allows: a small goal in minutes, a hard one in as many hours as it keeps
gaining. A climb ends when the bar is met or the gains stop, not on a
clock. Where the time goes, in order: setup, slow checks, noisy checks,
bars no step can reach, and retrying ideas. Each section below cuts one of
them.

- **Never wait with a sleep loop.** Run long commands in the background and
  let the harness wake you when they finish. Plan the next step meanwhile.

`CLIMB` below means the absolute path of `scripts/climb.py` next to this file.
Write the full path into each command, because shell variables may not
survive between calls. Run it from inside the target repo, or any repo of
a multi-repo climb. Every command is
in "Commands" at the end, so you never need to read the script.

The climb gets its own branch. An undone step resets the tree and deletes
untracked files that git doesn't ignore. If someone else works in the same
checkout, climb in a separate worktree.

## 0. Resume or reuse

Run both in one call:

```
python3 "$CLIMB" list; python3 "$CLIMB" kits "<two or three goal words>"
```

- A climb for this goal exists: switch to its branch, run `status <name>`,
  read `.hill-climb/<name>/notes.md`, and go to step 4. "Continue" after a
  crash or a reset means this.
- A kit fits: `python3 "$CLIMB" reuse <kit>` restores its check, guards,
  holdout, and notes, and prints the `init` it used. Edit what differs for
  this goal, run the check once, and go to the card. A kit from another repo
  is a starting point, not a check: make it fail and pass before you trust it.

## 1. Get to a first score fast

A rough check that runs beats a perfect one you are still designing. Aim for
a first real score within 15 minutes and the card within 30. You can sharpen
the check later with `relock`. A realistic rig, like a real server behind a
slow-network proxy, is worth building only as the holdout; the per-step
check stays small.

- **Read in bulk.** One command that greps or prints ten files beats ten
  calls. If you can start subagents, send read-only explorers in
  parallel, one per area: the code path, the tests and harnesses, the setup. Build
  the check while they read.
- **Reuse a harness.** Search for one before you write one: `bench`, `perf`,
  `latency`, `e2e`, `fixture`, `harness`, `mock`. Extending one beats
  writing one.
- **Start slow setup at once, in the background.** Installs, builds, and
  seed data run while you read.
- **Small data.** A small synthetic fixture beats a copy of real data. Copy
  real data only when its shape matters, keep it under 100 MB, and put it
  under `.hill-climb/<name>/data/`, where git ignores it and kits skip it.
- **Profile once.** Before step 1, find where the time or the errors go.
  Attack the biggest part first.

## Helpers

If the harness can start subagents, use them to work in parallel. Pick each
helper's model by the job, from the models the harness offers. Don't
hard-code a name:

| Tier | Example | Use it for |
| --- | --- | --- |
| Fast | the cheapest model, like a Haiku or mini class | Reading code, finding harnesses, summarizing logs |
| Mid | a Sonnet class model | Proposing next ideas from the profile and the log |
| Frontier | the strongest model, like an Opus class | The blocker review and the final review |

- **Only you write in the climb tree.** `try` resets it, so a helper that
  edits it loses its work. A helper may read, or draft a fix in its own
  worktree and return a patch. You apply the patch and run `try`.
- **Run them in the background** while a check runs or setup installs. Don't
  wait on a helper when you have other work.
- **Brief them tight:** the goal, the files, and the answer shape, like
  "up to 5 ideas, each with file:line and an expected gain, under 200 words".
  Ask for conclusions, not file dumps.
- **Use as many as help.** Start one per independent question, all at once.
  Use the cheapest tier that can answer it. Don't start a helper for
  something two of your own tool calls can do.
- No subagents in this harness: do the same work inline.

Good moments for helpers:

- **Setup:** fast explorers map the code path, the tests, and any harness
  while you start the install.
- **Each long check:** mid helpers read the log, `notes.md`, and the profile,
  each from a different angle, and return the next ideas ranked by expected
  gain.
- **PLATEAU:** frontier helpers do the blocker review with a fresh view.
- **Before the report:** frontier helpers review the whole branch diff, for
  example one for correctness and one for what the change could break (see
  "Keep everything working").

## 2. Build the check

The climb is only as good as its check. A check that measures the wrong thing
spends the whole budget making the wrong thing better. For example, a judge
that compares against the wrong reference will keep pushing the work toward
that reference.

Ask one question: what would I run to see that the goal is met? Then make
that command print a number. Use the strongest form that fits:

1. **Exact:** outputs match a reference, or tests pass. Count the matches,
   or the failures.
2. **A count of the work:** round trips, queries, bytes, allocations,
   tokens. Steady and fast.
3. **A clock:** only when no count fits. Use `--runs` and `--paired`.
4. **A judge:** `scripts/judge.py` with a rubric, when only taste can tell.

Examples, not a closed list. Recipes are in `references/checks.md`:

| Goal | Score |
| --- | --- |
| Port or clone a tool | Outputs that match the real tool |
| Bug or feature | Failing tests written from the spec, not from your fix |
| Audit, stabilize, "make X work" | Failing tests, one per finding. Add a test for each new finding and `relock` |
| Speed or size | A count of the work behind the time |
| Several goals at once | Progress toward the worst bar |
| Look, feel, writing, API shape | `judge.py` with a rubric and good examples |

Use what the repo already has. `--score '<regex>'` reads the score from
any test runner's output, so you need no wrapper script. It reads the last
line that matches and adds up every number the regex captures on it, so
`'failures=(\d+)|errors=(\d+)'` counts both. A passing run with no match
scores 0. Patterns for common runners are in `references/checks.md`.
Repeat `--check` to run several commands at once, like the backend and the
frontend suites. Their scores add up. Give one `--score` for all of them,
or one per `--check` in the same order.

**Work in several repos?** Add `--repo <path>` for each other checkout the
climb edits. Each gets the same `climb/<name>` branch. `try` keeps or undoes
the step in all of them at once, and `drop` restores all of them. Lock their
check files with a path from this repo, like `--lock ../web/tests/e2e`.

Test the check before you trust it. Run these in one call where you can:

- **It can fail.** Break the code on purpose and see the score get worse.
  Then `git checkout -- <file>`.
- **It can see a win.** If you know a small real improvement, the score must move.
- **It is steady.** Run it 3 to 5 times. If the score drifts with no code
  change, first try to replace the clock with a count. Otherwise init with
  `--runs 3` or more and a `--min-gain` above the drift, and add `--paired`
  when the machine is shared. Use a percent like `--min-gain 3%` when the
  score will shrink a lot.
- **It can't be gamed.** Vary the input on each run (shuffle, reseed, sample)
  and compare against the reference. Add a guard that checks fresh inputs.
  Try one cheat by hand, like hard-coding the answer, and confirm the guard
  catches it. Undo it with `git checkout`, not `try`.
- **It is fast.** You pay every second of check time on every step: a
  40-minute check gets 4 tries in 3 hours, a 1-minute one gets 180. Get a
  step under 2 minutes before the card. Use a sample or a count per step,
  and the full suite or the timed run as a guard or the holdout. Recipes
  are under "Fast checks" in `references/checks.md`. If `init` still warns
  that a step is slow, say why on the card's Budget line.
- **The bar is reachable.** Work out the floor: the best each goal can reach
  with the current design. If a bar sits below its floor, put that in the
  card under "Needs your answer" with a bar you can reach, or the design
  change that would lower the floor.

**Audits and open goals.** Before init, list what the goal covers, as
scenarios in `.hill-climb/<name>/notes.md`. Send helpers to find bugs, one
area each. Write one failing test per real finding, from the spec or the
bug report. The score is the failing count, with a bar of 0. When a step
finds a new bug, add its test and run `relock --why "found <bug>"`. The
score goes up for an honest reason, and the log shows it. A finding that
needs my answer goes in the notes and in the report, not in the score.

Keep a holdout: cases you never train on. Store them under
`.hill-climb/<name>/holdout/` and pass their check as `--holdout`. Don't open
those files again. If the visible score goes up and the holdout doesn't, the
climb is overfitting. Stop and say so.

Lock the check, the guards, the tests, the fixtures, and the holdout with
`--lock`. Lock the test runner's config too (`vitest.config.*`, `jest.config.*`,
`pytest.ini`, `pyproject.toml`), or a step can pass by running fewer tests.
The script refuses to score while a locked file changed. New check
files under a `--lock` path become the first commit on the climb branch.
Anything else uncommitted stops init.

## 3. The card

Send me one message with the card filled in and nothing else to decide. Send
it as Markdown, not in a code block, so it renders. Use this layout:

> ### Climb card: `build-speed`
> **Goal:** cold build of the app 2x faster, same output
>
> | Score | Now | Bar |
> | --- | --- | --- |
> | Median build seconds, lower is better | **47.0s** | **23.5s** (2x) |
>
> | Setting | Recommended | Default | Why |
> | --- | --- | --- | --- |
> | Check | `./scripts/bench-build.sh` | none | Builds from clean, prints seconds |
> | Kit | new | none | No saved kit fits |
> | Runs per score | **3** | 1 | Score drifts 1.2s between runs |
> | Paired | **yes** | no | Shared machine, so old and new run in turns |
> | Min gain | **3%** | 0 | Above the drift, so luck can't win |
> | Guards | `npm test`, `npm run typecheck` | none | Faster must still be correct |
> | Holdout | 3 of the 12 sample apps | none | Catches overfitting |
> | Locked | `scripts/bench-build.sh`, `test/`, `samples/` | none | So no step can edit the check |
> | Timeout | 1800s | 1800s | |
> | Budget | no limit | no limit | About 2 min a step, so 40 steps is about 1.5 hours |
> | After the bar | **stop** | stop | |
> | Branch | `climb/build-speed` | `climb/<name>` | One commit per kept step |
>
> **Needs your answer:** none
>
> Reply **go** to start, or change a line, like "runs 5".

Bold a recommendation that differs from the default. Keep each "Why" to a few
words, and leave it empty when the default is fine. Fill every line with your
best guess. List a line under "Needs your answer" only when I must confirm it.
If I named a goal but no bar, propose one that is ambitious and checkable,
like "2x faster" or "every sample matches".

My reply "go" approves the card, the branch, and the commits on it. Ask for
it with the question tool. If I already approved ahead, like "yolo" or "full
send", don't send the card. Put it at the top of the report, and start at
once. After that, do not ask me anything you
can find out or decide yourself.

If I have no single goal, don't invent one. Ask what I wish existed, and offer
the most tedious useful task you can see in the repo.

Then start it:

```
python3 "$CLIMB" init build-speed --goal "cold build 2x faster" \
  --check ./scripts/bench-build.sh --direction min --target 2x --after stop \
  --runs 3 --paired --min-gain 3% --guard "npm test" --guard "npm run typecheck" \
  --holdout ./scripts/bench-holdout.sh --lock scripts --lock test \
  --lock .hill-climb/build-speed/holdout
```

An audit over a backend and a frontend looks like this:

```
python3 "$CLIMB" init billing-audit --goal "every billing finding fixed" \
  --check "pytest tests/billing -q" --check "cd ../web && npx vitest run billing" \
  --score '(\d+) failed' --direction min --target 0 --repo ../web \
  --guard "cd ../web && npx tsc --noEmit" \
  --lock tests/billing --lock ../web/src/billing/__tests__
```

Set `--max-hours` or `--max-steps` only when I name a limit. Without one,
the climb runs until the bar is met or `status` says STUCK, so a quick
goal ends early and a hard one keeps going while it gains. A limit is soft:
past it, `try` goes on while a step was kept in the last hour and in the
last 5 steps, and stops at the first lull. Add `--hard` only when I say the
limit is strict. The hours count from init. When I change my mind later,
run `budget --hours <more>`, `budget --steps <more>`, or `budget --off`.

Without `--score`, the check's last line of output must be the score as a
bare number. Guards pass by exiting 0. init makes the branch, measures the baseline, refuses to
start if a guard already fails, and saves the check as a kit for next time.

## 4. Climb

Each step is one idea, one change, one `try`:

1. Read `status`, and `.hill-climb/judge-notes.md` if judges are in use.
   Don't retry an idea the log already undid unless you can say what is
   different this time. Try one idea at most twice. If you still believe in
   it after that, the check can't see it: make the check finer and `relock`.
2. Make one change for one reason, and guess its effect. Put the guess in the
   idea, like `"cache the parser (expect -10%)"`. When a guess is far off,
   your model of the code is wrong: profile before the next step.
3. `python3 "$CLIMB" try "<idea>"`. It commits a win or resets the tree.
   It commits exactly the code it scored. A check or guard that edits a
   file breaks the step, so guard with `prettier --check`, not `--write`.
   New files they write, like reports, are never committed.
   Either way, move on. The full check output of the step is in
   `.hill-climb/<name>/last.txt`, and of the best step in `best.txt`. Read
   it there instead of running the check again.
4. While a long check runs, don't edit the tree. Read code and plan the next
   step. Run `try` in the background if the harness allows it, and wait for
   its finish notice, not a sleep loop. Only one command that changes the
   climb runs at a time. If one says another is still running, wait for it:
   an interrupted command can still be running.
5. Every 5 steps, update `.hill-climb/<name>/notes.md` in a few lines: what
   works, what doesn't, what to try next. A new session resumes from it.

Every 10 kept steps, look at the real thing yourself. Open the app, read the
output, view the screenshot. The score only stands in for what I want. If the
two drift apart, fix the check with `relock --why "..."`. Never edit a locked
file to make a step pass.

### Never cheat the check

These raise the score and make the work worse. Each one is a failed climb,
even if `try` keeps it:

- Special-casing the exact inputs the check uses.
- Hard-coding or caching expected outputs.
- Skipping, weakening, or deleting tests, or catching and hiding errors.
- Making the benchmark do less work instead of making the code faster.
- Leaving files or processes behind that slow the other side of a paired run.
- Reading the holdout.

A real win makes the same code faster or better on inputs the check has never
seen. If the only way forward is one of these, the check is wrong. Say so.

### Keep everything working

Undone steps never land, so a failed idea can't break anything. The risk is a
kept step that breaks something no guard checks. Close that gap:

- **Guard what people rely on.** Before init, list what the code you will
  change touches: callers, other platforms, saved data, public APIs. Every
  item needs a guard: the affected tests, typecheck, lint, the build. Keep
  per-step guards fast and put the slow full suite in the milestone check.
- **Milestone check.** Every 10 kept steps and at the bar, run the full test
  suite and the holdout. If something broke, find the step with
  `git bisect run <the failing command>` on the climb branch.
- **Fix forward.** Fix a break with `try --fix "<what broke>"`. It keeps a
  change that holds the score, so a repair is not undone for having no gain.
  If the only fix gives up that step's gain, `git revert` the step's commit
  and run `relock --why "reverted step N: broke X"` to measure the new best.
- **Final review.** Before the report, review `git diff <start>..HEAD` as a
  whole, or have a frontier helper do it with a fresh context. Look for
  removed tests, swallowed errors, a feature turned off, a changed default,
  and data or API changes. Fix what you find with `try --fix`. Fixes made
  after a review, including PR review, change the code: run the check and
  `holdout --why final` once more, so the report shows measured numbers,
  not ranges or "expected the same".

## 5. When it stalls, find what slows it

`status` prints PLATEAU after 5 steps with no gain. Stop and run a blocker
review. Measure before you guess. Profile, time each stage of the check, and
find the floor (the best this approach could ever do):

- Where does the time go? The check, a queue, a slow build, or thinking?
- Is the check flaky, too coarse to see small wins, or blind to what's wrong?
- What tool, access, data, or compute would change the next ten steps?
- Is there a bigger idea the small steps can't reach?

Log it with `python3 "$CLIMB" review "<what you found>"`. That quiets PLATEAU
for 5 steps. Fix what you can yourself: make the check faster, add a finer
metric, cache the build, run independent checks in parallel. If the fix needs
something only I can give, like money, access, or hardware, try every other
idea first, then ask with the question tool.

A blocker can be a climb of its own, for example a build too slow for the
check. Put it under "Next climb" in the report. Don't start it without a "go".

## 6. Reaching the bar

When `try` prints BAR REACHED, the script runs the holdout. A visible win
with a flat holdout is not a win.

For `raise`, check the floor from your last profile, then set a harder bar
with `python3 "$CLIMB" raise 2x --why "..."`. It takes a number or a factor of
the current best. For a lower-is-better score, 2x means half. A good next bar
is a bigger version of the same claim ("2x faster again", "all 400 samples,
not 40"), never a new goal.

## Stop when

- The bar is reached and the card says `stop`.
- A limit I set is spent and the gains stopped: `try` refuses with "Budget
  used".
- `status` prints STUCK: two blocker reviews with no gain between them.
- The holdout disagrees with the visible score.
- The next step needs something only I can give, and no other idea is left.

## The report

This is the message I read when I come back. Make it scannable in ten
seconds: a headline, one table, short bullets, no paragraphs. Use this layout:

> ### Climb `build-speed`: bar reached
> **47.1s → 18.7s**, 2.5x faster (bar 23.5s, reached at step 41)
>
> | | |
> | --- | --- |
> | Holdout | 51.0s → 20.2s, moved with the score |
> | Steps | 19 kept of 52 |
> | Safety | Guards passed on every kept step. Full suite and final review clean |
> | Time | 1h 50m, about 2 min a step |
> | Branch | `climb/build-speed`, 19 commits |
>
> **What worked**
> - Incremental type cache: −12s
> - Parallel emit: −9s
>
> **Tried and undone** (never landed)
> - swc swap: broke 3 guards
>
> **Your move**
> - Review: `git log --oneline 1a2b3c4..climb/build-speed`
> - Next climb: cache `node_modules` in the bench (check 2 min → about 35s)

The headline status is one of: bar reached, budget spent, stuck, holdout
disagrees, needs you. Put the biggest wins first, with what each one gained.
Keep each section to 3 bullets. Skip a section with nothing in it.

Before the report, delete `.hill-climb/<name>/data/` and anything else big
you made, and run `python3 "$CLIMB" save` so the kit holds the final check
and notes.

## Storage

Keep the footprint small, even after thousands of climbs. The script enforces
most of this:

- **Commits:** `try` and `init` refuse any file over 10 MB, so the climb
  branch never carries big binaries.
- **Climb state:** `status` prints STORAGE when `.hill-climb/` passes 200 MB.
  Shrink or delete `.hill-climb/<name>/data/` before the next step.
- **Kits:** one `.tar.gz` per climb under `~/.hill-climb/kits/<repo>/`, with
  only the locked check files and the notes. `save` skips files over 500 KB
  and the `data/` folder, and refuses a kit over 2 MB. A rerun overwrites the
  old kit.
- **Judges:** `judge.py` saves no session history. Overwrite screenshots each
  step. Don't keep one per step.
- **Your part:** keep notes short, reuse the existing dependency install
  instead of copying it, and delete `data/` before the report.

## Starting over

If the card was wrong, like a bad `--min-gain` or the wrong check, run
`python3 "$CLIMB" drop <name>`. It goes back to the base branch, keeps the old
climb on a renamed branch, and puts the check files back in the tree for a new
`init`.

## Running for a long time

A climb can outlast one session. Keep everything that matters on disk: the
card, the log, the notes, and the commits. If the client has a goal or loop
mode, give it a prompt like
"Continue the hill climb build-speed until climb.py status says the bar is
reached or STUCK, or try says the budget is used." When a session ends
mid-climb, the next one starts at step 0.

## Commands

| Command | Does |
| --- | --- |
| `init <name> --goal --check --direction min\|max` | Card, baseline, branch, kit. Options: `--check` (repeat, runs at once, scores add), `--score '<regex>'`, `--repo <path>` (repeat), `--guard` (repeat), `--target` (number or `2x`), `--after stop\|raise`, `--runs`, `--paired` (old and new code in turns), `--min-gain`, `--timeout`, `--holdout`, `--lock` (repeat), `--max-hours` and `--max-steps` (only when I set a limit, soft unless `--hard`), `--here` (no new branch) |
| `try "<idea>" [--fix]` | Score the edit, keep or undo it. `--fix` keeps a repair that holds the score |
| `status [name]` | Score, trail, last steps, PLATEAU or STUCK |
| `holdout --why "..."` | Run the holdout now |
| `raise <bar> --why "..."` | Set a harder bar after reaching this one |
| `relock [name] --why "..."` | Accept a fixed check and measure again |
| `review "<found>"` | Log a blocker review |
| `budget [name] [--hours N] [--steps N] [--off]` | Give N more hours or steps from now, or remove the limits |
| `drop [name]` | Abandon the climb, keep its branch |
| `list` | Climbs in this repo |
| `save [name]` | Save the kit now |
| `kits [words]` | Saved kits from every repo, this repo first |
| `reuse <name or repo/name>` | Restore a kit and print its `init` |
