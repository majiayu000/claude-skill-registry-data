---
name: open-researcher
title: "OpenResearcher: Offline Open-Domain Reasoning with Local Search"
version: 0.0.3
engine: skillxiv-v0.0.3-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2603.20278
keywords: [Research Infrastructure, Reasoning, Search, Offline, Tool Use]
description: "Replace live web API-dependent research with offline corpus-based trajectory synthesis. Decouples answer-guided document retrieval (10K gold + 15M FineWeb) from synthesis via local search engine, eliminating $5,760 Serper costs while enabling reproducible, analyzable reasoning chains through three primitives: Search (ranked retrieval), Open (full document fetch), Find (intra-document verification)."
---

## Capability Gap

Existing deep research systems (like those using live web APIs) face three critical limitations:

1. **Cost at scale**: $5,760+ for comprehensive search synthesis limits research automation
2. **Reproducibility**: Dynamic web content changes make trajectories non-deterministic and difficult to audit
3. **Analysis opacity**: Live API calls obscure failure modes—difficult to diagnose why reasoning chains fail

OpenResearcher eliminates these constraints through offline infrastructure.

## Core Abstractions

Three explicit browser primitives model human research behavior while enabling systematic analysis:

### 1. Search
Returns top-K ranked results with snippets from corpus.
- Executed against merged document pool (10K gold + 15M FineWeb)
- Deterministic ranking via local search engine
- Enables corpus-level evidence discovery

### 2. Open
Fetches full document content from URLs in corpus.
- Returns complete text for selected documents
- Supports multi-document integration
- Enables deep context understanding

### 3. Find
Locates exact string matches within opened documents.
- Precise evidence localization
- Supports substring search and regex
- Enables verification of claims

This progression from broad retrieval → content fetching → precise localization mirrors human research iterating from literature survey to evidence collection.

## Design Decisions

**Two-Phase Synthesis Pipeline:**

Phase 1: **Answer-Guided Corpus Bootstrapping**
- Initial query → Serper API gathers 10K gold documents
- Merged with 15M FineWeb base corpus
- One-time cost to construct domain-specific corpus

Phase 2: **Offline Trajectory Synthesis**
- Teacher model (GPT-OSS-120B) generates 97K+ trajectories
- No further API calls required
- Deterministic, reproducible reasoning chains

This separation decouples expensive retrieval from synthesis, making reasoning scalable once corpus is established.

## Integration Patterns

**API Layer Design:**

```
┌─────────────────────────────┐
│  Reasoning Agent            │
│  (queries research tasks)   │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Three-Tool Abstraction     │
│  Search / Open / Find       │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Local Search Engine        │
│  (Merged corpus: 10K+15M)   │
└─────────────────────────────┘
```

**Tool Sequencing Pattern:**
1. Agent calls `Search(query)` → receives ranked candidates
2. Agent calls `Open(url)` → retrieves full document
3. Agent calls `Find(text, document)` → locates specific evidence
4. Agent integrates evidence into reasoning step
5. Repeat until answer is complete or confidence sufficient

This is directly executable without external APIs, enabling both cost reduction and reproducibility.

## Performance & Cost Analysis

**Cost Comparison:**
- Live API approach (Serper): $5,760 for comprehensive search synthesis
- OpenResearcher offline: $0 after corpus bootstrapping
- Cost reduction: 100% (amortized per-query cost approaches zero)

**Reproducibility:**
- Live APIs: trajectories change if web content changes
- OpenResearcher: identical results across time
- Enable corpus versioning for comparative analysis

**Analysis Capability:**
- Systematic gold-document hit tracking
- Identify failure modes (missed documents, insufficient evidence)
- Debug reasoning chains with perfect record of tool calls

## When to Use

Apply OpenResearcher when:
- Reproducibility is critical (academic research, verification)
- Cost is a constraint (scaling reasoning across many queries)
- Offline operation is required (no internet access)
- Reasoning chains must be auditable

Less suitable for:
- Real-time current-events reasoning (corpus is static)
- Domains with rapidly evolving information
- Tasks requiring hyperlink traversal beyond merged corpus
