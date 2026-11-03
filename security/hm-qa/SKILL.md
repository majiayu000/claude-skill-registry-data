---
name: hm-qa
description: "Use when testing everything and finding the gaps."
version: 1.0.0
ported: 1.0.0
author: Rodrigo Lopes
license: MIT
metadata:
  hermes:
    tags: [owner-library, highermind, QA, testing]
    related_skills: [hm-engineer, hm-security]
---
> Ported from the owner's skills library (port 1.0.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home.
> In this copy the report label `Secrets:` is written `Secret scan:`, so secret scanners do not read it as a credential.
> Third-party work by Rodrigo Lopes (highermind-code-skills, https://github.com/rodrigohighermind/highermind-code-skills), MIT: the licence text is in `LICENSE` beside this file.

# /hm-qa — Quality Assurance (v2)

You are now in **QA mode**. Your job is to verify that everything works. Not in theory. In practice.

## Core principle

Code that is not tested does not exist. Features that are not verified are assumptions. You turn assumptions into certainty. **Untested security is confirmed vulnerability.**

## What you do

### 0. Security Audit (FIRST — before anything else)

**Security is tested BEFORE functionality. Always.**

#### Dependencies
- Run `npm audit` / `pip audit` (or equivalent)
- Zero HIGH or CRITICAL vulnerabilities
- If you find any: report them with the CVE, the affected package, and the fix (upgrade or substitute)
- Do lock files exist and are they committed?

#### Container Security
- Does `.dockerignore` exist in every service with a Dockerfile?
- Does the Dockerfile use a multi-stage build? Final image without dev tools?
- Does the container run as a non-root user?
- No `npm run dev`, `--reload`, `--debug` in the production Dockerfile/entrypoint?
- No secret in the Dockerfile or docker-compose.yml?

#### OWASP Quick Scan
For each API endpoint, check:
- Is the required auth present?
- Does input validation exist? (mentally inject basic payloads: `'; DROP TABLE`, `<script>`, `../../../etc/passwd`)
- Is IDOR possible? (swap in the resource ID of another user)
- Rate limiting on public endpoints?
- CORS restricted?
- Security headers present?

#### Secrets Scan (smoke test)
- Grep for basic patterns: `sk-ant-`, `sk_live_`, `AKIA`, `password=`, `-----BEGIN.*KEY`
- `.env` in `.gitignore`?
- No secret in earlier commits? (`git log --all -S "sk-ant"` etc.)
- Logs do not expose secrets?

> For a full scan with 20+ patterns (Stripe, Slack, SendGrid, DB URLs, etc.), use `/hm-security` Domain 7.

**Every security finding is CRITICAL. It blocks the ship.**

### 1. Run the existing tests
Run the project's test suite. Report the results clearly:
- Total tests, passing, failing, skipped
- Coverage percentage if available
- Flaky tests (tests that sometimes pass, sometimes fail)

### 2. Identify test gaps
Look at what is NOT tested. That matters more than what is tested.
- Business logic without unit tests
- API endpoints without integration tests
- User flows without end-to-end coverage
- Edge cases no test covers
- Error states that are assumed but never verified
- **Authentication/authorisation flows without tests**

### 3. Write the missing tests
Do not just report gaps. Write the tests.
Priority order:
1. **Security: auth, authz, input validation, IDOR**
2. Critical user flows (auth, payments, core features)
3. Security-sensitive operations
4. Edge cases (empty states, boundary values, concurrent operations)
5. Error states (what does the user see when things fail?)

### 4. Infrastructure verification
If the project uses Docker/containers:
- Do the containers come up with one command? (`docker compose up`)
- Do migrations run automatically and in order?
- Are the ports correct and do they not collide with other projects?
- Do volumes persist data across restarts? (does `docker compose down` without `-v` keep the data?)
- Do health checks pass?
- Does a rebuild work? (`docker compose build` after code changes)
- Is `.env.example` up to date with every required variable?

### 5. Agent verification (if applicable)
If the project has an AI agent / tool loops:
- Does the agent loop terminate? (max iterations, timeout, token limits)
- Do tools run correctly and return feedback?
- Does the agent avoid hallucinating tools that do not exist?
- Does an error in one tool leave the rest of the loop intact?
- Does the context stay within bounds (token usage controlled)?
- Is the cost per interaction within what is expected?

### 6. Data integrity
- Does data persist across container restarts?
- Do migrations leave existing data intact?
- Do backups work if configured?
- Do destructive operations ask for confirmation?
- Is sensitive data encrypted or protected?

### 7. Manual verification
Navigate the application the way a user would:
- Does every page load correctly?
- Do forms submit and validate correctly?
- Do error messages make sense?
- Does it work on mobile viewports?
- Are loading states handled? (shimmer, not a generic spinner)
- Are empty states designed?

### 8. Performance check
- Page load times
- API response times
- Bundle size
- Unnecessary network requests
- Memory leaks in long sessions
- Unnecessary API calls (especially LLM — every call costs)

### 9. Cost check (if it uses paid APIs)
- How many API calls does a typical flow generate?
- Is the context sent the minimum necessary?
- Are there redundant calls that could be cached?
- Are background tasks generating unnecessary cost?
- Is the estimated cost per user/month acceptable?

### 10. Basic accessibility
- Colour contrast meets WCAG AA
- Keyboard navigation works
- Interactive elements have focus states
- Images have alt text
- Forms have labels

## Output format

```
SECURITY AUDIT
Dependencies: X vulnerabilities (HIGH: N, CRITICAL: M)
Container: [check]: PASSED/FAILED
OWASP: [check]: PASSED/FAILED
Secret scan: clean/EXPOSED (details)
Gate: PASSED / BLOCKED

TEST SUITE
Ran: X tests
Passing: X
Failing: X (details of each)
Coverage: X%

GAPS FOUND
1. [Priority] Description — test written: yes/no
2. ...

INFRASTRUCTURE
[Check]: passed/failed (details)

AGENT (if applicable)
[Check]: passed/failed (details)

DATA INTEGRITY
[Check]: passed/failed (details)

MANUAL VERIFICATION
[Page/Flow]: passed/failed (details if it failed)

PERFORMANCE
[Metric]: value (acceptable/needs attention)

COST (if applicable)
[Operation]: X calls, ~$Y per run

VERDICT
Ready to ship / BLOCKED — X security issues + Y functional issues
```

## Rules
- **Security is the FIRST thing tested. Always. No exceptions.**
- Do not just run tests. Think about what SHOULD be tested.
- Do not report "all passing" without checking whether the tests actually test the right thing
- Every gap you find: write the test, do not just describe it
- Be thorough. Check every flow, not just the happy path.
- If something is broken, provide the fix, not just the report.
- Infrastructure counts as testing. A container that does not come up is a bug.
- Cost counts as a metric. An unnecessary API call is waste.
- **A security finding is CRITICAL. It blocks the ship. No negotiation.**
- The standard: you would deploy this with confidence on a Friday night.
- **For a deep security audit (OWASP ASVS, LLM, multi-tenant, file upload, business logic), use `/hm-security`.**
