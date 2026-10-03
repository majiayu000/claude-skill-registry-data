---
name: create-pr
description: Create a draft GitHub PR from the current feature branch with a convention-aware title and body. Use when the user asks to create, prepare, draft, or open a pull request.
---

# Create PR

Create a draft GitHub PR from the current branch with a convention-aware title and body.

This skill has remote side effects: it may push the current branch and create a PR on GitHub. Do not push or create the PR until the user explicitly approves the PR description and confirms creation.

## Inputs

Parse any PR options from the user's request before gathering context:

- `--base <branch>`: use this branch as the PR base.
- `--branch <branch>`: alias for `--base <branch>`.
- `--title <title>`: include this title as the first title suggestion.

If the user provides an unknown flag or a flag missing a required value, report valid usage and stop.

## User Questions

When user input is needed, ask in plain chat text with concise numbered options. This keeps the skill compatible with Codex and other chat-only runners.

Ask the user when:

- Selecting or confirming the base branch.
- Uncommitted changes exist and the user must decide whether to continue.
- The generated PR title needs user selection or editing.
- The generated PR description needs explicit approval.
- The final push and PR creation needs confirmation.

Question rules:

- Do not depend on an interactive selector UI.
- Do not say that an interactive selector cannot be rendered.
- Put the recommended option first when there is one.
- Let the user answer with a number, exact option text, or free-form replacement.

## Step 1: Select and Validate Base Branch

Confirm the working tree is on a feature branch and has commits to submit.

1. Get the current branch:
   ```bash
   git branch --show-current
   ```
2. Resolve the base branch explicitly:
   - List local branches:
     ```bash
     git branch --format='%(refname:short)'
     ```
   - If `--base` or `--branch` was provided, include that value as the first option.
   - Otherwise, if a likely default branch is known from `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, put it first.
   - Ask the user `Which base branch should I create the PR against?` in plain chat text.
   - Show branch choices as a numbered list, with the recommended branch first.
   - If the user provides free-form input, treat it as the base branch.
3. If the current branch is the base branch, output `Nothing to submit -- current branch is the base branch.` and stop.
4. Fetch the base branch:
   ```bash
   git fetch origin <base> --quiet
   ```
5. Count commits ahead:
   ```bash
   git rev-list --count origin/<base>..HEAD
   ```
6. Check local changes:
   ```bash
   git status --short
   ```

If there are zero commits ahead and no uncommitted changes, output `Nothing to submit -- no commits ahead of base branch.` and stop.

If there are uncommitted changes, tell the user that uncommitted changes will not be included in the PR. Ask whether to continue using a plain-text yes/no question. If the user declines, stop.

## Step 2: Learn PR Conventions

Examine recent merged PRs to infer the repository's PR style:

```bash
gh pr list --state merged --limit 5 --json title,body,number
```

Analyze the returned PRs for:

- Title format: prefixes such as `feat:`, `fix:`, ticket IDs, capitalization, and length.
- Body style: how much context they include, when they use headings, how they link issues, and how casual or formal the writing is.
- Code links: prefer full GitHub `blob/<sha>/path#Lx-Ly` links for important ranges. GitHub renders linked code snippets in the PR, which makes reviews easier. Example: `https://github.com/a4s-lab/spreadsheet/blob/44aa272358fa048cfe2c52b0c6dccdb182513bc2/crates/workbook/src/operation.rs#L357-L370`.

If no merged PRs exist or `gh pr list` fails, use a concise body with only the sections that help this PR.

## Step 3: Gather Diff and Commit History

Collect enough context to write the PR:

```bash
git log --oneline origin/<base>..HEAD
git log --format="%h %s%n%n%b" origin/<base>..HEAD
git diff --stat origin/<base>...HEAD
git diff origin/<base>...HEAD
```

For large diffs, focus on `git diff --stat` and read changed files selectively. Do not paste long raw diffs into the final response.

## Step 4: Generate and Confirm PR Title

Generate 2-3 title suggestions from the conventions and branch diff, then ask the user to choose or edit the title.

Title rules:

- Match the repository's recent PR convention.
- If `--title` was provided, include it as the first suggestion.
- If no convention is detected, use a concise imperative title.
- Keep the title under 72 characters.

Ask in plain chat text:

```text
Which PR title should I use? Reply with a number, or type an edited title.

1. <suggested title>
2. <suggested title>
3. <suggested title>
```

If the user replies with a number, use that suggestion. If the user types free-form input, use that as the final title.

## Step 5: Generate and Approve PR Description

Generate a PR description that fits this repository and this change. Choose the smallest useful structure based on recent merged PRs, the commit history, and the diff.

Recent `a4s-lab/spreadsheet` PRs are good examples: short opening context, a few targeted links, and extra explanation only when the implementation is non-obvious.

Writing rules:

- Start high level: what this PR enables or fixes, not how every file changed.
- Keep it concise. Reviewers dislike text-heavy descriptions.
- Use markdown for scanability: short paragraphs, bullets, and headings only when they help.
- No strict template. Decide section breaks per PR. A forced `Summary / Changes / Tests` shape can look generated.
- Do not list every changed file.
- Link important code ranges with full GitHub URLs so GitHub shows code snippets inline.
- Explain complex or surprising implementation choices, but stay out of low-level narration.
- Casual fragments are fine in bullets. They do not all need to be complete sentences.
- Mention issue links, validation, screenshots, rollout notes, breaking changes, or follow-ups only when useful.

A good description may be as small as:

```markdown
This PR implements `Operation::SetCellFormats` and `Operation::ClearCellFormats`.

https://github.com/a4s-lab/spreadsheet/blob/44aa272358fa048cfe2c52b0c6dccdb182513bc2/crates/workbook/src/operation.rs#L357-L370

The old `FormatStore` had behavior that did not match the spreadsheet model, so this redesign moves the store under `sheet/stores` and keeps changed ranges sparse for reviewers to inspect.

Please refer to #143 for the background.
```

After generating the description, show the full proposed description and ask for explicit approval in plain chat text:

```text
Use this PR description?

1. Approve description
2. Regenerate description

Or type requested edits.
```

If the user types requested edits, revise the description once using those edits and ask for approval again. Do not create the PR until the user approves the final description.

## Step 6: Confirm and Create PR

Before any remote side effect, show:

- Base branch
- Current branch
- Draft mode: always enabled
- Final title
- Approved description

Ask for confirmation in plain chat text. If the user does not confirm, stop without pushing or creating a PR.

After confirmation:

1. Push the current branch:
   ```bash
   git push -u origin <current-branch>
   ```
2. Create the draft PR:
   ```bash
   gh pr create --draft --base <base-branch> --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```
3. Output the PR URL returned by `gh pr create`.

If `git push` or `gh pr create` fails, report the exact failure and stop.
