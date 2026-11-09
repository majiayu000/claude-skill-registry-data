---
name: github-cli
description: Every GitHub job from this server through the gh CLI - list, create and clone repos, push code, pull requests, issues, releases, Actions runs. Use when the owner mentions GitHub, a repo, a PR, an issue, a release, a push or a clone.
---

`gh` is signed in as the owner and `git push` uses that login over HTTPS. Never print the token, never run `gh auth logout` or `gh auth refresh`.

```bash
gh auth status                                   # who is signed in
gh repo list --limit 30                          # their repos
gh repo clone <owner>/<repo> ~/projects/<repo>   # code lives in ~/projects
gh repo create <name> --private --source . --push
```

```bash
gh pr create --fill          # from the current branch
gh pr list ; gh pr view <n> ; gh pr checks <n>
gh issue list ; gh issue create --title "<title>" --body "<body>"
gh release create v1.0.0 --generate-notes
gh run list --limit 5 ; gh run view <id> --log-failed
```

Anything else: `gh <command> --help`, or `gh api <path>` for the REST API.

- New repos are private unless the owner asks for public.
- Never force-push, delete a repo or a branch, or rewrite history without the owner's yes.
- Commit with clear messages on the branch already checked out; open a PR only when the owner asks for one.
