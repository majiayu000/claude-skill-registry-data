---
name: rhetoric
description: Structured reasoning and deliberation. Record thoughts, deliberate on decisions, review thinking patterns.
license: MIT
metadata:
  version: 2.0.0
  dependencies: python>=3.10, httpx, pydantic
---

# Rhetoric: The Reasoning Engine

> "The unexamined thought is not worth having."

## Overview

**Rhetoric** provides structured reasoning capabilities for complex problem-solving. It records thoughts with full revision tracking, orchestrates multi-model deliberation for decisions, and reviews thinking patterns to detect cognitive biases.

## Commands

### `think "<thought>" [--session-id <id>]`
Record a thought with structured metadata. Supports revision tracking and branching.

```bash
python3 scripts/rhetoric.py think "We should use a factory pattern here" --session-id project-123
```

**Output:**
```json
{
  "status": "success",
  "thought_id": "th-abc123",
  "session_id": "project-123",
  "thought_number": 3,
  "total_thoughts": 5
}
```

**Options:**
- `--session-id <id>`: Group thoughts into sessions
- `--revision-of <id>`: Mark as revision of previous thought
- `--branch-from <id>`: Create a branching thought path

### `deliberate "<question>" [--rounds <n>]`
Deliberate on a question through internal multi-perspective analysis.

```bash
python3 scripts/rhetoric.py deliberate "Should we use microservices or monolith?" --rounds 3
```

**Output:**
```json
{
  "status": "completed",
  "question": "Should we use microservices or monolith?",
  "rounds_completed": 3,
  "consensus": "Monolith recommended for MVP, with clear module boundaries for future extraction",
  "confidence": 0.85
}
```

**Options:**
- `--rounds <n>`: Number of deliberation rounds (1-5, default: 2)
- `--context <text>`: Additional context for deliberation
- `--debug`: Show internal deliberation details (hidden by default)

**Note:** Requires at least 2 configured model credentials. Returns clear error if insufficient.

### `review [--session-id <id>]`
Review thought history and detect patterns.

```bash
python3 scripts/rhetoric.py review --session-id project-123
```

**Output:**
```json
{
  "status": "success",
  "session_id": "project-123",
  "thought_count": 15,
  "patterns": {
    "revision_rate": 0.2,
    "branch_count": 2,
    "detected_issues": ["analysis_paralysis"]
  },
  "recommendations": ["Consider narrowing scope", "Make a decision to proceed"]
}
```

### `status`
Get current reasoning session status.

```bash
python3 scripts/rhetoric.py status
```

**Output:**
```json
{
  "active_sessions": 2,
  "total_thoughts": 45,
  "models_available": 3,
  "deliberation_ready": true,
  "last_activity": "2024-01-15T10:30:00Z"
}
```

## Thought Persistence

Thoughts are persisted with the following schema:

```json
{
  "id": "th-abc123",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "project-123",
  "content": "The thought content",
  "type": "analysis",
  "revision_of": null
}
```

Thoughts are stored in `thoughts.json` and retained indefinitely unless explicitly deleted.

## Deliberation

The `deliberate` command orchestrates multi-model debate internally:

1. **Minimum 2 models** required (validates credentials at startup)
2. **Maximum 5 rounds** of deliberation
3. **Convergence detection** when confidence exceeds 0.8
4. **Model names hidden** from output (opaque interface)

### Required Credentials

At least 2 of the following in `.env.local`:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
GOOGLE_CLOUD_API_KEY=AIza...
```

### Error Handling

```json
{"status": "error", "code": 4, "message": "Insufficient models for deliberation. Configure at least 2 of: OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY"}
```

## Configuration

### Environment Variables

Set in `.env.local`:

```bash
# Primary (at least 2 required for deliberation)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
GOOGLE_CLOUD_API_KEY=AIza...

# Optional
TAVILY_API_KEY=tvly-...  # Enhanced search in think
```

## Files

- `thoughts.json`: Thought history with full schema
- `deliberations/`: Deliberation transcripts (session-specific)
- `constitution.md`: Reasoning rules and guidelines
- `sessions/`: Session state files

## Backends

Rhetoric orchestrates these MCP servers internally (opaque to user):

- **sequential-thinking**: Structured thought recording
- **ai-counsel**: Multi-model deliberation
- **vibe-check**: Pattern detection and risk assessment

Backend details are hidden - you interact only through Rhetoric's unified interface.

## Synergies

Rhetoric optionally integrates with other Cognitive Construct skills:

- **→ Encyclopedia**: Fetch context during deliberation
- **→ Inland Empire**: Store significant decisions as memories
- **← Volition**: Complex actions can request deliberation first
