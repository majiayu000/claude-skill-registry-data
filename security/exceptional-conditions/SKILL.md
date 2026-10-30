---
name: exceptional-conditions
description: Detects error handlers that leak stack traces or fail open on exception. Use
  when writing error handlers, exception catching blocks, try/catch/finally
  constructs, or API error responses. Also invoke when an application could
  fail open on exception, or when stack traces might reach end users.
---

# Exceptional Conditions Security Check (A05:2025)

## What this checks

Protects against information disclosure and fail-open logic. Stack traces in API responses leak internal paths, library versions, and logic for attackers to target; swallowed exceptions and default-allow error paths grant unintended access.

## Vulnerable patterns

- Error handler that returns the raw exception message, stack trace, or internal path in the HTTP response body
- Catch block that silently swallows exceptions with no logging, re-raise, or controlled error
- Authorization or permission exception caught and turned into a success or fall-through that grants access
- Debug or verbose-error flag enabled at deployment, exposing tracebacks to clients
- Default framework error page left in place, leaking file paths, library versions, or framework banner

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Client responses carry no internal detail.** No stack trace, no file path, no
   library version, no raw exception message. The client gets a generic message
   and an opaque reference ID; the full traceback goes to a server-side log keyed
   by that same ID.
2. **No catch block exits silently.** Every catch / except / recover takes a
   definite action: re-raise, log, or return a controlled error. A bare catch-and-pass
   is the exact bug this skill prevents.
3. **Authorization failures fail closed.** A permission or access-denied exception
   inside a catch block must produce a deny response — never a fall-through or
   default-allow. The safest pathway on ambiguity is refusal.
4. **Debug / verbose-error flags are off at deployment.** The framework's
   production-mode switch is set explicitly, not left at its development default.
5. **Every unhandled exception produces a server-side log entry containing a
   correlation ID** that matches the opaque reference returned to the client, so
   operators can reconstruct the failure without leaking internals to the user.

Translate these principles to the audited file's language and framework. Use the
documented error-handler hook, production-mode switch, and logging facility for
that stack — do not invent ad-hoc traceback formatters or response shapes.

## Verification

Confirm the following *properties* hold (language-agnostic):

- [ ] No stack trace, file path, library version, exception message, or other internal detail reaches the client response body — only a generic message and opaque reference ID
- [ ] Every catch/except/recover block takes a definite action (re-raise, log, or return a controlled error) — no silently swallowed exceptions
- [ ] Authorization and permission failures produce a deny response (HTTP 401/403, or equivalent error return) — never a success or fall-through that grants access
- [ ] If the code configures a server or application entry point, debug/verbose-error flags are explicitly set to off using the framework's documented production-mode switch. Skip this criterion for library-level code or handlers that have no configuration surface
- [ ] Every unhandled exception produces a server-side log entry containing a correlation ID (UUID or equivalent) that matches the opaque reference returned to the client

## References

- CWE-388 ([Error Handling](https://cwe.mitre.org/data/definitions/388.html))
- CWE-391 ([Unchecked Error Condition](https://cwe.mitre.org/data/definitions/391.html))
- CWE-209 ([Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html))
- [OWASP A05:2025 Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
