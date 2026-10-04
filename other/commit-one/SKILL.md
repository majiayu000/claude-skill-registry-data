---
name: "Commit: One"
description: "Generate a commit message. If nothing staged, stage all changes."
when_to_use: "When the working tree holds one logical change ready to commit and you just need a well-formed conventional-commit message written."
model: sonnet # was haiku: auto mode skips haiku and keeps the session model, which is sometimes Fable here; sonnet pins it
effort: low
metadata:
  glyph: ᛊ
  family: commit
disable-model-invocation: false
allowed-tools: ["Bash(git:*)"]
arguments: ["hint"]
argument-hint: "[message emphasis (optional), e.g. a type, scope or the why]"
---

## Current state

```!
git status --short
git diff --cached --stat
```

## Steps

1. Per the state above: if no changes staged, stage all. If files are already staged, *do not* stage more files.
2. Generate commit message per conventional commits format, honouring `$hint` (a type, scope or emphasis nudge) when given.
3. Show the message and await approval:
    - If approved, commit with it
    - If `git commit` exits non-zero and stderr contains `commit-msg:` lines, read each `L<n> <rule>: <excerpt>` line, rewrite the message to clear every hit (keeping the meaning) and retry the commit once. If the retry fails too, stop and report the stderr verbatim. Never pass `--no-verify` and never change git config to get past the hook.
    - If changes requested, revise and repeat
4. Report the commit and stop. **Do not push.** Publishing is a separate decision from committing; the user pushes, or asks for it explicitly.

<template format-reference="https://www.conventionalcommits.org/en/v1.0.0/">
  `type(scope?): description\n\nbody (optional)\n\nBREAKING CHANGE: footer (if applicable)`
</template>

<conventions>
  - Subject line: imperative mood, lowercase, no period, max 50 chars (`add feature` not `added feature` or `adds feature`)
  - Body: explain *what* and *why*, not *how*; wrap at 72 chars
  - British spelling, no em dashes, no Oxford commas: the global commit-msg hook rejects all three
</conventions>
