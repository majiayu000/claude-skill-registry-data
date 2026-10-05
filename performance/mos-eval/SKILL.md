---
name: mos-eval
description: Evaluates the perceptual audio quality of neural vocoder outputs by measuring how closely synthesized speech matches natural human speech. It probes the model's ability to generate high-fidelity waveforms from mel-spectrograms without audible artifacts like jitter or metallic sounds. Use when the user wants to benchmark on Data-Baker (Chinese female speaker), or asks about evaluating this task. Reports MOS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2005.05106
  bibtex_key: yang2020multibandmelgan
  confidence: high
---

# mos-eval

> Multi-band MelGAN: Faster Waveform Generation for High-Quality Text-to-Speech — Geng Yang et al. (2020) (arXiv:2005.05106, 2020)

## What this evaluates

Evaluates the perceptual audio quality of neural vocoder outputs by measuring how closely synthesized speech matches natural human speech. It probes the model's ability to generate high-fidelity waveforms from mel-spectrograms without audible artifacts like jitter or metallic sounds.

## Datasets

- **Data-Baker (Chinese female speaker)** — total ?; splits: test (20); repo https://www.data-baker.com/open_source.html

## Metrics

- `MOS` **(primary)** — range: [1, 5]
  - Mean Opinion Score measured via subjective listening tests on a standard 1-5 scale. Ratings from 20 native Chinese speakers are averaged per sample, with 95% confidence intervals reported.

## Input / output format

**Input**: Normalized mel-spectrograms extracted with 50 ms frame length, 12.5 ms frame shift, and 1024-point FFT. For TTS pipeline evaluation, syllable sequences with tone index and prosodic boundaries are used to generate mel-spectrograms via Tacotron2.

**Output**: 16 kHz audio waveform.

## Scoring recipe

```python
def compute_mos(predictions, gold, listeners=20):
    ratings = []
    for sample in predictions:
        # 20 native Chinese speakers rate quality 1-5
        r = get_listener_ratings(sample, listeners)
        ratings.append(mean(r))
    return mean(ratings), confidence_interval(ratings, 0.95)
```

## Common pitfalls

- MOS is highly dependent on listener demographics and language proficiency; this benchmark uses only native Chinese speakers, limiting cross-lingual generalization claims.
- RTF and GFLOPS are measured on a specific Intel Xeon CPU E5-2630v3 without hardware optimization, making direct efficiency comparisons with GPU-accelerated or optimized baselines invalid.
- TTS evaluation MOS includes errors from the acoustic model (Tacotron2), not just the vocoder, so it measures the full pipeline rather than the vocoder in isolation.

## Evidence (verbatim from paper)

> For evaluation, we adopt mean opinion score (MOS) tests to investigate the performance of the proposed methods. There are 20 native Chinese speakers evaluating the speech quality.

## Citation

```bibtex
@misc{yang2020multibandmelgan,
  title={Multi-band MelGAN: Faster Waveform Generation for High-Quality Text-to-Speech},
  author={Geng Yang et al. (2020)},
  year={2020},
  note={arXiv:2005.05106}
}
```

- arXiv: 2005.05106
