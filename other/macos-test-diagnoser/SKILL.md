---
name: macos-test-diagnoser
description: "macOS Xcode and SwiftPM tests: run focused scopes and diagnose build, assertion, crash, async-flake, fixture, entitlement, and host-app failures; separate regressions from setup issues."
---

# macOS Test Diagnoser

Before invoking Apple-only binaries, confirm the execution context is macOS. From Windows or Linux, run those steps in a Mac SSH project or through an already configured remote transport; do not retry missing Apple binaries locally.

## Quick Start

Use this skill to run the smallest meaningful test scope first, classify
failures precisely, and avoid treating every test failure like a product bug.

## Workflow

1. Detect the test harness.
   - Use `xcodebuild test` for Xcode-based projects.
   - Use `swift test` for SwiftPM packages.

2. Narrow the scope.
   - If the user gave a target, product, or test filter, use it.
   - If not, prefer the smallest likely failing target before a full suite.

3. Classify the result.
   - Build failure
   - Assertion failure
   - Crash or signal
   - Async timing or flake
   - Environment or fixture setup issue
   - Missing entitlement or host app issue

4. Rerun intelligently.
   - Use focused reruns when a specific case fails.
   - Avoid burning time on full-suite reruns without new information.

5. Summarize clearly.
   - What command ran
   - Which tests failed
   - What kind of failure it was
   - The best next proof step or fix path

## Result Bundle Inspection

When console output alone is not enough, read the `.xcresult` bundle instead
of rerunning:

- Pass `-resultBundlePath ./Tests.xcresult` to `xcodebuild test` so evidence lands at a known path.
- Run summary: `xcrun xcresulttool get test-results summary --path Tests.xcresult`
- Per-test outcomes: `xcrun xcresulttool get test-results tests --path Tests.xcresult`
- One failure in depth: `xcrun xcresulttool get test-results test-details --test-id <id> --path Tests.xcresult`
- Attachments such as screenshots and logs: `xcrun xcresulttool export attachments --path Tests.xcresult --output-path ./attachments`
- Older bundles or full object graph: `xcrun xcresulttool get --legacy --format json --path Tests.xcresult` (drop `--legacy` on pre-Xcode 16 toolchains).

`swift test` produces no `.xcresult`; use console output, `--filter` reruns,
and `--xunit-output` when a machine-readable report is needed.

## Guardrails

- Distinguish compilation failures from test execution failures.
- Call out when a test appears to assume iOS-only or simulator-only behavior.
- Mark likely flakes as such instead of overstating confidence.

## Output Expectations

Provide:
- the command used
- the smallest failing scope
- the `.xcresult` path when one was produced
- the top failure category
- a concise explanation of the likely cause
- the next rerun or fix step
