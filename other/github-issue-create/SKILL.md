---
name: github-issue-create
description: Use when the user wants to create GitHub issues from a discussion, investigation, rough idea, plan, bug report, feature request, or a conversation meant to discover the right issue breakdown.
---

# GitHub Issue Create

## Scope

Use this skill to turn user intent into one or more well-scoped GitHub issues
in the current repository. The input may be an existing discussion, an
investigation result, a rough idea, or a live conversation whose purpose is to
discover what issues should be created.

Do not assume the result is exactly one issue. Split the work when separate
deliverables, dependencies, risk areas, or parallel workstreams would make the
issues easier to implement and review.

## Workflow

1. Resolve the current repo from local git context.
2. Understand the source material.
   - If the current conversation already contains enough context, summarize it into issue-ready points.
   - If the user wants to talk through an issue before creating it, ask focused questions one at a time until the problem, desired outcome, constraints, and acceptance criteria are clear.
   - If the request is vague or too broad, help narrow it before drafting issues.
3. Check the repository's GitHub issue template files before drafting issues.
   - Look for markdown templates and issue forms under `.github/ISSUE_TEMPLATE/`.
   - If there are multiple templates, infer the best fit for each proposed issue from the content.
   - If the best template for an issue is unclear, ask instead of guessing.
4. Decide the issue breakdown.
   - Prefer one issue when the work has one clear outcome and one implementation path.
   - Split into multiple issues when the work has independent deliverables, different owners/subsystems, meaningful sequencing, or parts that can be implemented in parallel.
   - Identify dependencies between proposed issues.
   - Estimate each issue's touched areas: the files, directories, or modules it is expected to change, plus shared resources such as schemas, config, migrations, lockfiles, or public interfaces.
   - When otherwise parallel issues need the same schema, interface, config, workflow, or policy decision, extract that decision into a precursor issue that settles the contract, and make the dependent issues blocked by it instead of serializing all of them.
   - Group issues into waves: each wave contains issues whose dependencies are all in earlier waves. Mark issues in the same wave as parallelizable only when their touched areas do not overlap.
   - Propose a tracker issue only when there are 3 or more child issues, or when dependencies/order make a coordination issue useful.
5. Draft each issue title and body from the chosen template.
   - Carry over template defaults such as labels or assignees when the template makes them clear and they fit the issue.
   - If the repository uses an issue form, convert the form fields into an equivalent markdown issue body.
   - If no issue template exists, fall back to a compact generic issue body with `Summary`, `Background`, `Acceptance Criteria`, `Implementation Notes`, `Touched Areas`, `Dependencies`, and `Parallelization`.
   - When the chosen template has no equivalent fields, append `Touched Areas` and `Dependencies` sections after the template content.
   - Write touched areas as a list of repository paths or module names, marking each entry as an estimate.
   - Write dependencies as one `Blocked by #<n>` line per blocking issue so other skills can parse them. Use a placeholder such as `Blocked by <precursor title>` in the preview and replace it with the real number at creation time.
   - Include only facts supported by the discussion, investigation, repository context, or user-provided requirements.
   - Leave unknowns as explicit open questions instead of inventing answers.
6. Show a preview before creating anything:
   - proposed issue count and why that split is appropriate
   - tracker issue, if proposed, with why it is useful
   - for each issue: chosen template, title, body, labels or assignees if any, touched areas, dependencies, and parallelization notes
   - the waves, any precursor issues and the contract each one settles, and any touched-area overlaps that kept issues out of the same wave
   - the GitHub relationships that will be registered: sub-issue links to the tracker and `blocked by` dependencies
   - the exact creation order when dependencies exist
7. Wait for explicit user confirmation before creating any issue.
8. After confirmation, create the GitHub issues in dependency-aware order.
   - Create tracker issues before child issues when a tracker was approved.
   - Create blocking issues before the issues they block, so every `Blocked by #<n>` line uses the real issue number.
   - Link related issues in their bodies when useful.
   - Register the previewed relationships with GitHub's native features: add child issues as sub-issues of the tracker, and add each `Blocked by #<n>` as an issue dependency. Both APIs take the issue's database `id`, not its number.
   - If a relationship API is unavailable or fails, keep the body text as the source of truth, continue, and report which relationships were not registered.
   - Do not apply labels or assignees unless they came from the template or the user explicitly approved them.
9. Return the created issue numbers and URLs plus:
   - a short summary of each issue
   - dependencies or suggested implementation order
   - the waves and safe parallel groups, if any
   - any relationships that could not be registered natively
   - the recommended next command, such as `$github-issue-start #<n>` or `$github-issue-start #<a> #<b>`

## Guardrails

- This skill is current-repo only.
- Do not create any issue before showing a preview and receiving explicit confirmation.
- Do not force one broad issue when the work naturally splits into independent or parallelizable issues.
- Do not put issues with overlapping touched areas in the same parallel wave.
- Do not create a tracker issue by default. Propose one only for 3 or more child issues or meaningful dependencies/order.
- If the best template is unclear, say so and ask instead of guessing.
- If required information is missing, ask before creating issues.
- Do not ignore repository issue templates just because a generic issue would be faster.
- Do not close, edit, label, assign, or comment on existing issues unless the user explicitly asks.
