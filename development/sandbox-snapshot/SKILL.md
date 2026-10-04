---
name: sandbox-snapshot
description: Erstellt rotierende Verzeichnis-Snapshots (GreyHack-DB, Tool-Repos) mit rsync+hardlink und liefert einen Diff-Report für Änderungs-Detection. Trigger bei cron-gesteuerten Backups oder vor größeren Änderungen.
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
triggers:
  - cron: stündlicher/täglicher Snapshot-Run
  - pre-mutation: vor jedem großen Schreibvorgang (Build, Update, Reset)
  - manual: bei Bedarf via `snapshot.sh <dir>`
metadata:
  openclaw:
    tags:
      - filesystem
      - backup
      - greyhack
      - ops
---

# sandbox-snapshot

Rotierende, platzsparende Verzeichnis-Snapshots nach dem **rsync+hardlink**-Prinzip
(wie `snapper`/`timeshift`-Light). MaxClaw nutzt das, um GreyHack-Spielstände,
Tool-Repos und beliebige Workspace-Ordner ohne Deduplizierungs-Filesystem
rückwirkend wiederherstellbar zu halten.

## When to use

- **Cron-Trigger**: stündlich/täglich ein inkrementeller Snapshot von
  `~/.local/share/GreyHack/` und `~/maxclaw-tools/`.
- **Pre-Mutation**: vor `greybel build`, `git reset --hard`, DB-Migrationen
  oder Repo-Updates.
- **Recovery**: wenn ein Build rot, eine Config überschrieben oder ein
  Sandbox-Test das Repo zugemüllt hat → Snapshot zurückspielen.

## Pattern

### 1. Snapshot-Script (`scripts/snapshot.sh`)

```bash
#!/usr/bin/env bash
# snapshot.sh — rotierende Verzeichnis-Snapshots (rsync + hardlinks)
# Nutzung: snapshot.sh <QUELLE> [ANZAHL=24]
set -euo pipefail

SRC="${1:?Usage: snapshot.sh <source> [keep]}"
KEEP="${2:-24}"
NAME="$(basename "${SRC%/}")"
DEST="${SNAPSHOT_BASE:-$HOME/.local/share/maxclaw/snapshots}/$NAME"
mkdir -p "$DEST"

# neuester Snapshot als Referenz (Hardlink-Basis)
latest="$(ls -1dr "$DEST"/snap-* 2>/dev/null | head -1 || true)"
link_dest=()
[[ -n "$latest" ]] && link_dest=(--link-dest="$latest")

TS="$(date +%Y%m%d-%H%M%S)"
new="$DEST/snap-$TS"
mkdir -p "$new"

# Spiegelung; --link-dest macht unveränderte Dateien zu Hardlinks
rsync -a --delete "${link_dest[@]}" "$SRC/" "$new/"

# Alte Schnappschüsse außerhalb KEEP entfernen
mapfile -t old < <(ls -1dt "$DEST"/snap-* | tail -n +$((KEEP + 1)))
rm -rf "${old[@]:-}"
echo "snapshot ok: $new (behalte $KEEP)"
```

### 2. Diff-Engine (`scripts/snapshot-diff.sh`)

```bash
#!/usr/bin/env bash
# snapshot-diff.sh — Änderungen zwischen zwei Snapshots listen
set -euo pipefail
A="${1:?old-snapshot}"; B="${2:?new-snapshot}"
# rsync --dry-run + -i liefert pro Datei Status-Codes (cd>/.+ etc.)
rsync -anic --delete "$A/" "$B/" | grep -v '^\.' | head -200
```

### 3. Wiederherstellung

```bash
# Restore: Snapshot-Inhalt zurück nach $SRC
rsync -a --delete /path/to/snap-20260704-120000/ "$SRC/"
```

## Pitfalls

- ❌ **Pfad ohne Trailing-Slash** → rsync legt ein Unterverzeichnis an. Immer `"$SRC/"`.
- ❌ **Snapshots auf demselben FS wie Source** ist OK (hardlinks), aber **nicht
  auf einem Netz-Mount** — `--link-dest` wird dort zur Full-Copy.
- ❌ **Hardlink auf Filesystem ohne reflink** (ext4 ok, NFS nicht) — `--link-dest`
  funktioniert nur auf POSIX-Hardlink-fähigen FS; sonst wird's Vollkopie.
- ✅ `--delete` nur in der Spiegelung, **niemals** in der Restore-Richtung ohne
  Backup dahinter.
- ✅ `SNAPSHOT_BASE` als eigene Variable → Backup-Festplatte tauschen ohne
  Skriptänderung.

## Cron-Beispiel

```cron
# stündlich: Sandbox + GreyHack-DB
0 * * * * /home/bratan/.openclaw/skills/sandbox-snapshot/scripts/snapshot.sh \
    /home/bratan/.local/share/GreyHack 24
0 * * * * /home/bratan/.openclaw/skills/sandbox-snapshot/scripts/snapshot.sh \
    /home/bratan/maxclaw-tools 24
```