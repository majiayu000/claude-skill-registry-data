---
name: face-alignment
description: Face alignment, landmark extraction, and quality gating. Use when debugging alignment issues, reviewing rejected faces, or tuning quality thresholds.
---

# Face Alignment Skill

Use this skill to debug face alignment artifacts and embedding gating behavior.

## When to Use

- Faces being rejected but you don't know why
- Identity fragmentation that might be alignment-related
- Need to adjust alignment quality thresholds
- Debugging how `alignment_quality` is computed and consumed
- Planning promotion/integration (FEATURE sandbox → production)

## Sub-agents

| Sub-agent | Purpose |
|-----------|---------|
| **FaceAlign2DSubagent** | FAN 68-point 2D landmark extraction |
| **FaceAlign3DSubagent** | 3DDFA_V2 dense 3D alignment (planned) |
| **AlignmentQualitySubagent** | LUVLi-style uncertainty scoring (planned; heuristic today) |

## Key Skills

### Run FAN alignment on a face bbox

Run alignment on detected face boxes (produces 68-point landmarks; optional aligned crop).

```python
from FEATURES.face_alignment.src.run_fan_alignment import FANAligner, align_face_crop

aligner = FANAligner(model_type="2d", landmarks_type="2D", device="cpu")
landmarks = aligner.align_face(image, bbox)  # 68 x 2
aligned_crop = align_face_crop(image, landmarks, output_size=112)
```

### Compute `alignment_quality` (heuristic today)

Get a per-face quality score (0–1). Current implementation is heuristic-based.

```python
from FEATURES.face_alignment.src.alignment_quality import compute_alignment_quality

quality = compute_alignment_quality(bbox=bbox, landmarks_68=landmarks)
```

### Generate episode artifacts

```bash
python -m FEATURES.face_alignment --episode-id <EP_ID>
```

## Config Reference

**Alignment Artifact Config:** `config/pipeline/face_alignment.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `face_alignment.enabled` | true | Produce `face_alignment/aligned_faces.jsonl` |
| `face_alignment.model.type` | `2d` | FAN model variant (`2d` / `3d`) |
| `face_alignment.processing.stride` | 1 | Sample every Nth frame |
| `face_alignment.processing.batch_size` | 16 | Faces per batch |
| `face_alignment.processing.device` | `auto` | `auto` / `cuda` / `cpu` |

**Embedding Gating Config:** `config/pipeline/embedding.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `face_alignment.enabled` | true | Enable/disable gating logic |
| `face_alignment.min_alignment_quality` | 0.3 | Skip faces below this threshold |

## Common Issues

### Faces unexpectedly skipped before embedding

**Cause:** Face below quality threshold

**Check:** `alignment_quality` in `data/manifests/{ep_id}/face_alignment/aligned_faces.jsonl`

**Fix:** Lower threshold in `config/pipeline/embedding.yaml`:
```yaml
face_alignment:
  min_alignment_quality: 0.2  # default is 0.3
```

### High `landmark_jitter`

**Cause:** Unstable landmarks across frames

**Check:** Per-frame landmark variance in track

**Fix:**
- Ensure FAN model loaded correctly
- Check input face crop quality
- May need temporal smoothing

### 3D head pose / profile gating isn’t available

**Cause:** 3DDFA_V2 isn’t implemented yet (planned).

## Diagnostic Output

```json
{
  "face_id": "F_42_100",
  "alignment_quality": 0.72,
  "landmarks_detected": 68,
  "head_pose": {
    "yaw": -25.5,
    "pitch": 10.2,
    "roll": 3.1
  },
  "quality_breakdown": {
    "eyes": 0.85,
    "nose": 0.80,
    "mouth": 0.65,
    "chin": 0.55
  },
  "aligner_used": "fan_2d"
}
```

## Key Files

| File | Purpose |
|------|---------|
| `FEATURES/face_alignment/src/run_fan_alignment.py` | FAN landmarks + crop utilities |
| `FEATURES/face_alignment/src/face_alignment_runner.py` | Episode runner (`python -m FEATURES.face_alignment`) |
| `FEATURES/face_alignment/src/alignment_quality.py` | Heuristic `alignment_quality` |
| `FEATURES/face_alignment/src/run_luvli_quality.py` | LUVLi-style scaffolding (not true LUVLi yet) |
| `config/pipeline/face_alignment.yaml` | Alignment artifact config |
| `config/pipeline/embedding.yaml` | Embedding gating config |
| `FEATURES/face_alignment/tests/test_face_alignment.py` | Unit tests (synthetic) |
| `tests/integration/test_face_alignment_pipeline.py` | Pipeline integration helpers/tests |

## Related Skills

- [pipeline-insights](../pipeline-insights/SKILL.md) - General pipeline debugging
- [cluster-quality](../cluster-quality/SKILL.md) - Clustering metrics
