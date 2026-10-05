---
name: sync-skills
version: 1.0.0
description: "Sync skills between Claude Code and Codex runtimes. Handles project-level (.claude/skills ↔ .agents/skills) and user-level (~/.claude/skills → ~/.codex/skills or reverse). Trigger with /sync-skills or when the user mentions 'sync skills,' 'codex skills,' 'update agents skills,' or 'sync runtimes.'"
---

# Sync Skills

Synchronize skills between Claude Code and Codex so both runtimes share the same skill library.

## Step 0: Detect Primary Runtime

Read `.compound-marketing.yml` in the repo root. The `primary_runtime` field (`claude` or `codex`) determines sync direction:

- **claude** (default): `.claude/skills/` → `.agents/skills/`
- **codex**: `.agents/skills/` → `.claude/skills/`

If `.compound-marketing.yml` doesn't exist or has no `primary_runtime`, default to `claude`.

Set `SRC` and `DST` based on the primary:

```bash
CONFIG=".compound-marketing.yml"
PRIMARY="claude"
if [ -f "$CONFIG" ]; then
  PRIMARY=$(grep 'primary_runtime:' "$CONFIG" | awk '{print $2}' | tr -d '"'"'" || echo "claude")
fi

if [ "$PRIMARY" = "codex" ]; then
  SRC=".agents/skills"
  DST=".claude/skills"
else
  SRC=".claude/skills"
  DST=".agents/skills"
fi
```

## Step 1: Ask Scope

Ask the user which sync to run:

- **Project** — Sync `$SRC/` → `$DST/` in the current repo using hardlinks
- **User** — Sync user-level skills using copies with marker files
- **Both** — Run both syncs

If invoked from `/start`, default to **Project** without prompting.

## Step 2: Run the Sync

### Project-Level Sync

Hardlinks keep both paths pointing to the same file on disk, so edits in either location are instant. New or renamed skills need a re-sync.

```bash
mkdir -p "$DST"

# Add/update: link any file in SRC that's missing or has a different inode in DST
# Exclude sync-skills itself — it's runtime-specific, not useful in the secondary
cd "$SRC"
find . -type f -not -path './sync-skills/*' -not -path './setup/*' | while read -r f; do
  dst_file="$DST/$f"
  if [ ! -f "$dst_file" ] || [ "$(stat -f %i "$SRC/$f")" != "$(stat -f %i "$dst_file")" ]; then
    mkdir -p "$(dirname "$dst_file")"
    rm -f "$dst_file"
    ln "$SRC/$f" "$dst_file"
  fi
done

# Remove: delete anything in DST that no longer exists in SRC
cd "$DST"
find . -type f | while read -r f; do
  [ ! -f "$SRC/$f" ] && rm -f "$DST/$f"
done

# Clean up empty directories
find "$DST" -type d -empty -delete 2>/dev/null
```

Report what was added (+) or removed (-). If nothing changed, say so in one line.

### User-Level Sync

Copies skills between user-level directories. Direction follows the same primary logic:

- **claude primary**: `~/.claude/skills/` → `~/.codex/skills/`
- **codex primary**: `~/.codex/skills/` → `~/.claude/skills/`

Uses a `.synced-from-primary` marker file inside each synced skill directory to track provenance.

```bash
if [ "$PRIMARY" = "codex" ]; then
  SRC_USER="$HOME/.codex/skills"
  DST_USER="$HOME/.claude/skills"
  MARKER=".synced-from-codex"
else
  SRC_USER="$HOME/.claude/skills"
  DST_USER="$HOME/.codex/skills"
  MARKER=".synced-from-claude"
fi

mkdir -p "$DST_USER"

for skill_dir in "$SRC_USER"/*/; do
  [ -f "${skill_dir}SKILL.md" ] || continue
  skill_name=$(basename "$skill_dir")
  case "$skill_name" in .*) continue ;; esac
  [ -L "${skill_dir}SKILL.md" ] && continue

  target="$DST_USER/$skill_name"

  # If target exists without marker, it's a manual skill in the secondary runtime — don't overwrite
  if [ -d "$target" ] && [ ! -f "$target/$MARKER" ]; then
    echo "SKIP: $skill_name (manual skill in secondary runtime)"
    continue
  fi

  rm -rf "$target"
  cp -r "${skill_dir%/}" "$target"
  echo "$skill_dir" > "$target/$MARKER"
  echo "SYNC: $skill_name"
done

# Report orphans
for target in "$DST_USER"/*/; do
  [ -f "${target}$MARKER" ] || continue
  skill_name=$(basename "$target")
  [ ! -d "$SRC_USER/$skill_name" ] && echo "ORPHAN: $skill_name (source removed from primary)"
done
```

Report what was synced, skipped (manual), and any orphans. Do NOT auto-delete orphans — flag them and let the user decide.

## Step 3: Sync Instruction Files

After syncing skills, also sync the root instruction files if either has changed:

- **claude primary**: If `CLAUDE.md` is newer than `AGENTS.md`, regenerate `AGENTS.md` from it (swap title, swap `.claude/` → `.agents/` path references)
- **codex primary**: If `AGENTS.md` is newer than `CLAUDE.md`, regenerate `CLAUDE.md` from it (swap title, swap `.agents/` → `.claude/` path references)

Title swap: replace the first line's "Claude Instructions" with "Codex Instructions" or vice versa.

Path swaps:
- `/.claude/skills/` ↔ `/.agents/skills/`

## Step 4: Summary

Show a short summary:

```
## Skills Sync Complete

Primary runtime: [claude|codex]

### Project ($SRC → $DST)
[X added, Y removed, Z unchanged]

### User ($SRC_USER → $DST_USER)  (if run)
[X synced, Y skipped (manual), Z orphans]

### Instruction files
[AGENTS.md regenerated from CLAUDE.md | No changes needed]
```

## Rules

- Never delete manual skills in the secondary runtime (those without the sync marker)
- Never delete orphaned skills automatically — only flag them
- Use hardlinks for project-level (same filesystem, zero disk cost)
- Use copies for user-level (may be different filesystems)
- The marker file contains the source path for traceability
- Skip symlinked SKILL.md files in user-level sync — these are managed by their own installer
- Never sync the `sync-skills` or `setup` skills themselves — they belong to the primary runtime only
- Direction is always primary → secondary, governed by `.compound-marketing.yml`
