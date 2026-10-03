---
name: memfly
title: "MemFly: On-the-Fly Memory Optimization via Information Bottleneck"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: "https://arxiv.org/abs/2602.07885"
keywords: [Memory Management, Information Bottleneck, LLM Agents, Memory Retrieval, Long-term Memory]
description: "Optimize agent long-term memory by treating it as an information bottleneck problem. Dynamically compress redundant information while preserving task-relevant content through semantic-symbolic-topological hybrid retrieval."
---

# MemFly: Information Bottleneck Memory Optimization

## Problem Context

LLM agents struggle with effective long-term memory management. As interaction history grows, memory becomes bloated with redundant information, making relevant evidence retrieval expensive and ineffective. Traditional approaches either keep everything (wasteful) or apply uniform summarization (lossy). The core challenge: compress memory while preserving task-critical information without knowing future task demands.

## Core Concept

MemFly treats long-term memory as an **information bottleneck optimization problem**. It dynamically constructs a three-layer memory hierarchy (Notes → Keywords → Topics) while minimizing two competing objectives:

1. **Compress**: Remove redundant information
2. **Preserve**: Maintain task-relevant content

During memory construction, an LLM-based optimizer performs three operations (Merge, Link, Append) guided by redundancy and complementarity scores. During retrieval, three pathways (semantic, symbolic, topological) work synergistically to find relevant information across levels.

## Architecture Overview

- **Three-Layer Memory Hierarchy**: Notes (raw), Keywords (entities), Topics (concepts)
- **Information Bottleneck Optimization**: Greedy Merge/Link/Append operations
- **Redundancy Scoring**: Identify and consolidate duplicate information
- **Complementarity Assessment**: Preserve novel, task-relevant content
- **Hybrid Retrieval System**: Macro-semantic, micro-symbolic, topological pathways
- **Reciprocal Rank Fusion**: Combine results from multiple retrieval paths
- **Iterative Refinement**: Progressively expand evidence for complex reasoning

## Implementation

The information bottleneck memory construction:

```python
class MemoryOptimizer:
    """
    Optimize memory through information bottleneck principles.
    Compress redundancy while preserving task-relevant information.
    """

    def __init__(self, model, max_tokens=50000):
        self.model = model
        self.max_tokens = max_tokens
        self.memory = {
            'notes': [],        # Raw facts
            'keywords': set(),  # Entity anchors
            'topics': []        # Concept clusters
        }

    def compute_redundancy_score(self, new_note, existing_notes):
        """
        Measure how redundant new_note is with existing memory.
        High redundancy → candidate for merge.
        """
        if not existing_notes:
            return 0.0

        # Semantic similarity with existing notes
        similarities = [
            self.model.similarity(new_note, existing)
            for existing in existing_notes
        ]
        return max(similarities)

    def compute_complementarity_score(self, new_note, task_context):
        """
        Measure how novel and task-relevant new_note is.
        High complementarity → preserve information.
        """
        # Relevance to current task
        task_relevance = self.model.task_relevance(
            new_note, task_context)

        # Novelty compared to existing memory
        memory_text = ' '.join(self.memory['notes'])
        novelty = 1.0 - self.model.similarity(new_note, memory_text)

        return 0.6 * task_relevance + 0.4 * novelty

    def add_note(self, new_note, task_context):
        """
        Add new information to memory with optimization.
        Decides whether to merge, link, append, or discard.
        """
        redundancy = self.compute_redundancy_score(
            new_note, self.memory['notes'])
        complementarity = self.compute_complementarity_score(
            new_note, task_context)

        # Greedy information bottleneck decisions
        if redundancy > 0.85:
            # Merge with most similar existing note
            self._merge_with_most_similar(new_note)
        elif complementarity > 0.5:
            # Append novel information
            self.memory['notes'].append(new_note)
            # Extract and add entity keywords
            keywords = self.model.extract_entities(new_note)
            self.memory['keywords'].update(keywords)
        # else: discard low-complementarity information

    def _link_to_topics(self):
        """
        Create topical associations between notes.
        Enable topological expansion during retrieval.
        """
        topics = self.model.cluster_by_topic(self.memory['notes'])
        self.memory['topics'] = topics
        # Build topic-to-note graph for traversal
        self.topic_graph = {
            topic: notes for topic, notes in topics.items()
        }
```

Hybrid retrieval system combining three pathways:

```python
class HybridRetriever:
    """
    Retrieve relevant memory through semantic, symbolic, topological paths.
    Combines results using Reciprocal Rank Fusion.
    """

    def __init__(self, memory_optimizer):
        self.memory = memory_optimizer.memory
        self.topic_graph = memory_optimizer.topic_graph
        self.model = memory_optimizer.model

    def macro_semantic_navigation(self, query, k=5):
        """
        Pathway 1: Navigate through Topics for high-level localization.
        Reduces search space before detailed retrieval.
        """
        # Find most relevant topic
        topic_scores = {
            topic: self.model.similarity(query, ' '.join(notes))
            for topic, notes in self.topic_graph.items()
        }
        best_topic = max(topic_scores, key=topic_scores.get)
        # Return notes in best topic
        return self.topic_graph[best_topic][:k]

    def micro_symbolic_anchoring(self, query, k=5):
        """
        Pathway 2: Extract entities from query and match in keywords.
        Provides precise entity-based retrieval.
        """
        # Extract entities from query
        entities = self.model.extract_entities(query)

        # Find notes containing these entities
        relevant_notes = []
        for note in self.memory['notes']:
            note_entities = self.model.extract_entities(note)
            overlap = len(entities & note_entities)
            if overlap > 0:
                relevant_notes.append((note, overlap))

        # Sort by entity overlap and return top k
        relevant_notes.sort(key=lambda x: x[1], reverse=True)
        return [note for note, _ in relevant_notes[:k]]

    def topological_expansion(self, seed_notes, k=5):
        """
        Pathway 3: Expand from seed notes through topic associations.
        Finds logically related evidence.
        """
        expanded = set(seed_notes)
        for note in seed_notes:
            # Find notes in same topics
            for topic, notes in self.topic_graph.items():
                if note in notes:
                    expanded.update(notes)

        return list(expanded)[:k]

    def retrieve_with_fusion(self, query, task_context, k=5):
        """
        Combine all three pathways using Reciprocal Rank Fusion.
        """
        # Run all pathways in parallel
        semantic_results = self.macro_semantic_navigation(query, k)
        symbolic_results = self.micro_symbolic_anchoring(query, k)

        # Topic expansion from symbolic results
        topological_results = self.topological_expansion(
            symbolic_results, k)

        # Reciprocal Rank Fusion: weighted combination
        rrf_scores = {}
        for i, note in enumerate(semantic_results):
            rrf_scores[note] = rrf_scores.get(note, 0) + 1/(i+1)
        for i, note in enumerate(symbolic_results):
            rrf_scores[note] = rrf_scores.get(note, 0) + 1/(i+1)
        for i, note in enumerate(topological_results):
            rrf_scores[note] = rrf_scores.get(note, 0) + 1/(i+1)

        # Return top k by RRF score
        sorted_notes = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [note for note, _ in sorted_notes[:k]]

    def iterative_refinement(self, query, task_context, max_rounds=3):
        """
        For complex queries, progressively expand evidence.
        Stop when sufficient evidence gathered.
        """
        evidence = self.retrieve_with_fusion(query, task_context, k=5)

        for round_num in range(max_rounds):
            # Evaluate if current evidence suffices
            sufficiency = self.model.evaluate_evidence_sufficiency(
                query, evidence, task_context)

            if sufficiency > 0.8:
                break

            # Expand topologically
            evidence.extend(
                self.topological_expansion(evidence, k=3)
            )

        return evidence
```

## Practical Guidance

**When to use**:
- Building long-running agent systems with extensive interaction history
- Need to manage memory growth while preserving effectiveness
- Task-relevant information varies over time
- Want to balance memory size and retrieval quality

**Memory construction tuning**:
- **Redundancy threshold**: Set to 0.85 for aggressive merging, 0.95 for conservative
- **Complementarity threshold**: 0.5 balances novelty and task relevance
- **Merge strategy**: Combine semantically similar notes into abstracted form

**Retrieval configuration**:
- Start with semantic navigation for high-level scoping
- Add symbolic anchoring for entity-specific queries
- Use topological expansion for reasoning tasks requiring context
- Reciprocal Rank Fusion weights all pathways equally (tune if needed)

**Expected improvements**:
- 60-70% memory compression vs storing all interactions
- Comparable or better retrieval effectiveness than full-memory baselines
- Faster response times due to reduced search space
- Graceful degradation as memory grows

**Implementation checklist**:
1. Initialize LLM-based optimizer for redundancy/complementarity scoring
2. Implement three-layer memory hierarchy
3. Build topic graph for topological navigation
4. Deploy hybrid retrieval with RRF fusion
5. Add iterative refinement for complex queries

## Reference

Information bottleneck memory optimization enables efficient long-term memory for agents by compressing redundancy while preserving task-relevant information. The hybrid retrieval system leverages semantic, symbolic, and topological pathways to find evidence across scales of abstraction.
