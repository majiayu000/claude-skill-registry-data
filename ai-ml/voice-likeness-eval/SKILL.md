---
name: voice-likeness-eval
description: Measure how much a cloned voice sounds like the real character, and whether a change really helped. Covers speaker-embedding similarity (ECAPA) against the centroid of held-out real clips, word error rate with Whisper, comparing per line with paired t-tests, how many runs it takes to beat sampling noise, checking a take-picker with an independent speaker model, and simulating picking strategies on many scored takes. Use when comparing voice engines or settings (Fish Audio Drama 3 vs S2 Pro vs ElevenLabs, sampling, reference clips, best-of-N, fine-tuning), or before telling anyone that one voice setup is better than another.
---

# Is the voice actually better?

Ears are good at "that's wrong" and bad at "that's 3% better". This repo's numbers all come from one scorer
(`server/finetune/train.py`, class `Scorer`), run on a GPU in Modal:

- **Voice match:** cosine similarity of the ECAPA speaker embedding (speechbrain `spkrec-ecapa-voxceleb`) of the
  generated line to the **centroid of 60 real clips** of the character that were never used as references. Real
  clips of the same character score ~0.8 against it; 0.6-0.8 is the range where engines differ.
- **Word error:** Whisper large-v3 transcribes the line; WER against the text, with `[tags]` and punctuation
  removed. Slang ("busta" → "buster", "Ballas" → "ball is") puts a floor of ~5-8% under every engine, so compare
  WER between engines, not to zero.
- **Ten test lines** in the character's style with a spread of moods (`TEST_LINES` in `train.py`).

```bash
modal run server/finetune/train.py::score_extra --model drama3best8a,drama3best8b   # <model>_<line>.wav files
modal run server/finetune/train.py::pick_study_run --models run1,run2,...           # every take, both models
```
`score_extra` adds `<model>_<line>.wav` files from `data/finetune/<speaker>/` to `scores.json` and rebuilds
`compare.html` (every line from every engine, playable, with what Whisper heard).

## Rules that kept us honest
1. **Compare per line.** Average each engine over its runs per line, then a paired t-test over the 10 lines
   (|t| > 2.26 is p < 0.05 with 9 degrees of freedom). Report "better on 8 of 10 lines" next to the mean.
2. **Run it more than twice.** Identical settings, two runs: 0.715 and 0.645. One lucky run made a sampling
   change look like +0.08 when it was +0.017. With 10 runs of single takes, the baseline settled at 0.660.
3. **Report every run** (`0.704 (runs 0.702 / 0.706)`), and say when a difference isn't significant. A tie is
   a result.
4. **Correct yourself in the same place you claimed it.** If a later run undoes a claim, say so where the
   claim was made.
5. **Don't let the picker grade itself.** If a setting picks takes by a speaker model, check the picks with a
   different one too. Here: picks by ECAPA raised ECAPA a lot and WavLM a little; picks by WavLM raised WavLM a
   lot and ECAPA less; both together kept most of each. If only the picker's own metric moves, it's gaming the
   metric, not cloning better.

## Simulate before you deploy
Rendering N takes per line and scoring every take lets you test picking rules offline. 100 takes (10 per line)
gave, at 8 takes per line: one take 0.660; WavLM pick 0.706; ECAPA pick 0.723; both 0.721 with the lowest word
error (7.4%); the true best of 8 by real-clip ECAPA 0.732 (the ceiling). The deployed rule measured 0.704 directly
(2 runs), close to its simulation.

## What was measured (Lamar, 10 lines)
| Setup | Voice match | Word error |
|---|---|---|
| ElevenLabs instant clone | 0.612 | 10.5% |
| Fish Audio Drama 3, defaults (2 runs) | 0.643 | 7.1% |
| Drama 3, temperature 0.7 / top_p 0.8, one take (10 runs) | 0.660 | 7.9% |
| S2 Pro, same reference clip | 0.680 | 6.1% |
| **Drama 3, best of 8, checked, ECAPA + WavLM pick (2 runs)** | **0.704** | 8.6% |
| S2 Pro, its best single clip | 0.707 | 5.6% |
| S2 Pro fine-tuned (LoRA, step 250; needs training) | 0.785 | 7.5% |

Without training, Drama 3 with best of 8 ties S2 Pro's best zero-shot result; only the fine-tune is clearly
higher. Likeness isn't everything: Drama 3 acts `[crying]` and `[laughing]` better, and that's a listening
test, not a number.
