---
name: handoff
description: "Captures unfinished work as a structured comment on the issue or pull request, covering state, done, open and next steps, built from git and gh state rather than memory. Use when stopping mid task, running low on context, or asked for a handoff or handover note."
---

# handoff

Leave unfinished work resumable without reconstructing it from memory.

## When to use

- Stopping before the work is done: end of session, low context, blocked, handing over.
- Finished work: use `tldr` instead.

## Steps

1. Read the real state: `git status --short`, `git diff`, `git log --oneline <base>..HEAD`,
   `git branch --show-current`.
2. Read the remote state: `gh pr view --json number,title,isDraft,reviewDecision,mergeStateStatus`,
   `gh pr checks`.
3. Commit uncommitted work with Conventional Commits, or state in the note why it stays
   uncommitted.
4. Push the branch so every referenced commit is reachable.
5. Fill the template from what was read, never from memory of the conversation.
6. Name failing checks by their actual reason, not just that they are red.
7. Decisions include the rejected option, since the diff alone does not carry it.
8. Next steps are ordered, each naming a file or command.
9. Post as a comment: `gh issue comment <number> --body-file <file>` or
   `gh pr comment <number> --body-file <file>`.
10. Never commit the handoff note into the repository.

## Template

```markdown
## Handoff
- Branch: `<branch>`
- PR: <#number, or none>
- State: <in progress | blocked on X | ready for review>
## Done
- <Outcome> (`<sha>`)
## In progress
- `<path>`: <what is half done>
## Next steps
1. <Action naming a file or command>
## Checks
- <check name>: <failing reason> | all green | not run
```

## Guardrails

- State comes from `git` and `gh`, never from memory.
- Every uncommitted file is either committed or explained, never left silent.
- No secrets, tokens or internal hostnames in the note.
- No version bump or changelog edit.

## References

- `gh pr checks`: <https://cli.github.com/manual/>
- Conventional Commits: <https://www.conventionalcommits.org/en/v1.0.0/>
