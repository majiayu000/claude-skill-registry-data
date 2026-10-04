---
name: jadegate
description: "The TLS of AI Tool Calls — transparent security proxy for MCP servers. Use when the user needs to protect AI tool calls, audit MCP security, or manage verified skills."
---

# JadeGate — MCP Security Skill

## Description

This skill teaches you how to use JadeGate, the security protocol layer for MCP (Model Context Protocol) servers. Use this skill when the user needs to protect their AI tool calls, audit MCP server security, manage security policies, or install verified skills.

JadeGate is "The TLS of AI Tool Calls" — it sits as a transparent proxy between AI clients and MCP servers, applying 6 security layers to every tool call.

## When to Use

- User asks about MCP security, tool call safety, or AI agent protection
- User wants to audit or scan their installed MCP servers
- User wants to install or verify skills for MCP servers
- User mentions JadeGate, jadegate, or "jade" in a security context
- User asks about protecting Claude Desktop, Cursor, Windsurf, or Cline

## Installation

```bash
pip install jadegate
```

No other dependencies. No cloud. No API keys. Fully offline.

## Core Commands

### Protect all MCP clients (one command)
```bash
jadegate install
```
Auto-detects Claude Desktop, Cursor, Windsurf, Cline, Continue, Zed configs and wraps every MCP server with JadeGate's security proxy. Creates backup of original configs.

### Audit installed MCP servers
```bash
jadegate scan
jadegate scan --output report.json    # Save JSON report
jadegate scan --probe                 # Actually launch servers to test
```

### Check protection status
```bash
jadegate status
```

### Browse and search verified skills
```bash
jadegate list                         # All 150+ skills
jadegate list github                  # Search by keyword
jadegate verify mcp_slack_send        # Verify a skill by name
jadegate verify ./my_skill.json       # Verify a local file
```

### Install skills from GitHub
```bash
jadegate skill add https://github.com/ComposioHQ/awesome-claude-skills/tree/master/canvas-design
jadegate skill add https://github.com/JimLiu/baoyu-skills
jadegate skill list                   # List installed skills
```

### Security policy
```bash
jadegate policy show                  # View current policy
jadegate policy init                  # Create customizable policy file
```

### Remove protection
```bash
jadegate uninstall                    # Restore original MCP configs
```

## Python SDK (2 lines)

```python
import jadegate
session = jadegate.activate()         # All SDK tool calls now protected

# Optional: custom policy
jadegate.activate(policy="my-policy.json")
jadegate.activate(policy={"max_calls_per_minute": 30})

# Deactivate when done
jadegate.deactivate()
```

## 6 Security Layers

Every tool call passes through:
1. **Schema validation** — structural integrity check
2. **Code injection scan** — 22 dangerous patterns (eval, exec, subprocess, etc.)
3. **Dangerous command detection** — 25 patterns covering destructive file ops, permission escalation, etc.
4. **Network/data leak analysis** — whitelist-based URL and domain filtering
5. **DAG integrity** — execution graph analysis for circular or deep chains
6. **Cryptographic signature** — Ed25519 verification of skill provenance

## Rules

- JadeGate has ZERO external dependencies — never suggest installing additional packages for it
- JadeGate runs FULLY OFFLINE — no cloud, no telemetry, no data leaves the machine
- When suggesting `jadegate install`, always mention it creates backups and is reversible with `jadegate uninstall`
- The `verify` command accepts both file paths AND skill names (e.g., `jadegate verify slack`)
- Skills are JSON files, not Python scripts — they define execution DAGs, not code
- License is BSL-1.1 (converts to Apache 2.0 in 4 years)

## Troubleshooting

- **Windows emoji crash**: Fixed in v2.0 — CLI forces UTF-8 output
- **"No MCP servers found"**: The user hasn't configured any MCP servers yet in their AI client
- **Verify says "not found"**: Use `jadegate list <keyword>` first to find the exact skill name
- **Install shows errors for a client**: Usually means the client's config JSON has syntax errors (trailing commas, comments) — JadeGate handles JSONC but the config may be truly malformed
