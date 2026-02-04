---
name: vision-analytics
description: Advanced visibility analysis using head pose, face mesh, and temporal patterns. Use for face-visible vs body-only breakdowns.
---

# Vision Analytics Skill

Use this skill for planned advanced visibility metrics and analytics (mesh/visibility/gaze). As of 2025-12-13 this is docs/config scaffolding only.

## When to Use

- Need detailed visibility breakdown (not just visible/not visible)
- Analyzing gaze patterns in an episode
- Debugging visibility fraction calculations
- Understanding regional face occlusion
- Screen time breakdown by visibility type

## Sub-agents

| Sub-agent | Purpose |
|-----------|---------|
| **VisibilityEstimatorSubagent** | LUVLi + 3DDFA + Mesh visibility signals |

## Key Skills

### `compute_visibility_labels()` (planned)
Compute per-frame visibility metrics (not implemented yet).

```python
# Planned module: FEATURES/vision_analytics/src/visibility.py
# from FEATURES.vision_analytics.src.visibility import compute_visibility

# Planned API:
# result = compute_visibility(mesh=face_mesh_result, face_bbox=bbox, frame_shape=(1080, 1920))
```

### `generate_screen_time_breakdown()` (planned)
Generate face vs body timeline for an identity (not implemented yet).

```python
# Planned module: FEATURES/vision_analytics/src/timeline.py
# from FEATURES.vision_analytics.src.timeline import generate_screen_time_breakdown

# Planned API:
# breakdown = generate_screen_time_breakdown(identity=identity, face_segments=face_timeline, body_segments=body_timeline)
```

## Config Reference

**File:** `config/pipeline/analytics.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `face_mesh.enabled` | true | Enable mesh extraction (planned; no runnable implementation yet) |
| `face_mesh.execution.closeup_threshold` | 0.05 | Face area / frame area |
| `face_mesh.execution.sample_rate` | 30 | Every Nth frame |
| `gaze.enabled` | true | Enable gaze estimation |
| `gaze.use_iris` | true | Use refined iris landmarks |
| `gaze.thresholds.center_threshold` | 15 | Degrees from center |

## Visibility Fraction

Visibility fraction indicates how much of the face is visible:

| Fraction | Interpretation |
|----------|----------------|
| 0.90-1.00 | Full frontal view |
| 0.70-0.90 | Minor occlusion or slight profile |
| 0.50-0.70 | Profile or significant occlusion |
| 0.30-0.50 | Near-profile or major occlusion |
| <0.30 | Mostly occluded |

## Regional Breakdown

Face regions tracked:

| Region | Landmarks | Importance |
|--------|-----------|------------|
| Left eye | 33, 133, 160... | High (identity) |
| Right eye | 362, 263, 387... | High (identity) |
| Nose | 1, 2, 98... | Medium |
| Mouth | 13, 14, 78... | Medium |
| Forehead | 10, 67, 109... | Low |
| Chin | 152, 377, 400... | Low |

## Gaze Direction

Coarse gaze categories:

| Horizontal | Degrees |
|------------|---------|
| Left | < -15° |
| Center | -15° to +15° |
| Right | > +15° |

| Vertical | Degrees |
|----------|---------|
| Up | < -15° |
| Center | -15° to +15° |
| Down | > +15° |

## Common Issues

### Low visibility on frontals

**Cause:** Mesh extraction failing or thresholds too strict

**Check:** `mesh_confidence` in diagnostic

**Fix:** Lower detection confidence:
```yaml
face_mesh:
  confidence:
    min_detection: 0.4  # default is 0.5
```

### Gaze always "center"

**Cause:** Iris landmarks not detected

**Check:** `use_iris` setting and iris landmark presence

**Fix:** Ensure iris refinement enabled:
```yaml
gaze:
  use_iris: true
```

### Mesh not running on faces

**Cause:** Faces not classified as close-ups

**Check:** Face area vs `closeup_threshold`

**Fix:** Lower threshold or increase sample rate:
```yaml
face_mesh:
  execution:
    closeup_threshold: 0.03  # default is 0.05
    sample_rate: 15  # default is 30
```

## Diagnostic Output

```json
{
  "face_id": "F_42_100",
  "visibility": {
    "overall_fraction": 0.85,
    "left_eye_visible": 1.0,
    "right_eye_visible": 0.7,
    "nose_visible": 1.0,
    "mouth_visible": 0.9,
    "forehead_visible": 0.8,
    "chin_visible": 0.75,
    "occluded_regions": ["right_eye"],
    "occlusion_type": "partial"
  },
  "gaze": {
    "horizontal": "center",
    "vertical": "center",
    "yaw_degrees": 5.2,
    "pitch_degrees": -3.1,
    "looking_at_camera": true,
    "confidence": 0.82
  },
  "mesh": {
    "landmarks_count": 468,
    "confidence": 0.91
  }
}
```

## Key Files

| File | Purpose |
|------|---------|
| `FEATURES/vision_analytics/docs/README.md` | Feature notes (planned) |
| `FEATURES/vision_analytics/TODO.md` | Sandbox TODO (planned) |
| `config/pipeline/analytics.yaml` | Configuration |
| `docs/todo/feature_mesh_and_advanced_visibility.md` | Implementation plan + QA checklist |

## Related Skills

- [face-alignment](../face-alignment/SKILL.md) - Alignment quality
- [body-tracking](../body-tracking/SKILL.md) - Body visibility
