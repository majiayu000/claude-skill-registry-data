---
name: linux-ebpf-tracing
description: >
  Diagnose Linux latency, CPU, I/O, syscall and scheduling problems by writing small, bounded
  bpftrace programs after forming a hypothesis, with explicit checks for kernel support (BTF,
  kernel version), privileges (root or CAP_BPF/CAP_PERFMON), probe stability and tracing overhead.
  Use when top/strace/perf are not enough and you need per-event or per-latency evidence from
  a live Linux host, for example "what is opening these files", "why is read latency spiky",
  "which process causes block I/O". Not for first-line triage (use linux-troubleshooting), for
  CPU flame-graph profiling workflows (use performance-profiling), nor for macOS/Windows, nor
  for writing production eBPF programs in C/Rust (libbpf, Aya) or security enforcement.
compatibility: >
  Linux only. bpftrace 0.19+ for the args.field syntax used here (check bpftrace --version).
  Needs a kernel with BPF tracing support; BTF (CONFIG_DEBUG_INFO_BTF) strongly recommended for
  struct access. Requires root or equivalent capabilities. Verify support on the host with
  bpftrace --info.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, ebpf, bpftrace, tracing, observability, latency, kernel"
  topics: "linux, performance"
---

# Linux eBPF Tracing with bpftrace

eBPF tracing lets you ask a running kernel narrow questions ("how long does `vfs_read` take per process?") with low overhead, without restarting anything. The risk is not the language; it is **asking vague questions, attaching to hot paths, and drawing causal conclusions from correlation**. This skill teaches the diagnosis loop; the mechanics are small.

Boundaries: start with `linux-troubleshooting` (load, memory, disk, logs) and `linux-processes-systemd`; use `performance-profiling` for sampling profilers and flame graphs; this skill is for event-level tracing when those leave a specific unanswered question. Hardening of the host is `linux-hardening`.

## Non-negotiable rules

1. **Authorization first.** Loading BPF programs on a host needs privileges and affects a live system. Get the user's explicit go-ahead for each host, especially production. Never use `sudo` implicitly; show the exact command.
2. **Read-only observation only.** Do not use state-changing facilities: `system()`, `signal()`, `override()`/return-value overriding, or `-c` with a command that mutates anything. They are off by default for a reason. Do not attach with `--unsafe` unless the user requested it and understands it relaxes kprobe safety checks and enables state-changing helpers such as `system()` and `signal()`.
3. **Bound every probe.** Always filter (`/pid == X/`, `/comm == "name"/`, a cgroup) and always bound duration (`interval:s:N { exit(); }` or an outer `timeout`). Unbounded tracing of `sys_enter` on a busy host is the classic way to cause the incident you are chasing.
4. **Prefer stable probes.** Tracepoints and USDT are stable ABI-like interfaces; kprobes attach to internal functions that can be renamed, inlined or removed between kernel versions. Use kprobes only when no tracepoint answers the question and state that assumption.
5. **Output is sensitive.** Strings such as file paths, `comm`, command-line arguments and user data may contain secrets or personal data. Aggregate (`count()`, `hist()`) in preference to dumping raw events, and do not paste raw output containing credentials into tickets.
6. **Stop on surprise.** If the host slows down, kernel warnings appear, or the verifier rejects with an unclear error, stop (Ctrl-C detaches the probes) and reassess; do not retry with looser safety.

## Workflow

### 1. Write the hypothesis and the metric that would settle it

"Latency spikes in the API are caused by slow `read()` on the data volume" predicts: p99 of `vfs_read` duration for pid X on that mount rises during spikes. If the prediction fails, the hypothesis is out. Decide the *aggregation* (histogram, count by key) before the probe.

### 2. Check the environment (read-only)

```bash
uname -r
bpftrace --version
bpftrace --info 2>&1 | head -60     # reports supported features; needs privileges
ls /sys/kernel/btf/vmlinux          # present when the kernel exposes BTF
id                                  # root, or CAP_BPF + CAP_PERFMON on kernels that define them
```

- **Kernel and BTF:** bpftrace tracing needs a kernel with BPF and perf-event support. Modern distribution kernels ship BTF (`CONFIG_DEBUG_INFO_BTF=y`), which lets `kprobe` programs read struct fields without kernel headers. Without BTF you must include kernel headers (see the `path.h` example in the official tutorial) and results are more fragile. Do not assume a minimum from memory; trust `bpftrace --info` on the target.
- **Privileges:** tracing programs are root-only in the classic model. Kernels with `CAP_BPF` and `CAP_PERFMON` allow a narrower grant, but other kernel settings (lockdown mode, `kernel.perf_event_paranoid`, container seccomp/AppArmor) can still block it. Inside containers you usually cannot trace without privileged access to the host kernel; that is a request to the node owner, not something to work around.
- **Syntax versions:** `args.filename` needs bpftrace 0.19+; older versions use `args->filename`.

### 3. Discover probes before writing

```bash
bpftrace -l 'tracepoint:syscalls:sys_enter_open*'
bpftrace -vl tracepoint:syscalls:sys_enter_openat     # shows the args fields
bpftrace -l 'kprobe:vfs_*' | head
```

### 4. Dry-run, then run bounded

```bash
bpftrace --dry-run -e 'tracepoint:syscalls:sys_enter_openat { @[comm] = count(); }'   # check `bpftrace --help` for exact --dry-run semantics
timeout 30 bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @[comm] = count(); }'
```

On exit bpftrace prints all maps, so aggregation maps (`@name`) are your result. `timeout` is a coreutils tool; prefer in-script `interval:s:30 { exit(); }` when you want maps printed by bpftrace itself on exit.

### 5. Interpret with care

- **Histograms** show distributions; read the bucket where the tail lives, not the average.
- **Latency pairs** (kprobe entry + kretprobe) store the start time in a map keyed by `tid`; delete the key on return, or the map leaks and entries from interrupted calls corrupt results.
- **Sampling vs tracing:** `profile:hz:99` samples stacks; counts are proportional, not exact.
- **Probe effect:** per-event probes on high-rate functions slow the target. Compare workload throughput with and without probes if you suspect distortion.
- **Dropped data / map limits:** if bpftrace warns about lost events or full maps, your numbers are incomplete; narrow the filter rather than raising limits.
- One tracing run supports or refutes a hypothesis; it rarely proves a cause. Cross-check with a second signal (e.g. `iostat`, application logs, `perf`).

### 6. Report and clean up

Report: kernel and bpftrace versions, the exact program, duration, load conditions, the result, and what remains uncertain. Probes detach when bpftrace exits; confirm with `bpftool prog show` if available that nothing of yours remains.

## Program patterns (all bounded, read-only)

```bash
# Who is opening files (counts per process), 10 seconds
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { @[comm] = count(); } interval:s:10 { exit(); }'

# read() latency histogram per process name (kprobe: version-fragile), 10 seconds
bpftrace -e 'kprobe:vfs_read { @start[tid] = nsecs; }
  kretprobe:vfs_read /@start[tid]/ { @ns[comm] = hist(nsecs - @start[tid]); delete(@start[tid]); }
  interval:s:10 { exit(); }'

# Block I/O size distribution, 10 seconds
bpftrace -e 'tracepoint:block:block_rq_issue { @bytes = hist(args.bytes); } interval:s:10 { exit(); }'

# On-CPU kernel stacks sampled at 99 Hz, 10 seconds
bpftrace -e 'profile:hz:99 { @[kstack] = count(); } interval:s:10 { exit(); }'
```

These follow the official bpftrace one-liner tutorial. Note that bpftrace prints every map at exit, so a leftover `@start` map clutters the output; add `END { clear(@start); }` to the latency program to keep only results. Adapt filters (`/comm == "myapp"/`) before running on shared hosts. For ready-made tools, the bpftrace repository ships canonical scripts under `tools/` (for example `opensnoop.bt`, `biolatency.bt`, `runqlat.bt`); review a script before running it.

## Worked example: spiky disk reads

1. Hypothesis: spikes come from slow block I/O on `nvme0n1`, not from CPU scheduling.
2. Confirm authorization and kernel support (step 2). Kernel has BTF; bpftrace 0.19+.
3. Run the block I/O histogram for 30 s during a spike window. Result: bimodal histogram with a tail at 8-16 ms.
4. Cross-check with `iostat -x 1` during the same window: `r_await` rises. Evidence agrees.
5. Refine: split by `comm` to identify the issuing process. Finding: the backup agent, not the API. Hypothesis about the API's own reads is refuted; report with the caveat that this was a single 30 s window.

## Anti-patterns

- Tracing `raw_syscalls:sys_enter` with a per-event `printf` on a busy host.
- Treating a kprobe script as portable across kernels or distro builds.
- Averages instead of histograms; single-run conclusions.
- Leaving `@start[tid]` entries behind, or keying by `pid` when threads interleave.
- Using `--unsafe`, `system()` or signals "to also kill the offender" while diagnosing.
- Running as root over an unattended long period without a duration bound.
- Pasting full `comm`/path/argument dumps into tickets.

## Verification checklist

- [ ] Hypothesis and expected observation written down before tracing.
- [ ] Authorization obtained; command shown before running.
- [ ] Filter and duration bound present; dry-run passed.
- [ ] Kernel, bpftrace version and probe type (tracepoint vs kprobe) recorded.
- [ ] Result cross-checked with an independent signal; limitations stated.
- [ ] No state-changing helpers used; probes confirmed detached.

## References

- [references/probe-selection.md](references/probe-selection.md): choosing probe types and diagnosing attach failures.
- [references/scenarios.md](references/scenarios.md): evaluation scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
