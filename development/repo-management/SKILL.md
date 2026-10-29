---
name: repo-management
description: >
  Reconcile repository issues, pull requests, merge requests, local git
  state, commits, and pushes across GitHub, GitLab, Gitea, Forgejo,
  Codeberg, Bitbucket, Azure DevOps, and SourceHut.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-repo-management
    version: "1.0.0"
    created: 2026-05-15T00:00:00Z
    category: devops
    layer: null
    provides:
      primitives: []
      mcp_tools:
        - detect_repo_provider
        - inspect_repo_state
        - list_repo_issues
        - list_repo_change_requests
        - plan_repo_reconcile
        - resolve_repo_issue
        - merge_change_request
        - commit_local_changes
        - push_current_branch
        - run_repo_reconcile
      assets: []
    commands:
      - name: pk-repo-reconcile
        args: "scope (optional: all, issues, prs, local, push)"
        description: "Plan and apply guarded repository reconciliation across issues, change requests, local commits, and pushes."
---

# Repo Management

## Intro

`repo-management` gives agents a provider-neutral workflow for routine
repository stewardship: inspect open issues and change requests, plan
safe actions, merge only ready work, commit local changes, and push.
Use it when the user asks to check all open issues or PRs, clean up a
repo, reconcile repository state, merge ready work, commit and push, or
perform repo-maintenance across providers.

## Overview

The default workflow is plan-first and guarded:

1. Call `detect_repo_provider(project_root, remote)` to identify the
   remote platform and available local CLI.
2. Call `inspect_repo_state(project_root)` to inspect branch, dirty
   state, upstream, ahead/behind status, remotes, and provider support.
3. Call `list_repo_issues()` and `list_repo_change_requests()` for the
   current provider when supported.
4. Call `plan_repo_reconcile(scope)` to build a concrete action plan.
5. Apply only actions that pass the safety rules below. Use
   `run_repo_reconcile(dry_run=false)` for guarded batch work, or call
   the narrow mutating tools directly.

When the task involves branch policy, review judgment, or release work,
also follow the local `git-workflow`, `code-review`, and
`release-semver` skill guidance.

`/pk-repo-reconcile` is the user command for the same workflow. Without
extra arguments it means `scope=all`: local git state, open issues,
open change requests, and push readiness. Users may narrow it with
`issues`, `prs`, `local`, or `push`.

### Provider support

| Provider | Detection | Read support | Mutating support |
|---|---|---|---|
| GitHub | `github.com` remotes | `gh issue list`, `gh pr list` | issue comments/close, PR merge, commit, push |
| GitLab | `gitlab.com` or `REPO_PROVIDER=gitlab` | capability report, local git | local commit/push only |
| Gitea | `REPO_PROVIDER=gitea` | capability report, local git | local commit/push only |
| Forgejo / Codeberg | `codeberg.org` or `REPO_PROVIDER=forgejo` | capability report, local git | local commit/push only |
| Bitbucket Cloud | `bitbucket.org` remotes | capability report, local git | local commit/push only |
| Azure DevOps | `dev.azure.com` or `visualstudio.com` remotes | capability report, local git | local commit/push only |
| SourceHut | `git.sr.ht` remotes | capability report, local git | local commit/push only |

Unsupported provider actions must return structured evidence instead
of pretending the work is complete. Agents should still commit and push
local changes through git when the repository policy allows it.

### MCP tools

| Tool | Purpose |
|---|---|
| `detect_repo_provider(project_root, remote)` | Detect remote host, owner/repo, provider, and local CLI availability. |
| `inspect_repo_state(project_root, include_remote)` | Inspect branch, dirty state, upstream, ahead/behind, remotes, and provider capabilities. |
| `list_repo_issues(state, limit)` | List open issues when the provider adapter supports it. |
| `list_repo_change_requests(state, limit)` | List open PRs/MRs/change requests when supported. |
| `plan_repo_reconcile(scope, dry_run)` | Produce the action plan and blockers without mutating. |
| `resolve_repo_issue(id, resolution, comment, close, confirmation)` | Comment and optionally close a supported issue. |
| `merge_change_request(id, method, auto_queue, confirmation)` | Merge or queue a supported ready change request. |
| `commit_local_changes(paths, message, checks)` | Run optional checks, stage paths, and commit local changes. |
| `push_current_branch(remote, branch)` | Push the current branch to its remote. |
| `run_repo_reconcile(dry_run, max_items, commit_message, push)` | Apply the guarded batch workflow. |

## Gotchas

- **Do not close issues without evidence.** A close action needs a
  linked merged change, a duplicate reference, a clear no-repro
  disposition, or explicit user instruction.
- **Do not merge drafts or WIP change requests.** Draft state is a hard
  blocker even if checks are green.
- **Do not bypass branch protection.** Never force-push, override
  required reviews, skip required checks, or bypass merge queues.
- **Do not assume GitHub-only behavior.** Detect the provider first and
  return unsupported evidence for adapters that are not configured.
- **Do not treat listing as resolving.** If issues or change requests
  remain open, report the plan or blocker that remains.
- **Do not push unrelated local work blindly.** Inspect `git status`
  and commit only the intended paths or the current complete worktree
  when the user asked for all local changes.
- **Do not run mutating batch actions without a dry-run plan.**
  `run_repo_reconcile(dry_run=false)` should report the plan it applied
  and every command result.
- **Do not hide external auth failures.** Missing `gh`, `glab`, `tea`,
  `bb`, `az`, or `hut` authentication is an actionable blocker, not a
  successful no-op.
- **Do not assume a reused gateway sees newly exported credentials.** A
  long-lived daemon cannot inherit later shell environment changes. Configure
  an owner-only token file for refreshable GitHub CLI authentication.

## Full reference

### Safety policy

The skill is deliberately conservative:

- No force pushes.
- No direct API bypass of provider protection rules.
- No draft/WIP merge.
- No issue close without a comment or explicit resolution evidence.
- Mutating issue and merge tools require exact confirmation tokens:
  `close-issue:<id>` and `merge-change-request:<id>`.
- Provider-specific actions are serialized by the caller; batch tools
  return per-action evidence.

### Scope names

`plan_repo_reconcile()` and `/pk-repo-reconcile` accept these scopes:

| Scope | Includes |
|---|---|
| `all` | local, push, issues, and change requests |
| `local` | dirty state and commit readiness |
| `push` | ahead/behind and push readiness |
| `issues` | open issue listing and resolution candidates |
| `prs` | open pull requests, merge requests, or provider change requests |
| `change-requests` | Alias for `prs` |

### Provider notes

GitHub is the first fully mutating adapter because the `gh` CLI is
common in aibox environments and enforces provider-side checks. GitLab,
Gitea, Forgejo/Codeberg, Bitbucket Cloud, Azure DevOps, and SourceHut
are first-class provider identities in the schema and detection layer;
their remote issue and change-request mutation paths return
`unsupported` until the matching local CLI or API credential contract is
implemented.

### Long-lived gateway GitHub authentication

The gateway daemon and direct stdio servers continue to support normal `gh`
authentication through `GH_TOKEN`, `GITHUB_TOKEN`, `GH_ENTERPRISE_TOKEN`,
`GITHUB_ENTERPRISE_TOKEN`, and the GitHub CLI config or keyring.

For a long-lived daemon that must observe token rotation without a restart,
set `PROCESSKIT_GITHUB_TOKEN_FILE` to a regular file owned by the gateway user
with mode `0600`. The file must contain only the token. GitHub Enterprise may
use `PROCESSKIT_GITHUB_ENTERPRISE_TOKEN_FILE` instead. The file is read
immediately before every `gh` call and injected only into that child process.
Direct token environment variables take precedence.

Token values are never added to MCP arguments, command results, diagnostics,
the gateway catalog, or tracked MCP configuration. A shared daemon has one
GitHub identity; use isolated daemons when clients require separate identities.
