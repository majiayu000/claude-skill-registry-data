---
name: generate-video
description: "Generates product demo videos and release walkthroughs via Remotion. Use when creating video documentation or animated demos."
when_to_use: "generate video, product demo video, release walkthrough, Remotion, animated demo"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Task", "AskUserQuestion", "WebFetch"]
disable-model-invocation: true
argument-hint: "[demo|arch|release]"
context: fork
---

# Generate Video Skill

A collection of skills responsible for automatically generating product explanation videos.

---

## Overview

This skill is used internally by the `/generate-video` command.
It executes the flow of codebase analysis → scenario proposal → parallel generation.

## Feature Details

| Feature | Details |
|---------|--------|
| **Best Practices** | See [references/best-practices.md](${CLAUDE_SKILL_DIR}/references/best-practices.md) |
| **Codebase Analysis** | See [references/analyzer.md](${CLAUDE_SKILL_DIR}/references/analyzer.md) |
| **Scenario Planning** | See [references/planner.md](${CLAUDE_SKILL_DIR}/references/planner.md) |
| **Parallel Scene Generation** | See [references/generator.md](${CLAUDE_SKILL_DIR}/references/generator.md) |
| **Visual Effects Library** | See [references/visual-effects.md](${CLAUDE_SKILL_DIR}/references/visual-effects.md) |
| **AI Image Generation** | See [references/image-generator.md](${CLAUDE_SKILL_DIR}/references/image-generator.md) |
| **Image Quality Assessment** | See [references/image-quality-check.md](${CLAUDE_SKILL_DIR}/references/image-quality-check.md) |

## Prerequisites

- Remotion is set up (`/remotion-setup`)
- Node.js 18+
- (Optional) `GOOGLE_AI_API_KEY` - for AI image generation

## `/generate-video` Flow

```
/generate-video
    │
    ├─[Step 1] Analysis (analyzer.md)
    │   ├─ Framework detection
    │   ├─ Key feature detection
    │   ├─ UI component detection
    │   └─ Project asset analysis (Plans.md, CHANGELOG, etc.)
    │
    ├─[Step 2] Scenario Proposal (planner.md)
    │   ├─ Auto-determine video type
    │   ├─ Scene composition proposal
    │   └─ User confirmation
    │
    ├─[Step 2.5] Asset Generation (image-generator.md) ← NEW
    │   ├─ Determine if assets are needed (intro, CTA, etc.)
    │   ├─ Generate 2 images with Nano Banana Pro
    │   ├─ Claude assesses quality (image-quality-check.md)
    │   └─ OK → adopt / NG → regenerate (up to 3 times)
    │
    └─[Step 3] Parallel Generation (generator.md)
        ├─ Parallel scene generation (Task tool)
        ├─ Integration + transitions
        └─ Final rendering
```

## Execution Steps

1. User runs `/generate-video`
2. Verify Remotion setup
3. Analyze codebase with `analyzer.md`
4. Propose scenario with `planner.md` + user confirmation
5. Parallel generation with `generator.md`
6. Completion report

## Video Types (by funnel stage)

| Type | Funnel Stage | Approx. Length | Auto-detection Criteria | Core Structure |
|------|-------------|----------------|------------------------|---------------|
| **LP/Ad Teaser** | Awareness → Interest | 30-90s | New project | Pain → Result → CTA |
| **Intro Demo** | Interest → Consideration | 2-3 min | UI changes detected | Complete 1 use case |
| **Release Notes** | Consideration → Conviction | 1-3 min | CHANGELOG updated | Before/After focused |
| **Architecture Overview** | Conviction → Decision | 5-30 min | Major structural changes | Production use + evidence |
| **Onboarding** | Retention & Adoption | 30s - several min | First-time setup | Shortest path to Aha moment |

> Details: [references/best-practices.md](${CLAUDE_SKILL_DIR}/references/best-practices.md)

## Scene Templates

### 90-second Teaser (for LP/ads)

| Time | Scene | Content |
|------|-------|---------|
| 0-5s | Hook | Pain or desired outcome |
| 5-15s | Problem+Promise | Target user and promise |
| 15-55s | Workflow | Signature workflow |
| 55-70s | Differentiator | Basis for differentiation |
| 70-90s | CTA | Next step |

### 3-minute Intro Demo (for consideration)

| Time | Scene | Content |
|------|-------|---------|
| 0-10s | Hook | Conclusion + pain |
| 10-30s | UseCase | Use case declaration |
| 30-140s | Demo | Full walkthrough on actual screens |
| 140-170s | Objection | Address one common concern |
| 170-180s | CTA | Call to action |

### Common Scenes

| Scene | Recommended Duration | Content |
|-------|---------------------|---------|
| Intro | 3-5s | Logo + tagline |
| Feature Demo | 10-30s | Playwright capture |
| Architecture Diagram | 10-20s | Mermaid → animation |
| CTA | 3-5s | URL + contact |

> Detailed templates: [${CLAUDE_SKILL_DIR}/references/best-practices.md](${CLAUDE_SKILL_DIR}/references/best-practices.md#templates)

## Audio Sync Rules (Important)

Strictly follow these rules for narrated videos:

| Rule | Value |
|------|-------|
| Audio start | Scene start + 30f (1-second wait) |
| Scene length | 30f + audio length + 20f padding |
| Transition | 15f (overlap with adjacent scenes) |
| Scene start calculation | Previous scene start + previous scene length - 15f |

**Pre-check**: Verify audio length with `ffprobe` before designing scenes

> Details: [${CLAUDE_SKILL_DIR}/references/generator.md](${CLAUDE_SKILL_DIR}/references/generator.md#audio-sync-rules-important)

## BGM Support

| Item | Recommended Value |
|------|------------------|
| With narration | bgmVolume: 0.20 - 0.30 |
| Without narration | bgmVolume: 0.50 - 0.80 |
| File location | `public/BGM/` |

> Details: [${CLAUDE_SKILL_DIR}/references/generator.md](${CLAUDE_SKILL_DIR}/references/generator.md#bgm-support)

## Subtitle Support

| Rule | Value |
|------|-------|
| Subtitle start | Same as audio start |
| Subtitle duration | Audio length + 10f |
| Font | Base64 embedding recommended |

> Details: [${CLAUDE_SKILL_DIR}/references/generator.md](${CLAUDE_SKILL_DIR}/references/generator.md#subtitle-support)

## Visual Effects Library

A collection of effects for impactful videos:

| Effect | Use Case |
|--------|----------|
| GlitchText | Hook, titles |
| Particles | Background, CTA convergence |
| ScanLine | Analysis in-progress effect |
| ProgressBar | Parallel processing display |
| 3D Parallax | Card display |

> Details: [references/visual-effects.md](${CLAUDE_SKILL_DIR}/references/visual-effects.md)

## Notes

- If Remotion is not set up, guide users to `/remotion-setup`
- Number of parallel generations auto-adjusts based on scene count (max 5)
- Generated videos are output to the `out/` directory
- AI-generated images are saved to `out/assets/generated/`
- When `GOOGLE_AI_API_KEY` is not set, image generation is skipped (existing assets or placeholders are used)
