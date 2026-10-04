---
name: apply-premortem
description: Use when a plan is finalized but not yet launched, to surface failure modes the team hasn't acknowledged before commitment is locked in.
source: Gary Klein, "Sources of Power" (1998); Klein "Performing a Project Premortem" Harvard Business Review (2007); adopted by Google Ventures and standard in decision-making research
tags: [risk-analysis, decision-making, project-planning, cognitive-bias, mental-models, team-process]
related: [apply-devils-advocate-technique, apply-dual-process-diagnostic, apply-reference-class-forecasting, apply-sunk-cost-discipline, apply-hindsight-bias-correction]
verified: true
---

# Apply Premortem

Before launching a plan, imagine it has already failed catastrophically — then work backwards to identify every cause of that failure while you can still act on them.

## Why This Is Best Practice

**Adopted by:** Google Ventures (Sprint methodology), U.S. Intelligence Community (analytical red-teaming), and recommended in standard decision-making curricula at Harvard Business School, Wharton, and by Nobel laureate Daniel Kahneman as the single most effective debiasing technique available before a decision.
**Impact:** Klein's original research showed premortems increase the ability to identify reasons for future outcomes by 30% over standard prospective analysis. Kahneman in "Thinking, Fast and Slow" (2011) states: "The premortem is a prophylactic against overconfident planning." Google Ventures adopted it as a standard Sprint exercise, exposing critical failure modes in product plans before any code is written.
**Why best:** Planning suffers from two documented biases: optimism bias (overestimating success probability) and groupthink (dissent is socially costly after a plan is endorsed). The premortem defeats both simultaneously — by framing failure as a given, it gives permission to voice concerns without appearing disloyal, and by forcing specificity about how failure happened, it bypasses the vague "what could go wrong?" question that teams answer with platitudes.

Sources: Gary Klein "Sources of Power" (1998) Ch. 7; Klein HBR "Performing a Project Premortem" (Sept 2007); Kahneman "Thinking, Fast and Slow" (2011) §24

## Steps

1. **Wait until the plan is final** — Run premortem after the plan is complete but before execution begins. Too early and there's nothing concrete to analyze; too late and sunk-cost effects make people defensive.
2. **Frame the failure** — Tell the group: "It is one year from now. This project has failed completely and publicly. We are reading the post-mortem report. What does it say?" State this as a fact, not a hypothesis.
3. **Write independently** — Each participant silently writes every cause of failure they can think of for 5–10 minutes. No discussion, no filtering. Individual writing prevents anchoring on the first idea voiced.
4. **Round-robin collection** — Go around the table, each person reads one item from their list. Record every cause on a shared visible list. Continue until all unique items are captured. No debate at this stage.
5. **Identify the highest-probability causes** — After collection, have each participant mark their top 3–5 most likely causes. Tally votes. High-vote items are your priority failure modes.
6. **Analyze root causes for top items** — For each priority failure cause, ask: what specific condition allowed this to happen? What was the decision or omission at the origin? This is the actionable level.
7. **Assign countermeasures** — For each priority root cause, assign a named owner and a specific action: redesign a process, add a checkpoint, change a resource allocation, or explicitly accept the risk with a monitoring signal.
8. **Document accepted risks** — For failure causes you cannot eliminate, record them explicitly with their probability, impact, and the signal that would trigger a response. This becomes the risk register for the project.

## Rules

- The facilitator must actively protect dissenting voices — anyone who agrees with a concern already listed should add their own framing; new perspectives matter even on overlapping issues.
- Do not let the team negotiate failure causes during collection — debate happens after all items are on the board, not while they're being raised.
- Every participant writes independently before discussion — this is non-negotiable; skipping it collapses the exercise into groupthink.
- A premortem is not a veto — its purpose is to harden the plan, not abandon it. The outcome is a better plan with identified failure modes addressed.

## Common Mistakes

- **Running it as a group brainstorm from the start** — the vocal dominant person sets the frame, others anchor to it, and half the failure modes stay unvoiced. Silent independent writing first is the mechanism, not a detail.
- **Stopping at cause identification** — listing failure causes without assigning countermeasures is a worry list, not a premortem. Every priority cause must have an owner and an action.
- **Running it too early** — a premortem on a vague plan surfaces vague concerns. Wait until the plan is concrete enough that specific failure causes can be named.
- **Treating it as pessimism or loss of confidence** — frame explicitly: "We are doing this because the plan is good and we want to protect it."

## Examples

**Product launch:** Frame: "It's Q4. The launch failed. Customers churned in the first 30 days and press coverage was negative." Causes collected: onboarding too complex, support team undertrained, pricing misaligned with segment, key integration broke at launch. Top causes hardened: onboarding redesign assigned to PM, support training added to launch checklist.

**Organizational change:** Frame: "The reorg was announced six months ago and has reduced output by 20%. Half the senior engineers are interviewing elsewhere." Causes: unclear reporting lines, no communication about career paths, managers lost span of control without buy-in. Countermeasures: RACI chart before announcement, individual manager conversations scheduled, retention risk flagged to CHRO.

## When NOT to Use

- When a decision is already in execution — sunk cost and commitment effects make premortem findings hard to act on; use an active risk review or retrospective instead.
- When the team is in crisis or high-stress — premortem requires reflective thinking; under acute pressure, focus on stabilization first.
- When the plan is truly exploratory with no committed path — premortem requires a specific plan to fail; if the plan is "explore options," apply structured brainstorming first.
