---
name: academic-paper-review
description: "Structured peer-review of academic papers."
allowed-tools:
  - browse_page
  - web_search
  - write_file
  - present_files
enabled: true
related-skills: [arxiv, systematic-literature-review, deep-research]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Academic Paper Review

## Overview

Produces structured, peer-review-quality analyses of academic papers. Follows
review standards used by top-tier venues (NeurIPS, ICML, ACL, Nature, IEEE) to
provide rigorous, constructive, and balanced assessments.

Covers **summary, strengths, weaknesses, methodology assessment, contribution
evaluation, literature positioning, and actionable recommendations** — all
grounded in evidence from the paper itself.

## When to Use

- User provides a paper URL (arXiv, DOI, conference proceedings)
- User asks to "review", "analyze", "critique", "assess", or "summarize" a
  research paper
- User wants to understand strengths and weaknesses of a study
- User requests a peer-review-style evaluation

## Review Methodology

### Phase 1: Paper Comprehension

#### Step 1.1: Identify Paper Metadata

Extract: Title, Authors, Venue/Status, Year, Domain, Paper Type (Empirical /
Theoretical / Survey / Systems / Position).

#### Step 1.2: Deep Reading Pass

Read the paper systematically using `browse_page`:
1. **Abstract & Introduction** — Identify claimed contributions and motivation
2. **Related Work** — Note how authors position relative to prior art
3. **Methodology** — Understand the proposed approach in detail
4. **Experiments / Results** — Examine datasets, baselines, metrics, outcomes
5. **Discussion & Limitations** — Note self-identified limitations
6. **Conclusion** — Compare concluded claims against actual evidence

#### Step 1.3: Key Claims Extraction

List the paper's main claims explicitly:
```
Claim 1: [Specific claim]
Evidence: [What evidence supports this]
Strength: [Strong / Moderate / Weak]
```

### Phase 2: Critical Analysis

#### Step 2.1: Literature Context Search

Use `web_search` to understand the research landscape:
```
"[paper topic] state of the art [current year]"
"[key method name] comparison benchmark"
"[specific technique] limitations criticism"
```

Use `browse_page` on key related papers or surveys.

#### Step 2.2: Methodology Assessment

| Criterion | Questions to Ask | Rating |
|-----------|-----------------|--------|
| **Soundness** | Is the approach technically correct? | 1-5 |
| **Novelty** | What is genuinely new vs incremental? | 1-5 |
| **Reproducibility** | Are details sufficient? Code/data available? | 1-5 |
| **Experimental Design** | Are baselines fair? Ablations adequate? | 1-5 |
| **Statistical Rigor** | Results significant? Error bars? Multiple runs? | 1-5 |
| **Scalability** | Does it scale? Computational costs discussed? | 1-5 |

#### Step 2.3: Contribution Significance

| Level | Description |
|-------|-------------|
| **Landmark** | Fundamentally changes the field |
| **Significant** | Strong contribution advancing state of the art |
| **Moderate** | Useful contribution with some limitations |
| **Marginal** | Minimal advance over existing work |
| **Below threshold** | Does not meet publication standards |

### Phase 3: Review Synthesis

Produce the final review using this template:

```markdown
# Paper Review: [Paper Title]

## Paper Metadata
- **Authors**: [Author list]
- **Venue**: [Publication venue or preprint server]
- **Year**: [Year]
- **Domain**: [Research field]
- **Paper Type**: [Empirical / Theoretical / Survey / Systems / Position]

## Executive Summary
[2-3 paragraph summary of core contribution, approach, and main findings.
State overall assessment upfront.]

## Summary of Contributions
1. [First claimed contribution]
2. [Second claimed contribution]

## Strengths
### S1: [Concise strength title]
[Detailed explanation with specific references to sections, figures, tables.]

### S2: [Concise strength title]
[...]

## Weaknesses
### W1: [Concise weakness title]
[Detailed explanation. Explain impact. Suggest how to address.]

### W2: [Concise weakness title]
[...]

## Methodology Assessment
| Criterion | Rating (1-5) | Assessment |
|-----------|:---:|------------|
| Soundness | X | [Brief justification] |
| Novelty | X | [Brief justification] |
| Reproducibility | X | [Brief justification] |
| Experimental Design | X | [Brief justification] |
| Statistical Rigor | X | [Brief justification] |
| Scalability | X | [Brief justification] |

## Questions for the Authors
1. [Specific question]
2. [Question about methodology choices]

## Literature Positioning
[How does this work relate to current state of the art? Key related works cited?]

## Recommendations
**Overall Assessment**: [Accept / Weak Accept / Borderline / Weak Reject / Reject]
**Confidence**: [High / Medium / Low]
**Contribution Level**: [Landmark / Significant / Moderate / Marginal / Below threshold]

### Actionable Suggestions for Improvement
1. [Specific, constructive suggestion]
2. [Specific, constructive suggestion]
```

## Review Principles

- **Always suggest how to fix it** — Don't just point out problems; propose solutions
- **Give credit where due** — Acknowledge genuine contributions even in flawed papers
- **Be specific** — Reference exact sections, equations, figures, tables
- **Separate minor from major** — Distinguish fatal flaws from fixable issues

### Objectivity Standards

- ❌ "This paper is poorly written" (vague, unhelpful)
- ✅ "Section 3.2 introduces notation X without formal definition, making the
  proof in Theorem 1 difficult to follow. Consider adding a notation table."
  (specific, actionable)

## Adaptation by Paper Type

| Paper Type | Focus Areas |
|------------|-------------|
| **Empirical** | Experimental design, baselines, statistical significance, ablations |
| **Theoretical** | Proof correctness, assumption reasonableness, tightness of bounds |
| **Survey** | Comprehensiveness, taxonomy quality, coverage of recent work |
| **Systems** | Architecture decisions, scalability evidence, real-world deployment |
| **Position** | Argument coherence, evidence for claims, impact potential |

## Common Pitfalls

- ❌ Reviewing the paper you wish was written instead of the paper submitted
- ❌ Demanding additional experiments that are unreasonable in scope
- ❌ Penalizing the paper for not solving a different problem
- ❌ Being overly influenced by writing quality versus technical contribution
- ❌ Providing only a summary without critical analysis

## Quality Checklist

- [ ] Paper read completely (not just abstract and introduction)
- [ ] All major claims identified and evaluated against evidence
- [ ] At least 3 strengths and 3 weaknesses with specific references
- [ ] Methodology assessment table complete with ratings and justifications
- [ ] Literature search conducted to contextualize the contribution
- [ ] Recommendations are actionable and constructive
- [ ] Review tone is professional and respectful

## Output

- Output the complete review in Markdown
- Save to `.poirot/outputs/review-{paper-topic}.md` via `write_file`
- Present to user via `present_files`
