---
description: Define the scope and plan for an accessibility audit
---

# Scope

Define the accessibility audit scope for "$ARGUMENTS". Determine what to test, which WCAG level to target, and what pages or features to include.

## Prerequisites

None — this is the first phase.

## Process

1. **Understand the audit target:**
   - What is "$ARGUMENTS"? A website, app, component, feature, or page?
   - Ask the user to clarify if ambiguous

2. **Define the scope:**
   - Which pages or features to test (sample representative pages)
   - Which WCAG level to target (A, AA, or AAA — recommend AA as baseline)
   - Any specific compliance requirements (Section 508, EN 301 549, EAA)
   - Any known accessibility concerns to prioritize

3. **Identify testing approach:**
   - Automated testing: code analysis, ARIA validation, contrast checks
   - Manual testing: keyboard navigation, screen reader flow, focus management
   - Content review: alt text quality, heading structure, link text

4. **Write the artifact** to `.metapowers/accessibility/$ARGUMENTS/01-scope.md` with sections:
   - **Target** — what's being audited
   - **WCAG Level** — target conformance level
   - **Pages/Features** — specific items to test
   - **Compliance Requirements** — applicable standards
   - **Testing Methods** — automated + manual approach
   - **Known Concerns** — pre-existing issues to prioritize

## Output

The audit scope written to `.metapowers/accessibility/$ARGUMENTS/01-scope.md`. Present a summary to the user highlighting:
- Scope boundaries
- Target WCAG level
- Testing approach
