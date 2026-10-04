---
name: misc
description: misc. Use when you need help with misc.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: program-types
---

# Miscellaneous Program Types

Less common types used for program composition, kernel extension, and specialized hooks.

## Related Guidance

- For cross-kernel compatibility checks, see `workflows/testing.md`.
- These advanced hooks often depend on exact kernel object semantics. If a struct, callback contract, or attach target is unclear, check Linux kernel source and kernel docs directly.

## Quick Choice

- Use `freplace` when you need to replace or wrap an already loaded BPF program.
- Use `struct_ops` when implementing kernel callback tables in BPF.
- Use `syscall` only for specialized privileged loader designs.
- Use LWT hooks only when the routing/tunneling path is the real integration point.

---

## BPF_PROG_TYPE_EXT (Program Extension)

Replaces or wraps an existing loaded BPF program. Used to hot-patch a running program without reloading it.

**When to use it:**
- hot-patching or extending an already loaded BPF program
- runtime replacement where a full reload is undesirable

```c
// The replacement program must match the signature of the target
SEC("freplace/original_prog_name")
int replacement_handler(struct xdp_md *ctx) {
    // pre-processing...
    // bpf_tail_call into the original, or fully replace it
    return XDP_PASS;
}
```

**Attaching (libbpf):**
```c
// Open the target object and find the program to replace
struct bpf_program *ext_prog = bpf_object__find_program_by_name(obj, "replacement_handler");
bpf_program__set_attach_prog_fd(ext_prog, target_prog_fd);
bpf_object__load(obj);

struct bpf_link *link = bpf_program__attach(ext_prog);
```

**Notes:**
- Available since kernel 5.6
- The extension program's prototype must exactly match the replaced program's signature
- Used by projects like Katran for runtime policy updates without downtime
- `BPF_PROG_TYPE_EXT` programs can only be attached to one target at a time

---

## BPF_PROG_TYPE_STRUCT_OPS

Implements kernel struct operations (e.g. TCP congestion control algorithms, scheduler ops) entirely in BPF. The BPF program replaces a kernel vtable.

**When to use it:**
- kernel callback-table implementations in BPF
- TCP congestion control or sched-ext style customization

```c
// Implement a custom TCP congestion control algorithm
SEC("struct_ops/tcp_init")
void BPF_PROG(my_cc_init, struct sock *sk) { }

SEC("struct_ops/tcp_cong_avoid")
void BPF_PROG(my_cc_cong_avoid, struct sock *sk, u32 ack, u32 acked) { }

SEC("struct_ops/tcp_ssthresh")
u32 BPF_PROG(my_cc_ssthresh, struct sock *sk) { return 0; }

// Register the struct_ops — must match the kernel struct exactly
SEC(".struct_ops")
struct tcp_congestion_ops my_cc = {
    .init        = (void *)my_cc_init,
    .cong_avoid  = (void *)my_cc_cong_avoid,
    .ssthresh    = (void *)my_cc_ssthresh,
    .name        = "my_bpf_cc",
};
```

**Notes:**
- Available since kernel 5.6 (TCP CC); extended in 6.x for scheduler and other ops
- Each function in the struct_ops must be a separate BPF program
- Load with libbpf skeleton — `bpf_map__attach_struct_ops(skel->maps.my_cc)`
- Used for: TCP congestion control (Chromium's BBR via BPF), custom sched_ext schedulers

---

## BPF_PROG_TYPE_SYSCALL

Allows BPF programs to issue BPF syscalls themselves — enabling one BPF program to load and manage other BPF programs.

**When to use it:**
- specialized privileged bootstrap or loader setups
- advanced environments where one BPF program manages others

```c
SEC("syscall")
int prog_loader(struct pt_regs *ctx) {
    // Can call bpf() syscall to create maps, load programs, etc.
    return 0;
}
```

**Notes:**
- Available since kernel 5.14
- Requires `CAP_BPF` + `CAP_PERFMON` or `CAP_SYS_ADMIN`
- Primary use: privileged loader programs that bootstrap unprivileged eBPF setups
- Not commonly needed in application-level eBPF work

---

## Lightweight Tunnel Types (LWT)

Hook into the Linux lightweight tunnel subsystem for custom encapsulation/decapsulation logic.

**When to use them:**
- routing-path encapsulation or decapsulation
- SRv6 and lightweight tunnel integration points
- cases where XDP or TC are not the right place in the packet path

| Type | SEC() | Direction | Use Case |
|------|-------|-----------|----------|
| `lwt_in` | `SEC("lwt_in")` | Ingress | Process inbound tunnel packets |
| `lwt_out` | `SEC("lwt_out")` | Egress | Process outbound tunnel packets |
| `lwt_xmit` | `SEC("lwt_xmit")` | Transmit | Custom encapsulation before transmit |
| `lwt_seg6local` | `SEC("lwt_seg6local")` | SRv6 | Segment Routing v6 local processing |

```c
SEC("lwt_in")
int handle_lwt_in(struct __sk_buff *skb) {
    return BPF_OK;
}

SEC("lwt_xmit")
int handle_lwt_xmit(struct __sk_buff *skb) {
    // Can call bpf_lwt_push_encap to add encapsulation
    return BPF_OK;
}
```

**Attaching:**
```bash
# Attach via iproute2 route command
ip route add 10.0.0.0/24 encap bpf in obj prog.o sec lwt_in dev eth0
ip route add 10.0.0.0/24 encap bpf xmit obj prog.o sec lwt_xmit dev eth0
```

**Notes:**
- Available since kernel 4.10 (in/out/xmit), 4.14 (seg6local)
- Context is `struct __sk_buff *` — similar to TC but in the routing path
- Niche use case — prefer XDP/TC for most packet processing needs
- `lwt_xmit` can call `bpf_lwt_push_encap` to prepend MPLS, IP-in-IP, etc.
