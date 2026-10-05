---
name: commit-all
description: Batch-commit all uncommitted changes grouped by relevance. Use when multiple accumulated changes need committing. Invoked by saying "commit all" or "commit everything".
---

# Commit All Uncommitted Changes

Stage, commit, and push **all** uncommitted changes — grouped by relevance so each commit is cohesive.

---

## Branch Safety (BLOCKING GATE)

1. **Check the current branch** — run `git branch --show-current`.
2. **If on `master` or `main`** — **STOP immediately**. Do not stage, commit, or push.
3. **Stay on the current branch.** Never switch branches.

---

## Steps

### 1. Assess All Changes

```bash
git status --short
git diff --stat
```

### 2. Group Changes by Relevance

Cluster files into **commit batches** based on:
- Feature/module area
- Change type (docs, config, source)
- Logical coupling

Target 1–5 batches. If all related, one batch is fine.

### 3. For Each Batch — Present 3 Commit Message Options

Before committing each batch:
1. List the files in the batch
2. Present **3 numbered commit message options** (concise → descriptive)
3. Wait for the user to pick

### 4. Stage and Commit Each Batch

```bash
git add <explicit-file-paths>
git commit -m "<type>(<scope>): <subject>" -m "<body>"
```

**Never use `git add .` or `git add -A`.** Always explicit paths.

### 5. Push

After all batches committed:
- Ask: "All batches committed. Ready to push to `<branch>`?"
- Wait for explicit approval before pushing.

---

## Commit Message Rules

Same rules as the `$commit` skill:
- Subject: `<type>(<scope>): <summary>` — under ~80 chars
- Types: `feat`, `fix`, `refactor`, `docs`, `style`, `data`, `config`, `chore`
- Body: 2–3 `-m` flags max, end with `Files:` list
- **3 options per batch** — user picks.

---

## Rules

- **Never stage without showing batch contents first.**
- **Never combine unrelated changes.**
- **Never skip the 3-option presentation.**
- **One commit per batch, one push at the end.**
- **Always ask for explicit user approval.**
