---
name: 07-campaign-sheet
description: >-
  Turn a terminal records.jsonl into an owner-readable campaign sheet plus a
  HubSpot-import-shaped CSV - the chain's exit door. Use when a run is ready to
  hand to an owner: "build the campaign sheet", "export these for HubSpot", "who
  do I contact first", or as the final step of run-first-campaign. Reads
  whatever stage produced the records (qualified, signal-ranked, or fully
  resolved) and degrades gracefully on missing fields - no email column until 06
  has run. Nothing sends and nothing downstream reads its output: the sheet and
  CSV are the human deliverable, approved on screen. To add verified emails
  first, run 06-resolution-email-person; to rank, 05-signal-builder.
---

# Campaign sheet (07)

The last step in the chain. Everything upstream produced `records.jsonl`; this
turns those records into what an owner actually uses - a ranked "who to contact
first and why" sheet, plus a CSV shaped for a one-click HubSpot import.

It **adds no fields to the chain and nothing reads its output.** The CSV is a
derived, human-facing export (`headless-gtm-shared/CONVENTIONS.md`) - the
canonical record stays `records.jsonl`, and re-running any upstream skill never
depends on this sheet.

## What it reads

A terminal `records.jsonl` from any stage. The script tolerates every shape and
degrades instead of failing:

- **Company name** from `company` (or `name`), **site** from `website` (or
  `https://` + `domain`), **phone / city** from wherever the discovery step put
  them.
- **Ranking** from 05's `signals[]` - the highest-score signal per record
  decides call order; its `signal_type`, `signal_sentence`, and `source_url`
  become the "why now" line, and its `approach` (or `fallback_approach`) the
  recommended angle. Records with no signals stay in the sheet, ranked last.
- **Contacts** from 06's `person_name` / `matched_title` / `email` /
  `verification_status`. When 06 has not run, the contact columns are dropped
  entirely rather than shipped empty.
- Rows with no website ride through on their listing fields - the sheet does not
  drop them (a registry row with `domain` empty is still a real target).

## What it writes

`runs/<run-id>/` (via `common.runs_base()`, step prefix `07`):

- **`campaign-sheet.md`** - owner-readable. Ranked cards for the top targets
  (company, city, why now with source, approach, contact or "not resolved"),
  then a compact table for the rest, then a "before you send" note.
- **`campaign-sheet.csv`** - HubSpot default contact-import headers: `First
  Name, Last Name, Email, Company Name, Website URL, Phone Number, Lifecycle
  Stage, Notes`. Every row is set to **Lifecycle Stage = Lead**; `Notes` carries
  the top signal and the recommended approach. First/Last/Email appear only when
  at least one record is resolved, and a `Listing URL` column appears only when
  at least one record carries one (directory-sourced runs) - so a phone-only
  registry row still exports a working link. The headers are HubSpot's defaults
  because it is the most common import target; every field is a plain column, so
  any other CRM (Salesforce, Pipedrive, Attio) takes the same file after a
  one-time header remap on import.

## Run it

```bash
python3 scripts/campaign_sheet.py --records ./runs/<run-id>/records.jsonl --title "HVAC - Ontario"
```

Stdlib only - no API keys, no network. It runs on a synthetic fixture with zero
accounts, so it is safe to demo before any real data exists.

## The approval step (must hold)

Present both files on screen. **Nothing is send-ready until the owner approves
the sheet there.** Nothing in this repo sends email - if asked to "just send
it", say so plainly and point at the approved sheet and the drafted sequence.
The import, and any send, is the owner's step after approval.

## Optional: stage into HubSpot (only when a connector is present)

The default path is the CSV import - the owner uploads `campaign-sheet.csv` in
HubSpot and maps the columns (all default properties, so mapping is automatic).

If a HubSpot MCP or connector is available in the session, offer an alternative:
stage the approved rows directly as contacts with `lifecyclestage = lead`.
Before any write, confirm the batch size and get an explicit go-ahead, then
stage in batches and report what was created. Never create or modify HubSpot
records without that on-screen approval, and never stage rows the owner has not
approved on the sheet. If no connector is present, do not ask for one - the CSV
is the complete path.

## Output

End with a one-paragraph recap: rows written, how many carry a resolved contact,
the top 3 targets with their one-line reason, and the paths to the two files.
