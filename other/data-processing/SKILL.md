---
name: data-processing
description: Process, transform, import, export, and handle large datasets using bounded and reliable technology-agnostic patterns.
metadata:
  internal: true
---

# data-processing

Use this skill for imports, exports, transformations, batch processing, files, large datasets, and data pipelines.

## Principles

Make data boundaries explicit.

Validate external data before relying on it.

For large workloads prefer bounded processing such as:

- streaming
- chunking
- pagination
- iterators
- batches

Avoid loading unbounded datasets into memory.

Define behavior for:

- malformed records
- partial failure
- retries
- duplicates
- ordering
- checkpointing
- resumability

Keep transformation logic separate from transport/storage concerns where useful.

For destructive or bulk operations, consider dry-run or preview mechanisms when appropriate.

Verify record counts and important invariants after processing.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.