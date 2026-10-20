---
name: research
owner: baseline
description: Workflow Phase 3 — Research and Solution Exploration. Surfaces 2–4 candidate solution approaches with concrete tradeoffs, grounded in current library docs (fetched through the provider named in `.claude/docs-provider.json`) — never in training-data recall. Output lives at `docs/research/<slug>.md`. Candidate ranking and the memo execute in main context; doc/source gathering MAY be delegated to read-only advisory subagents (seed.md §4.2-A).
---

You are surfacing a small set of candidate approaches to a task, with honest tradeoffs, so the spec author can pick one. Decisions are not made here — the human reviewer decides at `/spec`. Your job is to lay out the option space.

# Prereqs

- `scout` in `completed` OR in `exceptions`.

# Inputs

- The intake at `docs/intake/<slug>.md` — **Constraints** and **Acceptance criteria** sections filter which approaches are viable.
- The scout report at `docs/scout/<slug>.md` — patterns in use, touchpoints, landmines.
- The BRD at `docs/brd/<slug>.md` if present — NFR-### requirements (latency, compliance, etc.).
- The existing tech stack — read `package.json`, `pyproject.toml`, `go.mod`, lockfiles.

# Mandatory: verify library APIs against current docs (the provider is a default)

For any library you intend to cite, verify its API against current documentation — never training recall.

The MCP server that fetches those docs is named in `.claude/docs-provider.json`; resolve it with `readDocsProvider` from `.claude/skills/lib/docs-provider.mjs`, which falls back to the shipped default when the pointer is absent or unreadable. Use that server's own library-resolution and documentation-fetch tools — read their names from the tool list rather than assuming a shape, because a project may point at a different provider.

**Never cite an API from memory.** Record the version present in the lockfile and confirm the docs match that major version. If the provider has no coverage (or the project ships none), fall back to `WebFetch` against the library's official docs / `llms.txt` and note the source. Any current-docs source satisfies the rule — the declared provider is the convenient default, not a hard requirement (seed.md §2.5).

# Method

0. **Retrieve prior art before deriving.** Run:

   ```
   node .claude/skills/research/retrieve.mjs --slug <slug> --terms "<intake topics + scout touched modules>" \
     --touched '["<scout-touched path>","<scout-touched path>"]' --spec-dir docs/system 2>/dev/null
   ```

   Two lanes answer, and the `via` field on every hit says which one did.

   - **`via: "source_spec"` — the structural lane.** Each `--touched` path walks up through `docs/system/` to the elements that govern it; an element carrying `source_spec:` names the archived spec that authored it. These are provenance, not word overlap, so they rank **above** every term hit.
   - **`via: "terms"` — the term lane.** Scans `docs/archive/**/{research,spec}.md` plus the `decisions` and `libraries` memory categories for overlap with `--terms`, returning `score` + `matchedTerms` per source. It runs unchanged whether or not the structural lane finds anything: only a minority of elements carry `source_spec:`, so the structural lane alone answers a minority of questions.

   Read `structuralUnresolved` too — an element that names a `source_spec:` with no archived spec on disk is reported there rather than dropped, so a thin structural result is visible instead of silent. `summary` carries the counts, so stdout alone is enough; `--touched` takes **one quoted JSON array** (zsh does not word-split).

   Pass `--touched` only when `docs/scout/<slug>.md` exists — its touched-path list is the input. Without it, or with `memory.architecture_map.enabled` off, the structural lane is inert and the term lane behaves exactly as before.

   For every hit you reuse, cite its `path`; consume `docs/scout/<slug>.md` when present; then derive only the genuine **delta** not already covered. Empty archive → no hits → derive fresh as below.
1. **Identify libraries and frameworks** the solution would likely touch.
2. **Verify each library API** against current docs (the declared provider, above).
3. **For each candidate**, evaluate against:
   - Fit with existing patterns (per scout report).
   - YAGNI: does it need abstractions beyond what this task requires?
   - Test-ability: can it be driven by tests seed.md permits — no internal mocks, no mocked DB?
   - Reversibility: if it proves wrong post-implementation, what is the blast radius?
4. **Rank candidates.** State your recommendation. Name what would flip the decision.

**Gathering delegation (seed.md §4.2-A).** Doc/source gathering MAY be delegated to read-only advisory subagents; findings return here, and candidate evaluation, ranking, and the memo stay in main context.

# Output

Write the memo to `docs/research/<slug>.md`. Format:

```
# Pattern Research — <task>

## Prior art (retrieved)
<Reused prior findings from `retrieve.mjs`, each cited to its source path (e.g. `docs/archive/<date>/<slug>/research.md`) and labelled with the lane that found it — `via: source_spec` is the spec that authored a touched path, `via: terms` is word overlap. State the delta: which parts are already answered upstream vs. newly derived below. Empty when the archive had no relevant hits.>

## Candidate A: <short name>
- **Summary**: <1–2 sentences>
- **API references (current)**:
  - `<lib>@<version>` — <specific API> — <provider citation or doc URL>
- **Fits**: <yes/no — anchored to a Scout observation>
- **Tests it enables**: <kinds of tests>
- **Tradeoffs**: <honest, not marketing>

## Candidate B: ...

## Recommendation
<Which candidate, and what would flip the decision.>

## Open questions
<Things a human reviewer must decide before the spec is written.>
```

After writing the file, append `"research"` to `workflow.json → completed`.

Tell the user: `Research memo at <path>. Next: /spec.`

# Constraints

- **No code generation.** Memo only.
- **No API assertion without a provider or docs reference.** "Unable to verify" is the honest answer when you hit a gap; do not guess.
- **No reimplementing what an approved dependency provides** (YAGNI, per seed.md).
- **Prefer 2–3 candidates over 6+.** Half-baked options are noise.
- **The recommendation is a recommendation.** The human reviewer decides at `/spec`.
- **Project source is read-only.** The only write is to `docs/research/<slug>.md`.
