---
name: go-cli-progress
description: The progress surface for Go CLI tools - the two-line live block, the in-place meter carrying rate and ETA, how it degrades with terminal width, and the settled and summary lines it collapses into. Use when a command runs work worth watching, when clearing terminal lines, when showing a download or a file count advance, or when a command prints "Running..." then replaces it with a result. Triggers on ClearLines, NewMeter, NewGroup, Meter.Set, Meter.Add, Meter.Rate, Meter.Fields, Meter.Done, Meter.Fail, StdoutIsTerminal, GlobalDebugFlag, term.GetSize, out_time_us, speed=, and an in-place progress bar.
user-invocable: false
---

# Go CLI Progress

**One operation at a time in a two-line block that redraws in place, carrying how much is left and how fast it is going, collapsing into a single settled line when it finishes.**

This applies to CLI Only projects and the command surface of a CLI + Web hybrid, since it assumes the `utils` package exists.

One meter is live at a time. Two writers clearing lines each erase the other's output, so concurrent work reports through a single meter rather than a lane per worker. How that work is scheduled is the project's own decision, and nothing here imposes a pipeline, a job interface, or a resume file on it.

Redrawing is a terminal affordance, so the live block exists only when stdout is a terminal and `--debug` is off. Everywhere else every step is announced and nothing is cleared, which leaves a log or a pipe holding the full progression rather than cursor escapes.

| Behavior | Terminal | Piped | `--debug` |
|---|---|---|---|
| Styled icons and colors | yes | glyphs kept, color stripped | no |
| The live block | redraws in place | one line per tick, no bar | one zerolog entry per tick |
| Tick interval | 100ms | 1s | 1s |
| `ClearLines` / `ClearPreviousLine` | clears | no-op | no-op |
| The live block persists | no | yes | yes |

Glyphs survive a pipe because `✓`, `↻`, and the bar rune are text rather than escapes, and only color and cursor control are stripped. What disappears outside a terminal is the redraw, never the fact that a step ran.

A piped line carries the fields without the bar, which means something only while it redraws in place. One bar per tick fills a log with rows of dashes saying what the percent beside them already said.

Ten frames a second is below what reads as stutter in a terminal, and one line a second is the most a log can carry and still read as a progression.

## Reading the Source

A meter needs a position and a total, and derives everything else. What a source reports varies, so the source decides how the meter is built rather than the other way round.

| The source reports | The meter takes |
|---|---|
| a position and a total | `Set` or `Add`, and the total |
| a position, no total | `Set` or `Add`, and a total of zero |
| a percentage alone | a ratio unit, `Set(pct)`, and a total of 100 |
| finished items | `Add(1)`, and a total of `len(items)` |
| nothing countable | no meter, the running line |

A position is set when the source says where it is and added when it says how far it moved. `ffmpeg -progress` reports `out_time_us`, an absolute offset. A loop converting it into an increment gets the first tick wrong and every resumed run wrong after it.

```go
m := utils.NewMeter("Encoding", name, durationUS, utils.UnitMicros)
for b := range progressBlocks(stdout) {
    m.Set(b.OutTimeUS)
    m.Rate(b.Speed * 1e6)
}
m.Done()
```

A number the source measures is placed, and a number the meter can compute is derived. `speed=15.4x` is measured inside the encoder against its own frame accounting. A meter sampling positions reads each half-second report as a burst then a stall, printing 9.5x and 19x alternately for a run that never left 15x.

`Rate` takes the position's own unit per wall second, so a source reporting in other terms converts once at the call site.

An estimate is not a measurement, so a reported eta is discarded and the meter computes its own. `rsync --progress` prints one, but it is arithmetic over a position, a total and a rate the meter already holds. Two estimates disagreeing beside each other is worse than either alone.

## Line Clearing

```go
func ClearLines(n int) {
    if GlobalDebugFlag || !StdoutIsTerminal {
        return
    }
    for range n {
        fmt.Print("\033[A\033[2K")
    }
}

func ClearPreviousLine() {
    ClearLines(1)
}
```

The escapes go out through `fmt.Print` rather than a printer, since they are cursor control rather than content.

A running header cleared with its sub-lines takes `lineCount + 1`, the `+1` being the header. Counting only the sub-lines leaves the header stranded above the summary meant to replace it.

## The Live Block

A meter owns two lines: a header naming the work, and an indented meter line carrying the numbers.

```
↻ Downloading ubuntu-24.04.3-desktop.iso  file 1 of 2
  ─────────────────────────────   36%  242 / 661 MB  28.3 MB/s  eta 15s  avg 40.7 MB/s
```

The header glyph costs two columns, so its text and the meter line's bar both start at column 2. Every baseline line sits at column 2 and every indented detail line at column 4, which lets a meter, a settled line, and a failure stack without looking ragged.

Context after the name takes the muted color: the position in a set, a running total, and the item being worked. It drops entirely before the name is clipped, because the name is what the user is waiting on.

```go
m := utils.NewMeter("Downloading", name, resp.ContentLength, utils.UnitBytes)
m.Context("file 1 of 2")
if _, err := io.Copy(dst, io.TeeReader(resp.Body, m)); err != nil {
    m.Fail(err)
    return err
}
m.Done()
```

The verb and the name are separate arguments, because the header reads `↻ <verb> <name>` while the settled line and the group total carry the name alone.

A meter is an `io.Writer`, so a byte stream feeds it through `io.TeeReader` and the caller counts nothing. Work measured in items calls `m.Add(1)` once per item, and work that reports where it already is calls `m.Set`.

The meter owns its own ticker and line count. A caller tracking either has to get the clear count right on every path out of the function, and the path it misses is the error path.

A frame is assembled into one string and written with one `fmt.Print`. Two writes let the terminal paint a half-cleared block, which reads as a flicker on every tick.

A frame walks back over the lines it drew last time with `\033[1A\033[2K`, then writes each new line as `\r\033[2K` and the text. The meter holds the count it drew, since only it knows how many lines the last frame took.

The cursor is hidden while a meter is live and restored when it settles, including on the error path, because a process that exits with the cursor hidden leaves the user's shell without one.

The same restore runs from an interrupt handler, installed once when the first meter hides the cursor, and the process then exits `130`. Ctrl+C reaches neither `Done` nor `Fail`, and it is the most common way a long transfer ends.

## The Meter Line

Six fields in a fixed order, so a reader's eye lands in the same place moving from a download to a file count. A meter carries the ones its source can answer, not all six.

| Field | Example | Reserved | Drops |
|---|---|---|---|
| bar | `─────────` | 8 to 30 cells | when its floor stops fitting |
| percent | ` 36%` | 4 | with an unknown total |
| pair | `242 / 661 MB` | the widest form its unit takes | never |
| current rate | `28.3 MB/s` | the widest form its unit takes | third |
| eta | `eta 15s` | 11 | second |
| average rate | `avg 40.7 MB/s` | 4 more than the rate | first |

The reserved widths size the bar rather than pad the fields. The bar takes what the reservations leave, and the fields are joined by exactly two spaces at their natural width. A reserved width is the widest form that field takes for its unit, which keeps the bar from resizing when `eta 9s` becomes `eta 15s`. `avg 40.7 MB/s` needs fifteen cells against nine for `avg 15.4x`, so a constant would spend six cells of bar on nothing.

The pair is always carried, since it is the meter. The bar and the percent need a known total. The eta needs a known total and a run long enough to plan around. The current rate is carried when the work moves at a speed the tool does not control. A stall is then the thing being watched for. The average is carried only beside the current rate, because its whole job is the contrast.

| Set | Fields | Fits |
|---|---|---|
| `FieldsFull` | bar, percent, pair, rate, eta, average | a transfer over a link the tool does not control |
| `FieldsRate` | bar, percent, pair, rate, eta | the same, where the average is not worth its cells |
| `FieldsLean` | bar, percent, pair, eta | local work at a speed the user cannot act on |
| `FieldsBare` | bar, percent, pair | a short operation where only position matters |

```go
m := utils.NewMeter("Installing", pkg, 100, utils.UnitPercent)
m.Fields(utils.FieldsLean)
```

Omitting `Fields` takes the unit's own default, so a byte transfer needs no decision and only the unusual case says anything.

Percent is the one field rendered at a fixed width, `%3d%%`, so the fields to its right hold their column from `  9%` through `100%`.

Fields drop from the right as the terminal narrows and the bar shrinks toward its eight-cell floor. The bar goes once that floor no longer fits beside the fields still standing, leaving the numbers rather than a stub. Nothing wraps and no field is cut mid-value, because a wrapped frame makes the next redraw clear the wrong number of lines.

```
↻ Copying db.sqlite
   71%  45.8 / 64.0 MB
```

Width comes from `term.GetSize` on stdout, then `COLUMNS`, then a default of 80. A `COLUMNS` below the minimum of 24 is a stale value from a resized terminal rather than a real width, and 24 is where the stats alone stop fitting.

`GetSize` comes from `github.com/charmbracelet/x/term`, which already supplies the `IsTerminal` in `utils/globals.go` and arrives under the lipgloss stack anyway. `golang.org/x/term` for the same pair adds a second module for nothing.

The bar is a single `─` rune for both halves, filled in info blue and unfilled in dimmed chrome. One rune means the bar's length never changes as it fills, where a two-glyph bar reserves the wider of them everywhere.

An unknown total arrives as zero or less, which is what `resp.ContentLength` returns when the server sends no length. The bar sweeps across the track instead of filling, since a share of an unknown quantity is a number the tool does not have.

## Rates and ETA

The instantaneous rate comes from a trailing window and the average from the whole operation. A single rate hides a stall behind a healthy-looking average, and the user is watching precisely to see the stall.

The window is 800ms wide and reports zero until 200ms of samples have accumulated. A two-sample window microseconds wide divides a chunk by almost no time and reports hundreds of MB/s on the first tick.

The whole-operation average carries that same 200ms floor while the meter is live and none on the settled line, since a run that really did take 40ms has a real average and only a first tick that wide is an artifact.

ETA is computed from the whole-operation average rather than the windowed rate. An 800ms window swings the estimate on every tick, and a figure the user re-averages in their head is not an estimate. A stall then shows as the estimate climbing, which is the truth arriving gradually rather than all at once.

ETA is unknown whenever the total is unknown, the average is zero, or the result runs past about a hundred hours. Printing `eta 3170h` is worse than printing nothing, because the user reads it as a real estimate before working out that it is not.

A rate during a stall reads `0.0 B/s` rather than being blanked, since a blank field reads as a rendering bug and a zero reads as the truth.

Under a minute an elapsed time reads `9.5s` and an estimate reads `eta 15s`, because a measurement is accurate to a tenth of a second and an estimate is not. Both read `6m12s` under an hour and `3h04m` above one, which keeps the eta field inside the eleven cells `eta unknown` already needs.

## Settling

`Done` clears the live block and leaves one line in its place, so a finished run shows one line per operation regardless of how long each took.

```
✓ ubuntu-24.04.3-desktop.iso  661 MB  9.5s  avg 69.6 MB/s
```

`Fail` clears the block and prints an indented failure that persists, because a failure is what the user still has to act on.

```
  ✗ receipts/hotel-0913.heic: unsupported image format
```

`Fail` takes the error itself rather than a formatted string. The line reads the name, a colon, and the error's message, and the same error reaches the debug tier as `.Err(err)` with its whole wrapped chain.

This is the one exception to error detail staying in the debug tier, since a failure inside a run of twelve is unusable without naming which one failed and why.

A long name is clipped with `…` on both the header and the settled line, so the same name does not look different depending on which line it lands in.

## Grouped Work

Several operations under one heading print their settled lines as they land and close with a summary.

```
✓ assets.tar  180 MB  3.4s  avg 52.6 MB/s
✓ db.sqlite  64.0 MB  2.4s  avg 26.6 MB/s
↻ Copying media/clip-01.mp4  file 3 of 4  244 / 664 MB total
  ─────────────────────────────   31%  133 / 420 MB  73.0 MB/s  eta 4s  avg 91.5 MB/s
```

```
→ Copy  4 files  664 MB  11.9s  avg 56.0 MB/s
✗ Process  10 ok, 2 failed  11.0s  avg 0.9 items/s
```

```go
g := utils.NewGroup("Copy", "files")
for _, f := range files {
    m := g.Meter("Copying", f.Name, f.Size, utils.UnitBytes)
    if err := copyFile(f, m); err != nil {
        m.Fail(err)
        continue
    }
    m.Done()
}
g.Done()
```

A group is opened with the label its summary carries and the plural noun it counts in, and every meter under it comes from `g.Meter` rather than `NewMeter`. `→ Copy  4 files` has no other source for either word, and a meter that does not know its group cannot add what it moved to the total.

A failure with no meter behind it is reported with `g.Fail(name, err)`. A group counting only what a meter reported prints `4 files` for a run that attempted six.

The summary and the settled line are built by one function with the same field order, so the two read as one shape with a count in front. Two hand-rolled formats drift apart on the first change.

A summary is printed when more than one operation ran or when any failed. A single clean operation is already described by its settled line, and repeating it says nothing twice.

The amount sums what actually moved, including the partial bytes of a failed transfer, because the elapsed time bought those bytes. It is omitted when the count already carries the same number, and again when summing would add unlike units.

The glyph carries the outcome: `→` when everything succeeded, `✗` when anything failed, and the count reads `10 ok, 2 failed` instead of the plain total in that case.

## Work with No Quantity

Work with nothing to count uses the running line and the clear, with no meter at all. A bar that cannot move is worse than no bar, because it suggests progress the tool is not tracking.

Several sequential steps that read as one operation each announce and clear themselves, leaving one line behind.

```go
utils.PrintRunning("checking latest version")
release, err := checkVersion()
utils.ClearLines(1)

utils.PrintRunning(fmt.Sprintf("downloading %s", release.Tag))
err = download(release)
utils.ClearLines(1)

utils.PrintSuccess(fmt.Sprintf("updated: %s → %s", old, new))
```

A read-only scan over many items prints nothing per item, just one running line and then the findings. Per-item output during a check scrolls the findings off the screen before the user can read them.

## Units

A unit says what the counted quantity is, and four kinds cover every source measured so far.

| Kind | Counts | Amount | Rate |
|---|---|---|---|
| bytes | bytes | `242 / 661 MB`, binary multiples | `28.3 MB/s` |
| count | a plural noun | `7 / 12 items` | `1.1 items/s` |
| duration | a span of time | `30s / 24m52s` | `15.4x` |
| ratio | a proportion | nothing | nothing |

A duration's rate is a multiplier rather than a quantity over a second. Seconds per second is dimensionless, and the ratio already has a name. `ffmpeg` prints `speed=15.4x` for the same reason, so a tool wrapping it and the user reading both see one figure.

A duration unit carries the resolution it counts in, so a source reporting microseconds hands over `out_time_us` untouched. The amount still renders as `24m52s`, since the resolution governs the counter and never the display.

A ratio has no amount and no rate, so both render as nothing and the fields carrying them drop themselves. A percentage-only source needs no foresight from the caller and settles as one line.

```
✓ linux-image-6.14.0-32-generic  13.3s
```

A field whose unit cannot express it renders nothing and leaves the frame. That is what lets an unfamiliar source be wired up without knowing in advance which fields it will support.

A number carries one decimal below 100 and none at or above it, so `45.8 MB`, `242 MB`, `15.4x`, and `1.1 items/s` all stay inside the width their field reserved.

Both halves of a pair are scaled by the total rather than each by itself, so `39.9 / 64.0 MB` stays readable where `40874 KB / 64.0 MB` does not.

## Debug

The debug tier emits one zerolog entry per tick with the numbers as structured fields, never a formatted string, so a log query can filter on them.

```go
log.Info().
    Int("percent", pct).
    Int64("current", cur).
    Int64("total", m.total).
    Float64("rate", rate).
    Str("eta", eta).
    Msg(m.label)
```

zerolog's writer is settled once in `setupLogs` and nothing in the meter re-decides it.
