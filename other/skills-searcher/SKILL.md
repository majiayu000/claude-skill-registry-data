---
name: skills-searcher
description: Search for installable agent skills across GitHub and skills.sh. Use when Codex needs to find SKILL.md files, compare candidates, inspect skill metadata, validate search backends, diagnose GitHub search rate limits, or produce install commands from gh skill search, Sourcegraph, GitHub code search, and npx skills results.
---

# Skills Searcher

Use the bundled CLI to search all backends together. It requires the sibling `search` skill from the same utils-agent package and uses Python's standard library through a `uv run --script` shebang. Paths in this skill are relative to its base directory.

Run this package's bundled script so it uses the matching sibling search engine:

```bash
scripts/skill-search --json search <query> --relevance --fetch-limit 25 --limit 5 --no-enrich
```

## Search and select candidates

1. Read the parent [selection and diagnostics procedure](../search/references/selection.md).
   It owns task fit, hard constraints, inspection, ordering, omissions and receipts.
   Use `agent-search capabilities --json` for local readiness; `skill-search doctor`
   spends calls and is reserved for connectivity diagnosis.
2. Search with `skill-search --json search <query> --relevance --fetch-limit 25
   --candidate-limit 30 --limit 5 --no-enrich`. Supply `--intent intent.json` for the
   original request and constraints and `--capabilities host.json` for later reads.
   The wrapper returns an unassessed pool without a popularity cutoff. Finish when
   each discovery backend has results or an explicit failure/skip.
3. Check actual `SKILL.md` contents for narrow task fit, authorship and installability.
   For example, a general writing guide may be adjacent to an anti-slop workflow.
   Prefer upstream authors or appropriate domain educators among similarly relevant
   candidates. Confirm the file/path, supported client and installation method;
   generated install commands alone establish none of these facts. Finish when each
   finalist has content evidence and its remaining uncertainties are recorded.
4. Use the returned `trace.state` with the parent engine's `extend`, `continue`,
   `assess` and `select` commands. Keep query expansions and inspections in that run.
   Discovery and optional metadata enrichment already share it. Finish with the
   selected shortlist and compact receipt required by the parent procedure.

Stars and installs may distinguish peers after task fit and evidence quality.
Missing metrics are unknown; small counts are normal for niche topics. Repository
stars describe a repository, not necessarily this skill. GitHub skill and code
transports share an upstream. A registry entry without a file path remains a
separate candidate until its identity can be established.

When the user asks to install a skill, use the verified result's install command.
The search workflow only prints commands.

## Commands

```bash
skill-search doctor
skill-search --json doctor
skill-search search "chezmoi dotfiles" --limit 25 --progress
skill-search --json search "react testing" --limit 25 --no-progress
skill-search search "github pr review" --sort-by sources --direction desc
skill-search raw sourcegraph "chezmoi dotfiles"
```

The `--json` option emits structured JSON for search and doctor. The search output includes preview and install commands alongside each result.

Sort fields are `stars`, `installs`, `sources`, `file-commits`, `repo-commits`, and `skill-name`.

`--limit` remains the printed row cap in legacy metric mode; with `--relevance`
it is the final shortlist cap, and `--candidate-limit` bounds the visible pool.
`--fetch-limit` now independently controls each backend's requested fetch size
(default 25). Previously `--limit` controlled both retrieval and output. `--all`
retains its 1000-row legacy display/fetch defaults; an explicit `--fetch-limit`
overrides retrieval. The legacy sort flags and TSV columns remain compatible.
JSON exposes the run, trace, diagnostics and candidate provenance; TSV prints the
receipt to stderr. Use parent candidate pages to inspect beyond the first page.

Use `--no-enrich` when popularity is unnecessary or GitHub is slow or rate-limited. `--github-concurrency <n>` remains accepted as an upper bound for compatibility; the shared engine currently serializes GitHub calls. Discovery reserves pagination calls. Enrichment declares two calls per unique repository plus one per visible file, with missing metadata left unknown. Relevance mode reserves content inspection allowance via `--max-opens` before metadata calls. `--max-calls N` caps discovery plus enrichment across the invocation; exhausted enrichment remains partial, with unknown counts.

## Backends

Each backend reaches a different part of the ecosystem:

- `gh skill search` is a narrow, curated GitHub-native index with high precision and lower recall.
- Sourcegraph `src search` finds skills in registry-style aggregators that GitHub-native indexes may miss.
- GitHub code search through `gh api /search/code` finds raw `SKILL.md` matches, including dotfiles and tooling repositories that registries have not indexed.
- `npx skills find` is the only source of install counts; use it when popularity matters.

## Sourcegraph query shape

The Sourcegraph backend builds queries in this form:

```text
file:(?i)skill\.md <terms> select:file count:<limit> timeout:<seconds>s
```

Each term expands to `(file:<term> OR repo:<term> OR content:/(?m)^(name|description):.*<term>/)`. Results must match a term in the `SKILL.md` path, repository name, or frontmatter `name:`/`description:` line. Body matches are excluded because they surfaced skills that only mentioned a term in passing. Keep `select:file` so Sourcegraph returns file-level matches, and `(?i)` so filename matching is case-insensitive.

## Rate limits

GitHub skill search and GitHub code search may hit search quotas or secondary rate limits. Check the quota. If GitHub enrichment calls are rate-limited, retry with `--no-enrich` to skip them; a search backend that is itself rate-limited may remain unavailable:

```bash
gh api rate_limit
skill-search search <query> --no-enrich
```

While GitHub recovers, use Sourcegraph and `npx skills` results. Keep `--fetch-limit` bounded during exploration, and avoid tight retry loops against GitHub.

## Validation

After editing this skill, run:

```bash
python3 -m py_compile scripts/skill-search
zsh tests/skill-search.zsh
```

## Shared retrieval boundary

The sibling [search skill](../search/SKILL.md) owns adapters, failure classification,
budgets and provenance. This skill owns its query builders, frontmatter parsing,
legacy presentation/metric merging and preview/install fields. Relevance mode
uses the engine's canonical candidates; the host applies the shared selection
procedure plus this skill's domain checks. Preview
and install commands are output only; this workflow never executes them. General
transport improvements belong in search; read its [extension guide](../search/references/extending.md)
when adding a provider or deciding whether another domain workflow needs a skill.
