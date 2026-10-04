---
name: kernel-lpe-triage
version: "1.0.0"
description: Assess Linux kernel LPE exposure — Copy Fail, Dirty Frag, Fragnesia, live-patch vs. reboot remediation paths, framework gap declarations
triggers:
  - kernel lpe
  - privilege escalation
  - copy fail
  - dirty frag
  - fragnesia
  - cve-2026-31431
  - cve-2026-43284
  - cve-2026-46300
  - linux root
  - kernel patch
  - live kernel patch
data_deps:
  - d3fend-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs:
  - T1068
  - T1548.001
framework_gaps:
  - NIST-800-53-SI-2
  - ISO-27001-2022-A.8.8
  - PCI-DSS-4.0-6.3.3
  - NIS2-Art21-patch-management
  - NIST-800-53-SC-8
  - CIS-Controls-v8-Control7
  - UK-CAF-D1
  - AU-Essential-8-Patch
rfc_refs:
  - RFC-4301
  - RFC-4303
  - RFC-7296
cwe_refs:
  - CWE-125
  - CWE-362
  - CWE-416
  - CWE-672
  - CWE-787
d3fend_refs:
  - D3-ASLR
  - D3-EAL
  - D3-PA
  - D3-PHRA
  - D3-PSEP
  - D3-SCP
forward_watch:
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12 or sooner via Patch Tuesday) — Windows 11 LPE improper access control by DEVCORE (Angelboy + TwinkleStar03); track MSRC advisory and KEV add
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12 or sooner via Patch Tuesday) — Windows 11 LPE heap buffer overflow by Marcin Wiązowski; track MSRC advisory and KEV add
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12 or sooner via Patch Tuesday) — Windows 11 LPE 2x use-after-free by Kentaro Kawane (GMO); track MSRC advisory and KEV add
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — RHEL race-condition LPE by chompie / IBM X-Force XOR; track Red Hat advisory and KEV add
last_threat_review: "2026-09-28"
---

# Kernel LPE Triage

## Threat Context (mid-2026)

### Copy Fail — CVE-2026-31431

**Classification:** Local Privilege Escalation | CISA KEV | AI-Discovered  
**CVSS:** 7.8 (High) | **RWEP:** 90/100

An AI system discovered this vulnerability in approximately one hour. It is a page-cache copy-on-write (CoW) primitive in the Linux kernel affecting all major distributions since kernel 4.14 (2017). Every major Linux distribution is affected: RHEL 7–9, Ubuntu 18.04–24.04, Debian 9–12, CentOS, Fedora, Amazon Linux 2/2023, SUSE 12/15, Alpine, and derivatives.

Key characteristics that make this exceptional:
- **Deterministic exploitation** — no race condition, no heap spray, no timing sensitivity
- **Single-stage** — 732-byte script achieves root from unprivileged user in one step
- **No privileges required** — accessible from any unprivileged container or local user
- **No user interaction** — fully automated
- **CISA KEV listed** — active exploitation confirmed in the wild

The attack abuses a write primitive in the copy-on-write path of the page cache. An attacker with any local code execution can reliably escalate to root. In containerized environments without proper namespace isolation, this means container escape.

**What SI-2 says:** "Identify, report, and correct information system flaws; install security-relevant software updates within organizationally defined time periods."  
**Why SI-2 fails here:** The control is operationalized as a patch cycle (typically 30 days for High, 7 days for Critical). Copy Fail has a public PoC, is CISA KEV listed, and takes 732 bytes and zero expertise to exploit. The 30-day window is not a security window — it is an exploitation window.

---

### Dirty Frag — CVE-2026-43284 + CVE-2026-43500

**Classification:** Local Privilege Escalation Chain | Breaks IPsec Mitigations  
**CVSS / RWEP:** CVE-2026-43284 (CVSS 8.8 High, RWEP 53/100), CVE-2026-43500 (CVSS 7.6 High, RWEP 47/100)

Discovered by Hyunwoo Kim with AI assistance, per Sysdig's write-up. A two-CVE chain exploiting page-cache write primitives in:
- ESP/IPsec subsystem (CVE-2026-43284)
- RxRPC subsystem (CVE-2026-43500)

Key characteristics:
- **Disclosed before patches existed** — no coordinated disclosure window observed
- **Single command** — root access via one-line invocation
- **Breaks IPsec** — the exploit path runs through the IPsec subsystem, meaning the exploit actively compromises the IPsec subsystem as it runs. Controls that rely on IPsec for network isolation cannot be considered mitigating controls for this vulnerability.
- **Chained primitive** — more sophisticated than Copy Fail; requires kernel version fingerprinting to select the right gadget chain

The IPsec dimension is critical: organizations with network segmentation controls implemented via IPsec tunnels cannot claim those controls mitigate Dirty Frag exposure. The exploitation path breaks those controls.

**What SC-8 (Transmission Confidentiality and Integrity) says:** Implement cryptographic mechanisms to prevent unauthorized disclosure during transmission.  
**Why SC-8 fails here:** Dirty Frag exploits the IPsec implementation itself. SC-8 compliance via IPsec does not mitigate an LPE that runs through the IPsec subsystem.

---

### Fragnesia — CVE-2026-46300

**Classification:** Local Privilege Escalation | Dirty Frag family sequel | AI-Assisted Discovery  
**CVSS:** 7.8 (High) | **RWEP:** 35/100 (60 on a CISA KEV listing)

Disclosed 2026-05-13 by William Bowling (V12 security team). The Hacker News and Help Net Security attribute the discovery to William Bowling of Zellic working with Zellic's AI-agentic software auditing tool. Same primitive class as Dirty Frag — Fragnesia is the sibling bug introduced by the patch for CVE-2026-43284 / CVE-2026-43500. The defect is in `skb_try_coalesce()`: when transferring paged fragments between socket buffers, the kernel fails to propagate the `SKBFL_SHARED_FRAG` marker, losing track of externally-backed fragments (page-cache pages spliced from a file). An unprivileged local user can deterministically overwrite read-only file data in the kernel page cache without modifying the on-disk file. Public PoC targets `/usr/bin/su` for a one-line root shell.

Key characteristics:
- **Deterministic exploitation** — no race condition, no kernel-version fingerprinting beyond the affected version range.
- **Public PoC** — one-liner against `/usr/bin/su` from the V12 disclosure.
- **Page-cache corruption without on-disk write** — file-integrity tools that hash on-disk bytes (AIDE, Tripwire, IMA in measure-only mode) cannot detect the corruption.
- **Module-unload mitigation is identical to Dirty Frag** — blacklist `esp4`, `esp6`, `rxrpc` in `/etc/modprobe.d/`. Any host already mitigated for Dirty Frag by module blacklist is already mitigated for Fragnesia, with no further action required.
- **Live-patch is non-reboot** — AlmaLinux + CloudLinux kernels in testing as of 2026-05-13; Canonical Livepatch + kpatch follow standard cadence.
- **Not CISA KEV-listed as of the 2026-09-27 KEV catalog**, and no active exploitation has been observed in the wild. RWEP is 35; a KEV listing takes it to 60, and confirmed active exploitation to 80.

**Lesson for operators:** when a CVE patch lands, retain the pre-patch compensating controls (module blacklists, sysctl restrictions) until the patched code has soaked. Fragnesia is the canonical case — the Dirty Frag patch introduced Fragnesia, and the same `modprobe -r esp4 esp6 rxrpc` mitigation covers both.

**Detection signature (page-cache-aware):**
```
# Drop caches, read fresh from disk, compare to page-cache-resident copy
sha256sum /usr/bin/su
echo 3 > /proc/sys/vm/drop_caches
sha256sum /usr/bin/su
# Mismatch indicates page-cache corruption — primary forensic signature
```

---

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| NIST 800-53 Rev 5 | SI-2 Flaw Remediation | Network-centric patch cycles, 2013–2020 era | "Timely" is undefined for instant-root deterministic LPEs with public PoC. 30-day window = exploitation window. |
| NIST 800-53 Rev 5 | SC-8, SC-28 | Network/storage encryption via standard protocols | Dirty Frag exploits IPsec implementation — SC-8 controls via IPsec are not compensating controls for CVE-2026-43284 |
| ISO 27001:2022 | A.8.8 Management of technical vulnerabilities | Patch management timelines defined by risk classification | No framework for kernel-specific live patching vs. reboot requirement. "Appropriate timescales" undefined for CISA KEV + public PoC. |
| PCI DSS 4.0 | 6.3.3 | Critical patches within 1 month, all others within 3 months | 1-month window for a 732-byte public PoC is operationally indefensible. No guidance for live kernel patching on PCI-scoped systems. |
| NIS2 Directive | Art. 21 (vulnerability handling) | Systematic patch management for essential/important entities | No guidance on live kernel patching as a required capability. "Appropriate measures" undefined for CISA KEV LPEs. |
| CIS Controls v8 | Control 7 (Continuous Vulnerability Management) | Regular vulnerability scanning and patching | IG1/IG2/IG3 all recommend "remediate within one month" for critical — same problem as PCI. No live-patch framework. |
| ASD Essential 8 | Patch Operating Systems (Maturity 1–3) | Maturity 3: "within 48 hours" for critical with public exploit | Closest to adequate. ML3 "48 hours" with public exploit is approaching the right frame. Still no live-patch operationalization. |

**Spec layer vs. implementation layer.** Dirty Frag (CVE-2026-43284, CVE-2026-43500) exploits the Linux kernel's IPsec ESP implementation, not the underlying protocol specifications. The spec layer is defined by RFC 4301 (IPsec architecture), RFC 4303 (ESP datagram format), and RFC 7296 (IKEv2) — see `data/rfc-references.json` for status and errata. NIST 800-53 SC-8 and equivalent transmission-confidentiality controls implicitly cite this RFC family but do not operationalize the gap between *spec compliance* and *kernel-implementation safety*: an IPsec deployment can be fully RFC-conformant and still expose root via the ESP path. Auditors evaluating IPsec controls must ask whether the kernel is patched against CVE-2026-43284/-43500, not just whether the spec is followed.

---

## TTP Mapping (MITRE ATT&CK Enterprise, mid-2026)

Each CVE class in this skill maps to ATT&CK technique IDs declared in frontmatter (`T1068`, `T1548.001`). Gap flags identify which standard controls fail against the specific TTP variant — these are the controls a compliance-passing org will rely on, and which the exploit walks past.

| CVE Class | ATT&CK Technique | Sub-Technique / Variant | Gap Flag (Controls That Fail) |
|---|---|---|---|
| CVE-2026-31431 (Copy Fail) | T1068 — Exploitation for Privilege Escalation | Page-cache CoW write primitive; deterministic, single-stage; no race | NIST 800-53 SI-2 30-day SLA (exploitation window for 732-byte public PoC); ISO 27001:2022 A.8.8 "appropriate timescales" undefined for CISA KEV; PCI DSS 4.0 6.3.3 1-month critical window is indefensible; CIS Controls v8 Control 7 IG3 "within one month" identical failure |
| CVE-2026-31431 (Copy Fail — container escape variant) | T1611 — Escape to Host | Privileged container or shared host namespace + Copy Fail = host root | NIST 800-53 SC-39 (Process Isolation) assumes kernel boundary is intact; Copy Fail breaks it. No framework requires kernel CVE status be tracked as a precondition for container isolation claims. |
| CVE-2026-43284 (Dirty Frag — ESP/IPsec) | T1068 — Exploitation for Privilege Escalation | Chained page-cache write through ESP/IPsec; requires kernel fingerprinting | NIST 800-53 SC-8 (Transmission Confidentiality) when implemented via IPsec — control runs through the vulnerable subsystem and cannot be claimed as compensating; NIS2 Art. 21 "appropriate measures" silent on crypto-subsystem-CVE → control-degradation linkage |
| CVE-2026-43500 (Dirty Frag — RxRPC) | T1068 — Exploitation for Privilege Escalation | Chain component via RxRPC subsystem | ISO 27001:2022 A.8.8 — no requirement to inventory loaded kernel modules against active CVE chains; ASD Essential 8 ML3 48h-with-exploit window still long for chained public PoC |
| Both classes (post-exploit token abuse) | T1548.001 — Abuse Elevation Control Mechanism: Setuid and Setgid | Setuid binary or capability abuse following LPE foothold | NIST 800-53 AC-6 (Least Privilege) assumes UID boundary holds; after T1068 root, AC-6 audit trail shows legitimate root actions — control surface is gone |
| Both classes (detection gap) | T1068 (detection) | auditd/eBPF coverage for `userfaultfd`, `/proc/self/mem` writes, unprivileged-userns-clone | Missing entirely — no framework (NIST, ISO, PCI, NIS2, CIS, Essential 8) requires kernel-LPE exploitation-pattern detection rules. Detection-as-compensating-control claims are unverifiable without these rules. |

Note: ATLAS refs are intentionally empty in frontmatter — these are Linux kernel LPEs, not AI/ML TTPs. Cross-cutting AI-discovery context (Copy Fail was AI-found in ~1h) is captured in the Threat Context section, not via an ATLAS TTP ID.

---

## Exploit Availability Matrix

| CVE | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch Available | Live Patch | Reboot Required |
|---|---|---|---|---|---|---|---|---|---|
| CVE-2026-31431 (Copy Fail) | 7.8 | 90 | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte script | Yes | Confirmed | Yes | Yes (kpatch/livepatch/kGraft) | Yes |
| CVE-2026-43284 (Dirty Frag ESP) | 8.8 | 53 | No | Yes | Yes (AI-assisted) | Suspected | Yes | No (kpatch RHEL-only) | Yes |
| CVE-2026-43500 (Dirty Frag RxRPC) | 7.6 | 47 | No | Yes (chain component) | Yes (AI-assisted) | Suspected | Yes | No | Yes |
| CVE-2026-46300 (Fragnesia) | 7.8 | 35 | No (likely candidate) | Yes — one-liner vs /usr/bin/su | Yes (AI-assisted) | None observed | Yes (testing on Alma/CloudLinux) | Yes (kpatch / canonical-livepatch / KernelCare) | No (module-unload mitigation is non-reboot) |

---

## Compliance Theater Check

Run this check for any org claiming patch-management compliance for kernel LPE class CVEs:

> "Your patch-management control (NIST SI-2 / ISO 27001:2022 A.8.8 / PCI-DSS v4 6.3.3 / NIS2 Art. 21(2)(g) / UK-CAF B4 / AU ISM-1695) documents a 30-day remediation window for Critical/High CVEs. CVE-2026-31431 (Copy Fail) is CISA KEV listed with a public deterministic exploit requiring no privileges and KEV listing dated 2026-05-01. What is the actual time, on this fleet, between KEV listing and confirmed patch-or-mitigate for the affected kernel versions? If that interval exceeds 72 hours without live-patching as a deployed capability for the affected hosts, the patch-management control is theater for the KEV-class kernel-LPE threat surface."

**Theater fingerprints (any of these reduces the control to paper compliance):**

- Patch SLA is measured against advisory-publication date, not KEV-listing date — KEV listings are the operational signal that exploitation is happening now, and the SLA must trigger from there.
- The fleet inventory cannot answer "which hosts run the affected kernel version" within minutes — without live inventory, the SLA cannot be measured.
- Live-patching is described as "available" but no kernel was live-patched in the last 30 days — capability without operation is theater.
- The compensating-controls plan for hosts that cannot be rebooted within SLA is undocumented or relies on controls the CVE PoC bypasses (e.g. AppArmor profiles where the exploit runs as the legitimate user).
- "Patch management" includes only OS vendor patches, not third-party kernel modules or out-of-tree drivers — Dirty Frag RxRPC class lives in the network subsystem and is often patched on an asymmetric cadence.

**Real requirement:** patch SLA anchored to KEV listing date, fleet inventory live enough to answer "affected hosts" in under 5 minutes, live-patching deployed and exercised in the prior 30 days, written compensating-controls plan that survives the PoC test, third-party kernel modules in scope.

---

## Analysis Procedure

When a user invokes this skill, perform this assessment in order:

### Step 1: Inventory the environment

Ask for or assess:
- Linux distribution and version
- Kernel version (`uname -r`)
- Deployment model: bare metal / VM / container / serverless
- Existing live-patching capability: kpatch (RHEL), livepatch (Ubuntu), kGraft (SUSE), or none
- Whether IPsec is used for any network segmentation or encryption controls
- Current patch management SLA (how many days for Critical/High CVEs)
- Whether systems can tolerate a reboot (and when)

### Step 2: Determine exposure

**Copy Fail (CVE-2026-31431):**
```
Exposed if: kernel >= 4.14 AND kernel < [patched version for distribution]
Patched versions:
  RHEL 8/9:        kernel-4.18.0-553.xx.el8 / kernel-5.14.0-427.xx.el9
  Ubuntu 22.04:    linux-image-5.15.0-<patch-revision> (check USN-7<advisory-number>)
  Ubuntu 24.04:    linux-image-6.8.0-xxx (check USN-7<advisory-number>)
  Debian 12:       6.1.xxx (check DSA-5xxx)
  Amazon Linux 2:  kernel 5.10.xxx (check ALAS-2026-<advisory-number>)
  SUSE 15:         kernel 5.14.xxx (check SUSE-SU-2026:xxx)
```

**Dirty Frag (CVE-2026-43284/43500):**
```
Exposed if: IPsec or RxRPC modules loaded AND kernel < patched version
Check: lsmod | grep -E 'esp|xfrm|rxrpc'
Additional exposure: any IPsec-based network control becomes unreliable
```

**Fragnesia (CVE-2026-46300):**
```
Exposed if: kernel >= 5.10 AND kernel < [Fragnesia-patched version for distribution]
            AND any of esp4 / esp6 / rxrpc loaded
Check: uname -r; lsmod | grep -E '^(esp4|esp6|rxrpc)\b'
Mitigation (no reboot): blacklist the unused modules in /etc/modprobe.d/fragnesia.conf
  install esp4  /bin/false
  install esp6  /bin/false
  install rxrpc /bin/false
  (or just: modprobe -r esp4 esp6 rxrpc; only ESP / RxRPC users need to retain them)
Identical mitigation set to Dirty Frag — hosts already blacklisted from the
CVE-2026-43284/43500 response are already mitigated for Fragnesia.
```

### Step 3: Score exposure level

| Condition | Exposure Level |
|---|---|
| Kernel unpatched + no live patch + public internet access | Critical |
| Kernel unpatched + no live patch + internal only | High |
| Kernel unpatched + live patch deployed | Medium (verify live patch applied: `kpatch list` or `canonical-livepatch status`) |
| Kernel patched but reboot pending | Medium |
| Kernel patched + rebooted | Low |
| Containerized + privileged mode or host PID namespace | Add one severity level |
| IPsec used for network controls + CVE-2026-43284 unpatched | Add: "IPsec controls not compensating for Dirty Frag" |

### Step 4: Generate remediation path

**If live patching is available and system cannot tolerate reboot:**
1. Deploy live kernel patch immediately (kpatch/livepatch/kGraft)
2. Verify patch applied: `kpatch list` / `canonical-livepatch status`
3. Schedule reboot at next maintenance window to apply full kernel update
4. Document: "Live patch deployed YYYY-MM-DD; full patch pending reboot at [maintenance window]"

**If no live patching available and system cannot tolerate reboot:**
1. Compensating controls (reduce blast radius, do not eliminate exposure):
   - Seccomp profile restricting `userfaultfd`, `TIOCCONS`, and page-cache-adjacent syscalls
   - User namespace restrictions (`sysctl -w kernel.unprivileged_userns_clone=0` where supported)
   - Network-level isolation of affected hosts
   - Enhanced monitoring: eBPF/auditd rules for exploitation patterns (see detection section)
2. Document as open risk with compensating controls and reboot timeline
3. CISA KEV listing requires documented remediation or mitigation with timeline

**If system can tolerate reboot:**
1. Apply kernel update immediately
2. Reboot to load new kernel
3. Verify: `uname -r` shows patched version

**For containerized workloads:**
- The container host kernel determines exposure — container image patching is irrelevant
- Privileged containers with Copy Fail exposed = host root exposure
- Apply host kernel patch or live patch
- Remove `--privileged` and shared host namespaces from containers where possible

### Step 5: Compliance theater check

Run this check for any org claiming patch management compliance:

> "Your patch management control (SI-2 / A.8.8 / PCI 6.3.3) documents a 30-day remediation window for Critical/High CVEs. CVE-2026-31431 (Copy Fail) is CISA KEV listed with a public 732-byte exploit script requiring no privileges. What is the actual time between CISA KEV listing (2026-05-01, federal due 2026-05-15) and confirmed patch-or-mitigate? If it exceeds 72 hours without live patching as a deployed capability, the patch management control is theater for CISA KEV class vulnerabilities."

### Step 6: Assess IPsec dependency

If the organization uses IPsec for any of the following, flag explicitly:
- Network segmentation between security zones
- Encryption of inter-host traffic
- VPN tunnels for site-to-site connectivity
- Compliance with SC-8 or equivalent

Flag: "Dirty Frag (CVE-2026-43284) exploits the IPsec implementation. Network controls relying on IPsec cannot be claimed as compensating controls for this vulnerability. These controls should be noted in the risk assessment as providing reduced assurance until CVE-2026-43284 is fully patched."

---

## Output Format

The triage produces a structured Kernel LPE Exposure Assessment per host or fleet snapshot. The shape below is consumed downstream by `exploit-scoring` (which converts the per-CVE exposure into RWEP bands), by `incident-response-playbook` (which uses the affected-host count to scope IR), and by `compliance-theater` (which compares the deployed-mitigation field against the org's claimed SI-2 / A.8.8 patch SLA). Operators surfacing the output to auditors should preserve the CISA KEV due-date field verbatim — federal due dates are the authoritative regulatory clock, not internal SLAs.

Produce this structure:

```
## Kernel LPE Exposure Assessment

**Assessment Date:** YYYY-MM-DD  
**Kernel Version:** x.x.x  
**Distribution:** [name + version]

### Exposure Summary
| CVE | Status | Severity |
|-----|--------|----------|
| CVE-2026-31431 (Copy Fail) | [Exposed / Live-patched / Patched] | [Critical/High/Medium/Low] |
| CVE-2026-43284 (Dirty Frag ESP) | [Exposed / Patched] | [Critical/High/Medium/Low] |
| CVE-2026-43500 (Dirty Frag RxRPC) | [Exposed / Patched] | [Critical/High/Medium/Low] |
| CVE-2026-46300 (Fragnesia) | [Exposed / Module-unloaded / Live-patched / Patched] | [Critical/High/Medium/Low] |

### IPsec Control Impact
[If applicable: which network controls are affected by Dirty Frag]

### Remediation Path
[Live patch or full patch instructions for this specific distro/version]

### Compensating Controls (if no-reboot required)
[Specific sysctl settings, seccomp profiles, monitoring rules]

### Framework Gap Declaration
[Per-framework statement of what the org's patch management control covers and where it falls short]

### Compliance Theater Check Result
[Date of CISA KEV listing vs. date of remediation — theater flag if > 72h without live patch capability]

### RWEP Scores
CVE-2026-31431: CVSS 7.8 / RWEP 90 — immediate action required (4h)
CVE-2026-43284: CVSS 8.8 / RWEP 53 — remediate within 7 days; disable RxRPC/IPsec chain if not required
CVE-2026-43500: CVSS 7.6 / RWEP 47 — remediate within 7 days; consider disabling RxRPC module
CVE-2026-46300: CVSS 7.8 / RWEP 35 — patch within standard cycle; module unload (esp4/esp6/rxrpc) is the immediate non-reboot mitigation. Same mitigation set as Dirty Frag — already-blacklisted hosts are already covered. Reassess on a CISA KEV listing, which adds 25 points.
```

---

## Detection Rules

If patching is delayed, deploy these detection rules:

**auditd — Copy Fail exploitation pattern:**
```
-a always,exit -F arch=b64 -S userfaultfd -k lpe_attempt
-a always,exit -F arch=b64 -S process_vm_writev -k lpe_attempt
-w /proc/self/mem -p w -k lpe_mem_write
```

**sysctl hardening (reduce attack surface, not a full mitigation):**
```
kernel.unprivileged_userns_clone = 0
kernel.perf_event_paranoid = 3
kernel.kptr_restrict = 2
vm.unprivileged_userfaultfd = 0
```

**Monitoring alert:** Any unprivileged process writing to `/proc/[pid]/mem` or invoking `userfaultfd` outside of a known application allowlist should be treated as a potential LPE attempt.

---

## Defensive Countermeasure Mapping

Maps the kernel LPE findings above to MITRE D3FEND techniques with explicit defense-in-depth layer position, least-privilege scope, and zero-trust posture. Source: `data/d3fend-catalog.json`.

| D3FEND Technique | Mapping | Defense-in-Depth Layer | Least-Privilege Scope | Zero-Trust Posture |
|---|---|---|---|---|
| **D3-PSEP** (Process Segment Execution Prevention) | Counters T1068 page-cache CoW write primitives (Copy Fail) and adjacent kernel write-where exploits by enforcing NX / W^X on user-mapped segments and rejecting writeable-and-executable kernel mappings. | Layer 1 (Harden — kernel build flags + runtime mitigations: SMEP, SMAP, KPTI, KRG). | Per-system — the entire kernel image is the principal scope. | Treat every userspace write to a kernel-shared mapping as untrusted until verified by an immutable mapping policy; auditd / eBPF rules emit a tamper signal on any anomalous write path. |
| **D3-ASLR** (Address Space Layout Randomization) | Raises the cost of reliable kernel LPE exploitation by randomising kernel base and module load addresses; Copy Fail is deterministic without an info-leak primitive, so KASLR alone is not sufficient but is the first-floor mitigation against the broader class. | Layer 1 (Harden). | Per-boot — randomisation applies system-wide each boot. | Combine with `kernel.kptr_restrict=2` (already in the sysctl block above) so unprivileged processes cannot read kernel pointers that would defeat KASLR. |
| **D3-EAL** (Executable Allowlisting) | Restricts which userspace executables can run on the host. A Copy Fail PoC is a 732-byte binary; allowlisting denies unauthorised execution of any binary not on the allowlist, raising the cost of post-exploit shell payloads even when the in-kernel write itself succeeds. | Layer 2 (Harden — execve gate). | Per-system / per-workload — fleet baselines (gold images) define the allowlist; SOC / EDR enforces it. | Verify the binary identity on every `execve`; reject on hash mismatch. In ephemeral / serverless contexts bake the allowlist into the function image at build-time. |
| **D3-PHRA** (Process Hardware Resource Access) | Constrains hardware-resource access from userspace (page table writes via `/proc/self/mem`, `userfaultfd`, `process_vm_writev`) that the Copy Fail PoC relies on. The sysctl hardening above (`vm.unprivileged_userfaultfd=0`, `kernel.unprivileged_userns_clone=0`) is the D3-PHRA enforcement layer. | Layer 1 (Isolate — kernel-syscall surface). | Per-process — capability set + namespace + seccomp filter define the syscall allowlist. | Default-deny: an unprivileged process gets the minimum syscall surface and is denied `userfaultfd`, `unshare(CLONE_NEWUSER)`, and `process_vm_writev` unless explicitly required. |
| **D3-SCP** (System Call Filtering) | Per-container / per-workload seccomp profile blocks the syscalls Copy Fail abuses (`userfaultfd`, `process_vm_writev`, `pwritev2`) without requiring kernel patch. For container-escape variants (T1611 — Copy Fail in a privileged container), this is the only viable runtime mitigation between KEV-listing and the next reboot window. | Layer 2 (Isolate — runtime syscall gate). | Per-container — runtime profile is the principal scope. | Define a default-deny seccomp baseline; the host kernel patch is necessary but seccomp is the per-workload extension that survives an unpatched kernel during the live-patch deployment window. |
| **D3-PA** (Process Analysis) | Detects post-exploit anomalies — root shell spawned by previously-unprivileged process, suid-binary creation, capability escalation — that follow a Copy Fail-class write. The auditd and Falco / Tetragon rules in the Detection Rules section above are the D3-PA enforcement layer. | Layer 5 (Detect). | Per-host — SOC / EDR ingest the audit stream. | Continuously evaluate process lineage; alert on uid transitions, capability gains, or suid mounts that don't appear in the baseline. |

**Defense-in-depth posture:** the live-patch is the closure; the five D3FEND techniques above are the layers that must remain active *during* the live-patch deployment window. A SOC claiming "we have EDR" is at one D3FEND layer (D3-PA) for a six-layer-deep finding — the harden / isolate / detect stack collapses to a detect-only posture, and a kernel-write primitive that succeeds before EDR fires is unrecoverable. In ephemeral / serverless contexts, D3-PSEP / D3-EAL / D3-SCP / D3-PHRA are configured at image build time; the host-kernel layer remains the CSP's responsibility for managed runtimes, with the consumer responsible for the guest-OS posture on IaaS workloads.

---

## Hand-Off / Related Skills

After producing the kernel LPE triage output, the operator should chain into the following skills. Each entry names a downstream or sibling skill and the specific reason to invoke it from this finding.

- **`exploit-scoring`** — recalculate RWEP when any of the inputs that drive the score change post-triage: a new CISA KEV listing for Dirty Frag, confirmed active exploitation of either leg, or an AI-discovery flag flip. RWEP, not CVSS, is the prioritisation signal — re-run scoring rather than re-reading the static value in the matrix above.
- **`defensive-countermeasure-mapping`** — map each kernel LPE finding to D3FEND counters (D3-EAL for executable allowlisting at the kernel-module layer, D3-ASLR for address-space layout randomisation hardening, D3-PSEP for process self-modification prevention, D3-PHRA for process hardening / runtime attestation) and produce the defence-in-depth, least-privilege, zero-trust layered remediation plan rather than a single-control patch ticket.
- **`attack-surface-pentest`** — verify that the kernel LPE class is in the organisation's pen-test scope (TIBER-EU / DORA TLPT for EU financial-sector orgs, CBEST for UK financial, or the equivalent red-team programme). Most 2025-vintage pen-test scopes are perimeter / web-app focused and do not exercise local LPE primitives against the patched-kernel claim.
- **`compliance-theater`** — test whether the org's SI-2 / A.8.8 / PCI 6.3.3 patch-management evidence is CVSS-anchored theater for a KEV-listed, AI-discovered, 732-byte deterministic LPE. The 30-day window is the exploitation window; if the org cannot show live-patch-within-4-hours capability or documented compensating controls, the patch-management control is theater for this CVE class.
- **`policy-exception-gen`** — generate a defensible exception for ephemeral container workloads where the 30-day patch window is architecturally impossible: immutable image fleets, short-lived serverless functions, and Knative-style scale-to-zero workloads cannot accept a runtime patch and must instead document the compensating controls (host-kernel patched, seccomp profile, namespace isolation, unprivileged-userns disabled) as the exception evidence.
