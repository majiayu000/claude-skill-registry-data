---
id: logging-security
version: "2.0.0"
title: "Logging Security"
description: "Keep secrets and personal data out of logs at the call site rather than relying on redaction, neutralize log and field injection, record audit events that survive, and treat log read access as data access. Use when generating logger calls or structured-logging schemas, wiring log shippers, sinks, retention, and access controls, or specifying audit-logging requirements."
category: prevention
severity: high
applies_to:
  - "when generating logger calls or structured-logging schemas"
  - "when wiring log shippers, sinks, retention, and access controls"
  - "when granting access to a log store"
  - "when reviewing requirements for audit logging"
languages: ["*"]
token_budget:
  minimal: 1100
  compact: 1500
  full: 1900
rules_path: "rules/"
related_skills: ["secret-detection", "error-handling-security", "api-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP Logging Cheat Sheet"
  - "CWE-532 — Insertion of Sensitive Information into Log File"
  - "CWE-117 — Improper Output Neutralization for Logs"
  - "NIST SP 800-92 (Guide to Computer Security Log Management)"
---

# Logging Security

## Rules (for AI agents)

### ALWAYS
- Decide what is safe to log **at the call site**, and log a reference rather than a
  value: an id, a hash, a type, a count. A redactor is the last net, not the design —
  it matches field names and known patterns, so it cannot see personal data sitting
  inside an assembled string. A formatted notification body, a templated message, an
  exception with interpolated arguments: the name and the address are in the prose,
  in no named field, matching no pattern. Nothing downstream will catch that.
- Run a **redactor** at the sink anyway, for the cases the call site missed:
  credential-shaped values, `Authorization` and `Cookie` headers, query strings
  carrying tokens, and the personal-data patterns in `rules/redaction_patterns.json`.
  `secret-detection` owns which literals count as a credential; this rule is that the
  redactor exists and runs before anything leaves the process.
- Log in a **structured format** (JSON or logfmt) with stable field names —
  `timestamp`, `service`, `version`, `level`, `trace_id`, `span_id`, `request_id`,
  `event`, and `user_id` when there is an authenticated one. Structure is what makes
  redaction, retention, and access control expressible per field instead of per line.
- Neutralize user-controlled strings before they enter a log record. Line injection
  (CWE-117) is the classic case — a `\n` or `\r` lets an attacker forge a whole
  record — but structured logging moves the problem: a value that parses as JSON can
  inject *fields* into the ingested document, and ANSI escape sequences (`\x1b[`) are
  interpreted by the terminal of whoever reads the log. Encode the value; do not
  concatenate it into the line.
- Record security-relevant events as **immutable audit records**: authentication
  success and failure, MFA challenges, password and role changes, permission grants
  and revocations, data export, administrative action. These carry longer retention
  and stricter access than operational logs, and they are the reason failed logins
  must keep being written even when someone calls them noise.
- Treat **read access to the log store as access to the data inside it**. A
  centralized store aggregates every tenant's records, so grant it like production
  data access — named principals, reviewed, audited — not like an observability
  convenience handed to everyone who might want to debug something.
- Set retention per data category — short for debug, long for audit — and make it
  **executed**, not declared. A retention or deletion policy that no job enforces
  looks identical to one that works, right up to the point someone asks for evidence.
- Alert on the log pipeline itself: a service that stops logging, and volume that
  departs sharply from its own baseline in either direction. Calibrate the threshold
  against that service's normal traffic rather than a fixed multiple — a job that
  runs hourly and a request path have nothing in common.

### NEVER
- Log a full request or response body, at any level. The level is not the control:
  a body captured at DEBUG in production is the same disclosure as one at INFO, and
  DEBUG in production is itself the finding.
- Log an entire bound SQL statement with its parameter values. Log the statement
  template, the parameter names, and a hashed identifier for the value.
- Use `print()` / `console.log` / `fmt.Println` in a production service. They bypass
  the redactor, the structure, and the sink — which is exactly the path by which the
  one unredacted value reaches disk.
- Write production logs only to local disk. They are lost with the pod, container or
  VM, which is usually the moment they were about to matter.

### KNOWN FALSE POSITIVES
- Health-check and load-balancer probe logs downsampled or suppressed at the balancer
  to control volume.
- A `request_id` that happens to look like a token. Pattern redactors over-redact;
  allowlist your own correlation-id prefixes.
- Anonymous public-API access logs without auth headers are not in themselves a
  privacy problem — though client IPs may still be personal data under GDPR.
- Recording the *type* of record touched ("user accessed claim record") is the audit
  trail working. The rule is against field contents, not against recording that the
  access happened.
- Long audit retention, often years, is deliberate — an exemption from the general
  retention sweep rather than an oversight in it.

## Context (for humans)

Logs are where secrets end up, and the reason is structural: logging is the one
operation a developer performs without thinking about who reads the output. Request
dumps, exception traces, debug prints and third-party SDK telemetry all default to
"write everything", and the log store is then read by more people, for longer, than
any database.

The order of the rules above is deliberate. Teams reach for a redactor first because
it is a single place to fix everything, and it does catch the credential-shaped
values. What it cannot catch is data that never looks like a credential — a customer
name inside a rendered notification, an address in an exception message, a free-text
field concatenated into an error. Those have no field name and match no pattern, and
they are most of the personal data that leaks. The call site is the only place that
knows what the value is.

The second thing worth stating plainly: the audit trail and the operational log are
different products with different retention, different access, and different
consumers. Storing them together is convenient and makes both harder to govern.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `rules/redaction_patterns.json` — the single redaction policy for this library;
  `error-handling-security` hands off to it rather than carrying its own
- `rules/audit_event_schema.json`
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
- [CWE-532](https://cwe.mitre.org/data/definitions/532.html) · [CWE-117](https://cwe.mitre.org/data/definitions/117.html).
- [NIST SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final).
