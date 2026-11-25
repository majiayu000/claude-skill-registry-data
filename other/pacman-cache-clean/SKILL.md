---
name: pacman-cache-clean
description: Inspect and clean the pacman package cache on Arch Linux, keeping only the installed versions and removing stale partial-download dirs. Use when asked to "clean pacman cache", "free disk space from pacman", "paccache", "keep only used package versions", or invokes /pacman-cache-clean.
---

# Pacman cache clean

Reclaim `/var/cache/pacman/pkg` without deleting the versions currently installed.

## 1. Measure first

```bash
du -sh /var/cache/pacman/pkg
cd /var/cache/pacman/pkg && ls -1 *.pkg.tar.* 2>/dev/null | grep -vc sig; ls -1d download-* 2>/dev/null | wc -l
```

`ls | wc -l` lies: it counts `download-*` dirs and `.sig` files as packages. Split the count into real packages vs. stale download dirs — the download dirs are usually where the gigabytes are.

## 2. Dry run

```bash
paccache -dk1     # old versions of installed packages
paccache -dk1 -u  # cached packages no longer installed
```

`-d` is dry run and needs no root. Report the MiB each would free before touching anything.

## 3. Clean

`paccache -r` needs root, and `sudo` cannot prompt for a password from a non-interactive tool call. If `sudo -n true` fails, print the commands for the user to run instead of guessing:

```bash
sudo paccache -rk1                             # keep 1 (installed) version
sudo paccache -rk0 -u                          # drop cache for uninstalled packages
sudo rm -rf /var/cache/pacman/pkg/download-*   # stale partial downloads
```

## 4. Report

State the before size, what each step frees, and which step is the real win. Suggest `systemctl enable --now paccache.timer` only if the user wants it automated.

## Notes

- Never `pacman -Scc`: it empties the cache including installed versions, so downgrades stop working.
- `download-*` dirs are interrupted downloads. Safe to delete; pacman refetches.
