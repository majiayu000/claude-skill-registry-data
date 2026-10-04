---
name: cli-anything
description: Turns any GUI-only software into an agent-usable CLI/REPL harness backed by the software's real engine (Blender, GIMP, LibreOffice, etc.).
---

## Full Role Description

Transforms any GUI software into an agent-usable, stateful CLI harness using the software's
native CLI interface as the backend. Agents get structured commands, JSON output, undo/redo,
and a REPL — no GUI, no screenshots, no pixel-clicking. Trigger when: adding CLI capabilities
to Blender, GIMP, LibreOffice, Inkscape, Shotcut, Audacity, or similar; automating a
professional tool that has no API; building a CLI wrapper around a desktop application;
controlling a software tool that only has a GUI; or generating a CLI harness from source code
or documentation. Key capabilities: 7-phase pipeline (analysis → architecture → implementation
→ test planning → implementation → documentation → PyPI publish); direct invocation of the
real software backend (ffmpeg, melt, LibreOffice, Blender); stateful session management with
exclusive file locking and undo/redo; dual output modes (human-readable tables and machine-readable
JSON via --json flag). Ideal for agents that need programmatic, reproducible control of creative
and engineering tools. Also for: generating PyPI packages from CLI wrappers; building CLI tools
for open-source software that only ships a GUI.

# CLI-Anything

Transform any open-source GUI application into a command-line tool an AI agent can operate — no display, no mouse. The agent uses Click subcommands to manipulate native project files (XCF, SVG, ODF, MLT XML, .blend) and calls the real software's CLI as a subprocess for rendering and export.

---

## When Invoked

- User asks to make a GUI app agent-controllable
- User asks to add CLI capabilities to Blender, GIMP, LibreOffice, Inkscape, Shotcut, Audacity, OBS, or similar
- User asks how to control a software tool that only has a GUI
- User asks for a CLI wrapper around a desktop application
- User asks to automate a professional tool that has no API
- User asks to generate a CLI from source code or documentation

---

## The 7-Phase Pipeline

### Phase 1: Codebase Analysis

1. **Identify the backend engine** — Find the core library/framework the GUI wraps (MLT for Shotcut, ImageMagick for GIMP, Blender Python API for Blender)
2. **Map GUI actions to API calls** — Catalog every button, drag, and menu item as a function call
3. **Identify the data model** — What file formats? How is state represented? (XML, JSON, binary, database?)
4. **Find existing CLI tools** — Backends often ship their own CLI (`melt`, `ffmpeg`, `convert`, `libreoffice --headless`, `blender --background --python`)
5. **Catalog the command/undo system** — If the app has undo/redo, it uses a command pattern. These are your CLI operations

### Phase 2: CLI Architecture Design

1. **Choose interaction model** — Stateful REPL + Subcommand CLI (recommended: both)
2. **Define command groups** matching logical domains: Project management, Core operations, Import/Export, Configuration, Session/State management
3. **Design the state model** — What persists between commands, where stored, how serialized
4. **Plan output format** — Human-readable (tables, colors) + Machine-readable (JSON via `--json` flag). Always both.

### Phase 3: Implementation

1. Start with the **data layer** — XML/JSON manipulation of native project files
2. Add **probe/info commands** — Agents must inspect before modifying
3. Add **mutation commands** — One command per logical operation
4. Add **backend integration** — `utils/<software>_backend.py` that wraps the real software's CLI. Handle:
   - Finding the executable (`shutil.which()`)
   - Invoking with proper arguments (`subprocess.run()`)
   - Clear error messages with install instructions if not found
5. Add **rendering/export** — Generate valid project files, invoke the real software for conversion
6. Add **session management** — State persistence, undo/redo with exclusive file locking
7. Add the **REPL with ReplSkin** — Copy `repl_skin.py` into `utils/repl_skin.py`, use `invoke_without_command=True` to make REPL the default

### Phase 4: Test Planning (TEST.md - Part 1)

**BEFORE writing test code**, create `tests/TEST.md` with:

1. **Test Inventory Plan** — List planned test files and estimated test counts
2. **Unit Test Plan** — For each core module, describe what will be tested with edge cases
3. **E2E Test Plan** — Real-world scenarios with output property verification
4. **Realistic Workflow Scenarios** — Multi-step operations chained together

### Phase 5: Test Implementation

1. **Unit tests** (`test_core.py`) — Synthetic data, no external dependencies
2. **E2E tests — intermediate files** — Verify project files are structurally correct
3. **E2E tests — true backend** — **MUST invoke the real software.** Create a project, export via the actual backend, verify output:
   - File exists and size > 0
   - Correct format (magic bytes, ZIP structure, etc.)
   - Content verification where possible
   - Print artifact paths for manual inspection
4. **Output verification** — Never trust that export works just because it exits successfully
5. **CLI subprocess tests** — Use `_resolve_cli` helper to test the installed command:
   ```python
   def _resolve_cli(name):
       import shutil, os, sys
       force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
       path = shutil.which(name)
       if path:
           return [path]
       if force:
           raise RuntimeError(f"{name} not found in PATH")
       module = name.replace("cli-anything-", "cli_anything.") + "." + name.split("-")[-1] + "_cli"
       return [sys.executable, "-m", module]
   ```
6. **Round-trip test** — Create project via CLI, open in GUI, verify correctness

### Phase 6: Test Documentation (TEST.md - Part 2)

After running all tests, append to TEST.md:
1. Full `pytest -v --tb=no` output
2. Summary statistics — total tests, pass rate, execution time
3. Coverage notes — any gaps

### Phase 6.5: SKILL.md Generation

Generate `skills/SKILL.md` inside the Python package so it installs with pip. Include:
- YAML frontmatter with name and description
- Command groups table
- Installation prerequisites
- Usage examples
- Agent-specific guidance (always use `--json`, check return codes, verify outputs)

Ensure `setup.py` includes it as package data:
```python
package_data={
    "cli_anything.<software>": ["skills/*.md"],
},
```

### Phase 7: PyPI Publishing

1. Structure as PEP 420 namespace package — `cli_anything/` has NO `__init__.py`, sub-packages DO
2. Create `setup.py` with `entry_points={"console_scripts": ["cli-anything-<software>=..."]}`
3. Test local install: `pip install -e .`
4. Run tests against installed: `CLI_ANYTHING_FORCE_INSTALLED=1 python3 -m pytest`

---

## Critical Rules

### The #1 Rule — Use the Real Software
- The CLI **MUST** call the actual software for rendering and export. Not reimplement in Python.
- **Anti-pattern**: Building a Pillow-based compositor to replace GIMP
- **Correct**: Generate valid project files, hand them to the real software
- The software is a **hard dependency** — not optional, not gracefully degraded

### The Rendering Gap
- Most GUI apps apply effects at **render time**. Manipulating project files alone silently drops effects
- **Priority**: Native engine (`melt`) → Filter translation layer → Manual render script
- Never assume export works because it exited successfully — **verify programmatically**

### File Locking for Session State
- When saving session JSON, use exclusive file locking. **Never** use bare `open("w") + json.dump()`
- Open with `"r+"`, lock, then truncate inside the lock

### Timecode Precision
- Use `round()`, **not** `int()`, for float-to-frame conversion
- Accept ±1 frame tolerance at non-integer FPS (e.g. 29.97fps = 30000/1001)

### Filter Translation Pitfalls (ffmpeg)
- Same filter twice in a chain: merge into one
- Stream ordering for concat: **interleaved** `[v0][a0][v1][a1]`
- Effect parameter scales differ between tools — document every mapping explicitly

---

## Directory Structure

```
<software>/
└── agent-harness/
    ├── <SOFTWARE>.md          # Project-specific analysis and SOP
    ├── setup.py               # PyPI package configuration
    └── cli_anything/          # Namespace package (NO __init__.py)
        └── <software>/        # Sub-package (HAS __init__.py)
            ├── __init__.py
            ├── __main__.py
            ├── README.md      # REQUIRED — installation, usage, testing
            ├── <software>_cli.py  # Main Click CLI entry point
            ├── core/
            │   ├── __init__.py
            │   ├── project.py     # Project create/open/save/info
            │   ├── export.py      # Render pipeline + filter translation
            │   └── session.py     # Stateful session, undo/redo
            ├── utils/
            │   ├── __init__.py
            │   ├── <software>_backend.py  # Backend: real software invocation
            │   └── repl_skin.py   # Unified REPL skin
            └── tests/
                ├── TEST.md        # Test documentation and results — REQUIRED
                ├── test_core.py   # Unit tests (synthetic data)
                └── test_full_e2e.py # E2E tests (real files)
```

---

## Backend Reference

| Software | Backend CLI | Native Format | System Package |
|----------|-------------|--------------|----------------|
| LibreOffice | `libreoffice --headless` | .odt/.ods/.odp (ODF ZIP) | `apt install libreoffice` |
| Blender | `blender --background --python` | .blend-cli.json | `apt install blender` |
| GIMP | `gimp -i -b '(script-fu ...)'` | .xcf | `apt install gimp` |
| Inkscape | `inkscape --actions="..."` | .svg (XML) | `apt install inkscape` |
| Shotcut/Kdenlive | `melt` or `ffmpeg` | .mlt (XML) | `apt install melt ffmpeg` |
| Audacity | `sox` | .aup3 | `apt install sox` |
| OBS Studio | `obs-websocket` | scene.json | `apt install obs-studio` |

**The pattern is always the same: build the data → call the real software → verify the output.**

---

## Output Modes

Every command supports dual output:

- **Human-readable** (default): Tables, colors, formatted text
- **Machine-readable** (`--json` flag): Structured JSON for agent consumption

```bash
# Human output
cli-anything-gimp project info -p project.json

# JSON output for agents
cli-anything-gimp --json project info -p project.json
```

Agent rules for CLI output:
1. **Always use `--json`** for parseable output
2. **Check return codes** — 0 for success, non-zero for errors
3. **Parse stderr** for error messages on failure
4. **Use absolute paths** for all file operations
5. **Verify outputs exist** after export operations
