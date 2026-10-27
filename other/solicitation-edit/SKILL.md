---
name: solicitation-edit
description: >
  Edit an existing labs solicitation: extend its deadline, rewrite its text or criteria, change its
  visibility, or close or reopen it. Use when asked to change a published solicitation. Needs its
  id.
---

# Edit a solicitation

Changes a solicitation that is already published or drafted. Typical changes: extend the
deadline, fix the scope text, add a question, unlist it, or close it. `solicitation-create` makes
new ones; `solicitation-review` scores responses and awards. This skill does neither.

Platform facts: [`connect-labs.md` § Changing live labs objects](../../playbook/integrations/connect-labs.md#changing-live-labs-objects)
and § Solicitations, responses, reviews, awards.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `solicitation_id` | the solicitation (integer) | explicit arg; default: run_state `phases.solicitation-management.products.solicitation.solicitation_id`; else the program context doc |
| `update_data` | the fields to change, in `update_solicitation`'s canonical shape (all optional, shallow-merged) | explicit arg |

No `run_state.yaml` is needed. **Unlisted (`is_public: false`) solicitations are readable by their
owner**, so ACE reads its own unlisted calls with `get_solicitation` and the id alone; `program_id`
is accepted for compatibility but is not needed (live schema, 2026-10-18).

## Products

- A change record with the fields before, requested and read back:
  - inside a run, `8-solicitation-management/solicitation-edit_<YYYYMMDD-HHMM>.md`;
  - on a program project, a dated line in the context doc's Decisions.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

1. **Confirm the approval.** A published solicitation is visible to its audience, and candidates
   may already have responded. The caller at level 0 must already have shown the before and after
   and got approval. With none recorded, return the proposal and stop.
2. **Read the before state** with `get_solicitation` and `list_responses`. Responses change what is
   safe to edit:
   - **Questions:** responses are keyed by question `id`. Never remove or re-id a question that
     has answers. Add new ids instead.
   - **Evaluation criteria:** once `criteria_locked` is set, `evaluation_criteria` cannot change
     and the lock cannot be lifted. Refuse a criteria edit on a locked call.
   - **Deadline:** shortening a deadline past the date of an existing response is legal but
     surprising. Say so in the proposal.
3. **Check visibility before writing.** Setting `is_public: true` lists the call for every
   logged-in labs user. Never make a call public on a run where the operator has said
   "non-public". Omit `is_public` to leave visibility unchanged.
4. **Write.** Call `update_solicitation` with `{solicitation_id, update_data}`. Only send fields
   that change; the merge keeps the rest.
5. **Read back** with `get_solicitation`. Diff the result against `update_data`; any field that
   did not take is a failed edit.
6. **Record.** Write the fields before, requested and read back to the record named in
   § Products. Inside a run, also update `phases.solicitation-management.products.solicitation`
   (deadline, status, visibility) with `update_yaml_file` `merge: 'deep'`.

## MCP Tools Used

- connect-labs: `get_solicitation`, `list_responses`, `update_solicitation`
- ace-gdrive: `update_yaml_file` (run write-back only)

## Existing objects

- **A solicitation is not tied to a Connect opportunity** (`connect-labs.md` § A solicitation is
  not tied to a Connect opportunity). Editing it never touches the opportunity, and the reverse
  is also true.
- **Locked criteria cannot change.** Refused in step 2.
- **Answered questions keep their ids.** Enforced in step 2.

## Mode Behavior

- **Auto:** with approval recorded in the dispatch, runs steps 2–6.
- **Review:** presents the step 2 analysis and waits before step 4.

## Dry-Run Behavior

When `--dry-run` is active, run steps 2–3 and write the proposal. Do not call `update_solicitation`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Initial version: the edit path for existing solicitations, aligned with the live schema (unlisted calls are owner-readable without program_id) | ACE (build-vs-maintain audit) |
