---
name: debugging
description: debugging. Use when you need help with debugging.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: workflows
---

# Debugging Workflow

Use this file for runtime debugging, attach/load diagnosis, missing-event investigation, and host-level eBPF troubleshooting.

## When to Use This File

- program loads but does nothing
- attach fails or succeeds inconsistently
- events are missing, out of order, or unexpectedly empty
- maps are not updating
- the host seems not to support the expected feature

## First Pass

Start with the smallest observable checks:

```bash
mount -t bpf bpffs /sys/fs/bpf
bpftool prog list
bpftool map list
bpftool feature
bpftool prog tracelog
cat /sys/kernel/debug/tracing/trace_pipe
```

Guidance:
- use `bpftool prog tracelog` first when available instead of assuming the user will watch `trace_pipe`
- if the host seems feature-poor, verify with `bpftool feature` before redesigning the program
- if LSM is involved, inspect `/sys/kernel/security/lsm`
- if hook behavior is missing, verify both kernel support and runtime enablement

## Load and Attach Diagnosis

Typical sequence:

```bash
mount -t bpf bpffs /sys/fs/bpf
bpftool prog load prog.bpf.o /sys/fs/bpf/test
export LIBBPF_LOG_LEVEL=debug
bpftool prog show
bpftool map dump name <map_name>
```

Use this workflow:
1. Confirm the object actually loads.
2. Confirm the program is attached where you think it is.
3. Confirm maps exist and contain expected state.
4. Confirm events or debug output are observable.
5. Only then change logic.

## If Attach Succeeds But Behavior Is Missing

Check these before rewriting the program:

- wrong hook or wrong attach target
- feature unsupported on that kernel
- feature compiled in but disabled at boot/runtime
- filter too narrow or global variable misconfigured
- wrong map chosen for the access pattern
- user-space reader not polling or parsing correctly

Good confirmations:

```bash
bpftool prog show id <ID>
bpftool map dump name <map_name>
bpftrace -l 'tracepoint:*'
bpftrace -l 'kprobe:<pattern>'
```

## Runtime Signal Sources

Use the least noisy source that answers the question:

- `bpftool prog tracelog` for printk-style output
- `trace_pipe` when `tracelog` is unavailable or insufficient
- `bpftool map dump` for live state inspection
- `bpftool prog dump xlated` when instruction-level review matters
- `bpftrace` one-liners to cross-check whether expected events are firing at all

## Noise Reduction

- clear or ignore stale tracing noise before a repro
- make the repro path as small as possible
- reduce filters and globals to permissive values before suspecting verifier or kernel issues
- prefer one hook and one event path while debugging

## Common Runtime Failure Patterns

| Symptom | Likely Cause | First Check |
|---------|--------------|-------------|
| program loads, no events | wrong hook, wrong target, over-filtering | attachment details and globals |
| maps stay empty | hook not firing or key path never reached | add temporary prints or dump xlated code |
| lost or missing events | undersized ring/perf buffers | increase buffer size and inspect reader loop |
| feature appears unavailable | kernel/config mismatch | `bpftool feature`, config, boot state |
| attach works on one host only | kernel/version/runtime differences | compare `bpftool feature` and attach mode |

## Useful External Tools

- `bpftop` when overhead and loaded-program visibility matter
- upstream `bpftool` releases when distro packages lag too far behind
