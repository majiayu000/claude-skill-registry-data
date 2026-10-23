---
name: tui-snapshot-tester
description: "Snapshot testing for terminal UI apps (TUIs) - captures rendered terminal frames as deterministic SVG / text snapshots, diffs them on every run, surfaces a reviewable HTML report on failure, and supports `--snapshot-update` to accept changes intentionally. Wraps `pytest-textual-snapshot` for Python Textual apps; provides equivalent recipes for Ratatui (Rust) `insta` snapshots, Charm Bracelet (Go) `teatest` golden files, and Ink (Node) `ink-testing-library`. Use for any TUI where layout regressions otherwise reach users via `screenshot looks wrong in terminal`."
---

# tui-snapshot-tester

## Overview

Per [textual-testing][txt]:

[txt]: https://textual.textualize.io/guide/testing/

> "Snapshot testing is the process of recording the output of a test, and
> comparing it against the output from previous runs." Textual's
> `pytest-textual-snapshot` plugin does this by saving an SVG screenshot of
> the running app to disk.

A TUI snapshot test:
1. Renders the TUI to a deterministic frame (SVG / text).
2. Compares the new frame to a stored baseline.
3. Fails on diff; produces an HTML diff report so the human
   reviews the change.
4. Updates the baseline only when the human says so.

This catches layout regressions (clipped text, wrong column
widths, broken borders) that exit-code / output assertions miss.

## When to use

- The unit-under-test is a TUI (Textual / Ratatui / Bubble Tea /
  Ink / curses).
- The TUI's value is its visual layout - assertions on individual
  cells are brittle and miss "the box border now looks broken."
- The team needs PR-time review of layout changes (vs catching
  them in user feedback).

For headless CLIs that emit text only, prefer
`bats-testing` +
`cli-output-conventions`;
TUI snapshots are only needed for layout-rich UIs.

## Step 1 - Install (Python / Textual)

Per [txt][txt]:

```bash
pip install pytest-textual-snapshot
```

This pulls Textual + the `snap_compare` pytest fixture.

## Step 2 - First snapshot test

Per [txt][txt] (verbatim):

```python
def test_calculator(snap_compare):
    assert snap_compare("path/to/calculator.py")
```

First run fails (no baseline). Per [txt][txt]:

> "Only ever run pytest with `--snapshot-update` if you're happy
> with how the output looks on the left hand side of the snapshot
> report."

Workflow:
1. Run `pytest`. It fails; emits an HTML report at
   `snapshot_report.html`.
2. Open the report. The "left hand side" shows the new render;
   the "right hand side" shows the saved baseline.
3. If the new render is correct, run `pytest --snapshot-update`
   to accept it.
4. Commit the updated `__snapshots__/` directory.

## Step 3 - Drive interactions before capture

Per [txt][txt]:

```python
# Press keys before snapshotting
assert snap_compare("path/to/calculator.py", press=["1", "2", "3"])

# Custom terminal dimensions
assert snap_compare("path/to/calculator.py", terminal_size=(50, 100))

# Run setup code (mouse hover, etc.)
async def run_before(pilot) -> None:
    await pilot.hover("#number-5")

assert snap_compare("path/to/calculator.py", run_before=run_before)
```

The `Pilot` API per [txt][txt]:

```python
async def test_keys():
    app = RGBApp()
    async with app.run_test() as pilot:
        await pilot.press("r")
        assert app.screen.styles.background == Color.parse("red")
```

`pilot.press()` / `pilot.click()` / `pilot.pause()` simulate user
input.

## Step 4 - CI integration (Textual)

Per [txt][txt]:

> "work well in CI on all supported operating systems, and the
> snapshot report is just an HTML file which can be exported as a
> build artifact."

```yaml
jobs:
  tui-snapshot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with: { python-version: '3.13' }
      - run: pip install pytest-textual-snapshot
      - name: Run snapshot tests
        run: pytest tests/ui/
      - uses: actions/upload-artifact@v4
        if: failure()
        with: { name: snapshot-report, path: snapshot_report.html }
```

Reviewer downloads `snapshot_report.html` from the failed CI
artifact, opens it locally, and decides accept / reject.

## Step 5 - Equivalent for Rust / Ratatui

Use `insta` for snapshot testing:

```toml
# Cargo.toml
[dev-dependencies]
insta = "1"
ratatui = { version = "0.29", features = ["test-buffer"] }
```

```rust
#[test]
fn renders_main_view() {
    let mut terminal = Terminal::new(TestBackend::new(80, 24)).unwrap();
    terminal.draw(|f| draw_main(f, &app_state())).unwrap();
    insta::assert_snapshot!(terminal.backend().to_string());
}
```

Update with `cargo insta accept` (or `cargo insta review` for
interactive triage). Snapshots stored in `tests/snapshots/`.

## Step 6 - Equivalent for Go / Bubble Tea

Use `teatest`:

```go
func TestApp(t *testing.T) {
    tm := teatest.NewTestModel(t, NewModel(), teatest.WithInitialTermSize(80, 24))
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})

    teatest.RequireEqualOutput(t, tm.FinalOutput(t,
        teatest.WithFinalTimeout(2*time.Second)))
}
```

`teatest.RequireEqualOutput` writes / compares against
`testdata/<test-name>.golden`. Update with `-update`:

```bash
go test -update ./...
```

## Step 7 - Equivalent for Node / Ink

Use `ink-testing-library`:

```typescript
import { render } from 'ink-testing-library';
import App from './app';

test('renders welcome screen', () => {
  const { lastFrame } = render(<App />);
  expect(lastFrame()).toMatchSnapshot();
});
```

Jest's built-in `toMatchSnapshot` writes to
`__snapshots__/`. Update with `jest -u`.

## Step 8 - Determinism

Snapshots fail randomly if any of these vary:

- **Date / time in output.** Mock the clock (Textual: `freezegun`;
  Ratatui: pass `now` as state; Ink: use `vi.useFakeTimers()`).
- **Random IDs.** Seed PRNGs deterministically.
- **OS-specific glyphs / fonts.** Pin OS in CI; warn on cross-OS
  diffs.
- **Locale.** `LC_ALL=C` in CI.

Without determinism, snapshot tests become noise → team disables.

## Step 9 - Snapshot review discipline

Treat snapshot diffs like test diffs in code review:

- Every snapshot change must be reviewed in PR.
- The HTML report is the artifact reviewers consult.
- Auto-update in CI (e.g., bot pushes `--snapshot-update` commit
  on diff) defeats the purpose.

The same review discipline applies to browser screenshots (covered by
the qa-visual-regression sister plugin).

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| `--snapshot-update` in CI by default                                   | Defeats regression detection; baselines drift silently.                  | Updates only on developer machine + reviewed in PR (Step 2). |
| Snapshots with timestamps / random IDs                                | Random failures; team disables tests.                                    | Mock clock + seed PRNG (Step 8). |
| One giant snapshot per app                                             | Any change forces full baseline review; reviewer skips.                | Per-screen / per-state snapshots. |
| Skipping Step 8 (determinism)                                          | Cross-OS / cross-machine diffs.                                       | `LC_ALL=C` + pin OS in CI. |
| No HTML report artifact                                                | Reviewer can't see the diff; rejects blindly or rubber-stamps.        | Upload `snapshot_report.html` artifact (Step 4). |

## Limitations

- **Brittle to font / terminal width changes.** Pin terminal size
  in tests (Step 3 `terminal_size=`).
- **Binary diff is harder to review.** Per-pixel SVG diffs require
  the HTML report; raw text diff is unreadable.
- **Slow on large UIs.** Each snapshot renders the full UI.
- **Platform divergence.** Cross-OS snapshots may diverge by font
  rendering; restrict CI to one OS for golden files.

## References

- [txt][txt] - `pytest-textual-snapshot`, `snap_compare`,
  `--snapshot-update`, `Pilot.press` / `Pilot.click` / `Pilot.pause`,
  HTML report, CI workflow.
- `insta` (Rust): `https://insta.rs/`.
- `teatest` (Go Bubble Tea): `https://github.com/charmbracelet/x/tree/main/exp/teatest`.
- `ink-testing-library` (Node Ink): `https://github.com/vadimdemedes/ink-testing-library`.
- `bats-testing` - exit-code + text
  output testing (text CLIs); pair with TUI snapshots for
  layout regression.
