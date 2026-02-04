---
name: artisanal-helper
description: Guidance for building polished CLIs and TUIs with the Artisanal Dart package. Use when users ask for terminal UIs, live dashboards, log viewers, interactive input, or CLI tools with subcommands using Artisanal.
---

# Artisanal Helper

Artisanal is a Dart terminal toolkit. Use `package:artisanal/...` imports.

## Quick triage

- CLI with subcommands or rich console output: use `package:artisanal/args.dart` and `package:artisanal/artisanal.dart`.
- Interactive TUI (Elm-style Model/Update/View): use `package:artisanal/tui.dart` and bubbles widgets.
- High-performance rendering or custom terminal behaviors: use `package:artisanal/uv.dart` and UV primitives.

See `references/exports.md` for entrypoints, `references/examples.md` for example map, and `references/api_reference.md` for API notes.

## Workflow

1. Pick the closest example and adapt it; start from TUI examples for dashboards/input.
2. Keep the Model immutable and small; put derived view data in helpers.
3. Use `Cmd.tick` or `every(...)` for live dashboards and periodic refresh.
4. Prefer bubbles widgets for input, lists, tables, and viewports before custom drawing.
5. For CLI tools, wire `CommandRunner` with subcommands and use `Console` for styled output.

## Task playbooks

### Create a nice log dashboard

- Start from `packages/artisanal/example/log_viewer_demo.dart`.
- Reuse viewport + list or table components; keep log lines as model data.
- Use `every(...)` to append new entries; gate auto-scroll with a "live" flag.

### Create a live dashboard

- Start from `packages/artisanal/example/tui/examples/realtime/main.dart`.
- Track data in model, render with tables or gauges; use `every(...)` for refresh.
- Optionally add `DebugOverlayModel` to show render metrics.

### Create a TUI to handle user input

- Start from `packages/artisanal/example/tui/examples/textinput/main.dart` or `textarea/`.
- Use bubbles widgets (`TextInputModel`, `TextareaModel`, `SelectModel`, `ListModel`).
- Forward input `Msg` to the active widget, then compose view strings.

### TUI patterns to follow

- Compose multiple widgets with layout helpers; see `packages/artisanal/example/tui/examples/composable-views/main.dart`.
- Use `ViewportModel` for log panes or long text; see `packages/artisanal/example/tui/examples/pipe/main.dart`.
- Add help overlays with `HelpModel`; see `packages/artisanal/example/tui/examples/help/main.dart`.
- Prefer `ProgramOptions` for renderer/input toggles over manual terminal calls.

### UV (low-level) patterns to follow

- Start from `packages/artisanal/example/uv/helloworld.dart` or `packages/artisanal/example/uv_demo.dart`.
- Use `Terminal` + `Screen` + `Buffer` for drawing; call `draw()` to flush.
- Use `Canvas` for immediate-mode shapes; see `packages/artisanal/example/uv/draw.dart`.
- Use layout helpers (`splitHorizontal`, `splitVertical`) in `packages/artisanal/example/uv/layout.dart`.

### Create a CLI with subcommands

- Use `package:artisanal/args.dart` and `CommandRunner`.
- Keep each subcommand in its own class; return non-zero exit codes on failure.

```dart
import 'package:artisanal/args.dart';

class HelloCommand extends Command {
  @override
  String get name => 'hello';

  @override
  String get description => 'Print a greeting.';

  @override
  void run() {
    print('Hello, world!');
  }
}

void main(List<String> args) {
  final runner = CommandRunner('my-cli', 'A great CLI');
  runner.addCommand(HelloCommand());
  runner.run(args);
}
```

## Resources

- `scripts/example.py`: list or search Artisanal examples by keyword.
- `assets/example_asset.txt`: TUI skeleton template (copy into a new Dart file).
