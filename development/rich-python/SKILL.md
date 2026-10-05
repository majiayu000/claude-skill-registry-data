---
name: rich-python
description: Use for writing, reviewing, debugging, or testing Python terminal presentation built with Rich, including Console streams, Text and markup safety, tables, trees, panels, progress, status, Live displays, render protocols, and deterministic output capture. Do not use for CLI argument parsing, structured logging design, browser UI, or machine-readable protocol output that must remain plain.
argument-hint: "[Rich terminal output task, code, rendering defect, or test]"
---

# Rich Python

Design terminal output around a render target and data contract. Rich objects
describe presentation; a `Console` decides capabilities, dimensions, stream,
and rendering.

## Boundary

Use this skill when a Python project already uses Rich or the user requests
Rich terminal output. Do not introduce styling into stdout promised as JSON,
CSV, a pipe protocol, or another machine-readable format. Do not use Rich to
define command arguments (use the CLI framework), to replace structured logs,
or to build a web interface.

## Know the objects

| Object | Meaning | Use |
|---|---|---|
| `Console` | Rendering environment plus output stream | Own terminal detection, width, color, capture, and printing. |
| `Text` | Styled text with explicit spans | Dynamic/untrusted text or programmatic styling. |
| Renderable | Object implementing Rich's console protocol | `Table`, `Tree`, `Panel`, `Syntax`, user-defined views. |
| `Progress` / `Status` | Managed transient display | Bounded work with a lifecycle. |
| `Live` | Refresh controller for a changing renderable | Multi-field dashboards or custom updating layouts. |
| `Group` / layout container | Composition of renderables | One coherent frame rather than interleaved prints. |

Read [the rendering model](references/rendering-model.md) when output breaks
under redirection, width changes, markup-like data, or tests.

## Ordered workflow

1. Classify the channel: human stdout, diagnostics stderr, machine stdout,
   captured test output, file export, or interactive TTY.
2. Identify the semantic structure: prose, records, hierarchy, source, progress,
   or a changing dashboard. Choose one matching renderable.
3. Create or reuse a `Console` at the application boundary. Inject it into code
   that must be testable; do not scatter independently configured consoles.
4. Convert untrusted/dynamic strings to literal `Text` or escape markup. Never
   interpolate user text inside markup tags.
5. Define width, overflow, wrapping, and empty-state behavior. Tables need
   stable column meaning, not one visual column per arbitrary key.
6. Put transient output in a context manager so teardown occurs on errors.
7. Test at a fixed width with color disabled unless ANSI output itself is the
   contract. Test non-TTY behavior for progress/live code.

## Intent to renderable

| Intent | Use | Avoid |
|---|---|---|
| One styled message | `Console.print` with `Text` or trusted markup | Building a one-cell table |
| Aligned records with headers | `Table` | Manual spaces/tabs |
| Nested ownership or paths | `Tree` | Flattened repeated prefixes |
| Framed summary | `Panel` around a composed renderable | ANSI box-drawing strings |
| Source/config excerpt | `Syntax` | Hand-injected color codes |
| Known iterable progress | `track` or `Progress.track` | Printing every iteration |
| Multiple tasks/columns | Explicit `Progress` and task IDs | Nested independent progress bars |
| Arbitrary changing view | `Live` | Clear-screen loops |
| Machine-readable data | Plain serialization on stdout | Rich markup or tables |

## Canonical static output

```python
from rich.console import Console
from rich.table import Table
from rich.text import Text


def render_jobs(console: Console, jobs: list[dict[str, object]]) -> None:
    table = Table("ID", "State", "Owner", show_header=True)
    for job in jobs:
        state = str(job["state"])
        state_text = Text(state, style="green" if state == "ready" else "yellow")
        table.add_row(str(job["id"]), state_text, Text(str(job["owner"])))
    console.print(table if jobs else Text("No jobs.", style="dim"))
```

`Text(str(value))` keeps brackets and markup-like input literal. `repr`-style
highlighting is not a stable serialization format.

## Streams and terminal capability

- Reserve stdout for the documented primary result. Send diagnostics to a
  console configured with `stderr=True`.
- Let Rich auto-detect terminal capability for ordinary execution. Do not force
  color or interactive mode to make redirected output look like a TTY.
- Respect `NO_COLOR`, dumb terminals, narrow width, and noninteractive CI.
- Use `force_terminal`, `force_interactive`, or a fixed width only when the
  caller/test explicitly owns that rendering environment.
- If the command supports `--json`, bypass Rich on stdout entirely; Rich may
  still render errors to stderr.

## Progress and live lifecycle

Choose `Progress` when task completion is the primary state. Choose `Live` when
the whole view changes. Keep one active live display per console; print through
its console so messages do not corrupt the frame. Update at meaningful work
boundaries, not every byte or tight-loop iteration. Always use `with` so final
refresh and cursor restoration occur after success or failure.

Read [progress and live rules](references/progress-live.md) before combining
tasks, nesting displays, redirecting output, or running in CI.

## Deterministic verification

Inject `Console(file=StringIO(), width=<fixed>, color_system=None,
force_terminal=False)` for semantic text tests. Use `console.capture()` for a
small local capture. Assert content, row order, empty state, and absence of ANSI
codes; avoid full snapshots unless exact layout is contractual. Read [testing
terminal output](references/testing-output.md).

Inspect the installed version of Rich and its signatures when a constructor keyword,
environment override, or live behavior may drift. The authoring anchors were
executed on Rich 15.0.0; official rendered docs may show an earlier stable
version. Completion requires correct stream separation, safe dynamic text,
readable narrow/non-TTY output, managed live teardown, deterministic tests, and
no Rich formatting in machine-readable output.

## References

- [Rendering model and markup safety](references/rendering-model.md)
- [Progress and Live lifecycle](references/progress-live.md)
- [Testing terminal output](references/testing-output.md)
