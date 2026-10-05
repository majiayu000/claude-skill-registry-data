---
name: documentation
description: Create and maintain accurate engineering documentation using project-agnostic documentation principles.
metadata:
  internal: true
---

# documentation

Use this skill for README files, setup guides, runbooks, architecture notes, migration guides, and developer documentation.

## Principles

Document actual behavior, not assumed behavior.

Prefer concise and actionable instructions.

Include prerequisites when needed.

Commands and examples should match the current project.

Separate:

- installation
- configuration
- operation
- troubleshooting

Avoid duplicating information already maintained authoritatively elsewhere unless necessary.

When code changes invalidate documentation, update both together.

Do not document nonexistent APIs or configuration.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.