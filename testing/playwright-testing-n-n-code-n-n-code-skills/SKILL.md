---
name: playwright-testing
description: Use for explicitly requested live browser investigation with `playwright-cli`, or for writing, debugging, reviewing, or hardening Playwright tests in an existing working harness across Node, Python, .NET, or Java. Covers flake triage, locator refinement, visual and responsive checks, test structure, fixtures, auth-state use, and mock boundaries. Generic ad hoc Chrome work defaults to `chrome-devtools-axi`. Not for installing or repairing runner config, browser binaries, reusable-auth plumbing, or CI harnesses; use `setup-playwright`.
---

# Playwright Testing

Turn a focused browser question or named product claim into the smallest
durable evidence. Preserve the repository's runner and language; do not
translate every Playwright task into Node Playwright Test.

## Choose The Lane

Route by the artifact and state model, not by the word “Playwright.”

### Live investigation

Use `playwright-cli` when the user explicitly selects Playwright investigation
or when the investigation serves the Playwright test work owned by this skill.
Inspect the running app, reproduce behavior, or collect evidence. This lane
does **not** require a repo-owned test harness and does not authorize adding
one. Keep the CLI agent-side unless the user asks for repo changes.

Generic ad hoc Chrome investigation and browser use default to
`chrome-devtools-axi`. Preserve an explicitly chosen browser/tool and its
session. AXI findings may feed a durable Playwright test; this skill owns that
test artifact and the existing runner's behavior.

Load [references/playwright-cli-investigation.md](references/playwright-cli-investigation.md).

Use the executable's help and official Playwright documentation for current
command mechanics. This package supplies the investigation and test workflow;
no separately installed skill is required. Verify runtime help when a local
example or documentation page describes a different version.

### Existing-harness test work

Use this lane when a working Playwright harness exists and the main artifact is
a spec, test review, locator change, flake diagnosis, mock decision, or visual
check. Inspect the active ecosystem before choosing syntax or commands.

Load [references/ecosystem-testing.md](references/ecosystem-testing.md) for
Python, .NET, or Java, or whenever runner semantics are uncertain.

For review-only requests, inspect the tests and report findings without editing
specs, generating tests, or accepting new snapshots. Use only safe verification
within scope; a baseline update cannot substitute for explaining a regression.

### Setup or repair

Use `setup-playwright` when the requested artifact is package installation,
browser installation, runner config, `webServer`, project wiring, reusable-auth
plumbing, or CI shape. If the user wants both a new harness and tests, apply
`setup-playwright` first, then return here for the specs.
Persisted `@playwright/cli` tooling and Playwright Test Agent definitions also
belong to `setup-playwright`; Test Agents require a compatible Node Playwright
Test harness rather than a generic sidecar.

## Adjacent Skills

- Add `tester-mindset` when the claim, risk model, oracle, or edge cases are
  still the main unknown. It is optional for routine authored checks.
- Add `ui-guidance` or `ui-design-guidance` when visual quality,
  accessibility, interaction, or responsive behavior is itself under review.
- Use `security` first when the job is explicitly a security review. Add
  `security-identity-access` only when the scope centers on authentication,
  sessions, recovery, federation or account linking, invitations, or tenant
  authorization.

## Core Workflow

1. **Name the question or claim.** For investigation, state what is unknown and
   what observation would answer it. For a test artifact, state the behavior,
   user or system at risk, oracle, and what passing would not prove. Keep E2E
   coverage focused on journeys whose browser integration matters.
2. **Inspect the apparatus.** For test work, read the runner config, nearby
   specs, fixtures, auth helpers, page objects, package scripts, and CI hints.
   Record the language, runner, base URL, browser scope, retries, artifact
   policy, startup contract, and isolation model. For live investigation,
   confirm the target URL and allowed environment instead.
3. **Observe before encoding.** Reproduce uncertain behavior with the existing
   runner's UI/debug tools or `playwright-cli`. Use snapshots and generated
   locators as evidence, not as code to paste unreviewed.
4. **Branch at the requested artifact.** For investigation-only work, stop once
   the question has sufficient observed evidence and proceed to reporting. If
   tests are requested, design proportional happy, failure, boundary, role, or
   viewport cases because they protect the claim—not to satisfy a fixed count.
5. **Implement tests in the native runner.** Follow neighboring structure and
   naming. Add page objects, fixtures, parameterization, or mocks only when
   repetition, isolation, or a deliberate boundary justifies them. Skip this
   step for investigation-only work.
6. **Validate the active lane narrowly.** Reproduce the observation in the CLI,
   or run the smallest supported file, test, browser, or filter. Inspect traces,
   reports, snapshots, console, and requests before changing timeouts or
   retries.
7. **Harden or broaden only when risk warrants it.** Repeat the observation or
   targeted test enough to challenge the suspected failure mode. Expand
   browsers, devices, workers, or CI coverage only when the question or claim
   needs that evidence.
8. **Report narrowly.** Separate observed behavior, test results, inference,
   mocks or exclusions, and residual risk.

## Durable Authoring Rules

Apply these as risk-based defaults, not grammar checks.

- Assert observable product behavior. Actions, HTTP success, or absence of an
  exception are not automatically a user-facing oracle.
- Prefer role, label, placeholder, text, alt text, title, or agreed test-id
  locators. Refine ambiguity rather than hiding it with `first()`, `nth()`,
  CSS, XPath, or `force: true`.
- Use the active ecosystem's retrying assertions. Avoid one-shot reads such as
  `expect(await locator.isVisible()).toBe(true)` when a web-first assertion is
  available.
- Synchronize on meaningful UI, URL, event, or request state. Do not use fixed
  sleeps or `networkidle` as a generic readiness signal.
- Prefer `fill()` for ordinary text entry; use per-key entry only when the app
  genuinely reacts to each keystroke.
- Keep tests independent and data ownership explicit. Derive unique data from
  a stable seed or worker identity when parallelism matters, and clean up
  persistent server-side state.
- Treat pass-on-retry as flakiness evidence. Retries collect evidence; they do
  not convert an unreliable check into a clean pass.
- Scope timeout changes to the slow assertion, action, fixture, or test whose
  budget is understood. In Node Playwright Test, `expect(...).toPass()` has no
  useful default polling timeout, so set one explicitly.
- Wait for popups, downloads, dialogs, and similar events before triggering the
  action. Use frame-aware APIs for iframes.
- Reuse configured auth state when login is not the claim. Keep roles in
  separate contexts, and never commit credentials or saved authenticated
  state.
- Mock only an intentional boundary or failure mode. Do not mock the behavior
  being proved; account for service workers when request interception appears
  ineffective.
- Use screenshot assertions only when rendering is the contract and the
  environment can keep baselines meaningful. Automated accessibility scans and
  ARIA snapshots are evidence, not complete accessibility signoff.
- Treat difficult testability as product feedback when hidden state, real-time
  coupling, inaccessible controls, or uncontrolled side effects are the root
  cause.

## Debugging Order

1. Re-run one failing case with the same project and environment.
2. Open the first available trace or report before editing the test.
3. Classify the failure: product behavior, assertion or locator, test data or
   isolation, auth state, mock boundary, startup/config, or environment.
4. For suspected flakes, vary one dimension at a time: worker count, headed
   mode, browser project, retries, locale/timezone, or repeated runs.
5. Fix the cause, rerun the narrow case, then the affected suite. Do not widen
   assertions or add sleeps merely to turn the run green.

If browser binaries, ports, sandboxing, build locks, or runner configuration
are the cause, hand the repair to `setup-playwright` (and use
`project-platform-diagnose` while an environment-dependent cause is still
uncertain).

Load [references/debugging-and-visual-qa.md](references/debugging-and-visual-qa.md)
for Node runner commands, trace inspection, UI Mode, `codegen`, and visual
checks.

## Reference Map

- [references/ecosystem-testing.md](references/ecosystem-testing.md) — runner
  and command boundaries for Node, Python, .NET, and Java.
- [references/testing-patterns.md](references/testing-patterns.md) — Node
  Playwright Test examples for fixtures, auth use, parameterization, route/HAR
  mocking, roles, and test steps.
- [references/browser-boundaries.md](references/browser-boundaries.md) —
  iframes, events, API contexts, clock control, and accessibility probes.
- [references/playwright-cli-investigation.md](references/playwright-cli-investigation.md)
  — live snapshots, sessions, request inspection, tracing, and paused-test
  attachment.
- [references/debugging-and-visual-qa.md](references/debugging-and-visual-qa.md)
  — runner-side debugging and visual evidence.
- [references/pressure-tests.md](references/pressure-tests.md) — shortcut
  rationalizations and expected responses; load only when those pressures are
  present or when maintaining the skill.

## Output Contract

Report:

- **Question or claim:** unknown investigated or behavior/risk tested
- **Observations or cases:** browser observations and/or checks implemented or reviewed
- **Evidence:** exact commands, artifacts, and observed results
- **Interpretation:** what the evidence supports versus merely suggests
- **Residual risk:** mocks, browsers, roles, environments, or behaviors excluded

For maintainer provenance and routing fixtures, use
[references/coverage-and-validation.md](references/coverage-and-validation.md).
