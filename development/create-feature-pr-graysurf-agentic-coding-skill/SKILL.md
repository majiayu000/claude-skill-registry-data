---
name: create-feature-pr
description: Create a new feature branch, implement feature work, commit with commit-message, and open a PR with gh using standardized templates. Use when the user asks to develop a new feature, start a feature branch, or open a feature PR; also when asked to draft a feature PR based on the latest commit message.
---

# Create Feature PR

## Setup

- Load commands with `source $CLI_TOOLS/tools.sh`

## Inputs

- Prefer explicit user feature description and acceptance criteria.
- If missing, read the latest commit message: `git log -1 --pretty=%B`.
- If still unclear, ask for a 1-2 sentence feature summary and expected behavior.

## Branch naming

- Prefix: `feat/`.
- Build the slug from the feature summary or latest commit subject.
- Slug rules: lowercase; replace non-alphanumeric with hyphens; collapse hyphens; trim to 3-6 words.
- If a ticket ID like ABC-123 appears, prefix it: `feat/abc-123-<slug>`.

## Workflow

1. Confirm the working tree is clean; stash or commit if needed.
2. Determine the base branch (default `origin/HEAD`); ask if unclear.
3. Create the branch: `git checkout -b feat/<slug>`.
4. Implement the feature with minimal scope; avoid unrelated refactors.
5. Add or update tests when reasonable; run available lint/test/build commands.
6. Commit using the `commit-message` skill; prefer a single commit unless splitting is justified.
7. Push the branch and open a PR with `gh pr create` using `references/PR_TEMPLATE.md`.

## PR rules

- Title: capitalize the first word; reflect the feature outcome; do not reuse the commit subject verbatim.
- Replace the first H1 line in `references/PR_TEMPLATE.md` with the PR title.
- Always include Summary, Changes, Testing, and Risk/Notes sections.
- If tests are not run, state "not run (reason)".
- Use `scripts/render_feature_pr.sh --pr` to generate the PR template quickly.

## Output

- Use `references/OUTPUT_TEMPLATE.md` as the response format.
- Include `git-scope` output after commit using `git-scope commit HEAD --no-color`.
- Use `scripts/render_feature_pr.sh --output` to generate the output template quickly.
