---
name: ebpf-attacks
description: eBPF-based post-exploitation for kernel-level credential harvesting, process hiding, and traffic interception on Linux
category: post-exploitation
tags: [ebpf, bpf, kernel, post-exploitation, credential-access, defense-evasion, persistence, linux, rootkit]
tech_stack: [linux, ebpf, kernel, bcc]
cwe_ids: [CWE-269, CWE-522, CWE-693]
chains_with: [T1014, T1055, T1556, T1205.002, T1003, T1059.004]
prerequisites: [T1068, T1548]
version: "2.0"
---

# eBPF Post-Exploitation Methodology

eBPF (Extended Berkeley Packet Filter) enables kernel-level instrumentation without loading kernel modules. After gaining root on a Linux target, eBPF programs can intercept system calls, userspace function calls, and network traffic — operating below userland monitoring tools.

## Prerequisites

Before deploying eBPF tools, verify:

1. **Root access** — all eBPF operations require `CAP_SYS_ADMIN` or `CAP_BPF`
2. **Kernel version** — Linux 4.18+ for full BPF features, 5.8+ for BPF ring buffer
3. **BCC installed** — `python3 -c "from bcc import BPF"` must succeed on target
4. **No BPF LSM** — check `cat /sys/kernel/security/lsm` for bpf restrictions

```bash
# Quick prerequisite check
uname -r                                    # kernel version
cat /proc/config.gz | zcat | grep CONFIG_BPF  # BPF config
ls /sys/fs/bpf/                             # BPF filesystem mounted
python3 -c "from bcc import BPF; print('OK')" # BCC available
```

## Kill Chain Phases

### Phase 1 — Situational Awareness (First 60 seconds)

Understand the environment before deploying persistent hooks.

| Action | Command | Purpose |
|--------|---------|---------|
| Scan dependencies | `ebpf dep_scan` | Map all loaded libraries across all processes |
| Vuln check | `ebpf dep_scan --json-output` | Identify vulnerable library versions |
| Monitor executions | `ebpf execve_sniff --duration 30` | Understand what runs on the system — cron, services, monitoring |
| DNS baseline | `ebpf dns_sniff --duration 30` | Map DNS activity — identify internal services, C2 detection |

### Phase 2 — Credential Harvesting

Intercept credentials at the kernel level — no file modification, no log entries.

| Action | Command | Purpose |
|--------|---------|---------|
| PAM interception | `ebpf pam_sniff --duration 300` | Capture SSH, sudo, su, login passwords in cleartext |
| TLS interception | `ebpf ssl_sniff --pid <PID>` | Capture HTTPS plaintext for a specific service |
| Keystroke capture | `ebpf keylog --duration 120` | Capture interactive terminal input from TTY sessions |

**PAM sniffing** hooks `pam_get_authtok` in `libpam.so` via uprobe. Every authentication event (SSH login, sudo, su, screen unlock) passes through PAM — the cleartext password is captured before hashing.

**SSL sniffing** hooks `SSL_write` and `SSL_read` in `libssl.so`. Data is captured in plaintext before encryption (write) and after decryption (read). Use `--pid` to target a specific process (e.g., a web application handling API keys).

**Keystroke logging** hooks `sys_read` on TTY file descriptors (`/dev/tty*`, `/dev/pts/*`). Captures all interactive terminal input including passwords typed in non-echo mode.

### Phase 3 — Stealth Operations

Hide your presence from system administrators and monitoring tools.

| Action | Command | Purpose |
|--------|---------|---------|
| Hide process | `ebpf proc_hide --pid <PID>` | Remove process from ps, top, htop, /proc listing |
| Hide files | `ebpf file_hide --name <NAME>` | Remove file/directory from ls, find, directory listings |
| Hide connections | `ebpf conn_hide --port <PORT>` | Remove network connection from netstat, ss, /proc/net/tcp |

**Process hiding** hooks `sys_getdents64` on `/proc`. When the kernel returns directory entries, entries matching the target PID are overwritten with `.` — the process becomes invisible to all userland tools that enumerate `/proc`.

**File hiding** uses the same `sys_getdents64` hook but matches against a filename instead of a PID. Effective for hiding implants, scripts, and data exfiltration staging directories.

**Connection hiding** hooks `sys_read` on `/proc/net/tcp` and `/proc/net/tcp6`. When a monitoring tool reads the connection table, lines containing the target port are overwritten with spaces.

### Phase 4 — Blind Spot Detection (20 monitors)

Detect attack primitives that bypass classical syscall hooks and operate through kernel subsystems invisible to standard monitoring.

| Action | Command | Purpose |
|--------|---------|---------|
| io_uring bypass | `ebpf io_uring_sniff --duration 60` | Detect file/socket/connect operations via io_uring that bypass syscall hooks (kernel 5.1+) |
| Fileless execution | `ebpf memfd_exec --duration 60` | Detect memfd_create + execveat diskless payload delivery chains |
| ptrace injection | `ebpf ptrace_sniff --duration 60` | Monitor ATTACH → POKEDATA → SETREGS shellcode injection sequences |
| Cross-process memory | `ebpf crossmem_sniff --duration 60` | Detect stealthy process_vm_writev/readv memory injection |
| Race condition exploits | `ebpf userfaultfd_sniff --duration 60` | Detect userfaultfd-based timing control primitives |
| BPF integrity | `ebpf bpf_integrity --baseline --duration 300` | Verify CyberStrike hook integrity, detect unauthorized BPF program loads |
| Netlink manipulation | `ebpf netlink_sniff --duration 60` | Detect stealthy route/firewall rule manipulation via netlink |
| Sandbox weakening | `ebpf seccomp_sniff --duration 60` | Detect processes disabling their own seccomp/prctl security profiles |
| Shared memory IPC | `ebpf mmap_sniff --duration 60` | Detect covert IPC via mmap MAP_SHARED, shmget, shmat — data flows without syscalls |
| Zero-copy transfers | `ebpf zerocopy_sniff --duration 60` | Detect splice/tee/sendfile64 fd-to-fd transfers invisible to buffer profilers |
| VDSO tampering | `ebpf vdso_sniff --duration 60` | Detect timing side-channels and VDSO page modification attacks |
| Kernel keyring abuse | `ebpf keyring_sniff --duration 60` | Detect credential storage in kernel keyring (add_key/keyctl) |
| Namespace escape | `ebpf namespace_sniff --duration 60` | Detect container escape via setns/unshare namespace pivoting |
| Terminal injection | `ebpf ioctl_sniff --duration 60` | Detect TIOCSTI keystroke injection and terminal manipulation |
| Mount manipulation | `ebpf mount_sniff --duration 60` | Detect overlay/bind mounts hiding changes on sensitive paths |
| FUSE hijacking | `ebpf fuse_sniff --duration 60` | Detect userspace filesystem mounting that bypasses kernel VFS |
| Perf side-channel | `ebpf perf_sniff --duration 60` | Detect perf_event_open side-channel attacks via HW counters |
| BPF map covert channel | `ebpf bpfmap_sniff --duration 60` | Detect covert data sharing via BPF map create/update operations |
| LD_PRELOAD injection | `ebpf ldpreload_sniff --duration 60` | Detect library injection via LD_PRELOAD env and ld.so config |
| Futex covert channel | `ebpf futex_sniff --duration 60` | Detect timing-based covert channels via futex WAIT/WAKE |

**io_uring sniffing** monitors SQE submissions via `io_uring_submit_sqe` kprobe. Operations like CONNECT, READ, WRITE, OPENAT through io_uring bypass classical syscall hooks entirely — a reverse shell built on io_uring is invisible to execve/connect tracepoints.

**Fileless execution detection** correlates `memfd_create` → `write` → `execveat(fd, "", AT_EMPTY_PATH)` chains. The payload never touches disk — it exists only in memory via memfd. This is the primary technique for diskless implant delivery.

**ptrace injection monitoring** tracks the ATTACH → POKEDATA → SETREGS → CONT sequence that constitutes shellcode injection. Each ptrace operation is logged with target PID and memory addresses.

**Cross-process memory monitoring** captures `process_vm_writev`/`process_vm_readv` syscalls. These enable memory injection without ptrace — bypassing ptrace-based detection entirely.

**userfaultfd monitoring** detects creation of userfaultfd file descriptors. Legitimate use is rare (QEMU/KVM live migration); in exploit context, userfaultfd provides precise timing control for race condition exploitation.

**BPF integrity verification** takes a baseline of loaded BPF programs via `bpftool` and periodically verifies no CyberStrike programs have been detached or tampered with. Also monitors `bpf()` syscall for unauthorized program loads.

**Netlink monitoring** captures netlink socket messages for NEWROUTE, DELROUTE, NEWRULE, DELRULE operations — detecting stealthy routing table and firewall rule manipulation.

**Seccomp/prctl monitoring** captures PR_SET_SECCOMP, PR_SET_NO_NEW_PRIVS, PR_SET_NAME, PR_SET_DUMPABLE, and seccomp filter installation — detecting processes weakening their own security profiles or masquerading via name changes.

### Phase 5 — Cleanup (MANDATORY)

Always run cleanup before exiting a target.

```bash
# List all CyberStrike eBPF programs on the system
ebpf cleanup

# Remove all CyberStrike eBPF programs
ebpf cleanup --remove --force

# Dry run — show what would be removed
ebpf cleanup --dry-run
```

The cleanup tool uses three detection methods:
1. `bpftool prog list` — enumerate all loaded BPF programs
2. `/sys/fs/bpf/` — check for pinned programs
3. `/sys/kernel/debug/tracing/` — check for registered kprobe/uprobe events

## Detection Considerations

eBPF programs are detectable by:
- `bpftool prog list` — shows all loaded BPF programs
- `/sys/kernel/debug/tracing/kprobe_events` — shows registered kprobes
- `/sys/kernel/debug/tracing/uprobe_events` — shows registered uprobes
- `auditd` rules on `bpf()` syscall — `auditctl -a always,exit -F arch=b64 -S bpf`
- EDR agents with BPF LSM hooks (Falco, Tracee, Tetragon)

## Program Reference

| Program | Hook Type | Target | MITRE ATT&CK |
|---------|-----------|--------|---------------|
| pam_sniff | uprobe | `pam_get_authtok` in libpam.so | T1556 — Modify Authentication Process |
| ssl_sniff | uprobe | `SSL_write`/`SSL_read` in libssl.so | T1040 — Network Sniffing |
| dep_scan | procfs | `/proc/<pid>/maps` | T1518 — Software Discovery |
| proc_hide | kprobe | `sys_getdents64` on /proc | T1014 — Rootkit |
| file_hide | kprobe | `sys_getdents64` | T1014 — Rootkit |
| conn_hide | kprobe | `sys_read` on /proc/net/tcp | T1014 — Rootkit |
| execve_sniff | tracepoint | `sys_execve` | T1057 — Process Discovery |
| dns_sniff | kprobe | `udp_sendmsg` port 53 | T1071.004 — DNS Application Layer Protocol |
| keylog | kprobe | `sys_read` on TTY fds | T1056.001 — Keylogging |
| cleanup | bpftool | BPF programs/maps | — |
| io_uring_sniff | kprobe | `io_uring_submit_sqe` | T1014 — Rootkit (syscall bypass) |
| memfd_exec | tracepoint | `memfd_create` + `execveat` | T1620 — Reflective Code Loading |
| ptrace_sniff | tracepoint | `sys_enter_ptrace` | T1055.008 — Ptrace System Calls |
| crossmem_sniff | tracepoint | `process_vm_writev`/`readv` | T1055.012 — Process Hollowing |
| userfaultfd_sniff | tracepoint | `sys_enter_userfaultfd` | T1068 — Exploitation for Privilege Escalation |
| bpf_integrity | tracepoint | `sys_enter_bpf` + bpftool | T1553 — Subvert Trust Controls |
| netlink_sniff | kprobe | `netlink_sendmsg` | T1562.004 — Disable or Modify System Firewall |
| seccomp_sniff | tracepoint | `sys_enter_prctl` + `sys_enter_seccomp` | T1562.001 — Disable or Modify Tools |
| mmap_sniff | tracepoint | `sys_enter_mmap` + `sys_enter_shmget` + `sys_enter_shmat` | T1055.009 — Proc Memory (shared memory IPC) |
| zerocopy_sniff | tracepoint | `sys_enter_splice` + `sys_enter_tee` + `sys_enter_sendfile64` | T1041 — Exfiltration Over C2 Channel |
| vdso_sniff | tracepoint | `sys_enter_clock_gettime` + `sys_enter_mprotect` | T1497.003 — Time Based Evasion |
| keyring_sniff | tracepoint | `sys_enter_add_key` + `sys_enter_keyctl` + `sys_enter_request_key` | T1003 — OS Credential Dumping |
| namespace_sniff | tracepoint | `sys_enter_setns` + `sys_enter_unshare` | T1611 — Escape to Host |
| ioctl_sniff | tracepoint | `sys_enter_ioctl` (TIOCSTI/TIOCLINUX/TIOCSCTTY) | T1056.001 — Keylogging |
| mount_sniff | tracepoint | `sys_enter_mount` + `sys_enter_umount` | T1006 — Direct Volume Access |
| fuse_sniff | tracepoint | `sys_enter_openat` (/dev/fuse) + `sys_enter_mount` (fuse) | T1014 — Rootkit |
| perf_sniff | tracepoint | `sys_enter_perf_event_open` | T1497.003 — Time Based Evasion |
| bpfmap_sniff | tracepoint | `sys_enter_bpf` (MAP_CREATE/UPDATE/LOOKUP/DELETE) | T1071 — Application Layer Protocol |
| ldpreload_sniff | tracepoint | `sys_enter_execve` (env scan) + `sys_enter_openat` (ld.so) | T1574.006 — Dynamic Linker Hijacking |
| futex_sniff | tracepoint | `sys_enter_futex` (WAIT/WAKE/BITSET/PI) | T1029 — Scheduled Transfer |

---

## 5. CONFIRMING THE FINDING

The four sections above describe WHAT each hook targets. This table is what turns a target into a proven
finding, and its centre is a distinction this domain lives or dies on: **a program that loaded is not a
program that intercepted.**

| Step | Question | What it proves |
|---|---|---|
| 1 | Is the hook point named as a **type + symbol + attach point**? | the transferable intelligence, and what is visible |
| 2 | Is the program **LOADED** (`bpftool prog show`), with its ID, type, and tag? | necessary, and NOT sufficient |
| 3 | Is it **ATTACHED** (`bpftool link show`), to the **symbol you claim**? | loaded without a link does nothing |
| 4 | Did the **verifier's own log** record the load (a before/after `dmesg` diff)? | the load's independent evidence |
| 5 | Did a **known value** appear in the captured output? | falsifiable capture, not "we saw traffic" |
| 6 | Did the **detached control** produce **nothing** on the same trigger? | the definitive control |
| 7 | For **hiding**: absent WITH the hook AND present WITHOUT it? | a crashed process is not a hidden one |
| 8 | Was **cleanup** verified by re-running the pre-test observation? | the restoration is the evidence |

**The hook point is the artefact, and the detached control is what makes a capture attributable.** Where
the tooling is not available, the **posture findings** (prerequisites, lockdown, `bpf` LSM, the unprivileged
`sysctl`) are valid evidence in their own right - every control's presence is a mitigation and its absence
is the finding.

---

---

## 6. EXECUTION PRIMITIVES

The tables above name the hooks; this section is **how to prove a hook is actually attached and actually
firing**. The distinction is the whole file: a program that LOADED is not a program that INTERCEPTED, and
the verifier's own log plus a control program that does not fire is what proves the difference.

### 5.1 The name, and the phantom-command hazard

```bash
echo "=== READ THIS FIRST: EVERY 'ebpf <program>' ROW ABOVE IS A REFERENCE TO A PROGRAM YOU MUST OBTAIN ==="
cat <<'NAME'
  THIS FILE USES `ebpf <program>` AS SHORTHAND FOR 'the eBPF program that hooks <target>'. THE STRING
  `ebpf` HERE IS NOT A BINARY THAT SHIPS WITH THIS PACKAGE, AND NO SUCH CLI EXISTS AS A GENERIC TOOL.
  WHAT ACTUALLY EXISTS, and what each row maps to:
    bcc / bpftrace / bpftool / libbpf   -> the real toolchain for writing and loading BPF programs
    the family of public eBPF projects   -> e.g. the tracee/ tetragon/ bcc-tools families, each with
                                            its OWN command names, which are NOT 'ebpf <x>'
  SO THE PROCEDURE IS: take the HOOK POINT from the tables (the section and target column), and use a
  REAL toolchain to attach at that point. THE HOOK POINT IS THE TRANSFERABLE INTELLIGENCE. The
  command spelling above is notation, and treating it as a literal binary produces a fabricated
  command - which is exactly the defect this section exists to prevent.
  WHEN AN AGENT CONSUMES THIS FILE IT MUST SUBSTITUTE a real tool, and the tables give it everything
  it needs to do so: the hook TYPE (uprobe/kprobe/tracepoint), the TARGET SYMBOL, and the MITRE ID.
NAME
echo
echo "=== THE HOOK POINT TABLE, mechanically extracted from the rows above ==="
python3 - <<'PY'
HOOKS = [
 ("pam_sniff",   "uprobe",     "pam_get_authtok in libpam.so",        "userspace function entry", "the cleartext argument BEFORE hashing"),
 ("ssl_sniff",   "uprobe",     "SSL_write / SSL_read in libssl.so",  "userspace library function", "the plaintext BEFORE encryption / AFTER decryption"),
 ("keylog",      "kprobe",     "sys_read on a TTY fd",               "syscall entry/return",      "the buffer contents read from a TTY"),
 ("proc_hide",   "kprobe",     "sys_getdents64 on /proc",            "syscall return",            "the entries the kernel RETURNS (mutated before userspace)"),
 ("file_hide",   "kprobe",     "sys_getdents64",                     "syscall return",            "the same, matched by NAME rather than by PID"),
 ("conn_hide",   "kprobe",     "sys_read on /proc/net/tcp",          "syscall return",            "the connection table's returned bytes"),
 ("dns_sniff",   "kprobe",     "udp_sendmsg to port 53",             "syscall entry",             "the DNS payload"),
 ("execve_sniff","tracepoint", "sys_enter_execve",                   "tracepoint",                "the exec arguments, at the standard tracepoint"),
]
print("%-14s %-11s %-36s %-26s %s" % ("program","hook type","target","attach point","what is captured"))
for a,b,c,d,e in HOOKS: print("%-14s %-11s %-36s %-26s %s" % (a,b,c,d,e))
print()
print("  THE 'attach point' COLUMN IS WHAT DECIDES WHAT YOU CAN SEE:")
print("    a SYSCALL ENTRY hook sees the arguments BEFORE the operation")
print("    a SYSCALL RETURN hook sees the RESULT, and can REWRITE it (that is how hiding works)")
print("    a UPROBE sits at a userspace function, so it sees PLAINTEXT that the syscall layer")
print("      would only ever see encrypted or hashed")
print("  GETTING THIS WRONG IS THE FAMILY'S MAIN TECHNICAL ERROR: a syscall-entry hook CANNOT see")
print("  a password that PAM has already hashed in userspace, and a return hook is REQUIRED for hiding.")
PY
```

**The hook point is the transferable intelligence; the `ebpf <program>` spelling is notation, not a binary.**
And the attach point decides what is visible: a userspace uprobe sees plaintext that a syscall hook cannot.

### 5.2 Proving the program is LOADED, and proving it FIRES

```bash
echo "=== STEP 1: PROVE IT IS LOADED (necessary, NOT sufficient) ==="
sudo bpftool prog show 2>/dev/null | head -40
echo "  record: the program's ID, its TYPE (kprobe/uprobe/tracepoint), and its TAG."
echo "  a program that is loaded but never invoked is the commonest failure in this family."
echo
echo "=== STEP 2: PROVE IT IS ATTACHED, at the point you claim ==="
sudo bpftool link show 2>/dev/null | head -40
echo "  the LINK is what actually routes events to the program. LOADED WITHOUT A LINK = NOTHING HAPPENS."
echo "  and a link to the WRONG symbol is indistinguishable from success unless you check the symbol."
echo
echo "=== STEP 3: THE VERIFIER'S OWN LOG, which is the load's independent evidence ==="
sudo dmesg 2>/dev/null | tail -30 | grep -iE 'bpf|verif|prog|trace' || \
  echo "  (the verifier's messages appear here; capture them BEFORE and AFTER the load)"
cat <<'VERIFIER'
  THE VERIFIER'S LOG IS THE RICHEST SINGLE ARTEFACT IN THIS DOMAIN:
    - it shows the program was ACCEPTED (with its name and tag), or REJECTED with a reason
    - a REJECTION is a finding about the target's LOCKDOWN (see 5.4), not a failure of yours
    - it records the loaded instruction count and the verifier's own pass/fail
  CAPTURE IT AS A DIFF: `dmesg > /tmp/before.txt` before the load, and a diff afterwards. THAT
  DIFF IS THE PROOF THE LOAD HAPPENED, and it is independent of your tool's exit status.
VERIFIER
echo
echo "=== STEP 4: THE EVENT, with the CONTROL that makes it attributable ==="
cat <<'EVENT'
  A TEST HARNESS WITH ITS OWN CONTROL PAIR:
    1. TRIGGER the event deliberately from a process you control, e.g.:
         for pam_sniff : run `sudo -k; su -c 'true' someuser` with a KNOWN password
         for ssl_sniff : curl a local HTTPS endpoint with a KNOWN string in the body
         for keylog    : write a KNOWN string to a TTY
         for dns_sniff : resolve a name you control, under a label you choose
    2. READ the program's own output (its map, its ring buffer, or its tool's stdout) and confirm
       the KNOWN value appears IN THE FORM YOU EXPECT
    3. THE CONTROL: perform a DIFFERENT operation that should NOT fire the hook, and confirm the
       output does not change. AND, separately:
       detach the program (or load it WITHOUT attaching) and confirm the SAME trigger produces NOTHING.
  STEP 3'S SECOND CONTROL IS THE DEFINITIVE ONE: no program, no event. If the event still appears
  with the program detached, you are reading someone else's output, a stale buffer, or your own echo.
EVENT
echo
echo "=== THE 'KNOWN VALUE' DISCIPLINE, which turns a detection into a proof ==="
echo "  NEVER report 'we captured credentials'. Report: 'with a known password K sent through PAM, the"
echo "  program's map contained K as the argument to pam_get_authtok, and the same trigger with the"
echo "  program detached produced nothing.' THE KNOWN VALUE IS WHAT MAKES IT FALSIFIABLE."
```

**Loaded without a link does nothing, and the definitive control is the same trigger with the program
detached.** A known value in the captured buffer is what makes the capture falsifiable.

### 5.3 Hiding primitives, and their own evidence

```bash
echo "=== THE HIDING PRIMITIVES ARE PROVEN FROM THE USERSPACE SIDE, not from BPF ==="
cat <<'HIDING'
  THIS IS THE KEY ASYMMETRY: hiding works by MUTATING THE KERNEL'S RETURN DATA, so the proof is
  ALWAYS an ordinary userspace observation, and it needs BOTH halves:

    A. WITH THE HOOK:   `ps -ef | grep <name>`          -> ABSENT
                        `ls -la /path/<name>`           -> ABSENT
                        `ss -tnp | grep <port>`         -> ABSENT
                        and, for completeness:
                        `cat /proc/<pid>/status`        -> STILL PRESENT (the hook does not
                                                           remove the file, it rewrites a listing)
    B. WITHOUT THE HOOK: the SAME three commands        -> PRESENT

  **B IS THE CONTROL, AND IT IS WHAT SEPARATES A HIDING FINDING FROM A FAILED TOOL.** A process that
  is absent from ps because it crashed is not hidden. Without half B you cannot tell the difference.

  AND THE DEEPER POINT, WHICH BELONGS IN THE REPORT: getdents64 rewriting hides the process from
  EVERY TOOL THAT ENUMERATES /proc, and from NOTHING ELSE. The process still:
    - occupies a PID, and appears in the scheduler's own accounting
    - holds open file descriptors visible via other paths
    - consumes CPU and memory, which a MONITORING AGENT MEASURING THOSE (rather than listing
      processes) would still see
  SO THE HONEST FINDING IS: 'hidden from the standard enumeration path, and detectable by an agent
  that measures resource accounting, eBPF integrity, or the listing's own anomaly.' NOT 'invisible'.
HIDING
echo
echo "=== THE SELF-DETECTION HAZARD, which every practitioner hits ==="
echo "  a getdents64 hook that matches too broadly WILL hide your own tools and even your shell."
echo "  record the MATCH PREDICATE (the exact PID or name) and demonstrate that a NON-matching"
echo "  process remains visible - THAT is the precision control, and it is the same shape as the"
echo "  detection's own control in 5.4."
echo "  and note: the hook mutates the return buffer, so a process that HOOKS ITSELF is visible in"
echo "  its own listing only through the unmutated /proc/<pid> paths. THAT asymmetry is the detection."
```

**Without the un-hooked half, a process absent from `ps` because it crashed is indistinguishable from a
hidden one.** And a hidden process consumes CPU and memory that a resource-measuring agent still sees.

### 5.4 The lockdown, and the end-to-end harness

```bash
echo "=== WHEN THE LOAD FAILS, THE TARGET'S LOCKDOWN IS THE FINDING ==="
cat <<'LOCKDOWN'
  A REFUSED LOAD IS NOT A DEAD END - IT IS OFTEN THE MOST VALUABLE RESULT HERE, AND IT IS CLASSIFIED
  AS A DEFENCE FINDING. The refusals and what each means:

    'Operation not permitted' on the bpf() syscall   -> CAP_SYS_ADMIN/CAP_BPF absent
                                                       -> the process is not as privileged as assumed
    'EPERM' with no verifier message                 -> a kernel LSM refused it before the verifier
    a VERIFIER REJECTION with a message in dmesg     -> the program is genuinely malformed or its
                                                       helper calls are not permitted at that hook
    kprobes DISABLED in /sys/kernel/debug/...        -> lockdown is active; the hook points are gone
    /sys/kernel/security/lsm containing 'bpf'        -> the BPF LSM is enforcing; programs are
                                                       constrained by policy, not just by privilege
    CONFIG_BPF_UNPRIV_DEFAULT_OFF, or a
      kernel.unprivileged_bpf_disabled=1 sysctl     -> the RELAXED path is closed, and this is a
                                                       POSTURE FINDING worth reporting by itself
  READ THE PREREQUISITES SECTION AT THE TOP OF THIS FILE BACKWARDS: every item there is a control,
  and each one's PRESENCE is a mitigation and its ABSENCE is the finding. THAT is the assessment
  this domain performs, and it is valid whether or not any program ever loads.
LOCKDOWN
echo
echo "=== THE PRE-TEST POSTURE CHECK, which is itself the finding's evidence ==="
uname -r
cat /proc/sys/kernel/unprivileged_bpf_disabled 2>/dev/null || echo "  (sysctl absent)"
cat /sys/kernel/security/lsm 2>/dev/null || echo "  (LSM list absent)"
cat /sys/kernel/security/lockdown 2>/dev/null || echo "  (lockdown interface absent)"
ls /sys/fs/bpf/ 2>/dev/null | head -5
grep -E 'CONFIG_(BPF|BPF_SYSCALL|DEBUG_INFO_BTF|BPF_LSM)' /boot/config-"$(uname -r)" 2>/dev/null || \
  echo "  (generated config not readable at /boot; try /proc/config.gz)"
echo
echo "=== THE CLEANUP (PHASE 5) IS PART OF THE PROOF, not housekeeping ==="
echo "  after detaching, the SAME commands from 5.3 half B must return to their PRE-TEST state."
echo "  if they do not, THE HOOK IS STILL ATTACHED, and reporting the test as 'cleaned up' without"
echo "  this check is a false statement about the target's state. THE RESTORATION IS THE EVIDENCE."
echo
echo "=== the end-to-end harness ==="
python3 - <<'PY'
print("=== eBPF ACCEPTANCE CHECKLIST ===")
CHECKS = [
 ("the HOOK POINT is named: the hook type, the exact target symbol, and the attach point",
  "the hook point is the transferable intelligence; 'ebpf proc_hide' is notation, not a binary"),
 ("a REAL toolchain is substituted for the `ebpf <program>` notation, and the substitution is stated",
  "the notation is not an executable, and treating it as one produces a fabricated command"),
 ("the attach point's SEMANTICS are justified: entry vs return vs userspace probe",
  "a syscall-entry hook cannot see a password already hashed in userspace; hiding needs the return"),
 ("the program was shown LOADED (bpftool prog show, with its ID, type, and tag)",
  "loaded is necessary and NOT sufficient"),
 ("the program was shown ATTACHED (bpftool link show), to the SYMBOL you claim",
  "a loaded program with no link does nothing, and a link to the wrong symbol looks like success"),
 ("THE VERIFIER'S LOG was captured as a before/after dmesg diff",
  "the load's independent evidence, and a rejection is a lockdown finding"),
 ("a KNOWN VALUE was pushed through the hook and found IN THE CAPTURED OUTPUT",
  "a known value is what makes the capture falsifiable"),
 ("THE DETACHED CONTROL was run: the same trigger with the program detached produced NOTHING",
  "the definitive control; if the event still appears you are reading a stale buffer or your own echo"),
 ("for a HIDING primitive: BOTH halves were shown - absent WITH the hook, present WITHOUT it",
  "a process absent because it crashed is not a hidden process"),
 ("the hiding claim is scoped: 'hidden from /proc enumeration', NOT 'invisible'",
  "a hidden process still occupies a PID and consumes CPU and memory, which some agents measure"),
 ("the MATCH PREDICATE is recorded, and a non-matching process remained visible",
  "the precision control; an over-broad predicate hides your own tools"),
 ("the target's LOCKDOWN was characterised, whether or not the load succeeded",
  "each prerequisite is a control: its absence is the finding"),
 ("CLEANUP was verified by re-running the pre-test observations and confirming the restore",
  "the restoration is the evidence, and an unverified cleanup is a false statement"),
]
for n, how in CHECKS: print("  [ ] %-76s -> %s" % (n, how))
print()
print("=== THE REPORT SHAPE ===")
print("  posture  : kernel, config, LSM, lockdown, and the sysctls - the control inventory")
print("  hook     : the type, the target symbol, the attach point, and the real toolchain used")
print("  load     : prog show and link show, plus the verifier's before/after dmesg diff")
print("  proof    : the known value found in the output, and the detached control")
print("  hiding   : both halves, with the match predicate and the scoped claim")
print("  cleanup  : the re-run observation showing the restore")
PY
```

**A refused load is a defence finding, not a dead end** — every prerequisite at the top of the file is a
control whose absence is the finding. And cleanup verified by re-running the pre-test observations is part
of the proof, not housekeeping.

---

## 7. EVIDENCE STANDARD
| Item | Why |
|---|---|
| The **program's source or its bytecode hash**, and the kernel version | load behaviour is version- and verifier-specific |
| The proof the program **LOADED** (the loader's own output, the program id) | loading is the first of three states, and it is not the interesting one |
| The proof it **ATTACHED** (the link, the hook point, the attach log) | attached is the second state, still not firing |
| The proof it **FIRES** (the event observed, the known value in the output) | the third state, and the only one that is a finding |
| The **verifier's own dmesg output** where a load was refused | a refused load is a defence finding, and it is worth reporting |
| The **detached control**: the same observation with the program detached | proves the observation is attributable to the program |
| The **hiding claim proven from BOTH halves**: the object is absent from the view AND present in the kernel's own state | one half alone is an illusion or a false positive |

### eBPF failures — how they mislead

| Failure | How it misleads |
|---|---|
| **LOADED read as FIRING** | the commonest error in this domain; a loaded program that never attaches observes nothing |
| **ATTACHED read as FIRING** | an attached program whose condition never matches never emits |
| **`ebpf <program>`** run as if it were a binary | that is notation, and the phantom-binary habit fabricates findings |
| **No detached control** | the observation may be the system's own activity |
| A **refused load** reported as a failure rather than a defence finding | the verifier stopping you is a result |
| **Hiding proven from one half only** | absence from a `ps` view and absence from the kernel are different claims |
| A **map value** read without the program that wrote it | the value's presence does not prove the program ran |

| Item | Why |
|---|---|
| The program's hash and the **kernel version**, with the verifier's behaviour on it | load behaviour is version-specific |
| The **three states separated**: loaded, attached, and firing, each with its own proof | only firing is a finding |
| The **verifier's dmesg output** where a load was refused | a refusal is a defence finding with its own value |
| The **detached control** proving the observation is attributable | without it, the observation may be the system's own |
| The **known value** in the output, where the program is meant to observe something specific | proves the program, not the ambient activity |
| The **hiding claim from both halves** | absent from the view AND present in kernel state |
| The explicit statement that **`ebpf <program>` is notation**, not a command | prevents the phantom-binary habit |

**PROVEN THAT IT FIRES, with a detached control and the verifier's own output** — loaded is not attached,
attached is not firing, and a refused load is a defence finding rather than a failure.

---

## 8. REMEDIATION REFERENCE

1. **Fix the load path, not the program.** A rootkit's load requires the privilege; the durable controls
   are capability restriction, a hardened kernel LSM configuration, and a restricted `bpf()` surface.
2. **Keep the verifier's refusal as a control.** Where the verifier stopped the load, record which check
   fired, because that is the control that worked and it should be monitored.
3. **Monitor attachment, not just load.** Detection belongs at the attach points that matter (kprobes on
   credential paths, tracing programs on syscall entry), because load alone is noisy and benign.
4. **State what the fix does not cover.** Restricting `CAP_BPF` does not remove an already-loaded program,
   and it does not cover a legitimate privileged workload.
5. **Treat a refused load as a defence finding.** It should be reported with the same rigour as a
   successful one, since it identifies a control that is functioning.

---

## 9. RELATED SIBLINGS - LOAD TOGETHER
- [linux-security-bypass](../linux-security-bypass/SKILL.md) - the confinement layers an eBPF load must pass
- [anti-debugging-techniques](../anti-debugging-techniques/SKILL.md) - the same hook-and-hide logic at the userspace layer
- [memory-forensics-volatility](../memory-forensics-volatility/SKILL.md) - the acquisition that survives a listing rewrite
- [kernel-exploitation](../kernel-exploitation/SKILL.md) - the other kernel-level route to the same visibility
- [linux-privesc-gtfobins-master](../linux-privesc-gtfobins-master/SKILL.md) - how the CAP_SYS_ADMIN this requires is usually obtained
