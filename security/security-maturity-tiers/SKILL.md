---
name: security-maturity-tiers
version: "1.0.0"
description: Three-tier implementation roadmap — MVP you can ship today, practical best practices usable now, overkill gold standard for defense-in-depth
triggers:
  - security maturity
  - implementation roadmap
  - what should we do first
  - security tiers
  - mvp security
  - where to start
  - security roadmap
  - minimum viable security
  - what's practical
  - security best practices
  - defense in depth
  - how do we get from here to there
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - d3fend-catalog.json
  - rfc-references.json
atlas_refs: []
attack_refs: []
framework_gaps: []
d3fend_refs:
  - D3-CSPP
  - D3-EAL
  - D3-EFA
  - D3-FAPA
  - D3-IOPR
  - D3-ITF
  - D3-KBPI
  - D3-MENCR
  - D3-MFA
  - D3-NI
  - D3-NTA
  - D3-OTF
  - D3-SCA
rfc_refs:
  - RFC-9954
forward_watch:
  - New attack classes that change MVP requirements (especially zero-interaction RCE)
  - Framework updates that change minimum compliance baselines
  - New tooling that makes higher tiers more accessible
  - PQC tooling maturity shifting overkill to practical
last_threat_review: "2026-09-28"
---

# Security Maturity Tiers

Three tiers. Each is complete, not a stepping stone to the next. An organization that ships Tier 1 correctly is more secure than one that half-implements Tier 3.

**The cardinal rule:** A half-implemented Tier 3 is worse than a complete Tier 1. Do not reach for the overkill tier if the foundation isn't solid.

---

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. This skill produces a roadmap shape that applies to *every* security domain the project covers (kernel patching, AI systems, cryptography, MCP, RAG, identity, supply chain, etc.). The three-tier roadmap is domain-agnostic; the domain-specific TTPs and framework gaps live in the downstream skill that owns the domain. Pinning a fixed subset here would falsely imply tier-mapping applies only to that subset.

---

## How to Use This Skill

This skill produces a three-column roadmap for any security domain. Tell it:
- What domain (kernel patching, AI systems, cryptography, MCP security, etc.)
- Your current state
- Your constraint (team size, budget, compliance requirement, timeline)

It outputs Tier 1 (MVP), Tier 2 (Practical), Tier 3 (Overkill) for that domain — specific, actionable, honest about trade-offs.

---

## Tier Framework

| Tier | Name | Principle | Trade-off |
|---|---|---|---|
| 1 | MVP | The smallest set of controls that closes your highest-priority RWEP gaps | Coverage over depth: broad protection of the most critical things |
| 2 | Practical | Production-grade controls that scale, monitor, and adapt | Operational cost to maintain properly |
| 3 | Overkill | Defense-in-depth that assumes Tier 1 and Tier 2 have been bypassed | High cost, high operational complexity — but you're safer than sorry |

---

## Domain: Kernel LPE (Copy Fail / Dirty Frag Class)

### Tier 1 — MVP

**What it is:** The minimum that closes RWEP 90+ exposures today.

**Deploy in order:**

1. **Triage exposed systems** (today, < 2 hours)
   ```bash
   # On each Linux host:
   uname -r
   # Cross-reference against patched versions for your distro
   # RHEL: kernel >= 4.18.0-553.xx = patched
   # Ubuntu 22.04: linux-image-5.15.0-<patch-revision> (check latest USN)
   ```

2. **Deploy live kernel patches on exposed systems** (same day)
   ```bash
   # RHEL: 
   kpatch install [patch-name]
   kpatch list  # verify active
   
   # Ubuntu:
   canonical-livepatch enable
   canonical-livepatch status  # verify applied
   ```

3. **Audit rules for exploitation detection** (same day, takes 5 minutes)
   ```bash
   cat >> /etc/audit/rules.d/lpe-detection.rules << 'EOF'
   -a always,exit -F arch=b64 -S userfaultfd -k lpe_attempt
   -w /proc/self/mem -p w -k lpe_mem_write
   EOF
   augenrules --load
   ```

4. **Schedule reboots** for full kernel update at next maintenance window. Document the date.

**Tier 1 is done when:** Every production host is either live-patched, fully patched, or network-isolated with a reboot date scheduled and documented.

**Cost:** Hours of engineer time. No new tooling required.

**What Tier 1 misses:** Automated detection pipelines, fleet-wide patch visibility, centralized alerting. You're protected but flying manual.

---

### Tier 2 — Practical

**What it is:** Sustainable, scalable patch and detection operations.

1. **Fleet-wide vulnerability scanning** (automated, continuous)
   - Wazuh, Tenable, Qualys, or equivalent
   - Daily scans cross-referenced against NVD
   - Alert on: any KEV-listed CVE on a publicly exposed asset unremediated after 48h. The US federal ceiling is now 3 days plus forensic triage for the KEV + publicly-exposed + automatable + total-control combination — CISA BOD 26-04 replaced the uniform KEV due dates of BOD 22-01 with risk-tiered ones.

2. **Live patching fleet management**
   - Canonical Livepatch / Red Hat Insights (manages live patch deployment across fleet)
   - Patch status dashboard: which hosts are live-patched, which need reboots, which are pending
   - SLA tracking: time from CISA KEV listing to live-patch verified

3. **SIEM integration for LPE detection**
   - auditd + SIEM (Splunk, Elastic, Wazuh SIEM)
   - Alert rule: `lpe_attempt` or `lpe_mem_write` audit keys trigger P1 alert
   - Automated isolation workflow for confirmed exploitation

4. **Maintenance window calendar** (automated)
   - Hosts grouped by reboot-tolerance
   - Kernel reboot SLA tracked per host group
   - Automated reminders when reboot is overdue

**Tier 2 is done when:** You have visibility into patch status for every host, automated alerting for CISA KEV exposures, and a measured SLA for live-patch deployment.

---

### Tier 3 — Overkill

**What it is:** Assumes an LPE exploit will run. Limits what it can do.

1. **Kernel hardening** (reduce attack surface before exploitation)
   ```bash
   # /etc/sysctl.d/99-kernel-hardening.conf
   kernel.unprivileged_userns_clone = 0
   kernel.kptr_restrict = 2
   kernel.perf_event_paranoid = 3
   vm.unprivileged_userfaultfd = 0
   kernel.yama.ptrace_scope = 2
   ```

2. **seccomp profiles** for all containerized workloads (limits syscalls available to container processes — raises bar for exploitation even on unpatched kernel)

3. **eBPF-based runtime security** (Tetragon, Falco, Cilium)
   - Monitor all privilege escalation events in real time
   - Automatic process kill on confirmed LPE pattern detection
   - Kernel subsystem integrity monitoring

4. **Immutable infrastructure** — ephemeral hosts that are replaced, not patched
   - On-demand provisioning from known-good base images
   - Kernel version is part of the image specification
   - No persistent hosts = no accumulated patch debt

5. **Blast radius isolation**
   - Container runtime: no `--privileged`, no host PID namespace, no host network
   - Workload network micro-segmentation: even a rooted container can't reach production DBs
   - Separate kernel per workload via VM/MicroVM (Firecracker) for maximum isolation

**Tier 3 is done when:** An exploited LPE gets root on one process in one container on one host, and can't reach anything else.

---

## Domain: AI Attack Surface

### Tier 1 — MVP

1. **Audit all MCP servers** (today, < 1 hour)
   ```bash
   # Check each AI coding assistant's config:
   cat ~/.claude/settings.json | python -m json.tool | grep -A5 mcpServers
   cat ~/.cursor/mcp.json
   cat ~/.windsurf/mcp.json
   cat ~/.gemini/settings.json
   # VS Code: check settings.json for mcp entries
   ```
   Remove any server you didn't explicitly install and verify.

2. **Pin all MCP server versions** (no auto-update)
   - Change `@modelcontextprotocol/server-filesystem` to `@modelcontextprotocol/server-filesystem@1.2.3`

3. **Add explicit tool allowlists** where the client supports it
   ```json
   { "allowed_tools": ["read_file", "list_directory"] }
   ```

4. **Turn on full prompt+response logging** for AI coding assistants where possible.

5. **Treat the AI assistant's output like untrusted input** — don't run AI-suggested shell commands without reading them first.

6. **Inventory self-hosted LLM application infrastructure** (today, under an hour) — LLM gateways and proxies, and flow builders. For each instance record: reachable from the internet? authentication enforced on every endpoint? version current? Any instance reachable from the internet without authentication is remediated today — either put it behind authenticated ingress or take it off the public network. This product class has produced repeated KEV-listed pre-authentication RCE against default deployments, so an unauthenticated internet-reachable instance is an immediate MVP failure, not a Tier 2 refinement.

**Tier 1 is done when:** You know what MCP servers are installed, versions are pinned, no self-hosted LLM gateway or flow builder is reachable from the internet without authentication, and you're reading AI-suggested commands before executing.

---

### Tier 2 — Practical

1. **Organizational MCP approved registry** — list of approved servers with version + hash
2. **MCP server provenance verification** (npm provenance attestation check on install)
3. **AI API traffic logging** — all AI API calls logged with process identity
4. **Behavioral baseline** — alert on AI API calls from unexpected processes
5. **Prompt injection classifier** in front of any LLM that processes external content
6. **Phishing simulation updated** — use AI-generated content in phishing tests, retire template-based tests

---

### Tier 3 — Overkill

1. **Sandboxed MCP servers** — each MCP server runs in a network-isolated process with no filesystem access beyond its declared scope. Enforced at OS level (seccomp + network namespace), not just by config.
2. **AI agent action audit trail** — every tool call logged with: who initiated the AI session, what prompt triggered the tool call, what the tool did, what was returned. Immutable log.
3. **Per-invocation authorization** — each AI agent session is issued a scoped capability token. The token expires. The AI cannot take actions beyond the token's scope regardless of what instructions it receives.
4. **Adversarial testing continuous** — automated red teaming of AI surfaces in CI: does the prompt injection classifier catch new injection patterns? Does the MCP allowlist block new tool exposure?
5. **AI traffic TLS inspection** — full prompt+response content captured and monitored for AI-as-C2 patterns (SesameOp indicators) and AI-generated malware queries (PROMPTFLUX indicators)

---

## Domain: Cryptography / PQC

### Tier 1 — MVP

1. **Inventory all asymmetric cryptography** in production systems (TLS certs, JWT signing, code signing, API auth)
2. **Upgrade OpenSSL to 3.5+** in all new deployments (not legacy — just new)
3. **Enable TLS 1.3 minimum** everywhere (already quantum-safe symmetric if using AES-256; the KEM is what needs upgrading)
4. **Identify HNDL-exposed data** — what data captured today, if decrypted in 10 years, causes harm?
5. **Pin a migration start date** — document it. "We will begin PQC migration for HNDL-exposed systems by [date]."

**Tier 1 is done when:** You know what you have, you know what's exposed, and you have a start date for migration.

---

### Tier 2 — Practical

1. **Enable X25519+ML-KEM-768 hybrid in TLS** for all systems handling HNDL-exposed data. Hybrid key exchange is specified in RFC 9954, and X25519MLKEM768 is offered by default from OpenSSL 3.5 onward — on current libraries this is a version upgrade plus a config assertion, not a migration project.
   ```
   # OpenSSL 3.5+ server config
   Curves = X25519MLKEM768:X25519:P-384
   ```
2. **ML-DSA-65 for new code signing** (keep ECDSA as hybrid verification fallback)
3. **SLH-DSA-SHAKE-256f for audit chain** checkpoints (tamper-evident logs)
4. **Certificate refresh plan** — replace P-256 leaf certs with hybrid certs on next renewal cycle
5. **Document PQC migration in vendor questionnaires** — note OpenSSL version, PQC TLS support, migration plan

---

### Tier 3 — Overkill

1. **Full PQC-only key exchange** for new systems (no classical fallback) — accept the small compatibility risk for maximum quantum safety
2. **ML-KEM-1024 + P-384 hybrid** for all keys with > 20-year sensitivity lifetime
3. **HSM firmware update** to PQC-capable firmware for all key material
4. **Certificate Transparency + signed audit logs** with SLH-DSA checkpoints — tamper-evident, quantum-safe, offline-verifiable
5. **Crypto agility layer** — envelope headers on all encrypted blobs (like blamejs's 4-byte algorithm header) so future algorithm migration doesn't require re-encryption
6. **HNDL monitoring** — detect and alert on unusual traffic patterns that suggest bulk traffic capture by adversaries

---

## Domain: GRC / Compliance

### Tier 1 — MVP

1. **Map your compliance framework(s)** — which frameworks apply?
2. **Run the compliance theater check** (compliance-theater skill) — identify which controls are theater
3. **Document the theater findings** with the specific evidence gaps
4. **Generate policy exceptions** for architectural gaps (policy-exception-gen skill) — document what you can't do and why, with compensating controls
5. **Update one control** — pick the highest-RWEP theater finding and fix it

**Tier 1 is done when:** You know which of your controls are theater, you've documented the gaps, and you've started closing the highest-priority one.

---

### Tier 2 — Practical

1. **Framework gap analysis** (framework-gap-analysis skill) for all in-scope frameworks
2. **Compliance theater score tracked quarterly** — is it going up or down?
3. **Global jurisdiction mapping** (global-grc skill) if operating in multiple jurisdictions
4. **Policy exception catalog** — all architectural exceptions documented, reviewed annually, compensating controls verified
5. **Threat model currency score tracked quarterly** — target > 80%

---

### Tier 3 — Overkill

1. **Continuous compliance monitoring** — controls are machine-verified in real time, not point-in-time audited
2. **Automated theater detection** — weekly automated check: has any control degraded from Tier 2 practice to theater?
3. **Framework lag tracking** — formal process for monitoring framework updates and assessing whether gaps have been closed
4. **Forward control coverage** — for every documented universal gap, a proposed internal control that exceeds current framework requirements. Documented, reviewed by risk committee, formally adopted or explicitly risk-accepted.
5. **Zero-day rapid assessment** — within 24h of a major CVE: RWEP score calculated, theater impact assessed, framework gap analysis run, executive briefing ready

---

## Analysis Procedure

When a user invokes this skill, ask:

### Step 1: Identify domain and current state

What area? (kernel patching, AI, crypto, GRC, etc.)

What do they have today? (nothing / ad-hoc / Tier 1 equivalent / Tier 2 equivalent)

### Step 2: Identify constraints

- **Time:** "we need something this week" → Tier 1 only
- **Team size:** "one security engineer" → Tier 1 + prioritized Tier 2
- **Compliance requirement:** specific frameworks required → include compliance notes per tier
- **Risk appetite:** "we handle PHI" → push toward Tier 2/3 for relevant domains
- **Budget:** explicit constraints → note what each tier costs in tool/time

### Step 3: Produce tiered roadmap

For each applicable domain:
- What does Tier 1 look like for this specific environment? (not generic — specific commands, versions, timelines)
- What does Tier 2 add? (what operational capability does it require?)
- What does Tier 3 add? (what does it assume about attacker persistence and capability?)

### Step 4: Sequence recommendation

Sequence matters. Recommended default:

```
Week 1:   Tier 1 — Kernel (RWEP 90+ exposure is immediate)
Week 1:   Tier 1 — MCP/AI (zero-interaction RCE exposure)
Month 1:  Tier 1 — Crypto inventory + PQC migration plan
Month 1:  Tier 1 — GRC theater mapping
Quarter 1: Tier 2 — Kernel (fleet management, SLA tracking)
Quarter 1: Tier 2 — AI (organizational registry, behavioral baseline)
Quarter 2: Tier 2 — Crypto (hybrid TLS, ML-DSA for signing)
Quarter 2: Tier 2 — GRC (gap analysis, exception catalog)
Year 1+:  Tier 3 — by domain, starting with highest-sensitivity data
```

---

## Output Format

The skill produces a Security Maturity Roadmap that scores each in-scope domain against the published tier definitions and surfaces the next-tier upgrade path with budget bands and dependency ordering. The shape below is consumed downstream by `policy-exception-gen` (for domains where the operator chooses a lower tier than the threat model requires), by `compliance-theater` (which compares the claimed tier against deployed controls), and by `global-grc` (for cross-jurisdictional tier obligations). Preserve the per-domain tier rows verbatim — they are the auditable baseline for the upgrade plan.

```
## Security Maturity Roadmap

**Date:** YYYY-MM-DD
**Domains in scope:** [list]
**Current state:** [assessment]
**Constraint:** [time / team / compliance / budget]

### Priority Sequence
[Week 1 / Month 1 / Quarter 1 / Year 1 items]

### Domain: [name]

#### Tier 1 — MVP (Ship this week)
[Specific commands, configurations, verification steps]
**Done when:** [concrete completion criteria]
**Cost:** [hours, no new tools needed / minimal tooling]

#### Tier 2 — Practical (Quarter 1)
[Scalable, monitored, sustainable]
**Adds:** [what Tier 1 misses that Tier 2 provides]
**Cost:** [operational overhead to sustain]

#### Tier 3 — Overkill (Year 1+)
[Defense-in-depth, assumes compromise at lower tiers]
**Adds:** [blast radius reduction, detection at depth]
**Cost:** [significant operational complexity — only if the threat model warrants it]

### What to Skip (and Why)
[If any Tier 3 items are inappropriate for this environment: say so explicitly]
```

---

## Compliance Theater Check

Apply this check to every maturity-tier engagement before recommending a roadmap:

> "Your security program currently sits at Tier <N> by self-assessment for domain <D>. The compliance framework you cite (e.g. NIST CSF 2.0 / ISO 27001:2022 / NIS2 Art. 21 / UK-CAF / AU Essential 8) classifies your posture as <attested-tier>. If the threats now in scope for this domain (specific CVE / TTP from `data/cve-catalog.json` and `data/atlas-ttps.json`) include a class where the framework control is structurally insufficient (the framework-lag class — framework controls trail current threats), then your attested tier and your operational tier diverge by exactly that gap. Which of the controls you would cite for your attested tier would survive a primary-source IoC test against the highest-RWEP CVE in scope?"

**Theater fingerprints for tier conflation:**

- The org has Tier 3 controls in one domain (e.g. SIEM with hundreds of alerts) but Tier 1 gaps in an adjacent domain (e.g. no kernel-LPE patch SLA on the SIEM host). The Tier 3 alert never fires because the underlying integrity is missing.
- "Mature" is asserted on the basis of tool ownership, not behavior — HSMs purchased, never operationally rotated; ZTA architecture documented, default-allow policies in force; PQC algorithms in code, no key-rotation playbook.
- The maturity model used is the org's own framework-attestation tier, not the lived operational tier — the audit report says Tier 3, the on-call says "what's that runbook again."
- Tier-3 controls audited annually, Tier-1 controls (patching, MFA on privileged identities, secrets in git) never re-audited because they "passed once."
- The roadmap promotes the org from Tier 1 to Tier 3 in a single budget cycle, skipping the Tier 2 operational work that converts point-in-time controls into continuous ones.

**Real requirement:** maturity assessed per domain, not org-wide; the assessed tier matches operational behavior (not the audit attestation); promotion happens domain-by-domain with explicit Tier-2 instrumentation between Tier-1 controls and Tier-3 sophistication; the same CVE-anchored primary-source IoC test applies at every tier — if a Tier-3 control cannot defend against the published PoC of the highest-RWEP CVE in scope, the tier classification is theater.

---

## The Anti-Pattern: Tier 3 Security Theater

Tier 3 controls without Tier 1 and Tier 2 in place is its own form of theater.

Common examples:
- SIEMs that alert on everything and are tuned by no one
- HSMs for key storage with weak key generation practices
- ZTA architecture with default-allow policies
- PQC cryptography with no key rotation

**Before reaching for Tier 3:** verify Tier 1 is complete and Tier 2 is operational. The most sophisticated defense is useless if the basic controls have gaps.

This is the same principle as blamejs's "no-MVP" rule applied to security: better to ship a complete Tier 1 than a partial Tier 3.

---

## Threat Context

The 2026 threat baseline forces an MVP that would have looked like a Practical tier in 2022. The cardinal observed change: attacker capability now compresses the time from disclosure to reliable exploitation to hours for an entire class of vulnerabilities, and AI-mediated attack surfaces (prompt injection, MCP supply chain, AI-API C2) sit outside the perimeter and identity controls every framework relies on. The implications by tier:

- **MVP for any org touching AI APIs or AI coding agents** must include: SDK-level prompt and response logging that captures full request/response bodies (without it, the SC-7 boundary gap means AI-mediated C2 like SesameOp / AML.T0096 is invisible to the SOC); Ed25519-signed deployable artifacts (the closest practical analogue to the integrity verification that EU CRA Annex I compels for the EU market from 2027-12-11); an actively-exploited-vulnerability reporting path that can meet EU CRA Art. 14 from 2026-09-11 — 24h early warning to the coordinating CSIRT and ENISA, 72h vulnerability notification — for any product with digital elements placed on the EU market; and KEV-class CVE monitoring with RWEP-anchored SLAs (see `lib/scoring.js`), not CVSS-anchored ones — CVE-2026-31431 is CVSS 7.8 (High, not Critical) but RWEP 90 because KEV+deterministic+AI-discovered+broad blast radius dominate the actual risk.
- **Practical** assumes MVP is in place and adds the operational instrumentation that converts point-in-time controls into continuously verified ones: fleet-wide patch visibility for KEV-class with measured live-patch SLA, organisational MCP allowlist with provenance attestation, AI-API behavioral baselines per service identity, ephemeral-aware asset inventory.
- **Overkill** assumes Practical can still be bypassed by an AI-accelerated adversary: per-invocation capability tokens for AI agents, sandboxed MCP execution, eBPF runtime detection (Tetragon/Falco), continuous adversarial testing of AI surfaces in CI, immutable infrastructure that closes the patch-debt window entirely.

The MVP tier is non-negotiable for any org with internet exposure plus AI usage. Every higher tier is a deliberate increase in defense depth, not a checkbox upgrade.

---

## Framework Lag Declaration

Each tier diverges from at least one widely-cited framework control because the framework control is operationally inadequate for the threats the tier addresses. The divergences are deliberate and documented per tier.

| Tier | Framework / Control | Framework prescription | Tier prescription | Why the framework is insufficient |
|---|---|---|---|---|
| MVP | NIST 800-53 SI-2 (Flaw remediation) | "Within organisationally defined time periods" — interpreted across industry as 30 days for critical | Live kernel patch within 4 hours for KEV-listed deterministic LPE (Copy Fail class) | 30 days is an exploitation window, not a security window, for CVE-2026-31431 (RWEP 90, deterministic 732-byte PoC) |
| MVP | ISO 27001:2022 A.8.8 (Technical vulnerability management) | "Appropriate timescales" — undefined | Same as above — RWEP-indexed, not calendar-indexed | "Appropriate" leaves the operationally critical SLA undefined precisely where definition matters |
| MVP | PCI DSS 4.0 6.3.3 | Critical patches within 1 month | Same divergence — RWEP >= 70 must be live-patched within hours | 1 month is multiple AI-accelerated exploit cycles |
| MVP | EU NIS2 Art. 21(2)(f) (vulnerability handling) | "Policies/procedures to assess vulnerability handling measures" | Concrete RWEP-anchored SLA published as policy | "Procedures to assess" is meta-control, not a control |
| MVP | UK Cyber Essentials | High-risk patches within 14 days | Same divergence — 14 days insufficient for KEV-class deterministic LPE | Better than NIST but still loses to AI-accelerated weaponization |
| MVP | AU ASD ISM-1877 and ISM-1696 / Essential 8 | 48h patch when a working exploit exists (internet-facing systems at every maturity level, workstations at ML3) | Aligned at the framework level; tier adds live-patch capability requirement | Closest national framework alignment globally; still no live-patch mandate |
| MVP | CISA BOD 26-04 (Prioritizing Security Updates Based on Risk) | Urgency set by four decision points — asset exposure, KEV status, exploit automation, technical impact — 3 days at the top band, "fix on system upgrade" at the bottom | RWEP-indexed SLA with the live patch verified within hours for KEV-listed deterministic LPE | Closest framework alignment to risk-indexed remediation to date, but the top band is still 3 days, there is no live-patch requirement, and it binds only US federal civilian agencies |
| Practical | ISO 27001:2022 A.5.9 (Inventory of information and other associated assets) | Point-in-time CMDB / asset register | Ephemeral-aware inventory snapshots (continuous, container/serverless-native) | Point-in-time CMDB misses ephemeral workloads; Practical Tier requires an inventory that reflects actual workload existence within minutes, not days |
| Practical | NIST 800-53 CM-8 (System component inventory) | Documented inventory, updated periodically | Same divergence — continuous, attestation-based inventory | CM-8 cadence is multi-day at best; AI-speed reconnaissance (36,000 probes/sec) requires continuous attack-surface awareness |
| Practical | EU DORA Art. 8 (ICT risk identification) | "On an ongoing basis" | Same — continuous, with explicit AI/MCP categories | "Ongoing" undefined; the tier defines it as < 1h staleness for production assets |
| Practical | NIST 800-53 SC-7 (Boundary Protection) | Perimeter and internal boundary protection | Add AI-API egress logging and behavioral baselining | SC-7 is perimeter-centric; AI-API egress is internal-trusted traffic that hides AML.T0096 (LLM C2) |
| Overkill | NIST 800-53 AC-6 (Least privilege) | Privilege minimisation for principals | Per-invocation capability tokens for AI agents | AC-6 controls principal permissions; AI agents need per-call scoped capabilities the framework does not contemplate |
| Overkill | ISO 27001:2022 A.8.31 (Separation of development, test, production) | Environment separation | Add: sandboxed MCP servers with seccomp+netns enforcement | A.8.31 does not contemplate developer-installed AI tool plugins as a privilege-bearing execution surface |
| Overkill | EU AI Act Art. 15 (Cybersecurity for high-risk AI) | "Appropriate level" of cybersecurity; applies to Annex III high-risk systems from 2027-12-02 and Annex I embedded systems from 2028-08-02 | Continuous adversarial testing of AI surfaces in CI | "Appropriate" is interpretive, and the obligation does not bind for another 16–24 months while the attack surface is live today; the tier operationalises it now |

The divergences above are surfaced against US, EU, UK, AU and ISO 27001:2022 — every tier's framework lag declaration is global by construction.

---

## TTP Mapping

Per-tier TTP coverage is cumulative: Practical includes MVP's coverage plus additions; Overkill includes both plus additions. Source-of-truth: `data/atlas-ttps.json` (MITRE ATLAS v2026.09) and ATT&CK references in `data/cve-catalog.json`.

| Tier | Must cover | TTP | Source | Tier-specific control element |
|---|---|---|---|---|
| MVP | Privilege escalation | T1068 (ATT&CK) | cve-catalog.json: CVE-2026-31431 | Live-patch + auditd userfaultfd / proc/self/mem rules |
| MVP | LLM Prompt Injection | AML.T0051 | atlas-ttps.json | Don't execute AI-suggested commands without read; turn on prompt+response logging |
| MVP | ML Supply Chain Compromise (MCP) | AML.T0010 | atlas-ttps.json | MCP server inventory + version pinning + tool allowlist |
| MVP | LLM Jailbreak | AML.T0054 | atlas-ttps.json | Same control as AML.T0051; the two are operationally adjacent — adversarial-instruction injection bypasses guardrails |
| Practical | Exploit Public-Facing Application | T1190 (ATT&CK) | cve-catalog.json (CVE-2025-53773 attack_refs) | External attack-surface management + AI-mediated T1190 coverage |
| Practical | Discover AI Model Ontology | AML.T0013 | atlas-ttps.json | Inference-API rate + shape monitoring; reconstruct adversary's model-family map |
| Practical | Poison Training Data | AML.T0020 | atlas-ttps.json | Training-pipeline integrity verification for any in-house ML used in decisions |
| Practical | Obtain / Develop Capabilities (AI-assisted weaponization) | AML.T0016, AML.T0017 | atlas-ttps.json | RWEP-anchored monitoring; treat KEV+PoC as immediate live-patch trigger; phishing detection updated for AI-generated content; behavioural signals primary |
| Overkill | AI Service API (C2) | AML.T0096 | atlas-ttps.json | AI-traffic content inspection + SesameOp-pattern detection with behavioural baseline |
| Overkill | Backdoor ML Model | AML.T0018 | atlas-ttps.json | Model integrity verification (behavioural regression tests, model signing) |
| Overkill | Craft Adversarial Data (RAG/general) | AML.T0043 | atlas-ttps.json | Vector-store access controls + retrieval-anomaly monitoring |

The full canonical truth set is `data/atlas-ttps.json` (all `AML.T*` keys excluding `_meta`) union the `attack_refs` field of every entry in `data/cve-catalog.json`. The tiered selection above is the minimum coverage; orgs in regulated verticals (finance, health, critical infrastructure) typically push Overkill items into Practical based on threat-model output.

---

## Defensive Countermeasure Mapping

D3FEND references from `data/d3fend-catalog.json`. This skill prescribes a roadmap shape rather than domain controls, so the mapping below is tiered the way the roadmap is: each row pairs the TTP a tier must cover with the D3FEND technique that closes it and the downstream skill that owns the implementation detail. Coverage is cumulative — Practical inherits MVP's techniques, Overkill inherits both.

| Tier | Offensive TTP | D3FEND ID | Defensive technique | Owning downstream skill |
|---|---|---|---|---|
| MVP | T1068 (Exploitation for Privilege Escalation) | `D3-KBPI` + `D3-SCA` | Kernel-Based Process Isolation + System Call Analysis | `kernel-lpe-triage` |
| MVP | AML.T0051 / AML.T0054 (Prompt Injection / Jailbreak) | `D3-IOPR` | Input/Output Profiling | `ai-attack-surface` |
| MVP | AML.T0010 (ML Supply Chain Compromise — MCP) | `D3-EAL` | Executable Allowlisting (tool allowlist + version pinning) | `mcp-agent-trust` |
| MVP | T1190 (Exploit Public-Facing Application — self-hosted LLM infrastructure) | `D3-NI` + `D3-ITF` | Network Isolation + Inbound Traffic Filtering | `webapp-security` + `ai-attack-surface` |
| Practical | T1190 (Exploit Public-Facing Application) | `D3-ITF` + `D3-NI` | Inbound Traffic Filtering + Network Isolation | `attack-surface-pentest` |
| Practical | AML.T0013 (Discover AI Model Ontology) | `D3-CSPP` | Client-server Payload Profiling (inference-API rate and shape monitoring) | `ai-attack-surface` |
| Practical | AML.T0020 (Training Data Poisoning) | `D3-FAPA` | File Access Pattern Analysis (training-pipeline integrity) | `mlops-security` |
| Practical | AML.T0016 (Obtain Capabilities, AI-generated phishing and payloads) | `D3-CSPP` + `D3-MFA` | Client-server Payload Profiling + Multi-factor Authentication (passkey class) | `email-security-anti-phishing` + `identity-assurance` |
| Practical | Harvest-now-decrypt-later (T1040, T1557) | `D3-MENCR` | Message Encryption (PQC-hybrid KEM per RFC 9954) | `pqc-first` |
| Overkill | AML.T0096 (AI Service API, C2) | `D3-NTA` + `D3-OTF` | Network Traffic Analysis + Outbound Traffic Filtering | `ai-c2-detection` |
| Overkill | AML.T0018 (Manipulate AI Model) | `D3-EFA` + `D3-FAPA` | Executable File Analysis (model signing) + File Access Pattern Analysis | `mlops-security` |
| Overkill | AML.T0043 (Craft Adversarial Data — RAG) | `D3-IOPR` + `D3-FAPA` | Input/Output Profiling + File Access Pattern Analysis (vector-store access control) | `rag-pipeline-security` |

**Defense-in-depth posture:** the tiers are the defence-in-depth axis. A tier is complete only when every technique at that tier *and every tier below it* is deployed — this is the cardinal rule of the skill expressed in D3FEND terms. An org running `D3-NTA` for AI-C2 detection while `D3-KBPI` is absent has an Overkill technique guarding a host that a deterministic LPE owns outright, which is precisely the half-implemented-Tier-3 anti-pattern.

**Least-privilege scope:** each downstream skill is authoritative for principal-class scoping. The tier model adds one constraint of its own: a technique introduced at MVP must be deployable without a privileged agent identity, or it does not belong at MVP. `D3-EAL` as a client-side tool allowlist qualifies; a fleet-wide allowlisting service does not, and belongs at Practical.

**Zero-trust posture:** tier placement is set by the attack surface, not by network position. The MVP `D3-NI` + `D3-ITF` row exists because a self-hosted LLM gateway on an "internal" network is reachable by anything that reaches that network, and this product class has produced repeated pre-authentication RCE against default deployments — an internal-network assumption is not a control.

**AI-pipeline applicability:** every `AML.*` row applies to AI workloads specifically, and none of them has a binding regulatory mandate in any jurisdiction (see `global-grc`). Their tier placement is therefore threat-driven rather than compliance-driven, which is why an org that builds its roadmap from framework requirements alone lands at Tier 1 with the entire AI attack surface uncovered.

---

## Exploit Availability Matrix

Tiered to the current `data/cve-catalog.json`, using RWEP (`lib/scoring.js`) as the priority metric, not CVSS:

| Tier | Coverage requirement | Example CVEs in scope | Available exploits | Required protective state |
|---|---|---|---|---|
| MVP | RWEP >= 70 | CVE-2026-31431 (Copy Fail, RWEP 90, CVSS 7.8) | Public 732-byte deterministic PoC; KEV-listed 2026-05-01 (federal due 2026-05-15); AI-discovered; live-patch available (kpatch / canonical-livepatch / kGraft) | Live-patched within hours of KEV listing OR fully patched + rebooted OR network-isolated with documented reboot date |
| Practical | RWEP >= 30 | CVE-2026-31431 (90), CVE-2026-43284 (Dirty Frag ESP/IPsec, 53, CVSS 8.8), CVE-2026-43500 (Dirty Frag RxRPC, 47, CVSS 7.6), CVE-2026-30615 (Windsurf MCP local-vector RCE, 35, CVSS 8.0), CVE-2025-53773 (Copilot YOLO-mode RCE, 30, CVSS 7.8) | Copy Fail as above; the Dirty Frag pair has a public chain PoC and no broad live patch (kpatch RHEL-only); CVE-2026-30615 + CVE-2025-53773 both AV:L local-vector, demonstrated PoC, vendor-patchable; AI-coding-assistant scope | All MVP coverage plus: prompt-injection classifier in front of any LLM processing external content; phishing simulation using AI-generated content; org-wide AI-coding-assistant version management; MCP server allowlisting with signed manifests |
| Overkill | All catalog entries regardless of RWEP | CVE-2026-31431 (90), CVE-2026-43284 (Dirty Frag ESP/IPsec, 53, CVSS 8.8), CVE-2026-30615 (Windsurf MCP local-vector RCE, 35, CVSS 8.0), CVE-2026-43500 (Dirty Frag RxRPC, 47, CVSS 7.6), CVE-2025-53773 (Copilot YOLO-mode RCE, 30, CVSS 7.8) | Public PoC for all; Dirty Frag pair has no live patch (kpatch RHEL-only); Windsurf is local-vector supply-chain class; chained Dirty Frag requires kernel-version fingerprinting | All Practical coverage plus: kernel hardening (unprivileged_userns_clone=0, unprivileged_userfaultfd=0, kptr_restrict=2); seccomp profiles on all containers; eBPF runtime detection; immutable infrastructure for the workloads that tolerate it; sandboxed MCP execution; per-invocation capability tokens for AI agents |

Refresh trigger: re-run `node lib/scoring.js` and rebuild this matrix whenever `data/cve-catalog.json` is updated. The zero-day learning loop also feeds back into the tier mapping when a new CVE is added.

Note on CVSS divergence: every CVE in this matrix has a CVSS between 7.6 and 8.8, so CVSS alone would prioritize the highest-band CVE without distinguishing the AI-discovered KEV-listed deterministic LPE (Copy Fail) from the local-vector MCP supply-chain class (Windsurf). RWEP correctly ranks Copy Fail (90) above Windsurf (35) because KEV listing, deterministic exploitability, AI discovery, and broad blast radius dominate. The MVP tier protects against the right thing first.

---
