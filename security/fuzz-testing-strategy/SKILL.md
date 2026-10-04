---
name: fuzz-testing-strategy
version: "1.0.0"
description: Continuous fuzzing as a security control — coverage-guided fuzz (AFL++/libFuzzer), AI-assisted fuzz, OSS-Fuzz integration, kernel fuzz (syzkaller), AI-API fuzz, integration into CI/CD as compliance evidence
triggers:
  - fuzz testing
  - fuzzing
  - oss-fuzz
  - syzkaller
  - libfuzzer
  - afl
  - coverage-guided fuzz
  - ai-assisted fuzz
  - continuous fuzz
  - prompt fuzz
  - api fuzz
data_deps:
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - zeroday-lessons.json
atlas_refs:
  - AML.T0043
attack_refs:
  - T1190
framework_gaps:
  - NIST-800-218-SSDF
  - NIST-800-115
  - OWASP-ASVS-v5.0-V14
rfc_refs: []
cwe_refs:
  - CWE-125
  - CWE-20
  - CWE-362
  - CWE-416
  - CWE-78
  - CWE-787
forward_watch:
  - NIST SP 800-218A (AI-specific SSDF practices) for any explicit fuzz requirement on model-serving stacks
  - OpenSSF Scorecard "fuzzing" check threshold evolution
  - syzkaller eBPF and io_uring surface expansion as new kernel attack surfaces ship
  - OSS-Fuzz-Gen / AI-assisted harness generation becoming the default expectation for OSS maintainers
d3fend_refs:
  - D3-EAL
  - D3-IOPR
  - D3-PSEP
last_threat_review: "2026-09-18"
discovery_mode: "standalone"  # operator-reached via `exceptd brief fuzz-testing-strategy` or `exceptd ask`; not chained into any playbook's direct.skill_chain by design
---

# Fuzz Testing Strategy

Continuous fuzzing is a security control, not a QA activity. This skill treats fuzz presence, coverage, and SDLC integration the same way patch management treats SI-2: as an operational requirement whose absence is a finding.

---

## Threat Context (mid-2026)

By mid-2026 the asymmetry between offensive and defensive fuzzing has flipped. The defender's question is no longer "should we fuzz?" — it is "are we fuzzing as fast as attackers are fuzzing us?"

- **AI-assisted fuzz campaigns produce real-world CVEs on weekly cadence.** Copy Fail (CVE-2026-31431, CVSS 7.8 / RWEP 90, CISA KEV) was discovered by an AI-system-driven fuzz campaign in approximately one hour against a kernel surface that humans had fuzzed for years (`data/cve-catalog.json`). The Linux page-cache copy-on-write path had been a syzkaller target since 2018. What broke was not the technique — it was the harness-generation cost. AI lifted that cost to near-zero.
- **AI harness generation is the new force multiplier.** Microsoft's AIM (AI-augmented fuzzing internal program), Google's OSS-Fuzz-Gen pipeline (LLM-generated harnesses scaled across the OSS-Fuzz corpus), and academic systems including TitanFuzz / Fuzz4All / WhiteFox produce semantically valid inputs and target-specific harnesses that classical coverage-guided fuzzers (AFL++/libFuzzer) cannot reach without expert authoring. The expert-authoring bottleneck was the single biggest gate on fuzz coverage for a decade. That gate is gone for attackers.
- **OSS-Fuzz is now table-stakes infrastructure, not a research curiosity.** OSS-Fuzz exceeded 1,000 onboarded projects in 2024 and has produced more than 10,000 reproducible bug reports across its lifetime. By 2026, OpenSSF Scorecard penalizes any C/C++/Rust dependency whose upstream is not enrolled in OSS-Fuzz or equivalent continuous fuzz infrastructure. Vendor risk assessments increasingly require evidence of upstream fuzz coverage.
- **Kernel and parser surfaces remain the highest-yield targets.** syzkaller has produced more than 5,000 Linux kernel bugs since 2016. By mid-2026 io_uring, eBPF verifier, and netfilter remain the top-yielding surfaces, with the page-cache subsystem newly added after Copy Fail. Userspace parsers (image, video, font, archive, protocol) continue to yield memory-safety CVEs at the rate of dozens per month across the OSS-Fuzz corpus.
- **AI / LLM surfaces are now first-class fuzz targets.** PromptBench (LLM input robustness), garak (vulnerability scanner for LLM systems), and NVIDIA NeMo Guardrails red-team harnesses run prompt-fuzz campaigns mapping to AML.T0043 (Craft Adversarial Data) and feed adversarial-input findings back into model serving stacks. By mid-2026 any production LLM-fronted application without continuous prompt fuzz is exposed to attacker-class adversarial generation.
- **The compliance gap is operational, not theoretical.** No framework requires fuzz as a control (see Framework Lag Declaration). The result: an org can be NIST 800-218 SSDF-compliant on paper while shipping parser code that has never been fuzzed. That gap is what this skill exists to surface.

---

## Framework Lag Declaration

| Framework | Control | What It Assumes | Why It Fails (mid-2026) |
|---|---|---|---|
| NIST SP 800-218 SSDF v1.1 | PW.7 (Review and/or Analyze Human-Readable Code), PW.8 (Test Executable Code to Identify Vulnerabilities) | "Use appropriate testing techniques" including fuzz is mentioned in informative references, not normative requirements | PW.8 lists fuzzing in NIST 800-53 mapping informatively. There is no normative requirement that fuzz harnesses exist, that they run continuously, or that uncovered code is treated as a finding. An org with zero fuzz harnesses can claim SSDF conformance. |
| NIST SP 800-115 (2008) | §4 Technical Assessment Techniques | Point-in-time penetration testing methodology written before coverage-guided fuzz was mainstream | Predates AFL (2013), libFuzzer (2015), OSS-Fuzz (2016), syzkaller (2015). No continuous-fuzz concept. No AI-assisted-harness concept. Treats fuzz as an optional technique alongside scanners. Cited by FedRAMP and DoD assessments where its absence of fuzz requirements becomes the auditable baseline. |
| NIST 800-53 Rev 5 | SA-11 (Developer Testing and Evaluation), SA-11(8) (Dynamic Code Analysis) | Developer "performs dynamic code analysis"; control enhancement (8) names fuzz as an example | Method-agnostic. A vendor running quarterly licensed-scanner runs against a staging URL can claim SA-11 conformance. No requirement for coverage-guided fuzz, no requirement for continuous operation, no requirement that uncovered branches be tracked. |
| OWASP ASVS v5.0 | V14 (Configuration), V10 (Coding) | Application security verification across configuration and malicious-code controls | Neither V14 nor V10 requires fuzz harnesses for parsers, deserializers, or IPC surfaces. ASVS L3 (highest) does not mandate continuous fuzz. An L3-verified app can ship a hand-written XML parser that has never been fuzzed. |
| PCI DSS 4.0 | 6.2 (custom software developed securely), 11.3 (vulnerability testing) | "Vulnerability testing" operationalized as authenticated and unauthenticated scans | PCI 6.2.4 lists "fuzz testing" as one of several "industry-accepted methods" of testing for "common software attacks" — but does not require it. An assessor will accept SAST + DAST + scanner output as conformance. No continuous-fuzz requirement, no coverage threshold. |
| ISO 27001:2022 | A.8.29 (Security testing in development and acceptance) | "Security testing processes shall be defined" — method-agnostic | The standard is deliberately method-agnostic. An org can document "we run a SAST scanner quarterly" and pass A.8.29 audit. No fuzz, no coverage measurement, no AI-augmented testing required. |
| EU NIS2 Directive | Art. 21(2)(e) — "policies and procedures to assess the effectiveness of cybersecurity risk-management measures" | Essential and important entities must test the effectiveness of their risk-management measures | "Test the effectiveness" is undefined at the technique level. National implementations (e.g., Germany BSI, Italy ACN) do not operationalize fuzz as a required measure. An entity can pass Art. 21 audit with scanner-only testing. |
| EU Cyber Resilience Act (CRA) | Annex I §1(2)(b), §2 | Products with digital elements must "deliver security updates" and be "designed, developed, produced to ensure an appropriate level of cybersecurity" | The CRA's "appropriate level" language has no technique floor. Annex I requires vulnerability testing but does not mandate fuzz. Conformance assessment under the harmonized standards (in draft as of mid-2026) is unlikely to mandate continuous fuzz before publication. |
| UK NCSC CAF (Cyber Assessment Framework) v3.2 | Principle B4 (System Security), Objective B4.b (Secure Configuration) | OES / RDP entities must "secure their networked systems and data" | CAF B4 is outcome-focused. No technique-level fuzz requirement. CAF Indicators of Good Practice (IGPs) mention "rigorous testing" without operationalizing fuzz. |
| Australia ASD Essential 8 | Application Control (ML1–ML3), Patch Applications (ML1–ML3) | Pre-execution control of binaries; rapid patching of known vulns | Essential 8 is post-disclosure. No pre-disclosure-via-fuzz requirement. The ASD ISM control 1235 (development) is method-agnostic, identical failure mode to ISO A.8.29. |
| EU AI Act | Art. 15 (Accuracy, robustness and cybersecurity for high-risk AI) | High-risk AI systems must "achieve an appropriate level of accuracy, robustness and cybersecurity" and be "resilient against attempts by unauthorised third parties to alter their use, outputs or performance" | Robustness is operationalized in the draft harmonized standards as "adversarial robustness testing" — but does not mandate continuous prompt-fuzz, does not name PromptBench / garak / equivalent, and provides no coverage metric. An obligor can ship an LLM-fronted product with zero adversarial-input fuzz and claim Art. 15 conformance via point-in-time red-team evidence. |

**Cross-framework conclusion:** No major framework (NIST, ISO, PCI, OWASP, NIS2, CRA, CAF, Essential 8, EU AI Act) mandates continuous fuzz as a required security control for products with parser, IPC, native-code, or LLM surfaces. Fuzz appears in informative references and example lists. The framework lag is uniform.

---

## TTP Mapping (MITRE ATLAS v2026.09 + MITRE ATT&CK Enterprise)

Fuzz is a pre-exploit control: it surfaces weaknesses before they leave the build pipeline. Mapping is via the weakness root cause (CWE) rather than the post-exploit technique.

| Surface | Pre-exploit TTP (what fuzz prevents) | Root CWE | Gap Flag |
|---|---|---|---|
| Native code parsers (image, archive, protocol, font) | T1190 (Exploit Public-Facing Application — prerequisite weakness class) | CWE-787 (Out-of-bounds Write), CWE-416 (Use After Free) | NIST 800-218 PW.8 informative-only; no normative requirement that parser code be fuzzed |
| Input validation across all external interfaces | T1190 (prerequisite) | CWE-20 (Improper Input Validation) | OWASP ASVS V5 (input validation) requires checks, not fuzz to verify checks survive adversarial input |
| Command construction in shells, exec wrappers, MCP tool surfaces | T1190 (prerequisite); pre-T1059 (Command and Scripting Interpreter) at trust boundaries | CWE-78 (OS Command Injection) | Static rules in SAST routinely miss runtime command construction; only fuzz with command-injection harnesses surfaces these |
| LLM-fronted application surfaces | AML.T0043 (Craft Adversarial Data) prerequisite — adversarial inputs surfaced before deployment | CWE-20 (Improper Input Validation on prompt-derived control flow) | EU AI Act Art. 15 robustness operationalization does not name adversarial-input fuzz; no NIST/ISO/PCI control covers prompt fuzz at all |
| Kernel system-call surface | T1068 (Exploitation for Privilege Escalation) prerequisite — kernel weaknesses surfaced before they ship | CWE-787, CWE-416 | No framework requires kernel-fuzz coverage as a precondition for shipping kernel-mode drivers or modules. syzkaller-equivalent coverage is industry good-practice, not control. |

**Why this mapping is conservative:** ATT&CK and ATLAS catalog post-exploit techniques. Fuzz is a pre-exploit control. The map shows the chain: fuzz-prevents-weakness → weakness-enables-TTP. Removing the weakness denies the TTP.

---

## Exploit Availability Matrix (Fuzz Tool Landscape)

Tools used by attackers and defenders alike. "AI-assistance" column reflects whether AI-augmented harness generation or input synthesis is available in the toolchain ecosystem as of mid-2026.

| Component Class | Tool(s) | Industry Maturity | Integration Cost (engineer-days) | AI-Assistance | Time-to-First-Crash (median, mature target) |
|---|---|---|---|---|---|
| Native code / library | AFL++, libFuzzer, honggfuzz | Production-grade since 2015 | 2–5 per harness | Yes (OSS-Fuzz-Gen, Fuzz4All for harness generation; TitanFuzz for inputs) | Minutes to hours on a fresh harness; days to weeks on a mature corpus |
| OSS C/C++/Rust/Go/Python projects | OSS-Fuzz (managed) | Operational since 2016, 1000+ projects | 3–7 for onboarding | Yes (OSS-Fuzz-Gen integration) | Hours to days |
| Linux kernel | syzkaller, kAFL, Healer | Operational since 2015 (syzkaller); 5000+ kernel bugs filed | 5–10 for cluster + descriptions | Limited (semantic syscall sequence generation is an open research area) | Hours on a new subsystem; weeks on hardened subsystems |
| Hypervisor / VMM | kAFL, Nyx, hAFL2 | Operational since 2019 | 10–20 (snapshotting + harness) | Limited | Days to weeks |
| HTTP / REST APIs | RESTler (Microsoft), Schemathesis, Boofuzz, ZAP fuzzer | Operational; OpenAPI-driven | 1–3 per service (with spec) | Yes (LLM-generated state-machine inference, parameter synthesis) | Minutes to hours |
| gRPC / Protobuf | Boofuzz with protobuf harness, custom libFuzzer harnesses | Solid but bespoke | 3–7 per service | Yes (harness generation from .proto) | Hours |
| GraphQL | clairvoyance + custom fuzz, InQL fuzzer | Maturing | 2–5 per schema | Yes (LLM-generated query mutation) | Hours |
| Parsers (general — XML/JSON/YAML/protobuf/binary formats) | Peach Fuzzer (peach3), AFL++ with format-aware mutators | Mature | 1–3 per format | Yes (grammar inference) | Hours to days |
| LLM prompts and AI APIs | garak, PromptBench, NeMo Guardrails red-team toolkit, PyRIT (Microsoft) | Maturing rapidly since 2024 | 1–3 per model surface | Yes (this is the AI-vs-AI loop — adversarial generators target the model) | Minutes to hours per attack class |
| Smart contracts | Echidna, Foundry fuzz, Medusa | Mature in Ethereum ecosystem | 1–3 per contract | Limited | Hours |

**Industry maturity for compliance evidence:** OSS-Fuzz, syzkaller, AFL++, libFuzzer, and RESTler are all production-grade. An org that cannot point to which of these (or equivalent) is running against its parser / IPC / API / kernel-mode surfaces has not deployed continuous fuzz as a control regardless of what its SSDF self-assessment claims.

---

## Analysis Procedure

Continuous fuzz must be threaded through the three foundational security principles. Single-layer fuzz (e.g., "we fuzz the public API") is brittle by construction.

### Foundational principles

**Defense in depth — fuzz at multiple layers.**
- Unit-level harnesses for each parser entry point (libFuzzer-style, one harness per format / message type)
- Integration-level fuzz for IPC and serialization boundaries (cross-process, cross-language)
- Differential fuzz between two implementations of the same protocol (find divergences that indicate at least one bug)
- Protocol-level fuzz for external API surfaces (RESTler/Schemathesis state-aware)
- AI-prompt fuzz for any LLM-fronted application surface (garak/PromptBench/PyRIT)
- Reliance on any single layer is brittle: parser-only fuzz misses IPC-level type confusion; API-only fuzz misses parser bugs reachable behind authentication.

**Least privilege — fuzz with the lowest privilege available.**
- A fuzzer running as root finds different bugs than one running as a sandboxed unprivileged user. Run both.
- Crash-reproduction must happen under the actual production privilege profile (container UID, seccomp profile, capability set). A crash that requires CAP_SYS_ADMIN is a different finding from one that does not.
- For kernel fuzz: run unprivileged-user syscall fuzz separately from privileged-user fuzz; both are needed.

**Zero trust — every external interface is hostile by construction.**
- Threat model output → fuzz target list. Every trust boundary identified during threat modeling is an explicit fuzz target.
- Internal interfaces previously presumed safe (intra-VPC, intra-pod, sidecar IPC) are explicit fuzz targets after zero-trust adoption — the network presumption is no longer compensating.
- Authenticated endpoints get fuzzed with valid credentials and with credential mutations both.

### Step-by-step procedure

**Step 1 — Inventory all fuzz-eligible interfaces.**
Pull from the threat model and code inventory:
- Every parser / deserializer (image, video, font, archive, protocol, document, config)
- Every IPC surface (gRPC, REST, GraphQL, message queues, shared memory)
- Every native-code library boundary called from a higher-level language (FFI / cgo / JNI / PyO3)
- Every kernel module or kernel-mode driver shipped
- Every LLM-fronted endpoint
- Every state machine that consumes external input

**Step 2 — Classify each interface by fuzz approach.**
- Native code with deterministic input → libFuzzer / AFL++ unit harness
- OSS dependency → verify OSS-Fuzz enrollment; if absent, file an issue and add to vendor risk register
- HTTP/REST with OpenAPI spec → RESTler / Schemathesis
- HTTP/REST without spec → reverse-engineer spec, then Schemathesis; concurrently apply Boofuzz
- gRPC → libFuzzer harness over the protobuf entry point
- Kernel module → syzkaller description (syz_struct definitions) + cluster
- LLM endpoint → garak baseline pass + PromptBench / PyRIT for targeted attack classes
- Stateful protocol → Boofuzz or stateful AFL++ with corpus seeding

**Step 3 — Stand up continuous fuzz infrastructure.**
- OSS components → OSS-Fuzz enrollment (free for OSS; ClusterFuzzLite for self-hosted)
- Proprietary components → ClusterFuzzLite in GitHub Actions / GitLab CI / equivalent, or Mayhem / Code Intelligence as commercial alternatives
- Kernel components → syzkaller dashboard self-hosted with reproducer support
- LLM endpoints → garak in CI on every model serving update + scheduled deep campaigns

**Step 4 — Define crash-triage workflow.**
- Every crash → CWE classification on intake (memory safety, input validation, command injection, deserialization, etc.) using `data/cwe-catalog.json` as the controlled vocabulary
- Every crash → severity tag via RWEP factor pre-fill: is the crash reachable from an unauthenticated surface? Is the affected codepath in production? Does it survive ASLR / stack canaries / CFI? These pre-fill RWEP factors when the crash becomes a CVE
- Triage SLA: P0 (memory corruption on reachable unauthenticated surface) → 24h investigation; P1 (memory corruption gated by auth) → 72h; P2 (denial of service only) → 7 days
- Every triaged crash → either a code fix or a documented filter-not-fix decision (e.g., harness limitation, false positive due to test setup)

**Step 5 — CWE classification on every finding.**
Crash inventory categorized by CWE root cause. Track quarterly: are CWE-787 / CWE-416 findings trending down (memory-safety improvements landing) or up (new attack surface added)? Are CWE-78 findings appearing where none existed before (regression)?

**Step 6 — Run AI-augmented fuzz against high-priority targets.**
- OSS-Fuzz-Gen or equivalent LLM-driven harness generation against any parser surface with low corpus coverage
- Differential fuzz between server implementations (e.g., two TLS stacks, two JSON parsers) — AI-assisted divergence detection
- LLM-fronted endpoints → garak with model-specific probes plus PromptBench-style adversarial generation; PyRIT for orchestrated multi-turn attacks
- Track time-to-first-crash improvement vs. classical-only fuzz baseline; this is the AI-leverage measurement

**Step 7 — Surface uncovered code as a finding.**
- Coverage report per harness; merged coverage across all harnesses
- Code reachable from an external interface and not covered by any fuzz harness is a finding, not a metric. Open as a backlog item with the same severity as a missing unit test for security-critical code.
- This is the step that converts fuzz from "we run fuzz" theater into "we measure where fuzz fails to reach" honest posture.

**Step 8 — Integrate into CI/CD as a quality gate.**
- Pre-merge: every PR touching fuzz-eligible code triggers a fuzz job in CI on the relevant harness(es). Gate: zero new crashes for N CPU-hours (N defined per-target; typical: 30 minutes for parsers, 4 hours for kernel modules).
- Post-merge: continuous fuzz cluster runs against the main branch corpus, regression-tracking against the previous build.
- Release gate: no open P0 fuzz findings; all P1 findings have a documented disposition.

**Step 9 — Produce compliance evidence.**
For each shipping component, generate an artifact:
- Harness inventory (which interfaces have harnesses)
- Coverage measurement (line / branch / function coverage per harness)
- Continuous-fuzz uptime metric (CPU-hours fuzzed per release)
- Crash inventory by CWE class
- Time-to-fix metric per severity band

This artifact is what an auditor receives instead of a self-attestation that "we test for vulnerabilities."

**Step 10 — Feed fuzz outputs back into the zero-day learning loop.**
Internally discovered fuzz findings that map to a CWE class already in `data/cve-catalog.json` are evidence that the framework gap for that class is real. Append the finding to `data/zeroday-lessons.json` (attack vector → control that should have caught it → framework that covers the control → adequacy assessment → new control requirement). Internally found bugs close the loop just as well as external CVEs.

---

## Output Format

The skill produces a Fuzz Posture Assessment covering fuzz-eligible interface inventory, harness coverage, crash inventory, and quarter-over-quarter CWE-class trend. The shape below is consumed downstream by `zeroday-gap-learn` (which appends internally found crashes as lesson entries), by `compliance-theater` (which compares the harness-coverage gap against SAMM / BSIMM / SDL compliance claims), and by the SBOM evidence chain (which inherits the per-component fuzz-instrumentation status). Preserve the per-interface CI-gated field verbatim — it distinguishes deployed fuzzing from one-shot security-team exercises.

```
## Fuzz Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Component / Estate:** [scope]
**Assessor:** [role]

### Fuzz-Eligible Interface Inventory
| Interface | Class | Harness Present | Tool | CI-Gated | Last Run |
|---|---|---|---|---|---|
| [name] | parser/IPC/API/kernel/LLM | Yes/No | [AFL++/libFuzzer/syzkaller/RESTler/garak/...] | Yes/No | YYYY-MM-DD |

### Coverage Report
| Harness | Line Coverage | Branch Coverage | CPU-Hours / Release | Uncovered Reachable Code |
|---|---|---|---|---|
| [name] | [N]% | [N]% | [N] | [list of un-fuzzed reachable functions] |

### Crash Inventory (current release window)
| Crash ID | CWE | Severity | Surface | Status | Time to Triage | Time to Fix |
|---|---|---|---|---|---|---|
| [id] | [CWE-N] | P0/P1/P2 | [interface] | open/fixed/filtered | [duration] | [duration] |

### Quarter-over-Quarter Trend
| CWE Class | Last Q Count | This Q Count | Direction | Notes |
|---|---|---|---|---|
| CWE-787 (OOB Write) | N | N | up/down/flat | [explanation] |
| CWE-416 (UAF) | N | N | up/down/flat | [explanation] |
| CWE-20 (Input Validation) | N | N | up/down/flat | [explanation] |
| CWE-78 (Command Injection) | N | N | up/down/flat | [explanation] |

### Vulnerability Disclosure Intake (prioritized)
[Ranked list of fuzz-discovered findings with CWE class, RWEP factor pre-fill, owner, target-fix date]

### NIST 800-218 SSDF Evidence Mapping
| SSDF Practice | Fuzz Artifact Supplied |
|---|---|
| PW.7 (Code Review) | [coverage report by harness] |
| PW.8 (Test Executable Code) | [continuous-fuzz CPU-hours, crash inventory, time-to-fix metrics] |
| PW.9 (Configure Software to Have Secure Settings by Default) | [harnesses run with production seccomp/capability profile] |
| RV.1 (Identify and Confirm Vulnerabilities) | [crash triage workflow, CWE-classified inventory] |
| RV.2 (Assess, Prioritize, and Remediate) | [time-to-fix per severity, RWEP-fed prioritization] |

### Framework Gap Declaration
[Per-framework statement: which controls the org claims cover this domain, and where the absence of normative fuzz requirements creates a gap. Mandatory rows: NIST 800-218, NIST 800-115, NIST 800-53 SA-11, OWASP ASVS V14, PCI DSS 4.0 6.2, ISO 27001:2022 A.8.29, EU NIS2 Art. 21, EU CRA Annex I, UK CAF B4, ASD Essential 8 / ISM 1235, EU AI Act Art. 15 (if LLM in scope).]

### Theater Check Result
[See the Compliance Theater Check section — answer the four questions, record the gap]

### Defensive Countermeasure Mapping
| Fuzz Finding Class | D3FEND Countermeasure | Implementation |
|---|---|---|
| Memory-safety crashes (CWE-787, CWE-416) | D3-PSEP (Process Segment Execution Prevention) | DEP/NX enforced; W^X mappings verified |
| Command injection (CWE-78) | D3-EAL (Executable Allowlisting) | Production exec allowlist with no shell expansion paths |
| Adversarial AI input (AML.T0043) | D3-IOPR (Input/Output Profiling) | Prompt/response telemetry baseline + drift alerting on garak-discovered probe classes |

### RWEP Pre-Fill for Open Findings
[For each open fuzz finding likely to become a CVE: pre-filled RWEP factors per the exploit-scoring skill output format]
```

---

## Compliance Theater Check

Run these four questions against any organization claiming NIST 800-218 SSDF, ISO 27001:2022 A.8.29, PCI DSS 4.0 6.2, OWASP ASVS, or equivalent secure-development conformance:

> **Q1.** "Is fuzz a required pre-merge gate for every PR that touches parser, IPC, deserialization, or native-code path? Pull a PR from the last sprint that modified parser code and show me the CI run that includes a fuzz job and its exit criterion. If the gate does not exist, NIST 800-218 PW.8 conformance is paper — the practice is documented but not enforced at the integration point where it matters."

> **Q2.** "Are AI-augmented fuzz campaigns running against your high-priority targets (parsers, kernel modules if shipped, LLM endpoints if any)? Specifically, can you produce evidence of OSS-Fuzz-Gen / Fuzz4All / equivalent harness-generation output, or garak / PyRIT runs against LLM endpoints, within the current release window? If the answer is 'we run classical AFL++/libFuzzer with hand-written harnesses,' the org is fuzzing at the 2020 industry frontier while attackers fuzz at the 2026 frontier. The asymmetry is the finding."

> **Q3.** "Is time-to-fix measured on fuzz-discovered findings, broken out by CWE class and severity? Show the last quarter's metric. If the answer is 'we don't differentiate fuzz findings from other bug reports,' the org cannot demonstrate that fuzz is an effective control — there is no signal that fuzz output is acted on faster than scanner output, and the framework claim of 'we test for vulnerabilities' collapses to 'we file tickets we don't measure.'"

> **Q4.** "What is the merged coverage of all fuzz harnesses against the external attack surface? What reachable code is not covered by any harness? If the answer is 'we don't measure merged coverage' or 'we don't track uncovered reachable code as a finding,' the fuzz program optimizes for the existing harnesses (selection bias) and the framework gap (no normative requirement that uncovered code be a finding) is the operational gap."

**Theater answer pattern:** "We run fuzz on a quarterly basis. We have AFL running against our main parser. We don't have specific metrics."

**Real-posture answer pattern:** "Every PR touching parser, IPC, or native-code path triggers a per-harness fuzz job in CI; the gate is zero new crashes in 30 CPU-minutes for parsers, 4 CPU-hours for kernel modules. Merged branch coverage across harnesses is 78% of reachable external-surface code; the uncovered 22% is in the backlog at P1. AI-augmented harness generation runs nightly via OSS-Fuzz-Gen on internal repos. P0 fuzz findings have a 24-hour triage SLA with a 7-day median time-to-fix last quarter (CWE-787: 3 findings, all fixed; CWE-416: 1 finding, fixed). garak runs against the model-serving stack pre-deployment with a fixed probe set."

The gap between the two patterns is the size of the fuzz-as-control theater.

---

## Defensive Countermeasure Mapping

Fuzz output is most useful when it routes directly to a deployed countermeasure rather than only to a code fix. Map each fuzz finding class to a D3FEND defensive technique so the operational response includes both the source-level remediation and the runtime hardening that bounds the blast radius if the fix is delayed.

| Fuzz Finding Class | Root CWE | D3FEND Countermeasure | Why This Pairing | Implementation Note |
|---|---|---|---|---|
| Memory-safety: out-of-bounds write | CWE-787 | D3-PSEP (Process Segment Execution Prevention) | Even when the OOB write reaches an executable region, DEP/NX denies the resulting code from executing. D3-PSEP bounds the impact while the upstream fix lands. | Enforce W^X mappings, NX stack, NX heap; verify on every binary at release time |
| Memory-safety: use-after-free | CWE-416 | D3-PSEP | Heap UAF that achieves arbitrary write benefits from segment-execution prevention identically to OOB write. | Same as above; combine with hardened allocator (e.g., GWP-ASan, scudo) and ASLR (D3-ASLR available in `data/d3fend-catalog.json`). |
| Input validation failures with command-construction reachable paths | CWE-78 | D3-EAL (Executable Allowlisting) | Command injection succeeds when an attacker invokes an unexpected binary. D3-EAL constrains the runtime exec set so injected commands fail at the allowlist boundary even when the input validation regression ships. | Production exec allowlist; no shell-expansion paths in the trusted set; audit denied-exec events as high-severity. |
| Generic input validation failures | CWE-20 | D3-EAL (where the downstream effect is exec); D3-IOPR (where the effect is logical / data-plane) | Input validation issues with non-exec consequences need profile-based detection of out-of-bounds parameter usage. | Pair input validation fixes with a runtime profile of acceptable parameter shapes; alert on drift. |
| Adversarial AI inputs (prompt injection variants, jailbreaks) | CWE-20 (improper validation of prompt-derived control flow) | D3-IOPR (Input/Output Profiling) | Prompt-fuzz outputs (garak/PromptBench/PyRIT) produce a probe corpus. Profiling prompt-and-response telemetry against that corpus identifies the same attack class at runtime. | Maintain a probe corpus from continuous prompt fuzz; emit a telemetry signal when production traffic matches a probe class; integrate with the AI-attack-surface skill output. |

**Why this section exists:** A fuzz finding that produces only a source-level fix is half-deployed. The other half — the runtime control that limits exploitability of any latent variant or regression — is what makes fuzz a security control rather than a quality activity. Every fuzz finding closes with both halves.
