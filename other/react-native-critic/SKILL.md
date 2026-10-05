---
description: Review React Native/Expo code for performance, platform APIs, and releases.
name: react-native-critic
---

# React Native Critic

## Overview
Run a harsh-critic style review with React Native/Expo checks, explicit evidence requirements, and context-driven audience perspectives.

## Jobs To Be Done

Use react-native-critic when you need to:

- **Review React Native components** — native module usage, bridge performance, FlatList optimization, platform-specific code
- **Audit Expo integration** — SDK usage, EAS Build/Submit configuration, OTA update strategy, API routes
- **Catch mobile performance issues** — JS thread blocking, native rendering bottlenecks, image optimization, memory leaks
- **Evaluate native architecture** — module boundaries, navigation patterns, state management for mobile, offline-first design
- **Review RN or Expo upgrades** — native dependency alignment, breaking changes, migration paths, metro config
- **Assess platform integrations** — Sentry error monitoring, Auth0 authentication, push notifications, deep linking
- **Review CI/CD and release workflows** — EAS pipelines, OTA vs native updates, code signing, app store submission
- **Evaluate cross-platform patterns** — Platform.OS handling, responsive layouts, platform-specific components, web bridging via use-dom

The router (`js-critic-router`) dispatches here when it detects: `react-native` or `expo` in imports/package.json, `ios/`/`android/` file paths, `metro.config.*`, `app.json`/`eas.json`, or RN-specific components (`View`, `FlatList`, `Pressable`).

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
- RN rubric: [references/react-native-review-rubric.md](references/react-native-review-rubric.md)
- RN audience triggers: [references/audience-activation-matrix.md](references/audience-activation-matrix.md)

## Defaults
- Expo is first-class in v1.
- Mobile release safety and observability checks are mandatory.

## Workflow
1. Confirm target (RN CLI, Expo managed/bare, or mixed).
2. Make 3-5 pre-commitment predictions about likely mobile failure points before deep review.
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
7. Apply shared JS and RN rubrics.
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
- Release Manager
- Product Reliability

Perspective notes must appear in `Multi-Perspective Notes`.

## React Native / Expo Must-Check List
Always check these before final verdict:
- UI performance: list virtualization, jank sources, animation main-thread pressure.
- Platform correctness: iOS/Android divergence and native module assumptions.
- Expo/RN upgrade safety: SDK/RN version compatibility and migration/rollback path.
- Offline/data behavior: sync semantics, retry strategy, and data-loss risk.
- Release readiness: build profile/channel assumptions, observability coverage, failure recovery.
- Security: token storage, device-level secret handling, and network trust boundaries.

## Skill Loading Rules
- Default: one core review skill + one specialist skill.
- Avoid loading overlapping core skills simultaneously unless scope is broad.
- Prefer higher-priority, active entries in external manifest.

## Severity Calibration
- CRITICAL: security, data loss, or release-blocking flaws.
- MAJOR: likely user-facing regressions or significant rework required.
- MINOR: non-blocking correctness/maintainability issues.
- Do not inflate severity for style-only points.

## Stop Conditions
- If review scope is too broad, narrow by component/feature/path.
- If evidence cannot be found, move concern to `Open Questions`.
