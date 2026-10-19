---
name: web-security-testing
description: >
  Plan and run authorized, defensive security testing of web applications you own or
  have written permission to test (localhost, a dev/staging environment, or an explicitly
  scoped target), organized by the OWASP Web Security Testing Guide: scoping and rules of
  engagement, passive reconnaissance, security headers and cookies, authentication,
  session, authorization (IDOR), input handling, client-side, and API checks, with
  evidence-based reporting and remediation. Use when asked to security-test your own web
  app, verify fixes, review a scan result, or write a test plan. Refuses unauthorized
  targets and does not provide exploit payload collections. Do not use for source-code
  review (security-code-review), writing secure code (secure-coding), threat modeling
  (threat-modeling), or browser bug hunting (browser-debugging).
compatibility: >
  Any web app reachable from the tester's machine; tools include a browser with DevTools,
  curl, an intercepting proxy such as OWASP ZAP, and Playwright for repeatable checks.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "web-security, owasp, wstg, appsec, headers, cookies, authz, idor, defensive"
  topics: "security, web, testing"
---

# Web Security Testing (Authorized, Defensive)

The goal is to find and fix weaknesses in applications you are responsible for, with proof a developer can reproduce. This skill is a method, not an attack toolkit.

Related skills: `security-code-review` (read the code), `secure-coding` (fix patterns), `threat-modeling` (decide what to test), `oauth-jwt-auth`, `secrets-management`, `playwright-testing` (turn findings into regression tests), `browser-debugging`, `github-actions-security`.

## Authorization gate (do this first, every time)

Proceed only if at least one is true and you can state which:
1. The target is `localhost`/`127.0.0.1` or a throwaway environment you started.
2. The target is the user's own application in a dev/staging environment they control.
3. The user provides explicit written scope (targets, dates, allowed techniques, contacts), such as a signed rules-of-engagement or bug bounty policy that covers this asset.

If none holds, or the target is a third-party site, a shared production system without permission, or the scope is ambiguous, stop and ask. Do not "just look". Ownership of a domain does not authorize testing a third-party service it embeds (CDN, SaaS, identity provider).

## Non-negotiable rules

1. **Stay in scope.** Only listed hosts, paths, and techniques. Re-check scope before each new target or tool.
2. **Least intrusive first.** Passive observation and read-only requests before anything that changes state. No denial-of-service, no load tests, no brute-forcing real accounts, no social engineering, no destructive actions, no mass data extraction.
3. **Use test accounts and synthetic data.** Never touch real users' data. If you accidentally see real personal data, stop, do not copy it, and report it to the owner.
4. **Proof of concept, minimal.** Demonstrate impact with the smallest harmless evidence (for example, a second test account's object ID returning 200, not a dump of records). Do not collect, store, or exfiltrate secrets, tokens, or personal data; redact them in reports.
5. **No exploit payload dumps.** Describe vulnerability classes, test conditions, and expected secure behavior; use benign canary values (a unique harmless string) to test reflection or handling.
6. **Production caution.** Prefer staging. If production is explicitly in scope, agree timing, rate limits, and a stop condition. Respect rate limits and avoid triggering alerts unannounced.
7. **Disclose responsibly.** Findings go to the owner privately with a fix suggestion; no public disclosure without agreement.

## Workflow

### 1. Scope and plan
Record targets, environments, accounts/roles to be used (at least two ordinary users and one admin for authorization tests), allowed tools, time window, rate limits, data handling, and contacts. Use a threat model or the app's feature list to prioritize (login, payments, file upload, admin, APIs).

### 2. Map the application
Browse as a normal user with DevTools open and, if allowed, an intercepting proxy (OWASP ZAP in manual-explore mode). Inventory pages, forms, API endpoints, roles, parameters, third-party scripts, and where user input is stored and reflected. Check `robots.txt`, `sitemap.xml`, and published API docs (OpenAPI) that the owner intends to be public.

### 3. Test by WSTG category
The OWASP Web Security Testing Guide (stable v4.2) organizes tests into: Information Gathering (INFO), Configuration and Deployment Management (CONF), Identity Management (IDNT), Authentication (ATHN), Authorization (ATHZ), Session Management (SESS), Input Validation (INPV), Error Handling (ERRH), Cryptography (CRYP), Business Logic (BUSL), Client-side (CLNT), and API Testing (APIT). Use it as the checklist; pull per-test IDs into your plan.

Examples of safe, high-value checks:

- **Transport and headers (CONF/CRYP)**: HTTPS everywhere with redirect from HTTP; `Strict-Transport-Security`; `Content-Security-Policy` (avoid `unsafe-inline`/wildcards where possible); `X-Content-Type-Options: nosniff`; `Referrer-Policy`; framing protection via `Content-Security-Policy: frame-ancestors`; `Permissions-Policy`. Inspect with `curl -sI https://target.example` or the Network panel.
- **Cookies (SESS)**: session cookies have `Secure`, `HttpOnly`, and an appropriate `SameSite`; scope (`Domain`/`Path`) is minimal; session ID rotates at login and is invalidated at logout and password change.
- **Authentication (ATHN)**: generic error messages (no account enumeration), lockout or throttling on repeated failures (test with your own test account at a gentle rate), password reset tokens are single-use, expiring, and unguessable, MFA cannot be bypassed by direct navigation.
- **Authorization (ATHZ)**: for each endpoint and object, test with user A's session against user B's object IDs (IDOR/BOLA), a low-privilege role against admin functions (function-level authorization), and unauthenticated access. Compare expected vs. actual status codes (403/404 vs 200).
- **Input handling (INPV)**: send unique benign canary strings and observe where they reappear (HTML, attributes, JavaScript, URLs) and whether output is context-encoded; verify parameterized queries by reviewing code (`security-code-review`) rather than injecting destructive input; check file upload type/size/storage rules and that uploads are not served from an executable path.
- **Client-side (CLNT)**: no secrets in JS bundles or source maps; `postMessage` handlers check origin; `localStorage` does not hold long-lived tokens where an XSS would expose them; third-party scripts use Subresource Integrity where feasible.
- **Errors and information leakage (ERRH/INFO)**: no stack traces, framework versions, or internal hostnames in responses.
- **API (APIT)**: authentication on every route, object- and property-level authorization, input schema enforcement, rate limits, unintended HTTP methods, verbose errors, CORS policy not reflecting arbitrary origins with credentials.
- **Business logic (BUSL)**: step skipping, repeating one-time actions (coupon reuse), negative quantities, race conditions on balances. Test only in staging with test data.

### 4. Automated scanning (carefully)
Passive scanning, against in-scope targets only, is generally safe: for example OWASP ZAP's baseline scan runs a spider and passive rules only (check the ZAP docs for the current command and image, for example `zap-baseline.py -t https://staging.example.test` from the official container image). Active scanning sends attack traffic and can modify data or degrade a service; run it only where scope explicitly allows, against staging with test data, and with the owner aware. Treat every scanner finding as a hypothesis: confirm manually, remove false positives, and note the confidence.

### 5. Triage and rate
For each confirmed issue record: title, affected asset, WSTG reference, preconditions (role, state), reproduction steps, evidence (redacted), impact in terms of confidentiality/integrity/availability, severity (state the method, e.g. CVSS v3.1/v4.0 vector or a simple High/Medium/Low rubric, plus exploitability and exposure), and a remediation recommendation (link to `secure-coding` patterns).

### 6. Report and retest
Deliver: scope and dates, what was and was not tested, findings ordered by risk, positive observations, and recommended fixes. After fixes, retest the exact steps and add automated regression checks (`playwright-testing`, for example asserting security headers and that user A cannot fetch user B's resource).

## Worked example

Scope: the user's own task-tracker app on `http://localhost:3000`, test users `alice` and `bob` created for this purpose.

1. Gate: localhost, own app; passes.
2. Map: `GET /api/tasks/:id` returns a task; IDs are sequential integers.
3. Authorization test: log in as alice, create task 41; log in as bob, request `/api/tasks/41`. Expected: 403 or 404. Observed: 200 with alice's task body (use only the test data). Confirmed broken object-level authorization (WSTG ATHZ category).
4. Evidence: request/response summary with session cookies redacted.
5. Remediation: enforce ownership in the data-access layer (`WHERE id = $1 AND owner_id = $2` with the authenticated user), prefer non-guessable identifiers as defense in depth, return 404 for non-owned objects.
6. Retest and regression test:
```ts
import { test, expect } from "@playwright/test";

test("bob cannot read alice's task", async ({ request }) => {
  // Assumes fixtures that log in test users and create the task; names are illustrative.
  const res = await bobApi.get(`/api/tasks/${aliceTaskId}`);
  expect([403, 404]).toContain(res.status());
});
```

## Anti-patterns

- Testing a target because it "looks like" the client's, without written scope.
- Running an active scanner against production by default.
- Reporting raw scanner output as findings without validation.
- Exfiltrating real data to "prove" impact.
- Hunting only for injection while missing authorization and business-logic flaws (the common high-impact bugs).
- Testing with one account only.
- Publishing findings before the owner can fix them.
- Copying payload lists from the internet and spraying them at endpoints.
- Vague findings without reproduction steps or fix guidance.

## Verification checklist

- [ ] Authorization gate satisfied and documented
- [ ] Scope, window, rate limits, and contacts recorded
- [ ] Test accounts and synthetic data only
- [ ] Passive checks done before active ones; active ones explicitly approved
- [ ] Each finding confirmed manually, with redacted evidence and severity method
- [ ] Remediation and retest steps included; regression tests added
- [ ] Report states what was not tested

## References

- [Test plan template and evidence format](references/test-plan-template.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
