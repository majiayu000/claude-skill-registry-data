---
name: insolvia-github-auth
description: >-
  Which GitHub account `gh` and `git` act as in this repo, and how to keep it
  right on a developer machine that holds more than one GitHub account. Use
  this BEFORE any GitHub write — `gh pr create/edit/merge`, `gh api` with a
  method, `gh run rerun`, `gh stack submit`, `git push`, turning on auto-merge —
  and the moment one fails with "Resource not accessible by integration",
  "Permission to insolvia-ai/… denied to <user>", HTTP 403/404 on an
  `insolvia-ai` repo, "must have admin rights", GraphQL `FORBIDDEN`, "Auto merge
  is not allowed for this repository", or the desktop app's auto-merge switch
  failing. Also read it before EVER running `gh auth switch`, `gh auth login`,
  `gh auth logout` or `gh auth setup-git` — the answer is almost always "don't".
---

# GitHub identity in the Insolvia repo

## The rule: check who you are; never switch

Everything here lives in the **`insolvia-ai`** org. A developer machine may have
**several GitHub accounts logged into `gh` at once** — a personal one and the
Insolvia one — and only the Insolvia one can push, merge or administer. So
before a GitHub write, check that the account you're about to use can do it:

```bash
gh api user --jq .login                                          # who gh is right now
gh api repos/insolvia-ai/insolvia --jq .permissions.push         # must print true
```

**Never run `gh auth switch`, `gh auth login`, `gh auth logout` or
`gh auth setup-git`.** Each one changes machine-wide state — `gh`'s *active*
account, or the global git credential config — for every repo and every other
agent session on the machine. Switching to fix this repo silently breaks the
developer's other repos (they start acting as the Insolvia account, or vice
versa). This has happened. If no logged-in account can push, **stop and ask
the human**; `gh auth login` is a browser sign-in they do themselves.

## How each tool picks its account

| Tool | Where its account comes from |
|---|---|
| `gh` in your Bash commands | `GH_TOKEN` if set, else `gh`'s **active** account (machine-wide) |
| `git push` / `git fetch` | git's credential helper — may be set **per folder** in `~/.gitconfig` (`includeIf "gitdir:…"`), independent of `gh`'s active account |
| The desktop app's PR controls (auto-merge switch, PR status, CI monitor) | the **app's own process** — `gh`'s active account. It does not see `GH_TOKEN` or direnv |

On a multi-account machine the usual setup is a **direnv `.envrc`** above the
checkout that exports `GH_TOKEN` (and `AWS_PROFILE` — see `insolvia-aws-auth`)
for the Insolvia account. Your Bash commands run in non-interactive shells that
never trigger direnv's prompt hook, so this repo's SessionStart hook
(`.claude/hooks/session-accounts.sh`) loads that environment into every
Bash command and reports the resolved identity as a `GitHub:` line in your
context. **Read that line first** — it tells you who you are before you act.

## When `gh` is the wrong account

1. `gh auth status` — lists every logged-in account and which is active. It
   never prints tokens; don't try to make it.
2. Find the account that can push: for each login `L` in that list,
   `GH_TOKEN="$(gh auth token --user L)" gh api repos/insolvia-ai/insolvia --jq .permissions.push`.
3. Use it **per command**, without switching:

   ```bash
   GH_TOKEN="$(gh auth token --user <insolvia-login>)" gh pr create …
   ```

   Env vars don't persist between your Bash calls, so prefix each `gh` command
   (or chain them in one call). Never echo the token or write it to a file.
4. Tell the human the SessionStart identity line was wrong or missing, so they
   can fix their `.envrc` — don't patch their dotfiles yourself.

## When `git push` is denied

`remote: Permission to insolvia-ai/insolvia.git denied to <user>` means git's
credential helper handed over the wrong account. Check which one, without
printing the secret:

```bash
printf 'protocol=https\nhost=github.com\n\n' | git credential fill | grep '^username='
git config --show-origin --get-urlmatch credential.helper https://github.com
```

One-off push as the Insolvia account, through `gh`'s token (no config change):

```bash
GH_TOKEN="$(gh auth token --user <insolvia-login>)" \
  git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push
```

Then tell the human; the durable fix is their `~/.gitconfig`, not yours to edit.

## Merging: auto-merge is OFF in this repo

`insolvia-ai/insolvia` has `allow_auto_merge = false`, so the desktop app's
auto-merge switch and `gh pr merge --auto` **both fail here whatever the
account** (the app reports it as `forbidden`). Don't retry the switch. To
"merge when green":

```bash
gh pr checks <n> --watch --fail-fast && gh pr merge <n> --squash --delete-branch
```

Stacks merge with `gh stack merge --yes` (see `insolvia-pr-description`).
Check the setting before assuming it's still off:
`gh api repos/insolvia-ai/insolvia --jq .allow_auto_merge`.

## Installing `@insolvia-ai/*` packages (`read:packages`)

`scripts/github-packages-auth.sh` tries `GH_TOKEN` and then `gh auth token` —
which, with `GH_TOKEN` set, is the same Insolvia token. If that login lacks the
`read:packages` scope, the install 401s, and the script's fallback
(`gh auth refresh`) can't help from an agent shell: it needs a browser, and it
only ever refreshes gh's *active* account. Don't switch accounts to work around
it. Tell the human to add the scope to the Insolvia login once, themselves:

```bash
gh auth switch --user <insolvia-login>
gh auth refresh --hostname github.com --scopes read:packages
gh auth switch --user <their-usual-default>
```

## Commit author

`git config user.email` in this checkout is whatever the developer set for it
(often per folder, via the same `includeIf`). Don't change it; if it looks
like the wrong identity, say so.
