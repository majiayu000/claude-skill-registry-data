---
name: claim-extraction
description: Guides rigorous evidence extraction from papers. Use when reviewing literature to ensure proper provenance tracking.
user-invocable: true
---

# Claim Extraction Guidelines

Extract evidence with full provenance from research papers.

## Target: 2-5 Claims Per Paper

If averaging less than 2 claims per paper, re-read. You're missing evidence.

## What to Extract

### From Results Section (Richest)
- Quantitative findings ("X increased by Y%")
- Comparative results ("A outperformed B")
- Statistical significance ("p < 0.05")

### From Methods Section
- Algorithmic claims ("uses penalty-based scoring")
- Parameter choices ("default k=5 optimal")
- Implementation details affecting reproducibility

### From Discussion Section
- Limitations acknowledged
- Comparisons to prior work
- Future directions

### From Introduction
- State-of-the-art claims
- Known gaps motivating the study

## Claim Structure

```json
{
  "claim_text": "Tool-X achieves O(n) time complexity for data processing",
  "supports_rq": ["RQ1", "RQ2"],
  "rq_context": "Addresses RQ1 by characterizing efficiency; supports RQ2 baseline",
  "importance": "Establishes performance expectations for analysis tools",
  "evidence": {
    "source_doi": "10.1093/nar/gks596",
    "source_type": "journal",
    "quote": "The algorithm achieves linear time complexity O(n) where n is the input data size",
    "page": 7,
    "section": "Results",
    "context_surrounding_text": "We benchmarked Tool-X on datasets ranging from 1KB to 10GB. The algorithm achieves linear time complexity...",
    "confidence": 0.95,
    "confidence_justification": "Explicit quantitative statement with empirical validation in peer-reviewed publication"
  }
}
```

## Required Fields

Every claim MUST have:
- `source_doi` - Paper DOI
- `quote` - EXACT text (not paraphrased)
- `page` or `section` - Location in source
- `confidence` - 0.0-1.0 score
- `confidence_justification` - Why this confidence

## Confidence Guidelines

| Score | Meaning | Example |
|-------|---------|---------|
| 0.9-1.0 | Explicit quantitative with validation | "achieved 95% accuracy (n=1000, p<0.001)" |
| 0.7-0.9 | Clear statement with evidence | "significantly outperformed baseline" |
| 0.5-0.7 | Reasonable inference | "suggests improved performance" |
| 0.3-0.5 | Weak evidence, needs corroboration | "may indicate..." |
| <0.3 | Speculation | Don't extract as claim |

## Handling Conflicts

When papers disagree:

```json
{
  "conflict": "Paper A claims X, Paper B claims Y",
  "investigation": {
    "paper_a_method": "Used dataset Z with parameters...",
    "paper_b_method": "Different dataset W with...",
    "root_cause": "Different experimental setups"
  },
  "resolution": "Both valid in their contexts",
  "confidence": 0.8
}
```

## Anti-Patterns

- **Paraphrased quotes**: Must be exact text
- **Missing DOIs**: Every claim needs source
- **Vague claims**: "Tool is good" (no specifics)
- **Unsupported confidence**: Score without justification
- **Single-source claims**: Try to corroborate

## Output Format

Save to `evidence_report.json`:
```json
{
  "papers_reviewed": 12,
  "rq_coverage": {
    "RQ1": {"status": "answered", "confidence": 0.9, "claims": [...]},
    "RQ2": {"status": "partial", "gaps": ["..."]}
  },
  "all_claims": [...],
  "conflicts_identified": [...],
  "new_rqs_proposed": [...]
}
```

**Extract rigorously. Cite exactly. Justify confidence.**
