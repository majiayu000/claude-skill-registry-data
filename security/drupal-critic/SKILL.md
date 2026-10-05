---
name: drupal-critic
description: "Drupal code, config, and architecture review for PRs, implementations, and migration plans."
---

# Drupal Critic

## Overview
Run a harsh-critic style review with Drupal-specific checks, explicit evidence requirements, and context-driven audience perspectives.

## External Skill References (No Copy Policy)
Use external skills as references only.

- Canonical reference file: [external-skills-manifest.yaml](references/external-skills-manifest.yaml)
- Routing policy: [skill-routing-map.md](references/skill-routing-map.md)

Rules:
- Do not copy external skill body content into this repository.
- Use manifest IDs/URLs and pinned commit metadata for traceability.
- If a referenced skill is unavailable in runtime, continue with local rubric fallback and state the limitation.

## Workflow
1. Confirm review target and scope.
2. Make 3-5 pre-commitment predictions about likely failure points before deep review.
3. Run protocol phases in order: verification, multi-perspective analysis, explicit gap analysis, synthesis.
4. If reviewing plans/specs, also run plan-specific checks: key assumptions extraction, pre-mortem, dependency audit, ambiguity scan, feasibility check, rollback analysis, and devil's-advocate challenge for major decisions.
5. Run mandatory self-audit before finalizing findings:
   - LOW confidence or easily-refutable claims move to `Open Questions (unscored)`.
   - Preference/style-only points are downgraded or removed from scored sections.
   - Keep scored sections evidence-backed and high-confidence.
6. Run Realist Check on every surviving CRITICAL/MAJOR finding:
   - "If we shipped this as-is today, what is the realistic worst-case outcome?" (not theoretical — the likely worst case given actual usage, traffic, and environment)
   - "Is there a mitigating factor that limits the blast radius?" (e.g., feature flag, low traffic path, existing monitoring, downstream validation, limited user exposure)
   - "How quickly could this be detected and fixed in production?" Minutes (monitoring) vs days (silent corruption) vs never (subtle logic error).
   - "Is the severity proportional to actual risk, or was it inflated by investigation momentum?"

   SECURITY EXPLOITABILITY GATE (mandatory for all security-related findings):
   - "Who can trigger this? What privilege level is required to reach this code path?"
   - "Can a non-privileged user actually exploit this, or does it require admin/superuser access?"
   - "Does the existing access control model already make this moot?"

   Drupal privilege model awareness:
   - Drupal administrators can already execute arbitrary PHP, inject code via UI, and modify all site configuration. Flagging admin-only surfaces as security vulnerabilities is a false positive unless the issue allows non-admins to bypass access controls.
   - `settings.php` is only accessible to users with server/code access (effectively site admins/developers). Issues in settings.php are configuration concerns, not security vulnerabilities.
   - Admin screens (`/admin/*`) are not security risks unless they enable: privilege escalation to non-admins, CSRF that tricks admins into unintended destructive actions, or stored XSS that persists beyond the admin session and affects non-admin users.
   - Focus security findings on: anonymous access, authenticated non-admin access, and privilege escalation paths.

   If you cannot demonstrate a concrete exploit path accessible to non-admin/non-privileged users:
   - Tag the finding as `[UNCONFIRMED]` and move it to Open Questions
   - Add the note: "Security finding unconfirmed — no demonstrated exploit path for non-privileged users."
   - Do NOT leave unconfirmed security findings in scored sections

   A theoretical vulnerability that requires admin access in Drupal — where admins already have full control — is not a finding. It is manufactured alarmism that damages review credibility.

   Recalibration rules:
   - Minor inconvenience with easy rollback → downgrade CRITICAL to MAJOR
   - Mitigating factors substantially contain blast radius → downgrade CRITICAL to MAJOR or MAJOR to MINOR
   - Fast detection + straightforward fix → note context in the finding but keep it
   - Survives all four questions → correctly rated, keep it
   - NEVER downgrade findings involving data loss, security breach, or financial impact
   - Every downgrade MUST include a "Mitigated by: ..." statement explaining what real-world factor justifies the lower severity. No downgrade without an explicit mitigation rationale.
   Report any recalibrations in the Verdict Justification (e.g., "Realist check downgraded finding #2 from CRITICAL to MAJOR — mitigated by the fact that the affected endpoint handles <1% of traffic and has retry logic upstream").
7. Apply Drupal rubric from [drupal-review-rubric.md](references/drupal-review-rubric.md).
8. Activate perspectives based on [audience-activation-matrix.md](references/audience-activation-matrix.md).
9. Load at most 2-3 specialist external skills from the routing map when needed.
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
- Open Source Contributor
- Site Builder (Drupal admin UI)
- Content Editor/Marketer

Perspective notes must appear in `Multi-Perspective Notes`.

## Drupal-Specific Must-Check List
Always check these before final verdict:
- Contrib-first decision quality: should this be upstream patch/work instead of custom code?
- Access and trust boundaries: routes, entity queries, permissions, token checks — but always verify the exploit path is reachable by non-admins. Admins already own the site; only flag admin-surface issues if they enable privilege escalation, CSRF, or stored XSS affecting non-admin users.
- Render safety: `#markup`, Twig raw output, sanitization path — focus on anonymous and authenticated non-admin paths. Admin-only XSS is low-priority unless it persists to non-admin contexts.
- Cache correctness: tags/contexts/max-age and BigPipe/Dynamic Page Cache implications.
- Config workflow safety: `drush cex/cim`, environment drift and import risk.
- Update/deploy safety: composer constraint risk, DB updates, rollback/snapshot path.
- Migration safety: source assumptions, idempotency, replay/rollback behavior.
- Operability: logging, failure handling, and blast radius.

## Skill Loading Rules
- Match the review context against each skill's JTBD statement in the routing map before selecting. Load the skill whose situation clause most closely matches the artifact under review.
- Default: one core review skill + one specialist skill.
- Avoid loading overlapping core skills simultaneously unless scope is broad.
- Prefer higher-priority, active entries in external manifest.

## Severity Calibration
- CRITICAL: exploit/security bypass/data-loss/deploy-blocking flaws.
- MAJOR: likely regressions or significant rework required.
- MINOR: non-blocking correctness/maintainability issues.
- Do not inflate severity for style-only points.

## Stop Conditions
- If review scope is too broad, narrow by component/feature/path.
- If evidence cannot be found, move concern to `Open Questions`.
