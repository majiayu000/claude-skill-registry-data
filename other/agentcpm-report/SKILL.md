---
name: agentcpm-report
title: "AgentCPM-Report: Interleaving Drafting and Deepening for Deep Research"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.06540"
keywords: [Agent Planning, Research Automation, Iterative Refinement, Report Generation, Multi-Stage Training]
description: "Enable research agents to interleave evidence-based drafting with reasoning-driven deepening, automatically expanding outlines based on discovered gaps, using trajectory pruning for efficient RL training."
---

# AgentCPM-Report: Interleaving Drafting and Deepening for Deep Research

## Problem Context

Existing deep research systems separate planning from writing, limiting adaptive discovery. Agents that rigidly follow pre-planned outlines miss opportunities to refine understanding as evidence emerges. The "insight ceiling" arises from static structure: agents execute plans without evaluating draft quality or identifying knowledge gaps mid-process.

## Core Concept

**WARP (Writing As Reasoning Policy)** interleaves evidence-based drafting with reasoning-driven deepening. Rather than plan-then-write, the agent autonomously:
- Generates search queries from accumulated narrative context
- Drafts evidence-grounded content
- Analyzes drafts for logical gaps
- Decides whether to expand sections or terminate
- Updates outlines based on discoveries

This mirrors human knowledge-transforming processes where writing reveals what you don't know.

## Architecture Overview

- **Sparse Level-1 Outline**: Initial high-level structure from query
- **Evidence-Based Drafting**: Per-section search, retrieval, synthesis
- **Gap Analysis**: Logical consistency checking on drafted content
- **Adaptive Expansion**: Outline evolution based on insufficiencies
- **Multi-Stage Training**: Cold-start SFT → atomic skill RL → holistic pipeline RL

## Implementation

**Core cycle (Plan-Draft-Deepen-Decide):**

```python
class ResearchAgent:
    def __init__(self, query):
        self.outline = create_sparse_outline(query)
        self.draft = ""

    def evidence_based_draft(self):
        for section in self.outline:
            search_query = contextual_query(self.draft, section)
            docs = retrieve_documents(search_query)
            section_content = synthesize(docs)
            self.draft += section_content

    def reasoning_driven_deepen(self):
        # Analyze draft for logical gaps
        gaps = identify_gaps(self.draft)
        confidence = analyze_coverage(self.draft)

        if gaps and confidence < threshold:
            # Expand insufficient section
            section = gaps[0]
            self.outline = expand_section(self.outline, section)
            return True  # Continue
        else:
            return False  # Terminate
```

**Training procedure (3-stage):**

1. **Cold-Start SFT**: Finetune on teacher-generated research trajectories with dense annotations
2. **Atomic Skill RL**: Optimize individual actions (search, write, plan, terminate) using GRPO with trajectory pruning
3. **Holistic Pipeline RL**: End-to-end optimization of final report quality against reference benchmarks

**Trajectory pruning**: Identify optimal stopping points in teacher sequences—the earliest decision point where continuing doesn't improve final report quality. This accelerates training by removing redundant steps.

## Practical Guidance

**When to use**: Deploy for research tasks requiring iterative knowledge discovery (literature reviews, technical feasibility studies, competitive analysis). Less effective for well-structured tasks with clear boundaries.

**Query structuring**: Start with complex, multi-part queries; agent naturally decomposes during deepening. Avoid over-specific initial queries.

**Convergence signals**: Monitor draft-to-outline ratio (well-formed drafts show 5–10× expansion); terminate after 2–3 deepening cycles without gap discovery.

**Model scaling**: Cold-start SFT works with 8B models; smaller models may require larger teacher datasets. Scaling to 70B improves deepening quality significantly.

## Reference

The framework uses atomic skill decomposition to train small models on complex agentic reasoning. Trajectory pruning removes ~40% of redundant steps without quality loss, enabling efficient RL on limited data. Small (8B) models achieve competitive performance with appropriate curriculum, demonstrating that multi-stage training is more important than model scale for agentic systems.
