---
name: accessibility-report
description: Generate in-depth, evidence-based accessibility reports for software projects. Use when Codex is asked for an accessibility audit, accessibility review, WCAG report, a11y report, inclusive design review, screen reader review, keyboard navigation review, or accessibility findings for a codebase, website, web app, mobile app, component library, design system, documentation site, or frontend project.
---

# Accessibility Report

## Objective

Analyze the target project as thoroughly as the available files, tools, and runtime access allow. Produce a structured Markdown accessibility report that identifies accessibility risks, explains user impact, connects findings to relevant standards, and gives practical remediation guidance developers can act on.

Prioritize WCAG 2.2 Level A and AA. Cover keyboard accessibility, screen reader compatibility, semantic HTML and ARIA usage, color contrast, forms, labels, validation, focus management, navigation structure, images and media, dynamic content, motion, responsive and zoom behavior, automated test coverage, manual verification gaps, and concrete remediation recommendations.

## Operating Rules

- Do not assume the project is accessible or inaccessible without evidence.
- Ground findings in actual project files, configuration, routes, components, tests, documentation, commands, and runtime behavior when available.
- Do not make code changes unless the user explicitly asks for fixes.
- Prefer actionable, developer-focused recommendations over vague guidance.
- Do not overstate automated scan results. Explain that automated tools catch only a subset of accessibility issues.
- Mark unverifiable areas as `Not assessed` or `Needs manual verification`.
- Distinguish confirmed issues, likely risks, recommended improvements, and manual-verification items.
- Preserve the project's framework, architecture, design system, component APIs, and coding conventions.
- Prefer native HTML semantics before ARIA. Avoid recommending ARIA when native elements solve the problem more robustly.
- Cite relevant WCAG success criteria when reasonably clear.
- Be specific to the project. Avoid generic filler that could apply to any codebase.

## Audit Workflow

### 1. Orient To The Project

Inspect the repository before running commands. Determine:

- Framework and runtime, such as React, Vue, Angular, Next.js, Svelte, Astro, Remix, plain HTML, React Native, native mobile, or documentation tooling.
- Package manager and available scripts.
- App entry points, layouts, routes, pages, and major user flows.
- Component library, design system, theme, or shared UI primitives.
- Existing accessibility dependencies, tests, linting, docs, CI checks, and Storybook setup.

Look for:

- `package.json`
- `README.md`
- `src/`, `app/`, `pages/`, `components/`, `routes/`, `views/`
- `public/`
- `tests/`, `e2e/`, `playwright.config.*`, `cypress.config.*`
- `.storybook/`, `stories/`
- `eslint.config.*`, `.eslintrc*`
- `tailwind.config.*`
- design system, theme, token, or style files
- accessibility documentation

### 2. Discover Existing Tooling

Inspect scripts and dependencies before running commands. Look for:

- `axe-core`
- `@axe-core/playwright`
- `jest-axe`
- `vitest-axe`
- `pa11y`
- `lighthouse`
- `eslint-plugin-jsx-a11y`
- `storybook-addon-a11y`
- Playwright
- Cypress
- Testing Library
- WebdriverIO accessibility plugins

Run only available, safe commands, such as lint, tests, build, accessibility-specific scripts, Storybook accessibility checks, or Playwright/Cypress accessibility tests. Do not install new dependencies unless the user explicitly approves or the environment clearly permits it.

Record commands run, pass/fail status, relevant failures, pages/routes/components checked, and testing limitations.

### 3. Perform Static Review

Review source files for common accessibility issues:

- missing or incorrect accessible names
- interactive controls implemented with non-interactive elements
- click handlers without keyboard equivalents
- missing `button`, `a`, `label`, `fieldset`, `legend`, or heading semantics
- improper ARIA roles, states, or properties
- redundant, conflicting, or invalid ARIA
- missing or poor alternative text
- icon-only buttons without accessible labels
- form inputs without associated labels
- validation errors not programmatically associated with fields
- missing focus traps or focus restoration for modals, dialogs, drawers, menus, or popovers
- hidden content that remains focusable
- inadequate heading hierarchy or landmark structure
- color-only communication
- hard-coded colors likely to fail contrast
- removed or weak visible focus indicators
- disabled zoom or poor responsive behavior
- animation without reduced-motion support
- timeouts or auto-updating content without controls
- data tables without headers or captions where needed
- inaccessible custom selects, comboboxes, tabs, accordions, carousels, menus, and tooltips

### 4. Perform Runtime Or Automated Review

When the project can be run or tested, use existing commands and browser-based checks to gather evidence. Prioritize:

- existing accessibility test scripts
- end-to-end tests with accessibility hooks
- Storybook accessibility checks
- axe, Lighthouse, pa11y, Playwright, Cypress, or framework-specific checks already present in the project

Avoid claiming coverage for routes, components, states, or authenticated flows that were not actually checked.

### 5. Apply Manual Review Reasoning

Even when automated tooling exists, evaluate manual accessibility risks from code and UI patterns.

Assess keyboard access:

- Confirm whether all interactive controls appear keyboard-reachable.
- Check likely tab order and visible focus.
- Check expected key support for custom widgets.
- Check focus management for modals, menus, drawers, dialogs, popovers, and route changes.

Assess screen reader support:

- Check page titles, headings, landmarks, labels, and accessible names.
- Check names, roles, values, and states for controls.
- Check status messages, validation errors, and dynamic content announcements.
- Check decorative elements are hidden appropriately.

Assess visual accessibility:

- Check color contrast risks and color-only meaning.
- Check focus-state visibility.
- Check 200% zoom and responsive behavior when possible.
- Check text sizing, spacing, and hit target concerns.

Assess cognitive and interaction accessibility:

- Check clarity of instructions and errors.
- Check predictability of complex interactions.
- Check whether animations are controllable or respect reduced motion.
- Check whether time limits are avoidable or extendable.

## Severity Model

Classify every finding:

- `Critical`: Blocks users with disabilities from completing a core task, such as logging in, purchasing, submitting a form, navigating the app, or accessing primary content.
- `High`: Creates a major barrier for keyboard, screen reader, low-vision, motor, cognitive, or assistive technology users, but may have a workaround.
- `Medium`: Causes meaningful accessibility friction or partial non-compliance, especially in secondary flows or reusable components.
- `Low`: Minor issue, polish item, best-practice improvement, or issue with limited user impact.
- `Needs Verification`: Suspected issue that requires runtime access, assistive technology, design specs, or manual browser testing to confirm.

Use `Status: Confirmed`, `Likely`, or `Needs manual verification` for each detailed finding.

## Report Format

Generate the final report in Markdown with this structure:

```markdown
# Accessibility Report: <Project Name>

## Executive Summary

Briefly summarize the overall accessibility posture.

Include:
- overall risk level
- most important accessibility strengths
- most important accessibility risks
- highest-priority remediation themes
- major audit limitations

## Scope

Describe what was reviewed.

Include:
- repository areas inspected
- pages, routes, components, or flows reviewed
- tools or commands run
- standards referenced
- anything not reviewed

## Methodology

Explain static code review, automated checks, manual reasoning based on code and UI patterns, and limitations.

## Standards Referenced

Use WCAG 2.2 as the primary reference, especially Level A and AA. Mention WAI-ARIA Authoring Practices, HTML accessibility best practices, and platform-specific mobile guidance when relevant.

## Findings Summary

| ID | Severity | Area | Finding | Primary Impact | WCAG Reference |
| --- | --- | --- | --- | --- | --- |

## Detailed Findings

### Finding <ID>: <Title>

Severity: <Critical, High, Medium, Low, or Needs Verification>
Status: <Confirmed, Likely, or Needs manual verification>
Affected area: <file, component, route, or feature>
Relevant WCAG: <specific criterion if known>

User impact: Explain who is affected and how.

Evidence: Describe the code, behavior, command output, or pattern that supports the finding.

Recommendation: Give a concrete fix.

Example remediation: Include minimal, realistic code examples when useful.

Verification steps: Explain how to confirm the fix.

## Positive Accessibility Practices

List project-specific strengths, such as semantic elements, existing accessibility tests, good labels, good focus states, reduced-motion support, consistent design system patterns, or proper native controls.

## Cross-Cutting Recommendations

Provide broader recommendations, such as automated accessibility tests in CI, semantic HTML before ARIA, accessible component contracts, keyboard interaction tests for custom widgets, focus management utilities, contrast-safe design tokens, and accessibility acceptance criteria.

## Suggested Test Plan

Include automated checks, keyboard-only testing, screen reader smoke testing, browser zoom testing, color contrast checks, form validation checks, and regression tests for key components.

## Prioritized Remediation Roadmap

### Immediate

Issues that block access or affect core workflows.

### Near-Term

Important improvements that reduce major friction.

### Longer-Term

Structural improvements, documentation, tooling, and regression prevention.

## Limitations

Clearly state what could not be verified, such as app runtime, browser access, authenticated test accounts, dynamic behavior, design files, or assistive technology testing.

## Appendix

Include commands run, tool output summary, files reviewed, components reviewed, accessibility checklist, and recommended dependencies or scripts when relevant.
```

## Remediation Guidance

When giving code examples:

- Prefer native HTML elements.
- Use ARIA only when necessary.
- Preserve existing component APIs where possible.
- Show minimal, realistic examples.
- Explain why the change improves accessibility.
- Include verification steps.

## Final Response

When the audit is complete, provide:

- a concise summary of what was reviewed
- the full accessibility report
- a short list of the highest-priority next actions
- a note about areas needing manual verification

Do not claim full WCAG compliance unless the evidence truly supports that conclusion. If the evidence supports that conclusion, still recommend human review to confirm compliance.
