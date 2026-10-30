---
name: logging-failures
description: Detects missing security event logs, logged secrets, and log injection through
  user input. Use when writing logging code, audit trails, error handlers that
  log, authentication event recording, or any code that writes security-
  relevant events. Also invoke when logging user inputs, API responses, or
  system actions that touch sensitive data.
---

# Security Logging and Monitoring Failures Security Check (A09:2025)

## What this checks

Protects the ability to detect and respond to attacks. Missing security event logs
leave breaches undetected; logging sensitive fields creates new data-exposure
vulnerabilities; CRLF injection lets attackers forge log entries.

## Vulnerable patterns

- Log statement that interpolates a credential, token, or other secret as a value
- Authentication failure, authorization denial, or privileged action that exits without producing a log record
- Log call that dumps a full request body, response, or other payload containing PII or tokens
- User-controlled string interpolated into a log line without CRLF/newline stripping, allowing forged log entries
- Unstructured string logs that a SIEM cannot reliably parse or alert on

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Every security-relevant decision point emits exactly one log record.**
   Authentication outcomes, authorization outcomes, privileged actions — no branch
   silently exits. A successful login and a failed login should both produce a
   record; a missing failure log is as bad as no logging at all.
2. **Credential-like fields never appear as values.** Names like password, token,
   secret, authorization, api_key, session, credit_card, ssn are either omitted or
   redacted before the log call. Do this at the logger, not at every call site — a
   forgotten call site is a guaranteed leak.
3. **Every user-controlled string passes through a CRLF/newline stripping step
   before reaching the log sink** — including fields that "look safe" like
   usernames, and including any dedicated actor/subject/user-id parameter. A
   username containing an embedded newline followed by a forged event prefix
   smuggles fake log lines whether it arrives as a positional argument or a
   keyword argument.
4. **Records are structured key/value data — not an interpolated message string.**
   A SIEM should be able to read fields directly; a regex-parsed message string
   misses things attackers can exploit.
5. **Each record carries an event-type identifier and an actor identifier.** The
   actor is a non-null field naming who or what triggered the event — a user id,
   session id, an explicit anonymous marker, or a system marker for
   server-initiated jobs. Never silently omitted.

Translate each principle to the logging framework and structured-logger conventions
of the audited file's language. Use the framework's documented structured-event API
— do not hand-build log lines from string interpolation.

## Verification

Confirm these properties hold (language-agnostic):

- [ ] Every security-relevant decision point (authentication outcome, authorization outcome, privileged action) emits exactly one log record — no branch silently exits without logging
- [ ] Credential-like field names (password, token, secret, authorization, api_key, session) never appear as values in any log record — they are omitted or redacted before the log call
- [ ] Every user-controlled string reaching a log sink passes through a CRLF/newline stripping step — including fields that look safe like usernames, and including dedicated actor/subject/user-id parameters
- [ ] Log records are emitted as structured key/value data — not as a single interpolated message string that a SIEM would have to regex-parse
- [ ] Each record carries an event-type identifier and a non-null actor identifier (user id, session id, anonymous marker, or system marker for server-initiated jobs)

## References

- CWE-117 ([Improper Output Neutralization for Logs](https://cwe.mitre.org/data/definitions/117.html))
- CWE-223 ([Omission of Security-relevant Information](https://cwe.mitre.org/data/definitions/223.html))
- CWE-532 ([Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html))
- [OWASP A09:2025 – Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
