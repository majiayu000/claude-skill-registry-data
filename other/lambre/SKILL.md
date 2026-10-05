---
name: lambre
description: Evaluates the morphosyntactic well-formedness and grammaticality of generated natural language text. It measures how closely a generated sentence or corpus adheres to language-specific dependency rules extracted from treebanks. Use when the user has predictions and gold and needs to compute L'AMBRE.
metadata:
  skill_kind: metric
  source_arxiv: 2103.16590
  bibtex_key: pratapa2021lambre
  confidence: high
---

# lambre

> Evaluating the Morphosyntactic Well-formedness of Generated Texts — Pratapa et al. (2021) (arXiv:2103.16590, 2021)

## What this evaluates

Evaluates the morphosyntactic well-formedness and grammaticality of generated natural language text. It measures how closely a generated sentence or corpus adheres to language-specific dependency rules extracted from treebanks.

## Datasets

- (no dataset; pure metric skill)

## Metrics

- `L'AMBRE` **(primary)** — range: [0, 1]
  - Segment-level: weighted average of the percentage of applicable morphosyntactic rules satisfied within a segment. Corpus-level: macro-average of the empirical satisfiability counts for each applicable rule across the entire corpus.

## Input / output format

**Input**: A text segment or corpus, accompanied by a set of language-specific morphosyntactic rules and a dependency parser/tagger.

**Output**: A single floating-point score between 0 and 1.

## Scoring recipe

```python
def compute_lambre(text, rules, parser, corpus_level=False):
    tree = parser.parse(text)
    applicable = [r for r in rules if is_applicable(r, tree)]
    satisfactions = []
    for r in applicable:
        sat = count_satisfied(r, tree)
        total = count_applicable_instances(r, tree)
        satisfactions.append(sat / total if total > 0 else 0)
    if corpus_level:
        return mean(satisfactions)
    return weighted_average(satisfactions)
```

## Common pitfalls

- Requires a robust dependency parser capable of handling noisy or ungrammatical generated text, as parsing errors directly lower rule satisfaction counts.
- Segment-level and corpus-level scores use different aggregation methods (weighted average vs. macro-average of empirical counts), making them non-interchangeable.
- Rule coverage and accuracy depend heavily on the quality of the automatically extracted morphosyntactic rules from the source treebank.

## Evidence (verbatim from paper)

> In this section, we present L'AMBRE, a metric to gauge the morphosyntactic well-formedness of generated natural language sentences. ... The final score is a weighted average of the scores of individual rules. Our score lies between [0,1], where 1 and 0 represent that rules are perfectly satisfied or not satisfied at all respectively.

## Citation

```bibtex
@misc{pratapa2021lambre,
  title={Evaluating the Morphosyntactic Well-formedness of Generated Texts},
  author={Pratapa et al. (2021)},
  year={2021},
  note={arXiv:2103.16590}
}
```

- arXiv: 2103.16590
