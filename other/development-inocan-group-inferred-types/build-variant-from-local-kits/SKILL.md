---
name: build-variant-from-local-kits
description: Build a variant using locally published kits for development validation
---

# Skill: Build Variant from Local Kits

Build a complete Bottlerocket variant image using kits published to the local development registry. This enables end-to-end testing of kit changes before publishing to production registries.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., UPDATE_CONFIG.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
workspace = f"planning/build-variant-{timestamp}"
bash(f"mkdir -p {workspace}")

# Write input configuration
input_data = {
  "kits": [
    {"name": "bottlerocket-core-kit", "version": "<version>"},
    {"name": "bottlerocket-kernel-kit", "version": "<version>"}
  ],
  "variant": "",  # Optional: e.g., "aws-k8s-1.31"
  "arch": ""      # Optional: e.g., "aarch64"
}
write("create", f"{workspace}/input.json", file_text=json.dumps(input_data, indent=2))

while True:
  result = bash(f"python3 skills/build-variant-from-local-kits/next-step.py {workspace}", on_error="raise")
  action = json.loads(result)
  
  if action["type"] == "done":
    final = fs_read("Line", f"{workspace}/FINAL.md", 1, 100)
    log(final)
    break
  
  if action["type"] == "gate_failed":
    log(f"Gate failed: {action['reason']}")
    break
  
  if action["type"] == "spawn":
    r = spawn(
      action["prompt"],
      context_files=action["context_files"],
      context_data=action["context_data"],
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

1. **UPDATE_CONFIG**: Update Twoliter.toml and Infra.toml to reference local kits
2. **UPDATE_LOCK**: Run twoliter update to regenerate lock file
3. **BUILD**: Execute cargo make to build the variant
4. **VALIDATE**: Verify the built image exists and is valid

## Inputs

The orchestrator must create `input.json` in the workspace with:

```json
{
  "kits": [
    {"name": "bottlerocket-core-kit", "version": "1.0.0"},
    {"name": "bottlerocket-kernel-kit", "version": "1.0.0"}
  ],
  "variant": "aws-k8s-1.31",
  "arch": "x86_64"
}
```

- `kits`: List of kit names and versions (required)
- `variant`: Specific variant to build (optional)
- `arch`: Target architecture (optional)

## Outputs

- `FINAL.md`: Build summary with image path and next steps

## Prerequisites

- Kits already built and published to local registry (use `build-kit-locally` skill)
- Local registry running
- Bottlerocket variant repository

## When to Use

- Testing kit changes in a complete variant build
- Creating bootable images for local testing
- End-to-end validation of kit modifications
