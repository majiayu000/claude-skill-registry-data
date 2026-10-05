---
name: APESsrc
description: Evaluates the faithfulness of abstractive summaries by verifying if factual claims (masked as cloze questions) in the reference summary can be correctly answered using only the generated summary, compared against a gold-standard answer derived from the source context. Use when the user has predictions and gold and needs to compute APESsrc.
metadata:
  skill_kind: metric
  source_arxiv: 2104.02112
  bibtex_key: huang2021efficientattentions
  confidence: high
---

# APESsrc

> Efficient Attentions for Long Document Summarization — Huang et al. (2021) (arXiv:2104.02112, 2021)

## What this evaluates

Evaluates the faithfulness of abstractive summaries by verifying if factual claims (masked as cloze questions) in the reference summary can be correctly answered using only the generated summary, compared against a gold-standard answer derived from the source context.

## Datasets

- **GovReport** — total ?; splits: test (-1)
- **PubMed** — total ?; splits: test (-1)

## Metrics

- `APESsrc` **(primary)** — range: [0, 1]
  - Unigram F1 score between the answer span predicted by a QA model reading the system summary ($a_{sys}$) and the answer span predicted by the same QA model reading the source context ($a_{cxt}$).

## Input / output format

**Input**: Cloze question $q$ (constructed by masking entities, events, and numbers in the reference summary), the system-generated summary, and the source context (greedily selected sentences maximizing ROUGE-2 recall improvement over the reference).

**Output**: Answer span $a_{sys}$ extracted from the system summary, and answer span $a_{cxt}$ extracted from the source context.

## Scoring recipe

```python
def compute_apes_src(q, sys_summary, src_context):
    a_sys = qa_model.predict_span(q, sys_summary)
    a_cxt = qa_model.predict_span(q, src_context)
    if a_sys is None or a_cxt is None:
        return None
    return unigram_f1(a_sys, a_cxt)
```

## Common pitfalls

- The metric relies on a BERT-based QA model fine-tuned to predict answer spans, not a generative language model.
- The source context is not the full document but a subset of sentences greedily selected to maximize ROUGE-2 recall improvement over the reference summary.
- Samples where the gold answer cannot be found in the selected context are excluded from evaluation.

## Evidence (verbatim from paper)

> Different from APES, we further use the QA model to read the context (sentences selected from the source) and give an answer $a_{cxt}$ to the question $q$. We compute a unigram F1 by comparing $a_{sys}$ and $a_{cxt}$, denoted as APESsrc.

## Citation

```bibtex
@misc{huang2021efficientattentions,
  title={Efficient Attentions for Long Document Summarization},
  author={Huang et al. (2021)},
  year={2021},
  note={arXiv:2104.02112}
}
```

- arXiv: 2104.02112
