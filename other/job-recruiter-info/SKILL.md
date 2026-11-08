---
name: job-recruiter-info
description: 'Finds recruiter, hiring-manager and careers contacts for one job or company. Use when the user wants to know who to apply to ("find a recruiter", "who recruits for X", "careers email for X"). Not for B2B contacts (use outreach-enrich-company).'
argument-hint: '"<job listing URL or company name>" [region:<region>] [language:<lang>]'
allowed-tools: Agent, AskUserQuestion, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(test *), Bash(mv *), Bash(rm *), Bash(rmdir *), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Job Recruiter Info

## Overview

You are an orchestrator that runs a one-shot recruiter-contact lookup for a single job target. Given a job listing URL or a company name plus an optional role hint, you dispatch the `job-contact-finder` agent against that target and produce a compact markdown report containing the named recruiter (if any), careers-page email, LinkedIn company page, generic-pattern guesses, apply URL, and a confidence assessment.

This is the standalone counterpart to Phase 6 of `/job-search`. Use it when the user already has a target job and only needs the contacts — no CV, no scoring, no cover letter, no pipeline state.

## When to Use

Looks up apply-target contacts for one job listing or one company, without running the full job-search pipeline.

### When NOT to use

- The user wants to scan many jobs against a CV — use `/job-search`.
- The user wants company contacts for B2B outreach (sales, partnerships) — use `/outreach-research` (full pipeline) or `/outreach-enrich-company` (deepen an existing card) in mz-biz-outreach.
- The user wants to draft a cover letter for that role — use the copywrite skill from mz-creative.
- The user wants to investigate the company itself (reputation, growth, tech) — use `/outreach-research` for a single-company scan.

## Input

- `$ARGUMENTS` — Free-text identifying the target. Either:
  - A canonical job listing URL (`https://jobs.lever.co/...`, `https://boards.greenhouse.io/...`, LinkedIn job link, etc.), OR
  - A company name plus an optional role hint (e.g. `"Acme Corp — Senior Backend Engineer"` or just `"Acme Corp"`).
- Optional modifiers (case-insensitive):
  - `region:<value>` — geographic hint for disambiguation (e.g. `region:DACH`, `region:EU`).
  - `language:<value>` — language hint when the user expects non-English recruiter contacts (e.g. `language:de`, `language:fr`).

If `$ARGUMENTS` is empty, ask the user for a job URL or a company name before invoking.

## Argument Parsing

Extract from `$ARGUMENTS`:

- **target** — the listing URL or company name (everything not matching a parameter pattern).
- **role_hint** — optional, the role description if combined with a company name (split on `—`, `-`, `:`, or `,`).
- **region** — optional, from `region:<value>` (default: derived from the listing URL host or the company domain TLD).
- **language** — optional, from `language:<value>` (default: `en`).

## Directory Structure

- **State** — `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`. Source of truth across phases.
- **Output** — `<PROJECT_ROOT>/.mz/outreach/<run_name>/` (called `<RUN_DIR>` in phase files) holds `target.json` (parsed target), `contacts.json` (raw agent output), and the final `<YYYY_MM_DD>_recruiter_info_<slug>.md` report.

`task_name` follows `<YYYY_MM_DD>_job_recruiter_info_<slug>`; `run_name` is `<YYYY_MM_DD>_job_recruiter_info_<slug>` (same leading-date convention; max 40 chars). Same-day collisions append `_v2`, `_v3`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.

## Core Process

### Phase Overview

| #   | Phase                   | Agent(s)             | Details                       |
| --- | ----------------------- | -------------------- | ----------------------------- |
| 0   | Setup + target parsing  | — (orchestrator)     | Inline below                  |
| 1   | Contact lookup          | `job-contact-finder` | `phases/lookup_and_report.md` |
| 2   | Compact markdown report | — (orchestrator)     | `phases/lookup_and_report.md` |

Read `phases/lookup_and_report.md` when you reach Phase 1.

### Phase 0: Setup + target parsing

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Parse arguments. Derive:

- `task_name` (state dir) = `<YYYY_MM_DD>_job_recruiter_info_<slug>` where `<slug>` is a snake_case summary of the target (max 20 chars, derived from company name or listing host).
- `run_name` (outreach output dir) = `<YYYY_MM_DD>_job_recruiter_info_<slug>` (max 40 chars).

```bash
mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"
mkdir -p "<PROJECT_ROOT>/.mz/outreach/<run_name>"
```

Detect input shape:

- **URL** — `target` matches `^https?://`. WebFetch the page once to extract: `company`, `role_title`, `location_string`, `summary_snippet`. If WebFetch fails, fall back to the URL host as the company hint and surface the failure as a `DONE_WITH_CONCERNS` note in the final report.
- **Company name (with optional role hint)** — Use `target` as `company`; use `role_hint` as `role_title` if provided. Derive the company domain via WebSearch (`"<company>" official site`); first authoritative result is the domain.

Write `<PROJECT_ROOT>/.mz/outreach/<run_name>/target.json`:

```json
{
  "input_type": "url" or "company",
  "input_raw": "<original argument>",
  "company": "<resolved company name>",
  "role_title": "<resolved role title or null>",
  "listing_url": "<resolved URL or null>",
  "company_domain": "<resolved domain or null>",
  "location_string": "<from listing or null>",
  "summary_snippet": "<from listing or null>",
  "region": "<from arg or inferred or null>",
  "language": "<from arg or 'en'>"
}
```

Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`:

```yaml
schema_version: 2
Status: running
Phase: 0
Started: <ISO timestamp>
phase_complete: false
what_remains: []
Target: <input_raw>
InputType: <url|company>
Company: <resolved company>
RoleTitle: <resolved role or null>
RunName: <run_name>
```

After setup completes, read `phases/lookup_and_report.md` and proceed to Phase 1.

## Red Flags

- You fabricated a recruiter name or email that did not appear in any verified source.
- You included a `noreply@`, `no-reply@`, `donotreply@`, `mailer-daemon@`, or `postmaster@` address in the report.
- Marked `confidence: high` without a named recruiter AND a verified email (verified means seen on the listing, careers page, or a named LinkedIn handle).
- Followed a LinkedIn profile URL deep into the platform (only the search-results page is allowed per agent rules).
- Report lives in chat instead of `.mz/outreach/<run_name>/<YYYY_MM_DD>_recruiter_info_<slug>.md`.

## Verification

Before completing, output a visible block showing: target (company + role if known), confidence level (`high`/`medium`/`low`), whether a named recruiter was found, careers-page email status (`verified`/`guessed`/`none`), and the absolute path of the report. Confirm both `contacts.json` and the report file exist on disk.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Resume Support

Before creating anything in Phase 0, check if `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` exists for the resolved `task_name`. If it does, read the `Phase` field and resume from the next incomplete phase. All phases are idempotent — re-running overwrites output files.

## Error Handling

- Agent returns empty: append an `Errors:` bullet in `state.md`, write a report that explicitly says "no contacts surfaced" with the `ZERO RESULTS VERIFIED` or `ZERO RESULTS UNVERIFIED` disclosure tag from the agent.
- Agent returns `STATUS: NEEDS_CONTEXT`: invoke `AskUserQuestion` to fill the missing field (typically the company domain), then re-dispatch.
- Agent returns `STATUS: BLOCKED`: stop the pipeline, set `Status: blocked` with the cause in `what_remains`, surface the cause to the user.
- Never fabricate data — incomplete results are better than false results.
- Listing URL was provided but unreachable: degrade to `input_type: company`, surface the WebFetch failure in the final report.
