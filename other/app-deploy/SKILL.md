---
name: app-deploy
description: >
  Upload Nova-built Learn and Deliver apps to CommCare HQ as drafts, or re-upload an edit onto the
  existing HQ app. Needs the Nova app ids and a project space.
disable-model-invocation: false
---

# App Deploy

Upload the Nova-generated apps to CommCare HQ and capture the resulting
HQ app IDs and URLs. The actual upload is performed by Nova
(`/nova:upload_to_hq`); this skill orchestrates the inputs, the
pre-flight, and the artifact writeback.

**Scope:** this skill uploads apps as **draft builds**. Nova does not
release apps by design. Connect's deliver-unit sync only reads released
builds, so `app-release` must run after this skill before any Connect
payment-unit configuration. See `skills/app-release/SKILL.md` for the
release flow + the App Editor permission prerequisite.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `learn_nova_app_id` / `deliver_nova_app_id` | the Nova apps to upload (either or both) | explicit argument; default: `3-commcare/pdd-to-{learn,deliver}-app_summary.md` frontmatter `nova_app_id` |
| `hq_domain` | target project space | explicit argument; default: `run_workspace.hq_domain`, else `ACE_HQ_DOMAIN` (Step 2) |
| `expected_hq_app_id` | re-upload only: the HQ app this Nova app already backs, used to prove the id did not change | explicit argument; default: run_state `phases.commcare-setup.products.apps.<app>.hq_app_id` |

Steps 1–6 are the Phase 3 build path. To push an edit of an app that is already live, use
§ Re-uploading to an existing HQ app. It needs no run.

## Existing objects

Re-uploading changes an HQ app that may already back a live opportunity. Nova updates the HQ app
in place, so the id normally holds. Three things are still shared or one-way. Each is handled in
§ Re-uploading to an existing HQ app:

- **The HQ app id is wired into the Connect opportunity at create time**, and Connect's edit form
  cannot repoint it. If the id changes, the opportunity can only be fixed by delete-and-recreate.
- **A Nova re-upload wipes `appearance="acquire"` and per-module `display_style`** (ace#1643).
  `app-hq-settings` must be re-applied before the next build.
- **An upload only changes the HQ draft.** Workers see nothing until `app-release` builds and
  releases it.

## Products

- `3-commcare/app-deploy_summary.md` — HQ app IDs + URLs for both apps (run-bound; a standalone re-upload records into the program context doc instead)
- `run_state.yaml.phases.commcare-setup.products.apps` — run-bound only: consolidated Learn + Deliver app handoff (name, nova_app_id, nova_url, hq_app_id, hq_url, build_status) written as a single atomic block at the end of Phase 3. This skill is the **sole writer** of `products.apps`; readers (ace-web summary, downstream phases) see the block populated once both apps are deployed.
<!-- 0.13.116: legacy `3-commcare/app-deploy_gate-brief.md` removed.
Pause-time summary at the Phase 3→4 Pause Point is composed by the
orchestrator from per-skill QA + eval verdicts. -->


## Process

1. **Resolve the Nova app ids** per § Inputs: explicit arguments first,
   else the app summaries' frontmatter `nova_app_id` in GDrive. These are
   the inputs to `/nova:upload_to_hq`.

**Run workspace:** when the dispatch carries a `run_workspace:` block, its values replace the `.env` ones this skill names — `ACE_HQ_DOMAIN` → `run_workspace.hq_domain`, and Step 4.6's `commcare_delete_app` passes `allow_foreign_domain: <hq_domain>` for a partner space — and a partner workspace never falls back to `.env`. Contract: [`skills/_run-workspace.md`](../_run-workspace.md).

2. **Pre-flight check.** Read `ACE_HQ_DOMAIN` (and `ACE_HQ_BASE_URL`,
   default `https://www.commcarehq.org`) from the loaded environment.
   That's the HQ project space ACE uploads each app to. If
   `ACE_HQ_DOMAIN` is unset or empty, default to `connect-ace-prod` (the
   canonical ACE project space) with an `[INFO]` note in
   `auto_surfaced` — do not pause to ask. Only halt if the env loader
   returned an explicit non-empty value that looks malformed.

   Nova's `/nova:upload_to_hq` takes the target project space as an
   explicit trailing argument (Nova plugin ≥ the
   voidcraft-labs/nova-plugin#12 release). ACE always passes
   `ACE_HQ_DOMAIN` — naming the space IS the upload confirmation, so
   Nova goes straight to the upload with no interactive prompt and no
   need to pre-verify Nova's bound domain. There is no longer a
   "watch the confirmation line / abort on mismatch" step; correctness
   is enforced at upload time by the `domain_not_authorized` handling in
   Steps 3–4 below.

2.5. **XML-escape lint.** Before uploading, walk every form on the Learn
   and Deliver Nova apps and verify no field has unescaped XML
   metacharacters in `label`, `hint`, or `option` text. Specifically,
   look for raw `<` or `>` (not part of a valid `&lt;`/`&gt;` entity,
   and not part of a markdown-fenced code block). XForm XML is the
   upload target; an unescaped `<` will pass Nova's own `validate_app`
   ({"success":true}) but get rejected by CCHQ's build with
   `Error on line N column M: not well-formed`.

   **`&` is NOT in scope — do not scan for it and never rewrite it.**
   Nova entity-encodes `&` (and non-ASCII such as an en-dash, as
   `&#x2013;`) at compile: the blueprint stores the bare `&`, the
   compiled form XML carries `&amp;` (18 escaped / 0 bare across a
   compiled `spark-facilitator/20260907-1120` Deliver CCZ; re-observed
   on `spark-facilitator/20261004-1706` Learn; verified against a
   released build in ace#2150). Rewriting a blueprint `&` to `&amp;`
   therefore DOUBLE-escapes — the worker sees a literal `&amp;` — and
   on a multilingual app the `edit_field` also demotes that unit's
   translations to `out-of-date`, silently falling back to English
   (ace#2207). A partner's published name ships verbatim, `&` included.

   Procedure:

   1. Load every form in both apps with
      `get_form({app_id, moduleUuid, formUuid})` — one call per
      `(moduleUuid, formUuid)`. Nova is **uuid-addressed** since
      2026-07-31 and no tool accepts an index param (see
      `playbook/integrations/nova-integration.md § The 2026-07-31
      uuid-addressing migration`); resolve the whole map with ONE
      `get_app({app_id})` per app — its blueprint prints `[uuid …]` on
      every module, form, and field — or read the uuids off the build
      summary's `nova_uuids:` frontmatter if `pdd-to-*-app` wrote one.
   2. For each field, scan `label`, `hint`, and option `label`s with the
      regex:
      ```
      /<(?![/!?a-zA-Z])|(?<!\\)>(?!\s)/i
      ```
      (A simpler heuristic that catches the common cases: any literal
      `<` or `>`. A literal `&` is never a hit — see above.)
   3. For each hit, fix via `edit_field` — replace `<` with `&lt;` and
      `>` with `&gt;` (or reword: "under 2kg" reads better than
      `(<2kg)`). Never touch `&`. The fixes are private-work edits
      (voidcraft-labs/commcare-nova#693): one `begin_work({app_id,
      request_id})` per app, each `edit_field` with that `work_id` and a
      fresh `request_id` (no `app_id`), then `save_work({work_id,
      request_id, expected_revision})` — which must answer `saved: true`
      BEFORE Step 3, because the upload reads only the saved app. Contract:
      `playbook/integrations/nova-integration.md § The private-work
      authoring contract`. Document each change in
      `ACE/<opp-name>/app-summaries/{learn,deliver}-app-summary.md` under
      a `## XML-escape lint fixes` section.
   4. Note: this is a **class-level preventer**, not a one-time
      workaround. The turmeric e2e hit it on q10 with `(<2kg)` /
      `(>10kg)` in the field label. Filed as
      `docs/issues/nova-validate-app-misses-xml-escapes.md`. Until Nova
      auto-escapes on `add_field`/`edit_field` (or `validate_app`
      rejects), every Phase 3 run does this lint.

   If the lint is skipped (e.g. Nova MCP unauthed at this point), log
   `app-deploy-xml-lint: skipped-nova-unauthed` in `run_state.yaml` and add
   a `[WARN]` to `auto_surfaced`.

2.9. **No unsaved ACE work on either app.** `upload_app_to_hq` reads the
   SAVED app; pending private-work edits are silently excluded, with no
   error anywhere. Every earlier ACE edit pass on these apps (Step 2.5,
   `app-connect-coverage`, `app-media-coverage`, `pdd-to-*-app` post-build
   steps) must have ended in a `save_work` that answered `saved: true`. Confirm
   with one `list_work({app_id})` per app: any entry with `pending_changes > 0`
   is an edit that will NOT ship. Halt with `[BLOCKER] unsaved-nova-work`
   naming the `work_id` — do not save it blind (it may be stale or
   half-finished; the skill that opened it owns it) and do not upload past it.

3. **Upload Learn app.** Run (always pass the target project space as
   the trailing argument):

   ```
   /nova:upload_to_hq <learn_app_id> <ACE_HQ_DOMAIN>
   ```

   Capture from the response:
   - HQ application ID
   - HQ application URL (typically
     `https://www.commcarehq.org/a/<domain>/apps/view/<app_id>/`)
   - Build status (`success` / `errored` / `pending`)
   - Any warnings

   **Handle `domain_not_authorized`.** If Nova returns
   `error_type: domain_not_authorized`, the HQ API key saved in Nova's
   settings can't reach `<ACE_HQ_DOMAIN>`. Nova's `message` lists every
   space the key CAN reach — surface that as a `[BLOCKER]` (do not
   silently upload to a different space) with the reachable-spaces list
   and a pointer to either fix `ACE_HQ_DOMAIN` or re-mint/re-paste an HQ
   key that reaches it. Other error types (`hq_not_configured`,
   `hq_upload_failed`) are also `[BLOCKER]`s — surface Nova's `message`.

   **Handle `project_space_incompatible`.** The upload runs Nova's
   compatibility probe itself and refuses before any remote write when a
   required capability is `missing` **or `unverified`** — "Couldn't confirm
   … Nothing has been sent" is a refusal, not a warning (Nova's own
   `content/docs/project-space-compatibility.mdx`). Branch on the blocker's
   `state`:
   - `missing` → the Step 4.5 `missing` remedies (operator/support, or a
     BUILD DEFECT).
   - `unverified` → **Nova could not complete its live HQ check; it is not
     evidence the space lacks the capability** (ace#2704). Nova probes with
     the HQ API key stored in its own Settings — `GET
     /api/user_domains/v1/` unfiltered, then `?feature_flag=<slug>` — and any
     non-200, malformed body, or 5 s timeout settles to `unverified`
     (`lib/commcare/client.ts` `probeHqProjectSpaceCompatibility`).
     `get_hq_connection` answering `configured: true` proves nothing here: it
     returns STORED settings, makes no HQ call. Discriminate with ACE's own
     key: `npx tsx "$CLAUDE_PLUGIN_ROOT/scripts/probe-hq-connect-flag.ts" <ACE_HQ_DOMAIN>`. If
     ACE's key sees the space in both lists, the space is fine and Nova's
     stored-key path is what fails → `[BLOCKER] nova-hq-probe-unverified`;
     operator re-saves the HQ API key in Nova Settings
     (https://commcare.app → Settings → CommCare HQ), then retry. If ACE's
     key also fails, it is an HQ outage/auth problem — surface that instead.
     Do not upload to another space, and do not strip Connect blocks.
     **Interim for a text-only change to an already-deployed app:** patch
     the changed XForm on HQ directly (`commcare_get_form_source` → edit →
     `commcare_patch_xform` with its sha1 token) and build/release, as long as
     the same change is already saved in Nova (so the next successful Nova
     upload is a content no-op). Anything structural waits for the upload.

   **Handle `hq_confirmation_needed` — verify against HQ, then confirm
   (ace#3164).** Some things an app needs from the space cannot be read with
   any API key, so the upload refuses BEFORE any remote write and lists them in
   `confirmations_needed[]` (each `{kind, subject, label, consequence,
   reasons}`). Every Connect app hits this once per app — the confirmation is
   then stored on the deployment (`deployment.confirmations`). Seen live on
   `bednet-check-2-visit/20261018-0554`: `plan-feature: data-forwarding` and
   `connect-forwarder`, on both apps. **Never confirm blind** — the
   consequence of a false "yes" is that HQ forwards no forms to Connect and no
   Learn or Deliver progress is ever recorded. Verify each item with ACE's own
   HQ session first:

   | `kind` / `subject` | Verify with | Confirm when |
   |---|---|---|
   | `plan-feature` / any subject (`data-forwarding`, `lookup-tables`, `child-cases`, `advanced-case-actions`, …) | `commcare_get_subscription({domain})` (one read covers every plan feature) | the returned `edition` is named in THAT entry's `plans` string — `planIncludesEdition(plans, edition)` in `lib/plan-feature-edition.ts` (case-insensitive, whole-item; Nova's shape is e.g. `"Pro, Advanced and Enterprise"`) |
   | `connect-forwarder` | `commcare_list_connections({domain})` | a connection's `url` is `https://connect.dimagi.com/api/receiver/` and `used_by` includes Data Forwarding |
   | anything else (`flat_location_fixture`, any kind with no ACE probe) | no ACE probe yet | do NOT confirm — `[BLOCKER]` naming the item for the operator |

   A plan feature whose `plans` string does NOT name the space's `edition` is
   a failed verification — `[BLOCKER]` naming the feature, its `plans` and the
   edition — never a confirm. Do not hard-code which editions a feature needs:
   Nova's `plans` string on the entry is the authority (ace#3206).

   Then re-call the upload with `confirm_plan_features: [<subject>, …]` and/or
   `confirm_connect_forwarder: true`, and record each confirmation with its
   evidence (edition; connection id + url) under `nova_confirmations` in the
   Step 5 summary. A failed verification is a `[BLOCKER]` naming what the space
   lacks — do not confirm to get past it.

4. **Upload Deliver app.** Same shape — `/nova:upload_to_hq <deliver_app_id> <ACE_HQ_DOMAIN>` — including the `domain_not_authorized`, `project_space_incompatible` and `hq_confirmation_needed` handling.

4.5. **Verify the target space can run each app** (ace#1048). Some
   CommCare capabilities only work when the project space supports them (a
   domain feature flag, most often), and an app that works in a space where a
   flag happens to be on silently does not in one where it isn't. Ask Nova,
   per app, about the space we just uploaded to:

   ```
   check_project_space_compatibility({ app_id: <nova_app_id>, domain: <ACE_HQ_DOMAIN> })
   ```

   Use the **Nova** `app_id` (not the HQ app id). Run it for **both** apps.
   The tool is read-only; it never enables anything. (It replaced the
   retired `get_app_hq_feature_flags`, which is absent from the 127-tool
   surface verified 2026-09-28. `upload_app_to_hq` now also runs this check
   itself before any remote write and refuses a `blocked` app with
   `project_space_incompatible` — so reaching this step means the upload
   passed it; this re-read records the result and its advisories.)

   Branch on `project_space_compatibility.status` and each entry's state:

   | result | disposition |
   |---|---|
   | `not_needed`, or `ready` with no `unverified` advisories | `[PASS]` — record and move on |
   | `blocked` with a `missing` blocker | **`[BLOCKER]`** — the app needs a capability the target space does not have |
   | `blocked` with an `unverified` blocker | unreachable after a successful upload — the upload itself refuses on it (Step 3 § `project_space_incompatible`). If this re-read alone returns it (the probe flaked between calls), **`[WARN]`** — record as explicitly UNVERIFIED |
   | any `unverified` advisory | **`[WARN]`** — record as explicitly UNVERIFIED |

   Advisories never block (e.g. slower large Search results); record them.

   On a `missing` blocker: surface its friendly `label`, `description`, and
   the app-specific `reasons` naming the configuration that caused the
   requirement (Nova deliberately hides flag slugs here). Then
   **branch on WHERE the requirement came from** — the two cases have opposite
   remedies, and emitting the wrong one costs a redeploy (ace#1195):

   - **The capability traces to something the PDD asked for** → operator
     action. Tell the operator to contact `support@dimagi.com` naming the
     project space (Nova returns `support_email` + `docs_url` for exactly
     this). **Do NOT strip, downgrade, or rebuild the app to dodge the flag** —
     Nova's contract states this result "must never cause an agent to remove,
     undo, or avoid requested app functionality." The app stays as built; a
     human enables the flag.
   - **The capability does NOT trace to the PDD** — it came from default
     module authoring rather than a stated requirement → **`[BLOCKER]` BUILD
     DEFECT.** Do not send the operator to support. Name the capability to
     remove and halt for remediation. Per
     `_app-component-library.md § connect-supported-capabilities-only`, the
     only flag an ACE app may depend on is `commcare_connect`; anything else is
     outside the capability budget. **Many HQ flags are frozen or deprecated,
     meaning HQ's own source instructs staff not to enable them for new
     projects** — so "email support" is not merely slower, it asks a human to
     override a stated policy for a capability the app never needed.

   The canonical instance: case-search inputs on a Deliver menu require
   `search_claim` (+ `case_search_advanced` for fuzzy matching), both frozen.
   A case LIST needs no flag and is what the worker actually uses. If no PDD
   line asked for case search, the fix is `remove_search_input`, not a support
   ticket.

   On unverified: say so plainly rather than substituting a guess. An
   unverified result is not a pass — it is an open question that Phase 9 must
   close before partner handoff.

   If the tool is unavailable (older Nova plugin — see Step 0a's
   `nova_plugin_current`), log `app-deploy-flag-check: skipped-tool-unavailable`
   and add a `[WARN]`. Do not halt.

4.6. **Record `hq_app_action`, and clean up anything in `deployment.left_behind`.**
   **Nova updates the HQ app in place.** The first upload to a project space
   CREATES the HQ application; every upload after that UPDATES that same HQ app
   document, keeping its id. `hq_app_action` in the result says which happened
   (`created` | `updated`), and `deployment.remote_revision` advances on each
   update. So a mid-run re-upload — an XForm escape fix, a Connect-marker patch,
   a Step 4g screen split, any build-rejection iteration — **does not mint a new
   HQ app id and does not strand an orphan.**

   Verified live 2026-08-18 against `connect-ace-prod`: Nova app
   `4dd0325b…` re-uploaded twice returned `hq_app_action: "updated"` both
   times, held `hq_app_id: c0d7027316bc46f8b4fdf4b47fd8d90b` constant, advanced
   `remote_revision` 6 → 8, and returned `left_behind: []` each time. (This
   supersedes the pre-2026-08-18 belief that CCHQ has no atomic app-update API
   and that every upload mints a fresh application document — see
   `playbook/integrations/nova-integration.md § Uploading to HQ updates in
   place`.)

   Record `hq_app_action` per app in the Step 5 summary. `left_behind` is
   normally `[]`; treat a non-empty one as the exception it now is. It can still
   happen when the linked HQ app was deleted on HQ — the call then refuses with
   `remote_app_missing`, and the next upload creates a fresh one, superseding
   the dead link.

   ### If you need a FRESH `cc_app_id`, COPY the app — do not delete it

   Uploading in place is the right default, but a second opportunity on the same
   released Deliver app cannot get a payment unit: `DeliverUnit.payment_unit` is
   a single FK, so one DeliverUnit backs exactly one PaymentUnit ever (ace#573).
   The route previously documented for this — soft-delete the HQ app so the next
   upload hits `remote_app_missing` — works, but it is **destructive**: it breaks
   the app links of whatever opportunity is currently live on those apps, and on
   a run carrying a per-opp OCS TaskType it takes that down too.

   **Copy instead. Same domain, unlinked:**

   ```
   commcare_linked_app_copy({ upstream_domain: <ACE_HQ_DOMAIN>,
                              downstream_domain: <ACE_HQ_DOMAIN>,   // SAME
                              upstream_app_id: <existing hq app id>,
                              name: <UNIQUE name>, linked: false })
   commcare_make_build  ->  commcare_release_build
   ```

   That configuration is HQ's plain "Copy Application"; the linked-domain-pair +
   Pro Edition (`LITE_RELEASE_MANAGEMENT`) requirement binds only `linked: true`.
   Live-validated 2026-09-01 on `connect-ace-prod` — one Learn and one Deliver
   copy, both built and released. Three reasons it beats delete-and-re-upload:

   - **Nothing is destroyed.** The prior opportunity keeps working apps, and any
     per-opp OCS TaskType survives.
   - **It sidesteps ace#1643.** A document copy PRESERVES `appearance="acquire"`
     and per-module `display_style` — the two settings a Nova re-upload wipes —
     so the `app-hq-settings` re-apply becomes unnecessary. Verified in the built
     CCZ *and* on-device (`assertNotVisible "CHOOSE IMAGE"` still passed).
   - Fresh `cc_app_id` ⇒ new `CommCareApp` row ⇒ the posted `passing_score` is
     honoured instead of silently inherited, and the new DeliverUnits are
     unbound so a payment unit attaches.

   Two traps, both hit live: the `name` must be **unique** in the domain (the new
   id is recovered by re-listing and matching on name), and **a timeout on that
   recovery re-list does NOT mean the POST failed** — re-list before retrying, or
   you create a duplicate and break name-based recovery for both copies.

   So: for each id in `deployment.left_behind`, call

   ```
   commcare_delete_app({ domain: <ACE_HQ_DOMAIN>, app_id: <left-behind id> })
   ```

   This is HQ's own **soft** delete (it flips `doc_type` to `<original>-Deleted`
   and writes a `DeleteApplicationRecord`), so the app stays restorable from
   HQ's deleted-applications list — the operation is reversible, which is why it
   is safe to do automatically. Record every deleted id in the Step 5 summary
   under `<app>_superseded_hq_app_id`.

   **Guard rails.** Only delete ids that came back in THIS call's
   `left_behind` — never an id read from an artifact, and never the id you just
   uploaded to. If a delete fails, log `[WARN] orphan-cleanup-failed: <id>`,
   name it in the summary so `/ace:sweep hq` can finish the job, and **continue**
   — a failed cleanup must never halt a successful deploy.

   **When the id DOES change, surface it loudly.** Phase 4 wires the HQ app ids
   into the Connect opportunity at create time (`connect_create_opportunity`),
   and Connect's edit form does not expose those fields — so an opportunity
   created against a stale id needs delete-and-recreate to repoint. Under
   update-in-place this is no longer the ordinary re-upload case, but it is
   still reachable: whenever `left_behind` is non-empty, or `hq_app_action` came
   back `created` for an app this run had already uploaded, the Step 5 summary
   MUST carry an explicit "this app's HQ id CHANGED — use the id above" callout,
   not just the changed frontmatter value.

5. **Write the deployment summary** to
   `ACE/<opp-name>/runs/<run-id>/3-commcare/app-deploy_summary.md`:

   ```yaml
   ---
   hq_base_url: <ACE_HQ_BASE_URL>
   hq_domain: <ACE_HQ_DOMAIN>
   learn_app_id: <hq-app-id>
   learn_app_url: <hq-app-url>
   learn_build_status: <success|errored|pending>
   learn_nova_app_id: <nova-app-id>
   deliver_app_id: <hq-app-id>
   deliver_app_url: <hq-app-url>
   deliver_build_status: <success|errored|pending>
   deliver_nova_app_id: <nova-app-id>
   uploaded_at: <ISO-8601>
   # `created` on the first upload of this app to the space, `updated`
   # thereafter — Nova updates the HQ app in place (Step 4.6).
   learn_hq_app_action: <created|updated>
   deliver_hq_app_action: <created|updated>
   # Normally absent. Present only if `deployment.left_behind` came back
   # non-empty — one entry per id soft-deleted in Step 4.6. See the
   # id-CHANGED callout that step requires.
   learn_superseded_hq_app_id: [<hq-app-id>, …]
   deliver_superseded_hq_app_id: [<hq-app-id>, …]
   hq_feature_flags:
     domain: <ACE_HQ_DOMAIN>
     verification: <verified|not_checked>
     learn_missing: [<slug>, …]        # [] when clean
     learn_unverified: [<slug>, …]
     deliver_missing: [<slug>, …]
     deliver_unverified: [<slug>, …]
     checked_at: <ISO-8601>
   ---
   ```

   Body: human-readable narrative including any Nova warnings and a
   link to each HQ app.

6. **Write the `products.apps` block to `run_state.yaml`** as one atomic
   patch. This skill is the sole writer of `products.apps`, so the
   `deep` `update_yaml_file` merge replaces the `apps` block cleanly
   while preserving sibling phase keys (`status`, `started_at`, `steps`).

   For each app, read the friendly name from the source summary's
   frontmatter (`title`), the `nova_app_id` from the same summary, and
   the HQ details from this skill's upload response. Construct the Nova
   preview URL from the `nova_app_id` directly — Nova's working route
   is `/build/<id>`, not the legacy `/apps/<id>` URL that the upstream
   summaries' frontmatter still carries (which 404s).

   ```yaml
   phases:
     commcare-setup:
       products:
         apps:
           learn:
             name: <from learn summary frontmatter `title`>
             nova_app_id: <from learn summary frontmatter `nova_app_id`>
             nova_url: https://commcare.app/build/<nova_app_id>
             hq_app_id: <from Step 3 upload response>
             hq_url: <from Step 3 upload response>
             build_status: <success | errored | pending>
           deliver:
             name: <from deliver summary frontmatter `title`>
             nova_app_id: <from deliver summary frontmatter `nova_app_id`>
             nova_url: https://commcare.app/build/<nova_app_id>
             hq_app_id: <from Step 4 upload response>
             hq_url: <from Step 4 upload response>
             build_status: <success | errored | pending>
   ```

   **Build the block with `buildCommcareProducts` (`lib/commcare-products.ts`),
   not by hand** — it derives `nova_url` and owns the componentized key.
   **Componentized run** (`phases.idea-to-design.products.mode ===
   'componentized'`): pass Phase 1's `products.components[]` as `components`
   and each summary frontmatter's `components_built:` list as that app's
   `components_built`; the builder writes it per app
   (`apps.learn.components_built`, `apps.deliver.components_built`) and THROWS
   if an app records none or names a component Phase 1 never declared. That is
   the ONE name for the fact — never `components_covered`, never a
   products-level list, never `mode` on an app entry (ace#2157, operator
   decision 2026-10-16). Synthesized run: omit both; the builder refuses a
   stray `components_built`.

   Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
   `merge: 'deep'` on the current run's `run_state.yaml`. This patch is
   rooted at `phases.commcare-setup.products` — a *partial* patch of the
   `commcare-setup` phase child. `two-level` would replace the entire
   `commcare-setup` child wholesale, silently dropping any sibling keys
   already set on it (`status`, `started_at`, `halt_reason`, `steps` —
   e.g. when the orchestrator set `status: in_progress` on resume before
   this write). `deep` recursively merges `apps` under `products` while
   preserving every sibling at every depth. This skill is still the sole
   writer of `products.apps`, but it does NOT own the rest of the phase
   block, so it must not clobber it. See the CLAUDE.md gotcha
   (`update_yaml_file two-level merge replaces a phase child WHOLESALE`)
   and jjackson/ace#572 / #587.

## HQ-id stability — EVERY re-upload rewrites the artifacts (dimagi-internal/ace#1239)

The summary's ids are only trustworthy if the re-upload path owns the
bookkeeping. The obligation below binds to the ACT of re-uploading a
Phase 3 app, **wherever it happens** — Step 4.6's in-skill path, a Step
4g split, or a mid-Phase-3 repair re-upload performed while debugging
`app-release` / `app-release-qa`, long after Step 5 first wrote the
summary. Whoever re-uploads MUST, in the same breath:

1. **Rewrite `app-deploy_summary.md` frontmatter**: the new id into
   `<app>_app_id` / `<app>_app_url`, the old id APPENDED to
   `<app>_superseded_hq_app_id`, and `uploaded_at` refreshed. If the
   body claims "each app was uploaded exactly once", delete that claim —
   it is now false and nothing else marks it stale.
2. **Patch `run_state.yaml` `products.apps.<app>.hq_app_id`** (merge:
   `deep`, per Step 6).
3. **Never leave a prose note as the only guard.** A hand-written
   `FINAL_IDS:` warning in run_state is a manual guard doing a machine's
   job — the live case (spark-facilitator/20260812-1635, Deliver
   uploaded four times) left the summary pointing at the superseded
   original while every downstream mutation atom would have returned
   200 against the wrong app (the ace#1046 silent-wrong-target class,
   arriving through a stale artifact).

Consumers: `run_state.yaml` is the run's source of truth (CLAUDE.md);
downstream skills treat `products.apps.*.hq_app_id` as PRIMARY and this
summary as the cross-check — and may assert their target id is absent
from `<app>_superseded_hq_app_id` before mutating. See
`app-hq-settings` Step 1 for the consumer-side contract.

## Re-uploading to an existing HQ app

This section is the standalone path for pushing a Nova edit onto an HQ app that already exists,
whether it is a finished run's app or a live program's (`skills/partner-on-connect-program`).
It needs no run: pass `nova_app_id`, `hq_domain` and `expected_hq_app_id` explicitly.

1. **Save the Nova edit first.** Nova stages every edit in private work (`begin_work` →
   edits → `save_work`), and `upload_app_to_hq` uploads only the SAVED app. An edit whose
   save did not answer `saved: true` is not in the upload, and nothing will error.
2. **Upload.** Run `/nova:upload_to_hq <nova_app_id> <hq_domain>`, naming the space explicitly
   as in Step 2.
3. **Prove the id held.** Expect `hq_app_action: updated`, `hq_app_id == expected_hq_app_id`,
   and an empty `deployment.left_behind`. If the id CHANGED (`created`, or a non-empty
   `left_behind`), stop and tell the owner. Every opportunity wired to the old id keeps the old
   app and cannot be repointed (Connect wires HQ app ids at create time). Clean up `left_behind`
   per Step 4.6's guard rails.
4. **Re-apply HQ settings.** Run `app-hq-settings` with explicit `--hq-app-id` / `--domain`. The
   re-upload wiped camera-only capture and grid display (ace#1643).
5. **Release.** Run `app-release` with explicit ids, then `app-release-qa` with
   `--opportunity-id` for each live opportunity on the app. Its Step 4.7 re-release invariants
   catch a change that silently breaks Connect's form-field rules or deliver-unit ids.
6. **Record it.** In a run, rewrite the artifacts per § HQ-id stability. For a live program,
   append the change to the program context doc's Decisions: what changed, the before and after
   build versions, and the opportunities affected.

<!-- 0.13.116: gate-brief write step + ## Gate Brief section removed.
At the Phase 3→4 Pause Point, the orchestrator composes the
pause-time summary from this skill's eval verdict
(`app-release-eval`) + downstream `app-connect-coverage` verdict +
the deploy status fields in `app-deploy_summary.md` + the release
fields in `app-release_summary.md` (the owner of release state, ace#1636). The
producer no longer authors a separate gate-brief artifact. -->

## MCP Tools Used

- **Google Drive MCP:** `drive_read_file`, `drive_create_file`
- **Nova plugin slash commands:** `/nova:upload_to_hq`, `/nova:show`
- **Nova MCP (private work):** `list_work` (Step 2.9), and for Step 2.5 fixes
  `begin_work` → `edit_field` → `save_work`
- **Nova MCP:** `check_project_space_compatibility` (Step 4.5 — read-only; never enables anything; replaced `get_app_hq_feature_flags`)
- **ace-connect MCP:** `commcare_delete_app` (Step 4.6 — soft-deletes a
  superseded HQ app returned in `deployment.left_behind`; reversible from HQ's
  deleted-applications list)

## Mode Behavior
- **Auto:** Pre-flight, upload, write summary, notify admin, proceed.
- **Review:** Same, but pause at the Phase 3→4 Pause Point (per
  `agents/ace-orchestrator.md § Pause Points`); orchestrator presents
  the per-skill verdicts.

## Dry-Run Behavior
When `--dry-run` is active:
- Run the pre-flight (it's read-only) and report the result.
- Do NOT call `/nova:upload_to_hq` (this writes to a live HQ project
  space).
- Write the intended Nova invocations (including the resolved
  `<ACE_HQ_DOMAIN>` trailing argument) and the `nova_app_id` values
  resolved from the summaries to `comms-log/dry-run-app-deploy.md`.
- State tracks as `dry-run-success`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-17 | Emit gate brief at `ACE/<opp-name>/runs/<run-id>/3-commcare/app-deploy_gate-brief.md` covering build status, Connectify flags, and workaround-path warnings for the Phase 3→4 gate | ACE team (PM scout, internal-admin lens) |
| 2026-04-27 | Switch from manual HQ-UI upload to `/nova:upload_to_hq` via the Nova plugin. Inputs are now `nova_app_id` values read from the app summaries. New pre-flight check compares Nova's bound HQ project space against `ACE_HQ_DOMAIN`. Gate brief drops the workaround-path WARN and adds a domain-mismatch BLOCKER. | ACE team |
| 2026-04-29 | Carve out app release into the new `app-release` skill (Step 2.5 of Phase 3). This skill now ends at "draft uploaded" — release is a separate, permission-sensitive step. Reason: Connect's `Sync Deliver Units` only enumerates units from released builds, so unreleased apps silently break Phase 4's payment-unit config. (0.10.1) | ACE team |
| 2026-05-29 | Pass the target project space explicitly: `/nova:upload_to_hq <app_id> <ACE_HQ_DOMAIN>` (Nova plugin voidcraft-labs/nova-plugin#12). Naming the space skips Nova's interactive confirmation, so hands-off runs go straight to upload. Pre-flight no longer watches the confirmation line; the domain-mismatch BLOCKER is now driven by Nova's `domain_not_authorized` error at upload time (which enumerates the reachable spaces). | ACE team |
| 2026-08-01 | **Migrated the Step 2.5 XML-escape lint's form load to uuid addressing (ace#1132).** It read "one call per `(moduleIndex, formIndex)`"; Nova's 2026-07-31 redeploy accepts no index param on any of its 63 tools, so the lint named an uncallable operation and would have skipped silently. Now `get_form({app_id, moduleUuid, formUuid})`, with the uuid map resolved from ONE `get_app({app_id})` per app (or off the build summary's `nova_uuids:` frontmatter). Enforced by `test/skills/nova-uuid-addressing.test.ts`. | ACE team |
| 2026-08-13 | **Step 4.6 — clean up `deployment.left_behind` instead of only naming it.** HQ has no atomic app-update API, so every `upload_app_to_hq` mints a fresh application document; Nova returns the superseded id(s) in `deployment.left_behind`. Nova's own guidance stops at naming them, which is the right boundary for Nova (it will not delete a user's app) and the wrong one for ACE — the superseded draft is ours, seconds old, unreferenced, and leaving it behind means every re-upload silently adds an orphan for `/ace:sweep hq`. Observed on hh-poverty-targeting/20260812-2034, where a screen-split re-upload stranded `07f9b7c8…`. Now soft-deleted via `commcare_delete_app` (HQ's own reversible delete — restorable from the deleted-applications list, which is why it is safe automatically), with guard rails: only ids from THIS call's `left_behind`, never one read from an artifact, never the id just uploaded to; a failed delete is a `[WARN]` named in the summary for sweep to finish, never a halt. Adds `{learn,deliver}_superseded_hq_app_id` to the summary frontmatter and REQUIRES an explicit re-upload callout in the summary body whenever `left_behind` is non-empty — the new HQ id is what Phase 4 wires into the Connect opportunity at create time, and Connect's edit form does not expose those fields, so a stale id costs a delete-and-recreate. | ACE team |
| 2026-08-18 | **Step 4.6 — HQ uploads UPDATE IN PLACE; the fresh-app-id premise is retired.** The 2026-08-13 entry above rested on "CCHQ has no atomic app-update API, so every `upload_app_to_hq` mints a fresh application document." That is no longer true, and the whole orphan-per-re-upload model went with it. Verified live against `connect-ace-prod` on 2026-08-18: Nova app `4dd0325b…` re-uploaded twice returned `hq_app_action: "updated"` both times, held `hq_app_id: c0d7027316bc46f8b4fdf4b47fd8d90b` constant, advanced `deployment.remote_revision` 6 → 8, and returned `left_behind: []` each time. So a mid-run re-upload no longer changes the id Phase 4 wires into the Connect opportunity, and no longer strands an orphan for `/ace:sweep hq`. The `left_behind` cleanup and its guard rails STAY — Nova still returns the field, and the id can still change via `remote_app_missing` (the linked HQ app was deleted there, so the next upload creates a fresh one). Adds `{learn,deliver}_hq_app_action` to the summary frontmatter; the loud callout now fires on an id that actually CHANGED (non-empty `left_behind`, or `hq_app_action: created` for an app already uploaded this run) rather than on every re-upload. | ACE team |
| 2026-09-06 | **Stop routing concerns to a gate brief that does not exist (dimagi-internal/ace#1884).** 0.13.116 removed the per-skill gate-brief file class and the ace#1880 sweep removed the remaining `*.md` PATHS, but prose directives naming the gate brief as a DESTINATION survived in 15 files — a concern "surfaced in the gate brief" is surfaced nowhere. Repointed at the verdict YAML's `auto_surfaced` block, which is what the orchestrator actually renders the pause summary from. Gated by the new destination check in `test/skills/gate-brief-removal-complete.test.ts`. | ACE team |
| 2026-09-28 | **Private-work edits and an unsaved-work gate (voidcraft-labs/commcare-nova#693).** Nova now stages every mutation until `save_work`, and `upload_app_to_hq` reads only the SAVED app — so an unsaved ACE edit ships nowhere with no error. Step 2.5's `edit_field` fixes run in `begin_work` / `save_work` and must answer `saved: true` before upload; new Step 2.9 checks `list_work({app_id})` for pending changes and halts `unsaved-nova-work` rather than uploading past them. | ACE team |
| 2026-10-18 | **Handle `hq_confirmation_needed` (ace#3164).** Nova's upload now refuses before any remote write until the caller confirms what no API key can read — on `bednet-check-2-visit/20261018-0554` the Data Forwarding plan feature and a Connect forwarder, on both apps. The skill had no branch for it, so an unattended run had to halt or guess. Steps 3/4 now verify each item against HQ (`commcare_get_subscription` edition; `commcare_list_connections` for the connect.dimagi.com receiver) before re-calling with `confirm_plan_features` / `confirm_connect_forwarder`, record the evidence in the summary, and BLOCK on anything unverifiable. | ACE team |
| 2026-10-19 | **Verify EVERY `plan-feature` confirmation by edition, not just `data-forwarding` (ace#3206).** The ace#3164 table accepted the subscription edition as evidence for `data-forwarding` only and BLOCKed every other plan feature, so any Deliver app with a lookup-backed select or child cases halted Phase 3. On `connect-fi/20261018-1440` the Deliver app needed `lookup-tables` ("Standard, Pro, Advanced and Enterprise"), `child-cases` and `data-forwarding` ("Pro, Advanced and Enterprise") and `advanced-case-actions` ("Advanced and Enterprise") on edition `Advanced` — the same evidence answers all four. The row is now general: confirm a plan feature when `commcare_get_subscription`'s `edition` is named in that entry's own `plans` string (`planIncludesEdition` in `lib/plan-feature-edition.ts`, tested in `test/lib/plan-feature-edition.test.ts`). `connect-forwarder` is unchanged; `flat_location_fixture` and any kind with no ACE probe stay a do-not-confirm `[BLOCKER]`. | ACE team |
