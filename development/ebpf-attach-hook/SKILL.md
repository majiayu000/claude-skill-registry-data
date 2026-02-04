---
name: ebpf-attach-hook
description: Implement eBPF program attachment logic for various hooks (XDP, TC/tcx, netkit, kprobe, tracepoint, cgroup) with proper error handling, cleanup, and link management. Includes Go code using cilium/ebpf library. Use when attaching CNF programs to kernel hooks.
---

# eBPF Attach Hook Skill

This skill generates Go code for attaching eBPF programs to various kernel hooks in CNF applications.

## What This Skill Does

Generates code for:
1. Attaching to XDP (eXpress Data Path)
2. Attaching to TC/tcx (Traffic Control)
3. Attaching to netkit devices
4. Attaching to kprobes/kretprobes
5. Attaching to tracepoints
6. Attaching to cgroup hooks
7. Proper cleanup and error handling
8. Link management with defer patterns

## When to Use

- Attaching CNF programs to network interfaces
- Hooking into kernel functions for tracing
- Setting up packet processing pipelines
- Implementing network policies
- Creating observability tools
- Building traffic control CNFs

## Supported Hook Types

### Network Hooks
- **XDP**: Earliest packet processing (driver level)
- **TC/tcx**: Traffic control (ingress/egress)
- **netkit**: BPF-programmable network device (primary/peer)

### Tracing Hooks
- **kprobe**: Kernel function entry
- **kretprobe**: Kernel function return
- **tracepoint**: Static kernel tracepoints

### Control Hooks
- **cgroup**: Socket operations, device access
- **socket filter**: Per-socket filtering
- **SK_SKB**: Socket buffer operations

## Information to Gather

Ask the user:

1. **Hook Type**: Which hook to use? (XDP, tcx, netkit, kprobe, etc.)
2. **Interface**: Which interface (for network hooks)?
3. **Attach Point**: Ingress/egress (for TC), primary/peer (for netkit)?
4. **Program Name**: What is the eBPF program called?
5. **Cleanup**: Need signal handling for graceful shutdown?

## XDP Attachment

### XDP Modes

```go
const (
    // Generic XDP (slowest, works everywhere)
    XDPGenericMode = 1 << iota

    // Driver XDP (requires driver support)
    XDPDriverMode

    // Offload XDP (requires NIC support)
    XDPOffloadMode
)
```

### Basic XDP Attachment

```go
package main

import (
    "log"
    "net"
    "os"
    "os/signal"
    "syscall"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

func main() {
    // Load eBPF program
    spec, err := LoadMyProgram()
    if err != nil {
        log.Fatalf("loading spec: %v", err)
    }

    objs := &MyProgramObjects{}
    if err := spec.LoadAndAssign(objs, nil); err != nil {
        log.Fatalf("loading objects: %v", err)
    }
    defer objs.Close()

    // Get interface
    iface, err := net.InterfaceByName("eth0")
    if err != nil {
        log.Fatalf("finding interface: %v", err)
    }

    // Attach XDP program
    l, err := link.AttachXDP(link.XDPOptions{
        Program:   objs.XdpProgram,
        Interface: iface.Index,
        Flags:     link.XDPGenericMode, // or link.XDPDriverMode
    })
    if err != nil {
        log.Fatalf("attaching XDP: %v", err)
    }
    defer l.Close()

    log.Printf("XDP program attached to %s", iface.Name)

    // Wait for signal
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    <-sig

    log.Println("Detaching XDP program...")
}
```

### XDP with Auto-Mode Selection

```go
func attachXDP(prog *ebpf.Program, ifaceName string) (link.Link, error) {
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        return nil, fmt.Errorf("finding interface: %w", err)
    }

    // Try driver mode first, fall back to generic
    l, err := link.AttachXDP(link.XDPOptions{
        Program:   prog,
        Interface: iface.Index,
        Flags:     link.XDPDriverMode,
    })
    if err != nil {
        log.Printf("Driver mode failed, trying generic mode: %v", err)
        l, err = link.AttachXDP(link.XDPOptions{
            Program:   prog,
            Interface: iface.Index,
            Flags:     link.XDPGenericMode,
        })
        if err != nil {
            return nil, fmt.Errorf("attaching XDP: %w", err)
        }
        log.Println("Using generic XDP mode")
    } else {
        log.Println("Using driver XDP mode")
    }

    return l, nil
}
```

## TC/tcx Attachment

### tcx (Kernel 6.6+, Preferred)

```go
package main

import (
    "log"
    "net"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

func attachTCX(prog *ebpf.Program, ifaceName string, ingress bool) (link.Link, error) {
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        return nil, fmt.Errorf("finding interface: %w", err)
    }

    attach := ebpf.AttachTCXIngress
    if !ingress {
        attach = ebpf.AttachTCXEgress
    }

    l, err := link.AttachTCX(link.TCXOptions{
        Program:   prog,
        Attach:    attach,
        Interface: iface.Index,
    })
    if err != nil {
        return nil, fmt.Errorf("attaching tcx: %w", err)
    }

    direction := "ingress"
    if !ingress {
        direction = "egress"
    }
    log.Printf("tcx program attached to %s %s", iface.Name, direction)

    return l, nil
}

func main() {
    // Load program
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    // Attach to ingress
    ingressLink, err := attachTCX(objs.TcxIngress, "eth0", true)
    if err != nil {
        log.Fatal(err)
    }
    defer ingressLink.Close()

    // Attach to egress
    egressLink, err := attachTCX(objs.TcxEgress, "eth0", false)
    if err != nil {
        log.Fatal(err)
    }
    defer egressLink.Close()

    // ... wait for signal ...
}
```

### Legacy TC (Kernel < 6.6)

```go
func attachTC(prog *ebpf.Program, ifaceName string, ingress bool) (link.Link, error) {
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        return nil, fmt.Errorf("finding interface: %w", err)
    }

    attach := ebpf.AttachTCIngress
    if !ingress {
        attach = ebpf.AttachTCEgress
    }

    l, err := link.AttachTC(link.TCOptions{
        Program:   prog,
        Attach:    attach,
        Interface: iface.Index,
    })
    if err != nil {
        return nil, fmt.Errorf("attaching TC: %w", err)
    }

    return l, nil
}
```

### Auto-Detect tcx vs TC

```go
func attachTrafficControl(prog *ebpf.Program, ifaceName string, ingress bool) (link.Link, error) {
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        return nil, fmt.Errorf("finding interface: %w", err)
    }

    attach := ebpf.AttachTCXIngress
    if !ingress {
        attach = ebpf.AttachTCXEgress
    }

    // Try tcx first (kernel 6.6+)
    l, err := link.AttachTCX(link.TCXOptions{
        Program:   prog,
        Attach:    attach,
        Interface: iface.Index,
    })
    if err == nil {
        log.Println("Using tcx (modern)")
        return l, nil
    }

    // Fall back to legacy TC
    log.Printf("tcx failed, using legacy TC: %v", err)

    tcAttach := ebpf.AttachTCIngress
    if !ingress {
        tcAttach = ebpf.AttachTCEgress
    }

    l, err = link.AttachTC(link.TCOptions{
        Program:   prog,
        Attach:    tcAttach,
        Interface: iface.Index,
    })
    if err != nil {
        return nil, fmt.Errorf("attaching TC: %w", err)
    }

    log.Println("Using legacy TC")
    return l, nil
}
```

## netkit Attachment

```go
package main

import (
    "log"
    "net"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

func attachNetkit(primaryProg, peerProg *ebpf.Program, ifaceName string) (link.Link, link.Link, error) {
    iface, err := net.InterfaceByName(ifaceName)
    if err != nil {
        return nil, nil, fmt.Errorf("finding interface: %w", err)
    }

    // Attach to primary
    primaryLink, err := link.AttachNetkit(link.NetkitOptions{
        Program:   primaryProg,
        Interface: iface.Index,
        Attach:    ebpf.AttachNetkitPrimary,
    })
    if err != nil {
        return nil, nil, fmt.Errorf("attaching to primary: %w", err)
    }

    // Attach to peer
    peerLink, err := link.AttachNetkit(link.NetkitOptions{
        Program:   peerProg,
        Interface: iface.Index,
        Attach:    ebpf.AttachNetkitPeer,
    })
    if err != nil {
        primaryLink.Close()
        return nil, nil, fmt.Errorf("attaching to peer: %w", err)
    }

    log.Printf("netkit programs attached to %s (primary and peer)", iface.Name)

    return primaryLink, peerLink, nil
}

func main() {
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    primaryLink, peerLink, err := attachNetkit(
        objs.NetkitPrimary,
        objs.NetkitPeer,
        "netkit0",
    )
    if err != nil {
        log.Fatal(err)
    }
    defer primaryLink.Close()
    defer peerLink.Close()

    // ... wait for signal ...
}
```

**Tip:** When you create interfaces programmatically (e.g., `netkit.CreatePair`), use the returned index directly instead of looking up by name. See [EXAMPLES.md](EXAMPLES.md) for the pattern.

## kprobe/kretprobe Attachment

```go
package main

import (
    "log"

    "github.com/cilium/ebpf/link"
)

func attachKprobe(prog *ebpf.Program, symbol string) (link.Link, error) {
    // Attach kprobe to kernel function
    l, err := link.Kprobe(symbol, prog, nil)
    if err != nil {
        return nil, fmt.Errorf("attaching kprobe to %s: %w", symbol, err)
    }

    log.Printf("kprobe attached to %s", symbol)
    return l, nil
}

func attachKretprobe(prog *ebpf.Program, symbol string) (link.Link, error) {
    // Attach kretprobe to kernel function return
    l, err := link.Kretprobe(symbol, prog, nil)
    if err != nil {
        return nil, fmt.Errorf("attaching kretprobe to %s: %w", symbol, err)
    }

    log.Printf("kretprobe attached to %s", symbol)
    return l, nil
}

func main() {
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    // Attach to tcp_v4_connect entry
    kprobeLink, err := attachKprobe(objs.TraceTcpConnect, "tcp_v4_connect")
    if err != nil {
        log.Fatal(err)
    }
    defer kprobeLink.Close()

    // Attach to tcp_v4_connect return
    kretprobeLink, err := attachKretprobe(objs.TraceTcpConnectReturn, "tcp_v4_connect")
    if err != nil {
        log.Fatal(err)
    }
    defer kretprobeLink.Close()

    log.Println("Tracing TCP connections...")

    // ... wait for signal ...
}
```

## Tracepoint Attachment

```go
func attachTracepoint(prog *ebpf.Program, group, name string) (link.Link, error) {
    // Attach to tracepoint
    l, err := link.Tracepoint(group, name, prog, nil)
    if err != nil {
        return nil, fmt.Errorf("attaching tracepoint %s:%s: %w", group, name, err)
    }

    log.Printf("tracepoint attached to %s:%s", group, name)
    return l, nil
}

func main() {
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    // Attach to syscalls:sys_enter_execve tracepoint
    l, err := attachTracepoint(objs.TraceExecve, "syscalls", "sys_enter_execve")
    if err != nil {
        log.Fatal(err)
    }
    defer l.Close()

    log.Println("Tracing execve syscalls...")

    // ... wait for signal ...
}
```

## cgroup Attachment

```go
func attachCgroup(prog *ebpf.Program, cgroupPath string, attachType ebpf.AttachType) (link.Link, error) {
    // Open cgroup directory
    cgroupFd, err := os.Open(cgroupPath)
    if err != nil {
        return nil, fmt.Errorf("opening cgroup: %w", err)
    }
    defer cgroupFd.Close()

    // Attach to cgroup
    l, err := link.AttachCgroup(link.CgroupOptions{
        Path:    cgroupPath,
        Attach:  attachType,
        Program: prog,
    })
    if err != nil {
        return nil, fmt.Errorf("attaching to cgroup: %w", err)
    }

    log.Printf("Program attached to cgroup %s", cgroupPath)
    return l, nil
}

func main() {
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    // Attach to socket connect
    l, err := attachCgroup(
        objs.CgroupConnect,
        "/sys/fs/cgroup/unified/my-cgroup",
        ebpf.AttachCGroupInet4Connect,
    )
    if err != nil {
        log.Fatal(err)
    }
    defer l.Close()

    // ... wait for signal ...
}
```

## Multi-Interface Attachment

```go
func attachToMultipleInterfaces(prog *ebpf.Program, interfaces []string) ([]link.Link, error) {
    var links []link.Link

    for _, ifname := range interfaces {
        iface, err := net.InterfaceByName(ifname)
        if err != nil {
            // Cleanup already attached
            for _, l := range links {
                l.Close()
            }
            return nil, fmt.Errorf("finding interface %s: %w", ifname, err)
        }

        l, err := link.AttachXDP(link.XDPOptions{
            Program:   prog,
            Interface: iface.Index,
            Flags:     link.XDPGenericMode,
        })
        if err != nil {
            // Cleanup already attached
            for _, l := range links {
                l.Close()
            }
            return nil, fmt.Errorf("attaching to %s: %w", ifname, err)
        }

        links = append(links, l)
        log.Printf("Attached to %s", ifname)
    }

    return links, nil
}

func main() {
    spec, _ := LoadMyProgram()
    objs := &MyProgramObjects{}
    spec.LoadAndAssign(objs, nil)
    defer objs.Close()

    interfaces := []string{"eth0", "eth1", "wlan0"}
    links, err := attachToMultipleInterfaces(objs.XdpProgram, interfaces)
    if err != nil {
        log.Fatal(err)
    }

    // Cleanup all links
    defer func() {
        for _, l := range links {
            l.Close()
        }
    }()

    // ... wait for signal ...
}
```

## Complete CNF Example with Signal Handling

```go
package main

import (
    "context"
    "log"
    "net"
    "os"
    "os/signal"
    "syscall"

    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

//go:generate go tool bpf2go MyCNF mycnf.c

func run(ctx context.Context) error {
    // Load eBPF objects
    spec, err := LoadMyCNF()
    if err != nil {
        return fmt.Errorf("loading spec: %w", err)
    }

    objs := &MyCNFObjects{}
    if err := spec.LoadAndAssign(objs, nil); err != nil {
        return fmt.Errorf("loading objects: %w", err)
    }
    defer objs.Close()

    // Get interface
    iface, err := net.InterfaceByName("eth0")
    if err != nil {
        return fmt.Errorf("finding interface: %w", err)
    }

    // Attach XDP
    xdpLink, err := link.AttachXDP(link.XDPOptions{
        Program:   objs.XdpCnf,
        Interface: iface.Index,
        Flags:     link.XDPGenericMode,
    })
    if err != nil {
        return fmt.Errorf("attaching XDP: %w", err)
    }
    defer xdpLink.Close()

    log.Printf("CNF attached to %s", iface.Name)

    // Wait for cancellation
    <-ctx.Done()

    log.Println("Shutting down CNF...")
    return nil
}

func main() {
    // Setup signal handling
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        <-sig
        log.Println("Received shutdown signal")
        cancel()
    }()

    // Run CNF
    if err := run(ctx); err != nil {
        log.Fatalf("error: %v", err)
    }
}
```

## Best Practices

1. **Always use defer for cleanup**: `defer link.Close()`
2. **Handle errors properly**: Check all attachment errors
3. **Use context for graceful shutdown**: Especially for long-running CNFs
4. **Log attachment details**: Interface names, modes, etc.
5. **Try driver mode first**: Fall back to generic if needed
6. **Clean up on partial failure**: When attaching to multiple interfaces
7. **Use signal handling**: Allow Ctrl+C to gracefully detach
8. **Prefer tcx over legacy TC**: On kernel 6.6+
9. **Use netkit for BPF-programmable paths**: Better than veth for eBPF
10. **Test attachment before deployment**: Verify hooks work as expected

## Error Handling Patterns

```go
// Pattern 1: Cleanup on error
func attachWithCleanup() error {
    var links []link.Link
    defer func() {
        for _, l := range links {
            l.Close()
        }
    }()

    // ... attachment code ...

    return nil
}

// Pattern 2: Explicit cleanup
func attachExplicit() (link.Link, error) {
    l, err := link.AttachXDP(...)
    if err != nil {
        return nil, err
    }

    // If we fail after this, clean up
    if someCondition {
        l.Close()
        return nil, errors.New("failed")
    }

    return l, nil
}
```

## Debugging Attachment Issues

```go
// Check if program is attached
func checkAttachment(ifname string) {
    // Use bpftool in bash: bpftool net show dev eth0
    // Or use netlink to query XDP/TC status
}

// Verify link is valid
func verifyLink(l link.Link) bool {
    info, err := l.Info()
    if err != nil {
        log.Printf("Link info error: %v", err)
        return false
    }
    log.Printf("Link ID: %d, Type: %s", info.ID, info.Type)
    return true
}
```