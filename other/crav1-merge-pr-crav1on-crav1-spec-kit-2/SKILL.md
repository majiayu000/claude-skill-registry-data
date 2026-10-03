---
name: crav1-merge-pr
description: >-
  Merge one named pull request with a merge commit. GitHub uses gh pr merge
  --merge. Azure Repos uses az repos pr update --status completed --squash
  false. Use only when this turn explicitly asks to merge a pull request by
  number or URL. Cross-cutting. Never squash, rebase, bypass policy, or
  follow on from open-pr.
disable-model-invocation: true
icon: git-merge
color: green
---

# Merge a pull request

Merge **one** named pull request with a **merge commit**, then stop. Never squash. Never rebase.

Command: `/crav1-merge-pr`.

Run it only when **this turn** explicitly asks to merge a specific pull request, named by number or URL. `/crav1-open-pr`, a complete-task loop, a review, or an earlier turn naming a URL is not that ask. Do not run this skill from those steps. If this turn does not name a pull request, ask which one. That turn is the question only. No merge.

On Windows, `git` may not be on `PATH`. Try `git`, then `C:\Program Files\Git\cmd\git.exe`. `az` may be `az.cmd`. Quote any `--query` value that contains parentheses; `cmd.exe` treats an unquoted `(` as syntax. This skill does not pass a multi-line body to `az`. A multi-line `--description` on Windows uses the `@file` steps in `/crav1-open-pr`.

## Which pull request

Accept a number (`123`) or a URL.

| URL | Id |
| --- | --- |
| `https://github.com/<owner>/<repo>/pull/<n>` | `<n>` |
| `https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<n>` | `<n>` |
| `https://<org>.visualstudio.com/<project>/_git/<repo>/pullrequest/<n>` | `<n>` |

A branch name is not a pull request. Do not pick the newest pull request for the current branch. If the URL's repository is not this git remote, stop and name both. Do not merge across that mismatch.

Remote: the single `git remote`. If several remotes exist, ask which one. A full URL still names the host. A bare number needs that remote, or a `gh` repo that matches it.

## Host

Resolve **one** merge path, in this order: GitHub `gh`, then Azure DevOps `az`, then printed commands and web UI steps. Do not claim the pull request was merged unless that path returned a merge commit hash. On Azure DevOps, that commit must also have two parents, counted with `git rev-list` after the completed re-read (commits API only when git cannot see the commit).

### GitHub (`gh`)

Use `gh` only when **both** are true: `gh auth status` succeeds, and the pull request is on GitHub (`github.com` in the URL or the remote, or `gh repo view` succeeds for that repo).

**Merge** then uses the GitHub steps. If the pull request is on GitHub and `gh auth status` does not succeed, print the GitHub fallback below. Do not use `az`.

### Azure DevOps (`az`)

Treat the remote or the pull request URL as Azure DevOps when it matches `dev.azure.com` or `*.visualstudio.com` (HTTPS or SSH). Read org, project, and repository from that URL when you can:

| Shape | Org / project / repo |
| --- | --- |
| `https://dev.azure.com/<org>/<project>/_git/<repo>` | path segments |
| `https://<org>@dev.azure.com/<org>/<project>/_git/<repo>` | path segments (ignore the userinfo) |
| `https://<org>.visualstudio.com/<project>/_git/<repo>` | host label is the org |
| `git@ssh.dev.azure.com:v3/<org>/<project>/<repo>` | path after `v3/` |
| `git@vs-ssh.visualstudio.com:v3/<org>/<project>/<repo>` | path after `v3/` |
| `<org>@vs-ssh.visualstudio.com:v3/<org>/<project>/<repo>` | path after `v3/` |

`ssh://` URLs use the same path segments. Strip a trailing `.git`. Percent-decode project and repository when the URL encoded them. A collection segment such as `DefaultCollection` stays in the web URL; it is not the project name.

Use `az repos pr` only when **all** of these are true:

1. `az` is on `PATH` (on Windows, `az.cmd` counts).
2. The azure-devops extension works or can be used. `az repos pr list -h` exits 0, or the first `az repos pr` call succeeds. Microsoft documents that this extension installs automatically the first time an `az repos pr` command runs (Azure CLI 2.30.0 or higher). If that first call still cannot run `az repos pr`, the extension is not usable.
3. The CLI is already authenticated for a non-interactive call. A show or list call for this pull request that returns without an auth error counts. `az account show` exiting 0 is a hint, not proof. An `AZURE_DEVOPS_EXT_PAT` the user already set is a credential for that call. Do not print it. A dialog box or a browser Microsoft sign-in is not a merge path. Do not run `az login`, `az devops login`, a device-code flow, or a web login. Do not create a token. See **Auth notes**.

Prefer org, project, and repository parsed from the pull request URL, else the remote. Project and repository fill the REST fallback and the web UI. `az repos pr show`, `az repos pr policy list`, and `az repos pr update` do not take `--project` or `--repository`. A pull request id is unique in the organization. Pass `--org` and `--id`, and pass `--detect false`.

- `--org` is the organization URL, for example `https://dev.azure.com/<org>` or `https://<org>.visualstudio.com`
- `--id` is the pull request id

`--detect` is documented as "Automatically detect organization" (`true` or `false`; default `true`). From a local Azure Repos checkout it reads **that** git remote and overrides `az devops configure` defaults. Command flags win over detection. Use `--detect true` and omit `--org` **only** when the URL did not yield the organization **and** this command runs in a local checkout of that same remote. Otherwise do not use `--detect true`. Do not pass `--project` or `--repository` on show, policy list, or update.

**Merge** then uses the Azure DevOps steps. If `az` is missing, the extension is not usable, the CLI is not already authenticated, or show/update fails, print the Azure DevOps fallback below. Do not invent a merge commit hash. Do not run `az rest`.

### Other remotes

When the pull request is neither GitHub nor Azure DevOps, print the GitHub-shaped fallback below. Do not claim it was merged.

## Read it first

The pull request must be **open**. Anything else: stop and say the state. Do not reopen it.

### GitHub

```text
gh pr view <n-or-url> --json number,url,title,state,isDraft,baseRefName,headRefName,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
gh pr checks <n-or-url>
```

`state` must be `OPEN`.

### Azure DevOps

```text
az repos pr show --org <org-url> --id <n> --detect false --output json
az repos pr policy list --org <org-url> --id <n> --detect false --output json
```

Use the `--detect true` form from **Host** only in the case Host allows, and omit only `--org`.

`status` must be `active`. That is the open set, including drafts.

Keep `title`, source branch (`headRefName` or `sourceRefName`), and target branch (`baseRefName` or `targetRefName`). Strip a `refs/heads/` prefix when you show the branches.

## Mark ready

Only when this turn is the explicit merge ask, and the pull request is a draft.

GitHub: `gh pr ready <n-or-url>`. That is the whole ready step. Do not pass extra flags.

Azure DevOps: set `isDraft` false and do not complete in the same call.

```text
az repos pr update --org <org-url> --id <n> --draft false --detect false --output json
```

`--draft` accepts `false` or `true`. This call uses `--draft false`. Do not pass `--project`, `--repository`, or `--status` on it.

Then read the pull request and its policies again. Publishing can queue checks. If the checks are not passing yet, stop and report that. Do not complete while the checks are queued. If this update fails, print the Azure DevOps fallback. Do not complete. Do not retry.

If `az` is missing and the pull request is a draft, print a first PATCH body `{"isDraft": false}` in the fallback below, then the complete PATCH. Do not claim either call was sent.

## What must pass

Required checks, branch policies, and reviews must pass. If anything blocks, stop and report what. Do not merge.

Never bypass. No `gh pr merge --admin`. No `--bypass-policy`. No `bypassPolicy: true`. No admin override in the web UI steps you print.

### GitHub

Stop unless all of these are true after the ready step:

| Check | Pass | Stop and report |
| --- | --- | --- |
| `mergeStateStatus` | `CLEAN` | `BLOCKED`, `DIRTY`, `DRAFT`, `BEHIND`, `UNSTABLE`, `UNKNOWN`, or anything else |
| `reviewDecision` | `APPROVED`, or empty when `mergeStateStatus` is `CLEAN` | `REVIEW_REQUIRED`, `CHANGES_REQUESTED` |
| `gh pr checks` | every required check passed; exit 0 | failing or pending lines |

`BEHIND` means the head is behind the base. Report that. Do not update the branch in this skill.

`UNSTABLE` is not a pass. Report the check names. Do not merge.

### Azure DevOps

Stop unless all of these are true after the ready step:

| Check | Pass | Stop and report |
| --- | --- | --- |
| `mergeStatus` | `succeeded` | `conflicts`, `failure`, `rejectedByPolicy`, `queued`, or anything else |
| Required reviewers | `isRequired` and vote `10` or `5` | vote `0`, `-5`, or `-10` on a required reviewer |
| Blocking policies | enabled and `isBlocking`, status `approved` or `notApplicable` | `queued`, `rejected`, `broken`, `running`, or any other status |

Do not call `az repos pr set-vote`. Do not vote for the user.

Before the complete call, read that same policy list for a merge-type restriction. Stop and print the Azure DevOps fallback, and do not call update, when an enabled blocking policy's `configuration.settings` sets `allowNoFastForward` to false, or sets the legacy `useSquashMerge` to true. That policy does not allow a no-fast-forward merge commit. Name the policy (`configuration.type.displayName` when it is present; merge-strategy type id `fa4e907d-c16b-4a4c-9dfa-4916e5d171ab`). Do not retry with another merge type. Do not pass `--bypass-policy`.

When those settings are absent, the table above is the whole policy check.

## Show, then merge

Before the merge command, show:

```text
Title: <title>
Source: <source> → Target: <target>
Strategy: merge commit (GitHub --merge; Azure Repos noFastForward via --squash false). Not squash. Not rebase.
```

Then merge. If a blocker stopped you, show those three lines and the blocker, and do not merge.

## Merge

### GitHub

When **Host** says to use `gh`:

```text
gh pr merge <n-or-url> --merge
```

Do not pass `--squash`, `--rebase`, `--admin`, `--auto`, or `--delete-branch`.

On success, read the merge commit:

```text
gh pr view <n-or-url> --json state,mergeCommit --jq .mergeCommit.oid
```

Report that hash. If it is empty, say the host did not return a merge commit. Do not invent one.

If merge fails, show the error and the GitHub fallback. Do not retry with another strategy. Do not claim a merge.

### Azure DevOps

When **Host** says to use `az`, and the read and policy checks have passed, including the merge-type check above:

```text
az repos pr update --org <org-url> --id <n> --status completed --squash false --detect false --output json
```

`--squash false` is the no-fast-forward merge commit. On Azure DevOps, a non-squash completion without an explicit `mergeStrategy` is `noFastForward`. `--output` is a global flag so the completion body can be read. Do not pass `--project`, `--repository`, or `--merge-strategy`. `az repos pr update` does not accept them. Do not pass `--squash true`, `--bypass-policy`, `--bypass-policy-reason`, `--delete-source-branch`, `--transition-work-items`, `--auto-complete`, or `--merge-commit-message`.

If this command fails, stop. Do not retry. Do not try `--squash true`, `--status completed` alone, `--merge-strategy`, or any other strategy. A status-only complete copies completion options already on the pull request, and those can be squash. Print the Azure DevOps fallback. Do not claim the pull request was merged. Do not run `az rest`. Do not start a sign-in.

On success, fetch the pull request again and confirm it. Do not treat the update body as the last word. The update response can still say `status` `active` after a successful complete. Only the re-read counts.

```text
az repos pr show --org <org-url> --id <n> --detect false --output json
```

`status` must be `completed`. `lastMergeCommit.commitId` is the merge commit. Keep that hash. Do not invent one. If `status` is not `completed`, stop and say the state. If `lastMergeCommit.commitId` is empty, say the merge commit is not in the response yet. Do not guess. Do not continue.

Do not read `lastMergeCommit.parents` on the pull request. That array is null on a real Azure DevOps response even when the commit has parents, so a parent check cannot use it.

Count parents with git. Use the `git` from the top of this skill, the remote from **Which pull request**, and the target branch name without `refs/heads/`. `<commitId>` is `lastMergeCommit.commitId` from the re-read.

```text
git fetch <remote> <target>
git rev-list --parents -n 1 <commitId>
```

The line is `<commitId> <parent1> <parent2>` for a merge commit. Two ids after the commit id means a merge commit. One parent is not a merge commit.

If `git rev-list` exits non-zero, or does not print that commit id, git cannot see the commit. Fall back to the Azure DevOps commits API. This GET only counts parents. Do not use it to complete, update, or bypass the pull request. Do not run it when git already returned a parent count. Do not add an Authorization header. Do not print a token. Do not start a sign-in.

```text
az rest --method get --uri "https://dev.azure.com/<org>/<project>/_apis/git/repositories/<repo>/commits/<commitId>?api-version=7.1"
```

Use `https://<org>.visualstudio.com/...` when that is the host. Repository id from `repository.id` on the show payload when it is present; otherwise the repository name. Count the `parents` array. Two entries is a merge commit. One entry is not.

If that GET fails, or `parents` is missing, stop and say the merge type could not be verified. Name the commit id. Do not claim a no-fast-forward merge. Do not fast-forward local `main`. Do not treat the update body, or a null `lastMergeCommit.parents`, as proof.

If the commit does not have two parents, stop and report plainly: the pull request is completed, the hash, and the parent count. A branch policy may have forced squash or rebase. Do not fast-forward local `main`. Do not retry. Do not claim a no-fast-forward merge.

## Fallback (no merge)

Print the title, `source` → `target`, and the strategy line from **Show, then merge**. Then the filled commands. This printout is not a completed merge.

GitHub, or a remote that is not Azure DevOps:

```text
gh pr ready <n>
gh pr checks <n>
gh pr merge <n> --merge
gh pr view <n> --json mergeCommit --jq .mergeCommit.oid
```

Web UI: open the pull request. If it is a draft, choose **Ready for review**. Then **Merge pull request** → **Create a merge commit**. Do not choose **Squash and merge** or **Rebase and merge**. Do not use an admin override. Do not delete the branch unless the user asked in this turn.

Azure DevOps. Fill org, project, and repository from the URL or the remote when you have them. Name any you could not parse. Do not invent them. Repository id from `repository.id` on a show payload when you have it; otherwise the repository name from the URL.

Print the request and the web UI. Do not run it. Do not run `az rest`. That path depends on an `az login` session, which often is not authorized for an organization that belongs to a personal Microsoft account. Do not add an Authorization header. Do not print or echo a token. See **Auth notes**.

Draft, when it is still a draft:

```text
PATCH https://dev.azure.com/<org>/<project>/_apis/git/repositories/<repo>/pullrequests/<id>?api-version=7.1
Content-Type: application/json

{"isDraft": false}
```

Complete (merge commit). `lastMergeSourceCommit.commitId` is the pull request's current source head (`lastMergeSourceCommit` on the open pull request). Do not invent that SHA. If it could not be read, leave the placeholder and say so.

```text
PATCH https://dev.azure.com/<org>/<project>/_apis/git/repositories/<repo>/pullrequests/<id>?api-version=7.1
Content-Type: application/json

{
  "status": "completed",
  "lastMergeSourceCommit": { "commitId": "<lastMergeSourceCommit.commitId>" },
  "completionOptions": { "mergeStrategy": "noFastForward" }
}
```

Use `https://<org>.visualstudio.com/...` when that is the host. Do not set `bypassPolicy`, `deleteSourceBranch`, `squashMerge`, or `transitionWorkItems`.

Web UI: open `https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<id>` (or the `*.visualstudio.com` form). If it is a draft, **Publish**. Then **Complete**, then **Merge (no fast-forward)**. Do not choose **Squash commit**, **Rebase and fast-forward**, or **Semi-linear merge**. Leave bypass policies off. Do not delete the source branch unless the user asked in this turn. Do not change work-item links.

GitKraken stays **GUI paste only** when the user already uses it for this repo: complete the named pull request with a merge commit (no fast-forward). Do not squash. Do not rebase.

## After it merged

Report the merge commit hash, the title, and `source` → `target`. Repeat the strategy: merge commit. On Azure DevOps, also say the merge commit has two parents. Reach this section only after that check passes.

When you only printed commands, stop after those commands. Do not invent a hash.

## Local main

Run this only after a confirmed merge commit. On Azure DevOps that includes a completed pull request whose merge commit has two parents, counted with `git rev-list` or, when git cannot see the commit, the commits API. If that check stopped the skill, do not fast-forward.

When the working tree is clean, fast-forward local `main`:

```text
git checkout main && git pull --ff-only
```

Clean means `git status --porcelain` is empty, ignoring `agent-tools/`. If anything else is dirty, skip the checkout and say so. The merge on the host still stands.

When the pull request target is not `main`, use that target branch name in the same two commands. If the local branch does not exist, say so. Do not create it. If the pull is not a fast-forward, show the error. Do not `reset`, rebase, or force.

## Branches

Do not delete the remote branch or the local branch unless the user asked in this turn. No `--delete-branch`. No `deleteSourceBranch`. If the user asked, delete only the source branch named in that ask: `git branch -d <branch>` and, when the user asked for the remote, `git push <remote> --delete <branch>`. Do not use `git branch -D` unless the user asked to force.

## Tracker

Tracker-neutral. Do not change work-item links.

Do not read or write `work-item.md`. Do not pass `--work-items` or `--transition-work-items`. Do not call `az repos pr work-item`. Do not set `transitionWorkItems`. Do not edit the pull request title or description.

## Auth notes

The skill does not run `az login`, `az devops login`, a device-code flow, or a web login. It does not create a token. It does not print or echo a token. It does not put a token on a command line.

When the azure-devops extension crashes with `module 'keyring' has no attribute 'core'` (seen on Azure CLI 2.90.0), skip `az devops login`. The user sets a personal access token scoped to Code (Read & Write) in the `AZURE_DEVOPS_EXT_PAT` environment variable, then runs this skill again. Do not print or echo that value.

When a call returns `TF400813` after `az login`, the signed-in directory identity is not a member of the organization. That is common when the organization belongs to a personal Microsoft account. Do not run `az login` again. Use the same `AZURE_DEVOPS_EXT_PAT` route. Do not print or echo the token.

An `AZURE_DEVOPS_EXT_PAT` the user has already set is a credential for the `az repos pr` calls. A missing variable is not a prompt to invent one. Print the Azure DevOps fallback and these notes, and stop.

## Hard rules

- No merge unless this turn names the pull request and asks to merge it.
- No squash (`--squash true`, squash merge, `mergeStrategy` `squash`). Azure DevOps complete uses `--squash false`, which is the no-fast-forward merge commit.
- No rebase (`--rebase`, rebase and fast-forward, semi-linear / `rebaseMerge`).
- No `--admin`, no `--bypass-policy`, no `bypassPolicy`.
- No second strategy attempt after a refusal or a failed `az repos pr update`.
- No `git commit`, no stash, no new branch, no force-push.
- No branch delete unless the user asked in this turn.
- No dialog-box or browser Microsoft sign-in (`az login`, `az devops login`, device code, or a web login).
- No token printed, echoed, or created. An `AZURE_DEVOPS_EXT_PAT` the user already set is the PAT route in **Auth notes**.
- Do not run `az rest` to complete, update, or bypass a pull request. The parent-count fallback in **Merge** may GET one commit when git cannot see it.
- Do not claim a merge commit hash the host did not return.
- Do not claim a no-fast-forward merge unless the parent count was verified as two. A null `lastMergeCommit.parents` is not that count.
- Do not run this skill from `/crav1-open-pr`, `crav1-complete-task-agent`, or a review.
