---
name: ebpf-cnf-scaffold
description: Scaffold new eBPF-based Cloud Native Network Function (CNF) projects with proper directory structure, boilerplate C kernel code, Go userspace application, bpf2go generation, and build configuration following established patterns. Use when creating new CNF examples or starting fresh eBPF projects.
---

# eBPF CNF Scaffold Skill

This skill scaffolds complete eBPF-based CNF projects following the established patterns in this repository.

## What This Skill Does

Creates a new eBPF CNF project with:
1. Proper directory structure (`examples/{name}/`)
2. eBPF kernel program in Restricted C (`bytecode/{name}.c`)
3. Go userspace application (`main.go`)
4. bpf2go code generation setup (`bytecode/gen.go`)
5. Go module initialization
6. README with build/run instructions
7. Optional Dockerfile for containerization

## When to Use

- Creating a new CNF from scratch
- Adding a new example to the examples/ directory
- Starting a new eBPF networking project
- Need a working template that follows repository conventions

## Project Structure Created

### Basic Structure

```
examples/{name}/
├── main.go                 # Go userspace application
├── bytecode/
│   ├── gen.go             # bpf2go generation directive
│   ├── {name}.c           # eBPF kernel program (Restricted C)
│   ├── {name}_bpfel.go    # Generated (after go generate)
│   └── {name}_bpfeb.go    # Generated (after go generate)
├── go.mod                 # Go module file
├── README.md              # Build and run instructions
└── Dockerfile             # Optional containerization
```

### With Internal Packages

For complex CNFs, use subpackages to organize code:

```
examples/{name}/
├── main.go                 # Entry point, CLI, event loop
├── main_test.go           # Integration tests
├── bytecode/
│   ├── gen.go             # bpf2go generation
│   ├── vmlinux.h          # Kernel types for CO-RE
│   ├── {name}.c           # eBPF program
│   ├── {name}_bpfel.go    # Generated
│   └── {name}_bpfeb.go    # Generated
├── {subpkg}/              # Internal package
│   ├── {subpkg}.go        # Core functionality
│   ├── {subpkg}_test.go   # Unit tests
│   └── options.go         # Functional options
├── go.mod
└── README.md
```

Example from `netkit-ipv6`:
```
examples/netkit-ipv6/
├── main.go
├── main_test.go
├── bytecode/
│   ├── gen.go
│   ├── vmlinux.h
│   └── netkit_ipv6.c
├── netkit/                 # Subpackage for device management
│   ├── netkit.go          # CreatePair, Delete
│   ├── netkit_test.go
│   ├── options.go         # WithL2Mode, WithL3Mode
│   └── ipv6.go            # ConfigureIPv6LinkLocal
└── go.mod
```

Benefits of subpackages:
- Separation of concerns (bytecode generation vs device management)
- Reusable components
- Independent unit testing
- Clearer imports in main.go

## Information to Gather

Before scaffolding, ask the user:

1. **CNF Name**: What to name the CNF (lowercase, hyphens only)
2. **Hook Type**: Which eBPF hook to use (XDP, TC/tcx, netkit, kprobe, tracepoint)
3. **Functionality**: Brief description of what the CNF should do
4. **Maps Needed**: Does it need eBPF maps? (hash, array, ringbuf, etc.)
5. **Dockerfile**: Should a Dockerfile be included?

## Boilerplate Components

### 1. eBPF Program Template (bytecode/{name}.c)

```c
//go:build ignore

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

// Add appropriate headers based on hook type
// XDP: <linux/if_ether.h>, <linux/ip.h>
// TC/tcx: <linux/pkt_cls.h>
// netkit: <linux/if_link.h>

char _license[] SEC("license") = "GPL";

SEC("{hook_section}")
int {function_name}(struct {ctx_type} *ctx) {
    // TODO: Implement CNF logic
    return {return_value};
}
```

### 2. Go Generation File (bytecode/gen.go)

```go
package bytecode

//go:generate go tool bpf2go -type {types} {CapitalizedName} {name}.c -- -O2 -Wall -Werror
```

### 3. Go Userspace Application (main.go)

```go
package main

import (
    "log"
    "os"
    "os/signal"
    "syscall"

    "{module}/bytecode"
    "github.com/cilium/ebpf"
    "github.com/cilium/ebpf/link"
)

func main() {
    // Load eBPF objects
    spec, err := bytecode.Load{Name}()
    if err != nil {
        log.Fatalf("loading eBPF spec: %v", err)
    }

    objs := &bytecode.{Name}Objects{}
    if err := spec.LoadAndAssign(objs, nil); err != nil {
        log.Fatalf("loading eBPF objects: %v", err)
    }
    defer objs.Close()

    // TODO: Attach program to hook
    // TODO: Read from maps/ringbufs if needed

    log.Println("{Name} CNF is running...")

    // Wait for signal
    sig := make(chan os.Signal, 1)
    signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
    <-sig

    log.Println("Shutting down...")
}
```

### 4. README Template

````markdown
# {Name} CNF

{Description}

## Build

Compile the eBPF program:
```shell
go generate ./bytecode
```

Build the userspace application:
```shell
go build -o {name}
```

## Run

```shell
sudo ./{name}
```

## Test

```shell
sudo -E go test .
```
````

## Hook-Specific Configuration

### XDP
- Section: `SEC("xdp")`
- Context: `struct xdp_md *ctx`
- Return values: `XDP_PASS`, `XDP_DROP`, `XDP_TX`, `XDP_REDIRECT`, `XDP_ABORTED`
- Attach: `link.AttachXDP()`

### TC/tcx (Kernel 6.6+)
- Section: `SEC("tc")` or `SEC("tcx/ingress")` / `SEC("tcx/egress")`
- Context: `struct __sk_buff *skb`
- Return values: `TC_ACT_OK`, `TC_ACT_SHOT`, `TC_ACT_REDIRECT`, `TC_ACT_PIPE`
- Attach: `link.AttachTCX()` for tcx, `link.AttachTC()` for legacy

### netkit (BPF-programmable network device)
- Section: `SEC("netkit/primary")` and `SEC("netkit/peer")`
- Context: `struct __sk_buff *skb`
- Return values: `NETKIT_PASS`, `NETKIT_DROP`, `NETKIT_REDIRECT`
- Attach: `link.AttachNetkit()` with `ebpf.AttachNetkitPrimary` or `ebpf.AttachNetkitPeer`
- Note: Requires two programs (primary and peer) for bidirectional processing

### kprobe/kretprobe
- Section: `SEC("kprobe/function_name")` or `SEC("kretprobe/function_name")`
- Context: `struct pt_regs *ctx`
- Return value: `0`
- Attach: `link.Kprobe()` or `link.Kretprobe()`

### tracepoint
- Section: `SEC("tracepoint/category/name")`
- Context: Custom struct based on tracepoint
- Return value: `0`
- Attach: `link.Tracepoint()`

## Go Module Initialization

After creating the structure, initialize the Go module:

```shell
cd examples/{name}
go mod init github.com/{username}/xcnf/examples/{name}
go get -tool github.com/cilium/ebpf/cmd/bpf2go
go mod tidy
```

## Post-Scaffold Instructions

After scaffolding, remind the user to:

1. **Enter the Linux VM** (if using OrbStack):
   ```shell
   orb
   ```

2. **Generate vmlinux.h** (for CO-RE programs):
   ```shell
   cd examples/{name}/bytecode
   bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
   ```

3. **Generate eBPF bytecode**:
   ```shell
   cd examples/{name}
   go generate ./bytecode
   ```

4. **Implement the CNF logic** in:
   - `bytecode/{name}.c` - kernel-space processing
   - `main.go` - userspace control and data handling

5. **Build and test**:
   ```shell
   go build -o {name}
   sudo ./{name}
   ```

## Best Practices

- Use meaningful variable names that describe the CNF's purpose
- Add TODO comments for areas that need implementation
- Include bounds checking for all packet data access
- Use appropriate helper functions (`bpf_printk` for debugging)
- Follow the existing patterns in the repository
- Add proper error handling in Go code
- Use `defer` for cleanup (Close(), link cleanup)

## Example Usage

User: "Create a new CNF called 'rate-limiter' that uses XDP to rate limit incoming packets"