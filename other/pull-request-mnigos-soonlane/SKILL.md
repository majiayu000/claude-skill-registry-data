---
name: pull-request
description: Use when the user asks to open, create, or prepare a GitHub pull request from the current branch.
---

# Pull Request

Use this skill when the user asks for a PR.

## Related Skills

- Commits follow Conventional Commits; `commitlint` checks them in the `commit-msg` hook and in CI.

## Flow

1. Inspect branch, status, recent commits, and diff against the base branch.
2. If uncommitted changes exist, identify those within the requested scope and commit only those. The PR request authorizes the necessary commits and push; do not ask for separate confirmation.
3. Fetch the base branch and rebase the PR branch onto the latest base before creating the PR.
4. Push the current branch.
5. Open a ready-for-review PR unless the user says otherwise. Dependent PRs form a native GitHub stack; never fake a stack with chained bases alone.
6. Write the description with the format below; include validation, important risks, and the linked issue when discoverable.
7. For UI changes, upload and embed screenshots in the PR description using the rules below.
8. Before reporting the PR as ready, verify it on GitHub, not locally: `gh pr view --json mergeable,mergeStateStatus` shows `MERGEABLE`, `gh pr checks` has no failing or pending check for the current head, and the UI screenshot checklist below is complete. A local rebase or a green local check is not evidence; if anything is red, pending, or conflicting, say so instead of calling the PR ready.

## Description Format

The description is a guide for a reviewer, not a change log. A reviewer should absorb it in under a minute.

- Open with 2–3 short sentences: what was wrong or missing, what this PR does, what it leaves out. No heading above them.
- Then, in this order and only when non-empty: `## What changes`, `## How to review` (large PRs only: where to start, one sentence), `## Validation` (one sentence: what ran and the numbers), `## Deploy` (migrations, Vercel env, Google OAuth or manual steps), then `Closes #<issue>` when an issue exists.
- `What changes` is at most five bullets, each one line, each describing an effect a reviewer can see, not an internal mechanism.
- Hard caps: 120 words for a small PR, 200 for a large one. At most one backticked name per bullet or sentence, and only when the reviewer has to open it. No file inventories, no env var lists, no decision essays, no review-round history, no tool attribution.
- Anything longer belongs in the module README or an ADR; link it instead of repeating it.
- Screenshots follow the UI rules below.

## UI Screenshots

- Every PR that changes visible UI requires screenshots of the affected views at desktop and mobile sizes, including relevant open dialogs, menus, or other changed states. UI work is incomplete until the screenshots are attached and verified.
- Capture the running application at the latest PR revision. Inspect each image to confirm that it shows the intended view and state. Refresh screenshots after subsequent changes that affect their appearance or behavior.
- Upload screenshots as GitHub attachments and embed their URLs in the PR description with descriptive labels. Before requesting browser login, check authenticated CLI attachment support, including a current official CLI if the installed version lacks it. Prefer `gh pr edit --attach` when available. Preserve private-repository access restrictions. Do not leave local paths in the saved description or commit screenshot files for it.
- Stack screenshots vertically, one image per row with a descriptive caption above. Never use tables or grids. Desktop screenshots use the full available width; only mobile screenshots may use a narrower display width.
- Label sample or mocked data. Isolated component previews may supplement application screenshots; they do not replace them or count as end-to-end verification.
- Exclude secrets and personal customer data from uploaded images.
- Read back the saved PR description and verify every image references an uploaded attachment. Visually inspect every attached image in the rendered PR; if the browser lacks private-repository access, use authenticated API readback and download each attachment for visual inspection. Local originals, images shown only in chat, DOM checks, and passing checks do not substitute for verifying the saved body and actual uploaded images.
- If capture or upload fails, keep working through available tools and authentication flows allowed by the active browser and security rules. If still blocked, report the concrete blocker and missing captures, and state that screenshot verification remains incomplete. Reporting a blocker does not complete UI work.

## Rules

- Always open ready-for-review PRs unless the user says otherwise.
- A PR request authorizes scoped commits, push, and PR creation without separate permission.
- Do not prefix branches with `codex/`, `claude/` or `t3code/`.
- Do not create GitHub comments or discussions unless explicitly asked.
- Do not create new labels.
- Before creating a PR, run `git fetch origin <base>` and `git rebase origin/<base>`; after rebasing an already-pushed PR branch, push with `--force-with-lease`.
- Use `gh` for GitHub operations.
- Every Vercel preview runs its own build and migrations against the Neon `preview` branch; mention a migration in `## Deploy`.
- Before editing files while preparing a PR, read at least 3 similar files.
