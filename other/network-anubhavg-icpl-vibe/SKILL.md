---
name: network
description: network. Use when you need help with network.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: program-types
---

# Network Program Types

## Related Guidance

- For cross-kernel compatibility checks, see `workflows/testing.md`.
- Network hooks interact with kernel packet metadata, sockets, devices, and routing objects. If any context field or kernel object is unclear, check Linux kernel source and kernel docs directly.

## Quick Choice

- Use `xdp` for the earliest, fastest drop/redirect path.
- Use `tc` when you need skb metadata or packet mutation inside the network stack.
- Use `tcx` on new kernels when multi-program ordering matters.
- Use `sk_skb` / `sk_msg` for socket-level stream or message redirection.
- Use `sk_lookup` or `sk_reuseport` for socket selection decisions.
- Use `flow_dissector` only when you need to control flow key extraction.
- Use `netfilter` when netfilter hook ordering matters more than XDP/TC placement.

## XDP (eXpress Data Path)

Earliest packet processing hook — runs in the NIC driver's RX path before the kernel network stack. Fastest possible packet processing.

**When to use it:**
- packet drop, pass, redirect, and early L3 forwarding
- high-rate filtering on the RX hot path
- AF_XDP, DEVMAP, or CPUMAP based pipelines

```c
SEC("xdp")
int handle_xdp(struct xdp_md *ctx) {
    void *data     = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_DROP;

    return XDP_PASS;
}
```

**Return codes:**
| Code | Meaning |
|------|---------|
| `XDP_PASS` | Send packet up the stack normally |
| `XDP_DROP` | Drop the packet silently |
| `XDP_TX` | Transmit back out the same interface |
| `XDP_REDIRECT` | Redirect to another interface or CPU |
| `XDP_ABORTED` | Drop with trace event (debugging only) |

**Attaching:**
```bash
# Generic mode (works everywhere, slower)
bpftool net attach xdp id <prog_id> dev eth0

# Native mode (requires driver support, fastest)
bpftool net attach xdp id <prog_id> dev eth0 # driver picks mode

# Detach
bpftool net detach xdp dev eth0
```

**Notes:**
- Always bounds-check packet data before access: `if (ptr + size > data_end) return XDP_DROP;`
- Cannot call `bpf_printk` in XDP without careful consideration — hot path
- Fragmented packets: `ctx->data` only contains the first fragment; handle with `bpf_xdp_adjust_head`

### XDP Routing Pattern — FIB Lookup + Redirect

The canonical pattern for XDP-based L3 forwarding: parse headers → FIB lookup → rewrite MACs/TTL → redirect.

```c
SEC("xdp")
int xdp_router(struct xdp_md *ctx) {
    void *data     = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end) return XDP_DROP;

    struct iphdr *iph = (void *)(eth + 1);
    if ((void *)(iph + 1) > data_end) return XDP_DROP;

    // FIB lookup — resolves next-hop MAC + egress ifindex
    struct bpf_fib_lookup fib = {
        .family   = AF_INET,
        .tos      = iph->tos,
        .l4_protocol = iph->protocol,
        .ipv4_src = iph->saddr,
        .ipv4_dst = iph->daddr,
        .ifindex  = ctx->ingress_ifindex,
    };
    int rc = bpf_fib_lookup(ctx, &fib, sizeof(fib), 0);
    if (rc != BPF_FIB_LKUP_RET_SUCCESS) return XDP_PASS;

    // Rewrite L2 headers and decrement TTL
    if (iph->ttl <= 1) return XDP_PASS;  // let kernel send ICMP TTL exceeded
    iph->ttl--;
    // Efficient checksum update: add 0x0100 (decrement TTL by 1 in network order)
    iph->check += bpf_htons(0x0100);
    if (iph->check == 0) iph->check = 0xffff;  // RFC 1624 carry

    __builtin_memcpy(eth->h_dest,   fib.dmac, ETH_ALEN);
    __builtin_memcpy(eth->h_source, fib.smac, ETH_ALEN);

    return bpf_redirect(fib.ifindex, 0);
}
```

**FIB lookup return codes:**
| Code | Meaning |
|------|---------|
| `BPF_FIB_LKUP_RET_SUCCESS` | Forward — use `fib.ifindex`, `fib.dmac`, `fib.smac` |
| `BPF_FIB_LKUP_RET_BLACKHOLE` | Drop |
| `BPF_FIB_LKUP_RET_UNREACHABLE` | No route — pass to stack |
| `BPF_FIB_LKUP_RET_NOT_FWDED` | Not forwarded (e.g. local delivery) |
| `BPF_FIB_LKUP_RET_FWD_DISABLED` | Forwarding disabled on interface |
| `BPF_FIB_LKUP_RET_NO_NEIGH` | Route found but no ARP/ND entry yet |

---

## TC / TCX (Traffic Control)

Runs inside the kernel network stack on both ingress and egress. Has access to socket metadata and can modify packet headers. TCX is the newer multi-prog version.

**When to use it:**
- packet rewriting inside the stack
- policy that needs skb metadata, marks, or socket identity
- `tcx` when ordered multi-prog chaining is important on new kernels

```c
// Classic TC
SEC("tc/ingress")
int handle_ingress(struct __sk_buff *skb) {
    return TC_ACT_OK;
}

SEC("tc/egress")
int handle_egress(struct __sk_buff *skb) {
    return TC_ACT_OK;
}

// TCX — preferred for new programs (supports ordered multi-program attachment)
SEC("tcx/ingress")
int handle_tcx_ingress(struct __sk_buff *skb) {
    return TCX_NEXT;  // pass to next program in chain
}

SEC("tcx/egress")
int handle_tcx_egress(struct __sk_buff *skb) {
    return TCX_PASS;
}
```

**TC return codes:**
| Code | Meaning |
|------|---------|
| `TC_ACT_OK` / `TCX_PASS` | Pass packet |
| `TC_ACT_SHOT` / `TCX_DROP` | Drop packet |
| `TC_ACT_REDIRECT` | Redirect packet |
| `TCX_NEXT` | Pass to next program in the chain (TCX only) |

**Attaching classic TC:**
```bash
tc qdisc add dev eth0 clsact
tc filter add dev eth0 ingress bpf da obj prog.bpf.o sec tc/ingress
tc filter del dev eth0 ingress
```

**Attaching TCX (bpftool):**
```bash
bpftool net attach tcx ingress id <prog_id> dev eth0
bpftool net detach tcx ingress dev eth0
```

**Notes:**
- TC has access to `skb->mark`, `skb->priority`, socket cookie — richer metadata than XDP
- TCX supports stacking multiple programs; `TCX_NEXT` passes to next in chain
- Use `bpf_skb_store_bytes` / `bpf_l3_csum_replace` to modify headers

---

## sk_skb (Socket Buffer Stream)

Two-stage pipeline for intercepting TCP streams at the socket level. The stream_parser frames the data; stream_verdict decides what to do with each frame.

**When to use it:**
- TCP stream framing and redirection
- protocol-aware socket processing built around `SOCKMAP`

```c
SEC("sk_skb/stream_parser")
int handle_stream_parser(struct __sk_buff *skb) {
    // return the length of the current message frame
    return skb->len;
}

SEC("sk_skb/stream_verdict")
int handle_stream_verdict(struct __sk_buff *skb) {
    // redirect to another socket, or pass/drop
    return SK_PASS;
}
```

**Attaching:**
```c
// Requires a SOCKMAP to bind programs together
struct {
    __uint(type, BPF_MAP_TYPE_SOCKMAP);
    __type(key, int);
    __type(value, int);
    __uint(max_entries, 1);
} sock_map SEC(".maps");

// Userspace — attach via bpf_prog_attach
bpf_prog_attach(parser_fd, map_fd, BPF_SK_SKB_STREAM_PARSER, 0);
bpf_prog_attach(verdict_fd, map_fd, BPF_SK_SKB_STREAM_VERDICT, 0);
```

**Notes:**
- Use for protocol-aware socket redirection (e.g., Envoy sidecar acceleration)
- Works only on TCP sockets added to a SOCKMAP
- `stream_parser` must return the byte length of a complete message

---

## sk_msg (Socket Message)

Intercepts `sendmsg` calls. Can redirect messages between sockets without copying through userspace.

**When to use it:**
- send-path socket redirection
- zero-copy socket-to-socket forwarding

```c
SEC("sk_msg")
int handle_skmsg(struct sk_msg_md *msg) {
    // inspect msg->data / msg->data_end
    // bpf_msg_redirect_map to redirect to another socket
    return SK_PASS;
}
```

**Notes:**
- Attach to a SOCKMAP or SOCKHASH via `bpf_prog_attach` with `BPF_SK_MSG_VERDICT`
- `bpf_msg_redirect_map(msg, &sock_map, key, 0)` redirects to the socket at `key`
- Zero-copy path: bypasses kernel TCP stack for socket-to-socket forwarding

---

## sk_lookup (Socket Lookup)

Overrides which socket receives an incoming packet. Runs during the kernel's socket lookup phase.

**When to use it:**
- custom incoming socket selection
- transparent service routing based on packet metadata

```c
SEC("sk_lookup")
int handle_sklookup(struct bpf_sk_lookup *ctx) {
    struct bpf_sock *sk;

    // look up a socket and assign it
    sk = bpf_map_lookup_elem(&sock_map, &ctx->local_port);
    if (sk) {
        bpf_sk_assign(ctx, sk, 0);
        bpf_sk_release(sk);
        return SK_PASS;
    }
    return SK_PASS;
}
```

**Attaching:**
```bash
bpftool cgroup attach /sys/fs/cgroup/unified sk_lookup id <prog_id>
```

**Notes:**
- Useful for wildcard port handling — one program can route to different sockets based on custom logic
- `bpf_sk_assign` must be followed by `bpf_sk_release` to release the reference
- Attach to a cgroup, affects all sockets in that cgroup

---

## sk_reuseport

Load-balance incoming connections across `SO_REUSEPORT` sockets. Replaces the kernel's default hash-based selection.

**When to use it:**
- custom load balancing within a reuseport group
- reuseport-aware selection or migration logic

```c
SEC("sk_reuseport")
int handle_sk_reuseport(struct sk_reuseport_md *ctx) {
    // ctx->hash, ctx->len, ctx->data available
    // bpf_sk_select_reuseport to pick a socket
    return SK_PASS;
}

// Migrate connections from closing sockets
SEC("sk_reuseport/migrate")
int handle_sk_reuseport_migrate(struct sk_reuseport_md *ctx) {
    return SK_PASS;
}
```

**Notes:**
- Requires `SO_REUSEPORT` on all participating sockets
- Attach via `setsockopt(SO_ATTACH_REUSEPORT_EBPF)`
- `/migrate` variant handles connection migration when a socket leaves the group

---

## flow_dissector

Provides custom flow key extraction for traffic classification. Replaces the kernel's built-in flow dissector.

**When to use it:**
- custom flow-key extraction for classification-heavy networking stacks
- environments where kernel-default flow dissection is not enough

```c
SEC("flow_dissector")
int handle_dissector(struct __sk_buff *skb) {
    // populate flow key fields
    return BPF_OK;
}
```

**Notes:**
- Attach to root network namespace via `bpf_prog_attach` with `BPF_FLOW_DISSECTOR`
- Used by TC, RSS, and other kernel subsystems that need flow keys
- Only one flow dissector can be active at a time per netns

---

## netfilter

Integrates eBPF into the netfilter framework. Runs at standard netfilter hook points.

**When to use it:**
- netfilter integration is explicitly required
- hook ordering relative to netfilter matters
- you are already operating in a netfilter-oriented architecture

```c
SEC("netfilter")
int do_netfilter(struct bpf_nf_ctx *ctx) {
    // ctx->skb available for packet inspection
    return NF_ACCEPT;
}
```

**Return codes:** `NF_ACCEPT`, `NF_DROP`, `NF_STOLEN`

**Notes:**
- Attach via `bpf_program__attach_netfilter()` (libbpf) specifying hook, priority, and flags
- Available since kernel 6.4
- Less common than XDP/TC — use when you need netfilter hook ordering guarantees
