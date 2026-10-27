---
name: simulated-execution
description: >
  Run N backdated weeks of a program with no real LLO: synthetic visits, weekly stock and reviews.
---

# Simulated execution

Runs a program's delivery for N simulated weeks after the award, with no real LLO involved. The
visits are synthetic, the week's stock moves through labs supply chain, labs saves one report run
per week, and each week gets a review an LLO and a program manager could act on. Everything is
dated in the past (`lib/sim-calendar.ts`), because labs has no clock to move.

In `/ace:run` this is the optional `simulate_weeks` step, run by `agents/execution-manager.md`
§ Simulated mode, Phase 9 `mode: simulated` only (spec
`docs/superpowers/specs/2026-10-18-optional-labs-e2e-steps.md` § G). It is OFF by default.

**It never contacts anyone.** No email, no Connect invite, no `llo-onboarding`, no Connect
opportunity mutation. The visits live on a labs-only opportunity filed under the ACE winner org,
never on the run's real Phase 4 opportunity.

**The bar is what a viewer sees, not what the files say** (owner, 2026-10-21, ace#3265). A
simulated delivery is done when labs' own pages show a supply chain working: stock leaving the
central store, workers holding phones between visits, handovers labs read off the visits, a map,
and a programme, partner and worker report to open. connect-fi/20261018-1440 passed every file
check while 44 of 814 phones moved and every worker sat at 0; `simulated-execution-qa`'s
`supply_in_motion` and `downstream_reports` checks now fail that.

**One synthetic programme holds everything.** The labs-only opportunity is its own programme
(`program_id = opportunity_id`), and the whole supply chain (`supply-chain-setup`, `-procure`,
`-fulfil`, `-operate`) is built on THAT programme id, never on the run's Connect program. Labs
reads visits into a worker's stock only when the visits' opportunity and the supply chain are on
one registered synthetic programme (connect-labs `supply_chain/scopes.py` `opportunity_problem`);
across programmes a dispensing rule is refused ("opportunity 10168 belongs to programme 10168,
not 361", ace#3265). That is why this skill's Steps 1-3 run first, at Phase 9 S0b, before
`supply-chain-setup`: they create the programme the supply chain is built on.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `calendar` | week 0 + delivery weeks | explicit arg; default: run_state `phases.execution-management.products.simulation.calendar` (written by the agent's S0 from `scripts/sim-calendar.ts`) |
| `weeks` | N | explicit arg; default: run_state `optional_steps.simulate_weeks` |
| `winner_org_name` | the org the labs-only opportunity is filed under | explicit arg; default: the display name of `connect_orgs.llo_org` (`selected_llo.org_slug`) |
| `program_name` | the labs-only opportunity's program name | explicit arg; default: the PDD's program title |
| `template_workflow` | the semantic-snapshot report cloned for the weekly runs (the programme report) | explicit arg `{workflow_id, program_id}`; default: run_state `phases.synthetic-data-and-workflows.products.synthetic.cascade.programme_report`. Never `cascade.worker_review` for the weekly history: it is a drill-down template with no snapshot contract, and `workflow_history_eligibility` answers it `template_not_saved_runs` (ace#3263) |
| `partner_template`, `worker_template` | the partner (opportunity) report and the worker review cloned beside it, so a viewer can go programme → partner → worker | explicit args; default: the first `role: opp_report` dashboard of run_state `products.synthetic.source.dashboards` and `products.synthetic.cascade.worker_review` |
| `geography` | where the workers and stores are, so Map draws them | explicit arg `{country, admin_area, centers: [{lat, lon, label}]}`; default: the PDD's delivery area, geocoded once to its public coordinates (district or village centroids) and cited in the plan. Never invent a place the PDD does not name |
| `float_weeks` | how many weeks of handovers a worker carries | explicit arg; default: the PDD's stated worker stock, else `2` (a simulation assumption the plan and every review state as such) |
| `registry_eval_verdict` | the registry gate of `scripts/run-labs-synthetic-generate.ts` | explicit arg (a local file); default: a local copy of the run's `7-synthetic/semantic-registry-author-eval_verdict.yaml` |
| `pdd_targets` | what each week is judged against (ID, SIM, phone, wallet funded) | explicit arg; default: the PDD's Performance Measures section (run_state `phases.idea-to-design.products.pdd`) |
| `supply_chain` | whether each week also runs `supply-chain-operate` | explicit arg; default: run_state `optional_steps.supply_chain` |
| `out_folder_id` | where the files go | explicit arg; default: the run's `9-execution-manager/` folder |

Outside a run, pass every parameter; nothing reads or writes `run_state.yaml`.

## Products

- `9-execution-manager/simulated-execution_plan.yaml`: the window, the synthetic-data manifest
  (whose persona ids are the setup plan's FLW usernames, so distributions map to workers 1:1), and
  the per-week enrolment the PDD implies. Written **before any write**.
- `9-execution-manager/simulated-execution_issue-events.yaml` (with `supply_chain`): per commodity,
  its `issue_event`, its `issue_events_source` and the note `deriveIssueEvents` returned, and per
  delivery week and worker the issue events and the quantity they give. What each week's
  `week_activity` is.
- `9-execution-manager/simulated-week-<w>_review.md`: one per delivery week, by
  `simulated-weekly-review`.
- `9-execution-manager/simulated-execution_summary.md`: links every weekly review, the labs report
  run for each week, and the supply-chain programme pages.
- `9-execution-manager/simulated-execution_supply-motion.yaml` (with `supply_chain`): labs'
  `stock_flow` and `worker_stock` reads as of the last delivery day and `assessSupplyMotion`'s
  verdict (`lib/sim-supply-motion.ts`): what `simulated-execution-qa` gates on.
- run_state `phases.execution-management.products.simulation`: `synthetic_opportunity_id`,
  `program_id` (= the opportunity id: labs files it as its own programme), `workflow_id`,
  `reports: {programme, partner, worker}` (each `{workflow_id, url}`), `weekly_reviews[]` (the
  calendar was written by the agent's S0). Each id is written **the moment its create call
  returns**, because a re-run would otherwise create a second copy (ace#2412).

## Process

Phase 9 runs this skill in two halves: **Steps 1-3 at S0b**, before `supply-chain-setup`, because
they create the programme the supply chain is built on; **Steps 4-9 at S4**, after week 0's
procurement and fulfilment.

1. **Preconditions.** Calendar present and valid (`assertSimCalendar`); `selected_llo.synthetic_winner: true`.
   Any miss halts with `[BLOCKER]` naming it. (At S4, additionally, with `supply_chain`,
   `supply-chain-procure-qa` and `supply-chain-fulfil-qa` both `pass`: never start week 1 on a
   broken week 0.)
2. **Plan** (first Products file). The manifest's `timeline` is `deliveryWindow(calendar)`, and
   visit cadence follows the PDD's enrolment target spread over N weeks. Plant one under-performing
   worker so the reviews have something to act on. Three things the viewer depends on, each
   stated in the plan:
   - **Geography.** The manifest carries `geography` (`persona_centers` at the plan's `centers`,
     one per worker's area), so every visit has GPS and labs places each worker on Map from their
     visits. Without it Map draws nothing real (connect-fi's manifest had none).
   - **Handovers at the PDD's rate.** The issue field (the commodity's `issue_event.field`, e.g.
     `form.phone_screen.phone_obtained`) is authored so that about `eligible_share` of
     beneficiaries reach a "handed over" answer by their later visit inside the window. Check the
     authored pool before generating: count the beneficiaries whose visits carry a handover answer
     and compare with `eligible_share × beneficiaries with a later visit`. A pool where nearly
     every answer is `not_yet` simulates a programme that never hands anything over (connect-fi:
     40 of 400 adults in four weeks against a share of 0.55).
   - **A stated quantity.** Where the Deliver app records how many were handed over, author that
     field too (a number), so the dispensing rule can read an exact `stated` line rather than an
     estimated `protocol` one.
3. **Create the labs-only opportunity (= the simulation programme), then generate the visits into
   it once**, for the whole window (the C1 pattern of `demo-data-setup`; ace#3263).
   1. `synthetic_create_labs_only({label: "<opp> simulated delivery", gdrive_folder_id:
      'pending-generate', org_name: <winner_org_name>, program_name, notes: "<sweep handle: opp/run
      id>", allowed_domains: ['@dimagi.com', '@dimagi-associate.com', '@dimagi-ai.com']})`, with
      `program_id` UNSET so the opportunity is its own programme. Write
      `products.simulation.synthetic_opportunity_id` AND `products.simulation.program_id` (the
      same id) the moment it returns (ace#2412). Without ACE's own domain in `allowed_domains`,
      ACE cannot read what it just created, and labs refuses to declare a runner on it.
   2. Generate with the plugin's own script, which reads the manifest off disk, so the archived
      manifest is the one labs received:

      ```bash
      ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
      node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/run-labs-synthetic-generate.ts" <plan's manifest> --opportunity-id <synthetic opp> --registry-eval-verdict <registry_eval_verdict>
      ```
   3. Record labs' returned `record_counts` verbatim in the plan, never the manifest's authored
      totals: on connect-fi/20261018-1440 the generator kept 1,557 of 1,614 authored visits.

   **Generate once.** Re-generating into an opportunity labs has already read gives the visits
   new ids, and the dispensing rule then hands every phone over twice; a second generation needs
   a fresh opportunity. **Never generate against the run's real Phase 4 opportunity:**
   `synthetic_generate_from_manifest` registers its target opportunity as synthetic.
   `synthetic_clone_to_labs_only` is not part of this step.

   *Phase 9 now runs S1-S3 (`supply-chain-setup`, `-procure`, `-fulfil`) with `program_id` =
   `products.simulation.program_id`, then returns here at Step 4.*
4. **Issue events and top-ups** (with `supply_chain`; ace#3216, ace#3265). Read the generated
   `user_visits.json` from the fixture folder the generator returned (`drive_read_file`), and for
   each commodity in the setup plan call `deriveIssueEvents({commodity, issue_event, visits,
   calendar, seed: <manifest random_seed>})` (`lib/supply-chain-issue-events.ts`). Then plan what
   each worker is ISSUED with `planWorkerTopUps({issues, weeks: N, float_weeks})`
   (`lib/sim-supply-motion.ts`): each week the LLO issues that week's handovers plus what brings
   the worker back to their float (two weeks of their average handovers), so stock leaves the
   store every week and every worker holds phones between visits. Never withhold a top-up to plant
   a stockout: labs' dispensing rule takes every handover off the worker's stock from the visits,
   so a withheld top-up drives the ledger negative. The planted stockout is a worker's
   self-reported zero count (`supply-chain-operate` Step 5), which labs reads as variance against
   the ledger. Write the second Products file
   with both: per week and worker the issue events, their quantity, and the planned `top_up`.
   - Mirror-mode visits carry form identity, so a `form_answer` issue event is read off the visits
     (`source: form_answer_visits`). Labs' de-novo stream merges every form into one schema and
     carries no form identity; for that case the helper generates the handovers from the PDD's
     `eligible_share` (`source: simulated_from_eligibility`), and the summary and every review say
     so. With no `eligible_share` it throws, and the step halts with `[BLOCKER]` quoting it.
5. **The reports a viewer opens: programme, partner, worker.** On the synthetic opportunity, clone
   each with `workflow_clone({source_workflow_id, source_program_id, target_opportunity_id: <synthetic
   opp>, linked: true, new_name: "<opp> simulated <role>"})` and write
   `products.simulation.reports.<role>` the moment each returns:
   - **programme** from `template_workflow` (this is also the weekly history workflow,
     `products.simulation.workflow_id`);
   - **partner** from `partner_template` (an `indicator_opp_report`: the LLO's own view with its
     workers' table);
   - **worker** from `worker_template` (`indicator_worker_review`: the drill-down a worker row
     opens). A clone of it comes UNBOUND (`registry.source: "disk"`, labs' on-disk `kmc`
     registry), so bind it with `workflow_update_definition({patch: {registry_source:
     {registry_id, program_id}}})` and re-read. Then create its one run (`workflow_create_run`,
     the window as its period) and point the programme and partner reports' `config.worker_review`
     at `{workflow_id, run_id}` of the clone; a clone keeps the SOURCE's, so worker rows would
     otherwise open Phase 7's workers (connect-fi rebuild, 2026-10-21).
   A linked clone keeps the registry binding and pipelines, and also the SOURCE cascade's
   opportunity list and description. So repoint each:
   `workflow_update_opportunity_ids({workflow_id, opportunity_id: <synthetic opp>, opportunity_ids:
   [<synthetic opp>], expected_version})`, with `expected_version` from `workflow_get`, then
   replace the inherited description (`workflow_update_definition`, the next `expected_version`)
   with one naming the simulated delivery. Without the repoint, `workflow_preview_as_of` caches
   and grades the source cascade's opportunities (connect-fi: 10163..10167). Then
   `workflow_history_eligibility` on the programme report must say eligible; if not, halt with
   `[BLOCKER]`.
6. **Save one run per week** of the programme report (and of the partner report when
   `workflow_history_eligibility` says it is eligible). `workflow_preview_as_of({definition_id,
   opportunity_id, as_of: week1.end})` first: if `cache.partial_cache` or every count is 0, call
   `workflow_ensure_visit_cache` and retry, never build history over a cold cache. Then
   `workflow_rebuild_history({definition_id, opportunity_id, cadence: "weekly", start: week1.start,
   end: weekN.end, limit: N})`; while `done` is false call again with `start = next_start` and the
   same `end`; follow a `job_id` with `job_status`. (The worker review keeps no saved runs; its
   one run was created in Step 5.)
7. **The weeks.** With `supply_chain`, in two passes, because labs reads the visits into the
   ledger on an hourly beat and there is no on-demand trigger over MCP:
   1. **Write every week** (`supply-chain-operate` in `mode: write`, w = 1..N, in order):
      transfers, the planned top-ups, counts.
   2. **Turn on the dispensing rule**, then wait for labs to read the visits
      (`supply-chain-operate` § Dispensing rule). Its stock reads are wrong until it has: a worker
      would show what they were issued and nothing handed over.
   3. **Read every week** (`supply-chain-operate` in `mode: read`, w = 1..N), then its QA. A
      failed week halts the loop.
   Then, for each week, `simulated-weekly-review` and `simulated-weekly-review-eval` unless
   `--no-evals`.
8. **Is it moving?** Read, as of the last delivery day, `supply_chain_stock_flow({program_id,
   item_id})`, `supply_chain_worker_stock({program_id, item_id, opportunity_id})` and each
   store's `supply_chain_supply_point_get`, plus each week-end `worker_stock` from the week files.
   Run `assessSupplyMotion` (`lib/sim-supply-motion.ts`) and write the third Products file. A
   failing verdict is a defect to fix before the summary, not a residual to list: its problems
   name the cause in the order to check it.
9. **Summary** (last Products file): link every weekly review, every report (programme, partner,
   worker) and the labs supply pages a viewer should open, each as
   `https://labs.connect.dimagi.com/supply/<page>/?program_id=<program_id>`: Overview (`overview/`),
   Map (`map/`), Workers (`workers/`), Where it went (`flow/`), the order (`orders/<id>/`) and the
   tender (`procurement/tenders/<id>/`). Then write `products.simulation.weekly_reviews` and
   `reports`, dispatch `simulated-execution-qa`, and capture the pages with
   `output-preview-capture` so the run page shows them.

## MCP Tools Used

- connect-labs: `synthetic_create_labs_only`, `workflow_clone`, `workflow_get`,
  `workflow_update_opportunity_ids`, `workflow_update_definition`, `workflow_history_eligibility`,
  `workflow_preview_as_of`, `workflow_ensure_visit_cache`, `workflow_rebuild_history`,
  `workflow_create_run`, `job_status`, `workflow_history_runs`, `supply_chain_stock_flow`,
  `supply_chain_worker_stock`, `supply_chain_supply_point_get`
- ace-gdrive: `drive_create_file`, `drive_read_file` (the fixture `user_visits.json`), `update_yaml_file` (`merge: deep`)
- Scripts: `scripts/run-labs-synthetic-generate.ts` (calls `synthetic_generate_from_manifest`)
- Skills: `supply-chain-operate`, `simulated-weekly-review`, `output-preview-capture`
- Helpers: `lib/supply-chain-issue-events.ts` (`deriveIssueEvents`), `lib/sim-supply-motion.ts`
  (`planWorkerTopUps`, `assessSupplyMotion`)

## Existing objects

- **The weekly runs are replaceable; the supply-chain records are not.** Re-running Step 5
  replaces only the runs `workflow_rebuild_history` itself made, with new run ids: relink the
  weekly reviews afterwards. Stock movements cannot be deleted (spec § F6); a re-run of a week
  replays by `source.ref`.
- **Never simulate on a program ACE does not own,** and never on the real Phase 4 opportunity.

## Mode Behavior

- **Auto:** Steps 1-3 at S0b, Steps 4-9 at S4.
- **Review:** shows the Step 2 plan and waits before Step 3.

## Dry-Run Behavior

Steps 1-2 and Step 5's eligibility read only. Write the plan; create nothing in labs. (Step 4 needs the generated visits, so a dry run writes no issue-events file.)

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-21 | One synthetic programme holds visits AND supply chain (Steps 1-3 move to Phase 9 S0b, before supply-chain-setup); manifest carries geography and handovers at the PDD's share; workers carry a float (`planWorkerTopUps`); a dispensing rule reads the handovers (write-all, rule, read-all); programme + partner + worker reports; `assessSupplyMotion` gate; summary links the supply pages (owner audit of connect-fi/20261018-1440, ace#3265) | ACE |
| 2026-10-19 | `template_workflow` defaults to `cascade.programme_report` (the worker review is never history-eligible); Step 3 creates the labs-only opportunity first and generates into it, never into the real Phase 4 opportunity; Step 4 repoints the linked clone at the synthetic opportunity (ace#3263) | ACE |
| 2026-10-19 | Step 3a: per-worker, per-week issue events from each commodity's declared `issue_event` drive the week's distribution (`week_activity`), generated from the PDD's eligibility share because the synthetic stream carries no per-form visits (ace#3216) | ACE |
| 2026-10-18 | Initial version (optional-track PR10): backdated N-week simulation on a labs-only copy under the ACE winner, weekly stock and saved report runs, one review per week | ACE |
