---
name: board-of-advisors
description: |
  Simulates a panel of expert advisors who each evaluate a problem from their distinct perspective — surfacing blind spots and generating more diverse thinking than a single viewpoint. Use when asked to get multiple perspectives, consult experts, think through a decision from different angles, or when a problem benefits from specialist input.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-board-of-advisors
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: product
    layer: 2
---

# Board of Advisors

## Intro

Assembling a mental board of advisors forces structured perspective-
taking. Each advisor has a distinct domain, incentive structure, and
way of framing problems. Their disagreements are the signal: when
advisors conflict, you've found a real trade-off that deserves
explicit resolution. The technique is most valuable when the default
view is too narrow, too technical, or too aligned with the user's
existing beliefs.

## Overview

### When to invoke the board

Apply this skill when:
- A decision has implications across multiple domains (tech AND
  business AND user experience)
- The user is too close to a problem and needs outside perspectives
- The obvious answer feels too easy (may be missing something)
- Stakeholders with different concerns need to be represented
- The user explicitly asks "what would X think about this?"

### Selecting the advisors

Choose 3-5 advisors whose perspectives create productive tension.
The advisors should have different incentive structures — not just
different knowledge domains.

**Common advisor archetypes:**

| Archetype | Their priority | Their typical objection |
|---|---|---|
| **Security engineer** | Risk reduction | "What's the attack surface?" |
| **Product manager** | User value and delivery speed | "Does this solve the user's problem faster?" |
| **CFO / financial lens** | Cost and ROI | "What's the total cost and what's the return?" |
| **Senior operator** | Reliability and maintainability | "Who is on-call for this at 3am?" |
| **New user / newcomer** | Clarity and ease of adoption | "Can someone pick this up without help?" |
| **Skeptic** | First principles challenge | "Why do this at all? What's the null hypothesis?" |
| **Domain expert** | Technical correctness | "Is this consistent with how X actually works?" |
| **Long-term thinker** | Consequences and precedents | "What does this look like in 3 years?" |

For software decisions: Security + Product + Operator + Newcomer works well.
For business decisions: CFO + Long-term thinker + Skeptic + Domain expert.
Customize for the specific problem.

### The board session format

```
## Board of Advisors — [Topic]

**Question before the board:** [Specific question or decision]

---

### [Advisor 1 Name/Archetype]

**Perspective:** [What this advisor cares about most]

**Their take:** [2-4 sentences from their point of view, using their
priorities and vocabulary — not generic praise or criticism]

**Their key question:** [The one thing they'd want answered before
endorsing]

---

### [Advisor 2 Name/Archetype]

[Same structure]

---

### [Advisor 3 Name/Archetype]

[Same structure]

---

## Where the advisors agree

[The points of convergence — these are the high-confidence observations]

## Where they conflict

[The genuine disagreements — these are the real trade-offs to resolve]

## Synthesis

[A short paragraph reconciling the perspectives, or naming the
decision the user must make to resolve the conflicts]
```

### Staying in character

Each advisor must reason from their own priorities — not from the
agent's default perspective. Indicators of shallow role-playing:

- Every advisor slightly reframes the same concern
- All advisors ultimately endorse the plan
- No advisor challenges a core assumption
- The vocabulary is the same across all advisors

Strong advisors:
- Use different vocabulary (the CFO says "burn rate", not "costs")
- Disagree with each other on real trade-offs
- Ask questions the user hasn't thought of
- Are sometimes wrong in ways that reflect their bias

### Naming specific advisors

When the user names a specific person ("What would Linus Torvalds
think?" "How would Jeff Bezos evaluate this?"), reason from what
is publicly known about that person's stated priorities,
public decisions, and decision-making style — not from a caricature.
Note when you're speculating beyond public record.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **All advisors agreeing with the plan.** If every advisor endorses the proposal, the advisors were not chosen or played with enough diversity. The whole point of the board is to surface the real trade-offs — an unanimous board has failed to do that. Choose advisors with genuinely conflicting incentives and let them conflict.
- **Each advisor using the same vocabulary and framing.** A product manager and a security engineer should sound different. If they use the same words ("this is a good approach but we should consider X"), they're not being played as distinct characters. Give each advisor a distinct frame — their priorities, their vocabulary, their professional instincts.
- **Picking advisors that all share the user's existing bias.** If the user is a startup founder who loves moving fast, and all five advisors also love moving fast, the board reinforces the existing view rather than expanding it. Always include at least one advisor whose incentives run counter to the user's instincts.
- **Making the synthesis do the decision for the user.** The board's job is to surface the trade-offs, not to resolve them. The synthesis section should identify the conflict clearly and name what the user must decide — not collapse it into a clean recommendation. "You must choose between X and Y because the CFO and the operator disagree on what matters more" is the right output.
- **Assigning advisors before understanding the problem domain.** A software deployment decision benefits from a Security + Product + Operator board; a fundraising decision benefits from a CFO + investor + skeptic board. Assigning the same advisors to every problem produces generic perspectives that don't illuminate the specific trade-offs at stake.
- **Letting each advisor speak at length before surfacing their conflict.** Long monologues from each advisor before any summary loses the reader. Lead with the key observation from each advisor, then go deeper only where needed. The conflicts section is where the value is — reach it quickly.
- **Treating the technique as a substitute for talking to real experts.** The board-of-advisors skill generates structured hypothetical perspectives, not real expert opinions. For high-stakes decisions — architectural choices, legal questions, financial commitments — the board helps frame the questions, but actual experts should be consulted.

## Full reference

### Pre-built boards for common problem types

**Technical architecture decision:**
- Security engineer: attack surface, secrets, least privilege
- Senior operator: operational complexity, monitoring, on-call load
- Product manager: delivery speed, feature impact on users
- Skeptic: why not the simpler / existing approach?

**Startup / product strategy:**
- Customer advocate: does this solve a real problem better?
- CFO / financial: unit economics, burn, return timeline
- Long-term thinker: moat, defensibility, 3-year consequences
- Devil's advocate: why would this fail?

**Team or process change:**
- New team member: onboarding burden, clarity
- Senior engineer: maintenance, technical debt created
- Manager: coordination cost, visibility
- Impacted stakeholder: who loses something here?

**Communication / messaging:**
- Skeptical audience: what objections will they raise?
- Friendly audience: what do they want to hear vs. what they need?
- Legal / compliance: what claims need qualification?
- Journalist: what's the most critical read of this?

### When to use board-of-advisors vs. devils-advocate

| | Board of Advisors | Devil's Advocate |
|---|---|---|
| **Goal** | Multiple perspectives | Single adversarial critique |
| **Output** | Diverse viewpoints + synthesis | Focused critique + verdict |
| **Best for** | Cross-domain decisions | Stress-testing one proposal |
| **Number of voices** | 3-5 advisors | 1 adversarial voice |
| **Depth** | Breadth across domains | Depth on one angle |

Use board-of-advisors when the decision spans domains or needs
stakeholder modeling. Use devil's advocate when you want a focused
stress-test of a single proposal.
