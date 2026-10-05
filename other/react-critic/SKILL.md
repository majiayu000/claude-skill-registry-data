---
description: Evidence-backed review of React components, hooks, state, and rendering.
name: react-critic
---

# React Critic

## Overview
Run a harsh-critic style review with React-specific checks, explicit evidence requirements, and context-driven audience perspectives.

## Jobs To Be Done

Use react-critic when you need to:

- **Review React components** for hook correctness, dependency array bugs, stale closures, and rule-of-hooks violations
- **Audit state management** — local vs shared vs server state ownership, mutation safety, and unnecessary re-renders
- **Catch rendering performance issues** — expensive computations in render path, missing memoization, list virtualization gaps, waterfall data fetching
- **Evaluate async correctness** — race conditions in effects, missing cancellation/teardown, concurrent request handling
- **Review React upgrades or migrations** — version assumptions, deprecated API usage, fallback strategy, migration scope
- **Assess operational safety** — error boundaries, monitoring visibility, blast radius of changes, rollback paths
- **Review TypeScript + React patterns** — type safety, generic component design, API contract correctness

The router (`js-critic-router`) dispatches here when it detects: React imports, JSX/TSX with hooks (`useState`, `useEffect`, etc.), React component patterns — without Next.js or React Native signals.

## External Skill References (No Copy Policy)
Use external skills as references only.

- Canonical reference file: [external-skills-manifest.yaml](references/external-skills-manifest.yaml)
- Routing policy: [skill-routing-map.md](references/skill-routing-map.md)

Rules:
- Do not copy external skill body content into this repository.
- Use manifest IDs/URLs and pinned commit metadata for traceability.
- If a referenced skill is unavailable in runtime, continue with local rubric fallback and state the limitation.

## References
- Shared rubric: [../shared-js-core/references/js-review-rubric.md](../shared-js-core/references/js-review-rubric.md)
- Shared audiences: [../shared-js-core/references/shared-audience-activation-matrix.md](../shared-js-core/references/shared-audience-activation-matrix.md)
- React rubric: [references/react-review-rubric.md](references/react-review-rubric.md)
- React audience triggers: [references/audience-activation-matrix.md](references/audience-activation-matrix.md)

## Workflow
1. Confirm review target and scope.
2. Make 3-5 pre-commitment predictions about likely React failure points before deep review.
3. Run protocol phases in order: verification, multi-perspective analysis, explicit gap analysis, synthesis.
4. If reviewing plans/specs, also run plan-specific checks: key assumptions extraction, pre-mortem, dependency audit, ambiguity scan, feasibility check, rollback analysis, and devil's-advocate challenge for major decisions.
5. Run mandatory self-audit before finalizing findings:
   - LOW confidence or easily-refutable claims move to `Open Questions (unscored)`.
   - Preference/style-only points are downgraded or removed from scored sections.
   - Keep scored sections evidence-backed and high-confidence.
6. Run Realist Check on every surviving CRITICAL/MAJOR finding:
   - If shipped now, what is the realistic worst-case outcome?
   - Which mitigation currently limits blast radius?
   - How quickly would production detect this?
   - Is severity proportional to actual risk?

   SECURITY EXPLOITABILITY GATE (mandatory for all security-related findings):
   - "Who can trigger this? What privilege level is required?"
   - "Can a non-privileged user actually exploit this, or does it require admin access?"
   - "Does the existing access control model already make this moot?"
   If you cannot demonstrate a concrete exploit path accessible to non-admin/non-privileged users, tag the finding as `[UNCONFIRMED]` and move it to Open Questions. Do NOT leave unconfirmed security findings in scored sections.

   Recalibration rules:
   - Downgrade when mitigation meaningfully limits impact.
   - Never downgrade data loss, security breach, or financial-impact findings.
   - Any downgrade must include `Mitigated by: ...` rationale.
7. Apply shared JS and React rubrics.
8. Activate audiences based on audience matrix.
9. Load at most 2-3 specialist external skills from the routing map.
10. Return structured verdict with evidence.

## Required Output Contract
Use this exact top-level structure:
- `VERDICT: [REJECT | REVISE | ACCEPT-WITH-RESERVATIONS | ACCEPT]`
- `Overall Assessment`
- `Pre-commitment Predictions`
- `Critical Findings`
- `Major Findings`
- `Minor Findings`
- `What's Missing`
- `Ambiguity Risks` (plan reviews only)
- `Multi-Perspective Notes`
- `Verdict Justification`
- `Open Questions (unscored)`

Rules:
- CRITICAL and MAJOR findings must include concrete evidence (`file:line` or backtick-quoted artifact reference).
- If a section has no items, write `None.`
- Keep speculative points in `Open Questions` only.
- In `Verdict Justification`, state whether escalation to adversarial review happened and why.

## Perspectives
Always run:
- Security
- New-hire
- Ops

Context-driven (activate when triggered):
- Performance Engineer
- DX Maintainer
- Product Reliability

Perspective notes must appear in `Multi-Perspective Notes`.

## React-Specific Must-Check List
Always check these before final verdict:
- Hook correctness: dependency arrays, stale closures, rule-of-hooks adherence.
- State ownership: local vs shared vs server-state boundaries and mutation safety.
- Render behavior: unnecessary re-renders, expensive computations in render path, list virtualization gaps.
- Async correctness: waterfall risk, cancellation/teardown handling, race-prone effects.
- Upgrade safety: React version assumptions, migration scope, fallback strategy.
- Operability: actionable errors, monitoring visibility, blast radius.

## Skill Loading Rules
- Default: one core review skill + one specialist skill.
- Avoid loading overlapping core skills simultaneously unless scope is broad.
- Prefer higher-priority, active entries in external manifest.

## Severity Calibration
- CRITICAL: security, data loss, or deploy-blocking flaws.
- MAJOR: likely user-facing regressions or significant rework required.
- MINOR: non-blocking correctness/maintainability issues.
- Do not inflate severity for style-only points.

## Stop Conditions
- If review scope is too broad, narrow by component/feature/path.
- If evidence cannot be found, move concern to `Open Questions`.
