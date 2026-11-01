---
name: rfi-writer
description: "This skill should be used when the user provides an informal construction-site question — drawing/spec discrepancies, dimension conflicts, missing details — and needs a formal Request for Information (RFI) document filed in the project. Trigger on phrases like \"make an RFI\", \"draft an RFI\", \"send this as an RFI\", or pasted site questions implying transmittal to design consultants. Generates a numbered RFI markdown file in `docs/rfis/` and updates the project's RFI log."
license: MIT
metadata:
  title: "RFI Writer"
  summary: "Turn a site question into a filed, formal RFI"
  discipline: "construction-admin"
  tags: "Construction"
---


# RFI Writer


## Overview


Turn informal construction-site questions into formal RFI markdown files inside the user's architecture project. Each invocation produces a numbered RFI file in `docs/rfis/` and updates the running log so the team has a single source of truth for transmitted questions.


## Scope and limits — read first


**What this does.** Turns one field question into one numbered RFI in
`docs/rfis/`, routed to the discipline that owns the answer, with the
conflicting drawing or spec text quoted, and adds the row to the RFI log. The
number comes from the log rather than from counting.

**What this does not do.**

- **It does not invent a reference.** Drawing numbers, revision letters, spec
  sections, and prior RFI numbers are asked for when they are missing, never
  reconstructed from what a sheet is probably called.
- **It does not answer the question.** Proposing the answer inside the request
  is the habit this document exists to break.
- It does not send anything. The file is written and the log updated;
  transmitting through email, ACC, or Procore stays with you.
- It does not bundle. Several questions become several RFIs, because one RFI is
  one decision.
- It does not track responses, chase due dates, or price the impact of an
  answer. The log records what was asked and when it is due back.

**What you need before starting.** The field question, the drawing or spec text
it conflicts with, and who should answer it. Say whether the work is stopped:
that is what sets the response window.

## When to use


Trigger on:

- Pasted one-line site questions implying transmittal.
- Drawing/spec discrepancy descriptions.
- Field condition photos that need design clarification.
- Explicit requests ("make an RFI", "let's RFI this").

Do NOT trigger on general questions about RFI process, status checks, or formatting questions. For "how do RFIs work" or "show me my RFI log", answer directly without invoking this skill.


## Workflow


### Step 1 — Bootstrap if needed


Check whether `docs/rfis/RFI-log.md` exists. If not, run:


```bash
python scripts/init_rfi_workspace.py
```


This creates `docs/rfis/` and a fresh log file from `assets/RFI-log-template.md`. If the project lacks any `docs/` folder, confirm with the user before bootstrapping.


### Step 2 — Identify content


Pull these from the user's input. Read `docs/project.md` if it exists for project name, default discipline contacts, and team naming.

- **Subject**: Problem statement, not a question. ("Level 3 partition wall thickness discrepancy", not "what thickness?")
- **Discipline**: Architecture / Structural / MEP / Civil / Landscape / Interior. Use `references/discipline_routing.md` to map field topics to the responsible consultant.
- **References**: Drawing numbers (e.g. A-301 Rev.B), spec sections (validate codes against `references/csi_masterformat.md`), prior RFIs, addenda. Never invent drawing numbers — ask if missing.
- **Priority**: Critical (blocks today's work, 2-day response) / Standard (5-day) / Low (10-day).
- **Decision needed**: The single answer that unblocks the field.

If the user input contains multiple unrelated questions, split them into separate RFIs. One RFI = one decision.


### Step 3 — Get the next number


Run:


```bash
python scripts/next_rfi_number.py
```


The script parses `RFI-log.md` and prints the next zero-padded number (e.g. `007`). Use the printed value verbatim. Do not count by hand.


### Step 4 — Generate the RFI file


Read `assets/RFI-template.md`. Fill placeholders. Slugify the subject for the filename:


`docs/rfis/RFI-<NUMBER>-<slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, spaces → `-`, max 50 chars.


Use the Write tool to create the file.


### Step 5 — Update the log


Run:


```bash
python scripts/append_to_log.py \
  --number 007 \
  --subject "..." \
  --to "..." \
  --priority Standard \
  --due 2026-05-12 \
  --file RFI-007-partition-wall-thickness.md
```


The script appends a row to the markdown table and validates table integrity. Do NOT edit `RFI-log.md` directly with the Edit tool — table alignment breaks easily.


### Step 6 — Report


Tell the user:

- Path to the new RFI file
- Response-required date
- One-line summary

If `docs/project.md` mentions a transmittal process (email tool, ACC/BIM 360 module), surface that as the next step. Do not auto-send.


## Rules

- Subject is a problem statement, not a question.
- Description states facts and quotes conflicting drawings/specs verbatim.
- Request is unambiguous — the answer should be a single decision.
- One RFI = one decision. Split bundled questions into separate files.
- Never invent drawing/spec reference numbers. Ask if missing.
- Never auto-send the RFI. Generate the file and let the user transmit.

## Anti-patterns

- Adding pleasantries ("hope this finds you well"). RFIs are functional documents.
- Proposing the answer in the Request field. Asking and pre-answering is a CYA antipattern.
- Manually counting RFI numbers. Use the script.
- Editing `RFI-log.md` with the Edit tool. Use `append_to_log.py`.
- Bundling multiple decisions into one RFI.

## Resources

- `scripts/init_rfi_workspace.py` — bootstrap `docs/rfis/` with log template
- `scripts/next_rfi_number.py` — print next zero-padded RFI number
- `scripts/append_to_log.py` — append a row to the RFI log table
- `references/csi_masterformat.md` — common CSI MasterFormat division/section codes
- `references/discipline_routing.md` — map field topics to responsible consultant
- `assets/RFI-template.md` — RFI markdown template
- `assets/RFI-log-template.md` — log file template (used during bootstrap)
