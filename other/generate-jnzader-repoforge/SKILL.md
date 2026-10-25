---
name: start-generation
description: >
  This skill covers the generation routes for starting, streaming, canceling, downloading, and previewing.
  Trigger: When generating content.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# start-generation

This skill covers the generation routes for starting, streaming, canceling, downloading, and previewing.

**Trigger**: When generating content.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Start generation | `start_generation()` |
| Stream generation | `stream_generation()` |

## Critical Patterns (Summary)
- **Start Generation**: Initiates the generation process.
- **Stream Generation**: Streams the ongoing generation process.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Start Generation

Initiates the generation process by calling the `start_generation` function.

```python
from apps.server.app.routes.generate import start_generation

result = start_generation(data)
```

### Stream Generation

Streams the ongoing generation process using the `stream_generation` function.

```python
from apps.server.app.routes.generate import stream_generation

for chunk in stream_generation(generation_id):
    process_chunk(chunk)
```

## When to Use

- When a user requests to start a new generation task.
- When streaming updates for a long-running generation process.

## Commands

```bash
docker-compose up
python apps/server/app/main.py
```

## Anti-Patterns

### Don't: Start without validation

Starting a generation without validating input can lead to errors and unexpected behavior.

```python
# BAD
start_generation(None)
```
<!-- L3:END -->