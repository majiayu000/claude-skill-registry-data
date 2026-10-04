---
id: security-regression-tests
version: "2.0.0"
title: "Security Regression Tests"
description: "Turning a confirmed and fixed finding into a permanent guard: proving the test fails without the fix, asserting the effect and not only the status code, seeding the two principals an authorization test needs, making a timing or out-of-band proof deterministic enough for CI, and keeping the test in a job that can actually block. Use once a security finding has been confirmed and fixed, or when a security test is failing, skipped, or about to be deleted."
category: prevention
severity: medium
applies_to:
  - "when a security finding has been confirmed and fixed"
  - "when graduating a live proof-of-concept into a committed test"
  - "when a security test is failing, skipped, quarantined, or being deleted"
languages: ["*"]
token_budget:
  minimal: 1100
  compact: 1550
  full: 1900
related_skills: ["dynamic-verification", "cicd-security", "secret-detection", "api-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP Web Security Testing Guide (WSTG)"
  - "CWE-1006 — Bad Coding Practices"
---

# Security Regression Tests

## Rules (for AI agents)

### ALWAYS
- **Prove the test fails without the fix.** Revert the patch, or mutate the guard, and
  confirm the new test goes red — then restore. A test written after the fix can be
  vacuously green: wrong route, wrong fixture user, wrong assertion target, a typo in
  the payload. It will stay green forever and nobody will learn anything from it. This
  is the one step that distinguishes a guard from a decoration, and it is the one
  most often skipped.
- Assert **both directions**: the attack input now yields the secure outcome, *and* a
  legitimate input still succeeds. A deny-only test passes equally well against an
  endpoint that is broken for everyone, so it will hold the line and tell you nothing
  when someone disables the feature entirely.
- Assert the **effect**, not only the status code. A `403` proves the request was
  refused; it does not prove the write did not land somewhere else, that the record
  was not returned in a different shape, or that a queue message was not emitted.
  Check the state the attack was trying to reach.
- Seed the **fixtures the assertion depends on** before writing it. A cross-tenant test
  needs two principals and two owned resources, deterministically created — if both
  test users end up in the same tenant, the deny assertion is untestable and passes for
  the wrong reason.
- Make it **deterministic and offline**. Freeze the clock for expiry and TTL
  assertions, stub the HTTP client, dialer or resolver rather than reaching the
  network, fix random seeds, and avoid sleep-based timing assertions and state shared
  between tests. Note that a canonical SSRF payload such as
  `http://169.254.169.254/latest/meta-data/` is a *live, reachable* address on a cloud
  CI runner, so the naive test both leaves the sandbox and returns a different verdict
  on a laptop.
- Graduate a live proof-of-concept by keeping its **shape and dropping its mechanism**.
  `dynamic-verification` confirms some classes with a timing delta or an out-of-band
  callback, and neither survives in CI: replace the time-based payload with an
  assertion that the query was parameterized, and the callback with a stubbed dialer
  asserting no outbound request was attempted.
- Put the test in a **job that can block the merge**. A committed test in a job that is
  `continue-on-error`, not a required check, or nightly-only is documentation.
  `cicd-security` owns the gate configuration itself.
- Name it so a reviewer sees what it guards — `test_idor_orders_cross_tenant_403` —
  and reference the finding in the test body or the commit, so the next person to see
  it fail knows what it is protecting rather than what it is blocking.

### NEVER
- Close a confirmed finding without a regression test. "Fixed by inspection" rots: the
  next refactor reintroduces it, and there is nothing to notice.
- **Skip, quarantine, `xfail`, or delete** a security test to get a build green. A
  skipped security test is a removed control that still looks like a present one, and
  it is indistinguishable in a passing build from one that runs. A failing security
  test is either a real regression or a wrong test — both need a person, neither needs
  a decorator.
- Relax an assertion until it passes. Widening an expected status set, dropping the
  effect check, or accepting either outcome converts the guard into a formality.
- Put a **live-target probe in CI** as the verification. Attack traffic from a build
  agent is non-deterministic, sometimes illegal against infrastructure you do not own,
  and the reason the committed test exists.
- Put a **real** secret in a fixture to exercise a secret check. Use the documented
  sentinels that scanners already exclude by name — `secret-detection` owns them.

### KNOWN FALSE POSITIVES
- A regression test necessarily **commits attack payloads**: `' OR 1=1--`,
  `<script>alert(1)</script>`, `{{7*7}}`, `../../etc/passwd`, a fake token. The
  project's own SAST and secret scanners will re-flag them on the next run. That is
  the test doing its job — exclude the fixture path, do not weaken the payload.
- A **refuted** candidate never triggered the rule: there is no fix, so there is
  nothing to pin. This is not an exemption, it is the precondition not being met.
- A finding fixed in configuration rather than code — a base image, a workflow
  permission, a cloud setting, a dependency bump — is pinned by the **scanner gate**
  rather than a unit test, because there is no application behaviour to assert. The
  gate then needs the same both-directions proof: a fixture that fails it and one that
  passes, or nobody can tell a working gate from a misconfigured one.
- A test asserting a *narrower* outcome than the original report — a `404` where the
  report said `403`, because the application hides existence — is correct if that is
  the intended behaviour. Match the application's contract, not the report's wording.

## Context (for humans)

The failure this skill exists to prevent is not the missing test; it is the test that
exists and proves nothing. There are three common ways to get one, and the rules above
are ordered by how often each occurs: the test never fails because it does not actually
reach the vulnerable path, the test only checks the deny direction so it stays green
against a completely broken endpoint, and the test checks a status code while the
dangerous effect still happens.

The second theme is that a security test's value decays through ordinary maintenance.
Nobody deletes a control deliberately; someone adds `@pytest.mark.skip` to unblock a
release, and the skip outlives the release. A build with a skipped security test and a
build with a passing one look identical from the outside, which is why the rule against
skipping is stated as flatly as it is.

Where a finding is confirmed live rather than by reading code, the proof usually cannot
be committed as-is — a timing delta and an out-of-band callback are both properties of
a running system. What transfers is the claim being made, not the way it was
demonstrated.

## References

- `references/where-verification-runs.md` — live probe versus CI regression test, and
  why CI must never send attack traffic
- `references/test-by-class.md` — attack input, secure outcome, the effect to assert
  and the paired control case, per finding class
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/).
