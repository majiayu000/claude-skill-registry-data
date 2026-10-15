---
name: tagging-commits-with-notes
description: Tags commits with git-notes labels via the git T aliases and finds or filters commits by tag. Use for "commits tagged X".
argument-hint: "[add|find|list|rm] <tag> [commit or range]"
allowed-tools: Bash(git T *), Bash(git Tls), Bash(git Tgrep *), Bash(git log *), Bash(git notes --ref=topics show *), Bash(git notes --ref=topics list*)
---

# Tagging Commits with Notes

A tag is one line in the commit's note on `refs/notes/topics`. A commit can have
several tags, one per line. The `git T` alias family in `~/dotfiles/.gitconfig`
is the interface. Re-read it if a command misbehaves, because it changes. Never
use bare `git notes add`: it writes to `refs/notes/commits`, which no alias reads.

## Aliases

| Command | Does |
|---|---|
| `git T <tag> [commit]` | Adds one tag. Commit defaults to HEAD. Quote multi-word tags. |
| `git Tls` | Lists each tag with its commit count. |
| `git Tgrep <tag>` | Lists commits with the exact tag, plus the local branches holding each one. |
| `git Te <commit>` | Edits tags in `$EDITOR`. Interactive, so it's for the user, not you. |
| `git Trm <commit>` | Removes all tags from the commit. |

`git T` with no arguments prints the cheatsheet.

## Recipes beyond the aliases

**Tagged commits in a range** (usually "on my branch, not on develop"). `Tgrep`
has no range and also lists tagged commits already merged to develop:

```bash
git log --notes=topics --grep='^rbf$' --format='%h %s' develop..HEAD
```

`--grep` is a regex, so escape `.`, `+`, etc. in the tag.

**Show tags inline:**

```bash
git log --format='%h %s' develop..HEAD | while read -r h s; do
  echo "$h $s  [$(git notes --ref=topics show "$h" 2>/dev/null | sed '/^$/d' | paste -sd,)]"
done
```

**Batch tag.** Print the selection and confirm it with the user before tagging:

```bash
git log --format='%h %s' develop..HEAD -G rbf -- <path>      # 1. show
git log --format=%H develop..HEAD -G rbf -- <path> | xargs -I{} git T rbf {}   # 2. tag
```

Adjust the selection to the request: `--author`, `--grep` on the commit message,
`-G`/`-S` on the diff, or a pathspec.

**Drop one tag and keep the rest** (the non-interactive version of `Te`):

```bash
git notes --ref=topics show <c> | grep -vFx 'siren' | sed '/^$/d' \
  | git notes --ref=topics add -f -F - <c>
```

If no tags remain, use `git Trm <c>` instead.

## Behaviors to know

- **Rebase and amend** copy tags to the new commit (`notes.rewriteRef`), but the
  old commit keeps its note. `Tls` and `Tgrep` hide commits that are on no local
  branch. `git notes --ref=topics list` still shows them. After gc,
  `git notes --ref=topics prune` clears them.
- **Local branches only**: `Tls` and `Tgrep` skip remote refs because
  `--contains` across the monorepo's remotes is slow.
- **Squash-merge drops tags**: the commit that lands on develop has no note.
- **Not pushed**: notes stay local. Don't push `refs/notes/topics` to the
  monorepo remote unless the user asks.
- **Exact match**: `Tgrep rbf` doesn't match `rbf-sweep`. For a prefix, use the
  range recipe with `--grep='^rbf'`.
