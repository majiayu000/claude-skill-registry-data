---
name: radar-analysis
description: Analyze the multi-track ai-signal-radar repository to produce monthly or quarterly reviews, theme and trend synthesis, cross-period comparisons, or idea-mining reports from existing Ray-reviewed data. Use for historical analysis of an explicit systems or creation track, or an explicitly requested cross-track comparison, based on track-scoped data, radars, themes, generated indexes, and monthly reports without ingesting new weekly reports.
---

# Radar Analysis

## Source Contract

Select an explicit track before analysis:

- `systems` for AI systems engineering, infrastructure, runtime, security,
  evaluation, and architecture signals;
- `creation` for AI-native works and products admitted under the repository's
  creation evidence standard.

Keep the tracks separate. Perform a cross-track comparison only when the user
explicitly requests one, and preserve `radar_type` provenance in every claim.

Treat these sources in this order:

1. `data/<track>/YYYY/*.json` as the primary structured record;
2. `radars/<track>/YYYY/*.md` as Ray-reviewed narrative context;
3. `themes/<track>/*.md` as curated track-specific recurring judgments;
4. `indexes/radars.json`, `indexes/tracks.json`, `indexes/themes.json`,
   `indexes/summary.json`, and `themes/README.md` as generated navigation.

Filter shared indexes by `radar_type`; a matching date or theme alone does not
make an entry part of the selected track. Do not use external sources or OpenAI
API calls unless the user explicitly changes the analysis contract.

Before producing an analysis report, run or mentally apply the target repository's consistency checks:

```bash
uv run python scripts/validate_content.py
```

If indexes are stale and the user asked for a committed artifact, regenerate them with the target repository's script first:

```bash
uv run python scripts/update_indexes.py
```

Do not edit reviewed weekly source files under `data/` or `radars/` during analysis. Those files are human-reviewed ingestion outputs.

## Monthly Reviews

For a deterministic monthly scaffold, use the target repository's generator:

```bash
uv run python scripts/generate_monthly_review.py YYYY-MM --track <systems|creation>
```

The generated file belongs at
`reports/monthly/<track>/YYYY-MM.md`. Keep deterministic extraction and counts
separate from any interpretive prose. Ground interpretation in cited dates,
signal titles, themes, and track-scoped source paths.

## Quarterly Reviews

For a quarter such as `2026-Q2`:

1. Select one track, or declare an explicit cross-track comparison.
2. Read `indexes/tracks.json`, `indexes/themes.json`, and
   `indexes/summary.json` for navigation and repository-level counts.
3. Load canonical records only from `data/<track>/YYYY/` whose dates fall
   within the quarter; verify `radar_type` on every record.
4. Group by theme frequency, repeated signal language, recurring ideas or
   patterns, and evidence links.
5. Compare against prior quarters only when matching track records exist
   locally.
6. Report sparse coverage and missing weeks before making a trend claim.

Use headings such as `Coverage`, `Recurring Themes`, `Signals Worth Rechecking`, `Idea Candidates`, and `Open Questions`.

The current repository has no canonical quarterly generator or default
quarterly output path. If the user requests a file, use their destination or an
existing checked-in convention; do not invent a new authoritative path during
analysis.

## Idea Mining

When mining ideas:

1. Start from `ideas` arrays in the selected track's JSON records.
2. Add supporting signals from records with overlapping themes.
3. Distinguish repository evidence from your inference.
4. Prefer a short ranked list over a broad brainstorm.
5. Do not create or update files under `ideas/` unless the user explicitly asks for an artifact.

For creation analysis, preserve each source's observation window and evidence
level, and use recurring `patterns` as supporting context rather than upgrading
creator or vendor claims. For cross-track idea mining, present track-local
evidence first and label the cross-track synthesis as inference.

Each idea should include:

- working title
- source dates
- supporting themes
- strongest supporting signals
- why it may matter
- what would falsify or weaken it

## Output Rules

Keep analysis anchored to repository facts:

- Cite dates and file paths for claims.
- Preserve Ray's reviewed framing; do not rewrite weekly reports as news summaries.
- Avoid claiming a trend from a single record unless labeled as an early signal.
- Separate deterministic extraction, track-local interpretation, and
  cross-track inference.
- If producing a file, run validation after generation when practical.

## Portability Notes

- Specific to the author's current workflow: this assumes a multi-track
  `ai-signal-radar` repository with `systems` and `creation` records, Ray's
  reviewer framing, shared generated indexes, track-specific curated themes,
  and track-specific monthly reports.
- Reusable: select an explicit corpus, treat structured data as primary, retain
  provenance, use reviewed narrative as context, separate extraction from
  interpretation, and validate generated artifacts.
- Adapt before reuse: replace track taxonomy, repository paths,
  validator/generator commands, reviewer naming, evidence standards,
  theme/index conventions, and report periods with the target repository's
  checked-in contract.
