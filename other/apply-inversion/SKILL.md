---
name: apply-inversion
description: Use when solving a hard problem, stress-testing a plan, or identifying risks by reasoning backwards from failure instead of forwards from goals.
source: Carl Jacobi (mathematician, 1804–1851); Charlie Munger, "Poor Charlie's Almanack" (2005); widely taught at Berkshire Hathaway and in mental models curricula
tags: [mental-models, problem-solving, risk-analysis, decision-making, first-principles]
related: [apply-problem-reframing]
verified: true
---

# Apply Inversion

Solve problems by asking "what would cause failure?" then eliminating those causes — rather than asking "how do we succeed?" and hoping to avoid obstacles along the way.

## Why This Is Best Practice

**Adopted by:** Charlie Munger and Warren Buffett (Berkshire Hathaway), mathematicians (Carl Jacobi's dictum: "Invert, always invert"), and standard curriculum in decision-making programs at top business schools including Harvard Business School and Stanford GSB.
**Impact:** Munger attributes inversion as a primary driver of Berkshire's 50-year compounding record — it systematically surfaces risks that forward-thinking misses. In mathematics, Jacobi's inversion principle solved problems that direct approaches failed to crack for decades. Inversion is taught as a core mental model in Shane Parrish's Farnam Street curriculum, used by hundreds of thousands of practitioners.
**Why best:** Forward planning optimism bias is a documented cognitive failure mode: teams overestimate success probability and underestimate failure modes. Inversion bypasses this bias by starting from the failure endpoint and working backward, forcing explicit enumeration of every path to disaster. Removing failure paths is often more tractable than constructing success paths.

Sources: Charlie Munger "Poor Charlie's Almanack" (2005); Carl Jacobi "Fundamenta Nova Theoriae" (1829); Kahneman "Thinking, Fast and Slow" §24 on planning fallacy

## Steps

1. **State the goal** — Write the desired outcome in one sentence. "We want to ship a reliable payment system by Q3."
2. **Invert it** — Ask: "What would guarantee failure?" Write the inverted goal. "What would guarantee a broken, unreliable payment system?"
3. **Enumerate failure causes** — List every concrete action, omission, or condition that would cause the inverted outcome. Be specific. "Ship without integration tests. Give one engineer all DB access. Skip staging environment."
4. **Include human and systemic failures** — Don't stop at technical causes. Include process failures, communication gaps, incentive misalignments, and organizational blind spots.
5. **Score each by severity and likelihood** — For each failure cause, rate: how likely (1–5) and how catastrophic (1–5). High likelihood × high catastrophe = priority risk.
6. **Eliminate or mitigate each cause** — For every failure cause, decide: remove it entirely, reduce its probability, or reduce its impact. Document the countermeasure.
7. **Re-invert to your plan** — Flip back: the set of countermeasures to failure causes is your risk-hardened plan. What remains is the forward path with identified failure modes closed off.
8. **Pressure-test residual risks** — For any failure cause you couldn't eliminate, document it explicitly as an accepted risk with a monitoring signal and response plan.

## Rules

- List failure causes before solutions — switching to solutions early reintroduces optimism bias.
- Include obvious failures — teams routinely skip causes they consider "too embarrassing" to write down; those are often the ones that actually happen.
- Treat "we didn't do X" as a failure cause — omissions cause as many failures as commissions.
- Do not stop at the first level: invert the inverted causes to find second-order failure modes.

## Common Mistakes

- **Inverting the goal but only listing technical failures** — process, communication, and incentive failures are often the real causes; include them or the analysis is incomplete.
- **Treating inversion as pessimism** — it is not pessimism; it is systematic risk enumeration. The output is a better plan, not a reason to abandon the goal.
- **Stopping at cause identification without countermeasures** — inversion produces value only when each failure cause is addressed. A list of risks with no action is a worry list, not a strategy.
- **Running inversion once and filing it** — plans change; re-run inversion when scope, team, or constraints change significantly.

## Examples

**Project launch:** Goal: "ship MVP by April 15." Inversion: "What guarantees we miss April 15?" Causes: scope creep, no prioritized backlog, single point of failure on key engineer, no staging environment. Countermeasures: scope freeze, weekly backlog review, cross-training, staging setup in week 1.

**Investment decision:** Goal: "this acquisition creates value." Inversion: "What guarantees this acquisition destroys value?" Causes: culture mismatch, key talent departure, integration costs exceed projections, customer churn post-announcement. Each cause gets a due-diligence check or integration safeguard.

## When NOT to Use

- When a decision is already made and irreversible — inversion is a planning tool, not a post-mortem; use Five Whys instead for past failures.
- When the failure space is too large to enumerate usefully — complex open-ended systems (e.g., "make our culture better") require root cause analysis or structured prioritization first.
- When time pressure requires immediate action — inversion takes 30–60 minutes minimum; in a live incident, stabilize first, then apply inversion in the retrospective.
