---
name: restore
description: 'Guided restore / disaster recovery from a restic repository Arguments: [--what <path>] [--snapshot <id|latest>] [--target <dir>].'
---

# restic Restore

Guided restore of files, volumes, or databases. Restore is destructive when applied in place — confirm before overwriting anything.

Parse `[--what <path>] [--snapshot <id|latest>] [--target <dir>]` from "$ARGUMENTS" (defaults: snapshot `latest`, target `/restore`).

## Process

Follow the `disaster-recovery` skill. For a full server rebuild, hand off to the `restic-backup-engineer` agent.

1. **Confirm access** — `set -a; . /root/.restic/r2.env; set +a` then `restic snapshots`. If the repo can't be read (no password / keys), stop and explain that recovery is impossible without them.
2. **Locate** — `restic ls <snapshot>` / `restic find <pattern>` to confirm what will be restored.
3. **Plan & confirm** — show the user exactly what will be restored and where. **Restore to a staging target by default** (`/restore`), not in place. Get explicit confirmation before any in-place / `--overwrite` restore.
4. **Restore files:** `restic restore <snapshot> --target <dir> [--include <what>]`.
5. **Restore a database** (if requested): stop app containers (not the DB), then `restic dump <snapshot> <dump.gz> | zcat | docker exec -i <db> ...` (see `disaster-recovery`).
6. **Verify** — `diff` a known file, check DB rows / app health. Report what was restored.

Never run `restic init` here — reconnecting to an existing repo uses `snapshots`, not `init`.