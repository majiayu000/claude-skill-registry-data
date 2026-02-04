---
name: test-settings-locally
description: Build and test settings SDK changes locally using core-kit and variant builds
---

# Test Settings Locally

Build and test Bottlerocket settings changes end-to-end using local builds.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., SETUP.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
workspace = f"planning/test-settings-{timestamp}"
bash(f"mkdir -p {workspace}", on_error="raise")

while True:
    result = bash(f"python3 skills/test-settings-locally/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)
    
    if action["type"] == "done":
        final = fs_read("Line", f"{workspace}/FINAL.md", 1, -1)
        program_return(final)
        break
    
    if action["type"] == "gate_failed":
        log(f"Gate failed: {action['reason']}")
        program_return(f"Failed: {action['reason']}")
        break
    
    if action["type"] == "spawn":
        r = spawn(
            action["prompt"],
            context_files=action["context_files"],
            context_data=action.get("context_data"),
            allow_tools=True
        )
        write("create", f"{workspace}/{action['output_file']}", file_text=r.response)
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

1. **SETUP**: Verify prerequisites, start local registry
2. **BUILD-KIT**: Build core-kit with settings changes, publish locally
3. **BUILD-VARIANT**: Configure and build variant using local kit

## Inputs

The orchestrator needs:
- Settings changes in bottlerocket-settings-sdk or core-kit
- Docker installed and running
- Bottlerocket variant repository available

## Outputs

- `{workspace}/00-setup.md` - Setup verification results
- `{workspace}/01-build-kit.md` - Kit build results
- `{workspace}/02-build-variant.md` - Variant build results
- `{workspace}/FINAL.md` - Summary and next steps

## Purpose

Validate settings SDK changes by building core-kit with your changes and testing in a variant build, all using local registry.

## When to Use

- Testing changes to bottlerocket-settings-sdk
- Validating new settings extensions
- End-to-end testing before publishing

## Related Skills

- `local-registry` - Registry management
- `build-kit-locally` - Kit building
- `build-variant-from-local-kits` - Variant building
