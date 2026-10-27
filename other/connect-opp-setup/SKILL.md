---
name: connect-opp-setup
description: >
  Create and configure a Connect opportunity from a PDD: shell, verification flags, payment units,
  test-user invite. Needs an approved PDD, a program, and released apps.
disable-model-invocation: false
---

# Connect Opportunity Setup

**Run workspace:** when the dispatch carries a `run_workspace:` block, its values replace the `.env` ones this skill names — `ACE_HQ_DOMAIN` → `run_workspace.hq_domain`, `${ACE_HQ_API_KEY}` → `run_workspace.hq_api_key` (minted here, per run, for a partner space), the preflight `connect_orgs` → `run_workspace.connect_orgs` — and a partner workspace never falls back to `.env`. Contract: [`skills/_run-workspace.md`](../_run-workspace.md).

Create and fully configure a Connect managed opportunity on the program
owned by the PM org — **the configured PM org (`connect_orgs.pm_org` from
`/ace:doctor --preflight`, passed in by the connect-setup dispatch)** for a
program this run created, or — when the program was reused — the org recorded
in its URL (`opp.yaml.connect.program.url`, `/a/<org>/program/<id>/`), which
stays authoritative. **When `connect_orgs.nm_org` is configured the
opportunity is HELD by that network-manager org** (the real PM→NM flow, Step
3); when it is not, the PM org holds it (legacy self-managed). Never type an
org slug here (`playbook/integrations/connect-api.md § Which Connect orgs ACE
acts in`).

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `pdd` | archetype + Evidence Model (Layer A → verification flags), payment plan, `program_parameters.learn_passing_score` | explicit arg (a Drive file id); default: `1-design/idea-to-pdd.md` |
| `program_id` | program UUID (the opportunity is scoped to it) | explicit arg; default: `4-connect/connect-program-setup.md`; else `opp.yaml.connect.program.id` |
| `pm_org` / `holding_org` | the program's org (every PM-only page) and the org the opportunity is created HELD BY | explicit arg; default: the dispatch's `connect_orgs` block (`lib/connect-orgs.ts` `phase4Orgs()`; see Step 3) |
| `hq_server`, `hq_domain`, `learn_app_id`, `deliver_app_id` | the released apps the opportunity wires to | explicit arg; default: `3-commcare/app-deploy_summary.md` |
| `component_pdds` (componentized only) | the component PDDs, read for their verification rules and payment terms. Step 8a's rule rows need every rule in the PDD set, and on a componentized programme they live in the component PDDs (e.g. a Targeting PDD's duplicates rule), not the overview; Step 6's payment-unit set comes from each component's payment terms (§ Archetypes › Componentized programmes, ace#2163) | explicit arg; default: run_state `…idea-to-design.products.components[].pdd_file_id` + `.program_level[].file_id` |
| `deliver_app_summary` | Step 8a's rule rows: the CCZ-side enforcement a rule relies on when Connect cannot carry it | explicit arg; default: `3-commcare/pdd-to-deliver-app_summary.md` |

Creating an opportunity is a build step: the full Process below runs inside
`/ace:run` Phase 4. Its configuration steps also run on an opportunity that
already exists, with explicit ids and no `run_state.yaml`. See § Operations
on an existing opportunity.

## Phase folder anchor

The connect-setup agent passes a `phaseFolderId` (the `4-connect` folder ID,
anchored to the run folder per `agents/orchestrator-reference.md § Per-Phase
Folder Lifecycle`). **Every `drive_create_file` write in this skill MUST set
`parentFolderId = phaseFolderId`** — `drive_create_file`'s `parentFolderId` is
required and must be a folder ID, never a path string. Writing by path-string
alone makes the artifact land outside `4-connect` and fail
`verify_phase_artifacts(phase='connect')` (jjackson/ace#635).

## Products

- `4-connect/connect-opp-setup.md` (written with `parentFolderId = phaseFolderId`) — opp UUID, verification flags, payment units, ACE test-user invite URL, connect_int_id (ConnectProd integer id, from the create response)
- `decisions.yaml` rows (`phase: 4-connect`, `skill: connect-opp-setup`) — one rule row per PDD verification rule, plus `[ACE]` latitude and `[FIXED]` ambiguity rows (Step 8a, § Decisions Log). The decisions log is the run's review artifact; these rows are the only record of where each rule is enforced
- `run_state.yaml.phases.connect-setup.products.connect` — single atomic block with `program` (copied from `opp.yaml.connect.program` for run self-containment), `opportunity`, `ace_test_user` sub-keys. Read by `synthetic-data-generate` (`opportunity.connect_int_id`), Phase 6 mobile recipes, and other skills within the same run. Per-run only — no other run reads it.

## Operations on an existing opportunity

Three parts of the Process are the one place their mechanics are written
down, and each runs standalone against an opportunity that already exists:
one ACE built, or one it didn't. `connect-opp-modify` is the procedure for a
change to a live opportunity (approval, before-read, refusals, record), and
it points here for these mechanics instead of restating them.

| Operation | Section | Needs | Build-only parts to skip outside a run |
|---|---|---|---|
| **Verification flags** (`form_field_rules`, duration floors, submission window) | Step 5 | `opportunity_id`, `pm_org`, the rules (from a PDD's Layer A or the caller), the released Deliver CCZ for the real question paths | the `self-managed` gap rows (Step 8a); `run_state` writes |
| **Payment units** | Step 6 | `opportunity_id`, `pm_org`, `total_budget`, the payment plan, deliver-unit `server_id`s from `connect_list_deliver_units` | the `phases.connect-setup.status` write on `opportunity_underfunded` (report to the caller instead) |
| **Learn passing score read-back and repair** | Step 4, verify-after-create › `passing_score` | `program_id`, `opportunity_id`, `pm_org`, the intended score, whether a PDD decided it | none; the shared-row caution applies everywhere |

Outside a run, write the outcome where the caller says: the program
context doc's Decisions for a program project, or the run folder when one
is bound. `comms-log/observations.md` and `auto_surfaced` mean the
caller's record.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

1. **Read inputs from GDrive** (paths in `## Inputs` above).

2. **Read the PDD's `archetype:` and `## Evidence Model` section.**
   These are the inputs for steps 4–5. The Evidence Model's Layer A column
   is the spec for verification flags; Layer B/C inform soft-flag metadata.
   **If the PDD has no Evidence Model section, stop and return an error** —
   the PDD is incomplete and `idea-to-pdd` should re-run with the
   stress-test rubric.

3. **Pre-flight: resolve the two orgs, then make the holding org's
   program application ACCEPTED.**

   **3.0 Resolve the orgs (operator decision 2026-09-26).** From the
   connect-setup dispatch take `connect_orgs` (`/ace:doctor --preflight`)
   and compute, exactly as `phase4Orgs()` in `lib/connect-orgs.ts` does:

   | `connect_orgs.nm_org` | mode | `pm_org` (program's org) | `holding_org` (`target_organization_slug`) |
   |---|---|---|---|
   | set, ≠ PM org | **`pm-nm`** (the normal shape) | `connect_orgs.pm_org`, or a reused program's recorded org | **`connect_orgs.nm_org`** |
   | unset | `self-managed` (legacy, other instances) | same | the PM org |

   `pm_org` is the program's org and the org whose URL every **PM-only**
   surface needs; `holding_org` is the org the opportunity is created
   under and lives in forever. **Never type either slug** —
   `playbook/integrations/connect-api.md § Which Connect orgs ACE acts in`.

   > ### Why Phase 4's opportunity is held by the NM org
   >
   > **The program-manager / network-manager model.** A program manager
   > creates the program in the PM org, invites a network manager, and
   > **only once the NM accepts can the PM create an opportunity held by
   > that NM** — Connect enforces the gate itself (live on
   > `turmeric-market-study/20260914-1742`): `POST
   > /api/programs/<id>/opportunities/` rejects with `Organization must have
   > an accepted application for this program`.
   >
   > Until 2026-09-26 Phase 4 always created a **self-managed** opportunity
   > (held by the PM org). That shape can never carry verification rules:
   > Connect's verification-rules page is PM-only and serves only when the
   > requesting org is NOT the holding org (`is_opportunity_pm`,
   > `commcare_connect/program/utils.py`) — so every self-managed run
   > silently dropped its PDD's Layer A payability rules (ace#2419,
   > observed `spark-facilitator/20260925-1536`). With an ACE-controlled NM
   > org configured, Phase 4 now runs the **real** PM→NM flow on every run:
   > the NM org holds the opportunity, and the PM org — a different org —
   > sets its rules. Proved live 2026-09-26 on probe opportunity
   > `7bfcb845-015c-416a-a200-9795c68dfc55` (matrix in
   > `playbook/integrations/connect-api.md § PM→NM org-URL matrix`).
   >
   > **This is still ACE's build/QA opportunity, not the partner LLO's.**
   > The NM org here is ACE's own; the awarded partner's opportunity is
   > created in Phase 9 by `llo-onboarding`, after the partner accepts, on
   > freshly-copied `cc_app_id`s (ace#573). **Two opportunities remains the
   > model.**
   >
   > **There is no repair path if the holding org is wrong**:
   > `target_organization_slug` is create-time only and
   > `connect_update_opportunity` carries no org field. The Playwright
   > create fallback therefore THROWS `cross_org_create_unsupported` rather
   > than creating under the PM org (it used to warn and do exactly that).

   **3a. Invite + accept the holding org (unconditional; the conflict is
   the skip).** In BOTH modes the holding org needs an ACCEPTED
   `ProgramApplication` for this program — in `self-managed` mode the
   holding org is the PM org itself, which still needs one (omitting
   `target_organization_slug` does not waive it: the REST backend sends
   `organization_slug` as the holding org — dimagi-internal/ace#1251).

   1. **Any other `target_organization_slug` → HALT.** Phase 4 never
      creates an opportunity for a *partner* LLO (Phase 8/9 have not run,
      so no partner has accepted). If a caller passes a slug that is not
      `holding_org` above, halt:

      > FATAL: `target_organization_slug` names `<slug>`, which is not this
      > instance's configured holding org (`<holding_org>`). Phase 4 builds
      > ACE's own build/QA opportunity; the partner's opportunity is created
      > in Phase 9 by `llo-onboarding` after their invite is accepted. An
      > opportunity created under the wrong org can never be reassigned.

   2. Run the round-trip **unconditionally** — attempt the transition and
      treat the conflict as the skip (CLAUDE.md § Conventions). Do NOT try
      to read the application state first. (`connect_list_invites` now
      reads the PM page's real rows — org display name + status, integer
      ids, no UUID — since #3017; it is a status read, not the trigger.)

      ```
      mcp__plugin_ace_ace-connect__connect_send_llo_invite({
        organization_slug: <pm_org>,           // the program's org
        program_id,
        organization: <holding_org>,           // nm_org in pm-nm mode; pm_org when self-managed
      })
      // → { program_application_id, status: 'invited' }  — CAPTURE the id NOW
      mcp__plugin_ace_ace-connect__connect_accept_program_application({
        organization_slug: <pm_org>,
        program_id,                            // REQUIRED — the accept is program-scoped
        application_id: <program_application_id from the invite>,
      })
      // → { status: 'accepted' }
      ```

      **Capture `program_application_id` from the invite POST** and write
      it to `products.connect.program_application_id` (Step 10). It is not
      recoverable later: `connect_list_invites` shows only the integer
      row id, never the UUID.

      The accept is Connect's automation shortcut: its REST view
      (`ProgramApplicationAcceptView`) authorises the caller as an admin of
      the **program's** org, so it is called with the PM org and the NM
      admin identity plays no part. Observed live 2026-09-26: invite
      `68b0a689-7326-4c13-a21e-ef492db3a738` → `invited`, accept →
      `accepted`, then the NM-held create succeeded.

      **The accept is gated (ace#2954, ace#3009, operator rule 2026-10-16)
      and takes no extra argument.** It allows exactly two cases:
      (a) the application is listed on the OWN programme page
      (`/a/<org>/program/`) of an org ACE controls (`ACE_CONNECT_PM_ORG` /
      `ACE_CONNECT_NM_ORG` / `ACE_CONNECT_CONTROLLED_ORGS`, environment
      only) — internal testing: ACE's own NM org never "applies", so the PM
      accepts it from `INVITED`; or (b) the partner has already accepted
      their invitation, i.e. a row on the PM programme page reads `APPLIED`
      — the PM's accept is then the legitimate final step. It refuses a
      non-controlled org still at `INVITED` (`PartnerHasNotAppliedError` —
      the tekzal/20261013-2314 incident) and fails closed when neither can
      be read (`ApplicationAcceptUnverifiableError`). In Phase 4 only (a)
      applies. A refusal here is unexpected — it usually means the PM org's
      own application (`self-managed`; the PM view lists no application
      ids). Do not work around it; record it and halt.

      **Do not paraphrase these signatures — the parameter names above are
      the atoms' real ones, per `docs/atom-schemas.md`.** Every name in this
      block was wrong until ace#1800 (`connect_send_llo_invite` takes
      `organization`, not `target_organization_slug`;
      `connect_accept_program_application` takes `organization_slug` /
      `program_id` / `application_id`). The wrong block was invisible
      because it only executes on the FIRST Phase 4 run of a program —
      every later run short-circuits on the conflict below.

   3. **The skip response carries no id — do not go looking for one (ace#1800).** On a
      reused program the invite rejects with `{error: 'validation_error',
      fields: {organization: ['Organization already has an application for
      this program.']}}` and names no `application_id` (observed on
      `hh-poverty-targeting/20260828-0702`, ace#1800). That is fine: the
      create derives the application server-side from
      `(target_organization_slug, program_id)`. Record
      `program_application_id: null` with the reason. This error does NOT
      distinguish `INVITED`/`APPLIED` from `ACCEPTED` — if the existing
      application is merely pending, `connect_create_opportunity` fails
      loudly with `Organization must have an accepted application for this
      program.` Let that be the check; do not infer acceptance from the skip.

   4. Log the round-trip result to `comms-log/observations.md` so the
      operator can audit the state mutation. This is the only Phase 4
      step that mutates Connect state outside the opp itself.

4. **Create the opportunity** via `connect_create_opportunity`.

   **⚠️ Single-active-opp check (per-program, per-application) — an
   OBSERVATION, not a rule Connect is known to enforce.**
   ACE has one recorded instance of a prior opp deactivating when a new
   managed opp was created on the same program: the leep-paint-collection
   run, 2026-05-06, where `LEEP Paint Surveillance — India v1` flipped
   from active to inactive without warning as this skill recreated the opp
   (jjackson/ace#106 finding 11). It also has a direct counter-observation:
   on `bednet-check-2-visit/20260908-1544` (program
   `efb8af66-fbfd-488f-bf99-66f864cea68b`, org `ai-demo-space`) **ten**
   opportunities on one program were concurrently `active: true`, and an
   immediate post-create re-read of the very opp that run's WARN named
   (`5fdee3b8-e859-4aa7-a4be-8ad6f727917a`) came back `active: true` with
   `dashboard_read: "ok"` — a real read of the edit-form toggle, and no
   deactivation (ace#2290). So neither half of the old wording holds up:
   do not write "Connect enforces one active managed opp per accepted
   `ProgramApplication`" or "creating this opp will deactivate `<x>`" into
   the WARN, the phase summary, or `connect-opp-setup.md`. Neither is
   established.

   **Leading hypothesis for the divergence — a hypothesis, not a finding.**
   The 2026-05-06 side effect was attributed to the accept-application step
   in 3a. On a self-managed org (PM org == target org) that step now
   short-circuits on `Organization already has an application for this
   program` and never reaches the accept call at all, which would explain
   the side effect not firing today. That is checkable in upstream source,
   not from here: run `skills/upstream-regression-triage` against
   `dimagi/commcare-connect` before promoting either half of this back to
   fact (ace#2290).

   **Keep the check regardless.** It is one list call, and one real
   deactivation was observed once — what changed is the claim it makes,
   not whether it runs. Before calling `create_opportunity`, list opps for
   this program and report which are active:

   ```
   mcp__plugin_ace_ace-connect__connect_list_opportunities({
     organization_slug,
     hydrate: true,            // REQUIRED — see below
   })
   ```

   **`hydrate: true` is not optional, and do NOT pass `program_id`
   (ace#1022).** The opportunity LIST page carries only id / name / short
   description. Until #1022 this atom hardcoded `active: false` on every
   row, so this WARN could **never fire** — the silent-deactivation
   surprise it exists to catch was undetectable by it. It also accepted
   `program_id` and silently ignored it, returning the whole org (live: 20
   opportunities from four other programs for a program that had zero).
   Now `program_id` is refused loudly, and `active` is **absent** unless
   you hydrate — a missing value you must handle, rather than a fabricated
   one you cannot tell from a real one. `hydrate: true` fetches each row
   through `get_opportunity`, which parses the real toggle off the edit
   form. Filter to this program yourself from the hydrated rows.

   Count the hydrated rows in this program with `active=true`. **N>1 is
   the normal case on a mature program** — every `/ace:run` publishes a
   fresh opp and per-run accumulation is by design (`CLAUDE.md`), so
   "close prior opps first" is not the remedy and is no longer asked for.
   If the count is non-zero, surface ONE `[WARN]` line in `auto_surfaced`
   carrying the count and the ids:
   `[WARN] <N> opportunit(y|ies) already active on this program before
   creating "<new-name>": "<old-name>" (id=<old-uuid>), … . A new
   managed opp MAY deactivate them — unverified, one observation each way
   (ace#2290). Proceeding.`

   Do not assert in that WARN — or anywhere downstream — that a named opp
   will be, or has been, deactivated. If a prior opp matters to this run,
   re-read it with `connect_get_opportunity` after the create and record
   the `active` value you actually observed.

   The auto-mode default is to proceed, unchanged (matches current Phase 9
   pause-point auto-approval). Review-mode pauses for explicit operator
   confirmation.

   **4.0 Resume check — finish THIS run's opportunity, never mint a second
   (ace#2083).** The create below makes an opportunity with no payment units;
   Connect's `is_setup_complete` stays false until Step 6 adds one, and every
   read then reports `dashboard_read: 'setup_incomplete'`. A dispatch that dies
   between here and Step 6 leaves exactly that, and a re-dispatch that creates
   again strands it for good: Connect has no opportunity-delete route, and its
   only purge (`delete_stale_opportunities`) takes visit-free opportunities at
   SIX MONTHS. Meanwhile each one costs a full `EXPECTED_OPP_BUDGET` in every
   program-ceiling sum on the org (11 of 71 rows on the shared PM org, 2026-09-06 —
   ACE's own abandoned Phase 4 runs). So, before creating:

   1. Read `phases.connect-setup.products.connect.opportunity` from this
      run's `run_state.yaml` (null on a first dispatch).
   2. `connect_list_opportunities({organization_slug: <pm_org>, name:
      <run_id>, hydrate: true})` — the PM org lists NM-held opportunities too;
      `name` is a substring match, so the run id finds every row of this run.
   3. Decide with `planOpportunityCreate({runId, expectedName, recorded,
      listing, rows})` (`lib/connect-opp-resume.ts`, pinned by
      `test/lib/connect-opp-resume.test.ts`), where `expectedName` is the
      exact `"<run_id> · <PDD display name>"` you would create:
      - `create` → proceed with the create below.
      - `adopt` → do NOT create. Use `opportunity_id`, record it now (the
        write below), take `deliver_units[].server_id` from
        `connect_list_deliver_units`, and continue at Step 5 on that
        opportunity. `setup_incomplete: true` means Steps 5, 6 and 6.5 all
        still have to run on it; `false` means setup is done — call
        `connect_list_payment_units` before Step 6 and create only the units
        not already listed by name. Log the adoption and its `reason` to
        `comms-log/observations.md` and the step log.
      - `halt` → stop Phase 4 with a `[BLOCKER]` carrying `code`,
        `opportunity_ids` and `reason`. Never create on a halt: every halt is
        a case where creating could add another permanent orphan.

   **The atom enforces the same rule.** `connect_create_opportunity` refuses an
   `is_test` create whose exact name already exists (`OPPORTUNITY_ALREADY_EXISTS`,
   naming the ids) or whose listing came back incomplete
   (`OPPORTUNITY_EXISTENCE_UNKNOWN`). Treat either as this step's `adopt` /
   `halt`; `allow_existing_name: true` is for a replacement the operator
   explicitly approved, never a retry.

   **Record the id the moment the create returns (ace#2412).** Right after a
   successful create (or an `adopt`), before Step 5, write
   `phases.connect-setup.products.connect.opportunity: {id, name, url}` with
   `update_yaml_file({merge: 'deep'})` on the run's `run_state.yaml` (no
   `validateAs` — Step 10 writes the full block and validates it). That one
   write is what lets the next dispatch's 4.0 take the `recorded` branch.

   **Endpoint:** the new endpoint is
   `POST /api/programs/<program_id>/opportunities/` and takes the
   full opp config in one shot — including dates, total_budget, and
   structured `learn_app` / `deliver_app` payloads. The server resolves
   HQ creds, registers HQApiKey records as needed, fetches app names
   from CommCareHQ synchronously, and syncs learn modules + deliver
   units in the same transaction. Args:

   - `organization_slug`: `pm_org` from Step 3.0 — the org that owns the
     program (`connect_orgs.pm_org`, or the reused program's recorded org)
   - `program_id`: from step 1 (program.md)
   - `name`: **construct as `"<run_id> · <PDD display name>"`** — the
     `run_id` from run_state (format `YYYYMMDD-HHMM`) as a FRONT prefix,
     separated by ` · ` (space-middot-space, U+00B7), then the PDD
     display name. Example: `"20260601-0739 · Malaria RDT Performance
     Sampling"`. **The run-id MUST lead.** Why front-prefix: the ACE
     test user accumulates dozens of near-identical opp invites across
     dogfood runs, and the run-id is the only token that disambiguates
     THIS run's opp from all the others. As a front prefix it lands on
     the tile's FIRST line — short and never clipped by the tile's
     name-wrap — so Phase 6's mobile claim/resume recipes can anchor
     their tile match on it (`text: ".*${OPP_RUN_ID}.*"`) and find this
     run's opp deterministically. The old run-id-SUFFIX form
     (`"<display> — <slug> (run <run-id>)"`) put the discriminator at
     the END of a long name that wraps to 2-3 lines on the tile — the
     most-clipped position — which is exactly the wrong place for the
     matcher. (Applies to ACE-driven dogfood runs — same `is_test: true`
     framing as below.) **Code-enforced** since jjackson/ace#755: the
     `connect_create_opportunity` atom rejects an `is_test: true` name
     without the run-id front prefix (`INVALID_OPP_NAME_PREFIX`,
     `mcp/connect/opportunity-name.ts`) before any network call.
   - `short_description`: **≤50 chars** (server-enforced; the Connect
     opportunity edit form rejects longer values with a generic
     `Ensure this field has no more than 50 characters` error).
     Truncate the PDD's intervention summary to a one-line headline
     and stash the long-form intent in `description`. Mobile-app-facing.
   - `description`: **default to ≤250 chars** — a single-paragraph
     headline. The Connect server has an undocumented length threshold
     where HTTP 500s start firing intermittently around ~700 chars;
     trimming to ~250 cleared the path on leep-paint-collection (see
     #106 finding 7). Stash the full PDD intervention prose in the
     opp's Drive summary doc and link to it from the headline. When
     the server-side length cap is widened safely, drop this guidance.

     **`description` is WORKER-VISIBLE — it renders in full on the job
     card, the first screen an FLW sees.** It is not a bookkeeping field
     and it is not internal. Write it for the worker deciding whether to
     accept the job. Never put run ids, phase names, capture bookkeeping
     or any other build-time scaffolding in it.

     Live on turmeric-market-study/20260828-1108: a capture opportunity's
     `description` ended "…This opportunity is a capture vehicle for
     Phase 6 walkthrough screenshots on run 20260828-1108." It rendered
     legibly on the job card, the job card was captured as a walkthrough
     screenshot, and that frame was then cited by BOTH the FLW training
     guide and the training deck — internal scaffolding one review away
     from reaching trainees. **A screenshot cannot be retro-fixed:**
     correcting the field does not correct frames that already show it,
     and re-shooting the job card needs an unclaimed opportunity. Get it
     right at create time.
   - `target_organization_slug`: **`holding_org` from Step 3.0** — the
     configured NM org in `pm-nm` mode (its application ACCEPTED in 3a).
     Pass it explicitly in both modes. Read the create response's
     `organization_slug` back and assert it equals `holding_org`; a
     mismatch is a `[BLOCKER]` (the holding org cannot be changed later).
   - `start_date` / `end_date`: opportunity dates (YYYY-MM-DD; must fit
     inside the program window)
   - `total_budget`: an integer in the opp currency's whole unit (Connect
     stores `total_budget`, `amount`, `org_amount`, `max_total` as integers
     in the SAME unit — `PositiveBigIntegerField` / `PositiveIntegerField` in
     `commcare_connect/opportunity/models.py`; no cents). Two bounds, both
     mandatory:
     - **Upper bound (ceiling):** must fit inside
       `program.budget − Σ(other managed opps)`.
     - **Lower bound (floor — funds ≥1 FLW):** must be
       `≥ min_budget_for_one_user × FUND_USERS`, where
       `min_budget_for_one_user = Σ over the opp's planned payment units of
       (max_total × (amount + org_amount))` and `FUND_USERS` is a small smoke
       headroom (**default 3**) so a few claims are possible. This mirrors
       Connect's managed-opp capacity formula
       `number_of_users = total_budget / Σ(max_total × (amount + org_amount))`
       (`Opportunity.number_of_users`, models.py): a `total_budget` below
       `min_budget_for_one_user` yields `number_of_users < 1`, which
       under-allocates `create_claim_limits` and leaves the FLW unable to
       claim a full visit allotment.
     - ACE computes `min_budget_for_one_user` from the **planned** payment
       units — known from the PDD's deliver design BEFORE create — and sizes
       `total_budget` to `≥ min_budget_for_one_user × FUND_USERS` clamped by
       the ceiling. The PDD's program budget is a HINT/ceiling, NOT the opp
       budget: if the PDD budget is too small to fund even one user at the
       planned payment units, **the opp-budget floor WINS** and the program
       budget must be raised to accommodate (see `connect-program-setup`
       headroom, jjackson/ace#588). Archetype-agnostic — applies to every opp.
   - `is_test`: **set explicitly to `true`** for every ACE-driven run. The
     server defaults to `true` if omitted, but sending it explicitly makes
     the value visible in the create-response and auditable in the
     verify-after-create check below. ACE is in dogfood mode — every opp
     it stands up is for engineering exercise, NOT a production rollout —
     so the test flag must be on. The eventual production-grade opp (post-
     dogfood) will flip this to `false`; that flip will be a deliberate
     operator decision, not a defaulted-off slip.
   - `learn_app`: `{ hq_server_url, api_key, cc_domain, cc_app_id, description, passing_score }`
     - `hq_server_url`: full URL (e.g. `https://www.commcarehq.org`)
     - `api_key`: the **raw 40-char HQ API key** for the project space
       (read from `~/.claude/plugins/data/ace-ace/.env` → `ACE_HQ_API_KEY`).
       Server creates the `HQApiKey` record if it doesn't exist.
       **Partner workspace** (`run_workspace.is_default: false`): instead
       mint a key restricted to the partner's space first —
       `commcare_create_api_key(domain: <run_workspace.hq_domain>, name:
       ace-run-<hq_domain>-<run-id>)` — and pass the returned
       `hq-key:<name>` reference here (and as `api_key` to
       `connect_preflight_learn_app_user`). Never `ACE_HQ_API_KEY` on a
       partner's opportunity (`skills/_run-workspace.md`).
     - `cc_domain`: HQ project space slug
     - `cc_app_id`: bare 32-char HQ app id
     - `description`: required (Connect form marks it `*`); pulled from PDD
       § Training Plan
     - `passing_score`: 0–100. **Read it from
       `run_state.yaml.phases.idea-to-design.products.pdd.program_parameters.learn_passing_score`
       — that is the typed handoff and it is authoritative.** Fall back to the
       PDD's § Program Parameters table, then to 80 ONLY when the PDD decides
       nothing; when you fall back, say so explicitly in the step log and in
       `comms-log/observations.md`, because a defaulted gate is a program
       decision ACE made on the operator's behalf.

       **This value cannot be set anywhere else.** Nova's `connect.assessment`
       exposes only `{id, user_score}` — there is no `passing_score` slot — so
       this call is the ONLY place the Learn gate is established. It is a
       required field on the atom, so it cannot be omitted, only set wrong.
       Getting it wrong is silent: the app still builds, the worker still sees
       a result screen, and only the gate is different from the one the program
       specified. On `bednet-check-2-visit/20260813-2313` the PDD specified a
       source-stated 6-of-6 gate (100); with percentage scoring over six items
       5-of-6 is 83.3, so defaulting to 80 would have passed a worker who got
       one wrong, against an explicit program decision that they must not.
   - `deliver_app`: `{ hq_server_url, api_key, cc_domain, cc_app_id }`
     — `cc_app_id` MUST differ from `learn_app.cc_app_id` (server-validated)
   - `auto_activate`: **pass `false` explicitly** (it is also the atom
     default since #584). This skill's ordering is create (Step 4) →
     create payment unit(s) (Step 6) → activate (Step 6.5). Activation
     requires at least one PaymentUnit; `auto_activate: true` would try to
     activate at create time before any PU exists, which Connect rejects
     ("At least one payment unit must exist before activating") AND rolls
     back the entire create — leaving no `opportunity_id` and an orphan
     inactive opp. Create the draft here, then activate in Step 6.5.

   The response includes `opportunity_id` (UUID), the resolved app names,
   and arrays of `learn_modules` / `deliver_units` already synced from HQ.
   Capture `opportunity_id` for downstream steps. **Don't** call
   `connect_list_deliver_units` after this — the create response already
   carries the full list under `deliver_app.deliver_units`.

   **A 5xx or timeout from the create is an AMBIGUOUS outcome — never retry
   it blind (ace#2580).** The endpoint fetches app names from HQ and syncs
   learn modules + deliver units synchronously, so a slow HQ can push it past
   the gateway while the transaction still commits. Observed on
   `spark-facilitator/20261001-2208`: `504 Gateway Time-out`, an immediate
   list showed no new row, and ~2–3 minutes later the opportunity was there.
   A retry would have minted a second opportunity on the program. So: wait,
   then `connect_list_opportunities({organization_slug, name: <the run id>})`
   (`name` is a case-insensitive SUBSTRING match, so the run-id prefix alone
   is enough and is unique; it was strict equality until ace#2891, which made
   a run-id lookup answer `[]` with `listing.complete: true` — the one answer
   that licenses exactly the retry this paragraph exists to prevent) — repeat
   over a bounded window of ~5 minutes. **Corroborate a `[]` against the
   UNFILTERED walk's `listing.total_count` before believing it.** If the row
   appears, adopt it: take `deliver_units[].server_id` from
   `connect_list_deliver_units` and `connect_int_id` from the Step 6.5
   `/activate/` response (it returns `id`, the integer), and say in the
   step log that the create response was lost. Re-create only once the
   bounded wait has confirmed the opportunity is absent — and if the row
   lands after that, the atom's `OPPORTUNITY_ALREADY_EXISTS` refusal names it:
   adopt it per Step 4.0.

   **App-wire fields are write-once at create.** Connect's `/edit` form
   does NOT expose `learn_app` / `deliver_app` — they're only set at create.
   `connect_update_opportunity` only covers `name` / `short_description` /
   `description` / `end_date` / `is_test`. **If Phase 3 re-uploads an app
   after this skill ran, the existing opp is wired to a stale (now-abandoned)
   HQ id** — the recovery is **manual deletion in the Connect web UI**
   (Connect's `delete_opportunity()` helper exists in
   `commcare_connect/opportunity/deletion.py` but no Django view exposes
   it yet; see `skills/sweep-connect/SKILL.md § Implementation notes`)
   followed by `connect_create_opportunity` against the canonical HQ ids
   (if the stale one could not be deleted, the create needs
   `allow_existing_name: true` — the operator's call, since the stale one stays
   on the org until Connect's six-month purge), then update the current run's
   `phases.solicitation-management.products.solicitation.connect_opportunity_id`
   to the new UUID. **This recovery is low-cost.** A labs solicitation
   already published for this opp is unaffected: solicitations are
   scoped to the labs `program_id`, not to any specific Connect
   opportunity UUID (`connect_opportunity_id` is ACE-side bookkeeping
   recording ACE's intended target, not a labs-side foreign key — see
   `skills/solicitation-create/SKILL.md`). The public solicitation
   URL, deadline, and pending applications all continue uninterrupted.
   CCC-301 will eventually retire this dance by exposing
   `update_opportunity({learn_app, deliver_app})`.

   **Verify-after-create (mandatory).** Immediately after the create
   response returns, call `connect_get_opportunity({organization_slug,
   opportunity_id})` and compare what was sent against what the server
   stored.

   **⚠️ Only some of those fields are READABLE at this point
   (dimagi-internal/ace#1647).** A never-activated opportunity renders
   only the edit-form half of `connect_get_opportunity`'s hydration; the
   dashboard half returns nothing until the opp has been through
   `/activate/` (Step 6.5). A Write→Read→Compare that cannot read is
   worse than no check — it reports confidence it does not have — so the
   list below is split, and the unreadable half is **deferred to Step
   6.6**, not asserted here.

   *Verified live on `bednet-check-2-visit/20260825-1310` Phase 4: the
   same opp read twice through the same atom, ~2 min apart either side of
   activation. Pre-activation the payload carried `name`,
   `short_description`, `description`, `end_date`, `is_test`, `active`,
   `currency`, `country` and nothing else; post-activation it also
   carried `total_budget`, `start_date`, `program_name`, `learn_app` and
   `deliver_app`. Upstream half tracked as #1637.*

   **Verify HERE (readable pre-activation):**
   - `name`, `short_description`, `description` — string match
   - `end_date` — `YYYY-MM-DD` match (the `turmeric-20260503` run hit a
     write-vs-read drift where `end_date=2026-08-09` was accepted by
     create but `connect_get_opportunity` returned `""`; this read-back
     is the canary)
   - `is_test` — boolean match

   **DEFER to Step 6.6 (unreadable pre-activation — do NOT assert here):**
   - `start_date` — `YYYY-MM-DD` match
   - `total_budget` — numeric match
   - `learn_app.cc_app_id` and `deliver_app.cc_app_id` — bare 32-char match

   **An absent field is `unreadable-at-this-point`, never a match.** If
   any DEFERRED field unexpectedly IS present in this read, compare it —
   a present value is real. But never record a comparison you did not
   perform: write `unreadable-at-this-point (deferred to Step 6.6)`
   against each one you skipped, in `comms-log/observations.md` and in
   whatever verification summary this step reports. Silently counting an
   absent field as a pass is the exact defect #1647 fixed; the sibling
   class is ace#1449 below, where a field the read surface does not
   render came back `undefined` and read as "unreadable" rather than
   "mismatch".

   Also check:
   - `passing_score` *(also runs on an existing opportunity: § Operations
     on an existing opportunity)* — numeric match. **Read it with
     `connect_get_learn_passing_score({organization_slug, program_id,
     opportunity_id})`, NOT from `connect_get_opportunity`** (ace#1449).
     `connect_get_opportunity` hydrates from `/a/<org>/opportunity/<id>/edit`
     plus the read-only detail page, and `learn_app_passing_score` is rendered
     on **neither** — it lives only on the program-scoped init-edit form. So
     this comparison silently had nothing to compare against: the field came
     back `undefined`, which reads as "unreadable", not as "mismatch". There is
     no REST alternative — commcare-connect's automation API (PR #1135) ships
     no opportunity GET endpoint at all.

     Two return values that are NOT the same thing:
     - `passing_score: null` — the input rendered EMPTY, i.e. the gate is
       **unset**. Do not coerce that to `0`; `0` means "every worker passes",
       the most permissive possible gate, and is the opposite of unconfigured.
     - the atom THROWS — the field is absent from the form altogether, meaning
       the form shape changed. Treat as `[BLOCKER]`; do not substitute a
       default, or you will report a gate value ACE invented as one Connect
       stored.

     **Severity depends on whether the PDD decided the value**, because the two
     cases mean different things:
     - The PDD stated a gate (`program_parameters.learn_passing_score` is
       set) and the read-back differs → **`[BLOCKER]`**. The gate the
       program specified is not the gate that is live, this call is the
       only place it can be set, and nothing downstream re-checks it. Do
       not proceed; log both values to `comms-log/observations.md`.
     - ACE defaulted the value (the PDD decided nothing) and the server
       returned its own → `[INFO]`; document the diff and proceed.

     The pre-2026-08-14 rule made this `[INFO]` unconditionally, on the
     reasoning that "Connect's server has its own default". That is true
     and irrelevant when the PDD stated a gate: a server default silently
     overriding an explicit program decision is precisely the drift this
     read-back exists to catch.

     **On a mismatch, name ROW REUSE as the first suspect — not server
     drift** (dimagi-internal/ace#1350). Connect keys `CommCareApp` on
     `(cc_app_id, cc_domain, organization, hq_server)`, **not** on the
     opportunity, and the create path calls
     `_build_commcare_app(update_existing=False)`. So when a `CommCareApp`
     row already exists for this `cc_app_id`, `get_or_create`'s `defaults`
     are IGNORED and the `passing_score` you just posted is **silently
     discarded** — the opportunity inherits whatever an earlier one set.
     The POST looks perfectly healthy; only this read-back sees it.

     That is the likeliest cause of "posted 100, read back 80", and it
     looks nothing like a server default, so say so in the `[BLOCKER]`:

     > `passing_score` mismatch on `<opp>`: sent `<X>`, server returned
     > `<Y>`. Most likely cause is CommCareApp ROW REUSE — Connect keys
     > that row on `(cc_app_id, cc_domain, organization, hq_server)`, not
     > on the opportunity, and the create path ignores `defaults` for an
     > existing row. Repair with `connect_set_learn_passing_score` — and
     > note it will move the gate for EVERY opportunity in this org wired
     > to the same HQ Learn app, so check `previous_passing_score` in its
     > response before accepting the change.

     ACE normally avoids this because every `/ace:run` builds a fresh Nova
     Learn app, so every create posts a new `cc_app_id` and always takes
     the `created=True` branch. That invariant breaks on a forked run, a
     hand-wired opp, or a Phase 4 re-mint against the same release —
     exactly the cases where a mid-run operator is least expecting it.

     **Do not eyeball the severity — call
     `classifyPassingScoreReadback` from `lib/passing-score-readback.ts`**
     with `{posted, readBack, pddDecided}`. It also names the CAUSE, which
     the `[BLOCKER]` alone did not, and returns the repair (ace#1350):

     > A mismatch here is almost certainly **not** server drift. Connect's
     > create path runs
     > `CommCareApp.objects.get_or_create(cc_app_id, cc_domain, organization,
     > hq_server, defaults=...)` with `update_existing=False`, and the row is
     > keyed on the **app**, not the opportunity. If a row for this
     > `cc_app_id` already exists in this org, `get_or_create` ignores
     > `defaults` and **the posted `passing_score` is silently discarded** —
     > the opportunity inherits whatever an earlier one set.

     On the `blocker` verdict, apply the returned repair —
     `connect_set_learn_passing_score(posted)` — then re-read. **Surface its
     `caution` in `auto_surfaced`:** the score lives on the shared
     `CommCareApp` row, so the repair moves the gate for **every**
     opportunity in the org wired to this HQ Learn app. Record the
     `previous_passing_score` the atom returns.

     ACE has escaped this only by an unstated invariant — every `/ace:run`
     builds a fresh Nova Learn app, so every create posts a new `cc_app_id`
     and takes the `created=True` branch. It breaks the moment anything
     reuses an HQ Learn app: a forked run, a hand-wired opp, a Phase 4
     re-mint against the same release, or an opp created against a prior
     run's app to save a build.

   **Action on mismatch:**
   - `end_date` (or any DEFERRED field that did read, and disagreed) →
     `[BLOCKER]` in `auto_surfaced`; log the diff to
     `comms-log/observations.md` with both values; do NOT proceed to
     Step 5. The opp is in an unknown state — operator must inspect via
     the Connect web UI before continuing. (The deferred fields get the
     same `[BLOCKER]` treatment at Step 6.6, where they are readable.)
   - Description / is_test disagreement → `[INFO]` log to observations;
     proceed.
   - `passing_score` disagreement → severity per the rule above:
     `[BLOCKER]` when the PDD stated the gate, `[INFO]` when ACE defaulted.

   This step costs one extra HTML-driven `connect_get_opportunity` call
   (~2s) and catches a class of bugs the producing skill's response
   alone cannot — server-side serialization gaps, schema drift, or
   silent overrides. The 0.11.7 ocs-chatbot-qa rework adopted the same
   "verify after every external write" discipline; this is the Connect
   side of that rule (see `agents/ace-orchestrator.md § External
   Mutations — Verify After Create`).

5. **Configure verification flags** via `connect_set_verification_flags`
   *(also runs on an existing opportunity: § Operations on an existing opportunity)*,
   mapping the PDD's Evidence Model Layer A to the surfaces Connect
   *actually has*. *(This atom still goes through the legacy HTML form —
   the verification config page isn't part of PR #1135's automation API.)*

   **Call it with `organization_slug: <pm_org>` — the PROGRAM's org, never
   the holding org.** The page is PM-only: Connect serves it only when the
   requesting org manages the program AND is not the org holding the
   opportunity (`is_opportunity_pm`; ace#2419). So:

   - **`pm-nm` mode** → call at `pm_org`. Proved live 2026-09-26 on the
     NM-held probe `7bfcb845-015c-416a-a200-9795c68dfc55`: at the PM-org
     URL a rule saved (`form_field_rules_saved: 1`); at the NM-org URL the
     page redirected.
   - **`self-managed` mode** → the page can never serve (request org ==
     holding org). The atom now raises a typed `verification_page_pm_only`
     error instead of mis-blaming the payload. Do not retry; record every
     intended rule under `verification.not_applied_reason` citing ace#2419,
     record each as a rule decision row with `enforcement: gap` (Step 8a),
     and carry the rules
     to Phase 9's partner opportunity. Configuring `ACE_CONNECT_NM_ORG` is
     the fix.

   **Read this before writing anything: five of the eight documented
   flags no longer exist on Connect's form (dimagi-internal/ace#1013).**
   `duplicate`, `gps`, `gps_radius_meters`, `catchment_areas` and
   `deliver_unit_checks[].check_attachments` are still *accepted* by the
   atom for back-compat, but the corresponding inputs are ABSENT from the
   page — Django drops them and the atom **still returns `ok: true`**.
   Setting them does not enforce anything; it only writes an artifact that
   claims enforcement which does not exist. **Do not send them.** Record
   the affected Layer A rules as `[PLATFORM]` gaps in the phase summary
   and name where they are enforced instead (usually the CCZ).

   What works today:

   - `form_field_rules` — **the only surface on which a PDD Layer A
     predicate can be enforced server-side.** One entry per
     `(question_path, question_value, deliver_unit_id)` the predicate
     requires. Additive and idempotent.
     - **`question_path` is a JSONPath into the HQ form-JSON doc, NOT an
       XForm XPath.** Connect evaluates it as
       `jsonpath_ng.ext.parse(f"$.{question_path}")` against the whole
       forwarded document, in which HQ nests the instance under `form` —
       so the CCZ's `/data/meeting_basics/meeting_conducted` is written
       here as **`form.meeting_basics.meeting_conducted`**. An XPath makes
       that parse raise, the receiver 500s on the HQ→Connect forward, and
       **every payable visit is lost while the device still shows "1 form
       sent to server!"** (observed on `spark-facilitator/20260813-2126`,
       dimagi-internal/ace#1301 — HQ motech log recorded a 500 for the
       deliver form while every non-payable form on the same app got 200).
       The atom normalises `/data/a/b` → `form.a.b` for you, but write it
       correctly so the artifact reads truthfully.
     - **Read the group/question names out of the RELEASED CCZ, never
       from the PDD's prose.** The PDD quotes the partner's original app;
       Nova rebuilds the form and routinely flattens or renames groups, so
       the PDD path can name a node that does not exist — and a rule
       matching no node enforces nothing while reporting success. Download
       the released CCZ (`commcare_download_ccz` with `write_to_path`),
       read the payable form's `<bind nodeset=...>` list and its
       `<select1>` `<value>` options, and translate each nodeset to
       `form.<...>`. (Live example: PDD said
       `/data/community_meeting/meeting_type`; the released CCZ bound it
       at `/data/meeting_type`, so the rule is `form.meeting_type`.)
     - `question_value` is the **stored** option value, never the display
       label.
     - `deliver_unit_id` is the DU `server_id` — same value
       `required_deliver_units` takes, not the per-opp display index.
     - `name` is capped at **25 chars**; a longer name silently fails the
       WHOLE formset.
     - **Verify via `form_field_rules_saved` in the response** — the count
       Connect actually persisted. It is the only evidence the write
       landed; compare it against the number of rules you sent. But note
       what it does NOT prove: ace#1301 shipped two rules that persisted
       fine and then crashed Connect's receiver on every payable visit,
       because "Connect stored the string" and "Connect can evaluate the
       string" are different claims. The end-to-end proof is Phase 6's
       `connect_get_deliver_progress` showing `delivered >= 1`.
   - `form_submission_start` / `form_submission_end`: HH:MM:SS — set
     only if the PDD has time-of-day plausibility constraints.
   - `deliver_unit_checks[].duration_minutes` — MINUTES, matching the
     form's own help text. Set only if the PDD states a minimum delivery
     duration. (The old `duration_seconds` spelling is now REFUSED with a
     typed error rather than silently writing a 60x-too-long floor —
     ace#1013.) **Verify via `deliver_unit_checks` in the response** — the
     deliver_unit formset read back after the write, one
     `{deliver_unit_id, duration_minutes}` per row. A requested floor that
     does not read back on its unit throws
     `verification_duration_not_persisted` (ace#2945); record the read-back
     value, not the value you sent.
   - **Any other flag is refused, not dropped.** `gps`, `duplicate`,
     `catchment_areas`, `gps_radius_meters` and `check_attachments` have no
     input on the live form, so a truthy value now raises
     `unsupported_verification_flag` BEFORE the POST. That is deliberate:
     the atom used to accept them, Django dropped them, and it returned
     `ok: true` — which is how six opportunities across 2026-06-06..07-28
     reported "verification flags configured" with nothing persisted. If
     the PDD needs one of these predicates, express it as a
     `form_field_rules` rule or cite the CCZ-side enforcement; do not
     re-send the dead flag.

   **A per-entity cap or a "repeat is not payable" rule REQUIRES a
   `form_field_rules` row — the `entity_id` key does not enforce it
   (ace#2512).** With `duplicate` refused (above) and force-disabled under
   automatic visit verification, Connect resets a repeat key to `pending`,
   auto-approves it and pays it again (`playbook/integrations/connect-api.md
   § A repeated entity_id is PAID AGAIN`). So when the PDD caps paid
   encounters per entity (or per step), write a rule on the Deliver form's
   computed `payable_slot` field (`question_value` = its stored `yes`),
   read out of the released CCZ like any other path. If the released form has
   no such field, do NOT record the cap as enforced: record it as a
   `[PLATFORM]` gap / Phase 3 defect in the summary. Also check the payment
   unit's `max_daily` / `max_total` against EVERY record kind that carries the
   `deliver_unit` marker, not only the payable ones — flagged and rejected
   visits still count toward both caps, so a non-payable record kind on the
   paid unit exhausts `max_total` early.

   Layer A rules that none of these can carry (photo-present, date sanity,
   cross-field consistency) are normally already enforced *in the CCZ* — cite
   that in the summary rather than leaving the rule looking dropped. Dedup is
   NOT among them: a CCZ cannot see another submission's payment, and Connect
   does not dedup payment on a repeated key (ace#2512).

6. **Configure payment units** *(also runs on an existing opportunity:
   § Operations on an existing opportunity)* via `connect_create_payment_units` (plural,
   atomic batch — the new automation API takes a list). Build one entry
   per unit in the PDD's payment plan; the entire request is rejected if
   any unit is invalid.

   > **Which org URL, Steps 6–7 (live matrix 2026-09-26,
   > `playbook/integrations/connect-api.md § PM→NM org-URL matrix`).**
   > Pass `organization_slug: <pm_org>` to every call in Steps 6–9. The REST
   > atoms here (`create_payment_unit(s)`, `activate_opportunity`,
   > `send_flw_invite`) hit `/api/opportunities/<id>/…`, which authorises an
   > admin of EITHER the program's org or the holding org, so the slug does
   > not select anything — but the HTML reads DO read the org off the URL:
   > `connect_list_payment_units` at the NM-org URL returns rows WITHOUT
   > `payment_unit_uuid` / `amount` (observed on the probe), and
   > `connect_get_learn_passing_score` is program-scoped (404 at the NM org).
   > `pm_org` serves every surface Phase 4 uses.
   >
   > **ace#573 does not bite across orgs.** Connect keys the `CommCareApp` row
   > — and so its `DeliverUnit`s — on the HOLDING org
   > (`program/api/serializers.py`: `CommCareApp.objects.get_or_create(...,
   > organization=<holding org>)`). The probe opportunity, held by the NM org
   > and wired to a Deliver app whose PM-org DeliverUnit (7083) was already
   > bound to another opportunity's payment unit, got a fresh DeliverUnit
   > (7084) and its payment unit created cleanly.

   **ALWAYS pass `total_budget`** (the same whole-unit integer you set on
   the opportunity in Step 4) as a top-level arg to
   `connect_create_payment_units` / `connect_create_payment_unit`. The MCP
   uses it to enforce the funds-≥1-FLW guard **in code** — it computes
   `number_of_users = total_budget / Σ(max_total × (amount + org_amount))`
   over the integers in the request and **rejects with `opportunity_underfunded`
   BEFORE creating any PU** when `< 1` (jjackson/ace#729). This is the
   authoritative guard; it cannot be fooled by a dollars-vs-cents mix the way
   the old hand-computed check could. If you get `opportunity_underfunded`,
   the opp is genuinely unclaimable — raise `total_budget` (and the program
   budget), lower `max_total`, or fix the `amount` unit; do NOT retry
   unchanged. Per-unit fields:
   - `name`: descriptive (e.g. `"Per verified visit"`)
   - `description`: payment criteria
   - `amount`: per-unit FLW pay from PDD. **MUST be a non-negative
     integer in WHOLE currency units** (e.g. whole USD), NOT cents.
     Connect stores `amount`, `org_amount`, and `total_budget` as plain
     integers in the SAME whole-currency unit — verified against
     commcare-connect `opportunity/models.py`: `PaymentUnit.amount` and
     `org_amount` are `PositiveIntegerField`, `Opportunity.total_budget`
     is `PositiveBigIntegerField`; no cents, no decimals. The serializer
     rejects floats. If the PDD specifies a fractional rate (e.g.
     `$1.50`), **round to the nearest whole unit** (`$1.50` → `2`) and
     log an `[INFO]` to `comms-log/observations.md` noting the rounding.
     - **NEVER pass cents.** `$1.50` → `150` is a 100× overpay: Connect
       reads `150` as **$150 per visit**, which (a) renders the wrong
       number on the FLW Download gate ("Earn up to N USD for visit")
       and (b) inflates `Σ(max_total × (amount + org_amount))` 100×, so
       the budget guard below demands a 100×-too-large `total_budget`
       and `number_of_users = total_budget / Σ(...)` collapses below 1
       → the FLW physically cannot claim the opp (no `OpportunityClaim`
       is created). Caught live on `bednet-spot-check/20260605-2303`: a
       `$1.00` intent passed as `100` showed "Earn up to 100 USD for
       visit" and made a `$100` program budget fund 0.008 users.
     - Never silently truncate (`$1.50` → `1`) — that's where the
       prior `turmeric-20260503` run produced a malformed PU.
     - **Sub-\$1 rates round UP to the \$1 minimum, never to cents.** A
       PDD smoke rate like `$0.50` is NOT representable in whole USD —
       use `1` (the minimum payable whole unit) and log an `[INFO]`. Do
       NOT reach for cents (`50`) to preserve the half-dollar: Connect
       reads `50` as **$50/visit**, which is the exact mix that shipped
       an unclaimable opp on `bednet-spot-check/20260606-2013`
       (`amount=50, total_budget=50` → `number_of_users=0.05`). If the
       PDD genuinely needs sub-dollar economics, that's a PDD/program
       issue to raise, not a cents workaround.
   - `org_amount`: per-unit LLO pay — **REQUIRED for managed opps**.
     Same WHOLE-currency-unit integer constraint as `amount` (NOT cents).
     (Note: commcare-connect commit
     `4c430de3` loosened this validation on 2026-04-29 to accept `0` —
     before that fix, falsy values were rejected with
     `org_amount is required for managed opportunities.`)
   - `max_total`: total visits per user across the opportunity (≥1)
   - `max_daily`: visits per user per day (≥1)
   - `start_date` / `end_date`: optional; default to opportunity dates
   - `required_deliver_units`: which DU ids MUST be completed for this
     payment to trigger. **Pass `du.server_id`, not `du.id`.** As of
     0.13.126 `connect_list_deliver_units` populates `server_id` (the
     server-side primary key Connect's DB uses) on each returned DU by
     reading the create-payment-unit form's checkbox values; this is
     the field the create endpoint accepts. `du.id` is the per-opp
     display index (1, 2, 3…) and is rejected by the server as
     "Invalid Data". The MCP backend has a name-mapping fallback that
     accepts `du.id` and maps it for you, but passing `server_id`
     directly is the documented happy path. **Every payment unit MUST
     carry at least one `required_deliver_units` id — this is a hard
     pre-create gate, not a nicety.** Before calling
     `connect_create_payment_units`, assert each unit's
     `required_deliver_units` is non-empty (wire the just-synced DU
     `server_id`(s) from Step 4's `connect_list_deliver_units` onto the
     unit — for a single-DU app that's the one DU's `server_id`). An
     empty `required_deliver_units`: (a) fails the opp's
     `is_setup_complete`; (b) blocks Phase 8 `connect_send_flw_invite`
     and Phase 6 mobile screenshot capture (the FLW can't claim the
     opp); and (c) makes Phase 7 synthetic accrual mint
     `completed_works: 0` / `completed_module: 0` regardless of how many
     visits are generated — the engine attributes completed work to a
     unit's required DUs, so with none there is nothing to attribute
     (jjackson/ace#843, confirmed live on
     `hh-poverty-targeting/20260702-1456`: a PU existed but
     `required_deliver_units: []` → 498 visits, 0 completed works).
     Closes jjackson/ace#106 finding 5 + jjackson/ace#843.
   - `optional_deliver_units`: which DUs are bonus/optional. **No DU id
     may appear in `required` and `optional` of the same unit, AND no DU
     may appear in two payment units in the same request** — the server
     rejects the whole batch.

   Use `connect_create_payment_unit` (singular) only when adding a single
   PU after the fact; under the hood it sends a 1-item list to the same
   endpoint and shares the same validation rules.

   **Verify-after-create (mandatory) — the CREATE RESPONSE is the
   authoritative round-trip source.** `connect_create_payment_units`
   returns Connect's own post-persist serialization of each stored PU.
   That object — not a follow-up list call — is what you assert against
   the request payload. Per unit, check:
   - `name`, `amount`, `org_amount`, `max_total`, `max_daily` — exact
     match against the request payload.
   - `required_deliver_units` — **must be non-empty** AND array length
     matches request AND contains the same DU ids (order may differ). A
     genuinely empty `required_deliver_units` **in the create response**
     is a `[BLOCKER]` even if the rest of the unit matches (it zeroes
     Phase 7 accrual — see the create-time gate above, jjackson/ace#843).
   - `optional_deliver_units` — same.

   **Do NOT gate on `connect_list_payment_units` for these fields.** That
   atom's HTML-scraped read path cannot see them: `required_deliver_units`
   and `optional_deliver_units` come back `[]`, and `description` comes
   back `""`, **unconditionally** — the listing renders DU display names
   in an Alpine.js template with no server ids (pinned by
   `test/mcp/connect/unit/html-scrape.test.ts` "still cannot parse
   deliver-unit server IDs from the listing"). So an empty
   `required_deliver_units` from the list call is a constant of the read
   path, carrying zero information about stored state — halting on it
   halts every healthy run. Observed live on
   `spark-facilitator/20260813-2126`: the create response carried
   `required_deliver_units: [6617]` while the list call on the same PU
   returned `[]`, and the opp activated normally (Connect only permits
   activation when a valid PaymentUnit exists). Same divergence on
   `bednet-spot-check/20260728-2222`. Tracked as dimagi-internal/ace#1026
   (consolidated into the #1022 read-back umbrella); until the atom either
   parses the DU column or omits what it cannot read,
   `connect_list_payment_units` is corroboration on **`payment_unit_uuid`
   and `name` only**.

   **`id` is NOT on that list — it is a per-opp display index, not the
   server PK (dimagi-internal/ace#1642).** The listing's first column is
   the row's `#`, so the same PU that `connect_create_payment_units`
   returned as `id: 2495` reads back as `id: 1` seconds later (observed
   on `bednet-check-2-visit/20260825-1310`, opp
   `7cea3952-8375-43ca-979f-53db29302409`). Passing the list's `id`
   anywhere a server id is required reproduces the `du.id` vs
   `du.server_id` "Invalid Data" rejection this step already warns about
   for deliver units. **The durable identifier is
   `payment_unit_uuid`** — it matches the create response's
   `payment_unit_id` exactly and is the only field safe to key on.

   The check's intent stands — an unwired payment unit is exactly the
   #843 class and must still be caught. It is caught at the create
   response (and, end-to-end, by Phase 6's
   `connect_get_deliver_progress` showing `delivered >= 1`). What
   changed is only which source is authoritative.

   **Action on any mismatch in the create response:** halt with a
   `[BLOCKER]` in the gate
   brief specifying the exact field divergence (sent vs. stored). Log
   the full sent payload AND the full server response to
   `comms-log/observations.md`. Do NOT proceed to Step 7 — a malformed
   PU cascades through `is_setup_complete` and silently breaks every
   downstream skill (Phase 8 invites, Phase 6 screenshots). Operator
   recovery is delete + recreate via the Connect web UI; a
   connect-delete-payment-unit atom (*not yet built*) would let the
   skill self-heal.

   This guard is the producer-side complement to the
   `connect-program-setup-eval` rubric. The eval correctly graded a
   malformed PU as `payment_unit_fit: 5.0` (warn) on the
   `turmeric-20260503-0835` run, but by then Phase 4 had already
   handed off to Phase 5 with corrupted state. Catching the
   malformation at the source converts a multi-phase cascade into a
   single-skill halt.

   **Budget-funds-≥1-FLW guard — now enforced in MCP code (jjackson/ace#729).**
   You do NOT hand-compute this guard. When you pass `total_budget` to
   `connect_create_payment_units` (Step 6), the connect MCP computes
   `number_of_users = total_budget / Σ(max_total × (amount + org_amount))`
   over the request integers and **rejects with `opportunity_underfunded`
   BEFORE creating any PU** when `< 1`. This supersedes the hand-computed
   prose check that shipped in #722 — that check failed live on
   `bednet-spot-check/20260606-2013` because the agent evaluated it in
   dollars (`$0.50`) while storing cents (`50`), so `number_of_users` read
   as 5 in-head but 0.05 in Connect. Code over the sent integers can't make
   that mistake. **This is the silent root behind the Phase-6 Deliver
   "Unable to claim" / no-`OpportunityClaim` class.**

   On `opportunity_underfunded`: the create did NOT happen (no orphan PU).
   Write a `[BLOCKER]` to `comms-log/observations.md`, set
   `phases.connect-setup.status: error` in the current run's
   `run_state.yaml`, and **HALT** — do NOT activate or hand off to Phase 6.
   Remediate by raising `total_budget` (and the program budget — see the
   Step 4 floor + `connect-program-setup`), lowering `max_total`, or fixing
   the `amount` unit; then re-run. Do NOT retry unchanged. The error payload
   carries `total_budget`, `min_budget_for_one_user`, `number_of_users`, and
   a per-PU `breakdown` for the remediation message. The Step 4 `total_budget`
   floor sizes it right going in; this code guard is the structural backstop
   that makes an underfunded opp impossible to ship regardless of agent
   unit-reasoning.

6.5. **Activate the opportunity in Connect** (REQUIRED for ACE-driven runs;
   prerequisite for Step 7's test-user invite).

   ACE's dogfood pipeline activates the opp here, in Phase 4, so the ACE
   test user can be invited synchronously and Phase 6
   `app-screenshot-capture` can drive the AVD against a real opp.
   Real-LLO go-live remains a separate, human-gated event in Phase 9
   `llo-launch` — that skill becomes idempotent on already-active opps
   from this step (skip-and-log).

   Why this isn't a Phase 8→9 boundary violation: the opp lives in
   `connect-ace-prod` (Dimagi-controlled HQ project space) and is
   `is_test=true`. The ACE test user (`${ACE_E2E_PHONE}`) is also ACE-
   controlled. No real LLO sees this state until Phase 9's awardee
   email, which is still gated behind the unconditional Phase 8→9 pause.

   - **Always attempt the activate transition — do NOT pre-check the
     `active` flag to decide whether to call it.** Call
     `connect_activate_opportunity({organization_slug, opportunity_id})`
     unconditionally. The atom hits `POST /api/opportunities/<id>/activate/`,
     which validates that the opp hasn't ended and at least one
     PaymentUnit exists (Step 6 satisfies the latter). Returns
     `{ id, opportunity_id, name, active: true }` on success.

     **Why unconditional (jjackson/ace#624):** the managed-opp create
     endpoint returns `active: true` as a create-side flag, but that is
     NOT the `/activate/` state transition `invite_users/` (Step 7)
     requires. `connect_get_opportunity` reports `active=true` while the
     opp is still un-transitioned, so the old "skip if already active"
     pre-check skipped the only call that actually enables invites — and
     Step 7 then failed. Calling `/activate/` on such an opp **succeeds**
     (it is not yet active by the endpoint's definition); it rejects only
     an opp that already went through this same transition. So always
     call it and branch on the result, never on the read-back flag.
   - **Treat the "already active" validation error as the idempotent
     skip signal** (NOT a hard error). If the activate call rejects
     specifically because the opp already completed the `/activate/`
     transition (e.g. a Phase-4 re-run on the same opp), catch that one
     error, log `[INFO]` to `comms-log/observations.md`, and proceed to
     Step 7:

     ```
     <ISO> connect-opp-setup: opp <id> already activated; treating activate rejection as idempotent.
     ```
   - **Verify activation via Step 7's invite succeeding — NOT via the
     scraped `active` flag.** Do not call `connect_get_opportunity` to
     confirm `active=true` here: that read-back flag is the same
     create-side signal that returns `true` on an un-transitioned opp
     (see above), so it can't distinguish a real `/activate/` from a
     no-op. The authoritative confirmation is the downstream
     `connect_send_flw_invite` in Step 7 — `invite_users/` hard-rejects a
     non-active opp ("Opportunity must be active to invite users"), so a
     successful invite is the only proof the transition actually landed.
     If Step 7's invite rejects with that error, the activate didn't take
     — halt there with `[BLOCKER]`.
   - **On hard error from the activate call**, halt with `[BLOCKER]` and
     surface the server error verbatim in `auto_surfaced`. The most
     common cause is "no PaymentUnit" — Step 6's verify-after-create
     check should already have failed loudly; if we got here without
     one, the verify-after-create has a gap to file against.

6.6. **Deferred verify-after-create — re-read the dashboard fields now
   that they are readable (dimagi-internal/ace#1647).**

   Step 4's Write→Read→Compare could not see `start_date`,
   `total_budget`, `learn_app.cc_app_id` or `deliver_app.cc_app_id`: a
   never-activated opportunity renders only the edit-form half of
   `connect_get_opportunity`. Activation (Step 6.5) makes the dashboard
   half readable, so the deferred comparisons run **here**, against the
   same payload Step 4 sent.

   - Call `connect_get_opportunity({organization_slug, opportunity_id})`
     once more.
   - Compare against the Step 4 request payload:
     - `start_date` — `YYYY-MM-DD` match
     - `total_budget` — numeric match
     - `learn_app.cc_app_id` — bare 32-char match
     - `deliver_app.cc_app_id` — bare 32-char match
   - **On any disagreement → `[BLOCKER]`** in `auto_surfaced`; log both
     values to `comms-log/observations.md`; do NOT proceed to Step 7.
     A wrong `cc_app_id` means the opportunity is wired to the wrong
     CommCare app, which cascades silently through Phase 6's device walk
     and Phase 7's accrual.
   - **If a field is STILL absent after activation, that is a
     `[BLOCKER]` too — not a pass.** The read surface changed shape;
     say so verbatim rather than substituting a default or treating the
     absence as agreement. Never record a comparison you did not
     perform.

   Do not confuse this with Step 6.5's own verification: activation is
   still confirmed by Step 7's invite succeeding, never by the scraped
   `active` flag (see above). This step re-reads *stored configuration
   values*, which is a different question from *did the state transition
   land*.

7. **Pre-invite the ACE test user (REQUIRED for PersonalID registration).**

   This step is structurally load-bearing for ACE's emulator-driven mobile
   testing — not just a convenience. Two reasons ACE must invite
   `${ACE_E2E_PHONE}` to every Connect opportunity it creates:

   **(a) Claim flow:** Phase 6 `app-screenshot-capture` drives Connect mobile
   through the claim-opp flow as this user; without the invite, the opp
   won't appear in the test user's opportunity list and the screenshot
   recipe stalls.

   **(b) PersonalID registration gate (the critical reason):** Connect-id's
   `/users/start_configuration` endpoint runs an `@app_integrity` decorator
   that synchronously calls `check_number_for_existing_invites(phone)` over
   HTTP to connect.dimagi.com. **For phone numbers with NO existing invite
   anywhere in Connect, this lookup hangs long enough to trip gunicorn's
   worker timeout, which kills the worker via `sys.exit(1)`.** The client
   receives an empty/malformed response and force-stops (CommCare NPE on
   `getSessionFailureSubcode()`). See Sentry `CONNECT-ID-3F`.

   `POST /api/opportunities/<id>/invite_users/` validates that the opp is
   **active** and not ended. Step 6.5 above just satisfied the active
   precondition synchronously, so the invite fires here directly — no
   deferral.

   Args:
   ```
   connect_send_flw_invite({
     organization_slug: <pm_org>,
     opportunity_id: <UUID from step 4>,
     phone_numbers: [process.env.ACE_E2E_PHONE]
   })
   ```
   The atom returns `{ status: 'queued', invited_count: N }` because the
   server invokes `add_connect_users.delay(...)` async. The `UserInvite`
   row + SMS go out within a few seconds. Treat `queued` as success **for
   sending the invite** — but see the queued ≠ accepted caveat below.

   **`queued` is NOT proof the invite landed — read it back (ace#824/#855).**
   `invited_count: N` only confirms Connect enqueued the `UserInvite`. The
   resulting `OpportunityAccess` may have **no linked ConnectID user**, and
   Connect's mobile API filters opportunities by `opportunityaccess__user`:

   ```
   Opportunity.objects.filter(opportunityaccess__user=request.user, archived=False)
   ```

   An access with a null user matches nothing, so the opportunity is invisible
   to the device **forever** — and per the ConnectID change in `2bd03c4` it does
   NOT self-heal. Proven live 2026-07-25: a fresh invite returning
   `{status:'queued', invited_count:1}` never appeared on device through either
   an in-app sync or a swipe-refresh, while five previously-linked
   opportunities rendered fine.

   **So read it back with `connect_list_flw_invites`** (ships since ace#855;
   read-only, one authenticated GET):

   ```
   connect_list_flw_invites({
     organization_slug: <pm_org>,
     opportunity_id: <UUID from step 4>,
     phone: '${ACE_E2E_PHONE}'
   })
   ```

   Branch on whether a row EXISTS — **not** on `claimed`:

   - **`match !== null`** → the invite is recorded. `status: 'pending'` with
     `name: null` is the NORMAL pre-claim state (acceptance happens on-device
     when Phase 6's `connect-claim-opp` claims the tile), so pending is a
     pass here. Record `invited_at` and proceed.
   - **`match === null`** (no row at all for that phone) → **recover before
     you warn — wait, re-read, then re-send ONCE (ace#2946).** A `queued` send
     fired right after `/activate/` can create nothing at all, and one
     identical re-send fixes it. Do this, in order:
     1. **Wait ~60 s and re-read** with the same `connect_list_flw_invites`
        call (wait via a Monitor/until-loop or the next tool call, never a
        foreground `sleep`). A row now → treat as `match !== null` below.
     2. **Still null → re-send the SAME `connect_send_flw_invite` call ONCE**
        (same `organization_slug`, `opportunity_id`, `phone_numbers`). The
        invite endpoint is idempotent per phone, so a second send cannot
        double-invite. Then re-read.
     3. **Only if the row is STILL absent** record `invite_row_present: false`
        and **WARN loudly**: the send reported success twice but Connect has
        no invite. That is the #824 silent failure; name it in the phase
        summary rather than letting Phase 6 discover it on AVD wall-clock.

     Record BOTH sends (timestamps + each read-back result) in the run's
     `comms-log/observations.md`, so a reader can tell "recovered on re-send"
     from "landed first time". Do not re-send more than once — a second
     failure is the signal, not something to loop on.

     *Live evidence:* `smallholder-seasonal/20261014-0859` Phase 4, opp
     `30605010-4be8-49e3-954c-deeb0b4ad8d6` (held by the NM org).
     `connect_activate_opportunity` at ~07:00:50Z, then the invite →
     `{invited_count: 2, status: "queued"}`; three reads at ~07:01, ~07:02 and
     ~07:03:50 (both PM- and NM-org URLs) returned `invites: []`, while the
     same atom returned rows on a sibling opp, so the reader worked. One
     identical re-send at ~07:03 → both rows present, `status: pending`, and
     the requester row's `invited_date` was `15-Oct-2026 07:03` — the RE-SEND
     time, not ~07:00. The first queued send created nothing; it was not lag
     that later caught up. (Suspected, not proven: the async
     `add_connect_users` task ran before the just-activated state was visible
     to the worker.)

   Do NOT gate on `match.claimed` — it reports whether the worker has already
   CLAIMED the opp, so requiring it would fail every legitimate fresh run.
   The atom throws `WorkersTableSchemaError` if Connect reshapes the workers
   table, so a parsing failure is loud rather than a false verdict.

   The claim-recipe centering bug (jjackson/ace#800 — `centerElement: true` on
   the OPP_RUN_ID title-scroll) is still the thing to rule out when a tile IS
   present and asserted-visible but won't claim; that is a recipe failure, not
   an invite-propagation one.

   Hold the invite metadata in memory for Step 10's consolidated write:

   **Collect the READ-BACK result, not just the send** — these are the exact
   field names `lib/phase-products-schema.ts` declares and
   `REQUIRED_PRODUCT_KEYS` checks at the phase boundary. Using any other
   spelling (the pre-#1286 template said `invited_phone` / `invited_at`)
   writes fields the schema does not declare: they survive only because the
   object is `.passthrough()`, so they validate clean at write time and
   contribute nothing at the boundary, and Phase 4 then fails
   `verify_phase_products` on every run and repairs by hand.

   ```
   ace_test_user = {
     phone: ${ACE_E2E_PHONE},           # or this run's minted phone — see 7b
     invite_row_present: <bool>,        # match !== null from connect_list_flw_invites — REQUIRED at the boundary
     connect_user_id: <string | null>,  # populates on CLAIM; null on a pending row is NORMAL
     status: <accepted | pending | unknown>,
     checked_at: <ISO timestamp>,       # when the read-back ran (NOT the send time)
   }
   ```

   `invite_row_present: false` is a LEGAL, contract-satisfying value — it
   records a verified-absent row, which is what Step 7's `[BLOCKER]` acts on.
   What the boundary rejects is the key being ABSENT, i.e. the read-back never
   ran. Capture `connect_user_id` and `status` for real rather than defaulting
   them — Phase 6 wants both — but do NOT read `connect_user_id` as a fault
   indicator here.

   **`connect_user_id: null` on a pending row is the NORMAL pre-claim state,
   NOT the ace#824 signature (ace#1663).** On this read path the id is not a
   view of the `OpportunityAccess.user` FK at all: `parseWorkersTable`
   (`lib/connect-flw-invites.ts`) extracts it from the **Name cell**, which
   Connect renders as a bare `-` until the worker claims the opportunity —
   so `cellText` yields null and the id stays null on *every* pending row,
   whatever the underlying link is. It populates on CLAIM, exactly like
   `name`, and null therefore carries no information about #824 at Phase 4.
   Reading it as a fault would raise a `[BLOCKER]` on every healthy run,
   since Phase 4 invites and Phase 6 claims. Verified live on
   `hh-poverty-targeting/20260824-1404`: the same atom and the same phone
   returned `connect_user_id: null` on a fresh pending invite and
   `"1277adbd0ceea89e367d"` on a CLAIMED opp of the same program.

   At Phase 4 the only #824 discriminator on this path is **row existence**
   (`invite_row_present`), which Step 7 already gates on. The linked-vs-
   unlinked distinction does not become observable until after a claim —
   Phase 6's claim attempt is what surfaces it.

   All Connect-opp-setup state is emitted in one atomic write at
   end-of-skill (Step 10). A crash between Step 7 and Step 10 loses
   the in-memory metadata; recovery is `/ace:step connect-opp-setup`
   re-run — the invite atom itself is idempotent (already-invited
   phone numbers return without error from the queued add-users
   task).

   The historical `ace_test_user_invite_pending_until_active` flag is no
   longer written. Step 6.5 activates synchronously, so the deferred-to-
   `llo-launch` branch is dead code. `llo-launch` (Phase 9) only sends
   the real-LLO invite; it does not re-fire the ACE test-user invite.

7b. **Per-run demo test user — OFF BY DEFAULT (ace#1289). Skip this entire
   sub-step unless the switch is on.**

   **Read the switch first, and read it exactly once:**
   `perRunTestUserEnabled()` from `lib/per-run-test-user.ts` — the env var is
   `ACE_PER_RUN_TEST_USER`, and it is `false` for unset / empty / `false` /
   `0` / `off` / any typo (it fails CLOSED). **If it is off, Step 7 above is
   the whole story: invite `${ACE_E2E_PHONE}`, read it back, and move on.
   Nothing below runs.**

   **What changes when it is on.** Instead of the fixed `${ACE_E2E_PHONE}`,
   this run mints its OWN demo number:

   ```
   const testUser = derivePerRunTestUser(run_state.yaml.run_id)   // lib/per-run-test-user.ts
   // → { phone: '+7426…', phoneLocal, countryCode: '+7', name: 'ACE Test <run_id>' }
   ```

   Deterministic from the run id, so a re-entered or resumed run registers the
   SAME user rather than orphaning the first one. Send the Step 7 invite to
   `testUser.phone` in place of `${ACE_E2E_PHONE}` — everything else about the
   call is identical.

   **The read-back branch INVERTS, and this is the part to get right.**
   Registration requires a pre-existing invite (connect-id `decorators.py`), but
   Connect creates the invite → `OpportunityAccess` link only at invite time and
   only if the ConnectID user ALREADY EXISTS (`opportunity/tasks.py`). A phone
   nobody has registered yet therefore produces **no row, or a row with
   `connect_user_id: null`** — and under a per-run phone that is the EXPECTED
   state, not the ace#824 silent failure. Do NOT `[BLOCKER]` on it.

   Classify with `classifyPerRunPreRegistrationGate(match)` and log its
   `reason` verbatim. The real gate lives downstream in Phase 6, after the
   device registers and the invite is re-sent — see
   `skills/app-screenshot-capture § Step 4`. The verified ordering is
   **invite → register → re-invite** (ace#855, live-verified on
   `hh-poverty-targeting/20260702-1456`); the old self-heal that used to paper
   over the missing link, `resend_connect_invite`, is dead code with zero
   callers.

   **Write two extra fields** into the Step 10 `ace_test_user` block — both are
   REQUIRED at the phase boundary once `per_run` is true
   (`PER_RUN_TEST_USER_REQUIRED_KEYS` in `lib/phase-products-schema.ts`):

   ```
   phone: <testUser.phone>   # the MINTED number, not ${ACE_E2E_PHONE} — Phase 6
                             # has no fallback and cannot proceed without it
   per_run: true             # the contract discriminator; it is what moves the
                             # blocking gate from Phase 4 to post-registration
   ```

   **Do not flip the switch on to "try it".** The precondition is: *the 7 camera
   ids in `connect-register-from-otp.yaml` are calibrated against a live
   `mobile_capture_ui_dump` on the APK baseline in force, and one fresh-signup
   registration has completed on that same baseline*. Until then, per-run phones
   route every run through an uncalibrated photo-capture surface whose
   `runFlow.when visible:` guard fails SILENTLY. The sentence names no version
   on purpose — it said `2.63.2`, the baseline moved to `2.64.0` on 2026-09-06,
   and all five copies stayed behind (ace#1289). Both clauses remain open at
   2.64.0: residuals R2 and R4 of
   `docs/mobile-calibration/connect-2.64.0-2026-09-06.md`.

7.5. **Learn-app CCHQ pre-flight (Phase 6 prerequisite, idempotent).**

   Call `connect_preflight_learn_app_user` against CCHQ before the
   Phase 6 mobile recipe triggers `start_learn_app` from the Android
   client. Defense-in-depth probe for the auth / domain / user-conflict
   failure modes — surfaces them as a structured `{ok, action, reason}`
   outcome before Phase 6 boots the AVD.

   The probe is read-only — it hits `GET /a/<domain>/api/v0.5/user/`
   with the same `ACE_HQ_API_KEY` Phase 6 will eventually use.

   Args:
   ```
   connect_preflight_learn_app_user({
     hq_domain: <opp.connect.program.learn_app.cc_domain>,
     connect_username: <ACE test-user ConnectID username> | omitted,
     api_key: "${ACE_HQ_API_KEY}",
     hq_username: "${ACE_HQ_USERNAME}",
   })
   ```

   Branch:
   - `ok: true, action: 'would_create' | 'would_reuse_existing' | 'skipped'`
     → log `[OK]` to `comms-log/observations.md` and proceed to Step 8.
   - `ok: false` → halt with `[BLOCKER]` and surface `reason` verbatim.
     The remediation text is embedded in `reason` (rotate the HQ API
     key, fix the domain, reconcile the conflicting CCHQ user record,
     etc.). DO NOT continue to Step 8 — Phase 6 would 500 with no
     diagnostic.

   If the run is being executed without the ConnectID username in
   hand (the common case — ACE doesn't always know the FLW's
   ConnectID at opp-create time), omit `connect_username`. The probe
   then validates only API-key auth + domain reachability, which
   already catches the most common failure modes (rotated key,
   archived domain, CCHQ outage) at near-zero cost.

8. **Write config summary** via `drive_create_file` with
   `parentFolderId = phaseFolderId` (the `4-connect` folder; surfaced at
   `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`):
   - Opportunity ID (UUID) and URL
     (`<CONNECT_BASE_URL>/a/<holding_org>/opportunity/<uuid>/`)
   - **Both orgs and the mode:** program org (`pm_org`), holding org
     (`holding_org`), `org_mode`, and the `program_application_id` from 3a,
     so a reviewer knows which org the opportunity lives in (and so which
     org's membership lets them see it).
   - All configuration details (dates, total_budget)
   - Verification flags (final values, including which were inherited
     from defaults vs. set explicitly)
   - Deliver units (from create response) and Payment units (from step 6)
   - Whether the FLW pre-invite landed or is deferred until activation
   - **ConnectProd int_id** (`connect_int_id`, from the Step 4 create
     response; see step 9)
8a. **Record the opportunity's calls as decision rows** — ONE
   `decisions_append_rows` call right after the Step 8 write (§ Decisions
   Log). The decisions log (`decisions.yaml`, schema v6) is the run's review
   artifact: ace-web renders every row with a comment box and an answer
   editor, so "where is each PDD verification rule enforced" is a question a
   reviewer can answer on the run page. These rows are the ONLY record of
   these calls — `connect-opp-setup.md` does not restate them. Three kinds:
     1. **Rule rows** — `connect-rule-<slug>`, question exactly
        `Where is the PDD verification rule '<rule>' enforced?`, with **one row
        per verification rule stated in ANY PDD of the run**: the overview, and
        on a componentized run every component and program-level PDD (see
        § Inputs). Each carries `plain`, `check_at` (the Connect setting or
        app form/field a reviewer opens) and `correct_looks_like`, plus
        `scope` (`record` | `entity` | `worker` | `programme`) and
        `enforcement` (`enforced` | `by-design` | `gap`) — set them, or omit
        both and the write boundary computes them (`classifyRule`,
        `lib/decision-review.ts`); never contradict its rules (below).
        `ai-default` is the short `options` label (§ Decisions Log table);
        `reasoning` names the precise placement and its evidence, which is
        exactly one of:
        - `Connect form_field_rules: <name>` — evidence: `form_field_rules_saved`;
        - `Connect payment unit max_daily = <n>` / `Connect payment unit
          max_total = <n>` (per worker) — evidence: the payment unit's create
          response;
        - `Connect deliver_unit_checks.duration_minutes` / `Connect form
          submission window` — evidence: the value persisted;
        - `CCZ: <form> / <field> — <constraint or relevant>` — evidence: the
          Deliver summary line or released-CCZ bind that carries it;
        - `Not configurable on Connect — applied in <where>`;
        - `Not configurable on Connect — not applied anywhere in this build`.

        **"Not configurable on Connect" is a valid answer and must be
        stated, never omitted.** `connect_set_verification_flags` refuses
        `duplicate`, `gps` and `gps_radius_meters` (Step 5, ace#1013), so a
        PDD's duplicate-visit or GPS rule is exactly the row a reviewer cannot
        find anywhere else. A rule with no row is the defect this step exists
        to prevent.

        **A known limitation is a rule row with `enforcement: gap`** — a rule
        Connect refused (the `self-managed`-mode `verification_page_pm_only`
        case in Step 5, a refused flag) and that nothing else in the build
        holds. Never `by-design`: the design needs it and the build does not
        carry it. `decisions_enrich` turns every `gap` row into a review ask
        at phase end, so you do not set `review_ask` on it yourself.

        **Name the enforcement point that holds the rule AT ITS SCOPE, first.**
        A rule about a WORKER ("at most 1 payable meeting per CBF per day",
        "total cap 21 per CBF") is held on Connect by the payment unit's
        `max_daily` / `max_total`, which count per worker. An app (CCZ) check
        is keyed on the case its form is filled against — a community, a
        household — so it cannot stop one worker recording two communities on
        one day, and a per-step clamp of 7 × 3 is 21 per COMMUNITY, not per
        worker. Write the payment-unit limit first; an app check may follow as
        support, stated at its own scope (`also CCZ: date_of_meeting check —
        per community`), and the row's `scope` is `worker`. On
        `spark-facilitator/20260926-1800` both caps were written `CCZ: … ;
        also Connect payment unit …` and recorded as `CCZ constraint`, which
        told the reviewer the app enforced them. The write boundary's
        `classifyRule` treats a per-worker rule held only by an app check as a
        `gap` — get the order right here so the row says what holds it.
     2. **`[ACE]` latitude rows** — `connect-latitude-<slug>`, one per
        opportunity-configuration value the PDD left to ACE (dates, budget,
        max visits, payment amounts, flag thresholds).
     3. **`[FIXED]` ambiguity rows** — `connect-ambiguity-<slug>`, one per
        `[FIXED]` statement Phase 4 could not configure exactly as written.

     The Phase 4 boundary fails this skill if it wrote `connect-opp-setup.md`
     but zero rows carry `phase: 4-connect` + `skill: connect-opp-setup`
     (ace#2384), and warns on any live partner-facing row with no `plain`.

9. **Capture the ConnectProd integer opportunity ID** (Phase 7 prerequisite).

   Phase 7's `synthetic-data-generate` addresses opportunities by their
   **ConnectProd integer id** (the labs/synthetic surfaces and the
   `/a/<org>/opportunity/<int>/` URLs key off it) — a different
   identifier from the UUID. ConnectProd exposes BOTH on the same
   Opportunity row: it predates UUIDs and still returns the legacy
   integer `id` alongside the `opportunity_id` UUID. It is **not** a
   labs-minted value (labs only mints its own id for a purely-synthetic
   opp with no Connect opp behind it).

   **The integer is already in the Step 4 create response.**
   `connect_create_opportunity` returns `int_id` (ConnectProd's integer
   `id`) next to `id` (the UUID) — it is a required field of
   `ManagedOpportunityResponse`. Capture `int_id` from that response as
   `connect_int_id`. No Labs call, no UUID→int mapping, no
   subagent-reachability concern — the value ACE needs is in the response
   it already received at create time. (`connect_activate_opportunity`
   returns it too, so a re-read is the fallback.)

   If `int_id` is somehow absent from the create response (it should not
   be — the field is required upstream), log `[WARN]` to
   `comms-log/observations.md` and continue with `connect_int_id: null`;
   the Phase 7 operator can pass `--opp-int-id` manually.

   **Historical note (jjackson/ace#686 follow-up):** earlier versions did
   a `mcp__connect-labs__labs_context()` lookup here, on the mistaken
   belief — from a 2026-05-06 observation of the UUID-only
   `connect_list_opportunities` *scrape* path — that "the integer lives
   only in the labs DB." That was wrong: the create/activate REST
   responses carry it. The Labs lookup ALSO failed silently whenever
   Phase 4 ran as a subagent (the connect-labs MCP atoms aren't bound in
   subagent sessions), which is exactly how `connect_int_id` was left
   `null` on malaria-rdt/20260602-1409.

10. **Write the consolidated Connect outputs block** to
    `run_state.yaml.phases.connect-setup.products.connect` as one
    atomic patch. Read the program reference from
    `opp.yaml.connect.program` (or from
    `runs/<run-id>/4-connect/connect-program-setup.md`) and copy it
    into the run's `products.connect.program` so the run state is
    self-contained:

    ```yaml
    phases:
      connect-setup:
        products:
          connect:
            domain: <ACE_HQ_DOMAIN, e.g. connect-ace-prod>   # REQUIRED handoff key — phase-products contract + ace-web summary read it; omitting it fails verify_phase_products at the Phase 4 boundary fence (jjackson/ace#734)
            organization_slug: <= pm_org_slug; LEGACY key kept so pre-2026-09-26 readers still resolve>
            pm_org_slug: <the program's org — Step 3.0 pm_org>             # PM-only pages (verification rules, passing score) resolve here
            holding_org_slug: <the org HOLDING the opportunity — Step 3.0 holding_org>   # nm_org in pm-nm mode; reviewer access + opp URL resolve here
            org_mode: <pm-nm | self-managed>
            program_application_id: <UUID captured from the Step 3a invite POST | null on the already-applied skip>
            program:
              id: <UUID copied from opp.yaml.connect.program.id>
              url: <CONNECT_BASE_URL>/a/<org>/program/<uuid>/
            opportunity:
              id: <UUID>                       # from Step 4 create response
              name: <verbatim display name>    # from Step 4 create response — the exact tile text Connect renders (em-dash, NOT slug-reassembled). Phase 6 reads this as its OPP_NAME envVar; never recompose.
              url: <CONNECT_BASE_URL>/a/<holding_org_slug>/opportunity/<uuid>/   # the HOLDING org's URL — where the opportunity lives
              connect_int_id: <integer | null>    # ConnectProd integer id = create-response int_id (Step 9)
            verification:                      # Step 5's persisted config (shape per lib/phase-products-schema.ts)
              form_field_rules:
                - name: <=25 chars, e.g. consent_confirmed=yes>
                  question_path: <dotted path READ FROM THE RELEASED CCZ, per Step 5>
                  question_value: "yes"          # ALWAYS QUOTE the predicate. Bare `yes` is the string "yes" to the plugin's YAML 1.2 readers and the BOOLEAN true to PyYAML (ace-web's Python side), so the audit record of the payability predicate becomes parser-dependent (ace#2296). update_yaml_file now serializes 1.1-safe, and validate_run_state warns if any unquoted ambiguous scalar reaches the file.
                  deliver_unit_id: <int>
              form_field_rules_saved: <int>      # the count Connect actually persisted — the only evidence the write landed
            ace_test_user:                     # field names per lib/phase-products-schema.ts
              phone: ${ACE_E2E_PHONE}          # from Step 7
              invite_row_present: <bool>       # REQUIRED — the Step 7 read-back result
              connect_user_id: <string | null> # populates on CLAIM; null on a pending row is NORMAL, not #824
              status: <accepted | pending | unknown>
              checked_at: <ISO timestamp>      # when the read-back ran
              # ONLY when Step 7b ran (ACE_PER_RUN_TEST_USER on — default OFF, so
              # normally OMIT this line entirely). Setting it flips the boundary
              # contract to PER_RUN_TEST_USER_REQUIRED_KEYS, which additionally
              # requires `phone` (the minted number) — see lib/phase-products-schema.ts.
              per_run: true
            postcondition:                     # Step 11 — the live read-back of the end state
              ok: <bool>
              checked_at: <ISO timestamp>
              failed: [<check id>: <detail>, ...]      # empty when ok
              phase6_blockers: [<check id>: <detail>, ...]   # non-empty ⇒ Phase 6 must not walk
    ```

    Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
    `merge: 'deep'` on the current run's `run_state.yaml`. This is a
    *partial* patch of the `connect-setup` phase child (just
    `products.connect`), so `two-level` would replace the entire
    `connect-setup` block wholesale — dropping `connect-setup`'s own
    `status`, `steps`, etc. when the orchestrator already set them (the
    #572/#587 lost-update footgun). `deep` recursively merges
    `products.connect` while preserving every sibling at every depth.
    This skill is the sole writer of `products.connect`.

    **Pass `validateAs: { kind: 'phase-products', phase: 'connect-setup' }`
    on this `update_yaml_file` call.** The server validates the
    `products.connect` block against the single-source contract
    (`lib/phase-products-schema.ts` — the same shape ace-web's summary
    page reads) BEFORE the Drive write, and rejects with
    `INVALID_PHASE_PRODUCTS` if the block drifted — e.g. writing the
    opportunity at `products.opportunity` instead of nesting it under
    `products.connect.opportunity` (the malaria-rdt/20260604-1604 blank-
    summary drift, jjackson/ace#705). No Drive write happens on rejection;
    fix the nesting and retry.

    Phase 8's `synthetic-data-generate` reads
    `phases.connect-setup.products.connect.opportunity.connect_int_id` from
    the current run's `run_state.yaml` as the default for its
    `--opp-int-id` flag. When `connect_int_id` is null, the skill
    surfaces a `[WARN]` and asks the operator to pass `--opp-int-id`
    explicitly OR re-run `connect-opp-setup` to re-read `int_id` from the
    Connect create/activate response.

    **Do not write `opp.yaml.connect.opportunity` or
    `opp.yaml.connect.ace_test_user`.** Connect opportunities are
    created fresh per run (not reused across runs) and live only in
    this run's `products.connect`. `opp.yaml.connect.program` is the
    *only* durable Connect reference — written by
    `connect-program-setup`, never mutated here.

11. **Post-condition: read the live opportunity back and check the END STATE
    (inline QA).** Every atom above validated its own CALL; none of that proves
    the opportunity Connect now holds is the one this skill decided. A valid-but-
    wrong end state — a payment unit that never landed, the test flag off, an
    invite that was "queued" and never existed (ace#824), an opportunity that
    never made the `/activate/` transition (ace#617/#624) — otherwise surfaces two
    phases later as a Phase 6 walk hunting a tile that cannot exist. Run the three
    reads in ONE parallel message, against the holding org's URL:

    - `connect_get_opportunity({organization_slug: <holding_org_slug>, opportunity_id})`
    - `connect_list_payment_units({organization_slug: <holding_org_slug>, opportunity_id})`
    - `connect_list_flw_invites({organization_slug: <holding_org_slug>, opportunity_id, phone: "${ACE_E2E_PHONE}"})`

    Then evaluate them with `checkOppPostcondition(read, decided)`
    (`lib/connect-opp-postcondition.ts`, pinned by
    `test/lib/connect-opp-postcondition.test.ts`). `decided` is what THIS skill
    did: the payment-unit names Step 6 created, the rules Step 5 decided and its
    `form_field_rules_saved`, `expectActive: true` (Step 6.5 activates every ACE
    build opportunity), `expectTestUserInvited: true` (Step 7). The checks:

    | Check | Passes when | Blocks Phase 6? |
    |---|---|---|
    | `opportunity_readable` | the read returns the opportunity | yes |
    | `is_test` | `is_test === true` (undefined is unknown, not a pass) | no |
    | `activated` | not `active: false` AND an invite row exists — `active` alone is the create-side flag (ace#617); `invite_users/` rejects a non-active opportunity, so the row is the proof | yes |
    | `payment_units_match` | every Step 6 unit is listed by name and nothing else is (`name` is the only reliable column) | no |
    | `verification_rules_persisted` | Step 5's `form_field_rules_saved` ≥ the rules decided (Connect has no read surface for them) | no |
    | `test_user_invited` | `connect_list_flw_invites` has a row for the test user (`match !== null` — never `claimed`) | yes |

    Write the result to `products.connect.postcondition` (`ok`, `checked_at`,
    `failed[]`, `phase6_blockers[]`) in Step 10's patch (re-apply it if Step 10
    already ran), and add a `## Post-condition` table to
    `4-connect/connect-opp-setup.md`. **A failure does not fail the skill or
    re-run anything** — it names the end-state defect in the Phase 4 summary.
    A non-empty `phase6_blockers` is what Phase 6's pre-flight reads to refuse
    the walk with that reason instead of failing on the device. A read that
    errors is reported as unconfirmed, never as fine.

## Existing objects

- **Deliver units are keyed on the holding org's `CommCareApp` row** (ace#573). A second
  opportunity in the same holding org on the same released Deliver app cannot bind a payment unit
  to a deliver unit the first already holds. Step 6 is the gate; a fresh Deliver release is the fix.
- **The Learn `passing_score` lives on the shared `CommCareApp` row** (ace#1350). A create against
  an existing row discards the posted score, and the repair moves the gate for every opportunity
  wired to that Learn app (Step 4's `passing_score` check).
- **The holding org is create-time only** (ace#2919). Step 3 resolves it before the create; there
  is no repair.
- **There is no payment-unit update or delete atom.** A malformed unit is recreated in the Connect
  UI (Step 6).

## Archetypes

The PDD's `archetype:` field shapes verification + payment unit setup:

### `atomic-visit`
- **Verification:** one `form_field_rules` entry per clause of the PDD's
  payment predicate, keyed to the released CCZ's paths and stored values.
  GPS-fence / duplicate / catchment / photo-attachment enforcement is
  **not available** (ace#1013 — see Step 5); a required photo is normally
  enforced in the form itself (`required="true()"` +
  `appearance="acquire"`), so record it as CCZ-enforced rather than
  missing.
- **Payment:** typically one main payment unit per verified visit,
  optional bonus tier when Layer B passes (e.g. AI photo-quality check).
- **Soft flags** (Layer B/C from PDD): logged in
  `opportunity.md` but no Connect toggle; surfaced via
  `flw-data-review` skill in Phase 6.

### `longitudinal-visits`
- **Verification:** as `atomic-visit` — one `form_field_rules` entry per
  clause of the payment predicate — **plus** the longitudinal clause of
  the PDD's Layer A. Where a longitudinal fact is written onto the form
  by a case preload, it is a normal form-field rule and needs nothing
  special; where the predicate depends on case state that never reaches
  the submitted form, it cannot be a form-field rule. Record that
  explicitly in `opportunity.md § caveats` rather than dropping it
  silently — a dropped longitudinal clause is exactly how this archetype
  degrades back into `atomic-visit` (ace#1462).
- **Payment:** **one** payment unit for the whole arc — not one per
  phase. The sequence is expressed in `entity_id`, not in the number of
  payment units. (Contrast `multi-stage`, which really does take one PU
  per stage.) On a **componentized** programme the per-component PDD
  payment terms set the PU count instead — see § Componentized programmes
  below; this rule then governs only `entity_id` shape.
- **`entity_id` is the load-bearing field for this archetype.** It must
  carry entity + sequence position, per the PDD's
  `payment-unit-entity-id` decision — e.g.
  `concat(<case_id>, '-', <activity_code>)`. **Resolve every component to
  its own `calculate` bind in the released CCZ before writing the record
  — a component is a NODE NAME, not a semantics.** Three failure modes to
  check, and the third is invisible to a reader of the composite alone:
    1. the case id **alone** folds the whole arc onto one entity row;
    2. a `concat(username, today())`-style key silently reverts to
       cross-sectional grouping;
    3. **the sequence component is present but UNCLAMPED**, so the
       per-entity grouping the PDD mandates silently does not hold.
  None of the three is what stops a payment: a repeat key is paid again
  (ace#2512), so the PDD's per-entity cap binds only through the
  `payable_slot` `form_field_rules` row of Step 5 — record whether it was
  written.
  The record must state, per component, whether the PDD's sequence/clamp
  semantics are actually implemented — not merely that the component is
  present. On spark-facilitator/20260828-0703 the key read
  `concat(<case>/@case_id, '-', /data/fcap_step/step, '-',
  /data/meeting_summary/meeting_index, '-', <meeting_type>)`; the PDD's
  third component is `min(<meetings_on_current_step>, 3)`, and the clamp
  lives entirely inside `meeting_index`'s own bind. That app was correct —
  but an UNCLAMPED `meeting_index` produces a byte-identical composite,
  passes both failure modes above, and puts every 4th+ meeting per step
  on its own key (payable either way without the Step 5 `payable_slot`
  rule, ace#2512). Phase 6's `delivered >= 1` does not catch it
  either; it takes a 4th meeting on one step to surface. Phase 3's
  `entity-id-grain` now reports these as
  `resolvedThroughIntermediate` — read that list and resolve each entry
  (ace#1810).
- **Soft flags** (Layer B/C): progression and sequence-integrity checks
  have no Connect toggle; log them in `opportunity.md` and leave them to
  `flw-data-review` in Phase 6.

### `focus-group`
- **Verification:** same `form_field_rules`-only surface as above (venue
  GPS was never meaningful here, and is unavailable regardless). Enforce
  the attestation form's consent / session-held clauses as field rules;
  the required audio attachment is CCZ-enforced.
- **Payment:** one payment unit per **completed group session** — set
  `max_total` to the PDD's planned session count. Do NOT model per-
  participant payment; the unit is the session.

### `multi-stage`
- Configure verification + payment for **Stage 1 only**. Subsequent
  stages get their own opportunities (or their own payment-unit calls
  on the same opportunity, depending on the PDD's stage-overlap pattern).

### Componentized programmes (`products.mode: componentized`) — any archetype

`mode` is a second axis, orthogonal to `archetype:`. When
`run_state.phases.idea-to-design.products.mode` is `componentized`, the
programme was authored as separately-designed components, and **each
component PDD declares its own payment terms** — so payability is
heterogeneous by construction (ace#2163, observed on
`poverty-graduation/20260905-1345` and `poverty-graduation/20260908-0510`).
The archetype rules above still apply, but only to what they actually
govern:

- **The archetype rule governs `entity_id` SHAPE only — never the payment-
  unit COUNT.** `longitudinal-visits`' "one payment unit for the whole arc"
  is a rule about where the *sequence* is expressed (in `entity_id`, not in
  a PU per phase). It is not a PU budget, which is why it composes with a
  componentized programme instead of conflicting with it. Keep every
  `entity_id` requirement of the declared archetype (entity + sequence
  position, the three failure modes above).
- **Per-component PDD payment terms set the payment-unit count.** Read every
  component PDD (`products.components[].pdd_file_id`, plus the overview's
  Downstream Phase Guide where it addresses Phase 4) and build one payment
  unit per component the terms make payable, each with that component's own
  deliver unit(s), `amount`, `max_total` and `max_daily`. A component its PDD
  declares not separately payable (e.g. enrolment) gets **no** unit. Never
  put two independently-payable components' deliver units in one PU's
  `required_deliver_units`: that field requires ALL listed units before
  payment triggers, so one PU over a targeting survey and an asset delivery
  withholds the survey payment until the asset lands months later — a
  payment model that cannot pay as designed.
- **A payability that depends on an undeclared deployment choice is a
  deployment parameter, not a silent pick.** Example: a consumption-support
  component paid for in-person distribution but not for remote transfer,
  with the transfer method undeclared. Do not choose a reading here. Write
  one decision row (the open question — `review_ask:
  recommended-confirmation`, `owner: partner`, the method named as the
  parameter in `plain_question`, both readings in `options`) and make the
  Deliver app (Phase 3), this skill's payment units and Phase 5's knowledge
  base carry the SAME working reading — the one the Phase 3 Deliver app
  already built, read from `3-commcare/pdd-to-deliver-app_summary.md` — and
  cite that row. Three phases answering it three ways (paid DU in the app,
  no PU on Connect, "unpaid" in the bot) is the failure this rule exists to
  prevent.
- **Record the precedence.** Write a decisions row (`cs-payment-unit-shape`
  or similar) naming the archetype, the per-component PU set, and each
  component left unpaid with the PDD clause that makes it so.

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file` (always with `parentFolderId = phaseFolderId` — the `4-connect` folder ID, never a path string), `update_yaml_file`
- Connect (`ace-connect` MCP, 0.10.47+):
  - `connect_create_opportunity` — REST `POST /api/programs/<id>/opportunities/`
  - `connect_get_opportunity` — verify after create (HTML-driven read,
    Step 4 verify-after-create, and again at Step 6.6 for the four
    dashboard fields that are unreadable until activation — ace#1647)
  - `connect_set_verification_flags` — still HTML-driven (no REST yet)
  - `connect_create_payment_units` — REST `POST /api/opportunities/<id>/payment_units/` (atomic list)
  - `connect_list_payment_units` — verify after create (Step 6
    verify-after-create — this is the canary that catches PU
    malformation before it cascades to Phase 8 invites)
  - `connect_send_flw_invite` — REST `POST /api/opportunities/<id>/invite_users/`

## Mode Behavior
- **Auto:** Create + configure end-to-end, proceed
- **Review:** Present configuration spec for approval before calling
  `connect_create_opportunity` (the highest-stakes step — opp creation
  is harder to roll back than verification-flag adjustments)

## Dry-Run Behavior
When `--dry-run` is active:
- Write the full opportunity configuration spec (all fields that would
  be POSTed, plus the per-deliver-unit verification + payment-unit
  matrix) to `comms-log/dry-run-connect-opp-setup.md`
- Do not call any `connect_*` mutation atom
- State tracks as `dry-run-success`

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. Rule rows carry `scope` (`record` | `entity` | `worker` | `programme`) and `enforcement` (`enforced` | `by-design` | `gap`) — or omit both and the atom computes them; a per-worker limit is enforced by the payment unit's `max_daily` / `max_total`, never first by an app check, and a rule Connect refused is a `gap`, never `by-design`. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes load-bearing defaults to the per-run
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`. The bar criterion and
schema live in `skills/idea-to-pdd/SKILL.md § Decisions Log Convention`
(canonical authority). The list below catalogs decisions that commonly
qualify under the bar for this phase — a working template, not a
required set. The skill applies the bar criterion and emits whatever
rows meet it; the catalog is a teaching device that improves over time.

### Common load-bearing decisions for Phase 4

| ID | Question | Map to surface |
|---|---|---|
| `verification-flags` | Which verification flags (gps, photo, location toggle, duration thresholds) does the opportunity require? | PDD `Verification Mechanism`; downstream Phase 6/8 verification |
| `payment-unit-shape` | Per-visit fixed amount, tiered, milestone-gated, etc.? | Connect payment-unit creation; PDD `Payment Rate` |
| `opportunity-end-date` | When does the opportunity close? | PDD `Timeline` numeric; gates Phase 9 monitoring cadence |

**A close date claims a buffer only when there is one.** Write "including a two-week buffer" (in `plain`, `reasoning` or the value) only when the close date is LATER than the delivery end the run states (Phase 1's `opportunity-dates` row). When delivery ends on the close date, state the date plainly — any slack in the PDD's timeline arithmetic sits inside the delivery window, not after it. On `spark-facilitator/20261001-2208` the row read "closes on 26 February 2027, including a two-week buffer" next to "delivery from 2 November 2026 to 26 February 2027", copying "2 weeks buffer" from the PDD's timeline line. *Enforced:* `decisions_append_rows` refuses such a row with `UNSUPPORTED_BUFFER_CLAIM` (`lib/buffer-claim.ts`, `test/lib/buffer-claim.test.ts`). The same holds for the opportunity `description` text: never describe a buffer the dates do not leave.

The orchestrator's Phase Write-Back Verifier (`agents/ace-orchestrator.md`
§ Phase Write-Back Contract § Decisions log clause) enforces the
contract; the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: "4-connect"` and
`skill: "connect-opp-setup"`. Append via the `decisions_append_rows` MCP
atom (ace-decisions server) — do not hand-construct YAML and do not
write decisions.yaml via `update_yaml_file`. The atom validates each row
against `lib/decisions-schema.ts` v6 at the call boundary; misspelled
keys (`decision`, `rationale`, `default`, `options_considered`, `notes`)
are rejected before they touch Drive, and so is any row missing
`evidence_basis` (`stated` | `inferred` | `conflicting` — mandatory on
every new row; `conflict_signals` required when `conflicting`). Contract:
`skills/idea-to-pdd/SKILL.md § The evidence_basis contract`. (ace#1485)

Tool call:

```
decisions_append_rows({
  runFolderId: <run-folder file_id>,
  opportunity: <opp-slug>,
  run_id: <run-id>,
  rows: [
    {
      id: "cs-verification-flags",
      phase: "4-connect",
      skill: "connect-opp-setup",
      question: "which verification flags does this opportunity require",
      "ai-default": "duplicate=true, gps=false, catchment_areas=false",
      options: [
        "duplicate=true, gps=false, catchment_areas=false",
        "duplicate=true, gps=true, catchment_areas=false",
        "duplicate=true, gps=true, catchment_areas=true"
      ],
      source: "PDD §6/§8 verification mechanism",
      status: "ai-default",
      evidence_basis: "stated",
      plain: "Connect checks each visit for duplicates only; it does not check location.",
      value_set_by: "ace",
      reasoning: "Smoke opp — no GPS or photo capture in scope; duplicate guard only."
    },
    ...
  ]
})
```

### Every verification rule, latitude and ambiguity is a decision row (REQUIRED)

Step 8a's rule, `[ACE]` latitude and `[FIXED]` ambiguity rows go in the same
`decisions_append_rows` call as the catalogue rows above, and the row is the
only rendering — nothing else lists these calls. The catalogue alone left
"where is the PDD's duplicates rule enforced" unanswerable on the run page
(ace#2384).

| Row field | From the entry |
|---|---|
| `id` | `connect-rule-<slug>` / `connect-latitude-<slug>` / `connect-ambiguity-<slug>`; slug from the PDD § and the subject, so a re-run re-derives the same id |
| `phase`, `skill` | `4-connect`, `connect-opp-setup` |
| `question` | rule: "Where is the PDD verification rule '<quoted>' enforced?"; latitude / ambiguity: what the PDD left open or said two ways at that § |
| `ai-default` | rule: the enforcement-point category as one of the `options` below; latitude / ambiguity: the chosen value or resolution as a short label |
| `options` | rule: `Connect form_field_rules`, `Connect deliver_unit_checks`, `Connect submission window`, `Connect payment unit limit`, `CCZ constraint`, `Not configurable on Connect — applied elsewhere`, `Not configurable on Connect — not applied`; latitude / ambiguity: the chosen label plus each alternative weighed. A per-worker rule (a daily or total cap per worker) is `Connect payment unit limit`, never `CCZ constraint` — see Step 8a's scope paragraph |
| `scope`, `enforcement` | rule rows only: `record` \| `entity` \| `worker` \| `programme` and `enforced` \| `by-design` \| `gap` — set, or omit both for the write boundary's `classifyRule`. A rule Connect refused and nothing else holds is `gap`, never `by-design` |
| `plain_value` | the `ai-default` in words — REQUIRED whenever the `ai-default` is itself jargon (`skills/_decisions-review-fields.md`), which three rule labels are: `Connect form_field_rules` → `A Connect payment rule on the submitted form`, `Connect deliver_unit_checks` → `A Connect check on each delivery`, `CCZ constraint` → `A check in the app's form`. Name the record when you can (`A Connect payment rule on the meeting record`). If you omit it on those three labels the write boundary stamps the default wording (`RULE_ENFORCEMENT_PLAIN_VALUE`, `lib/decision-review.ts`; ace#2654); the other labels read plainly and need none |
| `plain`, `check_at`, `correct_looks_like` | `plain` REQUIRED (one line for a partner, the rule may be quoted); `check_at` the Connect setting or app form › field a reviewer opens; `correct_looks_like` what they see there when it is right |
| `source` | the entry's PDD §, naming the document |
| `evidence_basis` | `[ACE]` latitude → `inferred`; `[FIXED]` ambiguity → `conflicting`; rule → `stated` when the PDD itself names where it is enforced, `inferred` when ACE chose, `conflicting` for `Not configurable on Connect — not applied` (the PDD requires it and Connect cannot hold it) |
| `conflict_signals` | `conflicting` rows only, at least 2 entries, each cited |
| `value_set_by` | `ace` |
| `status` | `ai-default`, always |
| `reasoning` | why, plus — on a rule row — the precise placement and its evidence (Step 8a's list); an ambiguity left OPEN begins `OPEN —`; it ends `Spot-check: <the Connect setting, or the CCZ form › field>.` |

Keep the `Spot-check:` sentence at the end of `reasoning` even when you set
`check_at`: the write boundary derives `check_at` from it when a producer
omits the field. **The boundary checks it:**
`verify_phase_artifacts(phase='connect')` returns a `decisions` report
(`lib/build-phase-decisions.ts`) that fails when this skill wrote
`connect-opp-setup.md` but zero rows in `4-connect` under
`skill: connect-opp-setup`, and warns on live partner rows with no `plain`.

Worked example — one rule held on Connect's form-field rules (its jargon
`ai-default` carries `plain_value`), and two rules Connect cannot hold
(`connect_set_verification_flags` refuses `duplicate` / `gps` /
`gps_radius_meters`, ace#1013): one the app holds instead, and one nothing
holds (a known limitation, `enforcement: gap`):

```
decisions_append_rows({
  runFolderId: <run-folder file_id>,
  opportunity: <opp-slug>,
  run_id: <run-id>,
  rows: [
    {
      id: "connect-rule-survey-completed",
      phase: "4-connect",
      skill: "connect-opp-setup",
      question: "Where is the PDD verification rule 'only a completed survey is payable' enforced?",
      "ai-default": "Connect form_field_rules",
      plain_value: "A Connect payment rule on the survey record",
      options: [
        "Connect form_field_rules",
        "CCZ constraint",
        "Not configurable on Connect — applied elsewhere",
        "Not configurable on Connect — not applied"
      ],
      source: "Targeting PDD §9 [FIXED]",
      status: "ai-default",
      evidence_basis: "stated",
      scope: "record",
      enforcement: "enforced",
      plain: "\"only a completed survey is payable\" applies to each survey; Connect pays a survey only when the worker recorded it as completed.",
      check_at: "Connect › opportunity › verification rules",
      correct_looks_like: "A rule is listed that pays only surveys marked completed.",
      value_set_by: "ace",
      reasoning: "Connect form_field_rules: survey completed — form_field_rules_saved: 1. Spot-check: Connect › opportunity › verification rules."
    },
    {
      id: "connect-rule-one-survey-per-household",
      phase: "4-connect",
      skill: "connect-opp-setup",
      question: "Where is the PDD verification rule 'one payable survey per household' enforced?",
      "ai-default": "Not configurable on Connect — applied elsewhere",
      options: [
        "Connect form_field_rules",
        "CCZ constraint",
        "Not configurable on Connect — applied elsewhere",
        "Not configurable on Connect — not applied"
      ],
      source: "Targeting PDD §9 [FIXED]",
      status: "ai-default",
      evidence_basis: "conflicting",
      scope: "entity",
      enforcement: "enforced",
      plain: "\"one payable survey per household\" applies to each household; Connect cannot check it, so the app holds it by giving each household a single payable record.",
      check_at: "Deliver app › Targeting survey › registration",
      correct_looks_like: "A second survey of the same household is not counted as a new payable record.",
      conflict_signals: [
        "Targeting PDD §9 [FIXED]: one payable survey per household",
        "connect_set_verification_flags refuses duplicate (ace#1013): no Connect-side duplicate check"
      ],
      value_set_by: "ace",
      reasoning: "CCZ: Targeting survey / entity_id — payability-scoped key. Spot-check: Deliver app › Targeting survey › registration › entity_id."
    },
    {
      id: "connect-rule-gps-within-50m",
      phase: "4-connect",
      skill: "connect-opp-setup",
      question: "Where is the PDD verification rule 'visit GPS within 50 m of the household' enforced?",
      "ai-default": "Not configurable on Connect — not applied",
      options: [
        "Connect form_field_rules",
        "CCZ constraint",
        "Not configurable on Connect — applied elsewhere",
        "Not configurable on Connect — not applied"
      ],
      source: "Targeting PDD §9 [FIXED]",
      status: "ai-default",
      evidence_basis: "conflicting",
      scope: "record",
      enforcement: "gap",
      plain: "\"visit GPS within 50 m of the household\" is not checked anywhere in this build; Connect has no setting for it.",
      check_at: "Connect › opportunity › verification",
      correct_looks_like: "No location-distance check is listed.",
      conflict_signals: [
        "Targeting PDD §9 [FIXED]: visit GPS within 50 m of the household",
        "connect_set_verification_flags refuses gps / gps_radius_meters (ace#1013)"
      ],
      value_set_by: "ace",
      reasoning: "Not configurable on Connect — not applied anywhere in this build. Spot-check: Connect › opportunity › verification."
    }
  ]
})
```

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-19 | **`connect_list_opportunities` sends `filtered=1` (ace#3211).** Connect's opportunity list now applies default filters (status=Active, is_test=No) unless the request carries `filtered=1`; every ACE opportunity is `is_test`, so the listing came back `complete: true, total_count: 0` on orgs holding opportunities, blinding the Step 4 504 recovery, the `OPPORTUNITY_ALREADY_EXISTS` guard and Step 4a's Σ. Every page of the walk now carries it. *Enforced:* `test/mcp/connect/unit/list-opportunities-filtered.test.ts`. | ACE (#3211) |
| 2026-10-18 | `## Inputs` are parameters with resolvers. New § Operations on an existing opportunity names Step 5 (verification flags), Step 6 (payment units) and Step 4's passing-score read-back and repair as the one written source for those mechanics, runnable on an existing `opportunity_id`; `connect-opp-modify` points here instead of restating them. New § Existing objects. The stale Phase 8 `selected_llo` input row is gone (Phase 4 runs before Phase 8; the holding org comes from `connect_orgs`). | ACE (#3148 batch 3) |
| 2026-10-03 | **Build memo retired — decisions.yaml is the review artifact (schema v6).** Step 8 no longer ends `connect-opp-setup.md` with a memo section; new Step 8a records one rule row per PDD verification rule (`Where is the PDD verification rule '<rule>' enforced?`, with `plain`, `check_at`, and `scope` / `enforcement` set or computed by `classifyRule`), plus latitude and ambiguity rows, and a rule Connect refused is a rule row with `enforcement: gap` that `decisions_enrich` turns into a review ask; `products.connect.build_memo` is no longer written, and the Phase 4 boundary fails a written summary with zero rows under `skill: connect-opp-setup`. Contract: docs/decisions-contract.md. | ACE team |
| 2026-10-01 | **Step 8 names a per-worker rule's PER-WORKER enforcement point first (build-memo-eval, spark-facilitator/20260926-1800).** Both per-worker caps — "at most 1 payable meeting per CBF per day" and "total cap 21 per CBF" — were written `CCZ: … ; also Connect payment unit …` and recorded as `CCZ constraint` decisions, so the build memo told the reviewer the app enforced them. The app checks are keyed on the COMMUNITY case (the date check, the 7 × 3 per-step clamp) and cannot bound a worker across communities; only the payment unit's `max_daily` / `max_total` do. `Where applied` gains `Connect payment unit max_daily / max_total (per worker)`, the decision `options` gain `Connect payment unit limit`, and a scope paragraph says which goes first. *Enforced:* `lib/build-memo-compose.ts` `checkEnforcementScope` via `scripts/build-memo-compose.ts --check` (`test/lib/build-memo-compose.test.ts`, on that run's table and decision rows). | ACE team |
| 2026-10-04 | **Rule rows carry `plain_value` when their `ai-default` is jargon (ace#2654, spark-facilitator/20261004-1706).** The row contract mandated the closed `options` labels `Connect form_field_rules`, `Connect deliver_unit_checks` and `CCZ constraint` as `ai-default` but never mentioned `plain_value`, which the plain-language gate requires whenever `ai-default` is jargon — so 9 of that run's 12 compliant rule rows failed `decisions_enrich` and had to be re-emitted with `supersedes`. The table gains a `plain_value` row and the worked example a `Connect form_field_rules` row carrying it; the write boundary now stamps a default for those three labels (`RULE_ENFORCEMENT_PLAIN_VALUE`, `lib/decision-review.ts`). *Enforced:* `test/skills/connect-opp-setup-plain-value.test.ts` runs the real gate over every rule label and every worked-example row. | ACE team |
| 2026-10-01 | **Step 11: post-condition read-back (inline QA).** The atoms validate each call at the boundary, which catches a bad call but not a valid-but-wrong end state. Step 11 reads the live opportunity back (`connect_get_opportunity`, `connect_list_payment_units`, `connect_list_flw_invites`) and checks it against what the skill decided with `checkOppPostcondition` (`lib/connect-opp-postcondition.ts`): readable, `is_test`, activation PROVEN by an invite row (not the create-side `active` flag, ace#617), payment units by name, verification rules persisted, test user invited. Writes `products.connect.postcondition`; a non-empty `phase6_blockers` makes Phase 6 refuse the walk with the reason. Live on spark-facilitator/20260926-1800: 5 of 6 pass; `verification_rules_persisted` fails (2 decided, 0 saved — the self-managed refusal, ace#2419); no Phase 6 blocker. | ACE team |
| 2026-05-08 | Add `## Decisions Log` section: 3 anchor rows (verification-flags, payment-unit-shape, opportunity-end-date) + bar-criterion reference. Pairs with decisions-log PR #4 (Phase 3-10 writes). | ACE team (decisions-log PR #4) |
| 2026-05-10 | Move opp activation + ACE test-user invite from Phase 9 into Phase 4 (new Step 6.5 + rewritten Step 7). Closes the chicken-and-egg gap where Phase 6 `app-screenshot-capture` produced placeholder screenshots because the test user wasn't on the new opp yet — the opp couldn't be activated until Phase 9, but the test user couldn't be invited until activation. Phase 9 `llo-launch` now hits its idempotent skip-if-active path on every ACE-driven run; it still sends the real-LLO invite to the awarded LLO. Also: tighten Step 4 `is_test` from "defaults true server-side" to "set explicitly to true" — ACE is in dogfood mode and every opp it creates must be test-flagged so prod analytics, payment exports, and partner dashboards exclude these runs. | ACE team |
| 2026-06-01 | **Step 6.5: always attempt `/activate/`; treat only the "already active" error as the skip signal (jjackson/ace#624).** The managed-opp create endpoint returns a create-side `active: true` flag that is NOT the `/activate/` state transition `invite_users/` requires — so the old "read `active`, skip if true" pre-check skipped the only call that enables invites, and Step 7 failed. Calling `/activate/` on such an opp succeeds; it rejects only an opp that already completed the transition. Removed the pre-check; now call unconditionally and branch on the result, not the read-back flag. | ACE team |
| 2026-06-01 | **Step 6.5: verify activation via Step 7's invite, not the scraped `active` flag (closes jjackson/ace#617, and its #634 duplicate).** Dropped the post-activate `connect_get_opportunity` read-back check — that flag returns `true` on un-transitioned opps and can't distinguish a real `/activate/` from a no-op (the same create-side flag that motivated #624). The authoritative confirmation is `connect_send_flw_invite` in Step 7 succeeding: `invite_users/` hard-rejects a non-active opp, so a successful invite is the only proof the transition landed. | ACE team |
| 2026-08-12 | **Step 5 rewritten around what Connect's verification form actually has (dimagi-internal/ace#1013).** The step prescribed `gps` / `duplicate` / `catchment_areas` / `location` / `check_attachments`, all five of which were removed from the form — the atom accepts them, Django drops them, and it still returns `ok: true`, so a compliant agent produced an artifact claiming enforcement that never existed. Step 5 now leads with `form_field_rules` (the only server-side Layer A surface), requires reading `question_path` / `question_value` from the RELEASED CCZ rather than the PDD's prose (Nova flattens groups — a rule on a non-existent node enforces nothing and reports success), documents the 25-char `name` cap and the `duration_seconds`-is-really-minutes trap, and requires verifying via `form_field_rules_saved`. Archetype verification lines updated to match. Found live on spark-facilitator/20260810-0737. | ACE team |
| 2026-08-14 | **Step 5: `question_path` is a JSONPath into the HQ form-JSON doc, not an XForm XPath (dimagi-internal/ace#1301, `blocks-e2e`).** The step (and the atom's own schema) told agents to write `/data/<group>/<question>`. Connect evaluates the field as `jsonpath_ng.ext.parse(f"$.{question_path}")` against the whole forwarded document, so an XPath raises `JsonPathParserError` inside `clean_form_submission` — uncaught on the deliver path — and HQ's forward of every PAYABLE visit returns **HTTP 500**. The device is unaffected (CommCare shows "1 form sent to server!" because HQ *did* accept the submission), so the run looks green while Connect has no visit and the opportunity cannot pay. Observed live on `spark-facilitator/20260813-2126`: motech log 500 for the deliver form, 200 for every registration form on the same app; rewriting the rows to `form.meeting_basics.*` and requeueing the same payload moved Connect from `delivered: 0` to `delivered: 1 / approved: 1`. Correct spelling is `form.<group>.<question>`; `lib/connect-question-path.ts` now normalises `/data/a/b` → `form.a.b` on both incoming and replayed rows so a poisoned opportunity self-repairs. Also: `form_field_rules_saved` is no longer treated as sufficient evidence — it proves storage, not evaluability. | ACE team |
| 2026-08-14 | **Step 6 verify-after-create re-pointed at the CREATE RESPONSE (dimagi-internal/ace#1026, umbrella #1022).** The step mandated a `[BLOCKER]` when `connect_list_payment_units` returned an empty `required_deliver_units` — but that atom's HTML-scraped read path returns `[]` (and `description: ""`) unconditionally, so the halt condition was a constant of the read path, not a fact about stored state, and a compliant agent would halt every healthy run. Observed on `spark-facilitator/20260813-2126`: create response `required_deliver_units: [6617]`, list call `[]`, opp activated normally. The #843 check's intent is preserved — it now asserts against the create response (Connect's own post-persist serialization), with `connect_list_payment_units` demoted to corroboration on `id` / `payment_unit_uuid` / `name`. | ACE team |
| 2026-08-25 | **Step 4's verify-after-create no longer asserts four fields it cannot read; new Step 6.6 verifies them post-activation (dimagi-internal/ace#1647).** A never-activated opportunity renders only the edit-form half of `connect_get_opportunity`, so `start_date`, `total_budget`, `learn_app.cc_app_id` and `deliver_app.cc_app_id` were all absent at the moment Step 4 ran — four mandated comparisons passing vacuously on every run while the log read as verified. Same shape as ace#1449 (`passing_score` compared against a field the surface does not render). Step 4 now splits readable-here (`name`, `short_description`, `description`, `end_date`, `is_test`) from deferred, and requires an absent field to be recorded `unreadable-at-this-point` rather than counted as a match; Step 6.6 re-reads after `/activate/` and `[BLOCKER]`s on disagreement OR on continued absence. Verified live on `bednet-check-2-visit/20260825-1310` Phase 4 (same opp, same atom, either side of activation). Upstream half stays on #1637. | ACE team |
| 2026-08-25 | **Step 6: `id` dropped from the `connect_list_payment_units` corroboration allowlist (dimagi-internal/ace#1642).** The listing's first column is the row `#`, so the PU that `connect_create_payment_units` returned as `id: 2495` reads back as `id: 1` — a per-opp display index, not the server PK, and passing it where a server id is required reproduces the `du.id` vs `du.server_id` rejection. Corroboration is now `payment_unit_uuid` / `name` only, with `payment_unit_uuid` named as the durable identifier. Atom description in `mcp/connect-server.ts` corrected to match. Observed on `bednet-check-2-visit/20260825-1310` Phase 4. | ACE team |
| 2026-05-10 | State consolidation PR a: retire `connect-state.yaml`; emit a single `run_state.yaml.phases.connect-setup.products.connect` block at end of Step 10. Step 7 holds invite metadata in memory rather than writing immediately. (Initial implementation dual-wrote to `opp.yaml.connect`; corrected on 2026-05-11 — runs are now independent. `opp.yaml.connect.program` is durable cross-run state written by `connect-program-setup`; `opp.yaml.connect.opportunity` / `ace_test_user` are no longer written here.) See `docs/superpowers/specs/2026-05-10-state-consolidation.md`. | ACE team |
| 2026-09-08 | **Step 4's single-active-opp block stops asserting an enforcement and a deactivation it cannot support (dimagi-internal/ace#2290).** It read "Connect enforces one active managed opportunity per accepted `ProgramApplication`" and mandated a WARN reading "will deactivate prior active opp …", both generalized from a single 2026-05-06 observation (leep-paint-collection, jjackson/ace#106 finding 11). Counter-observed on `bednet-check-2-visit/20260908-1544`: **ten** opps on program `efb8af66-fbfd-488f-bf99-66f864cea68b` concurrently `active: true`, and a direct post-create re-read of `5fdee3b8-e859-4aa7-a4be-8ad6f727917a` returned `active: true` / `dashboard_read: "ok"` — no deactivation, so the WARN that run emitted was a prediction written into the artifact as fact. Both observations are now recorded as observations; the accept-application short-circuit on a self-managed org is named as the leading HYPOTHESIS with `upstream-regression-triage` against `dimagi/commcare-connect` as the way to settle it. The scan and the `hydrate: true` read are unchanged — the WARN is now singular-to-N, reports the count plus ids, drops the "close prior opps first" remedy (it contradicts per-run opp accumulation by design), and says "MAY deactivate — unverified" instead of predicting. Not CI-gateable: it is a claim about another system's behaviour. | ACE team |
| 2026-09-06 | **Stop routing concerns to a gate brief that does not exist (dimagi-internal/ace#1884).** 0.13.116 removed the per-skill gate-brief file class and the ace#1880 sweep removed the remaining `*.md` PATHS, but prose directives naming the gate brief as a DESTINATION survived in 15 files — a concern "surfaced in the gate brief" is surfaced nowhere. Repointed at the verdict YAML's `auto_surfaced` block, which is what the orchestrator actually renders the pause summary from. Gated by the new destination check in `test/skills/gate-brief-removal-complete.test.ts`. | ACE team |
| 2026-09-11 | **Step 8 ends `connect-opp-setup.md` with the Phase 4 half of the run's build memo (ace#2371).** Every poverty-graduation PDD names a build memo as the review artifact, and the Connect-side skills mentioned it zero times — so where a PDD verification rule was actually applied (on Connect, in the CCZ, or nowhere) was recorded nowhere a reviewer would look. That mattered concretely because `connect_set_verification_flags` refuses `duplicate` / `gps` / `gps_radius_meters` (ace#1013), leaving a Targeting PDD's duplicates rule with no Connect home. The new section maps one row per rule across the WHOLE PDD set (component PDDs included) to a closed `Where applied` vocabulary in which "Not configurable on Connect" is a required statement, not an omission, plus opportunity-config `[ACE]` latitudes and `[FIXED]` ambiguities. `skills/build-memo` collates it verbatim; `products.connect.build_memo` is the one `products.connect` key this skill does not write. *Enforced:* `test/skills/build-memo-contract.test.ts`. | ACE team |
| 2026-09-11 | **Every Step 8 build-memo entry — each verification rule, `[ACE]` latitude and `[FIXED]` ambiguity — is also a `decisions.yaml` row (ace#2384).** The mapping of "where is each PDD verification rule enforced" existed only as memo prose, so a reviewer could read it but not answer it on the run page. Rule rows draw `ai-default` from the closed `Where applied` categories; the specific form/field or Connect setting goes in `reasoning` as `Spot-check:` because ace-web drops unknown keys. The Phase 4 boundary fails a section with entries and no rows. *Enforced:* `lib/build-phase-decisions.ts` via `verify_phase_artifacts`, `test/skills/build-phase-decision-rows.test.ts`. | ACE team |

<!-- connect_int_id is read directly from the connect_create_opportunity response (ConnectProd integer id); the old post-create labs_context lookup was removed in the jjackson/ace#686 follow-up (the int was always in the create response). -->
| 2026-09-16 | **Phase 4 creates ACE's build/QA opportunity, never the LLO's — the network-manager / program-manager model (operator decision 2026-09-16).** Step 3a's third branch said of a distinct `target_organization_slug`: *"Phase 9 already handled the round-trip; skip this sub-step."* **That precondition is impossible** — `connect-setup` is Phase 4 and `llo-onboarding` is Phase 9, so no invite has been sent and none accepted when this skill runs; the create it waved through could only reject with `Organization must have an accepted application for this program`. Worse, had it succeeded the opportunity would be stranded: `target_organization_slug` is create-time only and `connect_update_opportunity` carries no org field, so it could never be handed to the LLO. That branch now HALTs with the remedy. Step 3 states the model: PM creates the program → invites the NM → **NM accepts** → PM creates the NM's opportunity (`llo-onboarding` § 2b, on freshly-copied `cc_app_id`s). Two opportunities is structural, not a workaround — it falls out of the ace#573 `DeliverUnit.payment_unit` FK constraint. | ACE team |
| 2026-09-26 | **Phase 4 runs the real PM→NM flow when `connect_orgs.nm_org` is configured (operator decision, Jon).** Step 3 was rewritten: 3.0 resolves `pm_org` / `holding_org` via `phase4Orgs()` (`lib/connect-orgs.ts`); 3a invites + accepts the HOLDING org (the NM org in `pm-nm` mode) and captures `program_application_id` from the invite POST; Step 4 passes `target_organization_slug = holding_org` and asserts the echo; Step 5 sets verification rules at `pm_org`, which Connect now serves because request org ≠ holding org (ace#2419 — a self-managed opp can never carry them; observed spark-facilitator/20260925-1536). Proved live 2026-09-26 on program `777f9060-8f26-43bb-aad1-b8f1d7df22db` / opportunity `7bfcb845-015c-416a-a200-9795c68dfc55` (NM-held; rule saved at the PM-org URL, refused at the NM-org URL). Step 10 records `pm_org_slug` + `holding_org_slug` (+ legacy `organization_slug`). The partner LLO's opportunity is still created in Phase 9. Self-managed behaviour is unchanged when `nm_org` is unset. | ACE team |
| 2026-10-15 | **Step 7: a `match === null` read-back now waits, re-reads and re-sends ONCE before it WARNs (dimagi-internal/ace#2946).** On `smallholder-seasonal/20261014-0859` (opp `30605010-4be8-49e3-954c-deeb0b4ad8d6`) the invite sent right after `/activate/` returned `queued` but created no row across three reads; one identical re-send produced both rows, and the requester row's `invited_date` equalled the re-send time — so the first send created nothing, it was not lag. The step previously went straight to WARN, so a run following it recorded `invite_row_present: false` and a Phase 6 blocker that one idempotent re-send would have cleared. Now: wait ~60 s → re-read → re-send once → re-read → only then `invite_row_present: false` + WARN; both sends are logged to `comms-log/observations.md`. *Enforced:* `test/skills/connect-opp-setup-invite-resend.test.ts`. | ACE team |
| 2026-10-16 | **Step 4.0: a re-dispatched Phase 4 finishes the opportunity it already created instead of minting a second (dimagi-internal/ace#2083 fix (1)).** A create with no payment unit yet is `setup_incomplete` in Connect (`is_setup_complete` needs one), and the skill had no resume path while `products.connect` landed only at Step 10 — so a dispatch killed between Steps 4 and 6 left an opportunity no read can open, and the re-dispatch created another. There is no delete API; Connect's `delete_stale_opportunities` purges visit-free opportunities only at six months, and each orphan costs one `EXPECTED_OPP_BUDGET` in every program-ceiling sum (11 of 71 `ai-demo-space` rows, 2026-09-06). Now Step 4.0 lists by run id and decides create / adopt / halt with `planOpportunityCreate` (`lib/connect-opp-resume.ts`), the id is recorded the moment the create returns (ace#2412), and `connect_create_opportunity` itself refuses an `is_test` create whose exact name exists (`OPPORTUNITY_ALREADY_EXISTS`) or whose listing is incomplete (`OPPORTUNITY_EXISTENCE_UNKNOWN`). *Enforced:* `test/lib/connect-opp-resume.test.ts`, `test/mcp/connect/unit/opportunity-duplicate-guard.test.ts`. | ACE team |
