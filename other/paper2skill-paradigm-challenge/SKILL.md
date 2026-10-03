---
name: paper2skill-paradigm-challenge
description: "Convert papers that disprove conventional wisdom into paradigm-challenge skills. Extracts the prior belief, the falsifying experiment, and the revised principle. Use this skill when extracting skills from Category 3 (Paradigm Challenge) papers — papers that say 'rethinking', 'revisiting', or 'do we really need X', where the core move is adversarial (proving the community wrong)."
---

## When to Use
Apply this skill when you encounter arXiv papers that:
- Explicitly state "we prove X wrong" or "we overturn the assumption that Y"
- Present controlled experiments designed to falsify a widely-held belief
- Argue against conventional wisdom with empirical evidence
- Reveal that practitioners' intuitions or standard approaches are incorrect
- Propose a revised principle that contradicts or extends prior understanding

Direction: ADVERSARIAL — the paper is arguing "you're wrong, here's why."

Examples: "Understanding Deep Learning Requires Rethinking Generalization" (proving that memorization doesn't explain generalization), "Rethinking Transformers in Solving POMDPs" (proving transformers are less capable than people thought in partially observable settings), "The Lottery Ticket Hypothesis" (proving neural networks contain subnetworks, invalidating assumptions about network necessity).

## When NOT to Use
Do not use this skill for:
- Papers that explore new phenomena without challenging prior beliefs (exploratory, not adversarial)
- Papers that improve upon prior work without falsifying the underlying principle
- Papers that discuss tradeoffs without claiming one side was fundamentally wrong
- Survey papers that analyze contradictory results
- Papers that challenge minor implementation details rather than principles
- Papers that propose alternatives without evidence the prior approach was wrong

---

## Extraction Template

### Step 1: Identify the Prior Belief
Extract what the community widely believed before this paper.

```markdown
**Prior Belief:** What did the community assume to be true?
**Who Believes It:** Research groups, practitioners, textbooks, or folk wisdom?
**Why It Seemed True:** What evidence or intuition supported this belief?
**Implications:** What decisions did people make based on this belief?
```

### Step 2: Locate the Falsifying Experiment
Identify the controlled experiment that disproves the belief.

```markdown
**Core Experiment:** What is the minimal experiment that proves the belief false?
**Experimental Design:**
- Control variables: What is held constant?
- Test variable: What is changed to test the belief?
- Measurement: How is the outcome measured?
- Sample size/conditions: How robust is the result?
**Why It's Convincing:** Why is this experiment hard to argue with?
**Edge Cases Tested:** Did the authors test boundary conditions?
```

### Step 3: Extract the Revised Principle
Document the correct understanding that replaces the prior belief.

```markdown
**Revised Principle:** What is now known to be true instead?
**Scope:** When does the revised principle apply? When doesn't it?
**Why It Matters:** How does this change practice?
**Remaining Questions:** What doesn't the revised principle explain?
```

### Step 4: Analyze Implications for Practice
Extract how the revised principle changes what practitioners should do.

```markdown
**For Research:** What research directions are now invalid?
**For Engineering:** How should deployment strategies change?
**For Intuition:** What mental models need updating?
**False Hope:** What does the revised principle NOT enable?
```

### Step 5: Map to Revised Mental Model
Synthesize the change in understanding.

```markdown
**Old Model:** [Prior belief and its predictions]
**New Model:** [Revised principle and its predictions]
**What Changed:** [The specific contradiction]
**Validation:** [How to verify the new model in your own work]
```

---

## Output Skill Format

Generate a new SKILL.md with:

**Frontmatter:**
```yaml
---
name: [kebab-case-paradigm-name]
title: [Paradigm Challenge: Rethinking {Belief}]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [verified arxiv link to source paper]
keywords: [paradigm-challenge, falsified-belief, revised-principle, {domain}, {old-assumption}]
description: Overturn the assumption that {prior belief} by understanding {revised principle}. Includes the falsifying experiment from {paper source}, implications for {practice area}, enabling practitioners to {outcome} when {prior approach} fails.
---
```

**Content structure:**
1. **Prior Belief** (1 paragraph): What the community believed and why
2. **The Falsifying Experiment** (2-3 bullet points): The core evidence that disproves it
3. **Revised Principle** (1 paragraph): What is actually true
4. **Implications for Practice** (3-4 bullet points): How to change your approach
5. **When to Use This Understanding** (1-2 sentences): When the revised principle applies
6. **When the Old Model Still Applies** (1-2 sentences): Scope limitations of the new principle
7. **Validation Checklist** (3-4 bullet points): How to verify the revised principle in your work

**Length:** 150-250 lines

---

## Processing Instructions

1. **Obtain the paper:** Fetch HTML from arxiv.org/html/{arxiv_id}, fallback to PDF
2. **Identify the thesis:** Look for explicit statements of what belief is being challenged
3. **Find the falsifying experiment:** Locate the core evidence that proves the belief wrong
4. **Extract design details:** Understand what makes the experiment convincing
5. **Synthesize revision:** Determine the corrected understanding
6. **Map implications:** Trace how this changes what practitioners should do
7. **Validate paradigm challenge:** Confirm this is ADVERSARIAL (proving wrong) not EXPLORATORY (discovering new)
8. **Generate skill:** Write output skill following the format above

---

## Quality Checks

- [ ] Paper explicitly argues against a widely-held belief or conventional wisdom
- [ ] Core experiment clearly falsifies the prior belief (not ambiguous)
- [ ] Revised principle is articulated and different from prior belief
- [ ] Paper provides scope for where revised principle applies/doesn't apply
- [ ] Implications for practice are extracted, not speculative
- [ ] Output skill makes the paradigm shift clear to someone unfamiliar with the paper
- [ ] Description is under 1024 characters, includes both belief and revision
- [ ] Keywords (5-10) include "paradigm-challenge" and reference the falsified belief
- [ ] Engine tag matches skillxiv-v0.0.2-claude-opus-4.6

---

## Distinguishing from Exploratory

**Paradigm Challenge (use this skill):**
- "We prove that X is not true" with falsifying evidence
- "Conventional wisdom about Y is wrong because [experiment]"
- "Prior understanding of Z should be revised to [revision]"
- Adversarial framing: explicit contradiction

**Exploratory (do NOT use this skill):**
- "We study what happens when X" without prior contradicting belief
- "We find that Y works better than Z" without arguing Z was fundamentally wrong
- "We propose a new understanding of Z" without evidence prior understanding was false
- Discovery framing: finding something new, not proving something old wrong

---

## Common Pitfalls

- **Confusing "better" with "disproven":** A paper that improves on prior work doesn't necessarily disprove the principle
- **Missing the scope:** Revised principle might only apply to specific settings; extract the boundary conditions
- **Overselling implications:** Some paradigm challenges have narrow applicability; don't generalize beyond the falsifying experiment
- **False paradigm challenges:** Some papers claim to disprove beliefs that are already nuanced in the literature
- **Ignoring caveats:** Paper might show belief is wrong in one setting but still useful in others; extract both
