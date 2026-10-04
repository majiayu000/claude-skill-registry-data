---
name: container-runtime-security
version: "1.0.0"
description: Container + Kubernetes runtime security for mid-2026 — CIS K8s Benchmark, NSA/CISA Hardening, Pod Security Standards, Kyverno/Gatekeeper admission, Sigstore policy-controller, eBPF runtime detection (Falco/Tetragon), AI inference workload hardening
triggers:
  - container security
  - kubernetes security
  - k8s security
  - cis kubernetes
  - nsa hardening
  - pod security standards
  - kyverno
  - gatekeeper
  - opa
  - falco
  - tetragon
  - sigstore policy
  - admission controller
  - networkpolicy
  - cilium
  - kserve
  - vllm
data_deps:
  - cve-catalog.json
  - cwe-catalog.json
  - d3fend-catalog.json
  - framework-control-gaps.json
atlas_refs:
  - AML.T0010
attack_refs:
  - T1610
  - T1611
  - T1068
  - T1190
framework_gaps:
  - NIST-800-53-CM-7
  - ISO-27001-2022-A.8.28
  - SLSA-v1.0-Build-L3
  - NIS2-Art21-incident-handling
  - UK-CAF-B2
  - AU-Essential-8-App-Hardening
rfc_refs:
  - RFC-8446
  - RFC-8032
cwe_refs:
  - CWE-269
  - CWE-732
  - CWE-1188
  - CWE-787
  - CWE-1395
d3fend_refs:
  - D3-EAL
  - D3-EHB
  - D3-PSEP
  - D3-NI
  - D3-NTPM
  - D3-IOPR
forward_watch:
  - Pwn2Own Berlin 2026 (disclosed 2026-05-14, embargo ends 2026-08-12) — NVIDIA Container Toolkit container escape ($50K award) by chompie / IBM X-Force XOR; high-severity container/hypervisor boundary break; track patch and KEV add post-embargo
last_threat_review: "2026-09-28"
---

# Container + Kubernetes Runtime Security (mid-2026)

## Threat Context (mid-2026)

Kubernetes is no longer "the cloud-native orchestrator." It is the AI inference runtime. KServe, vLLM, Triton Inference Server, Ray Serve, Seldon, BentoML, and the Hugging Face TGI / text-generation-inference family all ship as K8s workloads. Anywhere there is a production LLM endpoint in mid-2026 there is a K8s cluster underneath it, and the cluster's hardening posture is the LLM endpoint's hardening posture.

The dominant attack class is container escape (ATT&CK T1611). Two vectors drive it:

- **Kernel LPEs as container-escape primitives.** Copy Fail (CVE-2026-31431) is the canonical mid-2026 example: any unprivileged container on a Linux 4.14+ host that has not been live-patched is a kernel-LPE-driven host takeover. Hand off the host-level kernel triage to `kernel-lpe-triage`; the container-side reality is that namespace + seccomp + capability drops do not stop an in-kernel write primitive once the syscall surface is reachable, and most clusters do not deploy a syscall-restricting profile beyond the broken default. Earlier-era container-runtime CVEs (runc CVE-2024-21626 "LeakyVessels," containerd CVE-2024-21626 family, CRI-O CVE-2024-3154 class) remain instructive even where patched — they established that "the runtime is the perimeter" is wrong and that the host kernel is the perimeter.
- **Misconfigured admission and RBAC.** Privileged pods, `hostPID`, `hostNetwork`, mounted Docker sockets, wildcard ClusterRoles, and ServiceAccounts with `create`/`patch` on `pods` or `secrets` collapse the cluster to a single-node compromise. Tooling like Peirates, kube-hunter, and the offensive use of kube-bench results enumerates these in minutes.

The Pod Security Standards (Privileged / Baseline / Restricted) replaced PodSecurityPolicy in K8s 1.25 (PSP removed) and are enforced by the built-in PSA admission controller. The unhappy reality across the install base in mid-2026: PSS-Restricted is the documented target, PSS-Baseline is the typical actual posture, and a non-trivial fraction of production namespaces run effectively Privileged because operators namespace-label `pod-security.kubernetes.io/enforce: privileged` to unblock a vendor Helm chart and never roll it back.

Admission policy is the next layer. Kyverno (CNCF Incubating, in wide enterprise use by 2026) and OPA Gatekeeper are the dominant policy engines; both gate pod creation against declarative rules. Mature programs use admission policy to verify image signatures via Sigstore policy-controller (CNCF Sandbox, with the `policy.sigstore.dev/v1beta1 ClusterImagePolicy` CRD) — only signed images from approved publisher identities are admitted. Hand off the upstream signing pipeline to `supply-chain-integrity`; the container-runtime concern is admission-time verification, not build-time signing.

Runtime detection catches what admission misses. Falco (CNCF Graduated, libbpf-based by default in 2026 with the kernel-module fallback deprecated) and Tetragon (CNCF Sandbox, Isovalent, eBPF-only) are the canonical eBPF detection stacks. They observe syscalls, network flows, and process-exec events at kernel speed and emit policy-driven alerts (Falco) or in-kernel preventive enforcement (Tetragon's TracingPolicy CRD with `Sigkill` action). The NSA/CISA Kubernetes Hardening Guide v1.2 (August 2022) is still the de facto US baseline as of mid-2026 — no v1.3 has shipped — and treats runtime detection as a defense-in-depth pillar.

NetworkPolicy is the default-deny lateral-movement control. Stock NetworkPolicy is L3/L4 only; Cilium NetworkPolicy and CiliumClusterwideNetworkPolicy (eBPF datapath, CNCF Graduated 2023) add L7 (HTTP method, gRPC service, Kafka topic, DNS FQDN) and identity-aware policy via SPIFFE identities. Service mesh (Istio, Linkerd, Cilium Service Mesh) supplies mTLS between workloads by default. Without a default-deny NetworkPolicy posture per namespace, "zero trust between pods" is a slide.

The AI-inference-workload wrinkle. KServe `InferenceService` and vLLM deployments typically run as privileged-adjacent pods: GPU device plugins require host device access (`/dev/nvidia*`), model weights are mounted from PVCs or hostPath, and the model server itself loads code-executing serialization formats (PyTorch `.pt`, Python's native serialization) unless the pipeline enforces safetensors. A compromise of the inference pod yields not just an RCE foothold but model-weight exfiltration, training-data leak (via inference-time embedding extraction), and a privileged GPU container that bypasses most generic container hardening guidance. The CIS Kubernetes Benchmark v1.10 (early 2025) does not specifically cover AI inference workload patterns; NIST 800-190 (Application Container Security, September 2017) predates the AI workload class entirely.

State of standards baselines:

- **CIS Kubernetes Benchmark v1.10** (covering K8s 1.30–1.31) — current as of mid-2026. CIS lags upstream K8s by 1–2 minor releases; v1.11 expected to cover K8s 1.32+.
- **NSA/CISA Kubernetes Hardening Guide v1.2** (August 2022) — still the latest revision; voluntary; widely cited in US federal and CI sectors.
- **NIST 800-190** (September 2017) — superseded by reality on every page; NIST has not yet published a 2nd revision. Forward-watch.
- **OWASP Kubernetes Top 10** (2022, refreshed 2024) — the offensive-perspective companion to CIS.
- **Pod Security Standards** — built-in (`kubernetes.io/pod-security`), three levels, enforced via PSA admission.

## Framework Lag Declaration

| Framework | Control | Designed For | Fails Because |
|---|---|---|---|
| CIS Kubernetes Benchmark v1.10 | Master/worker/policy/managed-services controls | K8s 1.30–1.31 hardened baseline | Lags upstream K8s by 1–2 minor releases. Treats every cluster identically — no carve-out for AI inference workloads needing GPU device plugins, hostPath model PVCs, or large-memory huge-page configurations. Compliance-tool output (kube-bench) is interpreted as "the security posture" instead of "one input to the posture." |
| NSA/CISA Kubernetes Hardening Guide v1.2 (Aug 2022) | Pod security, network separation, authentication/authorization, audit logging, threat detection, upgrades | US federal + CI baseline | Voluntary. Predates Pod Security Standards going GA (K8s 1.25, Aug 2022 — only just). Predates the AI-inference-as-K8s-workload pattern entirely. No update through mid-2026; treats Falco/eBPF detection as "consider" rather than baseline. |
| NIST 800-190 Application Container Security | Container image, registry, orchestrator, host OS, container runtime risks and countermeasures | 2017-era container baseline (Docker-era) | Predates Pod Security Standards, Kyverno/Gatekeeper, Sigstore, eBPF runtime detection, and the AI inference workload class. No revision through 2026. Auditors still cite it because it is the most concrete NIST container document — that is the gap. |
| OWASP Kubernetes Top 10 (2022, refresh 2024) | Top-10 misconfigurations and attack patterns | Offensive-perspective awareness | Awareness document, not a controls catalog. K01 Insecure Workload Configurations and K02 Supply Chain Vulnerabilities map cleanly but stop short of admission-policy and runtime-detection prescription. |
| Pod Security Standards (Privileged / Baseline / Restricted) | Built-in PSA admission controller policy levels | K8s 1.25+ pod-level security profile | PSS is namespace-scoped via labels (`pod-security.kubernetes.io/enforce`). Privileged-namespace overrides are silent in audit unless explicit reporting layers (Kyverno PolicyReports, Kubescape) surface them. PSS does not cover network, RBAC, image-signing, or runtime — it is one of six required layers. |
| NIST 800-53 Rev 5 CM-7 (Least Functionality) | Configuration-management baseline | Method-neutral configuration hardening | Method-neutral on K8s entirely. CM-7 is satisfied by "we disabled unused features"; no requirement that Pod Security Standards Restricted be the namespace default. See `data/framework-control-gaps.json` `NIST-800-53-CM-7`. |
| ISO 27001:2022 A.8.28 (Secure coding) | Annex A 2022 refresh | Generic ISMS secure-coding control | Method-neutral. Does not address container image hardening, admission policy, or runtime detection. ISO 27002:2022 implementation guidance is high-level. See `data/framework-control-gaps.json` `ISO-27001-2022-A.8.28`. |
| SLSA v1.0 Build L3 | Hardened-builder provenance | Build-pipeline integrity | SLSA L3 attests how the image was built — not whether it is verified at admission. SLSA L3 evidence with no `ClusterImagePolicy` enforcement on the cluster is build-side theater. Hand off the build side to `supply-chain-integrity`. See `data/framework-control-gaps.json` `SLSA-v1.0-Build-L3`. |
| EU NIS2 Directive Art. 21 | Risk management measures for essential/important entities | EU-wide cybersecurity baseline | "Appropriate technical and organisational measures." Member-State authorities (ENISA NIS Cooperation Group guidance) increasingly cite CIS Benchmarks and NSA/CISA Hardening Guide as the operational floor; the Directive itself does not. |
| EU CRA (Regulation 2024/2847) | Annex I essential cybersecurity requirements for products with digital elements | Products placed on EU market | OT-style application to brownfield K8s distros (Red Hat OpenShift, SUSE Rancher, VMware Tanzu, Mirantis k0s) is in scope; managed services (EKS, GKE, AKS) are typically out of scope as services. Implementing acts through Dec 2027 may tighten container-runtime expectations. |
| UK NCSC CAF v3.2 (2024) | Cyber Assessment Framework outcomes (B2 Identity, B4 System Security, B5 Resilient Networks) | UK CNI outcome-focused assessment | Outcome-focused; sound principles but no K8s-specific operational floor. B2.b "technical configuration" maps to CIS K8s Benchmark in practice without naming it. |
| AU ISM (Sep 2024 update) | Control 1739 (containers) and Application Control (E8 ML2/ML3) | AU government and CI baseline | ISM 1739 references container hardening at high level; does not pin CIS K8s Benchmark version or PSS profile. E8 Application Control closest analogue is Kyverno verify-images + Sigstore policy-controller, not named in ISM. |
| JP NISC Container Security Guidance | NISC critical-infrastructure container guidelines | JP CI sectors | Sector-level policy; defers operational specifics to METI guidance. AI inference workload patterns not yet codified. |
| IL INCD Container Hardening | INCD national directive on container security | IL CI operators | OT-style application; AI inference workloads in K8s not yet codified. |
| SG GovTech Cloud-Native Standards | TRM container baseline + MAS TRM cloud guidance | SG public-sector + financial-sector cloud | Strong on managed-service usage; admission policy and eBPF runtime detection not yet pinned. |
| TW CSMA + FSC Cloud Guidance | National critical-infrastructure cyber + financial-sector cloud | TW CII operators | CSMA Art. 14 supplier-risk obligations apply to K8s distro vendors; technical container floor not pinned. |
| US FedRAMP Rev 5 + DoD SRG IL2/IL4/IL5 | Federal cloud authorization baseline + DoD impact-level baselines | Federal cloud workloads | FedRAMP Rev 5 inherits NIST 800-53 CM-7 / SI-7. CIS Kubernetes Benchmark is increasingly expected as ATO evidence but not mandated in Rev 5 baseline text. DoD SRG IL5 in practice requires CIS K8s Benchmark + STIG. |
| ISO 27001:2022 + ISO/IEC 27017 (cloud) | A.8.28, A.8.9 + cloud sector extension | Cloud-service ISMS | Method-neutral; cloud-sector extension predates K8s-native admission policy. |

**Cross-jurisdiction posture (global-first, not US-centric):** Any container/K8s assessment for a multi-jurisdiction operator must cite at minimum EU NIS2 + CRA, UK NCSC CAF, AU ISM, IL INCD, SG GovTech/MAS TRM, alongside ISO 27001:2022 + ISO/IEC 27017 and NIST 800-53 CM-7. US-only is insufficient.

---

## TTP Mapping

| Surface | TTP | Matrix | Variant in mid-2026 | Gap Flag |
|---|---|---|---|---|
| Adversary deploys a workload (malicious container image, attacker-pushed Helm chart, compromised CI deploy pipeline) | T1610 — Deploy Container | ATT&CK Enterprise | Typosquatted public image (`docker.io/libray/...`), compromised public Helm chart, AI-coding-assistant-emitted manifest with `:latest` tag from untrusted registry | NIST 800-53 CM-7 is method-neutral on image-source allowlisting; PSS does not gate image source; admission policy via Kyverno + Sigstore policy-controller is the actual control and is not mandated by any framework |
| Container escape to host | T1611 — Escape to Host | ATT&CK Enterprise | Kernel LPE (Copy Fail CVE-2026-31431, Dirty Frag CVE-2026-43284 family); historical runc CVE-2024-21626 LeakyVessels family; cgroup v1 release_agent legacy abuses; abuse of overly permissive capabilities (`CAP_SYS_ADMIN`, `CAP_SYS_MODULE`) | NIST 800-190 predates kernel-LPE-as-container-escape as the dominant vector. Defense requires kernel patching cadence (hand off to `kernel-lpe-triage`) plus seccomp default profile, capability drops, read-only rootfs, and runtime detection. None of these are framework-mandated. |
| Privilege escalation within the container | T1068 — Exploitation for Privilege Escalation | ATT&CK Enterprise | In-container kernel LPE (yields host root via T1611 chain); abuse of writable hostPath; abuse of mounted Docker socket | Method-neutral framework controls; the actual control is seccomp + dropped capabilities + read-only rootfs + non-root runAsUser, all enforced by PSS-Restricted profile |
| Exploit public-facing K8s component | T1190 — Exploit Public-Facing Application | ATT&CK Enterprise | Exposed kube-apiserver (rare but seen on self-managed clusters); exposed kubelet read-only port (10255) or read/write port (10250) without authentication; exposed Kubernetes Dashboard with no auth; exposed Argo CD or Jenkins on the cluster; ingress controller CVEs (ingress-nginx CVE-2025 family) | NSA/CISA Hardening Guide v1.2 addresses control-plane exposure; managed services close this by default; self-managed clusters in CI/government still expose these |
| Compromised container image at a public/private registry | AML.T0010 — AI Supply Chain Compromise (umbrella) | ATLAS v2026.09 | Poisoned base image; backdoored model-serving image; typosquatted MCP server in a sidecar; AI-pipeline-specific (KServe / vLLM / Triton image with embedded malicious payload) | ATLAS classifies; no framework mandates signature verification at admission. Hand off the build-side provenance to `supply-chain-integrity`; the container-runtime control is `ClusterImagePolicy` enforcement |

ATT&CK Containers matrix (sub-matrix, since 2021) and ATT&CK for Kubernetes (Microsoft's threat matrix, 2020, since absorbed conceptually into ATT&CK Containers) are both relevant prior art. The Enterprise IDs above are canonical in ATLAS v2026.09 alignment and pass the linter regex `^T\d{4}(\.\d{3})?$`.

CWE cross-walk (see `data/cwe-catalog.json`):

| CWE | Why It Maps |
|---|---|
| CWE-269 (Improper Privilege Management) | Privileged pods, hostPID/hostNetwork/hostIPC, mounted Docker sockets, wildcard ClusterRoles, ServiceAccount with `create/patch` on `pods` or `secrets`. PSS-Restricted closes most pod-level instances; RBAC review closes the cluster-level instances. |
| CWE-732 (Incorrect Permission Assignment for Critical Resource) | `runAsUser: 0`, world-writable mounts, hostPath mounted read-write, secret mounted with overly broad mode bits, ServiceAccount tokens auto-mounted by default. |
| CWE-1188 (Initialization of a Resource with an Insecure Default) | K8s ships with auto-mount of ServiceAccount tokens on by default; PSS namespace label default is none; NetworkPolicy default is allow-all. Every cluster begins insecure until the operator inverts these defaults. |
| CWE-787 (Out-of-bounds Write) | Kernel LPE class that drives container escape (Copy Fail CVE-2026-31431). The container is not the boundary; the kernel is. |
| CWE-1395 (Dependency on Vulnerable Third-Party Component) | Base-image transitive vulnerabilities; vendor Helm chart pinned to a version with known CVEs; cluster components (CNI plugin, CSI driver, ingress controller, admission webhooks) with known CVEs. SBOM + VEX is the discovery layer; admission policy enforcing image signing + version pinning is the prevention layer. |

---

## Exploit Availability Matrix

| Class / CVE | CVSS | RWEP | CISA KEV | PoC Public | AI-Discovered | Active Exploitation | Patch / Mitigation | Admission-Detectable | Runtime-Detectable (Falco/Tetragon) |
|---|---|---|---|---|---|---|---|---|---|
| Host-kernel LPE as container escape — Copy Fail (CVE-2026-31431) | 7.8 | 90 (see `cve-catalog.json`) | Yes (2026-05-01, due 2026-05-15) | Yes — 732-byte script | Yes | Confirmed | Kernel patch + live-patch (kpatch/livepatch/kGraft) on supported distros; reboot rolling fleet on others | No (admission doesn't see kernel ops) | Yes — Falco/Tetragon catches the post-escape host operations; the in-kernel write itself is invisible to eBPF |
| Container-runtime CVE class — runc CVE-2024-21626 ("LeakyVessels") family | 8.6 | 35 (see `cve-catalog.json`) | No | Yes | No (manual disclosure) | Patched in modern fleets; brownfield self-managed clusters lag | runc / containerd / CRI-O upgrade | Partial — admission can require minimum runtime versions via node-feature labels | Yes — Tetragon can enforce SIGKILL on the abuse syscall sequence |
| Misconfigured PSS — `pod-security.kubernetes.io/enforce: privileged` on a workload namespace | n/a (class) | n/a | n/a | Trivial — `kubectl run --privileged` | Operator misconfig + AI-coding-assistant template drift | Routinely observed in incident response 2024–2026 | Set namespace label to `restricted`; remediate the workload | Yes — Kyverno PolicyReport + Kubescape surface this; PSA itself enforces on admit if label set |
| Misconfigured RBAC — ServiceAccount with `create/patch` on `pods` or `secrets` cluster-wide | n/a (class) | n/a | n/a | Trivial — `can-i --list --as=system:serviceaccount:...` | Operator misconfig | Routinely observed | Replace wildcard ClusterRoles with scoped Roles; deny `automountServiceAccountToken: true` by default | Yes — Kyverno + OPA policies; kube-bench check | Yes — Falco detects token use from unexpected ServiceAccount |
| Exposed kubelet 10250 / 10255 | n/a (class) | n/a | n/a | Trivial — Shodan / Censys queries; Peirates | n/a | Confirmed in self-managed / CI / lab clusters | Network policy default-deny; kubelet authentication + authorization; firewall | No (network-layer control) | Yes — Cilium L7 policy + Falco network rule |
| Ingress controller CVE class — ingress-nginx (recent CVE-2025 family, "IngressNightmare"-style) | varies | varies | Mixed KEV listings | Yes (multiple) | Mixed (some AI-assisted RE) | Confirmed | Vendor patch; remove ingress-nginx admission webhook if not in use; restrict snippet annotations | Partial — admission policy can forbid the dangerous annotations | Yes — Tetragon process-exec detection |
| Unsigned container image admitted to production | n/a (class) | n/a | n/a | n/a | n/a | Pervasive — default cluster posture | Sigstore policy-controller `ClusterImagePolicy` requiring keyless verification against pinned publisher identity; Kyverno `verifyImages` rule | Yes — that is the entire point | n/a |
| AI-inference image with code-executing model load (PyTorch `.pt` / Python-native serialization) | n/a (class) | n/a | n/a | Trivial — published PoC research | Yes — adversarial-weights research and 2025 incident reports | Suspected in advanced campaigns | Reject code-executing serialization formats; require safetensors; verify model signature pre-load | Partial — admission policy on the model-PVC contents | Yes — Falco rule on unexpected serialization-load syscalls from inference container |

**Honest gap statement (no fabricated CVE data).** `data/cve-catalog.json` does not yet enumerate every ingress-controller, CNI plugin, CSI driver, or admission webhook CVE. The authoritative feeds are upstream advisories (`kubernetes.io/security/`, `kubernetes-announce@googlegroups.com`, vendor PSIRT feeds for managed services, ingress-nginx CHANGELOG, Cilium security advisories). Forward-watch covers ingestion of these feeds.

---

## Analysis Procedure

This procedure threads the three foundational principles (defense in depth, least privilege, zero trust) through every step. Containers are the canonical ephemeral runtime — and the audit/forensic implication is that this is the operating reality the program must design for, not work around.

### Defense in depth

Six layers, each independently capable of blocking a different attacker stage. A program with five of six is still better than a program with one strong layer; a program with one strong layer plus heroic effort is fragile.

- **Image signing and provenance.** Sigstore cosign keyless signing of every image at build time (hand off to `supply-chain-integrity`). Rekor inclusion verified.
- **Admission control.** Sigstore policy-controller `ClusterImagePolicy` + Kyverno `verifyImages` rule + Kyverno / OPA Gatekeeper constraints enforcing no-root, no-host-network, no-hostPID, no-hostIPC, no-privileged, no-CAP_SYS_ADMIN, no-mountedDockerSocket, no-`:latest`-tag, allowlisted registries only.
- **Pod Security Standards Restricted profile** enforced by built-in PSA admission controller at the namespace level (`pod-security.kubernetes.io/enforce: restricted`).
- **NetworkPolicy default-deny per namespace.** Cilium L7 policy where flow control needs HTTP-method / gRPC-service / DNS-FQDN granularity. mTLS via service mesh (Istio, Linkerd, Cilium Service Mesh) for service-to-service identity.
- **Runtime detection (eBPF).** Falco (CNCF Graduated) syscall + network + process-exec rules feeding a SIEM; Tetragon (CNCF Sandbox) TracingPolicy CRDs with `Sigkill` action for in-kernel preventive enforcement on selected high-confidence signatures.
- **Control-plane hardening.** kube-apiserver audit-log level `RequestResponse` for sensitive resources, log shipped to a SIEM out-of-cluster, audit retention per regulator. etcd encryption-at-rest with KMS-backed key. RBAC review every quarter. kubelet TLS bootstrap rotation. Anonymous auth disabled.

### Least privilege

- Every pod: non-root (`runAsNonRoot: true`, `runAsUser: 10000+`), all capabilities dropped (`drop: ["ALL"]`) with explicit `add:` list only where required, read-only root filesystem, `allowPrivilegeEscalation: false`, seccomp `RuntimeDefault` profile minimum, `automountServiceAccountToken: false` unless required.
- ServiceAccounts scoped per workload, never shared across unrelated workloads. ClusterRoles avoided where Roles suffice. No `*` verbs.
- RBAC verbs scoped per resource per namespace. `secrets` access on a separate ServiceAccount from `pods` access.
- AI inference workloads: scoped GPU access (NVIDIA device plugin with per-pod GPU allocation, no shared GPU containers across security boundaries); model PVCs mounted read-only; model-registry credentials in CSI Secret Store (External Secrets Operator + AWS Secrets Manager / GCP Secret Manager / Azure Key Vault / HashiCorp Vault), not in-cluster Secret resources.
- Cluster-admin is a break-glass identity, not a daily-driver account; just-in-time elevation via SPIFFE + OIDC + audit log; standing cluster-admin tokens are a finding.

### Zero trust

- Never assume the pod network is trustworthy because it sits inside the cluster CNI. NetworkPolicy default-deny at every namespace; explicit allow rules for every required flow.
- Every service-to-service call mutually authenticated (mTLS via service mesh or SPIFFE/SPIRE identities). Cilium identity-aware policy where the mesh sidecar overhead is unacceptable.
- kubelet TLS bootstrap rotation enforced (`RotateKubeletServerCertificate`, `RotateKubeletClientCertificate`).
- Every image untrusted until signature verified at admission against a pinned publisher identity. Verify the signature, not just its presence — bare `.sig` files without identity binding are decoration.
- Every kernel syscall from a container subject to seccomp default-deny outside the allowed set. Capability drops are a syscall-level zero-trust posture.
- AI inference outputs treated as untrusted content (hand off to `ai-attack-surface` and `rag-pipeline-security` for the downstream content layer).

### Step-by-step procedure

1. **CIS Kubernetes Benchmark baseline scan.** Run `kube-bench` (Aqua) on every cluster — control plane, worker, policy, managed-services sections per the cluster's distribution. Record pass/fail per check ID. Schedule weekly minimum, daily for high-impact clusters. Quarterly is theater (see Compliance Theater Check 1).

2. **Pod Security Standards enforcement audit.** Enumerate every namespace's `pod-security.kubernetes.io/enforce` label and `audit`/`warn` labels. Goal state: `enforce: restricted` on every workload namespace; `baseline` only for documented exceptions (vendor Helm chart requirements, GPU device plugin pods) with a written exception per the `policy-exception-gen` skill. `privileged` is a finding unless it is `kube-system` or a documented infrastructure namespace.

3. **Image-signing rollout.** Deploy Sigstore policy-controller (`policy.sigstore.dev/v1beta1 ClusterImagePolicy`). Define per-namespace policies pinning publisher OIDC identity (Fulcio certificate subject) and OIDC issuer. Migrate workloads from "any image, any tag" to "signed images from approved publishers, version-pinned digest references." Track coverage % per namespace. Hand off the build-side signing pipeline to `supply-chain-integrity`.

4. **Admission policy via Kyverno or OPA Gatekeeper.** Deploy at least the following ClusterPolicy / ConstraintTemplate rules:
   - `disallow-privileged-containers`
   - `disallow-host-namespaces` (hostPID, hostNetwork, hostIPC)
   - `disallow-host-path`
   - `disallow-host-ports`
   - `disallow-capabilities` (no `add` of `SYS_ADMIN`, `NET_ADMIN`, `SYS_MODULE`, `SYS_PTRACE`, `DAC_OVERRIDE`)
   - `require-non-root`
   - `require-read-only-root-fs`
   - `require-image-signature` (Kyverno `verifyImages` with Sigstore key/identity)
   - `disallow-default-namespace`
   - `restrict-image-registries` (allowlist)
   - `disallow-latest-tag`
   - `require-resource-limits`
   - `require-pod-disruption-budget` (production namespaces)
   Run Kyverno PolicyReports against the live cluster; non-compliance becomes the remediation backlog.

5. **NetworkPolicy default-deny per namespace.** Apply a default-deny `NetworkPolicy` (ingress + egress) to every namespace. Explicit allow rules per workload. Cilium L7 policy where HTTP / gRPC / DNS granularity is required. Validate with `cilium connectivity test` or equivalent.

6. **Runtime detection deployment.** Deploy Falco (libbpf driver) cluster-wide as DaemonSet. Ship alerts to SIEM (Splunk HEC, Elastic, Sumo Logic, Panther). Tune the default ruleset; add custom rules for AI inference workloads (Python-native serialization-load syscalls, `torch.load` from network paths, unexpected GPU library loads). Deploy Tetragon for selected high-confidence preventive policies (`Sigkill` on `/proc/self/exe` overwrite, on cgroup release_agent abuse, on container-runtime CVE syscall sequences). Track MTTR per alert class.

7. **Control plane hardening.** Audit kube-apiserver flags: anonymous-auth disabled, audit-log level `RequestResponse` for `pods`/`secrets`/`configmaps`/`serviceaccounts`/`roles`/`rolebindings`, audit-log shipped out of cluster, audit-log retention per regulator (NERC CIP 90 days, NIS2 indefinite, DORA 5 years). etcd encryption-at-rest with KMS provider. RBAC review: enumerate every ClusterRoleBinding to `cluster-admin`, every wildcard verb, every wildcard resource. Justify or remove. Kubelet authn + authz enabled (webhook mode, not always-allow).

8. **AI inference workload hardening.** For each `InferenceService` (KServe), `VLLMDeployment` (vLLM), `Triton` deployment, `RayService`, `BentoDeployment`:
   - Pod runs PSS Restricted with documented GPU-device-plugin exception.
   - Model PVC mounted read-only.
   - Model serialization format: safetensors (preferred) or GGUF; reject `.pt` / Python-native code-executing formats in admission policy (Kyverno rule on init-container model fetcher).
   - Model signature verified against pinned publisher identity before load (cosign or OpenSSF model-signing).
   - Model-registry credentials via External Secrets Operator from out-of-cluster KMS; never in `Secret` resource.
   - NetworkPolicy: egress to model registry + observability sink only; no general internet egress; ingress from API gateway only.
   - Inference-time content treated as untrusted (`ai-attack-surface` / `rag-pipeline-security` hand-offs apply).

9. **Kernel patching cadence (hand off to `kernel-lpe-triage`).** For every node OS (Ubuntu, RHEL, Bottlerocket, Talos, Flatcar, AKS Mariner, EKS AL2023, GKE COS), maintain a kernel-patch SLA. Copy Fail (CVE-2026-31431) — live-patch within 4 hours on supported distros; rolling node reboot within 7 days on unsupported. Bottlerocket / Talos / Flatcar deliver kernel updates via image swap, not in-place — operational pattern is node-pool rolling replace.

10. **Supply chain hand-off (`supply-chain-integrity`).** Every image in the admission allowlist must trace to a SLSA L3 build with cosign signature, Rekor inclusion proof, and SBOM. The container-runtime job is to enforce verification at admission; the build-side job is to produce the evidence.

### Ephemeral / audit-forensic posture

Containers are ephemeral by design: pods die, nodes are replaced, log file paths inside the container are gone the moment the pod is. The audit/forensic implication:

- **All audit data must leave the host before the host can be lost.** kube-apiserver audit log, container stdout/stderr, Falco/Tetragon events, kube-bench scan results, Kyverno PolicyReports — all shipped to an out-of-cluster sink (SIEM, object storage with WORM lock) within seconds, not on a scheduled cron.
- **Forensic disk acquisition is rarely meaningful for a container.** The relevant artifact is the image, the pod manifest at admission time, the audit log of operations performed by the pod, and the Falco/Tetragon event stream — not a disk image of an ephemeral container layer. IR playbooks must reflect this: snapshot the pod manifest, snapshot the image digest, pull the event window, isolate the node (cordon + drain + freeze instead of shutdown so the kernel + memory remain available for `crash` / live forensics if needed).
- **NERC CIP and NIS2 retention requirements still apply** to the out-of-cluster log sink; in-cluster log volumes are not the system of record.
- **AI inference workloads compound the challenge** — model weights at inference time may be loaded from object storage and only ever exist in pod memory; capturing them post-incident requires either a memory snapshot of the live pod or the registry pull record. Plan for both.

---

## Output Format

The skill produces a Container + Kubernetes Runtime Security Posture Assessment covering per-cluster CIS Kubernetes Benchmark coverage, NSA / CISA Kubernetes Hardening Guide alignment, admission-control (Kyverno / OPA / Gatekeeper) policy maturity, runtime detection (Falco / Tetragon) coverage, sandboxing (gVisor / Kata) deployment, and the prioritized remediation roadmap. The shape below is consumed downstream by `cloud-security` (for the cloud-tier IAM and KMS dependencies), by `supply-chain-integrity` (for image provenance), and by `compliance-theater` (which compares deployed admission-control coverage against PCI / FedRAMP claims). Preserve the per-cluster benchmark-coverage rows verbatim — they are the auditable evidence chain.

Produce this structure verbatim:

```
## Container + Kubernetes Runtime Security Posture Assessment

**Assessment Date:** YYYY-MM-DD
**Cluster(s) in scope:** [cluster name + K8s version + distribution (EKS / GKE / AKS / OpenShift / Rancher / k0s / Talos / kubeadm) + node OS]
**Workload classes in scope:** [general microservices / AI inference (KServe / vLLM / Triton / Ray Serve) / data / batch]
**Regulatory jurisdictions:** [US / EU NIS2+CRA / UK NCSC CAF / AU ISM / IL INCD / SG GovTech / TW CSMA / sector-specific]

### CIS Kubernetes Benchmark Scorecard
| Section | Total Checks | Pass | Fail | Manual | Last Scan Date |
|---------|--------------|------|------|--------|----------------|
| Master Node Configuration | ... | ... | ... | ... | ... |
| Worker Node Configuration | ... | ... | ... | ... | ... |
| Policies | ... | ... | ... | ... | ... |
| Managed Services | ... | ... | ... | ... | ... |

### Pod Security Standards Adoption Matrix
| Namespace | enforce | audit | warn | Workload Class | Exception Justified? |

### Admission Policy Coverage
| Policy Engine | Kyverno / OPA Gatekeeper | # ClusterPolicies | # Workload Exceptions | Blocking vs. Audit Mode |
| Rule | Status (enforce / audit / absent) | Coverage % | Workload Exceptions |

### Image-Signing Coverage
| Namespace | Images Admitted (count) | Cosign-Verified % | ClusterImagePolicy Identity Pinned? | Rekor Inclusion Verified? |

### NetworkPolicy Coverage per Namespace
| Namespace | Default-Deny Ingress? | Default-Deny Egress? | L7 Policy (Cilium)? | mTLS (Mesh)? |

### Runtime Detection Posture
| Tool (Falco / Tetragon) | Driver (libbpf / kmod / ko) | Ruleset Version | Custom Rules # | SIEM Sink | Alert Volume / day | MTTR (median) |

### Control-Plane Hardening Checklist
| Control | Status | Evidence |
| anonymous-auth disabled | ... | ... |
| audit-log level RequestResponse for sensitive resources | ... | ... |
| audit-log shipped out-of-cluster within seconds | ... | ... |
| etcd encryption-at-rest with KMS | ... | ... |
| kubelet authn/authz webhook mode | ... | ... |
| no standing cluster-admin tokens | ... | ... |
| RBAC reviewed within last 90 days | ... | ... |

### AI Inference Workload Posture
| InferenceService / Deployment | PSS Profile | Model Format (safetensors / pt / native-codec / GGUF / ONNX) | Signature Verified at Load? | GPU Access Scope | Egress Policy | NetworkPolicy Ingress |

### Compliance Theater Findings
[Outcome of the four tests in the Compliance Theater Check section]

### Defensive Countermeasure Plan (D3FEND)
[D3-NI, D3-NTPM, D3-EAL, D3-EHB, D3-PSEP, D3-IOPR — concrete control placements by cluster layer]

### Priority Remediation Actions
1. ...
2. ...
3. ...

### RWEP-Prioritised CVE Exposure
[Host-kernel + container-runtime + ingress-controller + admission-webhook CVEs ranked by RWEP, not CVSS; see `exploit-scoring` skill for recalculation]
```

---

## Compliance Theater Check

Run all four. Any "fail" is a theater finding documented with the evidence (or absence thereof).

**Theater Test 1 — CIS Kubernetes Benchmark scan currency.**
Ask: *"Show me the kube-bench output from this week, signed by a CI workflow run, with diffs against last week's run highlighting any newly failing checks."*

- If the answer is "we ran kube-bench at go-live two years ago": CIS conformance evidence is fabricated.
- If the answer is "we run it quarterly": theater for a workload class where new CVEs and policy drift land weekly.
- If the answer is "we run it weekly but no one looks at the diff": theater for the gap-closure intent.
- Acceptable: weekly automated run, diffs reviewed, newly-failing checks ticketed within 24h.

**Theater Test 2 — Pod Security Standards Restricted coverage.**
Ask: *"What percentage of your production-workload namespaces enforce `pod-security.kubernetes.io/enforce: restricted`? For namespaces at `baseline` or `privileged`, paste the documented exception."*

- If the answer is "0%" or "we don't track": PSS adoption is theater regardless of how the documentation describes the target.
- If the answer is a non-zero number but every exception traces to "vendor Helm chart required it": the documented exceptions are theater for the security review intent — the vendor relationship is a finding, not a justification.
- Acceptable: at least 80% of workload namespaces at `restricted`, every exception traces to a signed `policy-exception-gen` record with compensating controls listed.

**Theater Test 3 — Image-signing verification at admission.**
Ask: *"For your last 10 production container deploys, paste the Sigstore policy-controller ClusterImagePolicy that verified them, paste the cosign / Rekor verification record, and identify the OIDC identity that signed."*

- If the answer is "we sign images in CI but don't verify on the cluster": the signature is decoration. CVE-2026-30615-class supply-chain compromise is not blocked by build-side signing alone. See `supply-chain-integrity` Compliance Theater Test 2 for the matched build-side test.
- If the answer is "we verify but accept any signed image": identity-pinning is missing; any compromised CI workflow that produces a Sigstore signature gets in.
- Acceptable: ClusterImagePolicy pinned to specific OIDC identity + issuer; verification logs reviewable; admission denied for unsigned or wrongly-signed images.

**Theater Test 4 — Container-escape tabletop / IR readiness.**
Ask: *"Show me the most recent tabletop exercise where the scenario was a kernel-LPE-driven container escape on a production cluster. What was the detection MTTD, what was the kernel-patch / node-replace MTTR, what was the audit-evidence preservation procedure?"*

- If the answer is "we have a generic IR playbook": theater. Container-escape IR has specific moves (cordon-not-shutdown, snapshot the pod manifest and image digest before terminating, preserve eBPF event window) that a generic playbook will not cover.
- If the answer is "we don't run container-specific tabletops": exposure to T1611 is unmanaged regardless of the patch posture.
- If the answer is "we tested but the IR team had no kubectl access to the production cluster during the exercise": the playbook is theater because the responders cannot execute it.
- Acceptable: container-escape-specific tabletop within the last 12 months, MTTD under 1h on the test scenario, post-exercise tickets closed.

---

## Defensive Countermeasure Mapping

Maps container/K8s findings to MITRE D3FEND IDs from `data/d3fend-catalog.json`, with explicit defense-in-depth layer position, least-privilege scope, zero-trust posture, and AI-pipeline applicability (controls impossible in serverless / ephemeral contexts name an explicit scoped alternative).

| D3FEND ID | Technique | Cluster Layer Position | Least-Privilege Scope | Zero-Trust Posture | AI-Pipeline Applicability |
|---|---|---|---|---|---|
| D3-EAL | Executable Allowlisting | Admission control (Sigstore policy-controller `ClusterImagePolicy` + Kyverno `verifyImages`) as the cluster-layer analogue to host-OS allowlisting; secondary at the host OS layer for node-image hardening | Per-namespace ClusterImagePolicy pinning OIDC identity + issuer; per-workload allowlist where vendor images carry distinct identities | Default-deny on unsigned images at admission; verify identity + Rekor inclusion, not signature presence | Highly applicable. KServe / vLLM / Triton images go through the same admission gate; AI-inference vendor images (NVIDIA NGC, Hugging Face TGI) must carry the same signature evidence. The ephemeral nature of pods means D3-EAL is the most reliable layer — once a pod is admitted, the host-layer EAL is largely moot for the container's lifetime. |
| D3-EHB | Executable Hash-based Allowlist | Image digest pinning (`image: registry/repo@sha256:...`) at admission; model-weight SHA-256 pinning at pre-load for AI inference | Per-workload digest pin; model-weight digest pin per `InferenceService` | Tag references (`:latest`, `:v1`) are not zero-trust — digest references are. Admission policy can enforce `image: ...@sha256:...` only. | Highly applicable. Model-weight hash verification before load is the AI-inference analogue. Hand off model-weight signing pipeline to `supply-chain-integrity`. |
| D3-PSEP | Process Segment Execution Prevention | Pod-spec `seccompProfile: RuntimeDefault` minimum, `Localhost` with a custom restrictive profile for high-risk workloads; `readOnlyRootFilesystem: true`; `allowPrivilegeEscalation: false`; capability drops | Per-pod seccomp profile; per-pod capability set | Verify the syscall surface at runtime, not just declare the profile at admission. Tetragon TracingPolicy enforces in-kernel; Falco detects post-fact. | Applicable. AI inference workloads need a seccomp profile that accommodates GPU device-plugin syscalls (CUDA, NVIDIA driver ioctls) while still restricting the broader attack surface. `RuntimeDefault` is often too restrictive; `Localhost` with a tuned profile is the production posture. |
| D3-NI | Network Isolation | NetworkPolicy at every namespace; CiliumNetworkPolicy where L7 needed; service mesh mTLS at the workload-identity layer | Per-namespace default-deny; explicit allow rules per workload-to-workload flow; identity-aware policy via SPIFFE | Conduit posture is default-deny; every flow verified per-identity per-protocol | Highly applicable. AI inference workloads need narrow egress (model registry + observability + inference-result sink only); broad internet egress from inference pods is a finding. Identity-aware policy (Cilium + SPIFFE) is the production posture for multi-tenant inference clusters. |
| D3-NTPM | Network Traffic Policy Mapping | Cilium L7 policy expression of allowed HTTP methods, gRPC services, DNS FQDNs, Kafka topics per workload | Per-workload allowlist of L7 endpoints | Continuous verification of conformance; deviation triggers alert | Highly applicable. AI inference egress should be policy-mapped to specific Hugging Face / vendor registry FQDNs; deviation indicates either model-pull misconfiguration or exfiltration. |
| D3-IOPR | Input / Output Process Profiling | Falco / Tetragon eBPF syscall + network + process-exec event stream; behavioral baselines per workload class | Per-workload behavioral profile; deviation alerts scoped to that workload's owner | Detection assumes the container is hostile until profile-conformant per-event | Highly applicable. AI inference workloads have a tight behavioral profile (CUDA syscalls, model-PVC reads, inference-result writes); unexpected serialization-load syscalls, `subprocess.Popen`, or `socket(AF_INET)` to non-registry endpoints is a high-confidence alert. The ephemeral nature of pods means baselines should be per-image-digest rather than per-pod-instance. |

**Ephemeral runtime posture (applied straight).** Containers are the canonical ephemeral runtime: pods die, nodes are replaced, in-pod logs are gone the moment the pod is. Controls that assume a long-lived host (host-based EDR signature DB updated weekly, on-host log retention, in-place patching) are architecturally mismatched. The container-realistic posture: admission policy as the primary preventive layer (D3-EAL, D3-EHB), eBPF runtime detection with out-of-cluster event sink as the primary detective layer (D3-IOPR), node-image swap (Bottlerocket, Talos, Flatcar) as the primary patching pattern, and all audit/forensic data leaving the host before the host can be lost. Recommendations that read "deploy host EDR with weekly signature updates" without specifying how that survives a node replacement are operationally indefensible.

---

## Hand-Off / Related Skills

After producing the container/K8s posture assessment, chain into the following skills.

- **`kernel-lpe-triage`** — for every Linux node OS in scope, score Copy Fail (CVE-2026-31431) and Dirty Frag (CVE-2026-43284 / -43500) exposure. Container escape is fundamentally a kernel problem; the cluster-layer controls are mitigations, not the closure. Live-patch-vs-node-replace decisions depend on node OS class (in-place patching on Ubuntu/RHEL; image-swap on Bottlerocket/Talos/Flatcar).
- **`supply-chain-integrity`** — for the build-side provenance, SLSA L3 evidence, Sigstore signing keys, in-toto attestations, SBOM, and ML-BOM for model weights. The container-runtime skill enforces verification at admission; supply-chain-integrity produces the evidence to verify.
- **`cloud-security`** *(if shipped — currently surfaced via sector skills and `framework-gap-analysis`)* — K8s typically runs on cloud IaaS or managed K8s (EKS, GKE, AKS). The control-plane managed-services section of CIS K8s Benchmark and the IAM-to-K8s-RBAC bridge (IRSA, Workload Identity, AAD Pod Identity) are cloud-specific. Until a dedicated cloud-security skill ships, use `sector-federal-government` for FedRAMP Rev 5 cloud baseline, `sector-financial` for MAS TRM / DORA cloud expectations, and `framework-gap-analysis` for ISO/IEC 27017 cloud-sector ISMS alignment.
- **`mlops-security`** *(if shipped — currently surfaced via `ai-attack-surface`, `ai-risk-management`, `rag-pipeline-security`)* — AI inference workloads in K8s require additional MLOps-specific controls (model registry governance, training-data lineage, model versioning, A/B inference routing security). Until a dedicated mlops-security skill ships, the AI Inference Workload Posture section of the output references the model-side controls and `ai-attack-surface` covers the inference-input attack surface.
- **`defensive-countermeasure-mapping`** — to deepen the D3FEND mapping above into a layered remediation plan rather than a single-control patch ticket; the container-realistic compensating-control programme typically combines all six D3FEND techniques above plus host-layer kernel patching.
- **`attack-surface-pentest`** — K8s in pen-test scope. Pen-test rules of engagement must spell out: cluster-admin access not granted by default (red team starts from a workload-level foothold), no DoS testing on control plane, presence of a cluster operator with stop-test authority, and explicit identification of AI inference services that are out of scope for adversarial-input testing (route that to `ai-attack-surface` testing instead).
- **`compliance-theater`** — to extend the four theater tests above with general-purpose theater detection on the operator's wider GRC posture.
- **`framework-gap-analysis`** — for any multi-jurisdiction operator, to produce the per-jurisdiction reconciliation called for in Analysis Procedure Step 10.
- **`global-grc`** — alongside framework-gap-analysis when EU NIS2 + CRA, UK NCSC CAF, AU ISM, JP NISC, IL INCD, SG GovTech, TW CSMA all apply.
- **`ai-attack-surface`** and **`mcp-agent-trust`** — when AI inference workloads (KServe / vLLM / Triton / Ray Serve) are in scope. ai-attack-surface for prompt-injection and model-input threats against the inference endpoint; mcp-agent-trust for the developer-side MCP servers that may be used to push manifests or operate the cluster.
- **`identity-assurance`** — for the cluster-admin / kubectl identity layer. Standing cluster-admin tokens are an identity-theater finding; SPIFFE + OIDC + just-in-time elevation is the production posture.
- **`policy-exception-gen`** — to generate defensible exceptions for namespaces where PSS Restricted is architecturally infeasible (GPU device plugin, vendor Helm chart requirements). The exception evidence is the documented compensating-control programme: Kyverno workload-specific policy, scoped NetworkPolicy, scoped RBAC, Falco/Tetragon rule coverage.

**Forward watch (per skill-format spec).** CIS Kubernetes Benchmark v1.11 (covering K8s 1.32+); NIST 800-190 r2 (long-overdue revision covering Pod Security Standards, admission policy, eBPF detection, AI inference workloads); NSA/CISA Kubernetes Hardening Guide v1.3 (no public draft as of 2026-05-11); OWASP Kubernetes Top 10 next revision; ingress-nginx CVE feed; Cilium / Falco / Tetragon security advisory feeds; KServe and vLLM security advisory ingestion into `data/cve-catalog.json`; Sigstore policy-controller GA and CRD stability (`policy.sigstore.dev` graduating from v1beta1 to v1).
