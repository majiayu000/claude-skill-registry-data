---
name: validate-idea
description: >
  Validate a business idea using the minimalist entrepreneur framework before building anything.
  Use to test if an idea is worth pursuing through manual validation and customer feedback.
compatibility:
  models: [any-llm]
  use-case: idea-validation
  frameworks: [minimalist-entrepreneur, lean-startup, customer-validation]
---

# Validate Idea

Test if a business idea is worth pursuing through manual validation, customer conversations, and proof of customer demand—before writing a single line of code.

## Use This Skill When

- User has a business idea and wants to know if it's viable
- User wants to validate before investing time/money in building
- User is deciding between competing ideas
- User says phrases like "is this idea good", "should I build", "will people pay", "is there a market", "validate my idea"

## When NOT to Use

- User is ready to build the product (use MVP or processize skill)
- User is designing the product (use product-design skill)
- User needs formal market research/reports (use market-research skill)

## Context: Validation Maturity

**Unvalidated**: Idea only; no customer conversations; no evidence of demand  
**Partially validated**: Talked to some potential customers; mixed signals  
**Validated**: 10+ customers surveyed; 3+ willing to pay; problem confirmed → **Target**  
**Proven**: 10+ paying customers for manual version; repeatable sales process

## Core Principle

**Validation happens through selling, not building.** Most founders spend months building a product nobody wants. You validate by selling a manual version to real customers first. Money proves demand; opinions don't.

## Instructions

### Step 1: Define the Problem (Not the Solution)

**Clarify what problem you're solving**, not how you'll solve it.

**Questions to ask**:
- **Who specifically** has this problem? (Not "business owners" but "self-employed plumbers with <$500k revenue trying to stay organized")
- **Current workaround**: How are they solving it today? (Spreadsheet, competitor, manual process)
- **Pain level**: Mild inconvenience or critical blocker? (Hair-on-fire problems validate better)
- **Frequency**: How often do they face this problem? (Weekly problems validate better than annual ones)
- **Cost of problem**: What does it cost them in time, money, lost opportunity? ($0 problems don't validate)

**Red flag**: If you can't articulate the problem in one sentence, it's not clear enough.

**Good examples**:
- "Freelance writers with 1–3 clients struggle to track invoices and payment status" ✓
- "Businesses need better software" ✗

### Step 2: Can You Solve It Manually?

**Before building, can you deliver value by hand?**

This is **processizing**: proving you can solve the problem for real customers manually, then automating later.

**Test questions**:
- Can you solve this problem for someone this week, by hand?
- What would your process be? (Write it down)
- How long would it take per customer?
- What tools would you use? (Email, spreadsheet, phone, existing software)

**If you can't solve it manually**: Either the problem isn't clear, or you don't understand the solution space well enough yet.

**If you can**: You're ready for Step 3 (selling a manual version).

### Step 3: Talk to Potential Customers

**Find real people** with the problem and ask them directly.

**Conversation framework**:

1. **Find 10 specific people** with the problem
   - Where do they hang out? (Reddit, Slack, Discord, industry forums, LinkedIn, local meetups)
   - Can you contact them directly? (Better than cold outreach)
   - Aim for mix of different sub-segments if possible

2. **Have a 15-minute conversation**, not a survey
   - Describe the problem (confirm they have it): "Do you struggle with X?"
   - Ask about their workaround: "How do you handle this today?"
   - Ask about priorities: "What matters most: saving time, saving money, or reducing stress?"
   - Gauge interest: "If I built a solution, would you be interested?"
   - Ask for willingness to pay: "Would you pay $X/month for this?"

3. **Document responses**
   - Yes/No/Maybe for each person
   - Quoted pain points (their words)
   - Price sensitivity (what they'd pay)
   - Timing (when would they need it)

**Success criteria**: 
- ✓ 10+ conversations completed
- ✓ 7+ confirm they have the problem
- ✓ 3+ express strong interest/willingness to pay

### Step 4: Offer a Manual Version

**Try to sell** a manual version of the solution.

**Script**:
```
"I'm testing a solution for [problem]. 
I can manually do [deliverable] for you for $X. 
Would you be interested?"
```

**Goal**: Get 3–5 paying customers for the manual version.

**What you learn**:
- Will they actually pay? (Proof of demand)
- How long does it take? (Cost structure)
- What do they actually need? (Real vs. imagined problem)
- What objections come up? (Product direction)

**Success = people paying real money for your manual service**

### Step 5: The Four MVP Validation Questions

Before you even think about building, answer these four questions:

| Question | Good Answer | Bad Answer |
|----------|------------|-----------|
| **Can I ship it in a weekend?** | Yes: one core feature | No: needs months of work |
| **Does it make life better?** | Solves real, measurable problem | Incremental convenience |
| **Will customers pay?** | 3+ customers already paid | "They said they would" |
| **Can I get feedback fast?** | Weekly customer contact | Build in secret for months |

**Rule**: If you can't answer "yes" to all four, the idea needs more validation or refinement.

## Validation Decision Framework

Create a scorecard:

| Signal | Points | Your Answer | Score |
|--------|--------|------------|-------|
| **Problem clarity** | 10 | Can you describe in one sentence? | _/10 |
| **Customer identification** | 10 | Named 10+ specific people with problem? | _/10 |
| **Problem confirmation** | 15 | Talked to 7+ customers who confirm problem? | _/15 |
| **Willingness to pay** | 15 | 3+ expressed strong interest in paying? | _/15 |
| **Existing demand** | 15 | People paying for inferior alternatives? | _/15 |
| **You've solved manually** | 10 | Delivered manual version to 1+ customers? | _/10 |
| **Market size** | 10 | Problem affects 100+ potential customers? | _/10 |

**Scoring**:
- **80+**: Validated. Build the MVP.
- **60–79**: Partially validated. Do more customer interviews or manual tests.
- **<60**: Not ready. Revisit problem or pivot.

## Red Flags (Do NOT Build If...)

- Nobody is currently trying to solve this (no existing solutions/workarounds)
- You can't name 10 specific people facing the problem
- Validation comes only from "my friends think it's cool"
- You'd need to educate people that they have the problem
- You're building for a community you don't belong to
- People won't pay for the manual version
- The problem is "nice to have" but not urgent

## Green Flags (Worth Pursuing If...)

- ✓ People are already paying for inferior solutions
- ✓ You've manually solved this for someone and they loved it
- ✓ The community actively complains about the problem
- ✓ You can describe customer + problem in one sentence
- ✓ You're scratching your own itch (you're the customer)
- ✓ 3+ people willing to pay for manual version
- ✓ Problem is urgent, not convenient

## Common Validation Mistakes

- **Assuming demand**: "I showed 5 friends and they liked it" ≠ customer demand
- **Wrong customer**: "Businesses need this" when actual user is a specific role (not the business)
- **Solution confusion**: Jumping to "build an app" before confirming problem
- **Timing mismatch**: Problem is real but customer not ready to pay yet
- **Market too small**: Problem affects <100 customers (hard to build sustainable business)
- **Competitor denial**: "There's no competition" (usually false; they use workarounds)

## Output

After validation, provide a clear verdict:

**Verdict Type 1: VALIDATED ✓**
```
Strong signals to proceed. Specific evidence:
- 10+ customers confirmed problem
- 3–5 paying customers for manual version
- Clear, repeatable solution process
- You can ship MVP in <2 weeks

Recommendation: Start MVP or processize phase
```

**Verdict Type 2: PARTIALLY VALIDATED ⚠**
```
More evidence needed. Next steps:
- Complete X more customer interviews
- Try manual version with X more customers
- Refine problem definition
- Then reassess

Timeline: 2–4 weeks to re-validate
```

**Verdict Type 3: NOT VALIDATED ✗**
```
Weak or absent signals. Consider:
- Pivot to related problem that has stronger demand
- Validate manual version first before returning to product idea
- Combine with adjacent problem for stronger market fit
- Explore different customer segment for same problem

Alternative paths forward: [specific suggestions]
```

---

**For each validated idea, summarize**:
1. **Problem**: One sentence
2. **Customer**: Specific, named segment
3. **Proof of demand**: X customers confirmed, Y paying
4. **Next step**: Build MVP or continue validating
5. **Timeline**: When to launch manual or product version
