---
name: remotion-composition-metadata
description: Defining composition frame-rate, duration, and dimensions in Remotion. Use when configuring video size, target FPS, or total duration parameters.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Composition Metadata

## Purpose
Enforce standard parameter ranges for Remotion composition metadata, including FPS, aspect ratios, and timeline durations.

## When to Use This Skill
- Declaring a new video canvas size or frame rate.
- Configuring timeline frame bounds in `@remotion/player` or rendering pipelines.

## Output Format / Delivery
Provide compliant composition attributes for `<Composition />` components.

## Behavior Rules
1. **Always set FPS to 30 or 60** for standard web and video streaming formats.
2. **Always match aspect ratio width/height exactly to target media specs**.

## Maintenance Notes
This skill is locked for standard Remotion composition metadata.

---

## Phase 1: Video Metadata Configuration

- Default: 1920x1080, 30fps.
- Short SaaS: 5-10 seconds.