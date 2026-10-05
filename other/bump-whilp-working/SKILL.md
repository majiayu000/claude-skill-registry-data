---
name: bump
description: Check for new releases of ah and cosmic, update dependency pins, and commit changes.
---

# Bump

You are checking for new releases of dependencies and updating their version pins.

## Environment

- `WORK_REPO` is set to `whilp/working`.
- The repo is cloned at `o/repo/`.
- You have tools: `get_latest_release`, `update_dep`, `bash`.

## Dependencies

| dep | repo | asset name | file |
|---|---|---|---|
| ah | whilp/ah | ah | deps/ah.mk |
| cosmic | whilp/cosmic | cosmic-lua | deps/cosmic.mk |

## Instructions

1. For each dependency (ah, cosmic):
   a. Read `o/repo/deps/<dep>.mk` to get the current URL and SHA.
   b. Extract the current tag from the URL (the path segment before the asset name).
   c. Run `get_latest_release` with the upstream repo and asset name.
   d. Parse the returned `tag=<tag> url=<url>` string.
   e. If the latest tag matches the current tag, skip this dependency.
   f. If the latest tag is newer, run `update_dep` with the dep name and new URL (let it compute the SHA).
2. If any dependencies were updated:
   a. Stage the changed `deps/*.mk` files: `git -C o/repo add deps/ah.mk deps/cosmic.mk`
   b. Commit: `git -C o/repo commit -m "bump: update dependencies"`
3. If no dependencies were updated, make no commits.

## Output

Write `o/bump/bump.json`:

```json
{
  "updated": [{"dep": "<name>", "old_tag": "<tag>", "new_tag": "<tag>", "url": "<url>"}],
  "skipped": [{"dep": "<name>", "tag": "<tag>"}]
}
```
