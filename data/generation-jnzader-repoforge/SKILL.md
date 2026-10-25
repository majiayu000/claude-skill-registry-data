---
name: add-generation-event
description: >
  This skill covers the creation and management of Generation and GenerationEvent ORM models.
  Trigger: When working with generation data in the backend.
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
# add-generation-event

This skill covers the creation and management of Generation and GenerationEvent ORM models.

**Trigger**: When working with generation data in the backend.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Create a Generation | `create-generation` |
| Log a GenerationEvent | `log-generation-event` |

## Critical Patterns (Summary)
- **Create a Generation**: Use the Generation model to create new generation records.
- **Log a GenerationEvent**: Utilize the GenerationEvent model to log events related to generations.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Create a Generation

This pattern demonstrates how to create a new Generation record using the Generation model.

```python
from apps.server.app.models.generation import Generation
from uuid import uuid4
from datetime import datetime

new_generation = Generation(
    id=uuid4(),
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
```

### Log a GenerationEvent

This pattern shows how to log a GenerationEvent related to a specific Generation.

```python
from apps.server.app.models.generation import GenerationEvent
from uuid import uuid4
from datetime import datetime

event = GenerationEvent(
    id=uuid4(),
    generation_id=new_generation.id,
    event_time=datetime.utcnow(),
    description="Generation created"
)
```

## When to Use

- When you need to create a new generation record in the database.
- When logging events related to a specific generation for tracking purposes.

## Commands

```bash
python -m apps.server.app.models.generation
```

## Anti-Patterns

### Don't: Create Generation without Validation

Creating a Generation without proper validation can lead to data integrity issues.

```python
# BAD
new_generation = Generation(id=None)  # Missing required fields
```
<!-- L3:END -->