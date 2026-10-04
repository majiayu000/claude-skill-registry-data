---
name: sixhats
description: This skill should be used when the user asks to "use six hats", "apply six thinking hats", "think with different hats", "use De Bono's hats", "separate thinking modes", "look at this from all angles", "consider all perspectives", or wants to process input through Edward de Bono's Six Thinking Hats to systematically examine a topic from multiple cognitive perspectives.
version: 0.2.1
---

# Six Thinking Hats (De Bono)

## Overview

Apply Edward de Bono's Six Thinking Hats method — a structured parallel thinking framework that separates thinking into six distinct modes, each represented by a colored hat. By wearing one hat at a time, thinkers avoid the confusion of mixing facts with emotions, criticism with creativity, and analysis with action.

This is a *thinking organization* tool, not a truth-finding or analytical framework. It does not determine what is true (use Scholastic for that) or decompose complexity (use Cartesian for that). Its power is in ensuring that all relevant cognitive modes — factual, emotional, critical, optimistic, creative, procedural — are exercised deliberately rather than haphazardly. The output is a structured map of perspectives, not a resolved conclusion.

The Six Hats method excels at decisions, evaluations, planning, and any input where multiple perspectives need to be explored without the chaos of unstructured debate.

## The Six Hats

| Hat | Focus | Key Question |
|-----|-------|-------------|
| ⚪ **White** — Facts | Objective data, information, what is known and what is missing | "What do we know? What do we need to find out?" |
| 🔴 **Red** — Feelings | Intuitions, emotions, gut reactions — no justification required | "What is my gut feeling about this?" |
| ⚫ **Black** — Caution | Risks, dangers, problems, weaknesses, why it might fail | "What could go wrong?" |
| 🟡 **Yellow** — Optimism | Benefits, value, feasibility, why it might work | "What are the benefits? Why is this worth doing?" |
| 🟢 **Green** — Creativity | Alternatives, new ideas, possibilities, provocations, modifications | "What are the alternatives? What new ideas emerge?" |
| 🔵 **Blue** — Process | Meta-thinking, organization, summary, conclusions, next steps | "What have we learned? What should we do next?" |

## Core Methodology

1. 🔵 **Blue Hat Opening** — Define the focus. What is the topic, question, or decision? What outcome is needed? Set the sequence of hats to use. The default order below (White → Red → Black → Yellow → Green) works for most situations, but adapt it: start with Red if emotions are running high and need acknowledgment first; start with Black if the proposal seems risky and caution is the priority; skip Green if no alternatives are needed.

2. ⚪ **White Hat** — Lay out the facts. What information is available? What data is missing? Distinguish verified facts from beliefs or assumptions. "Facts" means empirical evidence, measurements, research findings, and documented data — not common knowledge, hearsay, or received wisdom. No interpretation — just information.

3. 🔴 **Red Hat** — Express feelings. Each participant states their emotional reaction without explanation or justification. Hunches, intuitions, likes, dislikes. This legitimizes emotion as valid input rather than suppressing it.

4. ⚫ **Black Hat** — Apply critical judgment. What are the risks? What could fail? Where are the weaknesses? This is logical negativity — grounded in evidence and experience, not emotional pessimism. The most powerful hat when used correctly.

5. 🟡 **Yellow Hat** — Explore value. What are the benefits? Why could this work? What is the best-case scenario? Requires effort — optimism must be justified with reasons, unlike the Red Hat.

6. 🟢 **Green Hat** — Generate alternatives. New ideas, modifications, creative possibilities. This is the productive hat — provocations, lateral jumps, "what if" thinking. Quantity over quality at this stage.

7. 🔵 **Blue Hat Closing** — Summarize findings from all hats. What conclusions emerge? What decisions can be made? What are the next steps?

## Key Concepts

- **Parallel Thinking:** Everyone wears the same hat at the same time. This replaces adversarial debate (where people defend positions) with cooperative exploration (where everyone looks in the same direction together).
- **Separation of Modes:** The power of the method comes from NOT mixing modes. Facts without judgment. Feelings without justification. Criticism without defensiveness. Creativity without premature evaluation.
- **Black Hat Discipline:** The Black Hat is the most misused — it is NOT general negativity. It is logical caution grounded in experience. "This failed before because X" is Black Hat. "I don't like it" is Red Hat.
- **Red Hat Permission:** By giving emotions a legitimate place, the Red Hat prevents feelings from secretly influencing what should be factual or logical thinking.
- **Green Hat Freedom:** The Green Hat creates a dedicated space for ideas without immediate criticism. Ideas generated under the Green Hat are evaluated later under Black and Yellow.
- **Hat Tensions:** The most valuable insight often comes from conflicts *between* hats — Red Hat enthusiasm vs. Black Hat caution, White Hat data vs. Yellow Hat optimism, etc. The Blue Hat Summary must explicitly surface these tensions rather than smoothing them over. A tension between hats is a signal that the decision involves genuine trade-offs, not a failure of the method.

## Analysis Protocol

### Structured Mode (default)

Produce the analysis in this exact section order:

```
## 🔵 Blue Hat — Focus
[Define the topic, question, or decision under examination]
[What outcome or clarity is being sought?]

## ⚪ White Hat — Facts
[Known facts and data relevant to the topic]
[Information gaps — what we don't know but need to]
[Distinguish verified facts from assumptions]

## 🔴 Red Hat — Feelings
[Emotional reactions, intuitions, gut feelings about this topic]
[No justification required — just honest reactions]

## ⚫ Black Hat — Caution
[Risks and dangers identified]
[Weaknesses and potential failure points]
[Historical precedents of failure in similar situations]

## 🟡 Yellow Hat — Optimism
[Benefits and value identified]
[Reasons it could succeed]
[Best-case outcomes and their likelihood]

## 🟢 Green Hat — Creativity
[Alternative approaches or ideas]
[Modifications to improve the original proposal]
[Provocative "what if" possibilities]

## 🔵 Blue Hat — Summary
[Key findings from each hat]
[Tensions between hats — where did different modes produce conflicting signals?]
[Conclusions and decisions]
[Recommended next steps]

**Confidence: [0.0–1.0]** — [Brief justification for the rating]
```

### Interactive Mode

When the user requests interactive/Socratic analysis:

1. Open with the Blue Hat — ask the user to define the focus clearly
2. Move through each hat one at a time, presenting your analysis and asking the user for their input under that hat
3. Enforce hat discipline — if the user mixes modes (e.g., criticizing during Yellow Hat), gently redirect to the current hat
4. After all hats, summarize together under the Blue Hat and ask what conclusions the user draws
5. Note where different hats revealed tensions or surprises

## Example

A brief example illustrating hat tension on "Should we rewrite our backend in Rust?":

> ⚪ **White Hat:** Current backend handles 10k req/s. Target is 50k. Rust rewrites in similar projects took 6–18 months. Team has 1 Rust developer out of 8.
>
> 🔴 **Red Hat:** Excitement about Rust's performance guarantees. Anxiety about the learning curve and timeline risk.
>
> ⚫ **Black Hat:** 7 of 8 developers would need training. Rewrite risks introducing new bugs in battle-tested code. 6–18 month timeline means delayed feature work.
>
> 🟡 **Yellow Hat:** Rust's memory safety eliminates a class of production bugs. Long-term maintenance cost drops. Performance headroom beyond 50k target.
>
> **Hat tension:** Red Hat excitement and Yellow Hat benefits pull toward rewrite; Black Hat timeline risk and White Hat staffing data pull against it. This is a genuine trade-off, not a clear call.

## When to Apply This Framework

**Strong fit:**
- Decisions that need structured evaluation from multiple angles
- Group thinking or stakeholder analysis where perspectives conflict
- Evaluating proposals, plans, or strategies
- Situations where emotions and facts are getting tangled
- Any input where "How should we think about this?" is the core question

**Weak fit:**
- Evaluating truth claims (use Scholastic instead)
- Systematic decomposition of complex systems (use Cartesian Reductionism instead)
- Value/quality judgments (use Pirsig instead)
