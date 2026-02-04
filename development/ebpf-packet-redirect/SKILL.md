---
name: ebpf-packet-redirect
description: Implement packet redirection and routing in eBPF programs using bpf_redirect and bpf_redirect_neigh helpers. Includes source-based policy routing, map-based routing tables, load balancing, and CNF router patterns. Use when building routers, gateways, load balancers, or any CNF that needs to control packet forwarding paths.
---

# eBPF Packet Redirect Skill

This skill provides comprehensive guidance for implementing packet redirection and routing in eBPF-based CNFs.

## What This Skill Does

Generates code for:
1. Basic packet redirection with `bpf_redirect`
2. Neighbor-aware redirection with `bpf_redirect_neigh`
3. Source-based policy routing
4. Map-based routing tables
5. Dynamic route updates from userspace
6. Load balancing across multiple paths
7. Complete CNF router implementations

## When to Use

- Building software routers or gateways
- Implementing source-based policy routing
- Creating load balancers
- Handling virtual IPs or anycast addresses
- Building service mesh sidecars
- Solving asymmetric routing problems
- Implementing multi-homing or multiple ISP scenarios
- Creating VPN/tunnel endpoints with custom routing

## Redirection Helpers Comparison

### bpf_redirect - Basic Redirection

```c
long bpf_redirect(u32 ifindex, u64 flags);
```

**What it does:**
- Changes output interface only
- You must handle everything else:
  - MAC address rewriting
  - ARP/NDP resolution
  - Route lookups
  - Next-hop determination

**Use when:**
- Redirecting within same L2 domain
- You control all network configuration
- Simple interface switching needed

**Example:**
```c
SEC("xdp")
int xdp_redirect_simple(struct xdp_md *ctx) {
    // Get interface
    struct net_device *eth1 = /* ... */;

    // Simple redirect to eth1
    return bpf_redirect(eth1->ifindex, 0);
}
```

### bpf_redirect_neigh - Neighbor-Aware Redirection (Preferred)

```c
long bpf_redirect_neigh(u32 ifindex, struct bpf_redir_neigh *params,
                        int plen, u64 flags);
```

**What it does:**
- **Automatic ARP/NDP resolution** - Handles neighbor discovery
- **Route lookup** - Finds next hop automatically
- **MAC rewriting** - Updates Ethernet headers
- **Gateway-aware** - Can forward through routers

**Advantages:**
- ✅ Full routing stack in eBPF
- ✅ Handles all L2/L3 details
- ✅ Production-ready forwarding
- ✅ Works across L3 boundaries

**Use when:**
- Building routers or gateways (most CNF use cases)
- Need L3 forwarding capability
- Want automatic neighbor resolution
- Forwarding across subnets

**Structure:**
```c
struct bpf_redir_neigh {
    __u32 nh_family;    // AF_INET or AF_INET6
    union {
        __be32 ipv4_nh;     // IPv4 next hop
        __u32 ipv6_nh[4];   // IPv6 next hop
    };
};
```

## Source-Based Policy Routing

### The Problem: Asymmetric Routing

**Scenario:**
```
Client (10.0.2.2)
  ↓
Router (10.0.2.1 / 10.0.1.1) [eBPF CNF]
  ↓
Server (10.0.1.2)
  - Default gateway: 192.168.0.1
  - Virtual IP: 192.168.100.5 on lo
```

**Issue:**
1. Client → 192.168.100.5 (server's virtual IP)
2. Router forwards to server ✅
3. Server replies, but routing table says "use default gateway"
4. Reply goes to 192.168.0.1 instead of back through router ❌
5. **Connection fails - asymmetric routing**

**eBPF Solution:** Attach program to server's egress that redirects based on **source IP**

### Complete CNF Router Example

#### C Code - eBPF Router (kernel space)

```c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/pkt_cls.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

// Routing policy record
struct route_policy {
    __u32 interface_id;  // Output interface
    __u32 next_hop;      // Next hop IP (network byte order)
};

// Map: Source IP → Routing Policy
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);   // Source IPv4 address
    __type(value, struct route_policy);
    __uint(max_entries, 1024);
} policy_routes_v4 SEC(".maps");

// Statistics
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, __u64);
    __uint(max_entries, 3);
} stats SEC(".maps");

#define STAT_TOTAL_PACKETS   0
#define STAT_POLICY_MATCHES  1
#define STAT_REDIRECTS       2

static __always_inline void update_stat(__u32 key) {
    __u64 *counter = bpf_map_lookup_elem(&stats, &key);
    if (counter)
        __sync_fetch_and_add(counter, 1);
}

SEC("tc")
int policy_router(struct __sk_buff *skb) {
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;

    update_stat(STAT_TOTAL_PACKETS);

    // Bounds check for Ethernet header
    if (data + sizeof(struct ethhdr) > data_end)
        return TC_ACT_OK;

    struct ethhdr *eth = data;

    // Only handle IPv4
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return TC_ACT_OK;

    // Bounds check for IP header
    if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) > data_end)
        return TC_ACT_OK;

    struct iphdr *iph = data + sizeof(struct ethhdr);

    // Look up source-based policy
    __u32 src_key = iph->saddr;  // Already in network byte order
    struct route_policy *policy = bpf_map_lookup_elem(&policy_routes_v4, &src_key);

    if (!policy) {
        // No policy match, use normal routing
        return TC_ACT_OK;
    }

    update_stat(STAT_POLICY_MATCHES);

    // Apply policy routing with neighbor-aware redirect
    struct bpf_redir_neigh nh = {
        .nh_family = AF_INET,
        .ipv4_nh = policy->next_hop,  // Already in network byte order
    };

    long ret = bpf_redirect_neigh(policy->interface_id, &nh, sizeof(nh), 0);

    if (ret == TC_ACT_REDIRECT) {
        update_stat(STAT_REDIRECTS);

        // Debug logging
        bpf_printk("Policy redirect: src=%pI4 iface=%d nexthop=%pI4",
                   &iph->saddr, policy->interface_id, &policy->next_hop);
    }

    return ret;
}

char _license[] SEC("license") = "GPL";
```

#### Go Code - Policy Configuration (userspace)

```go
package main

import (
    "encoding/binary"
    "fmt"
    "log"
    "net"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -type route_policy PolicyRouter policy_router.c

type RoutingPolicy struct {
    SourceIP  net.IP
    Interface string
    NextHop   net.IP
}

func main() {
    // Load eBPF program
    spec, err := LoadPolicyRouter()
    if err != nil {
        log.Fatalf("loading spec: %v", err)
    }

    objs := &PolicyRouterObjects{}
    if err := spec.LoadAndAssign(objs, nil); err != nil {
        log.Fatalf("loading objects: %v", err)
    }
    defer objs.Close()

    // Attach to default gateway interface (egress)
    iface, err := net.InterfaceByName("eth0")
    if err != nil {
        log.Fatalf("finding interface: %v", err)
    }

    l, err := link.AttachTCX(link.TCXOptions{
        Program:   objs.PolicyRouter,
        Attach:    ebpf.AttachTCXEgress,
        Interface: iface.Index,
    })
    if err != nil {
        log.Fatalf("attaching program: %v", err)
    }
    defer l.Close()

    log.Printf("Policy router attached to %s egress", iface.Name)

    // Configure routing policies
    policies := []RoutingPolicy{
        {
            SourceIP:  net.ParseIP("192.168.100.5"),
            Interface: "eth1",
            NextHop:   net.ParseIP("10.0.1.1"),
        },
        // Add more policies as needed
    }

    for _, policy := range policies {
        if err := addRoutingPolicy(objs.PolicyRoutesV4, policy); err != nil {
            log.Fatalf("adding policy: %v", err)
        }
        log.Printf("Added policy: %s via %s (next hop %s)",
            policy.SourceIP, policy.Interface, policy.NextHop)
    }

    // Monitor statistics
    go monitorStats(objs.Stats)

    // Wait for signal
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    <-sig

    log.Println("Shutting down policy router...")
}

func addRoutingPolicy(m *ebpf.Map, policy RoutingPolicy) error {
    // Get interface index
    iface, err := net.InterfaceByName(policy.Interface)
    if err != nil {
        return fmt.Errorf("interface %s not found: %w", policy.Interface, err)
    }

    // Convert source IP to key (network byte order)
    srcIP := policy.SourceIP.To4()
    if srcIP == nil {
        return fmt.Errorf("invalid IPv4 address: %s", policy.SourceIP)
    }
    key := binary.BigEndian.Uint32(srcIP)

    // Convert next hop to network byte order
    nextHopIP := policy.NextHop.To4()
    if nextHopIP == nil {
        return fmt.Errorf("invalid next hop IPv4 address: %s", policy.NextHop)
    }
    nextHop := binary.BigEndian.Uint32(nextHopIP)

    // Create policy record
    value := PolicyRouterRoutePolicy{
        InterfaceId: uint32(iface.Index),
        NextHop:     nextHop,
    }

    // Insert into map
    if err := m.Put(&key, &value); err != nil {
        return fmt.Errorf("map insert failed: %w", err)
    }

    return nil
}

func removeRoutingPolicy(m *ebpf.Map, sourceIP net.IP) error {
    srcIP := sourceIP.To4()
    if srcIP == nil {
        return fmt.Errorf("invalid IPv4 address: %s", sourceIP)
    }
    key := binary.BigEndian.Uint32(srcIP)

    if err := m.Delete(&key); err != nil {
        return fmt.Errorf("map delete failed: %w", err)
    }

    return nil
}

func monitorStats(m *ebpf.Map) {
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        var (
            key   uint32
            value uint64
        )

        // Read statistics
        stats := make(map[string]uint64)

        key = 0 // STAT_TOTAL_PACKETS
        if err := m.Lookup(&key, &value); err == nil {
            stats["total_packets"] = value
        }

        key = 1 // STAT_POLICY_MATCHES
        if err := m.Lookup(&key, &value); err == nil {
            stats["policy_matches"] = value
        }

        key = 2 // STAT_REDIRECTS
        if err := m.Lookup(&key, &value); err == nil {
            stats["redirects"] = value
        }

        log.Printf("Stats: total=%d matches=%d redirects=%d",
            stats["total_packets"], stats["policy_matches"], stats["redirects"])
    }
}
```

## Use Cases

### 1. Virtual IP / Anycast Handling

```go
// Server has 192.168.100.5 on loopback
// Route traffic from this IP via specific interface
policy := RoutingPolicy{
    SourceIP:  net.ParseIP("192.168.100.5"),
    Interface: "eth1",
    NextHop:   net.ParseIP("10.0.1.1"),
}
```

### 2. Multi-Homing / Multiple ISPs

```go
// Route customer A traffic via ISP 1
addRoutingPolicy(map, RoutingPolicy{
    SourceIP:  net.ParseIP("10.10.1.0"), // Customer A subnet
    Interface: "isp1",
    NextHop:   net.ParseIP("203.0.113.1"),
})

// Route customer B traffic via ISP 2
addRoutingPolicy(map, RoutingPolicy{
    SourceIP:  net.ParseIP("10.10.2.0"), // Customer B subnet
    Interface: "isp2",
    NextHop:   net.ParseIP("198.51.100.1"),
})
```

### 3. Service Mesh Sidecar

```go
// Pod has multiple interfaces:
// - Service traffic → service network
// - Management traffic → management network

servicePolicies := []RoutingPolicy{
    {
        SourceIP:  net.ParseIP("10.96.0.10"),  // Service IP
        Interface: "net1",
        NextHop:   net.ParseIP("10.96.0.1"),
    },
    {
        SourceIP:  net.ParseIP("192.168.1.10"), // Management IP
        Interface: "net0",
        NextHop:   net.ParseIP("192.168.1.1"),
    },
}
```

### 4. VPN / Tunnel Endpoint

```go
// Traffic from tunnel IPs → tunnel interface
addRoutingPolicy(map, RoutingPolicy{
    SourceIP:  net.ParseIP("172.16.0.0"),  // VPN subnet
    Interface: "tun0",
    NextHop:   net.ParseIP("172.16.0.1"),
})
```

## Advanced Patterns

### Load Balancing Across Multiple Paths

```c
#define MAX_BACKENDS 4

struct backend {
    __u32 interface_id;
    __u32 next_hop;
    __u32 weight;  // For weighted load balancing
};

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, struct backend);
    __uint(max_entries, MAX_BACKENDS);
} backends SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, __u32);
    __uint(max_entries, 1);
} backend_count SEC(".maps");

static __always_inline struct backend *select_backend() {
    __u32 key = 0;
    __u32 *count = bpf_map_lookup_elem(&backend_count, &key);
    if (!count || *count == 0)
        return NULL;

    // Round-robin selection
    __u32 idx = bpf_get_prandom_u32() % (*count);
    return bpf_map_lookup_elem(&backends, &idx);
}

SEC("tc")
int load_balancer(struct __sk_buff *skb) {
    // ... parse packet ...

    struct backend *backend = select_backend();
    if (!backend)
        return TC_ACT_OK;

    struct bpf_redir_neigh nh = {
        .nh_family = AF_INET,
        .ipv4_nh = backend->next_hop,
    };

    return bpf_redirect_neigh(backend->interface_id, &nh, sizeof(nh), 0);
}
```

### Conditional Routing Based on Multiple Criteria

```c
// Route based on source IP + destination port
struct policy_key {
    __u32 src_ip;
    __u16 dst_port;
    __u8 protocol;
    __u8 _pad;
} __attribute__((packed));

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, struct policy_key);
    __type(value, struct route_policy);
    __uint(max_entries, 1024);
} complex_policies SEC(".maps");

SEC("tc")
int complex_router(struct __sk_buff *skb) {
    // ... parse packet to get IP + TCP/UDP ...

    struct policy_key key = {
        .src_ip = iph->saddr,
        .dst_port = tcp->dest,  // or udp->dest
        .protocol = iph->protocol,
    };

    struct route_policy *policy = bpf_map_lookup_elem(&complex_policies, &key);
    // ... redirect based on policy ...
}
```

### Policy Chaining (Fallback Policies)

```c
SEC("tc")
int chained_router(struct __sk_buff *skb) {
    struct iphdr *iph = /* ... parse ... */;
    struct route_policy *policy = NULL;

    // Try source-based policy first
    policy = bpf_map_lookup_elem(&src_policies, &iph->saddr);

    // Fall back to destination-based policy
    if (!policy)
        policy = bpf_map_lookup_elem(&dst_policies, &iph->daddr);

    // Fall back to default route
    if (!policy) {
        __u32 default_key = 0;
        policy = bpf_map_lookup_elem(&default_route, &default_key);
    }

    if (!policy)
        return TC_ACT_OK;

    // Apply policy
    struct bpf_redir_neigh nh = {
        .nh_family = AF_INET,
        .ipv4_nh = policy->next_hop,
    };

    return bpf_redirect_neigh(policy->interface_id, &nh, sizeof(nh), 0);
}
```

## IPv6 Support

```c
// IPv6 routing policy
struct route_policy_v6 {
    __u32 interface_id;
    __u32 next_hop[4];  // IPv6 address (16 bytes)
};

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, struct in6_addr);  // IPv6 source address
    __type(value, struct route_policy_v6);
    __uint(max_entries, 1024);
} policy_routes_v6 SEC(".maps");

SEC("tc")
int policy_router_v6(struct __sk_buff *skb) {
    // ... parse IPv6 packet ...

    struct ipv6hdr *ip6h = /* ... */;

    struct route_policy_v6 *policy = bpf_map_lookup_elem(&policy_routes_v6, &ip6h->saddr);
    if (!policy)
        return TC_ACT_OK;

    struct bpf_redir_neigh nh = {
        .nh_family = AF_INET6,
    };
    __builtin_memcpy(nh.ipv6_nh, policy->next_hop, sizeof(nh.ipv6_nh));

    return bpf_redirect_neigh(policy->interface_id, &nh, sizeof(nh), 0);
}
```

## Return Value Handling

### TC Return Values for Redirection

```c
// Success
TC_ACT_REDIRECT  // Successfully redirected

// Errors
TC_ACT_OK        // Continue normal processing
TC_ACT_SHOT      // Drop packet
```

### Error Handling Pattern

```c
long ret = bpf_redirect_neigh(ifindex, &nh, sizeof(nh), 0);

if (ret != TC_ACT_REDIRECT) {
    // Log failure
    bpf_printk("Redirect failed: ifindex=%d ret=%ld", ifindex, ret);

    // Increment error counter
    __u32 key = STAT_REDIRECT_ERRORS;
    __u64 *counter = bpf_map_lookup_elem(&stats, &key);
    if (counter)
        __sync_fetch_and_add(counter, 1);

    // Fall back to normal routing
    return TC_ACT_OK;
}

return ret;
```

## Best Practices

1. **Always validate interfaces exist** before adding policies
2. **Use network byte order** for IP addresses in maps
3. **Add statistics** to monitor policy effectiveness
4. **Implement fallback** to normal routing if no policy matches
5. **Log redirections** during development (remove in production)
6. **Bounds check** before accessing packet data
7. **Use bpf_redirect_neigh** for L3 forwarding (handles ARP/MAC automatically)
8. **Test with real network topologies** (not just localhost)
9. **Monitor for redirect failures** and investigate root causes
10. **Document your policies** in userspace code comments

## Common Pitfalls

- Forgetting to attach to **egress** (not ingress) for source-based routing
- Using host byte order instead of network byte order in maps
- Not handling the case where policy lookup fails
- Redirecting without checking if interface is up
- Not validating that next hop is reachable
- Forgetting IPv6 support if dual-stack
- Not implementing statistics/monitoring

## Debugging

### Enable Debug Logging

```c
// In eBPF program
bpf_printk("Redirect: src=%pI4 dst=%pI4 iface=%d",
           &iph->saddr, &iph->daddr, policy->interface_id);
```

### View Logs

```bash
# Using tc
sudo tc exec bpf dbg

# Or using bpftool
sudo bpftool prog tracelog

# Or directly
sudo cat /sys/kernel/debug/tracing/trace_pipe
```

### Check Redirect Stats

```bash
# View eBPF program stats
bpftool prog show

# Check map contents
bpftool map dump name policy_routes_v4
```

### Verify Interface and Routes

```bash
# Check interface is up
ip link show eth1

# Verify next hop is reachable
ip route get 10.0.1.1
```

## Integration with Other Skills

- **ebpf-packet-parser**: Use to extract flow information before routing decision
- **ebpf-map-handler**: Manage routing policy maps
- **ebpf-attach-hook**: Attach router to TC egress
- **cnf-networking**: Set up test topology with netkit/veth
- **ebpf-test-harness**: Validate routing with multi-container tests