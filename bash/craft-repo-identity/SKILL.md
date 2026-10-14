---
name: craft-repo-identity
description: Binding one repository to one GitHub account when a machine holds several. Which identity signs a commit, which token pushes it, and why the CLI's account is global when everything else is per repo.
---

# Skill: Craft Repo Identity

> "One machine, many accounts. The repository says which. Nothing else gets a vote."

## When

Two GitHub accounts on one machine — work and personal, client and self. The global git identity
is right for one of them and silently wrong for the rest. A commit signed by the wrong account
still lands, and nobody is asked.

## The Standard

Every binding is `--local`. The global one stays whatever it was; each repo overrides it.

```bash
git config --local user.name  "Full Name"
git config --local user.email "<id>+<user>@users.noreply.github.com"
git config --local github.account "<user>"
git remote set-url origin "https://<user>@github.com/<owner>/<repo>.git"
```

Three jobs, and only the first two are git's:

| Binding | Decides |
|---|---|
| `user.email` | Who the commit is attributed to |
| Username in the remote URL | Which account git asks the credential helper for |
| `github.account` | What the sync hook reads |

`<id>` comes from `gh api user --jq .id` — a bare `<user>@users.noreply.github.com` will not
attribute. `.name` is often null, so set `user.name` by hand rather than piping a blank in.

## The Global One

Everything above is per repo. **The CLI's active account is not.** `gh auth git-credential` answers
only for whoever is active, so `git push` fails in a repo the CLI is not pointed at. Not `gh push`.
Plain `git`. Check a repo before trusting it:

```bash
git credential fill <<< "url=$(git config remote.origin.url)"
```

A password means the pairing holds. `could not read Password` means the CLI is somewhere else.

The username in the URL does not prevent that. It causes it — and that is the point. Bare, the
wrong token is accepted in silence.

A credential manager settles this half for good, and one usually ships with git already. Getting
it to run is its own problem: see [chain.md](chain.md).

## The Sync

The other half survives every fix above. `gh pr create` runs as whoever is active, and no
per-directory setting exists, so read `github.account` on directory change and switch the CLI to
match. Wrapping `gh` is the tempting shape and the wrong one — until a manager serves `git`, plain
`git push` needs the same switch and never calls `gh`.

## The Anti-Patterns

| Don't | Do | Why |
|---|---|---|
| Set the identity globally per project | `--local`, in the repo | The next clone inherits the wrong one |
| Assume a configured helper runs | Print the origin of each | A blank value upstream deletes it silently |
| Leave the remote URL bare | Put the username in it | Bare fails open — a wrong token is accepted |
| Trust a green `gh auth status` | Run `git credential fill` | Status reports the CLI, not this repo |
