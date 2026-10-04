---
name: film-completeness
description: Audit the final feature-film project for required control artifacts, approved sequences, coverage, continuity, editorial, generation, master, and release evidence.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Film Completeness

## Use

1. Read `../../references/FILM_COMPLETENESS_AUDIT.md`.
2. Read the current durable project state before you make a decision.
3. Work on the smallest valid `SEQ-###`, job frontier, or global gate.
4. Use `../../scripts/completeness_audit.py` for deterministic state changes or checks.
5. Save the result before you continue.
6. If the result blocks progress, keep the current Todo target blocked until the problem is fixed.

## Rules

- Do not load the full feature-film state when a sequence shard is sufficient.
- Do not infer completion from file existence alone.
- Do not hide an exception. Record the exception and the reason.
- Preserve stable IDs and project-relative paths.
- Use global checks only when the check needs global evidence.

## Done

The requested feature-scale state is written, validated, and traceable from durable project files.
