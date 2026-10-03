---
name: crav1-open-pr
description: >-
  Open a pull request for the current change branch (push with explicit yes).
  GitHub uses gh; Azure DevOps uses az when the CLI is available. Use after
  commits exist on feat/<slug> or spec/<slug>, or when the user asks for a PR.
  Cross-cutting. Does not merge; that is /crav1-merge-pr on a later
  explicit ask. Do not commit. When that slug has work-item.md, add a
  Work item section to the body.
disable-model-invocation: true
icon: git-pull-request
color: green
---

# Open a pull request

Push the change branch **only after an explicit yes**, open **one** pull request against the default branch, then stop. Do not merge in this skill. Merging is `/crav1-merge-pr`, a separate step, and only when they explicitly ask in that turn to merge a named pull request. Do not commit.

Create with GitHub `gh` when that host's checks pass. On Azure DevOps, create with `az repos pr` when the Azure CLI can run it. Otherwise print filled commands and GitKraken GUI paste fields. Do not claim a pull request was opened unless the host returned a URL.

Command: `/crav1-open-pr`.

Other skills may **name** this command as an optional next step. Do not run it from those steps. Run it only when the user invoked `/crav1-open-pr` or clearly asked to open a pull request in this chat. `crav1-complete-task-agent` does not push and does not open a pull request.

## Inputs

Resolve these before you push or create anything. Prompt when a value is missing or ambiguous. Show the resolved values with the title and body draft.

| Input | Default |
| --- | --- |
| Base | Repo default branch. See **Base branch**. Confirm when ambiguous. |
| Head | Current branch when it is not the base. Otherwise ask. Do not check out a different branch in this skill. |
| Title | `<slug>: <short summary>` when the head is `feat/<slug>` or `spec/<slug>`. Summary is the `spec.md` H1 when `docs/specs/<slug>/spec.md` exists; otherwise the latest commit subject on the head. No slug: latest commit subject. |
| Body | Template below. |
| Push | Ask once, **after** the title and body are visible. Options in order: **push and open PR** (first/top), **open PR only** (remote already has the branch), **stop**. |

On Windows, `git` may not be on `PATH`. Try `git`, then `C:\Program Files\Git\cmd\git.exe`. `az` may be `az.cmd`. When PowerShell calls `az.cmd`, `cmd.exe` cuts a multi-line argument at the first newline, and an unquoted `--query` value that contains parentheses is a syntax error. Quote every `--query` value (`--query "value[].pullRequestId"`). A multi-line pull-request description uses the `@file` steps in **Create**.

## Base branch

1. `git symbolic-ref refs/remotes/<remote>/HEAD` (for example `origin/main` → `main`) when that ref exists.
2. Else, when `gh auth status` succeeds and the remote is GitHub, `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`.
3. Else the local branch `main`, else `master`, else `develop`, when exactly one of those exists.
4. If more than one candidate remains, or none does, **ask**. Do not guess.

Remote: the single `git remote`. If several remotes exist, ask which one. If none exist, draft the title and body if you can, then stop. Say no remote is configured. Do not claim a push or a pull request.

## Checks (before the draft)

Run these first. Abort in one short message. Do not commit, stash, or check out.

| Condition | Stop |
| --- | --- |
| Not a git repo | Say so. |
| Detached HEAD (`git branch --show-current` empty) and they did not name an existing local head | There is no branch to open from. |
| Dirty tree | `git status --porcelain`, ignoring `agent-tools/`. Point them at `/crav1-finalize-commit`. This skill does not commit. |
| Head has no commits ahead of base | `git rev-list --count <base-ref>..<head>` is 0. Name the refs. Nothing to open. |
| Head branch does not exist locally | Ask for a local branch name. Do not create one. |

Compare against `refs/remotes/<remote>/<base>` when that ref exists, otherwise the local `<base>` branch. If neither ref exists, ask them to name the base. Do not treat a missing ref as “zero commits ahead.”

`agent-tools/` left dirty is fine. Mention that those paths stay uncommitted.

If the current branch **is** the base, ask for the head. Do not open a pull request of the default branch into itself.

If base or head is still ambiguous, that turn is the question only. No title, no body, no push menu.

## Draft title and body

When base, head, and the checks are settled, write the draft into the user-visible reply **before** any choice UI.

**Title** (one line):

```text
<slug>: <short summary>
```

**Body:**

```markdown
## What / why

<Two to four sentences from spec.md or the commits on base..head. Do not invent scope.>

## Spec

- [spec.md](docs/specs/<slug>/spec.md)
- [plan.md](docs/specs/<slug>/plan.md)
- [tasks.md](docs/specs/<slug>/tasks.md)

## Verify

<One line from verify.md when that file exists (pass, fail, or missing). Otherwise: No verify.md on this branch.>
```

When a work-item mention is resolved, add this section after Verify. The body of the section is the mention line only:

```markdown
## Work item

AB#52
```

**Spec** lists only files that exist on the head. Omit **Spec** when none of `spec.md`, `plan.md`, and `tasks.md` exist under `docs/specs/<slug>/`. Slug comes from `feat/<slug>` or `spec/<slug>`. If the head name has no slug and exactly one `docs/specs/<slug>/` folder changed vs base (not `_template/`), use that slug. If several changed, leave the slug out of the title and omit **Spec** rather than picking one.

**Work item** is included only when [references/work-item-mention.md](../crav1-draft-commit-message/references/work-item-mention.md) resolves a mention for that slug (plugin: sibling `skills/crav1-draft-commit-message/references/work-item-mention.md`). The section body is that one mention line (`#<id>` on Azure Repos, `AB#<id>` on GitHub, or the file’s full token). Omit the section when there is no mention. The hint from that reference, when it has one, is a single sentence after the draft, not inside the body.

The section is Markdown in the description. Do not pass `--work-items` or `--transition-work-items` because of it. The ban in **Create** stays as written. Host order and fallbacks stay as written.

Show base, head, remote, title, and body. Say they can edit any of those before you act.

**Then** offer the choices (questions tool when available). Put the actual title and body in the question prompt, for example:

```text
Base: <base>
Head: <head>
Title: <one line>

Body:
<the draft>

What next?
```

Options, **in this order**:

| Id | Choice | What it does |
| --- | --- | --- |
| `push` | Push and open PR | `git push -u <remote> <head>` (no force), then open one pull request. **Always list this first.** |
| `open` | Open PR only | Remote already has this head. Do not push. Open one pull request for that remote head. |
| `stop` | Stop | No push. No pull request. They can still copy the draft. |

Never call the questions tool before the title and body are in the reply. If they named `push` or `open` before any draft existed, ignore it, draft, show the text, then offer the choices.

If they edit the title, body, base, or head: apply only that edit, re-run the checks when base or head changed, show the new draft, **then** the same three choices (`push` still first). Do not push in the edit turn unless they pick `push` or `open` **after** seeing the new draft.

## Host

Resolve **one** create path, in this order: GitHub `gh`, then Azure DevOps `az`, then printed commands and GitKraken GUI paste. Do not claim a pull request was opened unless that path returned a URL.

### GitHub (`gh`)

Use `gh` only when **both** are true: `gh auth status` succeeds, and the remote URL is GitHub (`github.com`, or `gh repo view` succeeds for that repo).

**Create** then uses the GitHub steps. If the remote is GitHub and `gh auth status` does not succeed, print the GitHub-shaped fallback below. Do not use `az`.

### Azure DevOps (`az`)

Treat the remote as Azure DevOps when the URL matches `dev.azure.com` or `*.visualstudio.com` (HTTPS or SSH). Read org, project, and repository from that URL when you can:

| Shape | Org / project / repo |
| --- | --- |
| `https://dev.azure.com/<org>/<project>/_git/<repo>` | path segments |
| `https://<org>@dev.azure.com/<org>/<project>/_git/<repo>` | path segments (ignore the userinfo) |
| `https://<org>.visualstudio.com/<project>/_git/<repo>` | host label is the org |
| `git@ssh.dev.azure.com:v3/<org>/<project>/<repo>` | path after `v3/` |
| `git@vs-ssh.visualstudio.com:v3/<org>/<project>/<repo>` | path after `v3/` |
| `<org>@vs-ssh.visualstudio.com:v3/<org>/<project>/<repo>` | path after `v3/` |

`ssh://` URLs use the same path segments. Strip a trailing `.git`. Percent-decode project and repository when the URL encoded them. A collection segment such as `DefaultCollection` stays in the web URL; it is not the `--project` value.

Use `az repos pr` only when **all** of these are true:

1. `az` is on `PATH` (on Windows, `az.cmd` counts).
2. The azure-devops extension works or can be used. `az repos pr list -h` exits 0, or the first `az repos pr` call succeeds. Microsoft documents that this extension installs automatically the first time an `az repos pr` command runs (Azure CLI 2.30.0 or higher). If that first call still cannot run `az repos pr`, the extension is not usable.
3. The CLI is already authenticated for a non-interactive call. A list call for this remote that returns without an auth error counts. `az account show` exiting 0, or `AZURE_DEVOPS_EXT_PAT` already set, is a hint, not proof. A dialog box or a browser Microsoft sign-in is not a create path. Do not run `az login`, a device-code flow, or a web login. Do not create a token.

Prefer org, project, and repository parsed from the remote. Pass them on the command and pass `--detect false`:

- `--org` is the organization URL, for example `https://dev.azure.com/<org>` or `https://<org>.visualstudio.com`
- `--project` is the team project
- `--repository` is the repo name or id

`--detect` is documented as "Automatically detect organization" (`true` or `false`; default `true`). From a local Azure Repos checkout it reads **that** git remote and overrides `az devops configure` defaults. Command flags win over detection. Use `--detect true`, and omit only the flags you could not parse, **only** when the URL did not yield org, project, and repository **and** this command runs in a local checkout of that same remote. Otherwise do not use `--detect true`.

**Create** then uses the Azure DevOps steps. If `az` is missing, the extension is not usable, the CLI is not already authenticated, or list/create fails, print the Azure DevOps fallback below. Do not invent a URL.

### Other remotes

When the remote is neither GitHub nor Azure DevOps, print the GitHub-shaped fallback below. Do not claim a pull request was opened.

### Fallback (no URL)

After a successful `git push` (push path only), or instead of create (open-only path), print base ← head, the title and body they accepted, and the filled commands. On the open-only path, omit the `git push` line and say the remote branch must already exist.

GitHub, or a remote that is not Azure DevOps:

```text
git push -u <remote> <head>
gh pr create --base <base> --head <head> --title "<title>" --body "<body>"
```

Azure DevOps. Fill org, project, and repository from the remote when you have them. Name any you could not parse. Do not invent them. For `*.visualstudio.com`, `--org` is `https://<org>.visualstudio.com`.

```text
git push -u <remote> <head>
az repos pr list --org https://dev.azure.com/<org> --project <project> --repository <repo> --source-branch <head> --target-branch <base> --status active --include-links --detect false
az repos pr create --org https://dev.azure.com/<org> --project <project> --repository <repo> --source-branch <head> --target-branch <base> --title "<title>" --description "<body>" --detect false
```

On Windows, do not put a multi-line `<body>` on that create command. `cmd.exe` keeps only the first line. Write the accepted body to a temp file as UTF-8 without a BOM and pass `--description "@<file>"`, then delete the file. See **Create**. Quote any `--query` value that contains parentheses.

When org, project, and repository are known, also print the create-PR page they can open. This is not an opened pull request. URL-encode `<head>` and `<base>` (`/` as `%2F`):

```text
https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequestcreate?sourceRef=<head>&targetRef=<base>
```

Use `https://<org>.visualstudio.com/...` when that is the host. Keep a collection segment from the remote when the web repo URL has one.

GitKraken stays **GUI paste only**: open a pull request from `<head>` into `<base>`. Paste the title and body. Do not merge. A later explicit ask to merge that named pull request is `/crav1-merge-pr`.

Do not run `gk ai pr create` or any other interactive `gk` pull-request create. Those commands wait for a confirmation prompt and fail in a non-interactive shell.

## Push and open

Only after they pick `push` on the current draft.

1. `git push -u <remote> <head>`. Never `--force`, `--force-with-lease`, `--force-if-includes`, or a refspec that starts with `+`.
2. If the push fails, show the error. Do not open a pull request. Do not force-push.
3. Open one pull request (below). If one already exists for this head → base, print that URL instead.

## Open only

Only after they pick `open` on the current draft.

1. `git ls-remote --heads <remote> <head>`. If it is missing, say the remote has no such branch. Do not create a pull request. They can pick **push and open PR**.
2. If the local head has commits that are not on that remote head, say so and **do not push**. The pull request would miss them. They can pick **push and open PR**, or stop.
3. Open one pull request (below). If one already exists for this head → base, print that URL instead.

## Create

### GitHub

When **Host** says to use `gh`:

```text
gh pr list --head <head> --base <base> --state open --json number,url
```

If the list is non-empty, print the URL. Do not run `gh pr create`.

Otherwise:

```text
gh pr create --base <base> --head <head> --title <title> --body <body>
```

Pass the body with a HEREDOC or `--body-file` so quotes survive. Do not pass `--draft`, `--reviewer`, `--label`, `--assignee`, or `--milestone` unless they asked for that in this chat.

If create fails because a pull request already exists, print that URL. Do not open a second.

On success, follow **After it exists**.

### Azure DevOps

When **Host** says to use `az`, list open pull requests for this source → target **before** create. `--status active` is the open set, including drafts. Source is `<head>`. Target is `<base>`. Pass branch names (`dev`), not `refs/heads/...`.

Parsed org, project, and repository:

```text
az repos pr list --org <org-url> --project <project> --repository <repo> --source-branch <head> --target-branch <base> --status active --include-links --detect false --output json
```

Use the `--detect true` form from **Host** only in the case Host allows, and only for the flags you could not parse.

If the list is non-empty, print the web URL and stop. Do not run `az repos pr create`. Prefer `_links.web.href`. When the JSON has `pullRequestId` and no web link, print `https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<pullRequestId>` (or `https://<org>.visualstudio.com/...` when that is the organization host). That id came from the host.

If the list call fails, do not create. Print the Azure DevOps fallback from **Host**. Do not invent a URL. Do not start a sign-in.

If the list is empty, create one pull request.

Non-Windows: pass `--description` as one value (a HEREDOC is fine) so quotes and Markdown survive. Microsoft documents each `--description` value as one new line.

```text
az repos pr create --org <org-url> --project <project> --repository <repo> --source-branch <head> --target-branch <base> --title <title> --description <body> --detect false --output json
```

Windows (PowerShell calling `az.cmd`): do not pass the body on the command line. `cmd.exe` keeps only the text before the first newline.

1. Write the accepted body to a new temp file as UTF-8 without a BOM. A BOM shows up as a character at the start of the description. Non-ASCII (an en dash, for example) must survive. Windows PowerShell `Set-Content -Encoding utf8` writes a BOM. Do not use it.

```powershell
$path = Join-Path ([System.IO.Path]::GetTempPath()) ("az-pr-body-" + [guid]::NewGuid().ToString() + ".md")
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $body, $utf8NoBom)
```

2. Pass `--description "@<path>"` with the `@` file token quoted, so PowerShell does not treat `@` as a splat. Azure CLI loads that file and keeps every line.

```text
az repos pr create --org <org-url> --project <project> --repository <repo> --source-branch <head> --target-branch <base> --title <title> --description "@<path>" --detect false --output json
```

3. Delete the temp file after the create call returns, whether it succeeded or failed. Do not commit it. Do not leave it in the repo.

Quote any `--query` value that contains parentheses. `cmd.exe` treats an unquoted `(` as syntax.

Do not pass `--open`, `--auto-complete`, `--draft`, `--delete-source-branch`, `--reviewers`, `--optional-reviewers`, `--required-reviewers`, `--work-items`, `--transition-work-items`, `--squash`, `--merge-commit-message`, `--labels`, or `--bypass-policy` unless they asked for that in this chat. Do not set auto-complete, merge, draft, reviewers, work items, or delete-source-branch unless they asked.

On success, print the web URL the same way (`_links.web.href`, otherwise `/pullrequest/<pullRequestId>` from the id the command returned) and follow **After it exists**. A `url` field on that JSON counts as the host returning a URL; still print the web form when you can build it from that id.

If create fails because a pull request already exists, print that URL. Do not open a second.

If create fails for any other reason, print the Azure DevOps fallback from **Host**. Do not invent a URL. Do not start a sign-in.

### No host create

When **Host** says not to call `gh` or `az`, print the fallback from that section. Do not claim a pull request was opened. Tell them that if one already exists for this head → base, they should use that URL and not open a second.

## After it exists

When the host returned a pull request URL, print that URL and `base` ← `head`.

One sentence: they can review when they want. Next (optional): `/crav1-merge-pr` when they explicitly ask, in a later turn, to merge this named pull request. This skill does not merge, and it does not delete the branch. Do not run `/crav1-merge-pr` from this step.

When you only printed commands, stop after those commands. Do not invent a URL.

## Hard rules

- No `git commit`, no `git commit --amend`, no stash, no `git checkout`, no new branch.
- No force-push.
- No merge (`gh pr merge`, completing an Azure DevOps pull request, or a local merge). Merging is `/crav1-merge-pr` on a later explicit ask for a named pull request. Do not run it from this skill.
- No second pull request for the same head → base.
- No repository setting changes.
- No `gk ai pr create` and no other interactive `gk` pull-request create. GitKraken stays GUI paste only.
- No dialog-box or browser Microsoft sign-in (`az login`, device code, or a web login).
- No `--work-items` and no `--transition-work-items` unless they asked for that in this chat. A **Work item** section in the body is not that flag.
- Do not block the pull request when `work-item.md` is missing. Do not create a work item and do not look one up.
- Do not claim a pull request was opened unless the host returned a URL.
- Workers stay no push and no pull request. Do not run this skill from `crav1-complete-task-agent`.
