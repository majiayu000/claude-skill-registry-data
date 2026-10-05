---
name: l-eval
description: Evaluates long-context language models across 20 diverse sub-tasks spanning 3k–200k tokens, probing retrieval, reasoning, summarization, and instruction understanding. It specifically tests whether models can maintain performance and follow length constraints when context length increases, highlighting the failure of traditional n-gram metrics and the need for length-instruction-enhanced evaluation. Use when the user wants to benchmark on L-Eval, or asks about evaluating this task. Reports exact-match accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2307.11088
  bibtex_key: an2023leval
  confidence: high
---

# l-eval

> L-Eval: Instituting Standardized Evaluation for Long Context Language Models — Chenxin An et al. (2023) (arXiv:2307.11088, 2023)

## What this evaluates

Evaluates long-context language models across 20 diverse sub-tasks spanning 3k–200k tokens, probing retrieval, reasoning, summarization, and instruction understanding. It specifically tests whether models can maintain performance and follow length constraints when context length increases, highlighting the failure of traditional n-gram metrics and the need for length-instruction-enhanced evaluation.

## Datasets

- **L-Eval** — total 508; splits: test (-1); repo https://github.com/OpenLMLab/LEval

## Metrics

- `exact-match accuracy` **(primary)** — range: percent
  - Percentage of closed-ended questions where the model's output exactly matches the ground truth answer. Calculated as 100 divided by the number of questions per item.
- `ROUGE-L` — range: [0, 1]
  - Recall-oriented lexical matching metric based on the longest common subsequence between the generated text and the reference answer.
- `F-1` — range: [0, 1]
  - Harmonic mean of precision and recall computed over token-level overlap between prediction and reference.
- `LLM judge win-rate` — range: percent
  - Percentage of pairwise comparisons where the model's output is preferred over the baseline (GPT-4 Turbo-16k) by an LLM judge, given the query and reference answer.
- `Human score` — range: [1, 5]
  - Average rating assigned by human annotators on a 1-to-5 scale, where 1 indicates poor output and 5 indicates excellent output.

## Input / output format

**Input**: Long documents (3k–200k tokens) paired with task-specific instructions. For length-instruction-enhanced (LIE) evaluation, the exact word count of the reference answer is injected into the prompt (e.g., 'We need a 50-word summary').

**Output**: Model-generated text responses (answers, summaries, or extracted information) or selected options for multiple-choice questions.

## Scoring recipe

```python
def compute_metrics(predictions, gold, metric_type):
    if metric_type == 'exact_match':
        return sum(1 for p, g in zip(predictions, gold) if p.strip() == g.strip()) / len(predictions) * 100
    elif metric_type in ['rouge_l', 'f1']:
        return compute_lexical_overlap(predictions, gold)
    elif metric_type == 'llm_judge':
        wins = 0
        for p, g, q in zip(predictions, gold, queries):
            prompt = f'Q: {q}\nRef: {g}\nPred: {p}\nJudge: prefer pred over baseline?'
            if judge_prefers(prompt): wins += 1
        return wins / len(predictions) * 100
    elif metric_type == 'human':
        return sum(human_scores) / len(human_scores)
```

## Common pitfalls

- N-gram metrics (ROUGE-L, F-1) exhibit severe length bias, heavily penalizing models that generate longer outputs than the reference even if the content is correct.
- Standard LLM judges (e.g., GPT-4) favor verbose answers and struggle to verify details in long contexts without explicit length constraints or reference-grounded prompts.
- Assuming automated metrics correlate with human judgment; the paper shows Kendall-Tau correlations are low for n-gram metrics unless length instructions are added.

## Evidence (verbatim from paper)

> N-gram metrics like ROUGE-L (R-L) and F-1 score are widely used in traditional datasets and they are also widely adopted in the text generation benchmarks via performing lexical matching. It is worth noting that n-gram matching metrics are very sensitive to the length of the ground truth, exhibiting a length bias.

## Citation

```bibtex
@misc{an2023leval,
  title={L-Eval: Instituting Standardized Evaluation for Long Context Language Models},
  author={Chenxin An et al. (2023)},
  year={2023},
  note={arXiv:2307.11088}
}
```

- arXiv: 2307.11088
