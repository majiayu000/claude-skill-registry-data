---
name: docs-auto-sync
description: Automatically update repository documentation whenever code changes (add/edit/refactor) occur. Use when modifying source code, public APIs/contracts, rendering/interaction/data/compute logic, diagnostics, or build/release/CI flows so docs stay consistent without asking.
---

# Docs Auto Sync

## Overview
Keep documentation in sync with code changes by updating the required docs in the same change set. Default to automatic updates; only ask if a required detail is missing.

## Workflow
1. Classify the change scope.
- Identify layers touched (core/rendering/interaction/data/compute/api/diagnostics/ci/packaging).
- Note any contract, lifecycle, or budget changes (see `AGENTS.md`).

2. Choose docs to update.
- Use `references/doc-impact-matrix.md` to map change types to docs.
- If multiple layers are touched, add a short design note per `AGENTS.md`.
- For contract changes, add version notes and a migration note.

3. Update docs automatically.
- Apply edits in the same change set.
- Add a rationale to any new doc: why it belongs in chart-engine and not quant-lab.
- Keep cross-links and references consistent.

4. Validate before final response.
- Ensure doc DoD: cross-links updated, invariants/SLOs referenced, version notes added.
- Summarize which docs were updated and why.

## Resources
- `references/doc-impact-matrix.md` - change types and required docs.
