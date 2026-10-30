---
name: shield-wall
description: Suki's shield wall for a linear stack. Each warrior's shield overlaps the one below it, and one voice orders the line. Use for autopilot-stack, "stack them, don't ship", "build the stack, I'll land it", or a queue of coupled or sequenced changes built and verified with full autonomy and delivered as one reviewed base-chained stack for the operator to land.
---

# Suki's shield wall

A shield wall holds because every shield rests on the one below it and only one warrior calls the line. If two warriors shift the wall at once, it breaks. You own the stack, never the landing. Hand the operator one linear stack of base-chained PRs to review and land.

`full-patrol` holds except for how verified work leaves. Each tick re-reads both skills from disk under the installed plugin, and this one wins where they differ.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **Run `full-patrol`'s owners, minus the landing.** Owners report STACK-READY in place of merge-ready. They never rebase onto another branch, trunk included. They never retarget, merge, or close a PR, and never arm auto-merge, because the root owns the chain's topology and the operator owns the landing. When an item depends on another, its owner branches from that item's branch, not from trunk.
2. **Give the topology one writer.** Owners push only their own branches and report each tip and its intended parent. Only you rebase or retarget a link, because two writers on one chain undo each other. Append each clean PR in dependency order, with its base set to its parent's branch (`origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`). Never require `gt`. Before any rewrite or retarget, follow [Merge and restack safety](../safe-landing/references/merge-safety.md):
   - Capture the affected chain and its remote heads.
   - Cancel auto-merge requests and queue membership for that chain, and verify the cancellation.
   - Push with `--force-with-lease=refs/heads/<branch>:<captured-remote-head>`.

   An owner takes your push as its new base and lease. On a conflict, it resolves its own slice for you to push.
3. **Absorb drift at the root.** Until landing starts, apply `full-patrol` step 5's test to each link, and rebase the chain bottom-up where it calls for one. Then apply the patch-id rule from `safe-landing` link by link, since a link's base is its parent. Record each verdict's head SHA, base SHA, base branch, and patch-id. Send a link whose verdict no longer applies, or may not apply to its new base, back through verification before delivery. `orch frontier set` (`bun ../../tools/orch/orch.ts`, see `kyoshi-command`) records the chain with its head SHAs, and `bun ../../tools/watch-pr/watch-pr` watches it (see `long-flight`).
4. **Deliver the chain, then keep your hands off it.** Each link carries its verdict in its PR. Once landing starts, nobody writes to the chain except the post-merge retarget that `safe-landing` sanctions, because a second writer breaks a landing in flight. A mid-landing problem goes through you to the operator, and any fix waits for the operator's go.

## Choosing between the patrols

Use `full-patrol` when the PRs are independent and the operator will click each merge as soon as its PR is merge-ready. Use `shield-wall` when the operator wants review before landing, the work is sequenced or coupled, or merge authority is withheld.

## Reply

Catch the operator up per `iceberg-wake`. Link the stack root and tip as `https://github.com/<owner>/<repo>/pull/<number>`, give a one-line verdict per link, and name anything parked or excluded with the reason.
