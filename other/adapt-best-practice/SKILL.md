---
name: adapt-best-practice
description: Use when the user wants to apply a practice but has specific constraints that differ from the canonical case — team size, industry regulation, budget, maturity level, technology stack, or organizational culture. Produces an adapted version that preserves the practice's core while fitting the user's reality.
source: Situational Leadership model (Hersey & Blanchard, 1969); Lean principles — adapt to context while preserving core value (Womack & Jones, "Lean Thinking", 1996); contextual design methodology (Beyer & Holtzblatt, 1997)
tags: [adaptation, constraints, customization, context, fit, situational, pragmatic]
---

# Adapt Best Practice

Customize a practice for specific constraints while preserving its core effectiveness.

## Why This Is Best Practice

**Adopted by:** Situational Leadership (Hersey & Blanchard, 1969) is the canonical model for context-sensitive application — the same leadership approach applied uniformly across different team maturities produces worse outcomes than adapting to the situation. Lean manufacturing explicitly distinguishes between principles (non-negotiable) and tools (adapt to context) — Toyota Production System practitioners are trained to identify which is which before adapting. Contextual design methodology (Beyer & Holtzblatt, 1997) formalizes user-centered adaptation for design processes.
**Impact:** Organizations that apply best practices without adaptation to their context show lower adoption and higher abandonment rates than those that receive context-appropriate versions (McKinsey Organizational Health research, 2017). The most common reason practitioners abandon practices is "it doesn't fit how we work" — which usually means the form, not the substance, was incompatible. Adaptation preserves adoption.
**Why best:** The alternative — "apply the canonical practice or don't apply it" — produces two failure modes: abandonment when constraints make full compliance impossible, and compliance theater when people go through the motions without the core substance. Explicit Core/Adjustable/Optional classification makes the difference visible: what must stay, what can flex, and what can be skipped without breaking the practice's fundamental value.

Sources: Hersey & Blanchard (1969) "Management of Organizational Behavior"; Womack & Jones (1996) "Lean Thinking"; McKinsey Organizational Health Index research

## Steps

### Step 1: Identify the practice and constraints

From user input: "apply X but we're a 2-person team", "we're in a regulated industry", "we don't have budget for Y", "our team is new to this."

If the practice is named, match against installed skills. **Missing-practice fallback:** If the named practice does not exist in the installed skills index, do not invent one. Output:
```
Practice not found: [practice-name]
Closest match: [similar-skill-name] ([domain]) — is this what you meant?
```
If no close match exists: 'No installed practice matches [practice-name]. Run /discover-best-practices to find available practices for [domain].'

Do not proceed with adaptation until the source practice is confirmed.

If constraints aren't stated, ask ONE question:
```
What's the main constraint that makes the standard approach difficult?
```

Common constraint categories to listen for:
- Team size (solo / small team / large org)
- Industry regulation (healthcare, finance, legal, government)
- Budget / resource limits
- Technical maturity (beginner / intermediate / expert)
- Technology stack constraints
- Organizational culture (startup / enterprise / non-profit)
- Timeline pressure (needs to work this week, not this quarter)

### Step 2: Classify each step of the practice

Read the matched skill's Steps section. For each step, classify:

| Type | Definition |
|------|------------|
| **Core** | Non-negotiable — removing this breaks the practice's fundamental effectiveness. The reason the practice exists. |
| **Adjustable** | Can be scaled, simplified, substituted, or done differently without losing core value. The form can change; the substance stays. |
| **Optional** | Adds value in the ideal case but can be skipped under constraints without undermining the core outcome. |

**Classification rubric:**
- **Core** — step directly implements the practice's defining principle; removing it means the practice is no longer being applied (e.g., in TDD: 'write the test before the code' is Core — without it, it's not TDD)
- **Adjustable** — step implements the principle but the mechanism can vary by context (e.g., naming conventions, tool choices, team size thresholds)
- **Optional** — step adds quality or polish; the practice works correctly without it (e.g., adding inline comments, creating summary reports)

Test: ask 'If I remove this step, is the practice still being applied?' Yes → Optional or Adjustable. No → Core.

**Core-step confirmation:** Before adapting, explicitly state which steps are core (must be preserved) and which are context-specific (can be adapted). Show this to the user:
```
Core steps (preserved): [list]
Adaptable steps (context-specific): [list]
Adapting: [what will change and why]
```
This makes the adaptation principled rather than arbitrary — the user can see what's being treated as non-negotiable.

### Step 3: Map constraints to adjustments

For each constraint the user has, identify:
- Which steps it affects (Core / Adjustable / Optional)
- What adaptation preserves the core while accommodating the constraint
- What is lost by the adaptation (and whether that loss is acceptable)

Present as a mapping table:

```
Constraint: [user's stated constraint]
  Affects: Step N ([Adjustable/Optional])
  Adaptation: [what changes]
  Trade-off: [what's lost — acceptable because: reason]
```

### Step 4: Warn when a constraint compromises a Core step

If a constraint would require removing or fundamentally changing a Core step:

```
⚠ [constraint] conflicts with a core step of [practice].
Removing [step] would undermine the practice's primary value because [specific reason].
Proceed with adapted version? (y/n — or "explain the risk" for more detail)
```

If the user asks "explain the risk": describe the specific failure mode that occurs when this core step is skipped, with a concrete example if possible.

If all core steps would be removed by the constraints: don't adapt — redirect:
```
These constraints would remove all core steps of [practice].
The adapted version would not achieve [primary purpose].
Consider [alternative-practice] instead — it's designed for [constraint type].
```

### Step 5: Present the adapted version

Show the full practice with modifications annotated inline. Every step must be labeled:

```
Adapted [practice-name] for [stated constraints]:

Step 1: [original step text] — ✓ unchanged
Step 2: [original step text] — adapted: [what changes and why, one line]
Step 3: [original step text] — ✗ skipped: [what's lost, why acceptable given constraint]
```

After the adapted version, summarize the trade-off in one sentence:
```
Trade-off: [what this adaptation gains] at the cost of [what it loses].
```

## Rules

- Always label adapted steps — ✓ unchanged / adapted: / ✗ skipped — so the user knows what changed
- Never silently remove a Core step — always warn with Step 4 warning and get confirmation
- If constraints make the practice unworkable entirely, say so and redirect to an alternative
- Don't adapt to the point of inventing a new practice — if the adaptation diverges fundamentally from the original, name that explicitly
- The trade-off summary is required — don't leave the user guessing what they gave up
- Adaptation is not permission to skip hard parts — Core steps require a warning, not silent removal

## Common Mistakes

**Silent core step removal**: quietly dropping a step that is Core is worse than not adapting at all — it creates the illusion of following the practice while missing its substance. Always warn.

**Over-classifying as Optional**: when uncertain, classify as Core. The cost of over-adapting (losing the practice's value) is higher than the cost of keeping a step that could technically be skipped.

**Adapting form but not explaining why**: "Step 2: adapted" with no explanation leaves the user unable to judge whether the adaptation is sound. Name what changes and why.

**Redirecting when adaptation is possible**: if even one core step can be preserved, adapt — don't give up and redirect unless all core steps are compromised.
