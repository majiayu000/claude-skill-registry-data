---
name: update-learning-logs
description: Update the project learning logs (PowerShell/cmd, Git/GitHub/Copilot, AWS, TypeScript, Next.js/React, Playwright) by merging new knowledge into existing categories across one or more files.
---

# Goal

Keep learning notes searchable by topic (not by date) and continuously improved via **merge updates** (統合アップデート) instead of duplicating entries.

# When to use

Use this skill when:
- We executed or discussed PowerShell/cmd commands.
- We executed or discussed Git/GitHub operations (branches, PRs, Actions, Copilot, MCP).
- We executed or discussed AWS operations (S3/CloudFront/OAC/IAM/AWS CLI).
- We implemented or discussed TypeScript / Next.js / React topics.
- We added or modified Playwright tests, configuration, or debugging steps.

# Target files (choose one or more)

| Topic | File |
|------|------|
| PowerShell/cmd | `docs/command-learning-log.md` |
| Git/GitHub/Copilot/MCP | `docs/git-github-learning-log.md` |
| AWS | `docs/aws-learning-log.md` |
| TypeScript | `docs/typescript-learning-log.md` |
| Next.js/React | `docs/nextjs-learning-log.md` |
| Playwright | `docs/playwright-learning-log.md` |

# Process (multi-file aware)

1. **Collect new learnings** from the current work (commands used, concepts explained, errors encountered, decisions made).
2. **Decide target logs** (one or multiple files) based on topic.
3. For each target file:
   - Locate the existing best-matching category section.
   - **Merge-update** the existing entry:
     - Prefer adding missing sections (基礎/関連/応用/トラブル) over creating a new duplicate entry.
     - If there are duplicates, consolidate into one canonical section and keep the best wording/examples.
     - Keep headings stable so future updates land in the same place.
   - Add a short `学んだ日: YYYY-MM-DD` line when new knowledge was added.
4. **Show the proposed diffs** (file list + what changed) and ask for confirmation if committing.
5. If the user requests commit/push:
   - Stage **only** the learning-log related files (avoid accidental staging of generated artifacts like `playwright-report/`, `test-results/`, etc.).
   - Provide a clear commit message (e.g., `docs: update learning logs (git/github + playwright)`), then push.

# Output checklist

- [ ] Which log files were updated (may be multiple)
- [ ] What knowledge was added (bullets)
- [ ] Any risky commands/topics called out
- [ ] VERIFY commands to re-check
- [ ] Rollback steps (how to revert)
