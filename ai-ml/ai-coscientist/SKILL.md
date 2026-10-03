---
name: ai-coscientist
title: "Training AI Co-Scientists Using Rubric Rewards"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.23707
keywords: [research, reinforcement-learning, rubric-rewards, cross-domain]
description: "Train LLMs to generate high-quality research plans via rubric-based RL without requiring experimental verification. Extracts research goals and domain-specific rubrics from scientific papers, uses frozen model as grader with 12-22% relative improvements, achieves human-expert preference 70% of time with strong cross-domain generalization."
---

## Overview

Automated research plan generation using extractable domain knowledge from papers.

## Core Technique

**Rubric Extraction and Grading:**

```python
# Extract from papers
research_rubrics = extract_rubrics_from_papers(papers)

# Grade via frozen model
grade = frozen_model.score(generated_plan, rubrics)

# GRPO training on grade signal
```

## When to Use

Use when: Research automation, domain-specific planning, cross-domain generalization.

## References

- Rubric extraction from scientific papers
- Frozen model as grader
- Self-reward GRPO training
