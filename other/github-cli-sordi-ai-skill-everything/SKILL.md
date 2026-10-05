---
name: github-cli
description: Apply when using the gh CLI to manage pull requests, issues, releases, or CI workflows on GitHub.
license: MIT
version: 1.0.0
tokens_target: 1200
triggers:
  - gh cli
  - github pr create
  - github issues
loads_after: [git-conventions]
supersedes: []
---

# Sub-Skill: GitHub CLI (`gh`) Conventions

**Purpose:** Consistent, auditable use of the `gh` CLI for PRs, issues, releases, and CI — preventing gate bypasses and silent failures.

---

## Rules

### Authentication & Scopes

1. **Check auth scope before scripting.** Before running `gh` in CI or scripts, always verify the required scopes are granted with `gh auth status`; missing scopes produce silent 404s rather than auth errors.
2. **Use token env var in CI.** Always pass `GH_TOKEN` (or `GITHUB_TOKEN`) via environment variable in CI pipelines; never hard-code tokens or use `gh auth login --with-token` interactively in automated contexts.

### Pull Requests

3. **Include all required labels on PR creation.** Always pass `--label` for every gate-required label when running `gh pr create`; omitting a label silently bypasses automated approval gates. Reference: ERR-2026-023
4. **Set reviewer on creation.** Always use `--reviewer <handle>` when creating PRs that require CODEOWNERS approval; adding reviewers after creation delays the review clock.
5. **Open as draft when work is incomplete.** Use `gh pr create --draft` for PRs not yet ready for review; never open a ready-for-review PR on a branch with failing CI.
6. **Link issues explicitly.** Always include `--body "Closes #<issue>"` or `--body "Fixes #<issue>"` so GitHub auto-closes the linked issue on merge; never rely on branch name alone for issue linkage.

### Issues

7. **Assign and label on creation.** Use `gh issue create --assignee @me --label <label>` rather than creating bare issues and editing them in a second step; unassigned, unlabelled issues fall out of triage queues.
8. **Use JSON output for scripting.** Prefer `gh issue list --json number,title,labels` over parsing human-readable output; the `--json` flag is stable across `gh` versions, plain text is not.

### CI / Workflows

9. **Trigger runs explicitly when needed.** Use `gh workflow run <workflow.yml> --ref <branch>` to trigger a workflow rather than pushing an empty commit; empty commits pollute history.
10. **Watch run status in scripts.** After triggering a workflow, use `gh run watch <run-id>` or poll `gh run view <run-id> --json conclusion` rather than sleeping for a fixed duration.

### Releases & API

11. **Create releases from tags, not branches.** Always run `gh release create <tag> --generate-notes` after pushing the tag; never target a branch directly, as branch-based releases produce non-reproducible artifacts.
12. **Use `gh api` for endpoints not covered by subcommands.** Prefer `gh api repos/{owner}/{repo}/pulls --jq '.[].number'` over raw `curl` with manual auth headers; `gh api` inherits the active auth context automatically.
13. **Define aliases for repeated commands.** Use `gh alias set` to capture long flag combinations used more than twice in a project; aliases are stored in `~/.config/gh/config.yml` and are portable across machines via dotfiles.

---

## See also

- `skills/git-conventions/SKILL.md`
- `skills/error-log/SKILL.md`
