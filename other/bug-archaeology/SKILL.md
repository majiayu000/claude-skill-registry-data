---
name: bug-archaeology
layer: method
description: When a bug or regression is reported, the FIRST step — before fixing — is to research how and when it was introduced (git archaeology), then record that finding on the tracking issue/PR. Use the moment a bug, error, broken build, or "this used to work" is reported, before writing a fix. Produces a first-bad-commit (or "not a code regression") note you paste onto the issue.
allowed-tools: Bash, Read, Grep, Glob
---

# Bug Archaeology — find out *how & when* it broke, before you fix it

**The reflex for any bug is: research origin first, fix second.** Jumping
straight to a fix hides the real story and produces symptom-patches. The recent
case that motivated this (issue #424): a fanfare build warned that
`@fyit/crouton-printing/server/database/schema` "could not be resolved". It
*looked* like a code bug — but archaeology showed the code and lockfile were
correct since #329; the real cause was a **stale local install** (a missing pnpm
workspace symlink). A symptom-first reflex would have "fixed" package code that
was never broken.

So before you touch the code: **establish when the behaviour changed, what
change introduced it, and whether it's even a code regression at all** — then
write that down where the next person (or agent doing `git blame`/`git bisect`)
will find it.

## When to use
- **Default / first step** the moment a bug, crash, error, failed build, broken
  test, or "this used to work" is reported — *before* writing a fix.
- On ask: "when was this introduced", "find the regression", "root-cause this".
- **Skip** only for a brand-new feature that never worked (nothing to regress
  from) or a one-line obvious typo in code you just wrote this session.

## The protocol

### 1. Reproduce / pin the symptom
Get the exact error string, failing file, or observable. You need a concrete
needle to search history for.

### 2. Decide: code regression, or environment/state?
Before blaming a commit, rule out the non-code causes — they're common and
archaeology on the *wrong* axis wastes time:
- **Stale install** — `node_modules`/symlinks out of date vs the lockfile
  (run `pnpm install`; compare `ls -la node_modules/...` link mtimes to the dep's
  introduction date). This was the #424 cause.
- **Env/secrets/config** — a value differs between machines/envs, not the code.
- **Data/state** — a migration, a seeded row, an external service.

If it's one of these, that *is* the finding — record it and stop (don't go
commit-hunting for a regression that isn't in the code).

### 3. Git archaeology — find the first bad change
Pick the tool that fits the needle:

```bash
# A symbol/string appeared or vanished — pickaxe is the fastest first move:
git log -S '<exact string>' --oneline -- <path>     # commits that add/remove the literal
git log -G '<regex>' --oneline -- <path>             # commits whose diff matches a regex

# When did this file/area last change, and in what commit?
git log --oneline -- <path>
git log --oneline -L '<start>,<end>:<path>'          # history of a specific line range

# Who last touched the exact line, and why (read that commit's message):
git blame -L <line>,<line> -- <path>
git show <sha>                                       # the introducing change + its rationale

# Behaviour regression with no obvious line — bisect between a known-good and known-bad:
git bisect start <bad-sha> <good-sha>
git bisect run <command-that-exits-nonzero-on-the-bug>
git bisect reset
```

Tie the first-bad commit back to its **PR/issue** (`git log` shows the `(#NN)`
merge ref) so the finding links the original change.

### 4. Record the finding (REQUIRED — this is the deliverable)
Archaeology that isn't written down gets re-done. Post the finding **on the
tracking issue/PR** as a comment, or in the bug issue body. If no issue exists
yet, open one (per `github-tasks`) — the finding is its first content. Keep the
bare `(#NN)` convention in commits; link full URLs in chat replies.

## Finding template (copy-paste)

```markdown
## 🔬 Archaeology

- **Symptom:** <the exact error / observable>
- **First introduced:** <commit SHA> (<PR #NN>, <YYYY-MM-DD>) — `<one-line what that change did>`
  <!-- OR, when it's not a code regression: -->
- **Not a code regression:** <stale install | env/secret | data/state> — <what was actually wrong>
- **How found:** <git log -S '…' / git bisect / symlink mtime vs dep introduction / …>
- **Fix:** <the change that addresses the *root* cause, not the symptom>
```

A good finding states either a **first-bad commit (SHA + PR + date)** *or* an
explicit **"not a code regression — <cause>"**. "Looks broken, fixed it" is not
a finding.

## How this fits the workflow
This is **step 0** of bug work in `CLAUDE.md`'s Task Execution Workflow: research
origin and record it *before* the fix. It pairs with `/review` (which inspects a
diff for problems) and `github-tasks` (where the finding is recorded). The
durable archaeology note is exactly what a future `git blame`/`git bisect` lands
on — so we stop re-litigating settled regressions.