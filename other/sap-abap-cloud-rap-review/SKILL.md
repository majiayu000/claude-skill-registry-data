---
name: sap-abap-cloud-rap-review
description: Review ABAP Cloud and RESTful ABAP Programming Model (RAP) artifacts for clean-core compliance, released API usage, behavior definition and implementation correctness, CDS view design, BDEF modeling quality, authorization object coverage, and ABAP unit test completeness. Use when assessing RAP business objects on S/4HANA Cloud or BTP ABAP Environment. Does not touch live systems.
allowed-tools: Read Grep Glob WebSearch WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-19"
  category: architecture
  lifecycle: experimental
---

# SAP ABAP Cloud RAP Review

## Purpose

Assess the design, correctness, and clean-core compliance of ABAP Cloud and RESTful ABAP Programming Model (RAP) artifacts. Review CDS view hierarchies for correct view type usage (interface, projection, consumption). Review Behavior Definition (BDEF) design for correct implementation type selection (managed vs. unmanaged), draft enablement, authorization master/dependent assignment, and association exposure. Review Behavior Implementation (ABAP classes) for authorization object checks, action implementations, validation completeness, and forbidden language constructs. Assess released API consumption: confirm only C1/C2 released objects are used. Review ABAP unit tests for behavior test double usage, test isolation, and rollback patterns. Does not connect to or mutate any live ABAP system.

## When to use

Use this skill when the user asks to:

- review CDS view definitions for correct view type (data definition, projection, consumption) and annotation completeness (metadata extensions, UI, search, access control),
- assess Behavior Definition (BDEF) design: managed vs. unmanaged selection, draft enablement, alias assignment, feature control, action and function declarations, association exposure,
- review Behavior Implementation classes (ZBP_*) for authorization object checks (`AUTHORITY-CHECK`), action method completeness, validation messages, and determination logic,
- verify released API compliance: confirm only objects with C1 or C2 release contracts are used; flag any consumption of NOT_RELEASED or DEPRECATED SAP objects,
- assess ABAP Cloud tier compliance: identify forbidden language constructs (dynamic SQL, classic OPEN SQL with client-dependent access, direct access to SAP internal tables),
- review ABAP unit test quality: behavior test doubles (`if_abap_behv_test_environment`), CDS test environment (`if_cds_test_environment`), test class isolation, and `ROLLBACK ENTITIES` teardown,
- evaluate RAP business object composition: root vs. child entity hierarchy, composition relationships, UUID-based key design, ETag handling, and total ETag vs. field-level ETag selection.

## When not to use

- When the request is about CAP (Node.js/Java) side-by-side extensions on BTP — use `sap-cap-architecture-review`.
- When the request is about legacy ABAP custom code (Z/Y programs, function modules, classic user exits) rather than RAP objects — use `sap-clean-core-debt-review`.
- When the request requires live ABAP system access, SE80 navigation, or ABAP Test Cockpit execution — this skill accepts only user-provided ABAP source code, CDS DDL files, BDEF definitions, or written descriptions.
- When the request is about Integration Suite or API Management configuration — use `sap-integration-suite-review`.

## Does not touch live systems

This skill operates on user-provided ABAP source code snippets, CDS DDL source, BDEF source, metadata extension files, access control definitions, or written descriptions of the RAP object model. It does not connect to any ABAP system, ABAP Development Tools (ADT), SAP S/4HANA system, or BTP ABAP Environment tenant. All live inspection is out of scope.

## Lean operating rules

- Classify findings before recommending. Every finding must be assigned to a review domain (CDS Views / BDEF / Behavior Implementation / Released API Compliance / ABAP Unit Tests / Object Composition) before remediation is proposed.
- Released API compliance is non-negotiable in ABAP Cloud. Any ABAP Cloud object that consumes a NOT_RELEASED SAP object is non-compliant. This is a `high` finding with upgrade-blocking risk.
- Authorization checks must be implemented in the authorization master. For a RAP business object with `authorization master ( global )`, the `CHECK_AUTHORIZATION` method in the behavior implementation class must perform `AUTHORITY-CHECK` for every relevant operation. An absent or pass-through `AUTHORITY-CHECK` simulation left from development is a `critical` finding in production-bound code.
- Managed RAP is preferred for greenfield transactional objects. An unmanaged RAP implementation for a new transactional business object without explicit justification (e.g., wrapping a legacy function module) is a `medium` finding.
- Draft must be explicitly enabled in the BDEF. A RAP business object that requires Fiori Elements draft editing but lacks `with draft;` in the BDEF and `draft table` configuration in the CDS view is a `high` finding for UI correctness.
- ABAP unit tests must use test doubles, not live data. Test methods that execute `MODIFY ENTITIES` or `READ ENTITIES` against a live ABAP system database without a test double environment are `high` findings for test isolation.
- `ROLLBACK ENTITIES` is required in test teardown. An ABAP unit test class for a RAP business object that modifies test data without `ROLLBACK ENTITIES` in `teardown` is a `medium` finding.
- Evidence from official SAP ABAP Cloud and RAP documentation takes precedence over inference.
- Load only the reference needed for the component in scope.

## Evidence rules

Label all claims with one of:

- `documentation-based` — grounded in official SAP ABAP Cloud docs, SAP RAP documentation (help.sap.com/docs/abap-cloud), or SAP Help Portal
- `user-provided evidence` — ABAP source code, CDS DDL definitions, BDEF source, access control definitions, or written descriptions provided by the user
- `context7-supplementary` — grounded in RAP openSAP sample code from Context7 (supplementary to official SAP docs; applies for authorization implementation patterns and ABAP unit test patterns)
- `inference` — derived reasoning not directly confirmed by official docs or user evidence

## Live-environment rules

**This skill does not touch live systems.** There is no ABAP system RFC connection, ADT API call, SAP S/4HANA OData service call, or BTP ABAP Environment tenant access in this skill's execution path. Users must supply ABAP source code, CDS DDL source, BDEF definitions, or written descriptions for this skill to review.

## References

Load only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — review domain taxonomy, severity classification, output format.
- [Safety checklist](references/safety-checklist.md) — non-negotiables, common RAP mistakes, when to push back.
- [Official sources](references/official-sources.md) — SAP ABAP Cloud docs, RAP documentation, released API references, ABAP unit testing.
- [Context7 framework docs](references/context7-framework-docs.md) — RAP authorization implementation and ABAP unit test patterns (supplementary; applies for behavior implementation and test design).

## Response minimum

Return, at minimum:

- **Problem classification**: review domain(s) in scope and specific finding(s) per domain.
- **Evidence used**: documentation-based / user-provided evidence / context7-supplementary / inference.
- **Risk level**: critical (security or data integrity risk) / high (correctness, upgrade-blocking, or operational risk) / medium (governance or maintainability gap) / low (best practice deviation).
- **Recommended action**: specific remediation per finding (add `AUTHORITY-CHECK`, add `with draft;` to BDEF, replace NOT_RELEASED object with C1 equivalent, add `ROLLBACK ENTITIES` to teardown, etc.).
- **Refusal / escalation triggers**: if live ABAP system access, ATC execution, or ADT navigation is required to complete the review, state that clearly and do not proceed.
- **Business impact**: upgrade-blocking risk, security exposure, Fiori UI correctness failure, or test reliability gap.
- **Next verification step**: validate released API candidates against current SAP API Business Hub release contracts; validate forbidden construct findings against the ABAP Cloud 2.0 tier list for the target system version.
