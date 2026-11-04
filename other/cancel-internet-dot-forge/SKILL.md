---
name: cancel
description: "Use when canceling or cleaning up an active Forge project. Removes worktrees, clears state, preserves code already merged to main."
---

<Purpose>
Cleanly stops an active Forge project. Removes git worktrees, clears .forge/ state,
but preserves any code already merged to main branch.
</Purpose>

<Use_When>
- User says "forge cancel", "cancel project"
- KO: "포지 취소", "취소해줘"  JA: "キャンセル", "フォージ取消"  ZH: "取消", "锻造取消"
- Need to abort mid-project
- Need to clean up after a completed project
</Use_When>

<Steps>
1. Read .forge/state.json to understand current state
2. If not found → "No active Forge project to cancel."
3. Confirm with user:
   "Currently at Phase {{N}} ({{phase_name}}).
    Canceling will:
    - Delete .forge/ directory
    - Clean up active worktrees
    - Preserve code already merged to main
    Continue? (y/n)"
4. If confirmed:
   a. List and remove active worktrees:
      `git worktree list` → filter forge worktrees → `git worktree remove`
   b. Remove forge branches not merged to main:
      `git branch --list "forge/*" --no-merged main` → delete each
   c. Remove .forge/ directory
   d. Show summary: "Forge project canceled. Code on the main branch is preserved."
</Steps>

<Safety>
- ALWAYS confirm before deleting
- NEVER delete main branch or merged code
- NEVER force-delete branches that are merged
- If worktree removal fails, report error and continue with remaining cleanup
</Safety>

<Tool_Usage>
- Bash: git worktree list, git worktree remove, git branch -d
- Bash: rm -rf .forge/
- Read: .forge/state.json
</Tool_Usage>
