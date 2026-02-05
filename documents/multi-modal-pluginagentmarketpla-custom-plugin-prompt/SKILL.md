---
name: multi-modal
description: Multi-modal prompting with vision, audio, and document understanding
sasmp_version: "1.3.0"
bonded_agent: 07-advanced-techniques-agent
bond_type: PRIMARY_BOND
---

# Multi-Modal Prompting Skill

**Bonded to:** `advanced-techniques-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:multi-modal")
```

---

## Parameter Schema

```yaml
parameters:
  modality:
    type: enum
    values: [vision, document, audio, video]
    required: true

  task_type:
    type: enum
    values: [analysis, extraction, generation, qa]
    default: analysis

  detail_level:
    type: enum
    values: [low, medium, high]
    default: medium
```

---

## Vision Prompting

### Image Analysis Template

```markdown
Analyze this image and provide:
1. Main subjects and objects
2. Actions or activities
3. Setting and context
4. Notable details
5. Overall interpretation

Be specific and descriptive.
```

### Visual Q&A Pattern

```markdown
Look at the image carefully.

Question: {question}

Provide a detailed answer based only on what you can see in the image.
```

### Chart/Graph Analysis

```markdown
Analyze this chart/graph:
1. Type of visualization
2. Axes and labels
3. Key data points
4. Trends or patterns
5. Main insights
6. Limitations or caveats
```

---

## Document Processing

### PDF Extraction

```markdown
Extract the following from this document:
- Title and headers
- Key information: {fields}
- Tables (if any)
- Important dates/numbers

Output as structured JSON.
```

### Form/Invoice Processing

```yaml
extraction_schema:
  document_type: "invoice|form|contract"
  fields:
    - name: vendor
      type: string
    - name: date
      type: date
    - name: total
      type: currency
    - name: line_items
      type: array
```

---

## Audio Integration

### Transcription Enhancement

```markdown
Transcribe and enhance:
1. Accurate transcription
2. Speaker identification
3. Timestamps for key points
4. Summary of main topics
5. Action items (if applicable)
```

---

## Best Practices

```yaml
best_practices:
  image_prompts:
    - Be specific about what to look for
    - Request structured output
    - Ask for confidence levels

  document_prompts:
    - Define extraction schema
    - Handle multi-page documents
    - Validate extracted data

  audio_prompts:
    - Specify language if known
    - Request speaker diarization
    - Ask for timestamps
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Hallucinated details | Over-interpretation | Ask for visible-only info |
| Missed text in images | Low resolution | Request higher detail |
| Wrong document parsing | Complex layout | Break into sections |
| Inaccurate transcription | Audio quality | Acknowledge limitations |

---

## References

See: GPT-4V documentation, Claude Vision Guide
