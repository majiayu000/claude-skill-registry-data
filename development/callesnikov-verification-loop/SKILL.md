---
name: callesnikov-verification-loop
description: Verify Codex implementation work with repository-derived quality gates and an evidence-backed readiness report. Use after a feature, bug fix, refactor, dependency change, generated artifact, or substantial edit; before a commit or PR; or whenever the user asks to build, test, lint, review, validate, smoke-test, or prove that a change works.
---

# Callesnikov Verification Loop

Prove the requested behavior with the strongest checks the repository and environment support. Do not substitute a generic command list for project evidence.

## 1. Establish the baseline

Inspect the repository before running checks:

- read the nearest `AGENTS.md` and project instructions;
- inspect manifests, build files, CI workflows, task runners, and existing tests;
- inspect `git status` or the equivalent without reverting unrelated work;
- identify the changed behavior, affected modules, and required verification boundary.

Derive commands from the project. Never assume `npm`, TypeScript, an 80% coverage threshold, or a particular branch layout unless the repository establishes them.

## 2. Choose gates by risk

Run the smallest relevant checks first, then broaden when the change touches shared contracts or user-facing workflows.

Typical gates:

1. **Static integrity**: formatting, syntax, generated-file consistency, schema validation.
2. **Compile or type check**: affected module first, full build when justified.
3. **Focused tests**: tests that directly exercise the change.
4. **Broader tests**: shared or integration suites when the blast radius requires them.
5. **Lint and policy checks**: repository-configured lint, license, API, or architecture gates.
6. **Security review**: secrets, unsafe input handling, dependency or permission risk when relevant.
7. **Runtime verification**: smoke test, screenshot, device, browser, CLI output, or generated artifact inspection.
8. **Diff review**: unintended changes, missing error paths, stale names, and unverified assumptions.

Do not run expensive unrelated suites merely to make the report look complete.

## 3. Execute and repair

- Record the exact command and exit result.
- Read the failure, identify whether it comes from source, environment, permissions, missing dependencies, or flaky infrastructure.
- Fix source failures when implementation is in scope, then rerun the failing gate.
- Do not edit or delete user work to manufacture a clean result.
- Do not weaken tests, lint rules, or thresholds unless the user explicitly requests that policy change.
- Use timeouts appropriate to the project and wait for required sessions to finish.

## 4. Review the final diff

Check every touched file for:

- behavior outside the request;
- unresolved placeholders or debug output;
- missing loading, empty, error, cancellation, and recovery paths where relevant;
- contract or migration mismatches;
- accidental generated or binary artifacts;
- stale documentation, names, or invocation examples;
- tests that assert implementation details without proving behavior.

## 5. Report exact evidence

Use these statuses:

- `PASS`: command completed successfully and supports the claim.
- `FAIL`: command completed and found a source or behavior defect.
- `BLOCKED`: the check could not run because of an external or environment boundary.
- `NOT RUN`: consciously skipped; state why.
- `NOT APPLICABLE`: the gate does not exist or is irrelevant to this project.

```text
VERIFICATION REPORT

Behavior: <what was proved>
Build/type: <status, command, key result>
Focused tests: <status, command, counts>
Broader tests: <status or reason not run>
Lint/policy: <status>
Runtime/artifact: <status and evidence>
Diff review: <files and findings>

Overall: READY | NOT READY | PARTIALLY VERIFIED
Residual risk: <device, service, data, or scenario not verified>
```

Never report `READY` when a required gate failed or remained blocked. Distinguish compile, unit tests, lint, integration tests, and device/E2E evidence instead of collapsing them into “tests passed.”

## GPT-5.6 Sol discipline

Use the model's reasoning capacity to select high-signal gates and trace failures across modules. Keep the report grounded in command output and observable behavior. Do not infer success from code appearance, agent confidence, or a passing unrelated suite.
