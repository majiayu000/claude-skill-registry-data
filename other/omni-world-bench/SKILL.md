---
name: omni-world-bench
title: "Omni-WorldBench: A Unified Benchmark for Interactive World Models"
version: 0.0.3
engine: skillxiv-v0.0.3-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2603.22212
keywords: [World Models, Benchmark, Interaction, Video Generation, Evaluation]
description: "Evaluate world models on faithful interactive response capability through three hierarchical interaction levels (single object, localized, multi-object effects) and four complementary metrics measuring video quality, controllability, and physical plausibility. Identifies the gap between visual fidelity and true interactive state transition modeling."
---

## Task Definition

Omni-WorldBench organizes interactive evaluation across three interaction complexity levels:

- **Level 1**: Single-object actions with no environmental changes (pick, rotate, move)
- **Level 2**: Localized interactions where one object directly affects another (push, pour, place)
- **Level 3**: Complex multi-object effects where actions influence broader environmental state (knock over objects, trigger cascades)

Scene domains span daily-life scenarios and task-oriented settings: autonomous driving, embodied robotics, and gaming.

## Evaluation Metrics (Omni-Metric)

The benchmark measures three complementary dimensions:

### 1. Generated Video Quality
Temporal flickering, motion smoothness, content-query alignment, and dynamic degree of scene change.

### 2. Camera-Object Controllability
- **Camera adherence**: How closely generated trajectories match specified camera paths
- **Object consistency**: Persistent object identity across frames
- **Transitions Detect**: Novel metric scoring scene transition smoothness
- Jointly measured to ensure models respect spatial constraints while maintaining semantic coherence

### 3. Interaction Effect Fidelity
Measures whether state transitions faithfully reflect physical causality:
- **InterStab-L**: Long-term temporal consistency at revisit points (same location, different time)
- **InterStab-N**: Stability in non-target regions (unchanged areas remain stable)
- **InterCov**: Object-level semantic consistency across interaction
- **InterOrder**: Temporal event sequence alignment (if A causes B, sequences maintain order)

## What It Measures

The core measurement target: "Does the world model faithfully reflect how interaction actions drive state transitions across space and time?" This directly addresses the gap between achieving high visual quality and actually modeling interactive response capability—many models generate visually convincing videos without maintaining physical plausibility under interaction.

## Baseline Strategy

Rather than proposing novel baseline models, the benchmark evaluates 18 existing representative systems across three generative paradigms:
- **Text-to-Video**: Models taking natural language descriptions as input
- **Image-to-Video**: Models conditioning on initial frames
- **Camera-Conditioned**: Models taking explicit camera trajectories as control

This comparative evaluation establishes performance boundaries in current interactive modeling rather than anchoring evaluation to a single approach.

## When to Use

Apply this benchmark when evaluating any pretrained world model's interactive capability—video diffusion models, autoregressive video generators, or physics simulators. Particularly valuable for embodied AI systems where faithful interaction modeling is safety-critical.
