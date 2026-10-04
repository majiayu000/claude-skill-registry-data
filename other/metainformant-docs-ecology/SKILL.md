---
name: metainformant-docs-ecology
description: METAINFORMANT rules for directory docs/ecology. Use when editing, adding tests, or reviewing code under this path. Read the linked AGENTS.md first; use uv only, write outputs to output/, real implementations.
---

# METAINFORMANT — `docs/ecology`

Before editing files in this subtree:

- Read [`AGENTS.md`](../../../docs/ecology/AGENTS.md) for this folder (canonical technical context).
- Optional overview: [`README.md`](../../../docs/ecology/README.md).
- Global rules: [`CLAUDE.md`](../../../CLAUDE.md) at repo root (uv, `output/`, `.tmp/`, real implementations).
- Testing policy: [`docs/REAL_IMPLEMENTATION_POLICY.md`](../../../docs/REAL_IMPLEMENTATION_POLICY.md).
- Use `metainformant.core.io` for file I/O and `metainformant.core.utils.logging` for logs.

Keep changes scoped; match existing patterns in this directory.
