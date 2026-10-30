---
name: open-redirect
description: Detects redirects to user-controlled URLs that enable phishing and OAuth
  callback abuse. Use when writing code that redirects users to a URL from
  request parameters, form input, or any caller-controlled source. Also invoke
  when building login flows with "return to" URLs or OAuth callback redirects.
---

# Open Redirect Security Check (CWE-601)

## What this checks

Protects against open redirect vulnerabilities where an attacker crafts a link that
redirects users from a trusted domain to a malicious site. Used in phishing campaigns
to make malicious links appear legitimate, and in OAuth flows to steal authorization
codes.

## Vulnerable patterns

- Redirect target read directly from a query parameter, form field, or request body and passed unchanged to the framework's redirect API.
- Client-side navigation (`window.location` and equivalents) assigned a value derived from the URL or form input with no validation.
- "Return to" or "next" parameters on login flows that accept any URL without an allowlist check.
- Validation that uses prefix or substring matching against the allowed host — `allowed.com.evil.com` passes a naive prefix check.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and
HTTP framework — use that framework's documented URL-parsing and redirect APIs.

1. **Every redirect target is either a relative path or a member of an exact
   host allowlist.** Parse the URL, inspect the host component, and reject
   anything outside the allowlist. Prefix matching is not sufficient.
2. **Scheme-relative URLs are blocked explicitly.** A value starting with `//`
   parses as a protocol-relative URL and redirects to whatever host follows.
   Checking only for `http://` and `https://` misses this.
3. **OAuth and login "return-to" parameters go through the same validator** as
   any other redirect target. These are the highest-value targets because they
   run in an authenticated context; a redirect here hands the attacker the
   post-login session or an authorization code.
4. **On validation failure, redirect to a safe default** (home, dashboard)
   rather than echoing an error containing the malicious URL. Echoing it back
   gives attackers a reflected-XSS surface.

## Verification

- [ ] Every redirect target derived from user input is validated as either a relative path or a member of an explicit host allowlist
- [ ] Scheme-relative URLs (starting with `//`) are blocked — not just absolute `http://` and `https://` URLs
- [ ] OAuth and login "return_to" parameters are validated before redirect
- [ ] Validation failure routes to a safe default target, not back to the attacker-supplied URL

## References

- CWE-601 ([URL Redirection to Untrusted Site](https://cwe.mitre.org/data/definitions/601.html))
