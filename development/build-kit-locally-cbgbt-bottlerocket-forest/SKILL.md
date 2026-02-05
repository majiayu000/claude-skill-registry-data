---
name: build-kit-locally
description: Build a kit and publish it to a locally hosted registry for development testing
---

# Skill: Build and Publish Kit

Build a Bottlerocket kit (core-kit or kernel-kit) and publish it to a local OCI registry for development testing and validation.

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
workspace = f"planning/build-kit-{kit_name}"
bash(f"mkdir -p {workspace}", on_error="raise")

input_data = {"kit_name": kit_name, "arch": arch}
write("create", f"{workspace}/input.json", file_text=json.dumps(input_data))

while True:
    result = bash(f"python3 skills/build-kit-locally/next-step.py {workspace}", on_error="raise")
    action = json.loads(result)
    
    if action["type"] == "done":
        verify = fs_read("Line", f"{workspace}/04-verify.md", 1, 100)
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

1. **SETUP**: Ensure local registry is running and configure Infra.toml
2. **BUILD**: Build the kit for specified architecture
3. **PUBLISH**: Publish built kit to local OCI registry
4. **VERIFY**: Verify kit was successfully published

## Inputs

Create `{{workspace}}/input.json` with:
- `kit_name`: Name of the kit (e.g., "bottlerocket-core-kit")
- `arch`: Architecture to build (default: "x86_64", or "aarch64")

## Outputs

- `{{workspace}}/01-setup.md`: Registry and Infra.toml configuration status
- `{{workspace}}/02-build.md`: Build artifacts and status
- `{{workspace}}/03-publish.md`: Published tags and registry info
- `{{workspace}}/04-verify.md`: Verification results and next steps

## When to Use

- Making changes to kit packages and testing them in variants
- Iterative development on kits
- Before building a variant image that depends on kit changes

## Prerequisites

- Docker installed and running
- Kit repository cloned in `kits/` directory
- FOREST_ROOT environment variable set

## Common Issues

**Registry not running:**
```
Error: connection refused
```
Solution: The SETUP phase will start the registry automatically

**Infra.toml not configured:**
```
Error: vendor 'local' not found
```
Solution: The SETUP phase creates Infra.toml if missing

**Docker permission denied:**
Solution: Ensure user is in docker group and Docker daemon is running

## Next Steps

After the skill completes:
1. Update variant's `Twoliter.toml` to reference the new kit version
2. Run `make update` in the variant repo
3. Build the variant with `cargo make`
