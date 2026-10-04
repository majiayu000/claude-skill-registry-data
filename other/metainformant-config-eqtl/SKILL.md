---
name: metainformant-config-eqtl
description: METAINFORMANT rules for directory config/eqtl. Use when editing, adding tests, or reviewing code under this path. Read the linked AGENTS.md first; use uv only, write outputs to output/, real implementations.
---

# METAINFORMANT — `config/eqtl`

Before editing files in this subtree:

- Read [`AGENTS.md`](../../../config/eqtl/AGENTS.md) for this folder (canonical technical context).
- Optional overview: [`README.md`](../../../config/eqtl/README.md).
- Global rules: [`CLAUDE.md`](../../../CLAUDE.md) at repo root (uv, `output/`, `.tmp/`, real implementations).
- Testing policy: [`docs/REAL_IMPLEMENTATION_POLICY.md`](../../../docs/REAL_IMPLEMENTATION_POLICY.md).
- Use `metainformant.core.io` for file I/O and `metainformant.core.utils.logging` for logs.

Keep changes scoped; match existing patterns in this directory.
