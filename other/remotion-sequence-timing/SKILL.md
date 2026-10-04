---
name: remotion-sequence-timing
description: Managing layered sequences and delays in Remotion. Use when orchestrating multiple layered sequences, slide transitions, or audio delays.
version: "1.0.0"
verified_date: 2026-06-01
category: core
---

# Remotion Sequence Timing

## Purpose
Orchestrate frame ranges, sequence layers, and delayed presentation of visual blocks.

## When to Use This Skill
- Layering visual elements at specific offsets in a video composition.
- Choreographing entrance and exit delay boundaries for multiple segments.

## Output Format / Delivery
Provide compliant composition trees wrapping sub-elements inside `<Sequence />` blocks.

## Behavior Rules
1. **Always specify exact start frame and duration limits** on sequences.
2. **Never allow unmapped frames to flash** empty surfaces.

## Maintenance Notes
This skill is locked for Remotion sequence rules.

---

## Phase 1: Sequence Orchestration

Wrap components in `<Sequence from={30} durationInFrames={60}>`.
