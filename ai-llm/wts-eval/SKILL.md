---
name: wts-eval
description: Evaluates fine-grained spatial-temporal understanding and instance-aware video-to-text captioning in pedestrian-centric traffic scenarios. Probes a model's ability to accurately describe location, attention, behavior, and context of pedestrians and vehicles in complex traffic videos. Use when the user wants to benchmark on WTS, or asks about evaluating this task. Reports LLMScore.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.15350
  bibtex_key: kong2024wts
  confidence: high
---

# wts-eval

> WTS: A Pedestrian-Centric Traffic Video Dataset for Fine-grained Spatial-Temporal Understanding — Kong et al. (2024) (arXiv:2407.15350, 2024)

## What this evaluates

Evaluates fine-grained spatial-temporal understanding and instance-aware video-to-text captioning in pedestrian-centric traffic scenarios. Probes a model's ability to accurately describe location, attention, behavior, and context of pedestrians and vehicles in complex traffic videos.

## Datasets

- **WTS** — total ?; splits: train (2120), val (860)

## Metrics

- `LLMScore` **(primary)** — range: [0, 1]
  - LLMScore = 0.7 * Score_sem + 0.3 * Score_syn. Score_sem is the equal-weighted average of binary correctness (1 if semantically correct per aspect, 0 otherwise) across Location, Attention, Behavior, and Context. Score_syn is the equal-weighted average of cosine similarities between OpenAI text-embedding-3-small embeddings of answers to subjective questions derived from candidate and ground truth captions.
- `BLEU-4` — range: [0, 1]
  - Standard n-gram precision metric with geometric mean up to 4-grams.
- `METEOR` — range: [0, 1]
  - Precision/recall metric with synonym and stemming matching.
- `ROUGE-L` — range: [0, 1]
  - F-measure based on longest common subsequence.
- `CIDEr` — range: [0, 1]
  - TF-IDF weighted n-gram similarity against a corpus of reference captions.

## Input / output format

**Input**: Video segment (single main view) + prompt template (P-A, P-B, or P-C) instructing the model to describe the video from a pedestrian perspective with domain-specific constraints.

**Output**: Natural language caption (average length ~58.7 words) covering Location, Attention, Behavior, and Context of pedestrians/vehicles.

## Scoring recipe

```python
def compute_llmscore(pred, gold):
    aspects = ['Location', 'Attention', 'Behavior', 'Context']
    sem_scores, syn_scores = [], []
    for asp in aspects:
        sem_scores.append(prompt_llm_binary(pred, gold, asp))
        emb_p = embed(get_answers(pred, asp), model='text-embedding-3-small')
        emb_g = embed(get_answers(gold, asp), model='text-embedding-3-small')
        syn_scores.append(cosine_similarity(emb_p, emb_g))
    score_sem = sum(sem_scores) / len(aspects)
    score_syn = sum(syn_scores) / len(aspects)
    return 0.7 * score_sem + 0.3 * score_syn
```

## Common pitfalls

- Traditional n-gram metrics (BLEU, ROUGE) often yield high scores for captions that miss critical fine-grained semantic details in traffic scenarios.
- The evaluation relies on a specific LLM (GPT-3.5-turbo) and embedding model (text-embedding-3-small) with a fixed prompt template; results may not generalize to other LLMs or prompt designs.
- Multi-view consistency is mentioned as a goal but the benchmark primarily uses a single 'main view' per scenario for evaluation.

## Evidence (verbatim from paper)

> To achieve this, inspired by the evaluation protocol in GPTScore *[[11]]*, our LLMScore has a prompt template includes task description (comparing two captions), ground truth caption ($G$), inferred caption ($C$), and consideration aspects (location, attention, behavior of pedestrian/vehicle, and environment). Semantic score quantifies the degree of semantic similarity between two sentences. In our approach, we instruct the LLM (GPT-3.5-turbo) to evaluate the semantic accuracy of the caption for each aspect Location, Attention, Behavior, Context with respect to the ground truth. We assign a score of $1$ to the aspect that is semantically correct, otherwise 0. We take an equal-weighted average of these scores and call this Semantic Score ($Score_{sem}$).

## Citation

```bibtex
@misc{kong2024wts,
  title={WTS: A Pedestrian-Centric Traffic Video Dataset for Fine-grained Spatial-Temporal Understanding},
  author={Kong et al. (2024)},
  year={2024},
  note={arXiv:2407.15350}
}
```

- arXiv: 2407.15350
