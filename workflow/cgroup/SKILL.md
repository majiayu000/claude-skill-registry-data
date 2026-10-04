---
name: cgroup
description: cgroup. Use when you need help with cgroup.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: program-types
---

# Cgroup Program Types

All cgroup programs attach to a cgroup directory and affect all sockets/processes within that cgroup (and its descendants unless overridden).

## Related Guidance

- For cross-kernel compatibility checks, see `workflows/testing.md`.
- These hooks operate on real kernel objects such as cgroups, sockets, and sysctl state. If a context field or object behavior is unclear, consult Linux kernel source and kernel docs directly.

## Quick Choice

- Use `cgroup_skb` for coarse per-cgroup packet policy.
- Use `cgroup/connect` or `cgroup/bind` for address rewrite and transparent redirect workflows.
- Use `cgroup/sendmsg` / `cgroup/recvmsg` for UDP address rewriting.
- Use `cgroup/sockopt` or `cgroup/sysctl` for policy over socket options and sysctls.
- Use `cgroup/dev` for device access control.
- Use `sockops` for TCP lifecycle insight and tuning.

**Attach with bpftool:**
```bash
bpftool cgroup attach /sys/fs/cgroup/<path> <attach_type> id <prog_id>
bpftool cgroup detach /sys/fs/cgroup/<path> <attach_type> id <prog_id>
bpftool cgroup list /sys/fs/cgroup/<path>
```

---

## cgroup_skb — Packet Filtering per Cgroup

Filter ingress/egress packets for all sockets in a cgroup. Return `1` to pass, `0` to drop.

**When to use it:**
- coarse packet allow/deny by cgroup
- accounting or classification at the cgroup boundary

```c
SEC("cgroup_skb/ingress")
int handle_ingress(struct __sk_buff *skb) {
    return SK_PASS;  // or 1
}

SEC("cgroup_skb/egress")
int handle_egress(struct __sk_buff *skb) {
    return SK_PASS;
}
```

**Attach types:** `ingress`, `egress`

**Notes:**
- Cannot modify packet headers (read-only `skb`)
- Use for per-cgroup network accounting or coarse filtering

---

## cgroup/sock — Socket Lifecycle

Called on socket creation and release. Return `1` to allow, `0` to deny.

**When to use it:**
- socket create/release policy
- lightweight socket lifecycle observation at cgroup scope

```c
SEC("cgroup/sock_create")
int handle_sock_create(struct bpf_sock *ctx) {
    // ctx->family, ctx->type, ctx->protocol available
    return 1;  // allow
}

SEC("cgroup/sock_release")
int handle_sock_release(struct bpf_sock *ctx) {
    return 1;
}

// Called after bind() completes — can inspect the bound address
SEC("cgroup/post_bind4")
int handle_post_bind4(struct bpf_sock *ctx) {
    return 1;
}

SEC("cgroup/post_bind6")
int handle_post_bind6(struct bpf_sock *ctx) {
    return 1;
}
```

**Notes:**
- `sock_create` runs before the socket is fully initialized — limited fields available
- Denying (`return 0`) causes the syscall to return `-EPERM`

---

## cgroup/bind — Override Bind Address

Intercepts `bind()` calls. Can rewrite the address the socket binds to.

**When to use it:**
- bind-time address policy
- forcing or rewriting bind destinations

```c
SEC("cgroup/bind4")
int handle_bind4(struct bpf_sock_addr *ctx) {
    // ctx->user_ip4, ctx->user_port — can be rewritten
    return 1;  // allow (after any rewrites)
}

SEC("cgroup/bind6")
int handle_bind6(struct bpf_sock_addr *ctx) {
    return 1;
}
```

**Notes:**
- Write to `ctx->user_ip4` / `ctx->user_port` to redirect the bind
- Return `0` to block the bind entirely (`-EPERM`)

---

## cgroup/connect — Intercept connect()

Intercepts `connect()` calls. Can transparently redirect connections to a different address (e.g., service mesh transparent proxy).

**When to use it:**
- transparent proxying
- service-mesh-style connect redirection
- outbound connect policy by cgroup

```c
SEC("cgroup/connect4")
int handle_connect4(struct bpf_sock_addr *ctx) {
    // rewrite destination: ctx->user_ip4, ctx->user_port
    return 1;
}

SEC("cgroup/connect6")
int handle_connect6(struct bpf_sock_addr *ctx) {
    return 1;
}

SEC("cgroup/connect_unix")
int handle_connect_unix(struct bpf_sock_addr *ctx) {
    return 1;
}
```

**Notes:**
- This is how Cilium and Istio implement transparent proxying without iptables
- Write `ctx->user_ip4` and `ctx->user_port` to redirect to a different endpoint
- Original destination is preserved in the socket for the proxy to query

---

## cgroup/sendmsg — Intercept sendmsg()

Intercepts UDP `sendmsg()`. Can rewrite the destination address of outgoing datagrams.

**When to use it:**
- UDP destination rewrite on send path
- cgroup-scoped datagram policy

```c
SEC("cgroup/sendmsg4")
int handle_sendmsg4(struct bpf_sock_addr *ctx) {
    return 1;
}

SEC("cgroup/sendmsg6")
int handle_sendmsg6(struct bpf_sock_addr *ctx) {
    return 1;
}
```

**Notes:**
- Same `bpf_sock_addr` context as connect — field rewrites work identically
- Only fires for UDP (connected and unconnected send)

---

## cgroup/recvmsg — Intercept recvmsg()

Intercepts UDP `recvmsg()`. Can rewrite the apparent source address seen by the application.

**When to use it:**
- UDP source rewrite on receive path
- cgroup-scoped recvmsg mediation

```c
SEC("cgroup/recvmsg4")
int handle_recvmsg4(struct bpf_sock_addr *ctx) {
    return 1;
}

SEC("cgroup/recvmsg6")
int handle_recvmsg6(struct bpf_sock_addr *ctx) {
    return 1;
}
```

---

## cgroup/sockopt — Override Socket Options

Intercepts `getsockopt()` and `setsockopt()`. Can filter, replace, or synthesize socket option values.

**When to use it:**
- enforcing or virtualizing socket options
- policy that needs to inspect or override sockopt behavior

```c
SEC("cgroup/getsockopt")
int handle_getsockopt(struct bpf_sockopt *ctx) {
    // ctx->level, ctx->optname, ctx->optval, ctx->optlen
    // rewrite ctx->optval to change what the app sees
    ctx->retval = 0;
    return 1;
}

SEC("cgroup/setsockopt")
int handle_setsockopt(struct bpf_sockopt *ctx) {
    // intercept and modify socket options being set
    return 1;
}
```

**Notes:**
- `ctx->optval` points to a kernel buffer; use `bpf_probe_read_kernel` to read it
- Set `ctx->retval = 0` to override the return code seen by the application
- Useful for enforcing socket option policies across a cgroup

---

## cgroup/sysctl — Control sysctl Access

Intercepts reads and writes to sysctl variables for processes in a cgroup.

**When to use it:**
- per-cgroup sysctl access control
- policy around sysctl reads and writes in containerized environments

```c
SEC("cgroup/sysctl")
int handle_sysctl(struct bpf_sysctl *ctx) {
    // ctx->write: 1 if write, 0 if read
    // ctx->current_value, ctx->new_value
    return 1;  // allow; return 0 to deny
}
```

**Notes:**
- Return `0` to deny the sysctl access with `-EPERM`
- `ctx->current_value` is a string representation
- Useful for enforcing per-container sysctl policies

---

## cgroup/dev — Device Access Control

Controls access to character and block devices for processes in a cgroup. Equivalent to cgroup v1 `devices` controller but more flexible.

**When to use it:**
- device allow/deny policy for containers or service groups
- replacing cgroup v1 device rules with BPF logic

```c
SEC("cgroup/dev")
int handle_dev(struct bpf_cgroup_dev_ctx *ctx) {
    // ctx->access_type: BPF_DEVCG_ACC_READ, BPF_DEVCG_ACC_WRITE, BPF_DEVCG_ACC_MKNOD
    // ctx->major, ctx->minor: device numbers
    // ctx->type: BPF_DEVCG_DEV_CHAR or BPF_DEVCG_DEV_BLOCK
    return 0;  // 0 = deny, 1 = allow
}
```

**Notes:**
- Return `1` to allow, `0` to deny (opposite of most cgroup programs)
- Replaces cgroup v1 device whitelist/blacklist
- Useful for container runtimes to restrict device access

---

## sockops — TCP Connection Events

Receives callbacks at key TCP lifecycle events. Used to inspect and tune TCP socket parameters.

**When to use it:**
- TCP lifecycle tuning
- RTT/retransmission observation
- congestion-control related policy or socket tuning

```c
SEC("sockops")
int handle_sockops(struct bpf_sock_ops *ctx) {
    switch (ctx->op) {
    case BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB:
        // outgoing connection established — set TCP options
        bpf_sock_ops_cb_flags_set(ctx, BPF_SOCK_OPS_RETRANS_CB_FLAG);
        break;
    case BPF_SOCK_OPS_PASSIVE_ESTABLISHED_CB:
        // incoming connection established
        break;
    case BPF_SOCK_OPS_RETRANS_CB:
        // retransmission occurred
        break;
    }
    return 1;
}
```

**Common `ctx->op` values:**
| Op | When |
|----|------|
| `BPF_SOCK_OPS_TCP_CONNECT_CB` | Active connect initiated |
| `BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB` | Outgoing connection established |
| `BPF_SOCK_OPS_PASSIVE_ESTABLISHED_CB` | Incoming connection established |
| `BPF_SOCK_OPS_NEEDS_ECN` | ECN negotiation |
| `BPF_SOCK_OPS_RETRANS_CB` | Retransmission (must be enabled via flags) |
| `BPF_SOCK_OPS_STATE_CB` | TCP state change |

**Attaching:**
```bash
bpftool cgroup attach /sys/fs/cgroup/unified sock_ops id <prog_id>
```

**Notes:**
- Use `bpf_sock_ops_cb_flags_set` to opt into additional callbacks (retransmit, RTT, state)
- Can call `bpf_setsockopt` to tune TCP parameters (window size, congestion control, etc.)
- Cilium uses this for TCP acceleration between co-located pods

### Real pattern: congestion control + TCP socket introspection

```c
SEC("sockops")
int handle_sockops(struct bpf_sock_ops *ctx) {
    if (ctx->op != BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB &&
        ctx->op != BPF_SOCK_OPS_PASSIVE_ESTABLISHED_CB)
        return 1;

    // Switch to BBR on connections within the same /20 subnet
    if (ctx->family == AF_INET) {
        __u32 local  = bpf_ntohl(ctx->local_ip4);
        __u32 remote = bpf_ntohl(ctx->remote_ip4);
        if ((local & 0xfffff000) == (remote & 0xfffff000)) {
            char cong[] = "bbr";
            bpf_setsockopt(ctx, SOL_TCP, TCP_CONGESTION, &cong, sizeof(cong));
        }
    }

    // Opt into RTT callbacks for latency tracking
    bpf_sock_ops_cb_flags_set(ctx, ctx->bpf_sock_ops_cb_flags |
                                   BPF_SOCK_OPS_RTT_CB_FLAG);
    return 1;
}

// Access detailed TCP stats via bpf_tcp_sock
SEC("sockops")
int handle_rtt(struct bpf_sock_ops *ctx) {
    if (ctx->op != BPF_SOCK_OPS_RTT_CB) return 1;

    struct bpf_tcp_sock *tcp = bpf_tcp_sock(ctx->sk);
    if (!tcp) return 1;

    bpf_printk("srtt=%u loss=%u retrans=%u\n",
               tcp->srtt_us, tcp->lost_out, tcp->total_retrans);
    return 1;
}
```

**Additional `ctx->op` values:**
| Op | Enable flag |
|----|-------------|
| `BPF_SOCK_OPS_RTT_CB` | `BPF_SOCK_OPS_RTT_CB_FLAG` |
| `BPF_SOCK_OPS_RETRANS_CB` | `BPF_SOCK_OPS_RETRANS_CB_FLAG` |
| `BPF_SOCK_OPS_STATE_CB` | `BPF_SOCK_OPS_STATE_CB_FLAG` |
| `BPF_SOCK_OPS_RTO_CB` | `BPF_SOCK_OPS_RTO_CB_FLAG` |
