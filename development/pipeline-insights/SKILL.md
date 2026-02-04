---
name: pipeline-insights
description: AI-powered pipeline diagnostics. Explains why faces weren't detected, tracked, embedded, or clustered using OpenAI GPT-4o analysis. Use when debugging pipeline issues, reviewing unclustered tracks, or understanding why quality gates rejected faces.
---

# Pipeline Insights Skill

Use this skill to get AI-powered explanations for pipeline failures.

## When to Use

- Track wasn't clustered and you don't know why
- Faces show "skipped" but the reason isn't clear
- Quality gate rejected faces you expected to pass
- Need to understand which config threshold to adjust
- Batch diagnosing unclustered tracks

## Quick Start

### Diagnose a Single Track

```bash
curl -X POST "http://localhost:8000/diagnostics/episodes/{ep_id}/diagnose_track/{track_id}"
```

### Diagnose All Unclustered Tracks

```bash
curl -X POST "http://localhost:8000/diagnostics/episodes/{ep_id}/diagnose_unclustered" \
  -H "Content-Type: application/json" \
  -d '{"max_tracks": 50}'
```

### Check Service Status

```bash
curl "http://localhost:8000/diagnostics/status"
```

## Understanding Results

### Stage Progression

Each track progresses through these stages:

| Stage | Description | Failure Meaning |
|-------|-------------|-----------------|
| `detected` | RetinaFace found a face | Face not visible or below confidence |
| `tracked` | ByteTrack linked across frames | Lost tracking or single-frame only |
| `embedded` | ArcFace generated 512-d embedding | Quality gate rejected (blur, pose, contrast) |
| `clustered` | Agglomerative clustering assigned identity | Below similarity threshold or outlier |

### Common Failure Patterns

#### "embedding:min_blur_score"

**Cause**: Face too blurry (motion blur, out of focus)

**Check**: `max_blur_score` in diagnostic vs threshold (default: 18.0)

**Fix**: Lower `config/pipeline/faces_embed_sampling.yaml`:
```yaml
quality_gating:
  min_blur_score: 10.0  # default is 18.0
```

#### "clustering:min_identity_sim"

**Cause**: Embedding didn't match any existing cluster

**Check**: `nearest_cluster_sim` in diagnostic

**Fix**: Lower `config/pipeline/clustering.yaml`:
```yaml
cluster_thresh: 0.44  # default is 0.52
min_identity_sim: 0.40  # default is 0.45
```

#### "detection:confidence"

**Cause**: Face detection confidence too low

**Fix**: Lower `config/pipeline/detection.yaml`:
```yaml
confidence_th: 0.40  # default is 0.50
```

## Config Reference

### Embedding Thresholds

File: `config/pipeline/faces_embed_sampling.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `min_blur_score` | 18.0 | Minimum Laplacian variance (sharpness) |
| `min_confidence` | 0.45 | Minimum detection confidence |
| `min_quality_score` | 1.5 | Combined quality score |
| `max_yaw_angle` | 60.0 | Maximum head rotation (degrees) |
| `max_pitch_angle` | 45.0 | Maximum head tilt (degrees) |

### Clustering Thresholds

File: `config/pipeline/clustering.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `cluster_thresh` | 0.52 | Cosine similarity for clustering |
| `min_identity_sim` | 0.45 | Minimum similarity to centroid |
| `min_cluster_size` | 1 | Minimum tracks per cluster |

## Diagnostic Output Example

```json
{
  "track_id": 59,
  "stage_reached": "tracked",
  "stage_failed": "embedded",
  "raw_data": {
    "faces_count": 1,
    "faces_skipped": 1,
    "skip_reasons": ["blurry:10.8"],
    "max_blur_score": 10.78,
    "embedding_generated": false
  },
  "ai_analysis": {
    "explanation": "Track 59 has only 1 face, and that face was too blurry (score 10.78) to generate an embedding. The minimum blur threshold is 18.0.",
    "root_cause": "Single-frame track with blur below quality gate",
    "blocked_by": "embedding:min_blur_score",
    "suggested_fixes": [
      "Lower min_blur_score to 10.0",
      "Manually assign track in Faces Review UI"
    ],
    "config_changes": [{
      "file": "config/pipeline/faces_embed_sampling.yaml",
      "key": "quality_gating.min_blur_score",
      "current": 18.0,
      "suggested": 10.0,
      "reason": "Allow blurrier faces for short tracks"
    }]
  }
}
```

## Saved Reports

Diagnostic reports are saved to:
```
data/manifests/{ep_id}/diagnostics/
├── track_0059_diagnostic.json
├── track_0127_diagnostic.json
└── ...
```

Reports are cached - use `force_refresh: true` to regenerate.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DIAGNOSTIC_PROVIDER` | No | `anthropic` | AI provider: `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If using Anthropic | - | Anthropic API key |
| `ANTHROPIC_DIAGNOSTIC_MODEL` | No | `claude-sonnet-4-20250514` | Claude model to use |
| `OPENAI_API_KEY` | If using OpenAI | - | OpenAI API key |
| `OPENAI_DIAGNOSTIC_MODEL` | No | `gpt-4o` | OpenAI model to use |

**Provider Fallback**: If the preferred provider is unavailable, falls back to the other provider. If neither API key is set, uses rule-based analysis.

## Related Skills

- [pipeline-debug](../pipeline-debug/SKILL.md) - General pipeline debugging
- [cluster-quality](../cluster-quality/SKILL.md) - Quality metrics interpretation
