---
name: hermes-local-patches
description: >-
  Audit or maintain the narrow `~/.hermes/patches` replay layer now that repo-code
  customizations are preserved canonically on the local git branch instead of by
  top-level patch replay. Use for machine-local helper restores, emergency patch
  triage, or cleanup of stale replay artifacts.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Local Patches

This skill is now about the leftover replay layer, not the main preservation model.

## Core rule

Important repo-code customizations must live as commits on `local/studio-customizations`.

Do not treat these as canonical homes for repo code:
- dirty working tree
- `git stash`
- `~/.hermes/patches/*.patch`
- archived patch exports
- backup branches with no active merge path

`~/.hermes/patches/` is now for:
- machine-local non-repo helpers
- tiny emergency stopgaps with explicit justification
- archived recovery material kept for reference

## Current live role on this machine

Top-level `~/.hermes/patches/` may still be consulted by the local post-merge hook.
That does not make it the source of truth for repo behavior.

Steady-state goal:
- repo-code customizations survive because they are committed on `local/studio-customizations`
- top-level replay artifacts are minimal
- archived patch exports stay cold/inert unless deliberately inspected

## When to use this skill

Use it when you need to:
- inspect or narrow the live top-level replay set
- preserve a machine-local helper outside the repo
- retire a stale `.patch` or `.new` artifact
- explain why a hook restored something unexpected
- do emergency/manual recovery from an archived patch

Do not use this skill as the default answer to “how do we preserve local repo changes across update?”
For that, use the branch workflow and the update checklist.

## Canonical preservation model for repo code

- `main` = clean upstream-tracking branch
- `local/studio-customizations` = canonical local customization branch
- durable repo changes should be made there or cherry-picked there promptly
- update flow is: update `main`, merge `main` into `local/studio-customizations`, verify, commit any follow-up fixes

## What is still legitimate in `~/.hermes/patches/`

Good uses:
- `parakeet_mlx_stt.py.new` restoring `~/.hermes/scripts/parakeet_mlx_stt.py`
- archived stash exports kept under `~/.hermes/patches/archive/`
- one-off emergency patch files that are clearly labeled and time-bounded

Bad uses:
- long-lived Telegram/gateway repo features that matter operationally
- keeping the “real” version of repo code only as a top-level patch
- depending on patch replay instead of committing durable repo work

## Practical audit checklist

1. Inspect the top-level live set:
```bash
find ~/.hermes/patches -maxdepth 1 -type f | sort
```

2. Classify each top-level artifact:
- machine-local helper -> okay to keep
- emergency bridge -> keep only with explicit note and exit plan
- repo feature that matters -> promote to `local/studio-customizations`
- stale artifact -> archive or remove from the top level

3. Confirm archives are inert reference material, not active replay:
```bash
find ~/.hermes/patches/archive -maxdepth 2 -type f | sort
```

4. If a repo-code patch still matters, promote it into git history instead of refreshing the patch again.

## Archive/stash rules

- archives and stashes are safety/reference layers only
- do not auto-replay them after update
- if an archived repo-code behavior still matters, move it into `local/studio-customizations`
- if it does not matter, leave it archived or retire it; do not resurrect it by habit

## Troubleshooting

If behavior disappeared after update:
1. check whether it exists on `local/studio-customizations`
2. check whether `main` was merged into that branch correctly
3. verify the behavior from the branch-integrated tree
4. only then inspect emergency patch/archive material

If a top-level patch is still required for a repo feature, the migration is incomplete.
