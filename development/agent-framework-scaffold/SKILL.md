---
name: agent-framework-scaffold
description: Runs the 6-step wizard that generates the skeleton of a new project (operator-profile.yaml + the chosen templates) — check environment → configure → validate → generate.
---

> **Auto-Trigger:** When the user wants to start a new project with the operator-kit/continuity-kit structure, or asks to "build the skeleton", "create the initial profile", "setup wizard".
> **Keywords:** "scaffold", "wizard", "new project", "skeleton", "initial operator-profile", "setup wizard", "build the structure"
> **Priority:** MEDIUM
> **Tools:** Bash, Read, Write

## When NOT to Activate
- The project already has `operator-profile.yaml` — run the wizard only if you want to regenerate from scratch (it does not merge; it overwrites the files it generates).
- You only want to see what it would generate: run it with `--demo --out <a scratch directory>` first, never against the project itself.

## Contract

**INPUT:** `--out <dir>` (destination) + `--project-name` (optional, default "agente-teste" in `--demo`).

**OUTPUT:** `operator-profile.yaml` + the chosen templates, instantiated with `{{project_name}}` substituted, in `<out>/docs/plans/execution/`.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | scaffold generated (or already identical — no-op) |
| 2 | missing prerequisite (Python <3.9, git missing, PyYAML missing) or invalid config |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `templates/*.template.md` (bundled) | Reads | source of the templates to instantiate |
| `<out>/operator-profile.yaml` | Writes | generated profile (R0-R4 ladder + project name) |
| `<out>/docs/plans/execution/*.md` | Writes | instantiated templates |

## Process
1. **Run the wizard** (`--demo` mode = non-interactive, sensible defaults):
   ```bash
   python wizard.py --demo --out /path/to/new-project
   ```
2. **Confirm the IP/PII cleanliness** in the output (must always be exit 0 — the scaffold is 100% generic):
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/../installers/kit-forge/ip_pii_linter.py /path/to/new-project
   ```
3. **Re-running is safe** — same content = no-op, never duplicates or corrupts.

## Executed examples

Measured on Windows with Python 3.14.3; paths in the JSON use Windows separators.
Each example runs from a fresh module copy; the second one prepares its first run itself.

```console
$ python wizard.py --demo --out out
[1/6] check_python — Python 3.14.3
[2/6] check_git — git version 2.52.0.windows.1
[3/6] check_deps — PyYAML available
[4/6] configure
[5/6] validate
[6/6] generate_and_summary
{
  "project_name": "agente-teste",
  "out_dir": "out",
  "files_written": [
    "operator-profile.yaml",
    "docs\\plans\\execution\\00-READ-FIRST.md",
    "docs\\plans\\execution\\00-STATE.md",
    "docs\\plans\\execution\\00-VISION.md",
    "docs\\plans\\execution\\00-PROCESSES.md"
  ],
  "files_skipped_customized": [],
  "no_op": false
}
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python wizard.py --demo --out out >/dev/null && python wizard.py --demo --out out
[1/6] check_python — Python 3.14.3
[2/6] check_git — git version 2.52.0.windows.1
[3/6] check_deps — PyYAML available
[4/6] configure
[5/6] validate
[6/6] generate_and_summary
{
  "project_name": "agente-teste",
  "out_dir": "out",
  "files_written": [
    "operator-profile.yaml",
    "docs\\plans\\execution\\00-READ-FIRST.md",
    "docs\\plans\\execution\\00-STATE.md",
    "docs\\plans\\execution\\00-VISION.md",
    "docs\\plans\\execution\\00-PROCESSES.md"
  ],
  "files_skipped_customized": [],
  "no_op": true
}
```
<!-- executed: 2026-10-30 · exit=0 -->
(2nd run against the same destination = no-op — identical directory sha256; the 5 files are rewritten byte-identical, so nothing changes.)

```console
$ python wizard.py --out no-demo
usage: wizard.py --demo --out <dir> | wizard.py --answers <file> --out <dir> | wizard.py --interview
```
<!-- executed: 2026-10-30 · exit=2 -->
(without `--demo` the wizard refuses — the real interactive mode is not implemented yet, and the script is honest about that instead of pretending.)

## Proof

```bash
python wizard.py --self-test
```
