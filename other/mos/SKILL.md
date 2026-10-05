---
name: mos
description: Evaluates the naturalness, speaker similarity, and real-time synthesis speed of a Mandarin speech cloning system across diverse practical application scenarios. Use when the user has predictions and gold and needs to compute MOS (naturalness & similarity).
metadata:
  skill_kind: metric
  source_arxiv: 2203.02967
  bibtex_key: xing2022vaemandarin
  confidence: high
---

# mos

> Variational Auto-Encoder based Mandarin Speech Cloning — Xing Qingyu et al. (2022) (arXiv:2203.02967, 2022)

## What this evaluates

Evaluates the naturalness, speaker similarity, and real-time synthesis speed of a Mandarin speech cloning system across diverse practical application scenarios.

## Datasets

- **aidatatang_200zh, magicdata, aishell1, aishell3, and private dataset** — total 1200; splits: train (-1), test (20); repo https://github.com/keonlee9420/VAENAR-TTS

## Metrics

- `MOS (naturalness & similarity)` **(primary)** — range: [1, 5]
  - Subjective score on a 5-point scale averaged across 16 native listeners, assessing both naturalness and speaker similarity.
- `RTF` — range: ratio
  - Real-Time Factor: the ratio of synthesis time to generated audio duration, averaged over 10 runs on a single batch.
- `A/B Preference` — range: percent
  - Percentage of listeners who prefer the synthesized speech of one model over another in a forced-choice test.

## Input / output format

**Input**: 20 unseen Mandarin sentences spanning 9 practical scenarios, paired with reference audio for voice cloning.

**Output**: Synthesized audio files (16kHz, 16-bit WAV) for each sentence.

## Scoring recipe

```python
# MOS: Average listener rating (1-5) for naturalness & similarity
mos = sum(listener_scores) / len(listener_scores)
# RTF: Synthesis time per second of audio
rtf = total_synthesis_time / (num_samples * 1.0)
# A/B Preference: Win rate against baseline
preference_pct = (count_preferred / total_votes) * 100
```

## Common pitfalls

- MOS evaluation uses only 16 listeners, which is below standard ITU-T recommendations (typically 20-40+) and may yield high variance.
- RTF is benchmarked on a specific legacy GPU (NVIDIA Titan Xp) with batch size 1, making direct comparisons to modern hardware or batched inference invalid.
- The private dataset used for training is not publicly released, preventing full reproducibility of the cloning quality claims.

## Evidence (verbatim from paper)

> The synthetic speech's naturalness and similarity were assessed using the MOS test and the A/B test. The test included 16 native listeners, and the speech samples were shuffled in each test. The real-time factor (RTF), which is the time it takes to synthesize one second of speech spectrogram from text, is used to determine synthesis speed. The RTF benchmarks are run on a single NVIDIA GeForce Titan Xp GPU with a single batch size which averaged over 10 times runs on the entire test set for each model.

## Citation

```bibtex
@misc{xing2022vaemandarin,
  title={Variational Auto-Encoder based Mandarin Speech Cloning},
  author={Xing Qingyu et al. (2022)},
  year={2022},
  note={arXiv:2203.02967}
}
```

- arXiv: 2203.02967
