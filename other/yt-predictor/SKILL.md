---
name: yt-predictor
description: Creator Vision Pro. Vision AI analysis to predict YouTube thumbnail performance and CTR via eye-tracking simulation.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Marketing
---

### System Instructions
You are equipped with the `yt-predictor` deterministic tool. This tool performs Vision AI analysis on video thumbnails to simulate eye-tracking heatmaps and CTR performance. It scores contrast, emotion, and conceptual framing against high-performing metadata.

### Execution Protocol
Invoke the vision engine by passing strictly formatted JSON:

```json
{
  "thumbnail_image_id": "IMG_THUMB_V33",
  "concept_description": "AI Agents replacing middle management",
  "simulation_type": "eye_tracking_heatmap",
  "compare_variants": true
}
```

Outputs
- Eye-tracking heatmap simulation and focal point analysis.
- Predicted CTR performance and engagement scoring.
- Contrast, emotion, and conceptual framing diagnostic.
- A/B test concept scoring and design improvement tips.
