---
name: create-github-skills-outline
description: "Create learner-centered GitHub Skills exercise outlines from a topic, demo, workshop, or rough idea. Use this whenever the user wants to design a GitHub Skills exercise, convert training material into a self-paced GitHub exercise, define learning objectives and steps, or plan validation before building repository files."
---

# Create GitHub Skills outline

Use this skill to design a self-paced GitHub Skills-style exercise before implementation begins. The outline
is a build contract: `bootstrap-github-skills-exercise` should be able to generate the repository from it
without guessing.

## Workflow

1. Clarify the topic, target learner, prerequisites, time box, and desired outcome.
2. Narrow broad ideas to one primary learner outcome.
3. Design a scenario that gives the learner a reason to complete the task.
4. Break the exercise into 3 to 5 steps with one learner action per step.
5. Write a Theory block and at least one Activity block for every step.
6. Define validation signals and feedback for each step.
7. Name the repository files, workflows, and assets needed for implementation.
8. Call out open questions instead of inventing domain details that affect correctness.
9. Present the outline, take feedback, and revise. Repeat until the user explicitly approves.

## Approval gate

The outline is not finished until the user approves it. On each revision, state what changed and what still
needs a decision. When approved:

- record where the approved outline is stored so the bootstrap step can consume it,
- confirm the step count, graded steps, and file map one final time,
- hand off to `bootstrap-github-skills-exercise`.

Do not generate repository files from this skill.

## Step design requirements

Every step must include all of the following. A step missing a Theory block or an Activity block is an
incomplete outline: fill the gap, or ask the user for the missing detail. Never emit a step with a Theory
heading and no content.

| Element | Requirement |
| --- | --- |
| `📖 Theory` | Exactly one per step. Real awareness-level content, two to five sentences, directly tied to the Activity. Not a placeholder. |
| `⌨️ Activity` | At least one per step. Concrete numbered actions a learner performs in GitHub. |
| Action types | Tag each action as chat prompt, CLI prompt, terminal, or GitHub UI so bootstrap emits the right badge block. |
| Troubleshooting | Recovery hints for the likely mistakes in this step. |
| `Actions Trigger` | The GitHub event that advances the exercise (`pull_request`, `push` with `paths`, `issues`, `issue_comment`, `workflow_dispatch`). |
| `Grading-Check` | Whether the step is graded, and the concrete check: `skills/exercise-toolkit/actions/file-exists`, `skills/action-keyphrase-checker`, or a custom script. |
| Learner artifact | What exists in the repository after the step succeeds. |

Keep the exercise scoped to the requested topic. If a concept is useful but out of scope, list it as a
follow-up exercise instead of adding it to the current outline.

## Activity action types

When an activity action is a Copilot prompt or a terminal command, write the exact text in the outline and
tag its type. Bootstrap renders it as a badge-led blockquote:

- **chat prompt** — Copilot Chat or IDE prompt, purple `Prompt` badge.
- **CLI prompt** — Copilot CLI prompt, `CLI-Prompt` badge.
- **terminal** — shell command, blue `Terminal` badge.
- **GitHub UI** — plain numbered instruction, no badge.

## Reference guidance

- Prefer official references (GitHub Docs, GitHub Learn, GitHub Blog/Changelog, and official VS Code docs).
- Keep references relevant to the exact step content; do not add generic links that are not used.

## Formatting conventions

- Any image added for the exercise should be stored in `.github/images` and referenced with a relative path.
- Keep GitHub callouts left-justified (no indentation) when using `[!NOTE]`, `[!IMPORTANT]`, or `[!TIP]`.
- Use this exact style:

> [!NOTE]
> This is a note

> [!IMPORTANT]
> This is an important item to be aware of for this exercise

> [!TIP]
> It is a good idea and recommended to do this tip

## Outline template

Return this structure by default:

```markdown
# [Exercise title]

## Summary

One-line description of the exercise.

## Welcome block

- **Who is this for**:
- **What you'll learn**:
- **What you'll build**:
- **Prerequisites**:
- **How long**:

## Learning objectives

## Scenario

## Learner journey

### Step 1: [Step name]

**📖 Theory: [Theory title]**

[Two to five sentences of awareness-level context tied to the activity below.]

**⌨️ Activity: [Activity title]**

1. [Action] — _(type: chat prompt | CLI prompt | terminal | GitHub UI)_
1. [Action] — _(type: ...)_

**Troubleshooting**

- [Likely mistake and recovery]

**Transition**

- Actions Trigger: [event]
- Grading-Check: [graded? which check and what it asserts]
- Learner artifact: [what exists after this step]

### Step 2: [Step name]

[Same structure. Repeat for every step.]

## Review recap

Feeds `.github/steps/x-review.md`.

- Accomplishments:
- What's next:

## File map

| File | Purpose |
| --- | --- |
| `README.md` | |
| `.github/steps/1-step.md` | |
| `.github/steps/x-review.md` | |
| `.github/workflows/0-start-exercise.yml` | |
| `.github/workflows/1-step.yml` | |
| `.github/workflows/N-last-step.yml` | |

## Success criteria

## Risks and open questions
```

## Quality bar

- Objectives should be observable: the learner can demonstrate them through repository activity.
- Every step has a Theory block with real content and at least one Activity block.
- Steps should be small enough that validation can give targeted feedback.
- Validation should check intent, not only file existence.
- The file map should name real files, aligned by number, with the final workflow as `N-last-step.yml` and
  the review content as `x-review.md`.
- The outline should be implementable as GitHub issues, comments, workflows, and Markdown content.
