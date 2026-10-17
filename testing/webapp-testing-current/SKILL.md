---
name: webapp-testing-current
description: Verify local web application behavior with Playwright, observable readiness, controlled test targets, meaningful assertions, and accurate failure reporting. Use for browser regressions, UI workflows, screenshots, or console diagnosis; use the project's existing test runner when it already provides these contracts.
license: Apache-2.0
compatibility: Requires a qualified Playwright installation and matching browser; use the repository's declared Python or JavaScript runtime. Linux server-helper findings do not establish Windows process lifecycle behavior.
metadata:
  source: anthropics/skills
  revision-status: experimental-unbenchmarked
---

# Verify observable browser outcomes

Resolve the requested workflow, intended local target and relevant application
tests before choosing a script. Reuse the existing runner, fixtures and package
graph. An open port or one detected service does not establish the application's
identity or authorize its mutations. Use disposable test data and a known test
account for state-changing flows.

## Establish runtime and server readiness

Check installed package and browser versions against their current stable
release metadata. Provision dependencies explicitly in an isolated workspace
from a complete lockfile. Keep the original skill package unchanged. Avoid
implicit installation during test execution.

Prefer the project's server lifecycle integration. If starting a server, retain
its process identity, drain or redirect both output streams, bound startup, and
check that the launched process remains alive. Verify an application-specific
HTTP or UI condition before testing; a successful TCP connection alone is
insufficient. Record ownership before stopping processes and clean up the whole
owned process tree with a mechanism qualified for the operating system.

Read a helper's interface before invocation and inspect its implementation when
assessing its fitness or diagnosing failure. The original bundled server helper
has reproduced readiness, log-draining and child-cleanup defects; it is not a
qualified general server supervisor.

## Act and assert

Navigate to the explicit target and wait for the relevant rendered condition.
Prefer accessible roles, labels and stable test IDs. Use retrying assertions for
dynamic state. Network idle and fixed sleeps do not prove UI readiness.

Arm response, download or popup waits before the triggering action. Match the
request identity and expected status, then assert the user-visible outcome.
Treat navigation or authentication failures as failures. Do not blindly retry
an action whose effect may already have occurred; first inspect the resulting
state or use a controlled idempotent fixture.

Use isolated contexts and the project's viewport/device matrix. A screenshot
is evidence to inspect, not a correctness verdict. Distinguish functional,
accessibility and visual coverage. Control clocks, animations and data for
image comparisons and review baseline changes independently.

## Preserve evidence and cleanup

Use portable output paths and unique run directories. Register console and
page-error capture before navigation; keep diagnostics within the task's data
boundaries. Traces and authentication state can contain sensitive information.
Close contexts and browsers in finally blocks so artifacts finish even when
assertions fail. Preserve the command's actual status and failed attempts.

Report tested outcomes, failed/skipped/not-run checks, exact versions and
artifact paths. Do not count swallowed errors, retries or screenshot creation
as passing behavior. See [qualified controls and limits](references/controls.md).
