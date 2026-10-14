---
name: pr-description
description: Write or update the description of a DeltaTrack pull request. Use when opening a PR against develop or rewriting a PR body.
---

# Writing a DeltaTrack pull request description

The rules live in CONTRIBUTING.md "Submitting a pull request" and "Writing the
description"; AI disclosure is under "AI-assisted contributions". The shape is
`.github/pull_request_template.md`. Read those, then fill the template's sections in
order rather than replacing them:

1. **Related issue.** One closing keyword per issue, spelled exactly:
   `Closes #123, closes #124`. Use `Refs #123` instead when merging this PR won't finish
   the issue's "Done when" list, and say which items it covers.
2. **What does this change?** The behaviour change in plain words first, then files.
   Self-describing cross-references (`#141 (enrolled PDFs yield no anchors)`).
3. **How to test.** The commands you actually ran and what you checked: bill and
   versions compared, what the report showed. For a bug fix, confirm the new test
   fails without the fix. Never quote a result you didn't run.
4. **Checklist.** Tick only what's true.
5. **AI assistance.** Name the tool; one line is enough.

Also say what the PR deliberately leaves out, with the issue that owns it.

## Before opening

- Branch from and target `develop`, never `main`.
- Run the CI gates in CONTRIBUTING.md "What CI checks" and report their result.
- Keep one concern per PR. Unrelated fixes get their own PR.
- After opening, check the issue shows the PR under "Development". If it doesn't,
  the keyword didn't parse; fix the description.
