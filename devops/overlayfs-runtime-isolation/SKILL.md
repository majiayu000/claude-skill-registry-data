---
name: overlayfs-runtime-isolation
description: Isolate agent file-system writes using OverlayFS and bubblewrap (bwrap). Core directories mounted read-only; all agent writes go to RAM-backed tmpfs. Zero persistence on session end. Anti-graffiti immutable surface pattern.
origin: Linux OverlayFS docs, containers/bubblewrap (LGPL-2.0), YAMTAM Engine sandbox design
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# OverlayFS Runtime Isolation

Mount core infrastructure as read-only (lowerdir) and redirect all agent writes to ephemeral RAM (upperdir = tmpfs). On session close, tmpfs is discarded — disk never touched.

## When to Use

- Running untrusted or experimental agent tasks without risking real files
- Implementing the Anti-Graffiti immutable surface policy (rule 49)
- Testing destructive tool calls safely (rm, overwrite, git reset)
- Providing agents a writable scratch space that self-cleans on exit

## Do NOT use for

- Persistent storage — tmpfs is lost on unmount/reboot
- Production deployments where agent writes need to survive sessions
- Environments without Linux kernel ≥ 4.0 (OverlayFS requirement)

## Bubblewrap (bwrap) Quickstart

```bash
# Basic: core read-only, /tmp writable, full namespace isolation
bwrap \
  --ro-bind /workspaces/yana-ai /app \
  --bind   /workspaces/yana-ai/releases/logs /app/releases/logs \
  --tmpfs  /tmp \
  --proc   /proc \
  --dev    /dev \
  --unshare-all \
  --share-net \
  --die-with-parent \
  -- node /app/core/scripts/agent-runner.js
```

## OverlayFS Mount (kernel-level)

```bash
# Create layer directories
mkdir -p /tmp/overlay/{upper,work}

# Mount with lowerdir=read-only, upperdir=RAM writes
mount -t overlay overlay \
  -o lowerdir=/workspaces/yana-ai/core,\
     upperdir=/tmp/overlay/upper,\
     workdir=/tmp/overlay/work \
  /mnt/agent-view

# Agent sees /mnt/agent-view — writes go to /tmp/overlay/upper
# Real /workspaces/yana-ai/core is untouched

# Cleanup on session end
umount /mnt/agent-view
rm -rf /tmp/overlay
```

## YAMTAM Integration

```bash
# Enable via tool-proxy.sh
export YAMTAM_SANDBOX_MODE=1
export YAMTAM_SANDBOX_ROOTDIR=/workspaces/yana-ai
export YAMTAM_SANDBOX_WRITEDIR=releases/logs

bash core/scripts/tool-proxy.sh node agent-task.js
# → Phase 3.5 wraps command in bwrap automatically
```

## Namespace Isolation Flags

| Flag | Effect |
|------|--------|
| `--unshare-all` | Isolate pid, net, ipc, uts, cgroup namespaces |
| `--share-net` | Re-enable network (remove for full isolation) |
| `--die-with-parent` | Sandbox exits when parent process exits |
| `--ro-bind src dst` | Mount src as read-only at dst |
| `--tmpfs /path` | RAM-backed writable mount |

## Session Cleanup Verification

```bash
# After agent session ends, verify no writes escaped to real disk
diff -r /workspaces/yana-ai/core /mnt/agent-view/
# Expected: empty diff (all changes were in tmpfs, now gone)
```

## Anti-Fake-Pass Checklist

- [ ] `bwrap --version` confirms bubblewrap is installed (≥ 0.4.0)
- [ ] Write test: `echo test > /app/core/test.txt` inside sandbox → should succeed
- [ ] After exit: `cat /workspaces/yana-ai/core/test.txt` → should NOT exist
- [ ] `--die-with-parent` verified: killing parent kills bwrap child
- [ ] Network isolation tested if `--share-net` removed
