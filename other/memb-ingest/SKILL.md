---
name: memb-ingest
description: Use when deep scan and ingest project files (.md, .json, agent.md, .openwiki) and past conversation logs into the local memB vector memory engine.
category: bdb-core
---

# memB Deep Memory Ingestion Skill

When this skill is invoked via `/memb-ingest` or requested, you MUST orchestrate a deep scan of the user-specified project path or conversation logs to populate the **memB local vector database (`~/.MemBDB/memb.db`)**.

## Core Workflow & Instructions

### 1. Target Path & Filter Selection
- Ask the user: *"Which directory or project path would you like to scan into memB memory?"* (Default: Current Workspace or active project directory)
- Ask if they would also like to include **past Antigravity chat transcripts (`--transcripts`)** or filter specific file patterns (e.g., `*.md`, `agent.md`, `.openwiki/`).

### 2. Execution
Locate the `memb-mcp` installation (e.g., `~/.gemini/config/mcps/memb-mcp/` or `~/.gemini/mcps/memb-mcp/`) and execute the ingestion script via its virtual environment:

```bash
# Run ingestion with project detection & optional transcript indexing
~/.gemini/config/mcps/memb-mcp/.venv/bin/python ~/.gemini/config/mcps/memb-mcp/memb_ingest.py "<TARGET_DIRECTORY>" --transcripts
```

### 3. Verification
Query memB using `search_memory` or inspect `~/.MemBDB/memb.db` to confirm that the project architecture and key decisions are indexed.

## Execution Rules
1. **Never skip path confirmation:** Always verify the target path before running the scan.
2. **Filter Noise:** Ignore `node_modules`, `.venv`, `.git`, `dist`, and temporary cache directories.
3. **Report Summary:** Present a clear count of indexed documents to the user upon completion.

## 1. Overview
This skill provides domain-specific logic and rules for its respective BDB pipeline component to ensure standardization across multi-agent workflows.

## 2. When to Use
- Use when specifically requested by the user or triggered by an orchestration agent.
- Use when the current task aligns with the skill's domain.
- Exclude when standard tool execution is sufficient.

## 3. Core Process
1. Read the provided context and ensure preconditions are met.
2. Run the required script or tool and confirm the state change.
3. Verify exit codes, file modifications, or DB counts to guarantee success before reporting completion.

## 4. Common Rationalizations
| Rationalization | Reality |
|---|---|
| "The code change was small, so I skipped updating OpenWiki docs." | Every state change must be reflected in the relevant system records. |
| "The ingest script exited without an error, so the memB index must be updated." | Silent failures happen; explicit verification of the side effect is mandatory. |
| "I'll let the /startcycle proceed without a defined rollback path." | Proceeding without a rollback path corrupts the workflow integrity and safety. |
| "I trust the cached agent registry instead of rescanning after a skill change." | Caches stale out quickly; explicit rescans prevent ghost failures. |

## 5. Red Flags
- Bypassing the verification step after a script execution.
- Proceeding to the next pipeline stage without confirming the previous stage's side effects.
- Ignoring domain-specific constraints listed in this skill.

## 6. Verification
- [ ] Verified script exit codes are explicitly checked.
- [ ] Confirmed target files or database records reflect the expected change.
- [ ] Ensured no silent failures were ignored before reporting success.
