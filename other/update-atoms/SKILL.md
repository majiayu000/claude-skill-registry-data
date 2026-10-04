---
name: update-atoms
description: >-
    Refresh plainworks' vendored shadcn atoms the canonical way — bump the shadcn CLI in the
    catalog, rerun registry:update for every locked atom, reconcile any upstream change through the
    deviation ladder (theme tokens → call sites → @plainworks/ui wrappers) instead of editing the
    atom, and rerun the gallery browser gate. Use when bumping the shadcn CLI, pulling upstream atom
    fixes, adding an atom, or when registry:validate reports a lock mismatch.
---

# Updating the vendored shadcn atoms

The atoms in `packages/elements/src/shadcn/` are **vendored** shadcn CLI output, **locked** by `shadcn.lock.json` (CLI version, style, per-atom hash). They are never hand-edited. This skill is the one way to change them. The model is in [`packages/elements/README.md`](../../../packages/elements/README.md) and the [Vendored atoms](../../copilot-instructions.md#vendored-atoms) baseline.

## Quick path

```bash
cd packages/elements
bun run registry:update $(node -p "Object.keys(require('./shadcn.lock.json').atoms).join(' ')")
bun run registry:validate
```

`registry:update` reruns the pipeline (shadcn CLI → compat transform → Biome safe fixes), relocks each atom, and runs `registry:codegen`. Pass one name to refresh a single atom.

## Step 1 — Bump the CLI (only when upgrading)

- Change the `shadcn` entry in the root `package.json` catalog, then run `bun install`.
- Read the shadcn changelog for the jump. Note removed props, renamed exports, and changed styles.
- Keep `components.json` on the same style unless you mean to change it; the lock records the style too.

## Step 2 — Refresh every atom

Run the quick path above. Refresh **all** locked atoms after a CLI bump — the lock stores one CLI version, so a partial refresh leaves it claiming a version some atoms weren't built with.

To add a new atom, run `bun run registry:add <atom>` instead. A name that already lives in `src/atoms/` is refused; a name lives in only one folder.

## Step 3 — Review the diff

Every change under `src/shadcn/` is now upstream's. Read it for:

- **API changes** that break consumers (props, exports, `data-*` attributes).
- **Styling changes** that move color, contrast, focus, radius, or target size.
- **New raw CSS variables** an atom reads; `src/theme-variables.test.ts` fails until the theme declares them.

## Step 4 — Reconcile on the deviation ladder

Never fix the fallout inside the atom. Use the lowest rung that fixes it:

| Rung | Fix here |
|---|---|
| **Theme** | `@plainworks/theme` tokens and rules — color, contrast, focus, radius, focus for keyboard stops an atom leaves unmarked. |
| **Call site** | Props, `className`, `role` at the one usage that needs it. |
| **`ui` wrapper** | A `@plainworks/ui` wrapper for reusable tones or behavior. |

Don't re-add a variant (a tone, size, or state) that upstream dropped or never shipped; that belongs in a `ui` wrapper. If upstream has a real bug, fix it at the lowest rung and note it for upstream reporting.

## Step 5 — Validate

```bash
bun run --filter @plainworks/elements registry:validate
bun run lint
turbo run typecheck build test --filter=@plainworks/elements...   # elements and its dependents
(cd apps/showcase && bun run e2e e2e/gallery.spec.ts)                  # gallery browser gate
```

The gallery gate checks contrast, visible focus, and reduced motion on real layout. Run the full showcase `e2e` too if `ui` wrappers or theme rules changed. See [`validate`](../validate/SKILL.md) for the rest of the gates.

Add a Changeset for `@plainworks/elements` (and any package you reconciled). Name the CLI version in it when you bumped it.

## Checklist

- [ ] Changes under `src/shadcn/` and `shadcn.lock.json` come only from `registry:update` / `registry:add`
- [ ] After a CLI bump, every locked atom was refreshed; the lock's `cli` matches the catalog pin
- [ ] Fallout fixed on the deviation ladder, not in an atom; no re-added non-upstream variants
- [ ] `registry:validate`, the scoped gates, and the gallery browser gate green; Changeset added

Per repo workflow, **create the branch and make edits only** — the maintainer commits and pushes.
