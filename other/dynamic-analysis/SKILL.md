---
name: binary-re:dynamic-analysis
description: "Observes runtime behavior of binaries via QEMU emulation, GDB debugging, and Frida hooking — syscall tracing, breakpoints, memory inspection, and function interception. Use when running, tracing, or debugging a binary, verifying hypotheses from static analysis, or watching actual syscalls, network calls, or file access; requires human approval before any execution."
---

# Dynamic Analysis (Phase 4)

## Purpose

Observe actual runtime behavior. Verify hypotheses from static analysis. Capture data that's only visible during execution.

## Human-in-the-Loop Requirement

**CRITICAL: All execution requires human approval.**

Before running ANY binary:
1. Confirm sandbox configuration is acceptable
2. Verify network isolation if required
3. Document what execution will attempt
4. Get explicit approval

## Platform Support Matrix

| Host Platform | Target Arch | Method | Complexity |
|---------------|-------------|--------|------------|
| Linux x86_64 | ARM32/64, MIPS | Native `qemu-user` | Low |
| Linux x86_64 | x86-32 | Native or `linux32` | Low |
| macOS (any) | ARM32/64 | Docker + binfmt | Medium |
| macOS (any) | x86-32 | Docker `--platform linux/i386` | Medium |
| Windows | Any | WSL2 → Linux method | Medium |

### macOS Docker Setup (One-Time)

```bash
# Start Docker runtime (Colima, Docker Desktop, etc.)
colima start

# Register ARM emulation handlers (requires privileged mode)
docker run --rm --privileged --platform linux/arm64 \
  tonistiigi/binfmt --install arm
```

### Docker Mount Best Practices

**CRITICAL:** On Colima, `/tmp` mounts often fail silently. Always use home directory paths:

```bash
# ✅ GOOD - use home directory
docker run -v ~/code/samples:/work:ro ...

# ❌ BAD - /tmp mounts can fail on Colima
docker run -v /tmp/samples:/work:ro ...
```

---

## Analysis Options

| Method | Isolation | Granularity | Best For |
|--------|-----------|-------------|----------|
| QEMU -strace | High | Syscall level | Initial behavior mapping |
| QEMU + GDB | High | Instruction level | Detailed debugging |
| Docker | High | Process level | Cross-arch on macOS |
| Frida | Medium | Function level | Hooking without recompilation |
| On-device | Low | Full system | When emulation fails |

## Option A: QEMU User-Mode with Syscall Trace

**Safest approach - runs in isolation with syscall logging.**

### Setup

```bash
# Verify sysroot exists
ls /usr/arm-linux-gnueabihf/lib/libc.so*

# ARM 32-bit execution
qemu-arm -L /usr/arm-linux-gnueabihf -strace -- ./binary

# ARM 64-bit execution
qemu-aarch64 -L /usr/aarch64-linux-gnu -strace -- ./binary
```

### Sysroot Selection

| Binary ABI | Sysroot Path | QEMU Flag |
|------------|--------------|-----------|
| ARM glibc hard-float | `/usr/arm-linux-gnueabihf` | `-L` |
| ARM glibc soft-float | `/usr/arm-linux-gnueabi` | `-L` |
| ARM64 glibc | `/usr/aarch64-linux-gnu` | `-L` |
| ARM musl | Custom extraction needed | `-L` |

### Environment Control

```bash
# Set environment variables
qemu-arm -L /sysroot \
  -E HOME=/tmp \
  -E USER=nobody \
  -E LD_DEBUG=bindings \
  -- ./binary

# Unset dangerous variables
qemu-arm -L /sysroot \
  -U LD_PRELOAD \
  -- ./binary
```

### Syscall Analysis

Strace output patterns to watch:

```bash
# Network activity
openat.*socket
connect(.*AF_INET
sendto\|send\|write.*socket
recvfrom\|recv\|read.*socket

# File access
openat.*O_RDONLY.*"/etc
openat.*O_WRONLY
stat\|lstat.*"/

# Process operations
execve
fork\|clone
```

## Option B: QEMU + GDB for Deep Debugging

**Attach debugger for instruction-level control.**

### Launch Binary Under GDB

```bash
# Start QEMU with GDB server
qemu-arm -g 1234 -L /usr/arm-linux-gnueabihf ./binary &

# Connect with gdb-multiarch
gdb-multiarch -q \
  -ex "set architecture arm" \
  -ex "target remote :1234" \
  -ex "source ~/.gdbinit-gef.py" \
  ./binary
```

### GDB Commands for RE

```gdb
# Breakpoints
break *0x8400              # Address
break main                 # Symbol
break *0x8400 if $r0 == 5  # Conditional

# Execution control
continue                   # Run until break
stepi                      # Single instruction
nexti                      # Step over calls
finish                     # Run until return

# Inspection
info registers             # All registers
x/20i $pc                  # Disassemble from PC
x/10wx $sp                 # Stack contents
x/s 0x12345                # String at address

# Memory
find 0x8000, 0x10000, "pattern"  # Search memory
dump memory /tmp/mem.bin 0x8000 0x9000  # Extract region
```

### GEF Enhancements

With GEF loaded, additional commands:

```gdb
gef> vmmap                 # Memory layout
gef> checksec              # Security features
gef> context               # Full state display
gef> hexdump qword $sp 10  # Better hex dump
gef> pcustom               # Structure definitions
```

### Batch Debugging Script

```bash
# Create GDB script
cat > analyze.gdb << 'EOF'
set architecture arm
target remote :1234
break main
continue
info registers
x/20i $pc
continue
quit
EOF

# Run batch
gdb-multiarch -batch -x analyze.gdb ./binary
```

## Option C: Frida for Function Hooking

For Frida setup, architecture constraints, hook examples, and platform-specific instrumentation guides, read references/frida-setup.md.

## Option D: Docker-Based Cross-Architecture (macOS)

For Docker-based cross-architecture analysis on macOS including ARM32, ARM64, and x86-32 examples, read references/docker-setup.md.

---

## Option E: On-Device Analysis

For on-device analysis via gdbserver and remote strace when emulation fails, read references/on-device-setup.md.

## Sandbox Configuration

### Minimal Sandbox (nsjail)

```bash
nsjail \
  --mode o \
  --chroot /sysroot \
  --user 65534 \
  --group 65534 \
  --disable_clone_newnet \
  --rlimit_as 512 \
  --time_limit 60 \
  -- /binary
```

### QEMU with Resource Limits

```bash
# CPU time limit
timeout 60 qemu-arm -L /sysroot -strace ./binary

# Memory limit via cgroup (requires setup)
cgexec -g memory:qemu_sandbox qemu-arm -L /sysroot ./binary
```

## Anti-Analysis Detection

Before dynamic analysis, check for common anti-debugging/anti-analysis patterns:

### Static Detection (Pre-Execution)

```bash
# Check for anti-debug strings/imports
strings -a binary | grep -Ei 'ptrace|anti|debugger|seccomp|LD_PRELOAD|/proc/self'

# r2: Look for ptrace/prctl/seccomp imports
r2 -q -c 'iij' binary | jq '.[].name' | grep -Ei 'ptrace|prctl|seccomp'

# Common anti-analysis indicators:
# - ptrace(PTRACE_TRACEME) - Prevent debugger attach
# - prctl(PR_SET_DUMPABLE, 0) - Prevent core dumps
# - seccomp - Syscall filtering
# - /proc/self/status checks - Detect TracerPid
```

### Runtime Detection

```bash
# If native execution possible:
strace -f ./binary 2>&1 | grep -E 'ptrace|prctl|seccomp|/proc/self'
```

### Mitigation Strategies

| Pattern | Detection | Bypass |
|---------|-----------|--------|
| `ptrace(TRACEME)` | Returns EPERM if debugger attached | Patch call to NOP, use QEMU |
| `/proc/self/status` check | Reads TracerPid field | Use QEMU (no /proc emulation) |
| Timing checks | `gettimeofday`/`rdtsc` loops | Single-step with GDB, patch checks |
| Self-checksum | Reads own binary/memory | Compute expected checksum, patch |

**When anti-analysis detected:** Prefer QEMU-strace over GDB (fewer detection vectors), or patch checks in r2 before execution.

---

## Error Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| `Unsupported syscall` | QEMU limitation | Try Qiling or on-device |
| `Invalid ELF image` | Wrong arch/sysroot | Verify `file` output |
| `Segfault at 0x0` | Missing library | Check `ldd` equivalent |
| `QEMU hangs` | Blocking on I/O | Add timeout, check strace |
| `Anti-debugging` | Detection code | Use Frida stalker mode |
| `exec format error` in Docker | binfmt not registered | Run `tonistiigi/binfmt --install arm` |
| `ld-linux.so.3 not found` | Linker path mismatch | Create symlink in container |
| `libXXX.so not found` | Missing dependency | `apt install` in container |
| Empty mount in Docker | Colima /tmp issue | Use `~/` path instead of `/tmp/` |
| `ptrace: Operation not permitted` | strace in QEMU | Use `LD_DEBUG` instead |

## Output Format

Record observations as structured data:

```json
{
  "experiment": {
    "id": "exp_001",
    "method": "qemu_strace",
    "command": "qemu-arm -L /usr/arm-linux-gnueabihf -strace ./binary",
    "duration_secs": 12,
    "exit_code": 0
  },
  "syscall_summary": {
    "network": {
      "socket": 2,
      "connect": 1,
      "send": 5,
      "recv": 3
    },
    "file": {
      "openat": 4,
      "read": 12,
      "close": 4
    }
  },
  "network_connections": [
    {
      "family": "AF_INET",
      "address": "192.168.1.100",
      "port": 8443,
      "protocol": "tcp"
    }
  ],
  "files_accessed": [
    {"path": "/etc/config.json", "mode": "read"},
    {"path": "/var/log/app.log", "mode": "write"}
  ],
  "hypotheses_tested": [
    {
      "hypothesis_id": "hyp_001",
      "result": "confirmed",
      "evidence": "connect() to 192.168.1.100:8443 observed"
    }
  ]
}
```

## Knowledge Journaling

After dynamic analysis, record findings for episodic memory:

```
[BINARY-RE:dynamic] {filename} (sha256: {hash})

Execution method: {qemu-strace|qemu-gdb|frida|on-device}
DECISION: Approved execution with {sandbox_config} (rationale: {why_safe})

Runtime observations:
  FACT: Binary reads {path} (source: strace openat)
  FACT: Binary connects to {ip}:{port} (source: strace connect)
  FACT: Binary writes to {path} (source: strace write)
  FACT: Function {addr} receives args {values} at runtime (source: gdb)

Syscall summary:
  Network: {socket|connect|send|recv counts}
  File: {open|read|write|close counts}
  Process: {fork|exec|clone counts}

HYPOTHESIS UPDATE: {confirmed or refined theory} (confidence: {new_value})
  Confirmed by: {runtime observation}
  Contradicted by: {if any}

New questions:
  QUESTION: {runtime-discovered unknown}

Answered questions:
  RESOLVED: {question} → {runtime evidence}
```

### Example Journal Entry

```
[BINARY-RE:dynamic] thermostat_daemon (sha256: a1b2c3d4...)

Execution method: qemu-strace
DECISION: Approved execution with network-blocked sandbox (rationale: static analysis shows outbound only, no server)

Runtime observations:
  FACT: Binary reads /etc/thermostat.conf at startup (source: strace openat)
  FACT: Binary attempts connect to 93.184.216.34:443 (source: strace connect)
  FACT: Binary writes to /var/log/thermostat.log (source: strace openat O_WRONLY)
  FACT: sleep(30) called between network attempts (source: strace nanosleep)

Syscall summary:
  Network: socket(2), connect(1-blocked), send(0), recv(0)
  File: openat(4), read(12), write(8), close(4)
  Process: none

HYPOTHESIS UPDATE: Telemetry client confirmed - reads config, attempts HTTPS to thermco servers every 30s (confidence: 0.95)
  Confirmed by: connect() to expected IP, sleep(30) timing, config file read
  Contradicted by: none

Answered questions:
  RESOLVED: "Does it actually phone home?" → Yes, connect() to 93.184.216.34:443 observed
  RESOLVED: "What files does it access?" → /etc/thermostat.conf (read), /var/log/thermostat.log (write)
```

## Next Steps

→ `binary-re:synthesis` to compile findings into report
→ Additional static analysis if new functions identified
→ Repeat with different inputs if behavior varies
