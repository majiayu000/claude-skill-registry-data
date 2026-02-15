---
name: ams-mcp-server
description: |
  AMS (Application Management System) MCP Server - Educational roadmaps, task management with Eisenhower Matrix, and cryptographic audit (5-phase Merkle tree verification). 
  
  Use when working with:
  - Educational roadmaps (73 developer roadmaps from roadmap.sh)
  - Task management and productivity tracking
  - GSD (Get Shit Done) methodology projects
  - Audit trails with cryptographic verification
  
  ALWAYS use when user mentions: roadmaps, learning paths, task management, @ams, unified-mcp, or asks to work with E:/AMS projects.
---

# AMS MCP Server Skill

## Quick Decision Tree

```
User wants to...
├── Learn something new? → roadmap_list → roadmap_get → roadmap_nodes
├── Create project from roadmap? → roadmap_export_to_gsd (REQUIRED first!)
├── Manage tasks? → task_create, task_eisenhower, task_list
├── Track progress? → roadmap_progress_update, task_update
├── Watch file changes? → watcher_start (ONLY after roadmap_export_to_gsd!)
├── Audit/verify actions? → context_create → audit_session_start → merkle_finalize
└── Check system? → unified_vitals, unified_help
```

## Critical Rules

### ⚠️ Rule 1: watcher_start requires roadmap_export_to_gsd FIRST
**WRONG:**
```
@ams watcher_start { "project_name": "my-app" }  # ❌ Error: Project not found
```

**CORRECT:**
```
@ams roadmap_export_to_gsd { "roadmap_id": "frontend", "project_name": "my-app" }
@ams watcher_start { "project_name": "my-app" }  # ✅ Works!
```

### ⚠️ Rule 2: Always initialize first
```
@ams unified_init  # Creates required directories
@ams unified_vitals # Check system is operational
```

### ⚠️ Rule 3: Use @ams prefix explicitly
Most clients require `@ams` prefix for MCP tools:
```
@ams roadmap_list           # ✅ Correct
roadmap_list               # ❌ May not work
```

## Standard Workflow

### Phase 1: Discovery (5 minutes)
```
1. unified_init                                    # Setup directories
2. unified_vitals                                  # Check status
3. roadmap_list                                    # Show 73 roadmaps
4. roadmap_get { "roadmap_id": "frontend" }       # Details
5. roadmap_nodes { "roadmap_id": "frontend" }     # All topics
```

### Phase 2: Planning (10 minutes)
```
6. roadmap_export_to_gsd {                         # ⚠️ CRITICAL STEP
     "roadmap_id": "frontend",
     "project_name": "my-learning-project",
     "pace": "normal"
   }
7. task_create {                                   # Create specific tasks
     "title": "Learn React Hooks",
     "priority": "urgent_important"
   }
8. task_link_roadmap {                             # Link to roadmap
     "task_id": "...",
     "roadmap_id": "frontend",
     "node_id": "react-hooks"
   }
```

### Phase 3: Execution (ongoing)
```
9. watcher_start { "project_name": "my-learning-project" }
10. task_eisenhower                               # View matrix
11. task_update { "id": "...", "status": "in_progress" }
12. roadmap_progress_update {                     # Track learning
      "roadmap_id": "frontend",
      "node_id": "react-hooks",
      "status": "completed"
    }
```

## Configuration

### For Claude Code
```bash
mkdir -p ~/.claude
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "ams": {
      "command": "node",
      "args": ["E:/AMS/projects/unified-mcp/src/server.js"],
      "env": { "AMS_ROOT": "E:/AMS" }
    }
  }
}
EOF
```

### For Kimi Code
Config at: `~/.kimi/mcp.json`

### For AntiGravity
Config at: `~/AppData/Roaming/AntiGravity/User/mcp.json`

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Project not found" | watcher_start before export | Run roadmap_export_to_gsd first |
| "MCP server not found" | Client not configured | Check mcp.json, restart client |
| "Roadmap not found" | Wrong roadmap_id | Use roadmap_list to see valid IDs |
| "Connection error" | Server not running | unified_vitals to check |

## Key Tools Reference

### Essential (use frequently)
- `unified_init` - System setup
- `roadmap_list` - Browse roadmaps  
- `roadmap_export_to_gsd` - Create project (⚠️ prerequisite)
- `task_create` / `task_list` / `task_update`
- `watcher_start` / `watcher_status`

### Analysis
- `analysis_search` - TF-IDF search
- `roadmap_next_topic` - Recommendations

### Audit (advanced)
- `context_create` - Snapshot
- `audit_session_start` - Begin logging
- `merkle_finalize` - Cryptographic proof

## File Structure

```
E:/AMS/
├── data/
│   ├── roadmaps/        # 73 roadmap.sh sources
│   ├── projects/        # GSD projects (created by export)
│   └── ams.db          # SQLite (tasks, progress, audit)
└── projects/
    └── unified-mcp/
        └── src/server.js
```

## Advanced Patterns

### Pattern: Learning with audit trail
```
1. context_create { "roadmap_id": "frontend" }
2. audit_session_start
3. thought_plan { "plan": "Week 1: HTML/CSS basics" }
4. [do work...]
5. thought_decide { "decision": "Focus on Flexbox before Grid" }
6. merkle_finalize
7. merkle_attest  # External verification
```

### Pattern: Project with file sync
```
1. roadmap_export_to_gsd { "roadmap_id": "backend", "project_name": "api" }
2. watcher_start { "project_name": "api" }
3. [edit TODOS.md in E:/AMS/data/projects/api/]
4. [watcher auto-syncs to tasks]
```

## References

- [references/workflow.md](references/workflow.md) - Detailed workflows
- [references/tools.md](references/tools.md) - All 58 tools documentation
- [references/errors.md](references/errors.md) - Troubleshooting guide
