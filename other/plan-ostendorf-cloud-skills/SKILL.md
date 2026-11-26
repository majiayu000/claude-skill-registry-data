---
name: plan
description: "Writes a short implementation plan into a GitHub issue, split into verified facts and assumptions, ordered reviewable steps, files touched, a verification command, risks and open questions. Use before implementing a non trivial issue, or when asked to plan an approach first."
model: opus
---

# plan

Produce a short plan in the issue that can be approved or corrected before code exists.

## When to use

- An issue is ready to implement and the approach is not obvious.
- Skip for a typo, a one line fix or a mechanical rename: no plan needed.
- No issue exists yet: offer to create one with the `issue` skill first.

## Steps

1. Read the issue and its comments. Restate the request in one line.
2. Split verified facts (a file opened, a command run) from assumptions.
3. Verify the cheap things: module exists, pinned version, existing helper, current test
   coverage.
4. Steps in order, each ending reviewable and committable alone. Risky step first.
5. Files to touch, with paths. Flag shared interfaces, schemas or config contracts.
6. Name the verification command from config `verify`, or state why none is needed.
7. State risks: migration, backward compatibility, rollback.
   Add an expected duration for the whole plan and per step where it helps. A rough number,
   not a promise.
8. Pick a model per step only when a step needs something other than the configured implement
   model; state tokens and time against capability in one line.
9. List open questions: anything unclear, anything that could additionally be implemented, every
   assumption made.
10. Runs only when config `plan.critique` is enabled, and the plan is large or cross-cutting:
    crosses modules or services, touches a security boundary, touches a shared or public
    interface.
    Spawn two or three short-lived critic subagents, each on a distinct angle: security, data
    and schema, architecture and interfaces.
    Give each critic only the draft plan, not the issue or conversation history. Each critic
    returns objections or gaps.
    Fold genuine objections into the existing Risks and Open questions sections. No new template
    section for this.
    Critics run on `models.review` (default sonnet), not `models.plan`: this is a review task,
    not a planning authority task.
11. One screen. No plan content in `docs/`.
12. Write the plan as a `## Plan` section via `gh issue edit --body-file <file>`, appended to the
    existing body, when the body already follows this repository's template.
    A read-only planner cannot write into the repository. It writes the body file into the
    session scratchpad, which sits outside the repository on the write allowlist.
    A multi-line body goes through `--body-file`, never `--body "..."`.
    A gh configuration error on a long body means the body is too long, not an authentication
    problem.
13. Body does not follow that template: post the plan as a comment with `gh issue comment`
    instead, to avoid breaking a structure this skill does not own.
14. Stop at the plan. Do not implement here.

## Template

```markdown
## Plan
### Verified
- `<path>`: <what reading or running it confirmed>
### Assumed
- <Assumption>, correct me if wrong
### Steps
1. <Step ending reviewable>
### Files
- `<path>`: <change> <(new)>
### Verification
- `<command>`
### Risks
- <Risk, or none>
### Model per step
- Step <n>: <model>, because <one line>
### Open questions
- <Question>
```

## Guardrails

- Verified and assumed stay separate, never blended.
- Steps end reviewable alone. Risky step comes first.
- A model override is named with the tradeoff, never silent.
- No plan content lives in `docs/`.

## Config

Reads `.agent-skills.json` through the snippet in `~/.claude/skills/README.md`.

- `verify`: command that proves a change is good. Default `task check` when a Taskfile exists.
- `models.plan`: default `opus`. `models.implement`: default `sonnet`.
- `plan.critique`: boolean, default `false`. Runs the critic subagent step on a large or
  cross-cutting plan.

## References

- `gh issue edit`, `gh issue comment`: <https://cli.github.com/manual/>
