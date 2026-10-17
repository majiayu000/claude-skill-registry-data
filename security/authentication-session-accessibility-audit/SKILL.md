---
name: authentication-session-accessibility-audit
description: Audits login, registration, password, MFA, CAPTCHA, account recovery, reauthentication, session-expiry, and security-interruption flows for accessible authentication, recovery, and privacy-safe feedback. Use when the user asks to review sign-in accessibility, password-manager or paste support, OTP handling, session timeouts, CAPTCHA alternatives, lockout messaging, or WCAG 2.2 Accessible Authentication without requesting implementation changes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-accessibility-reviewers-security-and-identity-teams
  tags:
    - accessibility
    - authentication
    - session-management
    - password-manager
    - mfa
    - otp
    - captcha
    - account-recovery
    - wcag
  status: draft
  side_effects: none
---

# Authentication and Session Accessibility Audit

## Purpose

Audit authentication and session journeys as security-sensitive user tasks. Identify accessible, privacy-preserving ways to meet the real security objective; distinguish those requirements from avoidable barriers; and report only evidence-supported findings.

## When to use this skill

Use this skill when:

- The user asks to audit sign-in, registration, password setup or reset, MFA, CAPTCHA, account recovery, reauthentication, or session expiry.
- The task involves password managers, copy and paste, autofill, OTP entry, device switching, biometric or passkey choices, account lockout, or timeout warnings.
- The user wants WCAG 2.2 mappings for authentication or security interruptions, especially `3.3.8 Accessible Authentication (Minimum)`.
- An identity, security, or design team needs a review that preserves security intent while reducing unnecessary user burden.

Do not use this skill when:

- The request is to implement identity, authorization, cryptography, or backend session controls rather than review the user experience.
- The audit is only a general form review with no authentication, session, or security-interruption behavior in scope.
- The user wants a penetration test, a security certification, or a legal/compliance determination.
- The task requires evaluating a third-party identity provider that cannot be inspected or exercised; report the boundary and request its relevant evidence instead.

## Inputs to inspect

Start with the smallest relevant set:

- Sign-in, registration, password, MFA, recovery, reauthentication, lockout, and session-expiry routes, components, templates, and state diagrams.
- Rendered HTML or accessibility-tree snapshots for initial, error, pending, success, expired, locked, recovery, and return-to-task states.
- Client and server validation, session-timeout policy, redirect/return URL handling, retry limits, rate-limit behavior, and work-preservation rules.
- Password and OTP field attributes, including `type`, `autocomplete`, `inputmode`, paste handling, autofill integrations, and custom input code.
- CAPTCHA or bot-mitigation provider configuration, fallback paths, support escalation, and third-party embedded controls.
- Copy, localization, emails or messages referenced by the flow, privacy requirements, supported browser/device/assistive-technology matrix, tests, fixtures, recordings, and defect reports.

If a flow cannot be safely exercised with a test account, inspect source and supplied evidence, then put runtime behavior in the validation queue. Never use real credentials, send recovery messages, lock accounts, or alter security settings unless separately authorized.

## Audit rules

- Keep this review-only. Do not create accounts, submit personal data, consume real one-time codes, trigger lockouts, or change security settings without explicit authorization.
- Treat a security control's objective separately from its current interaction. A requirement to resist automated abuse, verify possession, or protect a session does not automatically require memorization, transcription, or a specific CAPTCHA.
- Treat source, rendered-DOM, reproducible runtime, or test evidence as confirmed only when it directly establishes the issue. Put unexercised screen-reader, timeout, email, cross-device, and third-party behavior in manual validation.
- Never expose passwords, one-time codes, recovery tokens, full identifiers, security answers, or sensitive account state in a report, screenshot, log, URL, or live-region recommendation. Redact evidence and use test data.
- Do not infer full WCAG 2.2 conformance, security strength, or privacy compliance from this focused audit. Map a criterion only when the observed issue and evidence support it.
- When `inclusive-interface-audit-orchestrator` is available, read and preserve its shared finding contract exactly. Otherwise, use the portable contract below.

## Workflow

1. **Define the authentication and interruption inventory.**
   - List entry points and complete paths for sign-in, account creation, password creation/change/reset, MFA enrollment and challenge, CAPTCHA, recovery, reauthentication, session warning/expiry, logout, account lockout, and return to interrupted work.
   - Record authentication methods, devices, channels, third-party dependencies, time limits, rate limits, data sensitivity, supported environments, and known exclusions.
   - Identify whether each task is access-critical, consequential, or recoverable, but do not equate that classification with WCAG severity.

2. **Model each state and transition.**
   - Cover initial, autofilled, editing, invalid, pending, network failure, server rejection, expired-code, locked-out, cancelled, recovered, reauthenticated, expired-session, and restored-work states.
   - Record focus destination, visible feedback, programmatic state, announcement expectation, available next action, and retained versus cleared data for every transition.
   - Require manual testing for browser, password-manager, screen-reader, virtual-keyboard, and cross-device behavior that source inspection cannot prove.

3. **Audit accessible authentication and password entry.**
   - Verify clear labels, instructions, required/invalid state, error recovery, and keyboard operation for every credential field and action.
   - Check appropriate `autocomplete` tokens such as `username`, `current-password`, `new-password`, `one-time-code`, and applicable personal-data tokens. Check that field names and purposes remain available to password managers and assistive technology.
   - Confirm that password managers and browser autofill can fill credentials without misleading errors, unexpected clearing, incompatible custom fields, or blocked submission.
   - Verify that copy and paste are permitted for passwords, passphrases, recovery codes, and OTPs unless an independently justified, accessible alternative meets the same security objective. Do not require users to retype, memorize, transcribe, calculate, or solve a puzzle merely to authenticate.
   - Check show/hide-password controls, password-rule feedback, password generation, confirmation fields, error correction, and credential changes for clear names, exposed state, focus order, and privacy-safe output.
   - Treat a password itself as a cognitive-function test under WCAG 2.2 only in the criteria's defined context. Review whether another authentication method, password-manager support, copy/paste, or an assistive mechanism enables users to avoid relying on memory or transcription.

4. **Audit registration, password creation, and recovery.**
   - Verify requirements before entry, precise error identification, actionable correction, and preserved non-sensitive work after failures.
   - Check whether password policies block paste, generated passphrases, spaces, Unicode where supported, or password-manager fills without a security reason and accessible fallback.
   - Verify that recovery does not unnecessarily require prior credential re-entry, repeated personal information, inaccessible support contact, or a remembered answer that cannot be reset.
   - Confirm that reset links, recovery codes, and cancelled recovery return users to a clear, safe state without leaking account existence or exposing tokens.

5. **Audit MFA, OTP, and device switching.**
   - Verify that MFA choices and setup instructions identify the channel, estimated wait, expiry, retry, resend, and an accessible alternative when a method or device is unavailable.
   - Prefer a single, correctly labelled OTP input with `autocomplete="one-time-code"` when appropriate. If segmented inputs are used, verify full-code paste, predictable focus movement, editing, screen-reader context, and an equivalent single-field or accessible alternative.
   - Ensure that code values are not automatically announced, exposed in labels, copied into live regions, or retained longer than necessary. Provide clear expired-code and incorrect-code recovery without revealing more account information than needed.
   - Test switching between devices, apps, email/SMS, authenticator, passkey, security key, backup code, and support recovery. Users must be able to understand which device is needed and resume or choose a safe alternative without losing the original task.
   - Treat a possession factor, rate limit, or verified recovery channel as a security requirement to preserve; assess whether its presentation and fallback impose unnecessary barriers.

6. **Audit CAPTCHA and bot mitigation.**
   - Identify every challenge, invisible score, proof-of-work, puzzle, image/audio task, third-party frame, failure state, and escalation path.
   - Verify keyboard operation, names/instructions, error recovery, time limits, and privacy disclosures for author-controlled challenge UI.
   - Determine the security objective, then verify an accessible, equivalent path for users who cannot complete the challenge. Alternatives may include risk-based controls, verified channels, accessible human support, or another method that does not require the same cognitive, perceptual, or motor ability.
   - Do not report the existence of CAPTCHA alone as a WCAG failure. Report the observable barrier, missing alternative, inaccessible integration, or unsupported cognitive test with its evidence.

7. **Audit session expiry, reauthentication, and preserved work.**
   - Identify idle, absolute, and transaction time limits; warning thresholds; extension controls; save/draft behavior; retry boundaries; and return-to-task behavior after reauthentication.
   - Verify a timely, perceivable, keyboard-operable warning that explains the consequence and provides enough time and a clear way to extend the session when the time limit is adjustable.
   - Confirm that a reauthentication interruption preserves safe user work, restores task context and focus, prevents duplicate irreversible action, and says what must be done next.
   - When data cannot be retained for security or privacy reasons, verify that the interface warns users in advance where possible, minimizes re-entry, and explains the safe recovery path without oversharing.
   - Distinguish security-essential, real-time, and other WCAG timing exceptions from poorly designed timers. Do not assume every session timeout must be extendable.

8. **Audit errors, lockouts, and privacy-safe announcements.**
   - Verify that failures identify the actionable problem without revealing whether an account, identifier, recovery channel, or authentication factor exists to an unauthorized person.
   - Check that lockout, rate-limit, suspicious-activity, and challenge failures state safe next steps, wait or support options, and retry constraints without false urgency or dead ends.
   - Verify that errors, pending states, and completion notices are visible, programmatically available, non-duplicative, and do not interrupt credential entry unnecessarily.
   - Ensure announcements use the minimum necessary information: announce status and next action, not secret values, full email/phone numbers, account balances, location, device inventory, or security details that increase exposure.
   - Check focus after failure, reauthentication, timeout warning, timeout expiry, dialog dismissal, and return to the interrupted action.

9. **Separate security requirements from avoidable barriers.**
   - For every suspected issue, state the security objective, the evidence that it is required, the user barrier, and a less exclusionary option. Escalate unresolved policy assumptions instead of guessing.

   | Preserve when justified | Question or replace when not justified |
   |---|---|
   | Rate limiting, server-side verification, replay resistance, secure session invalidation, and a possession or recovery factor | Paste blocking, forced password retyping, arbitrary password-composition rules, inaccessible CAPTCHA-only paths, and mandatory remembered answers |
   | Reauthentication for a sensitive or irreversible action, with a safe return path | Silent timeout, unexplained work loss, duplicated irreversible submission, or a reauthentication loop |
   | Generic external-facing failure messages that resist account enumeration | Generic messages that provide no recovery route after the user is authenticated or already in a trusted recovery context |
   | Privacy-minimizing announcements and redacted evidence | Hiding necessary error, expiry, or recovery information from the affected user |

10. **Classify, map, and report.**
    - Keep confirmed findings, provisional findings, and unperformed manual tests separate. Group duplicate manifestations by root cause while retaining affected paths.
    - Prioritize blocked access, irreversible loss of work, unsafe recovery, inability to use an available authentication method, and privacy exposure before consistency or polish concerns.
    - Map applicable WCAG criteria with a brief issue-specific rationale, then provide retest steps that cover the affected authentication method, state, device, and assistive technology.

## WCAG 2.2 mapping guide

Consider these criteria when the evidence supports them:

| Criterion | Apply to |
|---|---|
| `1.3.1 Info and Relationships` (A), `1.3.5 Identify Input Purpose` (AA), `1.4.1 Use of Color` (A), `2.4.6 Headings and Labels` (AA), `2.5.3 Label in Name` (A), `3.3.1 Error Identification` (A), `3.3.2 Labels or Instructions` (A), `3.3.3 Error Suggestion` (AA), and `4.1.2 Name, Role, Value` (A) | Credential, OTP, recovery, extension, and CAPTCHA controls; their labels, purposes, states, instructions, and errors. |
| `2.1.1 Keyboard` (A), `2.4.3 Focus Order` (A), `2.4.7 Focus Visible` (AA), and `2.4.11 Focus Not Obscured (Minimum)` (AA) | Completing and recovering from every authentication or interruption state without a pointer. |
| `2.2.1 Timing Adjustable` (A) | Adjustable warnings, extensions, and recovery for applicable time limits. Assess the criterion's real-time, essential, and other exceptions; do not apply it mechanically to every secure timeout. |
| `3.2.1 On Focus` (A), `3.2.2 On Input` (A), `3.2.6 Consistent Help` (A), `3.3.7 Redundant Entry` (A), and `4.1.3 Status Messages` (AA) | Unexpected changes, consistent recovery help, unnecessary re-entry during a process, and non-focus status feedback. |
| `3.3.8 Accessible Authentication (Minimum)` (AA) and `3.3.9 Accessible Authentication (Enhanced)` (AAA) | Authentication steps that require cognitive-function tests. Evaluate assistive mechanisms, password-manager and paste support, non-cognitive alternatives, and the different minimum/enhanced exceptions precisely. |
| `1.1.1 Non-text Content` (A) and `1.4.10 Reflow` (AA), where evidence supports them | CAPTCHA or verification controls with non-text content or layout barriers. Do not use either criterion as a substitute for evaluating accessible authentication and a meaningful alternative path. |

Use the current WCAG 2.2 Recommendation and Understanding documents when a mapping is uncertain. WCAG level is not severity, and a valid security objective does not by itself establish an exception or conformance.

## Shared finding contract

Return every finding with these required fields so it can be merged by `inclusive-interface-audit-orchestrator`:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier. |
| `target` | Route, component, flow, state, authentication method, device/channel, environment, and occurrence as applicable. |
| `evidence` | Evidence type, method, redacted reference, environment, and reproducible observation. |
| `user_impact` | Affected users, blocked or impaired task, consequence, and safe workaround if one exists. |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`. |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact. |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence. |
| `framework_mappings` | Zero or more valid WCAG criteria or other supplied frameworks, each with rationale. |
| `recommendation` | Outcome-focused remediation, security objective to preserve, constraints, and responsible surface. |
| `verification` | Retest steps, expected result, method, environment, and safe evidence required to close. |

Allow `source_skill`, `related_ids`, and `root_cause` when the caller permits optional traceability fields. Set `source_skill` to `authentication-session-accessibility-audit` when useful. Treat `accepted-risk` as a documented product decision, not an auditor decision; do not assign `resolved` without successful retest evidence.

## Output format

Return:

```md
## Audit summary

- Scope and authentication methods:
- Evidence and safe test environment:
- States and devices exercised:
- Exclusions and third-party boundaries:
- Overall outcome:
- Conformance disclaimer: This scoped audit does not establish full WCAG 2.2 conformance or security certification.

## Security objective and barrier assessment

| Flow or control | Security objective | Evidence it is required | Observed user barrier | Less exclusionary option | Decision or owner |
|---|---|---|---|---|---|

## Findings

### ASA-001 — Short title

- id:
- target:
- evidence:
- user_impact:
- status:
- severity:
- confidence:
- framework_mappings:
- recommendation:
- verification:
- source_skill: authentication-session-accessibility-audit
- related_ids: optional
- root_cause: optional

## Required manual validation

| ID | Flow and risk | Preconditions | Steps | Expected accessible behavior | Environment and evidence |
|---|---|---|---|---|---|

## Coverage and residual risk

| Area | Inspected | Exercised | Result or remaining risk |
|---|---:|---:|---|
| Password manager and paste | ... | ... | ... |
| MFA, OTP, and device switching | ... | ... | ... |
| CAPTCHA and alternatives | ... | ... | ... |
| Errors, lockout, and announcements | ... | ... | ... |
| Session warning, expiry, and reauthentication | ... | ... | ... |
| Preserved work and return to task | ... | ... | ... |

## WCAG mapping summary

| Criterion | Finding IDs | Manual-test IDs | Mapping rationale and limits |
|---|---|---|---|

## Retest priorities

1. ...
```

Omit the findings section only when there are no confirmed or provisional findings, and say so explicitly. Do not place unperformed behavior checks in findings merely to make the report appear complete.

## Quality bar

The task is complete only when:

- The scoped journey covers the applicable authentication, recovery, MFA, CAPTCHA, interruption, expiry, and return-to-task states.
- Password-manager support, paste, cognitive-function tests, input purpose, OTP handling, device switching, CAPTCHA alternatives, error recovery, and lockout messaging are assessed or explicitly excluded.
- Timeouts, extension, reauthentication, preserved work, and privacy-safe announcements are assessed whenever a session can interrupt a user task.
- Every finding preserves the shared contract, cites redacted evidence, separates status, severity, confidence, and WCAG mapping, and names the security objective that any change must retain.
- Manual tests name the needed account state, device/channel, browser, assistive technology, expected behavior, and safe evidence capture.
- The result never claims security certification, full WCAG conformance, or an unverified third-party behavior.

## Edge cases

- For SSO, federated identity, embedded identity-provider pages, passkeys, biometrics, and native app handoffs, audit the author-controlled launch, return, error, and fallback paths; state the provider boundary precisely.
- For shared devices, private browsing, offline states, low connectivity, SMS/email delay, lost or replaced devices, and international phone numbers, test recovery and privacy behavior without assuming a single channel works for everyone.
- For step-up authentication during a destructive action, verify a stable return point and idempotent confirmation so reauthentication cannot cause duplicate work.
- For security policies that appear to conflict with accessibility, document the objective and request the policy owner to validate whether the interaction is necessary; do not invent an exception.

## Related skills

- `forms-errors-accessibility-audit`
- `keyboard-focus-accessibility-audit`
- `dynamic-interface-accessibility-audit`
- `content-cognitive-accessibility-audit`
- `user-recovery-flow-planner`
- `inclusive-interface-audit-orchestrator`
