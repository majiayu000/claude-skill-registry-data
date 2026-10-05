---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "connector"
skill_id: "browser-screenshot-capture"
title: "Browser Screenshot Capture Connector Skill"
risk_area:
  - evidence
human_review_required: true
final_decision_allowed: false
paid_source_boundary: false
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# Browser Screenshot Capture Connector Skill

## Purpose

Capture browser-based evidence for AML review in a way that is reproducible and human-reviewable.

## When to Use

Use when an AML workflow requires a visual record of a web page, search result, registry page, sanctions result, adverse media result, website page, domain lookup or source document.

## Required Inputs

- case identifier;
- subject under review;
- source URL or page title;
- reason for capture;
- output folder;
- date/time if available.

## Workflow

1. Verify that the page relates to the correct subject or source query.
2. Capture the visible page area required by policy.
3. If the result spans multiple pages, capture each material page separately.
4. Ensure the URL/address bar or source identifier is visible where technically possible.
5. Save the screenshot using the implementation profile naming rule.
6. Add an entry to the evidence log.
7. Mark whether the capture is complete, partial or limited.

## Evidence Metadata

Record:

- source name;
- URL or source identifier;
- access date;
- query/search term;
- screenshot file name;
- evidence quality label;
- limitations.

## Red Flag Routing

The screenshot connector does not decide whether a finding is material. If the captured page contains a red flag under the selected AML skill or implementation profile, route the case to manual review.

## Agent Must Not

- crop out material context;
- edit or enhance evidence in a way that changes meaning;
- summarize a screenshot as a final compliance decision;
- omit visible uncertainty.
