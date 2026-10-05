---
name: t5-eval
description: Evaluates a unified text-to-text transformer's ability to generalize across diverse NLP tasks including language understanding, summarization, question answering, and machine translation. The protocol tests the efficacy of pre-training objectives, data scaling, and consistent text-to-text fine-tuning pipelines. Use when the user wants to benchmark on GLUE, SuperGLUE, CNN/Daily Mail, SQuAD, WMT, or asks about evaluating this task. Reports GLUE average score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1910.10683
  bibtex_key: raffel2019t5
  confidence: high
---

# t5-eval

> Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer — Colin Raffel et al. (arXiv:1910.10683, 2019)

## What this evaluates

Evaluates a unified text-to-text transformer's ability to generalize across diverse NLP tasks including language understanding, summarization, question answering, and machine translation. The protocol tests the efficacy of pre-training objectives, data scaling, and consistent text-to-text fine-tuning pipelines.

## Datasets

- **GLUE** — total ?; splits: val (-1)
- **SuperGLUE** — total ?; splits: val (-1)
- **CNN/Daily Mail** — total ?; splits: val (-1)
- **SQuAD** — total ?; splits: val (-1)
- **WMT** — total ?; splits: val (-1)

## Metrics

- `GLUE average score` **(primary)** — range: [0, 100]
  - Average of scores across all GLUE subtasks, as stipulated by the official benchmark.
- `BLEU` — range: [0, 100]
  - BLEU score computed using SacreBLEU v1.3.0 with 'exp' smoothing and 'intl' tokenization.
- `ROUGE-2-F` — range: [0, 1]
  - ROUGE-2 F1 score, reported as a proxy for ROUGE-1-F and ROUGE-L-F due to high correlation on CNN/Daily Mail.
- `Exact Match` — range: [0, 1]
  - Exact match score for SQuAD, reported as a proxy for F1 due to high correlation.

## Input / output format

**Input**: Text string formatted as a task-specific prefix followed by the input content (e.g., 'translate English to German: ...'). All tasks are unified into a text-to-text format.

**Output**: Text string generated via greedy decoding, representing the target answer, label, or translation.

## Scoring recipe

```python
def compute_metrics(predictions, golds, metric):
    if metric == 'glue_avg':
        return mean([compute_subtask_score(p, g) for p, g in zip(predictions, golds)])
    elif metric == 'bleu':
        return sacrebleu.corpus_bleu(predictions, [golds], smooth_method='exp', tokenize='intl')
    elif metric == 'rouge2f':
        return rouge_score(golds, predictions, rouge_types=['rouge2']).rouge2.fmeasure
    elif metric == 'exact_match':
        return sum(1 for p, g in zip(predictions, golds) if p.strip() == g.strip()) / len(golds)
```

## Common pitfalls

- Results are reported on validation sets to avoid test set leakage, not on held-out test sets.
- High inter-run variance on low-resource tasks (CoLA, CB, COPA) can disproportionately skew GLUE and SuperGLUE averages.
- Proxy metrics (ROUGE-2-F, Exact Match) are used instead of full metric suites due to high correlation, which may mask task-specific performance differences.

## Evidence (verbatim from paper)

> For GLUE and SuperGLUE, we report the average score across all subtasks (as stipulated by the official benchmarks) under the headings "GLUE" and "SGLUE". For all translation tasks, we report the BLEU score (Papineni et al., 2002) as provided by SacreBLEU v1.3.0 (Post, 2018) with "exp" smoothing and "intl" tokenization. ... For CNN/Daily Mail, we find the performance of models on the ROUGE-1-F, ROUGE-2-F, and ROUGE-L-F metrics (Lin, 2004) to be highly correlated so we report the ROUGE-2-F score alone under the heading "CNNDM". Similarly, for SQuAD we find the performance of the "exact match" and "F1" scores to be highly correlated so we report the "exact match" score alone.

## Citation

```bibtex
@misc{raffel2019t5,
  title={Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer},
  author={Colin Raffel et al.},
  year={2019},
  note={arXiv:1910.10683}
}
```

- arXiv: 1910.10683
