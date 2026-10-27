---
name: llo-launch
description: >
  Activate a Connect opportunity for live use once UAT and deep QA have signed off, and notify the
  LLOs of go-live.
disable-model-invocation: false
---

# LLO Launch (Go-Live)

Activate the opportunity and notify LLOs that they are live.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id`, `organization_slug` | the opportunity to activate (`connect_activate_opportunity`) | explicit arg; default: `runs/<run-id>/4-connect/connect-opp-setup.md` / run_state `selected_llo.opportunity_id`; else the program context doc |
| `llo_contacts[]` | who is told it is live | explicit arg; default: run_state `phases.solicitation-management.products.selected_llo` |
| `uat_results` | Step 3 sign-off gate | explicit arg (Drive id); default: `runs/<run-id>/9-execution-manager/llo-uat_results.md` |
| `release_summary` | Step 4 app-verdict freshness (released `build_id` / `version`) | explicit arg; default: `runs/<run-id>/3-commcare/app-release_summary.md`; live: `commcare_list_apps` on the released builds |
| `deep_verdicts` (`ocs`, `app`) | Step 4 deep-QA gate | explicit arg (Drive ids); default: `5-ocs/ocs-chatbot-eval_verdict-deep.yaml`, `6-qa-and-training/app-ux-eval_verdict-deep.yaml` |
| `archetype` | go-live semantics (§ Archetypes) | explicit arg; default: UAT results, then PDD |
| `run_id` | run-bound mode: comms-log, decisions rows | optional; absent = live-program mode |

**Live-program mode keeps every gate.** Without a run the skill still requires
a UAT sign-off and both deep verdicts, passed explicitly, and still checks
each verdict's freshness against the live bot version and released build.
A missing input is a halt, never a skip: activation starts deliveries
counting toward payment. The only way past a missing verdict is the owner's
explicit, recorded waiver in the program context doc's Decisions.

## Process

1. **Read inputs from GDrive:**
   - UAT results: `ACE/<opp-name>/runs/<run-id>/9-execution-manager/llo-uat_results.md` (includes archetype)
   - Deployment summary: `ACE/<opp-name>/runs/<run-id>/3-commcare/app-deploy_summary.md` (atomic-visit)
   - Release summary: `ACE/<opp-name>/runs/<run-id>/3-commcare/app-release_summary.md` — the artifact that owns released `build_id` / `version` / `is_released` per app (Step 4's app-verdict-freshness gate reads this)
   - Opportunity config: `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`
   - Awarded LLO: `phases.solicitation-management.products.selected_llo` in the current run's `run_state.yaml` (populated by Phase 8 `solicitation-review`)
   - PDD: `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md` (fallback archetype source)

2. **Read the `archetype:` field.** Go-live semantics differ per
   archetype — "deliveries count toward payment now" is atomic-visit
   language; an FGD opp's go-live is "Session 1 starts on the scheduled
   date and the first write-up is due 48h after." See `## Archetypes`
   below. Fall back to `atomic-visit` if unspecified.

3. **Verify UAT passed (archetype-aware sign-off criterion):**
   - Check that all LLOs have signed off against their archetype's
     sign-off criterion (apps-work-for-FLWs / could-run-Session-1 /
     Stage-1-readiness) or UAT window has closed without blocking
     issues
   - If blocking issues remain, halt and notify admin group

4. **Verify deep-QA verdicts before activation.** This is the
   highest-stakes gate in the pipeline; activation flips the opp from
   draft to live and deliveries start counting toward payment. Read
   both deep verdicts from `ACE/<opp-name>/runs/<run-id>/`:
   - `5-ocs/ocs-chatbot-eval_verdict-deep.yaml`
   - `6-qa-and-training/app-ux-eval_verdict-deep.yaml`

   For each verdict, require:

   1. **File exists.** If missing, the operator skipped `/ace:qa-deep`
      for that side.
   2. **`verdict: pass`** at the top level. (Canonical schema is
      `verdict:`, not `status:`. Per-item entries use the same key.)
   3. **Verdict is newer than the artifact it grades:**
      - **OCS verdict freshness:** call `ocs_get_chatbot` with the
        verdict's `target` (an `experiment_id` UUID) and confirm the
        chatbot's current `version_number` matches the verdict's
        `artifact_refs.version_number`. If the chatbot has been
        re-published since the verdict was written, the deep eval is
        stale.
      - **App verdict freshness:** read `learn_build_id` and
        `deliver_build_id` from
        `6-qa-and-training/app-ux-eval_verdict-deep.yaml`'s
        `artifact_refs:` block, then read
        `3-commcare/app-release_summary.md`'s `apps:` frontmatter —
        `apps.learn_app.build_id` and `apps.deliver_app.build_id`. The
        verdict's build IDs must match the latest released build IDs.
        If either app has been re-released since the verdict was
        written, the screenshots that grounded the eval are out of
        date.

        **Read the artifact that OWNS release state, not a
        cross-reference to it** (ace#1636, fourth instance of the
        ace#1010 / #1439 / #1567 class). `app-release` declares
        `apps.<app>.{hq_app_id, build_id, version, is_released,
        released_at}` in its `## Products` frontmatter contract
        (ace#1439); that is where released build IDs live. This gate
        previously read a `releases:` block appended into
        `3-commcare/app-deploy_summary.md`, an artifact `app-deploy`
        owns. That append was skipped on 2 of 2 observed runs
        (`bednet-check-2-visit/20260820-0832` and `/20260825-1310`)
        while the release itself was clean, so the gate had nothing to
        compare against — halting with a factually false `[BLOCKER]`,
        or silently skipping the staleness check and letting a stale
        deep app-UX verdict authorize a go-live. The `releases:` block
        has since been retired.

        If `app-release_summary.md` is missing or carries no
        `apps.<app>.build_id`, that IS a `[BLOCKER]` — `app-release`
        contractually owns it, so its absence means the release step
        genuinely did not complete.

   If ANY check fails, halt with `[BLOCKER]` and emit:

   > `[BLOCKER]` Deep QA verdicts missing or stale.
   > Run `/ace:qa-deep <opp>` before activation.
   > Missing or stale: <list of failing checks>

   List one entry per failing check (e.g.
   `5-ocs/ocs-chatbot-eval_verdict-deep.yaml missing`,
   `6-qa-and-training/app-ux-eval_verdict-deep.yaml verdict=fail`, `OCS
   chatbot re-published since verdict written (verdict v3, current v4)`,
   `learn app re-released since verdict written (verdict build abc...,
   current build xyz...)`).

   **Name every NOT REACHED criterion, even on a pass (dimagi-internal/ace#2670).**
   Read `not_reached` from `app-ux-eval_verdict-deep.yaml` (top-level, plus
   each `per_item[].not_reached`) and print one line per criterion with
   `notReachedGateLines` from `lib/criterion-reachability.ts`, e.g.
   `[WARN] journey-deliver-over-cap: fourth_meeting_labelled_not_paid NOT REACHED (reachability: multi-day — …)`.
   These do not block activation by themselves: the verdict's own
   `verdict:` and `journey_completion` cap already account for them. But
   they go in the activation summary and the go-live record, so an
   activation never implies a criterion was observed when it was not.
   A `reachability: multi-day` criterion is reached only by re-running
   `/ace:qa-deep` on successive device-days against the same cases.

5. **Override (operator-only, audited).** If this skill was invoked
   with `--override-deep-qa-gate=<reason>`, skip the gate above and
   proceed to activation. Constraints:
   - The flag must include a non-empty `<reason>` (e.g.
     `--override-deep-qa-gate="emergency-patch-cve-2026-001"`). An
     empty or missing reason is a hard error — do not activate.
   - **`/ace:run` cannot pass this flag.** It is reachable only via
     `/ace:step llo-launch <opp> --override-deep-qa-gate=<reason>`.
     If `--override-deep-qa-gate` arrives through `/ace:run` (e.g.
     embedded in run-mode args), refuse and instruct the operator to
     re-invoke via `/ace:step`.
   - Append an audit entry to
     `ACE/<opp-name>/comms-log/observations.md`:

     ```
     YYYY-MM-DD HH:MM TZ — Deep-QA gate overridden during activation.
     Reason: <reason>. Operator: <ace user from $(git config user.email)
     or env, fallback "unknown">. Verdicts at time of override:
     <ocs-status> / <app-status>.
     ```

     `<ocs-status>` and `<app-status>` are short tags like `missing`,
     `verdict=fail`, `stale (chatbot v3→v4)`, or `pass`. Both must
     appear in the audit line so a reader can reconstruct *what was
     overridden*, not just *that an override happened*.

6. **Confirm the opportunity is active in Connect** (almost always
   already-active by this phase).

   Phase 4 (`connect-opp-setup` Step 6.5) now activates the opp
   synchronously so the ACE test user can be pre-invited and Phase 6
   `app-screenshot-capture` has a real opp on the AVD. By the time
   `llo-launch` runs, the opp is virtually always already-active.

   - **Idempotency check first.** Call `connect_get_opportunity` and
     read `active`. If `active=true` already (the expected case — Phase
     3 activated it, or Connect's managed-opp create flow auto-activated
     as a side effect when `total_budget`/dates were populated up front),
     skip the activate call entirely and log an `[INFO]` line to
     `comms-log/observations.md`:
     `<ISO> llo-launch: opp <id> already active; skipping activate
     call (idempotent path).`
     `connect_activate_opportunity` itself **rejects already-active
     opps** as a validation error — without this pre-check, a clean
     Phase 4 cascades into a Phase 9 failure for no real reason.
     Tracking: jjackson/ace#106 finding 9.
   - **Otherwise activate** (rare — an operator manually deactivated
     between Phase 4 and Phase 9, or Phase 4's activation was rolled
     back). Pass `opportunity_id` from `connect-setup/opportunity.md` and
     `organization_slug` = the run's `products.connect.pm_org_slug`
     (legacy: `organization_slug`) — the activate endpoint is REST and
     authorises an admin of the program org or the holding org, so the
     PM org is always valid. The atom hits
     `POST /api/opportunities/<id>/activate/`, which validates that:
     (a) the opp isn't already active, (b) the opp hasn't ended, and
     (c) at least one PaymentUnit exists. Returns
     `{ id, opportunity_id, name, active: true }` on success.
   - Verify by calling `connect_get_opportunity` and confirming
     `active=true` (whether we activated this run or skipped because
     it was already active).
   - **ACE test-user pre-invite is NOT re-fired here.** As of 0.13.x,
     `connect-opp-setup` (Phase 4 Step 7) invites `${ACE_E2E_PHONE}`
     synchronously once Phase 4 Step 6.5 has activated the opp. The
     real-LLO invite below remains this skill's responsibility.
   - Payment/tracking semantics are archetype-specific — see § Archetypes

7. **Confirm delivery surface readiness (archetype-specific):** see
   `## Archetypes`. For atomic-visit this is app-build verification;
   for focus-group this is Session 1 logistics confirmation; for
   multi-stage this is Stage-1-specific.

8. **Send launch notification to each LLO (archetype-aware body):**
   - From: ace@dimagi-ai.com
   - CC: CRISPR Admin Dimagi Google Group
   - Subject: archetype-specific — see `## Archetypes`
   - Body: archetype-specific content; all three variants include
     activation confirmation, key contacts, support channels, training
     material links

9. **Write launch record** to `ACE/<opp-name>/runs/<run-id>/9-execution-manager/llo-launch_record.md`:
   - Archetype (recorded explicitly so `timeline-monitor` applies the
     right cadence and milestones)
   - Activation timestamp
   - LLO notifications sent
   - Archetype-specific details (app URLs + versions for atomic-visit;
     session schedule + audio-upload path for focus-group; stage
     number + next-stage kickoff window for multi-stage)
   - Any outstanding non-blocking issues

10. **Write `phases.execution-management.products.launch`** to the
    current run's `run_state.yaml` so downstream readers (ace-web's
    per-run summary, `cycle-grade`, the closeout phase) get the
    go-live identity without parsing the launch-record markdown.

    ```yaml
    phases:
      execution-management:
        products:
          launch:
            went_live_at: <ISO timestamp from Step 6 activation>
            archetype: <atomic-visit | longitudinal-visits | focus-group | multi-stage>
            llo_org_slug: <from products.selected_llo.org_slug>
            llo_org_display_name: <from products.selected_llo.org_display_name>
            record_file_id: <Drive fileId of llo-launch_record.md>
    ```

    Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
    `merge: 'deep'` (partial patch of the phase child — `deep` preserves
    the phase's `status`/`steps`; `two-level` would drop them, #572/#587).
    Sole writer of `products.launch`.

<!-- 0.13.116: gate-brief write step + ## Gate Brief section removed.
The Phase 9 "Before llo-launch" Pause Point is unconditional in all
modes (always pauses — the highest-stakes activation in the pipeline).
At pause time, the orchestrator composes the pause-time summary from:
- this skill's eval verdict (`llo-launch-eval`)
- the deep-QA verdicts (`ocs-chatbot-eval_verdict-deep.yaml`,
  `app-ux-eval_verdict-deep.yaml`) including freshness checks vs
  current build IDs
- the UAT results (`llo-uat_results.md`)
- archetype-specific readiness signals from this skill's pre-activation
  checks (per § Archetypes below)
The producer no longer authors a separate gate-brief artifact. -->


## Archetypes

Go-live is the highest-stakes gate. "Deliveries count toward payment
now" is atomic-visit-specific; an FGD opp goes live when Session 1 is
on the calendar with logistics locked. Same activation action in
Connect — different readiness criteria, different notification content,
different monitoring cadence downstream.

### `atomic-visit` (default)

**Delivery-surface readiness check:**
- Learn and Deliver apps are built and published on CCHQ (build status
  `success`)
- Mobile download is available (verify at least one FLW can install the
  updated app)

**Connect activation semantics:** flipping to active means deliveries
start counting toward payment immediately. If there's a scheduled start
date, defer activation until that date; don't pre-activate and risk
stray early-delivery payments.

**Launch email:**
- Subject: `"[Opportunity Name] — You Are Live!"`
- Body leads with: "Your opportunity is active. FLWs can now use the
  apps and deliveries count toward payment."
- Include app URLs (Learn + Deliver) and the opportunity dashboard link

**Launch record `archetype_details:`:** `{apps: [{name, url, version,
build_status}], first_delivery_eligibility_date}`

### `focus-group`

**Delivery-surface readiness check (replaces app-build verification):**
- Session 1 venue confirmed + available on the scheduled date/time
- Recording equipment tested successfully during UAT (not just "we have
  a phone")
- Audio-upload path verified with a real file (from UAT dry-run)
- Participant recruitment at target N for Session 1 — **do not launch
  if recruitment is below target for Session 1**; push the schedule
  rather than running a shorthanded first session
- Consent script practiced and approved during UAT

**Connect activation semantics:** if the opp uses Connect for payment
tracking, flipping to active is when session completion starts being
recorded toward the LLO's per-session rate. If the opp is paid
out-of-band (invoice), activation is ceremonial but still run it so
`timeline-monitor` can key off a canonical activation date.

**Launch email:**
- Subject: `"[Opportunity Name] — Session 1 is on the calendar!"` (not
  "You Are Live" — that phrasing is FLW-deployment coded)
- Body leads with: "Session 1 is confirmed for `<date>` at `<venue>`.
  Facilitator: `<LLO contact>`. Audio upload due within 48 hours of
  session end."
- Include: session schedule (all N sessions), audio-upload path, who
  to contact if a participant cancels, the OCS widget link

**Launch record `archetype_details:`:** `{sessions: [{n, date, venue,
participant_target}], audio_upload_path, write_up_due_hours}`

### `multi-stage`

**Delivery-surface readiness check:** pin to **Stage 1's protocol** and
apply the atomic-visit or focus-group check above accordingly. Later
stages are explicitly OUT OF SCOPE for this launch — they get their
own launch runs at their respective stage boundaries.

**Connect activation semantics:** activate only for Stage 1's delivery
surface. If Connect cannot scope activation by stage, note the
constraint in `launch-record.md § caveats`.

**Launch email:**
- Subject: `"[Opportunity Name] — Stage 1 is live"` (explicit stage
  number; avoids "you are live" implying the whole pipeline is running)
- Body leads with: "Stage 1 (`<stage-1-protocol>`) is active as of
  `<date>`. Stage 2 onboarding will follow separately after the Stage 1
  gate (expected: `<stage-transition-date>`)."
- Include Stage 1 specifics + note that Stage 2 details will come in a
  later email

**Launch record `archetype_details:`:** `{current_stage: 1,
stages_total: N, stage_1_protocol, stage_transition_criteria,
next_stage_kickoff_window}`

**Important:** `llo-launch` may be invoked MULTIPLE times across a
multi-stage opp's lifetime — once per stage transition. Each
invocation re-emits a stage-specific launch record. (0.13.116 removed
the separate gate-brief artifact; the orchestrator composes the
pause-time summary from this skill's verdict files instead.) Prior
launch records stay in
`runs/<run-id>/9-execution-manager/llo-launch_record-stage-N.md` so
history is preserved. (The
`runs/<run-id>/9-execution-manager/llo-launch_record.md` entry tracks
the latest/current stage.)

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`
- Connect (`ace-connect` MCP, 0.10.47+):
  - `connect_activate_opportunity` — REST `POST /api/opportunities/<id>/activate/`
  - `connect_get_opportunity` — verify post-activation (HTML-driven read)
  - `connect_send_flw_invite` — REST `POST /api/opportunities/<id>/invite_users/`
    (no longer used here as of 0.13.x — `connect-opp-setup` Step 7
    handles the ACE test-user invite synchronously at opp create time)
- Email: `email-communicator` skill (sends launch notifications)

## Mode Behavior
- **Auto:** Activate opportunity, send launch notifications, proceed to monitoring phase
- **Review:** Present launch readiness summary for approval before activating (this is a **gate step**)

## Dry-Run Behavior
When `--dry-run` is active:
- Write the intended activation action (opportunity ID, status change) to `comms-log/dry-run-llo-launch.md`
- Write the launch notification emails (recipients, subject, body) to the same file
- Do not activate the opportunity or send emails
- State tracks as `dry-run-success`

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes load-bearing defaults to the per-run
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`. The bar criterion and
schema live in `skills/idea-to-pdd/SKILL.md § Decisions Log Convention`
(canonical authority). The four rows below map 1:1 to `llo-launch-eval`'s
viability axis (PR #145) — when they're present in the log, the rubric
has structured input for those dimensions instead of grading on prose.
The list is a working template; the bar criterion is the sole filter.

### Common load-bearing decisions for Phase 9

| ID | Question | Map to surface |
|---|---|---|
| `llo-capacity-actual` | Did the LLO actually recruit the team they promised? | `llo-launch-eval` `llo_capacity_actual` (eval input, PR #145) |
| `day-one-readiness` | Are FLWs actually ready Day 1 (training complete, devices provisioned, accounts activated)? | `llo-launch-eval` `day_one_readiness` (eval input, PR #145) |
| `downstream-handoff-alignment` | Is the named downstream consumer ready to receive data on the agreed cadence? | `llo-launch-eval` `downstream_handoff_alignment` (eval input, PR #145) |
| `stop-loss-planning` | Is there a documented halt condition (data-quality floor, recruitment failure, etc.)? | `llo-launch-eval` `stop_loss_planning` (eval input, PR #145) |

The orchestrator's Phase Write-Back Verifier (`agents/ace-orchestrator.md`
§ Phase Write-Back Contract § Decisions log clause) enforces the
contract; the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: 9-execution-management` and
`skill: llo-launch`.


## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Add `## Inputs` as parameters (opportunity, LLO contacts, UAT results, release summary, deep verdicts, archetype) with run defaults. Live-program mode keeps every gate: missing inputs halt; only a recorded owner waiver passes a missing verdict. ace#3148. | ACE (build-vs-maintain audit) |
| 2026-08-26 | **Step 4's app-verdict-freshness gate reads the artifact that OWNS release state (ace#1636).** It read `3-commcare/app-deploy_summary.md`'s `releases:` block — a cross-reference `app-release` appended into `app-deploy`'s artifact at its Step 7. That step was skipped on 2 of 2 observed runs (`bednet-check-2-visit/20260820-0832`, `/20260825-1310`) while the release itself was clean and `app-release_summary.md` carried the full declared frontmatter, so this gate had nothing to compare against: it either halted with a factually false `[BLOCKER]` on a current build, or silently skipped the staleness check — which is worse, because it lets a stale deep app-UX verdict authorize a go-live. Now reads `3-commcare/app-release_summary.md`'s `apps.<app>.build_id`, the frontmatter contract `app-release § Products` declares (ace#1439), and a MISSING release summary is a genuine `[BLOCKER]` because `app-release` contractually owns it. `app-release` Step 7 is deleted with the block; `app-release-eval`'s corroborating leg and its every-run `[WARN]` go with it. Fourth instance of the ace#1010/#1439/#1567 class and the first where the reader was a producer skill, not an `-eval`. *Enforced:* `test/skills/deploy-summary-owns-no-release-state.test.ts`. | ACE team |
| 2026-05-05 | **Path-scheme migration on the deep-QA gate.** Step 4 verdict reads, error messages, and gate-brief BLOCKER rows now reference `5-ocs/ocs-chatbot-eval_verdict-deep.yaml` and `6-qa-and-training/app-ux-eval_verdict-deep.yaml` (per the manifest); freshness check pulls build IDs from `3-commcare/app-deploy_summary.md`. Wiring fix — the prior `verdicts/...` paths no longer exist on disk, so the gate would always fail with "verdict missing" against current main. No behavior change beyond paths. | ACE team |
| 2026-05-08 | Add `## Decisions Log` section: 4 anchor rows mapped 1:1 to `llo-launch-eval`'s viability axis (llo-capacity-actual, day-one-readiness, downstream-handoff-alignment, stop-loss-planning) + bar-criterion reference. Pairs with decisions-log PR #4 (Phase 3-10 writes). | ACE team (decisions-log PR #4) |
| 2026-05-10 | Drop the deferred FLW pre-invite path: `connect-opp-setup` (Phase 4 Step 7) now invites `${ACE_E2E_PHONE}` directly after activating the opp in Phase 4 Step 6.5. Step 6 here is reframed from "activate the opp" to "confirm the opp is active" — the idempotent skip-if-active path is now the canonical case; the active-otherwise branch is a fallback for the rare operator-deactivated case. No behavior change for real-LLO invites (still sent in this skill); behavior change for ACE test-user invites (no longer rescued here). Closes the Phase-6-placeholder-screenshots chicken-and-egg. | ACE team |
| 2026-10-05 | **Name NOT REACHED criteria at the gate (dimagi-internal/ace#2670).** Step 4 now prints every `not_reached` criterion from the deep app-UX verdict via `notReachedGateLines` (`lib/criterion-reachability.ts`) into the activation summary. Non-blocking: `app-ux-eval` already caps `journey_completion` at 2 for them. Earned by `spark-facilitator/20261004-1706`, where two `reachability: multi-day` criteria could not be reached in one session and nothing downstream said so. | ACE team |
