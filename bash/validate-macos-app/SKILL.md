---
name: validate-macos-app
description: Validate requested or discovered states in a native macOS app while preserving prior app state
argument-hint: "<bundle-id> [comma-separated view names]"
allowed-tools:
  - Bash
  - Task
  - Read
user-invocable: true
---

# Validate macOS App

Invoke `peekaboo` and validate `$ARGUMENTS`.

Parse the first argument as the required bundle ID. Treat the remaining text as
optional comma-separated view labels so labels may contain spaces. Parse this in
the agent; do not execute `$1`/`shift` in a fresh shell.

## Preflight and ownership

Check `peekaboo`, `jq`, selected-runtime permissions, and live help. Use
the primary `peekaboo` skill's setup diagnosis for missing prerequisites.

Before launch, query `peekaboo list apps --json` for the bundle ID and record
whether it is already running. Launch only when absent. Cleanup may quit the app
only when this command launched it; preserve a pre-existing process and report
that choice.

Use an artifact directory outside version control. Add the directory to
`.gitignore` when it lives under the repository. Track every task-created path
for cleanup.

## Observe and choose states

Predict JSON response size before each command. Persist every `see`,
`inspect-ui`, browser snapshot, capture result, or other likely-large response
to a named file and query only the fields needed for targeting and assertions.

If view labels were supplied, validate those. Otherwise discover likely
top-level navigation controls from roles and hierarchy. Do not include
destructive or irreversible controls such as delete, send, publish, purchase,
sign-out, or account mutation unless the user named them.

Before each action, define the expected product state: selected tab, heading,
visible control, value, window, persisted output, or another specific
postcondition. A changed tree or screenshot hash is supporting evidence, not
the postcondition.

Resolve exactly one actionable target from the latest snapshot. On zero or
multiple matches, refine from hierarchy/identifier or stop rather than clicking
an arbitrary result. Treat IDs as opaque and capture fresh state after every
mutation.

## Visual evidence

Treat every screenshot as large. Capture raw and annotated images only when
each answers a distinct question. Give a visual reader the minimum related
paths and request a compact report. As soon as it returns, terminate it with
the host's kill/stop/remove control and verify through worker listing that it is
gone. A blocking or synchronous result does not prove teardown.

Do not invoke `Task` for screenshot reading unless the runtime exposes both
termination and worker-listing controls. If it does not, continue with
structured evidence or report that isolated visual inspection is unavailable.

Use evidence-backed `PASS`, `WARN`, or `FAIL` plus an intent verdict; numeric
scores are optional and require an anchored rubric.

## Report and cleanup

Report each requested state, its exact behavioral postcondition, visual verdict
when applicable, and artifact path for failures. In guaranteed cleanup, quit
only an app started by this command and report whether restoration succeeded.
Delete every temporary screenshot, JSON file, trace, video, contact sheet, and
empty artifact directory by exact path before returning. Retain only requested
artifacts or necessary failure evidence.
