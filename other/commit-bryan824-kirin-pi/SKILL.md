---
name: commit
description: "When asked for a commit, its message, or a push — preserve staged intent and verified scope; execute only explicitly authorized operations."
---

# Commit

One commit should have one coherent reason to review or revert it. A verification
handoff is evidence, not commit authority; a request for a message alone changes
nothing.

- Establish the authorized paths and operations. Inspect status, staged and
  unstaged diffs, untracked files and recent message style. Do not include
  unrelated or pre-existing work merely because it is dirty.
- Preserve staged intent. Ask before unstaging or regrouping another selection.
  Never stash, clean, move user files or switch branches just to manufacture a
  clean tree. A request for all intended changes still allows logical commits;
  honor an explicit single-commit request.
- Consume fresh verification for the same complete change. New code or
  materially changed evidence requires review again; a prior pass does not cover
  later hunks. Required failed or unrun checks block the normal commit gate.
  Report any proposed exceptional checkpoint and obtain explicit authority
  without relabeling the verification as passed.
- Stage exact paths, inspect the staged diff and commit only the approved group.
  Preserve integrity hooks; a hook failure is work to diagnose, not bypass.
  Use the repository's message style, or concise imperative Conventional Commits
  when there is none. No generated/co-author attribution or unsolicited sign-off.
- Push only with explicit push authority. Verify the resulting commit and, when
  pushing, the actual remote/branch result. Report unexpected changes instead of
  hiding them behind a successful command.

Deliver: commit IDs, messages and included scope, verification used, untouched
work and push result if authorized. Stop at a message or proposed grouping when
that is all the user requested.
