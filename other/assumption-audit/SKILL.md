---
name: assumption-audit
description: Extract every assumption hidden in a claim, plan, or belief, classify each by load-bearingness and testability, and identify which single assumption would collapse the whole structure if false. Use when a plan feels solid but untested, or before committing to a decision built on unexamined premises.
---

# Assumption Audit

Use this skill to surface and stress-test the premises hiding inside a claim, plan, or belief. Most plans fail not at the visible steps but at an assumption nobody wrote down.

## Purpose

Every plan is a conclusion resting on premises, most of them implicit. An assumption audit makes the full list explicit, sorts it by how much weight each premise carries and how cheaply it can be tested, and names the keystone — the single assumption whose failure takes the whole structure down. This converts vague confidence into a concrete testing agenda.

## Procedure

1. State the claim, plan, or belief being audited.
2. Extract assumptions exhaustively. Look in these categories:
   - **Factual**: things believed true about the world
   - **Causal**: "doing X will produce Y"
   - **People**: what others want, know, or will do
   - **Continuity**: "current conditions will persist"
   - **Capability**: "we can execute this part"
   - **Definitional**: the framing of the problem itself
3. For each assumption, rate:
   - **Load**: if this is false, does the plan break entirely, degrade, or barely notice?
   - **Confidence**: how strong is the actual evidence (not the felt certainty)?
   - **Testability**: can this be checked cheaply, expensively, or only in hindsight?
4. Identify the **keystone**: highest load × lowest confidence.
5. Propose the cheapest test for the keystone and the top 2–3 risky assumptions.
6. State what the plan looks like if the keystone fails — is there a fallback?

## Output format

Use this concise structure unless the user asks otherwise:

```markdown
## Claim / plan under audit
...

## Assumption register
| # | Assumption | Category | Load | Confidence | Testability |
|---|---|---|---|---|---|
| 1 | ... | Causal | Breaks plan | Low | Cheap |

## Keystone assumption
...

## Cheapest tests
- ...

## If the keystone fails
...
```

## Guardrails

- Include at least one *definitional* assumption — the framing of the problem is always an assumption.
- Rate confidence by evidence, not by how long the assumption has been held.
- Do not pad the register with trivially safe assumptions to look thorough; focus on the load-bearing ones.
- If everything checks out, say so — the audit passing is a valid result.

## Canonical questions

- "We're about to spend 6 months building this feature — sanity-check the plan."
- "My startup thesis is that restaurants will pay for X."
- "I'm planning to move to Austin for the lower cost of living."
- "Our hiring plan assumes we close the Series A by Q3."
- "I believe my best customers come from word of mouth."

Poor fits: decisions already made and irreversible (use inversion for damage control instead), and pure preference questions with no factual premises.
