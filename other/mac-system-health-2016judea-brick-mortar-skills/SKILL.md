---
name: mac-system-health
description: Check a Mac's health from the shell — where the disk space went, what's eating CPU or memory, why it won't sleep (or why it slept during a long job), battery state, Time Machine status and pending updates. Use when you say "my disk is full", "what's using all my space", "why is my fan on", "what's using CPU", "is memory the problem", "keep my Mac awake while this runs", "why didn't my overnight job finish", "when did Time Machine last back up", "any updates". Read-only by default; names the one or two cleanup actions that need a human.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: df, du, diskutil, tmutil, pmset, caffeinate, top, ps, vm_stat, memory_pressure, sysctl, softwareupdate. No network except softwareupdate's own check.
metadata:
  grounded: "2026-11-03 — every read run live on macOS 26.6; nothing deleted or changed"
---

# Mac system health

Everything here reads. The few commands that change the machine are marked, and none of
them should run without the user saying so.

## Disk: where did the space go

```bash
diskutil info / | grep -E "Container (Total|Free) Space"   # the real numbers
df -h /System/Volumes/Data                                 # your files' volume
```

**`df -h /` lies on modern macOS.** `/` is the sealed, read-only system snapshot; it showed
12 GiB used on a disk that was 76 % full. Your files are on `/System/Volumes/Data`, and
all APFS volumes share one container, so the container's free space is the only free
space number that matters.

Find the big directories (no `ncdu` needed):

```bash
du -xhd1 ~ 2>/dev/null | sort -h | tail -15
du -xhd1 ~/Library 2>/dev/null | sort -h | tail -10
```

- `-x` stays on one filesystem; `2>/dev/null` hides the `Operation not permitted` lines
  from TCC-protected folders (which are then **under-counted**: grant Full Disk Access to
  the terminal for a true number, see `mac-permissions`).
- `du` over `~/Library` took ~1.5 minutes on a large home folder. Run it once, save the
  output, drill down from that.
- The usual suspects: `~/Library/Caches`, `~/Library/Developer` (Xcode DerivedData and
  simulators), `~/Library/Messages/Attachments`, `~/Library/Application Support/<app>`,
  Docker's VM disk, `~/Downloads`, old iOS backups under
  `~/Library/Application Support/MobileSync/Backup`.

**Local snapshots and "purgeable" space.** Time Machine keeps local APFS snapshots that
hold deleted files' blocks. Finder counts them as purgeable; `df` counts them as used.

```bash
tmutil listlocalsnapshots /
```

Changes (ask first): `tmutil thinlocalsnapshots / 10000000000 4` asks macOS to free up to
10 GB of snapshots; `tmutil deletelocalsnapshots <date>` deletes one. Deleting caches or
user files is the user's call, item by item. Never `rm -rf` a Library folder to make room.

## CPU and memory

```bash
top -l 2 -s 1 -n 10 -o cpu -stats pid,command,cpu,mem | awk '/^PID/{n++} n==2'
ps -Ao pid,%cpu,%mem,rss,comm -r | head -10
memory_pressure | tail -1                 # "System-wide memory free percentage: 54%"
sysctl -n vm.swapusage
sysctl -n hw.memsize machdep.cpu.brand_string
```

- **`top -l 1` shows 0.0 % CPU for everything**: CPU is a delta and the first sample has
  nothing to compare to. Take two samples and keep the second (the `awk` above).
- `ps %cpu` is a decaying average, good for "what's been busy", bad for "right now".
- `vm_stat` counts pages; on Apple silicon a page is **16384 bytes**, not 4096 (it says so
  on its first line). Multiply accordingly or just use `memory_pressure`.
- High memory use alone is normal (macOS fills RAM with cache). The signals are low
  free percentage from `memory_pressure`, swap that keeps growing, and the yellow/red
  pressure graph in Activity Monitor.
- `WindowServer` high = many displays/animations; `mds`/`mdworker`/`corespotlightd`
  high = Spotlight indexing after a big file change (it settles); `kernel_task` high =
  thermal throttling (it's cooling the CPU down, not using it).

Killing a process is the user's call; name it and its pid. `kill <pid>`, never `-9` first.

## Sleep, power, battery

```bash
pmset -g batt                    # % and charging state
pmset -g | grep -E "sleep|displaysleep|lowpowermode"
pmset -g assertions              # who is preventing sleep right now, and why
pmset -g log | grep -E "^\S+ \S+ \S+ (Sleep|Wake|DarkWake)\s\s|Display is turned" | tail -20   # sleep/wake history
```

- `sleep 1 (sleep prevented by powerd, ...)` in `pmset -g` names the blocker. The
  `Listed by owning process` section of `assertions` names the app and its reason.
- **Keep the Mac awake for a long job** (this is the fix for "my overnight run froze"):

  ```bash
  caffeinate -dims long-running-command args   # awake until the command exits
  caffeinate -i -t 3600 &                      # or for a fixed time
  ```

  It shows up in `pmset -g assertions` as `caffeinate command-line tool`. A sleeping Mac
  freezes timers, so a network timeout in a sleeping process never fires; a job that
  "hung" overnight is usually a job that slept.
- Closing the lid on battery sleeps regardless of `caffeinate -i`; plug in or keep it open.
- Changing `pmset` settings needs `sudo` (a human); reading never does.

## Time Machine

```bash
tmutil destinationinfo            # "No destinations configured." = no backups at all
tmutil latestbackup               # path of the newest backup (needs the disk mounted)
tmutil status                     # Running = 1 while a backup is in progress
```

`Failed to mount backup destination` from `latestbackup` means the disk isn't connected,
not that backups are broken.

## Updates and uptime

```bash
softwareupdate --history | head   # what was installed and when
softwareupdate -l                 # checks Apple's servers; slow; lists pending updates
uptime
sw_vers
```

Installing updates (`softwareupdate -i`) restarts things and needs the user. Report what's
pending; don't install.
