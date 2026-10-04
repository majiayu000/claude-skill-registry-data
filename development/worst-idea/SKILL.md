---
name: worst-idea
description: Worst Possible Idea (reverse brainstorming) — deliberately design the most terrible solutions to the problem, name the mechanism that makes each one bad, then invert those mechanisms into strong features. Use when ideas all feel timid and safe, when the team is optimizing instead of imagining, or for "worst idea", "reverse brainstorming", "what would make this worse", "design the disaster", "how would we guarantee failure". Do NOT use for analytical work like debugging, code review, or implementation tasks.
---

# Worst Possible Idea

## What this technique does

Ask for the *worst* solution to the problem, not the best. Design solutions that would reliably make things terrible, then dissect each one to find the exact mechanism that makes it bad. Invert that mechanism, and you have a feature. The move works because "what's the best design?" routes through everyone's inhibitions and lands on the safe, obvious answer, whereas "how would we guarantee failure?" removes the fear of being wrong and lets people say things out loud — and every named failure mode is a design principle wearing its opposite.

Source: reverse brainstorming, attributed to Hotpoint's product development practice in the 1950s, and standard in the d.school/IDEO facilitation toolkit as "Worst Possible Idea."

## Workflow

### Step 1: Confirm the target

A valid target is a concrete creative problem stated as something to design or reinvent: an onboarding flow, a pricing page, a landing page, a naming direction, a ritual the team runs. If the target is unclear, ask one focused question — "What are we designing, and what would 'good' look like?"

Refuse requests to *perform* analytical work — debugging, reviewing code, implementing a change — and suggest an analytical approach instead. Redesigning or ideating about such a process is a valid creative target: "reinvent our code-review ritual" is in scope; "review this PR" is not.

### Step 2: Generate genuinely terrible solutions

Produce 5–8 solutions that would make the problem *worse*. The bar is high: each one must be plausible enough that someone, somewhere, has actually shipped it. Cartoon evil ("delete the user's files!") is too easy and teaches nothing. The useful terrible ideas are the ones a real team rationalized its way into — the ones that sound almost defensible in a meeting.

Show them plainly. Do not soften them, and do not pre-apologize for them.

### Step 3: Isolate the mechanism of badness

For each bad idea, state in one sentence *why* it is bad — the mechanism, not the symptom. Not "it's annoying" but the structural reason it fails.

> Example: "it's bad because it makes the user prove value to the product, not the reverse."

The mechanism is the whole technique. A bad idea with no articulated mechanism is just a bad idea.

### Step 4: Invert the mechanism, not the idea

Flip the *mechanism* into its opposite. This is not "don't do the bad thing" — that only gets you back to neutral. Inverting the mechanism produces a positive design principle.

> Bad idea's mechanism: "it makes the user prove value to the product."
> Inversion: "make the product prove value before asking anything of the user."

Inverting the surface ("so, don't make users prove value") is the common failure. Invert the underlying force.

### Step 5: Develop the inversions

Take the 2–4 strongest inversions and push each into a concrete direction — an actual feature, layout, flow, or line of copy. An inverted mechanism is a principle; a direction is something you could build on Monday.

### Step 6: Meta-pattern scan

The mechanisms of badness cluster. Read them side by side and name the cluster out loud: it is a map of what this thing must *never* do. Often three or four separate terrible ideas turn out to be the same underlying sin in different costumes. State that sin explicitly — it is usually the sharpest output of the whole session.

### Step 7: Honest ranking, no closure pressure

Rank the surviving directions. Say which are strong, which are thin, and why. Offer next moves — develop one further, generate a fresh batch of terrible ideas, switch technique, or stop. Never push the user to commit.

## Honesty mechanics

**The secretly-clever disqualification.** Sometimes a "worst idea" turns out to be quietly good — a real business model or a legitimate feature in disguise. When that happens, the idea has failed *as a worst idea* and must be disqualified and replaced with a genuinely terrible one. Say so out loud:

> "charge per bug report" is actually a support-tier pricing model in disguise — too good, replacing.

This keeps the batch honest. If nothing in the batch makes you wince, the batch is fake.

**Dead mechanisms.** Not every mechanism inverts into something useful. Some flip into the blandly obvious, or into a principle you already follow, or into nothing at all. Show at least one dead — invert it, look at the result, and declare it dead rather than dressing it up. A batch where every mechanism yields treasure is a tell that the output was reverse-engineered from the answers.

**When the batch itself fails.** If most mechanisms invert into principles you already follow, the technique has told you something real: this thing is not failing for lack of imagination, and more terrible ideas will not help. Name the diagnosis, suggest the technique that fits it as the user's next move, and stop there — do not run it yourself:

- The inversions are all things you already do → the design is sound and the question is elsewhere. Suggest `concept-fan` to check you are solving the right problem.
- You cannot generate a terrible idea that anyone would actually ship → the target is too small or too abstract to have failure modes. Suggest `random-stimulus` for generative range.

## What NOT to do

- **Don't sanitize the terrible ideas.** The wince is the signal. If a bad idea is genuinely uncomfortable, keep it uncomfortable — the softened version teaches nothing.
- **Don't invert the surface.** "Don't do X" is not an inversion of X; it is the absence of X. Invert the *mechanism* underneath X into a positive force.
- **Don't skip the mechanism step.** Jumping straight from bad idea to good idea skips the only part that does work. The mechanism IS the technique; without it you are just guessing at features.
- **Don't force every mechanism to pay off.** Show the dead ones dead.
- **Don't push the user toward a decision.** The technique is divergent; convergence belongs to the user.

## References

- [`./references/worked-example.md`](./references/worked-example.md) — a real session showing the full shape, including a dead mechanism and a disqualified idea
