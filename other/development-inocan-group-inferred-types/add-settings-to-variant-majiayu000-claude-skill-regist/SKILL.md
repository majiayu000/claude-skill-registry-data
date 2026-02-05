---
name: add-settings-to-variant
description: Wire an existing settings model into a Bottlerocket variant via settings-plugins
---

# Add Settings to Variant

Wire an existing settings model into a Bottlerocket variant using the settings-plugins approach.

## Purpose

Integrates a settings model (already defined) into a variant by:
- Locating the variant's settings-plugins crate
- Adding the settings model as a dependency
- Verifying compilation

## When to Use

Use when you have:
- An existing settings model crate (e.g., `my-settings`)
- A target variant that needs to consume those settings
- Need to wire them together via settings-plugins

**Prerequisites:**
- Settings model crate exists and compiles
- Variant exists in bottlerocket/variants/
- Core-kit is available (contains settings-plugins)

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., LOCATE.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
import json

workspace = f"planning/add-settings-{variant_name}"
bash(f"mkdir -p {workspace}", on_error="raise")
write("create", f"{workspace}/input.json", file_text=json.dumps({
  "variant_name": variant_name,
  "settings_crate": settings_crate
}))

while True:
  result = bash(f"python3 skills/add-settings-to-variant/next-step.py {workspace}", on_error="raise")
  action = json.loads(result)
  
  if action["type"] == "done":
    final = fs_read("Line", f"{workspace}/FINAL.md", 1, -1)
    log(final)
    break
  
  if action["type"] == "gate_failed":
    log(f"Gate failed: {action['reason']}")
    break
  
  if action["type"] == "spawn":
    r = spawn(
      action["prompt"],
      context_files=action["context_files"],
      context_data=action.get("context_data", {}),
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

1. **LOCATE**: Find variant's settings-plugins crate, understand structure
2. **INTEGRATE**: Add settings model to plugin, update dependencies
3. **VERIFY**: Build settings-plugins package, confirm compilation

## Inputs

What the orchestrator needs to gather before starting:
- `variant_name`: Target variant (e.g., "aws-ecs-1")
- `settings_crate`: Settings model crate name (e.g., "my-settings")

## Outputs

- `{workspace}/FINAL.md`: Summary of integration with file locations and verification results

## Technical Notes

- Runtime discovery NOT YET IMPLEMENTED - must use settings-plugins approach
- Only one settings-plugin per variant (virtual package conflict)
- Settings-plugins typically in kits/bottlerocket-core-kit/packages/
