---
name: mk:qa-manual
description: Spec-driven manual QA testing and Playwright E2E code generation. Orchestrates browser skills to navigate apps like a human tester, producing structured test reports or production-ready .spec.ts files. Always prompts user for credentials — never guesses or stores auth. Use for QA testing, E2E generation, login flow testing, or exploratory testing from a URL. NOT for AI-autonomous flows (see mk:agent-browser).
argument-hint: '[spec-path | url] [--report | --generate]'
orchestrates:
  - mk:agent-browser
  - mk:playwright-cli
use_cases:
  - manual-qa
  - e2e-code-generation
requires_user_input: true
auth_handling: prompt-always
keywords:
  - qa-manual
  - spec-driven-qa
  - playwright-e2e-gen
  - login-flow-test
  - exploratory-test
when_to_use: Use for spec-driven manual QA testing or Playwright E2E code generation. Always prompts for credentials — never guesses. NOT for AI-autonomous flows (see mk:agent-browser).
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

<!-- Design decisions:
- Dynamic routing model: each action uses the best skill (Phase 1.2 routing tree)
- Auth protocol: prompt-always — NEVER guess credentials (absolute constraint)
- playwright-cli preferred for DOM interaction — generates PW code as side-effect
- agent-browser preferred for auth flows — session persistence support
- Role-based locators mandatory (getByRole, getByLabel) — not CSS selectors
- Script for Playwright execution — deterministic, not LLM judgment
-->

# QA Manual Testing & E2E Code Generation

Orchestrates browser skills to act like a human tester: navigate, interact, verify, and report.

## When to Use

**Trigger:** "test this flow", "QA this page", "generate E2E tests", "test login flow", "manual testing", "write Playwright tests for"

**Explicit:**
- `/mk:qa-manual tasks/plans/260315-auth-flow.md --report` → manual QA report
- `/mk:qa-manual tasks/plans/260315-checkout.md --generate` → Playwright .spec.ts
- `/mk:qa-manual https://app.example.com` → explore and test from URL
- `/mk:qa-manual [spec]` → auto-detect use case from spec content

## Workflow Integration

Operates in **Phase 4 (Review)** for QA reports or **Phase 3 (Build)** for E2E code generation.

## Skill Routing

Each action uses the best browser skill:

| Action | Skill | Why |
|--------|-------|-----|
| DOM interaction (click, fill, type) | `mk:playwright-cli` | Generates Playwright code as side-effect |
| Navigation + page load | `mk:playwright-cli` | goto + wait, code output |
| Visual verification (screenshot) | `mk:agent-browser` | Annotated snapshots |
| Auth flow (login, session, MFA) | `mk:agent-browser` | Session persistence, auth import |
| Execute Playwright test | Script: `npx playwright test` | Deterministic |

## Authentication Protocol

**On auth encounter** (login page, MFA, 401/403):

1. **STOP** current flow immediately
2. **Show user:**
   ```
   ⚠️ Authentication required at: [current URL]
   mk:qa-manual needs credentials to continue.
   Please provide:
   - Username/email: ___________
   - Password: ___________
   Type 'skip' to skip this flow or 'abort' to stop testing.
   ```
3. **WAIT** for user input — do NOT proceed without it
4. On credentials → fill form using `mk:playwright-cli`, continue flow
5. On 'skip' → mark flow SKIPPED, move to next
6. On 'abort' → end session, output partial report

**NEVER:** Guess credentials. Use hardcoded test credentials. Proceed past auth without input. Store credentials in any file.

## Process

See `references/qa-process.md` for detailed Use Case A and Use Case B processes.

**Use Case A — Manual QA:** Load spec → extract flows → navigate each → verify outcomes → report

**Use Case B — E2E Code Gen:** Run Use Case A → record interactions → generate .spec.ts with role-based locators

## Output Format

See `references/output-templates.md` for full templates.

**QA Report** → structured pass/fail per flow with evidence
**Playwright Code** → production-ready .spec.ts using `getByRole`, `getByLabel`, `getByText`

## Scripts

| Script | Purpose | Invocation |
|--------|---------|------------|
| `scripts/run-playwright.sh` | Execute generated .spec.ts | After E2E code generation |

## References

| Reference | When to load | Content |
|-----------|-------------|---------|
| **[qa-process.md](./references/qa-process.md)** | Steps 1-4 | Detailed Use Case A + B processes |
| **[output-templates.md](./references/output-templates.md)** | Step output | QA report + Playwright code templates |

## Failure Handling

| Failure | Detection | Recovery | Message |
|---------|-----------|----------|---------|
| Auth encountered | URL/form patterns | Auth protocol above | "⚠️ Authentication required..." |
| Page load timeout | 30s timeout | Retry ×2 then report | "Page load timed out at [URL]" |
| Element not found | Selector fails | Re-snapshot, try alternate | "Element not found, re-scanning..." |
| Spec not found | File missing | Ask user | "Spec file not found. Provide path or URL." |
| Playwright exec fails | Non-zero exit | Show error + fix hints | "Test failed: [error]. Fix: [hint]" |

## Gotchas

- **Testing against stale deployment**: Running E2E tests against yesterday's build → Verify deployment version matches expected before starting test run
- **Credentials hardcoded in generated spec files**: Auto-generated .spec.ts contains login credentials → Always use environment variables for credentials; never inline in test code
