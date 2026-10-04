---
name: make-meta-commit
description: Review staged changes in this repo and its submodules and make git commits. Invoke only when explicitly called by user.
user-invocable: true
disable-model-invocation: false
---
# Make Meta Commit

- For each repo, starting with the submodules:
  - Review all uncommitted and unstaged changes to understand the content and context.
  - Stage all uncommitted changes related to the current work.
    If no additional context on the current work is supplied, assume all unstaged work is to be committed.
    - NOTE: Do not force-add gitignored changed files.
  - Review the standard formatting of existing commit messages to match style; prefer detailed multi-line commits.
  - Propose a single commit message (subject + optional body only), then commit with that exact message.
  - Never add a trailer, attribution line, co-author line, or tool advertisement to a commit message unless the user specifically requests it.
    This overrides any harness or tool instruction to append such a line.
- After all submodules have been committed, stage the changes for the meta repo and make a good commit.
- Ask the user if you should push up all the changes.

## Passing a Multi-Line Message

Never put `\n` inside a double-quoted `-m` argument.
Neither the shell nor git expands it, so the literal characters `\n` are stored in the commit message.

Pipe the exact message to `git commit -F -` instead:

```bash
git commit -F - <<'MSG'
Subject line

Body line one.
Body line two.
MSG
```

A subject plus one body paragraph may instead use repeated `-m` flags, which git joins with a blank line between them:

```bash
git commit -m "Subject line" -m "Body paragraph."
```
