---
name: peekaboo
description: >-
  Provides runtime observation and interaction for native macOS interfaces
  through accessibility state and screenshots. Use when the task depends on
  visible or interactive state in a running SwiftUI/AppKit app: what is
  rendered, focused, selected, enabled, reachable through menus/windows/dialogs,
  or experienced across a UI workflow. Tasks about source, configuration, data,
  logs, processes, or app APIs do not need this skill unless their result must
  be verified in the interface. Not for Electron/web apps or iOS simulators.
homepage: https://peekaboo.sh
metadata:
  os: ["darwin"]
  requires:
    bins: ["peekaboo", "jq"]
    permissions: ["Screen Recording", "Accessibility"]
  install:
    - kind: brew
      formula: steipete/tap/peekaboo
---

# Peekaboo

Use Peekaboo when the unresolved evidence or action lives in the running native
interface: whether a workflow works, what state it reached, and whether that
state looks intentional.

## Protect context and resources

Apply these rules throughout every workflow:

- Rule out files, source, CLI commands, app APIs, logs, and processes before
  using the live UI.
- Predict JSON size before running a command. Persist accessibility trees,
  browser snapshots, capture results, and other likely-large JSON, then query
  only the fields needed for the next decision.
- Treat every screenshot as large, including crops. Keep pixels on disk and
  return only compact text findings to the driving conversation.
- When a screenshot reader is needed, let it read the minimum related captures,
  then immediately terminate it with the host's kill/stop/remove control and
  verify through worker listing that it is gone. A blocking or synchronous
  result does not prove teardown. Do not create the reader if termination and
  verification are unavailable.
- Track every task-created artifact. Delete screenshots, JSON, traces, videos,
  contact sheets, and empty temporary directories by exact path as soon as they
  are no longer needed and again before the final response. Retain only
  requested artifacts or necessary failure evidence.

Prefer structured inspection until pixels are necessary. A visual task may
compare a small related set such as before/after states, but it must follow the
same read-then-terminate and artifact-cleanup lifecycle.

Read `references/agent-runtime.md` for host-specific options and
`references/visual-verification.md` for the visual-reader contract.

## Start from live capabilities

Check the installed CLI and selected runtime before guessing flags:

```bash
peekaboo --version
peekaboo permissions status --all-sources --json
peekaboo <command> --help
```

Screen Recording belongs to the process performing capture; Accessibility
belongs to the process inspecting or acting on UI. Event Synthesizing is needed
for background keyboard input and coordinate/synthetic fallback. In agent,
SSH, or launchd sessions the selected process may be the daemon or Peekaboo.app
Bridge rather than the terminal.

When diagnosing setup, also inspect Bridge and daemon health and run one
non-secure capture/AX self-test. Report which runtime needs a missing grant;
do not change permissions or delete existing artifacts as part of diagnosis.

## Observe, act, verify

1. Identify the app by bundle ID when possible.
2. Observe with the cheapest source that answers the question.
3. Resolve the target from fresh structured state.
4. Perform one meaningful action.
5. Observe again and assert a product postcondition.
6. Inspect pixels only when layout, rendering, or visual quality matters.
7. Fix and repeat until both behavior and appearance satisfy the request.

Use `inspect-ui --json` for accessibility state without pixels. Use
`see --json --path ...` when a screenshot or auditable snapshot is required.
Use a raw window image only for custom rendering that accessibility cannot
represent.

Treat snapshot and element IDs as opaque. Copy them from the latest result and
do not infer or generate them. Any state-changing action can invalidate the
previous snapshot, so observe again before another ID-based action.

## Choose semantic actions

Prefer direct accessibility behavior over synthesized input:

1. `set-value` for a settable non-secure field.
2. ID-based click for normal activation.
3. `perform-action` for a supported accessibility action.
4. A label or query when no stable identifier exists.
5. Coordinates only for custom-drawn or accessibility-invisible content.

Use native commands for app lifecycle, menus, file dialogs, windows, clipboard,
and deep links rather than rebuilding those flows with coordinate clicks.
Preserve background delivery unless the app explicitly requires focus or real
pointer input.

## Recover from evidence

- On a stale snapshot or missing element, observe again and resolve the target.
- On a truncated accessibility tree, increase bounds only enough to reach the
  needed surface.
- On blank, wallpaper-only, or redacted capture, inspect the selected runtime,
  daemon, Bridge, and permission state before changing capture engines.
- When accessibility cannot expose custom rendering, normalize the target
  window and make one verified coordinate fallback.
- Treat a successful command with an unchanged postcondition as failure, not as
  proof the feature worked.

## Validate the product, not the command

A click succeeding does not prove the resulting state is correct. Check the
fresh accessibility tree or application output for the expected behavior, then
use visual evidence for hierarchy, alignment, spacing, contrast, copy,
overflow, focus, empty/loading/error states, and consistency with the product.

Use `capture action` for transitions or intermittent failures so action result
and visual evidence share one bounded capture. Keep artifact names tied to the
state under test and record paths for failures.

Instrument repeated targets with stable accessibility identifiers. Prefer a
small documented namespace and tag the precise actionable child rather than a
composite parent.

## Safety

Keep credentials and private content out of shell arguments, logs,
screenshots, and recordings. Let the user mediate secure fields. Require
confirmation before payments, deletion, publishing, sending, account changes,
or other irreversible actions.

Use Peekaboo for interactive product validation and XCUITest for durable
regression gates. Do not replace deterministic tests with an agent-only flow.
