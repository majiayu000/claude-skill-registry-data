---
name: lsdsk
description: Use when inspecting or diagnosing storage hardware - which disk hangs off which controller, whether a SATA, SAS or NVMe link runs at the speed both ends support, whether a controller sits in a slot worthy of it, how worn an SSD is, whether reallocated or pending sectors are climbing, drive temperatures, controller firmware, or where there is room for another drive. Also use when reaching for lspci, lsblk, smartctl or nvme-cli to answer any of those, and when reading an lsdsk report and deciding what to actually do about a finding.
---

# lsdsk

Groups disks by the controller they hang off, compares every link against what
both ends of it could do, and reports what is worth acting on. It also names the
mainboard, from DMI, which is what makes its placement advice actionable. Linux
and Windows, no subprocesses, no network. It runs anywhere `--replay` is all you
need, macOS included; only reading real hardware is the two.

**Bare `lsdsk` gives a PERSON the interactive view and a PROGRAM the printed
page.** It looks at whether stdin, stdout and the stream the view draws on are
all terminals: where they are it opens the full-screen application, because the
whole machine on one page is more than a reader takes in at once; where any is
not - a pipe, a redirect, a CI log - it prints the page. On Linux and macOS the
view draws on STDERR, so `lsdsk 2>err.log` at a terminal prints the page too; on
Windows it draws on stdout, so a redirected stderr keeps the view. The exit code
is the findings' in both, so `lsdsk; echo $?` means the same thing either way.
`lsdsk report` asks for the page by name, whatever the terminal looks like, and
`lsdsk tui` asks for the view by name: where one of those streams is not a
terminal it refuses with `22` rather than open a view nobody can see or quit.

**Being a subprocess does NOT mean you get the page. Say `lsdsk report` in
anything unattended.** Some callers hand their child a pseudo-terminal on both ends, and
there lsdsk cannot tell a program from a person: it opens the application and
waits for a keypress nobody can send. Measured in a notebook, where a CI job
hung on a bare `!lsdsk` for 900 seconds and was killed - IPython runs `!cmd`
under pexpect, so every notebook frontend does this. `script`, expect and
pty-allocating job runners allocate the same way, so treat them the same.

So `!lsdsk report` in a notebook cell, and `lsdsk report` in any scheduled or
unattended job, rather than reasoning about whether that caller counts as a
terminal. Getting it wrong costs a hang, and getting it needlessly right costs
nothing.

`lsdsk report` takes `--replay` like any other command, and the global options
still come first: `lsdsk --no-record report --replay file.json`.

That distinction matters when you TELL somebody to run it. If they want the
page on screen rather than the application, say `lsdsk report`.

For a TICKET or a handover, still send a snapshot rather than redirected text:
`lsdsk snapshot -o file.json` captures the raw reading, so the recipient can
replay every section at any width and any privilege question is settled by the
capture itself. A `lsdsk > report.txt` is a picture of one moment at one width.
A snapshot names the machine and every drive in it, so check who can read the
ticket before attaching one; `lsdsk snapshot` says the same on stderr when it
writes the file.

The page is the whole report: mainboard, problem summary, the PCI fabric,
the controller table, disk identities, wear and error counters, SMART
attributes, PCIe slots, counter trends, and every finding with its reasoning, in
that order. It already contains `trend` and `slots`, so running those again
after a bare `lsdsk` adds nothing. Run it first and nothing else, for a handover, a
ticket, or any machine you do not already know. Every subcommand is one section
of it, for when you already know which section you want. Unprivileged it still
renders every section and never aborts; what it could not read shows `-` and the
header names it, so check that line before quoting a counter as zero.

Bare `lsdsk` takes no `--format`: it is a group rather than a command. For a
structured capture of everything, use `lsdsk snapshot -o file.json`; for one
section's envelope, `lsdsk <section> --format json`.

## Running it

```bash
uvx lsdsk                     # at a terminal the interactive view, elsewhere the page
uvx lsdsk report              # everything on one page, by name. Start here
uvx lsdsk topology            # the problem summary and the PCI fabric, storage-only by default
uvx lsdsk findings            # every finding, with reasoning and a remedy
uvx lsdsk health              # wear, temperature, hours, error counters
uvx lsdsk smart               # every disk's SMART attributes against its thresholds
uvx lsdsk controllers         # controllers, PCIe placement, free ports
uvx lsdsk slots               # every PCIe port: what holds it, what is free
uvx lsdsk disks               # one row per disk
uvx lsdsk trend               # what each error counter is DOING, not just its total
uvx lsdsk record              # store one reading, print nothing, for a timer
uvx lsdsk tui                 # the same eight views, interactive (1-8, left/right, q)
uvx lsdsk snapshot -o m.json  # capture the raw reading
uvx lsdsk info                # version, homepage and the shell command name
uvx lsdsk config              # show effective configuration (--section thresholds for one)
uvx lsdsk config-deploy --target user   # write ~/.config/lsdsk so it can be edited (app|host need root)
uvx lsdsk config-generate-examples --destination DIR   # scaffold examples
uvx lsdsk --replay m.json     # render a capture from any machine
```

`--replay` works in either position on every command that reads a machine and
means the same thing, so `lsdsk --replay m.json health` and
`lsdsk health --replay m.json` are the same run; give both and the command's own
wins. `snapshot` is the exception: it captures the machine it runs on and
refuses `--replay` outright, as below. `--profile` is accepted after `config` and
`config-deploy`, but `config-generate-examples` takes it only before the command
and exits `2` otherwise. `--history-file` and `--no-record` exist only before the
command, so `lsdsk --history-file /var/lib/lsdsk/history.json record` is right and
`lsdsk record --history-file ...` is the usage error that exits `2`. Give that
path in full: a bare filename writes the store into whatever directory you
happened to be in. When in
doubt, `lsdsk <command> --help` (or `-h`) lists what that command takes.

`fail` and `logdemo` also exist. They are not diagnostic commands: they are the
vehicles the traceback and logging tests drive through the real entry point.
Never reach for them to answer a question about hardware.

## Reading `lsdsk topology`

It is the PCI fabric, drawn root-down. Every root complex is a port of the
processor on the board, the bridges between are the PATH a drive's traffic
takes, and a controller's drives are its own table nested under it rather than
another level of fabric.

```text
showing storage and the bridges above it; --tree-density to change the detail level
legacy = no PCIe capability
linux-sas-hba   2 root complexes (0000:00, 0000:ff)   root ports to PCIe Gen3x8   95 PCI devices
   └─┬ root complex 0000:00
     │     address       capable                running                name
     ├─┬── 0000:00:03.0  Gen3x8 (7.88 GB/s)     Gen3x8 (7.88 GB/s)     Intel Corporation Xeon E7 v2/Xeon E5 v2/Core i7 >
~    │ └── 0000:03:00.0  Gen4x8 (15.75 GB/s)    Gen3x8 (7.88 GB/s)     Broadcom / LSI Fusion-MPT 12GSAS/PCIe Secure SAS>
     │     device        model                         size  kind  bus   port    disk    link    temp  worn
~    │     /dev/sda      Samsung SSD 870 EVO 4TB     3.6TiB  SSD   SATA  12G     6G      6G       36C    1%
```

**The first line is the BOARD, not a bus.** It names the board where DMI gave a
name and the machine where it did not, how many root complexes the MACHINE has,
the best link the board's own root ports publish where one was read, and how
many PCI devices the capture holds. A tree whose first line were a bus label
would start one level below the thing that explains it.

**Under the board, each root complex has a heading of its own** -
`root complex 0000:00`, or `no bus address` for devices the platform published
no PCI address for - and that root complex's devices hang one level below it.
The heading is not a device: it carries no link and no hop figures, so a blank
there is not a reading of any kind, and the interactive view does not select
it. Every machine draws one, a single root complex included.

**The default draws the LEAST of the fabric, so a missing device is usually the
setting rather than the tool.** The note above the tree says which:

- `storage-only`, the shipped default - storage and the bridges above it.
- `storage-and-siblings` - those plus the devices sharing a bridge with storage.
- `full` - every PCI device.

So a graphics card, a NIC or a Thunderbolt leg is absent by design at the
default. Ask for more with `--tree-density full` before concluding lsdsk cannot
see a device, and in the interactive view press `d`, which cycles the three from
least detail to most. Do not report "lsdsk does not show my GPU" as a defect
without saying which density you ran.

**The two hop columns are what the DEVICE can do and what it NEGOTIATED**, in
the tool's own words:

- `capable` - the best link this device publishes.
- `running` - what it actually negotiated.

Where the two differ the device is below its own maximum, which is the
comparison this view exists to draw. Read them against the PORT above it, which
is the row one level up (a device directly under a root complex heading has
no port above it): in the sample the HBA is `capable` of `Gen4x8` and
running `Gen3x8` because the root port above it is a Gen3 port, so the card is
not faulty and the board is the ceiling.

**A hop column holds a SYMBOL when there is no figure, and the section spells
out whichever one it drew.** None of them is a fault, and reading one as a fault
is a work order against hardware that is fine:

- `- = not read` - nobody published the register. Windows exposes a PCIe link
  for endpoints and for BRIDGES not at all, so every bridge row reads this
  there. It means UNMEASURED, never "down".
- `legacy = no PCIe capability` - the device has no PCIe capability at all,
  which is an ordinary legacy PCI part. It is a reading, not a gap.
- `none = no link trained` - the register WAS read, and no lane is up: usually a
  slot or root port with nothing in it, or a function built into the chip with
  no link of its own. A reading like `legacy`, not a gap like `-`, and nothing
  to reseat on it. A storage controller whose link never trained raises its own
  critical finding, so `none` alone never calls for action. The row says which:
  a row tagged `root port` or `switch port` with nothing drawn beneath it is a
  slot with nothing working in it; any other row is a built-in function.

The distinction matters because those two look alike and mean opposite things
about the EVIDENCE. `legacy` is a positive reading - the platform answered, and
the answer was "this part has no PCIe capability". `-` is the platform declining
to answer, so nothing has been established about that link either way. No rule
fires on either, and no device is ever called slow on a symbol.

**The detail panel adds two more, and each panel explains only the ones it
drew.** A cell reading `n/a` is a value that CANNOT exist for that subject,
which is not the same fact as a reading nobody took: the four numbered ATA
attributes on an NVMe drive, which publishes one fixed log page and no attribute
table at all, and the occupant fields of a socket the panel has just reported
empty. Read as a missed reading it sends somebody looking for a fault.

A figure written `<= Gen3x8 (7.88 GB/s)` is a CEILING rather than a placeholder.
An uplink is the lower of what the card supports and what the bridge above it
does, so with one end unread it is whatever the other end said and can only be
too high. The end that WAS read is a real measurement, which is why the figure
is marked instead of dashed. On Windows this is every PCIe controller, because
Windows publishes a link capability for an endpoint and none for a bridge.

**The marker column on the far left is the finding, not the link.** A `!` or `~`
sits on the row a finding names, so a drive with a perfectly good link can carry
one for wear or for CRC errors. Read `lsdsk findings` for what it is about
rather than inferring it from the row it sits on.

## Devices with no hardware behind them

A zram swap device, a loop mount, a ZFS zvol, a device-mapper or mdraid node:
the kernel provides these itself, so they have no controller, no link and no
SMART. lsdsk reads them, says so, and does not judge them - no rule fires on one
and no finding names one, because there is nothing to compare against.

It decides by asking the kernel where the device sits, never by its name. A
device with no hardware parent resolves under `/sys/devices/virtual`; a real one
resolves under its PCI path. So an optical drive, named `sr0`, is ordinary
hardware occupying a real port and is counted as one.

They are folded away rather than listed, because a Proxmox host has more of them
than drives. The topology tree and the disk table each end with a line saying
how many and of what:

```text
kernel-virtual devices, with no controller and no counters
   3 not listed: 1 loop, 1 zd, 1 zram   (--expand-virtual lists them)
```

`--expand-virtual` gives each one a row, before or after `topology`, `disks` and
`tui`. To make that the default on a host whose zvols are the point, set the
configuration key - `lsdsk --set display.expand_virtual=true disks` for one run,
or `expand_virtual = true` under `[display]` in the deployed
`config.d/70-display.toml` to keep it:

```bash
uvx lsdsk config-deploy --target user     # then edit ~/.config/lsdsk/config.d/70-display.toml
```

**This setting changes the screen and nothing else.** The devices are always
read, always counted in the header, and always present in `--format json`. A
program never has to ask for them.

`--format json` gives a machine-readable envelope on every command that
produces data, including `info`, `snapshot`, `record` and all three
`config` commands. `tui`, `fail` and `logdemo` have none, having no data to
structure, and `report` has none deliberately: it is the whole page, whose
machine-readable form is `snapshot`.
It carries `ok`, `command`, `data` and `skipped`,
so a caller can tell a complete answer from a partial one.

**The envelope's four keys, and what a caller may rely on.** `ok` is true when
the command did everything asked of it, and false when something was left
undone - it is NOT "the hardware is healthy", so never alert on it. `skipped` is
a list of sentences saying what was not done and why, empty when nothing was. A
reading one DEVICE refused appears there too, as `<reading>: <subject> - <reason>`,
so a run made as root can still be incomplete: a drive behind some RAID drivers
refuses SMART passthrough, and an AHCI port count is read by mapping the
controller's own registers, which some hosts deny outright. Those entries name
the drive or the PCI address, so a check does not have to interrogate the machine
again to find out which one said no.
`command` names the command that produced the payload. `data` is that command's
own result.

**A finding, inside `data.findings`, has five string fields: `severity`,
`subject`, `title`, `detail`, `action`.** `severity` is exactly one of
`critical`, `warning`, `hint` - those three words, lower case, and no others.
That is what a monitor branches on, and it is the only way to separate critical
from warning, because the exit code cannot: `1` means "warning OR critical", so
a check that must fire only on critical has to read the field.

```bash
lsdsk findings --format json |
python3 -c 'import json,sys
d = json.load(sys.stdin)
sys.exit(any(f["severity"] == "critical" for f in d["data"]["findings"]))'
```

Keep every continuation line at column 0. An indented one inside `python3 -c` is
an `IndentationError`, which exits `1` - the same code these checks use for
"found", so the monitor reports a critical on a machine that has none.

**A disk, inside `data.disks`, carries `node`, `path`, `model`, `serial`,
`firmware`, `wwn`, `size_bytes`, `kind`, `bus`, `controller_address`, `link`,
`pcie`, `usb`, `health` and `readings_refused`.** Every one but `node`, `path`,
`model`, `bus` and `readings_refused` may be `null`, which means it was not read
rather than that it is zero. `readings_refused` is a list, empty on a drive that
answered everything, and each entry is an object of `reading` and `reason`: what
was asked for, and what the operating system said when it would not give it. `bus` is one of
`sata`, `sas`, `nvme`, `usb`, `virtual`, `unknown`; `kind` is `ssd`, `hdd` or
`unknown`. `link` is an object of `negotiated_gbps`, `drive_max_gbps` and
`port_max_gbps`, and a speed rule only fires when both ends are known. On a disk
reached over USB, `link` stays the drive's own link behind the bridge in its
enclosure, and `usb` is the USB link from the machine to that bridge: an object of
`running`, `device_max`, `port_max`, `behind_hub`, `upstream`, `on_usb2_twin` and
`transport` (`uas`, `bot` or `unknown`), each speed in it an object of
`lane_rate` (`1.5M`, `12M`, `480M`, `5G` or `10G`, where `M` is Mb/s and `G` is
Gb/s, per lane) and `lanes` (1 or 2). The speed is the lane rate times the lanes:
`{"lane_rate": "10G", "lanes": 2}` is 20 Gb/s and `{"lane_rate": "480M", "lanes": 1}`
is 0.48 Gb/s. `usb` is `null` on every other disk.

**A controller, inside `data.controllers`, carries `kind`**, which is one of
`ahci`, `sas`, `nvme`, `raid`, `ide` or `other` - read from the PCI class code,
so `other` is a mass-storage device of a subclass with no name of its own. It
carries `address`, `name`, `vendor`, `driver`, `firmware`, `link`, `port_count`,
`ports_used`, `upstream`, `upstream_address`, `upstream_name` and
`readings_refused` beside it. **Every entry is already a storage controller**:
both platforms list only PCI mass-storage devices (class `0x01`) there, so no
filter is needed and none is exported. That is not the same as "every controller
a disk hangs off": a USB disk's `controller_address` names its USB host
controller, which is not a storage device and is not in `data.controllers`.

**`data.virtual_disks` is a second list of the same shape**, holding the devices
with no hardware behind them. It is always populated, whatever `--expand-virtual`
or `display.expand_virtual` says, and `data.disks` never contains one - which is
what a check for "nothing without a transport among the real drives" reads:

```bash
lsdsk disks --format json |
python3 -c 'import json,sys
d = json.load(sys.stdin)["data"]
sys.exit(any(x["bus"] == "virtual" for x in d["disks"]))'
```

That check is Linux-only, deliberately. On Windows `bus` is `virtual` for a
HYPERVISOR disk, which is the machine's real storage, so the same line would
fail on a healthy guest. It is `data.virtual_disks`, not the bus value, that
means "provided by the kernel with nothing behind it" - so the check that holds
on either platform asserts the two lists stay disjoint:

```bash
lsdsk disks --format json |
python3 -c 'import json,sys
d = json.load(sys.stdin)["data"]
virtual = {x["node"] for x in d["virtual_disks"]}
sys.exit(any(x["node"] in virtual for x in d["disks"]))'
```

**`snapshot` is the exception to all of this.** With `-o` (`--output` in full) it writes the raw
reading - the bytes the platform gave, for `--replay` - which is a different
document from the envelope above and is not a list of disks. `-o -` writes that
reading to stdout instead of a file, which is why it refuses `--format json`.

**A monitor must read `data.privileged` too, or it reports clean on a blind
run.** Unprivileged, no SMART is read, so no wear or counter finding is ever
raised and the check above passes on a machine nobody looked inside.
`data.privileged` and `data.devices_accessible` are both booleans in the same
payload: treat `privileged` false as "unknown", never as "healthy".

**In a Python program, skip the subprocess.** `lsdsk.adapters.hw.snapshot`
gives an inventory and `lsdsk.domain.diagnostics.diagnose` gives the findings as
objects, with the same rules the CLI runs:

```python
from pathlib import Path

from lsdsk.adapters.hw import snapshot
from lsdsk.domain.diagnostics import diagnose

inventory = snapshot.load(Path("capture.json"))  # or snapshot.collect() for this machine
findings = diagnose(inventory)  # each has .severity, .subject, .title, .detail, .action
```

Both calls raise `lsdsk.domain.errors.ConfigurationError` - `load` for a file
that is unreadable, malformed, or not a snapshot this version parses, and
`collect` for a platform with no hardware reader, which raises the
`UnsupportedPlatformError` subclass. A path that is not there at all raises the
`MissingFileError` subclass, so a caller that wants to tell an absent snapshot
from a present but malformed one catches that before the base class rather than
reading the message. `collect` also lets a `PermissionError`
through when the read is refused outright, which is the exit 13 the CLI leaves.
Catch `ConfigurationError` and `PermissionError` around either call in anything
long-running.

`diagnose` returns a tuple and takes two more keyword arguments the CLI fills
in: `thresholds`, and `history` for the trend rules. Omit them and you get the
SHIPPED defaults with no history, which is not what the same machine's `lsdsk`
would report if its configuration deploys different thresholds.

**Do not hand-roll what `lsdsk.domain.diagnostics` already exports.**
`count_by_severity(findings)` returns a count per `Severity` including the zeros,
which is the whole split at once rather than the one-severity test the shell
check above can make.
`format_pcie_sentence(speed_gtps, width)` writes a link the one way the whole tool
writes it, so a sentence you compose agrees with the table beside it.
`interface_demand_gbytes(disk)` and `attached_demand_gbytes(controller, inventory)`
are the demand figures the oversubscription rule reasons from. Every rule is
callable on its own, which is how you run one without the rest:
`diagnose_disk_link(disk, inventory)`,
`diagnose_controller_link(controller, inventory)`,
`diagnose_controller_oversubscription(controller, inventory)`,
`diagnose_port_allocation(inventory)`, `diagnose_health(disk, series, thresholds)`
and `diagnose_firmware_consistency(inventory, thresholds)`. `DEFAULT_THRESHOLDS` is
what those rules fall back to when no `Thresholds` is passed, and its fields carry
the shipped figures: `wear_warning_percent` 80, `wear_critical_percent` 95,
`crc_errors_significant` 100. Build your own with `Thresholds(...)` and pass it,
rather than reading a field off the default and comparing yourself.

**`lsdsk.adapters.hw.snapshot` holds more than `load` and `collect`.**
`read_current_machine()` returns the raw reading as a dict, `serialise(capture)`
validates it and returns the text a capture file holds, and `save(capture, path)`
writes that text to a file. `snapshot -o <file>` is `read_current_machine` then
`save`; `snapshot -o -` is `read_current_machine` then `serialise`.
`parse_capture(reading)` types that dict and `build_from(reading)` turns it into an
inventory, so a capture already in memory never has to reach a file.
`current_platform()` names the reader this machine has. `SCHEMA_VERSION` and
`OLDEST_READABLE_SCHEMA` are the capture version this build writes and the oldest
it still reads, which is what tells you whether an archived capture will replay
before you try it.

The package's own `__all__` holds `get_config` and `print_info`, which are the
configuration loader and the `info` command's printer; neither is what you want
for hardware. Reading a machine needs privileges exactly as the CLI does, and
`snapshot.load` needs none. Run `lsdsk --help` and
`lsdsk <command> --help` for current options rather than trusting a list here.

The global options are `--replay`, `--profile`, `--history-file`,
`--no-record`, `--expand-virtual`, `--tree-density`, `--traceback`, `--env-file`,
`--version` and `--set SECTION.KEY=VALUE`, the last being how you move a
judgement for one run. Four also work after the subcommand: `--replay` on any
command that reads a machine, `--profile` on the `config` commands,
`--expand-virtual` on `topology`, `disks` and `tui`, and `--tree-density` on
`topology` alone - given globally it reaches every view that draws the fabric,
including a bare `lsdsk`. Every other global option is refused after the
subcommand with exit `2`.

The figures the rules turn on are all seven `[thresholds]` keys, so none of them
is fixed: `wear_warning_percent` 80, `wear_critical_percent` 95,
`crc_errors_significant` 100 (below it a CRC count is a hint), `quiet_expected_min`
10.0 (the line the whole "were due" idea rests on: fewer expected than this and
the tool refuses to call a counter quiet), `wear_projection_min_points` 2 (wear is
an integer, so one point is one unit of resolution and a rate from it is noise -
under this much measured movement no wear-out date is projected), `min_span_hours`
1 and `mixed_firmware_threshold` 2. Override one for a run with
`lsdsk --set thresholds.crc_errors_significant=10 findings`, or permanently by
editing the deployed `config.d/60-thresholds.toml`.

Exit codes: `0` nothing actionable, `1` a warning or critical. Hints never set a
non-zero code; a hint is a ceiling, not a fault.

**Only the eight section commands, `report` and bare `lsdsk` set `0`/`1` from findings.**
`record`, `snapshot` and the `config-*` commands exit `0` on success whatever the
hardware says, so never read their code as a verdict about the machine. They are
not always `0`, though: one that cannot write what it was asked to write leaves
`13` when it lacked permission and `74` for any other reason, with one stderr
line saying which. `record` also leaves `78` when the counter-history store it
would add to cannot be read, because it keeps that store rather than replacing
it and the record has stopped growing, and `1` when it could read no drive's
power-on hours at all, so there was nothing to store. For `record`, which prints nothing at all
in human mode when it succeeds, that code is what a timer reads. Neither an
internal error nor a failed write is one of the things `1` can mean: a crash leaves `70` and output
that could not be written leaves `74`, so a check can act on `1` as a verdict
without reading stderr first to find out whether the tool merely broke or its
output never arrived. A crash
writes no failure envelope of its own, because the handler that answers it never
reads `--format`: the exception goes to stderr in both modes and stdout holds
nothing, or a truncated report if the crash landed mid-write.

| Code  | Means                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `0`   | A reporting command found nothing actionable. `record`, `snapshot` and `config-*` exit `0` on success regardless                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `1`   | A reporting command found a warning or a critical. NOT a crash - that is `70` - and NOT a write that failed - that is `74`. From `record`, which reports no findings, it means no drive's power-on hours could be read, so nothing was stored                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `2`   | The command line was wrong. `USAGE_ERROR` in the envelope. See below, this one is misread constantly                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `13`  | Something needed privilege this run lacks: `config-deploy --target app` or `host` without root, a diagnostic run whose hardware read the kernel refused outright, or a `snapshot`, `record` or `config-generate-examples` whose destination refuses to be written. A field that merely could not be read is different - it degrades to `-` and names itself in `skipped`                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `22`  | `lsdsk config --section` named a section that does not exist, a `--profile` was rejected, `snapshot` was given a global `--replay`, or `-o -` together with `--format json` (the capture and the envelope would both be stdout) or while the logging console writes to stdout too, or `--format` was given to `report` or `tui`, which draw a page for a person - `findings --format json` is their machine-readable form - or `tui` was run where stdin, stdout or (on Linux and macOS) stderr is not a terminal. `--set SECTION.KEY=VALUE` is a different option and is not what produces this                                                                                                                                                                                                                                  |
| `70`  | An error inside `lsdsk` itself: an exception no command handled. A bug to report and never a statement about the machine, so route it to whoever owns the tool rather than to storage. An unhandled `OSError` keeps its own code instead, because its errno means something - EPERM is itself `1`; a write that fails is `74`, not its errno                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `74`  | A write this tool was asked to make failed for a reason other than permission - a full disk, a path that cannot exist: a `snapshot` destination, the counter-history file `record` writes, the files `config-deploy` or `config-generate-examples` writes, or - for a command whose output IS standard output - standard output refusing it or closed (`lsdsk findings > /full/disk/report.txt`, `lsdsk findings >&-`). `snapshot -o <file>` needs no standard output and succeeds without one; when standard output refuses the line reporting the capture, the run leaves `74` although the capture landed, and that line says so: `wrote the capture to <file>, but standard output refused the line saying so`. Never a verdict about the machine - some output did not arrive. One stderr line names the destination and why |
| `78`  | A configuration file this tool cannot load, such as malformed TOML in `config.d`; a file that is not a snapshot this version reads; a counter-history store `record` cannot read, which it keeps untouched and adds nothing to; or a platform with no hardware reader                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `141` | The process reading the output closed the pipe before the command finished. Neither a verdict nor a refusal; see the ranking below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

**`2` does not mean the file was missing.** It is the CLI framework's usage
error and an absent `--replay` path is only one of its causes: an unknown
option, an unknown command, a missing required argument, an invalid `--format`
value, a `--history-file` that exists but cannot be opened (a store whose CONTENT is
wrong is a different thing: it warns and the run continues), a malformed `--set`
and a
`--history-file` or `--no-record` placed after the subcommand all produce it
too. A wrapper that reads `2` as "the capture is
absent" will page whoever owns the capture pipeline when the actual fault is a
typo in the wrapper's own command line, and will keep doing so until somebody
reads the message on stderr. Read that message before concluding anything; it
names which it was.

**A usage error answers in JSON too, when the command line asked for it.**
`lsdsk disks --bogus --format json` writes one object on stdout and exits `2`:

```json
{"ok":false,"command":"disks","error":{"type":"USAGE_ERROR","message":"No such option '--bogus'."}}
```

with the framework's own usage text on stderr, where it does not disturb a
parser. The parser refuses before any command callback runs, so there is no
`--format` value to consult and the intent is read from the command line itself:
`--format json` anywhere before a bare `--` gets the envelope, and anything
ambiguous gets none. `error.type` is always the exit code's own name, so
`USAGE_ERROR` is `2`, `PERMISSION_DENIED` is `13`, `INVALID_ARGUMENT` is `22` and
`CONFIG_ERROR` is `78`; a caller may branch on the name or on the code and the two
cannot disagree.

**A failed write is reported as a SKIP, not as an error, because the command
still did something.** `lsdsk record --format json` whose store cannot be written
exits `13` (`74` when the cause is not permission) and still prints its action
envelope - `ok` false, `recorded` false, `data` naming the store and how many
drives were read, and the refusal as a sentence in `skipped` - rather than the
`error` object above. A store `record` cannot read answers the same way at `78`.
A run with nothing new to store, because no drive's power-on hours have advanced
since the last reading, is healthy: exit `0`, `ok` true, `recorded` false and
`skipped` empty. A run that could read NO drive's power-on hours - every SMART
reading refused, typically because it ran without root or Administrator - stored
nothing, and will store nothing until it can read one, so it is not "nothing new": exit `1`, `ok` false,
`recorded` false, `outcome` `no drive readable`, and the reason in `skipped` and
on stderr. In every case
`data.outcome` names what happened: `recorded`, `nothing new`,
`no drive readable`, `store not readable`, `not permitted` or `could not write`. So a
caller reading `error.type` alone sees nothing here: read `ok` first - false
means the record has stopped growing - then `data.outcome` and `skipped` for why.

**`141` is what a departed reader leaves, and which code wins does not depend on
the format.** `lsdsk findings ... | head -5` leaves `141` rather than the verdict
it reached, because a verdict that was not delivered is not a verdict: leaving `1`
there would tell a monitoring check it had a complete answer when it had five
lines of one. So `0` and `1` yield. A refusal is the other way round - `2`, `13`,
`22` and `78` stand whoever was reading, because there was never any output for
that reader to lose; an unknown option is an unknown option whether it went into
`head` or into a file, and `lsdsk disks --bogus | head -c 0` duly leaves `2` -
read through `${PIPESTATUS[0]}` or under `set -o pipefail`, because a bare `$?`
after a pipe is the READER's status and reports `head` succeeding whatever
`lsdsk` left. `70`
stands too, for its own reason rather than that one: a crash says nothing about
what the output CONTAINED, so the reason a verdict yields does not reach it, and a
check piping `lsdsk` into `head` or `jq` reads the crash rather than its own reader
leaving. The one crash that does NOT leave `70` is the one the departed reader
CAUSED - a failed write raises a broken pipe, which carries its own code, so that
leaves `141`. `74` stands as well: a write the destination refused is a fact about
the destination, whoever was reading. Both halves hold identically in human and
`--format json` output, which is the point of them: an exit code that changed with
the output format would be useless to a wrapper that uses both.

That ranking is about a code the run DECIDED. A command already writing when the
reader leaves exits `141` at that failing write, before it has decided anything -
so `lsdsk config --section nosuch` piped into a reader that has gone leaves `141`
and not `22`, because it prints the configuration before it discovers the section
is missing. Judge a command line by running it with its output going somewhere
that stays.

Do not parse what did arrive, either. Whether any of the output reached the
reader before the pipe closed is a question about buffering rather than about the
command, so a run that leaves `141` may have delivered a whole document, half of
one, or nothing at all. `141` means "what you asked for was not delivered"; the
only sound response is to run it again somewhere the output survives.

**The exit code can fall from `1` to `0` with the hardware untouched**, and if
somebody alerts on it they need to know. Two ways. A fault the recorded history
proves is over is downgraded to a hint, and a hint is not actionable, so a host
whose only complaint was a dead cable fault goes quiet - correctly. And an
unprivileged run reads no SMART at all, so the findings are never raised in the
first place; that one is a blind run, not good news. Tell them to pin the
privilege level and read the header for `-` columns rather than trusting `0`.

**An ELEVATED run writes to disk.** Reading the counters needs root, so an
unelevated run records nothing at all and its store never appears. A run that
can read them records every drive it read, owner readable only and capped per
drive (`history.max_samples_per_drive`), and only when some drive's own clock -
its power-on hours - has moved on since the last one. That covers the drives
whose own clock stood still too, and such a drive has its newest row REPLACED
rather than gaining one: two readings inside one power-on hour hold one hour of
information. So the store does not grow a row per drive per run, and a drive's
newest row is always its latest reading. That is what makes `lsdsk trend`
possible.

**Where it lives depends on who is running.** A root run on Linux or macOS uses
`/var/lib/lsdsk/history.json`; anyone else gets the per-user state directory:
`$XDG_STATE_HOME/lsdsk/history.json` or `~/.local/state/lsdsk/history.json` on
Linux, `~/Library/Application Support/bitranox/lsdsk/` on macOS,
`%LOCALAPPDATA%\bitranox\lsdsk\` on Windows. Reading
the counters needs root, so on a server it is the ROOT path that fills while the
per-user one stays empty. When a store is refused it is therefore
`/var/lib/lsdsk/history.json` you move aside on a server. The two paths are
separate files, so an unprivileged run neither reads nor is refused by the root
one; it has its own, which stays empty because recording needs root. `lsdsk record --format json` prints the path this run resolved, under
`store`.

A REPORTING
command does not write when replaying somebody else's snapshot or when
`--format json` is asked for. Global `--no-record` turns it off and
`--history-file` moves it; both go before the subcommand. `--no-record` still
*reads* the history and still grades against it, so it suppresses the write
without blinding the verdict.

**`lsdsk record` is the exception, and a read-only pipeline must exclude it.**
Storing a reading is its entire purpose, so it writes even under `--replay` and
even under `--format json` - `lsdsk record --replay other.json` is how you fold
somebody else's capture into the history deliberately. It prints nothing in its
human form, which is what suits it to a timer, but `--format json` gives it the
same envelope every other command has, with `recorded`, `outcome`, `store` and
`drives` inside `data`.
So the rule is "a REPORTING command asked for JSON does not mutate state", not
"lsdsk does not mutate state": put `topology`, `disks`, `health`, `smart`,
`findings`, `slots`, `controllers` or `trend` in that pipeline, and leave
`record`, `snapshot` and the two `config-*` commands out of it, all four of
which write by design whatever `--format` says. `snapshot` also REFUSES a global
`--replay` with exit `22` rather than obeying it: it always captures the machine
it runs on, so there is no snapshot of somebody else's capture to take. Copy the
file instead. It refuses `-o -` with `--format json` at `22` as well, because the
capture and the envelope would both be stdout. `info` and plain `config` write
nothing either and are safe to include; of the three `config` commands, `config-deploy`
and `config-generate-examples` are the two that create files.

**A run that cannot READ the history will not WRITE it either, and says so.**
On stderr you get `Warning: ignoring counter history: <why>` followed by
`Not recording this run, so <path> is left as it is.` The causes are a store
belonging to a different hostname, one written by a newer lsdsk, one too large
to read, and one that is not valid JSON. Two things follow, and both matter to
whoever is paged. On a reporting command the hardware is still diagnosed and the
exit code still reflects the findings, so this is not a failed run. `record` is
the exception, because storing the reading is its whole job: it prints those
same two lines, then a third, `Error: left the existing store at <path> alone,
because it could not be read: <why>`, and leaves `78`. And the file is INTACT: nothing was overwritten, so there is
nothing to restore from backup, and the
counters simply stop accumulating until somebody acts. To resume recording,
move the file aside or point `--history-file` somewhere else - a renamed host
is the common cause, because the default path carries no hostname.

Topology, link speeds, capacity and firmware read unprivileged. It never guesses
a value it could not read, so anything below shows `-` instead, and the header
says so.

Four things need root or Administrator, not one:

| Needs privilege                         | Because                                   | Costs you                                        |
|-----------------------------------------|-------------------------------------------|--------------------------------------------------|
| SMART attributes and wear               | ATA and NVMe passthrough ioctls           | Those columns, and every finding drawn from them |
| Error counters, so `trend` and `record` | Same passthrough read                     | An unelevated run records nothing at all         |
| PCIe slot numbers, connector detection  | Config space past the first 64 bytes      | The `slot` column, `FREE`, and any card move     |
| The AHCI ports-implemented bitmap       | A memory mapping of the controller's BAR5 | A SATA controller's free-port count              |

The last one is refused on some hosts even as root, so a `-` there is not proof
the run was unprivileged.

**Root does not always help.** In a container the device nodes do not exist, so
elevating changes nothing. Check what kind of machine you are on before
arranging access you cannot use.

**On Windows a port's own speed and width are not a privilege question.** Windows
publishes link registers for PCIe endpoints and none at all for bridges, so a
port's `capable` and `running` columns stay `-` and `upstream` stays null however
the run was started. Measured on one board: eight bridges, not one with a link
speed, and no registry key, WMI class or user-mode API that has them. Never tell
a Windows user to re-run elevated to reveal a port's capability - they will come
back with the same `-` and think something is broken.

**An unprivileged run that reports nothing is not a clean bill of health.** It
never read SMART, so those findings were never raised. That is a blind run, not
a quiet one.

## Check what kind of machine you are on first

The banner says so, and it changes the whole reading:

- **Bare metal.** Everything applies.
- **A container.** The disks and controllers shown belong to the host, seen
  through a shared kernel. The faults are real and worth reporting, but they are
  the host's faults, so investigate and act there. Health data is usually absent
  because the device nodes do not exist in the container, and elevating does not
  change that.
- **A virtual machine.** The disks, controllers and link speeds are the
  hypervisor's invention, so the link and placement rules are suppressed
  entirely: a cable warning about an emulated controller is noise. Health data
  can still be real if a device was passed through. Diagnose the host.

A container or a guest adds a caveat line under the banner; **bare metal adds
nothing**, so silence is the bare-metal answer rather than a missing check.
`--format json` states it outright in `data.environment`, one of `bare_metal`,
`virtual_machine`, `container` or `unknown`, with `data.environment_detail`
naming the hypervisor. Treat `unknown` as "not established", not as bare metal.

Never carry a link or placement recommendation from a guest to the host. Run it
on the host.

## A count is not a rate. Run `lsdsk trend` before advising anything

**Every error counter is a lifetime total held in the drive's own non-volatile
table.** It survives reboots, power cycles and reinstalls, and the host cannot
clear it. So a large number tells you how much damage there has ever been and
nothing at all about when. A fault that ended two years ago and one corrupting
data right now produce the same figure.

`lsdsk trend` is the answer, and it answers today:

```bash
uvx lsdsk trend
```

```
device        counter           total  change  span  per hour  verdict
/dev/sdd      interface CRC   2196127  +16642   15h      1109  rising
/dev/sde      interface CRC       430      +0   15h         -  too soon to say, this drive's rate would not have produced even one in 15h
/dev/sdj      interface CRC    462640      +0   16h         -  no new in 16h, 235 were due
```

`sdd` and `sdj` are the same drive model on one host with comparable totals.
`sdd` is failing now. `sdj` is a cable somebody already reseated. **Never send
somebody to reseat a cable for a `no new` row** - the fault is over, and the
work fixes nothing.

Rates are per power-on hour of the drive, not per hour of wall clock, so they
hold on a machine that is mostly switched off.

**`trend --format json` does not carry the trend.** Every reporting command
returns the same machine-wide envelope, and none of its fields is the verdict,
the rate or the `were due` figure - those exist in the human table only. A
rising counter reaches JSON only where it also produced a finding, inside that
finding's `detail`. Drive an automated decision from `findings`, and read the
human table when you need the rate.

`trend` says what is moving; `lsdsk findings` says how bad it is and what to do,
already graded by the same history. Pair them: pick the drive from `trend`,
quote the remedy from `findings`. When several drives are rising and only one
can be fixed now, rank by the rate, not by the total.

**Read the refusals as refusals.** `too soon to say` is not `no new`. Silence
counts only where the drive's own lifetime rate says errors were due in that
span, which is what the `were due` figure is: 235 expected and none seen is
evidence, while a rate that would not have produced even one is nothing. Below
one expected the row says exactly that in words instead of a figure, because
"only 0.0 were due" would contradict its own number. Do not upgrade a `too soon
to say` into an all-clear.

There is deliberately no fixed waiting period to quote, because the right one
differs per drive: a drive erroring a thousand times an hour proves itself quiet
within hours, and one at 0.04 an hour would need months. Quote the row's own
`were due` figure, or its sentence where the expectation is below one, instead of
inventing a window.

`counter reset` means the current total is BELOW what was recorded, which a
drive's own counter cannot do. The drive was swapped in that bay, its identity
changed, or the store belongs to other hardware. The rate is discarded; treat
the count as a first sample and check which drive you are looking at before
acting on it.

`first sample` means one reading exists. Say so and give the date a comparison
becomes possible; do not turn a single reading into a replacement decision.

**To get an answer the same day**, sample a few hours apart rather than waiting
for a daily job: a reading is only stored once the drive's own clock has moved
on, so runs minutes apart add nothing. Counters need root, so a run that is not
elevated records nothing at all.

A snapshot is still how you inspect a server from your desk or attach a
reproducible state to a bug report, and `lsdsk record --replay` folds one into
the history. Snapshots and the history store both contain every drive's serial
number and the machine's hostname, so either one identifies the machine it came
from.

```bash
uvx lsdsk snapshot -o /var/lib/lsdsk/$(hostname)-$(date +%F).json
```

`-o -` writes the capture to stdout rather than a file, so a server's capture
comes to your desk in one line and no copy is left on the server; the notice
about serial numbers still goes to stderr. Only the bare dash means stdout -
`-o ./-` writes a file named `-`.

```bash
ssh host.example lsdsk snapshot -o - > capture.json
lsdsk --replay capture.json
lsdsk --replay <(ssh host.example lsdsk snapshot -o -)   # replay without keeping a file
```

**Keep stderr off the redirect.** The serial-number notice is written to stderr,
so `2>&1`, `&>` or `ssh -t` - a pseudo-terminal carries both streams as one -
writes it into the file, and `--replay` then refuses that file at `78` as not a
snapshot. Use plain `ssh` and a plain `>`.

**A redirected capture gets your shell's umask, not `lsdsk`'s mode.** `-o <file>`
writes the capture owner-only (0600) because it holds every drive's serial
number; with `-o -` the shell creates the file, usually readable by everyone.
Run `umask 077` first, or write to a file with `-o`.

**A capture saved on Windows loads.** PowerShell 5.1's `>` writes UTF-16 with a
byte-order mark and `Out-File -Encoding utf8` writes UTF-8 with one; `--replay`
decodes a capture by its own mark, so either replays like any other.

## Reading a finding

Each disk row carries three speeds: `port` is what the seat can give, `disk` is
what the drive can do, `link` is what they agreed on. The structured output
splits them by transport: a SATA or SAS drive carries `link.negotiated_gbps`,
`link.drive_max_gbps` and `link.port_max_gbps` in Gbit/s with `pcie` null, while
an NVMe drive leaves that triple null and carries `pcie` instead, whose
`current_speed_gtps` and `max_speed_gtps` are GT/s where 2.5=Gen1, 5=Gen2,
8=Gen3, 16=Gen4, 32=Gen5, 64=Gen6. Reading a SATA 6.0 as GT/s yields a
generation that does not exist. Compare them to find the constraint. An orange `disk` means the drive cannot use its port, a placement
question rather than a fault; a red `link` means both ends could have gone
faster, which is a real one. A **yellow `link`** is a shortfall with only ONE end
measured: real, but not yet attributable, so establish what the port can carry
before touching a cable - this is what an unprivileged run and a legacy bridge
both produce. A **yellow `port`** means the seat is the slower of the two, so
the drive is fine and the port is the constraint. Markers repeat every finding
for readers without colour: `~` hint, `!` warning, `!!` critical.

**Five rows move with the recorded history and the rest are fixed.** Interface
CRC errors and the three sector counters plus media errors are the ones the
history regrades, by at most one step in either direction: a count proved to be
climbing is escalated and one proved to be over is stood down. Everything else
is decided by rule, including wear, which crosses from warning to critical at
its own threshold and not because of anything recorded. Either way read the
marker on the finding in front of you, which is what set the exit code.

| Finding                                                             | Means                                                                                                                             | Do                                                                                                                                                          |
|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Link below what both ends support                                   | Cable, backplane slot or connector                                                                                                | Reseat, swap cable, try another bay, before suspecting the drive                                                                                            |
| Runs below its own maximum, port not measured                       | ONE end was read. Real shortfall, cause unknown                                                                                   | Recommend nothing physical. Read `upstream_name`, then the board manual. See below                                                                          |
| In a slot narrower or slower than it needs                          | A better slot exists, and the drives on it would use it                                                                           | Move it; check the slot is mechanically long enough or open-ended                                                                                           |
| Has a faster slot free, though nothing on it needs one today        | A better slot exists, and the drives on it fit the one it has                                                                     | Move nothing yet. The detail says what the drives pull; the slot is named for when more are added                                                           |
| Could swap into a faster slot, though nothing on it needs one today | A swap would help, and the drives on it fit the slot it has                                                                       | Swap nothing yet. The swap is named for when more drives are added                                                                                          |
| Capped by the mainboard                                             | This port is the limit, not the card                                                                                              | Check `lsdsk slots` before proposing hardware. See below                                                                                                    |
| Held back by its controller                                         | The port is slower than the drive                                                                                                 | Move to a free faster port, or a better HBA                                                                                                                 |
| Drives in the wrong ports                                           | A slow drive holds a fast port a faster drive wants                                                                               | Swap the two drives over                                                                                                                                    |
| On the USB 2 side of a USB 3 port                                   | A USB 3 drive came up at USB 2 speed in a socket that has a USB 3 side                                                            | A USB 3 cable, seated fully, with no USB 2 hub or extension in between                                                                                      |
| USB link below what both ends support                               | Drive, port and any hub above it were all read: the cable, a hub or the plug                                                      | Reseat the plug and try another cable before suspecting the drive                                                                                           |
| Can do more, but its port or a hub only offers less                 | The port, or a hub in between, is the ceiling - not the cable. A hint when the drive behind the bridge could not pull more anyway | A faster port, or connect it directly or through a faster hub. Nothing to reseat                                                                            |
| USB below its own maximum, port not read                            | ONE end was read. Real shortfall, cause unknown                                                                                   | Recommend nothing physical. Establish what the port offers first; a USB port has no `upstream_name`                                                         |
| An attribute under the maker's threshold                            | The drive's own normalised value reached the limit it publishes                                                                   | Treat the drive as failing: check the backup and replace it                                                                                                 |
| Link never trained                                                  | The link is down, or negotiated to zero lanes                                                                                     | A seating, power or connector fault. Nothing behind it can be read                                                                                          |
| Reports itself as failing                                           | The drive's own overall SMART self-assessment says FAILED                                                                         | Treat it as failing now: check the backup and replace it                                                                                                    |
| Above its own temperature threshold                                 | Past the warning or critical limit the drive publishes                                                                            | Airflow and drive spacing. The bands are the drive's, not a fixed rule                                                                                      |
| Controller oversubscribed                                           | Its drives' links add up to more than the uplink figure, which can be a register default                                          | Check that figure before relaying it, and move a drive to a controller already fitted before any HBA. See below                                             |
| Publishes the PCIe floor as its link                                | An integrated function's register default, so not a ceiling                                                                       | Check the card's or board's specification for the real uplink; replace nothing on this figure. See below                                                    |
| Any other PCIe card: runs on fewer lanes than both ends support     | Card and port were both read and both support more lanes than trained: a contact, not the card's design                           | Reseat the card, check the slot and any riser. Not a storage finding: no cable, no bay. See below                                                           |
| Any other PCIe card: is capped by its slot                          | The card can do more than the port it sits in offers                                                                              | Move it to the free slot the action names; where it says that was not readable, re-run as root; where it names none, nothing on this board helps. See below |
| Wear-out                                                            | Rated endurance consumed                                                                                                          | Plan a replacement, see the thresholds below                                                                                                                |
| Reallocated sectors                                                 | Media degrading                                                                                                                   | Snapshot now, compare later                                                                                                                                 |
| Pending sectors                                                     | Unreadable, awaiting a write                                                                                                      | Back up first, then rewrite or replace                                                                                                                      |
| Uncorrectable sectors                                               | Data already lost                                                                                                                 | Replace, restore from backup                                                                                                                                |
| Media errors (NVMe)                                                 | Unrecovered integrity errors                                                                                                      | Snapshot now, compare later                                                                                                                                 |
| Interface CRC errors                                                | Frames corrupted on the wire, resent                                                                                              | Reseat or swap the cable; the drive is not at fault                                                                                                         |
| Mixed firmware                                                      | Same model, different revisions                                                                                                   | Level up at the next window                                                                                                                                 |

**A faster slot is graded by the drives on the controller.** lsdsk reports a move
or a swap as a warning only when the attached drives would use the faster slot,
and as a hint that still names the slot when they fit the one the controller
already has, so an empty controller or a pair of hard disks never reads as
urgent. A PCIe drive counts at what its link can carry, not at the speed it
rests at while idle.

**Every PCIe card no storage rule grades gets two hints of its own.** A graphics
card, a network card, or a switch or bridge carrying either is judged on its
link to the port above it, and only ever as a hint, so these never set a
non-zero exit code. They are not storage findings: the storage rows' advice
(cable, bay, drives, `lsdsk slots` before a new board) does not apply to them.
The title names the device at the card end of the link, which on a dual-GPU card
or a riser is its switch or bridge chip, followed by what it carries:
`<switch>, carrying 2x <graphics card>, is capped by its slot`. A link that only
runs SLOWER than both ends support is never reported, because graphics cards
lower their link speed while idle and retrain under load - read the running
column of `lsdsk topology` under load before calling that a fault. The capped
hint names a free slot only where the connector bits were read. It says "was
not readable" only where a free port that WOULD carry more had its own connector
bit unread, and it names that port: re-run as root on Linux, which is what tells
a slot from an internal port. Where no free slot would help, the action says so
and names the least port the card runs in full in - "a port of at least PCIe
Gen3x16" means any port at least that fast and that wide, not one particular
slot. On Windows neither hint appears: the platform
publishes no capability for the port above a card, and an unread end is never
graded.

**A USB disk is graded twice: its USB link by the four USB rows, and the drive
inside the enclosure on its own `link` by the other rows.** A USB figure is the
whole link, the lane rate times the lanes: `USB480M` is USB 2, any figure ending
in G is USB 3, and `USB10G` can be one 10G lane or two 5G lanes. Every column
and finding writes a figure with its bandwidth, which tells the two apart in
plain text - `USB10G (1.21 GB/s)` is one 10G lane, `USB10G (1.00 GB/s)` two 5G
lanes - and the `usb` object in the JSON names the lanes outright. The title says which USB row it is: "but both
ends support" means drive, port and every hub were read, "below its own" means
the port was not. The PCIe advice does not carry over: `lsdsk slots` lists PCIe
slots, not USB sockets, and `upstream_name` names a PCIe port only.

### The port was not measured

"runs below its own maximum, and the port was not measured" is a different
finding from the one below, and confusing the two is how somebody ends up
reseating a soldered-down drive. It means one end of the link was read and the
other was not, so the shortfall is real and its cause is unknown. A socket built
a generation below the device produces this reading exactly as a fault does.

Recommend nothing physical on it. No reseating, no cable, no bay, no slot-speed
override, and on Windows no elevated re-run - the port's registers are not
published there at any privilege (see above). Suggesting any of them asserts a
cause the tool explicitly did not establish.

**Read `upstream_name`, which is how this question usually closes.** It is what
the port is CALLED, carried because a platform can withhold a port's capability
and still name it. Many vendors put the width and generation in that name, so
`Intel(R) PCIe RC 060 (x4) G4` says Gen4x4 - and a Gen5 drive at Gen4x4 in a
Gen4 port is at its ceiling, with nothing wrong. Say where that came from: the
port's driver names it so, which is weaker than a measurement and strong enough
to act on. It is not parsed into a capability, and a name without numbers in it
tells you nothing - then send the reader to the board manual with the PCI
address.

`upstream_name` is not a column. It reaches a human reader only inside this
finding's text, as `The port is named "..."`, and a program reads it from any
controller's `--format json`. So a machine with no such finding shows it
nowhere, and asking a reader to look for a port column sends them hunting for
something that is not there.

**Two names, two sources, and only one of them follows the operating system's
language.** A CONTROLLER's name is resolved from its numeric PCI identifiers, so
it reads the same on every machine and always in English. The `upstream_name`
above is the exception: it is QUOTED from the platform, so on a German Windows
it arrives as `PCI-zu-PCI-Bruecke` and on an English one as `PCI-to-PCI Bridge`.
Nothing is misconfigured when one line is English and the other is not, and the
quoted name is still worth reading - it is the only statement about that port.

That also means lsdsk and the Windows Device Manager will disagree about what a
controller is called. Device Manager shows what the driver package calls it,
which for Microsoft's in-box drivers is a generic label like
`Standardmaessiger NVM Express-Controller`. lsdsk shows what the silicon is.
Same device at the same PCI address, named from different sources; match them by
ADDRESS, never by name, and do not tell anyone their machine is wrong.

**Width decides which way to lean.** A link at FULL width and lower speed is the
port's ceiling almost every time; seating and cabling faults cost LANES, so they
show as a width below maximum. Say which of the two you are looking at.

### Capped by the mainboard

The title names the port, not the board. Two different situations produce it and
they have opposite remedies, so read the finding's own detail before recommending
anything. It says which one this is.

- **The board has faster ports, but they are occupied.** The detail says so and
  names the generation, and the remedy is to free one. **Do not propose a new
  board**: the machine already has what the card needs. A Gen5 board with every
  Gen4 port full reads exactly like a Gen3 board until you read that sentence.
- **The board genuinely has nothing faster.** Only then name the PCIe generation
  it would need, not just "upgrade".

Either way, weigh it against demand first. When the attached drives want less
than the link carries, the ceiling costs nothing today: say that and stop. The
fix is never a new controller, which is already faster than the board.

Run `lsdsk slots` before answering. It is the only view that shows whether a
faster port exists and what is sitting in it.

### Controller oversubscribed

The finding offers two remedies and they are not equal. Look in `lsdsk
controllers` for a controller whose `load` is below what its `running` link
carries, because moving one drive onto hardware the machine already has costs
nothing, and a wider-uplink HBA is the last resort rather than the alternative.
A free port on an oversubscribed controller is not free.

**Having room in the uplink is not having somewhere to plug in.** A controller
showing no drives has spare bandwidth and may still have no port you can reach:
`ports` and `free` read `-` when the firmware did not publish the count, which
is unknown rather than zero. Confirm the destination in `lsdsk slots`, or name
the controller as a candidate and ask what is physically free, rather than
telling somebody to move a cable onto it.

**Check the uplink figure against something outside the tool before you relay
it.** The ceiling comes from what the controller's own PCIe link registers
publish, and some devices publish that register pair without having a link to
describe. The error only goes one way: the figure reads far too low, which turns
a working machine into a hardware recommendation.

Three readings say the figure is a register default rather than a data path, and
one of them is enough to stop:

- **The user measures more than the ceiling.** Ask for one throughput figure
  before recommending anything. A real ceiling cannot be exceeded. When you
  cannot get it in the same exchange, answer on the other two readings, give the
  command that would settle it, and say which answer each result would give.
- **`running` equals `capable` at the PCIe floor.** `Gen1x1` in both columns is
  the lowest value the pair can hold. A figure carries what it is worth where
  the width allows, so the reader may see `Gen1x1 (0.25 GB/s)`; match on the
  figure, which is there either way. Devices that negotiated a real link report
  a `capable` above their `running` wherever the two differ, so a device pinned
  at the floor in both has not negotiated anything.
- **A second function on the same silicon publishes the identical floor.** Run
  `lsdsk slots` and read the ports sharing the controller's upstream. A SATA and
  a USB controller both at `Gen1x1`, while the NVMe ports beside them publish
  Gen3, Gen4 and Gen5, is the discriminator. Those two are functions integrated
  into one chip; the others are ports that carry traffic. The floor value alone
  is not the discriminator, because a genuinely dead link reads the same. Nor is
  a second device at the floor on its own: a separate part, such as an onboard
  network controller, genuinely links at `Gen1x1`. `lsdsk slots --format json`
  carries `vendor` and `occupant_vendor` on every port, and a function built into
  the switch has the same identifier as the port in front of it, where a separate
  part has its own maker's.

**`lsdsk slots` lists PORTS, so its addresses are not the addresses in `lsdsk
controllers` and you have to join the two yourself.** Each row is a port, named
by the port's own address, with the device behind it in `occupant`. Ports on one
switch share a bus, so `0000:08:` in the port column is the group to read
together, but only when another row's occupant sits on that bus, because that
row is the bridge the bus hangs behind. Ports directly on a root bus share a
number too and are still independent slots. Do not match a controller to a row by eye: the occupant name comes
from the platform, so on Windows the row for a controller lsdsk calls an AMD 600
Series part reads `Standard SATA AHCI Controller`. `lsdsk slots --format json`
carries `occupant_address` on every port, and that IS the address in the
controllers table. Join on it.

That pattern is a desktop chipset used as a PCIe switch, which is how a
multi-drive expansion card is usually built. The card presents the chipset's
downstream ports, passes real links through to the M.2 sockets it wires, and
publishes the floor on the SATA and USB functions integrated into the chip. Its
real uplink is on the card's spec page, not in the register.

**lsdsk recognises the second and third readings itself** when the controller sits behind a switch: its own
link reads the floor in both columns, another function on that switch reads the identical floor, both carry
the vendor identifier of the switch ports in front of them, and a third device there has a real link. It
then reports the controller as publishing the PCIe floor, a hint, instead of calling it oversubscribed.
Where it cannot tell (no slot data, every link on the switch at the floor, a controller that sits on a root
port rather than behind a switch, or a device at the floor whose vendor is not the switch's) it still raises
the oversubscription warning, and the check above is yours to make.

**A controller row does not say whether it is a card or an onboard function, so
do not pass on "replace this card" as though it did.** Two readings in the same
output usually settle it. The banner names the board, and a chipset generation
that board cannot carry is on a card: a 600 Series SATA controller on a 500
Series board is not the board's own. `lsdsk slots` places it, by showing which
upstream it sits behind. When neither answers, ask what is plugged in rather
than naming a part for somebody to buy.

### Wear

Warning at 80% of rated endurance consumed, critical at 95%. Below 80% is not
flagged and is not a reason to replace anything: a drive at 59% has consumed
somewhat over half its rated writes and is not "wearing out" in any actionable
sense. Past 100% drives usually keep working; what ends is the warranty and the
manufacturer's prediction. Pair the percentage with lifetime bytes written to
estimate how long the rest will last at the current rate.

### CRC errors are about the cable, not the drive

The one health counter that says nothing about the media. Frames were corrupted
between the controller and the drive and had to be resent, which is a cable, a
connector or a backplane slot. Never recommend replacing the drive for it. SATA
also downshifts a link that keeps erroring, so a high CRC count beside a link
running below both ends is one fault showing up twice, not two problems. A
handful can come from a single hotplug; a persistent or rising count cannot.

The size of the count does not rank two drives. Check `lsdsk trend` before
recommending physical work on either: the bigger number is often the older,
finished fault. Where the record proves a count is still climbing, the finding carries the rate
and is raised one step - so a count below `crc_errors_significant`, which starts
as a hint, reads as a warning rather than a critical; where the record proves the
count is dead, the finding is downgraded to a hint and says so.

### Reallocated sectors and media errors

Different things. A reallocated sector was retired pre-emptively and the data
survived. A media error or an uncorrectable sector means recovery failed. A
non-zero reallocated count is common on old drives and is not by itself a
replacement trigger; growth is. Media errors and pending sectors are more urgent
because data was lost or is at risk.

There is no universal raw count that means "act now", and picking one is
guessing: what counts as many depends on the drive's spare pool, which differs
by model. The drive already publishes its own answer. Every SMART attribute
carries a normalised value and the threshold its maker set, both shown for every
disk on the SMART page of `lsdsk tui` and in `--format json`. Judge against those: a value
still far above its threshold is a drive reporting itself healthy however large
the raw count looks, and one approaching its threshold is the drive itself
saying it is running out of margin. Quote both numbers rather than the raw count
when you justify a replacement.

## Quoting a drive

Device names move between reboots, so a work order should quote the `wwn`
column, which is what the drive itself publishes: `naa.` for SATA and SAS,
`eui.` or a namespace `uuid.` for NVMe, and for an NVMe drive that offers
neither, the kernel's `nvme.<vendor>-<serial>-<model>-<nsid>` fallback. It stays with the drive into whatever
bay it lands in.

**Take it from `--format json`, not from the printed table.** The `wwn` column is
capped in both the printed table and the interactive page, because one NVMe
identifier runs to a hundred characters where the SATA ones beside it run to
twenty, and left uncapped that single drive pushes nine columns off the page. A
cut value is MARKED rather than shortened in silence, so a cut is visible if you
look for the marker - but a value copied out of piped output is a plausible
identifier that names no drive. `--format json` always carries the whole one, and
`lsdsk disks --full-wwn` prints it untruncated in the human table.

## Finding room, and what could move where

`lsdsk controllers` counts ports used against total per controller and what the
attached drives demand. Free ports on a controller whose uplink is oversubscribed
are not really free.

`running` and `capable` are the CONTROLLER's own PCIe link, negotiated and
maximum, never a drive's. `load` sums what the attached drives could pull at the
links they negotiated, so it is a capability total and not a measurement of
traffic: three SATA drives read 1.80 GB/s whether they are busy or idle. `load`
above what `running` carries is what raises the oversubscription finding.

A `-` in that count is not zero, and the reason differs by controller. A SAS HBA
always answers, because it publishes a phy per lane - though a phy is not a
connector, so read the caveat under `slots` before calling a free count free. An AHCI controller answers only
where firmware publishes its ports-implemented bitmap; where it does not, the
count is dropped rather than guessed, because the kernel's port list reports the
declared number and a chipset that declares six commonly wires two. An NVMe
controller has no spare port at all: it is the drive's interface, so a free-port
count would be a category error. When the count is absent, answer the question
from `lsdsk slots` instead, which shows the PCIe ports that are free.

`lsdsk slots` is the board-level view: every PCIe port, what it is capable of,
what it negotiated, what occupies it, what that occupant needs, and a verdict.

| Verdict                    | Means                                                                                                                                                                             |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FREE`                     | Empty, and the hardware confirmed a physical connector                                                                                                                            |
| `spare N GB/s`             | Occupied by a card that cannot use the port's full bandwidth                                                                                                                      |
| `port limits it`           | The occupant is faster than the port it sits in                                                                                                                                   |
| `full`                     | Occupant and port matched                                                                                                                                                         |
| `in use`                   | Occupied, and either the port's capability or the occupant's need went unread, so the two cannot be compared. The rule on Windows, which publishes no link registers for a bridge |
| `in use (graphics)`        | A graphics card. Never proposed for displacement                                                                                                                                  |
| `no connector`             | An internal port to a soldered-down device, not a slot                                                                                                                            |
| `empty, connector unknown` | Nothing there, and root was needed to tell whether it is a real socket                                                                                                            |

`spare` is a measurement and appears whether or not a move is possible, so it is
not on its own an instruction to swap anything. "Swappable" means the occupant
could take the slower slot without losing anything, which is why a card showing
`spare` is a swap candidate and a graphics card never is. A move additionally
needs a real connector at both ends and mechanical clearance, which is why an
unprivileged run never proposes one.

Read the two views together before moving anything. A `FREE` port is not by
itself a safe destination: check in `lsdsk controllers` that the controller
behind it is not already oversubscribed, or you move the bottleneck rather than
removing it.

Slot numbers and connector detection need root or Administrator. Without them the
`slot` column reads `-` and `FREE` is withheld, because an internal port to a
soldered-down device is empty in exactly the same way as a real socket.

## lsdsk does not go online. You can

Every limit below is the TOOL's, not yours. It reads hardware and makes no
network request by design, so it never reports a figure it did not measure. You
have a browser and `curl`, and the things it cannot know are published. Look them
up rather than reporting a dash back to somebody who asked a real question.

lsdsk gives you the exact search keys: the board name in the banner, from DMI;
the controller model in `lsdsk controllers`; the drive model and firmware in
`lsdsk disks`.

| Question lsdsk leaves open                                                                                    | Where the answer is                                          |
|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| How many SATA ports, how many M.2, which are Gen4 or Gen5                                                     | The board's spec page or manual                              |
| Whether slot #N is an M.2 socket or a card slot, and its silkscreen label                                     | The board manual's layout diagram                            |
| Which slots share lanes                                                                                       | The board manual, usually a footnote under the storage table |
| How many drives an HBA or RAID controller really drives, and whether its ports are direct or need an expander | The controller's product brief or datasheet                  |
| Whether a RAID controller is in IT/HBA mode or RAID mode, and what its cache and BBU do to write behaviour    | The controller's manual, then its own management tool        |
| A drive's rated endurance in TBW, to turn a wear percentage into a date                                       | The drive's spec sheet                                       |

Fetch it directly when you know the vendor URL, and search when you do not:

```bash
curl -sL https://vendor.example/products/motherboard/<board> | sed 's/<[^>]*>//g' | grep -iA3 sata
curl -sLI https://vendor.example/doc/<controller>-DS   # check it exists before fetching a large PDF
```

A web-search or fetch tool does the same job and handles PDFs better; use whichever you have.

**Lane sharing is the one worth looking up every time.** Boards routinely disable
SATA ports when an M.2 socket is populated, or drop a slot to x2 when its
neighbour is filled. That single footnote explains a whole class of lsdsk
findings: a port reporting fewer lanes than the slot is rated for, or SATA ports
that are simply absent. lsdsk sees the result and cannot see the cause.

**A SAS port count is phys, not connectors, so check it against the card.** The
count is the number of phy objects the driver publishes, which is right on many
cards and too high on some: a 9500-16i, a sixteen-lane card, publishes twenty-one
with no expander attached, so a free count derived from it overstates what you
can physically plug in. The model name usually carries the real number, and the
datasheet always does. Look it up before promising somebody free ports, and say
the count came from the card's specification rather than from the machine.

**Expect some vendor sites to refuse an automated fetch.** Supermicro and several
others answer 403 to `curl`. Do not quietly substitute a retailer listing and
present it as the manual: name the source you actually used, say the primary one
was unreachable, and hand over the URL so the reader can open it themselves.

**Keep the two apart when you answer.** Say which numbers lsdsk measured on this
machine and which you read from a manual, and cite the source. They fail
differently: a measurement is true of this box and a manual is true of the model,
so a board revision, a BIOS option or a populated shared slot makes them
disagree. When they do, lsdsk is usually describing what is actually there.

**Usually, not always: a specification or an independent measurement can REFUTE
a finding, not only supplement one.** lsdsk reports what a device PUBLISHES, and
a register that describes nothing is published exactly like one that describes a
link. So the arbitration has a direction. A ceiling cannot be exceeded, which
makes a measured throughput ABOVE one proof that the ceiling is not the path:
one number from the user, or one figure from a review of the same part, settles
it against the tool. A specification BELOW what lsdsk reports settles nothing on
its own, because that is what a downtrained or shared link looks like.

Reach for that test before relaying any finding whose remedy is to buy
something. Prefer the vendor's own page over a review or a retailer listing, and
say so when you had to settle for one of those.

## What it cannot tell you, so do not assert it

**It cannot tell an M.2 socket from a PCIe card slot.** No readable source gives
the form factor: the firmware slot table is the only one that carries it, and on
real boards it routinely lists no M.2 socket at all and names ports that do not
exist. Never infer the form factor from the width, because an x4 port is as
likely one as the other. `lsdsk slots` reports the board's own slot number
instead: match that against the mainboard manual, which is also how you turn a
PCI address into a slot you can point at.

**It cannot tell a card from an onboard function.** Nothing in a controller row
says whether the silicon is soldered to the board or sits on something
removable, so a remedy naming a card is a template rather than an observation.
See the oversubscription finding above for the two readings that usually settle
it.

It reads hardware, not configuration or physical layout. It does not know the
RAID or ZFS layout, which pool a disk belongs to, whether a drive is a boot
device or a cache, which physical bay holds it, how old a SATA drive is unless
it reports power-on hours, or whether newer firmware exists. It has no network
access, so it never knows a drive's rated endurance in terabytes written or an
OEM rebrand name. When a recommendation depends on any of those, ask rather
than infer, and map the device name to a bay before issuing a work order.
