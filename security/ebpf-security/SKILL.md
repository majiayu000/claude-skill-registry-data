---
name: ebpf-security
description: Use when assessing eBPF usage on Linux systems you own
  or are authorized to review. Covers eBPF program inventory,
  capability review, malicious eBPF detection, and safe development
  practices. Also use when investigating whether eBPF is abused for
  persistence or hiding.
version: 1.0.0
domain: linux
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [linux-hardening, systemd-deep, threat-hunting]
tools:
  - name: Python
    version: "3.12"
---

eBPF runs sandboxed programs in the kernel: observability,
networking, and security tools depend on it, and so can rootkits.
This skill covers the defensive review on systems you own:
inventorying loaded programs, checking who can load them, and
spotting malicious use. It is for defenders and auditors, not for
building offensive rootkits.

## Quick Workflow

1. Inventory loaded eBPF programs: what is attached, where, and by
   whom.
2. Check who can load eBPF: capabilities, unprivileged settings,
   and container access.
3. Review each program's purpose: known tool or unknown.
4. Look for malicious indicators: hiding, keylogging, backdoor
   triggers.
5. Check persistence: how the program gets reloaded after reboot.
6. Harden the loading path: restrict to privileged, audit loads.
7. Monitor: alert on new program loads outside change windows.
8. Document the baseline of expected programs.

## 1. Inventory and capability review

```bash
# List loaded programs (bpftool as tooling)
sudo bpftool prog show | head -30
sudo bpftool net show 2>/dev/null | head -10
# For each: type (kprobe, tc, xdp), name, and the owning process
```

```bash
# Who can load eBPF here
# - unprivileged eBPF: sysctl kernel.unprivileged_bpf_disabled (want 2)
# - CAP_BPF / CAP_SYS_ADMIN holders: who has them
sysctl kernel.unprivileged_bpf_disabled
# Containers: check for --privileged or CAP_BPF in the fleet
echo "unprivileged_bpf_disabled=2 is the hardened setting"
```

## 2. Malicious use indicators

```bash
# Hunt for the suspicious (on your own systems during investigation):
# - kprobes on credential or network functions with unknown owners
# - XDP/TC programs exfiltrating or redirecting traffic
# - programs with no matching installed security tool
sudo bpftool prog show | grep -i -E "xdp|kprobe" | head -20
# Correlate each program ID with its loader via /proc and audit logs
```

```bash
# Audit trail: who loaded what (auditd rule for bpf syscalls)
# auditctl -a always,exit -F arch=b64 -S bpf -k ebpf-load
ausearch -k ebpf-load --start recent 2>/dev/null | head -20
```

## Edge cases

- Legitimate security tools use eBPF heavily. Baseline them first;
  the unknown programs are the hunting ground.
- The kernel is old without CAP_BPF split. Then CAP_SYS_ADMIN
  governs; review its holders instead.
- Containers share the host kernel. A privileged container's eBPF
  is host eBPF; treat it as host compromise capability.

## Escalation

- Unknown program with hiding behavior: isolate the host and do
  full incident response; this is rootkit territory.
- Need the offensive view for red team: this skill stays
  defensive; scope offensive eBPF separately with authorization.

## Detection and defender view

eBPF abuse is detected through load auditing, program inventories
compared to baselines, and behavioral signs (hidden processes,
unexpected traffic). Defenders harden with unprivileged_bpf_disabled=2,
signed or reviewed programs where supported, and monitoring of the
bpf syscall. The durable stance: eBPF is powerful kernel access,
govern it like kernel module loading.

## Key references

- Linux kernel eBPF documentation and bpftool man pages.
- MITRE ATT&CK T1014 (Rootkit): eBPF techniques.
- Related skills: linux-hardening, threat-hunting.
