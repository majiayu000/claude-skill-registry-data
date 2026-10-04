---
name: dotnet-techne-cross-repo-impact
description: "Use when reviewing a .NET pull request for breaking changes that may affect other microservice repositories. Detects cross-repo API, DTO, endpoint, EF entity, and NuGet-package breaks, and checks whether a compatible downstream PR already exists. Keywords: cross-repo impact, breaking change, microservice compatibility, downstream break, compatible PR, blast radius review, api compatibility, contract break, dto shape change, endpoint break."
disable-model-invocation: false
user-invocable: true
license: MIT
compatibility: Requires Synopsis v1.6.0+ (from dotnet-techne-synopsis skill) with either its MCP daemon or CLI accessible. Requires git and a code-host CLI (gh for GitHub, glab for GitLab) for compatible-PR search. Works with any AI agent that supports the Agent Skills specification.
metadata:
  author: Metalnib
  version: "1.0.0"
  trigger_keywords:
    - cross-repo impact
    - breaking change review
    - microservice compatibility
    - downstream break
    - compatible PR
    - blast radius review
    - api compatibility
    - contract break
    - dto shape change
    - endpoint break
    - shared library bump
---

# .NET Cross-Repo Impact Analysis

Procedural recipe for reviewing a .NET pull request against a multi-repo
microservice workspace: detect breaking changes, trace their blast radius
across repo boundaries, check for a compatible downstream PR, and render
a structured `cross-repo-impact.md` report.

This skill is **procedural only**. It does not describe agent identity,
default stance, or severity philosophy — those belong in the consuming
agent's system prompt. This skill tells the agent *how* to run the
analysis when invoked.

## Requirements

- **Synopsis v1.6.0+** binary available, either:
  - as a long-running MCP daemon (preferred — fastest, combined multi-repo
    graph kept warm), or
  - as a CLI invoked per-run (one-shot mode, no daemon required).
  Use the companion `dotnet-techne-synopsis` skill to auto-download and
  detect the binary.
- **git** on the PATH for diff inspection.
- A code-host CLI on the PATH for compatible-PR search:
  - `gh` for GitHub (authenticated, repo read).
  - `glab` for GitLab (authenticated, MR read).
  - Others acceptable if the agent's harness provides an equivalent
    `searchOpenPrs` tool.
- Read access to a **workspace root** that contains the PR repo AND every
  other repo in the fleet as peer directories (Synopsis discovers repos
  by `.git` markers under the root).

## When to use this skill

Trigger this skill when a PR diff touches any of:

- Public types, methods, records, or interfaces in an assembly referenced
  by other projects.
- ASP.NET controllers, minimal-API endpoints, route constants, or HTTP
  verb attributes.
- EF Core entity classes, `DbContext` overrides, `OnModelCreating`
  configurations, `ToTable` / `HasColumnName` calls, or migration files.
- DTO classes or records carrying `[JsonPropertyName]`, `[DataMember]`,
  `[JsonConverter]`, or used as `HttpClient` request/response bodies.
- `PackageReference` elements in `.csproj` or `Directory.Packages.props`
  where the package is also referenced by other repos.
- `appsettings.json` keys that appear as `ConfigurationKey` nodes in the
  Synopsis graph.

If the diff is pure internal refactor (no public surface change, no
cross-repo edges touched), skip this skill and run standard review skills
only.

## Operating modes

Pick the mode based on what is available:

### Mode A — Daemon mode (preferred)

Used when a long-running `synopsis mcp` daemon is already serving a
combined multi-repo graph (typical deployment for an autonomous review
agent).

- Call MCP tools on the already-running daemon.
- Ask the daemon to re-index only the PR repo (`reindex_repository`) at
  the head SHA before analysis; other repos stay warm.
- Fastest: typical review in a few seconds of graph work plus the LLM
  turns.

### Mode B — One-shot mode

Used when Synopsis is not running as a daemon (Claude Code user running
this skill manually, CI one-shot, etc.).

- Scan the workspace once with `synopsis scan` to produce
  `head.graph.json`.
- Scan the base revision (checkout base ref → `synopsis scan` →
  `base.graph.json`).
- Run `synopsis breaking-diff base.graph.json head.graph.json --json` to
  get classified breaking changes.
- Query the head graph for blast radius via `synopsis query symbol --fqn
  <name> --blast-radius --json`.

Both modes produce the same findings; the skill text below uses MCP tool
names and notes CLI equivalents where relevant.

## Procedure

### 1. Resolve the workspace and PR

- Determine the **workspace root** (the directory containing all
  microservice repo checkouts). The agent's harness should provide it;
  if not, infer from the parent of the PR repo and verify at least two
  sibling `.git` directories exist.
- Identify the PR repo, base ref, head SHA, and the list of changed files
  via `git diff --name-only <base>...<head>`.

### 2. Ensure Synopsis sees the head revision

**Mode A:** call `reindex_repository { path: <pr-repo-abs-path>, ref: <head-sha> }`.
Wait for response. Inspect returned delta stats to confirm at least one
node changed.

**Mode B:** `synopsis scan <workspace-root> -o head.graph.json`
at head SHA, then `git checkout <base-ref>`, then
`synopsis scan <workspace-root> -o base.graph.json`, then restore head.

### 3. Compute classified breaking changes

**Mode A:** call `breaking_diff { before: <base.graph.json>, after: <head.graph.json> }`.
(The daemon may cache `before` as part of its pre-PR baseline; confirm in
the returned metadata.)

**Mode B:** `synopsis breaking-diff base.graph.json head.graph.json --json`.

The response is a typed list of changes. Each change has:

- `kind` — paired change kinds (`ApiSignatureChange`, `EndpointRouteChange`,
  `EndpointVerbChange`, `TableRename`, `NugetVersionBump`), removal kinds
  (`ApiRemoved`, `EndpointRemoved`, `TableRemoved`, `PackageRemoved`), or
  detection-pending kinds (`DtoShapeChange`, `EntityColumnChange`,
  `SerializationContractChange` — not yet emitted; reserved for future
  pass work).
- `severity` — classifier's base severity (Critical/High/Medium/Low).
- `certainty` — Synopsis certainty (`Exact` / `Inferred` / `Ambiguous` /
  `Unresolved`).
- `affectedNodes[]` — graph node IDs touched.
- `beforeSnippet`, `afterSnippet` — one-line summaries.
- `sourceLocation` — file + line (where applicable).

If the list is empty, skip to step 7 and emit a clean pass.

### 4. Filter to cross-repo impact

For each classified change, call `blast_radius { symbol: <nodeId>, direction: "upstream", depth: 4 }`
(CLI equivalent: `synopsis query symbol --fqn <name> --blast-radius --depth 4`).

Retain only changes whose upstream callers include at least one node with
`repositoryName != prRepo.name`. Group hits by downstream repository.

Changes with no cross-repo callers are not reported by this skill — they
are handled by the standard code-review skills. Always count them in the
summary as "internal-only changes: N".

### 5. Search for compatible downstream PRs

For each affected downstream repo, search open PRs/MRs that likely fix
the break. See `references/compat-pr-search.md` for the full heuristic
catalogue; the minimum set:

- **Keyword search** on the affected symbol's display name and common
  synonyms.
- **Branch-name patterns** commonly used in your org (e.g. `fix/*<symbol>*`,
  `chore/sync-<pr-number>`, `bump/<package>-<version>`).
- **Linked-issue** lookup: if the PR references issue `#N`, search open
  PRs in downstream repos mentioning that issue number.
- **Freshness window**: only consider PRs opened in the last 30 days (or
  since the PR under review was opened, whichever is longer).

GitHub example:

```bash
gh pr list --repo <owner>/<downstream-repo> --state open \
  --search "<symbol> in:title,body" --json number,title,url,headRefName
```

GitLab example:

```bash
glab mr list --repo <group>/<downstream-repo> --state opened \
  --search "<symbol>"
```

Record for each affected repo: `compatiblePrUrl: <url>` OR `compatiblePr: NONE FOUND`.

If the search hits its rate limit or errors, mark `compatiblePr: UNKNOWN`
for that repo and proceed — never fail the whole analysis on search
flakiness.

### 6. Apply severity rules

Start with the classifier's base severity, then apply these transforms:

- If **no compatible PR** was found for an affected downstream repo:
  escalate severity by one level (Low → Medium → High → Critical).
- If compat-PR search returned UNKNOWN: escalate by one level and add a
  `search-failed` warning.
- If all upstream callers are `Ambiguous` or `Unresolved`: cap severity
  at **Medium** and add an `ambiguous-evidence` warning.
- Never down-escalate. A change the classifier called Critical stays at
  least Critical.

See `references/severity-rubric.md` for the full table including edge
cases.

### 7. Render the report

Produce the `cross-repo-impact.md` report following the schema in
`references/report-schema.md`. Output destinations:

- If the agent has a "post inline comment" capability — post this as a PR
  review comment.
- If not, write the file to the workspace root and print its path.

Always also emit a structured JSON summary for programmatic consumers:

```json
{
  "severity": "<highest finding severity>",
  "counts": { "critical": 0, "high": 0, "medium": 0, "low": 0 },
  "affectedRepos": 0,
  "compatiblePrsFound": 0,
  "compatiblePrsMissing": 0,
  "findings": [
    { "kind": "...", "symbol": "...", "severity": "...", "recommendation": "..." }
  ]
}
```

Recommendation values: `BLOCK` | `REQUIRE-COORDINATED-PR` | `FLAG` | `OK`.

## Confidence mapping

The report's `Confidence` field mirrors the weakest Synopsis certainty
contributing to the finding:

| Synopsis certainty | Confidence |
|---|---|
| `Exact` | High |
| `Inferred` | Medium |
| `Ambiguous` | Low |
| `Unresolved` | Unknown |

When a finding has mixed certainty across its evidence, report the
**lowest** value.

## Failure modes

| Situation | Behaviour |
|---|---|
| Synopsis daemon unreachable (Mode A) | Fall back to Mode B. If that also fails, emit a degraded report with `severity: Unknown`, reason stated, and still run standard review skills. |
| `breaking_diff` returns no changes | Emit the summary JSON with all zero counts and a one-line "no cross-repo-relevant breaking changes detected" note. No markdown report. |
| `git checkout <base-ref>` fails in Mode B | Fall back to last common commit via `git merge-base`; record a warning in the report. |
| Compat-PR search CLI absent | Mark all findings `compatiblePr: UNKNOWN`, escalate one level, emit warning in each finding. |
| LLM suggests a cross-repo caller Synopsis did not report | **Reject the suggestion.** Every caller in the report must cite a Synopsis node or edge. If evidence is missing, omit the claim. |

## Skill hygiene

These invariants apply every run. Consumers cannot override them:

- **Classifier-first citation.** Every finding references at least one
  row from `breaking_diff` output AND at least one node/edge from
  `blast_radius`.
- **One-pass severity.** Severity is computed once in step 6. Do not
  re-interpret while rendering.
- **Advisory output only.** Recommendations (`BLOCK`, etc.) are
  suggestions. Gate enforcement is the code host's responsibility.
- **Cross-repo only.** Internal-only findings are counted but not
  reported — the standard code-review skills own those.

## References

- [`references/severity-rubric.md`](references/severity-rubric.md) — full
  rules table including edge cases.
- [`references/report-schema.md`](references/report-schema.md) — exact
  markdown format for `cross-repo-impact.md`.
- [`references/compat-pr-search.md`](references/compat-pr-search.md) —
  heuristics and CLI recipes for GitHub, GitLab, and others.

## See also

- `dotnet-techne-synopsis` — installs the Synopsis binary, exposes the
  graph query surface. This skill depends on it.
- `dotnet-techne-code-review` — standard .NET PR review skill. Runs
  alongside this skill; this one only handles cross-repo findings.
- `dotnet-techne-csharp-api-design` — guidance on designing API changes
  to avoid creating cross-repo breaks in the first place.
