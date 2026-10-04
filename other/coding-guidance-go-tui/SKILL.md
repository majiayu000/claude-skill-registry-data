---
name: coding-guidance-go-tui
description: Go terminal UI implementation and review guidance for interactive Bubble Tea state machines. Includes Huh only when embedded in Bubble Tea; use `coding-guidance-go` for standalone or one-shot Huh prompts and other non-TUI Go work. Covers Bubbles, Lip Gloss, key bindings, focus, and supported Charmbracelet major versions.
---

# Go TUI Coding Guidance

Portable implementation, refactoring, testing, and review guidance for
interactive Go terminal user interfaces built with Charmbracelet Bubble Tea,
Bubbles, Lip Gloss, Huh forms embedded in Bubble Tea, and related Charm
libraries.

## Adjacent Skills

Use this as the default principle skill for Charmbracelet Go TUI work. Compose
with:

- **Workflow:** `thinking` for ambiguous decision framing,
  `recursive-thinking` for
  stress-testing, `tester-mindset` for validation strategy, and `security` for
  sensitive input, shell execution, token display, or filesystem access
- **Project overlays:** `project-core-dev` for repo-specific completion
  discovery and reporting when needed,
  `project-config-and-tests` for config and deterministic tests at config or
  path seams, and
  `project-platform-diagnose` for terminal capability, piped stdio, SSH,
  alt-screen, shell, platform, install, or runtime smoke issues
- **Go depth:** `coding-guidance-go` only when the non-TUI Go package design,
  concurrency, service boundary, profiling, or module behavior is the main
  risk

Use `coding-guidance-go` instead when the task is a non-interactive Go CLI,
standalone or one-shot Huh prompt, library, worker, service, or test change with
no terminal UI state machine.

## Reference Map

Load references only when the task needs that depth:

- [references/charmbracelet-patterns.md](references/charmbracelet-patterns.md)
  for version-specific Bubble Tea APIs, Bubbles component integration, Huh
  forms embedded in Bubble Tea, Lip Gloss APIs, key binding patterns, and
  upstream example routing
- [references/tui-layout-and-production.md](references/tui-layout-and-production.md)
  for layout arithmetic, responsive panels, mouse hit testing, screen/focus
  state machines, production polish, performance, noninteractive fallbacks, and
  Bubble Tea code-review false positives

## When Not to Lean on This Skill

- non-Go terminal UI frameworks such as ncurses, Textual, blessed, termbox, or
  curses-style wrappers unless only the generic TUI UX ideas apply
- simple command-line flag parsing, one-shot command output, standalone Huh
  forms, or other prompt-only flows that do not maintain an interactive screen
- shell-only prompt polish with Gum, VHS, Mods, or plain shell unless the user
  is explicitly converting the flow into a Go Bubble Tea TUI
- web, mobile, or graphical desktop UI work; use the appropriate UI or platform
  guidance instead
- broad Go backend, package architecture, or performance work where Bubble Tea,
  Bubbles, and Lip Gloss are incidental

## Implementation Workflow

1. Inspect `go.mod`, imports, nearby models, Bubbles and Huh components, Lip
   Gloss styles, examples, tests, and docs before editing. Preserve the repo's
   current Charmbracelet major version and import path unless the task is
   explicitly an upgrade. Check upstream Charm examples when the component
   pattern is unfamiliar.
2. Identify the app mode: inline or full-screen, alternate screen or normal
   output, keyboard and mouse expectations, input/output streams, width and
   height constraints, external commands, background work, noninteractive or
   `--no-tui` fallback, and error states.
3. Model the TUI as an explicit state machine: screen or mode, focus target,
   previous screen or return path, dimensions, data loading state, request or
   stale-result marker, domain state, selected item, cursor or scroll position,
   pending command, error/status message, and child component state.
4. Keep `Update` deterministic and fast. Represent side effects as `tea.Cmd`
   values that return typed `tea.Msg` values; do not block on filesystem,
   network, subprocess, timers, or heavy rendering work inside `Update` or
   `View`. Use `tea.Batch` for independent commands and `tea.Sequence` only
   when ordering is observable behavior.
5. Compose Bubbles and Huh components deliberately. Store component models in
   the parent model, route key and resize messages by focus or mode, assign
   updated component values back to the parent, collect returned commands, and
   keep child widths, heights, styles, and focus state synchronized.
6. Render from state only. `View` should not mutate state, start work, read
   files, call services, log, or depend on wall-clock time. Build terminal
   layouts with Lip Gloss styles and cell-aware helpers instead of ad hoc ANSI
   string arithmetic; add builders or caches only when construction clarity or
   measured rendering cost justifies them.
7. Design terminal UX as product behavior: clear focus, visible help, safe quit
   and cancel paths, loading and empty states, recoverable errors, accessible
   keyboard shortcuts, resize behavior, narrow-terminal fallbacks, plain-output
   escape hatches, and no mouse-only interactions.
8. Add or update focused tests close to the changed behavior. Prefer model
   transition tests with synthetic messages, command tests around command
   constructors, and stable render assertions for important layout or text
   contracts.
9. Run the narrowest relevant formatter, import formatter, tests, and manual
   smoke command the repo supports. A visible TUI behavior change usually needs
   at least one interactive smoke run or recorded terminal-output check.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current states, messages, commands, key bindings, component
   ownership, render paths, dimensions, and external side effects.
2. Add characterization tests first when state transitions or command behavior
   are unclear.
3. Split tangled root models into screen, component, command, and style helpers
   only when the split makes state ownership and message flow easier to follow.
4. Preserve user-visible key bindings, output text, persisted formats, command
   side effects, and terminal mode choices unless the task explicitly changes
   them.
5. Keep the app runnable after each slice; terminal apps are easy to break with
   a compile-passing render or focus regression.

## Review Workflow

When reviewing, skip implementation steps and use this checklist:

1. Read the full state/message/render loop before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Rank correctness, data-loss, terminal-state, and event-loop defects above
   polish. Layout, color, and help-text issues become higher severity only when
   they block navigation, hide required information, or break supported terminal
   contexts.
4. Prioritize blocking `Update` or `View` work, lost or unordered commands,
   unhandled errors, command goroutine leaks, state mutation during rendering,
   stale window dimensions, unassigned Bubbles component updates, key binding
   conflicts, focus traps, missing quit/cancel behavior, alt-screen cleanup
   hazards, and fragile string-width math.
5. Avoid false positives: helper functions returning `tea.Cmd`, value receivers
   on `Update`, nested child `Update` calls, and `tea.Batch` are normal Bubble
   Tea patterns when no side effect runs before the command is returned.
6. Check whether rendering handles narrow terminals, Unicode width, color
   profiles, no-color environments, redirected input/output, and noninteractive
   CI execution where the repo claims support.
7. State findings with the triggering message or interaction path, the expected
   state transition, and the likely user-visible consequence.

Do not edit code or require findings to be fixed unless the user also asks for
remediation.

## Core TUI Rules

- Keep the Bubble Tea model as the source of truth for UI state. Use typed
  messages and explicit commands; do not hide UI state or active work in
  globals or unowned goroutines.
- Keep `Update` and `View` deterministic and non-blocking. Commands capture
  immutable inputs, perform side effects, and return typed success or failure
  messages.
- Store every child component model returned from `Update`, route messages by
  focus or mode, and propagate computed dimensions from the top level.
- Use Huh here only when the form is embedded in Bubble Tea through its
  `Init`, `Update`, and `View` lifecycle. A standalone or one-shot Huh form
  belongs to `coding-guidance-go`.
- Preserve the repository's Charmbracelet major version and its v1 or v2
  terminal-mode conventions unless the task is an upgrade.
- Measure terminal layout with ANSI-aware, cell-aware helpers rather than
  `len`; account for borders, padding, margins, Unicode width, and narrow
  terminals.
- Keep focus, help, quit, cancel, resize, loading, empty, error, and screen
  transition behavior explicit. Do not make required interactions mouse-only
  or encode state only through color.
- Keep logs and diagnostics out of rendered output, and provide plain-output or
  no-TUI behavior for supported pipes, CI, and noninteractive environments.
- Optimize rendering only from profiles, benchmarks, or realistic data
  pressure; reject stale asynchronous results when requests can complete out of
  order.

Load the two references above for component APIs, layout arithmetic, mouse hit
testing, multi-screen behavior, runtime fallbacks, or performance patterns.

## Validation

A Charmbracelet TUI change is done when:

- Go files are formatted with the repo's formatter and import tool
- touched packages compile and affected tests pass
- model transitions are tested with representative key, resize, success, error,
  quit, and cancel messages
- Bubbles component updates are covered where focus, validation, cursor,
  viewport, pagination, or timers changed
- important render output is checked at narrow and normal widths, with stable
  snapshots or focused string assertions when practical
- interactive behavior has been smoke-tested when terminal modes, keyboard
  input, alt screen, subprocess execution, mouse handling, clipboard, or cursor
  behavior changed
- noninteractive fallback is checked when the command can run in pipes, CI, or
  scripts, and narrow-terminal behavior is checked at representative supported
  dimensions
- color behavior is checked for both light/dark assumptions and `NO_COLOR` or
  limited-color terminals when the repo supports them
- `go test -race` or equivalent concurrency validation runs when commands,
  goroutines, timers, subprocesses, or shared state changed

For review, completion means `Critical` and `Important` findings identify the
triggering message or interaction, expected state transition, concrete
evidence, and likely user-visible consequence. Unfixed findings do not make the
review incomplete.
