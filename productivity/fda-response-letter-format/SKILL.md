---
name: fda-response-letter-format
description: Format and content for sponsor responses to FDA correspondence — information requests, Complete Response Letters (CRL), Refuse-to-File (RTF) and 510(k) additional-information letters — including the cover letter block and point-by-point response structure. Use when asked to draft, structure or pre-check a response to an agency letter, routing deficiency lookups, pre-mortems and drafts through the Concept2Cure connector.
---

# FDA response-letter format

An agency response is a governed document. This skill gives you the format;
the connector gives you the deficiency patterns, the pre-mortem and the
drafts. Every response is a DRAFT until a named person reviews and files it in
Concept2Cure.

## Structure of a response submission

1. **Cover letter** (Module 1.2 for eCTD; the 510(k) cover letter for CDRH):
   sponsor letterhead, date, application number (IND/NDA/BLA/K-number),
   product name, submission type (`Response to Information Request dated …`,
   `Complete Response Resubmission`, `Response to RTF`), FDA contact and
   division, a one-paragraph summary of what is enclosed, a table mapping each
   agency item to the section of the response, and a signature block. Draft it
   with `c2c_draft_cover_letter` (deterministic) and surface its
   `missingSections` before anyone signs.
2. **Point-by-point response**: reproduce each agency comment verbatim and
   numbered as the agency numbered it, then the sponsor response, then the
   supporting documents and their eCTD location. Never merge or reorder agency
   items.
3. **Supporting documents** filed at their CTD sections (new or replace
   leaves), with the cover letter table pointing to each.

## The response paragraph

* Open with the direct answer (agree / agree with modification / disagree with
  rationale).
* State the evidence with its exact location (study, table, page, eCTD leaf).
* State the change made to the application (section, what changed, lifecycle
  operator) — or that no change is proposed and why.
* Close with what remains open, if anything, and the proposed path.

## Workflow with the connector

1. **Classify the letter**: `c2c_lookup_submission_deficiencies` for the
   application type (`nda`, `bla`, `510k`, …); match each agency item to a
   pattern and note severity and the reviewer language the taxonomy records.
2. **Pre-mortem the draft response** before the meeting:
   `c2c_run_crl_premortem` on each response section with `submission_type`
   and `agency`. Report the findings, reviewer questions and remediation
   verbatim; report the precedent denominator and confidence as returned — a
   cold corpus is a fact, not a gap to fill.
3. **Draft the narrative**: `c2c_draft_agency_response` with the agency item
   verbatim and the verified facts. If the tool refuses (no provider
   configured), tell the user and stop; do not write the narrative from
   memory of the facts alone as if it were the governed draft.
4. **Draft the cover letter**: `c2c_draft_cover_letter`.
5. **File for review**: `c2c_file_draft_for_review` places each response
   document into the response sequence; a human freezes and signs in
   Submission Center.

## Things you must not do

* Invent a study result, table number or date to complete a response.
* Characterise the agency's position beyond the letter's text.
* Present a pre-mortem probability as a prediction when the artifact status is
  `not_assessed` or the precedent count is 0.
* Sign, freeze or transmit — the connector cannot, and neither can you.
