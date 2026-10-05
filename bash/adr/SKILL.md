---
name: adr
description: Never lose the reasoning behind an architecture decision again. Use when recording or revisiting an Architecture Decision Record — creating a numbered ADR, transitioning its status (Proposed, Accepted, Deprecated, Superseded), or regenerating the index. Auto-numbers, fills the template, and rebuilds the index for you, adapting to any repo via config or auto-detection.
license: MIT
---

# ADR Workflow

Record and manage Architecture Decision Records.

## Resolve configuration first

Run the index helper in read mode to learn the ADR directory and current records:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/adr-index.mjs"
```

This prints the current index table (using `chronicle.config.json` if present, else auto-detected `docs/adr` / `adr/`). The next ADR number is `max(existing) + 1`.

## Create a new ADR

1. Determine the next number from the index output above.
2. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md`.
3. Fill `{{NUMBER}}`, `{{TITLE}}`, `{{DATE}}` (today, from the user/environment — never guess a random date).
4. Write to `<adr.dir>/<NNNN>-<kebab-title>.md` (zero-padded to `numberWidth`).
5. Regenerate the index:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/adr-index.mjs" --write
```

## Transition status

Edit the ADR's frontmatter `status:` (and the `## Status` section) to one of: Proposed, Accepted, Deprecated, Superseded, Rejected. When superseding, add `Superseded by ADR-NNNN` and link both directions. Then re-run `adr-index.mjs --write`.

## Rules

- Numbers only increase; never reuse or renumber.
- One decision per ADR.
- Write the ADR *before* or *as* the decision is made, not long after.
- Always regenerate the index after any change.
