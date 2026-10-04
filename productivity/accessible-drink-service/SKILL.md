---
name: accessible-drink-service
description: Audit a pre-event drink-service journey from guest-stated preferences, supplied venue facts, communication formats, touchpoints, measurements, and current applicable official requirements. Use for approach, menu access, ordering, queues, payment, pickup, self-service water, seating, or restroom-route barriers. Exclude compliance certification, disability diagnosis, inferred needs, venue contact, physical verification, purchasing, modification, emergency-egress design, structural work, and electrical work.
---

# Accessible drink service

Trace each drink-service barrier to evidence and stop at a human review package.

The audit does not certify ADA or other legal compliance. It never diagnoses disability, infers a need from a condition, verifies a physical state, or changes a venue.

## 1. Confirm the audit boundary

Accept pre-event requests to review a guest journey through drink information and service.

Read [the high-risk handoff](references/high-risk-handoff.md) completely when a request asks for compliance certification, emergency-egress design, structural modification, electrical work, a load-bearing change, physical verification, guest or venue contact, purchasing, or execution.

Keep adjacent work outside this procedure.

- Station equipment placement belongs to a bar-station layout task.
- Drink selection and menu composition belong to menu planning.
- Medical interpretation belongs to a qualified health professional.
- Construction, code approval, and emergency planning require the responsible venue and qualified reviewers.

When an allowed audit and excluded work appear together, retain the evidence audit and mark every excluded action. If the request contains no auditable pre-event facts after exclusions, return `STOPPED: REVIEW AUTHORITY REQUIRED`.

Complete this step when the requested output is a pre-event guest-journey audit or the high-risk stop has fired.

## 2. Freeze the evidence register

Read [the source and status model](references/source-and-status-model.md) completely.

Record each input with its source, date, scope, and owner. Use `unknown` rather than filling gaps from a diagnosis, image, model memory, or another jurisdiction.

The minimum event record includes jurisdiction, venue type, public or private status, event date, service model, payment status, and applicable-rule status.

The journey record needs guest-stated preferences, menu formats, order methods, queue facts, payment touchpoint, pickup method, self-service water, seating facts, restroom route, staff assistance, supplied measurements, and venue review roles.

A guest's condition name is not an access preference. Preserve only the guest's stated format, route, assistance, timing, seating, or communication request.

Complete this step when every supplied fact has provenance and every missing field remains explicit.

## 3. Resolve legal applicability

For a US setting with a supplied determination that Title II or Title III applies, read [the US covered-setting branch](references/us-covered-settings.md) completely.

Do not decide whether a venue is covered. Treat a private setting, an uncertain US venue, or a non-US event as `UNRESOLVED LEGAL STATUS` unless current applicable requirements and a qualified reviewer are supplied.

Official guidance from one jurisdiction can inform a non-binding design discussion only when the output labels that use clearly. It cannot close the legal-status field.

Complete this step when each official requirement has a current source, jurisdiction, applicability record, and human reviewer, or the unresolved status appears as a readiness blocker.

## 4. Trace the guest journey

Read [the journey trace](references/journey-trace.md) completely.

Audit approach, entrance, menu discovery, ordering, queue or waiting, payment when present, pickup or handoff, water or self-service items, seating, restroom route, and departure.

For each touchpoint, compare the guest-stated preference or applicable official requirement with the supplied venue fact. Record `BARRIER TRACED` only when a mismatch has direct evidence.

Use `NO RECORDED BARRIER` when the supplied evidence shows no mismatch. This label is not a compliance finding and cannot replace missing facts.

Complete this step when every required touchpoint has a preference or requirement, a venue fact, a comparison, an evidence classification, and a review state.

## 5. Audit communication

For a covered US setting, apply the communication branch from [the US covered-setting reference](references/us-covered-settings.md). Elsewhere, use supplied guest preferences and current local requirements.

Separate menu receipt, question exchange, order confirmation, and pickup notification. A single alternative format does not prove that all four exchanges work.

Select no aid from a condition label. Match each proposed format to the guest's stated communication method, the nature and complexity of the exchange, and the venue's supplied capability.

Complete this step when every communication exchange has a primary format, a guest-requested alternative where supplied, an owner, and a human review state.

## 6. Compare physical facts

Use only measurements, photos, route descriptions, and seating facts supplied by a named source. The skill can compare a supplied measurement with a cited value, but it cannot confirm that the measurement or physical condition is accurate.

For covered US sales and service counters, use the values and service-equivalence limits in [the US covered-setting reference](references/us-covered-settings.md). Keep queue, route, self-service, and seating evidence separate.

Route emergency egress, ramp design, fixed-counter changes, wall or floor attachment, electrical installation, and load-bearing surfaces through [the high-risk handoff](references/high-risk-handoff.md).

Complete this step when every physical comparison names its measurement source, cited requirement or guest preference, uncertainty, and responsible reviewer.

## 7. Classify controls and proposed changes

Assign one record type to every audit item.

| Record type | Meaning |
|---|---|
| `GUEST-STATED PREFERENCE` | The guest supplied the requested access method |
| `OPERATIONAL CONTROL` | The venue supplied a current non-structural control |
| `PROPOSED CHANGE` | A draft adjustment awaits venue and guest review |
| `UNRESOLVED LEGAL STATUS` | Applicable law, coverage, or legal interpretation is missing |

A proposed change needs an owner, reviewer, deadline, evidence link, affected touchpoint, and implementation authority. The skill does not approve or execute it.

Complete this step when every barrier maps to a control, a draft change, or a blocked state without autonomous action.

## 8. Emit the review package

Read [the output contract](references/output-contract.md) completely and render every required section.

Use `READY FOR HUMAN REVIEW` when the audit record is complete, legal applicability is supplied, each barrier has a bounded response, every draft has an authorized reviewer, and no high-risk handoff remains unresolved.

Use `NOT READY: ACCESS REVIEW BLOCKERS` when a guest preference, venue fact, communication format, measurement, owner, current requirement, applicability decision, or qualified review is missing.

Use `STOPPED: REVIEW AUTHORITY REQUIRED` when the request reduces to certification, diagnosis, inference, physical verification, external action, or high-risk technical work.

Completion occurs when every journey touchpoint and evidence item appears in the audit, uncertainties remain visible, and no external or physical action has occurred.
