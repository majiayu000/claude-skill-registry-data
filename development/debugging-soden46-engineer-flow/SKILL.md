---
name: debugging
description: Diagnose defects systematically using evidence-driven, technology-agnostic debugging practices.
metadata:
  internal: true
---

# debugging

Use this skill for failures, exceptions, incorrect behavior, intermittent bugs, and root-cause analysis.

## Principles

Reproduce before changing code when practical.

Separate:

- symptom
- trigger
- root cause

Collect evidence from relevant:

- errors
- logs
- inputs
- state
- recent changes
- traces
- database behavior
- network behavior

Reduce the problem to the smallest useful reproduction.

Avoid broad speculative changes.

Once root cause is identified:

1. make the smallest correct fix
2. add regression protection where useful
3. verify nearby behavior
4. remove temporary debugging instrumentation

Do not hide failures merely by suppressing exceptions or logs.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.