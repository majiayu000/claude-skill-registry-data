---
name: evidence-ladder
description: >-
  Weights a pile of "validation" by what people DID, not what they said. Takes
  interview quotes, sign-ups, LOIs, pilots, payments and places each on one
  ladder — money moved 1.0, behaviour observed 0.7, artefact shown 0.5, verbal
  commitment 0.3, opinion 0.1 — then returns a weighted evidence table, the
  weight of the load-bearing claim, and for every low signal the cheapest probe
  that raises it a rung. Fires on "how strong is this signal", "score the
  interview", "did they actually validate", "weight this evidence", "is this
  real validation". NOT a build gate on a problem (use problem-quality-scorecard),
  NOT a picker for which test to run next (use probe-matrix), NOT a transcript
  summary (use summarize-interview). This is the reference skill the rest of the
  module cites for the ladder.
type: generator
supersedes: none
---

## What it does

Takes a pile of things a fellow is calling "validation" — quotes, landing-page
sign-ups, letters of intent, paid pilots, payments — and weights each one by what
the person actually did, on a single five-rung ladder. It returns a filled table
(claim → rung → weight → the observation behind it → the probe that raises it),
the weight of the one load-bearing claim, and a one-line honest read. Its job is
to stop a founder mistaking a wall of enthusiasm for evidence.

## The Icarus reframe

Every discovery signal is weighted by what a person DID, not what they said:
money moved (1.0) outranks a behaviour you observed (0.7), an artefact they
already made (0.5), a verbal promise (0.3), and a bare opinion (0.1). Rungs do
not stack — fifty people saying yes is still 0.3, because the only thing that
raises a claim is one signal at a higher rung, not more signals at the same one.
So a fellow's confidence should track the rung of the load-bearing claim, not the
volume of enthusiasm — and for every low-rung signal the ladder names the single
cheapest probe that would move it up.

## When to use / When NOT

Use it when a fellow holds evidence already and wants to know how much it weighs:
after interviews, after a landing page, after "they said yes", before writing
"validated" in a deck.

Do not use it for these — hand off instead:

| If the fellow wants… | Use instead |
|---|---|
| A build/no-build decision on one problem, scored to a gate | `problem-quality-scorecard` — it gates a problem; this weights loose signals |
| To pick which test to run next | `probe-matrix` — this skill hands it the "reach rung R" target; it picks the probe |
| A transcript turned into a structured summary | `summarize-interview` — it extracts; this weights |
| The five qualitative whole-idea questions | `so-what-stress-test` |
| To turn a solution back into a weighable claim | `problem-statement`, then return here |

`problem-quality-scorecard` *uses* this ladder as a ceiling on each of its eight
dimensions. This skill *is* the ladder: it weights any pile, gates nothing, and
picks no probe.

## Method

Fill in `template.md`. Six steps.

**Step 1 — List every signal, one per row.** For each, write the claim it
supports and *what the person physically did*. If the only honest thing you can
write is what they said or felt, write that — it will land low, and that is the
point. If the pile is empty — no signals at all — ask the fellow for signals and
stop: emit no headline score and invent nothing. A ladder with nothing on it is a
request for evidence, not a zero.

**Step 2 — Place each signal on the ladder.** The rung is set by the action, not
the wording. Downgrade every impostor.

| Rung | Weight | Counts only when | Common impostor → downgrade to |
|---|---|---|---|
| Money moved | 1.0 | cash or budget actually changed hands — invoice paid, deposit, pre-order, paid pilot | a signed LOI or quote with no payment → Verbal 0.3 |
| Behaviour observed | 0.7 | you saw them do it (or hold the logs); it cost them time, effort, or switching; unprompted | a self-reported routine you did not witness → Verbal 0.3; a free one-click sign-up → Verbal 0.3 |
| Artefact shown | 0.5 | they showed you a thing THEY made or use — a spreadsheet, a workaround, their permit log | a reaction to a mockup YOU made → Opinion 0.1 |
| Verbal commitment | 0.3 | a specific promise about the future — "I'd pay $X", "we'd switch by Q3" | vague praise ("great idea", "we'd love that") → Opinion 0.1 |
| Opinion | 0.1 | a view, a feeling, a prediction — "I think", "everyone needs this" | — floor: never below, never above |

The Artefact/Behaviour line: a log or artefact they *actively use in the
workflow* is behaviour (0.7); a static doc they made once and set aside is
artefact (0.5). What they do with it, not that it exists, sets the rung.

**Step 3 — Weight each claim by its BEST rung, never the sum.** A claim's weight
is the highest rung any of its signals reaches. Duplicates at the same rung do not
add: three verbal yeses is 0.3, not 0.9. The only way up is a signal at a higher
rung.

**Step 4 — Mark the ONE core claim and report the headline.** Exactly one claim is
load-bearing — usually "the target will pay for / adopt this". The headline
weighted score is that claim's weight. Do **not** average the pile: a mean lets one
payment launder a stack of opinion. Instead report a coverage tally — how many
distinct claims sit at behaviour-or-money (0.7+), how many are opinion-only (0.1).

**Step 5 — For every signal below 1.0, name the cheapest probe that reaches the
next rung.** Then hand the "reach rung R" target to `probe-matrix` to select the
specific probe.

| Signal now at | To reach | Cheapest probe |
|---|---|---|
| Opinion 0.1 | Verbal 0.3 | a direct, specific ask — "pre-order at $X today?"; costs one sentence |
| Verbal 0.3 | Artefact 0.5 | ask them to show or send what they use for this now |
| Verbal 0.3 | Money 1.0 | a paid concierge, pre-order, or deposit — skip the middle rungs, go straight to cash |
| Artefact 0.5 | Behaviour 0.7 | wizard-of-oz or fake-door — put the workflow in front of them and watch |
| Behaviour 0.7 | Money 1.0 | concierge with a price on it — do the task by hand, charge for it |

**Step 6 — Write the one-line honest read.** Format: "You have [rung]-grade
evidence for [core claim]. Cheapest way to make it [next rung]: [probe]." If the
pile is mostly opinion, say so plainly and name the gap.

## Evidence standard

This skill is the evidence standard the module runs on. The bar it enforces:
the headline equals the rung of the core claim's best *real* signal; opinion never
exceeds 0.1; stacking never raises a rung; a written promise, a free sign-up, and a
self-reported routine are not money or behaviour. Tag every empirical claim
`[Fact]`, `[Assumption]`, or `[Hypothesis]`. Kill line: scoring an opinion above
0.1 fails the skill.

## Gotchas

- **Stacking enthusiasm.** Ten yeses at 0.3 is still 0.3. Volume is not a rung.
  If the total climbed because more people said the same thing, you inflated it.
- **Their reaction to your demo, counted as their artefact.** "They loved the
  mockup" is the person reacting to a thing YOU made — opinion, 0.1. Artefact-shown
  means a thing THEY built or use, which reveals real behaviour.
- **LOI or signed quote, counted as money.** A written promise with no payment is
  a promise on paper, not money moved — 0.3. Only cash or redirected budget is 1.0.
- **Free sign-up, counted as behaviour.** A one-click email capture with no cost
  and no follow-through is an expression of interest — 0.3. Behaviour earns 0.7
  only when the action cost the person something.
- **Self-report, counted as observed.** "It takes me two hours every Monday", if
  you did not watch it or hold the logs, is verbal — 0.3. Observed behaviour needs
  eyes or data.
- **Averaging the pile.** A blended mean is how one payment hides a stack of
  opinion. Report the core claim's weight plus the coverage tally, never an average.

## Examples

`examples/sample.md` — a worked Barrier Intelligence pile: a paid rig pilot, a
field engineer's permit log, forty landing-page sign-ups, and two supervisors who
"love the alerts". Shows the downgrades, the headline pinned to the core claim, the
coverage tally, and the probe named for the one claim that is still only opinion.

## Related skills

Supersedes nothing; it formalises the ladder that Wave-1 already used informally.
Absorbs the signal-extraction shape of `summarize-interview` (pull the signal out
of the noise) and beats it on one axis: `summarize-interview` records what was
said; this weighs what it is worth and refuses to let a said-thing pass as a
done-thing.

Cited by: `problem-quality-scorecard` (uses these rungs as per-dimension
ceilings), and every probe skill (a probe's whole job is to move a claim up this
ladder). Composes with `probe-matrix` (hand it the target rung; it picks the
probe), the four probe runbooks (`paper-sketch-probe`, `wizard-of-oz-probe`,
`concierge-probe`, `agent-concierge-probe`), and `problem-statement` (reframe a
solution-in-disguise into a weighable claim before scoring).
