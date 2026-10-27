---
name: synthetic-summary
description: >
  Internal /ace:run step — DEPRECATED fallback: one-page reviewer summary of a synthetic-data
  demo.
user-invocable: false
disable-model-invocation: false
---

# Synthetic Summary

> **Deprecated (Plan C convergence, 2026-07-21).** Superseded by the `/ace:demo`
> pipeline (`demo-narrative` + the canopy DDD loop); Phase 7 no longer dispatches
> this. Kept as a fallback until the converged path is validated — see
> `agents/synthetic-data-and-workflows.md` § Deprecated skills.

Stage 1 sibling of `synthetic-data-generate`. Reads the Phase 7 artifacts in
the run folder and produces a single markdown page a Dimagi staffer can
forward to a stakeholder ("here is what this opportunity looks like running
well"). Pure aggregator — no MCP calls beyond Drive reads/writes, no eval.

In Stage 1 the only Phase 7 inputs are the data-generate summary and its
manifest. Later stages add walkthrough slideshows, workflow URLs, and
narrative-plan output; this skill grows to bundle them then.

## Inputs

Pipeline-only: summarises a run's Phase 7 synthetic demo from that run's artifacts.

| Source | Artifact | Used for |
|---|---|---|
| Phase 7 | `7-synthetic/synthetic-data-generate.md` | labs URL, GDrive folder ID, record counts |
| Phase 7 | `7-synthetic/synthetic-data-generate_manifest.yaml` OR `7-synthetic/synthetic-narrative-plan.yaml` | FLW personas, cohort size, anomalies, timeline (for the narrative paragraphs) |
| Phase 7 (optional) | `7-synthetic/synthetic-narrative-plan.md` | richer prose narrative — preferred over the manifest's bare data when present |
| Drive | `ACE/<opp>/opp.yaml` | `display_name`, `slug`, opp-level context |
| Current run's `run_state.yaml` | `phases.synthetic-data-and-workflows.products.synthetic.*` — `walkthroughs[]`, `workflows`, `generated_at`, etc. | Stage 2/3 content sections |

## Products

- `7-synthetic/synthetic-summary.md` — one-page reviewer-facing summary
- `run_state.yaml.phases.synthetic-data-and-workflows.synthetic-summary: done`

## Process

1. **Read Phase 7 artifacts.**

   **Resolve the current run-id.** Call
   `mcp__plugin_ace_ace-gdrive__resolve_current_run_id({slug: '<opp>'})`
   — returns `{run_id, run_folder_id}` (newest folder under
   `<opp>/runs/`; run-ids are `YYYYMMDD-HHMM` so lex == chronological).
   If `run_id` is `null`, halt with "no runs found — run
   `/ace:step synthetic-data-generate --opp <slug>` first." (Replaces
   the old `opp.yaml.last_run_id` read, which has been a dead field
   since 2026-05-10 — see `lib/artifact-manifest.ts`.)

   From `ACE/<opp>/runs/<run_id>/7-synthetic/`, read via
   `mcp__plugin_ace_ace-gdrive__drive_read_file`:

   - `synthetic-data-generate.md` — labs URL, GDrive folder ID, record
     counts, any warnings
   - The active manifest: prefer `synthetic-narrative-plan.yaml` (Stage 2)
     when present; fall back to `synthetic-data-generate_manifest.yaml`
     (Stage 1).
   - `synthetic-narrative-plan.md` (Stage 2, optional) — its prose seeds
     the "What you'll see" paragraphs more directly than the manifest
     can. Skip if absent.

   If `synthetic-data-generate.md` is absent, halt with: "run
   `/ace:step synthetic-data-generate --opp <slug> --opp-int-id <int>` first
   — this skill aggregates its output."

   Read `ACE/<opp>/opp.yaml` for `display_name` + `slug`. Read the
   current run's `run_state.yaml` for
   `phases.synthetic-data-and-workflows.products.synthetic.*`
   — the `walkthroughs[]` list (Stage 2 — empty in Stage 1, populated
   per-persona by `synthetic-walkthrough-run`), `workflows`,
   `generated_at`. Per-run only — this skill summarizes the current
   run's synthetic state, not a cross-run history.

2. **Compose the summary** at
   `ACE/<opp>/runs/<run_id>/7-synthetic/synthetic-summary.md`. Shape:

   ```markdown
   # <opp.yaml.display_name> — Synthetic Demo

   **Opp:** `<slug>` · **Fixture run:** `<run_id>` · **Generated:** <ISO from `products.synthetic.generated_at`>

   **See it live:** <labs URL from synthetic-data-generate.md> ← clickable

   **Fixture folder (read-only, for review):** <GDrive folder URL from synthetic-data-generate.md>

   ## Demonstrative workflows (Stage 3)

   Render this section ONLY when `products.synthetic.workflows.{llo_weekly_review_id, program_admin_audit_id}` are populated. For each:

   - **LLO Weekly Review** — when `synthetic-workflow-seed.md` recorded a saved run, deep-link the latest run so the polished dashboard renders directly (skips the run picker / "select an opportunity" gate): `${LABS_BASE_URL}/labs/workflow/<llo_weekly_review_id>/run/?run_id=<week_2_run_id, else week_1_run_id>&opportunity_id=<labs_opp_id>` (clickable). If no run was saved, fall back to `${LABS_BASE_URL}/labs/workflow/<llo_weekly_review_id>/?opportunity_id=<labs_opp_id>` (lands on the run picker).
     - Saved-runs progression (when `synthetic-workflow-seed.md` records `Week 1 run_id` + `Week 2 run_id`): "Week 1 → Week 2 trend visible: <one-line description from the manifest's `coaching_arcs[]` or `anomalies[]`>".
   - **Program Admin Audit** — deep-link the saved audit run when recorded: `${LABS_BASE_URL}/labs/workflow/<program_admin_audit_id>/run/?run_id=<audit_run_id>&opportunity_id=<labs_opp_id>` (clickable); else `${LABS_BASE_URL}/labs/workflow/<program_admin_audit_id>/?opportunity_id=<labs_opp_id>`.
     - "Reads the LLO Weekly Review's saved runs to render week-over-week LLO process compliance."

   If polish ran (`synthetic-workflow-polish.md` exists), append: "Per-opp visuals applied: <patches_applied count> patches across hero / FLW cards / anomaly callouts / domain branding."

   If polish-eval's verdict scored visual-judge dimensions, append: "Visual-judge: hierarchy=<score>, brand-fit=<score>." Skip if either is null (capture failure).

   When `synthetic.workflows` is empty, omit this section.

   ## What you'll see

   <Paragraph 1 — opp context.>
   One sentence summarizing the opp from the PDD's intervention summary
   (or display_name if PDD not read here). Then one sentence on the
   four-week cadence and total dataset size: "<N> synthetic FLWs delivered
   <M> visits across <K> beneficiaries over <weeks> weeks." Numbers come
   from the manifest's `flw_personas`, `beneficiary_cohorts[].size`,
   `timeline.weeks`, and `record_counts.user_visits`.

   <Paragraph 2 — the cast.>
   Walk the reader through the FLW roster: who's a rockstar, who's
   steady, who's struggling, who's new. Use the manifest's
   `flw_personas[].display_name` and `archetype`. If any persona has
   notes or an `improvement_arc`, mention them. The point is to show
   the data was authored, not random.

   <Paragraph 3 — the story.>
   Describe what a stakeholder will notice in labs. If `anomalies` is
   non-empty, name them ("Dinesh's weight outliers spike in week 3";
   "Esi missed two follow-ups in week 2"). If `kpi_config` has KPIs,
   describe what each measures and the threshold. If both are empty
   (default Stage 1 manifest), be honest: "This is a baseline dataset —
   no anomalies seeded yet. Add them by editing the manifest and
   re-running synthetic-data-generate."

   ## Persona walkthroughs (Stage 2)

   Render this section ONLY when `products.synthetic.walkthroughs[]` is
   non-empty. For each entry:

   - **<persona display name>** — `<eval_score>/5` average · captured
     `<run_at>`
     [Open slideshow](<webViewLink of slideshow_artifact>)

   Group by persona; if a persona has multiple runs (re-captures), list
   the most recent first and show older runs collapsed under "Earlier
   captures."

   If `walkthroughs[]` is empty, omit this entire section — don't emit
   "no walkthroughs yet." A stakeholder reading a Stage 1 summary
   shouldn't see promises about Stage 2 deliverables that didn't run.

   ## What's next

   Phase 7 ships in stages — emit only the lines that match THIS opp's state:

   - When `products.synthetic.workflows` is empty: "Stage 3 (demonstrative workflows) hasn't run for this opp — `/ace:step synthetic-workflow-seed` instantiates the LLO weekly review + program admin audit."
   - When `synthetic.workflows` exists but `synthetic-workflow-polish.md` is absent: "Stage 3.2 (polish) hasn't run — `/ace:step synthetic-workflow-polish` applies hero panels + named FLW cards + anomaly callouts."
   - When `synthetic.walkthroughs[]` is empty: "Stage 2.6 (persona walkthroughs) hasn't run — `/ace:step synthetic-walkthrough-run` produces stakeholder-ready slideshows. Requires `/ace:labs-login` first."
   - Always: "To regenerate this opp's data with a different manifest, run `/ace:step synthetic-data-generate --opp <slug>`. To fully disable synthetic mode, call `mcp__connect-labs__synthetic_disable(opportunity_id=<int>)`."

   Skip the entire section if all three stage gaps are filled (the demo is complete).
   ```

   Write via `mcp__plugin_ace_ace-gdrive__drive_create_file`. If the file
   already exists (re-run), overwrite via `drive_update_file`.

3. **Update `run_state.yaml`** via `update_yaml_file`:

   ```yaml
   phases:
     synthetic-data-and-workflows:
       synthetic-summary: done
   ```

## MCP Tools Used

- `mcp__plugin_ace_ace-gdrive__drive_read_file`
- `mcp__plugin_ace_ace-gdrive__drive_create_file`
- `mcp__plugin_ace_ace-gdrive__drive_update_file`
- `mcp__plugin_ace_ace-gdrive__update_yaml_file`

## Mode Behavior

Aggregator only — same behavior in auto and review modes. No external
side effects beyond writing the summary file.

## Dry-Run Behavior

`--dry-run` is a no-op pass-through: write the summary as normal (no
external side effects in this skill anyway). State tracks as
`dry-run-success`.

## Failure Modes

| Failure | Detection | Recovery |
|---|---|---|
| `synthetic-data-generate.md` missing | step 1 halt | Run `synthetic-data-generate` first. |
| Manifest YAML malformed | step 2 fallback | Skip persona-walk paragraph; emit a `> manifest unparseable — narrative truncated` banner and continue. |
| ``phases.synthetic-data-and-workflows.products.synthetic.generated_at`` missing | step 2 fallback | Use file-modified timestamp of `synthetic-data-generate.md` instead. |

## Related skills

- `synthetic-data-generate` — produces the inputs this skill aggregates.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-06 | Initial Stage 1 MVP skill — three-paragraph reviewer summary aggregating data-generate output | ACE team (Plan B Stage 1) |
| 2026-05-06 | Stage 2: prefer `synthetic-narrative-plan.{md,yaml}` when present; render Persona Walkthroughs section from `products.synthetic.walkthroughs[]`. Section is omitted entirely when empty (Stage 1 summaries unchanged). | ACE team (Plan B Stage 2) |
| 2026-05-07 | Stage 3+: render Demonstrative Workflows section from `products.synthetic.workflows.{llo_weekly_review_id, program_admin_audit_id}`; surface saved-runs Week-1/Week-2 trend (Stage 3b) + polish patch count + visual-judge scores (post canopy:visual-judge wire-up). Replace the static "What's next" block with conditional gap-detection so the summary self-describes which stages haven't run for this opp. | ACE team (Plan B Stage 3+) |
| 2026-06-13 | Demonstrative-workflow links now deep-link the saved run (`/labs/workflow/<id>/run/?run_id=<run_id>&opportunity_id=<opp>`) so they render the polished dashboard directly instead of the run picker; fall back to the bare URL only when no run was saved. Recipe per `docs/learnings/2026-06-13-labs-workflow-run-deeplink.md` (jjackson/ace#769). | ACE team |

<!-- audit-fix marker for 0.13.76 -->
