---
name: navigation-wayfinding-accessibility-audit
description: Audits website and application navigation, orientation, and wayfinding for accessibility. Use when the user asks to review landmarks, skip links, menus, current-page indication, breadcrumbs, page titles, heading hierarchy, consistent navigation, route changes, browser back behavior, focus after navigation, deep links, search, mobile navigation, repeated blocks, or large application shells.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access; running-interface and assistive-technology access are needed to verify route, history, focus, and mobile behavior.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-auditors-and-product-teams
  tags:
    - accessibility
    - wcag
    - navigation
    - wayfinding
    - landmarks
    - skip-links
    - breadcrumbs
    - spa
    - mobile-navigation
    - usability
  status: draft
  side_effects: none
---

# Navigation and Wayfinding Accessibility Audit

## Purpose

Audit whether people can determine where they are, what is available, and how to move to or return from a destination across websites and applications. Report evidence-bounded accessibility findings, separate supported WCAG mappings from broader wayfinding observations, and do not claim complete WCAG conformance.

Use this skill independently or as a specialist in an inclusive-interface audit. When an orchestrator supplies scope, IDs, severity rules, or the shared finding contract, preserve them. When used independently, establish the same evidence ledger, scope, and contract below.

## When to use this skill

Use this skill when:

- A site, portal, documentation set, dashboard, or application needs a navigation, orientation, information-scent, or wayfinding review.
- The user asks about landmarks, skip links, navigation menus, current location, breadcrumbs, search, page titles, headings, or repeated page chrome.
- A multi-page or single-page application may lose location, focus, title, history, scroll position, or navigation context after route changes.
- Responsive or mobile navigation changes the available choices, menu model, hierarchy, or return path.
- A large application shell contains global, contextual, utility, account, workspace, or nested navigation.

Do not use this skill when:

- The request is only to implement a navigation component or redesign an information architecture.
- The primary concern is a menu's keyboard pattern, focus trap, dialog behavior, or screen-reader announcement timing; route those mechanics to `keyboard-focus-accessibility-audit` or `dynamic-interface-accessibility-audit` while retaining any orientation evidence.
- The task is limited to static semantic HTML, headings, landmarks, or ARIA with no wayfinding concern; use `semantic-structure-accessibility-audit`.
- The user requests a legal opinion, certification, or a complete WCAG conformance determination.

## Operating rules

- Review only. Do not alter routes, markup, history, or navigation content.
- Keep source, rendered-DOM, keyboard, assistive-technology, responsive, and user-research evidence distinct. A screenshot cannot prove landmark exposure, focus destination, history behavior, deep-link recovery, or screen-reader output.
- Audit a representative navigation system and its route families, not one attractive header in isolation. For large products, sample each distinct shell, navigation tier, permission model, responsive variant, and critical flow, then name expansion triggers.
- Test deep links, refresh, browser back and forward, cancelled navigation, error or not-found routes, and return paths where they exist. Do not infer history semantics from router code alone.
- Do not require every page to have breadcrumbs, search, an `h1`, a skip link, or multiple navigation schemes. Evaluate the actual structure, repeated blocks, task needs, and applicable WCAG conditions.
- Do not treat skipped heading levels, multiple `nav` elements, use of a custom menu, or an omitted breadcrumb as automatic WCAG failures. Establish the unmet requirement and user impact.
- Do not treat a WAI-ARIA Authoring Practices pattern deviation, sitemap absence, information-architecture preference, or browser-history inconvenience as a WCAG failure without a criterion-level basis.
- Base severity on user impact, task criticality, breadth, workaround quality, persistence, and harm—not WCAG conformance level.

## Inputs to inspect

Start with the smallest evidence set that covers the navigation model and representative journeys:

- Audit brief, critical tasks, route or sitemap inventory, supported devices and assistive technologies, requested WCAG version and level, roles, locales, and authenticated states.
- Page shells, route layouts, document metadata, router configuration, route guards, redirects, not-found and error routes, history utilities, scroll-restoration code, and analytics or telemetry that changes navigation.
- Components and styles for skip links, headers, `nav`, `main`, menus, drawers, tabs, sidebars, breadcrumbs, pagination, search, account or workspace switchers, and repeated promotional or utility blocks.
- Heading and title data, localization, CMS mappings, link labels, navigation configuration, role- and permission-dependent destinations, and feature-flag variants.
- Tests, route-transition recordings, browser traces, rendered DOM, accessibility-tree snapshots, keyboard notes, assistive-technology notes, screenshots, and user research when supplied.
- A running target with safe test accounts and data for first visit, deep link, refresh, back/forward, route failure, changed permissions, narrow viewport, menu open and closed, and search-result states.

Do not read an entire repository when route definitions, shared shells, representative templates, menu primitives, and tests establish the relevant behavior.

## Evidence model

| Evidence | Can support | Cannot establish alone |
|---|---|---|
| Source or configuration | Intended route graph, title and landmark markup, links, conditional destinations, history or focus code paths | Rendered DOM, computed accessibility data, actual focus, history behavior, scroll position, or spoken output |
| Screenshot or design | Visible grouping, labels, hierarchy, current-location cues, and captured responsive layout | Semantics, keyboard path, route transitions, deep-link recovery, or uncaptured states |
| Automated check | Implemented rules and machine-reported candidates in scanned states | Complete route, history, task, or assistive-technology coverage |
| Browser runtime | Actual destinations, URL and title changes, focus, keyboard path, history, scroll restoration, rendered semantics, and responsive state | Spoken output or equivalent behavior in untested technologies and settings |
| Assistive-technology test | Observed navigation, landmarks, links, headings, current state, and route feedback in the named setup | Results on untested browser, platform, version, mode, or user strategy |
| User research or support evidence | Observed wayfinding failures, terminology confusion, discovery strategies, and task consequences | Universal experience or WCAG conformance |

Record the route, state, role, viewport, browser, input or assistive technology, starting URL, action, expected result, actual result, and evidence reference for each observation.

## Navigation coverage

Inspect the applicable surfaces below. Record absent patterns as not applicable only when the triggering need is absent.

| Area | Inspect for |
|---|---|
| Landmarks and repeated blocks | A clear main-content destination; meaningful landmark names where several landmarks of the same type exist; stable shell order; a way to bypass repeated navigation, banners, or utility blocks; no duplicated or hidden competing destinations |
| Skip links | Keyboard reachability before repeated content; visible-on-focus presentation; a target that exists, is meaningful, and receives focus or otherwise reliably moves the keyboard user to content; correct behavior after route changes |
| Menus and navigation tiers | Clear global, local, contextual, utility, and account navigation purpose; destination labels that match content; disclosed hierarchy and current state; intentional differences by role, locale, and state; no essential destination stranded in a responsive variant |
| Current location and breadcrumbs | Current page, section, workspace, step, or selection is perceptible and, when encoded, programmatically exposed; breadcrumbs describe the hierarchy and destination behavior accurately; custom separators and current items do not create misleading or redundant output |
| Titles and headings | Unique, descriptive document titles; route titles update; a clear main heading and section structure that supports navigation; title, visible heading, menu label, and breadcrumb do not contradict each other |
| Consistency and multiple ways | Repeated navigation remains in a consistent relative order and identifies the same function consistently; qualifying pages have the required ways of locating content; search, sitemap, index, category page, or navigation are effective where provided |
| Route transitions and return | URL, title, visible content, focus, scroll, current navigation state, and history remain coherent after link activation, redirects, loading, errors, cancel, back, and forward; users can return without losing essential context or submitted work |
| Deep links and search | Direct URLs, refresh, shared links, unauthorized or expired sessions, redirects, and not-found routes preserve or explain destination intent; search exposes query, result count, scope, filters, result identity, and a path to results and details |
| Mobile and responsive navigation | Menu trigger, expanded state, destination hierarchy, close and return behavior, and available choices remain understandable at narrow widths, zoom, orientation changes, touch, and keyboard use; responsive changes do not silently remove essential routes |
| Large application shells | Global, product, workspace, project, section, utility, and in-content navigation remain distinguishable; persisted shells do not obscure newly routed content; nested or virtualized navigation maintains a usable location and return model |

## Workflow

1. **Frame the audit and sample.**
   - Record the target, critical tasks, user roles, route families, navigation models, responsive breakpoints, standards target, available evidence, exclusions, and access limits.
   - If no WCAG version is specified, use WCAG 2.2 as a mapping reference. If no conformance level is specified, keep it as an open scope decision rather than inventing a target.
   - For large systems, sample every distinct shell and navigation model plus essential routes. Expand the sample when a shared component varies by role, content type, locale, feature flag, or implementation.

2. **Build a route and orientation inventory.**
   - Trace entry points, global and local navigation, utility or account controls, route hierarchy, deep links, search, breadcrumbs, pagination, errors, and return paths.
   - For each critical journey, record how people identify the current location, available next destinations, current selection or step, and a safe way to go back, change context, or recover.
   - Separate visual cues from programmatic exposure and from observed assistive-technology output.

3. **Inspect structural and static evidence.**
   - Review landmarks, skip-link targets, link semantics, menu labels, `aria-current` and expanded state, breadcrumb markup, title generation, heading data, route metadata, redirects, history calls, focus utilities, and responsive visibility rules.
   - Check whether repeated blocks precede the main-content target and whether the same control or destination changes name, order, destination, or meaning across repeated contexts.
   - Record what source proves and create `needs-validation` items for computed exposure, focus, history, scroll, and spoken behavior.

4. **Test entry, movement, and return at runtime.**
   - Start from a home route, a representative interior deep link, a refreshed route, a restricted route, and a not-found route when applicable.
   - Complete critical tasks using links, menus, skip links, headings or landmarks, search, browser back/forward, and direct URLs as relevant.
   - At each transition, capture URL, title, visible main content, current-location cue, focused element, scroll position, menu state, history result, and recovery route. Test slow or failed navigation where it can alter orientation.

5. **Test mobile and application-shell variants.**
   - Repeat the important journeys at each material responsive navigation model, including menu closed and open states, nested navigation, switchers, horizontal overflow, zoom, and orientation changes.
   - Verify that persistent app chrome does not make the destination, main heading, keyboard focus, or current context ambiguous after navigation.
   - Coordinate custom-menu keyboard behavior, focus containment or restoration, and route announcements with the dedicated keyboard and dynamic-interface specialists.

6. **Evaluate search and content-location mechanisms.**
   - Determine which qualifying pages require multiple ways of locating content and whether an exception applies. Do not mistake global navigation alone for proof that every in-scope destination is locatable.
   - Where search exists, test a successful query, no results, filters or scope changes, result-to-detail movement, and return to results. Search is not automatically required by WCAG.
   - Check that alternative pathways lead to the intended content rather than duplicate, stale, unauthorized, or context-losing destinations.

7. **Classify, map, and route findings.**
   - Put only evidence-supported criterion failures in `Applicable WCAG findings`.
   - Put orientation, information-scent, navigation-model, search, or return-path issues without a supported criterion in `Broader wayfinding observations`; leave WCAG mappings empty unless separately justified.
   - Use `provisional` for persuasive but incomplete evidence and `needs-validation` for behavior that requires a named runtime, assistive-technology, or user-research method.
   - Merge duplicate symptoms that have one root cause while retaining all affected routes, modes, and valid mappings. Route deeper semantic, keyboard/focus, dynamic-transition, or visual-responsive issues to the appropriate specialist.

8. **Report coverage and verification.**
   - Give reproducible retest steps for every finding, including start URL, role, viewport, input method, route action, expected orientation outcome, and closure evidence.
   - List verified strengths only as scoped observations. List untested route families, roles, states, devices, and assistive-technology combinations; do not call them passes or infer product-wide conformance.

## WCAG mapping boundary

Use the requested WCAG version as authoritative. These WCAG 2.2 criteria are common candidates, not an automatic checklist or an exhaustive mapping:

| Concern | Candidate criteria | Mapping boundary |
|---|---|---|
| Landmark structure, relationships, breadcrumbs, or heading structure | 1.3.1 Info and Relationships; 1.3.2 Meaningful Sequence | Map only when information, structure, or sequence needed for understanding or operation is not programmatically determinable or meaningful. |
| Bypassing repeated blocks | 2.4.1 Bypass Blocks | Apply when repeated content blocks cannot be bypassed by a mechanism; the exact solution need not be a skip link. |
| Descriptive route titles | 2.4.2 Page Titled | Apply when the web page lacks a title that describes its topic or purpose. In SPAs, verify the document title at the rendered route. |
| Link purpose and navigation labels | 2.4.4 Link Purpose (In Context); 2.4.9 Link Purpose (Link Only, AAA) | A vague label is not automatically a failure; establish that the required purpose cannot be determined from the applicable context. |
| Focus after route change | 2.4.3 Focus Order; 3.2.1 On Focus; 3.2.2 On Input | Map only when observed focus order or an unexpected context change violates the criterion. There is no universal rule that every route must move focus to its heading. |
| Multiple ways to locate pages | 2.4.5 Multiple Ways | Apply to pages within a set when more than one way is required and no exception applies; search itself is not required. |
| Descriptive headings and labels | 2.4.6 Headings and Labels; 2.4.10 Section Headings (AAA) | Do not map a stylistic hierarchy preference without evidence that headings or labels fail to describe topic or purpose. |
| Current location | 2.4.8 Location (AAA); 4.1.2 Name, Role, Value when a custom exposed current state is defective | Current-page indication is valuable at all levels, but only map the applicable criterion and requested level with evidence. |
| Consistent navigation and identification | 3.2.3 Consistent Navigation; 3.2.4 Consistent Identification | Apply when repeated navigation order or identification of the same functionality changes inconsistently within a set of web pages. Intentional role-, locale-, or context-based differences need an evidence-based rationale. |
| Repeated qualifying help | 3.2.6 Consistent Help | This does not require help or search to exist; it governs the relative order of qualifying help mechanisms when they recur. |

Do not report WCAG 2.2 Success Criterion 4.1.1 Parsing as a current failure. Do not use WCAG to describe a general dislike of a navigation model, an omitted breadcrumb, poor information architecture, or a browser-history inconvenience unless the criterion's conditions are met.

## Shared finding contract

Use the shared finding contract from `inclusive-interface-audit-orchestrator`. Every finding must contain:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier, such as `NWA-001` |
| `target` | Route, shell, component, flow, state, role, viewport, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, starting URL, action, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and available workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG criteria, usability heuristics, Universal Design principles, or Norman concepts, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Add `classification: applicable-wcag`, `broader-wayfinding-observation`, or `needs-validation` to make the report sections explicit. `source_skill`, `related_ids`, and `root_cause` are optional traceability fields; set `source_skill` to `navigation-wayfinding-accessibility-audit`. Keep severity, status, confidence, and mappings separate. `accepted-risk` requires a documented product decision, not an auditor decision.

## Output format

Return:

```md
## Audit summary

- Target and critical tasks:
- Route and shell sample:
- Evidence reviewed and environment:
- WCAG version and conformance level:
- Overall orientation and return-path impact:
- Coverage limitations and expansion triggers:
- Conformance disclaimer:

## Applicable WCAG findings

### NWA-001 — Finding title

- Classification: applicable-wcag
- Target:
- Evidence:
- User impact:
- Status:
- Severity:
- Confidence:
- Framework mappings:
- Recommendation:
- Verification:
- Source skill: navigation-wayfinding-accessibility-audit
- Related IDs:
- Root cause:

## Broader wayfinding observations

[Repeat the complete shared finding contract with `classification: broader-wayfinding-observation`. Keep WCAG mappings empty unless independently justified.]

## Needs-validation queue

[Repeat the complete shared finding contract with `status: needs-validation`, exact test steps, required environment, and closure evidence.]

## Verified checks and coverage gaps

- Scoped verified checks:
- Untested routes, shells, roles, states, viewports, and environments:
- Specialist handoffs:
```

Omit empty finding sections, but never omit coverage limitations. Do not describe a sampled verified check as product-wide conformance.

## Quality bar

The task is complete only when:

- The audit names the routes, shells, user roles, critical tasks, navigation variants, and evidence limitations it actually covers.
- It examines orientation before, during, and after movement, including at least applicable direct-entry and return paths.
- Every finding follows the shared contract, cites reproducible evidence, and has a task-specific verification method.
- Supported WCAG findings are separate from broader wayfinding observations, with mapping rationale and no speculative WCAG claims.
- Landmark, skip-link, menu, current-location, title, heading, consistency, route, history, focus, deep-link, search, mobile, repeated-block, and application-shell conditions are evaluated or explicitly marked not applicable, untested, or out of scope.
- Findings are deduplicated by root cause without concealing distinct routes or user impacts.
- The result states that it is a bounded review, not a conformance, certification, or legal-compliance determination.

## Edge cases

- **Single-page marketing site:** Inspect repeated blocks, landmarks, skip links, in-page links, title, headings, and return from linked sections; a breadcrumb or full search system may be not applicable.
- **Single-page application:** Test initial load, internal route change, refresh, deep link, browser history, redirects, loading, errors, and persistent shells. Do not assume a full-page-load model.
- **Authenticated or role-based application:** Test each material navigation model and access-denied state with safe accounts. Distinguish intentional permission differences from inconsistent navigation.
- **External links or embedded products:** State ownership and handoff boundaries. Verify warning, destination, and return behavior only within the controlled scope.
- **Infinite, virtualized, or hierarchical navigation:** Test location, count, selection, loading, collapse or expand, and return context. Route detailed composite-widget mechanics to the keyboard specialist.
- **No running target:** Produce source- and artifact-based provisional findings only; require runtime tests for focus, route, history, title, scroll, responsive, and assistive-technology conclusions.
- **Multiple locales or right-to-left layouts:** Sample translated labels, long text, reading direction, route slugs, and locale-specific navigation order. Do not assume the primary locale represents all variants.

## Related skills

- `semantic-structure-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `content-cognitive-accessibility-audit`
- `visual-responsive-accessibility-audit`
- `accessibility-validation-planner`
- `inclusive-interface-audit-orchestrator`
