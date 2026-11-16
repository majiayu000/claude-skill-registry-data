---
name: ebpf-syscall-monitoring
description: Monitor and intercept Linux kernel syscalls from agent processes using eBPF (Extended Berkeley Packet Filter). Real-time syscall filtering, PID-based policy enforcement, cgroups v2 throttling, and seccomp profile generation.
origin: Linux kernel eBPF docs, Cilium (Apache-2.0), Falco (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# eBPF Syscall Monitoring

Instrument the Linux kernel to intercept agent process syscalls in real time — without modifying agent code.

## When to Use

- Detecting when a containerized agent calls forbidden syscalls (open, write to protected paths)
- Building a dynamic seccomp profile from observed agent behavior
- Monitoring byte-level network activity between agent containers
- Enforcing cgroups v2 CPU/RAM hard limits on per-agent processes

## Do NOT use for

- macOS or Windows environments (eBPF is Linux-only)
- Application-level API monitoring (use OpenTelemetry spans instead)
- Replacing sandboxing — eBPF observes, seccomp enforces

## Core Tools

```bash
# Install BCC (BPF Compiler Collection)
apt-get install bpfcc-tools linux-headers-$(uname -r)

# Trace all file opens by a specific PID
opensnoop-bpfcc -p <agent-pid>

# Watch syscalls in real-time
syscount-bpfcc -p <agent-pid> --syscall write

# Monitor network bytes per container
nethogs  # or use cilium/tetragon for pod-level
```

## Seccomp Profile Generation

```bash
# Record allowed syscalls during a safe training run
oci-seccomp-bpf-hook --record --output agent-profile.json \
  -- node core/scripts/agent-runner.js

# Apply generated profile to restrict future runs
docker run --security-opt seccomp=agent-profile.json ...
```

## Dynamic Seccomp Morphing

```js
// Adjust allowed syscalls based on current task phase
const PHASE_PROFILES = {
  read_only:  ['read', 'close', 'stat', 'getdents64', 'mmap'],
  write_logs: ['read', 'close', 'stat', 'write', 'fsync', 'mmap'],
  network:    ['read', 'write', 'close', 'connect', 'send', 'recv'],
};

function applySeccompProfile(pid, phase) {
  const allowed = PHASE_PROFILES[phase];
  // write seccomp BPF filter to /proc/<pid>/fd via prctl() wrapper
  execSync(`seccomp-apply --pid ${pid} --allow ${allowed.join(',')}`);
}
```

## cgroups v2 Hard Limits

```bash
# Create per-agent cgroup
mkdir /sys/fs/cgroup/yamtam/agent-42

# Memory hard limit: 512MB
echo "536870912" > /sys/fs/cgroup/yamtam/agent-42/memory.max

# CPU: max 50% of one core
echo "50000 100000" > /sys/fs/cgroup/yamtam/agent-42/cpu.max

# Assign agent PID to cgroup
echo <agent-pid> > /sys/fs/cgroup/yamtam/agent-42/cgroup.procs
```

## OOM Score Tuning (Lớp 16)

```bash
# Agent gets killed first when system is under memory pressure
echo 900 > /proc/<agent-pid>/oom_score_adj  # range: -1000 to 1000
```

## Anti-Fake-Pass Checklist

- [ ] eBPF program loaded successfully (`bpftool prog list` shows it)
- [ ] Seccomp profile tested in dry-run mode before enforcing
- [ ] cgroup memory.max verified with `cat /sys/fs/cgroup/yamtam/agent-<id>/memory.current`
- [ ] OOM score confirmed with `cat /proc/<pid>/oom_score_adj`
- [ ] Syscall violations logged to Merkle audit chain (not just stderr)
