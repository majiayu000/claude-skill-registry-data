---
name: verify
description: "Verify code or product claims after changes using fresh, risk-matched evidence. Use before saying a bug is fixed, tests pass, requirements are met, or a branch is ready."
---

# Verify

Evidence must support the exact claim. Fresh verification is required after the final relevant change, but verification scope should match risk rather than defaulting blindly to the largest test suite.

## Define the claims

List the claims that matter, such as:

- The original bug no longer reproduces.
- A new behavior matches acceptance criteria.
- Targeted tests pass.
- The module builds or type-checks.
- No existing behavior in the affected area regressed.
- A migration is safe.
- The branch is ready to integrate.

For each claim, identify the command, inspection, or manual scenario that proves it. For decisive cross-boundary probes, name their entry point, relevant path, and material conditions. Freshness and a shared environment do not make a check that bypasses the failing boundary evidence of that boundary's health. A brief coverage note is enough; do not create a second ledger.

## Evidence budget

- Run a check only when its result supports a named claim or can change the next action.
- Do not calculate hashes without an identity or integrity decision that will use them.
- Do not rerun unchanged checks or add a second acceptance loop merely to restate existing proof.
- Stop when every material claim has proportionate fresh evidence; more commands do not automatically create more confidence.

## Evidence maturity without ceremony

Keep capability and effectiveness claims separate:

- A file, rule, tool, or configured capability proves that it exists, not that the task can reach it.
- A reachable route proves wiring, not successful use or delivery.
- A focused exercise or passing test proves current behavior under its observed conditions, not general runtime effectiveness. Keep mechanism repair and whole-user-experience recovery separate; residual symptoms do not automatically invalidate a verified contributing fix.
- A repair verified in the current task proves repair state. Only a later comparable outcome can support a claim that the workflow improved over time.
- Missing observation is `Not verified`, not automatically a defect.

These are claim boundaries, not a required scorecard, ledger, report, or extra review loop.

## Host-boundary evidence ladder

For a host-specific claim, keep these rungs distinct:

1. Source contract
2. Process-level behavior test
3. Built artifact or image identity
4. Activated runtime identity
5. Exact named-host surface
6. Owner-observed behavior

Each rung supports the next investigation step, not the claim above it. Local or dev-browser success is not named-host acceptance; a successful build is not proof that the intended runtime is active; deployment is not owner-observed behavior. After the final relevant change, verify the artifact and activated runtime identities, then obtain fresh acceptance on the exact named host when that is the contract. If the required deployment or owner observation is not authorized or available, mark the higher claim `Not verified`.

## Verification ladder

### Level 1: Focused

Use for local, low-risk changes:

- Regression test
- Affected test file
- Component or module check
- Targeted type-check or lint
- Focused manual interaction

### Level 2: Adjacent

Add when the change touches shared code or several consumers:

- Package or feature suite
- Integration tests around the boundary
- Build for the affected application
- Representative platform or browser check

### Level 3: Broad

Use for high-risk or integration-ready changes:

- Full relevant test suite
- Full build
- Migration dry run
- End-to-end path
- Security or compatibility checks
- Multiple environments when the risk requires it

Do not run Level 3 merely to make a small change look rigorous. Do not stop at Level 1 when shared state, data, security, or public contracts are involved.

## Run and read

For every command:

1. Run it after the final relevant change.
2. Read the complete result needed to assess success.
3. Check exit status, failure counts, warnings, skipped tests, and environment limitations.
4. Record what it actually proves.
5. Do not extrapolate beyond that scope.

A prior run before later edits is stale evidence for the affected behavior.

## Non-test checks

Inspect:

- Final diff and scope
- Untracked or generated files
- Debug output and temporary instrumentation
- Secrets or sensitive data
- Schema and fixture consistency
- Documentation when public behavior or setup changed

For UI work, include a real rendered or interaction check when practical. Unit tests alone may not prove layout or input behavior.

For optional host actions, verify the negative capability path before exposure as well as success. Preserve distinct absent, rejected, cancelled, and policy-denied results when the host distinguishes them; a generic error does not prove correct degradation.

## Regression evidence

For a bug fix, prefer a reproducer or test that would fail under the old behavior. Revert or mutation proof is useful when safe and efficient, but it is not mandatory when it would destabilize the workspace.

## Check the test criterion and close review findings

Before relying on a green result, consider a plausible incorrect implementation that this check would reject. This is a check on the existing evidence, not a mandatory mutation-testing stage or an extra reviewer loop. Schema presence, file signatures, compilation, a mocked success path, and expected-output updates can all miss the behavior being claimed. Use the nearest available behavioral check or full parser where that is the contract. Pair disappearing errors with the intended successful outcome so that suppressing work or bypassing the observed path cannot masquerade as repair. For state-preservation claims, prefer structured comparison or a demonstrably stable normalized before-image over scattered substring checks; retain semantic fields and ordering, and exclude only understood volatile fields. Keep static checks as static evidence.

For timing, ownership, recovery, or optional-host changes, inspect the relevant repeated, interrupted, stale, malformed, denied, or accessibility path. Select from these by the actual changed boundary; this is not an exhaustive test matrix for every task.

Resolve material review findings against the exact final revision. A finding may be fixed and checked, rejected with a concrete counterexample, or explicitly deferred under applicable authority. Record its disposition in the existing review or task surface. CI green or a merge does not itself resolve a reviewer-identified failure. Reproduce disputed findings instead of trusting either the reviewer or implementer by title.

For reusable instructions, distinguish discovery, context delivery, method use, and task outcome. Self-reported loading is supporting evidence only. A static assertion about prompt text cannot establish natural-language activation or improved model behavior.

## Blocked verification

When a check cannot run:

- State the exact reason.
- Separate environmental failure from code failure.
- Run the strongest available alternative.
- Narrow the completion claim.
- Give the command or condition needed to complete verification later.

## Output format

Use three categories:

- **Verified:** claim and evidence
- **Failed:** actual failure and impact
- **Not verified:** omitted or blocked checks and why

Do not say “all tests pass” when only targeted tests ran. Say exactly which tests passed.
