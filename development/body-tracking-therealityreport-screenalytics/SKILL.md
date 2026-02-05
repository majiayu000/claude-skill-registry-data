---
name: body-tracking
description: Person detection, tracking, and Re-ID. Use when faces aren't visible but cast should still be tracked, or when debugging face-body association.
---

# Body Tracking Skill

Use this skill to debug body tracking and face-body association issues.

## When to Use

- Screen time gaps when cast is on screen but face not visible
- Face-body association errors
- Re-ID matching issues after occlusion
- Debugging person detection coverage
- Track fusion problems

## Sub-agents

| Sub-agent | Purpose |
|-----------|---------|
| **PersonDetectorSubagent** | YOLO/DETR person detection |
| **PersonReIDSubagent** | OSNet/Torchreid embeddings |
| **TrackFusionSubagent** | Face-body association |

## Key Skills

### Run body tracking pipeline

Run the sandbox pipeline on an episode (writes artifacts under `data/manifests/{ep_id}/body_tracking/`).

```python
from pathlib import Path

from FEATURES.body_tracking.src.body_tracking_runner import BodyTrackingRunner

runner = BodyTrackingRunner(
    episode_id="my-episode",
    config_path=Path("config/pipeline/body_detection.yaml"),
    fusion_config_path=Path("config/pipeline/track_fusion.yaml"),
)
runner.run_full_pipeline()
```

### Fuse face ↔ body tracks

```python
from FEATURES.body_tracking.src.track_fusion import TrackFusion

fusion = TrackFusion()
identities = fusion.fuse_tracks(face_tracks=face_tracks, body_tracks=body_tracks)
```

### Compute body-only screentime deltas

```bash
python -m FEATURES.body_tracking --episode-id <EP_ID> --stage compare
```

## Config Reference

**File:** `config/pipeline/body_detection.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `body_tracking.enabled` | true | Enable body tracking |
| `person_detection.model` | `yolov8n` | Detector model |
| `person_detection.confidence_threshold` | 0.50 | Detection confidence |
| `person_tracking.track_buffer` | 120 | Frames to keep lost tracks |
| `person_reid.enabled` | true | Enable Re-ID embeddings |
| `person_reid.model` | `osnet_x1_0` | Re-ID model |

**File:** `config/pipeline/track_fusion.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `track_fusion.enabled` | true | Enable fusion stage |
| `iou_association.iou_threshold` | 0.50 | Face-in-body IoU threshold |
| `reid_handoff.similarity_threshold` | 0.70 | Re-ID match threshold |
| `reid_handoff.handoff.max_gap_seconds` | 30 | Max time for handoff |
| `reid_handoff.handoff.confidence_decay_rate` | 0.95 | Per-second decay |

## Common Issues

### Missing body detections

**Cause:** Person not detected by YOLO

**Check:** Detection confidence in logs

**Fix:** Lower confidence threshold:
```yaml
person_detection:
  confidence_threshold: 0.40  # default is 0.50
```

### Wrong face-body association

**Cause:** IoU too loose or multiple people close together

**Check:** `association_confidence` in track metadata

**Fix:** Increase IoU threshold:
```yaml
track_fusion:
  association_iou_thresh: 0.60  # default is 0.50
```

### Re-ID fails after occlusion

**Cause:** Clothing change or long gap

**Check:** `reid_similarity` between pre/post occlusion

**Fix:** Lower Re-ID threshold or increase gap tolerance:
```yaml
track_fusion:
  reid_similarity_thresh: 0.60  # default is 0.70
  handoff:
    max_gap_seconds: 45  # default is 30
```

### Body track ID switches

**Cause:** Tracker losing track through occlusion

**Check:** `body_id_switch_rate` in metrics

**Fix:** Increase track buffer:
```yaml
person_tracking:
  track_buffer: 150  # default is 120 (5 seconds)
```

## Diagnostic Output

```json
{
  "identity_id": "ID_001",
  "face_track_ids": [42, 256],
  "body_track_ids": [100127, 100345],
  "screen_time": {
    "face_visible_duration": 125.5,
    "body_only_duration": 45.2,
    "total_duration": 170.7
  },
  "associations": [
    {
      "face_track": 42,
      "body_track": 100127,
      "method": "iou",
      "confidence": 0.85
    },
    {
      "face_track": null,
      "body_track": 100127,
      "method": "reid_handoff",
      "confidence": 0.72
    }
  ]
}
```

## Key Files

| File | Purpose |
|------|---------|
| `FEATURES/body_tracking/src/detect_bodies.py` | YOLO person detection |
| `FEATURES/body_tracking/src/track_bodies.py` | Body tracking (ByteTrack + fallback) |
| `FEATURES/body_tracking/src/body_embeddings.py` | OSNet Re-ID embeddings |
| `FEATURES/body_tracking/src/track_fusion.py` | Face↔body fusion |
| `FEATURES/body_tracking/src/screentime_compare.py` | Screentime comparison |
| `config/pipeline/body_detection.yaml` | Detection config |
| `config/pipeline/track_fusion.yaml` | Fusion config |

## Related Skills

- [face-alignment](../face-alignment/SKILL.md) - Face alignment debugging
- [pipeline-insights](../pipeline-insights/SKILL.md) - General pipeline debugging
