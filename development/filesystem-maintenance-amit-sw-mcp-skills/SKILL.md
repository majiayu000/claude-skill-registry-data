---
name: filesystem-maintenance
description: Use when Codex needs to inspect or modify files via the local Python filesystem MCP server running at `servers/filesystem`.
---

# Filesystem Maintenance

## Purpose
Safely read, write, and delete files under `MCP_FS_ROOT` using the stdio-based filesystem MCP server bundled with this repository. Applies to refactors, log retrieval, and config updates when direct shell access is discouraged.

## Setup Checklist
1. Activate the repo virtual environment and install `servers/filesystem/requirements.txt`.
2. Launch the server through `mcp.json` (`python servers/filesystem/server.py`) with `MCP_FS_ROOT` pointing at the workspace root.
3. Confirm the server advertises the tools `list_dir`, `read_file`, `write_file`, and `delete_path`.

## Workflow
1. **Discovery** – call `list_dir` to understand the structure before editing. Limit breadth by passing the nearest parent directory.
2. **Read** – fetch file contents using `read_file(relative_path)` to avoid stale local copies.
3. **Edit** – stage modifications via normal repo tooling, then persist with `write_file`. When writing, pass relative paths (e.g., `skills/github-operations/SKILL.md`).
4. **Cleanup** – remove temporary artifacts using `delete_path` only after verifying that the target path is inside `MCP_FS_ROOT`.

## Notes
- The `_resolve` guard inside `server.py` prevents escaping above `MCP_FS_ROOT`. If you see a permission error, double-check the path.
- Use this skill when another skill (e.g., `github-operations`) references files you must read—chain the skills rather than reimplementing file access.
- Keep writes idempotent: re-read the file to ensure committed changes match expectations.
