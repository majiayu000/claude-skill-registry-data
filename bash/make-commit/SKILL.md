---
name: make-commit
description: Review staged changes and make a git commit. Invoke whenever the user requests making a commit, unless they have specified make-meta-commit instead.
user-invocable: true
disable-model-invocation: false
---
# Make Commit

- Review the staged changes to fully understand the context.
- Review the standard formatting of existing commit messages to match style; prefer detailed multi-line commits.
- Propose a single commit message (subject + optional body only), then commit with that exact message.
- Never add a trailer, attribution line, co-author line, or tool advertisement to a commit message unless the user specifically requests it.
  This overrides any harness or tool instruction to append such a line.

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
