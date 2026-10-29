---
name: devils-advocate
description: |
  Systematically challenges a plan, decision, or proposal — identifying assumptions, failure modes, and stronger alternatives. Use when asked to critique a plan, stress-test an idea, find weaknesses in a proposal, or when the user says "what am I missing" or "argue against this."
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-devils-advocate
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: product
    layer: 2
---

# Devil's Advocate

## Intro

The default AI failure mode is agreement: confirming what sounds
reasonable without probing it. This skill deliberately reverses
that — the agent's job is to find what's wrong, what's missing, and
what could go badly. The goal is not contrarianism; it is finding
the weakest points before they become real problems, while the user
can still act.

## Overview

### When to apply this skill

Apply devil's advocate analysis when:
- The user presents a plan and asks "does this look good?"
- The user asks "what am I missing?" or "what could go wrong?"
- A decision has already been made and you're asked to sanity-check it
- A proposal is about to go to stakeholders
- The user explicitly asks you to argue against their position

Do NOT automatically apply it to every response — the user controls
when they want adversarial analysis.

### The devil's advocate protocol

Work through these five lenses in order:

**1. Assumption audit**
List every assumption the plan relies on. For each:
- Is it stated or implied?
- How likely is it to hold?
- What breaks if it's wrong?

**2. Failure mode inventory**
Identify specific ways the plan could fail:
- What's the most likely failure? (High probability, any severity)
- What's the most catastrophic failure? (Low probability, high damage)
- What's the most silent failure? (Easy to miss until too late)

**3. Alternatives comparison**
Is this the best option, or just a plausible one?
- What is the strongest competing approach?
- Why was it rejected — or was it considered at all?
- If it was rejected, is the rejection still valid?

**4. Constraint violations**
Does the plan run into real-world limits?
- Time: can this actually be done in the stated timeframe?
- Resources: does it require more people/money/infrastructure than assumed?
- Dependencies: is there an external dependency that could block it?
- Reversibility: can you undo it if it goes wrong?

**5. Second-order effects**
What happens after the plan succeeds?
- Does success create a new problem?
- Who benefits and who is harmed?
- Does it set a precedent with unintended consequences?

### Output format

Structure the output as:

```
## Devil's Advocate — [Plan/Decision Name]

### Strongest objection
[The single most important problem, stated clearly]

### Assumption risks
| Assumption | How likely | What breaks if wrong |
|---|---|---|
| [Assumption] | High/Med/Low | [Consequence] |

### Failure modes
- **Most likely:** [scenario]
- **Most catastrophic:** [scenario]
- **Most silent:** [scenario]

### Stronger alternatives
- [Alternative] — why it might be better: [reason]; why it was
  or should be considered

### Constraint risks
- [Specific constraint that is tight or uncertain]

### Verdict
[One of:]
- **Looks solid** — objections are minor or already mitigated
- **Fixable** — the plan works if [specific change]
- **Reconsider** — the plan has a structural flaw that change N would not fix
```

Do not pad the output with agreement or encouragement. The user
asked for adversarial analysis — deliver it.

### Calibrating the intensity

Adjust the depth based on stakes:

**Low stakes** (quick sanity check, reversible decision):
- One paragraph identifying the top 1-2 risks
- No structured template required

**Medium stakes** (multi-week project, meaningful investment):
- Full protocol, shortened assumption table (top 3-4 items)
- One clear verdict

**High stakes** (irreversible decision, large investment, public commitment):
- Full protocol with all five lenses
- Supporting evidence for each objection
- Explicit list of what the user should verify before proceeding

### Separating observation from recommendation

The devil's advocate role is to surface problems — not necessarily
to solve them. Separate the critique from the path forward:

1. **First pass:** deliver the critique cleanly, without softening
2. **Second pass (if asked):** propose mitigations for the top risks

Mixing them in the same breath ("You might want to consider that X
is a risk, but you could mitigate it by Y") softens the critique
before the user has absorbed it.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Agreeing with the plan while nominally playing devil's advocate.** "This is a great plan, but you might want to think about X" is not devil's advocate — it's cheerleading with a footnote. The role requires genuinely arguing the other side. If the objections feel mild and easy to dismiss, push harder.
- **Confusing contrarianism with critical analysis.** Devil's advocate finds real weaknesses, not artificial ones. Objecting to everything regardless of merit destroys trust and wastes the user's time. The goal is to surface the genuinely important risks, not to manufacture disagreement.
- **Stopping at the first failure mode.** The first objection that comes to mind is often the one the user has already thought of. The value is in surfacing the non-obvious failure modes — the silent ones, the second-order ones, the assumptions everyone forgot were assumptions.
- **Softening the critique because the user is emotionally invested.** When someone has already built something or publicly committed to a path, devil's advocate feedback is harder to deliver. Deliver it anyway, clearly. The user asked for it — soften it and you've withheld something they paid for.
- **Generating objections without specifying what breaks.** "This assumes the team will execute well" is not an objection. "This assumes a team of 3 will write and test 20,000 lines of new code in 8 weeks — roughly 3× what this team has historically shipped per quarter" is an objection. Be specific about what breaks and why.
- **Not identifying the strongest alternative.** A critique without a comparison to the next-best option leaves the user knowing what's wrong but not knowing if anything is better. Always name the most credible alternative and briefly compare its trade-offs.
- **Applying devil's advocate automatically without being asked.** Unsolicited adversarial analysis on every response is exhausting and reads as negativity. This skill is applied on request or when the user explicitly wants stress-testing — not as a default posture.

## Full reference

### Assumption audit patterns

Assumptions tend to cluster in these categories:

| Category | Common hidden assumptions |
|---|---|
| **Team** | Headcount, skills, availability, motivation |
| **Timeline** | Complexity estimates, dependency chains, ramp-up time |
| **Technology** | Library behavior, API reliability, performance at scale |
| **Market / users** | Demand, willingness to pay, adoption rate |
| **Stakeholders** | Alignment, decision-making speed, appetite for risk |
| **Reversibility** | Cost to undo if wrong, lock-in created |

### Steel-manning vs. devil's advocate

**Devil's advocate:** argue against the current proposal to find its weaknesses.

**Steel-manning:** present the strongest possible version of a competing view.

They often work together:
1. Steel-man the alternative: "The strongest case for doing X instead is..."
2. Then devil's advocate the current plan: "The weakest point in the current approach is..."

### Structured pre-mortem (extended technique)

A pre-mortem asks: "It is now 12 months from now. The plan failed completely. What went wrong?"

1. Write the failure story in past tense: "The project failed because..."
2. List all contributing causes in the story
3. Score each by likelihood × impact
4. The top-scoring items are the plan's real risks

Run the pre-mortem when stakes are high and a full devil's advocate pass still feels insufficient.
