---
description: AI predicts which content will go viral before posting.
---

# Viral Predictor Skill

## Strategic Value

The Viral Predictor analyzes content before publication, forecasting viral potential based on historical performance data, audience psychology patterns, and platform algorithms. By identifying high-probability viral content before it goes live, marketers can optimize distribution timing, double-down on winning concepts, and avoid wasting resources on low-potential material—essentially trading reactive analysis for predictive advantage.

## Capabilities

- **Pre-Publish Scoring:** Assigns virality probability scores to draft content.
- **Multi-Platform Prediction:** Calibrated predictions for TikTok, Instagram, Twitter/X, YouTube, etc.
- **Hook Analysis:** Identifies strong vs. weak opening hooks.
- **Timing Optimization:** Recommends optimal posting times for viral potential.
- **Thumbnail/Creative Scoring:** Evaluates visual elements for click-through appeal.
- **A/B Variant Ranking:** Ranks multiple versions by predicted performance.

## Limitations

- Viral prediction is inherently probabilistic, not guaranteed.
- Requires continuous training on platform algorithm changes.
- Black swan events (unexpected virality) cannot be predicted.

## Examples

### Example 1: Video Content Prediction

**User Prompt:** "I have three video concepts for Instagram Reels. Predict which will perform best."

**Prediction Output:**
```json
{
  "predictions": [
    {
      "concept": "Behind-the-scenes product development",
      "viral_probability": 82,
      "confidence": "high",
      "key_factors": [
        "Novelty factor: BTS content trending +45%",
        "Emotional hook: Humanizes brand",
        "Shareability: High audience curiosity"
      ],
      "recommended_timing": "Tuesday 11 AM",
      "optimized_caption": "Ever wondered how we build... [intriguing hook]"
    },
    {
      "concept": "Product feature demo",
      "viral_probability": 45,
      "confidence": "medium",
      "key_factors": [
        "Risk: Too promotional for organic reach",
        "Mitigation: Lead with transformation story"
      ],
      "recommendation": "Repurpose for paid ads instead"
    },
    {
      "concept": "User-generated content compilation",
      "viral_probability": 68,
      "confidence": "medium",
      "key_factors": [
        "Positive: Social proof drives engagement",
        "Risk: Overused format, lower novelty"
      ]
    }
  ],
  "recommendation": "Proceed with Concept 1 (BTS), highest viral probability"
}
```

### Example 2: Ad Creative Optimization

**User Prompt:** "Score these 5 ad creatives for viral potential in our upcoming campaign."

**Prediction Output:**
```json
{
  "rankings": [
    {
      "creative_id": "ad_03_emotional",
      "score": 91,
      "prediction": "High viral potential",
      "strengths": ["Emotional hook in first 3 seconds", "Relatable story arc"],
      "estimated_reach": "500K-2M organic impressions",
      "cta_performance": "Expected 8-12% click-through rate"
    },
    {
      "creative_id": "ad_01_feature_focus",
      "score": 34,
      "prediction": "Low viral potential",
      "weaknesses": ["Feature listing lacks emotional hook", "Too promotional"],
      "recommendation": "Reframe as problem-solution narrative",
      "estimated_reach": "5K-15K organic impressions"
    }
  ],
  "budget_allocation_suggestion": "75% to ad_03, 25% to testing other variants"
}
```

## Configuration (config.yaml)

```yaml
prediction_models:
  instagram_reels:
    factors:
      - hook_strength
      - novelty_score
      - emotional_resonance
      - visual_appeal
      - timing_factor
  tiktok:
    factors:
      - first_3_seconds
      - music_trend_fit
      - comment_potential
      - shareability
      - completion_rate_estimate
  twitter:
    factors:
      - headline_hook
      - thread_structure
      - visual_inclusion
      - controversy_balance

training_data:
  historical_posts: 10000
  viral_threshold: "top_1_percent_engagement"
  update_frequency: "weekly"

scoring:
  threshold_high: 80
  threshold_medium: 50
  threshold_low: 30
```
