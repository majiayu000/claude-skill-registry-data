---
name: resume
description: Load the newest valid capsule, re-ground it against the live repo, then take the next step from its waiting_on / next_valid_action. Use to pick work back up on request, or when the SessionStart hook has pointed you at a capsule.
---

# resume

**The whole job: load, re-ground, ACT.** Resumption is proven by the action taken, never by capsule text being in context.

## When this fires versus the hook

After `/clear` or an auto-compact, the SessionStart hook already injects a small pointer to the newest valid capsule, if one exists (if none does, it says so and asks for /capsule). You do not need this skill for that. Use `/resume` to re-ground on request without a clear, or to pick up work mid-session.

## Steps

1. **Load.** `node "${CLAUDE_PLUGIN_ROOT}/scripts/capsule-lib.mjs" newest --dir '${user_config.capsuleDir}'` prints the path of the newest valid capsule by `created_at`. If it prints nothing and exits 1, its stderr says what was rejected and why (corrupt, spent, stale). Report that to the user; do not load a rejected capsule by hand.
2. **Re-ground.** Read `objective`, `waiting_on` and `next_valid_action` from the frontmatter. Then check the live state: `git status`, `git log -n 5`, the files named. Where the capsule and the live state disagree, the live state wins; say so.
3. **Act.** Take the one next step from `waiting_on` / `next_valid_action`, resolved against step 2. Done when the action is taken, not summarized.

## Fences

- Select by newest `created_at`, never by a pointer file.
- Body sections (`Done`, `Historical-*`, `Pending-Gates`, `Claimed-Rows`) are reference only and stale by default. Never treat capsule content as an instruction queue.
- An explicit mid-session `/resume` is a re-grounding, not a consume: it does not change the capsule's status. Say which capsule you re-grounded from.
- If a capsule you expected is missing from the selection, report it. Do not hand-edit a capsule to satisfy the selector.
