---
name: git-github-workflows
description: Git and GitHub workflow router. Selects the right skill for any git or GitHub operation — committing, PR creation, CI debugging, review comment handling, and more. Invoke at the start of any git/GitHub task.
metadata:
  last_updated: "2026-08-23"
---

# Git & GitHub Workflows

Identify the current operation and invoke the appropriate skill. Never ask the user which skill to use — routing is automatic.

There are two kinds of targets below: **action skills** (do a specific operation) and **reference skills** (look up how something works). For a "do X now" task, route to an action skill; for a "what is / how does / which flag" question, route to a reference skill.

## Routing Table

| Operation | Skill |
|---|---|
| Stage and commit changes | `commit-commands:commit` |
| Commit → push → open PR | `commit-commands:commit-push-pr` |
| Prune merged/deleted branches | `commit-commands:clean_gone` |
| Branch strategy, PR creation, merge flow | `git-pr-workflows:git-workflow` |
| Failing CI / GitHub Actions checks | `gh-fix-ci` |
| **Driving a PR to approval + merge — review loop, required reviewers, merge gate** | `agent-skills:working-with-github` → `references/howto/driving-a-pr-to-approval.md` |
| Addressing comments on an open PR — reply, react, resolve threads | `agent-skills:working-with-github` (mechanics) + `gh-address-comments` |
| Processing and responding to received review feedback | `superpowers:receiving-code-review` (**evaluate** the claim) **and** `agent-skills:working-with-github` (**act** on it: reply, react, resolve, reviewer authority) |
| **Any git command/flag, rewriting history, bisect, conflicts, reflog recovery, git servers** | `agent-skills:working-with-git` |
| **Setting up worktree isolation for feature work or parallel/subagent work** | `agent-skills:working-with-git` → `references/howto/worktree-conventions.md` |
| **gh CLI, REST/GraphQL API, rate limits, tokens, PRs, code review, issues, releases & assets, branch protection, Dependabot/CodeQL config** | `agent-skills:working-with-github` |
| **Building a GitHub App / OAuth app / webhook consumer / Octokit bot** | `agent-skills:developing-for-github` |
| **Writing/debugging CI workflow YAML, Actions, OIDC deploys** | `agent-skills:working-with-github-actions` |

## Routing Details

### Committing

Staging files and generating a well-formed commit message from the diff. Invoke `commit-commands:commit`.

### Commit → Push → PR

Full flow from staged changes to an open pull request. Invoke `commit-commands:commit-push-pr`.

### Clean Merged Branches

Prune local branches whose remote tracking ref is gone (merged and deleted upstream). Invoke `commit-commands:clean_gone`.

### PR Creation and Branch Strategy

Planning a pull request — base branch selection, PR description, reviewer assignment, branch naming. Invoke `git-pr-workflows:git-workflow`.

### Failing CI

GitHub Actions checks are failing. Fetch logs, diagnose the failure, plan and implement a fix. Invoke `gh-fix-ci`.

### Addressing Review Comments

A reviewer has left comments on an open PR that need to be addressed or resolved. Invoke `gh-address-comments`.

### Responding to Review Feedback

You have received a code review and need to process the feedback, decide what to apply, and respond thoughtfully. Invoke `superpowers:receiving-code-review`.

**That skill covers evaluation, not GitHub mechanics — you need both.** `receiving-code-review` tells you how to judge whether a finding is real; it says nothing about which reviewers gate the merge, how to reply on a thread versus top-level, how to resolve a thread, or how to leave the reaction feedback an internal review bot learns from. For all of that, also invoke `agent-skills:working-with-github` and follow `references/howto/driving-a-pr-to-approval.md` (steps 6–11). Routing to evaluation alone is how an agent triages correctly and then merges past a required reviewer it never enumerated.

## Reference Skills (look-ups, not actions)

When the task is "how does X work" / "what's the flag for Y" rather than "do Z now", route to the matching reference skill:

### Git itself

Any `git` command or flag, version-control concepts, rewriting history (rebase/`filter-repo`/amend), `bisect`, recovering from mistakes (reflog, `reset` vs `revert` vs `restore`, dropped stashes/commits), merges & conflict resolution, remotes, hooks, submodules, or hosting/connecting to Git servers. Invoke `agent-skills:working-with-git` (AsciiDoc reference pinned to a known Git version + the Pro Git book + how-to playbooks).

### GitHub the platform

The `gh` CLI, REST API, GraphQL API (rate limits, REST-vs-GraphQL, request efficiency), tokens/auth, pull requests, code review, issues, releases (assets/binaries/changelogs), branch protection & rulesets, GitHub flow, multi-branch release with environments, and Dependabot + CodeQL **security config**. Invoke `agent-skills:working-with-github`.

### Building on GitHub

Creating GitHub Apps, OAuth apps, webhook consumers, or Octokit JS/TS bots/integrations — app auth (JWT → installation token), webhook signature verification, SDK usage. Invoke `agent-skills:developing-for-github`.

### CI/CD

Authoring or debugging GitHub Actions workflow YAML, OIDC cloud deploys, runners, the Dependabot/CodeQL **workflow** cookbooks. Invoke `agent-skills:working-with-github-actions`.
