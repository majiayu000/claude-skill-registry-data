---
name: app-release
description: >
  Build and release Learn and Deliver apps on CommCare HQ so Connect can read their form schema
  and deliver units. Needs the HQ app ids.
disable-model-invocation: false
---

# App Release

**Run workspace:** when the dispatch carries a `run_workspace:` block, its values replace the `.env` ones this skill names — `ACE_HQ_DOMAIN` → `run_workspace.hq_domain` — and a partner workspace never falls back to `.env`. Contract: [`skills/_run-workspace.md`](../_run-workspace.md).

Make a new build of each app on CCHQ and mark it as **Released**, so Connect
can read its form schema and surface deliver units to the opportunity.

## Inputs

The skill releases any HQ app, whether ACE built it this run or it is a live program's app.
Pass the values explicitly. Inside `/ace:run` each one defaults to the run's Phase 3 artifacts.

| Parameter | Used for | Resolver |
|---|---|---|
| `hq_domain` | the project space the apps live in | explicit argument; default: `run_workspace.hq_domain`, else `app-deploy_summary.md` frontmatter `hq_domain` |
| `learn_app_id` / `deliver_app_id` | the 32-char HQ app ids to build + release (either or both) | explicit argument; default: `3-commcare/app-deploy_summary.md` frontmatter |
| `learn_nova_app_id` / `deliver_nova_app_id` | Step 3a drift check and the Step 4a build-rejection fix loop | explicit argument; default: `3-commcare/pdd-to-{learn,deliver}-app_summary.md` frontmatter `nova_app_id`. Omit for an app with no Nova source: Step 3a then records `conclusive: false` and Step 4a can only surface the rejection |
| `deployed_at` | Step 3a `deployedAt` signal | explicit argument; default: `app-deploy_summary.md` frontmatter `uploaded_at`; leave unset when unknown (the classifier handles an omitted signal, never a guessed one) |
| `opportunity_id` | an EXISTING opportunity wired to these apps, whose deliver units Step 7 re-syncs | explicit argument; default: run_state `phases.connect-setup.products.opportunity.id` when that phase has run; absent on a first build |
| `summary_folder_id` | where the release summary is written | default: the run's `3-commcare/` folder; outside a run, the program project's Drive folder (`skills/partner-on-connect-program`) |

## Existing objects

Releasing a new build of an app that a **live** opportunity already uses changes what
working FLWs run, and some of what it touches is shared:

- **Workers get the new build.** A released build is what CommCare offers on the next app
  update. Release only content you mean every worker on every opportunity wired to this app
  to receive.
- **Deliver units are keyed per app and shared within the holding org** (ace#573). Re-releasing
  the same `deliver_app_id` re-uses the existing `DeliverUnit` rows: it cannot give you a
  fresh payment unit. A new deliver form shows up only after the deliver-unit sync in Step 7.
- **The Learn passing score lives on the shared `CommCareApp` row** (ace#1350), not on the
  opportunity. A release does not change it, but every opportunity on this Learn app reads the
  same score, so don't "fix" it per opportunity.
- **Whether a live opportunity picks up a re-released build without a manual sync is
  unverified.** Read back with `connect_list_deliver_units` after Step 7 rather than assuming.
  See `playbook/integrations/connect-api.md`.

## Products

- `3-commcare/app-release_summary.md` — released build IDs + version numbers per app. Outside a run the same file goes into `summary_folder_id` (§ Inputs).

  **Frontmatter contract (ace#1439).** `app-release-eval § both_apps_released`
  reads these keys, so they are declared here rather than left to whatever the
  run happened to write. This file is the **sole owner of released build
  state** — `is_released`, `build_id` and `version` live HERE and nowhere
  else, and every reader (`app-release-eval`, `app-release-qa`,
  `llo-launch`'s app-verdict-freshness gate) reads them from here:

  ```yaml
  apps:
    learn_app:   { hq_app_id: <id>, build_id: <id>, version: <n>, is_released: true, released_at: <iso> }
    deliver_app: { hq_app_id: <id>, build_id: <id>, version: <n>, is_released: true, released_at: <iso> }
  # Step 3a's pre-build drift decision, per app (ace#1643). Present on
  # every run — `drift: false` is a RESULT and must be recorded, because a
  # skip that is not written down is indistinguishable from a check that
  # never ran.
  drift_check:
    learn:   { drift: <bool>, conclusive: <bool>, action: <build-directly|reupload-reapply-settings-then-build>, reupload: <bool>, settings_reapplied: [...], reasons: [...] }
    deliver: { drift: <bool>, conclusive: <bool>, action: <...>, reupload: <bool>, settings_reapplied: [...], reasons: [...] }
  ```

  `is_released` and `version` mirror what HQ returns from the release POST
  (`{"is_released": true, "latest_released_version": <n>}` — note HQ's field is
  `latest_released_version`; the artifact key is `version`, and conflating the
  two is what put a phantom key in the rubric for four months).

## Why this skill exists

Nova uploads apps to CCHQ as a **draft** only; Connect surfaces deliver
units only from a **released build**. This skill makes the versioned build
and releases it. For the full rationale, see reference.md § Why this skill
exists.

## Prerequisites

The CCHQ user backing `ACE_HQ_USERNAME` (`ace@dimagi-ai.com`) **must
have a role with `edit_apps` permission** on the target project space.
The standard `Admin` role on connect-ace-prod includes this. Verify
once via the Web Users page (`/a/<domain>/settings/users/`) if you hit
auth-shaped errors. Note the CCHQ `Sorry, you don't have permission to
do this action!` banner is a generic Knockout error fallback, NOT a
literal permission verdict — see § Failure Modes before treating it as
diagnostic.

## Endpoints (verified 2026-04-29)

CCHQ's URL patterns are internal UI routes, not public APIs. For how they
were discovered, see reference.md § How the endpoints were discovered.

```
# Step 1 — Make a versioned build (creates a "build" doc; sets built_on)
GET  /a/<domain>/apps/view/<app_id>/releases/             # GET first to refresh csrftoken
POST /a/<domain>/apps/save/<app_id>/                       # empty body suffices
  → 200 { "saved_app": { "_id": "<build_id>", ... } }      # _id IS the new build_id

# Step 2 — Release that build (toggles is_released=true)
POST /a/<domain>/apps/view/<app_id>/releases/release/<build_id>/
  Body: ajax=true&is_released=true
  → 200 { "is_released": true, "latest_released_version": <n> }
```

CSRF: extract from the `csrftoken` cookie set by the GET in step 1; pass
it as `X-CSRFToken` header on both POSTs.

Verify via the read-only HQ API (no UI session needed):
```
GET /a/<domain>/api/v0.5/application/<build_id>/
Authorization: ApiKey <ACE_HQ_USERNAME>:<ACE_HQ_API_KEY>
→ { "is_released": true, "version": <n>, "built_on": "<iso>" }
```

If the URL pattern shifts in a future CCHQ release, use the probe
procedure below to rediscover.

### Probe procedure (only when the verified URLs above fail)
1. Open `/a/<domain>/apps/view/<app_id>/releases/` in `/browse` with the
   CCHQ cookies imported from `~/.ace/connect-session.json`.
2. Inject an XHR/fetch interceptor (`window._cap = []; XMLHttpRequest…`).
3. Click `Make New Version`. Capture the POST URL + body.
4. Once a build appears, click the `Released` toggle (CSS-styled button,
   bound to `$root.toggleRelease`). Capture that POST URL + body.

## Process

1. **Resolve the app ids** per § Inputs. Explicit arguments win.
   - Inside a run, `ACE/<opp-name>/runs/<run-id>/3-commcare/app-deploy_summary.md` frontmatter
     has `learn_app_id` and `deliver_app_id` (the 32-char HQ app IDs Nova wrote there), plus
     `hq_domain` (typically `connect-ace-prod`) and `hq_base_url`.
   - Outside a run, take them from the caller, or from the program context doc's HQ apps row.
     Confirm each id exists in `hq_domain` (`commcare_list_apps`) before building, so a stale
     id fails here and not mid-release.

2. **Establish session.** Use the `~/.ace/connect-session.json` cookie jar
   (Connect's OAuth-via-CCHQ flow leaves valid CCHQ cookies). If
   expired, run `/ace:connect-login` to refresh.

3. **Pre-flight: Connect-marker coverage must be clean.** Releasing an
   app whose forms lack Connect markers succeeds at the build level, but the
   opportunity then gets stuck with empty deliver units (Phase 4 Step 2 on a
   build, a silently unpayable form on a live program). This gate is not
   optional, and it is a check this skill RUNS, never a file it trusts blindly:
   - **In a run where Phase 3 Step 1.5 already ran:** read
     `3-commcare/app-connect-coverage_{learn,deliver}.md`. `status: clean`
     passes. `blocked` halts.
   - **Otherwise (no coverage verdict for this app, or outside a run):** run
     `app-connect-coverage` now against each app's Nova app id. Its auto-fix
     edits Nova, so any fix it makes leaves the HQ draft stale. Step 3a then
     reports drift and forces the re-upload before the build. With no Nova app
     id, check the HQ draft's form XML for the markers instead
     (`commcare_get_form_source`). If any are missing, halt: there is no
     source to fix them in.
   - Either way, `blocked` or missing markers halt. Never build past them.

3a. **Pre-build drift check — is the HQ draft still the Nova app? (ace#1643)**

    `commcare_make_build` versions the **CCHQ draft**. It does not pull
    from Nova. So any Nova edit made after `app-deploy` is absent from
    the released CCZ and the release still reports success. Run this
    check per app, BEFORE Step 4.

    **Step 6's marker verification cannot cover this.** The markers were
    correct on the stale build too — it was a well-formed build of the
    wrong content. **Marker integrity is not a proxy for content
    integrity**, which is why this check is content-level and sits
    before the build. (`app-release-eval`, ace#1643.)

    1. **Gather the signals** (all cheap, all read-only):

       | Signal | Source |
       |---|---|
       | `deployedAt` | `deployed_at` per § Inputs (in a run: `3-commcare/app-deploy_summary.md` frontmatter `uploaded_at`) |
       | `novaEditedSinceDeploy` | THIS RUN's own knowledge — did any step dispatch `/nova:edit`, an eval-driven repair, or a Step 4a build-rejection fix on this app AFTER `app-deploy`? `true` / `false`; leave unset if genuinely unknown (the usual case outside a run — the content counts below still decide) |
       | `novaFormCount` | `get_app({app_id: <nova_app_id>})` — one call per app |
       | `novaVisibleFieldCount` | Same `get_app` response, normalized to the HQ walk's basis: **every non-`hidden` LEAF, plus every `group`/`repeat` whose label is NON-EMPTY**. Use `countNovaVisibleFields` from `lib/app-release-drift.ts` — don't do this arithmetic by hand. Two corrections, each found by a live mismatch: the walk emits no hidden fields (`user_score`, `qN_score`, `case_name`, `entity_key`, `entity_label`, … — every ACE app has them, ace#1789), and it emits a container only when that container rendered a `<label>`, so an EMPTY-labelled group compiles to a self-closing `<group ref="…"/>` and contributes nothing while Nova still counts 1 (ace#1807). **The exclusion is on the LABEL, not on "all children are hidden"** — the compiled CCZ emits the group element either way; ace#1807's original wording said otherwise and was refuted against `test/fixtures/ccz/spark-facilitator-meeting-record.xml` |
       | `hqDraftFormCount` / `hqDraftVisibleFieldCount` | `run-form-walk.ts <hq_domain> <hq_app_id> --draft-only --with-fields --out-scratch` (same invocation `app-hq-settings § Step 2` documents; check `fields_available: true` before trusting the field count) — already visible-only, nothing to exclude on this side |
       | `novaEditedAt` | optional — pass only if the Nova surface actually exposes a last-edited timestamp. Do NOT invent one; an omitted signal is handled, a guessed one is not |

    2. **Classify** with `classifyAppDrift` from `lib/app-release-drift.ts`
       (a pure function, unit-tested in `test/lib/app-release-drift.test.ts`
       — the decision is not left to prose). It returns
       `{drift, action, conclusive, reasons}`.

       Two properties of the classifier are deliberate and must not be
       "optimised" away:

       - **Matching counts never clear the build-directly branch.** Of the
         three drifting Deliver edits in the ace#1643 repro, only
         `gps_lat`/`gps_lon` moved a count; the extended consent paragraph
         and the `area_ref` constraint moved none. Counts detect drift;
         they cannot prove its absence. Clearing the skip needs an
         ORDERING fact.
       - **Unresolved signals default to `drift: true`** (with
         `conclusive: false`). A needless re-upload costs one idempotent
         call; a skipped one ships the wrong app and reports success.
       - **A field-count mismatch is a SOFT signal; a form-count mismatch
         is not (ace#1789).** A hidden field never creates a new form, so a
         form-count mismatch always forces drift. A field-count mismatch
         can be a basis artifact (see `novaVisibleFieldCount` above), so
         once an ORDERING fact is clear it is downgraded to corroboration
         rather than forcing drift — it still forces drift when no
         ordering fact resolves the question, matching the conservative
         default above.

    3. **On `action: 'reupload-reapply-settings-then-build'` — an ordered
       TRIPLE, and the middle item is the one a naive fix omits:**

       1. `/nova:upload_to_hq <nova_app_id> <ACE_HQ_DOMAIN>` — updates the
          HQ app in place (`hq_app_action: updated`, id unchanged,
          `left_behind: []`). Honour `app-deploy § HQ-id stability` if the
          id DID change.
       2. **Re-apply `app-hq-settings` and re-verify from
          `GET /apps/source/`.** The re-upload REVERTS two of the four
          settings that skill applies — measured on
          hh-poverty-targeting/20260824-1404 (ace#1643):

          | Setting | Survives a re-upload? |
          |---|---|
          | `appearance="acquire"` on Deliver image fields | **no — wiped** |
          | per-module `display_style: grid` | **no — reverted to list** |
          | app-level `use_grid_menus` | yes |
          | app-level `grid_form_menus` | yes |

          `app-release-qa` Step 2.8 BLOCKER-gates all three grid fields
          and the `acquire` appearance, so re-uploading WITHOUT this
          re-apply converts a silent stale-content bug into a hard Phase 3
          halt.

          After a re-upload the form uids are the 40-hex SHA-1 variant, not
          32-hex. `commcare_get_form_source` / `commcare_patch_xform` and
          `run-form-walk --draft-only` all accept both widths (ace#1644,
          `lib/hq-unique-id.ts`) — a `unique_id` validation error or a
          `resolved 0 forms` here means the plugin predates that fix, and
          **MCP code needs a full Claude Code restart, not `/reload-plugins`**.
       3. Only then proceed to Step 4.

    4. **On `action: 'build-directly'`**, go straight to Step 4 — and say
       so explicitly in the summary. A skip that is not recorded is
       indistinguishable from a check that never ran.

    5. **Record the decision** in `3-commcare/app-release_summary.md`
       frontmatter, per app, so it is auditable:

       ```yaml
       drift_check:
         learn:   { drift: false, conclusive: true,  action: build-directly, reupload: false, settings_reapplied: [], reasons: [...] }
         deliver: { drift: true,  conclusive: true,  action: reupload-reapply-settings-then-build, reupload: true, settings_reapplied: [camera_only_acquire, module_display_style_grid], reasons: [...] }
       ```

       `reasons` is `AppDriftDecision.reasons` verbatim. When
       `conclusive: false`, the body MUST say the verdict was a default
       taken on missing signals, not an observation.

4. **For each app (learn + deliver):** run the verified Step 1 + Step 2
   POSTs above. Each call is idempotent on the build side: re-POSTing
   `/apps/save/` after a release creates a new build at the next version,
   leaving prior builds released. So safe to re-run.

4a. **If `commcare_make_build` throws `BuildRejectedError` — auto-fix
    loop with the Nova architect.** This loop fixes the bad XForm at the
    source (the Nova app) and retries. For origin, see reference.md
    § BuildRejectedError auto-fix loop.

    The MCP atom now returns
    `{error: 'build_rejected', app_id, error_text, error_html, retryable: false}`
    with `error_text` already HTML-stripped (see
    `mcp/connect/backends/commcare.ts § BuildRejectedError`). Catch
    it; do **not** treat `retryable: false` as "give up." That field
    means "the same args won't succeed against this app id" — the loop
    fixes the app first, then retries.

    **Loop invariants (max 3 iterations per app):**

    1. **Parse `error_text` into a structured form locator.** CCHQ's
       canonical shape is:

           Cannot make new version
           "<form-name>" Form in the "<menu-name>" Menu
           Error parsing XML: <parser-message>, line <N>, column <M>
           Error in form "<form-name> [<lang>]": <repeat>

       Extract: `form_name`, `menu_name`, `line`, `col`,
       `parser_message`. The form-name is the human label (e.g. "Unique
       ID check"), not the form_unique_id; it's all you have at this
       point because the CCZ never built.

    2. **Map `form_name` → Nova `form_id`.** Resolve the app's
       `nova_app_id` per § Inputs (in a run:
       `3-commcare/pdd-to-{learn,deliver}-app_summary.md` frontmatter
       `nova_app_id`; with none, skip to step 6 and surface the rejection —
       there is no source to fix). Call
       `nova__get_app({app_id})` for the live structure and walk to
       the form whose name matches `form_name`. On ambiguity (two
       forms with the same name in different modules), use
       `menu_name` to disambiguate. If still ambiguous, halt the loop
       and surface the ambiguity in `auto_surfaced` — operator decides.

    3. **Dispatch the Nova architect** via `/nova:edit <nova_app_id>`
       with a brief that names the form, the line/col, the parser
       message, and the most-likely fix class. Template:

           Form "<form_name>" in module "<menu_name>" produces invalid
           XForm XML. CCHQ rejected `make_build` with:

             <parser_message>
             at line <N>, column <M>

           The most common cause is unencoded `<`/`>`/`&`/`"` in label,
           option, hint, or constraint-message text — Nova's emitter
           does not entity-encode these (tracked at
           voidcraft-labs/nova-plugin issue #15). Inspect every label,
           option, hint, and constraint_message in this form via
           `get_form` + the per-field `edit_field` getter. For any
           string that contains a literal `<`, `>`, `&`, or `"`,
           replace with words ("three letters") or backticks
           (`three letters`) via `update_form` / `edit_field`, then
           SAVE the checkpoint with `save_work` and confirm it answered
           `saved: true` — only saved changes are uploaded, and the
           save is where Nova validates the whole candidate. If you
           cannot save, report the work id instead of claiming a fix.

    4. **Re-upload via `/nova:upload_to_hq <nova_app_id> <ACE_HQ_DOMAIN>`**
       — only once the edit's return names a saved checkpoint. `/nova:edit`
       (plugin v2) works in private work (voidcraft-labs/commcare-nova#693):
       if it returns a `work_id` with pending changes, the fix is NOT in the
       saved app and re-uploading changes nothing — treat that iteration as
       a failed fix, not a retry of the build.
       Pass the target project space explicitly (same as `app-deploy`,
       Nova plugin voidcraft-labs/nova-plugin#12). Nova **updates the
       HQ app in place**: the id is unchanged and `hq_app_action` comes
       back `updated` (verified live 2026-08-18 — see
       `playbook/integrations/nova-integration.md § Uploading to HQ
       updates in place`). So there is normally no new id to chase and
       no orphan left behind.

       Read `hq_app_action` and `deployment.left_behind` anyway rather
       than assuming. If the id DID change (`left_behind` non-empty, or
       `hq_app_action: created` for an app already uploaded — reachable
       when the linked HQ app was deleted on HQ and the call refused
       with `remote_app_missing`), update the in-memory app reference to
       the new `hq_app_id`, record both ids in
       `3-commcare/app-release_summary.md.frontmatter.hq_app_id_history`
       so Phase 4's downstream wiring (which reads the LATEST id) lines
       up, and surface the change loudly.

    5. **Retry `commcare_make_build` against the current HQ app id** (the
       same one, unless step 4 reported it changed). If
       it still throws `BuildRejectedError`, parse the new
       `error_text` (it may name a different form / line / cause) and
       loop. **Cap at 3 total attempts per app.**

    6. **On exhaustion (3 failed attempts),** surface the FINAL
       `BuildRejectedError` to the orchestrator as a `[BLOCKER]` in
       this skill's returned summary with: every iteration's
       `error_text`, every Nova edit dispatched, the final
       `hq_app_id`, the operator-facing remediation (manual CCHQ
       form-designer edit on the final orphan id, OR wait for Nova
       upstream fix). Phase 3 halts. Do not silently downgrade to
       success.

    **Why bounded (3 attempts).** For the rationale, see reference.md
    § Why the BuildRejectedError loop is bounded at 3.

    **Dispatch-depth note.** `/nova:edit` runs the Nova architect via
    `Agent`, which costs a level of dispatch depth. `app-release` is
    invoked from Phase 3 (`commcare-setup`), a subagent, so the architect
    lands at depth 2. Moving `app-release` under more layers pushes it down;
    past the budget the `Agent` tool is withheld and the loop degrades
    silently instead of failing. `test/lib/agent-depth.test.ts` holds
    the number. Keep the
    invariant.

5. **Verify both apps show `is_released: true`** via the API.

6. **Verify the released CCZ via `commcare_download_ccz` projection.**
   Call `commcare_download_ccz(domain, app_id, build_id, include_multimedia=false)`
   and read all three gates on the response:

   - **`projected_connect_state.collision_count`** — MUST be `0`.
     This is a deterministic projection of what Connect's HQ→Connect
     sync will produce: every `<learn:deliver>` / `<learn:module>` /
     `<learn:task>` / `<learn:assessment>` element across every form,
     deduplicated by `(app, slug)` exactly like
     `commcare-connect/opportunity/tasks.py:sync_learn_modules_and_deliver_units`.
     A non-zero count means N forms emit the same `id` attribute and
     Connect will silently collapse them, leaving the non-first forms
     unwired to any payment_unit and unpaid in production.
   - **Per-type record counts** (`projected_connect_state.deliver_units.length`
     etc.) MUST be > 0 for the app type — Learn apps have ≥ 1 module,
     Deliver apps have ≥ 1 deliver_unit. Zero means the form lacks
     Connect metadata at the source (Nova didn't generate it).
   - **`projected_connect_state.oversized_slugs`** — every per-type array
     MUST be empty (`oversized_slugs.deliver_units === [] && .learn_modules
     === [] && .task_units === [] && .assessments === []`). Equivalently:
     `projected_connect_state.max_slug_length <= projected_connect_state.slug_length_limit`
     (50 today; constant on the projection so this gate is self-documenting).
     Connect's `LearnModule.slug` and `DeliverUnit.slug` are
     `SlugField()` with the Django default `max_length=50`. A slug > 50
     chars raises Postgres `DataError: value too long for type character
     varying(50)` at sync time, which falls through the narrow `except
     (CommCareHQAPIException, AppNoBuildException, httpx.*)` in
     `commcare_connect/program/api/views.py:102` and surfaces as HTTP 500
     with an empty body — Phase 4's `connect_create_opportunity` 500s
     opaquely. Reproducer: `leep-paint-collection/20260517-1515` Phase 4,
     module name "Stage 2: Sample Preparation, Drying, Bagging, Shipment"
     → slug `module_6_stage_2_sample_prep_drying_bagging_shipment`
     (52 chars). See `docs/learnings/2026-05-12-boundary-probe-registry.md`.

   On `collision_count > 0`, halt with a `[BLOCKER]` in this skill's
   returned summary to the orchestrator. The BLOCKER MUST name every
   `collisions.deliver_units[].slug` + the `kept` form + each `dropped`
   form so the operator can grep the source. Concrete remediation:
   re-build the affected app (typically Deliver) with **one form per
   module**, since Nova's `compile_app` emits the module slug as
   `<learn:deliver id>` for every form in a module, and the only
   reliable way to get N unique slugs is N modules. See
   `feedback_connect_deliver_unit_per_module` memory for full mechanism.

   On any `oversized_slugs.*` non-empty, halt with a `[BLOCKER]` in
   `auto_surfaced`. It MUST list each offender as
   `<type>: <slug> (<length> chars, in <first_seen_in>)`. Concrete
   remediation: rename the offending Nova module / deliver-unit to
   produce a shorter slug. Rule of thumb — keep `connect.learn_module.name`
   / `connect.deliver_unit.name` ≤ 40 chars so Nova's `module_<index>_`
   prefix + slugified name fits Connect's 50-char column. The
   `pdd-to-learn-app` / `pdd-to-deliver-app` SKILL.md brief templates
   carry this constraint upstream of `app-release` — but oversized slugs
   can still leak past the brief (e.g., when an operator re-runs Nova
   manually), so this gate is the structural wall.

   On `< 1` records of the expected type, halt with the same Step 3
   remediation (re-run coverage; this is a Nova autobuild marker-skip,
   not a slug collision).

   **Pre-0.13.81 fallback** (legacy `connect_markers` count, retained
   for one release): if the response only has `connect_markers` and not
   `projected_connect_state`, fall back to the old shape — count > 0
   per type, but cannot detect slug collisions. Treat that path as a
   degraded build (operator has not pulled the projection-aware MCP).

7. **Trigger Connect's deliver-unit sync.** Connect caches per-opp
   deliver units; after a release, the next opp create or wizard step
   will pick up the new schema. **If an opp ALREADY exists** (a re-release
   of an app that a live or earlier opportunity already uses), sync THAT
   opportunity. **Do not re-run `connect-opp-setup`**: it creates a new
   opportunity rather than re-syncing the existing one. A new opportunity
   on the same release also cannot get a payment unit, because deliver
   units are shared (ace#573).

   No atom syncs deliver units on its own. `connect_list_deliver_units`
   and `connect_create_payment_unit(s)` fire the sync only as a side
   effect, and only when the create-payment-unit form's checkbox list is
   EMPTY (`mcp/connect/backends/playwright.ts` `listDeliverUnits` /
   `createPaymentUnit`). So on an opp that already has deliver units,
   neither one re-syncs a changed schema. Instead:
   1. POST the sync route below for the existing opportunity at the
      program org's URL, the same org `app-modify` uses (`runConnectOrgs()`
      `pm_org_slug`). Or click `Sync Deliver Units` in that opp's wizard.
      The full live-change procedure, including a new deliver unit that
      needs its own payment unit, is `skills/app-modify`.
   2. Read back with `connect_list_deliver_units` on the same opp, and
      confirm every deliver-unit slug in the new release's
      `projected_connect_state` is listed.
   3. If an expected slug is still missing after the sync, halt and report
      it. Do not create a new opportunity to work around it.

   Sync URL pattern:
   ```
   POST /a/<connect_org>/opportunity/<opp_id>/sync_deliver_units/
   X-CSRFToken: <from hx-headers in form HTML>
   ```
   **`opp_id` takes the opportunity UUID OR the int PK — either works**, so
   there is nothing to discover from a wizard page. Connect resolves it with
   `get_object_by_uuid_or_int(..., uuid_field="opportunity_id")` inside
   `@opportunity_required`
   (`commcare_connect/organization/decorators.py:141`,
   `commcare_connect/utils/db.py:66-79`). The route itself is
   `commcare_connect/opportunity/urls.py:160` under the
   `a/<org_slug>/opportunity/` prefix (`config/urls.py:44`).

   > **Verification status (2026-09-07, ace#2185).** Route and ID-shape are
   > verified against upstream SOURCE at the commit above; the POST was **not
   > exercised live** (it is a state mutation and needs an existing opp).
   > Falsified by: a 404 on that path, or a 404 from the decorator when a UUID
   > is passed. The prior "int FK only, read it off the wizard's `hx-post`"
   > note was over-constrained and is retired.

8. **Verify Connect's HQ credential can see the release.**
   Optional but recommended sanity check before Phase 4 starts. Steps 5–6
   already establish `is_released` authoritatively on the HQ side, and
   **Connect stores no independent copy of that fact** — it re-reads the same
   `/a/<domain>/api/v0.5/application/` endpoint. So the only *additional*
   thing this step can tell you is whether **Connect's own stored HQ API key
   reaches `<hq_domain>` and resolves your app as released**. That is a real
   Phase-4 precondition (a wrong/expired key here surfaces as a confusing
   opportunity-create failure), and it is all this step is for. It cannot
   detect a release problem Steps 5–6 missed.

   Do NOT load the wizard page and read the dropdown — the app `<select>`
   ships as `<option value="">Loading...</option>` and is populated lazily
   over htmx. Call the fragment endpoint directly:

   ```
   GET /users/api_keys/?hq_server=<n>                     -> <option value="<api_key_id>">…
   GET /hq/applications/?hq_server=<n>&learn_app_domain=<hq_domain>&api_key=<api_key_id>
   ```

   `hq_server` is Connect's own FK, **not** ACE's cluster key:
   `1` = `https://www.commcarehq.org`, `2` = `https://india.commcarehq.org`,
   `3` = `https://eu.commcarehq.org`. Use `deliver_app_domain=` instead of
   `learn_app_domain=` for the Deliver app; the view accepts either
   (`commcare_connect/commcarehq/views.py`, `get_application`).

   **Match by app id, never by label text.** Each `<option value>` is
   HTML-escaped JSON `{"id": "<hq_app_id>", "name": "<label>"}`. Find the
   option whose `id` equals the `hq_app_id` recorded in Step 5, then judge:

   | Observation | Meaning |
   |---|---|
   | option present, label is the **bare app name** | released — PASS |
   | option present, label starts `Unreleased - ` | **not** released — investigate Steps 5–6 |
   | option **absent** | INCONCLUSIVE — not a failure (see below) |

   **There is no `Released - ` prefix.** Connect prefixes only the negative
   case: `app_name = f"Unreleased - {app_name}"` when no version has
   `is_released` (`commcare_connect/utils/commcarehq_api.py:74-82`). Asserting
   the presence of `Released - ` waits for a string the server never emits and
   would report a correctly-released app as unreleased (ace#2185).

   **Absence is inconclusive, not a failure.** `get_application` drops every
   app already bound to an *active, unexpired* opportunity on that domain
   (`existing_apps` in the same view). So the same app that passes here before
   Phase 4 legitimately vanishes from this list after Phase 4 activates the
   opportunity. Never treat a missing option as "the release did not
   propagate", and never assert "no `Unreleased - ` prefix appears" over the
   whole response — that passes vacuously when the option isn't there at all.

   > **Verification status (2026-09-07, ace#2185).** Live-verified read-only
   > against `connect.dimagi.com` on run `bednet-check-2-visit/20260907-1126`:
   > the fragment returned 143 options, 19 carrying `Unreleased - `, zero
   > carrying `Released - `, with both released app ids
   > (`cbf35cb3…`, `0f4f2a46…`) present under bare labels and matched by
   > option-value `id`. The `existing_apps` exclusion is verified against
   > upstream source only, **not** observed live.

   If you need the wizard page itself, it is
   `GET /a/<connect_org>/program/<program_id>/opportunity-init` — **hyphen, no
   trailing slash** (`commcare_connect/program/urls.py`, route name
   `opportunity_init`; `program_id` comes from `opp.yaml`
   `connect.program.id`). The trailing-slash and the old
   `/a/<org>/opportunity/init/` spellings both 404.

## Connect-marker verification

The `app-connect-coverage` skill (Phase 3 Step 1.5) verifies and
auto-fixes Connect markers before deploy — this skill consumes its
`clean | blocked` verdict. Step 6's CCZ structural verification
(the `projected_connect_state` per-type record counts) is the
post-release boundary check.

> **If you hand-check the CCZ, match markers by NAMESPACE, never by a
> `<learn:` prefix.** Nova emits them as **default-namespace** elements
> — there is no `xmlns:learn` declaration anywhere in the CCZ, so a
> literal `grep '<learn:module'` returns **0 on a perfectly clean app**
> and reads as a missing-marker halt. The wire format is:
>
> ```xml
> <module     xmlns="http://commcareconnect.com/data/v1/learn" id="m1_role">
> <assessment xmlns="http://commcareconnect.com/data/v1/learn" id="readiness_quiz">
> <deliver    xmlns="http://commcareconnect.com/data/v1/learn" id="vmf_visit">
> ```
>
> `commcare_download_ccz`'s own parser is namespace-aware and correct —
> prefer its `connect_markers` / `projected_connect_state` counts over any
> hand-rolled grep. The prefixed spelling used elsewhere in this file is
> shorthand for the element TYPE, not a literal string to search for.
> (dimagi-internal/ace#680 fixed this in the sibling `app-release-qa`;
> observed again from this file on spark-facilitator/20260813-2126.)

## MCP Tools Used

- **Google Drive MCP:** `drive_read_file`, `drive_update_file`
- **ace-connect MCP (CCHQ atoms, added 0.10.38+):**
  - `commcare_make_build` — POST `/apps/save/<app_id>/`, returns build_id.
  - `commcare_release_build` — POST `/apps/view/<app_id>/releases/release/<build_id>/`,
    sets `is_released: true`.
  - `commcare_download_ccz` — GET `/apps/api/download_ccz/?app_id=...&latest=release`,
    returns CCZ bytes (base64) + Connect-marker counts grepped from the
    inflated form XML.
  These run against `ACE_HQ_BASE_URL` (default `https://www.commcarehq.org`)
  using the same Playwright session as the Connect atoms — Connect's
  OAuth-via-CCHQ flow leaves valid CCHQ cookies in
  `~/.ace/connect-session.json`, so a single login covers both services.

  **Prefer these atoms over raw `Bash` + `curl`.** The bash/curl path
  documented earlier in this file is the fallback when the URL contract
  shifts and a re-probe is needed. For why, see reference.md § Why prefer
  the MCP atoms over raw Bash + curl.

## Mode Behavior
- **Auto:** Pre-flight, build, release, verify, update summary, proceed.
- **Review:** Same, but pause after step 4 and present the release status
  for confirmation before updating the summary.

## Dry-Run Behavior
When `--dry-run` is active:
- Run pre-flight (read-only).
- Do NOT POST to `save/` or `release/`.
- Write the intended invocations and the current `is_released` state to
  `comms-log/dry-run-app-release.md`.
- State tracks as `dry-run-success`.

## Failure Modes

- **HTTP 500 on `/apps/save/` with full payload**: usually a malformed
  app-state JSON (deprecated case types, missing required fields, etc).
  CCHQ's UI shows the generic `Sorry, you don't have permission to do
  this action!` banner regardless of the underlying cause — that text
  is bound to `buildState() == 'error'` in Knockout, NOT to a literal
  permission check. Don't let the banner mislead the diagnosis. Look
  at the actual response body or the CCHQ project's logs.
- **HTTP 200 from `/apps/save/` but no new build appears**: empty-body
  POST to /apps/save/ is a no-op that just reflects the saved app.
  You need to POST the full app-state JSON, which is non-trivial to
  reproduce outside the UI's Knockout viewmodel.
- **Broken existing build warning**: CCHQ's app-versions page sometimes
  shows "One or more of your versions is broken". This is a benign
  warning about prior builds; new build creation should still work.
- **`is_released` doesn't flip after release POST**: probe URL pattern;
  the release endpoint may have moved.
- **The release succeeded but ships stale content (ace#1643)**: the
  symptom is a green build + a green Step 6 whose CCZ is missing a Nova
  edit made after `app-deploy`. Step 3a is the guard; if the summary has
  no `drift_check` block, the guard did not run. Repair is the same
  ordered triple Step 3a prescribes — re-upload, **re-apply
  `app-hq-settings`**, rebuild, re-release.
- **`unique_id` validation error, or `--draft-only resolved 0 forms`,
  right after a re-upload (ace#1644)**: CCHQ hands back 40-hex SHA-1 form
  uids after `upload_app_to_hq`. Both widths are accepted since the
  ace#1644 fix (`lib/hq-unique-id.ts`). Seeing the old behaviour means
  the running MCP subprocess predates it — **quit and reopen Claude Code**;
  `/ace:update` + `/reload-plugins` do not respawn MCP children.
| 2026-09-28 | **The build-rejection fix loop requires a SAVED `/nova:edit` checkpoint (voidcraft-labs/commcare-nova#693).** Nova now stages edits until `save_work`, and upload reads only the saved app. The edit brief now asks the architect to save and confirm `saved: true` (replacing a call to the non-existent `validate_app`), and step 4 re-uploads only after a saved checkpoint — a returned `work_id` with pending changes is a failed fix. | ACE team |
