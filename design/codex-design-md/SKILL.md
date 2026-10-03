---
name: codex-design-md
description: Use for DESIGN.md visual identity contracts; author, scaffold, lint, diff, and export design contracts with the upstream spec and CLI.
load_priority: on-demand
---

## TL;DR
Load when a project needs a durable design contract, not just one-off styling advice. This skill adds a structured `DESIGN.md` layer with typed tokens, ordered rationale sections, and validation/export tooling. No upstream source checkout is required for the default workflow.

## Activation
1. Activate when the user mentions `DESIGN.md`, design tokens, Tailwind theme export, DTCG export, or a reusable visual identity contract.
2. Activate on `$design-md`, "create a design contract", "lint DESIGN.md", or "export design tokens".
3. Load alongside `codex-frontend-design` when UI work needs both creative direction and a durable source-of-truth file.
4. Auto-load when `frontend-specialist` is active and the task needs persistent design-system artifacts.

## Decision Flow
1. If no `DESIGN.md` exists, scaffold one first with `scripts/design_contract.py scaffold`.
2. Use `references/spec-essentials.md` to keep tokens and sections inside the canonical format.
3. Validate with `scripts/design_contract.py lint` before relying on the contract.
4. Compare revisions with `scripts/design_contract.py diff` when the contract changes.
5. Export to Tailwind or DTCG with `scripts/design_contract.py export` only after lint is clean.

## Rules
- Treat `DESIGN.md` as the durable source of truth for visual identity; do not scatter token decisions across ad-hoc prompts.
- Keep the file canonical: YAML tokens first, then markdown sections in spec order.
- Use exact token values. Do not write vague prose where a token should exist.
- Pair this skill with `codex-frontend-design` (references/ for OKLCH palettes, typography, layouts, motion) for the visual vocabulary.
- Prefer validation and diff evidence over aesthetic claims.

## Reference Files
- `references/spec-essentials.md`
- `references/cli-commands.md`
- `references/integration-playbook.md`
