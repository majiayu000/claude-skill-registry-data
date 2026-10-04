---
name: query-kb
description: Load scoped repository context, then search and navigate a hraness/wordcell Markdown vault with hybrid text retrieval, exact metadata, bounded links and typed relationships, backlinks, whole-vault graph reports, and optional Git provenance. Use when an agent needs the applicable repository instructions, rationale, prior knowledge, plans, captures, decisions, concepts, relationships, or evidence before answering, planning, or changing code.
---

# Query the knowledge base

Use the cheapest precise view first, then broaden. Markdown files remain the
authority; search scores, metadata rows, and graph results are derived views.

## Locate the vault

- Resolve `<vault>` to the directory containing its managed or authored `index.md`, then
  set the shell-local `KB_ROOT` to that path (`KB_ROOT=kb` from a typical
  repository root, or `KB_ROOT=.` from inside the vault).
- Resolve `<repository>` to the repository root when the question concerns a
  repository path (`KB_REPO=.` from that root).
- Read the vault's applicable agent instructions and note conventions.
- Pass the resolved path to every `--root`; do not scan a repository root merely
  because that is where the agent session started.

## Choose the retrieval lane

- Repository file or directory: run `wordcell context` first. Read its inherited
  guides root to nearest, then inspect its maintained knowledge, active plans,
  dated research, reports, and separate historical-plan group. Open only useful
  context hubs or records.
- Known frontmatter field or tag such as type, status, or area: use `wordcell list`.
- Known note title, path, or alias: use `wordcell links` or `wordcell backlinks`, which
  resolve note identities before returning authored relationships.
- A whole-vault structural question or relationship audit: use `wordcell graph --json`,
  then inspect the smallest relevant portion of its canonical output.
- A phrase, identity, or concept expressed with different vocabulary: use `wordcell search`, whose default hybrid result preserves exact and QMD evidence separately.
- Direct provenance for one note or repository path: use `wordcell history` or
  `wordcell history search` without changing authored metadata or links.
- Recent captures awaiting maintained disposition: use the advisory `wordcell inbox` view.
- Broad orientation: read `index.md`, then follow the smallest useful link trail. Use `wordcell catalog` when an exhaustive disposable inventory is actually needed.

```sh
wordcell context src/parser.ts --root "$KB_ROOT" --repo "$KB_REPO"
wordcell list --root "$KB_ROOT" --scope src/parser --where type=plan --json
wordcell list --root "$KB_ROOT" --where type=plan --where status=in-progress --sort area --json
wordcell list --root "$KB_ROOT" --tag retrieval --sort title --json
wordcell backlinks "Plan title or path" --root "$KB_ROOT" --json
wordcell links "Plan title or path" --root "$KB_ROOT" --direction both --depth 1 --limit 25 --json
wordcell relation list "Plan title or path" --root "$KB_ROOT" --json
wordcell graph --root "$KB_ROOT" --json
wordcell search "why browser capture uses the current tab" --root "$KB_ROOT" --json
wordcell search "accepted ingestion plans" --root "$KB_ROOT" --where type=plan --where status=accepted --tag ingestion --json
wordcell search "notes/write-path" --root "$KB_ROOT" --mode exact --no-history --json
wordcell history "notes/write-path" --root "$KB_ROOT" --repo "$KB_REPO" --json
wordcell history search src/parser.ts --root "$KB_ROOT" --repo "$KB_REPO" --json
wordcell inbox --root "$KB_ROOT" --limit 25 --json
```

`wordcell context` prints hub and record summaries, not their bodies. Each record
states the exact `repository_scopes` declaration that matched, the match depth,
and whether that declaration currently names a file, directory, or absent
future or retired path. Current memory and terminal plans stay in separate
groups. Guides remain
the normative, always-loaded home for ownership, required commands,
prohibitions, invariants, and edit gates. Scope hubs are optional pull-based
rationale, history, examples, evidence, and links; they cannot override a guide
or become the only home of a load-bearing rule. Use `--kind file` or
`--kind directory` when `auto` cannot classify a missing target reliably.

Repeated filters use AND semantics. Metadata paths may be dotted. String and
tag comparisons are case-insensitive; array metadata matches by membership.
Missing sort values come last, with path as the deterministic tie-breaker.
`--where` addresses authored frontmatter only; it does not filter derived H1
titles or file paths. Unquoted `true`, `false`, `null`, and numeric filter
values are typed. Keep quotes inside the argument to match a string with the
same spelling, for example `--where 'external_id="9007199254740993"'`.
`--scope` is an exact, case-sensitive repository-scope filter rather than a
substring or area match. Use it when the desired authored path declaration is
known.

## Use hybrid search as discovery

`wordcell search` first scans current Markdown for identity, phrase, metadata, tag,
and prose matches. By default it runs that exact lane alongside QMD's local
full-text and vector rankings, then combines the ranked lists while retaining
each lane's evidence. Exact title and alias identities stay ahead of broader
matches. The QMD path avoids query expansion and reranking models by default.

The first hybrid or semantic query downloads QMD's compact local embedding
model; later queries reuse the local cache. Prewarm explicitly when useful:

```sh
wordcell index --root "$KB_ROOT"
```

Use `--mode exact` for live model-free search, `--mode keyword` for QMD
full-text retrieval, or `--mode semantic` for its vector lane. Repeated
`--where`, `--has`, and `--tag` constraints are checked against the live
Markdown snapshot. QMD has no path-allowlist search in the pinned release, so a
selective semantic query over-fetches a bounded global window and reports a
degraded partial lane when that window cannot prove completeness. Treat every
retrieval rank as a lead, not a fact. Open the returned Markdown, read enough
surrounding context, and confirm claims against linked sources or capture
manifests.

Default search also returns bounded explicit graph context around the strongest
results. Supply `--related <note>` to seed a known neighborhood or `--no-graph`
when structure does not help. Search does no Git work unless provenance is
requested. Use `--history --repo <repository>` for optional recent per-note
provenance or `--require-history --repo <repository>` when the task cannot
proceed with a partial Git lane. `--no-history` remains an explicit compatibility
form. Graph neighbors and Git history remain separate from primary
text rank. They explain and expand candidates without becoming authored facts,
links, or recency boosts.

`wordcell history <note>` returns the bounded commit history already associated with
one resolved note. `wordcell history search <query-or-path>` searches the bounded Git
projection directly and retains hashes, subjects, matched paths, co-change
paths, and incomplete-detail diagnostics. Git co-change is historical evidence,
not permission to write a scope or relationship.

## Reuse one snapshot in code mode

For several related queries, prefer one SDK session to repeated CLI process
startup:

```ts
import { openKnowledgeBase, packSearchContext } from "@hraness/wordcell/sdk";

const kb = await openKnowledgeBase({ root: "kb", repository: "." });
try {
  const result = await kb.search({
    query: "why browser capture uses the current tab",
    graph: { depth: 1 },
    history: "auto",
  });
  console.log(packSearchContext(result).content);
} finally {
  await kb.close();
}
```

`grep`, `list`, `read`, `links`, `backlinks`, `search`, `history`, and
`searchHistory` share one confined read-only scan. QMD and Git initialize
lazily. The session does not watch Markdown or repository changes. Close it
before a write and open a new session after the final refresh and check.

When independent queries can run concurrently, compose them with
`defineWorkflow` and `runWorkflow` or import a packaged workflow. The runner
validates a finite acyclic graph, caps global concurrency, serializes QMD nodes,
and keeps Git concurrency bounded. Do not bypass those resource groups with
unbounded `Promise.all` calls. Custom workflows use the staged
`defineWorkflow<Input>("id").node(...).output(...)` builder so dependency
results and the final output remain typed.

## Use focused structural views

`wordcell graph --json` returns the current resolved wikilinks, typed relationships,
diagnostics, and note-level connection counts without creating a second graph
store. Use it when a question spans the vault. Prefer `wordcell relation list`,
`wordcell backlinks`, or `wordcell links` when a known note gives you a narrower starting
point.

`wordcell links` is cycle-safe and requires an explicit traversal depth and result
limit. `wordcell relation list` separates authored outbound assertions from derived
inbound relationships while retaining canonical note IDs and source
provenance. Open the returned Markdown before treating an edge as correct: a
typed relationship records an authored assertion, not proof.

If a structural question is not covered by a named command, inspect the
bounded JSON graph in the agent or a short task-local script. Do not create or
commit a parallel graph database merely to answer one query. A recurring query
is evidence for a focused, tested command with an explicit output contract.

## Combine meaning with structure

1. For a repository-path question, use `wordcell context` before broader retrieval.
2. Use default hybrid search to discover candidate identities when exact
   structure does not answer the question. Read its lane evidence and partial
   diagnostics before relying on the order.
3. Use `wordcell list` to narrow by authored metadata such as `type`, `status`,
   `area`, or `tags`.
4. Use `wordcell links` at depth 1 to inspect immediate explicit relationships and
   `wordcell backlinks` for a focused inbound view. Increase depth only when the
   first neighborhood is insufficient. Traversal defaults to 50 notes and
   reports truncation; lower `--limit` for tighter agent context or raise it
   deliberately when a high-degree hub is genuinely relevant.
5. Use `wordcell graph --json` only when the question genuinely spans multiple
   neighborhoods; keep one-off processing task-local.
6. Read the authoritative notes and cited captures before synthesizing.

A title match may identify a prerequisite, prior version, or supporting note
rather than the artifact that owns the current outcome. Confirm status and
ownership in the candidate Markdown before answering or editing it.

Do not infer an edge from semantic similarity, or a conclusion from a tag. Do
not write generated backlink sections into notes. If the query exposes stale
metadata or a broken link, repair the authored Markdown and finish with
`wordcell refresh --root "$KB_ROOT"` and `wordcell check --root "$KB_ROOT"`.
Close any open SDK session before that repair and reopen it after validation.

An authored `index.md` may declare `kb_catalog: authored`; refresh and check
then leave it untouched. `wordcell catalog --root "$KB_ROOT"` renders the exhaustive
inventory on demand. A managed vault keeps the original generated-catalog
behavior. Neither mode changes scanning, graph analysis, semantic indexing, or
attachment validation.
