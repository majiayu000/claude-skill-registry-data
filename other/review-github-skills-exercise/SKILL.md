---
name: review-github-skills-exercise
description: "Review GitHub Skills exercises for learner experience, validation correctness, workflow safety, accessibility, and publish readiness. Use this whenever the user asks to audit, review, improve, QA, or validate a GitHub Skills-style exercise repository or draft."
---

# Review GitHub Skills exercise

Use this skill to review an exercise draft with a high signal-to-noise ratio.

## Review process

1. Read the README and identify the promised learner outcome.
2. Trace the learner journey from start through completion.
3. Verify every step has a Theory block with real content and at least one Activity block.
4. Inspect workflows, local actions, scripts, and templates that drive validation or feedback.
5. Check template parity: file/workflow numbering, toolkit ref consistency, chaining, and leftover
   placeholders.
6. Check tests or validation docs.
7. Report only findings that affect learning, reliability, safety, accessibility, or publication.

## Rubric

### Step content completeness (blocking)

- Every `.github/steps/N-step.md` has exactly one `### 📖 Theory:` heading followed by real
  awareness-level content. A Theory heading with no content, or a step with no Theory block, is a blocking
  finding.
- Every step has at least one `### ⌨️ Activity:` heading with actionable numbered instructions. A step with
  no Activity block is a blocking finding.
- Theory content is tied to the Activity in the same step, not generic background.
- Every step has a `Having trouble? 🤷` recovery block.

### Learner experience

- The start path is obvious.
- Each step explains what to do and why it matters.
- Feedback helps the learner recover from common mistakes.
- Completion is visible and satisfying.

### Template parity

- Step files and step workflows align by number (`N-step.md` ↔ `N-step.yml` ↔ `name: Step N`).
- The final workflow is `N-last-step.yml` and posts `.github/steps/x-review.md`.
- Every `gh workflow enable "Step N"` names a workflow that exists.
- Every `STEP_N_FILE` and `REVIEW_FILE` value points at a file that exists.
- Every `skills/exercise-toolkit` reference uses the same pinned release tag, none use `@main`, and the
  pinned tag actually resolves (a draft release has no git tag and will break every workflow).
- If `check_step_work` exists, `post_next_step_content.needs` includes it; if it was removed, `needs` is back
  to `[find_exercise]`.
- The start workflow is guarded with `if: !github.event.repository.is_template`.
- The start workflow has a real first-run trigger, not only `workflow_dispatch`, unless the README explicitly
  tells the learner to start it manually. A README promising an automatic start with no event behind it
  leaves the learner on an apparently broken repository.
- No placeholder text remains in `README.md` or `.github/`: not only `replace-me`, but bare skeleton tokens
  (`OWNER`, `REPO`, `ORG`, `TITLE`, `FEATURE`) and bracketed slots such as `[Step name]`.
- The README Copy Exercise badge uses the correct `template_owner` and `template_name`.

### Activity block conventions

- Every Copilot prompt and terminal command inside an Activity uses a badge-led blockquote.
- Copilot Chat/IDE prompts use the purple `Prompt` badge; Copilot CLI prompts use the `CLI-Prompt` badge;
  terminal commands use the blue `Terminal` badge.
- Badge URLs are unmodified and alt text is `Static Badge`.
- Blockquote indentation aligns under its numbered list item so ordered-list numbering does not break.

### Validation reliability

- Checks verify the intended behavior.
- Failing states produce actionable messages.
- Success criteria are neither too loose nor too brittle.
- Re-running the exercise does not create confusing duplicate state.
- Step workflow variables match the template variables used in rendered markdown.
- Every grading check uses `continue-on-error: true` with a matching `results_table` row, and the job closes
  with `if: contains(steps.*.outcome, 'failure')`.

### Workflow safety

- Workflow permissions are least-privilege and granted per job, not workflow-wide. A workflow-level grant
  applies to every job, so check that the learner-triggered grading job does not inherit `actions: write`
  from the job that toggles workflows, and does not hold `contents: write` unless it actually commits.
- Automation does not overwrite learner or maintainer work unexpectedly.
- Issue comments use stable markers if they are updated. Any `find-comment` feeding an `edit-mode: replace`
  is scoped by `comment-author` and `body-includes`, so it cannot overwrite a learner's comment.
- Repository-specific links are rendered safely.
- Step 0/start behavior does not require manual workflow disabling and leaves expected step workflows off.
- Exercise workflows are disabled by default before publication and only run as the learner progresses.

### Accessibility and maintainability

- Images have useful alt text.
- Images are stored in `.github/images` and referenced with relative paths.
- Links are descriptive.
- Markdown is readable in GitHub.
- Repeated logic is shared or documented.
- Ordered activity steps render with correct numbering (no broken lists caused by mixed blocks).
- `[!NOTE]`, `[!IMPORTANT]`, and `[!TIP]` callouts are left-justified (no indentation).

Expected callout formatting:

> [!NOTE]
> This is a note

> [!IMPORTANT]
> This is an important item to be aware of for this exercise

> [!TIP]
> It is a good idea and recommended to do this tip

## Output format

```markdown
## Overall readiness

## Blocking findings

## Important findings

## Nice to improve

## Suggested validation
```

If no issues are found in a category, say `None`.
