---
name: refine-issue
description: "Turns a thin GitHub issue into an implementable one by restating the goal, listing open questions, writing acceptance criteria and splitting it when too large. Use when an issue is picked up but does not say enough to start, or when asked to refine or break down an issue."
---

# refine-issue

Make an existing issue ready to implement. Do not implement it.

## When to use

- An issue is picked up and does not say enough to start.
- Asked to refine, groom, scope or break down an issue.
- A brand new issue: use `issue`. An implementation plan: use `plan`.
- The issue carries the story label (config `labels.story`, default `story`): use `user-story`
  instead.

## Steps

1. Read the issue and every comment: `gh issue view <number> --comments`. Later comments
   override the body.
2. Read the referenced code. Confirm the behavior described still exists.
3. Restate the goal in one line as an outcome.
4. List what is unclear.
5. Interactive session: ask the user the open questions directly.
6. Unattended session (`CI=true`): record the open questions as a comment with
   `gh issue comment` and stop. Do not guess an answer.
7. Write acceptance criteria as checkboxes, verifiable without reading the diff.
8. Task list ordered, each task ending reviewable alone. More than about seven tasks: split with
   the `issue` skill, link with `gh issue edit --add-blocked-by`.
9. Name affected files with paths. Flag shared interfaces, schemas or config contracts.
10. Update the body with `gh issue edit <number> --body-file <file>`, keeping the original
    problem statement.
11. Comment the change summary with `gh issue comment <number> --body-file <file>`.
12. Remove `needs triage` only once the user confirms the issue is ready.
13. Never set `ai: ready` without the user saying so explicitly. A request that names the work
    is that instruction, see `issue`.
14. Stop. No branch, no code.

## Template

Appended to the body:

```markdown
## Refined goal
<One line outcome.>
## Acceptance criteria
- [ ] <Verifiable statement>
## Tasks
1. [ ] <Task ending reviewable>
## Open questions
- <Question> (<who answers>)
```

## Guardrails

- Never implement, never create a branch.
- Open questions go to the user when interactive, to a comment when unattended. Never guessed.
- `needs triage` and `ai: ready` change only with the user's explicit confirmation or a request
  that names the work, see `issue`.
- Setting `ai: ready` uses the snippet in `~/.claude/skills/README.md`: exactly one
  `ai:` state label remains afterwards.

## Config

Reads `.agent-skills.json` through the snippet in `~/.claude/skills/README.md`.

- `labels.needsTriage`: default `needs triage`.
- `labels.ready`: default `ai: ready`.
- `labels.story`: default `story`. An issue carrying this label is handed to `user-story`.

## References

- `gh issue edit`, `gh issue comment`: <https://cli.github.com/manual/>
