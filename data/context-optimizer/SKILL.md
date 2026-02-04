---
name: context-optimizer
description: "Format and structure data files for optimal Claude reasoning and extraction. Use when: (1) Preparing documents/data for Claude analysis, (2) User asks to 'optimize context' or 'format for Claude', (3) Structuring multi-document corpora, (4) Improving LLM retrieval/reasoning over files, (5) Converting data between formats for Claude consumption, (6) User mentions 'lost in the middle' or context window issues. Supports XML, JSON, YAML, CSV, and markdown."
---

# Context Optimizer

Optimize data file structure and formatting for Claude's reasoning and information extraction.

## Core Principle

Claude's attention follows a **recency gradient**: strongest at context boundaries (start/end), weakest in the middle. Optimization strategy:

1. **Position** - Where content appears matters more than format choice
2. **Structure** - Explicit delimiters enable selective retrieval
3. **Metadata** - Source attribution enables grounding in evidence

## Quick Reference

| Content Type | Optimal Position | Recommended Format |
|--------------|------------------|-------------------|
| Reference documents | **TOP** of context | XML with metadata |
| Instructions | After documents | Markdown/plain text |
| Examples | Between docs & instructions | XML with `<examples>` |
| Query/task | **END** of context | Plain text |
| State/status data | Any | JSON |
| Progress notes | Any | Unstructured text |
| Tabular data | TOP | CSV or markdown tables |

## Workflow

### Step 1: Classify Content

Determine content type and select format:

**Structured data** (schemas, records, API responses) → JSON
**Multi-document corpus** (reports, research, contracts) → XML with metadata
**Tabular data** (metrics, comparisons) → CSV or markdown tables
**Configuration** (settings, parameters) → YAML
**Narrative/progress** → Unstructured markdown

### Step 2: Apply Positioning Rule

```
┌─────────────────────────────────────┐
│  DOCUMENTS/DATA (position: TOP)    │  ← Strongest attention
├─────────────────────────────────────┤
│  EXAMPLES (if applicable)          │
├─────────────────────────────────────┤
│  INSTRUCTIONS                      │
├─────────────────────────────────────┤
│  QUERY/TASK (position: END)        │  ← Strongest attention
└─────────────────────────────────────┘
```

Placing queries at the end improves response quality by up to 30%.

### Step 3: Structure Documents

For multi-document contexts, use the standard wrapper pattern:

```xml
<documents>
  <document index="1" priority="primary">
    <source>filename.pdf</source>
    <type>financial_report</type>
    <content>
      {{DOCUMENT_CONTENT}}
    </content>
  </document>
</documents>
```

Always include:
- `index` - For unambiguous reference
- `source` - For citation/attribution
- `type` - For semantic filtering

See [references/format-patterns.md](references/format-patterns.md) for complete templates.

### Step 4: Add Retrieval Instructions

For long documents, add explicit grounding instructions:

```
Find quotes from the documents that are relevant to [TASK].
Place these in <quotes> tags with document index references.
Then, based on these quotes, [PERFORM ANALYSIS].
```

This helps Claude cut through noise and ground responses in evidence.

## Format Selection Guide

### When to Use XML

- Multi-document corpora requiring source attribution
- Content with hierarchical structure
- When parseability of output matters
- Combining with chain-of-thought (`<thinking>`, `<answer>`)

### When to Use JSON

- State tracking (test results, task status)
- API request/response data
- When schema enforcement is needed
- Structured output requirements

### When to Use Markdown Tables

- Comparisons and rankings
- Tabular data under ~50 rows
- When human readability matters

### When to Use Plain Text

- Instructions and queries
- Progress notes and narrative
- Simple, single-purpose content

## Critical Rules

1. **Never bury instructions in data** - Instructions surrounded by data get attention-diluted
2. **Reference documents explicitly** - Avoid "this document"; use `document index="3"` 
3. **Use consistent tag names** - Same vocabulary throughout; reference by name in instructions
4. **Nest semantically** - `<outer><inner></inner></outer>` for hierarchical content
5. **Include source attribution** - Every document wrapper needs `<source>`

## Common Pitfalls

See [references/pitfalls.md](references/pitfalls.md) for detailed mitigations.

| Pitfall | Quick Fix |
|---------|-----------|
| Lost in the middle | Put critical info at START or END |
| Ambiguous references | Use explicit index numbers |
| Context overflow | Pre-calculate tokens; split strategically |
| Format mismatch | Match structure complexity to data complexity |

## Transformation Script

For automated restructuring, use the transform script:

```bash
python scripts/transform_context.py input.json --format xml --output optimized.xml
python scripts/transform_context.py input.csv --format xml --add-metadata --output optimized.xml
```

See script help for all options: `python scripts/transform_context.py --help`
