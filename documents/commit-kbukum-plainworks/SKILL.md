---
name: commit
description: >-
    Commit staged (or explicitly named) changes with a single compact, developer-friendly commit
    message that states what changed — no Co-authored-by trailer, no plan/batch/PR numbers, no tool
    or review narration. Keep one commit per branch (amend). Use when asked to commit work in
    plainworks.
---

# Committing with a clean, developer-friendly message

A commit message tells the next developer *what changed and why*, in as few words as it takes. This skill keeps plainworks' history tidy: one focused change per branch, a message that reads like a maintainer wrote it, and **nothing extra** — no trailers, no attributions, no process log.

## 1. Know what you're committing

```bash
git status --short          # what's staged vs. unstaged
git diff --cached           # the exact change going in
```

- Stage deliberately (`git add <paths>`); don't sweep in unrelated edits or `tmp/` scratch. If the working tree mixes concerns, prefer amending into one coherent change per branch rather than piling on commits.
- Don't commit generated output (`dist/`, `coverage/`, `.turbo/`), secrets, or `tmp/`.

## 2. Write the message

plainworks uses **Conventional Commits** (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`). A single compact subject line, imperative mood, describing the change **as it now stands**:

```
feat(channel): add SSE reconnect with jittered backoff
fix(auth): reject token supplied via query string
refactor(state): per-request zustand store factory
docs: sync architecture layer map with the boundaries config
```

- **Subject only** for small changes; keep it under ~72 chars. Add a short body (blank line, then wrapped prose) **only** when the *why* isn't obvious from the subject.
- Scope is the package name (`std`, `channel`, `auth`, `boundaries`, …). Pick the one that matches the change; don't force a scope that isn't real.
- Describe the current change, not the journey: no "previously we…", no "as requested in review".

**Never include:**

- a `Co-authored-by:` trailer or any other trailer/attribution,
- plan / batch / step / PR / issue numbers as scaffolding,
- tool, agent, or session references.

## 3. Commit — one per branch

```bash
git commit -m "feat(channel): add SSE reconnect with jittered backoff"
```

The convention is **one commit per branch**: for follow-up edits on the same branch, **amend** rather than adding a new commit, unless told otherwise:

```bash
git commit --amend --no-edit        # fold new staged edits into the single commit
```

Use a message file for a subject + body: `git commit -F <path>`. Do **not** amend or rewrite already-pushed history unless explicitly asked, and do **not** run destructive git commands on uncommitted work. Push only when asked (or when the task — e.g. resolving PR reviews — requires the commit to be on the branch).
