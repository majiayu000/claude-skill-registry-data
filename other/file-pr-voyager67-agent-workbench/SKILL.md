---
name: file-pr
description: Prepare a clear pull request from an existing branch and diff. Use when asked to open or draft a PR; do not invent test results or scope.
---

# File a Pull Request

1. Read the original issue/request and inspect the complete diff against the target base.
2. Verify the working tree, branch, commit set, and repository/remote. Check for secrets, generated clutter, unrelated files, and accidental personal data.
3. Write a title that names the outcome. Lead the body with the problem and user impact, then explain the approach and key behavior changes.
4. Include evidence: tests/builds run, manual checks, screenshots or benchmark data only when actually available.
5. State risks, compatibility notes, rollout/migration needs, and what remains unverified.
6. Keep the PR concise; link relevant issues only when the relationship is real.
7. Ask before pushing or opening the PR if authorization is unclear.

Do not write a change inventory as the main summary. Never claim full test coverage or use fabricated screenshots. Do not request reviewers, labels, milestones, or merge the PR unless asked.
