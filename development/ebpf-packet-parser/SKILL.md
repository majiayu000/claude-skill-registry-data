---
name: ebpf-packet-parser
description: Generate verifier-safe packet parsing logic for eBPF programs including bounds checking, header extraction (Ethernet, IPv4/IPv6, TCP/UDP, ICMP), protocol identification, and proper pointer arithmetic. Use when implementing packet inspection or manipulation in CNFs.
---

# eBPF Packet Parser Skill

This skill generates production-ready, verifier-safe packet parsing code for eBPF programs used in CNFs.

## What This Skill Does

Generates eBPF C code for:
1. Safe packet data pointer management
2. Bounds checking before header access (verifier requirement)
3. Ethernet frame parsing
4. IPv4 and IPv6 header extraction
5. TCP, UDP, ICMP protocol parsing
6. IPv4-Mapped IPv6 address handling (RFC4291)
7. Port and flag extraction
8. Packet type filtering (broadcast/multicast)

## When to Use

- Implementing packet inspection in CNFs
- Adding protocol-specific processing (TCP, UDP, ICMP)
- Extracting flow information (5-tuple)
- Building packet filters or classifiers
- Implementing L3/L4 processing logic
- Need verifier-compliant parsing patterns

## Supported Protocols

### Layer 2
- Ethernet (802.3)

### Layer 3
- IPv4
- IPv6
- ARP (basic support)

### Layer 4
- TCP (with flag extraction)
- UDP
- ICMP/ICMPv6

## Information to Gather

Ask the user:

1. **Context Type**: What context? (`xdp_md`, `__sk_buff`, etc.)
2. **Protocols Needed**: Which protocols to parse? (IPv4, IPv6, TCP, UDP, ICMP)
3. **Data Extraction**: What data to extract? (IPs, ports, flags, payload)
4. **Filtering**: Any packet filtering? (skip broadcast, specific protocols)
5. **Output Format**: Store in struct, write to map, send to ringbuf?

## Core Parsing Patterns

### 1. Pointer Setup and Bounds Checking

For XDP (`xdp_md`):
```c
void *data = (void *)(long)ctx->data;
void *data_end = (void *)(long)ctx->data_end;

// Bounds check before accessing
if (data + sizeof(struct ethhdr) > data_end)
    return XDP_DROP;
```

For TC/tcx (`__sk_buff`):
```c
// Ensure data is linear (pulled into contiguous memory)
if (bpf_skb_pull_data(skb, 0) < 0)
    return TC_ACT_OK;

void *data = (void *)(long)skb->data;
void *data_end = (void *)(long)skb->data_end;

// Skip broadcast/multicast if needed
if (skb->pkt_type == PACKET_BROADCAST || skb->pkt_type == PACKET_MULTICAST)
    return TC_ACT_OK;

if (data + sizeof(struct ethhdr) > data_end)
    return TC_ACT_OK;
```

### 2. Ethernet Header Parsing

```c
#include <linux/if_ether.h>

struct ethhdr *eth = data;

// Bounds check already done above
// Access EtherType to determine L3 protocol
__u16 eth_proto = bpf_ntohs(eth->h_proto);

switch (eth_proto) {
case ETH_P_IP:
    // IPv4 processing
    break;
case ETH_P_IPV6:
    // IPv6 processing
    break;
case ETH_P_ARP:
    // ARP processing
    break;
default:
    return XDP_PASS; // Unknown protocol
}
```

### 3. IPv4 Header Parsing

```c
#include <linux/ip.h>

struct iphdr *ip;
__u32 ip_offset = sizeof(struct ethhdr);

// Bounds check
if (data + ip_offset + sizeof(struct iphdr) > data_end)
    return XDP_DROP;

ip = data + ip_offset;

// Extract IPv4 fields
__u32 src_ip = ip->saddr;
__u32 dst_ip = ip->daddr;
__u8 protocol = ip->protocol;
__u8 ttl = ip->ttl;
__u16 tot_len = bpf_ntohs(ip->tot_len);

// Calculate IP header length (IHL field is in 32-bit words)
__u8 ihl = ip->ihl;
if (ihl < 5)
    return XDP_DROP; // Invalid header length

__u32 l4_offset = ip_offset + (ihl * 4);

// Process L4 protocols
switch (protocol) {
case IPPROTO_TCP:
    // TCP processing
    break;
case IPPROTO_UDP:
    // UDP processing
    break;
case IPPROTO_ICMP:
    // ICMP processing
    break;
default:
    return XDP_PASS;
}
```

### 4. IPv6 Header Parsing

```c
#include <linux/ipv6.h>
#include <linux/in6.h>

struct ipv6hdr *ipv6;
__u32 ip_offset = sizeof(struct ethhdr);

// Bounds check
if (data + ip_offset + sizeof(struct ipv6hdr) > data_end)
    return XDP_DROP;

ipv6 = data + ip_offset;

// Extract IPv6 fields
struct in6_addr src_ip = ipv6->saddr;
struct in6_addr dst_ip = ipv6->daddr;
__u8 next_hdr = ipv6->nexthdr;
__u8 hop_limit = ipv6->hop_limit;

// L4 offset (IPv6 header is fixed 40 bytes)
__u32 l4_offset = ip_offset + sizeof(struct ipv6hdr);

// Note: This simplified version doesn't handle extension headers
// Production code should iterate through extension headers

switch (next_hdr) {
case IPPROTO_TCP:
    // TCP processing
    break;
case IPPROTO_UDP:
    // UDP processing
    break;
case IPPROTO_ICMPV6:
    // ICMPv6 processing
    break;
default:
    return XDP_PASS;
}
```

### 5. TCP Header Parsing

```c
#include <linux/tcp.h>

struct tcphdr *tcp;

// Bounds check
if (data + l4_offset + sizeof(struct tcphdr) > data_end)
    return XDP_DROP;

tcp = data + l4_offset;

// Extract TCP fields
__be16 src_port = tcp->source;  // Big endian
__be16 dst_port = tcp->dest;    // Big endian
__u32 seq = bpf_ntohl(tcp->seq);
__u32 ack_seq = bpf_ntohl(tcp->ack_seq);

// Extract TCP flags
__u8 syn = tcp->syn;
__u8 ack = tcp->ack;
__u8 fin = tcp->fin;
__u8 rst = tcp->rst;
__u8 psh = tcp->psh;

// Calculate TCP header length (doff is in 32-bit words)
__u8 doff = tcp->doff;
if (doff < 5)
    return XDP_DROP; // Invalid header length

__u32 payload_offset = l4_offset + (doff * 4);

// Access payload if needed
if (data + payload_offset > data_end)
    return XDP_DROP;

// Payload starts at: data + payload_offset
```

### 6. UDP Header Parsing

```c
#include <linux/udp.h>

struct udphdr *udp;

// Bounds check
if (data + l4_offset + sizeof(struct udphdr) > data_end)
    return XDP_DROP;

udp = data + l4_offset;

// Extract UDP fields
__be16 src_port = udp->source;  // Big endian
__be16 dst_port = udp->dest;    // Big endian
__u16 len = bpf_ntohs(udp->len);

// UDP payload starts immediately after header
__u32 payload_offset = l4_offset + sizeof(struct udphdr);

if (data + payload_offset > data_end)
    return XDP_DROP;

// Payload starts at: data + payload_offset
```

### 7. ICMP Parsing

```c
#include <linux/icmp.h>
#include <linux/icmpv6.h>

// For ICMPv4
struct icmphdr *icmp;

if (data + l4_offset + sizeof(struct icmphdr) > data_end)
    return XDP_DROP;

icmp = data + l4_offset;

__u8 type = icmp->type;
__u8 code = icmp->code;

// For ICMPv6
struct icmp6hdr *icmpv6;

if (data + l4_offset + sizeof(struct icmp6hdr) > data_end)
    return XDP_DROP;

icmpv6 = data + l4_offset;

__u8 type = icmpv6->icmp6_type;
__u8 code = icmpv6->icmp6_code;
```

## Complete Parsing Template

### Unified IPv4/IPv6 Parser with 5-Tuple Extraction

This pattern uses IPv4-Mapped IPv6 addresses (RFC4291) to unify handling:

```c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/in.h>
#include <linux/in6.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

// Flow tuple structure
struct flow_tuple {
    struct in6_addr src_ip;  // Unified IPv4/IPv6
    struct in6_addr dst_ip;
    __be16 src_port;
    __be16 dst_port;
    __u8 protocol;
};

static __always_inline int parse_packet(void *data, void *data_end, struct flow_tuple *flow) {
    // Initialize flow
    __builtin_memset(flow, 0, sizeof(*flow));

    // Parse Ethernet
    if (data + sizeof(struct ethhdr) > data_end)
        return -1;

    struct ethhdr *eth = data;
    __u16 eth_proto = bpf_ntohs(eth->h_proto);
    __u32 l3_offset = sizeof(struct ethhdr);
    __u32 l4_offset;

    // Parse L3
    switch (eth_proto) {
    case ETH_P_IP: {
        if (data + l3_offset + sizeof(struct iphdr) > data_end)
            return -1;

        struct iphdr *ip = data + l3_offset;

        // Store IPv4 as IPv4-mapped IPv6 (::ffff:x.x.x.x)
        flow->src_ip.in6_u.u6_addr32[2] = bpf_htonl(0xffff);
        flow->src_ip.in6_u.u6_addr32[3] = ip->saddr;
        flow->dst_ip.in6_u.u6_addr32[2] = bpf_htonl(0xffff);
        flow->dst_ip.in6_u.u6_addr32[3] = ip->daddr;

        flow->protocol = ip->protocol;

        l4_offset = l3_offset + (ip->ihl * 4);
        break;
    }
    case ETH_P_IPV6: {
        if (data + l3_offset + sizeof(struct ipv6hdr) > data_end)
            return -1;

        struct ipv6hdr *ipv6 = data + l3_offset;

        flow->src_ip = ipv6->saddr;
        flow->dst_ip = ipv6->daddr;
        flow->protocol = ipv6->nexthdr;

        l4_offset = l3_offset + sizeof(struct ipv6hdr);
        break;
    }
    default:
        return -1; // Unsupported protocol
    }

    // Parse L4
    switch (flow->protocol) {
    case IPPROTO_TCP: {
        if (data + l4_offset + sizeof(struct tcphdr) > data_end)
            return -1;

        struct tcphdr *tcp = data + l4_offset;
        flow->src_port = tcp->source;
        flow->dst_port = tcp->dest;
        break;
    }
    case IPPROTO_UDP: {
        if (data + l4_offset + sizeof(struct udphdr) > data_end)
            return -1;

        struct udphdr *udp = data + l4_offset;
        flow->src_port = udp->source;
        flow->dst_port = udp->dest;
        break;
    }
    default:
        // For ICMP, ports are 0
        break;
    }

    return 0; // Success
}
```

## Usage in eBPF Program

```c
SEC("xdp")
int xdp_parser(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct flow_tuple flow;
    if (parse_packet(data, data_end, &flow) < 0)
        return XDP_PASS; // Parsing failed

    // Now use the flow data
    bpf_printk("Proto: %d, Src Port: %d, Dst Port: %d",
               flow.protocol,
               bpf_ntohs(flow.src_port),
               bpf_ntohs(flow.dst_port));

    return XDP_PASS;
}
```

## Important Verifier Requirements

1. **Always bounds check before dereferencing pointers**
2. **Use `static __always_inline`** for helper functions (prevents function calls)
3. **Avoid loops or use bounded loops** with `#pragma unroll`
4. **Use `__builtin_memset`** for structure initialization
5. **Be careful with pointer arithmetic** - always check bounds after calculating offsets

## CO-RE (Compile Once, Run Everywhere)

For portable eBPF programs that work across kernel versions, use CO-RE with vmlinux.h:

### Setup

```c
//go:build ignore

#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <bpf/bpf_core_read.h>

#define ETH_P_IPV6 0x86DD
```

Generate vmlinux.h once:
```bash
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

### Using BPF_CORE_READ

For portable field access across kernel versions:

```c
// Direct access (works but not portable)
event->next_header = ip6->nexthdr;

// CO-RE portable access
event->next_header = BPF_CORE_READ(ip6, nexthdr);
event->payload_len = bpf_ntohs(BPF_CORE_READ(ip6, payload_len));
event->hop_limit = BPF_CORE_READ(ip6, hop_limit);
```

### Complete CO-RE IPv6 Parser Example

```c
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <bpf/bpf_core_read.h>

#define ETH_P_IPV6 0x86DD

struct ipv6_event {
    __u8 src_addr[16];
    __u8 dst_addr[16];
    __u8 next_header;
    __u16 payload_len;
    __u8 hop_limit;
} __attribute__((packed));

static __always_inline int parse_ipv6(struct __sk_buff *skb,
                                       struct ipv6_event *event) {
    void *data_end = (void *)(long)skb->data_end;
    void *data = (void *)(long)skb->data;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return -1;

    if (eth->h_proto != bpf_htons(ETH_P_IPV6))
        return -1;

    struct ipv6hdr *ip6 = (void *)(eth + 1);
    if ((void *)(ip6 + 1) > data_end)
        return -1;

    // Use __builtin_memcpy for address arrays
    __builtin_memcpy(event->src_addr, &ip6->saddr, 16);
    __builtin_memcpy(event->dst_addr, &ip6->daddr, 16);

    // Use BPF_CORE_READ for portable field access
    event->next_header = BPF_CORE_READ(ip6, nexthdr);
    event->payload_len = bpf_ntohs(BPF_CORE_READ(ip6, payload_len));
    event->hop_limit = BPF_CORE_READ(ip6, hop_limit);

    return 0;
}
```

**When to use CO-RE:**
- Programs that must run on multiple kernel versions
- Using kernel types that may change between versions
- Production deployments across heterogeneous systems

**When direct access is fine:**
- Single kernel version deployment
- Standard network headers (ethhdr, iphdr, ipv6hdr)
- Development/testing on known kernel

## Common Pitfalls

- Forgetting bounds checks (verifier will reject)
- Not handling variable-length headers (IPv4 IHL, TCP options)
- Incorrect offset calculations
- Not using `bpf_ntohs`/`bpf_ntohl` for network byte order
- Accessing context fields that don't exist for the program type

## Best Practices

- Create reusable parsing functions with `static __always_inline`
- Use helper functions to keep code modular
- Add debug prints with `bpf_printk()` during development
- Test with various packet types (IPv4, IPv6, fragmented, etc.)
- Handle edge cases (malformed packets, invalid headers)
- Document expected packet formats