---
name: ls-system-info
description: "Quick system diagnostics: CPU, memory, disk, uptime. Use when capturing server baseline or recording host layout and specs for further operations."
metadata:
  version: "1.1"
compatibility: "Linux: free, df, lscpu, uptime, ip, hostname, lsblk (or /proc); Python 3.12+ stdlib only for script. No sudo or extra packages."
---

# System info

Quick system diagnostics covering CPU, memory, disk, and uptime. Uses standard Linux utilities that are typically available. Use when you need a baseline snapshot of a server (layout, specs, installed software hints) to record for later operations.

## Commands

Run via your platform's command or terminal (e.g. shell tool, exec, or run command):

```bash
# CPU
lscpu
# or: cat /proc/cpuinfo

# Memory
free -h

# Disk
df -h

# Uptime
uptime
```

For a single combined snapshot, run in order: `lscpu`, `free -h`, `df -h`, `uptime`. Capture output to a file or paste into your baseline record.

## Extended snapshot (maximum context, no sudo)

To get maximum context without sudo or extra dependencies, use the bundled script. It uses only Python stdlib and commands/files readable by unprivileged users, with no network access. By default it writes only to stdout; `--output-basename` enables timestamped file output for unattended runs.

Choose the command for your current working directory. The repository-root examples apply to this document in the LocalSetup source checkout. Installed copies rewrite bundled paths; use the skill-directory examples there, from the directory containing this `SKILL.md`.

From the LocalSetup source repository root:

```bash
python3 ls/skills/ls-system-info/scripts/system_snapshot.py
```

From the skill directory (in the source checkout or an installed package):

```bash
python3 scripts/system_snapshot.py
```

Output is GFM markdown to stdout. It includes: identity and time, OS release, uptime and load, CPU, memory, disk and block devices, network (ip addr/route, resolv.conf), sessions (w/who), loaded kernel modules sample, and runtimes in PATH (e.g. python3, node). Redirect to a file to save a baseline, e.g. `... > baseline.md`.

For cron or unattended runs, set the job's working directory explicitly and write a timestamped markdown file with a relative output basename. From the LocalSetup source repository root:

```bash
python3 ls/skills/ls-system-info/scripts/system_snapshot.py --output-basename reports/system-snapshots/daily
```

From the skill directory (in the source checkout or an installed package):

```bash
python3 scripts/system_snapshot.py --output-basename reports/system-snapshots/daily
```

The output basename is relative to the process working directory, not the script location. These examples create parent directories as needed and write `reports/system-snapshots/daily-YYYYMMDDTHHMMSSZ.md` beneath the selected repository root or skill directory, respectively. Choose a writable working directory for unattended output. The script prints the written path to stdout and emits warnings to stderr when optional commands are unavailable or exit nonzero.

If you prefer not to run the script, you can run these manually (all no sudo):

- `hostname`; `uname -a`; `date -Iseconds`
- `cat /etc/os-release`
- `uptime`; `cat /proc/loadavg`; `cat /proc/uptime`
- `lscpu` (or `cat /proc/cpuinfo`)
- `free -h`; `cat /proc/meminfo`
- `df -h`; `df -i`; `lsblk -o NAME,SIZE,TYPE,MOUNTPOINT`; `cat /proc/partitions`
- `ip -br addr`; `ip route`; `cat /etc/resolv.conf`
- `w` or `who`
- `cat /proc/modules` (sample)
- `which python3 node`; `python3 --version`; `node --version` (if needed)

## Install

No installation needed. The quick commands use `free`, `df`, `uptime`, and `lscpu` (or `/proc`); the extended script uses Python 3.12+ stdlib only. If `lscpu` or `lsblk` is missing, the script retains its `/proc` fallbacks. To add an optional command, consult the target distribution's package metadata and obtain the required installation approval; do not assume a package named `util-linux` supplies it on every image. For example, Alpine lists separate [lscpu](https://pkgs.alpinelinux.org/package/v3.23/main/x86_64/lscpu) and [lsblk](https://pkgs.alpinelinux.org/package/v3.23/main/x86_64/lsblk) packages with `util-linux` as their origin.
