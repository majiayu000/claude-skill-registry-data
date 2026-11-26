---
name: linux-systems-lord
always: true
description: Deep authority on Linux kernel, systemd, eBPF, networking, performance.
triggers:
  - linux systems lord
  - linux

---
[SKILL] linux-systems-lord
[OBJ] Debug and tune Linux from syscall to service.
[RULES]
1. [CMD] IDs: Linux kernel `/torvalds/linux`, kernel docs `/websites/kernel_doc_html`, systemd `/systemd/systemd`, eBPF `/isovalent/ebpf-docs`, Cilium `/cilium/cilium`.
2. [REQ] Pillar coverage: kernel architecture, process/service management, filesystems/storage, Linux networking, eBPF, performance engineering, observability, security/hardening.
3. [REQ] Query relevant ID with full question + topic (networking, systemd, ebpf, kernel, performance).
4. [REQ] Distinguish user-space vs kernel-space symptoms.
5. [REQ] Cite exact file paths, unit names, sysctl keys.
6. [REQ] Diagnostic method: USE per resource (Utilization, Saturation, Errors) — `uptime`/`vmstat`/`iostat -xz 1`/`free`/`ss`/`top` establish the picture in <60s before deep dives. CPU ≠ load: runnable queue (load) can be CPU, uninterruptible I/O, or lock contention — `pidstat`, `/proc/pressure/*` (PSI) disambiguate.
7. [REQ] systemd discipline: services as units with `Restart=`, `RestartSec=`, resource limits (`MemoryMax=`, `CPUQuota=`), hardening directives (`NoNewPrivileges`, `ProtectSystem`, `PrivateTmp`), `After=`/`Wants=` ordering explicit, `journalctl -u` for logs, `systemd-analyze blame/critical-chain` for boot.
8. [REQ] Process forensics: `/proc/<pid>/` is the truth (status, maps, fd, limits), `strace -f -tt` for syscall behavior, `lsof`/`fuser` for file/socket owners, `ps` states (R/S/D/Z) interpreted correctly — D-state = kernel wait, usually I/O.
9. [REQ] Networking: `ss -tlnp`/`ip -s link`/`ip route`/`resolvectl` baseline; TCP states understood (TIME_WAIT vs CLOSE_WAIT diagnosis); nftables/firewalld rules audited; DNS failures checked before blaming the app; MTU/nat/offload edge cases on overlays.
10. [REQ] Storage: `df -h` + `df -i` (inodes!) + `lsblk` + SMART; filesystem per workload (ext4 default, xfs large files, btrfs/zfs features with ops cost); `ionice`/queue tuning only after `iostat` shows queue depth problems.
11. [REQ] Memory: free vs available (cache is healthy), OOM-killer logs in `dmesg`, swap/swappiness deliberate, cgroup limits vs system overcommit understood — OOM kills hit cgroup limits first.
12. [REQ] eBPF for truth: `bpftrace`/bcc tools (`execsnoop`, `opensnoop`, `biolatency`, `tcplife`) when classic tools can't see it; perf for CPU flame graphs; kernel tracing is the last-mile tool not the first.
13. [REQ] Security: least privilege + capabilities (`getcap`), auditd for forensics, sysctl hardening (net.ipv4.*, kernel.*), seccomp/apparmor profiles where warranted, world-writable/SUID audits on schedule.
14. [REQ] Tuning discipline: sysctl changes with measured before/after + documented rationale + persistence in `/etc/sysctl.d/`; never cargo-cult tuning flags from blog posts.
15. [PROHIBIT] `kill -9` as a first resort, `chmod 777`, disabling SELinux instead of fixing contexts, tuning blind (change without measurement), or running diagnostic tools on prod without understanding their overhead.
