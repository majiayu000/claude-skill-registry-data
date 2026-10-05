---
name: private-repo-search
description: >
  Use when you need to find code, a pattern, or a past implementation across
  GitHub repos — including private ones you have access to — not just the
  current working directory. grep/Glob only reach the checked-out repo; this
  reaches everywhere `gh` is authenticated for. Own version of the dx
  plugin's `/dx:private-github-search`.
---

# Private Repo Search

`gh search code` — GitHub's code search API through the CLI you already have
authenticated, scoped to exactly the repos/orgs you need instead of a raw
`gh api` call.

## Prerequisites

Requires the [`gh` CLI](https://cli.github.com) installed.

```bash
gh auth status  # confirm authenticated; code search needs no extra scope beyond default
```

## Core usage

```bash
gh search code <query> [flags]
```

| Flag | Use for |
|---|---|
| `--owner <org-or-user>` | Scope to everything an org/user owns |
| `--repo <owner/name>` (repeatable) | Scope to specific repo(s) |
| `--language <lang>` | Filter by language |
| `--filename <name>` | Filter by filename (e.g. `package.json`) |
| `--extension <ext>` | Filter by file extension |
| `--match file\|path` | Restrict the match to file contents or the path itself |
| `--json path,repository,sha,textMatches,url` + `-q <jq-expr>` | Structured output for scripting |
| `-L, --limit <n>` | Result cap (default 30) |

```bash
# Find where a symbol is used across every repo in an org
gh search code "someFunctionName" --owner patrickserrano

# Narrow to specific repos and a language
gh search code "RLSPolicy" --repo patrickserrano/harness --language go

# Find a config file by name across everything you can see
gh search code --filename .lacquer.toml

# Machine-readable output for a downstream step
gh search code "TODO(migration)" --owner patrickserrano --json path,repository,url -q '.[] | "\(.repository.nameWithOwner): \(.path)"'
```

## After finding a hit

`gh search code` returns matched paths, not full file content. Fetch the
actual content once you know the repo and path:

```bash
gh api repos/<owner>/<repo>/contents/<path> --jq '.content' | base64 -d
# or, simpler for a quick look:
gh api repos/<owner>/<repo>/contents/<path> -H "Accept: application/vnd.github.raw" 
```

## Caveats

- **Results lag behind pushes.** The index isn't real-time — a just-pushed
  commit may not show up for a few minutes.
- **Legacy search engine.** `gh search code` uses GitHub's older code-search
  API, not the newer engine github.com's web UI uses — results and available
  qualifiers (no regex) can differ from what you'd see in the browser.
- **Scope is "everywhere `gh` can see."** A search with no `--owner`/`--repo`
  filter that returns nothing from a private repo you expect usually means
  an auth/visibility gap, not that the content isn't there — check
  `gh auth status` and repo access before concluding a miss is real.
