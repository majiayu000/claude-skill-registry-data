---
name: create-settings-model
description: Create a new Bottlerocket settings model with SettingsModel trait implementation
---

# Create Settings Model Skill

Creates a complete settings model package with proper directory structure, dependencies, and SettingsModel trait implementation.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., SCAFFOLD.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
workspace = f"planning/{model_name}-settings"
bash(f"mkdir -p {workspace}", on_error="raise")
write("create", f"{workspace}/input.txt", file_text=f"Model name: {model_name}
Description: {description}")

while True:
  action = bash(f"python3 skills/create-settings-model/next-step.py {workspace}", on_error="raise")
  a = json.loads(action)
  
  if a["type"] == "done":
    final = fs_read("Line", f"{workspace}/FINAL.md", 1, 1000)
    break
  
  if a["type"] == "gate_failed":
    log(f"Gate failed: {a['reason']}")
    break
  
  if a["type"] == "spawn":
    r = spawn(
      a["prompt"],
      context_files=a["context_files"],
      context_data=a.get("context_data"),
      allow_tools=True
    )
    write("create", f"{workspace}/{a['output_file']}", file_text=r.response)
```

## Handling Exceptions

The state machine handles the happy path. When things go wrong, **exercise judgment**:

| Exception | Response |
|-----------|----------|
| Spawn times out | Assess: retry with longer timeout? Report partial progress? |
| Spawn returns error | Report failure to state machine, let it track retries |
| Empty/invalid response | Treat as failure, report to state machine |

**Don't silently advance past failures.** Either retry, fail explicitly, or document gaps.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Read phase files yourself | Pass phase files via context_files to subagents |
| Decide what phase is next | State machine decides via next-step.py |
| Skip gates "because it looks done" | Always validate gates |
| Store state in your memory | State lives in progress.json |
| Silently advance past failures | Retry, fail, or document gaps |

## Phases

1. **SCAFFOLD**: Create directory structure and basic files (Cargo.toml, lib.rs, main.rs)
2. **IMPLEMENT**: Implement SettingsModel trait methods (get_version, set, generate, validate)
3. **VALIDATE**: Verify with cargo check

## Inputs

Gather before starting:
- Model name (e.g., "myapp")
- Description of what settings this model manages
- Settings fields and their types

## Outputs

Complete settings model package at:
```
kits/bottlerocket-core-kit/packages/<name>-settings/
├── Cargo.toml
├── lib.rs
└── main.rs
```
