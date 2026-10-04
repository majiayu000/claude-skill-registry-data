---
name: tracing
description: tracing. Use when you need help with tracing.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: program-types
---

# Tracing Program Types

## Related Guidance

- For cross-kernel compatibility checks, see `workflows/testing.md`.
- Tracing often depends on exact kernel structs and object lifetimes. If a field, function signature, or kernel object relationship is unclear, check Linux kernel source and kernel docs directly.

## Quick Choice

- Use `tracepoint` for the most portable stable kernel events.
- Use `tp_btf` on modern kernels when you want typed tracepoint arguments.
- Use `kprobe` / `kretprobe` when no stable tracepoint exists.
- Use `BPF_KSYSCALL` for portable syscall entry tracing.
- Use `uprobe` / `uretprobe` for userspace function visibility.
- Use `fentry` / `fexit` when BTF is available and lower overhead matters.
- Use `perf_event` for sampling rather than event-per-call tracing.
- Use `lsm` only when you need policy enforcement, not just observation.

## kprobe / kretprobe

Attach to any kernel function entry or return. Use when no stable tracepoint exists for the function you need.

**When to use it:**
- ad-hoc kernel function tracing
- exploring internal kernel paths without stable tracepoints
- kernels where trampoline-based hooks are unavailable

```c
SEC("kprobe/tcp_connect")
int BPF_KPROBE(handle_tcp_connect, struct sock *sk) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    bpf_printk("pid=%d connecting\n", pid);
    return 0;
}

SEC("kretprobe/tcp_connect")
int BPF_KRETPROBE(handle_tcp_connect_ret, int ret) {
    bpf_printk("tcp_connect returned %d\n", ret);
    return 0;
}
```

**Notes:**
- `BPF_KPROBE` / `BPF_KRETPROBE` macros unpack `struct pt_regs *ctx` into named args automatically
- Function signatures can change between kernel versions — less portable than tracepoints
- Auto-attach: libbpf attaches based on `kprobe/<func>` in the SEC name

### kprobe.multi — Wildcard / Bulk Attach (kernel ≥ 5.18)

Attach one program to multiple functions in a single syscall. Supports glob patterns and is significantly cheaper than attaching N individual kprobes.

```c
// Attach to all spin_lock variants in one shot
SEC("kprobe.multi/spin_*lock*")
int BPF_KPROBE(handle_spin_lock) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    bpf_printk("spin_lock pid=%d\n", pid);
    return 0;
}

// Wildcard suffix — handles compiler-inlined/renamed variants of a function
// e.g. __netif_receive_skb_core.isra.0, __netif_receive_skb_core.constprop.1
SEC("kprobe.multi/__netif_receive_skb_core*")
int BPF_KPROBE(handle_netif_rx) { return 0; }
```

**Attaching (libbpf):**
```c
// Attach by pattern
LIBBPF_OPTS(bpf_kprobe_multi_opts, opts, .syms = syms, .cnt = cnt);
struct bpf_link *link = bpf_program__attach_kprobe_multi_opts(prog, NULL, &opts);
```

**Notes:**
- Use `*` suffix whenever a kernel function is frequently inlined or has compiler suffixes
- `kretprobe.multi/func*` works the same way for return probes
- `bpf_get_func_ip(ctx)` returns the address of the specific function that fired

### Macro-Generated Handlers

When attaching the same logic to many functions, use a macro to avoid boilerplate:

```c
#define PROBE(fname)                          \
    SEC("kprobe/" #fname)                     \
    int fname##_entry(struct pt_regs *ctx) {  \
        record_entry(#fname);                 \
        return 0;                             \
    }

PROBE(vfs_read)
PROBE(vfs_write)
PROBE(vfs_open)
```

---

## ksyscall

Portable syscall probing. Handles architecture-specific syscall ABI differences (e.g., `__x64_sys_open` vs `__arm64_sys_open`) so you don't have to.

**When to use it:**
- syscall entry tracing across architectures
- portable syscall-oriented tools where tracepoints are too limiting

```c
SEC("kprobe")
int BPF_KSYSCALL(handle_sys_open, const char *filename, int flags, umode_t mode) {
    char buf[256];
    bpf_probe_read_user_str(buf, sizeof(buf), filename);
    bpf_printk("open: %s flags=%d\n", buf, flags);
    return 0;
}
```

**Notes:**
- Use `BPF_KSYSCALL` instead of `BPF_KPROBE` for syscall entry points
- Declare the `SEC("kprobe")` without a function name; attach manually or via libbpf `bpf_program__attach_ksyscall()`

---

## uprobe / uretprobe

Probe userspace functions in a binary or library. No source changes needed — works on any ELF binary.

**When to use it:**
- tracing libraries or runtimes such as OpenSSL, libc, JVM, or language runtimes
- correlating userspace function calls with kernel activity

```c
SEC("uprobe/func_name")
int BPF_UPROBE(handle_func, int arg0, int arg1) {
    bpf_printk("uprobe hit: arg0=%d arg1=%d\n", arg0, arg1);
    return 0;
}

SEC("uretprobe/func_name")
int BPF_URETPROBE(handle_func_ret, int ret) {
    bpf_printk("uretprobe: ret=%d\n", ret);
    return 0;
}
```

**Notes:**
- Attach with `bpf_program__attach_uprobe(prog, false, pid, "/path/to/binary", func_offset)`
- Use `bpf_sym_to_addr` or `nm`/`objdump` to find function offsets
- Common targets: OpenSSL (`SSL_read`/`SSL_write`), language runtimes, database drivers

---

## tracepoint

Attach to stable, pre-defined kernel tracepoints. Most portable option — tracepoint ABIs are stable across kernel versions.

**When to use it:**
- production tracing with portability expectations
- syscall and scheduler tracing where a stable tracepoint already exists

```c
SEC("tp/syscalls/sys_enter_openat")
int handle_openat(struct trace_event_raw_sys_enter *ctx) {
    char fname[256];
    bpf_probe_read_user_str(fname, sizeof(fname), (void *)ctx->args[1]);
    bpf_printk("openat: %s\n", fname);
    return 0;
}
```

**Notes:**
- List available tracepoints: `bpftrace -l 'tracepoint:*'` or `ls /sys/kernel/debug/tracing/events`
- Context struct is `struct trace_event_raw_<name>` — defined in vmlinux.h
- Prefer over kprobes when a tracepoint exists for what you need

---

## raw_tracepoint

Like tracepoint but receives raw, unprocessed arguments. Slightly more overhead to use but avoids the kernel's argument transformation step.

**When to use it:**
- raw argument access matters more than convenience
- you want a lower-level tracepoint path and can tolerate manual argument handling

```c
SEC("raw_tp/sched_switch")
int BPF_PROG(handle_sched_switch) {
    // args available via BPF_PROG macro
    return 0;
}
```

**Notes:**
- Context args are `u64 *ctx` — cast manually or use `BPF_PROG` macro
- Lower overhead than tracepoint when the transformation cost matters
- Requires more manual argument handling than tp_btf

---

## tp_btf

BTF-typed raw tracepoint. Gets the best of both worlds: stable tracepoint attachment + direct native type access without `BPF_CORE_READ`.

**When to use it:**
- modern kernels with BTF
- tracepoints where you want both portability and typed ergonomic access

```c
SEC("tp_btf/sched_process_exec")
int BPF_PROG(handle_exec, struct task_struct *p, pid_t old_pid,
             struct linux_binprm *bprm) {
    // access fields directly — no BPF_CORE_READ needed
    u32 pid = p->pid;
    return 0;
}
```

**Notes:**
- Requires kernel BTF and kernel ≥ 5.5
- Arguments are typed via BTF — safest and most ergonomic tracing type for modern kernels
- Prefer over `raw_tp` and `tp` when the kernel is recent enough

---

## fentry / fexit / fmod_ret

BTF-based function hooks. Lower overhead than kprobe (no `int3` breakpoint). `fexit` uniquely has access to both input args and the return value at the same time.

**When to use it:**
- modern kernels with BTF
- lower-overhead function tracing
- `fexit` when you need both arguments and return value together
- `fmod_ret` only when controlled return-value override is actually intended

```c
SEC("fentry/tcp_connect")
int BPF_PROG2(handle_fentry, struct sock *, sk) {
    bpf_printk("fentry: tcp_connect\n");
    return 0;
}

SEC("fexit/tcp_connect")
int BPF_PROG2(handle_fexit, struct sock *, sk, int, ret) {
    bpf_printk("fexit: ret=%d\n", ret);
    return 0;
}

// fmod_ret — modify return value
SEC("fmod_ret/security_file_permission")
int BPF_PROG2(handle_fmod, struct file *, file, int, mask) {
    // return 0 to let original run; return non-zero to override
    return 0;
}
```

**Notes:**
- Requires kernel BTF — use `BPF_PROG2` macro (not `BPF_PROG` or `BPF_KPROBE`)
- Arg list in `BPF_PROG2` alternates: `type, name, type, name, ...`
- `fmod_ret` can short-circuit the original function — use carefully
- Not all functions are attachable (inline functions, those with `notrace` annotation)

---

## perf_event

Attach to hardware/software performance counters. Used for CPU profiling and sampling.

**When to use it:**
- periodic sampling
- CPU profiling and flame-graph pipelines
- lower-volume observability than function-per-event tracing

```c
SEC("perf_event")
int handle_perfevent(struct bpf_perf_event_data *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    bpf_printk("perf sample: pid=%d\n", pid);
    return 0;
}
```

**Notes:**
- Attach with `bpf_program__attach_perf_event(prog, perf_fd)` where `perf_fd` comes from `perf_event_open(2)`
- No auto-attach — must open perf event manually
- Common use: CPU flame graphs, cache miss profiling

---

## lsm

Enforce security policy by hooking Linux Security Module hooks. Can deny operations by returning a negative error code.

**When to use it:**
- allow/deny policy enforcement
- security controls tied to LSM hook points
- auditing plus optional denial

```c
SEC("lsm/security_file_permission")
int BPF_PROG(handle_file_perm, struct file *file, int mask) {
    // return 0 to allow, negative errno to deny
    return 0;
}

SEC("lsm/bprm_check_security")
int BPF_PROG(handle_exec_check, struct linux_binprm *bprm) {
    return 0;
}
```

**Notes:**
- Requires `CONFIG_BPF_LSM=y` and `lsm=bpf` in kernel boot params (or appended to existing lsm= list)
- Check enabled LSMs: `cat /sys/kernel/security/lsm`
- Use `BPF_PROG` macro (not `BPF_PROG2`)
- Returning a non-zero error denies the operation — incorrect policy can lock out the system, test carefully
