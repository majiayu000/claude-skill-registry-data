---
name: go-cli-output
description: The utils printer for Go CLI tools - the two output tiers behind --debug, the Print* API, table rendering, terminal colors, and error discipline. Use when writing anything a CLI prints, when building or changing utils/printer.go, utils/table.go, or utils/globals.go, or when a command reaches for fmt.Println. Triggers on PrintInfo, PrintSuccess, PrintError, PrintFatal, PrintWarn, PrintGeneric, PrintTable, GlobalDebugFlag, StdoutIsTerminal, lipgloss.Println, and lipgloss.ANSIColor.
user-invocable: false
---

# Go CLI Output

**Every line a CLI Only tool prints goes through `utils`, which renders it two ways depending on whether `--debug` is set, and drops its own color whenever stdout is not a terminal.**

Web Only and Headless API Service projects have no `utils/` package. They log through the same zerolog setup and print nothing else, since a container's stdout has no reader to style output for.

## The Two Tiers

| Tier | Flag | Output |
|---|---|---|
| Normal (default) | none | styled ANSI via lipgloss, transient lines cleared |
| Debug | `--debug` | zerolog with timestamps and full error detail, console on a terminal and JSON otherwise, nothing cleared |

There is no third tier for a machine reading the output, and a flag that asks for one is not added. An agent invoking the tool passes `--debug` and gets more than a plain-text mode could carry: every step announced, every wrapped error intact, and nothing redrawn over.

## Piped Output

Plain text is a property of the destination rather than a mode the caller selects. Every printer writes through `lipgloss.Println`, whose writer is `colorprofile.NewWriter(os.Stdout, os.Environ())`; that resolves to `NoTTY` when stdout is not a terminal and strips every escape sequence on the way out. Piping the tool anywhere produces plain text with nothing passed and nothing remembered.

zerolog answers the same check one level up, choosing the writer rather than decolorizing one: `ConsoleWriter` on a terminal, and its own JSON otherwise.

```go
var out io.Writer = os.Stdout
if StdoutIsTerminal {
    out = zerolog.ConsoleWriter{Out: os.Stdout, TimeFormat: time.DateTime}
}
log.Logger = zerolog.New(out).With().Timestamp().Logger()
```

Ephemeral output is a terminal affordance and nothing else. `ClearLines` and the in-place progress meter are inert under `--debug` and whenever stdout is not a terminal, so a log or a pipe keeps the full progression rather than a stream of cursor escapes.

## Globals

```go
package utils

import (
    "os"

    "github.com/charmbracelet/x/term"
)

var GlobalDebugFlag bool

var (
    StdinIsTerminal  = term.IsTerminal(os.Stdin.Fd())
    StdoutIsTerminal = term.IsTerminal(os.Stdout.Fd())
)
```

`term.IsTerminal` rather than `os.ModeCharDevice`: `/dev/null` is a character device, so the mode bit reports a terminal for the one stream that most certainly has nobody at it, and a prompt gated on it then opens a TUI into the void. The module already ships under the bubbletea and lipgloss stack, so using it directly adds no build.

Both are evaluated once at package init, since neither stream is replaced underneath a running process.

## The Print Shape

Every printer branches the same way, debug first and styled output otherwise. Writing them all to one shape means a new printer is a copy with a different glyph rather than a new decision.

```go
var (
    infoStyle    = lipgloss.NewStyle().Foreground(lipgloss.ANSIColor(12)) // bright blue
    successStyle = lipgloss.NewStyle().Foreground(lipgloss.ANSIColor(10)) // bright green
    errorStyle   = lipgloss.NewStyle().Foreground(lipgloss.ANSIColor(9))  // bright red
    warnStyle    = lipgloss.NewStyle().Foreground(lipgloss.ANSIColor(11)) // bright yellow
)

func PrintInfo(msg string) {
    if GlobalDebugFlag {
        log.Info().Msg(msg)
        return
    }
    lipgloss.Println(infoStyle.Render("→ " + msg))
}

func PrintError(msg string, err error) {
    if GlobalDebugFlag {
        if err != nil {
            log.Error().Err(err).Msg(msg)
        } else {
            log.Error().Msg(msg)
        }
        return
    }
    lipgloss.Println(errorStyle.Render("✗ " + msg))
}

func PrintFatal(msg string, err error) {
    PrintError(msg, err)
    os.Exit(1)
}
```

`fmt.Println` never appears in a printer, since it writes past the color profile and leaves escape sequences in a piped stream.

## The Print Surface

| Function | Normal | Debug |
|---|---|---|
| `PrintInfo(msg)` | `→ msg` blue | `log.Info()` |
| `PrintSuccess(msg)` | `✓ msg` green | `log.Info()` |
| `PrintError(msg, err)` | `✗ msg` red | `log.Error().Err(err)` |
| `PrintFatal(msg, err)` | `✗ msg` red, then `os.Exit(1)` | `log.Error().Err(err)`, then exit |
| `PrintWarn(msg, err)` | `! msg` yellow | `log.Warn().Err(err)` |
| `PrintGeneric(msg)` | `msg` | `msg` |
| `PrintRunning(msg)` | `↻ msg` blue | `log.Info()` |
| `PrintIndentedSuccess(msg)` | `  ✓ msg` green | `log.Info()` |
| `PrintIndentedError(msg, err)` | `  ✗ msg` red | `log.Error().Err(err)` |
| `PrintIndentedWarn(msg, err)` | `  ! msg` yellow | `log.Warn().Err(err)` |
| `PrintIndentedRunning(msg)` | `  ↻ msg` blue | `log.Info()` |

`PrintGeneric` adds no prefix, no glyph, and no style, because data the caller wants verbatim (a URL, a token, a rendered table) must not gain a marker that a consumer then has to strip.

`PrintFatal` exits with status 1 after printing, so a caller never has to remember the `os.Exit` that a fatal message implies.

## Error Discipline

The `msg` parameter is the human-readable label, and `err` is the Go error. Passing the actual `err` in the error parameter is what makes `--debug` useful, since zerolog's `.Err(err)` records it as a structured field that a baked-in string cannot become.

Normal output shows only `msg`. The error detail is exclusively for debug introspection, which keeps a stack of wrapped errors out of a user's face while leaving it one flag away.

```go
utils.PrintFatal("git not found in PATH", err)
utils.PrintIndentedError(toolName, result.Err)
```

Passing `nil` for `err` is correct only when there genuinely is no underlying error: a validation failure, a summary line, an informational warning.

## Subprocess Errors

A direct `exec.Command` that fails returns "exit status 1" and nothing else, so capture stderr into the error before printing it, or the debug tier records a message with no cause.

```go
cmd := exec.Command("sudo", "cp", src, dst)
var stderr strings.Builder
cmd.Stderr = &stderr
if err := cmd.Run(); err != nil {
    if detail := strings.TrimSpace(stderr.String()); detail != "" {
        err = fmt.Errorf("%s: %w", detail, err)
    }
    utils.PrintFatal("failed to copy binary", err)
}
```

A helper that already captures both streams into the returned error needs none of this.

## Terminal Colors

Colors are ANSI indices 0 through 15, never hex. An index is remapped by the user's terminal theme, so the same tool reads correctly under Dracula, Catppuccin, Solarized, or a scheme nobody has published; a hex value overrides that theme and fights it. Bright variants, 8 through 15, are preferred for foreground text.

```go
var (
    ColorBlue    = lipgloss.ANSIColor(12) // bright blue
    ColorGreen   = lipgloss.ANSIColor(10) // bright green
    ColorRed     = lipgloss.ANSIColor(9)  // bright red
    ColorYellow  = lipgloss.ANSIColor(11) // bright yellow
    ColorMagenta = lipgloss.ANSIColor(13) // bright magenta
    ColorCyan    = lipgloss.ANSIColor(14) // bright cyan
    ColorFg      = lipgloss.ANSIColor(15) // bright white, primary text
    ColorMuted   = lipgloss.ANSIColor(7)  // white, secondary text
    ColorChrome  = lipgloss.ANSIColor(8)  // bright black, borders and dim UI
)
```

## Tables

`PrintTable(headers, rows)` renders one way, as lipgloss box drawing. Box characters are not escape sequences, so a piped table arrives intact with only its colors stripped, and a second renderer for a second audience would be a format nobody validates.

```go
package utils

import (
    "charm.land/lipgloss/v2"
    "charm.land/lipgloss/v2/table"
)

var (
    headerStyle = lipgloss.NewStyle().Bold(true).Foreground(ColorFg).Padding(0, 1)
    cellStyle   = lipgloss.NewStyle().Foreground(ColorMuted).Padding(0, 1)
    borderStyle = lipgloss.NewStyle().Foreground(ColorChrome)
)

func PrintTable(headers []string, rows [][]string) {
    t := table.New().
        Border(lipgloss.NormalBorder()).
        BorderStyle(borderStyle).
        Headers(headers...).
        Rows(rows...).
        StyleFunc(func(row, col int) lipgloss.Style {
            if row == table.HeaderRow {
                return headerStyle
            }
            return cellStyle
        })
    PrintGeneric(t.Render())
}
```

A command whose output is meant to be parsed rather than read takes a `--json` flag and marshals a struct, which is a data contract instead of a table someone has to scrape.
