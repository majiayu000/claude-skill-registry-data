---
name: whats-new
description: Build or refresh a "What's New" digest of recently merged pull requests across one or more GitHub repos. Use when asked to produce a changelog, release digest, or weekly "What's New" report from merged-PR history.
---

# What's New digest builder

Turns the **merged pull requests** of one or more GitHub repositories into a
human-readable "What's New" digest. You (the AI assistant) write the one-line
summaries; a person reviews and commits the result. Runs locally against the
GitHub API via `gh`. No server infrastructure.

This skill is repo-agnostic: point it at any repo(s) you can read with `gh`.

## Prerequisites

- [`gh`](https://cli.github.com/) installed and authenticated (`gh auth status`).
- `jq` for shaping JSON (optional but convenient).
- Read access to the target repositories.

## Inputs you need from the user

- **repos** — one or more `owner/name` slugs (e.g. `octocat/hello-world`).
- **cutoff** — how far back to look. Default: 90 days. Or an explicit
  ISO-8601 UTC start (e.g. a go-live date).
- **output file** — where the digest JSON should live (e.g. `whats-new.json`,
  or a site data file). Ask if not given.

## Steps

1. **Fetch merged PRs since the cutoff.** For each repo, list PRs merged after
   the cutoff. Example (adjust `--search` window and `--limit` as needed):

   ```bash
   # Merged in the last 90 days:
   SINCE=$(date -u -d '90 days ago' +%Y-%m-%d 2>/dev/null || date -u -v-90d +%Y-%m-%d)
   gh pr list --repo <owner/name> --state merged --limit 200 \
     --search "merged:>=$SINCE" \
     --json number,title,body,mergedAt,url,labels,author \
     > /tmp/whats-new-<repo>.json
   ```

   For an explicit cutoff, set `SINCE` to the ISO date directly. Repeat per
   repo and concatenate. Note any repo that was empty or unreachable.

2. **Deduplicate against any existing digest.** If the output file already
   exists, load it and skip PRs whose `id` (use `repo#number` or the PR URL) is
   already present — **never re-summarize an entry that's already written**, so
   reviewed wording stays put. Idempotency is the point.

3. **Summarize each new PR.** For every PR produce
   `{ "id", "repo", "category", "title", "summary", "mergedAt", "url" }`:
   - `category` ∈ `Feature | Fix | Performance | Docs | Maintenance`. Use the
     conventional-commit prefix in the title as a hint
     (`feat`→Feature, `fix`→Fix, `perf`→Performance, `docs`→Docs;
     `chore`/`refactor`/`build`/`ci`/`test`/`style`→Maintenance), but reclassify
     from the actual PR body when that's clearer.
   - `summary`: ONE plain-language sentence describing the change and, where
     possible, its value to a user of the project. Strip issue numbers, internal
     ticket refs, deploy/CI mechanics, and jargon. Write in an approachable,
     community voice.
   - `title`: keep the PR title, or supply a cleaner display title.

4. **Write the digest.** Merge the new entries into the output file (append to
   the existing array, keep it sorted newest-first by `mergedAt`). Write valid
   JSON; don't reorder or reword existing entries.

5. **Report** to the user: how many new entries were added, from which repos,
   and covering which date range. Remind them to review the output file and
   commit it. This skill does not deploy or publish — it only produces the data.

## Notes

- **Idempotent:** PRs already in the file are never re-summarized.
- **Windows:** if `/tmp` isn't writable, use a temp dir you can write to.
- **Private/enterprise repos:** work fine as long as `gh` is authenticated for
  them; the digest content is only as public as you choose to publish it.
- **Adapt the schema** to your target. If you're feeding a static-site data file
  or a CHANGELOG, map the fields above onto that format in step 4.
