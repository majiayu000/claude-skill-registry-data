---
name: umbraco-docs
description: >-
  How to look up the official Umbraco docs for the major the project targets, from a local
  clone of umbraco/UmbracoDocs or the live site's Markdown pages. Use when you need
  Umbraco's documented way to do something: registering an extension point, a setting, a
  package or Marketplace requirement, or a tutorial.

---

# umbraco-docs

The CMS source (`umbraco-cms-source`) is the ground truth for how Umbraco behaves. The docs
support it: they explain what a feature is for, show the intended way to use it, and point
you at the right area of the source. Use them to get oriented and to understand intent, then
confirm any exact contract (a signature, a base class, a default value) in the source.

Read the docs for the major the project targets. Pages change between majors, and the
site's unversioned links show the newest major, which may not be the project's.

## Find the clone

The clone's path lives in the project's `CLAUDE.local.md` (personal, gitignored, set up by
`project-init`), on a line like:

```markdown
- Umbraco docs source: /Users/jane/Code/UmbracoDocs
```

Use that path as `$DOCS` in the commands below. If it starts with `~`, expand it to the full
home-folder path first: inside quotes, `~` isn't expanded and git can't find the folder. If
there's no such line, or the path isn't a git repo, use the live site fallback below. Don't
clone it yourself from here; `project-init` offers that, with the user's yes.

Then find the remote that points at `umbraco/UmbracoDocs`. In a direct clone it's `origin`;
in a clone of someone's fork it's usually `upstream`. Check once per session:

```bash
REMOTE=$(git -C "$DOCS" remote -v | awk 'tolower($2) ~ /[\/:]umbraco\/umbracodocs(\.git)?$/ {print $1; exit}')
```

If `$REMOTE` comes back empty, no remote points at Umbraco's repo: use the live site fallback below.

## Pick the folder

The docs aren't tagged per release. Most products have one folder per supported major on
`main`, with one folder per product inside it. Some products aren't versioned and sit at the
repo root instead:

```text
17/umbraco-cms/        17/umbraco-forms/      17/umbraco-commerce/   ...
18/umbraco-cms/        18/umbraco-forms/      ...
umbraco-cloud/         marketplace-and-integrations/                  ...
```

`gitbook-docs.yaml` at the repo root is the map. It lists every product on the site, each
version's folder (`directory:`), and its site path (`path:`). Read it when you're not sure
where a product lives, or when a product's site path doesn't match its folder name (the
Marketplace docs are in `marketplace-and-integrations/` but served under `umbraco-dxp/`).
Folders that aren't in the map aren't published, so don't rely on them.

1. Get the CMS major the project targets: the `Umbraco.Cms.*` package version in
   `Directory.Packages.props` or the `.csproj`, or `CLAUDE.md`'s Stack section.
2. Read from `<major>/<product>/`. Most lookups are in `<major>/umbraco-cms/`. A package
   that builds on Forms, Commerce or another product reads that product's folder too. For an
   unversioned product, read its root folder: there's only one version of it.
3. Update the clone's view of `main` once per session, then read from `$REMOTE/main`:
   ```bash
   git -C "$DOCS" fetch --quiet "$REMOTE" main
   ```
4. List the top level to see which majors are there:
   ```bash
   git -C "$DOCS" ls-tree --name-only "$REMOTE/main"
   ```
   Only supported majors have a folder, and not every product has every major. If the
   project's major has no folder for the product, it's out of support. Read the nearest newer major and say in your output that the page is for a
   different major.
5. If the project supports more than one major, check each major's folder. A page that
   differs between them is a multi-version finding, not a detail to average out.

## Read, search, list

Read straight from `$REMOTE/main`. These commands never touch the clone's working tree or
current branch:

```bash
# Read one page
git -C "$DOCS" show "$REMOTE/main:17/umbraco-cms/extend-your-project/server-side-extensions/scheduling.md"

# Search one major's CMS docs
git -C "$DOCS" grep -n -i "IRecurringBackgroundJob" "$REMOTE/main" -- '17/umbraco-cms/*.md'

# List pages under a folder
git -C "$DOCS" ls-tree -r --name-only "$REMOTE/main" -- 17/umbraco-cms/extend-your-project/
```

Each product folder has a `SUMMARY.md`: the site's table of contents for that product. Read
it to find the right page by topic when a search for a class name or setting comes up empty.
A folder's `README.md` is that folder's own landing page.

## No clone: live site fallback

The site serves every page as Markdown. Add `.md` to the page's path:

```text
https://docs.umbraco.com/umbraco-cms/17.latest/extend-your-project/server-side-extensions/scheduling.md
```

For a versioned product, the repo path maps to the site path like this:
`17/umbraco-cms/<path>.md` is `umbraco-cms/17.latest/<path>.md`. Always include the
`<major>.latest` part. Without it you get the newest major. An unversioned product has no
version part: `umbraco-cloud/<path>.md`. A few products break the pattern (a different site
path, or a version part like `17.search.latest-lts`); `gitbook-docs.yaml` has the real
mapping. A folder's `README.md` is the folder's own path plus `.md`.

To find a page, fetch the site index at `https://docs.umbraco.com/llms.txt`. It lists every
page with a one-line summary. It's large, so search it for the topic rather than reading it
all. It's only served from the site root, not per product.

## Rules

- **Never change the clone.** No `checkout`, `switch`, `pull`, `reset`, or edits. It may be the
  user's own working copy for writing docs. `fetch` is the only write, and it only updates
  `$REMOTE/main`.
- **Quote the page you read.** When a design, review finding, or decision relies on the docs,
  give the page's site link, with the version part if the product has one, so the claim can
  be checked.
- **Source wins.** If the docs and the CMS source at the project's tag disagree, the source
  is what runs: follow it, and say the docs differ. Docs still beat memory when there's no
  source to check.
