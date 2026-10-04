---
name: explain-best-practice
description: Use when the user wants to understand WHY a practice works — not just apply it. Covers the problem it solves, its origin, the evidence base, how the mechanism works, failure modes, and common misconceptions. Educational mode, not application mode.
source: Feynman Technique (Richard Feynman); Bloom's Taxonomy (Benjamin Bloom, 1956); "Made to Stick" (Heath & Heath, 2007) — why some ideas survive and others die
tags: [education, explanation, understanding, why, evidence, learning, mechanism]
---

# Explain Best Practice

Deep-dive into why a practice works: problem, origin, evidence, mechanism, failure modes, misconceptions.

## Why This Is Best Practice

**Adopted by:** The Feynman Technique — explain a concept as if teaching it to a novice — is the gold-standard self-assessment method at Caltech and has been adopted in medical education, law school, and engineering training programs. Bloom's Taxonomy (1956) defines six levels of understanding, and "explain why" sits at the third level (application/analysis) — the minimum needed for reliable transfer to new contexts. Heath & Heath (2007) document that ideas survive when they are concrete, credible, and story-driven — the exact structure this skill produces.
**Impact:** Practitioners who understand the mechanism of a practice adapt it correctly under novel conditions; those who only know the steps fail when conditions change. Malpractice and engineering failures are disproportionately caused by rule-following without mechanism understanding — the practitioner couldn't recognize when the rule didn't apply (Institute of Medicine "To Err is Human", 1999).
**Why best:** Applying a practice without understanding it works until it doesn't — the first novel condition breaks compliance. Understanding why a practice works enables correct adaptation, recognition of when it doesn't apply, and persuasive explanation to others. The six-section structure forces honest assessment: a practice with no known failure modes hasn't been examined honestly.

Sources: Bloom's Taxonomy (1956); Heath & Heath (2007) "Made to Stick"; Institute of Medicine (1999) "To Err is Human"; Feynman Technique (attributed)

## Steps

### Step 1: Identify the practice

From user input: "explain [practice]", "why do we do [X]?", "what's the evidence for [Z]?", "help me understand how [practice] works."

If the practice name is ambiguous, match against installed skills using the standard scoring model. If multiple practices score ≥ 0.4, ask the user to confirm which one.

### Step 2: Structure the explanation

Present each section with a header. Keep each section concrete — one specific example beats three abstract principles.

**Section prioritization:** When explaining a skill, prioritize sections in this order:
1. **Why This Is Best Practice** — establishes credibility and motivation
2. **Steps** — the actionable how-to
3. **Common Mistakes** — what goes wrong without it
4. **When NOT to Use** — scope limitations

If the user asks for a quick explanation, cover #1 and #2 only. If they ask for full detail, cover all four. Default to quick unless the user signals they want depth.

**The problem**
What goes wrong without this practice? Give a concrete failure case — not "things go wrong" but a specific type of incident, mistake, or waste that this practice was designed to prevent.

**The origin**
Who developed this practice, where, and why? A brief origin story grounds credibility and makes the practice feel like a solved problem rather than an arbitrary rule. One paragraph maximum.

**The evidence**
What proof exists that this practice works? Be honest about evidence tier:
- RCT or systematic review (strongest)
- Large-scale org adoption with measured outcomes
- Practitioner consensus across multiple independent sources
- Single-source or anecdotal (weakest — say so)

Don't overstate. "Widely adopted but limited controlled evidence" is more credible than invented precision.

**The mechanism**
HOW does it work? Not just "do these steps" — explain the causal chain from the practice to the outcome. Why do the steps produce the result? What would break if you skipped step 3? This is the section that enables correct adaptation.

**Failure modes**
When does this practice fail or backfire? Under what conditions does it not apply, produce diminishing returns, or actively harm outcomes? Every real practice has known failure modes. If you can't name any, the practice hasn't been examined honestly.

**Common misconceptions**
What do practitioners usually get wrong? What does "doing it wrong but thinking you're doing it right" look like? This section prevents the most common implementation errors.

### Step 3: Real-world failure example

One concrete story of what happened when this practice was skipped — ideally sourced, specific, and brief (3–5 sentences). Format:

```
When [practice] was skipped:
[Specific incident or case] — [what happened as a result]. [Source or organization if available.]
```

### Step 4: Offer to apply

```
Want to apply [practice] now? (y/n)
```

If yes, load the skill and follow its steps. If no, end gracefully — explanation was the goal.

**Uninstalled skill fallback:** Before handing off to suggest-best-practice, verify the explained skill is installed (present in `.grimoire/` or listed in `SKILLS.md`). If not installed: 'This skill is not currently installed. Install it with `/plugin install grimoire-[domain]@grimoire`, then invoke `/[skill-name]` directly.' Do not hand off to suggest-best-practice with an uninstalled skill pre-selected — it will fail to apply.

**Apply handoff:** If the user says 'apply this', 'use this', 'let's do this', or similar after the explanation, invoke `suggest-best-practice` with the explained skill pre-selected as the match. Pass the skill name as context so suggest-best-practice skips scoring and goes directly to application. Do not re-explain — the explanation is complete; just apply.

## Rules

- Be honest about evidence strength — never overstate; "widely adopted but limited RCT evidence" is the correct phrasing for practices without controlled studies
- The failure modes section is required — skip it only if the practice has no failure modes, which is rare enough to note explicitly
- Keep the explanation skimmable: one concrete example per section, headers visible, no wall-of-text paragraphs
- If the practice isn't installed, explain what's known from its description field and give the install command
- Educational mode means no pressure to apply — the goal is understanding, not compliance
- Don't conflate "evidence for the practice" with "evidence for the general category" — cite the specific practice's adoption or research, not adjacent work

## Common Mistakes

**Overstating evidence**: claiming RCT-level proof for practices that have only practitioner consensus damages trust when the user investigates. State the actual tier.

**Skipping failure modes**: "This practice always works" is a red flag. Every practice has conditions under which it fails. Name them.

**Abstract mechanism**: "It aligns incentives" or "it reduces complexity" is not a mechanism. "It separates the decision of what to build from the decision of how to build it, so each decision is made by the person with the most relevant knowledge" is a mechanism.

**Offering to apply mid-explanation**: save the apply offer for Step 4 — don't interrupt the explanation with action prompts.
