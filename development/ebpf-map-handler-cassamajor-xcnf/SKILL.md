---
name: ebpf-map-handler
description: Create eBPF maps (hash, array, ringbuf, LRU, per-CPU) with corresponding Go userspace code for reading and writing data between kernel and userspace. Includes map definitions, update/lookup operations, and event handling. Use when implementing state management or kernel-userspace communication in CNFs.
---

# eBPF Map Handler Skill

This skill generates eBPF map definitions and corresponding Go code for kernel-userspace data exchange in CNFs.

## What This Skill Does

Generates code for:
1. eBPF map definitions in C
2. Go code to interact with maps
3. Map operations (lookup, update, delete, iterate)
4. Ringbuf/perf event handling
5. Per-CPU map handling
6. Map-in-map patterns
7. Proper error handling and cleanup

## When to Use

- Storing state in eBPF programs (connection tracking, rate limiting)
- Passing data from kernel to userspace (metrics, events)
- Configuration from userspace to kernel (rules, policies)
- Sharing data between eBPF programs
- Implementing flow tables or caches
- Real-time event streaming

## Supported Map Types

### Hash Maps
- **BPF_MAP_TYPE_HASH**: General key-value storage
- **BPF_MAP_TYPE_LRU_HASH**: Automatic LRU eviction
- **BPF_MAP_TYPE_HASH_OF_MAPS**: Hash table of maps
- **BPF_MAP_TYPE_LRU_PERCPU_HASH**: Per-CPU LRU hash

### Array Maps
- **BPF_MAP_TYPE_ARRAY**: Fixed-size array
- **BPF_MAP_TYPE_PERCPU_ARRAY**: Per-CPU array
- **BPF_MAP_TYPE_ARRAY_OF_MAPS**: Array of maps

### Special Maps
- **BPF_MAP_TYPE_RINGBUF**: Ring buffer (kernel 5.8+, preferred)
- **BPF_MAP_TYPE_PERF_EVENT_ARRAY**: Perf events (legacy)
- **BPF_MAP_TYPE_QUEUE**: FIFO queue
- **BPF_MAP_TYPE_STACK**: LIFO stack

## Information to Gather

Ask the user:

1. **Use Case**: What is the map for? (state, events, config, metrics)
2. **Map Type**: Which type? (hash, array, ringbuf, etc.)
3. **Key/Value Structure**: What data structures?
4. **Size**: How many entries?
5. **Update Pattern**: Who updates? (kernel→user, user→kernel, both)
6. **Concurrency**: Per-CPU needed?

## Map Definitions in C

### 1. Hash Map for Flow Tracking

```c
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

// Key: 5-tuple flow identifier
struct flow_key {
    __u32 src_ip;
    __u32 dst_ip;
    __u16 src_port;
    __u16 dst_port;
    __u8 protocol;
} __attribute__((packed));

// Value: Flow statistics
struct flow_stats {
    __u64 packets;
    __u64 bytes;
    __u64 first_seen;
    __u64 last_seen;
};

struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 10000);
    __type(key, struct flow_key);
    __type(value, struct flow_stats);
} flow_table SEC(".maps");

// Usage in eBPF program
SEC("xdp")
int track_flows(struct xdp_md *ctx) {
    struct flow_key key = {0};
    // ... parse packet to fill key ...

    struct flow_stats *stats = bpf_map_lookup_elem(&flow_table, &key);
    if (stats) {
        // Existing flow - update stats
        __sync_fetch_and_add(&stats->packets, 1);
        __sync_fetch_and_add(&stats->bytes, ctx->data_end - ctx->data);
        stats->last_seen = bpf_ktime_get_ns();
    } else {
        // New flow - insert
        struct flow_stats new_stats = {
            .packets = 1,
            .bytes = ctx->data_end - ctx->data,
            .first_seen = bpf_ktime_get_ns(),
            .last_seen = bpf_ktime_get_ns(),
        };
        bpf_map_update_elem(&flow_table, &key, &new_stats, BPF_ANY);
    }

    return XDP_PASS;
}
```

### 2. Array Map for Per-Interface Counters

```c
#define MAX_INTERFACES 256

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, MAX_INTERFACES);
    __type(key, __u32);
    __type(value, __u64);
} interface_counters SEC(".maps");

SEC("xdp")
int count_packets(struct xdp_md *ctx) {
    __u32 ifindex = ctx->ingress_ifindex;
    __u64 *counter = bpf_map_lookup_elem(&interface_counters, &ifindex);

    if (counter)
        __sync_fetch_and_add(counter, 1);

    return XDP_PASS;
}
```

### 3. Ring Buffer for Events

```c
// Event structure sent to userspace
struct packet_event {
    __u32 src_ip;
    __u32 dst_ip;
    __u16 src_port;
    __u16 dst_port;
    __u8 protocol;
    __u64 timestamp;
};

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024); // 256 KB
} events SEC(".maps");

SEC("xdp")
int capture_events(struct xdp_md *ctx) {
    // ... parse packet ...

    // Reserve space in ring buffer
    struct packet_event *event = bpf_ringbuf_reserve(&events, sizeof(*event), 0);
    if (!event)
        return XDP_PASS;

    // Fill event data
    event->src_ip = /* ... */;
    event->dst_ip = /* ... */;
    event->src_port = /* ... */;
    event->dst_port = /* ... */;
    event->protocol = /* ... */;
    event->timestamp = bpf_ktime_get_ns();

    // Submit to userspace
    bpf_ringbuf_submit(event, 0);

    return XDP_PASS;
}
```

### 4. Per-CPU Hash Map for High-Performance Counters

```c
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_HASH);
    __uint(max_entries, 1024);
    __type(key, __u32);
    __type(value, __u64);
} percpu_stats SEC(".maps");

SEC("xdp")
int percpu_count(struct xdp_md *ctx) {
    __u32 key = 0; // Global counter key
    __u64 *value = bpf_map_lookup_elem(&percpu_stats, &key);

    if (value)
        *value += 1; // No atomic ops needed - per-CPU!

    return XDP_PASS;
}
```

### 5. Configuration Map (Userspace → Kernel)

```c
struct config {
    __u32 rate_limit;
    __u32 timeout_ms;
    __u8 enabled;
};

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct config);
} cnf_config SEC(".maps");

SEC("xdp")
int rate_limiter(struct xdp_md *ctx) {
    __u32 key = 0;
    struct config *cfg = bpf_map_lookup_elem(&cnf_config, &key);

    if (!cfg || !cfg->enabled)
        return XDP_PASS;

    // Use cfg->rate_limit for rate limiting logic
    // ...

    return XDP_PASS;
}
```

## Go Userspace Code

### 1. Reading from Hash Map

```go
package main

import (
    "fmt"
    "log"
    "encoding/binary"

    "github.com/cilium/ebpf"
)

// Must match C struct exactly
type FlowKey struct {
    SrcIP    uint32
    DstIP    uint32
    SrcPort  uint16
    DstPort  uint16
    Protocol uint8
    _        [3]byte // Padding for alignment
}

type FlowStats struct {
    Packets   uint64
    Bytes     uint64
    FirstSeen uint64
    LastSeen  uint64
}

func readFlowTable(flowMap *ebpf.Map) error {
    var (
        key   FlowKey
        value FlowStats
    )

    // Iterate over all entries
    iter := flowMap.Iterate()
    for iter.Next(&key, &value) {
        fmt.Printf("Flow: %d.%d.%d.%d:%d -> %d.%d.%d.%d:%d proto=%d packets=%d bytes=%d\n",
            byte(key.SrcIP), byte(key.SrcIP>>8), byte(key.SrcIP>>16), byte(key.SrcIP>>24), key.SrcPort,
            byte(key.DstIP), byte(key.DstIP>>8), byte(key.DstIP>>16), byte(key.DstIP>>24), key.DstPort,
            key.Protocol, value.Packets, value.Bytes)
    }

    if err := iter.Err(); err != nil {
        return fmt.Errorf("iterator error: %w", err)
    }

    return nil
}

// Lookup specific flow
func lookupFlow(flowMap *ebpf.Map, key FlowKey) (*FlowStats, error) {
    var stats FlowStats
    if err := flowMap.Lookup(&key, &stats); err != nil {
        return nil, fmt.Errorf("lookup failed: %w", err)
    }
    return &stats, nil
}

// Delete flow
func deleteFlow(flowMap *ebpf.Map, key FlowKey) error {
    if err := flowMap.Delete(&key); err != nil {
        return fmt.Errorf("delete failed: %w", err)
    }
    return nil
}
```

### 2. Writing Configuration to Map

```go
type Config struct {
    RateLimit uint32
    TimeoutMs uint32
    Enabled   uint8
    _         [3]byte // Padding
}

func updateConfig(configMap *ebpf.Map, cfg Config) error {
    key := uint32(0)
    if err := configMap.Put(&key, &cfg); err != nil {
        return fmt.Errorf("config update failed: %w", err)
    }
    log.Printf("Config updated: rate_limit=%d, timeout=%dms, enabled=%d",
        cfg.RateLimit, cfg.TimeoutMs, cfg.Enabled)
    return nil
}

// Usage
func main() {
    // ... load eBPF objects ...

    cfg := Config{
        RateLimit: 1000,
        TimeoutMs: 5000,
        Enabled:   1,
    }

    if err := updateConfig(objs.CnfConfig, cfg); err != nil {
        log.Fatal(err)
    }
}
```

### 3. Reading from Ring Buffer

```go
import (
    "bytes"
    "encoding/binary"
    "log"
    "os"
    "os/signal"
    "syscall"

    "github.com/cilium/ebpf/ringbuf"
)

type PacketEvent struct {
    SrcIP     uint32
    DstIP     uint32
    SrcPort   uint16
    DstPort   uint16
    Protocol  uint8
    _         [3]byte // Padding
    Timestamp uint64
}

func readRingBuffer(eventsMap *ebpf.Map) error {
    // Open ring buffer reader
    rd, err := ringbuf.NewReader(eventsMap)
    if err != nil {
        return fmt.Errorf("opening ringbuf reader: %w", err)
    }
    defer rd.Close()

    log.Println("Listening for events...")

    // Handle Ctrl+C
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        <-sig
        log.Println("Shutting down...")
        rd.Close()
    }()

    // Read events
    for {
        record, err := rd.Read()
        if err != nil {
            if errors.Is(err, ringbuf.ErrClosed) {
                return nil
            }
            return fmt.Errorf("reading from ringbuf: %w", err)
        }

        // Parse event
        var event PacketEvent
        if err := binary.Read(bytes.NewReader(record.RawSample), binary.LittleEndian, &event); err != nil {
            log.Printf("parsing event: %v", err)
            continue
        }

        log.Printf("Event: %d.%d.%d.%d:%d -> %d.%d.%d.%d:%d proto=%d ts=%d",
            byte(event.SrcIP), byte(event.SrcIP>>8), byte(event.SrcIP>>16), byte(event.SrcIP>>24), event.SrcPort,
            byte(event.DstIP), byte(event.DstIP>>8), byte(event.DstIP>>16), byte(event.DstIP>>24), event.DstPort,
            event.Protocol, event.Timestamp)
    }
}
```

### 4. Reading Per-CPU Maps

```go
func readPerCPUMap(m *ebpf.Map) error {
    var (
        key    uint32 = 0
        values []uint64
    )

    // Lookup returns slice with one value per CPU
    if err := m.Lookup(&key, &values); err != nil {
        return fmt.Errorf("lookup failed: %w", err)
    }

    // Sum across all CPUs
    var total uint64
    for cpu, val := range values {
        log.Printf("CPU %d: %d", cpu, val)
        total += val
    }

    log.Printf("Total across all CPUs: %d", total)
    return nil
}
```

### 5. Reading Array Map

```go
func readInterfaceCounters(countersMap *ebpf.Map) error {
    var (
        key   uint32
        value uint64
    )

    // Read all interface counters
    for ifindex := uint32(0); ifindex < 256; ifindex++ {
        key = ifindex
        if err := countersMap.Lookup(&key, &value); err != nil {
            continue // Skip non-existent entries
        }

        if value > 0 {
            log.Printf("Interface %d: %d packets", ifindex, value)
        }
    }

    return nil
}
```

## Complete Example: Flow Tracker CNF

### C Code (bytecode/flow.c)

```c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

struct flow_key {
    __u32 src_ip;
    __u32 dst_ip;
    __u16 src_port;
    __u16 dst_port;
    __u8 protocol;
} __attribute__((packed));

struct flow_stats {
    __u64 packets;
    __u64 bytes;
    __u64 first_seen;
    __u64 last_seen;
};

struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 10000);
    __type(key, struct flow_key);
    __type(value, struct flow_stats);
} flows SEC(".maps");

SEC("xdp")
int track_flows(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    // Parse packet (simplified - see packet-parser skill)
    struct flow_key key = {0};
    // ... fill key from packet ...

    struct flow_stats *stats = bpf_map_lookup_elem(&flows, &key);
    if (stats) {
        __sync_fetch_and_add(&stats->packets, 1);
        __sync_fetch_and_add(&stats->bytes, (__u64)(data_end - data));
        stats->last_seen = bpf_ktime_get_ns();
    } else {
        struct flow_stats new_stats = {
            .packets = 1,
            .bytes = (__u64)(data_end - data),
            .first_seen = bpf_ktime_get_ns(),
            .last_seen = bpf_ktime_get_ns(),
        };
        bpf_map_update_elem(&flows, &key, &new_stats, BPF_NOEXIST);
    }

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
```

### Go Code (main.go)

```go
package main

import (
    "log"
    "time"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

//go:generate go tool bpf2go -type flow_key -type flow_stats Flow flow.c

func main() {
    // Load eBPF program
    spec, err := LoadFlow()
    if err != nil {
        log.Fatalf("loading spec: %v", err)
    }

    objs := &FlowObjects{}
    if err := spec.LoadAndAssign(objs, nil); err != nil {
        log.Fatalf("loading objects: %v", err)
    }
    defer objs.Close()

    // Attach to interface
    iface, _ := net.InterfaceByName("eth0")
    l, err := link.AttachXDP(link.XDPOptions{
        Program:   objs.TrackFlows,
        Interface: iface.Index,
    })
    if err != nil {
        log.Fatalf("attaching XDP: %v", err)
    }
    defer l.Close()

    // Periodically dump flows
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        log.Println("=== Active Flows ===")

        var (
            key   FlowKey
            stats FlowStats
        )

        iter := objs.Flows.Iterate()
        for iter.Next(&key, &stats) {
            log.Printf("Flow: packets=%d bytes=%d duration=%dms",
                stats.Packets, stats.Bytes,
                (stats.LastSeen-stats.FirstSeen)/1000000)
        }

        if err := iter.Err(); err != nil {
            log.Printf("iteration error: %v", err)
        }
    }
}
```

## Map-Based Policy Configuration

Maps are ideal for implementing dynamic routing policies, firewall rules, and other configuration that needs to be updated from userspace without reloading the eBPF program.

### Use Case: Source-Based Routing Policy

**Scenario:** Route packets to different next-hops based on their source IP address.

### C Map Definition

```c
// Routing policy record
struct route_policy {
    __u32 interface_id;  // Output interface index
    __u32 next_hop;      // Next hop IP address (network byte order)
};

// Map: Source IP → Routing Policy
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u32);   // Source IPv4 address
    __type(value, struct route_policy);
    __uint(max_entries, 1024);
} policy_routes SEC(".maps");

// eBPF program that uses the policy map
SEC("tc")
int apply_routing_policy(struct __sk_buff *skb) {
    // ... parse packet to get source IP ...
    __u32 src_ip = iph->saddr;

    // Look up policy
    struct route_policy *policy = bpf_map_lookup_elem(&policy_routes, &src_ip);
    if (!policy)
        return TC_ACT_OK;  // No policy, use normal routing

    // Apply policy (see ebpf-packet-redirect skill)
    struct bpf_redir_neigh nh = {
        .nh_family = AF_INET,
        .ipv4_nh = policy->next_hop,
    };

    return bpf_redirect_neigh(policy->interface_id, &nh, sizeof(nh), 0);
}
```

### Go Policy Management

```go
package main

import (
    "encoding/binary"
    "fmt"
    "net"

    "github.com/cilium/ebpf"
)

//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -type route_policy PolicyRouter router.c

type RoutingPolicy struct {
    SourceIP  net.IP
    Interface string
    NextHop   net.IP
}

// Add routing policy to map
func addRoutingPolicy(m *ebpf.Map, policy RoutingPolicy) error {
    // Get interface index
    iface, err := net.InterfaceByName(policy.Interface)
    if err != nil {
        return fmt.Errorf("interface not found: %w", err)
    }

    // Convert source IP to map key (network byte order)
    srcIP := policy.SourceIP.To4()
    if srcIP == nil {
        return fmt.Errorf("invalid IPv4 address: %s", policy.SourceIP)
    }
    key := binary.BigEndian.Uint32(srcIP)

    // Convert next hop to network byte order
    nextHopIP := policy.NextHop.To4()
    if nextHopIP == nil {
        return fmt.Errorf("invalid next hop: %s", policy.NextHop)
    }
    nextHop := binary.BigEndian.Uint32(nextHopIP)

    // Create policy value
    value := PolicyRouterRoutePolicy{
        InterfaceId: uint32(iface.Index),
        NextHop:     nextHop,
    }

    // Insert into map
    if err := m.Put(&key, &value); err != nil {
        return fmt.Errorf("failed to add policy: %w", err)
    }

    return nil
}

// Remove routing policy from map
func removeRoutingPolicy(m *ebpf.Map, sourceIP net.IP) error {
    srcIP := sourceIP.To4()
    if srcIP == nil {
        return fmt.Errorf("invalid IPv4 address: %s", sourceIP)
    }
    key := binary.BigEndian.Uint32(srcIP)

    if err := m.Delete(&key); err != nil {
        return fmt.Errorf("failed to remove policy: %w", err)
    }

    return nil
}

// List all routing policies
func listRoutingPolicies(m *ebpf.Map) ([]RoutingPolicy, error) {
    var (
        key   uint32
        value PolicyRouterRoutePolicy
        policies []RoutingPolicy
    )

    iter := m.Iterate()
    for iter.Next(&key, &value) {
        // Convert key (uint32) back to IP
        srcIP := make(net.IP, 4)
        binary.BigEndian.PutUint32(srcIP, key)

        // Convert next hop back to IP
        nextHopIP := make(net.IP, 4)
        binary.BigEndian.PutUint32(nextHopIP, value.NextHop)

        // Get interface name
        iface, err := net.InterfaceByIndex(int(value.InterfaceId))
        if err != nil {
            continue // Skip if interface no longer exists
        }

        policies = append(policies, RoutingPolicy{
            SourceIP:  srcIP,
            Interface: iface.Name,
            NextHop:   nextHopIP,
        })
    }

    if err := iter.Err(); err != nil {
        return nil, fmt.Errorf("iteration error: %w", err)
    }

    return policies, nil
}

// Update policy (atomic replace)
func updateRoutingPolicy(m *ebpf.Map, policy RoutingPolicy) error {
    // Map updates are atomic, so just add with same key
    return addRoutingPolicy(m, policy)
}
```

### Usage Example

```go
func main() {
    // Load eBPF program
    spec, _ := LoadPolicyRouter()
    objs := &PolicyRouterObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    // Attach to interface...

    // Configure routing policies
    policies := []RoutingPolicy{
        {
            SourceIP:  net.ParseIP("192.168.100.5"),
            Interface: "eth1",
            NextHop:   net.ParseIP("10.0.1.1"),
        },
        {
            SourceIP:  net.ParseIP("10.10.1.100"),
            Interface: "eth2",
            NextHop:   net.ParseIP("10.0.2.1"),
        },
    }

    for _, policy := range policies {
        if err := addRoutingPolicy(objs.PolicyRoutes, policy); err != nil {
            log.Fatalf("adding policy: %v", err)
        }
        log.Printf("Added policy: %s via %s → %s",
            policy.SourceIP, policy.Interface, policy.NextHop)
    }

    // Later: update a policy dynamically
    updatePolicy := RoutingPolicy{
        SourceIP:  net.ParseIP("192.168.100.5"),
        Interface: "eth3",  // Changed interface
        NextHop:   net.ParseIP("10.0.3.1"),
    }
    updateRoutingPolicy(objs.PolicyRoutes, updatePolicy)

    // List all active policies
    activePolicies, _ := listRoutingPolicies(objs.PolicyRoutes)
    for _, p := range activePolicies {
        log.Printf("Active: %s → %s via %s", p.SourceIP, p.NextHop, p.Interface)
    }

    // Remove a policy
    removeRoutingPolicy(objs.PolicyRoutes, net.ParseIP("10.10.1.100"))
}
```

### Dynamic Policy Updates

One of the key advantages of map-based configuration is **dynamic updates without reloading**:

```go
// API endpoint to add routing policy
func handleAddPolicy(w http.ResponseWriter, r *http.Request) {
    var policy RoutingPolicy
    json.NewDecoder(r.Body).Decode(&policy)

    if err := addRoutingPolicy(policyMap, policy); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    w.WriteHeader(http.StatusCreated)
}

// Watch for configuration changes
func watchConfigChanges(configFile string, policyMap *ebpf.Map) {
    watcher, _ := fsnotify.NewWatcher()
    watcher.Add(configFile)

    for {
        select {
        case event := <-watcher.Events:
            if event.Op&fsnotify.Write == fsnotify.Write {
                // Reload and update policies
                policies := loadPoliciesFromFile(configFile)
                for _, p := range policies {
                    updateRoutingPolicy(policyMap, p)
                }
            }
        }
    }
}
```

### Other Policy Use Cases

**1. Firewall Rules:**
```go
type FirewallRule struct {
    SrcIP     net.IP
    DstIP     net.IP
    DstPort   uint16
    Protocol  uint8
    Action    uint8  // ALLOW or DROP
}
```

**2. Rate Limiting:**
```go
type RateLimitPolicy struct {
    SourceIP    net.IP
    MaxRate     uint32  // Packets per second
    BurstSize   uint32
}
```

**3. QoS / Traffic Shaping:**
```go
type QoSPolicy struct {
    FlowID      uint64
    Priority    uint8
    Bandwidth   uint32  // Kbps
}
```

**4. NAT Configuration:**
```go
type NATPolicy struct {
    InternalIP  net.IP
    ExternalIP  net.IP
    Port        uint16
}
```

### Best Practices for Policy Maps

1. **Use network byte order** for IP addresses in keys/values
2. **Validate policies** before inserting into map
3. **Check interface existence** before adding policies
4. **Log policy changes** for auditing
5. **Provide atomic updates** (update entire policy, not partial)
6. **Implement list/get operations** for visibility
7. **Handle map full errors** gracefully
8. **Version your policy structures** for upgrades
9. **Use LRU maps** if policies should auto-expire
10. **Document policy semantics** clearly

## Best Practices

1. **Match struct layout exactly** between C and Go (use `__attribute__((packed))`)
2. **Use atomic operations** when updating shared counters (`__sync_fetch_and_add`)
3. **Check return values** from map operations
4. **Use LRU maps** when entries should auto-expire
5. **Use ringbuf over perf events** (better performance, kernel 5.8+)
6. **Use per-CPU maps** for high-frequency updates
7. **Handle iteration errors** properly in Go
8. **Close readers** with defer
9. **Size maps appropriately** (affects memory usage)
10. **Use `-type` flag** in bpf2go to generate Go structs automatically

## Common Pitfalls

- Struct padding mismatches between C and Go
- Forgetting to check map operation return values
- Not using atomic operations for concurrent updates
- Ring buffer size too small (events dropped)
- Not handling iteration errors
- Memory leaks from not closing readers/links