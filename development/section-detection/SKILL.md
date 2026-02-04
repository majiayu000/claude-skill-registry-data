---
name: section-detection
description: Detect clinical note sections (HPI, ROS, Assessment, Plan) using regex patterns and LLM topic segmentation. Generates ToC with accurate byte offsets.
---

# Section Detection Skill

## Overview

Detects sections in clinical notes using hybrid approach: regex for explicit headers + LLM for inferred sections. Generates navigable Table of Contents with precise offsets.

## When to Use

- Generate Table of Contents for clinical notes
- Detect section boundaries for navigation
- Identify explicit and inferred sections

## Installation

**IMPORTANT**: This skill has its own isolated virtual environment (`.venv`) managed by `uv`. Do NOT use system Python.

Initialize the skill's environment:
```bash
# From the skill directory
cd .agent/skills/section-detection
uv sync  # Creates .venv (no external dependencies, uses Python stdlib)
```

## Usage

**CRITICAL**: Always use `uv run` to execute code with this skill's `.venv`, NOT system Python.

```python
# From .agent/skills/section-detection/ directory
# Run with: uv run python -c "..."
from section_detection import SectionDetector

detector = SectionDetector(ollama_client)

sections = detector.detect_sections(clinical_note_text)

for section in sections:
    print(f"{section['title']}: {section['start_offset']}-{section['end_offset']}")
    print(f"  Explicit: {section['is_explicit']}, Confidence: {section['confidence']}")
```

## Implementation

See `section_detection.py`.
