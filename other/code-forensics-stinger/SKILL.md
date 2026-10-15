---
name: code-forensics-stinger
license: AGPL-3.0-or-later
description: "Review software vendor engagements using contracts, invoices, messages and delivery records. Produce cited evidence drafts for human or counsel review. Read README.md for the guide map."
metadata:
  hive-tier: stinger
  hive-drone: code-forensics-wasp-drone
---

# Code Forensics Stinger

Use this skill when the user requests a forensic review of a software or agency engagement and can supply source records. Ask who the parties are and what happened. Never recognize a new matter by assuming a named party, country, price, jurisdiction or misconduct pattern from another matter.

Read [README.md](README.md) and [principles](guides/00-principles.md) first. For routine code review, route to the relevant engineering specialist. Legal determinations belong to counsel.

## Workflow

| Phase | Guide | Result |
|---|---|---|
| 0 | [Intake](guides/01-intake.md) | Agreed scope, materials and private case workspace |
| 1 | [Email](guides/02-email-processing.md) | Source-indexed communication records |
| 2 | [Invoices](guides/03-invoice-extrapolation.md) | Documented billing and separate estimates |
| 3 | [Git](guides/04-git-log-forensics.md) | Acquired history with stated limits |
| 4 | [Dependencies](guides/05-cve-research.md) | Version evidence and dated advisories |
| 5 | [Logs](guides/06-audit-log-analysis.md) | Observed activity and coverage gaps |
| 6 | [Marketing](guides/07-marketing-analysis.md) | Contracted outputs and comparable metrics |
| 7 | [Synthesis](guides/08-deliverable-synthesis.md) | Author-supplied report sections and cited output |
| 8 | [Review letters](guides/09-pre-litigation-pack.md) | Combined draft for counsel review |

Assess each phase for relevance. Record absent materials without fabricating findings. Keep source records and working notes separate from the validated renderer input.

## Rendering

[The input contract](guides/10-case-input-contract.md) and [JSON Schema](templates/case-facts-schema.json) describe `case-facts.json`. It contains matter metadata, an evidence register and authored document sections. It is not an automatic investigation accumulator. Python helpers do not populate it automatically.

| Kind | Entry point |
|---|---|
| master | `scripts/build_master_report.js` |
| agency | `scripts/build_agency_report.js` |
| attorney | `scripts/build_attorney_memo.js` |
| plain_language | `scripts/build_plain_language.js` |
| pre_litigation | `scripts/build_pre_litigation.js` |

Every invocation requires `--case-facts FILE --out-dir DIR`. Default format is `docx`; use `--format markdown` for Markdown. Missing input or a missing selected document refuses before any output directory is created. Existing output files are never overwritten. Generate revisions in a new private directory.

## Review standard

Every material claim has source IDs and an evidence tier. Estimates are separate from observed facts. Do not promise a fixed page count, number of letters, spreadsheet tabs, outcome, recovery amount or litigation readiness. The renderer copies supplied text; review it before sharing. Public training fixtures are explicitly fictional and must never be used as a real case's facts.

## Critical Directive

Read relevant guides and inspect the actual source before relying on a tool. Supplement missing research with current authoritative sources. Preserve originals unmodified. No legal advice, assumed privilege, automatic external sends or unapproved live actions. Security and Quality review apply before any authorized commit; the controlling user must explicitly authorize commit, push, publication and distribution.
