---
name: github-cli
description: "Work with GitHub repositories, issues, PRs, releases and Actions runs through the gh CLI instead of web fetches."
when_to_use: "Use when researching a GitHub repository or reading and changing its issues, PRs, releases and Actions runs; local commits and history are ac:commit."
---

# GitHub CLI

Use `gh` for every GitHub lookup. A GitHub page fetched through the web is rate-limited, truncated and stripped of structure, while `gh` returns the exact file text or JSON and authenticates with the user's own token. Check it is usable before the first call: `command -v gh && gh auth status`. If either fails, say so and fall back to web fetch rather than guessing.

Every command takes `--help`, and `gh <cmd> --json` with no value lists the available JSON fields. Outside a git checkout, pass the repository explicitly: `-R OWNER/REPO` on `issue`, `pr`, `release`, `run`, `workflow` and `label` commands, `OWNER/REPO` as the argument to `gh repo view` and `gh repo clone`, and a literal `repos/OWNER/REPO/...` path to `gh api`. The `{owner}` and `{repo}` placeholders resolve from the current directory's remote, so in research they would silently point at the wrong repository.

This file covers reading. Anything that changes state on GitHub is in `${CLAUDE_SKILL_DIR}/references/write-ops.md` (see Writing to GitHub below).

## Research recipes

Pin reads to a commit SHA, not a branch, so the lines you cite stay the lines you read.

### Resolve a ref to a SHA

```bash
SHA=$(gh api repos/OWNER/REPO/commits/main --jq .sha)        # branch, tag or short SHA all work
```

### Read a file at that commit

```bash
gh api -H 'Accept: application/vnd.github.raw+json' "repos/OWNER/REPO/contents/path/to/file.ts?ref=$SHA"
gh api "repos/OWNER/REPO/contents/path/to/file.ts?ref=$SHA" --jq .content | base64 -d    # same, via the JSON form
```

The raw header returns the file body directly. The JSON form is for when you also need `.sha`, `.size` or `.download_url`. Files over 1 MB come back without content; use the blob API (`repos/OWNER/REPO/git/blobs/<blob-sha>`) or a clone.

### List a directory or the whole tree

```bash
gh api "repos/OWNER/REPO/contents/src?ref=$SHA" --jq '.[] | .type + " " + .path'     # one directory
gh api "repos/OWNER/REPO/git/trees/$SHA?recursive=1" --jq '.tree[].path'            # every path
```

Check `.truncated` on the recursive tree for very large repositories. For more than a handful of files, a shallow clone into a fresh scratch directory is cheaper than many calls: `gh repo clone OWNER/REPO /tmp/scratch -- --depth=1`.

### History of a path and comparing refs

```bash
gh api "repos/OWNER/REPO/commits?path=src/app.ts&per_page=10" --jq '.[] | .sha[0:7] + " " + (.commit.message | split("\n")[0])'
gh api repos/OWNER/REPO/compare/v1.0.0...v1.1.0 --jq '.files[].filename'
```

### Search

```bash
gh search code "NewCmdApi" --repo OWNER/REPO --language go    # --extension, --filename, --owner, --match file|path
gh search repos "cli tool" --language go --stars ">100" --sort stars
gh search issues "memory leak" --repo OWNER/REPO --state open --json number,title,url
gh search prs "auth" --repo OWNER/REPO --merged
gh search commits "fix race" --repo OWNER/REPO
```

Code search runs on GitHub's legacy engine: no regex, and results can differ from the website. It also has its own, much smaller quota: 10 requests a minute against 30 for the other searches and 5,000 an hour for the core API (check with `gh api rate_limit --jq .resources`). Use it to find the file, then read the file with the core API. `gh search issues` includes issues only unless you add `--include-prs`. To exclude a qualifier put `--` before the query: `gh search issues -- "crash -label:bug"`.

### Issues and pull requests

```bash
gh issue view 123 -R OWNER/REPO --comments                       # readable thread
gh issue view 123 -R OWNER/REPO --json title,state,body,comments,labels
gh issue list -R OWNER/REPO --state all --search "is:closed label:bug" --limit 50 --json number,title,url
gh pr view 456 -R OWNER/REPO --json title,body,files,commits,reviews,comments,statusCheckRollup
gh pr diff 456 -R OWNER/REPO                                     # --name-only, --patch, -e '*.lock'
gh pr checks 456 -R OWNER/REPO
gh api repos/OWNER/REPO/pulls/456/comments --paginate --jq '.[] | .path + ":" + (.line|tostring) + " " + .body'   # inline review comments
```

`gh pr view --json comments` returns the conversation; line-level review comments live in `reviews` only as summaries, so use the `pulls/N/comments` endpoint for them. Issue and PR numbers share one number space per repository.

### Releases and changelogs

```bash
gh release list -R OWNER/REPO --limit 10 --json tagName,publishedAt,isPrerelease
gh release view v1.2.0 -R OWNER/REPO --json body --jq .body     # no tag argument shows the latest release
gh release download v1.2.0 -R OWNER/REPO --pattern '*.tar.gz' --dir /tmp/rel
```

Release notes are often thinner than the repository's own `CHANGELOG.md`; read that file with the contents recipe at the tag's SHA when you need migration detail.

### CI runs and logs

```bash
gh run list -R OWNER/REPO --workflow ci.yml --branch main --limit 5 --json databaseId,conclusion,headSha,url
gh run view 12345 -R OWNER/REPO --log-failed                    # only failed steps
```

Everything else about Actions (job ids, waiting on a run, artifacts, caches, the workflow file, secrets and variables, triggering and rerunning) is in `${CLAUDE_SKILL_DIR}/references/actions.md`; read it when the task is more than a status check.

### Repository facts

```bash
gh repo view OWNER/REPO --json description,defaultBranchRef,latestRelease,licenseInfo,stargazerCount,pushedAt
```

## gh api essentials

`gh api <endpoint>` calls any REST path (`repos/OWNER/REPO/...`, no leading host) or `graphql`.

- Method: GET by default, but any `-f` or `-F` field switches it to POST. For a GET with query parameters write `gh api -X GET search/issues -f q='repo:OWNER/REPO is:open'`, or put them in the URL.
- `-f key=value` sends a string as is. `-F key=value` converts `true`, `false`, `null` and integers to JSON types and reads `@file` or `@-` as a value from a file or stdin. Use `-F` for numbers and booleans, `-f` for text that must stay text.
- Arrays and nesting: `-f 'labels[]=bug' -f 'labels[]=docs'`, `-F 'files[a.txt][content]=@a.txt'`. A whole JSON body goes in with `--input file.json`.
- `--paginate` follows every page and prints each page separately; add `--slurp` to wrap the pages in one JSON array. Use `--jq` for a per-page filter and pipe a slurped result to `jq` for a global one.
- `--jq '<expr>'` filters with a built-in jq; `--template` takes a Go template; `-i` prints status and headers (useful for rate-limit and ETag checks); `--cache 1h` reuses a response.
- `-H 'Accept: application/vnd.github.raw+json'` returns raw file text; `-H 'Accept: application/vnd.github.sha'` on a commit returns just the SHA.

GraphQL passes the query with `-f query=` and every other field as a variable, which is why `-F` matters there:

```bash
gh api graphql -F owner=OWNER -F name=REPO -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      discussions(first: 5) { nodes { title url } }
    }
  }'
```

For a paginated GraphQL query declare `$endCursor: String`, pass `after: $endCursor`, and select `pageInfo { hasNextPage endCursor }` on the connection; `--paginate` fills in the rest.

JSON shaping with `--json` plus `--jq` works the same on every list and view command: `gh pr list --json number,title,author --jq '.[] | "\(.number) \(.title) by \(.author.login)"'`.

## Writing to GitHub

Creating, editing, closing, merging, commenting, releasing, triggering workflows and changing secrets, variables, labels or repository settings are outward actions visible to other people. Run one only when the user asked for that action in this conversation, and pass every title, body and flag explicitly because prompts hang a non-interactive shell. Flags and examples for each command are in `${CLAUDE_SKILL_DIR}/references/write-ops.md`, and for workflows, runs, caches, secrets and variables in `${CLAUDE_SKILL_DIR}/references/actions.md`; read the one that applies before the first write.

## Common mistakes

- Targeting the wrong repository: `{owner}` and `{repo}` placeholders and omitted `-R` resolve from the current directory. Name the repository explicitly.
- Citing a branch: a ref moves, so line numbers drift. Resolve to a SHA and cite that.
- Reading a page when a file will do: use the contents API instead of fetching `github.com/.../blob/...`.
- Spending code search quota on listing files: use the tree recipe. For public code, discover with the ac `web-code-search` tool; keep `gh search code` for private repositories or an exact repository scope.
- `-f` on a GET silently turning it into a POST; add `-X GET`.
- `--draft` on `gh pr list` means only drafts; write `--draft=false` for the rest.
- Truncated output: list commands default to 20 or 30 items. Pass `--limit`, or `--paginate` on `gh api`.
