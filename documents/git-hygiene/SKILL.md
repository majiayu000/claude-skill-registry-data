---
name: git-hygiene
description: >
  Keep git history human-readable. Use when committing, branching, or
  rewriting history; when prose reads like agent slop; or when a host name
  leaks into durable text. For issue and pull request prose, use
  $issue-and-pr instead.
---

# Git hygiene

Git tracks history. A host only publishes it. Write every durable word so it
still makes sense if the host changes: branches, remotes, and reviews are
git concepts, and no host name belongs in commits, issues, or lasting docs.

## Commits

One idea per commit. Start the message with a verb and say what changes:

```sh
git commit -m "Shorten the retry backoff to five seconds"
```

Add a body only when the why is not obvious from the diff. Never record the
conversation: no mention of who asked, which agent ran, or what turn this
was. Read the message as a stranger: it should explain the change, not the
chat that produced it.

## Branches and history

Tidy private branches freely and leave published ones alone. Never rewrite a
branch someone else may have pulled. Rebase to keep your own work readable;
merge to record that two lines of work joined. Force-push only to a branch
you own, and say so when you do.

## Issues and pull requests

Handled by $issue-and-pr. This skill keeps the history side; that one owns
the prose.

## Simple English

Short sentences. Common words. No jargon without an explanation on first
use. If a sentence needs a second reading, rewrite it before anyone else
has to.
