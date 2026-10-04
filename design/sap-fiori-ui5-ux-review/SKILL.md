---
name: sap-fiori-ui5-ux-review
description: Review SAP Fiori and SAPUI5 applications for Fiori design guidelines adherence, UI5 app structure and MVC correctness, OData consumption patterns, performance, accessibility, and Fiori launchpad integration. Use when assessing Fiori app code, manifest.json, XML views, controllers, OData model binding, or launchpad tile configuration for quality, compliance with SAP UX standards, and readiness for productive use. Does not touch live systems.
allowed-tools: Read Grep Glob WebSearch WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-19"
  category: platform
  lifecycle: experimental
---

# SAP Fiori and UI5 UX Review

## Purpose

Assess the quality, correctness, and SAP UX standards compliance of SAP Fiori and SAPUI5 applications. Review app structure for correct MVC separation, component configuration, and manifest.json completeness. Assess XML views, controllers, and fragment design for UI5 best practices. Evaluate OData V2 and V4 model binding for correct consumption patterns, error handling, and batch request strategy. Review adherence to SAP Fiori design guidelines including floorplan selection, responsive design, and accessibility. Assess Fiori launchpad integration: tile configuration, navigation intent, target mapping, and app descriptor correctness. Does not connect to or mutate any live UI5 app runtime, BTP system, or backend OData service.

## When to use

Use this skill when the user asks to:

- review a Fiori app's `manifest.json` (app descriptor) for completeness: data sources, routing configuration, model declarations, component settings, and library dependencies,
- assess UI5 XML view and fragment design: view nesting correctness, control usage compliance with Fiori design guidelines, missing aggregation bindings, and layout anti-patterns,
- evaluate controller code: MVC separation of concerns, correct lifecycle hook usage (`onInit`, `onExit`, `onBeforeRendering`, `onAfterRendering`), event handler design, and controller extension patterns,
- review OData V2 or V4 model consumption: binding paths, batch mode configuration, read/write operation patterns, error handling in `ODataModel`, and filter/sort expression correctness,
- assess Fiori design guideline adherence: correct floorplan selection (List Report, Object Page, Overview Page, Worklist, Wizard), SAP Fiori Elements usage versus freestyle compliance, header and footer bar patterns,
- review accessibility compliance: ARIA landmark usage, labeling of form fields and tables, keyboard navigation support, high-contrast theme compatibility, and screen reader compatibility of custom controls,
- evaluate Fiori launchpad integration: tile configuration, semantic object and action definition, target mapping correctness, cross-application navigation intent, and app descriptor `sap.app` and `sap.ui5` section completeness,
- identify UI5 performance issues: synchronous loading of UI5 modules, missing `async` component loading, oversized initial payload, missing lazy loading for non-critical views, and unoptimized OData batch grouping.

## When not to use

- When the request is about the CAP backend service layer providing OData — use `sap-cap-architecture-review`.
- When the request requires live UI5 app inspection, BTP cockpit access, or Fiori launchpad configuration execution — this skill accepts only user-provided code artifacts, manifest files, and written descriptions.
- When the request is about ABAP-side OData service implementation (CDS views, SEGW service builder, RAP) rather than the UI5 consumer side — use the appropriate ABAP review skill.
- When the request is about SAP Build Work Zone configuration (site-level configuration, workspace templates) rather than individual app quality.

## Does not touch live systems

This skill operates on user-provided UI5 source files, `manifest.json`, XML views, controller code, fragment files, OData metadata documents (`$metadata`), launchpad tile descriptors, or written descriptions of the Fiori app. It does not connect to any UI5 app runtime, BTP subaccount, ABAP backend, or Fiori launchpad configuration service. All live inspection is out of scope.

## Lean operating rules

- Classify findings by review domain before recommending. Every finding must be assigned to a domain (App Structure / XML View / Controller / OData Consumption / Fiori Design / Accessibility / Launchpad / Performance) before a remediation path is proposed.
- Fiori design guideline adherence is a first-class concern. A Fiori app that deviates from the correct floorplan for its use case (e.g., using a custom freestyle layout where a List Report or Object Page is the correct pattern) is a `medium` finding. A Fiori app missing required header or footer bar patterns for its floorplan is a `high` finding.
- Asynchronous component loading is required. A UI5 component that does not declare `async: true` in its `manifest.json` component settings, or that uses synchronous `sap.ui.require` calls in controllers, is a `high` performance finding.
- OData error handling is required. A controller that calls `ODataModel.read()`, `ODataModel.create()`, or `ODataModel.update()` without an `error` callback is a `high` finding for operational reliability.
- Accessibility is not optional. Missing ARIA labels on interactive controls, form fields without associated labels, and tables without column headers or row headers are `high` accessibility findings.
- Direct DOM manipulation in controllers is a `high` finding. Accessing `document.getElementById()` or jQuery DOM selectors in UI5 controllers bypasses the UI5 rendering lifecycle and breaks testability.
- Evidence from official SAP Fiori design guidelines, SAPUI5/OpenUI5 documentation, and user-provided artifacts takes precedence over inference.
- Context7-sourced SAPUI5/OpenUI5 documentation is supplementary to official SAP sources. Label it `context7-supplementary`.
- Load only the reference needed for the review domain in scope.

## Evidence rules

Label all claims with one of:

- `documentation-based` — grounded in official SAP Fiori design guidelines, SAPUI5 API documentation, or SAP Help Portal
- `user-provided evidence` — manifest files, XML views, controller code, fragment files, OData metadata, tile descriptors, or written descriptions provided by the user
- `context7-supplementary` — grounded in SAPUI5/OpenUI5 framework documentation fetched from Context7 (supplementary to official SAP Fiori and SAPUI5 docs; applies for MVC patterns, OData model usage, and component configuration)
- `inference` — derived reasoning not directly confirmed by official docs or user evidence

## Live-environment rules

**This skill does not touch live systems.** There is no UI5 app runtime API call, BTP subaccount access, ABAP backend OData request, Fiori launchpad configuration service call, or BTP cockpit session in this skill's execution path. Users must supply UI5 source files, manifest files, controller code, XML views, OData metadata documents, or written descriptions of their Fiori app for this skill to review.

## References

Load only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — review domain taxonomy, severity classification, output format.
- [Safety checklist](references/safety-checklist.md) — non-negotiables, common Fiori and UI5 review mistakes, when to push back.
- [Official sources](references/official-sources.md) — SAP Fiori design guidelines, SAPUI5 API docs, Fiori launchpad, OData consumption guides.
- [Context7 framework docs](references/context7-framework-docs.md) — SAPUI5/OpenUI5 MVC patterns, OData model binding, component configuration, and accessibility (supplementary; applies for this skill).

## Response minimum

Return, at minimum:

- **Problem classification**: review domain(s) in scope and specific finding(s) per domain.
- **Evidence used**: documentation-based / user-provided evidence / context7-supplementary / inference.
- **Risk level**: critical (security or data integrity risk from UI5 app) / high (functional, operational, or accessibility failure) / medium (Fiori design deviation, maintainability gap) / low (best practice deviation or code quality concern).
- **Recommended action**: specific remediation per finding (add `async: true`, implement OData error callback, add ARIA label, correct floorplan pattern, fix routing configuration, etc.).
- **Refusal / escalation triggers**: if live UI5 runtime access, BTP deployment, or ABAP backend inspection is required to complete the review, state that clearly and do not proceed.
- **Business impact**: user experience degradation, accessibility compliance failure, performance regression, launchpad integration failure, or OData consumption reliability risk.
- **Next verification step**: validate recommended changes against the target SAPUI5 version, Fiori launchpad configuration, and connected OData service metadata before deploying.
