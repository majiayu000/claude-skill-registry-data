---
name: frontier-tracker
description: Use when the user asks to track, scan, monitor, digest, or maintain a reading queue for new papers from top journals, Nature/Science/Cell/PNAS families, or any research field. Works with any discipline — ecology, environment, CS, medicine, physics, social sciences, etc.
---

# Frontier Tracker

Use this skill to run a personal literature surveillance workflow. Keep every output concise, dated, and easy to act on.

## Load the minimum context

- **Windows encoding:** Always run Python scripts with `python -X utf8` on Windows to avoid GBK encoding errors.
- Read `references/source-and-selection-rules.md` when building or refreshing the journal pool.
- Read `references/top-journal-families.md` when the user asks for top journals, Nature/Science/Cell/PNAS family tracking, or when no ranking export is available.
- Run `python -X utf8 scripts/build_top_family_watchlist.py --format json` to turn the top-family seed list into a machine-readable watchlist; add `--resolve-openalex` only when ISSN/OpenAlex source IDs are needed.
- Run `python -X utf8 scripts/scan_recent_papers.py --days 7 --update-state --output outputs/data/frontier_scan_<date>.json` for repeatable top-family scans with DOI/OpenAlex de-duplication.
- After the scan, run `python -X utf8 scripts/enrich_abstracts.py --input outputs/data/frontier_scan_<date>.json --output outputs/data/frontier_enriched_<date>.json --field new` to fill missing abstracts via three-way fallback (OpenAlex → Crossref → Semantic Scholar).
- Then run `python -X utf8 scripts/screen_by_profile.py --input outputs/data/frontier_enriched_<date>.json --output outputs/data/frontier_screened_<date>.json --profile references/<profile>.md --field both` to classify papers into core / proxy / eco / noise tiers using profile keywords.
- Read `references/example-profile.md` when the user needs help creating a research profile.
- Read `references/research-profile-template.md` only when the user wants to replace or extend their profile.
- Read `references/output-templates.md` when producing a daily digest, weekly report, reading list, or reminder list.
- Read `references/display-output-options.md` when the user asks how results should be shown, saved, exported, or reviewed.
- Run `python -X utf8 scripts/render_display_outputs.py --mode <excel|app|notes|codex>` after a scan when the user chooses a display form.

## Follow the operating rules

- Use exact dates. Say `As of <date>` instead of only `today` when reporting.
- Prefer official sources for rankings and journal scope. Do not invent rankings.
- Do not make ranking imports a hard prerequisite. The top-journal-family seed pool can run first and should remain trackable even when ranking data is missing.
- If a journal qualifies for `full-track` in any system, keep it in `full-track`.
- If a journal qualifies through the top-family seed pool, keep it in the watchlist and label the rank basis as `top-family seed; ranking pending`.
- If official ranking access is blocked, say so plainly and ask for an export or screenshot instead of guessing.
- If a paper is in the `full-track` pool but weakly related to the user's topic, keep it in the digest and mark it `low-relevance` rather than dropping it.
- Default to literature tracking outputs, not proposal-writing or review-writing outputs, unless the user explicitly asks.

## Build or refresh the journal pool

- Confirm the scope with the user.
- Start with the top-journal-family seed pool from `references/top-journal-families.md`.
- Run `scripts/build_top_family_watchlist.py` when a concrete watchlist table, JSON, CSV, or source-id lookup is needed.
- Add field-specific or local journals when the user requests them.
- Save or restate the pool in a compact table when the user asks for the watchlist.

## Establish the research profile

- Check for an existing profile in `references/`.
- Ask only for missing fields.
- Capture at least: core topics, secondary topics, methods, exclusion topics, and reading capacity.
- If the user has no fixed profile yet, build a draft from the last 5–10 papers they considered central.
- See `references/example-profile.md` for examples.

## Track new papers

- Search the defined journal pool for new papers in the stated time window.
- Prefer `scripts/scan_recent_papers.py` for top-family seed scans.
- By default the scan script excludes news, briefings, corrections, and retractions; add `--include-non-research` only when explicitly asked.
- Record: title, year, authors, journal, publication date, DOI, pool source, topic tags, and relevance.
- Separate results into `new`, `already seen`, and `needs manual verification`.

## Filter by topic

- Apply the research profile to title, abstract, keywords, methods, study system, and geography.
- Score relevance as `high`, `medium`, or `low`.
- In the `relevant-only` pool, keep only `high` and `medium` unless the user asks for exhaustive output.
- Distinguish `core`, `proxy`, and `noise` literature.

## Generate the Monday report

- Group papers into `must read`, `should read`, `watchlist`, and `notable methods or data`.
- Highlight repeated trends across multiple papers.
- Include exact coverage dates for the report window.
- End with a short action list for the coming week.

## Choose the display form

- The user decides the display form. If not specified, ask: `How would you like the results displayed: Excel, interactive HTML table, Obsidian/Zotero notes, or inline preview?`
- Supported forms: `excel`, `app`, `notes`, `codex`.
- Do not silently default to Markdown or HTML when the user has not chosen.

## Maintain the reading list

- Track statuses: `to-screen`, `queued`, `reading`, `noted`, `archived`, `skip`.
- Store durable scan state in `state/reading_state.json` for recurring monitoring.
- For ad hoc previews, run scan scripts without `--update-state`.
- Promote high-relevance items first.
- Keep the queue small enough to fit the user's declared weekly capacity.

## Keep the interaction practical

- Start by confirming the task mode: `refresh pool`, `daily scan`, `topic filter`, `weekly report`, `reading backlog`, or `reminder list`.
- For output tasks, confirm the display mode unless already specified.
- Ask one concise follow-up question only when missing information blocks a reliable answer.
