---
name: gs-unfreeze
version: 0.1.0
description: "Clear the freeze boundary set by gs-freeze, restoring edits everywhere. CARL TRIGGERS: unfreeze, remove lock, unlock edits, end freeze. SOURCE: garrytan/gstack/unfreeze, integrated as gs-unfreeze on 2026-05-29."
triggers:
  - unfreeze edits
  - unlock all directories
  - remove edit restrictions
allowed-tools:
  - Bash
  - Read
---

> INTEGRATION NOTE: Extracted from gstack and renamed gs-unfreeze (Phase 1B) to coexist with the host environment's CARL routing. Original gstack docs follow. Sibling gstack skills referenced below map to gs-* when installed (the 19-skill set); gstack-only infra (browse binary, gstack bin/ toolchain, ~/.gstack GBrain) is not installed here, so dependent steps degrade gracefully.

<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->


## When to invoke this skill

Use when you want to widen edit scope without ending the session.
Use when asked to "unfreeze", "unlock edits", "remove freeze", or
"allow all edits".

# /unfreeze — Clear Freeze Boundary

Remove the edit restriction set by `/freeze`, allowing edits to all directories.

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"unfreeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Clear the boundary

```bash
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
STATE_DIR="$GSTACK_STATE_ROOT"
if [ -f "$STATE_DIR/freeze-dir.txt" ]; then
  PREV=$(cat "$STATE_DIR/freeze-dir.txt")
  rm -f "$STATE_DIR/freeze-dir.txt"
  echo "Freeze boundary cleared (was: $PREV). Edits are now allowed everywhere."
else
  echo "No freeze boundary was set."
fi
```

Tell the user the result. Note that `/freeze` hooks are still registered for the
session — they will just allow everything since no state file exists. To re-freeze,
run `/freeze` again.
