---
name: ui-automation
description: Use when a task needs a rendered interface observed, a browser driven, or a desktop application operated — post-deploy UI acceptance, checking whether a page renders as expected, driving software with no usable CLI, or capturing visual evidence — and should be executed by the external Codex agent rather than in this session. Not for writing automation code such as test suites or Playwright specs. Covers dispatching through `codex exec`, the artifact contract, and evidence recovery.
whenToUse: When a task needs eyes on a screen or hands on a GUI and should be delegated to Codex — post-deploy UI acceptance, verifying page rendering, driving a native app that has no CLI, or gathering screenshots as evidence.
---

# UI Automation (delegated to Codex)

## Overview

Dispatch a self-contained task to the external Codex agent when the work requires eyes on
a screen or hands on a GUI: browser automation, Chrome inspection, desktop application
operation, or visual verification. Codex supplies its own model plus its own browser-use
and computer-use plugins. This session supplies the task, the contract, and the review.

**The return channel is text only.** Screenshots, recordings, and produced files never
travel back through it — they must land on disk. The artifact contract below is what makes
them retrievable.

## When to Use This Skill

- Verifying a deployed or released UI against expected behaviour
- Checking whether a page renders correctly, or inspecting it via browser devtools
- Driving an application that has no usable CLI (a GUI tool, an editor, a 3D package)
- Any task whose success is established by *looking at something* rather than by reading output
- Any task where the artifact produced (render, export, recording) is the deliverable

Do **not** use this skill when the task is fully expressible as shell commands and file
reads in this workspace — do that work directly.

Do **not** use this skill to *write* automation code (test suites, Playwright or Cypress
specs, scraping scripts). That is an ordinary coding task. This skill is for dispatching
interface work to an external agent, not for producing automation source.

## Workflow

### Step 1 — Scope the run

Write down, before dispatching:

- the exact URLs, app names, or file paths involved
- the checkable expectations, as a numbered list ("login form shows an error on empty submit")
- what artifacts you need back (screenshots of failures, the exported file, a recording)

Each dispatch is a **fresh, self-contained Codex thread**. It remembers nothing from a
previous dispatch, so everything it needs must be in this prompt or in files on disk.

### Step 2 — Prepare the run directory

```bash
RUN_ID="$(date +%Y%m%d-%H%M%S)-<slug>"
RUN_DIR="$PWD/.codex-runs/$RUN_ID"
mkdir -p "$RUN_DIR/shots" "$RUN_DIR/out"
cp <skill-dir>/references/output-schema.json "$RUN_DIR/schema.json"
```

Never write run artifacts to `/tmp` — use the workspace so they survive and can be reopened.

### Step 3 — Dispatch

```bash
codex exec --skip-git-repo-check \
  -C "$PWD" \
  --output-schema "$RUN_DIR/schema.json" \
  -o "$RUN_DIR/result.json" \
  "<prompt>"
```

The prompt must restate the contract every time:

> Work only inside `<RUN_DIR>`. Write every screenshot to `<RUN_DIR>/shots/` as
> `NN-<short-name>.png`. Write all other produced files to `<RUN_DIR>/out/`. Do not describe
> images in prose without also saving them. Your final message must satisfy the given
> schema, and every `fail` verdict must cite at least one saved screenshot path.

Useful additional flags:

| Flag | When |
|---|---|
| `--json` | You need the event stream (tool calls, progress) rather than just the end state |
| `-i <file>` | You want to hand Codex an image (a design reference, a previous screenshot) |
| `-m <model>` | Only to override the configured model deliberately |
| `--add-dir <dir>` | The task needs a writable directory outside the working root |
| `-s <mode>` | Override the sandbox policy for this run |
| `resume --last` | Follow-up question to the most recent thread, instead of a fresh dispatch |

Run it in the background: these tasks take minutes.

### Step 4 — Recover the evidence

1. Read `$RUN_DIR/result.json` for the structured verdict.
2. **Open the screenshots yourself** with the image-reading tool — do not relay conclusions
   you have not looked at. The paths are in the result's `artifacts` (and usually `evidence`).
3. If a `fail` verdict has no screenshot, treat the finding as unverified and re-dispatch
   rather than reporting it.

### Step 5 — Act and report

Fix what the evidence establishes. Surface the images to the user with the presentation
tool so they see what you saw. If you need to re-verify after a fix, dispatch a **new** run
with a new `RUN_ID` — do not assume continuity.

## Hard Constraints

- **Evidence over prose.** A claim without a saved artifact is not evidence. Reject it.
- **Artifacts land on disk, in the workspace.** The return channel cannot carry them.
- **One dispatch, one self-contained task.** No thread continuity across dispatches.
- **Unattended.** Codex cannot ask a human anything; approval requests are denied or
  auto-reviewed. If a task genuinely needs a human decision, split it out.
- **No rollback.** Files changed or external systems touched before a cancel are not undone.
- **Never let two agents drive the same screen at once.** This session and Codex must not
  both be operating the desktop concurrently.

## Environment Notes

- Prefer **browser use (Chrome over CDP)** over **computer use** for web work. It needs no
  screen-recording permission, yields clean page screenshots, and Codex itself prefers it.
- Reserve computer use for native desktop applications.
- A terminal-spawned process usually has **no macOS Screen Recording permission**, so
  shell screenshot utilities fail. Page screenshots via CDP are unaffected.
- If dispatch fails with a model or capability error, check `codex --version` against the
  Codex build the user actually runs, and `codex debug models` for the valid model list.
  A stale CLI reports unknown models and fails requests the current build handles.

## References

Load these only when the step needs them. They must be listed here — the load result does
not enumerate the skill directory.

- `references/contract.md` — the run directory layout, naming rules, and the exact prompt
  block that carries the contract. Read before your first dispatch.
- `references/output-schema.json` — the structured verdict schema passed to
  `--output-schema`. Copy it into each run directory.
- `references/ui-acceptance.md` — post-deploy page acceptance: expectation lists, viewport
  and state coverage, and how to report failures.
- `references/desktop-app-task.md` — driving a native GUI application and recovering the
  produced file.
