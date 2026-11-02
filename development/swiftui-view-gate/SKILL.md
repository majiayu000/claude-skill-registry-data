---
name: swiftui-view-gate
description: |
  Gate for SwiftUI view changes in native projects: look up the control, lint it,
  render it in its real container, report seen or unverified before done.
---

# SwiftUI view gate

A UI change is not done when it compiles. It is done when the view was **looked up before it
was written, linted after, and seen** — and the final report says which of those happened.

Field evidence (macOS app, 2026-10-13): a category dropdown got `.menuIndicator(.hidden)` and a
plain label, so it looked like static text. The user had to point it out. The first fix used sizes
and a "follows the HIG" claim nobody had looked up. Then `review_macos_hig` and
`review_accessibility` both said *clean* on a control that was still wrong: inside
`Menu { … } label: { Pill(…) }`, `.menuStyle(.borderlessButton)` makes AppKit draw its own chevron
on the left and discard the custom outline and colours. The same pill rendered alone looked right.
Only the composition showed it.

Invoke with `/superpowers-gstack:swiftui-view-gate`. A `PostToolUse` hook (`scripts/view-gate.py
nudge`) reminds the session when a view file is edited; it never blocks.

## Phase 0 — scope

Begin every Bash call that needs the scripts with:

```bash
SKILL_DIR='<the base directory the Skill tool printed when this skill loaded>'
VG="$SKILL_DIR/../../scripts/view-gate.py"; WS="$SKILL_DIR/../../scripts/window-shot.sh"
[ -f "$VG" ] || VG=$(ls ~/.claude/plugins/cache/*/superpowers-gstack/*/scripts/view-gate.py 2>/dev/null | sort -V | tail -1)
[ -f "$WS" ] || WS=$(ls ~/.claude/plugins/cache/*/superpowers-gstack/*/scripts/window-shot.sh 2>/dev/null | sort -V | tail -1)
[ -f "$VG" ] && [ -f "$WS" ] || { echo "BLOCKED — view-gate.py / window-shot.sh not found; run /plugin update superpowers-gstack"; exit 2; }
```

| Check | Detect via | If it fails |
|---|---|---|
| Native project | `.gstack/track` is exactly `ios`, `macos` or `both` | `web` or missing: refuse, "not a native Apple project". Anything else: `BLOCKED — invalid .gstack/track`. |
| Which files | `python3 "$VG" files --base <default-ref>` (`$VG` and `$WS` come from the block above) | None listed: say there is no view change and stop. |

Track decides the linters: `macos` → `review_macos_hig` + `review_accessibility`; `ios` →
`review_accessibility` only (the macOS linter's window and menu-bar findings mislead on iOS);
`both` → all, each on the files that belong to its platform. Add `review_liquid_glass` when the
project targets Liquid Glass (the `Liquid Glass` mention in `CLAUDE.md`, or macOS 26 / iOS 26
deployment target).

## Phase 1 — look up before writing

One `mcp__swiftui-rag__search_swiftui_corpus` query for the **control category** being built or
changed (pop-up button, table row, chip, toggle in a list), not for a SwiftUI symbol. Write down the
query and the one thing it decided. The corpus can answer off-topic (menu-bar examples for "Menu"):
when it returns nothing relevant, say so and do not cite it.

A design claim ("follows the HIG", "matches the system control") needs a source from this phase.
Without one, word it as a choice: "I chose 11 pt", not "11 pt per the HIG".

## Phase 2 — lint after writing

Run the linters from Phase 0 on each changed view file. Findings go in the same fix loop as compile
errors. The linters are **pattern checks**: *clean* means no known pattern matched, never that the
control looks right. In the field case they passed the very control the user found unusable.

## Phase 3 — see it

Render the changed view **in its real container**, not the bare subview: the `Menu`, the table row,
the toolbar. Leave a `#Preview` of that composition in the file. For a list or table render at least
one row per state: normal, longest label, empty (hover when cheap).

Choose the route by cost to the user, cheapest first:

1. **`live-swiftui`** (`render` + `screenshot`). No permission. Pass `packagePath` explicitly: in a
   worktree-isolated session it otherwise resolves to the primary checkout and renders stale code.
   No `#Preview` and no way to add one (hand-written pbxproj): append one to the view file, or use
   route 2.
2. **Window capture of the built app**, only when `.gstack/visual-verify` reads exactly `host`
   (the project owner's standing consent for *this* and nothing wider). Build the branch, launch that
   exact bundle and prove which one is running (`/superpowers-gstack:verify-and-land` Phase 5), then
   ```bash
   WINDOW_SHOT_EXPECT="$WANT" "$WS" "$PID" "${TMPDIR:-/tmp}/<name>.png"
   ```
   It captures one window by id, never the display, and exits non-zero rather than hand back an
   image that shows nothing (exit 3 not macOS, 4 no window, 5 blank capture, 6 wrong process,
   7 the Swift helper cannot be built). macOS only; `$PID` and `$WANT` are the Phase 5 proof of
   `verify-and-land`. The pin is committed, like `.gstack/e2e-executor`, so every worktree has it.
   `/superpowers-gstack:adapt` asks for it once on macOS projects. `vm` or `off` is the
   owner's answer: use route 1 or 4 and do not ask again. Only a missing file (a project
   adapted before 3.18.1) earns one question: may `host` be written into
   `.gstack/visual-verify`? Otherwise use route 1 or 4. Read the PNG afterwards; a path is not a look.
3. **Computer use** (clicks, typing) needs a per-session approval dialog that a plugin cannot grant.
   Use it only for a flow that must be driven, and prefer a mock backend over live data.
4. **VM with the E2E mock backend** (`vm-e2e`, `step()` screenshots) for states that need seeding
   (empty, failure, blocked) and for anything that must not touch real data.

Whole-display `screencapture` is not a route here: it shows whatever else is on the user's screen.
A hook that warns about `screencapture` is right about that; window capture of an app this session
launched is the exception `.gstack/visual-verify: host` grants.

## Phase 4 — affordance check

Every interactive element has a visible cue that it is interactive **without hovering**: a chevron
or indicator on pop-ups and pull-downs, an outline or fill on fields, the standard shape on buttons.
If the cue is hidden on purpose, state why in the report.

## Phase 5 — the report

Read the image and state what you saw, **including defects you were not looking for** (a truncated
label, a clipped chevron, a wrong side). List them before saying done. End with exactly one line:

```
View gate: rendered and seen — <files>; screenshot <path>; defects: <none | list>
View gate: built, appearance unverified — <files>; reason: <why no render was possible>
View gate: waived by user — <files>
```

`/superpowers-gstack:verify-and-land` reads this line. A diff that touches views and has no such
line is not presented as ready to land unless the user waives the gate. Never write the first form
without having read a rendered image this run.

## What this skill is not

- Not a plan review: `/superpowers-gstack:apple-native-review` reads specs and plans before code.
- Not a design-system review: `/superpowers-gstack:swiftui-design-consultation` owns `DesignSystem/`.
- Not a judgement of premium feel: that is `/superpowers-gstack:quality-review`.
- Not E2E: `/superpowers-gstack:e2e-route` owns scripted interaction.
