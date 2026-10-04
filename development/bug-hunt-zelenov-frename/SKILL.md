---
name: bug-hunt
description: >
  Find bugs in frename before the owner does, UI bugs first. Use in every nightly session (step
  "Bug hunt" of the nightly skill), or when asked to "look for bugs", "check the UI", "audit".
  Screenshots every reachable screen at several sizes and languages, audits the code against the
  project skills' rules, looks for siblings of past bugs, verifies each finding, files it as a
  `bug` issue that the nightly pipeline then fixes without waiting for approval.
---

# Bug hunt

The goal is bugs the editor would hit, found and proven by the agent. A finding that is not
reproduced (a screenshot that shows it, a failing test, or a step list a second reviewer confirmed
in the code) is not filed. A preference ("this would look better as …") is not a bug: file it as
an `idea` or drop it.

What counts as a bug: the app does something other than what the README, a design doc in
`docs/design/`, an issue the owner wrote, or the rules in the project skills (`ui-dev`, `ui-core`,
`undo-dev`, `core-dev`) say; or something no editor would want: a crash or panic, lost or wrong
data on disk, text cut off or overlapping, a control that does nothing, a key that does the wrong
thing, an untranslated string, a state the user cannot get out of.

## 0. Before hunting

1. List open and closed issues labelled `bug`, `regression` and `idea` (including `rejected`, and
   issues the owner closed: they count as rejected, see `nightly` → Trust), so
   nothing is filed twice and nothing rejected comes back.
2. Triage the agent's own open `idea` issues (body starts with `🤖 agent:`, no `rejected`, no
   `hold`): one that describes a defect by the definition above becomes a bug: remove `idea`, add
   `bug` and a priority (below), and comment `🤖 agent: this is a defect, not a proposal; it will be
   fixed without waiting for approval.` Proposals stay `idea`.
3. Limits: skip the hunt when 8 or more agent-filed `bug` issues are open (fix those first). File
   at most 5 new bugs per hunt, most severe first; keep the rest of the candidates in the hunt
   notes of the last one filed so the next hunt starts from them.

## 1. UI sweep (always first)

Build the debug app once (`cargo build`; `cargo test` alone leaves an old exe). On Linux run
everything under Xvfb (`CLAUDE.md` → "Looking at the UI"); also install `xdotool`.

1. **Every demo scenario** in `docs/screenshots/*.toml`, each rendered:
   - at its own window size, and at `1024x640` and `1920x1080` (copy the scenario to a temp
     folder, change `window`, scale `panels`; keep `source` pointing at `tests/folder`);
   - with `--lang ru` (the longest strings), `--mono`, `--batch`;
   - `--settings <page>` for every Settings page.
   Park the pointer off the window first (`ui-dev` → "Checking your work"), or a tooltip lands in
   the picture.
2. **States demo mode cannot reach** (an open menu, the marker list while typing, a running batch
   job, a narrowed column, fullscreen, hover tooltips, dialogs): start the app under Xvfb with
   `FRENAME_DATA_DIR` set to a temp dir, in a temp copy of `tests/folder`, drive it with
   `xdotool mousemove/click/key/type`, and `import -window root` after each step.
   Cover each main flow from `app-guide`: open folder, play, add/remove tags, rename, comment,
   markers and the marker list, in/out, fullscreen, undo/redo, search, batch actions, Settings.
3. **Read every PNG** (the Read tool shows it). Zoom on anything doubtful:
   `magick in.png -crop WxH+X+Y -scale 300% out.png`. Check each picture against:
   - text cut off, ellipsis where the full text fits, placeholders cut off (#133), wrapped labels
     in a row meant to be one line;
   - overlap: tooltips, notes or panels over the picture or over each other (#163), a control
     hidden under another;
   - missing glyphs (boxes), wrong or English text in `--lang ru`, raw message ids;
   - spacing, alignment, sizes and colours against the rules in `ui-dev` and `ui-core`
     (segmented controls, spinners, theme colours, no literals);
   - empty, loading and error states that say nothing or show stale data;
   - in `--mono`, anything that still relies on colour alone.
4. Keep the stderr of every run: a `panic`, `ERROR` or a GStreamer error that the UI does not
   show is a finding.

## 2. Code audit against the skills

Run read-only subagents in parallel (`Explore` or `general-purpose`), one per area, each given the
skill it audits against and told to report only rule violations with `file:line`, the rule, and a
concrete user-visible failure:

| Area | Rules from | Look for |
|---|---|---|
| Views and widgets | `ui-dev`, `ui-core` | each "must"/"never" rule broken somewhere; hard-coded strings or colours; scroll ids reused wrongly |
| Undo | `undo-dev` | an edit that is not undoable, undo that leaves files or sidecars behind (#31, #110) |
| Keyboard | `app-guide`, `ui-dev` | a shortcut that fires while typing, or stops working after typing (#32); two bindings for one key; focus lost after an action |
| Files and metadata | `core-dev` | non-atomic writes, a write while Windows locks the file, errors swallowed, a sidecar not moved with its clip |
| Async and windows | `app-guide` | a task result applied to the wrong clip or window after navigation (#105, #112) |

## 3. Siblings of past bugs

List `bug` and `regression` issues closed in the last 30 days. For each, name the mistake in one
line (e.g. "an overlay shows tooltips in fullscreen") and search the code for the same mistake in
other places. A sibling is a new finding.

## 4. Edge inputs

Exercise `frename-core` with inputs editors really have: Cyrillic and very long file names, dots
and spaces in tags, an empty folder, a zero-byte or truncated video, a read-only file, a file
locked by another process, a clip renamed outside frename while open. Write each probe as a unit
test; one that fails on `main` is a finding, and its test goes into the fix PR.

## 5. Verify

For each candidate, a fresh subagent that did not find it tries to prove it wrong from the code and
the evidence (the same rule as the review gate: never reuse the finder). Only `CONFIRMED`
candidates are filed. A screenshot that shows the bug, or a test that fails on `main`, counts as
proof by itself.

## 6. File

One issue per bug, English, body:

```
🤖 agent: found by the bug hunt on <YYYY-MM-DD>.

**What happens:** …
**Expected:** … (and where that is stated: README, design doc, skill rule, issue #)
**Steps:** 1. … 2. …
**Evidence:** screenshot / failing test / file:line
**Likely cause:** file:line, one or two sentences.
```

Screenshots go on the `pr-screenshots` branch under `bugs/<YYYY-MM-DD>/<name>.png` (nightly →
"Screenshots in the PR" for how), embedded by their raw URL.

Labels: `bug` and one priority:
- `P1` — crash, lost or wrong data on disk, the editor cannot go on;
- `P2` — wrong behaviour or broken layout in a main flow;
- `P3` — cosmetic, or only in a rare state.

Never `regression` (only the owner sets it). The nightly pipeline picks these up by priority like
any other request.
