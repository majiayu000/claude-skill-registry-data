---
name: setup
description: This skill should be used when the user asks to "set up restic backups on a server", "install restic", "prepare a Linux server for backups", "check what arch/init system my server uses", or needs to recon a server (architecture, OS, init system, timezone, free disk) and install the correct latest restic binary before configuring backups.
---

# restic Setup — Server Recon + Install

The first phase of standing up backups: understand the server, then install a current `restic`. Recon decisions ripple into every later skill (which binary, systemd vs cron, which timezone, where the cache lives). Do this before `discover-backup-sources` and `repository-setup`.

## Step 1 — Recon the server

Run these read-only commands and record the answers:

```bash
uname -m                       # arch: x86_64 -> amd64,  aarch64 -> arm64
cat /etc/os-release | head -3  # distro + version
ps -p 1 -o comm=               # 'systemd' -> systemd timers; else cron
timedatectl 2>/dev/null | grep -i 'time zone'   # timezone for the schedule
df -h /                        # free space on root fs (restic cache lives in ~/.cache by default)
df -h "${HOME}/.cache" 2>/dev/null || true      # where the cache will actually grow
docker --version 2>/dev/null && docker compose version 2>/dev/null   # is this a Docker host?
free -h                        # RAM (prune/check are memory-hungry on big repos)
```

### Decision table (recon → choices made later)

| Recon result | Decision | Used in |
|--------------|----------|---------|
| `x86_64` | download `..._linux_amd64.bz2` | this skill |
| `aarch64` | download `..._linux_arm64.bz2` | this skill |
| `ps -p 1` = `systemd` | systemd timer | `scheduling` |
| `ps -p 1` ≠ `systemd` (e.g. container, OpenRC) | cron + `flock` | `scheduling` |
| timezone (e.g. `Europe/Kyiv`) | `OnCalendar`/`CRON_TZ` value | `scheduling` |
| little free space on `/` | set `RESTIC_CACHE_DIR` to a roomy fs | `repository-setup`, `troubleshoot` |
| docker present | run `discover-backup-sources` | `discover-backup-sources` |

Emit a **recon summary** block (arch / os / init / tz / free / docker yes-no) — the discover and scheduling skills consume it.

## Step 2 — Install the latest restic

**Do not `apt install restic`.** Distro packages are frequently older than 0.14, which means no repository-format v2 and **no compression**. Install the official binary from GitHub releases.

```bash
cd /tmp
# resolve the latest version tag from the releases "latest" redirect
ver=$(curl -fsSLI -o /dev/null -w '%{url_effective}' \
      https://github.com/restic/restic/releases/latest | xargs basename); ver=${ver#v}
arch=$(dpkg --print-architecture 2>/dev/null)
[ -n "$arch" ] || case "$(uname -m)" in x86_64) arch=amd64;; aarch64) arch=arm64;; *) arch=$(uname -m);; esac
curl -fsSL -o restic.bz2 \
  "https://github.com/restic/restic/releases/download/v${ver}/restic_${ver}_linux_${arch}.bz2"
bunzip2 restic.bz2
install -m755 restic /usr/local/bin/restic
rm -f restic
restic version    # expect >= 0.14 (compression / repo format v2); recommended >= 0.19.1
```

If `restic` is already installed, prefer `restic self-update` (needs write permission to the binary path). In production pin a version rather than auto-updating on a schedule.

**Recommended version: ≥ 0.19.1** (≥ 0.14 is only the floor for repo format v2 and compression). 0.19.1 restores the `snapshots --latest <n>` grouping that 0.19.0 dropped, makes `backup` skip inaccessible source paths, and refuses a `mount` over the repository directory. Mind the 0.19 behaviour changes before upgrading a scheduled host: `backup` exits 3 for a missing source path, `forget` exits 3 when it cannot remove a snapshot, and an invalid `RESTIC_COMPRESSION`/`RESTIC_PACK_SIZE`/`RESTIC_READ_CONCURRENCY` is fatal (see `cli-reference`, `backup-script`).

## Verification

```bash
restic version    # prints version, go version, arch — confirms it runs
command -v restic # /usr/local/bin/restic
```

## Gotchas

- **`aarch64` ↔ `arm64` naming mismatch** — `uname -m` says `aarch64`, but the release asset is `arm64`. The snippet above maps it.
- **Need ≥ 0.14** for compression and repo format v2 (target ≥ 0.19.1). An older binary silently creates a v1 repo with no compression.
- **restic cache disk pressure** — the local cache (default `~/.cache/restic`) can grow to gigabytes on large repos. If `/` is tight, plan `RESTIC_CACHE_DIR` on a bigger filesystem (set in `repository-setup`).
- **`self-update` needs write access** to `/usr/local/bin/restic` (run as root). It will not update a package-manager-managed binary in a system path it can't write.
- **`self-update` can hit a GitHub API rate limit (403 Forbidden) on a shared IP** — since 0.19.0 set `GITHUB_ACCESS_TOKEN=<personal access token>` for that one command (never in `r2.env` or git).
- This skill only recons and installs — it does **not** touch credentials or the repository. That is `repository-setup`.

## What this skill does NOT cover

- Deciding what to back up → `discover-backup-sources`
- Creating the password / R2 credentials / `restic init` → `repository-setup`
- Writing the backup script or schedule → `backup-script`, `scheduling`