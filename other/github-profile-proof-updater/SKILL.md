---
name: github-profile-proof-updater
description: Refresh and verify a GitHub profile or public proof layer. Use when the user wants to update GitHub profile visuals, replace README assets while preserving paths, audit profile image references, validate live GitHub rendering, prepare LinkedIn/X proof copy, or document a profile-refresh proof trail.
---

# GitHub Profile Proof Updater

## Overview

Use this skill to turn a GitHub profile or proof-layer refresh into a repeatable, public-safe workflow: update visuals, preserve working README paths, verify the live page, and create the social/proof trail that explains the update.

Do not publish, commit, push, upload, or post externally unless the user explicitly asks for that action.

## Workflow

1. Confirm the target repo and the source asset folder.
2. Inspect the current repo state:
   - `git status --short`
   - README image references
   - target asset filenames and dimensions
3. Preserve existing public paths unless the user asks for a rename in README.
   - Prefer replacing assets under the old filenames.
   - Keep known-good hero images unchanged when the user says the hero is already good.
4. Copy or replace only the intended assets.
5. Validate the changed media:
   - destination files exist
   - images are readable
   - dimensions/aspect ratios are plausible for the README layout
6. Re-check README references.
   - Edit README only if an image path is broken, missing, or intentionally changing.
7. Review the diff and repo status.
   - Never use broad staging until the changed files are understood.
   - Prefer staging named files only.
8. If the user asks to commit/push, commit with a focused message and push the current branch.
9. Verify the live GitHub profile or public repo page after push.
   - Check that all updated visuals render.
   - Confirm the unchanged hero remains correct.
   - Capture any broken image, stale cache, or layout issue.
10. Create or update the proof trail:
   - public GitHub links
   - commit links or hashes
   - asset summary
   - LinkedIn/X post links when available
   - follow-up checklist

## Public Safety Rules

- Do not include local machine paths, private vault structure, raw prompts, logs, credentials, browser cookies, private repo names, account identifiers, or client data in public files.
- Screenshots must not reveal private tabs, emails, analytics, billing, dashboards, file paths, or account menus.
- Social copy should describe outcomes and workflow categories, not private implementation details.
- If a public artifact is being prepared, apply the `github-safe-publisher` rules and run its scanner when available.

## Social Proof Handoff

When the user wants LinkedIn or X copy for the refresh:

- Lead with the public proof angle.
- Keep LinkedIn reflective and explanatory.
- Keep X shorter, with one idea per post.
- Add alt text for every image.
- Put related X posts into a thread, not scattered comments.
- Track published links in a proof trail or engagement tracker.

## Output Format

Return:

1. Verdict: `BLOCK`, `REVIEW`, or `READY`.
2. Target repo and files changed.
3. Validation performed.
4. Live verification result, if applicable.
5. Proof/social artifacts created or updated.
6. Next recommended action.
