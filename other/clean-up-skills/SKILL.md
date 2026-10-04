---
name: clean-up-skills
description: Reconcile installed skills with removals from the latest main catch-up.
disable-model-invocation: true
compatibility: Git repo managing skills under home/.agents/skills and home/.claude/skills.
---

# Clean up skills

Remove stale installed skills by **provenance**, not by mirroring blindly:

```text
deletion candidates = installed extras ∩ paths deleted by the selected catch-up
```

Treat `home/.agents/skills` and `home/.claude/skills` as sources, and
`~/.agents/skills` and `~/.claude/skills` as their installed targets.

## Safety boundary

- Stay read-only until the user approves an exact deletion list.
- Never alter repo source files during cleanup.
- Never delete unrelated extras, Claude runtime state, or paths outside the two installed skill roots.
- Compare the two skill trees independently. Do not mirror a `.claude` deletion into `.agents`; this repo intentionally keeps some `.agents/.../agents/openai.yaml` files after matching Claude metadata is removed.
- Treat a target symlink resolving to its source file as matching content, not drift. Delete a symlink itself, never its target.
- Preserve the initial Git working-tree state. Existing changes belong to the user.

## 1. Select the catch-up range

Record `git status --short`, current branch, HEAD, and recent reflog. Identify the most recent reflog transition that caught the local default branch up through pull, merge, or rebase. Use its prior and resulting commit as `before` and `after`; include every commit in that range, not only the tip commit.

If the transition or intended range is ambiguous, stop and ask the user to choose it. Do not infer a destructive range from commit dates alone.

**Complete when:** one explicit `before..after` range is supported by reflog evidence, and the initial working-tree state is recorded.

## 2. Inventory skill drift

Compare each source tree with its installed target recursively. Report:

- source paths missing from the target;
- shared files whose dereferenced content differs;
- target paths absent from the source.

Collapse an extra directory in the report only when the whole subtree is extra. Keep missing files and content drift separate from deletion candidates; they may indicate an incomplete sync rather than stale skills.

**Complete when:** every path under both source and target skill roots is classified, with matching symlinks counted as matches.

## 3. Prove deletion candidates

List paths deleted in the selected range:

```bash
git diff --name-status <before>..<after> -- \
  home/.agents/skills home/.claude/skills
```

Intersect `D` entries with installed extras in the corresponding target tree. Recommend a whole installed directory only when:

1. no corresponding source path remains;
2. every installed descendant is explained by deletions in the range; and
3. removing it cannot remove an unrelated installed addition.

Otherwise recommend only proven files, plus directories that become empty afterward. Keep all other extras in a separate “unrelated extras” list.

**Complete when:** every candidate has a deleted repo path as provenance, and every non-proven extra is excluded.

## 4. Present before changing

Show:

- selected range and catch-up commits that removed skills;
- missing or content-different managed paths;
- exact installed paths recommended for removal;
- unrelated extras that will remain;
- initial dirty Git paths.

Ask one focused question for explicit approval of the exact candidate set. Do not delete on vague approval, and do not broaden the set after approval.

**Complete when:** the user explicitly approves an unchanged, exact deletion list or declines cleanup.

## 5. Remove and verify

Immediately before deletion, re-check that every approved path still exists as the same file, directory, or symlink observed during inventory. Stop and recompute if anything changed.

Delete only approved paths. Use exact quoted paths rooted under `~/.agents/skills` or `~/.claude/skills`; do not use globs. Then verify:

- each approved path is absent, including broken symlinks;
- every source-managed skill path still exists in its target and dereferenced contents match;
- unrelated extras remain;
- `git status --short` matches the initial state;
- no repo file was changed by cleanup.

Report removed paths, verification result, and remaining unrelated extras.

**Complete when:** all approved paths are absent, managed skill trees still match, and Git state is unchanged.
