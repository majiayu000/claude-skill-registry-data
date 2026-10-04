---
name: zeroday-gap-learn
version: "1.0.0"
description: Run the zero-day learning loop — CVE to attack vector to control gap to framework gap to new control requirement
triggers:
  - zero day lesson
  - zeroday gap
  - what control gap enabled this
  - learn from exploit
  - exploit to control gap
  - what should have caught this
  - 0day learning
data_deps:
  - cve-catalog.json
  - zeroday-lessons.json
  - framework-control-gaps.json
  - atlas-ttps.json
atlas_refs: []
attack_refs: []
framework_gaps: []
forward_watch:
  - New CISA KEV entries
  - New ATLAS TTP additions in each ATLAS release
  - Framework updates that close previously open gaps
  - Vendor advisories for MCP/AI tool supply chain CVEs
last_threat_review: "2026-09-28"
discovery_mode: "standalone"  # operator-reached via `exceptd brief zeroday-gap-learn` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Zero-Day Learning Loop

Every significant zero-day is a test of the control landscape. The question is not only "how do we patch this?" — it is "what control, if it had existed and been implemented, would have prevented or detected this?" The answer tells us what frameworks are missing.

This skill runs the full learning loop: zero-day description → attack vector extraction → control gap identification → framework coverage assessment → new control requirement generation → exposure scoring.

---

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. This skill exists to *generate* TTP-to-gap mappings from incoming zero-days, not to consume a fixed set — its output flows back into `data/atlas-ttps.json` and `data/framework-control-gaps.json` as new entries. Pinning a static reference set here would mis-frame the loop: every TTP and gap mapped by any other skill is a legitimate input, and the skill's job is to produce the *next* entries, not to inherit a fixed subset.

---

## Threat Context (mid-2026)

The zero-day learning cycle has compressed. The frameworks have not.

- **41% of 2025 zero-days were discovered by attackers using AI-assisted reverse engineering** (GTIG 2025). Copy Fail (CVE-2026-31431) was AI-found in approximately one hour; Fragnesia (CVE-2026-46300, 2026-05-13) is the canonical 2026 anchor case — Zellic's agentic code-auditing tool surfaced an 18-year-old Linux kernel page-cache primitive in load-bearing OSS. The first documented AI-built in-the-wild zero-day surfaced 2026-05-11 (GTIG AI 2FA-bypass case). The exceptd catalog's 2026 AI-discovery rate now stands at 40% (4/10), tracking the GTIG reference. The historical learning rhythm — researcher disclosure → industry analysis → framework update cycle measured in quarters or years — is incompatible with AI-discovery cadence measured in weeks. CTID Secure AI v2 (2026-05-06) replaces v1 as the alignment target for the learning-loop outputs.
- **The compounding consequence**: when a zero-day is announced, the relevant question is no longer "when will the patch ship?" but "what control, if it had existed, would have stopped this, and how do we add that control to the next thousand systems before the AI-generated variant lands?" Without a running learning loop, every novel TTP becomes a one-off incident response rather than a control-system improvement.
- **AI-acceleration also compresses variant generation.** A single disclosed primitive (Copy Fail's deterministic page-cache CoW; SesameOp's AI-API C2 channel) can be re-applied by AI tooling to adjacent code paths within days. Frameworks that only respond to specific CVE-IDs miss the class-level lesson entirely.
- **Compliance frameworks do not include zero-day learning as a required control category.** The "learn from incidents" language in NIST CSF 2.0 IMPROVE and ISO 27001:2022 A.5.7 is process-only, no required artifact. An org can be fully compliant while patching every CVE and learning nothing.

This skill exists because the gap between AI-accelerated zero-day production and framework-driven control evolution is the dominant mid-2026 risk multiplier.

---

## Framework Lag Declaration

Frameworks do not require a zero-day learning loop as a control. The closest analogs are process controls without learning artifacts.

| Framework | Control | What It Says | Why It Fails as a Learning Loop |
|---|---|---|---|
| NIST CSF 2.0 | IMPROVE function (ID.IM) | "Identify improvements to organizational cybersecurity risk management processes, procedures, and activities." | Process-level guidance only. Does not require: (a) per-zero-day attack-vector extraction, (b) framework-gap mapping, (c) new-control-requirement generation, (d) measurable closure of identified gaps. Compliance is satisfied by having "an improvement process" without showing it produced any specific control. |
| NIST 800-53 Rev 5 | CA-7 (Continuous Monitoring) + IR-4 (Incident Handling — Lessons Learned) | Lessons learned from incidents and continuous monitoring. | Lessons-learned is required after incidents, but not after public zero-days the org wasn't directly hit by. The most valuable learning surface — other people's incidents — is outside the control's scope. |
| ISO 27001:2022 | A.5.7 (Threat intelligence) | Information about information security threats shall be collected and analyzed. | Threat-intel collection is required; learning-loop output (new control requirements, framework-gap artifacts) is not. Process compliance with zero learning output is auditable as "compliant." |
| ISO 27001:2022 | A.5.27 (Learning from information security incidents) | Knowledge gained from incidents shall be used to strengthen controls. | Limited to incidents the org experienced. Does not require learning from industry-wide zero-days that didn't hit the org. |
| SOC 2 | CC4 (Monitoring Activities) | Ongoing/separate evaluations of internal controls. | Evaluation cadence is internal-controls focused, not threat-landscape focused. No requirement to re-evaluate controls against newly-disclosed TTPs. |
| NIS2 Directive | Art. 21 — incident handling and crisis management | Essential/important entities must handle incidents. | Same scope problem: incidents the org experienced, not zero-days landing across the sector. |
| MITRE ATT&CK / ATLAS | TTP catalogs | Reference taxonomies. | Not frameworks of required controls — they describe TTPs, they do not require an org to maintain a learning loop against them. |

Across all of these: **the learning loop is not a required control output, only an implied behavior.** An org can pass every audit while patching CVEs and absorbing zero TTP-level lessons.

---

## TTP Mapping

This skill is meta — it does not pin to a single TTP class. The learning loop iterates over the full corpus declared in this skill's `data_deps`. Frontmatter `atlas_refs` and `attack_refs` are intentionally empty.

| Input Catalog | Role in the Learning Loop |
|---|---|
| `data/cve-catalog.json` | The CVE-level corpus: each entry is a candidate lesson input. New entries trigger a new loop run. |
| `data/atlas-ttps.json` (MITRE ATLAS v2026.09) | The AI/ML TTP taxonomy. Attack-vector extraction maps the CVE's mechanism to an ATLAS ID (e.g., AML.T0096 for SesameOp AI-as-C2). |
| `data/framework-control-gaps.json` | The control-gap corpus. Framework-coverage assessment writes into this file via new entries or `status` updates. |
| `data/zeroday-lessons.json` | The output corpus. Each completed loop produces one entry here — the durable artifact of the lesson. |

The skill consumes all four and produces a delta against `zeroday-lessons.json` and `framework-control-gaps.json`. Coverage of any one specific TTP is the responsibility of the topic-specific skills (`kernel-lpe-triage`, `ai-attack-surface`, `mcp-agent-trust`, `ai-c2-detection`).

---

## Exploit Availability Matrix

Status of the learning-loop entry for each CVE currently in `data/cve-catalog.json`:

| CVE | KEV | PoC | AI-Discovered / AI-Enabled | RWEP | Lesson-Entry Status in `zeroday-lessons.json` |
|---|---|---|---|---|---|
| CVE-2026-31431 (Copy Fail) | Yes | Yes (732-byte) | Yes (AI-discovered ~1h) | 90 | Complete — pre-run lesson encoded below; new control requirements CISA-KEV-RESPONSE-SLA, LIVE-PATCH-CAPABILITY, KERNEL-EXPLOITATION-DETECTION generated |
| CVE-2026-43284 (Dirty Frag — ESP/IPsec) | No | Yes (chain) | Yes (AI-assisted discovery) | 53 | Complete — pre-run lesson encoded; new control requirements CRYPTO-SUBSYSTEM-INTEGRITY, PRE-PATCH-DISCLOSURE-RESPONSE generated |
| CVE-2026-43500 (Dirty Frag — RxRPC) | No | Yes (chain) | Yes (AI-assisted discovery) | 47 | Complete — covered jointly with CVE-2026-43284 (chain partner) |
| CVE-2025-53773 (Copilot YOLO-mode RCE) | No | Yes (demonstrated) | Yes (AI tooling enables) | 30 | Complete — pre-run lesson encoded; new control requirements AI-TOOL-ACTION-AUTHORIZATION, AI-TOOL-INPUT-SANITIZATION, PROMPT-INJECTION-MONITORING generated |
| CVE-2026-30615 (Windsurf MCP local-vector RCE) | No | Yes | No (supply-chain) | 35 | Complete — pre-run lesson encoded; new control requirements MCP-SERVER-SIGNING, MCP-TOOL-ALLOWLIST, MCP-SUPPLY-CHAIN-AUDIT generated |
| CVE-2026-45321 (Mini Shai-Hulud TanStack npm worm) | Yes (2026-05-27) | Yes (worm in-wild) | No (engineering-grade chain) | 70 | Pre-run exemplar lesson encoded below (chained CI/CD primitives — Pwn Request + pnpm-store poisoning + OIDC theft); new control requirements PR-WORKFLOW-PRIVILEGE-CAP, ACTIONS-CACHE-INTEGRITY, OIDC-PUBLISH-AUDIT generated |
| MAL-2026-3083 (Elementary-Data PyPI worm — forged release via GitHub Actions script-injection) | No (OSSF Malicious Packages dataset; CISA KEV catalogues vendor CVEs only) | Yes (orphan commit + exfil domain confirmed in-wild during 8h window) | No (manual chain) | n/a | Pre-run exemplar lesson encoded below; control requirements GHACTIONS-EVENT-INTERPOLATION-BAN, INSTALL-HOOK-AUDIT, OSSF-MALPACKAGES-INGEST generated |
| CVE-2026-46300 (Fragnesia — Dirty Frag sequel) | No (candidate within days) | Yes (one-liner vs /usr/bin/su) | Yes (AI-assisted discovery with Zellic's agentic auditing tool) | 35 | Complete — pre-run lesson encoded below; control requirements PAGE-CACHE-INTEGRITY-VERIFICATION, BUG-FAMILY-MITIGATION-PERSISTENCE, SCANNER-PAPER-COMPLIANCE-TEST generated. Pattern: a patch for one bug class introduced a sibling bug in the same primitive class. |

Every new entry added to `data/cve-catalog.json` must produce a corresponding entry here and in `data/zeroday-lessons.json` before the catalog change ships. Any CVE in the catalog without a complete lesson entry is a pre-ship-checklist failure.

---

## The Learning Loop

```
Input: zero-day (CVE ID, description, or vulnerability class)
   ↓
Step 1: Attack vector extraction
   — What technical mechanism was used?
   — What privileges were required?
   — What was the exploitation complexity?
   ↓
Step 2: Defense chain analysis
   — What control SHOULD have prevented this exploitation?
   — What control SHOULD have detected this exploitation?
   — Was that control in any major framework?
   — Was it typically implemented?
   ↓
Step 3: Framework coverage assessment
   — For each major framework: does it have a control that covers this?
   — Is the control adequate (specific enough, actionable enough)?
   — Or is the control present but insufficient (too vague, wrong time horizon)?
   ↓
Step 4: Gap classification
   — Missing entirely: no framework has a control for this attack class
   — Insufficient: controls exist but are inadequate for this specific TTP
   — Compliant-but-exposed: org can pass audit of the control and still be vulnerable
   ↓
Step 5: New control requirement generation
   — What specific, testable control would actually address this?
   — What evidence would demonstrate the control is working?
   ↓
Step 6: Exposure scoring
   — How many compliance-passing orgs are still exposed?
   — What is the RWEP for this zero-day?
Output: Lesson entry for data/zeroday-lessons.json
```

---

## Pre-Run Lessons (Encoded from Documented Zero-Days)

### Lesson: CVE-2026-31431 (Copy Fail)

**Attack vector:** Page-cache copy-on-write primitive in the Linux kernel. Unprivileged local user. Deterministic. No race condition. Single-stage. 732 bytes.

**What control should have prevented this:**
- Prevention: No local code execution → no LPE opportunity. But local code execution is baseline in any multi-user system or container environment. Prevention at this layer is not realistic.
- Mitigation before patch: seccomp profile blocking `userfaultfd`, user namespace restrictions, kernel hardening. These reduce attack surface but do not eliminate it.
- Patch: Apply kernel update. Live patching (kpatch/livepatch/kGraft) enables patching without service interruption.

**What control should have detected this:**
- Detection: auditd/eBPF monitoring for exploitation patterns — privilege escalation from unprivileged context, unusual /proc/self/mem writes, userfaultfd usage outside known applications.
- None of these are required by any major framework.

**Framework coverage assessment:**

| Framework | Control | Assessment |
|---|---|---|
| NIST 800-53 SI-2 | Flaw Remediation | Present but insufficient: 30-day SLA is exploitation window for CISA KEV + public PoC |
| ISO 27001 A.8.8 | Technical vulnerability management | Present but insufficient: "appropriate timescales" undefined; no live-patch requirement |
| PCI DSS 6.3.3 | Critical patches within 1 month | Present but insufficient: same problem |
| ASD ISM-1877 and ISM-1696 | Patch within 48h of release when a working exploit exists | Closest to adequate, but: no live-patch mandate, and 48h is still long for a 732-byte public exploit; for workstations the 48h window applies only at Maturity Level Three |
| Any framework | Detection for LPE exploitation patterns | Missing entirely: no framework requires auditd/eBPF exploitation detection |
| Any framework | Live kernel patching as required capability | Missing entirely |

**New control requirements generated:**

1. **CISA-KEV-RESPONSE-SLA**: For any CVE on the CISA KEV catalog: deploy verified mitigation (patch, live patch, or documented compensating controls) within 4 hours of KEV listing or patch availability, whichever is later.

2. **LIVE-PATCH-CAPABILITY**: For any system that processes production workloads and cannot tolerate unplanned reboots: live kernel patching capability (kpatch, livepatch, kGraft, or equivalent) must be deployed and tested quarterly.

3. **KERNEL-EXPLOITATION-DETECTION**: Deploy auditd or eBPF-based monitoring rules for kernel privilege escalation indicators. Alert within 60 seconds of pattern detection.

**Exposure scoring:**
- RWEP: 90 (current, with patch+live-patch available)
- Organizations compliant with standard patch management controls but still exposed: estimated 80%+ during the first week after KEV listing (based on industry patch deployment lag data)
- Coverage failure: standard controls allow full exploitation window while displaying "compliant" status

---

### Lesson: CVE-2026-43284/43500 (Dirty Frag)

**Attack vector:** Page-cache write primitive chain through ESP/IPsec (CVE-2026-43284) and RxRPC (CVE-2026-43500) subsystems. Chained — requires fingerprinting to select correct gadget. Disclosed before patches existed.

**What control should have prevented/detected this:**
- Critical insight: the exploitation path runs through the IPsec subsystem → controls that rely on IPsec for network isolation are not compensating controls for Dirty Frag exposure

**New control requirements generated:**

1. **CRYPTO-SUBSYSTEM-INTEGRITY**: Network controls claiming compliance via IPsec must include: kernel CVE status for IPsec-related CVEs, and explicit acknowledgment if IPsec-based controls are degraded by an unpatched IPsec CVE.

2. **PRE-PATCH-DISCLOSURE-RESPONSE**: For vulnerabilities disclosed before patches exist: immediately inventory affected systems, isolate high-risk systems at network layer, deploy detection rules, commit to patch timeline.

---

### Lesson: CVE-2026-46300 (Fragnesia — Dirty Frag Sequel)

**Attack vector:** Page-cache corruption via XFRM ESP-in-TCP skb coalescing. `skb_try_coalesce()` drops the `SKBFL_SHARED_FRAG` marker when coalescing paged fragments between socket buffers, so the kernel loses track of externally-backed fragments (page-cache pages spliced from a file). An unprivileged local user deterministically overwrites read-only file data in the kernel page cache without modifying the on-disk file. Public PoC targets `/usr/bin/su` for a one-line root shell. Disclosed 2026-05-13 by William Bowling (V12 security team). Same primitive class as Dirty Frag (CVE-2026-43284 / CVE-2026-43500) — Fragnesia is the sibling bug introduced by the patch for the original Dirty Frag.

**What control should have prevented this:**
- Module-unload mitigation: blacklist `esp4` / `esp6` / `rxrpc` in `/etc/modprobe.d/`. Identical to the Dirty Frag mitigation set — operators who retained that blacklist after patching Dirty Frag are already mitigated for Fragnesia at zero additional operational cost.
- Bug-family-aware patch policy: when a CVE patch lands, retain the pre-patch compensating controls until the patched code has soaked. Operators who removed the Dirty Frag blacklist on patch landing re-exposed the host to the sibling bug.

**What control should have detected this:**
- Page-cache integrity verification: read the binary through the page cache (`vmtouch -v <path>; sha256sum <path>`), drop caches, re-read from disk, compare hashes. Mismatch is the primary forensic signature. File-integrity tools that hash on-disk bytes (AIDE, Tripwire, IMA in measure-only mode) miss this entirely because the on-disk file is unchanged.
- No major framework requires page-cache-aware integrity verification.

**Framework coverage assessment:**

| Framework | Control | Assessment |
|---|---|---|
| NIST 800-53 SI-2 | Flaw Remediation | Present but insufficient: 30-day SLA is exploitation window for deterministic public PoC; module-unload is non-reboot and immediate but not required as a compensating control |
| ISO 27001 A.8.8 | Technical vulnerability management | Present but insufficient: same "appropriate timescales" gap |
| NIS2 Art. 21(2)(c) | Patch-management measures | Present but insufficient: undefined for fast-cycle kernel LPEs with public PoC; module-blacklist not in scope |
| DORA Art. 9 | ICT incident management | Present but insufficient: presumes vendor-patch cadence; module-unload as immediate mitigation has no place in the typical DORA evidence pack |
| UK CAF B4 | System security | Silent on subsystem module disable as a compensating control |
| AU Essential 8 (ISM-1692, ISM-1877) | Patch applications and operating systems | The 48h windows run from the vendor's release rather than from public-exploit availability, and are still long for a deterministic public exploit |
| ISO 27001 A.5.7 | Threat intelligence | Collects feeds; does not require operational pivot when intel shows a same-family sequel to a previously-patched bug |
| Any framework | Page-cache integrity verification | Missing entirely — on-disk file-integrity tools cannot detect this class |

**New control requirements generated:**

1. **PAGE-CACHE-INTEGRITY-VERIFICATION**: For setuid binaries on production hosts, periodically (or on alert) read the binary through the page cache, drop caches, re-read from disk, and compare hashes. Mismatch indicates page-cache-resident corruption that on-disk-only file-integrity tools cannot detect.

2. **BUG-FAMILY-MITIGATION-PERSISTENCE**: When a CVE patch lands, retain the pre-patch compensating controls (module blacklists, sysctl restrictions) until the patched code has soaked for a stated review period. Patches for one bug in a primitive class can introduce sibling bugs in the same class — the Dirty Frag → Fragnesia chain is the canonical example.

3. **SCANNER-PAPER-COMPLIANCE-TEST**: A vulnerability scanner that reports "patched" based on kernel package version alone is paper compliance. The operational test: does the scan account for the module-unload mitigation surface, AND does it verify the kernel is on a build that includes the specific Fragnesia patch (not just any version newer than the Dirty Frag patch that introduced Fragnesia)?

**Exposure scoring:**
- RWEP: 35 today. A CISA KEV listing adds 25 (60), and confirmed active exploitation adds 20 more (80).
- Audit-passing orgs still exposed: ~75%. Operators who retained the Dirty Frag module blacklist are already mitigated. Operators who relied on kernel-package-version alone with vanilla SI-2 / A.8.8 SLAs are exposed during the patch window.
- Coverage failure: on-disk file-integrity tools (AIDE, Tripwire) report clean while the page-cache copy of /usr/bin/su is corrupted.

**Class-level lesson:** "patch landed therefore safe" assumes patches close bug families. The Dirty Frag → Fragnesia pattern shows a patch can introduce a sibling bug in the same primitive class. Treat every patch in a primitive class as opening a new soak window during which the pre-patch compensating controls remain active.

---

### Lesson: CVE-2025-53773 (GitHub Copilot YOLO-Mode RCE)

**Attack vector:** Hidden prompt injection in any agent-readable content (source comments, README, PR descriptions, retrieved docs, MCP tool responses) coerces Copilot agent mode to write `"chat.tools.autoApprove": true` to `.vscode/settings.json`. Every subsequent shell tool call then auto-approves; the demo runs `calc.exe` / `Calculator.app` via the auto-approved `run_in_terminal` tool. CVSS 7.8 / AV:L (local-vector — developer-side IDE interaction; the NVD-authoritative score was corrected from initial 9.6 / AV:N). Affected: Visual Studio 2022 17.14.0–17.14.11 (fixed 17.14.12); GitHub Copilot Chat extension predating the 2025-08 Patch Tuesday fix.

**What control should have prevented this:**
- Access control for AI tool actions: the developer's GitHub session was correctly authenticated. The RCE happened because the AI tool executed adversarial instructions with the developer's authorization context.
- There is no framework control for "AI tool authorization scope at the action level."

**New control requirements generated:**

1. **AI-TOOL-ACTION-AUTHORIZATION**: AI coding assistants must have explicitly scoped permissions. Any action taken by an AI tool (file write, terminal command, API call) requires explicit user approval unless within a pre-approved action whitelist. Implied authorization from context is insufficient.

2. **AI-TOOL-INPUT-SANITIZATION**: Content ingested by AI tools from external sources (PR descriptions, code comments, documentation, web pages) must be treated as potentially adversarial. AI tools should apply adversarial instruction classifiers to externally sourced content before including it in model context.

3. **PROMPT-INJECTION-MONITORING**: Log all AI tool actions, including the content of prompts that triggered those actions. Alert on AI actions that deviate from the user's stated intent or that weren't preceded by an explicit user request.

**Framework coverage:** Missing entirely in all major frameworks. Even after the CVSS correction to 7.8 / AV:L (which reflects the local-vector reality, not severity), there is no framework control category for "prompt-injection-driven autoApprove escalation" — the bottleneck on the *attack* is a settings-file write that IS detectable as an IOC, but no framework currently mandates monitoring it.

---

### Lesson: CVE-2026-30615 (Windsurf MCP Local-Vector RCE)

**Attack vector:** Malicious MCP server drives RCE in the AI assistant's user context once installed. The attack vector is local (AV:L) — the attacker must control HTML content the Windsurf MCP client processes; supply-chain prerequisite (typosquatting, dependency confusion, or compromise of a legitimate server) puts the malicious server in front of the client. CVSS 8.0 (NVD-authoritative; corrected from initial 9.8 / AV:N). 150M+ combined downloads of MCP-capable AI coding assistants share the architectural surface.

**New control requirements generated:**

1. **MCP-SERVER-SIGNING**: All MCP servers must have verifiable provenance (npm provenance attestation, signed manifest, or equivalent). AI coding assistants must refuse to load unsigned MCP servers.

2. **MCP-TOOL-ALLOWLIST**: AI clients must implement explicit tool allowlists. Default deny — only tools in the allowlist may be called, regardless of what the MCP server exposes.

3. **MCP-SUPPLY-CHAIN-AUDIT**: MCP server installations must go through the organization's third-party software audit process. Automated installation of MCP packages without review is equivalent to installing unaudited dependencies.

**Framework coverage:** Missing entirely. Supply chain security controls (SA-12, A.5.19) don't address MCP servers as a category.

---

### Lesson: SesameOp (ATLAS AML.T0096 — AI as C2)

**Attack vector:** Compromised host encodes C2 commands in LLM API prompt fields. Exfiltrated data returned in completion fields. Traffic indistinguishable from legitimate AI API usage.

**New control requirements generated:**

1. **AI-API-BEHAVIORAL-BASELINE**: All AI API usage from organizational networks must be baselined (which processes, which users, what volumes, what times). Deviations from baseline must trigger alerts.

2. **AI-API-PROCESS-ALLOWLIST**: Maintain an allowlist of processes authorized to make AI API calls. AI API calls from unlisted processes must alert.

3. **AI-API-CORRELATION**: Correlate AI API call events with security-relevant host events (file access, credential access, lateral movement). AI API calls correlated with security events within defined time windows must escalate.

**Framework coverage:** Missing entirely. SI-4 (system monitoring) and A.8.16 (monitoring activities) don't address AI API behavioral baselines.

---

### Lesson: CVE-2026-45321 (Mini Shai-Hulud TanStack npm worm)

**Attack vector:** Engineering-grade three-primitive chain against the TanStack monorepo, disclosed 2026-05-11. (1) `pull_request_target` on `bundle-size.yml` runs fork-PR code with base-repo permissions (classic Pwn Request). (2) That run poisons the `actions/cache` pnpm-store under the key `Linux-pnpm-store-${hashFiles('**/pnpm-lock.yaml')}` that `release.yml` later restores. (3) On the next main push, `release.yml` (which has `id-token: write` for npm publish) restores the poisoned cache and the worm captures the OIDC token. 84 malicious versions published across 42 @tanstack/* packages between 2026-05-11 19:20-19:26 UTC. ~150M weekly downloads in scope. CVSS 9.6; CISA added it to KEV on 2026-05-27. Attribution: TeamPCP. No AI-assisted exploit-development attribution for this specific instance, but the chain shape is exactly what AML.T0017-class capability development produces at AI cadence — chained CI/CD primitives that no individual component owner recognises as exploitable.

**What control should have prevented this:**
- Workflow-privilege isolation: `pull_request_target` should never run fork-PR code with base-repo permissions in the same job as cache writes. The chain is broken if the bundle-size workflow runs with `permissions: contents: read` and writes to a separate cache key.
- Cache integrity: `actions/cache` keyed by `hashFiles('**/pnpm-lock.yaml')` is attacker-influenceable when the same key is restored by a privileged downstream workflow. Restore-only-on-verified-publisher caches or per-job cache namespacing breaks the link.
- OIDC token scoping: the publish job's `id-token: write` should be bound to a job that does *not* restore externally-influenced caches. Token scope minimisation (no orphaned-privilege workflows).

**New control requirements generated:**

1. **PR-WORKFLOW-PRIVILEGE-CAP**: Any workflow triggered by `pull_request_target`, `pull_request` from forks, or `issue_comment` MUST declare `permissions: contents: read` at the top level and MUST NOT write to `actions/cache` keys that any other workflow restores. Static analysis at PR merge time.
2. **ACTIONS-CACHE-INTEGRITY**: Cache keys used by publish-capable workflows MUST be namespaced per-job and MUST NOT include `${{ hashFiles(...) }}` expressions that fork PRs can influence. Where shared caches are unavoidable, restore-then-verify against an out-of-band integrity record before use.
3. **OIDC-PUBLISH-AUDIT**: Every npm / container registry / cloud-provider OIDC token issuance from CI must be audit-logged with the job's full permission set, the workflow file SHA, and the cache keys it restored. Anomalies (cache restored from a key written by a different workflow) must alert.

**Exposure scoring:**
- Any consumer that ran `npm install` / `pnpm install` between 2026-05-11 19:20Z and 2026-05-11 ~21:00Z (yank propagation window) with a `@tanstack/*` package in their dependency tree is suspect. Lockfile resolution time-stamp is the join key.
- Coverage failure: no major framework requires CI workflow-privilege static analysis. Supply-chain controls (SA-12, A.5.19) address vendor SaaS not GitHub Actions workflow files.

---

### Lesson: MAL-2026-3083 (Elementary-Data PyPI Worm — Forged Release via GitHub Actions Script Injection)

**Attack vector:** Disclosed 2026-04-24, OSSF Malicious Packages primary key (no CVE assigned as of 2026-05-13; OSV-native MAL-2026-3083, Snyk cross-reference SNYK-PYTHON-ELEMENTARYDATA-16316110, kam193 campaign id `pypi/2026-04-compr-elementary-data`). Attacker abused a GitHub Actions script-injection sink in `.github/workflows/update_pylon_issue.yml`: the workflow interpolated `${{ github.event.comment.body }}` directly into a `run:` shell script. Commenting on any open PR was sufficient to execute attacker-controlled shell with the elevated `GITHUB_TOKEN`. Attacker forged orphan commit `b1e4b1f3aad0d489ab0e9208031c67402bbb8480` (still readable on GitHub) and the workflow built and published `elementary-data==0.23.3` to PyPI with an install-time `.pth`-file payload. Window of live exposure: 2026-04-24 22:20Z → 2026-04-25 ~06:30Z (~8 hours). 1.1M monthly downloads in scope. CVSS 9.3 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H). Exfiltration domain (`skyhanni.cloud` subdomain) was active throughout the window.

**What control should have prevented this:**
- GitHub Actions hygiene: never interpolate `${{ github.event.* }}` into a `run:` script — use the value as an environment variable instead so the shell tokeniser treats it as data. Static-analysis tools (`zizmor`, `Octoscan`) flag this class.
- Install-hook auditing: `.pth` files run at every `import` of any package in the same site-packages directory. The MAL-2026-3083 payload is invisible to `pip install --dry-run` but visible in the wheel's `RECORD` file. `pip install --require-hashes` plus consumer-side `pip-audit --strict` against the OSSF Malicious Packages dataset would have caught the malicious version.
- Ingest-time intel: OSSF Malicious Packages publishes within minutes of detection. A consumer pipeline that ingests OSSF + Snyk + npm advisory feeds with sub-hour latency closes the window in proportion to the attacker's, not in proportion to vendor advisory cadence.

**New control requirements generated:**

1. **GHACTIONS-EVENT-INTERPOLATION-BAN**: Static-analysis gate on every CI pipeline: reject any workflow that interpolates `${{ github.event.* }}` (or `github.head_ref`, `inputs.*` from untrusted sources) directly into `run:` shell. Required tooling: `zizmor` / `Octoscan` / `actionlint` with the script-injection rule enabled. Hard fail on PR merge.
2. **INSTALL-HOOK-AUDIT**: Pre-install scan of every wheel / sdist for install-time hooks (`.pth` files, `setup.py` execution, `pyproject.toml` build hooks). Any package adding a `.pth` file that imports network code at module-load time gets quarantined for review. Tooling: `pip-audit` plus a custom `.pth`-file diff rule.
3. **OSSF-MALPACKAGES-INGEST**: Subscribe to the OSSF Malicious Packages OSV feed with sub-hour latency and apply it as a hard-block at the dependency resolver. Any organisation whose dependency pipeline is anchored to NVD CVE feeds alone misses MAL-2026-3083 entirely — there is no CVE ID, just an OSSF / Snyk / kam193 advisory. This control closes the no-stale-threat-intel loop for the OSV-native malicious-package class.

**Exposure scoring:**
- Anyone who `pip install`-ed `elementary-data` between 2026-04-24 22:20Z and 2026-04-25 ~06:30Z inside a dbt analytics pipeline (or any virtualenv where `elementary-data==0.23.3` resolved) was hit. The install-hook fires at the *next* import in the affected venv, which can be hours-to-days after the install.
- Coverage failure: NVD CVE feed coverage is structurally zero (no CVE issued); SOC playbooks that filter on "is there a CVE ID?" miss the entire OSV-native class. OSSF Malicious Packages + Snyk Advisor + kam193 campaign feeds are the operational intel layer.

---

## Analysis Procedure for New Zero-Days

When a user provides a new CVE or vulnerability description:

### Step 1: Extract attack vector

Document:
- What technical capability does the attacker need to execute this?
- What system components are used in the attack path?
- What is the exploitation complexity? (deterministic / race condition / heap spray / etc.)
- Is the exploit AI-assisted or AI-discovered?
- What is the blast radius? (specific config / default config / all major distros)

### Step 2: Defense chain analysis

Ask and answer:
1. **Prevention control:** What configuration, capability, or process would have prevented this exploit from being possible?
2. **Detection control:** What monitoring rule or anomaly detection would have fired during exploitation?
3. **Response trigger:** What evidence would appear in logs or alerts during/after exploitation?

For each: Is this control required by any major framework?

### Step 3: Framework coverage matrix

Run through each applicable framework:
- NIST 800-53 (which control family?)
- ISO 27001:2022 (which Annex A control?)
- SOC 2 (which trust service criterion?)
- PCI DSS 4.0 (which requirement?)
- NIS2 (which Art. 21 measure?)
- CIS Controls v8 (which control?)
- ASD Essential 8 (which mitigation?)
- ISO 27001:2022 (which control?)
- MITRE ATLAS v2026.09 (which TTP? Is it covered?)

For each: Covered (adequate) / Covered (insufficient) / Missing entirely

### Step 4: Generate new control requirements

Write new control requirements in the format:
```
[CONTROL-ID]: [One-line control name]
Description: [Specific, testable requirement]
Evidence: [What demonstrates compliance]
Framework gap it closes: [Which framework controls are insufficient]
CVE evidence: [Which CVEs demonstrate this gap]
```

### Step 5: Calculate exposure score

Estimate: What percentage of organizations that pass audits of existing controls are still exposed to this vulnerability?

Use: Known patch deployment lag statistics + framework SLA vs. RWEP gap analysis.

### Step 6: Produce lesson entry

Format the output for addition to `data/zeroday-lessons.json`.

---

## Output Format

The skill produces a Zero-Day Learning Loop entry per CVE, capturing attack-vector extraction, control-gap identification, framework coverage assessment, the new control requirement that closes the gap, and an exposure score for the org's environment. The shape below is consumed downstream by `framework-gap-analysis` (which converts the new control requirement into a Framework Lag Declaration), by `defensive-countermeasure-mapping` (which maps the requirement to D3FEND IDs), and by `data/zeroday-lessons.json` (which inherits the lesson entry as a persistent record). Preserve the attack-vector and control-gap fields verbatim — they are the auditable derivation of the new control requirement.

```
## Zero-Day Learning Loop: [CVE-ID / Vulnerability Name]

**Date:** YYYY-MM-DD
**RWEP:** [score]

### Attack Vector
[Extracted attack vector analysis]

### Defense Chain Analysis
| Layer | Required Control | Framework Coverage |
|---|---|---|
| Prevention | [control] | [Covered/Insufficient/Missing] |
| Detection | [control] | [Covered/Insufficient/Missing] |
| Response | [control] | [Covered/Insufficient/Missing] |

### Framework Coverage Matrix
[Per-framework table]

### Gap Classification
[Missing entirely / Insufficient / Compliant-but-exposed]

### New Control Requirements
[Generated requirements in standard format]

### Exposure Scoring
Estimated % of audit-passing orgs still exposed: [X]%
Reason: [RWEP vs. framework SLA gap analysis]

### Lesson Entry (for data/zeroday-lessons.json)
[Ready-to-add JSON entry]
```

---

## Compliance Theater Check

Run this check against any organization claiming a mature vulnerability-management or threat-intelligence program:

> "Pull the org's vulnerability-management runbook for the most recent five CISA-KEV-listed zero-days. For each: was the CVE patched? Almost certainly yes. Now ask the harder question: for each, where is the artifact that says (a) what attack vector this zero-day used, (b) what control would have caught it pre-patch, (c) which framework control was responsible for that detection/prevention, (d) was that framework control adequate, and (e) what new internal control requirement, if any, was created? If the answer is `we patched it, ticket closed` with no artifact, the program is patching CVEs and learning nothing. The next AI-generated variant of the same primitive will land against the same unchanged control surface. That is compliance theater for the threat-intel function — process compliance (A.5.7) with zero learning-loop output."

> "Open `data/zeroday-lessons.json` (or the org's equivalent). Count the entries. Compare to the count of CVEs the org actually responded to in the same period. If the lesson-entry count is < CVE-response count, the loop is partial. Partial is failure: every zero-day-in-scope must produce a lesson entry. The gap between CVEs-patched and lessons-learned is the size of the theater. The org's `Improve` function (NIST CSF 2.0) is not running."

> "Ask: in the last 12 months, has a single internal control requirement been created or modified as a result of a public zero-day the org was NOT directly hit by? If no, the org's threat-intelligence control (ISO A.5.7) is consumption-only — collecting feeds, not changing controls. Threat-intel without control-system change is library subscription, not security capability."

---

## Defensive Countermeasure Mapping

The learning loop's output is a new control requirement. The mapping below converts each of the lesson-class outputs this skill produces into the D3FEND defensive technique that codifies the requirement. A lesson entry that names a new control requirement without citing a D3FEND ID is incomplete — the requirement names the goal but not the implementation technique, which is exactly the framework-lag failure the learning loop is meant to close.

| Lesson class | Offensive TTP class | D3FEND ID | Defensive technique | Defense-in-depth layer |
|---|---|---|---|---|
| Deterministic kernel LPE (Copy Fail class) | T1068 | `D3-KBPI` | Kernel-Based Process Isolation | Kernel — compensating control during AI-compressed weaponization |
| Deterministic kernel LPE | T1068 | `D3-SCA` | System Call Analysis | Endpoint — detect the LPE primitive at syscall layer |
| Cryptographic subsystem compromise (Dirty Frag / Fragnesia) | T1190 | `D3-NI` | Network Isolation (non-IPsec data path) | Network — segmentation independent of the compromised subsystem |
| Cryptographic subsystem compromise | T1068 (post-exploit) | `D3-PA` | Process Analysis | Endpoint — anomalous-uid / capability-set detection |
| Prompt injection RCE (Copilot YOLO-mode class) | AML.T0051, AML.T0054 | `D3-IOPR` | Input/Output Profiling | SDK / application — content-aware prompt+completion inspection |
| Prompt injection RCE (gateway tier) | AML.T0051 | `D3-CSPP` | Client-server Payload Profiling | LLM gateway — when SDK-side instrumentation is not deployable |
| MCP supply chain RCE (Windsurf class) | AML.T0010 | `D3-EAL` | Executable Allowlisting | Managed endpoint — only sanctioned MCP servers execute |
| MCP supply chain RCE | AML.T0010 | `D3-EFA` | Executable File Analysis | Endpoint — pre-execution analysis of MCP-server binaries |
| AI-as-C2 (SesameOp class) | AML.T0096 | `D3-NTA` | Network Traffic Analysis | Network egress — per-identity baseline of model-API destinations |
| AI-generated malware (PROMPTFLUX class) | AML.T0016 | `D3-PA` | Process Analysis | Endpoint — behavioral detection of in-process LLM-query patterns |
| RAG exfiltration | AML.T0043 | `D3-FAPA` | File Access Pattern Analysis | Data tier — RAG-corpus retrieval-pattern baselining |
| Model poisoning | AML.T0020 | `D3-FAPA` | File Access Pattern Analysis | Data tier — training-corpus access-pattern baselining |
| Identity-provider blast-radius (sigstore-class) | T1078 (Valid Accounts) | `D3-CBAN` | Certificate-based Authentication | Identity — short-lived workload certificates limit token-theft blast radius |

**Defense-in-depth posture:** every lesson entry produced by this skill must cite at least one D3FEND technique from the table for the cited offensive TTP class. A lesson that names "we need better prompt-injection defence" without citing `D3-IOPR` or `D3-CSPP` is rhetorically complete but operationally vacant — the next variant lands against the same unchanged control surface because the lesson never named the technique that disrupts it.

**Least-privilege scope:** the D3FEND techniques in this table are technique-level; the per-principal scoping is owned by the downstream skill named in the lesson's `feeds_into` field (e.g. `ai-attack-surface` for AML.T0051 lessons, `kernel-lpe-triage` for T1068 lessons). A lesson entry routes the new control requirement to the downstream skill, which carries the principal-class scoping.

**Zero-trust posture:** a lesson entry closes only when the new control requirement is deployed and verified in production, not when the lesson is recorded. The Output Format's "Exposure Scoring" section must track lesson-deployment latency alongside lesson-creation latency — a lesson recorded but not deployed is the same operational state as no lesson at all.

**AI-pipeline applicability:** lessons targeting AML.T0010 (MCP / model-serving supply chain) must record AI-pipeline degradations explicitly. `D3-EAL` does not apply to serverless inference endpoints — the scoped alternative is `D3-CSPP` at the gateway plus signed-image attestation at the provider. `D3-FAPA` on ephemeral RAG indices degrades to per-query retrieval logging via `D3-IOPR` plus index-build provenance signed at construction. Lessons that omit these degradations propagate the framework-lag they were meant to close.
