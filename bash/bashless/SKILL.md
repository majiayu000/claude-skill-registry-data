---
description:  >
  Amend an existing Claude Code setup to replace the Bash tool with structured MCP tools,
  reducing agent reliance on unstructured shell access.
disable-model-invocation: true
user-invocable: true
---

# Claude Code Bashless Setup

Your goal is to amend an existing Claude Code project setup so that the agent no longer uses
the built-in `Bash` tool. Instead, all essential CLI capabilities are exposed as structured MCP tools
via a local MCP stdio server. This forces the agent to use purpose-built tools with explicit parameters
rather than being attracted to unstructured shell access.

**Additional user arguments**: $ARGUMENTS

**Language hint**: Always create all generated script content and comments in English
for consistency across the codebase, while continuing to speak to the user in the language of their choice.

**Platform hint**: Instructions and templates assume a Linux host with GNU coreutils. Adapt to the detected user OS.
- macOS   — Substitute BSD equivalents for GNU-only utilities.
- Windows — Still use `.sh` files (skip irrelevant `chmod +x`), assuming Git Bash is available at runtime.
            Highlight this requirement in the Debriefing. Set `"shell": "bash"` on new command hooks in `settings.json`.
            Launch the MCP server via bash rather than putting the `.sh` path directly in `command`.

# Workflow

Begin execution by creating a formal task list for progress tracking using the `TaskCreate` tool (if available).
Create a task for each of the following phases (##) and sub-phases (###).
This protects you from accidentally skipping phases and visualizes the progress for the user.

## Phase 1: Reconnaissance

Catalogue shell commands and MCP tools the agent will require during autonomous code development for this project.
Assume the project has already been initialized with artifacts for Claude Code and existing technology is documented.

### 1a — Shell Commands

Spawn an `Agent` to scan the following locations for explicit and implicit references to CLI commands: 
1. The project's `CLAUDE.md` and any sub-directory `CLAUDE.md` files
2. The project's `.claude` directory, particularly sub-directories `commands/`, `rules/` and `agents/`
3. Top-level documentation files (e.g. `README.md`, `CONTRIBUTING.md`, `docs/`)

Pay special attention to the following aspects:
- **Execution wrappers** — How commands are executed in general: directly, via Docker, NPX, Makefile, etc.
- **Test runners** — How are automated tests executed (e.g. `pytest`, `jest`, `siesta`, `phpunit`, `go test`)
- **Linters/formatters** — How is code quality ensured (e.g. `eslint`, `ruff`, `phpcs`)
- **Build tools** — Are builds executed manually and if so how (e.g. `make`, `npm run build`, `cargo build`)
- **Framework CLIs** — Project-specific console commands (e.g. `artisan`, `manage.py`, `nx`, `laravel`/`symfony`)

Use `TaskCreate` to add a task for each file that needs to be updated in Phase 3c below, so none is forgotten.

### 1b — MCP Tools

Spawn an `Agent` to summarize available MCP tools:
1. Read `.mcp.json` at the project root (if it exists) to identify existing project-registered servers.
2. Use the `ToolSearch` tool to query: "+mcp__" with high max_results to fetch schemas for all available MCP tools.
3. Return a full tool list, grouped by server (name pattern "mcp__<server>__"), with very short description per tool. 
   - Highlight tools suitable for codebase exploration (e.g. IDE search tools, Code Index, symbol/semantic search).
   - Highlight tools that can read or edit files and could make the agent ignore the native `Read`/`Write`/`Edit` tools.

## Phase 2: User Interview

Use `AskUserQuestion` during the following interview process to keep the conversation structured.
Offer pre-defined choice options where possible based on reconnaissance findings.

### 2a — Git Write Permissions

Ask the user to which degree the agent should be able to participate in Git code submission:

- **Read-only** — The user reviews all code changes in the IDE and makes commits manually.
  The agent only receives tools to explore and modify the current working tree 
  (`git_status`, `git_log`, `git_show`, `git_diff`, `git_blame`, `git_rm`, `git_mv`).
- **Commit** — The user reviews and amends finished commits by the agent and pushes them manually.
  The agent receives read tools plus `git_commit`.
- **Full** — The agent can interact with git fully autonomously.
  All of the above plus `git_branch`, `git_checkout` and `git_push`.
  If chosen, ask the user a follow-up question whether push to certain branches should be prohibited. 

### 2b — CLI Tool Selection

Present the proposed list of project CLI tools to the user. For each tool, show:
- CLI application name
- Example command
- Proposed MCP tool name (e.g. `git_log`, `npm_test`) and parameters

Detect or ask the user whether a sandboxed execution wrapper is available on the system
(e.g. `bubblewrap` on Linux, `sandbox-exec` on macOS).
- If sandboxing is available, suggest adding available read-only filesystem utilities (`diff`, `jq`).
- If sandboxing is unavailable but the user has explicitly requested such tools,
  warn against the resulting security risks and offer to help with the installation of a respective sandboxing tool.
  If the user explicitly insists on proceeding with an unsandboxed setup, note this for Phase 3a and the debriefing.

Ask the user to:
1. Confirm, remove, or add tools
2. Suggest additional project-specific commands not detected automatically

### 2c — Codebase Exploration Tools

Determine whether you have access to MCP tools for codebase exploration (from reconnaissance phase 1b).

- If such tools exist: Ask the user whether they also wish to disable the native `Glob` and `Grep`
  built-in tools, since the MCP alternatives may be superior in efficiency and speed.
- If no such tools exist: Inform the user that `Glob` and `Grep` will remain enabled as they are
  essential for codebase navigation without `Bash`.

### 2d — MCP Tool Pruning

Explain to the user that many MCP servers expose a large number of tools indiscriminately,
so disabling undesired and unnecessary tools helps the agent make better tool call decisions.

For each MCP server identified during reconnaissance phase 1b with more than ~5 tools:
1. Present a table of available tools with their short descriptions, grouped by server.
2. Ask the user to identify the tools they actively want to keep — or alternatively, tools they want to remove.

Recommendations:
 - Advise to keep search/find tools (especially indexed/semantic/structural/symbolic search).
 - Advise against redundant tools (overlapping functions) that make tool-choice less obvious.
 - Warn about tools that can execute external actions such as IDE run configurations.

**Important:** Always recommend deactivation of tools that can read or edit/refactor files!
These tools can tempt the agent to ignore native `Read`/`Write`/`Edit` tools
which are important for the enforcement of rules, hooks and permission checks.

### 2e — Sandbox Configuration

Check whether the current `.claude/settings.json` contains a `sandbox` configuration block.

- If it does: Explain that the sandbox only restricts the `Bash` tool and has no effect when `Bash` is disabled.
  Ask the user whether the sandbox block should be removed to reduce configuration noise.
- If it does not: Skip this question.

## Phase 3: Generate Artifacts

### 3a — CLI MCP Server

1. Copy the [template](./templates/bash-commands-mcp.sh) to `<project-dir>/.claude/mcp/bash-commands.sh` and make it executable (`chmod +x`).
2. Adjust the command execution wrappers to match the project's execution environment.
3. Uncomment and adapt the `run_local_sandboxed` wrapper based on the target operating system,
   independent of whether a sandboxing tool is actually installed, ensuring the function is available.
   - Use `run_local_sandboxed` for all tools that locally execute arbitrary code or filesystem operations.
   - Only fall back to `run_local` (unsandboxed) if the user explicitly insisted on doing so in phase 2b.
     Document this decision with an inline comment.
4. The template already contains working implementations of the git read tools.
   Based on the git permission level chosen in Phase 2a, uncomment the corresponding write tools:
   - **Commit:** Uncomment `git_commit` in both the tool definitions and the handler.
   - **Full:** Also uncomment `git_push`.
5. Replace `{{TOOL-DEFINITIONS}}` with JSON tool entries for the project-specific CLI tools confirmed in Phase 2b.
   Use the commented project tool example in the template as a guide.
6. Replace `{{TOOL-HANDLERS}}` with matching case branches for each project-specific tool added in step 5.
7. Create or update `.mcp.json` at the project root, registering the server:
   ```json
   {
     "mcpServers": {
       "bash": {
         "type": "stdio",
         "command": ".claude/mcp/bash-commands.sh"
       }
     }
   }
   ```
   If `.mcp.json` already exists, merge the new entry without removing existing servers.

### 3b — Ensure Git Index Coverage for Created Files

Inspect the `.claude/hooks/` directory (and the `hooks` section in `.claude/settings.json`) for any
`PostToolUse` hook that matches the `Write` tool and automatically runs `git add`.
If such a mechanism already exists, skip the rest of this step.

1. Explain to the user that our structured git tools cannot work on untracked files.
   Therefore, it must be ensured that `git add` is called automatically whenever new files are created.
2. Use `AskUserQuestion` to offer the following options or accept other user instructions:
   - **Amend existing hook** — For each `PostToolUse` hook script that exists and already handles `Write` events.
   - **Create minimal hook** — Create a new hook script `.claude/hooks/post-write.sh`,
3. Write the missing logic to the chosen script, using the [template](./templates/git-add-hook.sh) as inspiration.
4. Register a new hook script as a `PostToolUse` with matcher `Write` and make the script executable.

### 3c — Update Agent Instructions

Review all `CLAUDE.md` and `.claude/` files catalogued in Phase 1 for references to CLI commands.
For each file that mentions specific shell commands:

1. Replace references to bare shell commands with references to the corresponding MCP tool names,
   e.g. "use the `mcp__bash__pytest` tool" instead of "run `pytest`".
2. Where rules reference the `Bash` tool by name, remove or rephrase those references.
   In particular, replace references in `agents/` frontmatter field `tools` with suitable mcp tools.
   In custom explorer agents, these are typically: `mcp__bash__git_log`, `mcp__bash__git_show`, `mcp__bash__git_blame`

### 3d — Update Settings

Modify `.claude/settings.json` to disable the `Bash` tool (and optionally `Glob`/`Grep`) and prune MCP tools:

1. Add `"enableAllProjectMcpServers": true` at the root object level to enable the `.mcp.json` definitions.
2. Add `"includeGitInstructions": false` at the root object level, since the MCP git tools bring their own instructions.
3. Add `"mcp__bash__*"` to the `permissions.allow` array (create it if it does not exist).
4. Add `"Bash"` to the `permissions.deny` array (create it if it does not exist).
   Also add `"PowerShell"` tool to deny list on Windows hosts.
5. If the user chose to disable `Glob` and `Grep` in Phase 2c, also add `"Glob"` and `"Grep"` to `permissions.deny`.
6. Add every MCP tool the user explicitly or implicitly chose to remove in Phase 2d to `permissions.deny`.
   Wildcard patterns can be used to exclude all tools from a server (e.g. `"mcp__<server>__*"`)
   as well as certain namespaced tool groups within a server (`"mcp__<server>__<group>_*"`).
7. Add every MCP server as `"mcp__<server>__*"` to `permissions.allow` if it has a corresponding tool deny list.
   Deny rules are evaluated first, so this yields exactly the pruned tool set without per-call prompts for the rest.
8. If the user chose to remove the sandbox block in Phase 2e, delete the entire `sandbox` key.
9. If a `PreToolUse` or `PostToolUse` hook references `Bash` in its matcher, notify the user that this is now obsolete.

## Phase 4: Debriefing & Disclaimers

- Present a summary table of everything created or modified (file path, change type, purpose).
- Explain that this is a restrictive configuration change. Specifically:
  - **MCP Tool Coverage:** The generated server only wraps the tools identified during the interview.
    If the agent needs additional CLI capabilities later, developers must add new tool definitions
    and handlers to the MCP server script. Look out for agent complaints or hallucinations due to missing tools.
  - **Git Tools:** The git tools provide basic access. Complex git workflows (interactive rebase, etc.)
    still require human intervention.
  - **MCP Tool Security:** Unlike the `Bash` sandbox, the MCP server executes commands without any
    external containment. Each tool added to it represents an explicitly granted capability — developers
    are responsible for ensuring that no tool indirectly grants access beyond the project context.
    For example, `git rm` is preferred over `rm` not only because it stages changes transparently,
    but also because it is bounded by the git index and cannot reach outside the repository.
    Be particularly cautious with tools that invoke Docker or other container runtimes,
    as these can expose host filesystem mounts and network interfaces to the agent.
  - **Glob/Grep:** If these were disabled, ensure the alternative MCP exploration tools
    adequately cover the agent's search needs. Monitor whether the agent struggles to navigate the codebase.
  - **MCP Tool Pruning:** The denied tools are completely hidden from the agent. This can be verified using `/context all`.
    If the agent later seems unable to perform an expected task, check whether a required tool was accidentally denied.
  - **Hooks:** Promote the idea that hooks can also be used to integrate CLI command execution
    into agentic workflows and should be preferred when possible, as this is more reliable than agent tool calls.
  - **Restart Required:** New tools and hooks are only picked up after restarting Claude Code. 
