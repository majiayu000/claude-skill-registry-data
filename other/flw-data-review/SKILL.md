---
name: flw-data-review
description: >
  Analyze frontline-worker submissions on a live opportunity for quality issues, trends, and
  improvement opportunities. Needs a Connect opportunity with visits.
disable-model-invocation: false
---

# FLW Data Review

Analyze FLW data and recommend improvements to communicate to LLOs.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_ids` (+ `program_org`) | the opportunities whose submissions are reviewed | explicit arg; default: the current run's run_state opportunity (or `selected_llo.opportunity_id`); else the program context doc's Scope |
| `archetype` + Evidence Model / success metrics | quantitative vs qualitative review, and what each delivery is judged on | explicit arg; default: the PDD; else the context doc |
| `experiment_id` | the program's chatbot, for § OCS Integration | explicit arg; default: `5-ocs/ocs-agent-setup.md`; else the context doc |
| `report_folder` | where reviews land | default `ACE/<opp-name>/data-reviews/`; on a program project, the project's folder |

No `run_state.yaml` is needed when the ids are passed.

## Process (runs periodically)

1. **Read opportunity context** from GDrive:
   - App summaries and expected data patterns
   - Previous data reviews from `ACE/<opp-name>/data-reviews/`
   - PDD success metrics
   - **PDD `archetype:` and `## Evidence Model` section** — these determine whether this is a quantitative review (`atomic-visit`, query-driven) or a qualitative review (`focus-group`, content-driven). See `## Archetypes` below. The Evidence Model's Layer B is what step 2/3 evaluates per delivery; Layer C is what they evaluate across deliveries.

2. **Query FLW data** via the Connect and connect-labs atoms (there is no
   scout-data MCP — that server was never wired into `plugin.json`):
   - `connect_get_deliver_progress` / `connect_get_learn_progress` (ace-connect) — per-worker
     delivery and Learn counts the opportunity's dashboard shows
   - `explorer_describe({opportunity_ids})` (connect-labs) — the `visits` relation and an
     index of submitted form fields (path, type, fill rate); START HERE
   - `explorer_query({opportunity_ids, sql})` — one read-only SELECT over `visits`. Called
     through canopy it returns rows only for SYNTHETIC opportunities; on a REAL opportunity
     validate the SQL with `explorer_validate` and read the result on the labs page, or use
     a labs pipeline (`pipeline_create` + `pipeline_preview`)
   - Form submission rates by FLW
   - Completion rates and dropout patterns
   - Data quality issues (missing fields, outlier values)
   - Case management compliance
   - Compare against expected metrics from PDD

3. **Self-evaluate (LLM-as-Judge):**
   - Are the identified patterns real signals or noise?
   - Are recommendations specific enough to act on?
   - Is the analysis grounded in data, not speculation?

4. **Generate recommendations:**
   - Specific issues identified (with data evidence)
   - Suggested actions for the Auto-Connect team to relay to LLOs
   - Trends over time (improving, declining, stable)

5. **Write data review** to `ACE/<opp-name>/data-reviews/YYYY-MM-DD-review.md`.

6. **Notify admin group** with summary of findings and recommendations.

## Archetypes

What "FLW data review" means depends on the PDD's `archetype:` field. The base steps above describe a quantitative review (`atomic-visit`); other archetypes review fundamentally different things.

### `atomic-visit`
Quantitative review as written above:
- Submission rates by FLW (vs. expected daily caps)
- Completion rates and dropout patterns
- Outlier detection on numeric fields, photo features, GPS clustering
- Cap and rate-limit violations against the caps Connect actually enforces — the
  payment unit's `max_daily` and `max_total`, both **per worker**. Read the real
  values off the opportunity; do not assume a per-location cap (per market, per
  village, per facility), which Connect has no way to enforce and a PDD should
  not be stating (see `skills/idea-to-pdd/SKILL.md` § `atomic-visit`)
- Per-FLW outliers vs. cohort baseline
- Cross-FLW clustering (suspicious copy-paste patterns)

This corresponds to Layer B and Layer C of the PDD's Evidence Model.

### `longitudinal-visits`
Everything in `atomic-visit`, plus the per-entity views that are the
whole point of the archetype — cross-sectional review cannot see any of
these:

- **Progression** — entities on schedule vs stalled, by phase/sequence
  position. This is usually the partner's headline indicator.
- **Sequence integrity** — out-of-order visits, skipped activities,
  repeated activities within one case.
- **Coverage** — entities with no visit in the expected interval
  (an entity going quiet is invisible to submission-rate-by-FLW).
- **Dedup collapse** — visits submitted that shared an `entity_id` with
  a prior payment. A rising collapse rate means FLWs are doing work that
  will not be paid; that is a training or design signal, not fraud.
- **Per-FLW caseload** — cases owned vs cases actually visited.

This corresponds to Layer B and Layer C of the PDD's Evidence Model,
read along the entity axis rather than the submission axis.

### `focus-group`
Qualitative review — the FLW data is **session content**, not numeric submissions. The skill is acting as a research analyst, not a data quality auditor.

- **Per-session quality** (Layer B): for each session, read the per-domain summary sections — are they specific (with quotes, with examples) or generic (vague themes, no detail)? Is each domain actually covered or skipped? Does the facilitator reflection acknowledge what worked and what didn't?
- **Cross-session synthesis** (Layer C): across all completed sessions, what themes are emerging per segment? Where do segments differ (e.g., women-close-to-PHC vs. men-remote)? Where do they converge? Map findings to the PDD's intervention hypotheses.
- **Saturation check**: are new sessions still surfacing new themes, or are we hearing the same things? If saturation is reached, suggest stopping or moving to the next stage.
- **Quote bank**: extract the most illustrative verbatim quotes per theme, with segment attribution, for the eventual output report.
- **Facilitator coaching signals**: are some facilitators consistently capturing thinner summaries? Suggest probing/training adjustments.

Don't run quantitative checks (submission rates, outlier detection) — they don't apply. Don't grade individual FLWs on volume — sessions are facilitated, not metered.

### `multi-stage`
Run the per-archetype review against each stage's data. For multi-stage PDDs where Stage 2 design depends on Stage 1 findings, the Stage 1 review should explicitly produce input for `learnings-summary` and the Stage 2 PDD revision.

## OCS Integration

The flw-data-review skill mines OCS transcripts alongside CommCare form data
to build a full picture of LLO and FLW experience. Uses these MCP atoms:

- `ocs_list_sessions({ experiment_id })` — full session history for this opportunity's chatbot
- `ocs_get_session({ session_id })` — per-session transcripts
- `ocs_add_session_tags({ session_id, tags: [...] })` — categorize transcripts for downstream skills:
  - `'escalated'` — flagged for human review
  - `'training-gap'` — indicates the training materials missed something
  - `'product-feedback'` — substantive feedback about Connect / CommCare that should feed back to the product team
  - `'data-quality-issue'` — relates to a known data quality pattern from the CommCare analysis

The `experiment_id` for this opportunity comes from
`ACE/<opp-name>/runs/<run-id>/5-ocs/ocs-agent-setup.md`.

### Cross-referencing with CommCare data

When a transcript discusses a specific form submission, correlate via
participant identifier (if passed through `participant_data`) or timestamp
proximity to the form submission timestamp. Flag matched pairs in the review
output so `learnings-summary` can connect "what the LLO asked" to "what actually
happened in the data".

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`
- Connect (ace-connect): `connect_get_deliver_progress`, `connect_get_learn_progress`,
  `connect_list_payment_units` (the real `max_daily` / `max_total` caps)
- Connect (connect-labs): `get_opportunity_apps` for app structure; `explorer_describe`,
  `explorer_query`, `explorer_validate`; `pipeline_create` / `pipeline_preview` for
  recurring extractions
- OCS: `ocs_list_sessions`, `ocs_get_session`, `ocs_add_session_tags`

## Mode Behavior
- **Auto:** Analyze data, write report, email recommendations to admin group
- **Review:** Present findings and recommendations for team discussion

## Dry-Run Behavior
When `--dry-run` is active:
- Write the data review to `ACE/<opp-name>/data-reviews/` as normal
- Write the admin notification content (recipients, subject, body) to `comms-log/dry-run-flw-data-review.md`
- Do not send notifications or emails to the admin group
- State tracks as `dry-run-success`

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-08 | Add `## Archetypes` section: focus-group review = qualitative synthesis (per-session quality, cross-session themes, saturation, quote bank), no quantitative outlier checks | ACE team (PM scout, focus-group framework lens) |
| 2026-04-08 | Read PDD `## Evidence Model` in step 1; Layer B drives per-delivery evaluation, Layer C drives cross-delivery synthesis | ACE team (PM scout, focus-group framework lens) |
| 2026-10-18 | Replace the never-wired scout-data MCP with the real ace-connect progress atoms and connect-labs explorer/pipeline atoms | ACE (maintain-vs-build audit, Tier 3) |
