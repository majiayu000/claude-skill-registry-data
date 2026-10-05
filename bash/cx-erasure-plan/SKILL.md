---
name: cx-erasure-plan
description: Use to build a data-subject erasure plan for support conversations — GDPR right to erasure, CCPA deletion, right to be forgotten. Trigger for "delete this customer's data", DSR or SAR erasure request, GDPR deletion from our helpdesk, redacting personal data from tickets, or working out what can and cannot be erased.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Building a data-subject erasure plan

> **Operational guidance, not legal advice.** Whether erasure applies, what
> exemptions exist, and what you must retain are jurisdiction- and
> sector-specific. Have compliance review the plan before anything is applied.

Read-only. It produces a plan for review; a platform mutation skill applies it.

## The two distinctions that determine everything

Most erasure implementations get one of these wrong, and both failures are
serious in opposite directions.

**1. Is the subject the requester, or merely mentioned?**

| | Remedy |
| --- | --- |
| Subject is the **requester** — it is their conversation | You may erase the record |
| Subject is **mentioned** in someone else's conversation | **Redact the mention only. Never delete.** |

Deleting another customer's conversation because this subject appears in it
destroys a different data subject's record and your own legitimate business
record. This plan never proposes it, and the applier refuses it even if the plan
is hand-edited.

**2. Is the conversation open or closed?**

On Zendesk — and similarly elsewhere — **comments in a closed conversation cannot
be redacted at all.** Most erasure requests land on closed conversations, so this
is not an edge case, it is the common case.

That produces a four-way matrix, and one cell has no automated remedy:

| | Open / solved | Closed |
| --- | --- | --- |
| **Requester** | Redact the identifying text | Delete the whole conversation — the only option |
| **Mentioned** | Redact the mention | **No remedy. Escalate to compliance.** |

The bottom-right cell is a genuine dead end: you cannot redact (closed) and you
must not delete (someone else's record). This plan surfaces those explicitly as
`manual_review` rather than silently dropping them — which is what a naive
process does, and what turns into a finding later.

## Usage

```bash
node scripts/build-erasure-plan.mjs ./out/zendesk \
  --subject-id u_9001 \
  --subject-email jo@example.com \
  --subject-phone "+442079460958" \
  --legal-hold-file ./holds.txt
```

Input is a canonical export from any platform export skill, so this works
identically across every supported helpdesk.

**Arguments**

- `--subject-id <id>` / `--subject-email <email>` / `--subject-phone <number>` —
  repeatable. Supply **every** identifier you know.
- `--subjects-file <path>` — one identifier per line, type inferred.
- `--legal-hold-file <path>` — conversation ids that must not be erased.
- `--out <dir>` — where to write `erasure-plan.jsonl`. Default `./plans`.

**Message bodies are required.** Without them, mentions in other customers'
conversations are invisible and the plan is incomplete. The script says so when
`messages.jsonl` is missing.

Phone matching compares digits only, so `+44 20 7946 0958` matches
`020 7946 0958`. Email matching is case-insensitive but returns the **exact
literal** as it appears, because redaction APIs take a literal string — a
normalised form would match nothing.

## Legal hold overrides erasure

Retention obligations normally take precedence over an erasure request. Supply
`--legal-hold-file` with anything under litigation hold, regulatory retention, or
an active dispute. Those entries are marked `blocked_legal_hold` and are never
applied.

If you do not have a hold list, that is itself a finding: you cannot safely honour
erasure requests without knowing what you are obliged to keep. Say so rather than
proceeding as if the list were empty.

## What erasure from the helpdesk does not cover

This is the most useful part of the plan, and the part most often missed. Erasing
from the helpdesk is **not** erasing from your business. The plan lists these
every run:

- **Attachments and inline images** — not text, not covered by comment redaction.
- **Voice recordings and transcripts** — separate storage, separate deletion path.
- **Your warehouse, BI tool, and any dbt models** built from conversation exports.
- **Canonical exports on disk**, including ones produced by this catalog.
- **Search indexes and caches**, which retain content after the source is redacted.
- **Backups and snapshots**, usually under a separate retention policy.
- **LLM fine-tuning sets, embedding stores, and RAG indexes.** Embeddings are
  derived personal data; deleting the source row does not remove the vector. This
  is the newest gap and the one least likely to be in an existing DSR runbook.
- **Downstream integrations** — CRM, marketing tools, Slack messages containing
  ticket text.
- **The original inbound email** in your mail provider.

A DSR response covering only the helpdesk is incomplete, and the gap is invisible
unless someone enumerates it. That is what this list is for.

## Reading the plan

```jsonc
{
  "conversation_source_id": "201",
  "action": "manual_review",        // redact_messages | delete_conversation
                                    // manual_review | blocked_legal_hold
  "subject_role": "mentioned",      // or "requester"
  "status": "closed",
  "reason": "Subject is mentioned in another customer's closed conversation…",
  "blocked": true,
  "redactions": [
    { "message_source_id": "900", "literals": ["jo@example.com"] }
  ]
}
```

Entries are sorted with the ones needing a human decision first, because those are
what a reviewer must not skim past.

## Present results to the user

1. **The blocked entries first** — `manual_review` and `blocked_legal_hold`, with
   reasons. These need a person, and burying them under a count of successes is how
   they get missed.
2. **The action breakdown**, and specifically **how many conversations can only be
   erased by deleting the whole record** because they are closed. That is a
   business decision (lose the operational record) rather than a technical one.
3. **Mentions vs requester counts.** State plainly that mentions are redact-only
   and that no flag permits deleting them.
4. **The out-of-scope list**, in full. Do not summarise it — each line is a system
   somebody has to go and handle separately.
5. **Matching limitations.** Literal matching misses nicknames, misspelt
   addresses, and unusually formatted numbers. This is a high-recall aid, not a
   completeness guarantee, and the DSR response should not claim otherwise.
6. **That nothing has been changed**, and that applying requires compliance
   sign-off.

Do not quote conversation content into chat. Reference ids only — the whole point
is to remove this person's data, not to copy it somewhere new.

## Troubleshooting

**No conversations matched a customer you know exists** — check the identifiers
against the export's `customer_id` values. A helpdesk user id is not an email.

**Only the subject's own conversations matched** — `messages.jsonl` is missing or
was exported with `--no-bodies`, so mentions could not be scanned.

**Everything is `manual_review`** — the conversations are closed and the subject is
a third party throughout. That is a real answer, and it means the request needs a
compliance decision rather than a script.

**A phone number was not found** — it may be written with a different country
prefix or embedded in other digits. Add the local-format variant explicitly.
