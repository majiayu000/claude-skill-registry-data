---
name: openbrewerydb-pull-request
description: Open a GitHub pull request for committed brewery record changes in the openbrewerydb/openbrewerydb dataset, with a "data:" title and a body containing a full description plus one section and attribute table per changed record. Use whenever a branch of dataset commits is ready to submit, when the openbrewerydb-contributor workflow reaches its PR step, or when the user asks to open, write, or fix an Open Brewery DB data PR. Do not use to research or edit records, for audits or discovery reports, or for pull requests to other repositories.
---

# OpenBreweryDB Pull Request

Opens a pull request in `openbrewerydb/openbrewerydb` for a branch that already contains committed source CSV changes, and writes a title and body that let a maintainer review every record without opening the diff. Making the record changes is the job of `openbrewerydb-contributor`; this skill starts once the commits exist.

## Maintainer-only npm scripts: never run them

**Never run any npm script in the upstream dataset repository**, including `npm run validate`, `npm test`, any `generate:*` script, undocumented or newly added scripts, and `npm install` (its lifecycle hooks can run scripts). Do not invoke their implementation files directly, through another package manager, or through a subagent. The maintainer runs them only during the merge and publication workflow, and CI runs whatever checks the maintainer configured. Upstream CI failures are reported, not reproduced locally.

## Prerequisites

Confirm these before writing anything:

- `gh auth status` succeeds and `gh api user --jq .login` returns the account that will open the PR.
- The current branch is not `master` and `git status --short` prints nothing. Uncommitted work would not be in the PR, so stop and tell the user instead of committing, stashing, or discarding it.
- `git remote -v` identifies the canonical `openbrewerydb/openbrewerydb` remote and a remote the authenticated account can push to. Do not assume either is `origin`.

## Workflow

### 1. Inventory the branch

```bash
git fetch <upstream-remote> master
git rev-list --count HEAD..<upstream-remote>/master
git log --reverse --format='%h %s' <upstream-remote>/master..HEAD
git diff --name-only <upstream-remote>/master...HEAD
```

Stop and report to the user when:

- The behind count is not zero. The branch needs updating first; do not rebase or merge without the user's agreement.
- Any changed file is outside `data/**/*.csv`, or is a generated root-level artifact such as `breweries.csv`, `breweries.json`, or `breweries.sql`.
- A commit contains more than one record change, or there are no commits. Each record change must be its own commit so it can be reverted independently.
- An added row has a value in `id`. New breweries get their ID from the maintainer when merging, so the added CSV line must start with an empty first column (`+,` in the diff).

An open PR from the same branch also stops the workflow (`gh pr list --repo openbrewerydb/openbrewerydb --head <branch>`). Update that PR's body instead of opening a second one, and only when the user asks.

### 2. Build one change record per commit

For each commit, in commit order, read `git show <sha> -- <csv>` and the CSV header, then record:

- **Action**: `Add`, `Update`, or `Delete`.
- **Brewery name** and **source file** path.
- **Attribute changes**: for an addition, every column with old value `(none)`; for a deletion, every column with new value `(none)`; for an update, only the columns whose value changed. Show the new brewery's `id` as `(blank)`. Show an empty value as `(blank)` so reviewers can tell "intentionally empty" from "omitted".
- **Sources**: the URLs that support the change and what each one verifies.
- **Notes**: conflict resolution, geocoding accuracy or missing coordinates, why a deletion was chosen over `closed`, and anything else a reviewer should double-check.

Take sources and notes from the research earlier in the conversation. If the skill was invoked on its own and the sources are unknown, ask the user for them. Never fill a sources list with plausible-looking URLs; an unsourced data change is the first thing a maintainer will reject.

Derive values from the diff itself rather than memory of what was intended, so the PR describes what will actually merge.

### 3. Write the title

Format: `data: <short description>`

- Start with exactly `data: ` in lowercase, followed by a lowercase imperative phrase. Brewery and place names keep their capitalization.
- Keep the whole title under 72 characters and drop the trailing period.
- Name the brewery when one record changed. For several records, summarize by action, count, and shared region instead of listing names.

Examples:

- `data: add Alpha Brewing Co to Colorado`
- `data: update phone and website for Beta Brewery`
- `data: mark Gamma Brewing in Portland, OR as closed`
- `data: add 4 breweries in Boulder County, CO`
- `data: add 2 and update 3 breweries in Oregon`

### 4. Write the body

Use the template in `references/pr-body-template.md`. It has four parts:

1. **Required opening paragraphs**, copied exactly. The maintainer expects this wording on every dataset PR.
2. **`## Summary`**: a few sentences to a short paragraph describing the change as a whole: what changed and where, why (the user's request, a closure, a relocation, a discovery report), how it was researched, and the counts per action. A reviewer should understand the PR from this section alone.
3. **`## Changes`**: one `###` section per record changed, in commit order, each with the commit SHA, source file, attribute table, sources, and notes. When a single record changed, still use one section, so every data PR has the same shape.
4. **`## Reviewer notes`**: that no npm scripts were run, that generated artifacts and contributor files were left unchanged, and that new rows have a blank `id` for the maintainer to assign.

Table formatting:

- Wrap field names in backticks (`` `phone` ``). Escape a literal `|` in a value as `\|`, and keep values on one line so the table doesn't break.
- Keep the column order of the CSV header within each table, so tables are easy to compare against the file.

GitHub limits a PR body to 65,536 characters. If the body would exceed that, stop and suggest splitting the branch into smaller PRs rather than truncating the per-record sections.

Write the body to a temporary file outside the dataset worktree so it cannot be committed by accident.

### 5. Push and open the PR

```bash
git push -u <writable-remote> "<branch>"
gh pr create \
  --repo openbrewerydb/openbrewerydb \
  --base master \
  --head "<head-owner>:<branch>" \
  --title "data: <short description>" \
  --body-file <temporary-body-file-outside-worktree>
```

Always target `openbrewerydb/openbrewerydb:master` explicitly; `gh` can otherwise infer the fork as the base. Never push directly to `master`.

### 6. Verify

```bash
gh pr view <pr-url> --repo openbrewerydb/openbrewerydb --json url,title,baseRefName,body,commits,files
gh pr checks <pr-url> --repo openbrewerydb/openbrewerydb --watch
```

Confirm that:

- The title starts with `data: ` and the base is `master`.
- The body starts with the required paragraphs and has one `## Changes` section per commit with matching SHAs.
- Only the intended source CSVs changed.
- Checks have reached a terminal state. Report failures with their logs; do not run the corresponding npm scripts.

Report the PR URL, the title, and the check results to the user.

## When to stop and ask

- `gh` is missing or unauthenticated, or no writable remote exists.
- The working tree is dirty, the branch is behind `master`, or a PR already exists for the branch.
- The branch touches generated artifacts or non-source files, a commit holds more than one record change, or an addition has a non-blank `id`.
- Sources for any change are unknown.
- The body would exceed GitHub's size limit.
