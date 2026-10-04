---
name: mcp-agent-trust
version: "1.0.0"
description: Enumerate MCP trust boundary failures — tool allowlisting, signed manifests, bearer auth, zero-interaction RCE
triggers:
  - mcp security
  - model context protocol
  - agent trust
  - tool trust
  - mcp rce
  - cve-2026-30615
  - cursor security
  - windsurf security
  - claude code security
  - ai agent security
data_deps:
  - atlas-ttps.json
  - cve-catalog.json
  - d3fend-catalog.json
  - exploit-availability.json
  - rfc-references.json
atlas_refs:
  - AML.T0010
  - AML.T0053
  - AML.T0086
  - AML.T0096
attack_refs:
  - T1195.001
  - T1059
  - T1190
framework_gaps:
  - ALL-MCP-TOOL-TRUST
  - ISO-27001-2022-A.8.30
  - NIST-800-53-CM-7
  - NIST-800-53-SA-12
  - OWASP-LLM-Top-10-2025-LLM06
  - SOC2-CC9-vendor-management
  - SWIFT-CSCF-v2026-1.1
  - EU-AI-Act-Art-15
  - UK-CAF-A1
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-6749
  - RFC-7519
  - RFC-8446
  - RFC-8725
  - RFC-9114
  - RFC-9421
  - RFC-9700
cwe_refs:
  - CWE-22
  - CWE-345
  - CWE-352
  - CWE-434
  - CWE-494
  - CWE-77
  - CWE-918
  - CWE-94
d3fend_refs:
  - D3-CAA
  - D3-CBAN
  - D3-CSPP
  - D3-EAL
  - D3-EHB
  - D3-MFA
forward_watch:
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM 3-bug SSRF + Code Injection chain by k3vg3n; MCP-adjacent LLM proxy surface; track upstream patch and MCP trust advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LiteLLM full SSRF + Code Injection by Out Of Bounds (Byung Young Yi); duplicate-class with the k3vg3n entry; track unified patch advisory
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — LM Studio 5-bug exploit chain by STARLabs SG; impacts local MCP/agent runtime trust; track patch and integration advisories
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — Claude Code MCP collision-scored entry by Viettel Cyber Security; CVE in flight; track MCP trust and tool-collision advisory
last_threat_review: "2026-09-18"
---

# MCP Agent Trust Assessment

## Threat Context (mid-2026)

The Model Context Protocol (MCP) is an open protocol for connecting AI assistants to external tools and data sources. It is now the standard integration layer for AI coding assistants: Cursor, VS Code + GitHub Copilot, Windsurf, Claude Code, and Gemini CLI all support MCP servers. Background reality: 41% of 2025 zero-days were AI-discovered (GTIG 2025); Fragnesia (CVE-2026-46300, 2026-05-13) is the canonical AI-driven autonomous-discovery anchor — Zellic's agentic auditor surfaced an 18-year-old kernel primitive that load-bearing MCP-server hosts depend on. The first documented AI-built in-the-wild zero-day landed 2026-05-11 (GTIG AI 2FA-bypass). MCP trust posture should align to CTID Secure AI v2 (2026-05-06, replaces v1).

MCP creates an architectural trust problem that no existing security framework addresses.

### The Trust Boundary Failure

An MCP server is a process that exposes tools (functions the AI can call) and resources (data the AI can read). When an AI assistant decides to call an MCP tool, it does so based on:
1. The tool's description (provided by the MCP server)
2. The prompt context (which may contain adversarial instructions)
3. The model's own judgment

There is no mandatory:
- Code signing requirement for MCP server packages
- Tool allowlist (the client allows all tools by default)
- Authentication requirement between the AI client and the MCP server
- Output sanitization before returning tool results to the model
- Permission model for what the MCP server process can access on the host

This means: a malicious or compromised MCP server can execute arbitrary code by simply returning adversarial instructions in tool responses, which the AI model then follows.

### CVE-2026-30615 — Windsurf MCP Local-Vector RCE

**CVSS:** 8.0 (AV:L, NVD-authoritative; corrected from initial 9.8/AV:N) | **RWEP:** 35/100

A vulnerability in the Windsurf MCP client that allows a malicious MCP server to drive code execution in the user's context by returning attacker-controlled HTML the client processes. The attack vector is local — the attacker must first land a malicious MCP server in the user's installed set (typosquatting, supply-chain compromise, or social engineering). Once installed, the AI assistant invokes the tool and follows the adversarial response without an additional user-action gate.

**Affected:** Windsurf (all versions before patch), and by architectural similarity: Cursor, VS Code MCP extension, Claude Code, Gemini CLI (each has its own vulnerability profile; CVE-2026-30615 is specific to Windsurf's implementation but the architectural attack surface is identical across clients).

**Scale:** 150M+ combined downloads across affected MCP-capable AI coding assistants.

**Attack path:**
1. Attacker publishes malicious MCP server to npm or creates a typosquatting package
2. Developer installs the package (or a legitimate package is compromised via supply chain)
3. AI assistant starts, connects to MCP server, receives tool list
4. At any future point: AI assistant calls a tool on the malicious server (possibly triggered by a prompt injection in a code comment, PR description, or documentation)
5. MCP server returns a response containing adversarial HTML / instructions the Windsurf client renders or relays back to the agent loop
6. AI assistant follows the instructions — executes code, exfiltrates files, persists backdoor

The attack vector is local (AV:L): no network-side exploitation; the attacker's content must reach the client through the installed MCP server.

### CVE-2026-39884 — mcp-server-kubernetes Argument Injection

**CVSS:** 8.3 (AV:N/AC:L/PR:L/UI:N) | Patched in mcp-server-kubernetes 3.5.0+

A second-order example of the MCP trust failure pattern. Flux159's mcp-server-kubernetes (a popular MCP server granting AI assistants `kubectl` control) built kubectl command lines by `.split(' ')`-ing a string instead of using an argv array. The `port_forward` tool's `resourceName` parameter therefore allowed an attacker who controlled prompt content (RAG-poisoned docs, commit messages, retrieved tool responses) to inject space-delimited kubectl flags — e.g. `resourceName='pod-name --address=0.0.0.0'` binds the port-forward to all interfaces, `-n kube-system` redirects to an attacker-chosen namespace. Upstream gates exploitation on PR-injection / RAG-poisoning rather than direct network reach, but once a tainted resourceName reaches the tool, the MCP server is the abuse channel for cluster-scope kubectl. This is exactly the AML.T0010 + adversarial-tool-input pattern the trust-tier model in Step 5 below classifies — apply tool allowlisting (drop `port_forward` until 3.5.0+) and argv-array auditing to any MCP server that shells out to a CLI.

### Supply Chain Attack Surface

Every MCP server listed in popular registries (MCP Hub, npm `@modelcontextprotocol/*`) is a potential supply chain target. Unlike npm packages where exploitation requires running arbitrary code in the package lifecycle hooks, MCP servers are explicitly *designed* to run code on behalf of the AI model. The attack surface is the entire intended functionality.

**Observed patterns:**
- Typosquatting of popular MCP servers (e.g., `@mcp/filesystem` vs `@mcpfilesystem`)
- Legitimate servers with delayed malicious payloads (time-bomb or condition-based activation)
- Dependency confusion attacks targeting MCP servers in private registries

---

## Framework Lag Declaration

| Framework | Control | Why It Fails for MCP |
|---|---|---|
| NIST 800-53 | SA-12 (Supply Chain Protection) | Designed for software procurement and vendor management in enterprise contexts. No guidance for developer-installed AI tool plugins that execute code on behalf of AI models. SA-12's "supply chain risk management plan" does not contemplate MCP server provenance or trust. |
| NIST 800-53 | CM-7 (Least Functionality) | "Configure systems to provide only essential capabilities." Does not address the inverted trust model where the AI assistant decides which tools to call based on model judgment, not an allowlist. |
| NIST 800-53 | CM-11 (User-Installed Software) | User-installed software policy. MCP servers are installed by developers as part of their workflow. CM-11 doesn't distinguish between a code editor plugin and an MCP server that has RCE capability. |
| ISO 27001:2022 | A.8.30 (Outsourced development) | Third-party development supplier controls. MCP servers are not "outsourced development" — they are runtime tool providers that execute in the context of the AI session. Requires new control category. |
| ISO 27001:2022 | A.5.19 (Information security in supplier relationships) | Supplier risk management. Does not contemplate AI tool plugin supply chains or MCP server trust. |
| SOC 2 | CC9 (Risk Mitigation — vendor management) | Vendor review processes. SOC 2 vendor management reviews are designed for SaaS providers with data access, not MCP servers that run local code. Audit evidence does not cover MCP server signing or allowlisting. |
| CIS Controls v8 | Control 2 (Inventory and Control of Software Assets) | Software inventory and allowlisting. Does not explicitly cover MCP servers. AI coding assistant MCP configs are not in scope for most enterprise software inventory processes. |
| PCI DSS 4.0 | 12.3.4 | Review and manage third-party service providers. Scoped to service providers with access to cardholder data. An MCP server running on a developer workstation accessing a PCI-scoped codebase is not clearly in scope and would not appear in vendor management reviews. |
| SWIFT CSCF v2026 | 1.1 (SWIFT Environment Protection — allowlisted software inside the secure zone) | Mandates allowlisted software and protected operator-PC posture for the SWIFT secure zone. The control's allowlist concept is the closest existing analogue to MCP tool allowlisting, but CSCF 1.1 was written for traditional middleware and does not contemplate MCP servers, agent-mediated tool calls, or model-judgment-as-authorization on operator workstations adjacent to the SWIFT zone. |
| EU NIS2 | Art. 21(2)(d) (supply-chain security) + Art. 21(2)(e) (security in acquisition, development and maintenance) | "Appropriate and proportionate" supply-chain language. Member-state transpositions (BSI IT-SiG 2.0, ANSSI, CNIL) do not enumerate MCP servers as in-scope third-party components. An essential entity meets the NIS2 supplier-management obligation with traditional SaaS vendor reviews while leaving developer-workstation MCP servers entirely outside the supply-chain register. |
| EU DORA | Art. 28 (ICT third-party risk register) + Art. 30 (key contractual provisions) + Art. 6 (ICT risk-management framework) | Financial-entity ICT third-party language scoped to traditional ICT providers and cloud outsourcing. ESAs RTS on subcontracting (JC 2024/53) is silent on MCP servers running inside trading-desk developer environments, even though those MCP servers can reach repository, trading-system, and ticketing-system tools via the AI assistant. |
| EU AI Act (Regulation 2024/1689) | Art. 9 (risk management for high-risk AI) + Art. 15 (cybersecurity) + Art. 25 (responsibilities along the AI value chain) | Art. 25 addresses providers, deployers, importers, and distributors but does not categorize MCP server publishers as in-scope value-chain actors. High-risk AI cybersecurity language refers to "state of the art" without naming MCP supply chain as a scoped attack class. |
| UK NCSC CAF | Principle A4 (Supply Chain), B4 (System Security), B2 (Identity and Access Control) | Outcome-based language. NCSC's 2024 guidance on securing AI systems names supply-chain integrity for AI tooling, but the CAF outcome statements are unchanged — an organisation can achieve A4 / B4 outcomes at Achieved level with zero MCP server allowlisting, no signature verification, and no per-server authentication. |
| UK DSIT AI Cyber Code of Practice (2025) | Principle 7 (secure software supply chain) + Principle 8 (secure development) | Names supply-chain integrity for AI development but as a principle, not a testable control. No technical floor for MCP signing, allowlisting, or per-server auth. |
| AU ASD Essential 8 | Strategy: Application Control + Restrict Administrative Privileges | Application Control (allowlisting) is the closest existing strategy to MCP allowlisting but is scoped to operating-system-level executables. MCP servers run as long-lived child processes spawned by the AI assistant's process — Application Control rarely reaches the npm/pip-installed JavaScript or Python that constitutes an MCP server. None of the eight strategies address agent-mediated tool execution. |
| AU ASD ISM | ISM-2156 and ISM-2157 (agentic AI restricted to minimum tools; each tool call authorized for the user and the task) + ISM-2159 (tool invocations centrally logged) + ISM-1452 (supply chain risk assessment) + ISM-1657 (application control) | ISM-2156 and ISM-2157 cover what an agent may call, but neither covers where an MCP server came from: ISM-1452 assesses suppliers, not individual packages pulled from a registry, and ISM-1657 application control restricts executables and scripts on the host rather than the tool definitions an MCP server advertises to the agent. |
| AU APRA CPS 234 / CPS 230 | Para 27 (information security capability) + CPS 230 ICT-service-provider obligations | "Capability commensurate with vulnerabilities and threats" language. APRA-regulated entities deploying AI coding assistants meet CPS 234 attestation with traditional vendor-management capability; MCP-specific supply-chain capability is not an examined control. CPS 230 (effective 2025-07-01) third-party-arrangements obligations do not enumerate MCP servers as in-scope material service providers. |

**Fundamental gap:** No current framework has a control category for "AI tool trust boundaries" — the concept that an AI model can be the authorization mechanism for code execution, and that this creates a new class of supply chain and access control risk.

**Underlying RFC stack and its gaps.** MCP HTTP transport rides on RFC 9114 (HTTP/3) and/or RFC 9112 (HTTP/1.1). Server-to-agent authenticity claims rely on bearer tokens defined by RFC 7519 (JWT) — and MUST follow RFC 8725 (BCP 225, JWT Best Current Practices) to avoid `alg=none`, `kid` traversal, and audience-confusion attack classes. OAuth 2.0 (RFC 6749) is the typical authorization layer; operators should track RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) rather than the original RFC 6749 threat model. For per-request integrity, RFC 9421 (HTTP Message Signatures, published 2024-02) is the current standard, but the MCP specification does not yet mandate it — a documented gap that lets a network-positioned attacker tamper with or replay tool responses even when the transport is TLS-terminated at a reverse proxy. Reference `data/rfc-references.json` rather than restating content here.

---

## TTP Mapping

| ATLAS/ATT&CK ID | Technique | MCP Relevance | Gap |
|---|---|---|---|
| AML.T0010 | AI Supply Chain Compromise | Direct: malicious MCP server in public registry compromises AI assistant's tool execution | ATLAS covers this conceptually; no framework has a technical control |
| AML.T0054 | LLM Jailbreak | Indirect: adversarial prompt in tool response bypasses guardrails and triggers AI to call next malicious action | No framework control |
| AML.T0053 | AI Agent Tool Invocation | AI assistant is the integration point being abused — MCP tool calls are the mechanism | Not in ATT&CK; only in ATLAS v2026.09 |
| T1195.001 | Supply Chain Compromise: Compromise Software Dependencies | MCP server package as supply chain attack target | ATT&CK covers but enterprise controls don't reach developer MCP configs |
| T1059 | Command and Script Interpreter | MCP server causes shell command execution via model-mediated tool call | Standard SI-3/EDR doesn't attribute this to the MCP server as origin |
| T1190 | Exploit Public-Facing Application | CVE-2026-30615: MCP client vulnerability driven by a locally-installed malicious server (AV:L) | Standard vuln management covers client; MCP server trust is unaddressed |

---

## Exploit Availability Matrix

Sourced from `data/cve-catalog.json` and `data/exploit-availability.json` as of 2026-05-11.

| Threat | CVSS | RWEP | PoC Public? | CISA KEV? | AI-Accelerated Weaponization? | Patch Available? | Reboot / Version Bump Required? |
|---|---|---|---|---|---|---|---|
| CVE-2026-30615 (Windsurf MCP local-vector RCE) | 8.0 | 35 | Partial — conceptual exploit demonstrated; weaponization stage `partial` | No (architectural class; not in KEV catalog as of 2026-05) | No direct AI-assisted weaponization recorded; the attack vector itself rides on the AI agent's tool-call autonomy | Yes — vendor IDE update | IDE update / version bump required (no reboot); `live_patch_available: true` via vendor channel |
| CVE-2026-39884 (Flux159 mcp-server-kubernetes argument injection) | 8.3 | n/a | Yes — GHSA-4xqg-gf5c-ghwq publishes the PoC (port_forward `resourceName='pod --address=0.0.0.0'`) | No | No direct AI-assisted weaponization; the bug is reached by tricking the assistant via prompt injection in retrieved docs / commit messages into passing a tainted resourceName | Yes — upgrade mcp-server-kubernetes to 3.5.0+ (argv-array refactor); workaround: disable `port_forward` in MCP allowlist | Version bump on the MCP server side; no client reboot |
| MCP supply chain compromise — typosquatting / dependency confusion (ATLAS AML.T0010) | N/A (technique, not vendor CVE) | N/A | Yes — public typosquatting incidents in `@modelcontextprotocol/*` namespace observed | No (technique class) | Yes — AI assistants accelerate writing of convincing malicious tool descriptions | Mitigation only: pin versions, verify npm provenance attestation, enforce allowlist | Re-install / pin to known-good version |
| Adversarial tool response → indirect prompt injection (ATLAS AML.T0054 in MCP context) | N/A (technique, not vendor CVE) | N/A | Yes — public research demonstrations; weaponizable wherever output is unsanitized | No | Yes — adversarial instruction crafting is a documented AI-accelerated capability | Mitigation only: output sanitization, system-prompt authority hierarchy, tool allowlisting | Client configuration change; no version bump strictly required |
| AML.T0096 — MCP tool call as covert C2 conduit | N/A (technique) | N/A | Yes — SesameOp-class techniques apply when an MCP tool call is the relay | No | Yes — see `data/atlas-ttps.json` AML.T0096 real-world instances | Mitigation only: process-level AI/MCP egress monitoring | Configuration / monitoring change |

**Interpretation:** CVE-2026-30615 has a vendor patch and live-update path — verify Windsurf clients are on the patched version. The remaining rows are technique classes with no vendor CVE; mitigation is configurational (signed manifests, tool allowlists, bearer auth, output sanitization, version pinning) and cannot be "patched away" by a single vendor release.

---

## Analysis Procedure

The procedure runs five sequential steps: inventory installed MCP servers per workstation, verify each server's package provenance against npm signatures and CISA KEV listings, assess trust configuration (auth, allowlist, scope), score the trust posture against the published CVE class, and generate remediation actions for any server scoring above the operator's risk threshold. Each step's output feeds the next; the inventory drives the provenance check, the provenance result drives the trust score, and the trust score drives the remediation list.

### Step 1: Inventory installed MCP servers

For each developer workstation or shared AI system:

```bash
# AI coding assistant MCP configs (check all that are installed):
cat ~/.claude/settings.json | jq '.mcpServers'
cat ~/.cursor/mcp.json
cat ~/.windsurf/mcp.json
cat ~/.gemini/settings.json
cat ~/.vscode/settings.json | grep -A 20 '"mcp"'
```

For each server found, record:
- Package name and version
- Installation source (npm, local path, custom registry)
- What tools it exposes
- What filesystem/network/process permissions it requires
- Whether an explicit tool allowlist exists

### Step 2: Verify package provenance

For each npm-installed MCP server:
```bash
npm pack --dry-run <package-name>
npm audit <package-name>
# Check: is the package signed? (npm provenance)
npm view <package-name> dist.integrity
# Check: does it match the expected hash?
```

Red flags:
- Recent publication (< 30 days) with high download counts
- Package name close to a well-known server (typosquatting)
- Dependencies with postinstall scripts
- No npm provenance attestation

### Step 3: Assess trust configuration

For each MCP client configuration, check:

**Tool allowlisting:**
- Is there an explicit `allowed_tools` list? (restricts which tools the AI can call)
- If no allowlist: the AI can call any tool the server exposes, including tools added after installation
- Risk: server can add new malicious tools in an update, no re-consent required

**Authentication:**
- Does the MCP server require authentication (bearer token, mTLS)?
- If no auth: any local process can connect to the MCP server and impersonate the AI client
- Applies particularly to MCP servers that listen on a local port

**Output trust:**
- Are MCP server responses treated as trusted (passed directly to model context)?
- If yes: adversarial instructions in tool responses execute in model context

**Process isolation:**
- Does the MCP server process run with the same privileges as the AI client?
- Does it have filesystem access beyond its stated scope?
- Does it have network access?

### Step 4: Score MCP trust posture

| Factor | Risk Score |
|---|---|
| No tool allowlist | +High |
| No package signing verification | +High |
| No authentication required by server | +Medium |
| Server has filesystem read/write access | +High |
| Server has shell/process execution access | +Critical |
| Server has network access | +Medium |
| Outputs not sanitized | +High |
| Server was installed from public registry without audit | +Medium |
| Server version was auto-updated | +Medium |
| No MCP server activity logging | +High |

### Step 5: Generate remediation

**Immediate (regardless of risk posture):**
1. Audit all installed MCP servers — full inventory
2. Remove any servers that cannot be verified by provenance
3. Pin all MCP server versions (no auto-update)
4. Enable logging for all MCP tool calls (what tool was called, what arguments, what response)

**Configuration hardening:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@1.2.3"],
      "allowed_tools": ["read_file", "list_directory"],
      "env": {}
    }
  }
}
```

**Trust tier model:**
- Tier 0 (no install): MCP servers with shell/process execution, network exfil capability, unsigned
- Tier 1 (audited, pinned, allowlisted): Standard workspace MCP servers (filesystem, git, DB read-only)
- Tier 2 (monitored): Any server with write access — every tool call logged and alertable

**For organizational deployments:**
- Maintain an approved MCP server registry (name, version, hash, approved scopes)
- Distribute approved MCP configs via MDM/endpoint management
- Block unapproved MCP server installations on managed workstations
- Monitor for new MCP server additions in endpoint config files

---

## Output Format

The skill produces a structured MCP Trust Assessment per workstation or fleet. The shape below is consumed downstream by `supply-chain-integrity` (which picks up the per-server hash and provenance fields), by `ai-attack-surface` (which integrates the MCP Trust posture into the broader AI surface report), and by `compliance-theater` (which compares the unallowlisted-server count against any vendor-management compliance claim). Operators feeding the output into MDM or endpoint-management policy should preserve the approved-server registry shape verbatim.

```
## MCP Trust Assessment

**Assessment Date:** YYYY-MM-DD
**Scope:** [workstations / AI systems assessed]

### Installed MCP Server Inventory
| Server | Version | Source | Tools Exposed | Filesystem | Network | Shell | Auth Required | Allowlist |
|--------|---------|--------|---------------|------------|---------|-------|---------------|-----------|

### CVE-2026-30615 Exposure
[Windsurf version check — patched/unpatched]

### Trust Posture Score
[Per server: Critical/High/Medium/Low with factor breakdown]

### Immediate Actions Required
[Servers to remove, versions to pin, configs to lock]

### Hardened Configuration
[Ready-to-use JSON config for each AI client in scope]

### Framework Gap Declaration
[Per-framework: what control nominally applies, why it doesn't cover MCP trust, what a real control requires]

### Organizational Policy Requirements
[If org-level deployment: approved registry, MDM config, monitoring requirements]
```

---

## Hand-Off / Related Skills

After producing the MCP trust assessment output, the operator should chain into the following skills. Each entry is specific to a finding class this skill produces.

- **`supply-chain-integrity`** — MCP servers are software supply chain artifacts. For every server in the inventory, produce SLSA-level attestation, Sigstore signature verification, and in-toto provenance. The MCP ecosystem ships overwhelmingly via npm without provenance; this is the artefact-level control that the vendor-management gap above implicitly delegates to.
- **`defensive-countermeasure-mapping`** — map MCP trust failures to D3FEND counters: D3-EHB (hash-based executable allowlisting for the MCP server binary), D3-CBAN (certificate-based authentication between client and server), D3-MFA (multi-factor authentication on the MCP control plane where remote), D3-CSPP (client-server payload profiling on tool call / tool response shapes). The trust-tier model in Step 5 above is operationalised through these counters.
- **`attack-surface-pentest`** — explicitly include each installed MCP server in the in-scope target list for pen-testing and adversary emulation. 2025-vintage pen-test scopes overwhelmingly omit MCP servers; this is the single biggest assumed-out-of-scope gap discovered during this skill's analysis.
- **`dlp-gap-analysis`** — MCP tool arguments are a DLP egress channel. Verify that SDK-level prompt logging captures tool-arg egress (filenames, file contents, credential strings passed as arguments) and that DLP classifiers run on the tool-call payload, not just on file/email egress. Without this, an MCP server with filesystem read access is a fully invisible exfiltration path.
- **`framework-gap-analysis`** — when the MCP trust gap fails a specific framework control (NIST-800-53-CM-7 / ISO-27001-2022-A.8.30 / SOC2-CC9 vendor management), invoke this skill to produce the formal gap declaration tied to the organisation's compliance scope and jurisdiction, including the EU NIS2 / DORA / AU Essential 8 mappings (global-first coverage, not US-only).

For ephemeral / serverless AI-pipeline contexts (where some controls are architecturally impossible): live SLSA-attestation verification at runtime is architecturally impossible for inline-pulled MCP servers in serverless functions. The scoped alternative is build-time attestation pinning baked into the function image, with the runtime fetch path disabled at the network layer.

---

## Defensive Countermeasure Mapping

D3FEND v1.3.0+ references from `data/d3fend-catalog.json`. MCP trust failures land on a tightly bounded set of defensive techniques because the attack surface is structural: a tool registered in `mcp.json` runs with the AI assistant's authority unless the listed controls intervene.

| D3FEND ID | Name | Layer | Rationale (what it counters here) |
|---|---|---|---|
| `D3-EHB` | Executable Hash-based Allowlist | Host / MCP server registration | Pins each MCP server binary by hash so CVE-2026-30615-class supply-chain swaps (compromised `npx` package replaces the server with an exploit variant) cannot replace the trusted binary silently. Direct counter to AML.T0010 + T1195.001. |
| `D3-EAL` | Executable Allowlisting | Host / shell-capable tool | Restricts which executables an MCP shell-tool or process-exec-capable server can spawn. Without this, a server with `bash`/`pwsh` tools is a shell on the developer workstation with the developer's authority. |
| `D3-CAA` | Credential Access Auditing | Identity / MCP bearer-auth | Logs every MCP server's use of the bearer token / OAuth credential and the resources it touched. The audit anchor for AML.T0086 (model and credential exfiltration via tool calls); the only post-hoc evidence stream when an MCP server is trusted but malicious. |
| `D3-CSPP` | Client-server Payload Profiling | MCP gateway | Gateway-layer inspection of MCP tool-call args and tool-result bodies. The single control that can detect indirect prompt-injection payloads landing in `tools/call` results, AML.T0051 patterns reaching the assistant through document fetches, and AML.T0096 covert C2 over MCP transport. |
| `D3-CBAN` | Certificate Analysis | Transport / MCP server-side | Validates the MCP server's TLS certificate chain and binds it to a pinned identity registered in the host's MCP catalog. Counters the "stand-up a malicious MCP server with a Let's Encrypt cert pretending to be a sanctioned vendor" pattern. |
| `D3-MFA` | Multi-factor Authentication | Identity / OAuth client registration | Required for MCP servers registered as OAuth clients against enterprise IdPs. Without phishing-resistant MFA on the registration flow, a compromised developer credential can register an attacker-controlled MCP server inside the org's trust boundary. |

**Defense-in-depth posture:** `D3-EHB` is the registration layer (only signed/hashed binaries register); `D3-EAL` is the runtime layer (only allowlisted child processes spawn); `D3-CSPP` is the in-flight content layer; `D3-CAA` is the post-hoc audit layer; `D3-CBAN` is the transport-identity layer; `D3-MFA` is the registration-identity layer. CVE-2026-30615 demonstrated that any single-layer defence fails — a signed manifest alone (`D3-EHB`) does not prevent an in-band path-traversal RCE that lands once the manifest is honoured.

**Least-privilege scope:** every MCP server's tool allowlist is the minimum set required for its sanctioned use case — a documentation-search server does not get a `bash` tool, an issue-tracker server does not get a `read_file` tool with `/etc/**` glob authority. `D3-EAL` enforces this at the spawn boundary; `D3-CAA` audits every authorisation use against the documented scope.

**Zero-trust posture:** every MCP server is treated as an untrusted third party regardless of vendor reputation — `D3-EHB` pin on registration, `D3-CBAN` cert verification on every connection, `D3-CSPP` payload inspection on every tool call. No "first-party vendor" exemption; the Cursor / Windsurf / VS Code first-party plugins ship through the same supply-chain (`npm` / `pip` / VS Code marketplace) that AML.T0010 targets.

**AI-pipeline applicability (some controls are architecturally impossible in ephemeral / hosted contexts):** `D3-EAL` and `D3-EHB` apply only when the MCP server runs as a local executable. For hosted / remote MCP servers (the Claude Code, Cursor, and Windsurf hosted-tool pattern), the scoped alternative is `D3-CBAN` (pinned server identity) + `D3-CSPP` at the egress gateway + `D3-CAA` against the hosted-server provider's audit log feed. The endpoint controls (`D3-EAL`/`D3-EHB`) move from "verify locally before run" to "verify provider attestation before connect."

---

## Compliance Theater Check

> "Your vendor management control (CC9 / SA-12 / A.5.19) documents a review process for third-party software with access to sensitive systems. Enumerate the MCP servers installed on developer workstations that have access to production codebases or credentials. How many of those MCP servers went through your vendor review process? If the answer is zero, the vendor management control is theater for the attack surface where AI-assisted supply chain attacks are actually occurring."
