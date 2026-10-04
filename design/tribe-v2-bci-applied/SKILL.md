---
name: tribe-v2-bci-applied
category: neuroscience
description: >
  Applied BCI research and neuro-informed content optimization using Meta's TRIBE v2 brain encoder.
  Predicts neural responses to media, UI, and content without brain scanners — enabling stimulus
  optimization, attention ranking, and BCI groundwork research.
  Use when: (1) Predicting neural responses to video, audio, or text content, (2) Ranking content
  by predicted brain engagement (visual cortex, attention, emotion), (3) Optimizing stimuli to
  maximize activation in a target cortical region, (4) BCI research using non-invasive population
  priors, (5) Accessibility research (testing presentation formats for language/auditory processing),
  (6) Computational neuromarketing research (CC BY-NC, non-commercial only), (7) Any task involving
  brain response prediction for media, UI design, or BCI applications using TRIBE v2.
license: CC BY-NC 4.0
---

# TRIBE v2 Applied BCI Skill

Agentic skill for applied BCI research and neuro-informed content optimization — from predicting fMRI cortical responses to media without brain scanners, through stimulus optimization and attention ranking, to generating cortical priors for non-invasive BCI decoding research.

> **License constraint**: TRIBE v2 is CC BY-NC 4.0. This skill is for non-commercial research only. Commercial neuromarketing, advertising optimization, or audience profiling for profit requires a separate license from Meta. Read [references/ethics-privacy.md](references/ethics-privacy.md) before any applied use.

---

## Quick Start

### 1. Install TRIBE v2

```bash
# Python 3.11+ required
git clone https://github.com/facebookresearch/tribev2
cd tribev2
pip install -e .
```

### 2. Load Model and Run First Prediction

```python
from tribev2 import TribeModel

# Load model — downloads weights on first run (~several GB)
model = TribeModel.from_pretrained("facebook/tribev2", cache_folder="./cache")

# Build events dataframe from your stimulus
df = model.get_events_dataframe(video_path="path/to/video.mp4")

# Predict cortical responses
preds, segments = model.predict(events=df)

# preds.shape = (n_timesteps, n_vertices)
# n_vertices ~20,000 on fsaverage5 surface mesh
print(f"Predicted response shape: {preds.shape}")
print(f"Mean activation across all cortex: {preds.mean():.4f}")
```

### 3. Supported Input Modalities

```python
# Video (extracts visual + auditory + motion features)
df = model.get_events_dataframe(video_path="clip.mp4")

# Text only (activates language network)
df = model.get_events_dataframe(text_path="script.txt")

# Audio only (activates auditory + language regions)
df = model.get_events_dataframe(audio_path="voiceover.wav")
```

### 4. Extract Region Activation

```python
import numpy as np

# Visual cortex — approximate fsaverage5 vertex range
visual_vertices = list(range(1000, 7000))
visual_activation = preds[:, visual_vertices].mean()
print(f"Visual cortex mean activation: {visual_activation:.4f}")
```

---

## Workflow A: Content Engagement Ranking

**Trigger**: You have N media files (videos, audio clips, or text variants) and want to rank them by predicted neural engagement — which one will drive more visual attention, emotional resonance, or language processing.

**When to use**: A/B testing ad creative before production, ranking tutorial formats, comparing voiceover styles, testing UI motion animations.

**Tool**: `scripts/content_tester.py`

```
Input: folder of files (all same modality), target regions

1. Load TRIBE v2 once
   → Single model load amortized across all files

2. For each file:
   → model.get_events_dataframe(...)
   → model.predict(events=df)
   → Compute mean activation per requested region
   → Record per-file scores

3. Compute overall_engagement_score = mean(all region scores)

4. Rank files descending by overall_engagement_score

Output: CSV with per-region scores + overall rank, top-3 printed to console
```

**Run it:**

```bash
python scripts/content_tester.py \
  --input-dir ./ad_variants/ \
  --modality video \
  --regions visual,auditory,language \
  --output engagement_rankings.csv
```

**Interpreting results:**

| Score range | Interpretation |
|-------------|----------------|
| > 0.6 | High predicted engagement — stimulus strongly activates target networks |
| 0.3 – 0.6 | Moderate engagement — typical for well-produced content |
| < 0.3 | Low engagement — consider redesigning stimulus elements |

**Design considerations:**
- Scores are relative within your batch, not absolute fMRI values
- Compare within modality for best results (don't rank videos vs audio directly)
- High visual + low language = visually engaging but not verbally memorable
- High language + low visual = good for information retention tasks

---

## Workflow B: Stimulus Optimization

**Trigger**: You have a base stimulus and want to find variants that maximize predicted activation in a specific cortical region — e.g., maximize visual cortex response for a display ad, or maximize language network response for a tutorial narration.

**When to use**: Iterative content refinement, creative optimization loops, accessibility improvements (maximize auditory processing for hearing-impaired content), BCI stimulus design.

**Tool**: `scripts/optimize_stimulus.py`

```
Input: base stimulus file, target region, modality, number of variants

1. Predict baseline activation on original file
   → Establish baseline score for target region

2. Generate N perturbation variants
   Video: brightness (0.7x–1.4x), contrast (0.8x–1.3x), saturation, playback speed
   Audio: speed (0.85x–1.15x), pitch shift, volume normalization variants
   Text: model prints paraphrase suggestions for human review (cannot auto-perturb text)

3. Predict activation on each variant
   → model.predict(events=variant_df)
   → Score target_region_vertices.mean()

4. Rank variants by target region mean activation
   → Output CSV: variant_file, target_region_mean, rank
   → Print top variant's delta vs baseline

Output: Ranked CSV, best variant path, improvement percentage
```

**Run it:**

```bash
python scripts/optimize_stimulus.py \
  --input ./base_ad.mp4 \
  --target-region visual \
  --modality video \
  --n-variants 10 \
  --output-dir ./optimized/
```

**Target region options:**

| Region flag | Cortical target | Applied goal |
|-------------|-----------------|--------------|
| `visual` | V1–V4, MT (vertices 1000–7000) | Visual attention, saliency |
| `auditory` | A1 + belt + STS (vertices 8000–13000) | Voice quality, audio engagement |
| `language` | Broca's + Wernicke's (vertices 15000–18500, LH) | Comprehension, verbally memorable |
| `motion` | MT/V5 (vertices 5500–7000) | Motion perception, dynamic content |
| `default_mode` | mPFC/PCC/AG (vertices 19000–20000) | Mind-wandering, narrative immersion |

**Greedy optimization loop** (advanced — run in a shell loop):

```bash
BEST="base_ad.mp4"
for ITER in 1 2 3 4 5; do
  python scripts/optimize_stimulus.py \
    --input "$BEST" \
    --target-region visual \
    --modality video \
    --n-variants 8 \
    --output-dir ./iter_${ITER}/
  BEST=$(python -c "
import csv
with open('iter_${ITER}/rankings.csv') as f:
    rows = list(csv.DictReader(f))
print(rows[0]['variant_file'])
")
  echo "Iter $ITER best: $BEST"
done
```

---

## Workflow C: Attention Proxy Analysis

**Trigger**: You want to quantify predicted attentional engagement — not just one region, but a composite proxy combining visual and social/multisensory processing.

**Rationale**: True attentional engagement in fMRI correlates with simultaneous activation of:
- Early visual cortex (V1–V4): processing visual input at all
- MT/V5: tracking motion — moving stimuli attract attention
- STS (superior temporal sulcus): social signals, face motion, voice prosody

High combined score = stimulus is predicted to capture and hold attention.

```python
import numpy as np
from tribev2 import TribeModel

model = TribeModel.from_pretrained("facebook/tribev2", cache_folder="./cache")

def attention_proxy(model, file_path, modality="video"):
    """Compute attention proxy score from TRIBE v2 predictions."""
    if modality == "video":
        df = model.get_events_dataframe(video_path=file_path)
    elif modality == "audio":
        df = model.get_events_dataframe(audio_path=file_path)
    else:
        df = model.get_events_dataframe(text_path=file_path)

    preds, segments = model.predict(events=df)

    # Component regions
    early_visual = preds[:, 1000:5500].mean(axis=1)   # V1–V4
    motion_region = preds[:, 5500:7000].mean(axis=1)   # MT/V5
    sts_region = preds[:, 11500:13000].mean(axis=1)    # STS

    # Attention proxy: weighted combination
    attention_ts = 0.4 * early_visual + 0.3 * motion_region + 0.3 * sts_region

    return {
        "attention_proxy_mean": float(attention_ts.mean()),
        "attention_proxy_peak": float(attention_ts.max()),
        "attention_proxy_std": float(attention_ts.std()),
        "peak_timestep": int(attention_ts.argmax()),
        "early_visual_mean": float(early_visual.mean()),
        "motion_mean": float(motion_region.mean()),
        "sts_mean": float(sts_region.mean()),
    }

# Usage
result = attention_proxy(model, "campaign_video.mp4", modality="video")
print(f"Attention proxy: {result['attention_proxy_mean']:.4f}")
print(f"Peak engagement at timestep: {result['peak_timestep']}")
```

**Interpreting the attention proxy timeseries:**

```python
import matplotlib.pyplot as plt

# Visualize attention dynamics over time
preds, segments = model.predict(events=df)
early_v = preds[:, 1000:5500].mean(axis=1)
motion = preds[:, 5500:7000].mean(axis=1)
sts = preds[:, 11500:13000].mean(axis=1)
proxy = 0.4 * early_v + 0.3 * motion + 0.3 * sts

plt.figure(figsize=(12, 4))
plt.plot(proxy, label="Attention proxy", linewidth=2)
plt.plot(early_v, alpha=0.5, label="Visual (V1-V4)")
plt.plot(motion, alpha=0.5, label="Motion (MT)")
plt.plot(sts, alpha=0.5, label="STS (social)")
plt.xlabel("Timestep")
plt.ylabel("Predicted activation")
plt.title("Attention proxy across stimulus duration")
plt.legend()
plt.tight_layout()
plt.savefig("attention_dynamics.png", dpi=150)
```

**Use this to:**
- Find the moment in a video where attention is predicted to drop (cut or restructure that segment)
- Compare opening hooks: which 10-second intro scores highest on attention proxy?
- Identify which audio/visual elements drive the peaks

---

## Workflow D: BCI Prior Generation

**Trigger**: You are working on a non-invasive BCI (EEG, fMEG, or fNIRS) decoding project and need population-average cortical activation priors — e.g., to localize imagined speech, visual imagery, or auditory perception without running a full fMRI study.

**Rationale**: TRIBE v2 was trained on large-scale fMRI data. Its predictions represent population-average expected activations for a stimulus class. These priors can seed:
- Spatial filters for EEG source localization (beamforming, eLORETA)
- Region-of-interest masks for constrained decoding
- Expected activation patterns for cross-modal transfer learning

```python
import numpy as np
from tribev2 import TribeModel

model = TribeModel.from_pretrained("facebook/tribev2", cache_folder="./cache")

def generate_cortical_prior(model, stimulus_class_files: list, modality: str = "audio") -> np.ndarray:
    """
    Generate a population-average cortical activation prior for a stimulus class.
    
    Args:
        stimulus_class_files: list of file paths for stimuli in this class
        modality: 'video', 'audio', or 'text'
    
    Returns:
        prior: (n_vertices,) mean activation map across stimuli and time
    """
    all_preds = []

    for fpath in stimulus_class_files:
        if modality == "audio":
            df = model.get_events_dataframe(audio_path=fpath)
        elif modality == "video":
            df = model.get_events_dataframe(video_path=fpath)
        else:
            df = model.get_events_dataframe(text_path=fpath)

        preds, _ = model.predict(events=df)
        # Average over time for this stimulus
        all_preds.append(preds.mean(axis=0))

    # Average over stimulus class
    prior = np.stack(all_preds).mean(axis=0)
    return prior


def save_prior_as_nifti_compatible(prior: np.ndarray, output_path: str):
    """
    Save prior as numpy array for downstream BCI toolchain use.
    Compatible with MNE-Python, nibabel, and FSL workflows.
    """
    np.save(output_path, prior)
    print(f"Saved prior shape {prior.shape} to {output_path}")
    print("Load with: import numpy as np; prior = np.load('prior.npy')")


# Example: generate speech vs. non-speech priors for EEG decoding
speech_files = ["speech_1.wav", "speech_2.wav", "speech_3.wav"]
non_speech_files = ["music_1.wav", "noise_1.wav", "tone_1.wav"]

speech_prior = generate_cortical_prior(model, speech_files, modality="audio")
non_speech_prior = generate_cortical_prior(model, non_speech_files, modality="audio")

# Differential contrast prior (speech - non-speech)
contrast_prior = speech_prior - non_speech_prior
save_prior_as_nifti_compatible(contrast_prior, "speech_contrast_prior.npy")

# Identify top vertices (most discriminative regions)
top_vertices = np.argsort(np.abs(contrast_prior))[-500:]
print(f"Top 500 discriminative vertices: {top_vertices}")
print(f"Language network (Broca's ~15000-17000): {sum(15000 <= v <= 17000 for v in top_vertices)} vertices in range")
```

**Integrating with MNE-Python (EEG source modeling):**

```python
import mne
import numpy as np

# Load your TRIBE v2 prior
prior = np.load("speech_contrast_prior.npy")  # shape: (n_vertices_fsaverage5,)

# Use as initial weights for minimum norm estimate (MNE)
# Prior needs to be projected to source space matching your EEG setup
# See MNE docs: mne.minimum_norm.make_inverse_operator with depth weighting

# The prior defines which regions you expect to be active —
# feeds into beamformer spatial filter initialization or
# constrains the solution space for sparse inverse methods
```

**Important disclosures for BCI use**: TRIBE v2 priors are population-average predictions. Individual subject brains differ in activation patterns. When using these priors in real BCI pipelines, disclose this assumption to end users. Do not present population-average predictions as personalized neural decoding. See [references/ethics-privacy.md](references/ethics-privacy.md) for full BCI-specific risk disclosure.

---

## Ethical Guardrails

This skill operates under CC BY-NC 4.0 restrictions and ethical norms for brain simulation research.

**This skill MUST NOT be used for:**
- Commercial advertising optimization or neuromarketing for profit
- Building psychological profiles for commercial audience targeting
- Generating "neural dark patterns" — stimuli designed to bypass conscious decision-making
- Any profiling of individuals without explicit informed consent
- Any use involving minors without a guardian consent framework
- Surveillance or monitoring applications

**This skill MAY be used for:**
- Academic research and publication (non-commercial)
- Accessibility improvement research
- Clinical hypothesis generation (not diagnosis)
- UX research with full participant disclosure
- Non-invasive BCI research with appropriate consent frameworks

Before any applied use, read the full ethics and licensing reference: [references/ethics-privacy.md](references/ethics-privacy.md)

For commercial licensing, contact Meta Research: https://research.facebook.com

---

## Tool Reference

### TRIBE v2 API

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `TribeModel.from_pretrained(model_id)` | HuggingFace model ID | `TribeModel` instance | Downloads ~GB of weights on first call |
| `model.get_events_dataframe(video_path=)` | Video file path | `pd.DataFrame` | Extracts visual, auditory, motion features |
| `model.get_events_dataframe(audio_path=)` | Audio file path | `pd.DataFrame` | Extracts auditory + language features |
| `model.get_events_dataframe(text_path=)` | Text file path | `pd.DataFrame` | Extracts language + semantic features |
| `model.predict(events=df)` | Events DataFrame | `(preds, segments)` | `preds.shape = (timesteps, vertices)` |

### Key Output Properties

| Property | Value | Description |
|----------|-------|-------------|
| `preds.shape[0]` | Varies with stimulus duration | Number of predicted timepoints |
| `preds.shape[1]` | ~20,000 | Vertices on fsaverage5 surface mesh |
| `preds.mean()` | Float | Overall cortical activation mean |
| `preds[:, v_start:v_end].mean()` | Float | Region mean activation |

### Supported Formats

| Modality | Formats | Notes |
|----------|---------|-------|
| Video | `.mp4`, `.avi`, `.mov` | Extracts visual + audio features jointly |
| Audio | `.wav`, `.mp3`, `.flac` | Pure auditory feature extraction |
| Text | `.txt` | Language model feature extraction |

---

## Cortical Region Reference

For full region atlas with vertex ranges, activation profiles, and applied BCI use cases, see [references/cortical-region-atlas.md](references/cortical-region-atlas.md).

Quick vertex range cheatsheet:

| Region | Vertices (approx) | Key activators |
|--------|-------------------|----------------|
| V1/V2 (primary visual) | 1000–4000 | Edges, contrast, spatial frequency |
| V4 (color/form) | 4000–5500 | Color, shape, object form |
| MT/V5 (motion) | 5500–7000 | Optical flow, motion direction |
| IPS/FEF (attention) | 7000–8500 | Top-down attention, gaze control |
| A1 (primary auditory) | 8000–10000 | Tone, pitch, onset |
| Belt regions (auditory) | 10000–11500 | Voice, timbre, melody |
| STS (social/voice) | 11500–13000 | Speaker identity, prosody, face motion |
| FFA (faces) | 12000–14000 | Face identity, expression |
| PPA (places/scenes) | 14000–16000 | Spatial layout, architecture |
| Broca's area (LH) | 15000–17000 | Syntax, speech production |
| Wernicke's area (LH) | 17000–18500 | Speech comprehension |
| VWFA (reading) | 18500–19500 | Visual words, orthography |
| vmPFC (reward/value) | 18000–19000 | Emotional valence, reward expectation |
| mPFC/PCC/AG (DMN) | 19000–20000 | Narrative, self-referential, mind-wandering |

---

## References

- **[references/cortical-region-atlas.md](references/cortical-region-atlas.md)** — Full applied cortical atlas: region properties, vertex ranges, activation profiles, and BCI/neuromarketing use cases
- **[references/ethics-privacy.md](references/ethics-privacy.md)** — CC BY-NC license constraints, consent frameworks, prohibited uses, and BCI-specific risk disclosures
- **TRIBE v2 paper**: Benchetrit et al. (2025) — "Brain-wide visual responses to natural stimuli" — Meta AI Research
- **TRIBE v2 demo**: https://aidemos.atmeta.com/tribev2
- **TRIBE v2 repo**: https://github.com/facebookresearch/tribev2
- **fsaverage5 surface**: FreeSurfer fsaverage5 — 20,484 vertices per hemisphere; TRIBE v2 uses this as its prediction target
