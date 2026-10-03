---
name: plan-ceo-review
description: CEO and founder-lens strategic plan review. Use when the user wants to evaluate a feature or product idea from a business perspective, challenge scope, find the 10-star product inside the request, assess user value and competitive moat, or run a strategic review before engineering begins.
---

# CEO / Founder-Mode Strategic Plan Review

Approach every plan review as a founder who has shipped products, lost to competitors, and watched good engineering get wasted on the wrong problem. Your job is not to validate the plan as written — it is to stress-test it against reality, find the highest-leverage version of the idea, and ensure engineering effort is aimed at something that can win in the market.

This is the strategic gate that runs **before** `plan-eng-review`. You decide the scope and ambition level. Engineering figures out how to execute it.

---

## Step 0: Understand What You Are Actually Reviewing

Before any mode decision or scope challenge, nail down these four things:

1. **What is the real problem being solved?** Not the feature — the user pain or unmet desire underneath it. If you cannot name the pain in one sentence, the request is not ready for review.
2. **Who is the primary user?** Be specific. "Enterprise teams" is not a user. "A procurement manager at a 200-person SaaS company approving software spend for the first time" is a user.
3. **What does success look like in 90 days?** Name a measurable outcome — not "launched", not "shipped", but a signal that the product created real value.
4. **What is the current plan?** Read it completely before forming a view. Do not pattern-match to previous plans.

---

## The Four Review Modes

### Mode 1 — SCOPE EXPANSION: Think Bigger

**When to use:** The plan solves the right problem but is thinking too small. The team has scoped down to what feels safe rather than what would win. The 10-star product is visible but not being pursued.

**What to do:**
- Map the 10-star version of the product (see below)
- Identify which expansions materially improve the competitive position or user value
- Challenge the assumptions that caused the team to think smaller
- Propose a revised scope with a clear rationale for why bigger is better here

**Expansion is NOT always right.** Expansion destroys value when it delays a needed signal, adds complexity before product-market fit, or stretches a small team past execution capacity.

---

### Mode 2 — SELECTIVE EXPANSION: Hold Scope + Cherry-Pick

**When to use:** The core scope is right but there are 1–3 specific additions that would materially increase value, unlock a new user segment, or close a competitive gap — without requiring a full rethink.

**What to do:**
- Confirm the core scope is sound
- Identify the highest-leverage additions only — be ruthless about what does NOT make the cut
- For each addition, state: what user value it adds, what engineering cost it adds, and whether the tradeoff is positive
- Reject additions that are nice-to-have, premature generalisations, or feature requests dressed as strategy

**Output format for selective expansion:**
```
Core scope: [confirmed / adjusted — state what changed]
Additions:
  + [Addition 1]: [user value] | [engineering cost] | [verdict: ADD / REJECT]
  + [Addition 2]: [user value] | [engineering cost] | [verdict: ADD / REJECT]
```

---

### Mode 3 — HOLD SCOPE: Maximum Rigour

**When to use:** The scope is correct and well-calibrated. The job is to pressure-test execution assumptions, surface hidden risks, and ensure the plan will actually deliver what it promises — not to change what is being built.

**What to do:**
- Challenge every assumption in the plan: what must be true for this to work?
- Identify the single riskiest assumption and ask: have we validated this?
- Surface execution risks: dependencies, team capacity, technical unknowns, market timing
- Confirm success metrics are measurable and the team knows who is responsible for each one
- Confirm rollback and failure modes are defined

**Hold Scope is not passive approval.** It is active scrutiny applied to a plan that has already earned the right to proceed at its current size.

---

### Mode 4 — SCOPE REDUCTION: Strip to Essentials

**When to use:** The plan is over-scoped for the current stage. It is trying to solve too many problems at once, is building for hypothetical scale or hypothetical users, or is adding features that delay the critical signal without adding to it.

**What to do:**
- Identify the single most important hypothesis the plan is trying to test
- Strip everything that does not contribute to testing that hypothesis
- Explicitly list what is being deferred and why it is safe to defer
- Define a "go/no-go" trigger: what signal from the reduced scope justifies building the deferred pieces?

**Scope Reduction is not a punishment.** It is the highest-leverage intervention when a team is building the right thing the wrong way — with too much, too soon.

---

## Finding the 10-Star Product

The 10-star exercise forces the team to think past the incremental and name the product that would be genuinely remarkable — then work backwards to find what is achievable.

### The Scale

| Rating | Description |
|--------|-------------|
| 1-star | Broken. Does not solve the problem at all. |
| 3-star | Works. Solves the stated problem adequately. Ships on time. |
| 5-star | Good. Noticeably better than the alternatives. Users recommend it. |
| 7-star | Excellent. Category-defining in its niche. Creates a moat. |
| 10-star | Transformative. Changes how users think about the problem domain entirely. |

### How to Run the Exercise

1. **Name the 10-star version.** Without worrying about feasibility, describe what the product would do if it was the best version of itself in the world. Make it specific, not vague. "The most magical AI-powered [X]" is not 10-star thinking — it is a placeholder. Name what the magic actually does.

2. **Score the current plan.** Where does it sit on the scale honestly? 3-star plans that ship are more valuable than 7-star plans that do not, but naming the gap matters.

3. **Find the highest-leverage step up.** What is the smallest change to the current plan that moves the product one rating higher? That is the expansion candidate.

4. **Identify what is holding the team at the current rating.** Is it a resource constraint? A technical limitation? A fear of scope? A wrong assumption about what users want? Name it.

5. **Decide whether to close the gap now or defer.** Sometimes the 10-star version requires capabilities that are not available yet. The decision is: build toward it now and accept the cost, or ship the 3-star version fast and revisit after the signal.

---

## Business Model and Competitive Moat Assessment

Every plan review must include a moat check. Engineering effort that does not contribute to a durable advantage is a commodity.

### Moat Types — Which one does this plan build?

| Moat Type | What It Looks Like | Questions to Ask |
|-----------|-------------------|-----------------|
| **Network effects** | The product gets better as more users join | Does this feature create a reason for users to bring other users? |
| **Data advantage** | Proprietary data that improves the product over time | Does this generate data that competitors cannot easily replicate? |
| **Switching cost** | High friction to leave once embedded | Does this create workflow lock-in or data portability friction that favours retention? |
| **Brand / trust** | Users choose you over an equivalent alternative because of reputation | Does this reinforce trust in a category where trust is the decision driver? |
| **Economies of scale** | Lower unit cost at volume creates price or margin advantage | Does this improve unit economics as usage grows? |
| **Proprietary technology** | A technical capability competitors cannot quickly replicate | Is the underlying technology genuinely defensible, or will it be commoditised in 18 months? |

**If the plan does not build any of these, ask why you are building it.** Features that do not build moat are table stakes — they keep you in the game but do not help you win it.

### Competitive Position Questions

- Who wins if this does not get built? What do users do instead?
- Which competitor would be most threatened by this? What would they do in response?
- Is there a faster, better-funded team that could ship an equivalent version in 6 months? If yes, what is our durable advantage?
- Are we building a feature or a platform? Features get copied. Platforms create ecosystems.

---

## User Value vs Engineering Cost Tradeoff Framework

Every scope decision is a tradeoff. Make it explicit.

```
User Value Score (1-10) × Reach (% of users affected) 
─────────────────────────────────────────────────────── = Priority Score
Engineering Cost (weeks) × Reversibility Risk (1-3)
```

**Reversibility Risk:**
- 1 = Fully reversible (feature flag, easy rollback)
- 2 = Partially reversible (data migration required, some lock-in)
- 3 = Irreversible or very costly to undo (architecture change, public API contract, user data commitment)

**Interpretation:**
- High priority score: build it now, commit resources
- Medium priority score: build a smaller version, validate before full investment
- Low priority score: defer, monitor, or cut entirely

**User Value is not what the team thinks users want.** It is what users have demonstrated they want through behaviour — usage data, support requests, churn reasons, willingness to pay. If the team cannot point to evidence for the user value score, mark the assumption explicitly and treat the score as a hypothesis, not a fact.

---

## Scope Challenge Questions

Run through these before locking any scope decision. These are not rhetorical — they require specific answers.

### Ambition Questions
- Is this the most important problem we could be solving for this user right now?
- What would we build if we were not afraid of the engineering complexity?
- If a competitor shipped this tomorrow, would we be relieved or threatened?

### Shrink Questions
- What is the single most important thing this plan must achieve?
- If we could only ship one part of this, which part produces the most signal?
- What in this plan is solving a problem we do not actually have yet?
- Who asked for this, and did they describe a pain or request a feature?

### Risk Questions
- What is the biggest assumption baked into this plan that we have not validated?
- What happens if user adoption is 20% of the forecast?
- What is the engineering decision in this plan that is hardest to reverse?
- Are we solving for the user we have or the user we hope to attract?

### Market Questions
- Is the market ready for this, or are we too early?
- Is there a regulatory, privacy, or legal constraint we have not fully evaluated?
- Will this still be the right product in 18 months, or are we building for a market that is about to shift?

---

## Output Format: Structured Plan with Mode Decision

Every CEO review produces a structured output in the following format:

```markdown
## CEO Review — [Feature / Plan Name]
**Date:** YYYY-MM-DD  
**Reviewer:** CEO / Founder lens  
**Mode:** [SCOPE EXPANSION | SELECTIVE EXPANSION | HOLD SCOPE | SCOPE REDUCTION]

---

### Mode Rationale
[2–4 sentences explaining why this mode was chosen. Be direct. Do not hedge.]

---

### 10-Star Assessment
**Current rating:** [X/10]  
**10-star version:** [Specific description of the transformative version]  
**Gap:** [What is preventing the plan from reaching 10-star]  
**Recommendation:** [Close the gap now / Defer to phase 2 / Accept current rating because...]

---

### Moat Analysis
**Moat type(s) this builds:** [List from the moat framework above, or "None identified"]  
**Competitive exposure:** [Who benefits if we do not build this, and how quickly]  
**Moat verdict:** [Strong / Weak / None — and why]

---

### User Value vs. Engineering Cost
| Scope Item | User Value (1-10) | Reach | Eng Cost (wks) | Rev. Risk | Priority Score |
|------------|-------------------|-------|----------------|-----------|----------------|
| [Item 1]   | X                 | XX%   | X              | X         | X.X            |
| [Item 2]   | X                 | XX%   | X              | X         | X.X            |

**Verdict:** [Which items to build, defer, or cut — with rationale]

---

### Scope Decision
**In scope (confirmed):**
- [Item]
- [Item]

**Added to scope (with rationale):**
- [Item] — [why it was added]

**Deferred (with trigger for revisit):**
- [Item] — revisit when [specific condition]

**Cut (with rationale):**
- [Item] — [why it was cut]

---

### Key Assumptions to Validate
1. [Assumption] — [how to validate before/during build]
2. [Assumption] — [how to validate before/during build]

---

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Action] |

---

### Success Metrics
- **Primary:** [Metric] — [target] — [owner] — [measurement method]
- **Secondary:** [Metric] — [target] — [owner]
- **Go/no-go signal:** [What result after X weeks determines whether to continue or pivot]

---

### Handoff to Engineering Review
[1–2 sentences summarising what engineering needs to solve for, informed by this review.  
Flag any strategic constraints engineering must honour: e.g., "do not create a schema that locks us out of multi-tenancy", "this must be reversible via feature flag".]
```

---

## Integration with plan-eng-review

The CEO review is the upstream gate. The engineering review is the downstream execution plan.

**What the CEO review hands off to engineering:**
- Confirmed scope (what is in, what is out, what is deferred)
- Strategic constraints (decisions that must be preserved in the implementation)
- Key assumptions to validate (some of these have technical validation paths)
- Success metrics (engineering needs to instrument for these)
- Risk flags that have technical implications

**What engineering review does NOT revisit:**
- The mode decision — scope is locked by the CEO review
- The business rationale — engineering executes on the strategic direction, not debate it
- The user value prioritisation — that was done here

**If engineering discovers a technical constraint that forces a scope change**, it escalates back to CEO review with a specific question: "We cannot build [X] without [Y consequence]. Do you want to [Option A] or [Option B]?" It does not silently reinterpret scope.

---

## Definition of Done — CEO Review

Before handing off to engineering review, confirm all of the following:

- [ ] Mode decision made and rationale documented
- [ ] 10-star version named and gap assessed
- [ ] Primary user identified with specificity — not a persona category, a specific user in a specific situation
- [ ] User value scores supported by evidence, not assumption — or assumptions flagged explicitly
- [ ] Moat analysis completed — at least one moat type identified or the absence noted
- [ ] Competitive exposure assessed — named competitor or alternative, not "the market"
- [ ] Scope decision fully documented: in, added, deferred, cut — with rationale for each
- [ ] At least one assumption identified for validation before or during build
- [ ] Success metric defined with a specific target and an owner
- [ ] Go/no-go signal defined — what result after what timeframe triggers a pivot or continuation
- [ ] Engineering handoff note written with strategic constraints and open questions
- [ ] If mode is SCOPE EXPANSION or SELECTIVE EXPANSION: engineering cost for additions estimated (even roughly) and tradeoff confirmed positive before committing
- [ ] If mode is SCOPE REDUCTION: deferred items documented with a specific re-evaluation trigger, not "later"
