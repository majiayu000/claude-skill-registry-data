---
name: concept-council
description: First-contact teardown of a raw product idea. Fires when a fellow says "here's my idea", "tear this apart", "rip this concept apart", "what am I missing", or "what should I build first". Convenes five adversarial lenses, names the one load-bearing gap, and returns a Gap Map plus one First-Probe Brief costing under a week. NOT for an already-scoped concept you want stress-tested against the five so-whats (use so-what-stress-test) or scored numerically across eight dimensions (use problem-quality-scorecard).
type: interactive
supersedes: none
---

## What it does

Takes a raw, unproven idea and returns one decision: the single cheapest test to run this week. It convenes a five-lens adversarial panel, forces each lens to land its hardest single attack, ranks those attacks by how much of the idea they kill, and collapses the pile into one load-bearing gap and one probe. The output is a filled Gap Map plus a First-Probe Brief. It is the first thing a fellow runs when a concept is still a sentence, before any problem statement or PRD exists.

## The Icarus reframe

Generic brainstorming adds ideas; a SWOT lists strengths and weaknesses in parallel and stops. concept-council does the opposite: five adversarial lenses — Skeptic, Buyer, Incumbent, Engineer, Regulator — each return their single hardest attack, and a Synthesiser ranks those attacks by likelihood-the-attack-is-right times damage-if-right, names the one load-bearing gap (the single assumption that, if wrong, sinks the whole idea), and hands back exactly one probe you can run this week to test it. It is a teardown that ends in one action, not a list; if it gives you more than one thing to build first, it has failed.

## When to use / When NOT

Use it when the idea is still one sentence and unattacked. Use it before `problem-statement`, before any PRD, before you have picked a segment.

Do not use it for:

| If the fellow wants… | Use instead | Why not this skill |
|---|---|---|
| The five so-what questions run on an already-formed concept | `so-what-stress-test` | That interrogates a stated concept; this tears down a raw one and ends in a probe. |
| A numeric score across eight problem dimensions | `problem-quality-scorecard` | That grades; this does not score the idea, it finds the one gap and tests it. |
| The unit-cost physics floor of a claim | `physics-floor-gap` | That is a cost-teardown, not a five-lens attack. |
| A written PRD or spec | `prd-development`, `one-pager-prd`, `create-prd` | This runs upstream of any spec. Decline and point there. |

## Method

Fill `template.md` as you go. Do not skip the ranking. Do not return more than one probe.

### Step 1 — Restate the concept in one sentence

Write the idea back in the fellow's own words, one sentence. If you cannot — because the input names no user, no job, or no change — ask the **one** question that unblocks it and stop. Invent no user, no number, no domain detail.

### Step 2 — Convene the panel

Each lens returns its single strongest attack. Not a list. One line. If a lens has three worries, it must pick the one that does the most damage and drop the rest.

| Lens | The one question it must answer | Attack lands as |
|---|---|---|
| Skeptic | Is this a real problem, or would the user not notice if it vanished? | One sentence naming why the pain may not exist or may be tolerated. |
| Buyer | Who holds the budget, and why would they not pay — or keep doing nothing? | One sentence naming the non-purchase. |
| Incumbent | Why does the obvious existing player crush this, copy it, or rationally ignore it? | One sentence naming the incumbent's move. |
| Engineer | Why is this harder, slower, or costlier to build than the pitch assumes? | One sentence naming the hidden build cost. |
| Regulator | What legal, safety, data-rights, or jurisdiction landmine kills or gates it? | One sentence naming the landmine. |

### Step 3 — Score each attack

For each attack, set two numbers and multiply. Tag the evidence you actually have.

- **L (likelihood the attack is right)**: 0.1–1.0.
- **D (damage if right)**: 0.1–1.0, where 1.0 means the whole concept is dead.
- **Load-bearing score = L × D.**

Beside each, tag your basis: `[Fact]` if you have observed evidence, `[Assumption]` if it is inherited belief, `[Hypothesis]` if it is a guess to be tested. An attack you can only tag `[Assumption]` or `[Hypothesis]` is exactly what a probe is for.

### Step 4 — Name the one load-bearing gap

The Synthesiser takes the highest L × D and states it as one falsifiable sentence: "This idea dies if [assumption] is false." Ties break toward the attack that is cheapest to test, not the scariest. Everything below the top score is noted and parked, not probed.

### Step 5 — Design the First-Probe

Design the cheapest honest test of that one gap. Constraints, all mandatory:

1. It tests **the load-bearing gap**, not a nearby easier thing.
2. It costs **≤ 1 week** and ideally near-zero dollars.
3. It moves the claim **up the evidence ladder** to behaviour (0.7) or money (1.0). A probe that only gathers opinions (0.1) is rejected — redesign it until someone has to do or pay something. Exception: a **dispositive fact-establishing probe** — one that definitively resolves the load-bearing gap, e.g. securing a data feed or getting an authoritative HSE/legal ruling that can outright kill the idea — counts as high-value evidence even though it is not a demand signal.

### Step 6 — Write the First-Probe Brief

One probe. State what it tests, the method, the cost, the pass line, the fail line, and the rung it moves the claim to. If you have written two probes, delete one. If the cost exceeds a week, the probe is wrong, not the budget.

## Evidence standard

Every attack and every probe is weighed on the ladder: money moved **1.0** > behaviour observed **0.7** > artefact shown **0.5** > verbal commitment **0.3** > opinion **0.1**. The load-bearing gap is almost always an `[Assumption]` or `[Hypothesis]` today; the probe's whole job is to move it up at least to behaviour. Done means: one gap named, one probe written, and the probe would produce a signal of at least 0.7 within a week. A probe whose best possible result is an opinion (0.1) does not clear the bar and the skill must say so.

## Gotchas

- **More than one "build first" is an auto-fail.** The point is compression to a single action. If two probes feel equally urgent, you have not finished ranking — force the L × D tie-break.
- **A probe over a week is a rewrite, not a plan.** If the cheapest honest test takes a month, you are testing the wrong gap. Find a thinner slice of the same assumption that a person can react to in days.
- **Opinion-dressed-as-evidence.** "I asked five friends and they loved it" is a 0.1. Watch for probes that quietly collect enthusiasm instead of behaviour; the ladder rejects them.
- **Lenses that fetch instead of attack.** A lens that says "we should research the market" has not attacked. Send it back until it names a specific way the idea dies.
- **Fabrication to fill a lens.** If you have no basis for the Buyer or Regulator attack, tag it `[Hypothesis]` and lower L — do not invent a regulation or a competitor to make the panel look complete.
- **Solution in disguise.** When the "idea" is really a pre-chosen solution ("we don't have a mobile app", "we need a copilot"), it names a feature, not a job. Name the trap, reframe to the underlying job the missing feature would serve, and convene the panel on that job — do not attack the feature.

## Examples

See `examples/sample.md` for a full run on Mentix ("an AI copilot for factory managers"): five lens-attacks scored, the load-bearing gap named (managers will not act on the copilot mid-shift), and one week-long shadow probe that moves the claim from opinion to behaviour.

## Related skills

- Runs **before** `problem-statement`, `so-what-stress-test`, and `problem-quality-scorecard`. It turns a sentence into one tested assumption; those refine an already-scoped problem.
- Absorbs the experiment-framing bones of `brainstorm-experiments-new` (skin-in-the-game, your-own-data, behaviour over opinion) but inverts the flow: that skill generates several pretotypes for a concept assumed worth testing; this one first proves which single assumption is worth a pretotype at all. It does not supersede it — use `brainstorm-experiments-new` once the load-bearing gap survives its first probe and you need a fuller experiment set.
- Feeds `beachhead-segment` and the wedge skills: the surviving gap and its probe result are the raw input for choosing where to aim.
