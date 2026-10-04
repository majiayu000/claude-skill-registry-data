---
name: huashu-video-rendering
description: "Rendering React/Remotion sequences to MP4. Use when compiling Remotion compositions to final video files."
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Huashu Video Rendering

## Purpose
Compile high-performance Remotion-based animated compositions into standard video outputs like MP4.

## When to Use This Skill
Use when:
- Compiling React-based dynamic compositions into MP4 or WebM assets.
- Running headless Remotion rendering pipelines.

Do NOT use when:
- Building browser-only interactive animations with Framer Motion or GSAP.

## Phase 1: Remotion Composition Rendering
1. **Target Selection**: Determine target Remotion composition ID.
2. **Execute Render Command**:
   ```bash
   npx remotion render MyComp out.mp4
   ```

## Output Format / Delivery
- Rendered MP4 or WebM video file and terminal rendering logs.

## Behavior Rules
1. Always compile with optimized concurrency parameters based on core count.
2. Verify visual output dimensions match requested frame specs.

## Maintenance Notes
- Consolidated in June 2026.