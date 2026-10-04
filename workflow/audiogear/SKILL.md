---
name: audiogear
description: >-
  Annotate speech/TTS datasets with per-clip quality metrics (MOS, SNR, STOI,
  pitch, bandwidth, speaking rate, WER/CER, gender/emotion), multi-ASR consensus
  transcription and speaker labeling using the audiogear pipeline; then filter
  clips by quality and build listenable HTML QA reports. Use when asked to
  compute audio dataset metrics, build extended_metadata.csv, transcribe
  unlabeled audio, select clean TTS training data, or QA a speech dataset.
---

# audiogear — speech-dataset annotation pipeline

audiogear (https://github.com/lIkesimba9/audiogear) computes per-clip features
over a speech dataset: reader → metric blocks → CSV writer, configured with
Hydra, sharded across GPUs/nodes. This skill drives it from any project.

> Copy this file into the consuming project as
> `.claude/skills/audiogear/SKILL.md`. Set `AUDIOGEAR_HOME` below to wherever
> the audiogear checkout lives.

## Setup (once per machine)

```bash
export AUDIOGEAR_HOME=~/audiogear            # adjust; add to the project env
git clone https://github.com/lIkesimba9/audiogear.git "$AUDIOGEAR_HOME" || true
cd "$AUDIOGEAR_HOME"
uv sync --extra ru-pipeline                  # or à-la-carte: --extra mos --extra asr --extra pitch
sudo apt-get install -y espeak-ng            # needed only for SpeakingRateMetric
cp -n .env.example .env                      # put HF_TOKEN= in .env for gated models (pyannote)
```

Python 3.10–3.12. GigaAM pins torch <2.6 — do not "upgrade" torch inside this venv.

## Input contract

One directory per dataset with a `|`-delimited `metadata.csv`:

```
<data_root>/<dataset>/
  metadata.csv        # one row per clip
  audio/...           # referenced by audio_path, relative to the dataset dir
```

Required columns: `id` (unique), `audio_path`, `text` (may be empty).
All other columns pass through untouched; computed metric columns are appended.
If the source data has a different shape, first write a converter that produces
this layout (see `build_betterset`-style scripts) — do NOT teach audiogear the
foreign schema.

## Core workflow

### 1. Write a dataset config

Create `$AUDIOGEAR_HOME/configs/feat_<ds>.yaml`. Proven template (mirrors the
generated `feat_*` configs) with CPU∥GPU lanes so DSP metrics hide under GPU
time:

```yaml
defaults:
  - reader: ru          # CsvReader preset: delimiter "|", audio_key=audio_path, id_key=id
  - writer: csv
  - executor: local
  - _self_
hydra:
  job: {chdir: false}
  run: {dir: .}
  output_subdir: null
device: cuda
reader:
  data_folder: /path/to/data_root/<ds>
  glob_pattern: metadata.csv
  limit: -1             # set to 10 for a dry run
writer:
  output_folder: outputs/<ds>
  output_filename: ext_$rank.csv
  sep: "|"
executor:
  tasks: 8              # shards; rows are split round-robin
  workers: 2            # concurrent processes; each pins ONE GPU (rank % gpus)
  skip_completed: true
  logging_dir: logs/<ds>
metrics:
  - _target_: audiogear.pipeline.parallel.ParallelLanes
    lanes:
      cpu:
        - _target_: audiogear.pipeline.metrics.bandwidth.BandwidthMetric
        - _target_: audiogear.pipeline.metrics.wada_snr.SnrMetric
        - _target_: audiogear.pipeline.metrics.speaking_rate.SpeakingRateMetric
          language: ru
      gpu:
        - _target_: audiogear.pipeline.metrics.distillmos.DistillMosMetric
          device: ${device}
        - _target_: audiogear.pipeline.metrics.squim.SquimMetrics
          device: ${device}
        - _target_: audiogear.pipeline.metrics.pitch.CrepePitchMetric
          device: ${device}
          crepe_model: tiny
        - _target_: audiogear.pipeline.metrics.style.StyleMetric   # after pitch (reuses pitch_*)
        - _target_: audiogear.pipeline.metrics.gender.GenderMetric
          device: ${device}
```

Add `WhisperWer` to the gpu lane only when `text` is human-authored.

Lane rules (violating them corrupts data silently):
- lanes must write **disjoint** columns;
- a metric that consumes another's output (`StyleMetric` ← `pitch_mean`,
  `WhisperWer`/`SpeakingRateMetric` ← `text`) goes in the SAME lane, after its
  producer; a producer needed by both lanes (e.g. `ConsensusTranscriber`) runs
  as an ordinary step BEFORE the lanes block.

### 2. Dry run, then full run

```bash
cd "$AUDIOGEAR_HOME"
uv run python process.py --config-name feat_<ds> reader.limit=10   # smoke test, downloads models
uv run python process.py --config-name feat_<ds>                   # full run
```

Multi-GPU: `executor.workers=<n_gpus>`. `executor.gpus` is an **int** (count),
never a list. Never set `CUDA_VISIBLE_DEVICES` yourself — the executor pins it.
Multi-node: launch the same command once per node under SLURM, or set
`AUDIOGEAR_NODE_RANK`/`AUDIOGEAR_NUM_NODES`; put `executor.logging_dir` on
shared storage.

### 3. Merge shards → extended_metadata.csv

Each shard writes `outputs/<ds>/ext_<rank>.csv`. Merge with id-dedup (duplicates
appear if `executor.tasks` changed between an interrupted run and its rerun):

```bash
export AUDIOGEAR_DATA_DIR=/path/to/data_root
uv run python examples/run_batch.py <ds>     # run + merge + .FEAT_DONE marker per dataset
```

For many datasets, `examples/gen_configs.py` generates the per-dataset configs
and `examples/run_batch.py` sweeps them smallest-first with resume.

### 4. Filter + QA

```bash
uv run python examples/filter_clean.py <ds>   # extended_metadata.csv -> clean_metadata.csv + drop reasons
uv run python examples/qa_report.py <ds>      # -> <data_root>/<ds>/qa_report.html
```

`qa_report.html` is self-contained: metric histograms with the filter thresholds
drawn in, and playable audio just below/just above each threshold. To calibrate
thresholds: listen to both sides — rejected clips sounding fine ⇒ threshold too
strict; accepted clips sounding bad ⇒ too loose. Edit `TH` in
`examples/filter_clean.py` (single source of truth for filter and report) and
regenerate. Set `HUMAN_TEXT`/`ASR_TEXT` there: the CER filter is only valid
where `text` was written by humans, not by an ASR model.

## Metric catalogue

| Class (`audiogear.pipeline.metrics.*`) | Columns | Notes |
|---|---|---|
| `distillmos.DistillMosMetric` | `distillmos` | no-ref MOS, GPU |
| `squim.SquimMetrics` | `pyt_stoi`, `pyt_pesq`, `pyt_si_sdr` | GPU, never batched (padding skews scores) |
| `wada_snr.SnrMetric` | `wada_snr` | blind SNR, CPU |
| `bandwidth.BandwidthMetric` | `bandwidth_hz`, `is_upsampled_est` | detects upsampled audio; container sample_rate lies |
| `pitch.CrepePitchMetric` / `pitch.PitchMetric` | `pitch_mean`, `pitch_std` | GPU torchcrepe / CPU pyin |
| `style.StyleMetric` | `energy_db`, `energy_dynamics`, `expressiveness` | CPU; reuses `pitch_*` if present |
| `speaking_rate.SpeakingRateMetric` | `speaking_rate`, `phonemes_per_word`, `char_rate` | espeak-ng; NOT thread-safe — leave it serial |
| `wer.WhisperWer` | `whisper_wer`, `whisper_cer` | vs `text`; -1 when no reference. Skip for ASR-derived text (CER≈0, meaningless, expensive) |
| `gigaam_v3.GigaAMv3` | `gigaam3_text`, `gigaam3_cer`, `text_punctuated`, opt-in words JSON | punctuated-from-audio RU transcript + punctuation transferred onto reference words; `model_name: multilingual_ctc` for ru/en/kk/ky/uz (no punctuation — set `punct_column: null`); `words_column` adds word timestamps |
| `gender.GenderMetric` / `emotion.EmotionMetric` | `gender_pred` / `emotion_pred`, `emotion_score` | `_pred` suffix — never overwrite curated columns |
| `hf.HFAudioModelMetric` | configurable | any 🤗 audio classification/regression model, config-only |
| `brouhaha_snr_reverb.SnrReverbMetrics` | `snr`, `c50` | pyannote, gated (HF_TOKEN) |
| `speaker.SpeakerLabeler` | `speaker`, `speaker_conf`, `speaker_margin` | dataset-level clustering — run with `executor.tasks=1` |
| `transcribers.consensus.ConsensusTranscriber` | `text`, `asr_text_*`, `asr_agreement` | multi-ASR medoid; for datasets without transcripts |

## Reliability semantics (what to expect downstream)

- **Sentinels, not crashes.** A corrupt/unscorable clip never kills a run: the
  per-clip guard writes NaN (or `-1` for WER/CER/SQUIM) and continues. Always
  treat NaN and negative metric values as "no value" when filtering. A long
  unbroken failure streak (default 50) aborts the shard — that means a
  systematic problem (model/config), not bad data.
- **Resume is two-level.** Completed shards are skipped via markers in
  `logging_dir`; *inside* an unfinished shard, per-metric JSONL checkpoints in
  `<output_folder>/checkpoints/` resume from the last computed clip. Rerunning
  the same command after any crash is always safe. Checkpoints are keyed by clip
  id only — after changing a metric's model/parameters, delete
  `<output_folder>/checkpoints/` (or the run reuses stale values). Disable with
  `resume: false` in the config.

## Pitfalls checklist

- `executor.gpus: 1` (int) — `gpus: [0]` breaks.
- Whisper `compute_type: int8_float16` when 2 workers share a GPU (halves VRAM).
- Clips >25 s are truncated by GigaAMv3; SQUIM needs ≥1024 samples (else -1).
- Audio must be locally readable (torchaudio); CSVs/outputs/logs may be
  `s3://…` (fsspec), audio may not — FUSE-mount buckets instead.
- Models load lazily per worker process — first clips are slow, that's normal.
- Adding a metric: subclass `BaseMetric`, implement `compute_metric(segment)`,
  set `metric=` to the column name(s). Do NOT add try/except around it — the
  base class guards every path already. Load models lazily via
  `audiogear.utils.runtime.cached_model`.

## Programmatic use (no CLI)

```python
from omegaconf import OmegaConf
from audiogear.build import build_pipeline

cfg = OmegaConf.create({...})       # same shape as a yaml config
data = None
for step in build_pipeline(cfg):    # reader -> metrics -> writer
    data = step(data, 0, 1)         # (data, rank, world_size)
# data: list[AudioSegment]; computed values in segment.metadata
```
