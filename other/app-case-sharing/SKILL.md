---
name: app-case-sharing
description: >
  Design and build location-based case sharing into an app, so a supervisor sees their team's cases
  and other areas see none. Use when a request mentions case sharing or a supervisor seeing their
  team. Covers Nova authoring, its proof, and HQ setup.
disable-model-invocation: false
---

# App case sharing

Read `playbook/integrations/hq-case-sharing.md` first — it carries the evidence (what was observed vs read
from source vs assumed) and the HQ facts. This skill is the procedure. **Never tell a requester "ACE cannot do
case sharing"**: the app side is fully authorable, and the HQ side has atoms (`commcare_set_location_types`,
`commcare_list_locations`, `commcare_assign_user_locations`). What is still unproven is named in the playbook's
*Open* list; say exactly those items, not a blanket no.

## Inputs

- Who works where: roles (FLW, supervisor, M&E officer…), the place hierarchy, and which role must see whose records.
- The record(s) to share and which form creates them / which form a supervisor edits.
- The HQ project space (**ask — never pick one**; Nova's `get_hq_connection` lists reachable spaces and says never
  to choose for the user). Default for a throwaway: a scratch space the requester names.

If the requester names no hierarchy, derive the smallest one that expresses the three questions they asked and say
so. Do not invent real place names — use labelled test places (`Area 1`, `FLW 1A place`).

## Procedure

0. **Prove Nova can upload to the chosen space — before any Nova authoring (ace#3043).** Nova's
   `upload_app_to_hq` (step 5) refuses a space missing from its stored list (`domain_not_authorized`), and a
   fresh scratch space is missing from it by construction: Nova stores the key's reachable spaces when the key
   is saved. Find that out now, not after a build. Same gate as `agents/commcare-setup.md` § Step 0:
   - Call Nova's `get_hq_connection`. `configured: true` with the space in `available_domains[].name` →
     proceed to step 1.
   - `configured: true`, space NOT listed → refresh Nova's stored list yourself, **once**:
     `node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/nova-refresh-hq-domains.ts" --domain <space>`
     (`ACE_ROOT` resolved as in `agents/commcare-setup.md` § Nova contract probe), then re-call `get_hq_connection`.
     - exit 0 and the space is now listed → proceed.
     - exit 3 (`still-missing`) → **halt**: the HQ key's user is not a member of the space. Tell the requester
       to add that user (ace@) to the space, or name a space it already reaches (list `available_domains`).
     - exit 2 (`refresh-blocked`, the JSON names the Google challenge, e.g. `google-2fa` — seen from a cloud
       runner on `20261016-0618`) → **halt**: the operator presses **Refresh** on the CommCare HQ card at
       `https://commcare.app/settings` as the ACE identity, then re-runs. Do not build first and work around
       the upload with `compile_app` + an HQ import: that skips Nova's place push, which is the half of this
       skill that puts the places on HQ.
   - `configured: false` → **halt**: Nova has no HQ key; the operator saves one in Nova's settings.
   Never loop the script — a second refresh of unchanged membership answers the same.
1. **Design the levels from the visibility rules, one rule per level.**
   - The level whose places OWN records → `caseFlow.ownsCases: true`, `workers: assigned`, `descendantCases: none`.
   - A supervising level → `ownsCases: false` (or true if it also owns), `workers: assigned`,
     `descendantCases: all` or `down-to <level>`.
   - "Can colleagues see each other's?" is answered by *how many workers share one owning place*: one place per
     worker = they cannot; one shared place = they can. State it as a design choice.
2. **Author in Nova** (`begin_work`; every edit takes `work_id` + `request_id`; the app only exists after `save_work`).
   Order, because places need a saved app: levels (`add_organization_levels`) → a minimal valid module + forms →
   `save_work` → `create_location` (parents first; read `organizationRevision` and pass it as
   `expectedRevision`) → `add_user_types` → `add_personas` with `locationUuids` (primary first).
   - **Create the shared record from a SURVEY form** with an `add_case_operations` `create` whose
     `owner` is `external-user('commcare_primary_case_sharing_id')`. A registration form's record is owned by the
     individual worker and would not be shared.
   - The supervisor's edit is a follow-up form on the same case type.
3. **Prove the sharing in Nova before touching HQ**: `start_app_test` with one session per persona (up to four),
   each FLW enrols a record, then `sync` + open the record list per session. Assert what each persona sees and
   record it as a table. `finish` the test. This is Preview, not an HQ restore — say so.
4. **HQ levels** — `commcare_list_location_types` (read), then `commcare_set_location_types` with
   `dry_run: true`, show the plan (`created` / `updated` / `preserved`), then run it for real and require
   `problems: []`. Map Nova → HQ: `ownsCases` → `owns_cases`; `descendantCases` all|down-to →
   `view_descendants` (+ `view_descendants_down_to_code`). **Level `code`s must equal Nova's level codes** —
   Nova pushes places under those codes.
5. **Push**: `upload_app_to_hq` to the chosen space (Nova pushes the places). Confirm with `commcare_list_locations`.
6. **Workers**: `provision_workers` for the personas (it assigns places and returns one-time passwords — show every
   password to the user immediately; Nova stores none). For workers Nova did not create, find the id with
   `commcare_list_users` and call `commcare_assign_user_locations`.
7. **Report with the evidence tiers**: what Nova's test showed, what HQ read-backs showed, and what was not seen
   (device restore, Connect-provisioned worker assignment). Never write "works on Connect" from a Nova test.

## Hand-off when an atom cannot run

If the space lacks the `LOCATIONS` privilege, the key owner lacks Edit Locations / Access APIs, or ace@ is not a
domain admin, the atom's error says which gates are possible (HQ does not say which). Then the manual list is
exactly: turn the privilege on for the space; create the levels in *Settings → Organization Levels* with the flags
from step 4; assign each worker/officer a place on their user page. Give the requester that list, tied to the
specific codes and names designed in step 1.

## Gotchas

- A scratch Nova app is still a Nova app: delete it (`delete_app`) when the proof is done, or reuse the Project.
- `commcare_set_location_types` is a full-replace POST under the hood; never hand-roll it. The atom preserves
  every existing level; trust `preserved` in the dry-run output.
- A worker with no assigned place has an empty `commcare_primary_case_sharing_id`; their records get an empty
  owner. Assignment is part of the build, not an afterthought.
- Address-book visibility does not deliver records (Nova guide). Do not use it to "share" cases.
