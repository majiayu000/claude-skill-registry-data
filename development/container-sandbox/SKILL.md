---
name: container-sandbox
description: Run risky or destructive operations inside ephemeral Docker containers for isolation. Use when executing untrusted scripts, destructive Ansible playbooks, or operations that could damage the host.
triggers:
  - sandbox
  - container isolate
  - risky operation
  - destructive
  - isolated environment
  - safe container
---

# Container Sandbox — Isolated Execution Environment

Run potentially dangerous operations inside ephemeral Docker containers. The host filesystem is protected — containers get read-only project mounts with a writable overlay.

## When to Use

- Destructive Ansible playbooks (`--force`, `--limit` testing)
- Untrusted scripts from external sources
- Operations that modify system state (`rm -rf`, package installs)
- Testing migrations or schema changes before applying to production
- Running code from unknown repos

## Quick Start

### Basic sandbox (Ubuntu + project files):
```bash
docker run --rm -it \
  -v "$(pwd):/project:ro" \
  -v /tmp/sandbox-work:/work \
  -w /work \
  ubuntu:24.04 \
  bash -c "cp -r /project/* /work/ && bash"
```

### Python sandbox (with project deps):
```bash
docker run --rm -it \
  -v "$(pwd):/project:ro" \
  -v /tmp/sandbox-work:/work \
  -w /work \
  python:3.12-slim \
  bash -c "cp -r /project/* /work/ && pip install -r requirements.txt 2>/dev/null; bash"
```

### GPU sandbox (for CUDA operations):
```bash
docker run --rm -it --gpus all \
  -v "$(pwd):/project:ro" \
  -v /tmp/sandbox-work:/work \
  -w /work \
  nvidia/cuda:13.1-devel-ubuntu24.04 \
  bash
```

### Ansible dry-run sandbox:
```bash
docker run --rm -it \
  -v /opt/ai-project:/project:ro \
  -v ~/.ssh:/root/.ssh:ro \
  -w /work \
  --network host \
  willhallonline/ansible:latest \
  bash -c "cp -r /project/* /work/ && ansible-playbook -i inventory playbook.yml --check --diff"
```

## Extracting Results

After running operations in the sandbox:
```bash
# Copy results out of the sandbox work directory
docker cp <container_id>:/work/results/ ./sandbox-results/

# Or use the /tmp/sandbox-work mount (persists after --rm if pre-created)
ls /tmp/sandbox-work/
```

## Safety Rules

1. **Always mount project directories as `:ro`** (read-only)
2. **Use `/tmp/sandbox-work` or `/work`** for writable operations
3. **Use `--rm`** to auto-cleanup containers after exit
4. **Use `--network none`** for maximum isolation (no internet access)
5. **Never mount `/` or `/home` as writable** into a sandbox
6. **GPU sandboxes** (`--gpus all`) still share the host GPU — use for testing, not isolation

## Integration with Claude Code

When Claude needs to run something risky, instruct it to:
1. Build the Docker command with appropriate mounts
2. Execute the command via Bash tool
3. Capture stdout/stderr from the container
4. Extract any produced files from the work directory
5. Clean up: `rm -rf /tmp/sandbox-work`
