---
name: gh-create-pr
description: Create a GitHub PR from the current branch. Use when the user asks to "create a PR", "open a pull request", or "submit a PR".
allowed-tools: Bash
---

Create GitHub pull request(s) from the current branch. If this session touched multiple repos (check conversation context, plan issue, or ask the user), create a PR in each repo. Run steps 1-8 for each repo in sequence.

1. **Check state**: Run `git status` and `git branch --show-current`.
2. **Prepare a branch**:
   - Always fetch the latest base branch (main/master) first.
   - If the current branch is main/master, create a new branch off the freshly fetched base. Pick a short, descriptive branch name from the conversation context (e.g. `resource-tags-docs`). Move any uncommitted changes to the new branch.
   - Otherwise, rebase the current branch onto the freshly fetched base. If there are conflicts, stop and ask the user to resolve them.
3. **Handle uncommitted changes**: If there are uncommitted changes on the (now non-master) branch, ask the user if they want to commit first. Do not proceed until the working tree is clean.
4. **Check for leaked references**: Grep the diff and commit messages on this branch for references that the PR's audience cannot see: issues in a personal plan repo, internal issue trackers, or internal URLs. If found, warn the user and fix before proceeding.
5. **Push the branch**: Push the current branch to remote with `git push -u origin`.
6. **Gather context**: Read the git log for all commits on this branch since it diverged from the base branch. If a plan issue was referenced in this conversation, read it for additional context. Check for a PR template at `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md` in the repo. If one exists, use it as the structure for the PR description.
7. **Create the PR**: Always use `gh pr create --web --title <title> --body <body>`. The `--web` flag is mandatory; it opens the browser so the user can review and edit before submitting. Do not use `--edit` (terminal editor, unreliable). Do not omit `--web`.
   - A concise title (under 70 characters)
   - Body: for trivial PRs (single commit, simple change), a few plain-text sentences covering what, why, and how it was tested. For non-trivial PRs (multi-commit, multi-file, or complex changes), use three sections: `## What`, `## Why`, `## Tested`. Use bullet lists when listing multiple changes or test steps. Keep each section concise; reviewers read the diff for details.
     - Size the body to the change's consequence, not to the work behind it: a comment-only fix stays trivial however much investigation established it, while a one-line change to a widely-instantiated module is not.
     - Lead with what the change does for the reviewer rather than the method that found it, and leave evidence, log excerpts and ruled-out hypotheses in the plan issue.
     - Do not restate what the commit messages already say. The PR body adds the overarching why and how it was tested; the per-commit details are in the commits.
   - Link to the plan issue only if it is in the same repo as the PR. Never link to a plan issue in a personal or private repo from a PR in another repo. This applies to the PR description, comments, and commit messages.
   - For PRs to public repos: never reference internal issue trackers or internal URLs.
   - Do not set reviewers or labels.
   - **Footer**: Check for `~/.claude/skills/gh-create-pr/pr-footer.md`. If it exists, append its content to the PR body, separated by `---`. Replace `{{model}}` with the full model slug including version and variant (e.g. "Opus 4.8", "GPT-5.6 Sol"). For non-public repos only, append an HTML comment with session metadata after the footer text (invisible in rendered view): `<!-- session: <name> | dir: <directory> | model: <model> | id: <session-id> -->`. Never add this to PRs in open source repos.
8. **Post-creation**: If creating PRs across multiple repos, cross-link them in each PR description (e.g. "Related: owner/other-repo#N"). Do NOT cross-link from a public repo to a non-public repo.

Rules:
- Never create a PR without pushing the branch first.
- Keep the description concise. No empty boilerplate sections.
- Do not make unverified claims in the PR body or commit messages (e.g. "no functional change", "backward compatible"). Skip claims that don't add value.
