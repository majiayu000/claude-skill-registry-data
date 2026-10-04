---
name: octo-nvim-setup
description: Use when Octo.nvim shows "You are not logged into any accounts on <host>", "error connecting to github", "Could not resolve to a Repository with the name", "Cannot request Projects", or a gh token-scope error — troubleshooting Octo.nvim auth and GitHub Projects access in this dotfiles repo.
---

## Octo shows "not logged into <ssh-alias>" / "error connecting to github"

Octo determines the API host by running `git remote get-url origin`. This
command applies git's `insteadOf` URL rewriting — so a repo whose remote was
set via the `github-personal` SSH alias (see `gitconfig-multi-machine` skill
and `gitconfig/.gitconfig`'s `[url "git@github-personal:..."] insteadOf`
rules) reports back `git@github-personal:...`, not `github.com`. Octo takes
that literal string as the hostname, and since `gh` only has auth configured
for `github.com`, every request fails.

**Does NOT fix it**: pointing the remote at the canonical
`git@github.com:...` form and relying on `insteadOf` to rewrite it under the
hood. `git remote get-url` (and `git remote -v`) both apply the rewrite when
displaying/resolving the URL, so Octo still sees the alias either way. Only
`git config --get remote.origin.url` returns the raw, unrewritten value —
and Octo doesn't use that.

**Fix**: map the alias back to the real host in Octo's config
(`nvim/lua/plugins/coding.lua`):

```lua
{
  "pwntester/octo.nvim",
  opts = {
    ssh_aliases = { ["github-personal"] = "github.com" },
  },
},
```

This mapping is inert on machines whose remotes don't use the alias (e.g. a
work Mac using direnv-injected HTTPS tokens instead) — safe to keep
unconditional in the shared nvim config rather than branching on machine
profile.

## Octo shows "gh: Could not resolve to a Repository with the name '<owner>/<repo>'" (private repo)

Octo doesn't manage `gh` auth itself — it shells out via `plenary.job` with an
**explicit, hardcoded env whitelist** (`octo/gh/init.lua`'s `env_vars`):
`PATH`, `HOME`, `GITHUB_TOKEN`, a few XDG/proxy vars, but **not `GH_TOKEN`**.

If a project's `.envrc` exports `GH_TOKEN` to pin `gh` to a specific account
(e.g. because the repo is private and your `gh` default active account is a
different one — see `git-multi-identity` skill), Octo's job never sees it,
silently falls back to `gh`'s default keyring account, and that account gets
a 404-shaped "could not resolve" error from GitHub for any repo it can't see
— indistinguishable from a real hostname/repo-name problem at first glance.
This only surfaces on **private** repos; a public repo works under any
account, which is why e.g. this `dotfiles` repo itself never showed it while
a private repo like `homelab` did.

**Fix**: forward `GH_TOKEN` into the name Octo actually reads, via its
`gh_env` option (`nvim/lua/plugins/coding.lua`):

```lua
{
  "pwntester/octo.nvim",
  opts = {
    gh_env = function()
      return { GITHUB_TOKEN = vim.env.GH_TOKEN }
    end,
  },
},
```

Safe to keep unconditional: on a machine/project without `GH_TOKEN` set,
`vim.env.GH_TOKEN` is `nil` and this is a no-op merge.

**Prerequisite**: this only works if `GH_TOKEN` actually reaches Neovim's
process env in the first place, which requires **direnv to be hooked into
the shell** (`eval "$(direnv hook zsh)"` in `.zshrc`). Without the hook,
`.envrc` files never auto-load in any project — check for the hook line
before assuming the `gh_env` hookup should have worked.

**Debug tip**: to test Octo's actual `gh` job env directly without
reproducing through the UI, run headless:

```bash
nvim --headless -c 'luafile /path/to/script.lua' -c 'qa'
```
where the script calls `require("octo.gh").run({ args = {...}, cb = ... })`
and `vim.wait(...)` for the callback.

## Octo shows "Cannot request Projects" / "gh: Your token has not been granted the required scopes"

The `gh` CLI token (stored in macOS Keychain — check with `gh auth status`,
look for `(keyring)`) lacks the `project`/`read:project` scope needed for
GitHub Projects (v2) GraphQL queries. Regular repo/PR/issue operations work
fine without it, so this only surfaces when opening Octo's Projects view.

**Fix**: refresh the token with the extra scope (opens a device-code browser
flow — give the user the URL + code, this is not something you can complete
non-interactively). `gh auth refresh` has no `--user` flag — it always
targets whichever account is **currently active** for that host, so switch
first. It also refuses to touch keyring accounts while `GH_TOKEN` is set in
the environment ("The value of the GH_TOKEN environment variable is being
used for authentication") — `unset`/strip it for this step:

```bash
gh auth switch --hostname github.com --user <account>
env -u GH_TOKEN gh auth refresh -h github.com -s project,read:project
```

Verify with `gh auth status` — scopes list should now include `project` for
that specific account's `(keyring)` entry.

If that account is also used via a project's `.envrc`-exported `GH_TOKEN`
(see above), no further action is needed: `.envrc` typically derives it with
`gh auth token --user <account>`, which reads from the same keyring entry
just refreshed — the next new shell picks up the updated scope automatically.
Note **direnv only re-evaluates `.envrc` on directory entry or file change**,
not on every command, so a shell that was already sitting in that directory
when the token refreshed will keep serving the stale cached value; open a new
shell (or `cd` out and back in) to confirm.

## Debugging checklist

```bash
gh auth status                        # confirms login + lists granted scopes
git remote get-url origin             # what Octo actually sees (post-insteadOf)
git config --get remote.origin.url    # raw configured value (not what Octo sees)
direnv status                         # confirms .envrc is hooked/allowed/loaded
gh auth token --user <account>        # the token .envrc's GH_TOKEN actually derives
```
