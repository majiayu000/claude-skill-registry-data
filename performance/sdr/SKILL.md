---
name: SDR
description: Evaluates how effectively audio separation models isolate specific stems from a mixed recording while preserving signal integrity. It quantifies the ratio of target source energy to residual interference and distortion energy. Use when the user has predictions and gold and needs to compute SDR.
metadata:
  skill_kind: metric
  source_arxiv: 2305.07489
  bibtex_key: solovyev2023benchmarks
  confidence: high
---

# SDR

> Benchmarks and leaderboards for sound demixing tasks — Solovyev et al. (2023) (arXiv:2305.07489, 2023)

## What this evaluates

Evaluates how effectively audio separation models isolate specific stems from a mixed recording while preserving signal integrity. It quantifies the ratio of target source energy to residual interference and distortion energy.

## Datasets

- **Unspecified in section** — total ?; splits: test (-1)

## Metrics

- `SDR` **(primary)** — range: other
  - Per-stem SDR is 10 * log10(sum(s_stem,n^2) / sum(e_stem,n^2)), where s is ground truth and e is estimate. Record score averages SDR across all stems in a track. Total score averages across all test records.

## Input / output format

**Input**: Mixed audio waveform and ground truth stem waveforms.

**Output**: Estimated waveform for each target stem.

## Scoring recipe

```python
def compute_sdr(stem, estimate):
    return 10 * log10(sum(stem**2) / sum(estimate**2))

def compute_sdr_total(stems, estimates, records):
    record_scores = []
    for record in records:
        stem_scores = [compute_sdr(s, e) for s, e in zip(record.stems, record.estimates)]
        record_scores.append(mean(stem_scores))
    return mean(record_scores)
```

## Common pitfalls

- SDR is computed per stem before averaging, not directly on the full mixture.
- Higher SDR values indicate better separation performance.
- The metric measures energy ratio in dB and does not capture perceptual quality or phase errors.

## Evidence (verbatim from paper)

> The signal-to-distortion ratio (SDR) is a common metric used to evaluate the quality of audio separation algorithms. It is a measure of how well the desired audio sources have been separated from the mixture, while minimizing the distortion caused by residual interference.
The SDR is defined as follows:

|  | $SDR_{stem}\=10\cdot\log_{10}\left(\frac{\sum\limits_{n\=1}^{N}s_{stem,n}^{2}}{\sum\limits_{n\=1}^{N}e_{stem,n}^{2}}\right)$ |  | (1) |
| --- | --- | --- | --- |

where $s_{stem,n}$ is the waveform of the ground truth and $e_{stem,n}$ denotes the waveform of the estimate. The higher the SDR score, the better the output of the system is.

To rank the entire system, the average SDR across all stems is used for each record:

|  | $SDR_{record}\=\frac{1}{N}\sum_{i\=1}^{N}SDR_{i},$ |  | (2) |
| --- | --- | --- | --- |

where $N$ is the total number of stems in a given record, and $SDR_{i}$ is the SDR value for the $i$-th stem.

Finally, the overall score $SDR_{total}$ is the average of the scores for all records in the test set.

## Citation

```bibtex
@misc{solovyev2023benchmarks,
  title={Benchmarks and leaderboards for sound demixing tasks},
  author={Solovyev et al. (2023)},
  year={2023},
  note={arXiv:2305.07489}
}
```

- arXiv: 2305.07489
