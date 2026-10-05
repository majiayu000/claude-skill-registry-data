---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "core"
skill_id: "TCAML-S006"
title: "Trade & Goods Restriction Review"
risk_area:
  - trade
  - escalation
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
# TCAML-S006: Trade & Goods Restriction Review


## Purpose

TCAML-S006 defines how an AML agent should assist with the review of goods, services, HS codes, tariff codes and trade restriction indicators.

The agent prepares structured evidence for human review. It does not make legal, customs, sanctions or export-control determinations.

## When to Use

Use this skill when a case includes:

- import or export activity;
- cross-border sale of goods;
- goods or services that may be sensitive;
- HS code / tariff code / CN code / commodity code;
- invoices, contracts or shipping descriptions;
- counterparties in higher-risk jurisdictions;
- unclear goods descriptions;
- trade-based money laundering indicators;
- policy requirement for goods-code review.

## Agent May

- extract goods descriptions from forms, invoices or contracts;
- identify missing trade inputs;
- search approved trade restriction sources;
- compare code and description consistency;
- capture evidence;
- summarize possible restriction indicators;
- prepare a manual review package.

## Agent Must Not

- classify goods as legally permitted or prohibited;
- make export-control conclusions;
- determine sanctions applicability;
- replace customs, legal or MLRO review;
- invent HS codes;
- ignore uncertainty in goods descriptions.

## Required Inputs

- subject/customer name;
- goods or service description;
- code, where available;
- origin country, where available;
- destination country, where available;
- counterparty name, where available;
- transaction direction;
- source document reference;
- implementation profile or policy rule.

## Workflow

1. Confirm whether trade review is in scope.
2. Extract goods/services description and codes from source documents.
3. Mark missing inputs.
4. Search approved trade restriction or tariff sources.
5. Compare code and goods description.
6. Capture source evidence.
7. Identify possible red flags.
8. Prepare summary and limitations.
9. Route to manual review when policy requires or when indicators are present.
10. Update the client master checklist.

## Risk Indicators

- restricted or dual-use goods indicators;
- unclear or generic goods description;
- mismatch between code and description;
- high-risk origin, destination or transit country;
- counterparty exposure to high-risk sectors;
- inconsistent invoice, contract or shipping data;
- repeated changes in goods description;
- missing code where policy requires it;
- source result requiring interpretation.

## Evidence Requirements

For every source checked, record:

- source name;
- code searched;
- goods description searched;
- date;
- source jurisdiction or regime;
- result summary;
- evidence reference;
- confidence and limitation note;
- manual review requirement.

## Confidence

Use `Low` when:

- code is missing;
- goods description is vague;
- sources conflict;
- relevant jurisdiction is unclear;
- result requires legal interpretation.

Use `Medium` when:

- code and description align;
- at least one reliable source was checked;
- no material source conflict is observed;
- some inputs remain incomplete.

Use `High` only when:

- required inputs are complete;
- source evidence is captured;
- no material conflict is observed;
- the output remains limited to human-reviewable findings.

## Output

The output should include:

- case summary;
- goods/service table;
- source checks;
- possible restriction indicators;
- red flags;
- missing information;
- evidence references;
- confidence;
- human review routing.
