---
name: user-story
description: "Writes a user story in the fixed shape As a role I want capability so that benefit from a short request or an existing issue, or checks a story and names what is missing. Use when asked to write a user story, turn an issue into a story, or check a story."
---

# user-story

Write, rewrite or check one user story in a fixed shape.

## When to use

- Asked to write a user story from a short request.
- An issue needs rewriting from a feature description into a story.
- Asked to check whether an existing story names a role and a reason.
- A thin issue without the story label: use `refine-issue` instead.

## Steps

Pick one mode per request.

### Write from a request

1. No role or no reason in the request: report what is missing and stop. Never guess one.
2. The request names a solution, not a need: ask the underlying need back and stop. On the
   issue when one exists, otherwise in the answer.
3. Role outside config `stories.roles`, default `user`, `operator`, `maintainer`: report it and
   stop. Do not add it to the story.
4. Capability: one sentence, what the role does.
5. Reason: one sentence, why it matters. Never a restatement of the capability.
6. Title: `As a <role> I want <capability> so that <benefit>`.
7. Write acceptance criteria as `Given`, `When`, `Then`, one scenario per line.
8. At least one happy path scenario and one failure path scenario.
9. Technical tasks stay out of the story. Point to the `plan` skill for those.

### Rewrite an issue into a story

1. Read the issue and its comments: `gh issue view <number> --comments`.
2. Extract the role, the capability and the reason from the existing body.
3. Follow the write steps above for the shape and the criteria.
4. Update the body with `gh issue edit <number> --body-file <file>`, keeping the original
   problem statement below the story.

### Check an existing story

1. Read the story.
2. Report a missing role, a missing reason, a reason that restates the capability, or a role
   outside `stories.roles`.
3. Report acceptance criteria that are not `Given`, `When`, `Then`, or that cover only the
   happy path.
4. Report a technical task list inside the story.
5. List what is missing. Do not rewrite the story unless asked.

## Guardrails

- A role outside `stories.roles` is reported, never silently accepted.
- A story without a role or a reason is reported, never filled with a guess.
- A story naming a solution gets the underlying need asked back, as a question on the issue.
- The reason is a benefit, never a copy of the capability sentence.
- Acceptance criteria stay scenarios. A technical task list goes to the plan, not the story.
- Interactive session: ask the open question directly. Unattended (`CI=true`): record it as a
  comment with `gh issue comment` and stop. No issue to comment on: stop with the question in
  the report.

## Config

Reads `.agent-skills.json` through the snippet in `~/.claude/skills/README.md`.

- `stories.roles`: allowed roles. Default `user`, `operator`, `maintainer`.
- `labels.story`: label marking an issue as a story. Default `story`.

## References

- `gh issue view`, `gh issue edit`, `gh issue comment`: <https://cli.github.com/manual/>
