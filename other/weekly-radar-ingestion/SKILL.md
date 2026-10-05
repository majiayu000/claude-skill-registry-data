---
name: weekly-radar-ingestion
description: "Ingest Ray-reviewed systems or creation radar reports into the ai-signal-radar repository as durable signal records. Use when the user asks to ingest this weekly radar, add this reviewed report, import this week's signal report, store this AI radar, archive this reviewed report, or otherwise turn an approved AI signal report into radars/, data/, themes/, indexes/, and a commit."
---

# Weekly Radar Ingestion

## Purpose

Ingest one Ray-reviewed AI Signal Radar report into
`ai-signal-radar` as an approved signal record for future AI agents. Treat the
report as canonical input, not as a draft or news clipping. Preserve Ray's
reasoning and use additive, deterministic updates.

If details are missing, leave structured fields empty or ask for the missing
date. Never fabricate dates, themes, signals, action items, or importance.

## Repository Contract

Before editing, inspect the target repository from its root:

- `README.md`
- `schemas/`
- existing `radars/`, `data/`, `themes/`, and `indexes/`
- available scripts under `scripts/`
- `git status --short`

Prefer existing repository scripts and schemas when they exist. If a schema is
stricter than the recommended metadata below, conform to the checked-in schema
unless the user explicitly asks to update the repository schema too.

Read `references/repository-contract.md` when the repository structure, schema,
or theme file format is unclear.

## Workflow

### 1. Detect Track And Report Date

Select an explicit repository track from the approved report and user intent:

- `systems` for AI systems engineering and infrastructure;
- `creation` for AI-native creation, human behavior, and creative forms.

Do not combine tracks. Creation reports also require explicit observation
window start and end dates.

Determine one `YYYY-MM-DD` report date using this order:

1. Explicit user instruction.
2. Metadata block in the report, such as `date:`.
3. Report title or filename containing an ISO date.
4. A clear week-ending date inside the report body.

If no date is reliable, stop and ask for the date. Do not infer a date from the
current day unless the user explicitly says the report is for today.

Set `week` to an ISO week string such as `2026-W25` when useful. Leave it empty
if the repository schema does not support it.

### 2. Store the Original Report

Write the reviewed Markdown report to:

```text
radars/<track>/YYYY/YYYY-MM-DD.md
```

Preserve content. Normalize only:

- heading levels and spacing
- Markdown list and code-fence formatting
- links
- frontmatter or metadata block

Do not significantly rewrite the report. Do not summarize sections. Do not
remove caveats, reasoning, uncertainty, or Ray-specific judgment.

Use `templates/report.md` only as a formatting reference; do not force a report
into that structure if it would rewrite content.

### 3. Generate Metadata

Write structured metadata to:

```text
data/<track>/YYYY/YYYY-MM-DD.json
```

Recommended agent-friendly fields:

```json
{
  "schema_version": "2.0",
  "radar_type": "systems or creation",
  "date": "",
  "week": "",
  "title": "",
  "status": "reviewed",
  "reviewed_by": "Ray",
  "themes": [],
  "importance": 0,
  "top_signals": [],
  "action_items": []
}
```

When the repository already has `schemas/radar.schema.json`, validate against
that schema and use its field names. In the current ai-signal-radar schema,
store signal objects in `signals`, recurring creation forms in `patterns`, ideas
in `ideas`, and source provenance in `source`. Creation signals may preserve
domain, creator, evidence level, what was created, what AI changed, human
behavior change, and a transferable idea. Do not add unsupported properties
unless the schema is updated in the same change.

Use `templates/metadata.json` as the neutral metadata shape for repositories
without a stricter schema.

### 4. Extract Themes

Extract themes only from explicit report labels, metadata, headings, repeated
topic framing, or unambiguous signal content. Use lowercase hyphen slugs.

Known examples:

- `coding-agents`
- `agent-runtime`
- `llm-infrastructure`
- `evaluation`
- `observability`
- `backend-architecture`
- `ai-platforms`
- `ai-security`
- `mlops`

If a report has no explicit themes, set `themes` to `[]` and continue. If a
report introduces a genuinely new explicit theme, create that theme file rather
than forcing it into an existing bucket.

Maintain one file per theme under:

```text
themes/<track>/<theme>.md
```

Each theme file should keep these sections:

- `# <theme>`
- `## Summary`
- `## Related Reports`
- `## Notable Recurring Signals`

Use `templates/theme.md` for new theme files. Prefer additive updates to
existing theme files and keep report links stable.

### 5. Update Indexes

Update machine-readable indexes after metadata and theme files are written.
Prefer the repository's existing index names and scripts. In ai-signal-radar,
run:

```bash
python scripts/update_indexes.py
```

If no repository script exists, maintain:

- `indexes/reports.json`
- `indexes/themes.json`

Indexes should optimize future agent retrieval with dates, titles, themes,
Markdown paths, data paths, and compact signal references.

### 6. Validate Consistency

Verify:

- report file exists
- metadata file exists
- metadata date, status, reviewer, paths, and themes are coherent
- creation metadata contains a valid observation window
- every theme reference points to an existing report
- indexes include the ingested report and reference valid files

Use repository validation first when available, for example:

```bash
uv run pytest
```

Then run the bundled consistency helper:

```bash
python .codex/skills/weekly-radar-ingestion/scripts/validate_ingestion.py \
  --repo . --track <track> --date YYYY-MM-DD
```

Fix validation failures before committing.

### 7. Commit

Generate a concise commit message after validation, such as:

```text
ingest radar YYYY-MM-DD
```

or:

```text
update themes from radar YYYY-MM-DD
```

Commit only the ingestion-related files. Push only when the repository has an
ordinary configured remote/upstream and push is allowed by the user's request or
repository workflow. Never force-push.

## Rules

1. Treat the report as approved.
2. Preserve Ray's reasoning.
3. Do not summarize unless a structured field requires extraction.
4. Do not delete information.
5. Prefer additive changes.
6. Maintain deterministic paths and JSON ordering.
7. Optimize for future AI-agent retrieval.
8. Favor machine-readable metadata over prose.
9. Never fabricate themes, dates, signals, action items, or importance.
10. Leave missing fields empty rather than guessing.

## Portability Notes

- Specific to the author's current workflow: this assumes Ray-reviewed systems
  and creation radar reports and an `ai-signal-radar` repository with explicit
  tracks under `radars/`, `data/`, and `themes/`.
- Reusable: approved-report preservation, explicit track selection,
  deterministic track/date paths, schema-first metadata extraction, additive
  theme/index updates, and validation-before-commit discipline.
- Adapt before reuse: replace reviewer naming, track taxonomy, observation
  window requirements, repository layout, schema fields, validation commands,
  commit policy, and theme taxonomy with the target repository's checked-in
  contract.

## Bundled Resources

- `templates/report.md`: optional Markdown shape for normalized reports.
- `templates/metadata.json`: neutral metadata template.
- `templates/theme.md`: new theme file template.
- `templates/reports-index.json`: fallback reports index shape.
- `templates/themes-index.json`: fallback themes index shape.
- `examples/`: sample reviewed reports for normal ingestion, missing themes,
  and a new theme.
- `scripts/validate_ingestion.py`: repository consistency checker.
