---
name: citation-extraction
description: Extract and validate citations with Jaccard overlap calculation. Ensures all claims have verifiable source evidence with ≥0.7 alignment threshold.
---

# Citation Extraction Skill

## Overview

Validates citations by calculating Jaccard overlap (intersection over union) between cited text and source passages. Enforces ≥0.7 threshold for quality.

## When to Use

- Validate citations in clinical summaries
- Calculate Jaccard overlap for Evaluator metrics
- Extract source text spans for claims

## Installation

**IMPORTANT**: This skill has its own isolated virtual environment (`.venv`) managed by `uv`. Do NOT use system Python.

Initialize the skill's environment:
```bash
# From the skill directory
cd .agent/skills/citation-extraction
uv sync  # Creates .venv (no external dependencies, uses Python stdlib)
```

## Usage

**CRITICAL**: Always use `uv run` to execute code with this skill's `.venv`, NOT system Python.

```python
# From .agent/skills/citation-extraction/ directory
# Run with: uv run python -c "..."
from citation_extraction import CitationExtractor

extractor = CitationExtractor()

# Validate citation
jaccard = extractor.calculate_jaccard_overlap(
    claim_text="Patient has hypertension",
    source_text="Patient diagnosed with hypertension 10 years ago"
)

if jaccard >= 0.7:
    print(f"Valid citation (Jaccard: {jaccard})")
```

## Implementation

See `citation_extraction.py`.
