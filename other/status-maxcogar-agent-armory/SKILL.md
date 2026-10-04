---
name: status
description: Read-only status of an AgentBoard phase-based project — current phase (N/13), task counts by status, blockers, and the next action, without starting work. Use whenever the user asks where a project stands, what phase it's on, what's blocked, or what's next on an AgentBoard project — e.g. "project status", "where are we", "what phase are we in", "anything blocked". Mutates nothing. For a workspace-board snapshot, use board-status instead.
---

# AgentBoard Status

Quick situational awareness. Read-only — no mutations.

## Instructions

1. **Authenticate if needed, then verify connectivity.** If only `agentboard_authenticate` and `agentboard_complete_authentication` are visible, run the OAuth bootstrap from `skills/agentboard/SKILL.md` §1.3 first. Then call `agentboard_health_check`.
   - If `health_check` fails post-auth, tell the user: "AgentBoard cloud service is unreachable. Check your network connection or service status at agent-board.app."
   - Stop here if unhealthy.

2. **List projects** by calling `agentboard_list_projects`:
   - If no projects exist, tell the user: "No projects found. Use `/kickoff` to create one."
   - Stop here if no projects.

3. **For each project** (or the active one if only one), call `agentboard_get_project` and `agentboard_list_tasks`.

4. **Display a status summary**:

   ```
   ## AgentBoard Status

   **Project**: [name]
   **Phase**: [N]/13 — [phase name]
   **Target**: [target_project_path or "not set"]

   ### Tasks
   | Status | Count | Details |
   |--------|-------|---------|
   | In Progress | N | [task titles] |
   | Blocked | N | [task titles + reason if in notes] |
   | Ready | N | [next claimable task title] |
   | Review | N | [awaiting human review] |
   | Done | N/total | |

   ### Next Action
   [What should happen next — e.g., "Claim next ready task with /pickup" or "Waiting for human to approve Phase 3 document"]
   ```

5. **Do not start any work.** This skill is purely informational.
