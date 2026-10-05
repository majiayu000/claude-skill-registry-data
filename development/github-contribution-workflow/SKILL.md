---
name: github-contribution-workflow
description: Drive GitHub contributions through the gh CLI — pull requests, issues, GitHub-side file edits, repo secrets, contribution-flow repo settings, submodule pin bumps. Use when about to run `gh pr create` / `gh pr merge` / `gh pr checks` / `gh issue create` / `gh secret set` / `gh api`, or asked "open a PR", "merge this", "bump the submodule". Does NOT cover pure local git, diff-vs-commit sanity (pr-diff-verification), security repo settings (apple-dev-skills:apple-public-repo-security), worktree conflicts (subagent-conflict-detection), plugin distribution (claude-skill-plugin-packaging).
---

# GitHub Contribution Workflow

The `gh`-CLI contribution loop for an agent acting on a GitHub repo: branch →
commit → PR → CI → merge, plus issues, GitHub-side file ops, repo secrets, and
contribution-flow repo settings. Encodes conventions that keep an agent's
contributions reviewable and consistent. Tool-agnostic in spirit; concrete
commands are `gh` + `git`.

## Native mechanism

Claude Code's [Hooks](https://code.claude.com/docs/en/hooks) can intercept and block a tool call before it runs — e.g. a `PreToolUse` hook matching `Bash` can deny a `git push --force` or a bare `rm -rf`. Hooks enforce a hard gate at the tool layer; the `--no-verify` rule and CLEAN-before-merge convention below are conventions this skill asks the agent to follow voluntarily where no hook exists to enforce them.

- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## When to invoke

- Opening or merging a PR; opening or commenting on an issue.
- Creating or editing a file *through GitHub* (API / web flow) rather than a local clone.
- Setting a repo secret or configuring contribution-flow repo settings.
- Checking CI status before a merge; bumping a submodule pin.
- User says "open a PR / issue", "merge this", "set the secret", "configure the repo".

## Scope — what this does NOT own (route to sibling)

- **Verifying the diff matches the commit's claims** before push/PR → `pr-diff-verification`.
- **Security repo settings** (Secret Scanning, push protection, gitleaks, `.gitignore` baseline) → `apple-dev-skills:apple-public-repo-security`.
- **Parallel-session / submodule worktree conflicts** → `subagent-conflict-detection`.
- **Distributing or installing skill plugins** (marketplace, depth-1 rule) → `claude-skill-plugin-packaging`.
- **Pure local git** with no GitHub surface → out of scope.

## Intent → command

| Intent | Command |
|---|---|
| Open a PR | `gh pr create --title "<conventional title>" --body "<body + 🤖 footer>"` |
| Check CI before merge | `gh pr checks <n> --repo <o/r> --watch` ; `gh pr view <n> --json mergeStateStatus` |
| Merge a PR | `gh pr merge <n> --squash --delete-branch` (only when `mergeStateStatus` is `CLEAN`, or `HAS_HOOKS` on GHES) |
| Open an issue | `gh issue create --title "<title>" --body "<body>"` |
| Comment on an issue | `gh issue comment <n> --body "<text>"` |
| Create a new file via GitHub | `gh api -X PUT repos/<o/r>/contents/<path> -f message=… -f content=$(base64) …` (no local clone needed) |
| Edit an existing file via GitHub | Same, plus `-f sha=<current-blob-sha>` (from a prior `GET` on the same path) — omitting it on an update fails with 422 |
| Set a repo secret | `gh secret set <NAME> --repo <o/r>` (interactive paste; see Conventions) |
| List secrets | `gh secret list --repo <o/r>` (names only; values are write-only) |
| Configure merge / branch protection | `gh api -X PATCH repos/<o/r> -F allow_squash_merge=true -F delete_branch_on_merge=true` ; `gh api -X PUT repos/<o/r>/branches/<b>/protection …` |

## Conventions

- **Branch names** use Conventional-Commits-style type prefixes (house convention, not a named spec): `feat/ fix/ chore/ docs/ ci/ refactor/ test/`.
- **PR titles** follow Conventional Commits (some repos enforce this with a CI gate — e.g. a PR-title lint check; a non-conforming title fails the PR).
- **Commit trailer**: end commit messages with the harness's `Co-Authored-By:` trailer (Claude Code adds it by default). **PR body**: end with the 🤖 footer.
- **Merge**: `--squash --delete-branch`. **Never merge unless `mergeStateStatus` is `CLEAN` (or `HAS_HOOKS` on a GHES instance with pre-receive hooks) and `pr-diff-verification` has passed** — `gh pr checks` itself never prints `CLEAN`; that's a `gh pr view --json mergeStateStatus` value, not a `gh pr checks` state. Use `gh pr checks <n> --watch [--fail-fast]` to wait for checks — it blocks until nothing is pending: exit `0` = all pass, any other non-zero = a check failed (fail-fast returns before pending clears). Exit `8` ("still pending") is a *plain, non-watch* `gh pr checks <n>` result, not a `--watch` outcome. `BLOCKED` covers more than pending checks — it also covers a failed required check, a missing review, or an unresolved conversation — so don't poll it indefinitely assuming it will clear on its own; also watch for `UNSTABLE` (a non-required check failing) and `BEHIND` (branch needs updating against base).
- **Secrets**: `gh secret set <NAME>` **without `--body`** — a literal `--body "$TOKEN"` exposes the value in process args (`ps`) and in this harness's Bash-tool transcript, and if typed literally (not as `$TOKEN`) also lands in shell history. Use the interactive prompt or `gh secret set NAME < file`. Verify presence (not value) with `gh secret list`.
- **Submodule pin bump**: set the gitlink surgically with
  `git update-index --cacheinfo 160000,<commit-sha>,<submodule-path>` — no submodule checkout needed (works in a fresh worktree). Confirm the target SHA is pushed/tag-reachable on the submodule's remote first (`git ls-remote --tags <url> <tag>`).
- **`--no-verify`**: allowed ONLY for a commit with **no code and no secrets** (a submodule-pin bump, a `.gitmodules`/config-only change) when the repo's pre-commit gate is heavy and times out. `git commit --no-verify` skips both the pre-commit **and** commit-msg hooks (a commitlint-style message check is bypassed too — double-check the message format by hand); `git push --no-verify` separately skips pre-push. Never use either for code or content commits — those must pass the hooks.
- **Shared repo / submodule**: edit via an isolated worktree branched from `origin/main` + PR, never in place — see `subagent-conflict-detection`.

## Repo settings (contribution-flow only)

This skill owns the *contribution-flow* repo config: merge-button policy
(`allow_squash_merge`, `delete_branch_on_merge`), branch protection requiring CI,
required status checks, and labels. **Security settings (Secret Scanning, push
protection) are owned by `apple-dev-skills:apple-public-repo-security`** — set them there, not here.

## Common Mistakes

1. **Merging on a `mergeStateStatus` other than `CLEAN`/`HAS_HOOKS`, or without `pr-diff-verification`** — assuming `BLOCKED` only ever means pending checks and polling it forever, or force-merging past a real red check. Use `gh pr checks <n> --watch` plus `mergeStateStatus`; merge only on `CLEAN` (or `HAS_HOOKS` on GHES) and after `pr-diff-verification` has confirmed the diff matches the commits' claims.
2. **`gh secret set --body "$TOKEN"`** — exposes the value in process args and the tool transcript (and, if typed literally, shell history too). Use the interactive prompt or `gh secret set NAME < file`.
3. **Non-Conventional PR title** — fails a repo's title-lint gate; the PR can't merge.
4. **Editing a shared repo / submodule in place** — two writers clobber each other; use a worktree + PR.
5. **`--no-verify` on a code/content commit** — bypasses the gate that protects the repo. Reserve it for no-code/no-secret commits only.
6. **Hand-editing a submodule's checked-out files from the parent repo** — bump the pin instead (`git update-index --cacheinfo`), and land the submodule's own change via its own PR.
7. **Duplicating a sibling's job** — re-doing diff verification, security settings, or worktree conflict checks here instead of routing to the owning skill.

## Review Checklist

- [ ] Branch name uses a Conventional prefix; PR title is Conventional Commits.
- [ ] Commit carries the `Co-Authored-By:` trailer; PR body ends with the 🤖 footer.
- [ ] `mergeStateStatus` is `CLEAN` (or `HAS_HOOKS` on GHES) before merge (via `gh pr checks <n> --watch` + `gh pr view <n> --json mergeStateStatus`) and `pr-diff-verification` passed; merged with `--squash --delete-branch`.
- [ ] Any secret was set via interactive `gh secret set` (no `--body`); verified with `gh secret list`.
- [ ] A submodule bump used `git update-index --cacheinfo` against a remote-reachable SHA.
- [ ] `--no-verify` used only on a no-code/no-secret commit, with the reason stated.
- [ ] Shared-repo/submodule edits went through a worktree + PR.
- [ ] Nothing here duplicates a sibling skill's scope.

## Related skills

- `pr-diff-verification` — verify `git show --stat --summary HEAD` matches the commit's claims before push/PR.
- `apple-dev-skills:apple-public-repo-security` — security repo settings + secret-leak prevention.
- `subagent-conflict-detection` — worktree + PR flow for parallel sessions / submodules.
- `claude-skill-plugin-packaging` — distributing/installing skill plugins.
