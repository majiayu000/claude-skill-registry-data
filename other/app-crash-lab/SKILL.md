---
name: app-crash-lab
description: Test a local web app's saved state and save feedback using its existing Playwright suite or App Crash Lab contracts. Inspect the app and prepare a focused regression for the requested boundary; not a general UI audit.
---

# App Crash Lab

Turn the user's save workflow into a small, runnable test of **their app**.
Choose the test path that fits the requested behavior and existing project.
Do not implement another runner or silently substitute a bundled demo.

## Establish what the test means

Read the authorized app's README, startup scripts and relevant save/import
source. Use rendered DOM when needed for actual selectors. Obtain the local
origin and requested workflow from the user or project; ask only for missing
information that affects the test. Use a disposable local instance and synthetic
records. Do not read credentials, reuse a logged-in browser profile, deploy,
publish, or modify the app merely to manufacture a passing check. Test actions
can write data.

Before writing a test or JSON, show a short observation table:

| Requirement | How the app completes it | What will be compared |
| --- | --- | --- |
| The requested record was saved | Actual save-completion signal from source/UI | Complete selected persisted record(s), plus a meaningful visible result |
| Chosen follow-up has the expected outcome | Actual edit/delete, storage rejection, reload, or import completion | Complete retained values and the truthful visible result afterward |

Fill the table with this app's facts, not these descriptions. Input text, a toast,
record counts or a preference key alone may miss a lost record/field. Read the
actual canonical saved value where supported, keep full selected records and
IDs, and add UI observations when display behavior matters. Preservation does
not establish that the original calculation or content was correct.

For either test path, retain actual failure evidence. If fixes are already
part of the user's request and permission, continue within that scope after
establishing the failure. A test-only request does not authorize app changes;
do not invent an approval gate for an already requested fix.

## Choose native Playwright or a runner contract

First honor an explicit runner/JSON request or a real JSON backup roundtrip:
use the contract path below with the existing App Crash Lab **0.11.0** runner.
Do not replace a requested real-file restore with a native reload test.

Otherwise, if the app already has a working `@playwright/test` suite and the
requested boundary fits a measured native example, start with
[one native Playwright regression](references/native-playwright.md). Use the
app's existing configuration, dependencies and test naming. Adapt one example
to its actual UI, saved records and completion signals. This path requires
neither App Crash Lab JSON nor its runner; do not install them for it.

Without a verified existing suite, use the runner only if it covers the
requested workflow. If neither path establishes the requested boundary, report
the missing capability instead of substituting an easier passing check.
Native and contract checks prove their stated boundary, not every behavior
of the app.

For a runner contract, choose only the checks relevant to the request:

- `reload`: save through the normal flow, then compare after reload.
- `rejected-update`: separately establish that the invalid operation finished
  and was rejected, then compare the selected saved state. Do not treat the
  initial error-free state as a rejection signal.
- `backup-roundtrip`: use the app's real download, map complete selected records
  into its JSON, restore unchanged bytes into an empty browser context, and
  compare after import and reload. A malformed-file test is not this check.

For either path, if the app needs unsupported authentication, external services,
storage formats or confirmation steps, report the exact boundary. Do not replace
the real data with a simpler key, normalize away changed IDs, inject storage to prepare a
fresh restore, or add sleeps that conceal an incomplete save.

## Create and execute the contract

This section applies to the runner path, not the native path above.

Read [runner setup and contract sources](references/runner.md). Use the pinned
format and supported actions/observations; inspect the referenced contract and
one relevant example rather than guessing fields. Derive selectors, storage
keys, expected values and readiness from the app. `init` contains Notes demo
selectors and is not an automatic adapter.

Check input selectors again after editing their values. In a measured
Playwright 1.64.0 nested-label textarea, the exact `Notes` label stopped matching
after input while the exact `textbox` role and accessible name still matched.
If a selector changes this way, use a verified stable role/name or test ID for
both actions and observations. Preserve the first INCONCLUSIVE report and all
expected saved values; fix the selector without changing the app or adding waits.

Put the contract and evidence in a new local output folder, such as
`.crash-lab/my-flow/`, without overwriting earlier runs. Use a Node 22+
environment and the user's approved startup method; reuse a confirmed running
local app when possible. Keep app data and test output out of commits. Run the
contract against the unchanged app and read the **new** report.

Distinguish PASS, a reproducible FAIL, and INCONCLUSIVE. For a setup/selector
mistake, preserve the first report, make a focused correction and run to a new
output directory. Do not change expected values to observed values just to pass.
For an actual app failure, retain the failing contract and explain the mismatch.

Run the generated standalone Playwright test when dependencies and the requested
scope permit; otherwise state that it was generated but not rerun. Stop only
servers started for this task, leaving an existing user server running.

Return the app/workflow and runner version, observation table, exact commands
and exit codes, result and key differences, absolute report/contract/spec paths,
and the command to rerun after the next update. State untested behavior and
whether the standalone test actually ran. Do not call local testing an
independent user report or imply proof for all inputs and future failures.
