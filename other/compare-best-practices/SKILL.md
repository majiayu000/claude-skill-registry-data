---
name: compare-best-practices
description: Use when the user wants to choose between two or more practices that could apply to the same problem — or when suggest-best-practice surfaces multiple close-scoring options and the user needs help deciding. Produces a side-by-side comparison with trade-offs and a recommendation.
source: Multi-criteria decision analysis (Hammond, Keeney & Raiffa, "Smart Choices", 1998); Benjamin Franklin's "moral algebra" pro/con method (letter to Joseph Priestley, 1772)
tags: [comparison, decision, trade-offs, multi-option, choosing, recommendation]
---

# Compare Best Practices

Side-by-side comparison of two or more applicable practices, with a recommendation.

## Why This Is Best Practice

**Adopted by:** Multi-criteria decision analysis (MCDA) is standard in management consulting (McKinsey, BCG), engineering procurement, and policy evaluation — whenever multiple viable options exist and the stakes of the wrong choice are high. Benjamin Franklin's "moral algebra" (1772) is the earliest documented systematic pro/con framework; it has been in continuous use for 250 years precisely because it externalizes comparison and reduces cognitive bias.
**Impact:** Hammond, Keeney & Raiffa (1998) document that unstructured option comparison is the most common source of decision errors — people pick the option they encountered first or the one most recently described, not the one best suited to their situation. Structured comparison with explicit dimensions reduces this anchoring bias and produces more defensible decisions.
**Why best:** "I'll just pick one" fails under two conditions: when options are genuinely close (no dominant choice) and when context determines the winner (one is better for small teams, another for regulated industries). A side-by-side comparison makes context-dependence visible and forces a recommendation the user can accept or override — rather than leaving them to decide without the information they need.

Sources: Hammond, Keeney & Raiffa (1998) "Smart Choices"; Benjamin Franklin letter to Joseph Priestley (1772); Kahneman (2011) "Thinking, Fast and Slow" — anchoring bias

## Steps

### Step 1: Identify practices to compare

From user input ("compare X and Y", "which is better — X or Y?") or carried over from a multi-match result in `suggest-best-practice`.

**Infer before asking:** Before asking, try to identify practice names from the user's description — methodology names, approach descriptions, tool names, or framework mentions all count. Examples: 'debating TDD vs writing tests after' → infer test-driven-development vs post-implementation testing; 'OOP or functional for this service' → infer apply-oop-principles vs apply-functional-programming. Only ask if inference produces fewer than 2 candidates.

If practices aren't named explicitly, ask ONE question:
```
Which practices are you choosing between? (Names or descriptions both work)
```

Cap at 5 practices in one comparison. If more than 5 are named, ask the user to narrow to the top candidates first.

### Step 2: Extract comparison dimensions (silent)

For each practice, extract from its SKILL.md:

| Dimension | What to extract |
|-----------|----------------|
| **Approach** | One-line summary of what the practice prescribes |
| **Evidence** | RCT / systematic review / broad org adoption / practitioner consensus |
| **Best for** | Team size, maturity level, domain, urgency conditions where it excels |
| **Not ideal when** | Conditions where it underperforms or fails |
| **Trade-off** | What you gain and what you give up by choosing this one |
| **Adoption cost** | Low (< 1 day to start) / Medium (days to weeks) / High (structural change required) |
| **Constraints fit** | How well it fits the user's stated constraints: team size, timeline, existing stack, budget |

**Constraint dimension:** Always include a 'Constraints fit' row in the comparison table:
| Dimension | Practice A | Practice B |
|---|---|---|
| Constraints fit | [how well it fits user's stated constraints: team size, time, resources] | [same] |

User constraints (team size, timeline, existing stack, budget) often determine the choice more than abstract quality. If the user stated constraints, they must appear as a comparison dimension — not just an afterthought in the recommendation.

If a practice isn't installed, note it and compare abstractly from its description field only.

### Step 3: Present side-by-side table

```
Comparing: [practice-A] vs [practice-B]

                   [practice-A]              [practice-B]
Approach           [one line]                [one line]
Evidence           [level]                   [level]
Best for           [context]                 [context]
Not ideal when     [condition]               [condition]
Trade-off          [gain / loss]             [gain / loss]
Adoption cost      Low / Medium / High       Low / Medium / High
```

For 3+ practices, use a wider table or stack as separate columns.

### Step 4: Recommend with reasoning

```
Recommendation: [practice-name]
Reason: [2 sentences — why it fits this specific context better than the alternatives]
```

If context is unknown and it changes the recommendation, ask ONE question before recommending:
```
To recommend the right one, I need to know: [specific deciding factor].
```

If genuinely equal given the user's context, say so explicitly:
```
Both are valid here. Deciding factor: [the one dimension that would tip it — if you have X, pick A; if you have Y, pick B].
```

Never refuse to recommend. A recommendation with stated reasoning is always more useful than "it depends."

### Step 5: Apply recommendation

**Auto-apply condition:** Apply the recommendation silently ONLY when BOTH are true:
1. User explicitly asked for a decision ('which should I use?', 'help me choose', 'recommend one')
2. One practice rated higher on ≥ 3 of the comparison criteria (not just overall — must win on at least 3 individual dimensions)

Do NOT auto-apply when:
- Request was exploratory ('what's the difference between X and Y?', 'compare X and Y')
- Neither practice wins ≥ 3 criteria
- User's constraints favor different practices for different situations

When in doubt about request type: present recommendation with rationale, do not auto-apply.

When the auto-apply condition is met, announce before applying:
```
Applying [recommended-practice]... (say "no" or name the other to switch)
```

Load and follow the chosen skill's steps.

## Rules

- Never refuse to recommend — if one is genuinely better for the user's context, say so
- If context is unknown and it changes the recommendation, ask ONE question before comparing
- Only compare installed skills — if one isn't installed, give install command and compare abstractly from the skill's description
- Cap at 5 practices in one comparison; if more, ask user to narrow first
- The recommendation must cite the user's specific context, not just generic trade-offs — "better for your 2-person team" beats "better for small teams"
- If the user rejects the recommendation and applies the other, don't relitigate — apply what they chose

## Common Mistakes

**Refusing to recommend**: "It depends" is not a recommendation. State what it depends on and make the call given what you know.

**Generic trade-off language**: "More rigorous but takes more time" applies to almost everything. Name the specific dimension that matters for this user's context.

**Comparing only features, not fit**: The table shows what each practice is. The recommendation shows which fits. Don't stop at the table.

**Recommending without checking context**: If team size or domain changes the winner, ask before recommending — don't guess wrong and undermine trust.
