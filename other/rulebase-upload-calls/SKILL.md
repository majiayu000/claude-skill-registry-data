---
name: rulebase-upload-calls
description: Use to push call recordings into Rulebase over the REST API when the phone system has no native connection, in reviewed batches with a dry-run plan, resume and audit log. Trigger for "upload calls to Rulebase", "import call recordings", "backfill our call history into Rulebase", "get XCally calls into Rulebase", "Rulebase isn't seeing our calls", or bulk-ingesting audio for QA evaluation.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: mutation
  platform: rulebase
---

# Upload call recordings to Rulebase

Pushes audio recordings and their metadata into a Rulebase workspace over the v1
REST API, for phone systems with no native connection. Once received, uploads enter
the normal evaluation pipeline.

This writes to a live workspace. It runs a **dry run by default** and requires an
explicit `--apply` against a reviewed plan file.

## Reversibility

**Uploads cannot be undone through the API.** There is no delete endpoint for a
conversation upload. A batch pushed by mistake becomes conversations in the
workspace, is eligible for evaluation, and consumes evaluation volume. Removing
them is a support request, not a rollback.

What *is* safe: **re-running is safe.** Each call carries a `unique_id` that
Rulebase uses to identify it, and the journal in this skill skips anything already
uploaded. An interrupted run resumes without duplicating.

Because the damage is "too much data, unremovable" rather than "data destroyed",
the guardrail that matters most is `--max-changes`. Backfilling a year of call
history should be a deliberate sequence of bounded batches, each one verified,
not a single unbounded run.

## What the API actually accepts

Worth reading before planning a migration, because it is narrower than "push your
conversations in" suggests.

- **Audio only.** WAV, MP3 or M4A. This endpoint ingests call recordings; it is not
  a generic conversation-import API for helpdesk tickets.
- **`source` is a fixed enum.** The API accepts a specific set of source
  identifiers, not a free-text system name. Check the current v1 reference for the
  accepted values and use one of them exactly — an unrecognised source is rejected.
- **100 MB per file** on the multipart endpoint. Larger files go through the
  presigned-URL path.
- **Metadata is mandatory and asymmetric by direction.** All fields are required,
  and two of them mean different things for inbound and outbound calls:

  | Field | Inbound | Outbound |
  | --- | --- | --- |
  | `agent` | Agent email address | Agent email address |
  | `caller` | Customer phone number | Agent email (often duplicates `agent`) |
  | `called` | Trunk or extension number | Customer phone number |

  Getting `caller`/`called` backwards for outbound calls is the most common
  ingestion error, and it does not fail loudly — it produces conversations with the
  customer and agent transposed, which then get evaluated that way.

- **`agent` is how the employee is identified.** An email that does not match a
  person on the QA roster produces a conversation nobody is evaluated for. Reconcile
  the agent emails in your manifest against the roster *before* uploading; that is
  what the dry run does.

### Two upload paths

- **Multipart** (`POST /conversations/upload`) — one request per call, file in the
  body. Simplest, and correct for anything under the size limit.
- **Presign** (`POST /conversations/upload/presign` → PUT to the returned URL) —
  request a URL for a filename and source, then upload the bytes directly.
  **The presigned URL expires in 30 minutes**, so request it immediately before
  the transfer, never in a batch upfront. A pre-generated list of URLs for a
  thousand files will be mostly expired before you use it.

Poll `GET /conversations/upload/{id}` for processing status. Uploads that are
accepted still take time to become conversations, so a `201` is receipt, not
completion.

## Before you run

- **`RULEBASE_API_KEY`** in the environment. Never as an argument. If you don't have
  a key yet, or you're unsure of the region, set up access first — the region is
  the thing that silently returns `401` when wrong.
- **Region host.** `api.rulebase.co` for US, `eu.api.rulebase.co` for EU. A key from
  one region does not authenticate against the other, and the failure is an
  indistinguishable `401`.
- **The agent roster.** Have the list of evaluatable agent emails to reconcile
  against.
- **A manifest.** One JSON object per line describing each call:

  ```jsonl
  {"file":"/calls/2026-07-01/abc.mp3","unique_id":"xc-88213","type":"inbound","agent":"amara@example.com","caller":"+2348012345678","called":"+2341234567","recorded_at":"2026-07-01T09:14:22Z"}
  ```

  Build it from your phone system's own export. Do not hand-write it for more than
  a handful of calls.

## Safety

The seven rules this skill runs under:

1. **Dry run is the default.** `upload-calls.mjs` with no `--apply` validates and
   plans. It never transfers a byte.
2. **Deciding and doing are separate.** The dry run writes a plan file; `--apply`
   consumes it. A human can read the plan — or hand it to someone who can approve
   it — before anything is uploaded.
3. **Append-only audit log.** One JSONL record per attempted upload as it happens,
   with the target `unique_id`, outcome, returned upload id, and the plan it came
   from.
4. **Idempotent and resumable.** Completed `unique_id`s are journaled and skipped
   on re-run. Interruptions are expected on multi-hour backfills.
5. **Bounded blast radius.** `--max-changes` defaults to 100 and must be raised
   deliberately. Backfill in verified batches.
6. **Reversibility stated** above, not buried here.
7. **Verify after applying.** The run re-reads each upload's status and reports
   anything that did not land.

There is no flag that combines validating and uploading, and no `--force`.

## Usage

Dry run — validates the manifest, checks every file exists and is a supported
format and size, reconciles agent emails against the roster you supply, flags
inbound/outbound metadata that looks transposed, confirms auth, and writes a plan:

```bash
export RULEBASE_API_KEY=...
node scripts/upload-calls.mjs \
  --manifest ./calls.jsonl \
  --roster ./agents.txt \
  --region us \
  --plan ./out/upload-plan.json
```

Read the plan. Then apply it, bounded:

```bash
node scripts/upload-calls.mjs \
  --plan ./out/upload-plan.json \
  --apply \
  --max-changes 50 \
  --audit ./out/upload-audit.jsonl \
  --journal ./out/upload-journal.jsonl
```

Re-run the same command after an interruption; journaled calls are skipped. Raise
`--max-changes` only once a smaller batch has been verified in the workspace.

Write outputs outside the repository. Manifests contain customer phone numbers and
agent emails — they are production PII and must not be committed.

## When uploads are accepted but nothing appears

Check in this order, because each one masks the next:

1. **Processing status** — `GET /conversations/upload/{id}`. Accepted is not
   processed.
2. **The agent email matched a person on the roster.** If not, the conversation
   exists with nobody to evaluate.
3. **Evaluation eligibility.** Coverage sampling, the eligibility window, and
   eligibility instructions all gate whether a conversation gets scored. An
   eligibility window shorter than the age of a backfill will silently exclude the
   entire backfill — this is the usual reason a historical import produces no
   scores.
4. **A published scorecard exists** whose scope covers the channel and the people.
   No published scorecard means no evaluations at all.

Report which of these you checked. "The upload worked" and "the calls are being
evaluated" are different claims.

## Present results to the user

1. **Region and organization** you uploaded to, stated before anything else.
2. **Planned vs applied vs skipped**, with the `--max-changes` bound named.
3. **Validation findings from the dry run** — missing files, unsupported formats,
   oversized files, agent emails not on the roster, suspected transposed
   metadata. These are the findings worth acting on *before* uploading.
4. **Verification results** — per-upload status after applying, and anything that
   did not land.
5. **What remains** — how many calls are left in the manifest and the command to
   continue.
6. **Whether the calls will actually be evaluated**, or which of the four gates
   above you could not confirm.
