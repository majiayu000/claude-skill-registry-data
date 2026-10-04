---
name: board-status
description: Read-only progress snapshot of an AgentBoard workspace board — card counts per column, percent finished, blocking settings, cards needing attention, and recent activity, without resuming work. Use whenever the user asks how a board or orchestration is going, where a board stands, how many cards are left or finished, or wants a board snapshot — e.g. "board status", "how's the cleanup board doing", "how many cards left on the board", "show me where the board is at". Mutates nothing.
---

# Board Status

Show current state of a workspace board.

## Instructions

1. **Load tools** by calling `ToolSearch` for `agentboard`. Call `agentboard_health_check`.

2. **Select the board:**
   - Call `agentboard_list_apps`, then `agentboard_list_boards` for the target app
   - If the user passed a board ID as argument, use it directly
   - If multiple boards, ask the user which one

3. **Fetch board data:**
   - Call `agentboard_list_workspace_cards` for the board with `limit=100`. If the result count equals 100, paginate with `offset=100` until you have all cards.
   - Count cards per status column

4. **Display status:**

   ```
   ## Board: [name]
   ID: [board_id]

   | Column | Cards |
   |--------|-------|
   | backlog | [N] |
   | planning | [N] |
   | review | [N] |
   | implementation | [N] |
   | audit | [N] |
   | finished | [N] |

   Progress: [finished]/[total] ([percentage]%)

   ### Blocking Settings
   - Review blocking: [on/off]
   - Audit blocking: [on/off]

   ### Cards Needing Attention
   [List any cards not in backlog or finished, with title and assignee]

   ### Recent Activity
   [Last 5 card updates, if available from card notes]
   ```
