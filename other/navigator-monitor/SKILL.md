---
name: navigator-monitor
description: Utilities > System monitor, a departure from DN (DOS had one processor and nothing to measure it by) -- navigator/lib/system/monitor.py (cpu_times and CpuSampler's per-processor busy %, frequencies from cpufreq or cpuinfo, memory with the commit charge as Virtual, sensors from /sys/class/hwmon with the thermal-zone fallback, Snapshot.shape, Monitor, short_size), the meters (CpuMeters with cpu_layout's columns, MemoryMeters, SensorList), MonitorWindow (the natural size, refitting only while the rectangle is its own, the heights the boxes share), and [monitor] refresh. Use when changing the system monitor or reading another figure from /proc or /sys for it.
---

# System monitor

**Not DOS Navigator's.** DOS had one processor, no swap and no sensors, so the whole window is a departure, asked
for. It is recorded in three places: the module docstring of `navigator/lib/system/monitor.py`, the `#:` comment above
Utilities > *System monitor* in `main_menu.nml`, and the window's markup. It sits beside Process list
(`navigator-processes`) and is built the way that window is.

## The model (`navigator/lib/system/monitor.py`)

- **No psutil.** It reads `/proc/stat`, `/proc/meminfo`, `/proc/cpuinfo` and `/sys` directly, every path under a
  `root` (`/`, or a fake tree in `tmp_path` for tests). `available()` is false without `/proc/stat`, and
  `Shell.refusal` then greys out the menu entry with the reason.
- **Processors.** `cpu_times` turns each `cpu`/`cpuN` line into `Ticks(busy, total)`:
  - idle and iowait count as idle;
  - guest time is left out, because user and nice already hold it;
  - the summed `cpu` line is number -1.

  `CpuSampler` gives `Δbusy/Δtotal`. The first call is all zeros. A line that is new, or whose ticks went backwards
  (a processor brought online again), starts at 0.
- **Clocks.** `frequencies` reads `cpufreq/scaling_cur_freq` (kHz), else `/proc/cpuinfo`'s `cpu MHz`, else nothing.
  The clock column is shown only when some processor has one.
- **Memory.** *Memory* is `MemTotal - MemAvailable`. *Virtual* is the commit charge, `Committed_AS` of `CommitLimit`;
  under overcommit it passes 100%, so the bar clamps and the text says the truth. *Swap* is total less free, and reads
  *none* when there is no swap. The parsing is `navigator.lib.system.memory.meminfo`, which the editor's guard and
  System Information share.
- **Sensors.**
  - `sensors` walks `hwmon*` in number order. Each chip has `tempN_input` (millidegrees) with `_label`, `_max` and
    `_crit`, and `fanN_input` (RPM) with `_label`.
  - A reading that cannot be read is left out. A chip left with no readings is dropped; iwlwifi's sensor is
    unreadable while the radio is off.
  - Two chips of one name keep their device link's basename (`nvme0`, `0000:03:00.0`). A unique name drops it.
  - With no hwmon temperature at all, `/sys/class/thermal/thermal_zone*` becomes one `thermal` chip.
  - `Temperature.level` is `warm` at or past `_max` and `hot` at or past `_crit`. A limit of 0 or less is ignored.
- `Monitor()` is one read, called on the window's thread. `Snapshot.shape()` holds three things: the processor count,
  whether there are clocks, and each chip's name with its line count. It is what the window's size follows.

## The meters (`navigator/widgets/shell/monitor_meters/`)

These are Python only, as `ProcessList` is. Every line is one `draw_runs` call.

- **`cpu_layout(count, clocks, width)`** is the one place the column count is chosen:
  - it uses as few columns as keep a column at `COLUMN_ROWS` (8) rows, and never more than fit at `BAR_MIN` cells a
    bar; the bars then take the width there is;
  - **it depends on the width alone.** The CPU box's height follows from the rows, so if the height fed back into the
    columns, the layout would go round in a circle.

  A cell is a number, a bar, `nn%` and a clock. The cells flow down, then across.
- **The *All* line lines up with the cells under it.** The numbers are padded to `_label_width`: the widest number,
  or the translated *All* when that is wider. Every bar therefore starts in one column. *All*'s bar ends where the
  last column's bars end, with its share under theirs (`_cells_width`, `_cell_tail`).
- **`CpuMeters` and `SensorList`** are `ListViewer`s (`_Meters`):
  - **the cursor is never drawn**, because a reading is there to be seen, not chosen;
  - `move_cursor` scrolls by the delta and puts the cursor on the edge it moved towards, so the arrows, PgUp/PgDn,
    Home/End and the wheel scroll at once;
  - `CpuMeters` items are rows of `Cpu`s, set by the `_lay_out` effect. Its header row is the *All* bar;
  - `SensorList` items are `SensorRow`s (a chip's heading, then its readings), set by the `_list` effect.
- `MemoryMeters` is a plain `Widget` of three lines with tooltips that explain each one.
- Parts and classes:
  - `done` is the bar's filled part, and `done.busy` is the same at 90% or more;
  - `SensorList::heading` is a chip's line, and `::row.warm` and `::row.hot` are readings past a limit;
  - all are styled in `navigator.nss` under `MonitorWindow`.

## The window (`navigator/widgets/shell/monitor_window/`)

- **Reading.** `Background("nav-monitor", workers=1)` with a read counter: only the newest read is shown.
  - The first read starts in `mounted()`.
  - A `Timer` child (`ticker`, `interval: root.refresh_ms()` from `[monitor] refresh`, default 1, 0 turning it off)
    skips a tick while a read is in flight or `app.modal` is set. It follows the setting at once and stops with the
    window.
- **The size is the content's.**
  - `natural_size(w, h)` adds up the processors at `BAR_NATURAL`-cell bars, `memory_width()`, the longest sensor
    line, `MARGIN` (8: the frames, margins and scroll bar), the CPU rows plus the *All* row, the memory box (5) and
    the sensor lines. It is capped by the desktop.
  - `fit()` centres it at that size.
  - `mounted()` fits a first guess: every `processors()` with a clock and no sensors. Each read whose `shape()`
    differs fits it again.
  - **Refitting stops once the rectangle is the user's.** `fit()` remembers what it set (`_fitted`) and does nothing
    once `(x, y, width, height)` differs: moved, resized, tiled or zoomed.
- **`heights`** (computed) shares the window's rows:
  - the memory box gets 5;
  - the processors get what they need, but no less than half the rest when the sensors want more than there is;
  - the sensors get the remainder, and their box hides below 3 rows;
  - with no sensors, the processors take it all.
- Keys: Esc closes the window, Ctrl+R and Alt+R read again, and Tab moves between the two lists. *Monitor* (`Mo~n~itor`,
  because the bar's *Manager* holds M) joins the menu bar after *File*, and it is the right-click menu too. The key
  table is `monitor_window` in `keybindings.TABLES`; regenerate the default set after changing a binding.

## Tests

`tests/test_monitor.py` covers:
- the model over a fake `root`: `/proc/stat` deltas, a processor coming back, meminfo, hwmon chips with the same name,
  unreadable readings, the thermal fallback, and cpufreq vs cpuinfo;
- `cpu_layout`'s columns;
- the window, with `monitor.Monitor.__call__` monkeypatched to a queue of `Snapshot`s, `monitor_window.processors` set
  to 4 and `[monitor] refresh` set to 0. The checks are: its natural size and centring, growth when a sensor appears,
  no refit after `resize_to`, scrolling on 80x25 with 128 processors, Esc, and the warm/hot/busy colours.
