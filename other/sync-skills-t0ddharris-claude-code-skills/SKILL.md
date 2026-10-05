---
name: sync-skills
version: 1.0.1
description: "Sync Claude Code skills to Codex. Handles project-level (.claude/skills → .agents/skills) and user-level (~/.claude/skills → ~/.codex/skills). Trigger with /sync-skills or when the user mentions 'sync skills,' 'codex skills,' or 'sync to codex.'"
---

# Sync Skills

Synchronize Claude Code skills to Codex so both tools share the same skill library.

## Step 1: Ask Scope

Ask the user which sync to run:

- **Project** — Sync `.claude/skills/` → `.agents/skills/` in the current repo using hardlinks
- **User** — Sync `~/.claude/skills/` → `~/.codex/skills/` using copies with marker files
- **Both** — Run both syncs

If invoked from a session-start skill, default to **Project** without prompting.

## Step 2: Run the Sync

### Project-Level Sync

Hardlinks keep both paths pointing to the same file on disk, so edits in either location are instant. New or renamed skills need a re-sync.

Detect the platform first to use the correct stat command for inode comparison:

```bash
if stat -f %i / >/dev/null 2>&1; then
  inode_of() { stat -f %i "$1"; }
else
  inode_of() { stat -c %i "$1"; }
fi
```

Then sync:

```bash
SRC=".claude/skills"
DST=".agents/skills"

mkdir -p "$DST"

# Add/update: link any file in SRC that's missing or has a different inode in DST
# Exclude sync-skills itself — it's a Claude-only skill, not useful in Codex
cd "$SRC"
find . -type f -not -path './sync-skills/*' | while read -r f; do
  dst_file="$DST/$f"
  if [ ! -f "$dst_file" ] || [ "$(inode_of "$SRC/$f")" != "$(inode_of "$dst_file")" ]; then
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

Copies skills from `~/.claude/skills/` to `~/.codex/skills/`. Uses a `.synced-from-claude` marker file inside each synced skill directory to track provenance. Marker file approach borrowed from [ariccb/sync-claude-skills-to-codex](https://lobehub.com/skills/ariccb-sync-claude-skills-to-codex-sync-claude-skills-to-codex).

```bash
SRC="$HOME/.claude/skills"
DST="$HOME/.codex/skills"
MARKER=".synced-from-claude"

mkdir -p "$DST"

for skill_dir in "$SRC"/*/; do
  [ -f "${skill_dir}SKILL.md" ] || continue
  skill_name=$(basename "$skill_dir")
  # Skip hidden directories
  case "$skill_name" in .*) continue ;; esac
  # Skip symlinked SKILL.md files — these are managed by their installer (e.g. gstack)
  [ -L "${skill_dir}SKILL.md" ] && continue

  target="$DST/$skill_name"

  # If target exists without marker, it's a manual Codex skill — don't overwrite
  if [ -d "$target" ] && [ ! -f "$target/$MARKER" ]; then
    echo "SKIP: $skill_name (manual Codex skill)"
    continue
  fi

  # Copy and mark
  rm -rf "$target"
  cp -r "${skill_dir%/}" "$target"
  echo "$skill_dir" > "$target/$MARKER"
  echo "SYNC: $skill_name"
done

# Report any skills in DST with markers whose source no longer exists
for target in "$DST"/*/; do
  [ -f "${target}$MARKER" ] || continue
  skill_name=$(basename "$target")
  [ ! -d "$SRC/$skill_name" ] && echo "ORPHAN: $skill_name (source removed from Claude)"
done
```

Report what was synced, skipped (manual), and any orphans. Do NOT auto-delete orphans — flag them and let the user decide.

## Step 3: Summary

Show a short summary:

```
## Skills Sync Complete

### Project (.claude/skills → .agents/skills)
[X added, Y removed, Z unchanged]

### User (~/.claude/skills → ~/.codex/skills)
[X synced, Y skipped (manual), Z orphans]
```

## Rules

- Never delete manual Codex skills (those without `.synced-from-claude` marker)
- Never delete orphaned skills automatically — only flag them
- Use hardlinks for project-level (same filesystem, zero disk cost)
- Use copies for user-level (may be different filesystems)
- The `.synced-from-claude` marker contains the source path for traceability
- Skip symlinked SKILL.md files in user-level sync — these are managed by their own installer (e.g. gstack's `./setup --host codex`)
- Never sync the `sync-skills` skill itself — it's Claude-only and not useful in Codex
- Preview before mutating when the user asks for a dry run: report what *would* be added/removed (the same `+`/`-` summary) without running the `ln`/`rm`/`cp` operations, then wait for confirmation

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

