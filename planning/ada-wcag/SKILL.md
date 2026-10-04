---
description: Assess ADA Title III / WCAG 2.2 AA compliance — web accessibility legal requirements
---

# ADA / WCAG 2.2 Assessment

Assess ADA Title III and WCAG 2.2 Level AA compliance for "$ARGUMENTS". Evaluate web accessibility legal requirements, enforcement trends, and remediation planning with attention to heightened state requirements.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **ADA Title III applicability assessment:**
   - Determine if the organization operates a "place of public accommodation" with digital presence
   - Assess DOJ rulemaking and guidance on web accessibility under ADA Title III
   - Evaluate applicability of DOJ's April 2024 final rule on web and mobile accessibility (State and local governments under Title II; private sector guidance under Title III)
   - Review Section 508 applicability for federal-facing services
   - Assess state-level accessibility laws (California Unruh Civil Rights Act, New York State Human Rights Law)

3. **WCAG 2.2 Level AA assessment:**
   - Assess against all WCAG 2.2 Level AA success criteria across four principles:
     - **Perceivable:** text alternatives (1.1.1), captions (1.2.2), audio description (1.2.5), info and relationships (1.3.1), meaningful sequence (1.3.2), sensory characteristics (1.3.3), orientation (1.3.4), input purpose (1.3.5), contrast (1.4.3), resize text (1.4.4), images of text (1.4.5), reflow (1.4.10), non-text contrast (1.4.11), text spacing (1.4.12), content on hover/focus (1.4.13)
     - **Operable:** keyboard (2.1.1), no keyboard trap (2.1.2), timing adjustable (2.2.1), pause/stop/hide (2.2.2), three flashes (2.3.1), bypass blocks (2.4.1), page titled (2.4.2), focus order (2.4.3), link purpose (2.4.4), multiple ways (2.4.5), headings and labels (2.4.6), focus visible (2.4.7), focus not obscured minimum (2.4.11), dragging movements (2.5.7), target size minimum (2.5.8)
     - **Understandable:** language of page (3.1.1), language of parts (3.1.2), on focus (3.2.1), on input (3.2.2), consistent navigation (3.2.3), consistent identification (3.2.4), error identification (3.3.1), labels (3.3.2), error suggestion (3.3.3), error prevention (3.3.4), redundant entry (3.3.7), accessible authentication minimum (3.3.8)
     - **Robust:** parsing (4.1.1 — obsolete in 2.2), name/role/value (4.1.2), status messages (4.1.3)
   - Document pass/fail per success criterion with severity assessment

4. **DOJ guidance and enforcement trends:**
   - Review DOJ enforcement actions and settlement agreements for relevant industry
   - Assess structured negotiation trends and settlement terms
   - Evaluate private litigation risk factors (serial plaintiff patterns, high-risk industries)
   - Review recent case law developments affecting web accessibility obligations

5. **State-specific heightened requirements:**
   - **California:** Assess Unruh Civil Rights Act implications (statutory damages of $4,000+ per violation per visit), CCPA intersection with accessibility
   - **New York:** Assess New York State Human Rights Law and New York City Human Rights Law requirements
   - Evaluate other state-specific accessibility laws and pending legislation
   - Assess industry-specific requirements (financial services, healthcare, education)

6. **Remediation planning assessment:**
   - Evaluate existing structured remediation plan (scope, timeline, prioritization)
   - Assess accessibility statement presence and content (conformance level, known issues, feedback mechanism, date)
   - Review alternative access methods (phone support, in-person alternatives, accessible document formats)
   - Evaluate reasonable modification process for accessibility requests
   - Assess third-party component and embedded content accessibility (videos, forms, widgets, PDFs)

7. **Organizational accessibility program:**
   - Assess accessibility policy and governance structure
   - Evaluate developer and content author accessibility training
   - Review design system and component library accessibility
   - Assess automated and manual testing practices in development lifecycle
   - Evaluate assistive technology testing program (screen readers, keyboard-only, voice control)
   - Review accessibility bug tracking and prioritization process

8. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/ada-wcag.md` following the assessment template structure with:
    - **ADA Applicability** — Title III coverage, DOJ guidance, and Section 508 applicability
    - **WCAG 2.2 AA Assessment** — pass/fail per success criterion across all four principles
    - **Litigation Risk** — enforcement trends, state-specific exposure, and risk factors
    - **State Requirements** — California, New York, and other heightened obligations
    - **Remediation Program** — plan maturity, accessibility statement, and alternative access
    - **Organizational Program** — policy, training, testing, and governance
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The ADA/WCAG assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/ada-wcag.md`. Present a summary to the user highlighting:
- ADA Title III applicability determination and litigation risk level
- WCAG 2.2 AA conformance level (percentage of criteria met per principle)
- State-specific exposure areas (California, New York)
- Top 3 gaps requiring remediation
