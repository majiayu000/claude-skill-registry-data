---
name: docs
description: >-
  v0.1.0 — Write or update user-facing project documentation after a
  programming change when documentation is part of the requested workflow.
---

# Project documentation

Document the behavior delivered by the programming task after its code-writing
phase is complete. Update the existing documentation surface that owns the
changed behavior; create a root `README.md` only when the project has no more
appropriate documentation entrypoint.

Cover the information a user or maintainer needs to use the change:

- what the program or changed capability does;
- its public entrypoint, command, or API surface;
- supported inputs, options, and representative usage;
- configuration, setup, or migration steps introduced by the change; and
- important constraints or failure behavior that are not obvious from usage.

Keep documentation consistent with the implemented interface. Avoid copying
internal implementation details that do not affect users, and do not invent
commands or guarantees that the code does not provide. Function-level comments
and docstrings remain owned by any separately selected commenting skill.
