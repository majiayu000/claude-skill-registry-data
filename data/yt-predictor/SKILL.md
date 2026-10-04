---
name: youtube-thumbnail-predictor
description: Analyze YouTube thumbnail concepts, predict Click-Through Rate with A/B test recommendations, and track actual metrics. Integrates channel analytics and revenue tracking.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

Instructions:
To run this skill, you MUST call the run_js tool with this parameter:
- data: A JSON string with the keys "video_title" and "visual_concept" (a description of the image).

Example tool call: run_js(data='{"video_title": "I built a house in 24 hours", "visual_concept": "Close up of my shocked face holding a hammer with a finished mansion in the background"}')