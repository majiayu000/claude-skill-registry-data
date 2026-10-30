---
name: light-load
description: Appa's light load for reviewability. Appa flies farthest when the saddle carries only what the trip needs. Use for make-pr-easy-to-review, /make-pr-easy-to-review, "make this easy to review", "tidy this PR", "clean up commits", or "annotate the diff". Cleans noisy history, sharpens the description, and adds reviewer guidance without changing code behavior.
---

# Appa's light load

Appa can carry the whole team, but he flies farthest when the saddle holds only what the trip needs, packed so anyone can find what they are looking for. A PR is the same. Prepare it so a reviewer quickly understands the intent, the important files, and the risk. The default goal is reviewability with no behavior change.

## Steps

1. **Resolve the target PR.** Use the URL the user gave, or the PR for the current branch.
2. **Inspect it.** Read the commits, the diff size, the changed paths, the generated files, and the PR description.
3. **Name the reviewability problems.** Look for noisy commits, a stale description, unrelated changes, mechanical and logic changes mixed together, missing tests, or no clear place for the reviewer to start.
4. **Propose a plan before rewriting history or force-pushing.** Wait for the user's agreement on any history rewrite.
5. **Apply the safe improvements.** Then verify that the tree or diff still matches the intended code.

## History cleanup

Rewrite history only when the user asks for it or agrees to the plan. Before you rewrite, record the original tree:

```bash
gh pr view <PR> --json title,headRefName,baseRefName,state,commits
git fetch origin <headRefName> <baseRefName>
ORIGINAL_TREE=$(git rev-parse origin/<headRefName>^{tree})
```

Good commit groupings usually follow dependency order:

1. Schema, storage, or generated API definitions.
2. Core logic.
3. Wiring and integration.
4. UI or surface behavior.
5. Tests.

After you rewrite, verify that the content is identical:

```bash
echo "Original tree: $ORIGINAL_TREE"
echo "Current tree:  $(git rev-parse HEAD^{tree})"
git diff origin/<headRefName> --stat
```

Do not push if the tree changed unintentionally. An empty `git diff` and matching tree hashes are the proof.

## Reviewer guidance

When code behavior must stay untouched, improve the PR description and add review notes instead. Write them with `tea-time`, in the description shape from `yip-yip`.

- Add a short summary at the top that matches the actual diff.
- Separate the core files from generated or mechanical files.
- Call out risky behavior changes, migration order, the rollout plan, and test coverage.
- Link issue trackers, dashboards, or design docs when they explain intent.

## Rules

- Never hide a meaningful behavior change inside "cleanup".
- Do not bypass hooks (`--no-verify`) unless the user explicitly asks.
- Never force-push a branch others may have pulled without the user's word.
- If the PR is too large to make reviewable with notes, recommend splitting it into a stack (see `yip-yip`) instead of polishing around the problem.

## Reply

The problems you found, what you changed, the before and after tree hashes when history moved, and anything you recommend but did not do.
