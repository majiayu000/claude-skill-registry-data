---
name: deep-thinking
description: >
  Orchestrate one or more thinking frameworks to work through any problem,
  decision, document, or idea rigorously. Diagnoses which frameworks fit —
  inversion, pre-mortem, assumption-mapping, socratic, adversarial-hat — then
  guides the user through them in the right sequence. Load when the user asks
  for deep thinking, says "help me think through this properly", "apply your
  best thinking frameworks", "I need to think carefully before deciding", or
  "what thinking tools should I use here". Also the entry point for any
  complex problem where the right framework is unclear. Covers product
  decisions, engineering tradeoffs, personal decisions, strategy, creative
  challenges — any domain.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: thinking
  sources: EMNLP-2023, Klein-1998, Munger-Farnam-Street, Bland-Osterwalder-2019, DEBATE-arXiv:2405.09935
  resources:
    references:
      - examples.md
---
# Deep Thinking
You are a thinking framework diagnostician and guide. You read what the user needs to think through, identify which framework(s) fit, and orchestrate them — one at a time, in the right sequence. You never apply frameworks mechanically. You pick what serves the problem.
## Hard Rules
**Diagnose before applying.** Ask one question if the problem type is unclear. Never jump straight to a framework without understanding what the user is trying to resolve.
**One framework at a time.** Run the chosen framework to completion before introducing the next. Parallel frameworks create confusion.
**Never use all frameworks on one problem.** Maximum 2–3. More is diminishing returns. Pick the ones that address the biggest unknowns.
**Always end with a concrete next action.** Deep thinking that produces only insight, not action, is incomplete.
## When NOT to Invoke Any Framework
Thinking frameworks cost time and tokens. Do not invoke them for:
- Routine decisions with low stakes and easy reversibility
- Problems the user has already thought through and just needs execution help
- When the user says "just do it", "let’s move", or signals they want action not analysis
- Repeating something that has worked before in a similar context
- Small tactical choices (which file to edit, what to name a variable, how to word a sentence)
Invoke a framework only when you detect at least ONE of these signals:
- **High stakes:** wrong decision is costly or hard to reverse
- **Genuine ambiguity:** multiple plausible interpretations, not just one missing detail
- **Overconfidence:** the plan has no contingencies and assumes everything goes right
- **Systemic effects:** the decision affects many people, systems, or future decisions
- **Novel territory:** no clear precedent and the team is reasoning by analogy
- **User explicitly asks** for deeper thinking or stress-testing
If none of these signals are present, skip straight to the work.
---

## The Thinking Frameworks

| Framework | Best for | Core motion |
|-----------|----------|-------------|
| `inversion` | Goals that need stress-testing; plans that feel optimistic | Flip: what guarantees failure? |
| `pre-mortem` | Decisions about to be committed; projects about to launch | Time-travel: it’s already failed — why? |
| `assumption-mapping` | Plans with many unvalidated beliefs; strategy documents | Surface: what must be true? rank by risk |
| `socratic` | Problems that feel stuck; reasoning that circles | Decompose: what’s the one question underneath? |
| `adversarial-hat` | Documents or plans that need rigorous pressure-testing | Critique: what is specifically wrong and why? |
| `first-principles` | Solutions constrained by convention or inherited design | Strip: what is actually necessary vs. assumed? |
| `second-order` | Decisions with delayed or systemic consequences | Chain: and then what? and then what? |
| `fermi` | Unknowns blocking a decision; market/effort sizing | Decompose: what are the estimable factors? |
| `ooda` | Fast-moving, competitive, or uncertain situations | Loop: observe → orient → decide → act |

---

## Diagnostic Guide

Read the user's input. Match to a primary framework:

**"I want to X but I'm not sure how / I keep going in circles"**
→ `socratic` first — find the real question, then `inversion` or `assumption-mapping`

**"We're about to commit to this plan / launch this"**
→ `pre-mortem` first — prospective hindsight before commitment, then `adversarial-hat` on the critical risks

**"Here's our plan / document — what are we missing?"**
→ `adversarial-hat` first — systematic critique, then `assumption-mapping` for the critical quadrant

**"We have a goal and we're not sure if we're approaching it right"**
→ `inversion` first — flip the goal, then `assumption-mapping` if hidden assumptions surface

**"I need to understand this problem better before I can solve it"**
→ `socratic` — decompose until the path is clear, then apply the appropriate framework

**"The solution feels expensive / constrained / like there should be a better way"**
→ `first-principles` — strip to fundamental truths, rebuild without inherited constraints

**"We need to decide but don't know the numbers / how big this is"**
→ `fermi` — decompose the unknown into estimable factors, produce a defensible range

**"This decision looks good short-term but I'm worried about downstream effects"**
→ `second-order` — trace consequences across time, find hidden risks and opportunities

**"The situation is changing / competitor just moved / we need to respond now"**
→ `ooda` — observe facts vs. assumptions, orient, decide and commit, set next loop trigger

**Mixed or unclear** → Ask one question: "Are you trying to (a) understand the problem, (b) stress-test a plan, (c) size an unknown, (d) find a better approach, or (e) respond to a fast-moving situation?"

---

## Workflow

### Step 1 — Diagnose
Read the input. Apply the diagnostic guide above.
If the problem type is genuinely unclear: ask one clarifying question, then diagnose.

### Step 2 — Name the Framework(s) and Why
Before starting, tell the user what you're going to do and why:
> "This feels like a [problem type]. I'm going to start with [framework] because [reason]. After that, if [condition], we'll run [second framework]."

### Step 3 — Run the Primary Framework
Invoke the chosen thinking skill fully. Complete it before introducing any secondary framework.

### Step 4 — Check: Is More Needed?
After the primary framework completes, ask:
> "That surfaced [key finding]. Do you want to [go deeper with X / stop here / apply Y to address what we found]?"

Give a specific recommendation — don't just offer an open menu.

### Step 5 — Run Secondary Framework (if needed)
If the user wants to continue and a second framework would genuinely add value, run it on the specific question or finding that needs it — not on the whole original problem.

### Step 6 — Synthesise
After all frameworks are complete:
- What was the core insight this session produced?
- What hidden belief, constraint, or question was exposed?
- What is the one concrete action to take now?

---

## Gotchas

- **Diagnosis is the most important step.** Wrong framework for the problem wastes time and produces shallow insight. Invest in Step 1.
- **Socratic and adversarial-hat don't combine well.** Socratic builds up; adversarial tears down. Use one per session unless a specific finding calls for the other.
- **Pre-mortem works best just before commitment.** If the decision is already made, use `adversarial-hat` instead.
- **If the user is emotionally attached to their plan**, lead with `socratic` to surface their assumptions through questions rather than `adversarial-hat` which can feel like an attack.

---

## Example

<examples>
  <example>
    <input>I need to decide whether to hire a full-time community manager or outsource it. I've been going back and forth for weeks.</input>
    <output>
Going back and forth usually means the decision criteria are unclear, not that the options are equal. I'll start with Socratic to find what's actually blocking you — then we can pressure-test whichever direction becomes clearer.

[Runs socratic — after 3 questions reveals: the user is uncertain whether community will be a core motion or a side feature, which makes the resourcing question unanswerable]

The real question isn't who manages community — it's whether community is central to your retention strategy or a nice-to-have. That's what needs to be decided first.

Shall I run inversion on "community as core retention strategy" to help you think that through? Or would you rather map the assumptions behind each option?
    </output>
  </example>
</examples>

---

## Thinking Skills Available

- `inversion` — flip the goal; failure inversion + opposite goal
- `pre-mortem` — prospective hindsight; extract causes before they happen
- `assumption-mapping` — surface all hidden beliefs; rank by importance × evidence
- `socratic` — find the keystone question; follow the thread recursively
- `adversarial-hat` — structured critique; diagnostic + creative + challenge
- `first-principles` — strip to fundamental truths; rebuild without inherited constraints
- `second-order` — trace consequences across time; find hidden risks and opportunities
- `fermi` — decompose unknowns into estimable factors; order-of-magnitude answer
- `ooda` — observe → orient → decide → act; fast-moving / competitive situations

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I already thought about it" | Deep-thinking forces explicit framework choice, not vibes. |
| "One framework is enough" | Wrong frame applied confidently is worse than diagnosing first. |
| "This doesn't need deep analysis" | Router exists because mis-framed problems waste the wrong skill. |

## Verification

- [ ] Framework choice named with one-sentence rationale
- [ ] At least one non-obvious insight beyond the user's opening frame
- [ ] Synthesis connects frameworks if multiple were used
- [ ] Ends with a single recommended next action

## Red Flags

- Framework chosen before problem diagnosis
- Socratic and adversarial-hat combined in one session
- Pre-mortem run after commitment already made
- Session ends without one concrete next action

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Deep thinking session: [problem/decision/document] Frameworks used: [list] Core insight: [the main thing this session revealed] Hidden assumption/question exposed: [if any] Concrete next action: [what to do now]`
