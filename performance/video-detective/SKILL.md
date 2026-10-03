---
name: video-detective
title: "VideoDetective: Clue Hunting for Long-Video Understanding via Manifold-Aware Exploration"
version: 0.0.3
engine: skillxiv-v0.0.3-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2603.22285
keywords: [Video Understanding, Sparse Sampling, Graph Inference, Multimodal Evidence]
description: "Enable VLMs to find relevant clips in long videos through sparse observation and graph-based propagation. Iteratively hypothesize promising segments, extract multimodal evidence (captions, OCR, speech), and propagate relevance scores via visual-temporal affinity graph. Jointly model extrinsic relevance (query-to-segment matching) and intrinsic relevance (video internal structure) to infer unobserved segments. Achieves competitive accuracy with significantly fewer tokens than dense sampling."
---

## Clue Hunting Mechanism

VideoDetective decomposes long-video understanding into three iterative phases:

### Phase 1: Hypothesis
Select candidate video segments based on initial query relevance estimation. Rather than exhaustive sampling, prioritize segments likely to contain answer evidence.

### Phase 2: Verification
Extract multimodal evidence from selected segments:
- **Visual**: Frame content and appearance
- **Captions**: Automatically generated scene descriptions
- **OCR**: On-screen text (subtitles, labels, overlays)
- **Speech**: Transcript of audio content

Score each segment's relevance to query using evidence fusion.

### Phase 3: Refinement
Propagate relevance scores across visual-temporal affinity graph to estimate unobserved segments, creating global belief field over entire video.

This sparse observation approach requires far fewer tokens than methods that densely sample and process every frame.

## Extrinsic vs. Intrinsic Relevance

### Extrinsic Relevance
Query-to-segment direct matching: "How well does this segment answer the user's question?"
- Based on multimodal evidence (captions, OCR, speech)
- Direct semantic alignment with query
- Observable only by processing the segment

### Intrinsic Relevance
Video internal structure: "What's the semantic relationship between segments?"
- Segments clustered together likely share meaning
- Temporal proximity correlates with semantic continuity
- Visual similarity suggests related content
- Inferred without processing every segment

**Joint Modeling:**
Combine both signals: relevance = extrinsic confidence × intrinsic structure propagation

This enables the system to say "we only observed segment 5, which was relevant, and segments 4 and 6 are visually similar and adjacent, so they're likely relevant too."

## Frame Identification Strategy

Rather than pixel-level frame selection, VideoDetective operates at segment granularity:

**Graph Construction:**
Build visual-temporal affinity graph encoding:
- Visual similarity between segment pairs (CNN feature distance)
- Temporal proximity (segments close in time connected strongly)
- Result: k-nearest neighbor graph on segment embeddings

**Selective Observation:**
Use active learning to choose anchor segments:
1. High uncertainty regions (marginal relevance)
2. Representative of different video regions
3. Maximize information gain per token

**Propagation via Graph Diffusion:**
For each observed anchor segment:
1. Extract multimodal evidence (captions, OCR, speech)
2. Compute extrinsic relevance score
3. Run graph diffusion to propagate to unobserved neighbors
4. Create global belief field over all segments

**Diversity via Graph-NMS:**
Apply Non-Maximum Suppression on graph:
- Select high-confidence segments
- Suppress nearby neighbors (avoid redundancy)
- Ensures semantic aspect coverage across video

## Performance Characteristics

### Token Efficiency
Achieves competitive accuracy with significantly fewer visual tokens than:
- Dense frame sampling (every N frames)
- Uniform segment coverage (cover entire video equally)
- Multi-scale sampling (process at different resolutions)

Exact speedup depends on:
- Video length (longer videos benefit more from sparsity)
- Query complexity (localized queries use fewer segments)
- Segment-to-token ratio (coarse segments require fewer tokens)

### Accuracy-Efficiency Tradeoff
- More observation budget → higher accuracy, more tokens
- Fewer observations → faster inference, potential accuracy loss
- Graph propagation acts as implicit regularizer (neighboring segments should have similar relevance)

## Conditions of Applicability

**Works well when:**
- Video has clear temporal structure (coherent scenes, semantic continuity)
- Query is localized (answer in specific clips, not scattered throughout)
- Visual similarity correlates with semantic similarity (content is organized spatially)
- Token budget is limited (sparse sampling critical for efficiency)

**Less optimal when:**
- Query requires integrating evidence across entire video (non-localized)
- Video structure is fragmented (random cuts, rapid scene changes)
- Visual similarity misleads (visually similar scenes have different meanings)
- Dense processing is needed (safety-critical applications requiring comprehensive coverage)

## Integration Pattern

**Input Assumptions:**
- Segmented video (pre-computed clip boundaries)
- Query in natural language
- Optional: pre-computed segment embeddings/captions

**Output:**
- Ranked list of relevant segments
- Confidence scores (from relevance propagation)
- Evidence excerpts (captions, OCR, speech snippets)

**Minimal Wrapper:**
```
Long video query
    ↓
Segment hypothesis (initial ranking)
    ↓
Selective observation + evidence extraction
    ↓
Graph diffusion (propagate to unobserved)
    ↓
Graph-NMS (diversify + select top-K)
    ↓
Relevant clips + evidence
```

Works with any VLM capable of multimodal understanding without requiring architectural changes.
