---
name: tui-design
description: "Build terminal user interfaces with craft and intention — information architecture, interaction design, and visual hierarchy in monospace. Go + Bubble Tea + Lip Gloss. Use when building TUI dashboards, interactive CLIs, terminal menus, status displays, or any terminal interface. For Manzanita Research projects, this skill works alongside brand-tokens for the color palette."
license: Complete terms in LICENSE.txt
---

# TUI Design

You build terminal user interfaces with the same care you'd bring to a physical instrument. The terminal is an intimate space — just you and the machine — and it should feel like that. Not sterile. Not noisy. Like a well-organized workshop where every tool is within reach and every label is legible.

The user provides what to build. You design and implement it in Go with Bubble Tea and Lip Gloss, production-grade and thoughtful.

**For Manzanita Research projects:** Read the `brand-tokens` skill for the color palette. This skill handles the craft of TUI design; brand-tokens handles the specific palette values.

## Design Philosophy

The terminal is a constraint, not a limitation. Constraints are where character lives.

**The feeling:** Information presented with care, not dumped. The kind of CLI where you notice someone thought about the spacing, the wording, the rhythm of the output. Like the Whole Earth Catalog's index pages — dense with information but beautifully organized.

**What it is:** Calm. Readable. Status that communicates at a glance. Text that sounds like a person wrote it.

**What it is not:** Rainbow ANSI vomit. Boxes around everything. ASCII art logos on startup. Emoji-heavy output. Progress bars with cute animations that slow things down. Anything built to impress in a demo GIF rather than to be used daily.

## Color in Terminals

Terminals are intimate. The palette should be restrained — color where it counts, muted everywhere else.

### Principles

- **Color sparingly.** Most text should be the terminal's default color or a light/muted tone. Color marks meaning, not decoration. If everything is colored, nothing stands out.
- **Status uses natural tones.** Map status to a landscape palette: greens for good/healthy, gold/amber for caution/partial, warm reds for problems/errors, a primary accent for active/selected. These feel gentler than pure red/green/blue alarm colors.
- **Never use pure red, green, or blue.** `#FF0000`, `#00FF00`, `#0000FF` are alarm colors. We don't alarm. Use muted, warm versions.
- **Respect `NO_COLOR`.** Honor the `NO_COLOR` environment variable (https://no-color.org/). Degrade gracefully to plain text.
- **Test on both backgrounds.** Your palette should work on both dark and light terminal backgrounds. Muted, mid-range colors tend to survive both.

### Lip Gloss Style Hierarchy

Define a clear text hierarchy using style constants:

```go
// Level 1: Section titles — bold, accented
titleStyle := lipgloss.NewStyle().Bold(true).Foreground(accentColor)

// Level 2: Item names — default weight, lighter color
nameStyle := lipgloss.NewStyle().Foreground(textColor)

// Level 3: Descriptions — muted
descStyle := lipgloss.NewStyle().Foreground(mutedColor)

// Level 4: Hints and help — dim
hintStyle := lipgloss.NewStyle().Foreground(dimColor)
```

Keep all color definitions in one file (`styles.go`) so they're easy to swap for different projects or brand systems.

## Typography & Spacing

You're on a monospace grid. Every character placement is a design decision.

- **Generous whitespace.** Let the terminal breathe. `MarginBottom(1)` between sections. `Padding(0, 2)` on containers. Cramped TUIs are hostile TUIs.
- **Indent with 2 spaces** for hierarchy, not 4. Terminal real estate is precious.
- **Maximum content width of 80 characters.** Respect the classic terminal width even on wide screens. Use `MaxWidth()` to enforce this.
- **Left-align everything.** Centered text in a terminal looks lost.
- **Bold for titles and emphasis only.** If everything is bold, nothing is.
- **Don't depend on italic.** It's unreliable across terminals and fonts.

## Status Indicators

Status is the core vocabulary of a TUI. Get the symbols right.

```
●  linked / active / running      (accent/success color)
○  missing / inactive / stopped   (error or muted color)
◐  partial / syncing / stale      (warning color)
✓  complete / success             (success color)
✕  failed / conflict              (error color)
>  cursor / selected              (primary accent)
```

### Rules

- **One symbol system per tool.** Don't mix `✓`/`✕` with `●`/`○` for the same concept within the same interface.
- **Indicators at the start of the line.** Eyes scan the left edge. Status goes before content.
- **Color AND shape.** Don't rely on color alone — the symbols should communicate even without color, for `NO_COLOR` compatibility and colorblind users.

## Information Architecture

### Dashboard Views (the default when you launch a TUI)

- Show the most important state at a glance. No scrolling needed for the summary.
- Group by the highest-level concept (org, project, category) then show detail inline.
- Counts and summaries over exhaustive lists. "3/5 linked" over listing all five.
- Detail on demand — press enter or a key to drill in.

### List Views

- Use Bubble Tea's `list` component for anything scrollable.
- Show 2–3 pieces of metadata per item, not everything. The rest goes in a detail view.
- Filter and search should be available but not visually prominent until activated.

### Progress and Action Views

- Show what's happening, what happened, and what's next.
- Results grouped by outcome (created, skipped, errors) not by execution order.
- Counts at the top, details below. The summary is the headline.

## Interaction Design

### Key Bindings

```
q / ctrl+c    quit (always)
j/k or up/down    navigate (always in lists)
enter          select / drill in / confirm
esc            back / cancel
s              sync (when applicable)
r              refresh
?              help
```

### Rules

- **`q` always quits.** No confirmation dialog. Trust the user.
- **Show available keys at the bottom of every view.** Keep it to one line, in dim styling. This is the user's safety net.
- **Vim-style navigation (`j`/`k`) alongside arrow keys.** Both work, always.
- **Single keys over typed words.** Never require typing a full word when a single key will do.
- **Visible cursor/highlight.** The user should always know where they are. A clear selection indicator is the most important visual element in any interactive list.

## Language & Copy

Every string in a TUI is read closely. The tone matters.

### Principles

- **Lowercase for status messages.** "3 linked, 2 already up to date" not "3 Linked, 2 Already Up To Date."
- **Active voice, present tense.** "syncing..." not "Sync in progress..."
- **Name things plainly.** "no projects found" not "No projects were discovered."
- **Error messages say what happened and what to do.** "can't read config.json — check it exists and is valid JSON" not "Error: ENOENT."
- **Warm, brief help text.** "add a config file to get started" not "Please configure a manifest file in your repository."

### Never Say

- "Successfully" — if it worked, just say what happened.
- "Please" — we're not a waiter. Just say what to do.
- "Error:" as a prefix — the context makes it clear.
- "Invalid" — say what's wrong specifically.

## Bubble Tea Architecture

### Model Structure

```go
type Model struct {
    // State
    view     view        // which screen we're on
    cursor   int         // selection position
    err      error       // current error, if any

    // Data
    items    []Item      // whatever we're showing
    results  []Result    // action results

    // Layout
    width    int         // terminal width (from WindowSizeMsg)
    height   int         // terminal height
}
```

### Rules

- **One model per TUI.** Use a `view` enum to switch between screens, not separate programs.
- **Data loading in `Cmd` functions only.** Never in `Update` or `View`. Keep the render loop fast.
- **`View()` is a pure function of state.** No side effects. No I/O. It reads the model and returns a string.
- **Handle `tea.WindowSizeMsg`** to adapt layout to terminal size. Store width/height in the model.
- **Always handle `ctrl+c` in every view.** The user must always be able to exit.

### Message Pattern

```go
// Data loading results as messages
type dataLoaded struct {
    items []Item
    err   error
}

// Action results as messages
type actionDone struct {
    results []Result
    err     error
}
```

## Headless Mode

Every TUI tool should also work without the TUI. Same logic, plain text output. This is important because it makes the tool scriptable, pipeable, and testable.

- **Subcommands** (`sync`, `status`, `help`) run headless by default.
- **No subcommand** (bare invocation) launches the TUI.
- **Headless output** uses the same language but simpler formatting — no Lip Gloss, just plain text with Unicode indicators.
- **Exit codes:** 0 for success, 1 for errors. Pipe-friendly.
- **Human-parseable by default.** Machine-parseable output (JSON) is a separate `--json` flag if needed, not the default.

## Implementation Notes

**Stack:** Go with [Bubble Tea](https://github.com/charmbracelet/bubbletea), [Lip Gloss](https://github.com/charmbracelet/lipgloss), and [Bubbles](https://github.com/charmbracelet/bubbles) for standard components.

**Project structure:**
```
cmd/<tool>/main.go       — entry point, subcommand routing
internal/tui/
  tui.go                 — main Model, Update, View
  styles.go              — Lip Gloss style definitions (all colors here)
internal/<domain>/       — business logic, independent of TUI
```

**Performance:**
- Bubble Tea redraws on every message. Keep `View()` fast — precompute expensive string building in `Update` if needed.
- Use `tea.WithAltScreen()` for full-screen TUIs. Skip it for inline output that scrolls.
- Load data asynchronously via `Cmd`. Show "loading..." states, not frozen screens.

**Testing:**
- Business logic in `internal/<domain>/` is independently testable — no TUI dependency.
- TUI testing via Bubble Tea's `teatest` package for integration tests.
- Test headless output as plain strings — easy to assert against.

**Accessibility:**
- Screen readers work with terminal output. Use clear, semantic text.
- Every status indicator should have a text equivalent nearby (not just a colored dot).
- Respect `NO_COLOR`.
- Keyboard-only is the primary input mode — mouse support is a bonus, not a requirement.
