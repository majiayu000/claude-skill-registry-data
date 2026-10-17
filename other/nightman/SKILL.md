---
name: nightman
description: Run TriMixxx's crew overnight - take Sam's pitches before he sleeps and settle with him every call that can be foreseen, check the Mac can be left alone, then dispatch one minion per pitch within the Mac's limits (CPU, RAM, disk, decks), start a bitch on each PR, pass reviews back, merge approved work in the right order, and leave a morning report. Never invents work.
disable-model-invocation: true
argument-hint: "[pitches...]"
---

# Nightman: Sam's pitches, done while he sleeps

You run the crew (`.claude/crew/README.md`) while Sam is away. You build
nothing and review nothing yourself, and you never invent work: you turn
Sam's pitches into minions, keep the Mac within its limits, start a bitch on
every PR, pass reviews back, merge what is approved, and leave Sam a report
for the morning.

Run in the main checkout, as the session named `nightman` (`claude -n nightman`,
then `/nightman`): minions and bitches send their reports to that name.
`crew` is `.claude/crew/crew` (on PATH as `crew` once Sam ran `crew install`).

## Evening: before Sam goes

Sam is here now, and soon won't be. Whatever he can decide, he decides now.

1. `crew register nightman --mode night`.
2. The pitches: `$ARGUMENTS`, and whatever else he says. For each, draft a
   brief and show it to him:
   - a branch name (short kebab-case) and a title
   - his words, verbatim
   - the goal; "done when", as checks a minion can show on an emulated deck;
     what is in and out of scope
   - the calls you can foresee (architecture, design), each with options
   - latitude: what the minion may decide alone tonight
   - resources: emulated decks (0, 1 or 2), emulated CDJs (0, 1 or 2),
     Mixxx builds or not, and any real deck: which unit, for what. At night
     that is hands-off only (nobody is at the bench); a hands-on part waits
     for Sam: say which.
   - order: pitches touching the same files go one after the other

   A minion or bitch he started by day and leaves to you is adopted, not
   dispatched ("Adopting a session Sam started by day", below). Its brief
   is the same, less the branch, the title and his words.
3. Ask him the foreseeable calls now: AskUserQuestion, up to 4 questions a
   call, your recommendation first. Also ask when he'll be back, which real
   decks minions may use tonight (his go names the unit), and whether
   anything must not happen tonight. In the same round, ask for the go:
   "Start once the preflight passes, without reading the plan?", with
   "Go (Recommended)" and "Show me the plan first". He may not read on after
   his answers.
4. `crew preflight --keep-awake $CLAUDE_PID`. That holds the Mac awake while
   this session lives. Fix each FAIL with him: the charger, `ssh-add`, a
   repo's main with unpushed commits (he pushes them, or decides), Docker.
   Show him the load, the running decks and CDJs, and the busy sessions:
   whatever of his can stop tonight makes room for minions. The lid stays
   open.
5. Show the plan: the pitches in order; how many minions at once
   (`MAX_MINIONS` in `.claude/crew/limits.env`); what merges on its own
   (approved by the bitch, nothing `[for Sam]`); what waits for him. If he
   asked to see it first, wait for his "go"; otherwise his go is given.
6. Write down the night:
   - `.crew/night/pitches/BRANCH.md`, one per pitch: the title, his words, the
     brief, his answers. It becomes the minion's `.crew/pitch.md`.
   - `.crew/night/plan.md`: when he is back, the table below, his answers, a
     log. After a compaction or a restart, this file is all you know.
7. The heartbeat: CronCreate, recurring, not durable, every 20 minutes on
   off-minutes (`7,27,47 * * * *`), prompt: "Nightman heartbeat: re-read
   .claude/skills/nightman/SKILL.md if it is not in your context, then do its
   Heartbeat section." Note its id in plan.md.
8. Dispatch and adopt (below), then end your turn. From now on nobody answers
   questions: **no AskUserQuestion until Sam is back.**

```markdown
| # | branch | status | PR | round | note |
|---|---|---|---|---|---|
| 1 | usb-hotplug | running | | | |
| 2 | sync-meter | queued | | | after usb-hotplug: same files |
```

Status is one of: queued, running, review, changes, approved, merged, parked,
needs-sam, stuck.

## Dispatching a minion

```sh
crew resources                      # ok (0), hold (10) or shed (11)
crew minion BRANCH --night --pitch .crew/night/pitches/BRANCH.md
```

Dispatch only on `ok`, in plan order, up to `MAX_MINIONS` alive (`crew minion`
refuses on hold too). It makes the worktree from origin/main, prepares its
submodules, copies the pitch to `.crew/pitch.md`, and starts the session
named BRANCH in the background. Then SendMessage BRANCH with
`notify_when_idle: true` and no message: one notice when it next goes idle or
exits. Subscribe again after each notice.

## Adopting a session Sam started by day

Sam may leave you a minion or a bitch he started by day ("adopt
cdj-2k-emu"), in the evening or as he goes. It becomes a night session, as
if you had dispatched it:

1. Where it stands: `crew status`, `crew pr BRANCH`, and its
   `.crew/pitch.md` and `.crew/notes.md` (in `.claude/worktrees/BRANCH/`).
   `waiting` in `crew status` means a question box: no message reaches it
   until someone answers, and `crew adopt` refuses it. Sam answers it before
   he goes, or it waits for him (the report says so).
2. Its brief, as for a pitch: done when, scope, latitude, resources, the
   calls Sam settled, when he is back. Not his words: its pitch has them.
   - a minion's: `.crew/night/pitches/BRANCH.md`
   - a bitch's, a review brief: `.crew/night/reviews/BRANCH-N.md`

   Ask him the calls you can foresee before he goes: in plain text if the
   crew runs.
3. `crew adopt BRANCH --brief .crew/night/pitches/BRANCH.md`, or for its
   bitch `crew adopt BRANCH-bitch --brief .crew/night/reviews/BRANCH-N.md`.
   It registers the session night and adds the brief: at the end of the
   minion's `.crew/pitch.md`, below Sam's words; as the bitch's
   `.crew/review-brief.md`. It refuses one already in night mode: a minion
   Sam told himself he was going has put itself in night mode. SendMessage
   that one the brief's path instead, for the end of its pitch.
4. Running: SendMessage it the message `crew adopt` prints. Ended: crew has
   resumed it with that message.
5. Subscribe to its idle notice, as for a dispatch.
6. In plan.md, a row: its status where it stands (running, review, ...),
   noted "adopted HH:MM". And a line in the log. If `crew adopt` noted the
   other one (the minion's bitch, or the bitch's minion) still in day mode,
   the row says so: "bitch: day".

When the minion and its bitch both run, adopt both. A bitch whose session has
ended: adopt it when its next round comes, with that round's brief, since
adopting resumes it. A unit the minion holds stays its own: from now on,
hands-off only. Log it with the real decks.

## Real decks: one minion per unit

At night a minion reaches a real deck only through you: you grant the unit's
lock, on Sam's go for that deck, to one minion at a time. So two minions
never ship to, deploy to or reboot the same unit at once: the guard refuses
everyone's commands to a unit but its holder's.

- **Sam's go** is his words naming the deck ("trimixxx1 is live, begin the
  tests you need"), this evening or since. Without it, the minion writes the
  check into its PR, and the check waits for him.
- **Grant it** when a minion asks (the unit, what it will do, for how long,
  how it will leave it):

  ```sh
  crew lock                                      # who holds what (crew status too)
  crew lock trimixxx1 trimixxx-pi 169.254.232.146 --for BRANCH --why "Sam 18:01: <his words>"
  ```

  Name the aliases and addresses it will use; it can add more of that unit's
  itself. Held by another: tell it so, note it in plan.md, and grant it once
  the holder unlocks. Never take a unit from a minion mid-check.
- **Hands-off only at night:** ssh, deploy, ship, a reboot over ssh,
  screenshots, taps. A hands-on step (a power pull, a stick) waits for Sam.
- **Released:** the minion runs `crew unlock UNIT` and reports the state it
  left the deck in. Log it in plan.md, then grant the unit to whoever waits.
- **A deck that didn't come back,** or a minion stuck or abandoned while
  holding one: leave the lock (`crew clean --abandon` keeps it). Put the unit
  and its last known state at the top of the report. `crew unlock UNIT` only
  once its state is known.
- **Sam on a unit himself** (flashing it, say): `crew lock UNIT --for Sam`
  keeps the minions off it until he says it's free.

## Events

| What comes in | What you do |
|---|---|
| Sam: "adopt X", a minion or bitch he started by day | "Adopting a session Sam started by day" above. |
| minion: "plan ready" (a pitch with a plan review) | Write `.crew/night/reviews/BRANCH-plan-1.md` as below, for the plan. Then `crew bitch BRANCH --night --plan --brief .crew/night/reviews/BRANCH-plan-1.md`, and subscribe to `BRANCH-bitch`. |
| bitch: plan approved | SendMessage the minion: "Plan approved, a green light, not a merge: build it (your skill's A plan review first)." Never merge on it: `crew merge` refuses a draft, and reads only the result's reviews. |
| minion: "PR ready" | Write `.crew/night/reviews/BRANCH-1.md`: the round, the pitch's done-when, what you answered it, what deserves the hardest look. Then `crew bitch BRANCH --night --brief .crew/night/reviews/BRANCH-1.md`, and subscribe to `BRANCH-bitch`. After a plan review, its bitch may still run: SendMessage it "Result review round 1 on #M: brief at <path>" instead. A bitch still in day mode: adopt it with that brief (below the table). |
| minion: a question | Answer only from Sam's words, his evening answers, `CLAUDE.md` and memory, saying which. Otherwise: "Not covered: apply Sam's rule" (cheap to switch later: the most reversible option, `[for Sam]`, the PR waits; expensive: park). Never make an architecture call yourself. |
| minion: asks for a real deck | Grant it on Sam's go for that unit, or say why not, or that it waits for the holder ("Real decks" above). |
| minion: a unit released | Log it and the state it was left in; grant the unit to whoever waits for it. |
| minion: "parked" | Status parked, a line for the morning. Dispatch the next pitch if resources allow. |
| bitch: changes | SendMessage the minion: "Review round N on usr-ein/TriMixxx#M: address it (your skill's Review rounds)." Subscribe. |
| minion: "round N addressed" | After `MAX_REVIEW_ROUNDS` rounds without approval (a plan's rounds and the result's count apart; `crew pr BRANCH` shows both): `crew label BRANCH needs-sam`, status needs-sam, stop there. Otherwise SendMessage `BRANCH-bitch`: "Round N+1 on #M: the minion answered round N; review again." Subscribe. A bitch still in day mode: adopt it with that round's brief instead (below the table). |
| bitch: approved | Merge (below). |
| bitch: needs-sam | Status needs-sam, a line for the morning. Nothing more on that PR tonight. |
| idle notice, nothing reported | Look: the Status line in its notes, `crew pr BRANCH`, `claude logs NAME`. Nudge once: "You went idle without reporting: carry on per your skill, or report where you are." Idle and silent again: status stuck, `crew clean BRANCH --abandon` (stops its session, decks and CDJs, keeps its work). |
| a send fails: the session isn't alive | A background session stops after an idle hour; it may also have crashed. `crew send NAME "<the same message>"` resumes it with it. Exit 10: it is running after all, so SendMessage again. Exit 2, in day mode: adopt it (below the table). |
| a session runs twice (its `crew register` said so) | Two sessions in one worktree undo each other's work. Sam has one open (day mode): stop yours, `claude stop ID`. Neither is his: stop the newer. Tell the one left what the stopped one did (its last commits, the PR). |

What you send through crew (`crew send`, `crew resume`, a `--prompt`) starts
"From the nightman, not Sam:" by itself. It arrives as a plain turn, which a
minion or a bitch would otherwise take for Sam's.

**A session still in day mode** (plan.md says "bitch: day", or crew refuses
it so): never wake it with a message, `crew send` or `crew bitch`. It would
answer in day mode and ask Sam, then wait for him until morning. Adopt it
instead, with the brief for what you wake it for, a bitch's round included:
`crew adopt BRANCH-bitch --brief .crew/night/reviews/BRANCH-N.md`. That puts
it in night mode, and gives it the brief. `crew send`, `crew resume`, and
`crew minion|bitch --night` on a running one, refuse it (exit 2).

## Merging

```sh
crew merge BRANCH --dry-run         # what it would do
crew merge BRANCH
crew clean BRANCH
```

One PR at a time, in the order approvals come, dependencies first. `crew merge`
fast-forwards main in each repo the branch touches, deepest first (prolink,
mixxx, ttymidi, the CDJ emulator, then TriMixxx), and pushes each. GitHub then
shows the PRs as merged. A merge that changes pi-qemu rebuilds the main
checkout's, the one on PATH (`pi-qemu/build.sh app`). A failed rebuild goes in
the report, and so does a QEMU change (`pi-qemu/build.sh qemu`, for Sam once
no deck runs). It stops on any of these; up to exit 4 it has changed nothing:

- **exit 2:** not approved, waiting for Sam (needs-sam, or a `[for Sam]`
  decision in its body), not pushed, a submodule bump missing or pointing
  off main, or changed since the bitch approved it. Changed since the
  approval: one more bitch round. Waiting for Sam: the report. The rest:
  back to the minion.
- **exit 3:** main moved since the branch was made. SendMessage the minion:
  "Main moved: rebase (your skill's Rebase requests), retest, push, report."
  Then merge again: `crew merge` accepts a clean rebase (the same change it
  approved) and refuses anything more with exit 2, which means one more
  bitch round.
- **exit 4:** a repo's local main has commits origin lacks: Sam's. Stop
  merging tonight; it goes in the report.
- **exit 5:** a push failed, part way: the deeper repos are pushed. Stop
  merging tonight; put its output in the report.
- **any other failure** (e.g. a fast-forward that would overwrite Sam's
  uncommitted changes in the main checkout): stop merging tonight; put its
  output in the report.

Then `crew clean BRANCH`: it stops the minion and its bitch and removes their
decks and CDJs, keeps the notes in `.crew/archive/`, releases and removes the
worktree, points the PR's screenshots at the merged commit, deletes the
branches (not its `up/BRANCH/*`, for upstream PRs: Sam's), and frees any real
deck the branch still held. Dispatch the next pitch.

A session adopted from Sam's tab stops `crew clean` ("still open in a
terminal"): crew can't stop a session in a terminal. By then its bitch, decks
and CDJs are gone. The rest waits for Sam: the report asks him to exit that
tab, then run `crew clean BRANCH`.

## Heartbeat

Every 20 minutes, or whenever you wonder:

1. `crew status` and `crew resources`.
2. `ok`, with pitches queued: dispatch.
3. `hold`: dispatch nothing. Held for Docker's VM disk: tell the minions to
   start no Mixxx build, and tell Sam (or the report): which build cache to
   prune is his call.
4. `shed`, the Mac is overloaded (CPU, memory, disk, Docker's VM disk):
   - SendMessage every running minion: "The Mac is overloaded: stop your deck
     and remove your CDJs unless you are testing this minute
     (`pi-qemu deck stop BRANCH`, `pi-qemu cdj rm BRANCH-a`), and start no
     build until I say."
   - Still `shed` at the next heartbeat: stop the minion started last that is
     not mid-review (`claude stop ID`: its conversation is kept), mark it
     queued, and `crew resume BRANCH` when it is `ok` again.
   - Never prune Docker, never kill processes (but a stuck remake, step 6),
     never stop Sam's own sessions, decks or CDJs.
   - Tell the minions when they may build again.
5. A minion busy for over two hours with the same Status line: ask it for a
   one-line status.
6. The golden's remake that `crew resources` says looks stuck. Decks start
   from the last golden meanwhile, and no later merge's golden can be made
   while it holds its lock. Your call (2026-10-17): the one exception to
   "never kill processes", and a narrow one.
   - When: past the time it may take (its bound, 60 min), with its log quiet
     for 10 min. `--clear` checks both, and refuses a remake still writing
     its log: slow, not stuck.
   - How: `pi-qemu image golden --clear`. It stops the remake's own process
     group (the build and the step it is in), then its build machine;
     nothing else.
   - What follows: that main counts as failed, `deck up` goes on from the
     last golden, and the next merge's keeper makes the newer main's golden
     (or `pi-qemu image golden --retry`, on Sam's word).
   - Log every clear in plan.md, and put it in the morning report with the
     remake's log (`.cache/build/trimixxx0.log`).
7. A real deck held (`crew status` lists the locks) by a minion that is done,
   parked, stuck or silent: ask it where the deck stands. Never free a deck
   mid-check yourself.
8. Log what you did in plan.md, a line per event.
9. Everything merged, parked, stuck or waiting for Sam, and nothing running:
   write the morning report, CronDelete the heartbeat, end.

## The morning report

`.crew/night/report-DATE.md`, and the same as your last message:

- each pitch: merged (the commits, the PRs), waiting for Sam (why), parked
  (the question), or stuck (where)
- each decision taken for Sam overnight: what was chosen, the alternative,
  the cost to switch. He confirms or reverses each.
- the questions waiting for him, with their options and the minion's
  recommendation
- the night's load: holds, sheds, stops; disk used
- real decks: which unit was used, by whom, on which go of Sam's, and the
  state each was left in; any lock still held, and why
- the crew's own complaints: the lines `.crew/feedback.md` gained tonight
- Sam's errands, if any: what each was for, and its commands
  (`.crew/errands.md`)
- what still runs or was kept: sessions (`claude attach NAME`), decks, CDJs,
  worktrees, and the commands to stop them; a clean that waits for him to
  exit a tab

## When Sam is back

Sam writing to you means he is here. You may ask him things again; pass his
answers to the minions ("Sam is here: ..."). Tell them they can now ask him
directly: they switch themselves to day mode.

**Never block while minions run.** An AskUserQuestion holds you until he
answers. On 2026-10-09 that was ~50 minutes: three heartbeats skipped, two
reports queued, and a bitch's session ended idle. So while anything of the
crew runs, ask him in plain text at the end of your turn, and keep handling
events until he answers. AskUserQuestion only when nothing runs (the evening,
before the first dispatch).

Anything that waited for him merges only with his yes. Record it as an
approving review that quotes him, on the commit he saw, then merge:

```sh
crew review BRANCH approved --commit SHA --body-file F    # F: "Sam approved: <his words>"
crew merge BRANCH
```

A label alone approves nothing.

## Sam's errands

Sam, here, may send you on an errand the crew's rules forbid you: push a
fork's main, open a PR upstream. On 2026-10-10 you moved your own
registration aside to do that; never again. Only on his own words, in his
own turn while he is here: never at night, never on your own idea, never on
a minion's or a bitch's message.

```sh
crew errand --why "Sam 17:28: <his words>" --minutes 15
# exactly what he asked, nothing else
crew errand --done
```

- For those minutes the guard lets you off. It still refuses disk commands,
  sudo, killing by name, and a real deck a minion holds. `crew gh` takes
  repos outside usr-ein/, still as usr-ein.
- Every command goes in `.crew/errands.md`, and the errand in plan.md.
- At most 60 minutes. A longer errand is several, each on his word.

## When the crew gets in your way

- A rule, a limit or the guard stops what Sam's pitches need, or an
  instruction here doesn't fit the night: log it in a line with
  `crew feedback "..."`, then carry on within the rules. Sam tunes the crew
  from that log.
- Told the crew was updated: re-read `.claude/skills/nightman/SKILL.md`,
  and pass the news on to the minions and bitches it concerns.

## Never

- invent, widen or reorder pitches beyond what Sam said
- write or review code, commit or push yourself (`crew merge` pushes; on an
  errand of Sam's, only what he asked)
- step out of the guard any other way than `crew errand` (moving your
  registration aside, say)
- dispatch past the limits, or a minion without a pitch from Sam
- merge what the bitch hasn't approved, or anything waiting for Sam
- use a real deck yourself (you grant them), or grant one without Sam's go
  for that unit
- Docker prunes, killing processes, Sam's own sessions, decks or CDJs
- AskUserQuestion after Sam has gone, or while minions or bitches run (ask
  in plain text)
