---
name: header-injection
description: Detects HTTP response header construction from user input vulnerable to CRLF
  injection. Use when writing code that sets HTTP response headers using
  values from user input, request parameters, or external data. Also invoke
  when constructing email headers, Content-Disposition filenames, or Location
  headers from caller-controlled strings.
---

# HTTP Header Injection Security Check (CWE-113)

## What this checks

Protects against HTTP response header injection where user input containing CR/LF
characters is included in response headers, allowing attackers to inject arbitrary
headers or split the HTTP response. Exploitation leads to cache poisoning, session
fixation, XSS via injected headers, and response splitting.

## Vulnerable patterns

- Response header value set directly from a request parameter with no CR/LF stripping
- `Content-Disposition` filename interpolated from user input without normalization
- `Location` redirect header built from a caller-supplied URL with no validation
- Forwarded request header (correlation ID, user agent, custom header) echoed into an outgoing response without sanitization
- Email or SMTP header value built from form input without rejecting newline characters

## Fix immediately

Flag the vulnerable code and explain the risk. Translate the principles below to the
audited file's language and HTTP framework — use that stack's documented header API
and string-sanitization helpers.

For each finding, establish these properties:

1. **Every header value derived from user input is stripped of CR/LF before it
   reaches the header-set call.** A single newline sequence in a value ends the
   header block and starts a new header (or a new response body). The strip
   happens at or before the call site — relying on the framework to reject it is
   fragile across versions.
2. **Forwarded headers are sanitized too.** Values read from incoming requests
   (correlation IDs, user agents, custom headers) are attacker-controlled just
   like form inputs. Echoing them into outgoing responses or logs without
   stripping is the same vulnerability.
3. **Content-Disposition filenames are normalized** — CR/LF stripped, quotes
   escaped, and for international characters use the RFC 5987 `filename*` form
   rather than raw UTF-8 in the header value.
4. **Redirect Location headers are validated too.** A newline sequence in the
   target URL splits the response; see the `open-redirect` skill for target-host
   validation.

## Verification

- [ ] Every HTTP response header value derived from user input has CR and LF characters stripped or rejected before being set
- [ ] Content-Disposition filenames from user input are sanitized for CR/LF and special characters
- [ ] Forwarded headers (correlation IDs, request IDs) from incoming requests are sanitized before inclusion in outgoing responses

## References

- CWE-113 ([Improper Neutralization of CRLF Sequences in HTTP Headers](https://cwe.mitre.org/data/definitions/113.html))
- CWE-93 ([Improper Neutralization of CRLF Sequences](https://cwe.mitre.org/data/definitions/93.html))
