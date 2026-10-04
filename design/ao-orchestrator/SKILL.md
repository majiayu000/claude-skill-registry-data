---
name: ao-orchestrator
description: Use when acting as the multi-project orchestrator and lead coordinator across repositories using the Agent Orchestrator (AO) daemon. Spawns, inspects, coordinates, and reviews parallel coding agents in isolated Git worktrees.
category: bdb-core
risk: safe
tools:
- claude-code
- antigravity
- opencode
- cursor
- codex-cli
---

# 👑 AO Multi-Project Orchestrator (`/ao-orchestrator`)

## Overview

This skill equips any AI coding agent across all supported harnesses (**Claude Code**, **Google Antigravity**, **OpenCode**, **Cursor**, **Codex**) to act as a **Multi-Project Orchestrator** supervising tasks across independent code repositories via the **Agent Orchestrator (AO)** background daemon (`~/.local/bin/ao`).

Instead of making changes directly across multiple repositories within a single context window, the Orchestrator breaks down high-level business goals into scoped work items, delegates them to specialized worker agents running in isolated Git worktrees, monitors their progress, and reviews/integrates their Pull Requests.

---

## 🧭 Orchestrator Responsibilities

1. **Project Discovery & Mapping**: Identify which repositories and workspaces are involved in the user's goal.
2. **Task Decomposition**: Split cross-repo features into clear, atomic specifications for individual worker sessions.
3. **Session Lifecycle Management**: Spawn worker agents with explicit roles (`architect`, `techlead`, `ui_ux`, `engineering`, `reviewer`, `shipping`), appropriate harnesses (`claude-code`, `opencode`, `agy`), and specific prompts.
4. **Coordination & Supervision**: Track running sessions via `ao session ls`, inspect agent logs, and inject steering instructions or clarifications via `ao send`.
5. **Quality Gate & PR Review**: Run `ao review` once a worker completes its task, verify tests, and coordinate cross-project integration.

---

## 🛠️ AO CLI Core Command Suite

The Orchestrator interacts with the local daemon (listening on loopback port `3101`) strictly through the `ao` CLI:

### 1. Discovery & Status
```bash
# Check AO daemon health and version
ao status

# List all registered repositories and workspaces
ao project ls

# List active and recent agent sessions across all projects
ao session ls
```

### 2. Spawning Multi-Project Workers
Run worker agents in fresh, isolated Git worktrees (`ao/<session-id>/root`) so they never conflict with uncommitted working trees:

```bash
# Spawn a Backend Engineer in Project A
ao spawn \
  --project <project-id-or-path> \
  --name "Backend-API" \
  --role engineering \
  --harness claude-code \
  --prompt "Implement the OAuth2 callback handler per specification in issue #42. Ensure all tests pass."

# Spawn a Frontend Designer/Engineer in Project B
ao spawn \
  --project <project-id-or-path> \
  --name "Frontend-UI" \
  --role ui_ux \
  --harness claude-code \
  --prompt "Build the settings page OAuth connection cards with Tailwind and React."

# Spawn an Adversarial Reviewer for an existing worker branch
ao spawn \
  --project <project-id-or-path> \
  --name "Audit-Worker" \
  --role reviewer \
  --prompt "Review branch ao/<session-id>/root for security gaps, unhandled errors, and contract compliance."
```

### 3. Monitoring & Steering Sessions
```bash
# Inspect detailed state of a specific session
ao session get <session-id>

# Send instructions, feedback, or corrections to a running worker
ao send <session-id> "The database migration must support SQLite and Postgres. Please update the schema."

# Switch agent harness if needed (e.g. switch to opencode or agy)
ao session switch-agent <session-id> --to opencode
```

### 4. Review & Completion
```bash
# Trigger an AO code review of the worker's changes
ao review <session-id>

# Clean up or terminate completed sessions
ao session kill <session-id>
ao session cleanup
```

---

## 📋 Multi-Project Orchestration Protocol

When the user asks you to coordinate work across multiple projects:

1. **Step 1: Check Registered Projects**
   Run `ao project ls` to verify the repositories exist in AO. If a project is not registered, instruct the user to register it or navigate to the directory and run `ao project add .`.
2. **Step 2: Propose the Architecture & Work Breakdown**
   Present a clear plan to the user:
   - Which repo needs what changes.
   - What workers will be spawned and with which AOS roles.
   - The dependency order (e.g. Backend API first, then Frontend integration).
3. **Step 3: Spawn Workers Orderly**
   Spawn the prerequisite workers. Avoid spawning dependent workers before the contract/API they depend on is established.
4. **Step 4: Report Progress to User**
   Provide regular, concise summaries in your response showing the status of each spawned session and next actions.
