---
name: open-work
description: Inspect and optionally act on the current repository's OpenSpec changes and plan rows through one portable inventory and authority-gated workflow. Use when the user asks what work is open, invokes an open-work surface, wants a report of actionable work, or wants to archive, disposition, dispatch, or apply selected tracked work.
---

# Open Work

Produce one deterministic inventory, then act only through capabilities the current harness declares.
Accept one optional mode: `interactive` or `report`; reject other arguments. If the mode is absent,
default to `interactive`.

Before acquiring data, read these references completely:

1. [references/rendering.md](references/rendering.md) for source interpretation and exact output.
2. [references/capabilities.md](references/capabilities.md) for mode and capability behavior.
3. [references/actions.md](references/actions.md) only when interactive actions may be offered.

Use [references/acceptance.md](references/acceptance.md) when validating or changing this skill.

## Acquire one normalized snapshot

Resolve the producer root in this order:

1. An explicit `OPEN_WORK_ROOT` containing `bin/`.
2. This skill's adjacent `scripts/` directory.
3. Same-named resources on `PATH`.

The first two producers are required for a complete inventory. Invoke readable source through named
interpreters; executable bits are neither required nor permitted for packaged assets:

```bash
python3 "${OPEN_WORK_ROOT}/bin/open-items" --json
python3 "${OPEN_WORK_ROOT}/bin/triage-list-drafts" --json --include-approved
```

Both producers are Python; invoke each under the interpreter its shebang names. Running one under
`bash` does not merely fail — `bash` reads `import json` as ImageMagick's `import(1)`, emits
X-server errors, and still exits 0, so the caller cannot tell that garbage from a clean run.

Run each producer once. Treat every source independently: retain available sources and one bounded
warning for each unavailable source. Do not invent rows, counts, dependencies, dispositions, or progress.

## Render before acting

Normalize the producer results exactly as described in `references/rendering.md`. Render the full
report before offering or executing actions. The report is valid even when one or all sources are
unavailable.

In `report` mode, stop after rendering. In `interactive` mode, inspect the binding's declared
capabilities and follow `references/capabilities.md`. No response channel means render the report,
name the unavailable actions, and stop without mutation.

## Preserve authority

Offer only action classes with non-empty eligible sets. A current-invocation response must identify
known items and supported actions unambiguously. Cancellation, silence, or ambiguity grants no
authority. Execute confirmed actions only in the ordering and failure boundaries defined in
`references/actions.md`.

Never reimplement a missing workflow capability inline. Never perform Git commit, push, sync,
cross-repository mutation, or destructive cleanup merely because inventory was requested. Repository
instructions and the invoked workflow remain authoritative.
