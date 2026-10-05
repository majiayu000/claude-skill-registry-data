---
name: usage-limits
description: Check how much usage limit is left in this agent (Claude Code or Codex) and plan the work to fit inside it. Use before starting anything long, when the 5-hour or weekly limit is getting close, when asked how much usage or quota is left, whether there is enough left to finish, whether a job fits before the reset, when to stop and hand off, and when asked to work cheaply, burn fewer credits, or stretch the rest of the limit.
---

# usage-limits

Running out of limit halfway through a job is a scheduling failure, not bad
luck. The numbers are on disk before the work starts. Read them, size the job
against them, and either commit to finishing or cut the job down until it fits.

## 1. Measure

```
node scripts/usage.js
```

Paths here are relative to this skill's own directory, not the project you are
working in. Run them from there, or prefix them with the skill's path.

This works the same in Claude Code and in Codex. The host is detected from the
environment; add `--host codex` or `--host claude` if a machine has both
installed and the wrong one is picked. Everything below applies to both unless
it says otherwise.

It prints the real percentages and reset times from the CLI's own cache, plus
a pace measured from the local session transcripts:

```
  Window           Used   Resets in      Left  Turns left
  5-hour            62%      1h 40m     $46.0         ~88
  weekly            75%       2d 4h     $124         ~240   <- binding

  Recent pace   15 turns in the last hour, $0.164 per turn, effort xhigh
```

`Turns left` is the number that matters. It is the remaining headroom divided
by what a turn has actually been costing over the last hour, on this account,
at this effort level. Add `--json` when you want the raw fields.

If it says no snapshot was found, run `/usage` once in Claude Code and try
again. That populates the cache the script reads. In Codex the equivalent is
`node scripts/usage.js --refresh`, which asks Codex itself for a live reading
instead of using the newest one it happened to write.

`Left` is money, so it only appears under Claude Code. Codex meters a share of
an allowance and never quotes a price, so its report has no money column and
its percentages are exactly what they say they are.

The last line names the plan (Pro, Max 5x, Max 20x, Team, Enterprise) and what
it means for spending. Pro has the least room and the 5-hour window usually
binds first; Max 20x rarely binds at all. Take that line into account before
deciding how careful to be.

## 2. Size the job before starting it

Count the work in turns, not in tasks. A rough scale that holds up in practice:

| Work | Turns |
| --- | --- |
| Read and answer a question about existing code | 1 to 2 |
| One edit plus the check that it worked | 2 to 4 |
| A feature touching three or four files | 10 to 20 |
| Debugging something with an unknown cause | 15 or more, and unpredictable |

Then compare against `Turns left` and hold back a reserve. Reserve about a
fifth of the budget for landing the work: the test run, the commit, and the
handoff note. Work that gets cut off just before the commit is worth nothing,
so the reserve is not optional.

## 3. Decide, out loud

Tell the user which of these applies before doing anything expensive.

**It fits.** Say so with the number, then work normally. Do not slow down out
of caution when there is room. Cheapness is not a virtue when the budget is
not tight.

**It fits only if nothing goes wrong.** Say so, switch to low power for the
run, and reorder the work so the valuable part lands first.

**It does not fit.** Say so in one line before starting, and name the
wall-clock time the window resets so the user knows when the rest can happen.
Then do the whole thing anyway, ordered so that being cut off costs as little
as possible.

That is the part to get right, because the tempting move is the wrong one.
Deciding on the user's behalf to do less of what they asked spends their
request to protect a budget that expires regardless, and they did not ask for
that trade. Scaling the work down is their call, not yours.

So take the whole request, and make a cutoff cheap instead:

- Order it so the most valuable part lands first.
- Save at clean boundaries as you go, rather than once at the end.
- Keep a short running note of what is done, what is next, and which files are
  mid-change, so stopping at any moment loses nothing.

Half a feature, committed and working, still beats a whole one abandoned
mid-edit. The difference is that you get there by sequencing the work, not by
refusing part of it.

**The window resets first.** If the reset lands before the budget runs out,
the limit is not the constraint. Say that and stop optimising for it.

## The budget line ages during a turn

The hook runs when a prompt is submitted, so the figures you were given are
from the start of the turn. A message sent while you are already working does
not fire it again: it arrives without a budget line, and the numbers you are
holding are now older than they look.

The reading itself is kept fresh: the hook takes the same reading Claude Code
takes for `/usage` when the one on disk is older than three minutes, and the
mid-turn pulse does the same every two minutes through a long turn. So the
figures are as good as `/usage` at those moments. What no hook can do is fire
between them, and a burst of parallel agents can spend a great deal in the
gap: eight workflow agents once emptied half a 5-hour window in five minutes.
Spawn agents knowing that each fresh context re-reads what you already hold.

That matters most when it is the one thing you are about to assert. Re-check
before saying a job fits, if any of these are true:

- the turn has run long, or through many tool calls
- more requests arrived while you were working
- other sessions are active, so the budget is draining without you

```
node scripts/usage.js --status
```

That is one cheap read of a small file, no transcript scan, and it costs far
less than promising to finish something and stopping halfway. If you have no
budget line at all this turn, you are mid-turn: use the last one you were given
and treat it as a ceiling, not a reading.

## When messages stack up

Every message sent while work is already running starts another turn, and every
turn re-sends the whole conversation. Three follow-ups during one task can cost
more than the task did.

So when several additions arrive while you are still working and the binding
window is tight, say it once, then keep going:

> I have got all three. While the weekly window is this tight, sending them
> together costs a good deal less than one at a time, so I will fold these in
> and carry on. Send the rest in one go if you can.

Four rules keep that from being obnoxious, and they matter more than the saving.

**Ask once per stretch of work.** A second reminder costs more goodwill than
the tokens it saves.

**Only when the budget is actually tight.** With room to spare, asking someone
to hold their thoughts is rude for no gain. Say nothing.

**Never discourage a correction, a stop, or a bug report.** Those are the
messages that save the most work. Someone interrupting to say the approach is
wrong has just paid for their own interruption many times over, and a rule that
trains people out of that is far more expensive than the turns it saves. Only
additive scope, the "also do X" and "and can you Y", is worth batching.

**Never make it about you.** The cost lands on their limit, not yours. Frame it
as their budget, offer the saving, and let them decide. Then work. Do not stop
to negotiate about whether to stop.

## Credits

The `Credits` line in the report says what actually happens at the limit, and
the two cases need opposite handling.

**Off.** Work stops dead at the limit. Nothing spills over. This is the case
to plan hardest around, because there is no way to buy your way through it.

**On.** The limit is a cost boundary rather than a hard stop, so a job that
does not fit can still be finished, for money. Do not warn about the crossover
yourself: Claude Code announces it and asks before drawing on credits, and
repeating that only adds noise. Just factor it into the plan, and take the
user's answer to that prompt as the decision.

**Cloud credit.** A separate line, when the account is offered a credit for
cloud sessions. It is not usage credits and it can be there while they are
off. At the wall it is the way on now rather than after the reset: `relay
cloud` prints the `claude --cloud` command carrying the hand-off, and warns
about anything not pushed, because the cloud session clones from GitHub. Offer
it in one line; it spends the user's credit, so starting it is their call.
Inside a cloud session there is no usage snapshot, so do not send the user to
`/usage`; the report gives this session's spend at list prices instead.

## Opening with the budget

Start every reply with one line saying where the budget stands and whether what
was asked fits. The hook puts the numbers in front of you before the prompt, so
there is nothing to go and look up.

When there is room, one line, then get on with it:

> The 5-hour window is the binding one: 47% used, about 75 turns of headroom.
> This fits easily.

When it does not fit, that line becomes the plan:

> The weekly window has about 22 turns left. That covers the parser change and
> its tests, but not the migration or the docs pass, so I will do the first two
> and leave the rest for after the reset at 09:00.

What makes the second one useful is the split, not the percentage. "78% used"
is not something anyone can act on. "This fits, that does not, here is the
order" is.

Keep it to one line unless the work genuinely does not fit. The budget note is
a header, not a section, and it must never push the actual answer down the
page.

Which window binds is about what stops you soonest, not what stopping costs.
Those differ: a 5-hour window comes back in hours, the weekly one in days. So
when a window that is not binding sits near its wall, say so and weigh it. The
hook flags those. Running the weekly out to save a few turns of the 5-hour
window is a bad trade even though the 5-hour is what runs out first.

The exception is a weekly that caps one model. `weekly (Fable)` at 88 per cent
is not your wall while you are working on Opus - nothing you do moves it, and
doing less work will not un-spend it. The report marks those `not in use` and
the hook leaves them out of what it asks you to weigh. Do not weigh them back
in. They matter again the moment you switch to that model, and that is when
they come back.

That cuts both ways, and the second half is the useful one: when the window
that binds is a per-model weekly, the same work on another model draws on a
different window. The report's **Model headroom** table says what the room left
buys in turns of each model, priced from what that model has really cost here.
Moving mechanical bulk onto a model with room is not doing less work - it is
the same work against a wall that is further away, which is the one economy
worth making. A model with no turn count in that table has only ever run as a
subagent; its errands are not turns, so there is nothing to project from.

One thing to get right: **quote the binding window, not the roomiest one.**
Two windows run at once and they are rarely in the same place. The turns of
headroom and the reset time belong to whichever runs out first. Putting the
other window's percentage next to those figures claims far more room than
exists, and that is how a session ends mid-edit while the weekly number still
looks comfortable.

### Pricing the job before starting it

Size the work in turns using the table above, then price it:

```
node scripts/usage.js --forecast 15
```

That converts turns into points of each window using what turns have really
cost on this account, and reports a range rather than a single number, because
a turn that reads three files costs many times one that answers from context.
The upper end is the honest one for a long run, since turns get dearer as the
context grows.

Reach for it whenever the answer to "will this finish" is not obvious.

## Closing with what it cost

The budget line opens the reply; the cost closes it. When a reply completes
what was asked, or wraps up the session, end it with one plain line:

> Spent this session: 48 turns, 3.1M tokens, about $12.40.

The figures come from the `This session:` part of the budget line, so there is
nothing to run. They are exact as of the start of this turn, and the Stop hook
prints the up-to-date figure to the user the moment you finish, so do not go
and re-measure for the closing line.

Three rules keep it useful rather than noisy:

- **Finished work only.** A progress note mid-task, a clarifying question, or
  a reply that ends with "shall I go on" is not the moment. The line marks a
  goal reached or a session wrapped up.
- **One line, at the end.** It is a footer, not a section, and it never
  replaces the recap of what was actually done.
- **Plain text.** No symbols, no formatting tricks. The number is the point.

The user can also ask any time with `/usage-limits:session`, or run
`node scripts/usage.js --session last` for the full breakdown and
`--sessions` for the history of recent sessions on this machine.


## Turning it off

If the user says they do not want the budget line, the cost line, or the status
bars, do not argue and do not explain the trade-off unless asked. Run:

    node "$CLAUDE_PLUGIN_ROOT/skills/usage-limits/scripts/mode.js" off

and, for the bars, `statusline off`. `mode off --guard 95` is the middle
ground: silent until 95 per cent. Say which one you ran and stop.

## Budget modes

How hard this plugin leans, and what it costs to say it. Four modes, set by the
user and read by every hook:

```
node scripts/mode.js                 # which one, where it came from, what it changes
node scripts/mode.js max             # set it
node scripts/mode.js --list          # all four, and the aliases
node scripts/mode.js --explain high  # one mode's full record
```

| mode | one line |
| --- | --- |
| `max` | fewest tokens that can still finish the job: one terse line, readings every ten minutes, silent when nothing a decision depends on has moved |
| `high` | full capability, re-measured every two minutes mid-turn, and said only when the answer changes |
| `standard` | what the plugin does today, unchanged. The default |
| `off` | nothing injected at all; every hook returns before reading anything, including the end-of-reply tally |

Aliases: `ultra`, `ultra-efficient`, `maxtoken`, `maxefficient` map to `max`;
`smart`, `high-efficient` to `high`; `efficient`, `token-efficient`, `default`,
`on` to `standard`; `none`, `quiet`, `silent`, `ignore` to `off`.

**`normal` is not an alias for either.** To some people it means "the plugin
working as usual" (`standard`) and to others "the plugin stays out of the way"
(`off`) - opposite instructions, so a silent guess is wrong half the time. If
the user says "normal", ask which they meant and say what each one does. The
script answers the same way.

`auto` picks from how full the binding window is - standard under 50 per cent
used, high from 50 to 79, max at 80 or above - and always reports itself as
what it resolved to (`auto -> max`). It reads the snapshot already on disk
rather than scanning, because the mode has to be settled before anything
expensive runs, and with no readable window it stays on `standard` rather than
guessing. It never picks `off`: turning the plugin off is a decision a person
makes.

`off` means off, including at 100 per cent. That is deliberate. If the user
wants one line at the wall and nothing else, `node scripts/mode.js off --guard 95`
is it.

Two rules hold in every mode, and they are not negotiable:

- **A mode never lowers the quality of the work.** When things are tight you
  change the ORDER of the work, never the amount or the quality. The savings
  come from ceremony - speculative reads, re-reads, preamble, subagents nobody
  needed, workflows that cost more context than they save.
- **The modes govern the agent plane only**, and never write `settings.json`.

### Two planes, and the conversation between them

The **user plane** is `settings.json` (`model`, `effortLevel`), the `/effort`
and `/model` pickers, and `lowpower.js`. It is the user saying what they want
for themselves. It is theirs.

The **agent plane** is the tier actually running this turn, and the tier of
everything this turn spawns. That is what costs money.

What is actually yours to move, stated exactly, because a claim beyond this
would be a lie the user cannot check:

- **The model on an `Agent` call is yours.** `model: "sonnet" | "opus" |
  "haiku" | "fable"` on any Agent call, and it overrides both the agent
  definition and the configured default. It is ignored for `subagent_type:
  "fork"`, which always inherits the parent model.
- **Model and effort inside a `Workflow` script are yours**, per `agent()`
  call: `opts.model` and `opts.effort` (`low` | `medium` | `high` | `xhigh` |
  `max`). The host's own advice is to omit `opts.model` unless you are
  confident, and to use `opts.effort: 'low'` for mechanical stages - so lean on
  effort rather than model when sizing what you spawn.
- **Your own model and effort are NOT yours to change mid-session.** Nothing a
  hook can emit changes them: there is no such field anywhere in the hook
  output contract, and `PreModelSwitch` can only veto a switch someone else
  started. `/model` and `/effort` are typed by a person and
  `CLAUDE_CODE_EFFORT_LEVEL` is read at launch. So say the exact command in one
  line and let the user run it. Never imply you changed it yourself.
- `xhigh` and `max` are refused outright when thinking is disabled, so never
  point at either without that being true.

The two planes talk to each other, in both directions, through the
conversation. The whole rule in one line:

**You may RECOMMEND a user-plane change. You may MAKE one when asked. You may
never make one unasked.**

Recommending, when you do it:

- **Evidence or silence.** Cite a measurement - what this account has actually
  measured, from `usage.js --recommend`, the fit line in the budget briefing,
  or `scripts/drift.js`. "Recommended" with no number is nagging.
- **At most one per session**, and none at all in `off`. The plugin enforces
  this; do not route around it.
- **A declined recommendation is not raised again.** When the user says no,
  record it - `node scripts/mode.js --decline` - and it is never volunteered
  again, in this session or any later one. `--advice` shows what is pending.
- **Name the exact command, the plane it changes, and when it takes effect.**

When the user asks you to change something, or says **"change it back"**: read
`node scripts/mode.js --history` first, say out loud what you are reverting and
to what, then do it. Never infer a target that is not in the log. `node
scripts/mode.js undo` reverses the last change the plugin owns and names it
first; for a change to the user's own settings it names the command and leaves
the file alone, because that plane is not the plugin's to write.

The surprise to head off, every time: **a user-plane change does not move the
session already running.** If the user says "turn low power on" and you do it,
nothing about this session changes - `lowpower.js` says so itself ("Applies to
new sessions. For the session you are in, run /effort X"). Relay that in your
own words whenever you make one, and the same in reverse: putting the baseline
back does not restore this session's tier either.

### Bounds the user can set

```
node scripts/mode.js --floor sonnet/medium   # never point below this, even in max
node scripts/mode.js --ceiling opus/xhigh    # nor above it, even on the hard part
node scripts/mode.js --pin                   # do not self-switch at all: report only
```

Under `--pin` the plugin reports the gap between the baseline and what is
running and suggests nothing. Respect it in your own words too: report, do not
switch.

### Stepping back up

The efficient modes are two-directional, and that matters more than it sounds.
Having dropped to a cheap tier for a mechanical stretch, say so when the work
turns hard again and point back at the baseline. A one-way ratchet down is how
a long session quietly degrades, which is the thing the quality rule forbids.


## 4. Low power

Two halves, and the second one is the half that actually binds.

The setting:

```
node scripts/lowpower.js on              # effortLevel -> low, old value saved
node scripts/lowpower.js on --effort medium --model sonnet
node scripts/lowpower.js off             # restores exactly what was there
```

In a headless run (`claude -p`) there are no slash commands, so the script is
the only lever there.

`effortLevel` is what the `/effort` picker writes. Reasoning is billed as
output tokens, the most expensive tokens in the request, so dropping `xhigh`
to `low` is the largest per-turn saving available without changing model or
scope. The file change applies to new sessions; for the session already
running, `/effort low` takes effect immediately.

### Choosing the level

Do not guess which effort or model the budget calls for; the report can say:

```
node scripts/usage.js --recommend        # against the headroom in general
node scripts/usage.js --recommend 15     # against a 15 turn job
```

It weighs the binding window, the measured cost of a turn, and how much of
the output is actually reasoning, then names the posture (roomy, tight,
critical, or reset-first) and the exact commands. When there is room it says
to keep everything as it is, out loud, so cheapness never becomes a habit.
Add `--json` for the decision as fields.

The three levers it recommends across belong to different hands, and keeping
that straight is the whole trick:

| Lever | Whose hand | When it acts |
| --- | --- | --- |
| `/effort`, `/model` | the user's only | this session, immediately |
| `lowpower.js on` (writes settings.json) | yours, right now | new sessions, at launch |
| subagent model and effort | yours, freely | that dispatch, immediately |

The running session's own model and effort cannot be changed by any script or
hook: settings.json is read at launch and hook output has no model field. So
when the recommendation says `/effort low`, put that in front of the user as
one short line and keep working; do not wait on it. What can be done without
asking anyone is the other two rows: write the next session's settings with
`lowpower.js`, and send self-contained mechanical bulk to a subagent on a
cheaper model at low effort, which is a change of model that needs nobody's
permission. The cold start still costs (see `references/tactics.md` on
subagents), so delegate work that is big and mechanical, not quick questions.

One catch to know about: `settings.json` does not accept `max`, so a saved
effort level tops out at `xhigh`. `max` only survives through `/effort` or the
`CLAUDE_CODE_EFFORT_LEVEL` environment variable, and `lowpower.js` refuses to
write it rather than save a value the next session would silently ignore.

Do not take that on trust: the report measures it. Under the model table it
says how much of the output was reasoning and what that cost, for example

```
    Of that output, 74k was reasoning (40%, about $1.85), the part effort controls.
```

That share is the ceiling on what lowering effort can save, so read it before
deciding whether the saving is worth the loss of reasoning. Forty per cent of
output is worth acting on; four per cent is not, and turning effort down for it
would cost more in rework than it saves. The same figure covers reasoning asked
for per prompt, by `ultrathink` or any other means, because it is all the same
spend on the same meter and the transcript does not separate them.

The behaviour, which applies **even at xhigh or max effort**, because the
effort setting does not control any of it:

- Think briefly on routine steps. Save the long reasoning for decisions that
  are actually hard to reverse.
- Send independent tool calls together in one message. Three calls in one turn
  cost one context resend; three separate turns cost three.
- Read line ranges, not whole files. Grep with a head limit. A 40k-token file
  read is not paid once, it is paid again on every later turn in the session.
- Never re-read a file to confirm an edit landed. The edit tool already failed
  if it did not.
- No subagents. A subagent starts cold and re-derives context that is already
  in this session.
- Nothing that was not asked for. No speculative refactor, no extra test, no
  drive-by cleanup.
- Fewer, denser turns. Narration between tool calls is output tokens spent on
  nothing.

`references/tactics.md` has the full list and the billing reasons behind each
one.

## 5. The wall is not the end of the budget: switch, do not stop

Before treating a full window as a reason to stop, check what kind of window it
is. There are two, and only one of them is the account's budget.

- **A per-model weekly** (`weekly (Fable)`, `weekly (Opus)`, `weekly (Sonnet)`)
  counts turns by *that model only*. It is not your budget, it is that model's.
  Lowering effort does not free a single point of it. **Switching model retires
  it outright** - `/model opus`, `/model sonnet`, or
  `node scripts/lowpower.js on --model <id>`. Every other window carries on
  exactly as before.
- **A shared window** (the 5-hour, the all-models weekly) follows the account
  wherever the model goes, so a switch buys nothing. Here the lever is
  **effort**: `/effort medium` measured six times cheaper a turn than ultra on
  this account. `node scripts/usage.js --recommend` names both levers with the
  commands.

**The commands differ by host, and the wrong one does nothing.** `/model` and
`/effort` do not exist in Codex. Under Codex, change the model and effort for
the task in hand through Codex's own controls; `node scripts/lowpower.js on
--host codex --effort low --model <id>` only saves defaults for *new* sessions
and cannot change one already running. The budget line prints whichever
vocabulary the host it is running in actually understands, so use the command
it gives you rather than the one you remember.

**Check the setting against the work, not against the window.** Once there is
evidence for it, the budget line tells you what your current effort actually
costs against the cheapest level measured on this account - "ultra, measured at
6 times the cost of medium a turn (8 turns against 6)". It says this from the
first prompt, at any percentage, because a mechanical hour at the top setting is
waste at 10 per cent used exactly as much as at 80; the only difference is that
at 80 somebody notices.

It cannot judge how hard your work is. You can. So when you see it, look at what
is actually in front of you and reach for one of three levers, saying which in
one line. Two of them are yours to pull; the first is not.

1. **Drop the effort** for that stretch - a rename, a docs pass, running tests,
   applying a fix you have already worked out. `/effort` and `settings.json` are
   the user's own baseline, so this one you **offer**: name the command, say why
   the stretch does not need the tier, and leave the pulling of it to them.
2. **Hand the stretch to a cheaper model.** Your own model is the user's setting
   too, so say that in one line rather than switching - but the model on
   anything you SPAWN is entirely yours: an Agent call takes a model, and a
   Workflow's `agent()` takes a model and an effort. Size those to the stage.
3. **Do less of it at this setting** - a fan-out multiplies the setting across
   every agent, so six agents at ultra is six ultra turns, not one. Yours.

Put it back when the work gets hard again. The question is asked once per
setting per session, not every prompt, and never at all unless there is a real
measured comparison behind it - a ratio from a price list would have you drop
effort on a hunch and call it evidence.

**This is worth raising early, not only at the wall.** Say it whenever the
current setting is dearer than the work in front of you needs, long before any
window is tight: a mechanical rename, a docs pass or a mass find-and-replace
does not need the model and effort a hard design decision does. An agent that
only ever reads this as a wall notice runs every trivial turn at the top setting
and then wonders where the window went.

**And "offer it" is one line, not a stop.** Naming the lever and carrying on is
the whole action. Waiting for an answer before doing the work would cost more
than the tier ever did.

The budget line does this arithmetic for you. Once the binding window is half
gone it says which lever applies, and at the wall it says outright that you are
not out of budget and must not stop as though you were. When it does, the
sequence is: say in one line which command frees it and why, and carry on with
the whole request at full quality. A per-model weekly is not the account's
budget, and treating it as one is the error.

This is written down because it was got wrong. A session ended with the Fable
weekly at 89 per cent and the line saying the budget was nearly gone - while the
5-hour sat at 46 and every other model on the account was untouched. One command
would have carried it on, and naming that command costs a line. Stopping there
was not caution; it was quitting with a reason that sounded like one.

Only when the switch is genuinely unavailable - no other window has room, or the
user has ruled it out - does the checkpoint below apply.

### /low-priority: the user's lever, never yours

Claude Code has a hidden toggle, `/low-priority`, offered when the 5-hour session
limit is reached. It keeps the session working at reduced priority and spends the
**weekly** limit, plus a separate weekly lower-priority allowance; replies can
pause while it waits for spare capacity.

**You cannot switch it on.** You cannot type a slash command, and the command is
declared `supportsNonInteractive: false`, so it does not work in a headless or
relayed run either. What you may do is say, in one line, that it exists and what
it costs - and only when the budget line has already said so, because the line is
the only thing that knows whether this account is provisioned for it at all.
Never volunteer it otherwise: telling a user to run a command their account does
not have is worse than saying nothing.

Three rules when the line does mention it:

- **Word it as a possibility.** The offer is gated on an experiment arm that
  arrives in a response header, and the CLI also withholds it during a cooloff
  and once the weekly allowance is spent. "If the wall offers it", not "run it".
- **Never invent a wait time.** The retry interval and its ceiling come from the
  server on each response. There is no fixed number.
- **If the line says not to, say not to, and why.** Above 80 per cent weekly it
  is the wrong move: it spends the window that takes days to come back in order
  to save one that comes back in hours.

If the user tells you they have switched it on, the honest answer is to record
it: `node scripts/mode.js --low-priority on`. From then the budget line brakes on
the weekly instead of the 5-hour window, stops telling you to wind down at the
5-hour wall, and the relay stops booking a wake for a reset this session no
longer stops at. **Record it only when they said so.** Whether it is running is
in the CLI's process memory and readable nowhere, so nothing here may infer it,
and `mode --low-priority off` is how it is taken back.

The same applies to `/limit-reset`, the manual reset: only the user can type
it. The line names it only when the account's flags say it is set up. The
once-a-week kind resets the 5-hour limit and its work still counts toward the
weekly, so it is named only at a 5-hour wall; whether this week's is already
used, and how many of the counted kind are left, is not knowable from here.

And if the budget line says Claude Code is injecting its own wrap-up note at this
wall, follow that note: it is more specific than anything here, and two
instructions to wind down in different words is worse than one.

## 6. Checkpoint before the wall

When the binding window is under roughly 10 percent, or under about ten turns
of headroom, keep working and start keeping the work landable:

1. Commit or otherwise save the working state, at every clean boundary rather
   than once at the end.
2. Keep `HANDOFF.md` current as you go: what is done, what is next, which files
   are mid-change, what the next session should read first.
3. Say when the window resets, as a clock time and not just a duration, plus
   what to run on the way back in.

The point of the handoff is that it costs almost nothing and removes the reason
to stop early. With one in place, being cut off loses a turn instead of an
afternoon, so there is no longer anything to buy by winding down.

The one thing not to economise on is the handoff itself. Everything else can be
picked up next session; a session that ends without one cannot.

## 7. The relay: when the handoff picks itself up

If a relay is armed, the budget line says so, and the shape of the last hour
changes. The handoff stops being a note for a person to find and becomes the
prompt this conversation will be handed back a few minutes after the window
reopens. So do not wind down, do not narrow the request, and do not stop to
ask whether to carry on — write the continuation properly and keep working
until the window actually ends.

Write it with:

```
node "$CLAUDE_PLUGIN_ROOT/skills/usage-limits/scripts/relay.js" note "<text>"
```

Write it to be **acted on**, not read: what is done, what is next in order,
which files are mid-change, what must be verified before anything is built on
it. It is delivered as a prompt, so an instruction beats a summary. If nothing
is written, the relay falls back to the outstanding todo list, which is worse.

More than one session can be armed at once; each wakes on its own task, and
cancel takes down only this session's unless --all is given. Arming also
answers the two start-up questions (folder trust, bypass permissions) in
.claude.json for the folder it will resume in, so the window does not stop at
a prompt; doctor says whether they are answered.

**It arms at the end of a reply, not in the middle of one.** Crossing the
threshold no longer schedules anything by itself: the relay waits for the reply
to finish, so what it carries is work that reached a boundary rather than a
snapshot of an interruption. Past the backstop (95 per cent by default) it stops
waiting and arms anyway, because a completion that never comes - the limit cut
the reply off mid-sentence - is a relay that was never armed at all. That is
what "waiting for this reply to finish before arming" means when the budget line
says it, and it is not an error. `relay armon threshold` restores the old
behaviour.

**Being offline is not failing.** Before it launches anything the wake checks it
can actually reach the API, and a machine that cannot is held, not spent: it
retries on a backoff for hours rather than burning the relay on a launch that
could not work. This exists because it happened - a relay woke on time, said
`SSL certificate hostname mismatch` 1.5 seconds later, recorded a failure and
deleted itself, and a night's work was lost to a router being off. A failed
launch is also classified now: the network and a busy service buy another
window, an invalid key or a missing CLI does not, because retrying those would
waste the window and saying "retrying" would be a lie.

Run `relay doctor` before trusting it with anything. It checks the things that
fail silently hours later - a CLI that moved, a permission mode nobody set, a
machine whose power plan forbids wake timers, a scheduled task this account
cannot register, no continuation written, no network - and says which would
bite. Every resumed run's full output is kept: `relay log --run`.

An arm that fails says which route failed and why: the ScheduledTasks route
and the schtasks fallback are named side by side, since on 2026-09-20 only the
fallback's refusal was reported and the real failure - PowerShell timing out
while its module loaded - was never seen. The task runs a small launcher in
the config directory (`relay-task-<id>.cmd`), so the action fits schtasks
whatever the plugin path. The doctor also reports whether a login is there to
resume under; when it expires is not checked, so renew `/login` before a
relay that fires hours later.

The budget line's standing instruction - open with the fit line, quote the
binding window, close finished work with the total - is said in full once per
session and as twelve words after; it is the same instruction. When two
account readings disagree by more than five points the line names both rather
than one, and on the prompt right after a prompt-cache miss you caused it says
so in one clause.

The relay is off unless the user turned it on, and it only arms while there is
an unfinished todo list or an approved plan to carry. Do not turn it on for
them, and do not promise behaviour it does not have:

- It **cannot** type into a terminal or an editor. Computer Use refuses to send
  input to a shell on purpose; the relay uses it only to tell whether somebody
  is at the keyboard, and to show a banner.
- In `notify` mode — the default — it raises a notification and starts nothing.
- The resumed run is a real interactive session in its own window, with Remote
  Control on (named `usage-limits relay <project>` on claude.ai/code and the
  phone), and its first prompt points it at the hand-off file. `relay show off`
  makes it a headless `claude -p` run instead; the output is kept either way.
  `relay fresh on` makes the wake start a **new** conversation instead of
  resuming the old one: `claude` in the project with the whole hand-off as its
  first prompt, named `usage-limits relay <project> (new session)`. Off, the
  default, it resumes the same conversation. `defer` fires through the same
  wake, so the same settings decide what a deferral does.
  macOS and Linux open the same window in Terminal (unverified there). A saved
  continuation counts as work to carry, so a session with a note but no todo
  list still arms; and a wake that never reports back is reaped as "lost".
- In `resume` mode it runs the CLI itself. A headless resume does **not**
  inherit the session's permission mode, so unless one was set the resumed run
  will sit waiting for an approval nobody is there to give.
- Claude Code's own `autoContinueAtUsageLimit` is better wherever it applies,
  because the process never dies. It does not apply to `-p` runs, background
  sessions, or a terminal that has been closed.

`node scripts/relay.js` with no arguments reports all of it.

## Voice

The plugin keeps a small local profile of how the user writes — counters, plus
at most two short lines of their own text — so that anything written *as* them
sounds like them. It costs no model call and never leaves the machine.

Two separate things live there and they are not the same:

- The **learned traits** are for writing as the user. Today that is the relay
  prompt. Do not imitate them in your own replies.
- The **instruction** they typed at `/usage-limits:voice set` is how they want
  to be talked to. It appears in the budget line and it applies to you.

If asked what it knows, run `node scripts/voice.js` and read it back verbatim,
including the kept lines. `forget` deletes it outright.

## Codex, seen from Claude Code

When Codex is installed on the same machine, every display shows its meter
underneath Claude's: the panel, the status line, the budget line before each
prompt, the VS Code view and `check`. It is read from the rollouts Codex has
already written — no child process, no network, and nothing at all if Codex is
not installed.

**It counts the other way, and that is not a bug.** Codex writes what it has
*spent* but shows what is *left*: its own status card prints "82% left" where
Claude Code prints "62% used". So the Codex rows report what remains, their
bars drain as they are spent where Claude's fill, and every figure carries the
word "left" so the two can never be read as the same kind of number. The
colours turn at the same real moment either way — 80% used is 20% left is
yellow, 90% used is 10% left is red.

There is no mark beside it, only the word "Codex" in OpenAI's green. Codex has
no mark of its own — it uses OpenAI's Blossom, and there is no Blossom codepoint
in Unicode, so a terminal cannot draw one. The nearest rosette is a flower, and
a flower in the slot where a logo should be is not the logo; the word is
unambiguous and cannot come out as something else in a font that has never heard
of it.

## Running under Codex

One difference that matters for the budget modes. Every entry in Codex's
`hooks.json` carries an `additionalContextLimit` - a per-hook cap on how much
context a hook may inject, which Claude Code has no equivalent of. A long
briefing can therefore be truncated there without a word. If a line looks cut
off under Codex, that is why: `node scripts/mode.js max` keeps it to one line,
and `high` is the verbose one.


Everything above works the same. The numbers come from a different place and
one thing about how they arrive is different, and both are worth knowing.

Codex writes its session rollouts to `~/.codex/sessions`, one JSON object per
line, and every model request appends a record carrying both the account meter
and what that request cost in tokens. So the two things this skill needs, the
percentages and the pace, come out of the same files. Nothing is sent anywhere
and no credentials are read.

```
node scripts/usage.js --host codex
node scripts/usage.js --host codex --refresh
```

`--refresh` asks Codex itself for a live reading instead of the newest one it
happened to write. It starts a short-lived `codex app-server`, takes about a
second, and is the Codex equivalent of running `/usage` in Claude Code. Use it
when the report says the snapshot is old, not routinely.

The difference that matters: **the budget line is not automatic until you say
so.** Claude Code lets a plugin ship hooks, so it gets one on install. Codex
does not load hooks from a plugin (`plugin_hooks` is a removed feature), and it
runs the ones in `~/.codex/hooks.json` only after a one-time review it shows
when `codex` starts in a terminal: "Hooks need review - Trust all and
continue". The desktop app never shows that review, so a machine using only
the app can have the hooks installed for weeks and never run them once.
`install-codex-hook.js status` says whether they have ever run.

What replaces it is an instruction, installed by:

```
node scripts/install-codex-hook.js on
```

That writes a marked block into `~/.codex/AGENTS.md` saying to run the report at
the start of a substantial piece of work, and it stages the hooks for the build
that runs them. `status` says what is installed, `off` removes both, and neither
touches anything else in those files.

So under Codex, read the budget deliberately rather than waiting to be told it.
Once at the start of a piece of work, and again if the job grows or starts
looping. The rest of this skill applies unchanged.

The report has no money column under Codex. Codex meters a share of an
allowance and never quotes a price, so the percentages are exactly what they
say and there is no dollar figure to attach. `scripts/lowpower.js` is for Claude
Code only: it writes Claude's `settings.json`, so it must not be run under
Codex. Change model or effort through Codex's own controls instead.

### The effort setting is the thing that empties the window

On Codex this matters more than anywhere else, because the reasoning effort is
set in `~/.codex/config.toml` and then applies to everything until it is
changed:

```toml
model = "gpt-6-astra"
model_reasoning_effort = "ultra"
```

A percentage and a turn count do not warn you about that, and it is the single
most common way an allowance disappears. The headroom figure is built from what
a turn has cost *on average*, and the average is dominated by whatever effort
you were running last week. Move to a dearer one and every estimate is too
generous until enough expensive turns have landed to drag the average up — and
on a five-hour window on Plus there is no "enough", because the window is gone
first. One ordinary task at `ultra` on Astra can take the lot while the report
still says there is room.

So the report measures each effort separately and prices the window at the one
actually set. Two things surface it:

- `node scripts/usage.js --host codex` prints **what each effort costs,
  measured on this machine** — turns, output written per turn, and a `*` on the
  one in force.
- When the current effort is materially dearer than a cheaper one on record,
  the budget line says so outright, with what the window really holds at this
  setting rather than at the blend.

The comparison is on **output tokens per turn**, not cost per turn. Cost per
turn mostly tracks how big the context happened to be — measured that way,
`low` turns on a huge context can look dearer than `ultra` ones on a short one,
which is exactly backwards. Output is the part the effort setting controls.

Act on it the same way as everything else here: keep the high effort where the
work genuinely needs the thinking, and drop it where it does not. It changes
what every turn costs, not how many turns you get.

## When to skip this skill

Do not run the report on every prompt. Once at the start of a long piece of
work, and again if the job grows or something starts looping. The report costs
a turn, which is the thing it is trying to save.

The panel (`scripts/panel.js --open`, or `/usage-limits:panel`) and the status
line (`scripts/statusline.js on`) are for the person watching, not for you.
Nothing in them changes what you should do, and they draw from the same
reading the budget line already gave you, so do not open or install them
unless asked. When asked, run the command, say in one line what it did, and
stop.

## Files

| Path | What it is |
| --- | --- |
| `scripts/usage.js` | The report. `--json` for raw fields, `--status` for a one-line readout that skips the transcript scan, `--forecast N` for what an N turn job would cost, `--sessions` for what recent sessions cost, `--session last` (or an id) for one session in full, `--host codex` to read Codex's limits, `--refresh` to ask Codex for a live figure. |
| `scripts/brief.js` | What the hook runs before each prompt. Not meant to be called by hand. |
| `scripts/pulse.js` | What runs after tool calls, to re-check the budget during a long turn. Not meant to be called by hand. |
| `scripts/stop.js` | What runs after each reply: shows the user what the reply and the session have cost. Not meant to be called by hand. |
| `scripts/sessionend.js` | What runs when the session closes: the closing line, and the session marked closed in the history. Not meant to be called by hand. |
| `scripts/tally.js` | The running per-session total behind those two, kept in `usage-limits-sessions.json` and read incrementally. |
| `scripts/host.js` | Works out which agent this is running inside, so one host's percentages are never reported against the other's turns. |
| `scripts/codex.js` | The Codex reader: the meter and the pace out of `~/.codex/sessions`, plus the live `--refresh` call. |
| `scripts/install-codex-hook.js` | `status`, `on`, `off`. Installs the Codex-side instruction, which Claude Code does not need. |
| `scripts/mode.js` | The budget mode: no arguments to report it, `max`/`high`/`standard`/`off` to set it, `auto`, `off --guard 95`, `--list`, `--explain <name>`, `--floor`/`--ceiling`/`--pin`, `--baseline`, `--advice`/`--no-advice`, `--history`, `undo`, `--ledger`, `--low-priority [on|off]`. Reads settings.json and never writes it. |
| `scripts/lowpower.js` | `status`, `on`, `off`. Restores what it replaced. Claude Code only. |
| `scripts/recommend.js` | The chooser behind `usage.js --recommend`: posture, then the effort and model commands for each lever. Not meant to be called by hand. |
| `references/tactics.md` | Every lever that lowers cost, and why it works. |
| `scripts/panel.js` | The live panel beside the chat: `--open` puts it in a split pane to the right, `--once` prints one frame, `--json` the fields. For the person, not for you; open it only when asked. |
| `scripts/statusline.js` | `status`, `on`, `off`. Puts the bars under the prompt and restores what was there. |
| `scripts/feed.js` | The status line command Claude Code runs. Not meant to be called by hand. |
| `scripts/live.js` | The usage reading itself, taken the way Claude Code takes it for `/usage`, kept in `usage-limits-live.json` where `collect()` prefers it when newer than the cache. |
| `scripts/drift.js` | How wrong the reading was: each correction written down against the one it replaced. Run it with no arguments for the median and worst gap measured so far, `--json` for the fields. Answer "how far behind does this plugin actually run" from here rather than from memory. |
| `scripts/view.js`, `scripts/bars.js`, `scripts/activity.js` | The display model, the drawing in Claude's colours, and the working/idle marks the hooks leave for the panel. Not meant to be called by hand. |
| `scripts/relay.js` | The relay: `status`, `on`/`off`, `at N`, `grace N`, `mode notify\|resume`, `permission MODE`, `thinking off\|resume\|always`, `armon threshold\|completion`, `backstop N`, `show on\|off`, `fresh on\|off`, `onfailure rearm\|stop`, `rearms N`, `offline N`, `doctor`, `note "<text>"`, `cancel`, `log [--run]`. |
| `scripts/net.js` | Can this machine reach the API, and was a failed run the network's fault. Three probes, TLS-interception detection, and the backoff the offline retries use. |
| `scripts/wake.js` | What the scheduler runs after the reset: re-checks the meter, then notifies or resumes. Never called by hand. |
| `scripts/voice.js` | The local writing profile: `show`, `card`, `set "<instruction>"`, `clear`, `off`/`on`, `forget`. |
| `scripts/lowpri.js` | What Claude Code's own features at the wall are readable as: whether this account is provisioned for `/low-priority`, whether a manual session reset grant exists, whether the CLI injects its own wrap-up note here, whether usage credits are available, the cloud-session credit on offer and whether this is a cloud session, whether `autoContinueAtUsageLimit` is on, and the record of the user saying they switched low-priority on. Reads only; never writes anything but that one record. |
| `references/how-it-works.md` | Where the numbers come from and where they are soft. |

## Codex controls

Under Codex, use `node scripts/lowpower.js on --host codex --effort low` to save defaults for new sessions, optionally adding `--model <supported-model-id>`. `off --host codex` restores them; `--dry-run` previews them. These writes cannot change an active task. Use host controls for its current model and effort; do not prescribe Claude models or /effort in Codex. Headroom is an estimate shared with other account activity, not reserved capacity.
