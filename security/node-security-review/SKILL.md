---
name: node-security-review
description: "Findings-first application-layer security review for Node.js and Fastify backends. Use whenever the task is a security review, trust-boundary audit, auth or session check, secret-handling review, outbound HTTP or SSRF review, security PR review, or a 'what can an attacker do here?' pass in a Node backend, even if the user only provides a diff, route, middleware snippet, or asks for a quick sanity check."
---

# Node Security Review

## Purpose

Use this skill to review Node.js backend code, diffs, designs, or incidents for
real application-layer security findings:

- trust-boundary mistakes
- auth, session, JWT, or cookie verification gaps
- secret handling and exposure mistakes
- outbound HTTP and SSRF risk
- fail-open behavior under error, timeout, or misconfiguration
- unsafe exposure through errors, headers, logs, or third-party integrations

This skill is for review, not for broad security architecture authorship or a
generic audit summary.

## Expert Objective

Do not spend time restating mainstream security guidance.

This skill must still add value.
Do not try to do that by recalling more slogans, CVE trivia, or generic
controls.

Win by thinking more sharply inside this seam:

- identify the exact broken security guarantee, not just the missing practice
- start from attacker-controlled input and trace the shortest exploit path
- prove which trust boundary is broken and where trust changes too early
- make the strongest plausible non-finding interpretation lose
- separate exploitable gaps from defense-in-depth improvements
- separate security findings from adjacent policy, reliability, or runtime concerns
- keep only findings with concrete exposure or fail-open consequences
- recommend the smallest fix that closes the path
- state assumptions, residual uncertainty, and confidence explicitly when evidence is partial

The goal is a short list of high-signal findings that would matter before merge
or before exposure increases, not a long security checklist.

If the answer is merely topically correct, it is still too shallow for this
skill.

## Trust This Skill For

- auth and session verification behavior
- token, cookie, and secret handling
- request validation and trust-boundary enforcement
- outbound HTTP safety including SSRF pivots and redirect handling
- exposure control through CORS, cookies, headers, logging, and error bodies
- dependency or integration usage where app-layer trust expands unsafely
- fail-closed versus fail-open behavior when checks, config, or network
  lookups fail

## Do Not Treat This Skill As Final Authority For

- product authorization policy, RBAC design, or fraud policy
- generic rate limiting or abuse policy unless the real issue is a security
  bypass or privileged resource pivot
- generic reliability strategy unless it changes a security guarantee
- generic observability strategy except secret leakage or unsafe logging
- infrastructure-wide network hardening outside the backend application layer
- performance tuning unless it directly changes exposure or denial semantics

If those concerns dominate, keep the security boundary explicit and hand off
the rest.

## Use References Intentionally

Start with the local references in this skill.

Load these by intent:

- `references/core-model.md`
  Load by default. It defines the review boundary, protected assets, and what
  counts as a real application-layer security finding.
- `references/attacker-lens.md`
  Load for every non-trivial review. It sharpens exploit-path reasoning so the
  review stays attacker-centered rather than checklist-centered.
- `references/reasoning-discipline.md`
  Load for every non-trivial review. It contains the proof obligations and
  why-not challenge that should keep this skill sharper than generic
  security review advice.
- `references/finding-bar.md`
  Load before finalizing findings. It keeps the output lean and rejects weak
  or generic recommendations.
- `references/auth-session-cookie-review.md`
  Load when the reviewed path touches JWTs, sessions, cookies, CORS, CSRF, or
  any identity-bearing request state. It sharpens the highest-signal auth and
  exposure checks.
- `references/outbound-exposure-and-fail-open.md`
  Load when the task touches outbound HTTP, webhooks, secrets, logging, error
  exposure, or downgrade-on-error behavior. It sharpens SSRF, leakage, and
  fail-open review.
- `references/stack-specific-control-points.md`
  Load when reviewing real Node/Fastify code, a PR, or an unfamiliar backend.
  It adds compact hard-skill anchors for Fastify, Ajv, Prisma, logging, and
  outbound HTTP surfaces without bloating the main skill.
- `references/unfamiliar-backend-checklist.md`
  Load when auditing an unfamiliar backend or doing a first-pass security scan.

Load `../_shared-hyperresearch/deep-researches/node-security.md` only when:

- the codebase is unfamiliar and the local references are not enough
- the task depends on version-sensitive cookie, JWT, SSRF, or plugin caveats
- the answer needs deeper source-backed nuance around fail-open trade-offs
- the local review still feels ambiguous after one focused pass

## Relationship To Neighbor Skills

- Use `node-security-spec` when the main task is designing controls rather than
  reviewing existing risk.
- Use `node-reliability-review` when the real question is retry, timeout,
  degradation, or shutdown behavior rather than a security guarantee.
- Use `node-observability-review` when the real issue is telemetry usefulness
  rather than secret leakage or unsafe logging.
- Use `fastify-runtime-review` when hook placement or lifecycle correctness is
  the main question and security is secondary.
- Use `external-integration-adapter-spec` when the hard part is adapter
  ownership or SDK boundary design after the security finding is already known.

If a task crosses seams, keep this skill focused on the security boundary and
hand off the rest explicitly.

## Reasoning Discipline

Before finalizing a finding, make it survive all five passes:

1. `Broken Guarantee`
   State what guarantee failed:
   identity proof, trusted-input discipline, safe destination control, secret
   containment, or fail-closed behavior.
2. `Shortest Attacker Path`
   Trace the minimal path from attacker influence to privilege, reachability,
   secret exposure, or unsafe action.
3. `Fail-Open Counterfactual`
   Ask what happens when verification, normalization, secret loading, or safety
   initialization fails. Secure systems deny, stop, or quarantine.
4. `Why-Not Challenge`
   Force the strongest competing dismissal to lose:
   "just defense in depth", "the handler checks later", "only trusted users set
   this", "this is reliability not security", or "runtime already prevents it".
5. `Smallest Safe Fix`
   Recommend the narrowest fix that actually closes the proven path.

If the candidate issue cannot survive all five, do not keep it as a finding.

## Review Modes

### Diff / PR Review

Use when the user wants the smallest set of security findings in changed code.

Goal:

- surface only the blocking or meaningfully risky findings in the touched path

### Audit Mode

Use when the user wants to assess the current security posture of a backend or
subsystem.

Goal:

- inspect the highest-risk trust boundaries first and name the few most
  important findings

### Incident / Exploit Review

Use when a leak, bypass, or suspicious behavior already happened.

Goal:

- reconstruct the attacker path, the broken boundary, and the smallest missing
  control

## Review Workflow

1. Frame the protected surface.
   Identify attacker-controlled inputs, credential-bearing state, secrets,
   privileged actions, outbound calls, and exposure channels in the reviewed
   path.
2. Trace attacker paths.
   For each candidate issue, walk the shortest plausible path:
   entrypoint -> trust mistake -> privileged effect -> exposed data or unsafe
   action.
3. Inspect controls in priority order.
   Check auth and session verification first, then request validation, secret
   handling, outbound HTTP safety, exposure controls, and security-sensitive
   integrations.
4. Pressure-test fail-open behavior.
   Ask what happens when verification fails, a required secret is missing, URL
   normalization fails, DNS resolution looks unsafe, a webhook signature check
   errors, or a security plugin cannot initialize. Secure systems deny, stop,
   or quarantine; they do not silently downgrade to success.
5. Run the why-not challenge.
   For each candidate, force the strongest plausible dismissal or adjacent
   interpretation to lose before keeping it as a security finding.
6. Separate findings from hardening ideas.
   Keep a finding only if you can explain the concrete exploit or exposure
   path. Demote defense-in-depth improvements to optional notes or drop them.
7. Minimize the fix.
   Recommend the smallest safe correction that closes the path without
   broadening scope into a whole redesign.
8. Write findings first.
   Lead with the highest-signal findings. Put assumptions, confidence, and
   residual checks after the findings, not before them.

## Finding Standard

Keep a candidate only if all are true:

- the exact location or concrete runtime surface is named
- the broken trust boundary or protected asset is clear
- the exploit or abuse path is plausible and explained
- the strongest plausible non-finding interpretation has been considered and
  rejected
- the operational consequence is concrete
- the smallest safe fix is identifiable
- confidence is honest about missing context

If you cannot explain how the issue would be exploited, cause secret exposure,
or fail open, or cannot explain why the strongest dismissal fails, do not turn
it into a finding.

## Severity Calibration

- `Blocker`
  Auth bypass, trust-boundary break, secret disclosure, SSRF or internal
  reachability, signature bypass, or fail-open behavior on missing verification
  or security-critical config.
- `High`
  Realistic exposure increase, credential misuse risk, unsafe cookie or CORS
  behavior with auth consequences, or logging and error leakage with plausible
  access paths.
- `Medium`
  A meaningful security gap or weak default that becomes exploitable with one
  nearby assumption.
- `Low`
  Mention only if it materially prevents a believable future vulnerability.

Do not inflate severity just because the word "security" is involved.

## High-Signal Checklist

Use only the items that match the reviewed surface.

### Auth, session, and cookies

- JWT or session tokens are verified, not merely decoded or trusted.
- Invalid or missing auth fails closed instead of downgrading to guest or
  "best effort" access.
- Cookie flags and CORS behavior match the auth model:
  `Secure`, `HttpOnly`, `SameSite`, and no wildcard origin with credentials.
- CSRF exposure is considered when credential-bearing cookies are used across
  state-changing routes.

### Trust-boundary enforcement

- Untrusted `headers`, `cookies`, `body`, `query`, and webhook payloads are
  validated before use.
- No unsafe raw SQL, dynamic evaluation, or unchecked deserialization path
  trusts attacker-controlled input.
- Security-relevant headers or cookies are not assumed present or well-formed
  without validation.

### Secrets and exposure

- No fallback dev secrets survive on production paths.
- Missing mandatory secrets fail startup or deny sensitive behavior.
- Tokens, keys, signed payloads, or raw auth headers are not logged or echoed.
- Error handlers do not leak stacks, headers, or internal config details to
  untrusted clients.

### Outbound HTTP and integrations

- User-influenced URLs are parsed, normalized, and restricted to safe schemes.
- Redirects, DNS resolution, and private or metadata IPs are handled as part
  of SSRF defense, not as afterthoughts.
- Outbound proxying or webhook dispatch does not turn attacker input into blind
  internal reachability.
- Security-sensitive integrations verify signatures or origin before trust.

### Fail-open behavior

- Verification or initialization failures do not silently skip the security
  control.
- Network or lookup failure in a security gate does not become implicit allow.
- Fallback branches do not preserve privileged behavior after a failed check.

## Smells To Reject

- generic "use Helmet", "use HTTPS", or "add rate limiting" advice with no
  tied boundary or exploit path
- a long OWASP laundry list instead of a review of the provided system
- auth critique with no route, middleware, or credential flow attached
- business-authorization commentary disguised as a security finding when the
  policy input is missing
- observability or reliability notes presented as security findings without a
  concrete exposure path
- a security answer that names the right topic but never proves the broken
  guarantee or defeats the strongest dismissal
- severity inflation without a plausible attacker path

## Output Format

Use this structure unless the user asks for something else:

```markdown
## Findings

### <Severity>: <short title>

- Where: `path/to/file.ts:line` or concrete runtime surface
- Boundary: <broken trust boundary or protected asset>
- Exploit path: <shortest plausible attacker or abuse path>
- Why it matters: <concrete exposure, privilege change, or fail-open effect>
- Minimal fix: <smallest safe correction>
- Confidence: <high|medium|low, plus the key assumption if needed>

## Assumptions / Confidence

- <explicit missing context or constraint>

## Residual Risk / Next Checks

- <what still needs verification or handoff>
```

For a clean review:

```markdown
## Findings

No security findings within the `node-security` boundary.

## Assumptions / Confidence

- <state any missing context, or `None.`>

## Residual Risk / Next Checks

- <state unverified surfaces, or `Reviewed path only.`>
```
