---
name: "Commit: Batch"
description: "Split uncommitted changes into granular commits."
when_to_use: "When several unrelated changes have piled up uncommitted and a single commit would bundle them; splits into one logical commit per change."
model: sonnet # was haiku: auto mode skips haiku and keeps the session model, which is often Fable or Opus here; sonnet pins it
effort: low
metadata:
  glyph: ᛊ
  family: commit
disable-model-invocation: false
allowed-tools: ["Bash(git:*)"]
arguments: ["hints"]
argument-hint: "[grouping hints (optional), e.g. 'docs together, config separate']"
---

## Current state

```!
git status --short
git rev-parse --verify HEAD >/dev/null 2>&1 && git diff --stat HEAD || echo "(no commits yet, nothing to diff against)"
```

## Steps

1. The current state above was captured at invocation; run `git diff HEAD` on specific files only where the stat alone can't tell you what a change is.
2. Analyse the changes and group them into logical commit units; each group should represent a single coherent change (e.g. one feature, one fix, one refactor). If `$hints` was given, honour it as the intended grouping; it overrides the guidelines below where they conflict.
3. Present the proposed commit plan as a numbered list:
   - Group name / files involved
   - Suggested commit message (conventional commits format)
4. Await approval: **stop here and do not proceed until the user responds**:
   - If approved, execute commits sequentially. For each group:
     1. Stage **only** the files listed for that group (`git add <files>`)
     2. Commit with the proposed message
     3. If `git commit` exits non-zero and stderr contains `commit-msg:` lines, read each `L<n> <rule>: <excerpt>` line, rewrite the message to clear every hit (keeping the meaning) and retry the commit once. If the retry fails too, stop the batch and report the stderr verbatim along with which groups landed and which did not. Never pass `--no-verify` and never change git config to get past the hook.
     4. Confirm success before moving to the next group
   - If changes requested, revise the plan and repeat from step 3.
5. Report the commits made and stop. **Do not push.** Publishing is a separate decision from committing; the user pushes, or asks for it explicitly.

## Grouping Guidelines

- Prefer smaller, atomic commits over large ones
- Keep unrelated changes in separate commits even if they touch the same area
- Config/dependency changes separate from feature code
- Test changes alongside the code they test (same commit), unless the test is independent
- Generated files (lockfiles, build artefacts) get their own commit if significant

<template format-reference="https://www.conventionalcommits.org/en/v1.0.0/">
  `type(scope?): description\n\nbody (optional)\n\nBREAKING CHANGE: footer (if applicable)`
</template>

<conventions>
  - Subject line: imperative mood, lowercase, no period, max 50 chars (`add feature` not `added feature` or `adds feature`)
  - Body: explain *what* and *why*, not *how*; wrap at 72 chars
  - British spelling, no em dashes, no Oxford commas: the global commit-msg hook rejects all three
</conventions>
