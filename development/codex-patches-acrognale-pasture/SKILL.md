---
name: codex-patches
description: Use this when updating the codex submodule or when patch files in codex-patches/ need to be added, regenerated, or repaired.
---

# Codex Patch Workflow

Use this skill whenever you touch the codex submodule (`codex/`) or the patch series in `codex-patches/`.

## Apply Patches After Submodule Update

1. Update the codex submodule to the target commit:

```bash
cd codex
git checkout <commit>
cd ..
```

2. Apply our patches:

```bash
scripts/apply_codex_patches.sh
```

If a patch fails, fix only that patch before moving on.

## Repairing a Broken Patch

General approach:

1. Rehydrate `codex/` to clean upstream before re‑diffing:

```bash
git archive codex-upstream/main | tar -x -C codex
```

2. Re‑apply the remaining patches that still work. Fix conflicts manually if needed.
3. Regenerate the broken patch by diffing the upstream file(s) against our modified version.

### Regenerating a Patch (stable diff style)

Prefer diffs against the upstream tree to reduce context drift. For the full example script, see `references/regen_patch_example.md`.

### Patch Hygiene

- Keep each patch focused on a single feature or concern.
- Avoid bundling unrelated changes into the same patch.
- Do not include upstream-only changes; patches should be fork-only deltas.

## Quick Smoke Test

After applying patches, run:

```bash
turbo lint
turbo typecheck
```
