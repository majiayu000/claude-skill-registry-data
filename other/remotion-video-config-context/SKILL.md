---
name: remotion-video-config-context
description: Extracts global composition properties to create relative, responsive animations. Use when calculating relative animation offsets, frame timelines, or dynamic aspect bounds.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Video Config Context

## Purpose
Extract and utilize global composition metrics (fps, durationInFrames, width, height) to build relative and responsive video elements.

## When to Use This Skill
- Calculating relative entrance or exit anim keys (e.g. exit 1s before end).
- Adjusting component scales based on resolution aspect bounds dynamically.

## Output Format / Delivery
Provide client video hook integrations extracting metadata properties safely.

## Behavior Rules
1. **Never use hard-coded absolute frame indices** for exit animations — always calculate them relative to the total duration.
2. **Always leverage composition dimensions** to scale coordinate layouts.

## Maintenance Notes
This skill is locked for video contexts.

---

## Phase 1: Context Extraction Patterns

`const { fps, durationInFrames, width, height } = useVideoConfig();`
