---
name: rollback
description: "Use when the user wants to undo Forge progress and return to an earlier checkpoint or phase. Triggers include \"rollback\", \"go back\", \"the earlier version was better\", \"go back to design\", and any request to restore a previous Forge tag safely."
---

<Purpose>
Rolls the project back to a previous phase using git tags created at each phase completion.
The client can say "The earlier design was better" and Forge rolls back to that point.
</Purpose>

<Use_When>
- Client wants to undo recent work: "rollback", "go back", "the earlier version was better"
- KO: "되돌려줘", "아까가 더 나았어"  JA: "戻して", "前の方が良かった"  ZH: "回滚", "之前的更好"
- A phase produced unsatisfactory results
- Need to restart from a specific phase
</Use_When>

<Steps>
1. List available rollback points:
   `git tag -l "forge/v*" --sort=-version:refname`
   Show to user:
   "Available restore points:
    - forge/v1-spec (Phase 1 complete — Spec)
    - forge/v1-design (Phase 2 complete — Design)
    - forge/v1-dev (Phase 3 complete — Development)
    - forge/v1-qa (Phase 4 complete — QA)
    Which point would you like to return to?"

2. User selects a tag

3. Confirm with user:
   "Rolling back to forge/v1-design means:
    - Work after Phase 3 will be reverted
    - Code changes will be rolled back
    - We'll restart from after Phase 2 (Design)
    Continue? (y/n)"

4. If confirmed:
   a. Save current state as backup tag: `git tag forge/backup-{timestamp}`
   b. Reset to selected tag: `git checkout {tag} -- .` (safe checkout, not hard reset)
   c. Update .forge/state.json:
      - Restore phase number from tag name
      - Set status to "active"
      - Clear tasks/holes that came after this phase
   d. Clean up worktrees from later phases
   e. Show: "Rollback to Phase {{N}} ({{phase_name}}) complete. Continuing from this point."

5. Invoke forge:continue to continue from the rolled-back phase
</Steps>

<Safety>
- ALWAYS create backup tag before rollback
- NEVER use git reset --hard (use safe checkout)
- ALWAYS confirm with user before executing
- Show exactly what will be lost
</Safety>

<Tool_Usage>
- Bash: git tag -l, git tag (backup), git checkout {tag} -- .
- Write: update .forge/state.json
- Skill: forge:continue after rollback
</Tool_Usage>
