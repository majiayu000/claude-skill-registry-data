---
name: rulebase-work-items
description: Use to push back-office work into Rulebase over the REST API so it can be evaluated like a conversation, with a dry-run plan, idempotent external ids and an audit log. Trigger for "send our back-office work to Rulebase", "push work items", "QA our operations team", "get case work into Rulebase", disputes or KYC queues with no customer on the line, or duplicate work items appearing after a re-run.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: mutation
  platform: rulebase
---

# Pushing work items into Rulebase

A work item is a unit of back-office work with no customer conversation attached: a KYC
review, a dispute investigation, a manual payment repair, a fraud case. Rulebase evaluates
these the same way it evaluates a support conversation, but nothing syncs them
automatically, so they arrive over the REST API from your own admin tooling.

This writes to a live workspace. It runs a **dry run by default** and requires an explicit
`--apply` against a reviewed plan.

## Reversibility

**There is no delete endpoint for a work item.** A batch pushed by mistake becomes
evaluatable records in the workspace and removing them is a support request.

What saves you is that **the API is an upsert keyed on `external_id`**, so re-running is
safe and correcting a bad field is a matter of pushing the same id again. That property is
also the trap below.

## The trap: `external_id` is the idempotency key, and it is the only required field

`POST /work_items` requires exactly one thing: `work_item.external_id`. Agent, type,
status, timestamps and events are all optional.

Two consequences, and both bite:

**Generate a fresh id per run and you create duplicates rather than updating.** The id has
to be stable and derived from your source system's own primary key. A UUID minted at push
time looks fine, succeeds, and silently doubles your data on the second run.

**Events have their own `external_id`, and it upserts too.** The endpoint is documented as
*create or update a work item event*, so an event id reused across two genuinely different
events overwrites the first. Derive event ids from the source event, not from a loop index:
`case-8841-note-3` is stable, `event-3` is not.

## The silent gap: a work item with no agent is never evaluated

Because `agent_email`, `agent_name` and `agent_external_id` are all optional, a perfectly
valid work item can arrive attached to nobody. It will be accepted, stored, and never
evaluated, because there is no one to evaluate.

Reconcile agent identifiers against the QA roster **before** pushing. That is what the dry
run does, and it is the difference between a working integration and a workspace quietly
filling with unevaluatable records.

The same applies in a subtler way to **events**: a work item with no events has no
substance for a scorecard to assess. The item exists; there is nothing in it. Push the
events with the item where you can, since `POST /work_items` accepts an `events` array
inline and saves you a request per event.

## Status is a fixed enum

`status` accepts `pending`, `in_progress`, `completed` or `cancelled`. Your own system
almost certainly has more states than that, so the mapping is a decision to make once and
write down rather than improvise per record.

Two things worth deciding deliberately:

- **`completed_at` matters.** Evaluation eligibility keys off completion, so an item marked
  `completed` with no `completed_at` may sit outside whatever window the workspace is
  configured for.
- **`cancelled` is not `completed`.** Mapping abandoned work to `completed` puts
  never-finished cases into the evaluated population and drags every score.

Anything that does not fit the enum belongs in `custom_attributes`, which is a free-form
object and the right home for your own state machine, queue names, case values and
priorities. Send the raw value there alongside the mapped one, for the same reason every
export in this catalog keeps a `*_raw` field.

## Bulk upload has a size limit

`POST /work_items/upload` takes a multipart file and **documents a `413` response**, so
there is a payload ceiling. The exact figure is not in the spec, so do not hard-code one:
chunk the file, and treat a `413` as a signal to halve the chunk rather than as a failure.

The endpoint returns an upload id; poll `GET /work_items/upload/{id}` for its status. As
with any bulk path, acceptance is receipt rather than completion.

`429` is a documented response on every endpoint here. Back off on it rather than retrying
immediately.

## Before you run

- **`RULEBASE_API_KEY`** in the environment, never as an argument.
- **The right region host.** `api2.rulebase.co` for US, `eu.api2.rulebase.co` for EU. A key
  from one region against the other returns the same `401` as a wrong key, with nothing in
  the response to tell you which mistake you made.
- **The QA roster**, to reconcile agent identifiers against.
- **A manifest**, one JSON object per line:

  ```jsonl
  {"external_id":"case-8841","type":"kyc_review","status":"completed","completed_at":"2026-07-14T16:02:00Z","agent_email":"amara@example.com","custom_attributes":{"queue":"enhanced_dd","source_status":"closed_verified"},"events":[{"external_id":"case-8841-note-1","actor_email":"amara@example.com","content":"Requested proof of address","occurred_at":"2026-07-14T09:12:00Z"}]}
  ```

## Safety

1. **Dry run is the default.** Validates and plans; sends nothing.
2. **Deciding and doing are separate.** The dry run writes a plan file that `--apply`
   consumes, so a human can read it first.
3. **Append-only audit log**, one JSONL record per attempted push, written as the run
   proceeds.
4. **Idempotent and resumable.** Completed external ids are journaled and skipped. The API
   upserts, so a retry corrects rather than duplicates.
5. **Bounded blast radius.** `--max-changes` defaults to 100.
6. **Reversibility stated** above.
7. **Verify after applying.** Re-reads each item and reports anything that did not land.

No flag combines validating and pushing, and there is no `--force`.

## Usage

```bash
export RULEBASE_API_KEY=...

node scripts/push-work-items.mjs \
  --manifest ./work-items.jsonl \
  --roster ./agents.txt \
  --region us \
  --plan ./out/work-items-plan.json
```

Read the plan, then apply it bounded:

```bash
node scripts/push-work-items.mjs \
  --plan ./out/work-items-plan.json \
  --apply \
  --max-changes 50 \
  --audit ./out/work-items-audit.jsonl \
  --journal ./out/work-items-journal.jsonl
```

Re-run the same command after an interruption. Write outputs outside the repository:
manifests contain case content and agent identifiers, which is production PII.

## When items are accepted but never evaluated

Check in this order, because each masks the next:

1. **Is there an agent on the item**, and does the identifier match someone on the roster?
2. **Does the item have events?** No events means nothing to assess.
3. **Is the status `completed` with a `completed_at`** inside the workspace's eligibility
   window?
4. **Is there a published scorecard** whose scope covers work items and those people? A
   scorecard scoped only to conversations will never touch them.

Report which of these you checked. "The push worked" and "the work is being evaluated" are
different claims.

## Present results to the user

1. **Region and organization** pushed to, before anything else.
2. **Planned, applied and skipped**, with the `--max-changes` bound named.
3. **Dry-run findings** worth fixing before pushing: unstable or duplicated external ids,
   agent identifiers not on the roster, statuses outside the enum, items with no events,
   `completed` items with no `completed_at`.
4. **Verification** after applying, and anything that did not land.
5. **What remains**, and the command to continue.
6. **Whether the items will actually be evaluated**, or which of the four gates above you
   could not confirm.
