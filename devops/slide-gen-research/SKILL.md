---
name: slide-gen-research
description: "Autonomous web research for presentation topics using Claude Agent SDK. Conducts multi-step research, extracts insights, and manages citations."
version: "2.0.0"
author: "davistroy"
---

# Research Skill

Conducts comprehensive autonomous research on any topic using Claude Agent SDK with web search capabilities.

## Capabilities

- **Autonomous Research**: Multi-step web search and content extraction
- **Insight Extraction**: AI-powered analysis of research sources
- **Citation Management**: Automatic source tracking and formatting
- **Multi-Presentation Detection**: Identifies when topic should split into multiple presentations

## Usage

### Via CLI
```bash
python -m plugin.cli research "Rochester 2GC Carburetor Rebuild" --output research.json
```

### Via Python

```python
from plugin.skills.research.research_skill import ResearchSkill

skill = ResearchSkill(config)
result = skill.execute({
    "topic": "AI in Healthcare",
    "depth": "comprehensive",
    "max_sources": 20
})
```

## Input Parameters

| Parameter   | Type   | Required | Default    | Description                                              |
|-------------|--------|----------|------------|----------------------------------------------------------|
| topic       | string | Yes      | -          | Research topic                                           |
| depth       | string | No       | "standard" | Research depth: "quick", "standard", "comprehensive"     |
| max_sources | int    | No       | 10         | Maximum sources to gather                                |
| audience    | string | No       | "general"  | Target audience for content                              |

## Output Format

```json
{
  "topic": "string",
  "sources": [
    {
      "url": "string",
      "title": "string",
      "content": "string",
      "relevance_score": 0.95
    }
  ],
  "insights": [
    {
      "key_point": "string",
      "supporting_evidence": ["string"],
      "citations": ["string"]
    }
  ],
  "suggested_presentations": [
    {
      "title": "string",
      "audience": "string",
      "focus": "string"
    }
  ]
}
```

## Dependencies

- Claude Agent SDK
- ANTHROPIC_API_KEY environment variable

## Examples

### Basic Research

```bash
python -m plugin.cli research "Machine Learning Basics"
```

### Comprehensive Research with Custom Output

```bash
python -m plugin.cli research "Quantum Computing Applications" \
  --depth comprehensive \
  --max-sources 25 \
  --output quantum-research.json
```

### Research for Specific Audience

```bash
python -m plugin.cli research "Cloud Architecture" \
  --audience "C-level executives" \
  --depth quick
```
