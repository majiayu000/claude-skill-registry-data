---
name: auto-learn
version: 1.0.0
description: Autonomous web-based self-learning engine. Detects knowledge gaps, searches the web, reads, verifies, synthesizes, and stores learnings. Triggers automatically when confidence is low, evidence is thin, or a concept is unfamiliar. The brain that teaches itself.
---

# Auto-Learn — Autonomous Self-Learning Engine

> **"不知道 → 自己查 → 自己学 → 自己记住。不等用户教。"**

## Core Loop

```
Detect gap → Search → Read → Verify → Synthesize → Store
     ↑                                                    │
     └──────────── continuous improvement ────────────────┘
```

## Trigger: Knowledge Gap Detection

Auto-learn fires when any of:

| Signal | Meaning | Example |
|--------|---------|---------|
| **Confidence LOW** | Brain is guessing, not knowing | "I think this API works like..." |
| **No evidence** | Making a claim without a source | "This library is the fastest" without data |
| **Unfamiliar concept** | First time encountering a tool/term | User mentions a new framework |
| **Version uncertainty** | Might be outdated knowledge | "This changed in v3... right?" |
| **User challenge** | User pushes back on a claim | "Are you sure about that?" |
| **Trending topic** | Something new in the last 6 months | Recent releases, new standards |

## Process

### Step 1: Detect & Formulate
Turn the knowledge gap into 2-3 search queries:
```
Gap: "Not sure about the current state of X"
Query 1: "X latest version 2026"
Query 2: "X vs alternatives comparison 2026"
Query 3: "X common pitfalls 2026"
```

### Step 2: Search & Fetch (parallel)
```
WebSearch(query1) ─┐
WebSearch(query2) ─┼── parallel ──→ Fetch top 1-2 results each
WebSearch(query3) ─┘
```

### Step 3: Cross-Verify
Don't trust a single source. Check:
- Do 2+ independent sources agree?
- Is the source authoritative? (official docs > blog > forum)
- Is the information recent? (within 6 months for fast-moving tech)
- Any contradictions between sources?

### Step 4: Synthesize
Write a 3-5 sentence summary:
```
Topic: [what was learned]
Key facts: [3-5 bullet points with source references]
Certainty: HIGH / MEDIUM / LOW
Applicable to: [what problems does this knowledge solve?]
```

### Step 5: Store
```
memory-db.ps1 store
  - EntityName: [topic slug]
  - EntityType: "learning"
  - Content: [synthesized summary + sources]
  - Score: 0.6 (learned but not yet applied; will increase when used)
```

## When NOT to Use

| Skip | Reason |
|------|--------|
| Standard language syntax | Training data is sufficient |
| Well-known stable libraries | No version uncertainty |
| Opinion/preference questions | Not a knowledge gap |
| Already stored with score ≥0.8 | No need to re-learn |

## Integration

- **orchestrator**: L2+ tasks with knowledge gaps → orchestrator routes to auto-learn before execution
- **context7-proactive**: Auto-learn finds concept → context7 dives into API specifics
- **memory-lora**: All learnings stored with sources, cross-referenced
- **second-brain**: Brain 2 verifies auto-learn's synthesis for accuracy
- **thinking-dimensions**: Auto-learn findings → D1 (perspective matrix) enriched with latest data

## Anti-Patterns

- Learning for learning's sake (must serve the current task)
- Trusting the first search result (cross-verify required)
- Storing without verifying (false knowledge is worse than no knowledge)
- Re-learning what memory-lora already has at score ≥0.8

## Success Metric

Number of times a stored learning is RECALLED and APPLIED in a later task. A learning that's stored but never used = wasted token budget. A learning that prevents one wrong answer = 10x ROI.
