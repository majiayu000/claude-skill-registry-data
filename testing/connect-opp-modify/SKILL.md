---
name: connect-opp-modify
description: >
  Change a live Connect opportunity: verification flags, payment units, dates, budget, visit caps or
  the Learn pass mark, with a before-read and read-back. Use when asked to extend or reconfigure a
  live opp. Needs the opp id.
---

# Modify a live Connect opportunity

Changes configuration on an opportunity that already exists, whether or not ACE built it. Each
change reads the current value, writes it, and reads it back. Playwright-backed writes report the
POST status, not the saved state, so only the read-back counts.

Platform facts: [`connect-api.md` § Changing a live opportunity](../../playbook/integrations/connect-api.md#changing-a-live-opportunity)
and § Data model gotchas. This skill is the procedure.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id` | the opportunity UUID | explicit arg; default: run_state `phases.connect-setup.products.connect.opportunity.id`; else the program context doc's Scope |
| `program_org` | the org whose URL serves every opportunity operation: the **program's** org, not the holding org (`connect-api.md` § PM→NM org-URL matrix) | explicit arg; default: run_state `products.connect.pm_org_slug`; else the org in the program's recorded URL |
| `program_id` | needed only for the Learn passing score | explicit arg; default: `opp.yaml.connect.program.id`; else the context doc |
| `changes` | the requested change(s): any of `verification_flags`, `add_payment_units`, `end_date` / `name` / `short_description` / `description` / `active`, `total_budget`, `learn_passing_score` | explicit arg |

No `run_state.yaml` is needed.

## Products

- A change record with each field's before, requested and read-back values:
  - inside a run, `<N>-<phase>/connect-opp-modify_<YYYYMMDD-HHMM>.md`;
  - on a program project, a dated line in the context doc's Decisions.

## What this skill cannot do

| Requested | Why not | Say instead |
|---|---|---|
| Change or delete a payment unit (amount, caps, deliver units) | No atom exists | Do it in the Connect UI, or a new opportunity on a fresh Deliver release |
| Change the holding org | `target_organization_slug` is create-time only; `connect_update_opportunity` has no org field (ace#2919) | A new opportunity, which is a build, not a change |
| Delete the opportunity | No atom exists | Deactivate it (`active: false`) or delete it in the Connect UI |
| Bind a payment unit to a deliver unit another opportunity in the same holding org already holds | ace#573 | A fresh Deliver release |

Refuse these up front, with the reason, before any write.

## Process

1. **Confirm the approval.** These are writes to a live partner object. The caller at level 0 must
   already have shown the before and after values and got approval
   (`partner-on-connect-program § Changing a live program`). A subagent cannot ask the human; with
   no recorded approval, return the proposal and stop.
2. **Read the before state** at `program_org`:
   - `connect_get_opportunity`;
   - `connect_list_payment_units` and `connect_list_deliver_units`;
   - `connect_get_verification_flags`: the persisted `form_field_rules`, the per-deliver-unit
     duration floors and the submission window. It is read-only (ace#3161), so the before-read
     never goes through `connect_set_verification_flags`. An explicit `--form-field-rules`
     overrides it. Read it even when `changes` has no `verification_flags`: a new payment unit
     on a deliver unit that already carries rules changes what those rules gate;
   - for a passing-score change, `connect_get_learn_passing_score` (needs `program_id`).

   A missing opportunity at that org means the wrong org. Re-resolve it; never try the other org
   blind.
3. **Refuse what can't be done.** Check `changes` against § What this skill cannot do.
4. **Name the side effects in the proposal before writing:**
   - **Learn passing score:** shared by every opportunity in the holding org wired to the same
     HQ Learn app (ace#1350). List those opportunities with `connect_list_opportunities`.
     Changing the score changes the gate for all of them. Workers already past Learn are
     unaffected, because completion is one-way.
   - **New payment unit:** needs an unbound deliver unit. List the deliver units and check which
     are already referenced by `connect_list_payment_units`.
   - **Budget:** pass `total_budget` to `connect_create_payment_units`, so the server enforces
     funds for at least one worker (ace#729).
   - **`short_description` and slug:** both are truncated at 50 characters without warning.
     Refuse anything longer.
5. **Write, one change at a time**, each followed by its read-back. The payload rules for the
   first two live in one place, `connect-opp-setup` § Operations on an existing opportunity;
   follow them there rather than from memory:
   - **Verification flags:** `connect_set_verification_flags`, per `connect-opp-setup` Step 5
     (JSONPath `question_path` read from the released CCZ, the stored option value, the deliver
     unit's `server_id`, names of 25 characters or fewer, the refused dead flags). Its response
     carries `form_field_rules_saved` and the persisted rules. A deliver-unit move or a duration
     floor that did not persist is a typed error, not a success.
   - **Add payment units:** `connect_create_payment_units`, an atomic batch, per
     `connect-opp-setup` Step 6 (whole-currency integers, never cents; a non-empty
     `required_deliver_units` of `server_id`s; `total_budget` passed; the create response, not
     the listing, is the read-back).
   - **Dates, name, description, active:** `connect_update_opportunity`. Use it to deactivate
     only; activate with `connect_activate_opportunity`, which carries the activation
     preconditions.
   - **Learn passing score:** `connect_set_learn_passing_score`. Keep its
     `previous_passing_score` in the record. To diagnose a read-back that disagrees, use
     `connect-opp-setup` Step 4's `passing_score` check (`classifyPassingScoreReadback`).
6. **Read back and compare.** Run step 2's reads again and diff them against the requested values.
   Any mismatch is a failed change: report it. Retry only once, and only when the cause is
   understood.
7. **Record.** Write before, requested and read-back values to the record named in § Products.

## MCP Tools Used

- ace-connect: `connect_get_opportunity`, `connect_list_opportunities`, `connect_list_deliver_units`, `connect_list_payment_units`, `connect_get_verification_flags`, `connect_set_verification_flags`, `connect_create_payment_units`, `connect_update_opportunity`, `connect_activate_opportunity`, `connect_get_learn_passing_score`, `connect_set_learn_passing_score`

## Existing objects

- **Deliver units are shared** within a holding org on the same released Deliver app (ace#573). A
  new payment unit needs an unbound deliver unit. Step 4 checks for one; with none, refuse.
- **The Learn `passing_score` lives on the shared `CommCareApp` row** (ace#1350). Step 4 names
  every affected opportunity before any write.
- **The holding org is create-time only** (ace#2919). Refused in step 3.
- **There is no payment-unit update or delete atom.** Refused in step 3.

## Mode Behavior

- **Auto:** with approval recorded in the dispatch, writes and reads back each change; halts on the
  first mismatch.
- **Review:** presents the step 4 proposal (including every other opportunity a shared change
  touches) and waits.

## Dry-Run Behavior

When `--dry-run` is active, run steps 2–4 and write the proposal. Make no writes.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Step 5 points at `connect-opp-setup` § Operations on an existing opportunity for the flag, payment-unit and passing-score mechanics, so they are written down once (#3148 batch 3) | ACE |
| 2026-10-18 | Initial version: change a live opportunity, with explicit "cannot" rows and shared-state warnings (audit item 6) | ACE (build-vs-maintain audit) |
