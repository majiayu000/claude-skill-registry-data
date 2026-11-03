---
name: rebuttal
description: >
  Prepare a paper for peer review. Reads the paper and experiment results,
  selects the strongest ablations, anticipates reviewer questions, finds
  weaknesses before submission, and drafts rebuttals to actual reviews.
  Use when the user asks about "reviewer questions", "anticipate
  reviewers", "rebuttal", "paper weaknesses", "defend the paper",
  "strengthen the paper", "select the strongest ablations", "fortify the
  paper", or "prepare for peer review".
argument-hint: "<venue name (optional)>"
---

# Rebuttal: Prepare for Peer Review

Venue: $ARGUMENTS

## Step 1: Read the Paper and Results

Discover the paper, result and config files as in Step 1 (Discover Files) of `/labrat:paper-check`, including wandb logs and checkpoint directories. Then list the paper's claims (contributions and experiments), its metrics and baselines, and every available run and its outcome, including the ablation variants the configs define.

## Step 2: Vulnerability Analysis

Identify weaknesses from a reviewer's perspective:

### Technical Weaknesses
- Missing baselines that reviewers would expect
- Evaluation metrics that don't fully capture the contribution
- Assumptions stated without justification
- Scalability or generalization concerns not addressed
- Missing error analysis or failure case discussion

### Presentation Weaknesses
- Claims stronger than evidence supports
- Missing related work that a reviewer in the area would know
- Unclear methodology (could someone reimplement from the paper alone?)
- Figures that don't clearly convey the intended message
- Inconsistencies between sections

### Experimental Weaknesses
- Small dataset size without justification
- Missing statistical significance tests
- No comparison with state-of-the-art on standard benchmarks
- Hyperparameter sensitivity not explored
- No computational cost comparison

## Step 3: Venue-Specific Anticipation

If a venue was given, use its matching entry below.

**Top-tier ML/CV conferences (CVPR, NeurIPS, ICLR, ECCV)**:
- Expect extensive ablation studies
- Strong baseline comparisons required
- Novelty must be clearly articulated
- Reproducibility is valued

**Workshops**:
- More tolerant of work-in-progress
- Interesting ideas valued over exhaustive evaluation
- Novel applications of existing methods are acceptable

**Journals**:
- Expect thorough related work discussion
- Deeper analysis and more experiments than conferences
- Writing quality and organization matter more

## Step 4: Question Generation

List the 10 most likely reviewer questions, most likely first, phrased as a reviewer would write them, in this form:
```
Q: [Reviewer question]
Motivation: [Why this would be asked]
Answerable: [Yes, cite Table X / No, would need experiment Y]
Draft response: [If answerable, 2-3 sentences]
```

## Step 5: Ablation Selection

Take each delta from Ablation analysis in `/labrat:compare` (same-step, interaction-checked), then rank:

| Run | Factor Changed | Primary Metric Delta | Narrative Strength | Include? |
|-----|---------------|--------------------|--------------------|----------|

Ranking criteria:
- **Impact magnitude**: how much does it change the primary metric? The largest improvement is the most convincing.
- **Narrative strength**: does it directly support a specific paper claim?
- **Uniqueness**: does it show something no other ablation shows?
- **Anticipated questions**: does it preemptively answer likely reviewer concerns?
- **Cost**: main paper vs appendix (based on space constraints)
- **Coverage**: together the picks prove the core contribution, show each component's value and answer the top questions from Step 4

Recommend: main paper (top 3-5) vs supplementary (rest).

## Step 6: Negative Results

Frame negative results as analysis, not failure ("We explored X but found it did not improve over Y because Z"), and put them in the supplementary if they do not fit the main paper.

## Step 7: Rebuttal Preparation

If responding to actual reviews:

1. **Read ALL reviews** before responding to any
2. **Identify common concerns** across reviewers
3. **Prioritize**: address factual errors first, then major concerns, then minor ones
4. **Be respectful**: thank reviewers, acknowledge valid points
5. **Be specific**: point to exact sections, tables, figures
6. **New experiments**: only promise what you can deliver in the rebuttal period

Rebuttal structure per reviewer:
```
We thank Reviewer X for their thoughtful feedback.

**[Major concern]**: [Direct response with evidence]

**[Specific question]**: [Concrete answer]

**[Suggestion]**: [How we will incorporate it]
```

## Output Format

```
## Rebuttal Report

### Weaknesses
[Table of categorized weaknesses with severity, prioritized]

### Recommended Ablation Subset
[Table with justification for each]

### Top 10 Anticipated Questions
[Numbered list with answerability and draft responses]

### Suggested Edits
[Specific paragraph-level improvements to strengthen before submission]
```

Add the per-reviewer rebuttal drafts from Step 7 when responding to actual reviews.
