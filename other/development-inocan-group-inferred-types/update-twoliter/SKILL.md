---
name: update-twoliter
description: Update all Bottlerocket repositories to a new Twoliter version
---

# Skill: Update Twoliter Version

Update all repositories in the forest to a new version of Twoliter. This creates git commits in core-kit, kernel-kit, and bottlerocket repositories with the updated version and SHA256 checksums.

## Roles

**You (reading this file) are the orchestrator.**

| Role | Reads | Does |
|------|-------|------|
| Orchestrator (you) | SKILL.md, next-step.py output | Runs state machine, spawns subagents, writes outputs |
| State machine | progress.json, workspace files | Decides next action, validates gates |
| Subagent | Phase file (e.g., FETCH.md) | Executes phase instructions |

⚠️ **You do NOT read files in `phases/`** — pass them to subagents via context_files. Subagents read their phase file and execute it.

## Orchestrator Loop

```python
workspace = f"planning/update-twoliter-{version}"
bash(f"mkdir -p {workspace}", on_error="raise")
write("create", f"{workspace}/version.txt", file_text=version)
write("create", f"{workspace}/worktree_root.txt", file_text=worktree_root)

while True:
  result = bash(f"python3 skills/update-twoliter/next-step.py {workspace}", on_error="raise")
  action = json.loads(result)
  
  if action["type"] == "done":
    final = fs_read("Line", f"{workspace}/FINAL.md", 1, 100)
    break
  
  if action["type"] == "gate_failed":
    log(f"Gate failed: {action['reason']}")
    break
  
  if action["type"] == "spawn":
    r = spawn(
      action["prompt"],
      context_files=action["context_files"],
      context_data={**action.get("context_data", {}), "worktree_root": worktree_root},
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

1. **FETCH**: Download SHA256 checksums from GitHub releases
2. **UPDATE_KITS**: Update all kit Makefiles and commit (no 'v' prefix)
3. **UPDATE_BOTTLEROCKET**: Update bottlerocket/Makefile.toml and commit (with 'v' prefix)
4. **VALIDATE**: Verify all commits were created correctly

## Inputs

Before starting, gather:
- Target Twoliter version (e.g., "0.13.0" or "0.13.0-rc1")
- Worktree root path (where kits/ and bottlerocket/ directories exist)

## Outputs

- `<workspace>/FINAL.md`: Validation report with list of updated repositories

## Prerequisites

- All repositories cloned in the forest worktree
- Git configured with author information
- Network access to GitHub releases

## Common Issues

**SHA256 checksum not found:**
- Verify the release exists: `https://github.com/bottlerocket-os/twoliter/releases/tag/vX.Y.Z`
- Check that binary artifacts are attached to the release

**Wrong version format:**
- Kits use `"X.Y.Z"` (no `v` prefix) in their Makefiles
- bottlerocket uses `"vX.Y.Z"` (with `v` prefix) in Makefile.toml

**Amending commits:**
If you need to update an existing commit (e.g., moving from RC to stable):
```bash
git add <file>
git commit --amend -m "chore: bump to twoliter X.Y.Z"
```

## Notes

- This skill does NOT push commits or create pull requests
- After creating commits, you can push them and create PRs manually
- PRs will trigger CI to test the new Twoliter version
- Schema version changes are rare; only update if release notes specify
