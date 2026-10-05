---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "connector"
skill_id: "pdf-evidence-export"
title: "PDF Evidence Export Connector Skill"
risk_area:
  - trade
  - evidence
human_review_required: true
final_decision_allowed: false
paid_source_boundary: true
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# PDF Evidence Export Connector Skill

## Purpose

Export AML evidence and working notes into PDF files that can be retained, reviewed and linked to a case record.

## When to Use

Use when the AML workflow requires evidence to be saved as a PDF, including no-match results, potential hits, search results, website review pages, registry records and review summaries.

## Required Inputs

- case identifier;
- subject name or entity name;
- source name;
- check type;
- output folder;
- date of check;
- evidence content or captured page.

## Workflow

1. Confirm the subject and source.
2. Confirm whether the PDF is evidence, a draft report or a working note.
3. Export to PDF without removing material source context.
4. Include date of check and source reference where possible.
5. Save using the file naming rule.
6. Record the PDF in the evidence log.
7. Link the PDF to the relevant checklist item.

## Output Types

- source result PDF;
- search result PDF;
- website page PDF;
- registry evidence PDF;
- draft AML report PDF;
- manual review package PDF.

## Agent Must Not

- present PDF export as final human decision;
- overwrite previous evidence without versioning;
- remove source identifiers;
- hide failed or incomplete exports.
