---
name: sk-pr
description: Create or update a GitHub pull request via gh CLI. Use when the user wants a PR, pull request, gh pr create/edit, or provides a PR number or URL.
---

# PR

Create or update a GitHub PR for the current branch.

## Slug and flow folder

1. If the user provided a slug, use `.agents/flows/sk-<slug>/`.
2. Else inspect root runbooks. For a multi-PR runbook, use its exact `Active PR` and matching `Directory`; for a single-PR runbook, use the root. Require `4 - REVIEW.md` and missing `6 - PR.md` there.
3. Read the exact active plan (`2 - PLANNING.md`) and other phase docs in the selected flow or PR directory.
4. After creating/updating the PR, write `6 - PR.md` and set `RUNBOOK.md` row `6` to `done`.

## Active PR handoff

When the root runbook is multi-PR, fetch refs before this phase and verify the checked-out branch and HEAD against the active PR row. Use the harness-supported sync workflow and record the resulting HEAD in the active PR runbook. If the branch or HEAD cannot be reconciled safely, mark the PR blocked and stop instead of reviewing or changing the wrong diff.

## Route: update or new

1. If the user gave a PR number or GitHub PR URL, use **update** with that number.
2. Else run `gh pr view --json number,headRefName,title` from the repo root. If it succeeds, use **update**.
3. Else use **new**.

**Update guard:** before editing, confirm `gh pr view <n> --json headRefName -q .headRefName` matches `git branch --show-current`. If not, stop and tell the user.

## Environment and git

- Run `gh` from the repo root with network access.
- Warn and stop if the current branch is `main` or `master` unless the user overrides.
- Do not stage or commit uncommitted changes without permission.
- Base diff for context: `git diff origin/<default>...HEAD`, where `<default>` is `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (fallback `main`, then `master`).

## Corporate mode

1. **Overrides:** `PR_SKIP_JIRA` (non-empty) → off. `PR_REQUIRE_JIRA` → on even on `github.com`.
2. **Otherwise:** run `gh repo view --json url -q .url` and parse the host. Corporate is **off** for `github.com`, `gist.github.com`, `gitlab.com`, `codeberg.org`, `bitbucket.org`, `dev.azure.com`, `ssh.dev.azure.com`. **On** for any other host.
3. If `gh repo view` fails, default off.

In corporate mode, link any ticket key/URL found in user input, branch, or commits; use a placeholder like `PROJ-123` if none found. On `gh pr create`, append `--label "code-review:request"` if the repo supports it.

In OSS/standard mode, use a conventional-commit title (e.g. `feat(scope): add thing`). Add one linked issue/ticket line in the body only if the user provided it. Do not add the `code-review:request` label.

## Title and body

- **Keep the title and body short, clear, and concise.** Title is one line; body is brief and reviewer-focused.
- **With ticket key:** `<KEY>: <summary>` (e.g. `PROJ-123: feat(auth) add sso login` — omit a second colon after type/scope to avoid `::`).
- **Without:** `<conventional-commit-style summary>` (e.g. `feat(auth): add sso login`).
- **Body:** what changed, what files/areas, behavior added/changed/removed, linked issue/ticket. Avoid commit-by-commit narrative and long explanations.
- Regenerate the full body from scratch unless the user asks to preserve it.

## Template and checklists

- Search for `PULL_REQUEST_TEMPLATE.md` under `.github/`, `docs/`, and `.gitlab/`.
- If found, match its sections/headings.
- If missing, use a minimal body: Context, Changes, Related Issue/Ticket.
- Check `- [x]` only when clearly supported by evidence; leave `- [ ]` when unsure.

## Run gh

1. Compose the body and write it to `.pr-body-temp.md` in the repo root.
2. **Create:** `gh pr create --title "<title>" --body-file .pr-body-temp.md` (append `--label "code-review:request"` in corporate mode).
3. **Update:** `gh pr edit <n> --title "<title>" --body-file .pr-body-temp.md`.
4. Write `6 - PR.md` and update `RUNBOOK.md` row `6`.
5. **Always delete** `.pr-body-temp.md` last, even on failure.

## Troubleshooting

- `gh` not found/auth errors: tell the user to run `gh auth login` (and `gh auth refresh` if needed).
- Wrong repo: run commands from the project root.
- Ambiguous PR: use `gh pr view <n> --repo owner/name` when the user specifies the repo.

## Multi-PR completion

After writing the active PR's `6 - PR.md`, update its root initiative row with the PR URL, state `done`, branch, base SHA, and final HEAD. Select the first `pending` row in order whose dependencies are all `done`, set it to `in-progress`, and set `Active PR` to that slug. If no pending PR remains, set `Active PR: none` and the initiative status to `completed`. If pending PRs remain but none is unblocked, set `Active PR: none`, mark the initiative `blocked`, and record the unmet dependencies.
