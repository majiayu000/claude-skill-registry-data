---
name: paper-reviewer
description: Expert academic paper review including summary, methodology critique, and practical implications
version: 1.0.0
author: USER
tags: [paper-review, academic, research, methodology, analysis]
---

# Paper Reviewer

## Purpose
Review and analyze academic papers, research reports, and technical whitepapers, providing summaries, critiques, and practical implications.

## Activation Keywords
- paper review, research paper
- academic paper, whitepaper
- summarize paper, paper analysis
- methodology critique, research findings
- arxiv, journal article

## Core Capabilities

### 1. Paper Summary
- Key contributions
- Methodology overview
- Main findings
- Conclusions
- Limitations acknowledged

### 2. Critical Analysis
- Methodology validity
- Statistical rigor
- Reproducibility assessment
- Bias identification
- Gap analysis

### 3. Context Placement
- Prior work comparison
- Novel contributions
- Field impact
- Citation network
- Related work mapping

### 4. Practical Implications
- Real-world applications
- Implementation considerations
- Adoption barriers
- Business relevance
- Technical feasibility

### 5. Quality Assessment
- Peer review status
- Author credentials
- Publication venue
- Citation count
- Replication studies

## Paper Review Structure

```markdown
## Paper Review: [Title]

### Metadata
- **Authors**: [Names and affiliations]
- **Venue**: [Journal/Conference]
- **Year**: [Publication year]
- **Citations**: [Count if available]
- **arXiv/DOI**: [Link]

### TL;DR
[2-3 sentence summary]

### Key Contributions
1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]

### Methodology
- **Approach**: [Brief description]
- **Data**: [Dataset used]
- **Evaluation**: [Metrics used]

### Main Results
| Metric | Result | Baseline |
|--------|--------|----------|
| [Metric 1] | X | Y |
| [Metric 2] | X | Y |

### Strengths
- [Strength 1]
- [Strength 2]

### Weaknesses
- [Weakness 1]
- [Weakness 2]

### Practical Implications
[How this applies to real-world use]

### My Assessment
- **Novelty**: X/5
- **Rigor**: X/5
- **Impact**: X/5
- **Clarity**: X/5
- **Overall**: X/5

### Should You Read It?
[Yes/No and for whom]
```

## Methodology Checklist

```markdown
## Methodology Assessment

### Experimental Design
- [ ] Clear hypothesis stated
- [ ] Appropriate baselines chosen
- [ ] Controlled variables identified
- [ ] Sample size justified
- [ ] Randomization described

### Data
- [ ] Dataset described adequately
- [ ] Data collection process clear
- [ ] Preprocessing documented
- [ ] Train/test split appropriate
- [ ] Data availability mentioned

### Evaluation
- [ ] Metrics appropriate for task
- [ ] Statistical significance tested
- [ ] Confidence intervals provided
- [ ] Multiple runs/seeds used
- [ ] Ablation studies included

### Reproducibility
- [ ] Code available
- [ ] Hyperparameters documented
- [ ] Compute requirements stated
- [ ] Environment specified
- [ ] Random seeds provided
```

## Critical Reading Questions

```
1. Problem Statement
   → Is the problem well-motivated?
   → Is it clearly defined?

2. Related Work
   → Are key prior works cited?
   → Is positioning accurate?

3. Methodology
   → Is the approach sound?
   → Are assumptions reasonable?

4. Experiments
   → Do experiments support claims?
   → Are baselines fair?

5. Results
   → Are improvements significant?
   → Are limitations acknowledged?

6. Conclusions
   → Do conclusions follow from results?
   → Are future directions reasonable?
```

## Example Usage

```
User: "Review the 'Attention Is All You Need' paper"

Paper Reviewer Response:

## Paper Review: Attention Is All You Need

### Metadata
- Authors: Vaswani et al. (Google Brain)
- Venue: NeurIPS 2017
- Citations: 100,000+
- arXiv: 1706.03762

### TL;DR
Introduces the Transformer architecture, replacing
recurrence with self-attention for sequence modeling,
achieving SOTA on translation while being faster to train.

### Key Contributions
1. Self-attention mechanism for sequences
2. Multi-head attention concept
3. Positional encoding approach
4. Massively parallel training

### Main Results
| Task | BLEU | Previous SOTA |
|------|------|---------------|
| EN-DE | 28.4 | 26.0 |
| EN-FR | 41.0 | 39.0 |

### Strengths
- Elegant, simple architecture
- Massive parallelization possible
- Strong empirical results
- Well-written, clear presentation

### Weaknesses
- Quadratic complexity with sequence length
- Positional encoding limitations
- Large compute requirements

### Practical Implications
Foundation for: GPT, BERT, modern LLMs
Essential reading for anyone in NLP/ML.

### My Assessment
- Novelty: 5/5 (paradigm shift)
- Rigor: 4/5 (solid experiments)
- Impact: 5/5 (changed the field)
- Clarity: 5/5 (exceptionally clear)
- Overall: 5/5

### Should You Read It?
YES - Essential for anyone in ML/AI.
One of the most influential papers of the decade.
```
