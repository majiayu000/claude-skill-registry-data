---
name: file-pr
description: Open a pull request whose title says why the change matters and whose body opens with the problem in the requester's words. Use when asked to file, open, raise or create a PR, or to rewrite a PR's title or description.
---

# file-pr

Someone reads a pull request months later, trying to remember why the change exists. The diff already says what
changed. The title and body say why it mattered.

## Before filing

1. **Look for an existing PR.** `gh pr list --head <branch>`. If one exists, update it instead of opening a second.
   Done when you know whether this is a new PR or an update.
2. **Read the whole branch diff.** `git log <base>..HEAD` and `git diff <base>...HEAD`, where the base is the PR's
   base branch or the repository's default branch. Compare it with what was asked. If the diff drifted from the
   request, say so instead of filing the drift. Done when every change in the diff belongs to the request.
3. **Learn the house style.** Read the last ten merged PR titles and the repository's contributing guide and PR
   template. Done when you know the title format, and which template sections the repository requires.

## The title

The title usually becomes the commit message on the default branch. Write the outcome, not the mechanism, in the
repository's format (conventional commits unless it uses another).

| Mechanism (avoid) | Outcome (write) |
|---|---|
| `perf(server): negotiate per-message deflate on the websocket` | `perf(server): cut websocket frame size by 70% with compression` |
| `fix(cli): parse version string in preflight` | `fix(cli): stop the version-drift warning firing when versions match` |

A title that cannot be written without an implementation detail means the reason for the change is not yet clear.
Work it out before filing. No vague subjects (`update`, `cleanup`, `address feedback`) and no trailing period.

## The body

Open with the problem as the requester described it: what was broken or missing and why it hurt. Then one or two
sentences on what the change does about it. Add a third part only when a reviewer needs it: a surprising choice, a
risk, a migration step, a follow-up left undone, or where review should start.

```markdown
Starting a thread on an existing worktree ignored the new-worktree default, so the preference only worked half the time.

The preference now applies to every new thread.
```

- Scale the body to the change. A one-line fix gets two sentences. Stay under about 250 words.
- Fill the repository's PR template when it has one, keeping its required sections and writing the problem first
  inside them. Without a template, add no default `Summary`, `Changes` or `Test Plan` headings.
- Leave out file inventories, command logs, CI output, design history and review history. When refreshing a PR,
  describe the current full diff, not the sequence of revisions.
- Reference an issue only when its number is verified from the request, the branch, the commits or the tracker.
  `Fixes #<n>` closes it; `Refs #<n>` only links.
- A user-visible change gets its screenshot or recording, with one sentence on what to look at.
- Keep out customer names, private hostnames, tokens and personal data.

## Filing

1. When the branch has changes not yet on the remote, stage exact paths, commit and push. A title or description
   rewrite alone needs no commit.
2. Write the body to a temporary file and pass it with `--body-file`, so the shell does not mangle it.
3. Open a ready PR, not a draft, so required checks and review bots run: `gh pr create --title "<title>" --body-file
   <file>`. An existing PR is updated with `gh pr edit <n> --title "<title>" --body-file <file>`.
4. Report the PR URL. If asked to see it through, follow the checks (`gh pr checks <n> --watch`) and fix what fails.

Done when the PR exists, its title and body follow this file, and its URL is in the reply.
