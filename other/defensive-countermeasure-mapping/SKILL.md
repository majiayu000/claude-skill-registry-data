---
name: defensive-countermeasure-mapping
version: "1.0.0"
description: Map offensive findings (CVE / TTP / framework gap) to MITRE D3FEND defensive countermeasures with explicit defense-in-depth, least-privilege, and zero-trust layering
triggers:
  - defensive mapping
  - d3fend
  - countermeasure
  - blue team
  - defense in depth
  - least privilege
  - zero trust
  - control mapping
  - mitigation
  - defensive coverage
  - blue team map
data_deps:
  - d3fend-catalog.json
  - atlas-ttps.json
  - cve-catalog.json
  - framework-control-gaps.json
  - cwe-catalog.json
  - dlp-controls.json
atlas_refs: []
attack_refs: []
framework_gaps: []
rfc_refs: []
cwe_refs: []
d3fend_refs:
  - D3-ASLR
  - D3-CA
  - D3-CBAN
  - D3-CSPP
  - D3-DA
  - D3-EAL
  - D3-EHB
  - D3-FAPA
  - D3-FE
  - D3-IOPR
  - D3-MENCR
  - D3-MFA
  - D3-NI
  - D3-NTA
  - D3-NTPM
  - D3-PA
  - D3-PHRA
  - D3-PSEP
  - D3-RPA
  - D3-SCP
last_threat_review: "2026-06-10"
discovery_mode: "standalone"  # operator-reached via `exceptd brief defensive-countermeasure-mapping` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Defensive Countermeasure Mapping — D3FEND as the Blue-Team Counterpart to ATT&CK / ATLAS

ATT&CK and ATLAS catalog what attackers do. D3FEND catalogs what defenders do, in the same technique-grain taxonomy. Most SOCs in mid-2026 maintain an ATT&CK heatmap of detection coverage; far fewer maintain a D3FEND coverage map of the controls that actually counter those techniques. Operators can articulate attacker behavior with technique-level precision but can only articulate their own defenses at framework-control granularity ("we have SI-2"), which is a category mismatch. This skill closes that mismatch. Inputs are offensive findings — a CVE, an ATT&CK or ATLAS technique, a framework control gap. Outputs are layered defensive-countermeasure maps grounded in `data/d3fend-catalog.json` and explicitly threaded through defense-in-depth, least-privilege, and zero-trust principles.

## Frontmatter Scope

The `atlas_refs`, `attack_refs`, and `framework_gaps` arrays are intentionally empty. This skill maps defensive countermeasures (MITRE D3FEND) rather than owning a native set of offensive techniques — its subject is the blue-team control taxonomy, not adversary TTPs. The offensive techniques it counters come from whatever finding the operator supplies at invocation time; that input domain is the union of every ATLAS/ATT&CK technique in the catalog, so pinning a fixed subset here would falsely narrow it. The authoritative technique attachment lives in the offensive skill that produced the finding.

---

## Threat Context (mid-2026)

ATT&CK and ATLAS are now load-bearing in SOC detection engineering. Detection content is written against technique IDs; red-team reports are mapped to technique IDs; threat intel feeds emit technique IDs. The result: the offensive side of every blue-team discussion is technique-grained and crisp.

The defensive side has not caught up. Most SOCs maintain an ATT&CK heatmap (coverage of detection rules by technique). Few maintain a D3FEND coverage map of the controls that actually counter those techniques. The structural failure has three observable shapes:

- **Detect-only blue teams.** A SOC will claim coverage of T1068 (Privilege Escalation) because EDR alerts fire on suspicious process behavior. The Harden, Isolate, Evict, and Restore tactics are unrepresented. For Copy Fail (CVE-2026-31431) that means the org has a detection rule for the post-exploit shell but no D3-SCP (seccomp), no D3-PHRA (hardware isolation), and no live-patch path under D3-PA. Defense is one-layer-deep; the attacker only has to bypass detection to win.
- **Framework-grained articulation.** Asked "what countermeasures are in place for prompt injection?", the team answers "we have AC-3 and SI-10." Both controls exist on paper. Neither describes a defensive technique at the grain the attack operates at. The actual D3FEND mappings (D3-IOPR for I/O profiling, D3-CSPP for client-server payload profiling, D3-EAL for tool allowlisting on the MCP server side) are absent from the team's vocabulary.
- **Implicit-trust controls treated as zero-trust.** Many deployed defenses verify identity once at the perimeter and trust thereafter. Under D3FEND grain, these are not zero-trust controls — D3-NI (Network Isolation) without D3-NTA (Network Traffic Analysis) and per-request authorization assumes implicit trust on segments. The compliance audit passes; an attacker with one foothold moves laterally without re-verification.

Concrete examples from this project's catalogs:

- **Copy Fail (CVE-2026-31431).** Offensive: T1068 + AML.T0017. Defensive map produced by this skill: D3-EAL (Harden), D3-EHB (Harden), D3-SCP (Isolate), D3-PHRA (Isolate), D3-PA (Detect), plus the live-patch path under `kernel-lpe-triage`. A SOC claiming "we have EDR" is at one D3FEND layer for a five-layer-deep finding.
- **Windsurf MCP RCE (CVE-2026-30615).** Offensive: AML.T0010 + AML.T0096 + T1195.001. Defensive map: D3-EHB (binary hash pinning, primary), D3-EAL (executable allowlist on the MCP runtime), D3-NTA (network traffic analysis on egress from the dev workstation), D3-CSPP (payload profiling on MCP JSON-RPC calls), D3-IOPR (I/O profiling of tool invocations). Five D3FEND IDs spanning Harden / Isolate / Detect — the depth most "we trust our IDE plugins" defenses lack.
- **SesameOp AI-as-C2 campaign.** Offensive: AML.T0096 + T1071 + T1102. Defensive map: D3-NTA + D3-CSPP on Azure OpenAI egress, D3-DA (Domain Analysis) for the C2 domain set, D3-NTPM (Network Traffic Policy Mapping) to model legitimate-versus-anomalous LLM API usage, D3-RPA (Remote Process Analysis) on the calling host. The Detect tactic dominates here because Harden does not apply to a covert channel riding legitimate API traffic — which is itself a finding worth surfacing.

The skill exists because the inverse direction — given a CVE or TTP, produce the layered countermeasure map — is the question SOCs need to answer to demonstrate operational defense, and it is the question framework controls cannot answer at the right grain.

---

## Framework Lag Declaration

No major compliance framework requires technique-grained defensive mapping. Each requires controls; none require controls expressed in the D3FEND technique taxonomy that mirrors ATT&CK and ATLAS. The MITRE Center for Threat-Informed Defense ATT&CK Mappings project (the NIST 800-53 → ATT&CK and D3FEND → NIST 800-53 crosswalks) provides the bridge, but its latest published crosswalk targets ATT&CK Enterprise v16.1 — lagging the current v19.1 matrix — operator awareness is limited, and no framework yet requires its use.

| Jurisdiction | Framework / Control | What It Requires | Why It Is Insufficient at D3FEND Grain |
|---|---|---|---|
| US | NIST CSF 2.0 PROTECT (PR.AA, PR.DS, PR.PS, PR.IR, PR.PE) | Identity management, data security, platform security, infrastructure resilience, environmental protection | High-level outcomes. Does not require mapping each protect outcome to a D3FEND technique. A PR.PS implementation can be a vendor product purchase with no per-technique verification. |
| US | NIST 800-53 Rev 5 | Per-control families (AC, AU, CM, CP, IR, SI, SC, etc.) | Framework controls, not defensive techniques. "Implement SI-3 malicious code protection" is satisfied by deploying AV; it does not require D3-PA (Process Analysis) or D3-FAPA (File Access Pattern Analysis) at the technique grain. |
| US | NIST AI RMF 1.0 MAP / MEASURE / MANAGE | AI risk management functions | Risk-management vocabulary. No technique-level defensive mapping for AML attack surface. AI-pipeline gaps go invisible at this grain. |
| EU | NIS2 Directive Art. 21 | "Appropriate and proportionate technical, operational and organisational measures" | Outcome language. Member-state transpositions vary. None require D3FEND mapping or technique-grained defensive coverage demonstration. |
| EU | DORA Art. 6–10 | ICT risk management for financial entities | Risk-management process. Defensive technique grain unspecified. |
| EU | EU AI Act Art. 15 | "Appropriate level of accuracy, robustness and cybersecurity" for high-risk systems | Outcome standard. No technique mapping for AML or LLM attack surface. |
| EU | EU CRA | Cybersecurity essential requirements for products with digital elements | Product-level requirements. Says nothing about how an operator should structure defensive coverage. |
| UK | NCSC CAF v3.2 Objective B (Protecting against cyber attack) | Outcome-based principles (B1–B6) | Outcome-based by design. CAF does not prescribe defensive techniques. A B2 (identity and access control) achievement can be a SSO deployment with no D3-MFA / D3-CBAN technique verification. |
| UK | Cyber Essentials Plus | Five technical control categories | Coarse-grained checklist. No technique-level mapping. |
| AU | ASD Essential 8 ML1–ML3 | Eight mitigation strategies (app control, patching, MFA, etc.) | Closest to technique-grain (Essential 8 has named strategies) but still control-level not technique-level. Application Control is roughly D3-EAL / D3-EHB but the maturity model does not distinguish path-based allowlist from cryptographic hash allowlist. |
| AU | ISM | Detailed control catalog | Control-level. Does not require D3FEND mapping. |
| AU | APRA CPS 234 | Information security capability for regulated entities | Capability-level. Defensive technique grain unspecified. |
| Global | ISO 27001:2022 Annex A | 93 controls across organisational / people / physical / technological | Control-level. ISO 27001:2022 added A.5.7 (Threat Intelligence) and A.8.16 (Monitoring activities) but neither requires defensive technique mapping. |
| Global | ISO 27002:2022 | Implementation guidance for Annex A | Guidance, not requirement. |
| Industry | PCI DSS v4.0 | Twelve requirements for cardholder data environments | Control-level. The closest technique-grain language is in 5.x (malware protection) — does not require D3FEND mapping. |
| Industry | SOC 2 TSC | Trust Services Criteria outcome categories | Outcome-level. Auditor discretion on implementation. |

The cross-framework pattern is uniform: every framework operates at control or outcome grain. D3FEND operates at technique grain. The translation layer — which technique counters which attack technique, in which D3FEND tactic, at which trust posture, at which privilege scope — is the gap this skill fills. The framework controls themselves are not wrong; they are coarser than the threat. The framework lag is structural and first-class: no framework yet operationalizes the defensive technique taxonomy.

---

## TTP Mapping

This is a meta-mapping skill. Its TTP coverage equals the union of: every ATLAS technique in `data/atlas-ttps.json`, every ATT&CK technique appearing in any `attack_refs` field across the skill library, and every offensive technique referenced in any `counters_attack_techniques` array inside `data/d3fend-catalog.json`. Every D3FEND ID in the catalog is mapped to at least one offensive technique — there are no orphan defensive entries (no orphaned controls).

The skill consumes offensive findings from these inputs and produces defensive mappings. It does not author new offensive technique entries; that is the job of the catalogs upstream and the `zeroday-gap-learn` and `threat-model-currency` skills. The cross-walk surfaces:

| Input Source | Read From | Skill Produces |
|---|---|---|
| CVE | `data/cve-catalog.json` (entry's `atlas_refs`, `attack_refs`, `cwe_refs`) | D3FEND IDs whose `counters_attack_techniques` includes those refs |
| ATLAS technique | `data/atlas-ttps.json` | D3FEND IDs whose `counters_attack_techniques` lists the ATLAS ID |
| ATT&CK technique | implicit (no local ATT&CK catalog; technique is the key) | D3FEND IDs whose `counters_attack_techniques` includes the T-number |
| Framework gap | `data/framework-control-gaps.json` | D3FEND IDs whose `framework_controls_partially_mapped` references the gapped control |
| CWE | `data/cwe-catalog.json` | D3FEND IDs that mitigate the CWE's root-cause class (joined via the CVE catalog) |
| Data-loss / exfil concern | `data/dlp-controls.json` | D3FEND IDs in the Isolate and Detect tactics that the DLP entry's `d3fend_refs` field points to |

Reference `data/atlas-ttps.json` and `data/d3fend-catalog.json` for the canonical cross-references. The skill never invents a mapping not present in the catalogs; if a finding has no D3FEND coverage in the catalog, that is itself a finding to surface and route to `zeroday-gap-learn` for catalog update.

---

## Exploit Availability Matrix

This skill is the inverse of `exploit-scoring`. Where `exploit-scoring` produces a per-CVE matrix of offensive availability (CVSS, RWEP, KEV, PoC, AI-acceleration, live-patch availability), this skill consumes that matrix and produces the dual — a per-D3FEND-ID **defensive availability matrix** for the same finding. The dual question is not "how exploitable is this in the wild" but "how defended is this in the org's stack." Both matrices are per-finding; together they form the offense-defense pair the SOC needs.

For each D3FEND ID surfaced by Analysis Procedure Step 3, the matrix records:

| Factor | Source | Meaning |
|---|---|---|
| Deployed in the org's stack? | operator input, verified against asset inventory | Is the control actually running, or only purchased / specified? |
| Tunable per environment? | `data/d3fend-catalog.json` `implementation_examples` | Can the control be tuned for serverless vs. monolith vs. ephemeral container, or is it host-only? |
| AI-pipeline applicable? | `data/d3fend-catalog.json` `ai_pipeline_applicability` (mandatory field) | If the control is architecturally impossible in serverless / container / AI pipeline contexts, the catalog declares an explicit alternative (e.g., admission-controller signature verification as the D3-EAL surrogate for serverless). The matrix surfaces that alternative. |
| Defense-in-depth layer | computed from `data/d3fend-catalog.json` `tactic` (Model / Harden / Detect / Isolate / Deceive / Evict / Restore) | Which DiD layer the control occupies for this finding. A finding defended only in one layer is under-defended. |
| Privilege scope | computed from `data/d3fend-catalog.json` description and from the operator's deployment context | Per-process (D3-EAL, D3-EHB), per-segment (D3-NTA, D3-NI), per-request (D3-CBAN, D3-MFA when continuously verified), or blanket (D3-PSEP / D3-ASLR — kernel-wide). |
| Zero-trust posture | computed from D3FEND description; verifies-per-request vs. trusts-after-perimeter | A control that verifies on every request (D3-MFA continuous reauth, D3-CBAN per-call) is zero-trust. A control that authenticates once and trusts thereafter (vanilla session cookies, perimeter-only D3-NI) is implicit-trust. |
| Framework controls partially mapped | `data/d3fend-catalog.json` `framework_controls_partially_mapped` | The framework controls that nominally cover this technique but, per `lag_notes`, fail to operationalize it at D3FEND grain. |
| Live-tunable vs. requires deploy | operator input, joined with `implementation_examples` | Can the control be tuned without a rolling deploy (e.g., updating a Kyverno policy) or does it require image rebuilds and reboots? |

If the operator cannot supply deployment-status data, the matrix surfaces "unknown deployment status — must verify against asset inventory before claiming coverage" and the skill flags the finding as undefended for reporting purposes. No fabricated deployment data.

---

## Analysis Procedure

The procedure is threaded through three foundational principles. None are optional. Every output of this skill must visibly thread all three.

### Foundational principle 1 — Defense in depth

For any offensive finding, surface **multiple D3FEND IDs across different D3FEND tactics**. A finding mapped to a single D3FEND ID is, by definition, an under-defended finding. The taxonomy lists seven tactics (Model, Harden, Detect, Isolate, Deceive, Evict, Restore). A complete defensive map should populate at least three of them, with the floor being **Harden + Detect + Isolate** for any RWEP-significant finding. Findings that admit only one tactic (e.g., AI-as-C2 over legitimate API channels admits Detect almost exclusively) must surface that asymmetry as its own observation — the inability to Harden is itself a finding.

### Foundational principle 2 — Least privilege

Every D3FEND mapping must carry a **privilege-scoping note**. Controls differ sharply in scope:

- Per-process scope: D3-EAL (executable allowlisting), D3-EHB (executable hash-based allowlisting), D3-SCP (seccomp / syscall filtering), D3-PA (process analysis).
- Per-segment scope: D3-NTA (network traffic analysis), D3-NI (network isolation), D3-NTPM (network traffic policy mapping).
- Per-request scope: D3-CBAN (certificate-based authentication when verified per call), D3-MFA (multi-factor authentication when reauthenticated per session-action).
- Blanket scope (kernel-wide, applies to all processes uniformly): D3-PSEP (DEP/NX), D3-ASLR (KASLR), D3-PHRA (hardware resource access).

Least-privilege defense requires picking the finest available scope. A blanket-scope control is not a substitute for a per-process control when the threat operates at process grain. The output must surface, for each D3FEND ID, the scope at which it applies for this finding.

### Foundational principle 3 — Zero trust

Every D3FEND mapping must carry a **trust-posture classification**:

- **Verifies on every request.** Examples: D3-CBAN with per-call certificate validation, D3-MFA with continuous reauth, D3-CSPP applied to every JSON-RPC call.
- **Verifies on session establishment, trusts thereafter.** Examples: vanilla TLS session resumption, perimeter D3-NI without internal traffic analysis.
- **Assumes implicit trust on a segment.** Examples: bare D3-NI without D3-NTA inside the segment.

Zero-trust-compliant defense maps to controls that verify per request. Implicit-trust controls are not invalid — they are layer-1 — but the output must label them so the operator can see the trust assumption a given control is making. Never imply a framework control is adequate when current TTPs bypass it; the trust-posture column is the explicit corrective.

### Steps

**Step 1 — Ingest the offensive finding.** Classify the input as one of: CVE, ATLAS technique, ATT&CK technique, framework gap, CWE, or DLP/exfil concern. If the input is a CVE, pull the full entry from `data/cve-catalog.json` and extract `atlas_refs`, `attack_refs`, and `cwe_refs`. If the input is a TTP, capture it directly. If a framework gap, pull the full gap entry from `data/framework-control-gaps.json` and capture the controls that nominally cover it. If a CWE, pull it from `data/cwe-catalog.json` and capture the linked CVE class. If a DLP concern, pull from `data/dlp-controls.json` and capture the linked D3FEND techniques directly. Output the classification at the top of the report — every downstream step depends on it.

**Step 2 — Build the offensive-technique set.** For the input, build the full set of offensive techniques to map against. For a CVE: union of `atlas_refs` and `attack_refs`. For a TTP: the TTP itself. For a CWE: every CVE in `data/cve-catalog.json` that references the CWE, then the union of their `atlas_refs` and `attack_refs`. For a framework gap: the threats the gap is documented against in `data/framework-control-gaps.json`. The output of this step is a concrete list of technique IDs the defensive map must counter.

**Step 3 — Query D3FEND.** For every technique ID from Step 2, scan `data/d3fend-catalog.json` for entries whose `counters_attack_techniques` array includes that ID. Capture every match — do not stop at the first. Group results by D3FEND tactic (Model / Harden / Detect / Isolate / Deceive / Evict / Restore). The tactic grouping is the defense-in-depth view.

**Step 4 — Score each candidate countermeasure.** For each D3FEND ID surfaced in Step 3, record:
(a) Deployment status. Operator answers: deployed / partially deployed / not deployed / unknown.
(b) AI-pipeline applicability. Read `ai_pipeline_applicability` directly from `data/d3fend-catalog.json`. If the catalog states the control is architecturally impossible in the operator's environment, capture the explicit alternative the catalog provides.
(c) Defense-in-depth layer position — the D3FEND tactic the technique belongs to.
(d) Least-privilege scope — per-process / per-segment / per-request / blanket, per the principle 2 classification.
(e) Zero-trust posture — verifies-per-request / verifies-on-session / implicit-trust-on-segment, per the principle 3 classification.
(f) Live-tunable vs. requires deploy. Pull from `implementation_examples` and operator deployment context.

**Step 5 — Compute defensive depth.** Count the number of distinct D3FEND tactics in the map for this finding. If fewer than three tactics are populated, flag the finding as under-defended at the depth dimension. Separately, for each tactic, count how many D3FEND IDs are deployed (per Step 4(a)). If any tactic is empty of deployed controls, flag that tactic as a depth gap.

**Step 6 — Compute compliance-theater overlap.** For every D3FEND ID surfaced, read `framework_controls_partially_mapped` and the matching `lag_notes` from `data/d3fend-catalog.json`. Output the framework controls the operator's audit will claim as coverage and the lag-note text describing why those controls are insufficient at D3FEND grain. This is the bridge into the compliance-theater check below.

**Step 7 — Cross-walk through CWE and DLP.** If the finding has a CWE in `data/cwe-catalog.json`, surface the CWE's root-cause mitigation chain and link to any D3FEND IDs the catalog maps to that chain. If the finding involves data exfiltration, surface the `data/dlp-controls.json` entries whose `d3fend_refs` overlap with the D3FEND IDs surfaced in Step 3. The dual catalog joins ensure no orphan defensive recommendation.

**Step 8 — Produce the defensive-coverage map.** Render the matrix per Output Format below. Surface gaps prominently. Route to `policy-exception-gen` for any D3FEND ID the operator declares architecturally impossible. Route to `framework-gap-analysis` for any `framework_controls_partially_mapped` entry the operator wants escalated. Route to `zeroday-gap-learn` if any offensive technique in Step 2 has zero D3FEND coverage in the catalog (the catalog itself is the gap, not just the operator's deployment).

---

## Output Format

The skill produces a Defensive Countermeasure Map per input (CVE ID, ATLAS / ATT&CK TTP, threat-actor profile, or framework gap), pairing each offensive technique with the D3FEND defensive technique that disrupts it and the deployment layer that owns it. The shape below is consumed downstream by `framework-gap-analysis` (which wraps the map into Framework Lag Declarations), by `policy-exception-gen` (which converts the map into compensating-control language for defensible exceptions), and by every per-domain skill's own Defensive Countermeasure Mapping section. Preserve the D3FEND IDs verbatim — they are the auditable reference into `data/d3fend-catalog.json`.

```
# Defensive Countermeasure Map — <input>

## What this is
<one-line classification + canonical reference>
Example: "CVE — Linux kernel LPE. Canonical: CVE-2026-31431 (Copy Fail)."

## Offensive technique set (input to D3FEND query)
- <AML.T####-or-similar / T####-or-similar / CWE-<id> list, with one-line descriptions>

## Defensive-coverage map
| D3FEND ID | Name | Tactic (DiD layer) | Privilege scope | ZT posture | Deployed? | AI-pipeline applicable? | Framework controls partially mapped | Live-tunable? |
|-----------|------|--------------------|-----------------|------------|-----------|--------------------------|--------------------------------------|---------------|
| D3-EAL    | Executable Allowlisting | Harden | per-process | verifies on exec | partial | partially (serverless surrogate: admission-controller signature verification per d3fend-catalog) | NIST-800-53-CM-7(1), ISO-27001-2022-A.8.19 | tunable via policy update |
| D3-EHB    | Executable Hashbased Allowlist | Harden | per-process | verifies on exec | not deployed | yes (hash check at load time) | NIST-800-53-SA-12, SOC2-CC9.2 | tunable via hash list update |
| D3-SCP    | System Call Filtering | Isolate | per-process | verifies on syscall | partial | yes (seccomp profile applies in container runtime) | NIST-800-53-SC-39 | tunable via profile update |
| D3-PA     | Process Analysis | Detect | per-process | verifies on event | deployed | yes (EDR or eBPF) | NIST-800-53-SI-4 | tunable via rule update |
| ...       | ... | ... | ... | ... | ... | ... | ... | ... |

## Defense-in-depth summary
- Tactics populated: <count> of 7 (Model / Harden / Detect / Isolate / Deceive / Evict / Restore).
- Tactics with at least one deployed control: <count>.
- Under-defended tactics: <list — tactics with zero deployed controls>.
- Verdict: <defended at depth N | under-defended at depth N — needs M more tactics populated>.

## Least-privilege summary
- Per-process controls: <list + deployment status>.
- Per-segment controls: <list + deployment status>.
- Per-request controls: <list + deployment status>.
- Blanket controls: <list — note these are baselines, not substitutes for finer-grained controls>.

## Zero-trust summary
- Controls that verify per request: <list>.
- Controls that verify on session: <list>.
- Controls that assume implicit trust: <list — these are pre-zero-trust and must be paired with continuous verification or replaced>.

## Compliance-theater overlap
For each D3FEND ID surfaced, the framework controls the audit will claim as coverage and the lag-note from data/d3fend-catalog.json describing the grain mismatch. Example: "CM-7(1) covers least functionality, but accepts inventory-only implementations; D3-EAL requires runtime blocking — claim is paper-compliant only."

## Gaps and proposed remediation
1. <Specific deployment gap, e.g. "Deploy D3-EHB hash-pinning for MCP server binaries — currently not deployed; closes Detect-only coverage of T1195.001">.
2. <Specific scope gap, e.g. "D3-NI is deployed at perimeter; add D3-NTA on internal segments to convert implicit-trust to verifies-per-request">.
3. <Specific catalog gap, e.g. "AML.T0xxx has no D3FEND coverage in catalog — route to zeroday-gap-learn to add a defensive entry">.

## Global jurisdiction angle
EU: <which NIS2 / DORA / EU AI Act / EU CRA articles intersect the framework_controls_partially_mapped>.
UK: <NCSC CAF objective + Cyber Essentials Plus relevance>.
AU: <Essential 8 strategy + ISM control + APRA CPS 234 trigger if regulated>.
ISO 27001:2022: <Annex A control IDs from framework_controls_partially_mapped>.
US (for context): <NIST 800-53 control IDs + NIST CSF 2.0 function + NIST AI RMF function if AI-related>.

## Routed to
Primary: <this skill produced the map; no further routing required unless a gap was surfaced>.
For deployment gaps: skills/security-maturity-tiers — sequence the missing D3FEND IDs across MVP / Practical / Overkill tiers.
For catalog gaps: skills/zeroday-gap-learn — add the missing D3FEND entry to data/d3fend-catalog.json.
For ephemeral/serverless exception scope: skills/policy-exception-gen — document the architectural alternative.
For framework-grain escalation: skills/framework-gap-analysis — escalate the lag-note evidence.
```

The map fits on one or two pages depending on the number of D3FEND IDs surfaced. The "Defense-in-depth summary", "Least-privilege summary", and "Zero-trust summary" sections are mandatory — they are the explicit thread for the three foundational principles and must be visible in every report.

---

## Compliance Theater Check

The theater test for this skill is direct: the operator's defensive program is in theater if it can articulate attacker behavior at technique grain but cannot articulate its own defenses at the same grain.

> "For the top 10 ATT&CK techniques in your industry's threat intel for the last 90 days, list the D3FEND countermeasures deployed at each defense-in-depth layer (Harden, Detect, Isolate, Evict, Restore). For each D3FEND ID listed, state the privilege scope (per-process / per-segment / per-request / blanket) and the zero-trust posture (verifies-per-request / verifies-on-session / implicit-trust-on-segment). If the answer is 'we do not track at that level' or only one layer is named per technique, the defensive program is theater — the operator can describe attacks at technique grain but defends at framework-control grain, a category mismatch the audit cannot detect."

A second, complementary test:

> "Show your D3FEND coverage heatmap alongside your ATT&CK heatmap. If you have an ATT&CK heatmap (offensive coverage) but no D3FEND heatmap (defensive coverage at the same grain), your blue-team articulation is one-sided. The most common shape: ATT&CK heatmap exists, populated by EDR alerts; D3FEND heatmap does not exist; Harden, Isolate, Evict, and Restore tactics have no operator-known content. The org has bought defensive products and deployed framework controls, but cannot list which D3FEND technique each product implements. The framework controls are being treated as truth at a grain they do not address."

A third test, specific to AI-pipeline environments:

> "Pick any AI / LLM / RAG / MCP workload in your environment. List the D3FEND controls you would deploy on an on-prem monolith for the equivalent attack surface. Now, for each, state whether the control is architecturally possible in your ephemeral/serverless/AI pipeline runtime, and if not, what the explicit alternative is per `data/d3fend-catalog.json`'s `ai_pipeline_applicability` field. If the answer is 'the framework control exists, so we are covered', the program is in theater — the framework control is architecturally impossible in the workload's runtime and the alternative was never scoped. The audit passes; the workload is undefended."

An org that maintains a D3FEND coverage map alongside its ATT&CK heatmap, with explicit tactic-by-tactic deployment, scope and trust-posture annotations, and explicit ephemeral-environment alternatives, is not in theater. An org whose defensive articulation is "we have AC-3 and SI-4" without a technique-grain bridge to those controls is in theater for any RWEP-significant finding in its catalog — the program is paper-compliant, technique-blind.

---

## Defensive Countermeasure Mapping

This skill is itself the canonical mapper. The section name doubles as the section heading and as a recursive entry point: when another skill in the library needs to surface a defensive map for its finding, it routes here, and this skill produces the map by traversing the cross-walks enumerated below.

The cross-walks the skill maintains:

- **ATT&CK → D3FEND.** Sourced from the MITRE Center for Threat-Informed Defense ATT&CK Mappings NIST 800-53 → ATT&CK and D3FEND → ATT&CK crosswalks (latest crosswalk targets ATT&CK Enterprise v16.1; the live matrix is v19.1), materialized locally in `data/d3fend-catalog.json` as the `counters_attack_techniques` array on every D3FEND entry. To map an ATT&CK T-number to D3FEND, scan every catalog entry and collect those whose `counters_attack_techniques` includes the T-number. This skill never invents a mapping not present in the catalog; if a T-number has no coverage, the absence is a finding routed to `zeroday-gap-learn`.

- **ATLAS → D3FEND.** Sourced from cross-references in `data/atlas-ttps.json` (each ATLAS entry's defensive references) and from `data/d3fend-catalog.json` (each D3FEND entry's `counters_attack_techniques` array, which carries AML.T-numbers in addition to T-numbers). To map an AML.T technique to D3FEND, scan the catalog the same way as for ATT&CK. The bidirectional consistency is enforced by `lib/lint-skills.js` and by the schemas declared in the catalog `_meta` blocks.

- **CWE → D3FEND.** Sourced from root-cause mitigation chains in `data/cwe-catalog.json`. Each CWE entry links to one or more CVEs in `data/cve-catalog.json`; each CVE carries an `attack_refs` and `atlas_refs` array; the union of those refs is the technique set whose D3FEND coverage forms the CWE's defensive map. The chain is: CWE → CVE → ATT&CK/ATLAS → D3FEND. This skill walks the chain; the operator does not have to.

- **Framework controls → D3FEND.** Sourced from `framework_controls_partially_mapped` in `data/d3fend-catalog.json` and from `data/framework-control-gaps.json`. For a given framework control ID, the inverse lookup surfaces every D3FEND ID that nominally covers behavior the framework control claims — and via the catalog's `lag_notes`, the grain mismatch that makes the framework claim insufficient. This cross-walk is the most operator-facing one: it converts "we have CM-7" into "CM-7 nominally claims coverage of D3-EAL behavior, but the catalog's lag note records that auditors accept inventory-only CM-7 implementations, which is not D3-EAL — operationalize the runtime-blocking behavior or document the gap."

- **DLP / exfil → D3FEND.** Sourced from `data/dlp-controls.json`, whose entries carry a `d3fend_refs` field linking each DLP technique to the D3FEND countermeasures that detect or isolate the corresponding exfil pattern. The DLP catalog is the dedicated link for the Detect and Isolate tactics in data-loss scenarios.

When a new offensive technique is added to `data/atlas-ttps.json` or referenced in a new CVE in `data/cve-catalog.json`, the catalog steward must ensure at least one D3FEND entry covers it via `counters_attack_techniques`, or open a gap entry in `data/d3fend-catalog.json` (no orphaned controls — by inversion, no orphaned attack techniques). This skill is the consumer that surfaces the inversion failure if the catalog drifts.
