---
name: umbraco-cms-source
description: >-
  How to read Umbraco CMS source at the release tag the project targets, from a local clone
  of umbraco/Umbraco-CMS or from GitHub through `gh`. Use when you need to see how the CMS
  implements something: a base class, an extension point's contract, a backoffice element, a
  service's behavior.

---

# umbraco-cms-source

The CMS source is the ground truth for how Umbraco behaves. Reading it from a local clone is
much faster than fetching files one at a time from GitHub, and `git grep` searches a whole
release in one call. Read it at the release the project actually targets: code on `main` or a
newer major can have APIs, names, or layouts the project's version doesn't.

## Find the clone

The clone's path lives in the project's `CLAUDE.local.md` (personal, gitignored, set up by
`project-init`), on a line like:

```markdown
- Umbraco CMS source: /Users/jane/Code/Umbraco-CMS
```

Use that path as `$CMS` in the commands below. If it starts with `~`, expand it to the full
home-folder path first: inside quotes, `~` isn't expanded and git can't find the folder. If there's no such line, or the path isn't a
git repo, use the GitHub fallback below. Don't clone it yourself from here; `project-init` offers
that, with the user's yes.

Then find the remote that points at `umbraco/Umbraco-CMS`. In a direct clone it's `origin`;
in a clone of someone's fork it's usually `upstream`. Check once per session:

```bash
REMOTE=$(git -C "$CMS" remote -v | awk 'tolower($2) ~ /[\/:]umbraco\/umbraco-cms(\.git)?$/ {print $1; exit}')
```

If `$REMOTE` comes back empty, no remote points at Umbraco's repo: use the GitHub fallback below.

## Pick the tag

1. Get the exact CMS version the project targets: the `Umbraco.Cms.*` package version in
   `Directory.Packages.props` or the `.csproj`. `CLAUDE.md`'s Stack section has the major if
   the exact version isn't pinned.
2. The tag is `release-<version>`, e.g. `release-17.6.1`. For a major-only target, take the
   newest tag in that major:
   ```bash
   git -C "$CMS" tag -l "release-17.*" --sort=-v:refname | head -1
   ```
3. If the tag isn't there, fetch tags once, then look again:
   ```bash
   git -C "$CMS" fetch --tags --quiet "$REMOTE"
   ```
4. If the project supports more than one CMS major, check each major's tag. Behavior that
   differs between them is a multi-version finding, not a detail to average out.

## Read, search, list

Read straight from the tag. These commands never touch the clone's working tree or current
branch:

```bash
# Read one file
git -C "$CMS" show "${tag}:src/Umbraco.Core/Services/ContentService.cs"

# Search the whole release (narrow with a pathspec when you can)
git -C "$CMS" grep -n "class ContentService\b" "${tag}" -- 'src/*.cs'

# List files under a folder
git -C "$CMS" ls-tree -r --name-only "${tag}" -- src/Umbraco.Web.UI.Client/src/packages/core/
```

Write `"${tag}:path"` with braces. In zsh, `$tag:s` is read as a modifier on `$tag`.

Where to look: from `release-17.1.0`, the CMS has its own `CLAUDE.md` at the repo root and in each
project under `src/` (`src/Umbraco.Core/CLAUDE.md`, `src/Umbraco.Web.UI.Client/CLAUDE.md`, and
so on). Read the one for the area you need, at the same tag, before searching. It maps that
project's folders and names its conventions. Older tags don't have them; list the folder
instead. For a backoffice extension, each feature package's
`manifests.ts` under `src/Umbraco.Web.UI.Client/src/packages/` shows how a built-in extension
of the same type is registered.

## Rules

- **Never change the clone.** No `checkout`, `switch`, `pull`, `reset`, or edits. It may be the
  user's own working copy. `fetch --tags` is the only write, and it only adds tags.
- **Quote the tag you read.** When a design, review finding, or decision relies on CMS
  source, name the file and tag (`release-17.6.1:src/...`) so the claim can be checked.
- **Source beats memory and docs.** If what you remember about a CMS API, or what the docs
  (`umbraco-docs`) say, differs from the source at the project's tag, the source wins.

## No clone: GitHub fallback

Use `gh` against `umbraco/Umbraco-CMS` at the same tag:

```bash
gh api "repos/umbraco/Umbraco-CMS/contents/src/Umbraco.Core/Services/ContentService.cs?ref=${tag}" \
  -H "Accept: application/vnd.github.raw"
gh search code "class ContentService" --repo umbraco/Umbraco-CMS
```

`gh search code` only searches the default branch, not a tag. Confirm anything it finds by
reading the file at the project's tag before relying on it.

Without a signed-in `gh`, read the same file over plain HTTPS at the tag:
`https://raw.githubusercontent.com/umbraco/Umbraco-CMS/${tag}/src/Umbraco.Core/Services/ContentService.cs`.
There's no search this way, so find the path first (the docs, a stack trace, or the
namespace).
