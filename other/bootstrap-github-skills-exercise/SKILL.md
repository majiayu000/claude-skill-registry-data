---
name: bootstrap-github-skills-exercise
description: "Bootstrap a GitHub Skills exercise repository from an approved outline. Use this when the user asks to create exercise files, step Markdown, issue templates, GitHub Actions workflows, validation scripts, starter content, or repository structure for a GitHub Skills-style learning experience."
---

# Bootstrap GitHub Skills exercise

Use this skill when an outline is approved and the user wants repository content or automation.

> [!IMPORTANT]
> Read `references/exercise-template-contract.md` before writing files. It holds the exact file names,
> workflow skeletons, reusable workflow inputs and outputs, action pins, chaining rules, and Markdown
> skeletons implemented by `skills/exercise-template` and `skills/exercise-toolkit`. Follow it unless the
> target repository intentionally diverges, and say so when you diverge.

## Preconditions

Do not start until you have:

1. An approved outline. If none exists, run `create-github-skills-outline` first.
2. A step-by-step journey where **every step has a Theory block and at least one Activity block**.
3. A decision for each step on whether it is graded and what the grading check asserts.

If the outline is missing a Theory or an Activity for any step, stop and resolve it with the user. Do not
invent filler content to fill the gap.

## First inspect the repo

Before editing, identify existing conventions:

- Where learner steps live.
- How workflows create issues, post comments, and validate progress.
- Which `skills/exercise-toolkit` ref the repository already pins.
- Whether reusable local actions or scripts already render Markdown templates.
- Existing test commands or workflow harnesses.

## Build order

Work in this order so each file can reference something that already exists:

1. `README.md` — title, Welcome block, objectives, Copy Exercise badge, troubleshooting details.
2. `.github/steps/N-step.md` for every step.
3. `.github/steps/x-review.md`.
4. `.github/workflows/0-start-exercise.yml`.
5. `.github/workflows/N-step.yml` for each intermediate step.
6. `.github/workflows/N-last-step.yml`.
7. Grading jobs, local actions, or scripts.
8. Maintainer validation notes.

## Required file set

| File | Required |
| --- | --- |
| `README.md` | always |
| `.github/steps/N-step.md` | one per step |
| `.github/steps/x-review.md` | always |
| `.github/workflows/0-start-exercise.yml` | always |
| `.github/workflows/N-step.yml` | one per intermediate step |
| `.github/workflows/N-last-step.yml` | always |
| `.github/images/` | when the exercise uses images |
| `LICENSE`, `.gitignore` | for a new standalone exercise repository |

## Markdown templates

Feedback templates come from `skills/exercise-toolkit` and are consumed by checking the toolkit out into the
workspace:

```yaml
- name: Get response templates
  uses: actions/checkout@v6
  with:
    repository: skills/exercise-toolkit
    path: exercise-toolkit
    ref: v0.9.3
```

Do not copy toolkit templates into the exercise repository. Create a local `.github/markdown-templates/`
directory only for exercise-specific copy that has no toolkit equivalent.

## Toolkit version check

The default toolkit ref is `v0.9.3`. When creating a new exercise, check whether a newer release exists and
ask the user whether to adopt it:

> ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
>
> ```bash
> gh api repos/skills/exercise-toolkit/releases/latest --jq .tag_name
> ```

If the latest published release is newer than `v0.9.3`, ask the user before changing anything, then apply
their answer to every toolkit reference in the repository.

> [!WARNING]
> Never pin a draft or prerelease. A draft release appears in the releases API but **its git tag does not
> exist**, so `uses: ...@<tag>` fails to resolve and every workflow breaks. Use `releases/latest`, which
> excludes drafts, and confirm the tag resolves with
> `gh api repos/skills/exercise-toolkit/git/ref/tags/TAG` before pinning it.

## Workflow structure expectations

Follow the standard job shape from the contract reference:

- `find_exercise` to locate the learner issue and its number/URL.
- optional `check_step_work` for grading and targeted feedback.
- `post_next_step_content` for transition behavior.

If `check_step_work` is present, include it in `post_next_step_content.needs`. If you remove it, reduce
`needs` back to `[find_exercise]`.

## Workflow design guidance

- Use least-privilege `permissions` per the contract reference matrix. Grant them per job, not workflow-wide:
  set `permissions: {}` at the workflow level so the learner-triggered grading job does not inherit
  `actions: write` from the job that toggles workflows.
- Pin every action and reusable workflow. Use one `skills/exercise-toolkit` ref across the whole repository;
  the default is `v0.9.3`. Never pin a draft release, whose tag does not exist.
- Only `Step 0` is enabled on a fresh copy. Every other step workflow ships disabled and is enabled by the
  previous step.
- Guard the start workflow with `if: !github.event.repository.is_template`.
- Make check workflows fail helpfully before they pass. Every check uses `continue-on-error: true` and a row
  in the `step-results-table.md` `results_table`.
- Update the existing feedback comment via `peter-evans/find-comment` rather than posting duplicates. Always
  scope the lookup with `comment-author` and `body-includes`: a bare `direction: last` returns whatever was
  posted most recently, so `edit-mode: replace` can overwrite a learner's own comment.
- Avoid hardcoded repository-specific URLs in source Markdown; render them at runtime.
- Prevent one-shot bootstrap workflows from overwriting legitimate later edits.
- Use `paths` filters on push-based triggers where practical to avoid accidental transitions from unrelated
  commits.
- Ensure the last step finishes the exercise instead of enabling a non-existent next step.

## Step content requirements

Every `.github/steps/N-step.md` must contain:

- one `## Step N: <name>` heading,
- exactly one `### 📖 Theory: <title>` heading followed by real awareness-level content,
- at least one `### ⌨️ Activity: <title>` heading followed by numbered instructions,
- a `Having trouble? 🤷` `<details>` block with recovery hints.

## Activity block conventions

Inside an Activity, every Copilot prompt and every terminal command uses a badge-led blockquote: badge line,
a bare `>` line, then the fenced block inside the same blockquote, indented to align under its numbered list
item. Use the badge URLs verbatim and keep the alt text `Static Badge`.

Copilot Chat / IDE prompt:

```markdown
1. Ask Copilot Chat to summarize the change.

   > ![Static Badge](https://img.shields.io/badge/Prompt-text?style=for-the-badge&logo=github-copilot&logoColor=white&labelColor=purple&color=purple)
   >
   > ```text
   > Summarize the changes in this pull request.
   > ```
```

Copilot CLI prompt:

```markdown
1. Run the prompt with Copilot CLI.

   > ![Static Badge](https://img.shields.io/badge/CLI-Prompt-text?style=flat-square&logo=github-copilot&labelColor=8250df&color=fbefff)
   >
   > ```text
   > Explain what this workflow does.
   > ```
```

Terminal command:

```markdown
1. Run the command.

   > ![Static Badge](https://img.shields.io/badge/Terminal-text?logo=gnometerminal&labelColor=0969da&color=ddf4ff)
   >
   > ```bash
   > gh repo view
   > ```
```

## Content formatting conventions

- Store exercise images in `.github/images` and reference them with a relative path such as
  `../images/inspectocat.png`. Always provide meaningful alt text.
- Keep GitHub callouts left-justified (no indentation) when they are not nested in a list item.
- Use this exact style:

> [!NOTE]
> This is a note

> [!IMPORTANT]
> This is an important item to be aware of for this exercise

> [!TIP]
> It is a good idea and recommended to do this tip

## Completion gates

Do not report the bootstrap as done until all of these hold:

1. No placeholder text remains in `README.md` or `.github/` — not only `replace-me`, but also bare skeleton
   tokens (`OWNER`, `REPO`, `ORG`, `TITLE`, `FEATURE`, `VISIBILITY`) and bracketed slots such as
   `[Step name]` or `[Action]`.
2. Every step file has exactly one Theory heading with content and at least one Activity heading with
   numbered instructions.
3. Required files exist (`README.md`, `.github/steps/x-review.md`, `.github/workflows/0-start-exercise.yml`),
   there is at least one numbered step, step content and step workflows line up by number, each workflow's
   declared `name: Step N` matches its filename number, and the final workflow is `N-last-step.yml` for the
   highest step.
4. Every `gh workflow enable "Step N"` names a workflow that exists, and the final workflow enables nothing.
5. Every `STEP_N_FILE` and `REVIEW_FILE` value points at a file that exists, and the final workflow
   references `REVIEW_FILE`.
6. Every `skills/exercise-toolkit` reference uses the same pinned tag, and no toolkit checkout is unpinned.
7. `post_next_step_content.needs` includes `check_step_work` when that job exists, and does not reference it
   when it does not.
8. All workflow YAML parses.
9. The README Copy Exercise badge uses the correct `template_owner` and `template_name`.
10. The start workflow has a real first-run trigger enabled, not only `workflow_dispatch` — or the README
    explicitly tells the learner to start the exercise by running the workflow manually. The advertised
    "copy and wait" start path must have an event behind it.

The contract reference includes a copy-ready command block that mechanically verifies gates 1 through 8.
Gates 9 and 10 are judgement calls and need a human read.

## Report back

When the build round finishes, tell the user:

- the files created or changed,
- which steps are graded and what each grading check asserts,
- anything you had to decide on their behalf,
- what to review first.

Then stop and wait for approval or change requests before starting another round.
