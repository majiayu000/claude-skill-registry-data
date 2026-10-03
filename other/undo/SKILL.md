---
name: undo
description: "Reverts the last change(s) to a matter using git. Use when Mandy says 'undo', 'revert', 'go back', 'that was wrong', 'undo last change', or wants to reverse a recent action. Supports depth: '/undo chen 3' reverts last 3 changes."
---

# Undo

## Important
- Manual-only. Always confirm before reverting.
- MUST rebuild index.jsonl entry after revert (index is not reverted by git).

## Instructions

### Step 0: Resolve Matter

### Step 1: Parse Depth
Default: 1. Accept `/undo chen 3` for last 3 changes.

### Step 2: Show and Confirm
`git -C matters/ log -{depth} --oneline -- {id}/`
"This will undo: [list]. Continue?"

### Step 3: Revert
For depth=1, if HEAD only touched this matter: `git -C matters/ revert HEAD --no-edit`
If HEAD touched multiple matters: `git -C matters/ checkout HEAD~1 -- {id}/ && git -C matters/ add {id}/ && git -C matters/ commit -m "undo: {id} — Reverted last change"`
For depth>1: `git -C matters/ checkout HEAD~{depth} -- {id}/ && git -C matters/ add {id}/ && commit`

### Step 4: Rebuild Index
Read reverted `matter.json`. Recalculate all index fields. Update line in `matters/index.jsonl`. This is essential — the index was NOT reverted by git.

### Step 5: Commit and Confirm
Log the undo. Commit. "Undone. Use `/matter-status {name}` to verify."
