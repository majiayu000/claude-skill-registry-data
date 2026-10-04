---
name: UAT Checklist
description: Generate a User Acceptance Testing checklist for a feature based on requirements, user flows, and acceptance criteria. Triggers on phrases like 'uat checklist', 'acceptance test plan', 'sign-off checklist', or when reviewing a delivery PR. Produces a structured, role-tagged Markdown checklist covering happy paths, edge cases, accessibility, and FedRAMP-relevant data handling.
---

## Purpose

Give product owners and QA a deterministic, repeatable structure for UAT sign-off so launches do not depend on memory. The skill turns a feature description, user story, or PR into an actionable checklist with explicit roles, preconditions, expected results, and links to the implementing files.

## When to Invoke

- A feature is approaching launch readiness.
- A PO requests a "sign-off checklist" or "acceptance test plan".
- A PR is labeled `ready-for-uat`.
- During release planning to estimate UAT effort.

## When NOT to Invoke

- For internal refactors or developer-experience changes.
- As a substitute for automated tests — use `skill-run-relevant-tests`.
- For pure documentation PRs.

## Inputs

- **source**: a path to a user story, ADR, PR description, or feature spec; alternatively the active editor text.
- **flow** (optional): a named user flow (e.g. `search-and-bookmark`) used as a template anchor.
- **scope** (optional): `frontend`, `api`, or `e2e` (default).

## Procedure

1. Resolve the source. Extract acceptance criteria, in-scope user roles (applicant, agency reviewer, admin), and any explicit edge cases.
2. Identify the affected surfaces by scanning the linked PR diff or referenced files. Tag each surface as `frontend`, `api`, or `data`.
3. Generate checklist sections in this fixed order:
   1. Preconditions (test data, environment, feature flags, role accounts)
   2. Happy path (one row per acceptance criterion)
   3. Edge cases (empty state, max length, invalid input, network failure)
   4. Accessibility (keyboard, screen reader, focus management, USWDS compliance)
   5. Data handling (PII fields, audit log entries, retention) — cross-reference `documentation/rules/data-privacy.mdc`
   6. Cross-browser (Chrome, Firefox, Safari, Edge, mobile Safari)
   7. Rollback / feature-flag toggle
   8. Sign-off (named approvers and date fields)
4. For each row, populate: `ID`, `Role`, `Steps`, `Expected`, `Result`, `Notes`.
5. Cross-reference any related skill (e.g. `skill-accessibility-check` for the a11y section).
6. Emit the Output Format as Markdown ready to paste into a sign-off doc.

## Outputs

```
# UAT Checklist — Opportunity Bookmarking
Source: PR #1842 (user story US-318)
Generated: 2026-04-07
Scope: frontend + api

## 1. Preconditions
- [ ] Feature flag `bookmarks_v1` enabled in target env
- [ ] Test accounts: applicant@test, reviewer@test
- [ ] Seed data: 5 published opportunities

## 2. Happy Path
| ID  | Role      | Steps                                                | Expected                                | Result | Notes |
|-----|-----------|------------------------------------------------------|-----------------------------------------|--------|-------|
| H1  | applicant | Open opportunity, click Bookmark                     | Star fills, toast confirms              |        |       |
| H2  | applicant | Open Saved tab                                       | Bookmarked opportunity is listed        |        |       |
| H3  | applicant | Remove bookmark from Saved tab                       | Item disappears, count updates          |        |       |

## 3. Edge Cases
| ID  | Role      | Steps                                                | Expected                                |
|-----|-----------|------------------------------------------------------|-----------------------------------------|
| E1  | applicant | Bookmark while offline                               | Inline error, no optimistic flip        |
| E2  | applicant | Bookmark a closed opportunity                        | Allowed, badge shows "Closed"           |

## 4. Accessibility
- [ ] Bookmark button reachable by Tab and operable by Enter/Space
- [ ] aria-pressed reflects state
- [ ] Toast announced via aria-live polite
- [ ] Run /skill-accessibility-check on changed components

## 5. Data Handling
- [ ] Audit log row written on bookmark add/remove (audit_log.action = 'bookmark.*')
- [ ] No PII written to client logs
- [ ] Retention follows documentation/rules/data-privacy.mdc §4.2

## 6. Cross-Browser
- [ ] Chrome desktop, Firefox desktop, Safari desktop, Edge desktop, Safari iOS

## 7. Rollback
- [ ] Disabling `bookmarks_v1` hides UI without errors

## 8. Sign-off
- [ ] Product Owner: __________________ Date: ______
- [ ] QA Lead:        __________________ Date: ______
- [ ] Accessibility:  __________________ Date: ______
```

## Safety

- Never executes any test action.
- Never claims a feature is "approved" — it produces a template.
- Cross-references but does not edit `documentation/rules/data-privacy.mdc`.
- FedRAMP: explicitly includes audit-log and PII rows for any data-touching feature.

## Examples

**Example 1 — Bookmarking feature**
PR description + linked story produce a 22-row checklist with happy path, three edge cases, and a11y/data sections.

**Example 2 — API-only delivery**
Skill suppresses the cross-browser section and adds API-specific rows: schema validation, error codes, rate limits.

**Example 3 — Flag rollout**
Generates a checklist anchored on the flag toggle: enable, verify, disable, verify.

## Related

- `.cursor/skills/skill-accessibility-check/` — referenced in the a11y section.
- `.cursor/skills/skill-cross-browser-checklist/` — pairs with the cross-browser section.
- `.cursor/agents/test-plan-generator.md` — broader test plan beyond UAT sign-off.
