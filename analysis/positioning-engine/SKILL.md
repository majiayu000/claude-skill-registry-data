---
name: positioning-engine
description: >
  Activate when the user needs to analyze how their paper positions itself
  relative to the closest existing work. Builds a differentiation matrix,
  identifies unique positioning, and generates a positioning statement that
  strengthens the contribution argumentation. Complements the theory-engine
  by focusing on the competitive landscape of related papers.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Positioning Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (positioning-engine)
> **Input:** Paper draft + [N] comparison papers identified
> **Output:** Differentiation matrix with [N] dimensions, positioning_analysis.md saved
> ```

# Positioning Engine

## Core Principle

"How is your paper different from X?" is the question every reviewer asks. This
engine produces a systematic answer. It identifies the 5-10 most similar existing
papers, builds a structured differentiation matrix, and generates a positioning
statement that makes the unique contribution explicit and defensible.

The output directly strengthens the Introduction (gap + contribution paragraphs)
and the Discussion (theoretical implications).

## When to Activate

- User says "position my paper", "how is this different from X?", "differentiation"
- User says "compare to related work", "positioning analysis", "unique contribution"
- During Phase 2 (Framing) to sharpen the gap and contribution
- When a reviewer challenges the novelty or contribution
- User runs `/analyze-positioning`

## Prerequisites

- `draft.md` or `paper.tex` exists (to understand the paper's claims)
- `references.bib` and/or `literature_base.csv` exist (comparison candidates)
- Research questions and contribution are at least tentatively defined

---

## Step 1: IDENTIFY Closest Competitors

### Finding the Most Similar Papers

Sources for comparison papers:

1. **From the paper itself:** Papers cited in the Introduction and Related Work
   that address the same or very similar research questions
2. **From `literature_base.csv`:** Papers with the highest topical overlap
3. **From snowballing:** Forward citations of the paper's key references that
   appeared after those references were published
4. **Direct search:** Search for papers with very similar titles or identical keywords

### Selection Criteria

Select 5-10 papers that are the **closest competitors** — papers that a reviewer
might say "but Author X already did this." These are papers that:

- Address the same or very similar research questions
- Study the same phenomenon in a similar context
- Use a similar methodology
- Apply the same theoretical lens
- Were published recently (high overlap risk)

### Output

For each selected paper, extract:
```
{
  "bib_key": "[key]",
  "title": "[title]",
  "authors": "[authors]",
  "year": [year],
  "venue": "[venue]",
  "rq": "[their research question or objective]",
  "method": "[their method]",
  "theory": "[their theoretical lens]",
  "context": "[their empirical context]",
  "key_finding": "[their main finding]",
  "similarity_to_ours": "high/medium",
  "citation_count": [N]
}
```

---

## Step 2: BUILD Differentiation Matrix

### Matrix Structure

Build a table comparing the competitor papers against YOUR paper across key dimensions:

```markdown
## Differentiation Matrix

| Dimension | Our Paper | [Author1 (Year)] | [Author2 (Year)] | [Author3 (Year)] | ... |
|-----------|-----------|-------------------|-------------------|-------------------|-----|
| **Research Question** | [our RQ] | [their RQ] | [their RQ] | [their RQ] | |
| **Theoretical Lens** | [our theory] | [their theory] | [their theory] | [their theory] | |
| **Method** | [our method] | [their method] | [their method] | [their method] | |
| **Context/Sample** | [our context] | [their context] | [their context] | [their context] | |
| **Time Period** | [our period] | [their period] | [their period] | [their period] | |
| **Technology Focus** | [our tech] | [their tech] | [their tech] | [their tech] | |
| **Unit of Analysis** | [our UoA] | [their UoA] | [their UoA] | [their UoA] | |
| **Key Contribution** | [our contribution] | [their contribution] | [their contribution] | [their contribution] | |
| **Scope** | [our scope] | [their scope] | [their scope] | [their scope] | |
```

### Dimension Selection

Choose 6-10 dimensions that are most relevant for differentiation. Common dimensions:

| Dimension | When to Use |
|-----------|------------|
| Research Question / Objective | Always |
| Theoretical Lens | When theory is a differentiator |
| Method | When method is a differentiator |
| Context / Industry / Sample | When context is new |
| Time Period / Technology Generation | When recency matters |
| Level of Analysis (individual, team, org, industry) | When level differs |
| Unit of Analysis | When what's being studied differs |
| Geographic / Cultural Context | For cross-cultural studies |
| Dependent Variables / Outcomes | When outcomes differ |
| Stage of Adoption / Maturity | For implementation studies |
| Practitioner vs. Academic Focus | For applied research |

---

## Step 3: ANALYZE Positioning

### Gap Identification

From the differentiation matrix, identify:

1. **Unique dimensions:** Where does our paper differ from ALL competitors?
   - These are the strongest positioning arguments

2. **Underrepresented combinations:** What combination of dimensions is new?
   - Even if individual dimensions are not new, the combination may be

3. **Temporal advantage:** What has changed since the competitors published?
   - New technology, new phenomena, new policy context

4. **Methodological gap:** What method has NOT been applied to this topic?
   - E.g., many surveys, no case studies; many qualitative, no quantitative

5. **Contextual gap:** What context has NOT been studied?
   - E.g., many US studies, no European context; many large enterprises, no SMEs

### Positioning Patterns

Classify the paper's positioning into one or more patterns:

| Pattern | Description | Strength |
|---------|-------------|----------|
| **New phenomenon** | Studies something that didn't exist before | Very strong |
| **New context** | Applies known theories to unstudied context | Strong |
| **New method** | Uses a method not yet applied to this topic | Strong |
| **New theory** | Applies a theory not yet used for this topic | Medium-Strong |
| **Integration** | Combines previously separate research streams | Medium |
| **Replication** | Tests prior findings in new setting | Medium |
| **Update** | Revisits topic after significant change | Medium |
| **Deeper** | Goes beyond surface-level prior work | Depends on execution |

---

## Step 4: GENERATE Positioning Statement

### Positioning Paragraph Template

Generate a paragraph that can be directly inserted into the Introduction (Gap section)
or Related Work:

```markdown
While prior work has made important contributions to understanding [topic],
significant opportunities for advancement remain. Table [N] compares our study
to the most closely related work. [Author1] (Year) [their focus], but [key
difference from our paper]. Similarly, [Author2] (Year) [their contribution],
yet [what they don't address that we do]. [Author3] (Year) comes closest to
our work in [dimension], but differs in [key differentiator: method/context/theory].

Our study extends this body of work in [N] key ways. First, [unique dimension 1].
While prior studies have [what they did], we [what we do differently]. Second,
[unique dimension 2]. Third, [unique dimension 3, if applicable].
```

### Contribution Refinement

Based on the positioning analysis, refine the contribution statement:

```markdown
## Refined Contribution Statement

Based on the positioning analysis, the paper's unique contribution is:

1. **[Contribution 1]** — This is unique because no prior study has [specific gap].
   Closest competitor: [Author (Year)] who [what they did, but not this].

2. **[Contribution 2]** — This extends [theory/method] by [specific extension].
   Unlike [Author (Year)] who [their approach], we [our approach].

3. **[Contribution 3]** — Practical contribution: [specific practical value].
   This goes beyond [Author (Year)]'s [their practical contribution] by [how].
```

---

## Step 5: SAVE Output

### Output File: `positioning_analysis.md`

```markdown
# Positioning Analysis

**Paper:** [title]
**Date:** [ISO 8601]
**Competitors analyzed:** [N]

## Closest Competitors

[Brief 2-3 sentence description of each competitor paper]

## Differentiation Matrix

[Full matrix from Step 2]

## Positioning Assessment

### Unique Dimensions
[List dimensions where our paper is unique]

### Positioning Pattern
[Classified pattern from Step 3]

### Strongest Differentiators
1. [Differentiator 1 — why it matters]
2. [Differentiator 2 — why it matters]
3. [Differentiator 3 — why it matters]

### Potential Reviewer Challenges
[Anticipated "but Author X already did this" objections + prepared responses]

## Draft Positioning Paragraph
[Ready-to-insert paragraph from Step 4]

## Refined Contribution Statement
[Updated contribution claims from Step 4]

## Recommended Actions
- [ ] Insert differentiation table into Related Work section
- [ ] Update Introduction gap paragraph with positioning language
- [ ] Refine contribution statement in Introduction
- [ ] Add competitor comparison to Discussion section
```

---

## Error Recovery

- **No clearly similar papers found:** The paper may be highly novel (good!) or
  the search was too narrow. Expand search to adjacent topics.
- **Too many similar papers (>10):** Focus on the 5 most similar. Group the rest
  into clusters.
- **Paper appears to have no unique contribution:** Flag this honestly. Suggest
  ways to differentiate: new context, updated data, different method, integrative perspective.
- **Competitor paper discovered that is very close:** This is valuable information!
  Better to discover this now than during review. Help the user explicitly differentiate.

---

## Integration

| Scenario | Integration |
|----------|-------------|
| Phase 2 (Framing) | Positioning analysis sharpens gap + contribution |
| Theory-engine | Theory selection informed by what competitors used |
| Writing-engine | Positioning paragraph for Introduction/Related Work |
| Peer-review-engine | Anticipates reviewer objections about novelty |
| Review-engine | Responds to "how is this different from X?" reviewer comments |
