---
name: research-paper-writing
description: "ML paper pipeline: experiment design to submission."
allowed-tools:
  - bash
  - write_file
  - read_file
  - web_search
  - browse_page
enabled: true
related-skills: [arxiv, academic-paper-review, plan]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); Orchestra Research
---

# Research Paper Writing Pipeline

## Overview

End-to-end pipeline for producing publication-ready ML/AI research papers
targeting **NeurIPS, ICML, ICLR, ACL, AAAI, COLM**. Covers the full research
lifecycle: experiment design, execution, analysis, paper writing, review,
revision, and submission.

This is **not a linear pipeline** — it is an iterative loop. Results trigger
new experiments. Reviews trigger new analysis.

## When to Use

- User is writing an ML/AI research paper for a top venue
- User needs help with experiment design, execution, or analysis
- User wants feedback on a draft
- User is preparing a submission package

## Pipeline Phases

```
Phase 0: Project Setup → Phase 1: Literature Review
       │                        │
       ▼                        ▼
Phase 2: Experiment      Phase 5: Paper Drafting ◄──┐
       Design                  │                    │
       │                       ▼                    │
       ▼                 Phase 6: Self-Review       │
Phase 3: Execution            & Revision ───────────┘
       & Monitoring              │
       │                         ▼
       ▼                   Phase 7: Submission
Phase 4: Analysis
```

### Phase 0: Project Setup

- Define research question and hypothesis
- Identify target venue + deadline
- Set up project structure:
  ```
  project/
  ├── experiments/
  ├── data/
  ├── src/
  ├── paper/
  │   ├── main.tex
  │   ├── figures/
  │   └── references.bib
  └── README.md
  ```
- Initialize git repo, set up environment

### Phase 1: Literature Review

- Use `arxiv` skill to find related work
- Use `web_search` for non-arXiv papers (Semantic Scholar, Google Scholar)
- Use `browse_page` to read key papers in full
- Build a `references.bib` with all cited works
- Identify the gap your work fills

### Phase 2: Experiment Design

- Define baselines and comparison methods
- Choose datasets and evaluation metrics
- Design ablation studies
- Plan computational budget
- Write pre-registration document (optional but recommended)

### Phase 3: Execution & Monitoring

```bash
# Run experiments
python src/train.py --config configs/exp1.yaml

# Monitor with logging
python src/train.py --config configs/exp1.yaml --log-dir runs/exp1

# Track experiments
python src/eval.py --checkpoint runs/exp1/best.pt --eval-set test
```

- Log all hyperparameters, seeds, and environment details
- Save checkpoints for reproducibility
- Run each experiment with multiple seeds (3-5)

### Phase 4: Analysis

- Aggregate results across seeds
- Compute statistical significance (paired t-test, bootstrap CI)
- Generate comparison tables and plots:
  ```bash
  python src/plot.py --results runs/ --output paper/figures/
  ```
- Run ablation analysis
- Identify surprising findings (investigate, don't hide)

### Phase 5: Paper Drafting

Follow venue template structure:
1. **Abstract** — problem, method, key result, impact (write last)
2. **Introduction** — motivation, contribution summary, roadmap
3. **Related Work** — position within literature (from Phase 1)
4. **Method** — approach, architecture, training procedure
5. **Experiments** — setup, main results, ablations, analysis
6. **Conclusion** — summary, limitations, future work

Writing principles:
- **One idea per paragraph**
- **Figures tell the story** — design figures first, write text around them
- **Tables for comparisons** — main results table + ablation table
- **Reproducibility** — include all hyperparameters, release code

### Phase 6: Self-Review & Revision

Use `academic-paper-review` skill to self-review:
- Read the paper cold (fresh eyes)
- Check methodology soundness, novelty, reproducibility
- Identify weaknesses and fix them
- Get feedback from collaborators

### Phase 7: Submission

- Check venue formatting requirements
- Verify page limits
- Anonymize for blind review (if applicable)
- Prepare supplementary material (code, data, extended results)
- Submit before deadline (not at 23:59)

## Statistical Analysis

```bash
# Multiple seeds — compute mean ± std
python3 -c "
import numpy as np
results = [0.85, 0.83, 0.86, 0.84, 0.82]  # per-seed results
print(f'Mean: {np.mean(results):.4f} ± {np.std(results):.4f}')
"

# Paired t-test vs baseline
python3 -c "
from scipy import stats
baseline = [0.80, 0.79, 0.81, 0.78, 0.80]
ours = [0.85, 0.83, 0.86, 0.84, 0.82]
t, p = stats.ttest_rel(ours, baseline)
print(f't={t:.3f}, p={p:.4f}')
"
```

## Pitfalls

- **Single seed**: results from one seed are not reliable. Use 3-5 minimum.
- **Cherry-picking**: report all results, not just the best seed.
- **No ablations**: reviewers will ask "does each component matter?" — answer
  proactively.
- **Missing related work**: reviewers know the field. Cite comprehensively.
- **Unclear contributions**: list contributions explicitly in the introduction.
- **Overclaiming**: "state-of-the-art" needs evidence across datasets, not one.
- **Last-minute submission**: servers crash at deadlines. Submit early.

## Dependencies

This skill benefits from: `numpy`, `scipy`, `matplotlib` (analysis + plots).
Install via `pip install numpy scipy matplotlib`.
