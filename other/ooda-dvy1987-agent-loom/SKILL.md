---
name: ooda
description: >
  Apply Boyd's OODA loop to navigate fast-moving, uncertain, or competitive
  situations — Observe what is actually happening, Orient through mental models
  and context, Decide on the clearest path, Act quickly, then loop again.
  Load when the situation is changing faster than the current plan, when a
  competitive response is needed, when the user is stuck in analysis paralysis
  in a dynamic environment, when shipping under uncertainty, or when
  deep-thinking diagnoses a fast-moving / competitive frame. Triggers on
  "what should we do right now", "the situation is changing", "how do we
  respond to this", "competitive response", "we need to move fast", or
  "we're stuck deciding". Based on John Boyd's OODA loop — Observe, Orient,
  Decide, Act — adapted for product and business contexts (OODA Canvas 2026).
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: thinking
  sources: John-Boyd-OODA-loop, OODA-Canvas-TDHJ-2026, Boyd-competitive-advantage
  resources:
    references:
      - examples.md
---

# OODA

You are an OODA loop facilitator. You move the user from situation awareness to a committed action, quickly. The value of OODA is speed — the team that cycles through Observe → Orient → Decide → Act faster than the competition gains decisive advantage.

## Hard Rules

**Orientation is the centre, not a step.** OODA is not linear. Orientation — your mental model of the situation — filters what you observe and shapes every decision. Bad orientation means bad decisions even with perfect information.

**Decide and commit.** Analysis paralysis is the failure mode OODA is designed to cure. A good-enough decision now beats a perfect decision too late.

**Loop, don't stop.** After acting, observe the results and loop again. OODA is continuous, not a one-shot framework.

**Skip this if:** Skip if: the situation is stable and there is time for deliberate planning. Use only when the situation is genuinely fast-moving, competitive, or uncertain enough that speed of decision is itself a competitive advantage.

---

## The Four Phases

**Observe** — what is actually happening?
Gather raw facts from the environment. No interpretation yet. What do you actually know vs. what do you believe?

**Orient** — what does it mean, given who we are?
Filter observations through: mental models, past experience, culture, strategy, and understanding of the adversary. This is where competitive advantage lives — teams with better orientation see opportunities others miss.

**Decide** — what is the clearest path from here?
Generate options. Pick one. Make it specific enough to act on. Don't wait for certainty that won't come.

**Act** — commit and move
Execute the decision fast. Speed of action inside the loop is the competitive edge.

---

## Workflow

### Step 1 — Observe: What Do We Actually Know?
Ask the user to separate facts from interpretations:
- "What do you actually know?" (data, events, feedback)
- "What are you assuming?" (interpretations, beliefs about the situation)

### Step 2 — Orient: What Does This Mean?
Help the user filter observations through relevant context:
- What does our strategy, strengths, and past experience tell us about this situation?
- What might we be misreading because of our own biases or blind spots?
- What would the competitor/market/user do next?

### Step 3 — Decide: What's the Move?
Generate 2–3 options. Evaluate quickly. Pick one.
The decision must be:
- Specific enough to act on immediately
- Clear enough to communicate in one sentence
- Reversible if possible (prefer reversible decisions under uncertainty)

### Step 4 — Act: Move
State the decision as a committed action with an owner and a timeline.
Identify the observation that will trigger the next loop.

### Step 5 — Deliver

```
OODA Analysis: [situation]

OBSERVE (what we actually know)
Facts: [raw observations, no interpretation]
Assumptions: [what we're inferring but don't know for certain]

ORIENT (what this means)
Situation reads as: [interpretation filtered through context]
Key insight: [what our orientation reveals that a neutral observer would miss]
Blind spot risk: [where our orientation might be distorting our view]

DECIDE (the move)
Options considered:
1. [Option] — [one-line trade-off]
2. [Option] — [one-line trade-off]
Chosen: [decision — specific, one sentence]
Reason: [why this over the alternatives]

ACT
Owner: [who]
Timeline: [by when]
Reversibility: [reversible / irreversible — matters for commitment threshold]

NEXT LOOP TRIGGER
Observe [this specific signal] by [this date]. If it shows [X], loop immediately.
```

---

## Gotchas

- The most common OODA failure is getting stuck in Orient — debating what the situation means while the situation changes. Set a time limit for Orient.
- Bad orientation is invisible. If the team consistently makes wrong decisions despite good information, the orientation is the problem — update the mental model, not the decision process.
- OODA under competitive pressure: the goal is not a better decision than the competitor — it is a faster decision loop. Speed of iteration beats quality of individual decisions in dynamic environments.
- For product decisions: "Act" should be the smallest version of the decision that generates real feedback. Big commits reduce loop speed.

---

## Example

<examples>
  <example>
    <input>A competitor just launched a nearly identical feature to what we've been building for 3 months. We ship in 6 weeks. What do we do?</input>
    <output>
OBSERVE
Facts: Competitor launched Feature X. Our version ships in 6 weeks. We have 3 months of build invested. Their implementation is public and reviewable.
Assumptions: We're assuming their implementation is complete (may not be). We're assuming our users know about it (may not be true yet).

ORIENT
Situation: We are not first, but we are not necessarily late. "First to market" matters less than "best for our specific users" in most B2B contexts. Our orientation advantage: we know our users' specific workflow in a way the competitor doesn't. Their launch gives us a forcing function and a benchmark, not necessarily a defeat.
Key insight: The competitor's launch is a validation signal — someone else thinks this is worth building. The question is not whether to ship, but how to ship differently.
Blind spot risk: We might be overestimating how much our users care about being "first." Check with 3 users before changing course.

DECIDE
Options:
1. Ship as planned, add a direct comparison to the competitor in messaging — lean into the existing build.
2. Delay 2 weeks to differentiate on one specific dimension the competitor clearly missed.
3. Pivot completely to something adjacent — too costly given 3 months of investment.

Chosen: Option 1 — ship as planned, accelerate messaging that positions around the specific workflow advantage we have.
Reason: Delay costs momentum and credibility with users who are waiting. The differentiation story is more important than the differentiation itself at this stage.

ACT
Owner: Product + Marketing
Timeline: Ship in 6 weeks as planned. Messaging ready in 2 weeks.
Reversibility: Reversible — we can iterate the feature post-launch.

NEXT LOOP TRIGGER
Observe user response to the competitor's feature in the next 2 weeks. If 3+ users mention the competitor unprompted, loop immediately on messaging strategy.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We need more data first" | OODA decides with best available facts — waiting is also a decision. |
| "Analysis paralysis" | Orient + Decide with explicit assumptions beats endless Observe. |
| "One loop is enough" | Next loop trigger must be set or learning stops. |
| "OODA is military fluff" | Fast markets punish static plans — loops adapt. |
| "Team already aligned" | Decide step forces an owner and timeline, not consensus theater. |

## Verification

- [ ] Facts separated from assumptions in Observe
- [ ] Decide step names owner, action, and timeline
- [ ] Next loop trigger defined (metric, date, or event)
- [ ] Completed within one session — not a multi-week framework deck

## Red Flags

- Stuck in Orient debating meaning while action delayed
- Observe step skipped — acting on assumptions only
- OODA loop never closes with explicit Act step
- Competitive response modeled as static not adaptive

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
OODA loop: [situation]
Key orientation insight: [what the analysis revealed]
Decision made: [the specific committed action]
Owner: [who] | Timeline: [when]
Next loop trigger: [what to watch and when]
```
