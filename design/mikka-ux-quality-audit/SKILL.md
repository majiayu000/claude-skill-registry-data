---
name: mikka-ux-quality-audit
description: "Run a cross-product Mikka UI/UX and functional-quality audit: discoverability and missing actions, dead controls, state/permission parity, error recovery, keyboard/touch, responsive layout and accessible flows. Use for broad UX reviews and quality sweeps; route concrete command coverage to mikka-action-coverage."
---

# Mikka UX and quality audit

## Preflight

Read `AGENTS.md`, `CONTRIBUTING.md`, `docs/design/README.md`, `docs/review-checklist.md`, `docs/ci/test-ownership.md` and the actual current issue owner. Respect the single official UI and the as-shipped paid-block boundary. The public Server-only build is **not** another UI to review.

Before auditing, record exact public `Mikka` and private `mikka-hosted-ui` source SHAs, application/runtime build and tested environment. Search existing #1646/#1979/#1980/#1966 and #2212 findings before assigning new work. Keep one issue/PR owner per affected source path; never race the #1954 production cutover owner.

## Procedure: investigate, fix, verify

1. **Choose user journeys, not arbitrary screens.** Inventory roles (personal, team member/lead, org admin, read-only/revoked), the important jobs those users expect to finish, and the official entry paths (Web, Electron, applicable Expo/iOS, Cloud/self-hosted). Include first use, daily tasks and failure/recovery. Note an explicitly allowed redirect from a compact view.
2. **Audit missing and misleading functionality first.** Invoke [mikka-action-coverage](../mikka-action-coverage/SKILL.md). Map authorized backend command and state transition -> reachable UI affordance -> handler -> authoritative API -> durable readback. Reverse from visible controls to real operations. A static callback reference is not proof of a working action.
3. **Audit usability by evidence, not aesthetics.** Use [ux-heuristics](../ux-heuristics/SKILL.md) for the screen score and the Nielsen audit, [cognitive-walkthrough](../cognitive-walkthrough/SKILL.md), [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md), adapted [web-design-guidelines](../web-design-guidelines/SKILL.md) and [impeccable-audit](../impeccable-audit/SKILL.md). Prioritize status visibility, navigation, accurate feedback, focus, touch, wrapping, screen-reader semantics, error/empty/loading state and unnecessary network work. No new design system.
4. **Verify at actual boundaries.** Use [mikka-browser-qa](../mikka-browser-qa/SKILL.md) and the adapted [webapp-testing](../webapp-testing/SKILL.md). Pin a local production-build source pair. Distinguish source inspection, DOM/browser evidence, real HTTP + isolated PostgreSQL, packaged Electron, Expo Web and physical TestFlight. Test authorized write/readback and denied write; simulate 409, 401/403, 5xx, lost ACK, retries, cold/hot readiness and navigation only where relevant. Clean only disposable isolated fixtures.
5. **Triage and fix.** Each finding includes a real affected journey, fixed SHA and route/role, observed before/after, severity 0-4, occurrence (1-10) and impact (1-10), root-cause owner, exact failed contract and regression. Dedupe against open issues. Honor `AGENTS.md` risk triage: low occurrence×impact under 5 is filed rather than speculative refactoring unless security/irreversible harm. Fix confirmed meaningful bugs in their canonical source; do not clone a second reader, state machine or paid component.
6. **Ship with independent proof.** Read the existing [diagnosing-bugs](../diagnosing-bugs/SKILL.md), [test-audit](../test-audit/SKILL.md), and [verification-before-completion](../verification-before-completion/SKILL.md). Show a pre-fix failing observation and post-fix evidence at the strongest owner boundary. Run affected Nx/lint/API/PG and local production UI acceptance, review merge risk and use normal protected PR merge. Preserve platform/runtime production owner gates and close only when the issue's DoD truly holds.

## Evidence and reporting

Run the [domain workflow](../../../docs/design/ux-quality-audit.md#run-one-domain) from the public checkout. Attach the command results and observed interaction to the source-bound matrix. Statuses: `verified-missing`, `verified-broken`, `source-only-candidate`, `verified-intentional`, `verified-fixed`, `not-tested`. Never treat an empty result list or an AST pass as full functional coverage.

No general browser E2E CI gate, product polling, Vercel preview or new paid UI source. An audit does not authorize production data writes or publishing. If production/physical-device acceptance is unavailable, record the exact remaining gate; continue unrelated actionable work without declaring the entire goal finished.
