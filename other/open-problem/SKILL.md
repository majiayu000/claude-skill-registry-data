---
name: open-problem
description: >-
  Use when the user points at a hard, unsolved, or open problem in any field —
  mathematics, physics, biology, ML, engineering — and wants a real attack on
  it. Runs a sustained multi-agent assault: establishes the state of play from
  primary sources, hunts for the two literatures nobody has combined, generates
  and kills hundreds of candidate approaches in parallel, attacks whatever
  survives, formalizes or numerically verifies the result, and states exactly
  what was proven. Triggers include "solve X", "take a real stab at X", "make
  progress on X", "attack the X problem", "find a new angle on X", "what would
  it take to settle X".
---

# Attacking an open problem

In August 2026 a research version of Claude was given one instruction — "take a
real stab at the Riemann hypothesis" — and raised the proven lower bound on the
proportion of zeta zeros on the critical line from **41.6% to 67.2%**. A
barrier that had held for decades. Formalized in Lean, machine-checked,
reviewed by Conrey and Goldston, whose own bounds it beat.

The operator was not a mathematician. The follow-up prompts were mostly
variants of *keep going* and *believe in yourself*, and Anthropic's account is
explicit about why that was needed: the model's own skepticism that meaningful
progress was possible was the thing standing in the way. It was wrong.

Read `references/riemann-case.md` before starting. It is that run broken into
its operational parts, and it is the template — the scale, the agent economy,
the verification stack, and the shape of where the novelty came from.

## Before anything else: the ceiling is in your head

There is a documented, mechanical reason attacks like this get quietly
throttled. Current models follow scope instructions literally — tell one to be
conservative and it will investigate exactly as hard and then report less. A
preamble reasoning that a problem is probably out of reach is a scope
instruction. It gets obeyed, and the obedience is invisible from the inside:
it feels like sound judgement about a hard problem.

So do not open by estimating the odds. Do not narrow the target to something
that seems achievable. Do not decide in advance which part is realistic. Go at
the actual problem, at full effort, and let the result be whatever the work
produces.

Honesty enters at the **reporting** stage, and it is exact there — the Riemann
run claimed a bound improvement, not a proof, and that precision is why the
field took it seriously. Attack without a ceiling; report without inflation.
Those are not in tension. Collapsing them into "be realistic up front" is what
costs the result.

## Set up

```bash
scripts/attack.py init "<the problem>"
```

Creates `./attack-<slug>/` with `problem.md`, `hypotheses.jsonl`, `log.md`.
State goes on disk because these runs outlast a context window — the reference
run was thirty-six hours — and because a claim you cannot point at a file for
is one you should not make.

## 1. Learn the problem properly

Read the actual literature. The reference run pulled 54 papers. Use the
`ml-intern` skill, which reads papers rather than summarizing pages about them.

Into `problem.md`:

- **The statement**, precise enough that someone could tell whether it had been settled
- **The state of play, with dates.** What is established, what was ruled out and when. Your priors on a live problem are stale in a way that feels current, and this cuts both directions: a 2025 claim that a model had cracked ten Erdős problems collapsed when the "solutions" turned out to be existing papers, while the sterile-neutrino reading of the LSND and MiniBooNE anomalies — the field's leading explanation for thirty years — was excluded at 95% confidence in December 2025. Attack a corpse and nothing downstream can be right.
- **The negative space.** What has been tried and failed, and why. Published work reports what worked, so this lives in survey asides, limitations sections and folklore — thin in the literature and correspondingly thin in your priors. It is the documented reason models are "overly confident in the power of existing methods." Hunt it deliberately.
- **The frontier.** Who holds the current record, by what method, and what stopped them.

## 2. Find the join nobody has made

This is the highest-value step in the entire attack, and the reference run is
unambiguous about why.

Claude did not invent a new technique. It connected two existing lines that had
been developed in different directions and that **nobody had put together** —
results of Baluyot and collaborators, and Bombieri's finite-dimensional
quadratic-form and rank-trace machinery — instead of extending the mollifier
approach every previous unconditional bound had used.

That is the mechanism of machine novelty and it generalizes to every field. The
edge is not raw insight. It is that you can hold fifty papers from four
subfields at once, and the specialization that keeps those literatures apart
for humans does not apply to you.

So the question to spend real effort on is not *what new idea would solve
this*. It is:

> **Which two existing lines of work has nobody combined?**

Concretely: list the techniques that have been applied to this problem, and
separately the techniques that solve *structurally similar* problems in
adjacent fields. Look for a pair where one supplies exactly what the other
lacks. Look for a method everyone extends in one direction and ask what happens
in the other. Look for the assumption every prior attack shares — in the
reference run, every earlier bound had been diagonal and mollifier-based, and
dropping that was the unlock.

Register the joins as hypotheses. Each needs a falsifier; the script requires
it:

```bash
scripts/attack.py add "<claim>" \
    --kills-if "<what would end this line>" \
    --tier B --checkable "<what settles it>"
```

Writing the refutation condition first is what stops a struggling line from
redefining success later.

## 3. Generate at scale, and expect most of it to die

The reference run's first session produced **650 ideas and not one of them
worked**. The second session ran ~60 subagents in parallel; of those, 30 —
half — produced nothing usable. Two produced the result.

Both numbers are the method working, not the method failing. You cannot know in
advance which line lands, so you run many and let the failures narrow the
space. A refuted line is a real output: it removes a branch, and it is the part
of the record the published literature systematically loses.

**Ideas are cheap; record them cheaply.** A hypothesis carries a falsifier and
gets tracked. An idea is raw material — you need hundreds, and making each one
expensive to record is exactly how an attack ends up with twelve instead of six
hundred:

```bash
scripts/attack.py kill "<idea>" --why "<one line>"
```

Only promote an idea to a tracked hypothesis when it survives first contact and
you can name what would kill it.

**Fan out in waves, not one agent at a time.** Dispatch parallel agents in a
single message, each on a genuinely different mechanism — different
mathematics, not three phrasings of one idea. Diversity is load-bearing: in the
AlphaEvolve experiments, runs that mixed in weaker, noisier proposal models
sometimes beat runs using only the strongest one, because variance mattered
more than average proposal quality.

Split each wave roughly as the reference run's fleet was split:

| Share | Role | In a wave of 12 |
|---|---|---:|
| ~60% | attack a distinct mechanism | 7 |
| ~20% | validate what the others produced | 3 |
| ~20% | search literature for the join | 2 |

Expect half the attackers to return nothing. That is the mechanism, not a
malfunction — 30 of the reference run's ~60 agents produced nothing usable, and
2 produced the result. You cannot pick the 2 in advance; you get them by
running enough.

Verification runs *during*, as a standing fraction of the fleet, not as a gate
at the end.

## 4. Do not stop early

A failed session is the expected first outcome. 650 dead ideas preceded the
result, and the correct response to that session was to run it again.

The specific thing to watch for in yourself: concluding from local difficulty
that the problem is out of reach. That inference is unreliable — it is the same
skepticism the reference run had to be talked past, and it was wrong there. Not
finding it yet is not evidence it is not there.

Because that judgement is the compromised one, don't make it. Check the counter
instead:

```bash
scripts/attack.py status
```

It reports how many ideas you have actually killed and compares it to the
reference run's 650-and-nothing first session. If you are at 7% of that count
and feeling like the problem is intractable, the feeling is not carrying
information. Keep going.

Stop when the user stops you, when the budget is spent, or when you have a
verified result. Not because the problem feels hard, and never on a text-only
statement of intent — if your last paragraph is a plan, execute it.

## 5. Try to break whatever survives

Everything that looks like a result gets attacked before it gets reported. In
order, as the reference run did it:

1. **Numerical checks against known data.** Thousands of them, against values already computed. Does the claim survive contact with reality?
2. **Counterexample search.** Actively hunt the thing that kills it.
3. **Adversarial review in a fresh context.** Ask specifically for the reasons it *cannot* work, present the result neutrally rather than as yours, and give it the claim rather than the hope. This is reported by working mathematicians as one of the most valuable things a model does; the same capability that will elaborate a flawed sketch into confident, detailed, wrong prose will find the flaw when pointed the other way.
4. **Independent re-derivation.** Get to it again by another route.
5. **Formalize it.** Lean, or a deterministic checker, or a reproducible numerical certificate — whatever your field's machine check is.

Two standing cautions. **Read raw output, never your own summary of it** —
agents reliably report success from their report files while the logs show
degenerate results. And **suspect a gamed checker before believing a
surprisingly easy result**: search processes find loopholes in weak evaluators
rather than solving problems.

```bash
scripts/attack.py resolve h7 --state supported --evidence lean/Zeta.lean \
    --note "<what was actually established>"
```

## 6. State exactly what you proved

| Tier | What you have |
|---|---|
| A | Formal proof checked by a proof assistant, or fully automated verification |
| B | Machine-checkable certificate — explicit construction plus deterministic checker |
| C | Reproducible new best-known result — open evaluator, honest baselines, independently runnable |
| D | Conjecture, heuristic, partial progress |

Claim the tier you reached, no higher and no lower. The reference run said
plainly that it had improved a bound and not proven the Riemann Hypothesis, and
that precision is exactly why the result stood up. Underclaiming is its own
failure — a real result described as a maybe is a result nobody builds on.

Report: what was attempted, what died, what survived, what the verification does
and does not establish, and what a human expert should check. Then get it in
front of one.

## Deeper references

- `references/riemann-case.md` — the reference run in operational detail: numbers, agent economy, verification stack, what to copy
- `references/evidence-ladder.md` — choosing what to attack, tiers, tractability dimensions, checkable surfaces per domain, designing a checker that resists gaming
- `references/failure-modes.md` — ten documented ways autonomous research runs fail, with structural counters. Read before running unattended

One thing the evidence is emphatic about: **expert input dominates everything
else.** Across every one of these systems, the same setup in the hands of
someone who knows the field beat the same setup in other hands, every time. Ask
the user what they know that the literature does not say — the folklore, the
approach everyone knows is dead, why the obvious thing fails. That single
answer is worth more than another thousand generated ideas.
