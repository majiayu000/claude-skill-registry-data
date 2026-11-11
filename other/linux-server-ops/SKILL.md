---
name: linux-server-ops
description: "Audits and fixes Linux server resource pressure safely, with evidence. Covers full disks (ENOSPC, Errno 28), inode exhaustion, runaway logs, oversized journald, Docker images, volumes, logs and build cache, old kernels, package caches, core dumps, /tmp, memory and swap pressure, and runaway processes. Works read-only first, measures before and after, makes small reversible changes, never deletes data it cannot identify, asks before anything destructive, then adds prevention (logrotate, journald limits, Docker log options, alerts) and writes a short server report. Use when someone says \"disk full\", \"no space left on device\", \"Errno 28\", \"server is slow\", \"out of memory\", \"OOM killed\", \"what is eating my disk\", \"clean up my server\", \"docker is using all my space\" or \"load is high\"."
---

# Linux Server Ops

A full disk or a starved server usually has one boring cause: a log nobody rotates, a cache nobody prunes, a process that leaks. The real danger is the cleanup, like `docker system prune -a --volumes` on a live box deleting a database. This skill finds the cause with measurements, frees space in the safest order, and stops it coming back.

Commands target Ubuntu and Debian. Notes for RHEL-family, Alpine and Arch are in `references/commands.md`, which holds every copy-paste command this file refers to.

## What it does

1. **Inventory** the server read-only: disks, inodes, memory, swap, top processes, services, containers.
2. **Diagnose** what is actually growing and why, with numbers.
3. **Fix** in a fixed order, safest first, measuring each step. Anything destructive waits for a yes.
4. **Prevent** recurrence: rotation, size limits, alerts.
5. **Verify** services are healthy and write `SERVER-REPORT.md` from `templates/SERVER-REPORT.md`.

## Safety rules

- **Read-only first.** Inventory and diagnose change nothing. Some passive-sounding commands mutate: `npm cache verify` garbage-collects, `docker buildx du` can write config, and any `clean`, `prune`, `purge`, `gc`, `vacuum` or `autoremove` deletes. Keep those for the fix step.
- **Measure before and after every change.** The final `df` difference is the real result, not the sum of what you deleted (hard links, sparse files and other writers make them differ).
- **Never delete data you cannot identify.** If you cannot say what wrote a file, what reads it and how it would be rebuilt, it stays. Report it as "unknown, kept".
- **Always keep, unless the owner names the exact item:** databases and their WAL or journal files, Docker volumes, backups and snapshots, git repositories, user uploads and home directories, credentials and keys, anything under `/var/lib` that belongs to a running service, files under `/tmp` that are recent or held open.
- **Ask before destructive steps.** Show the exact command, paths, measured size and what is lost. A yes covers that bundle only.
- **Prefer reversible moves.** Truncate instead of delete, move instead of remove, disable a service before removing its unit, back up a config before editing it.
- **Do not kill what you do not understand.** Find the process's service and owner, and stop it through systemd rather than `kill -9`.
- **Lock-out safety.** Never change SSH, firewall or network config without a second way in (provider console or a second SSH path). Keep the current session open and test from a new one. Validate first (`sshd -t`, `nft -c`). No second path, no change: write it up instead.
- **Do not make it worse.** On a nearly full disk, install and download nothing during the audit.
- **Secrets stay secret.** Never print `.env` files, keys or credentialed unit files. Redact.

## Steps

### 1. Inventory (read-only)

Run the inventory block in `references/commands.md`: `df` in bytes and inodes (separate problems), memory and swap, top processes, failed units, `docker system df`, `journalctl --disk-usage`, and the timestamp. Write the numbers into the report's "Before" section straight away.

### 2. Diagnose

Work out which of these it is. More than one is common.

| Symptom | Likely cause | How to confirm |
|---|---|---|
| `df` at 100% | big files or directories | `du -x` by level, largest files list |
| `df` says full, `du` total is much smaller | deleted files still held open | `lsof +L1` |
| `df` has space, writes fail | inodes exhausted | `df -i` at 100%, count files per directory |
| `/var/log` huge | a log with no rotation, or a debug flag left on | measure the file twice 30 s apart for growth rate |
| `/var/lib/docker` huge | container JSON logs, dangling images, build cache, volumes | `docker system df -v`, per-container log sizes |
| `/var/log/journal` huge | no journald size limit | `journalctl --disk-usage` |
| `/boot` full | old kernels piling up | `dpkg -l 'linux-image-*'` vs `uname -r` |
| `/var/cache/apt` or `~/.cache` large | package caches | `du -sh` each |
| `/var/crash` or `/var/lib/systemd/coredump` large | crashing process dumping core | `coredumpctl list` |
| high load, slow, OOM in `dmesg` | a process leaking memory, too little RAM, no swap | `dmesg -T`, `journalctl -k`, RSS over time |

Rules for diagnosis:

- Use `du -x` so mounts are not counted twice. `du -d1 /` hides regular files directly under `/`; a swap file there is often the "missing" gigabytes.
- The largest file is not automatically the cause. A large database can be correct; an unbounded log or cache is the defect.
- Measure growth twice, do not guess it. Check whether a noisy log is the cause or a symptom of a disk that was already full.
- For memory, page cache is fine. "Available is low and swap is busy" is the problem, not "free is low".

### 3. Fix (safest first)

Go in this order and stop once there is comfortable headroom (at least 15% or a few GB free). Record bytes freed per step.

1. **Stop the bleeding.** Truncate a fast-growing file in place (`truncate -s 0 FILE`) once you know its producer. Deleting it frees nothing while the process holds it open.
2. **Deleted-but-open files.** Restart or reload the owning service. Ask first on production.
3. **Package caches.** `apt-get clean`; language caches only if nothing is mid-install.
4. **Journald.** `journalctl --vacuum-size=500M`.
5. **Rotated logs, core dumps, crash reports** past retention, after noting any crash in the report.
6. **Old kernels.** `apt-get autoremove --purge`, never the one from `uname -r`.
7. **Docker:** truncate oversized container logs, then dangling images, build cache, identified stopped containers. **Ask first** before `docker image prune -a`. **Never** remove volumes unless the owner names each one: that is where databases live.
8. **/tmp:** only files past a stated age, not open, from a producer you recognise.
9. **Memory:** restart a leaking process through systemd, cap it with `MemoryMax=`, or add swap if there is none. Do not disable the OOM killer.

If the disk is still full after the safe steps, more deletion is not the answer. Give the owner options with measured sizes: bigger disk, move data to another volume, or retire a workload.

### 4. Prevent

Add only what addresses the cause you found, and validate each config with its own checker. Snippets are in `references/commands.md`.

- **logrotate** for app logs without it. Test with `logrotate -d`.
- **journald limits** via a drop-in (`SystemMaxUse=`, `SystemKeepFree=`).
- **Docker log limits** in `daemon.json` (`max-size`, `max-file`). They only apply to new containers; existing ones need recreating (ask first) or a logrotate rule for their exact log paths.
- **Bounded scheduled cleanup**, e.g. weekly build-cache prune older than 7 days. No `-a`, no volumes in cron.
- **A disk alert** that is silent when healthy, checks block %, free bytes and inode %, and has a cooldown. Wire it to the notification channel you already use.
- **Core dump cap** with `MaxUse=`.

### 5. Verify

- Rerun `df -B1`, `df -i`, `free -h`. Report used-space reduction and available-space gain separately (on ext4 freed space refills reserved blocks first).
- `systemctl --failed` unchanged; healthy containers still healthy, same IDs unless recreated on purpose.
- No new "No space left on device" since the fix; the growth source measured again and stable.
- Every new config passed its validator; the alert is silent when healthy and fires on a forced test.

## Output

Fill `templates/SERVER-REPORT.md` (off the full disk if possible): a three-line summary (what was wrong, what was done, current headroom), before and after numbers, actions with bytes freed, what was kept and why, prevention added, and decisions waiting on the owner. In the chat, give only the summary, the before and after line, and pending yes or no questions.

## Honest limits

- Triage and hygiene, not capacity planning. If data is legitimately growing, the fix is more disk.
- Numbers are point-in-time; on a busy server they move while you measure.
- It cannot know your retention rules (compliance logs, audit trails). State them before cleanup.
- It does not tune databases (VACUUM, compaction). That needs the database's own tools and a maintenance window.
- Tested on Ubuntu and Debian; other distros get notes, not guarantees.
- With no backup and no second way in, it will tell you to fix that first and will refuse SSH or firewall changes.
