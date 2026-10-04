---
name: aqua
description: "Expert agent for Aqua Security platform. Covers full container lifecycle security — image scanning, KSPM, runtime protection with Aqua Enforcer, Dynamic Threat Analysis (DTA), vShield virtual patching, Trivy OSS integration, and Kubernetes-native deployment. WHEN: \"Aqua Security\", \"Aqua platform\", \"Aqua Enforcer\", \"Aqua image scanning\", \"vShield\", \"DTA\", \"Dynamic Threat Analysis\", \"Aqua KSPM\", \"Aqua runtime\", \"Aqua supply chain\", \"kube-bench Aqua\", \"Trivy Aqua\"."
license: MIT
---

# Aqua Security

This skill covers Aqua Security — a full lifecycle container and cloud-native security platform. Aqua covers the entire security lifecycle from developer workstation and CI/CD through production runtime, with a strong emphasis on Kubernetes-native deployment and open-source tooling (Trivy, kube-bench, kube-hunter).

## How to Approach Tasks

When you receive a request:

1. **Classify** the lifecycle phase:
   - **Build/CI** -- Image scanning with Trivy/Aqua Scanner, secrets detection, IaC scanning
   - **KSPM/Infrastructure** -- Kubernetes Security Posture Management, CIS benchmark, cluster hardening
   - **Runtime Protection** -- Aqua Enforcer deployment, runtime policies, drift prevention
   - **Virtual Patching (vShield)** -- Runtime protection for unpatched vulnerabilities
   - **Dynamic Threat Analysis (DTA)** -- Sandbox behavior analysis for unknown images
   - **Policy Management** -- Image assurance policies, runtime policies, admission control
   - **Supply Chain** -- Image signing, SBOM, provenance
   - **Compliance** -- CIS benchmarks, regulatory compliance reporting

2. **Identify environment** -- Kubernetes platform (EKS, AKS, GKE, self-managed)? Deployment scale? CI/CD platform? Aqua deployment model (SaaS or self-hosted)?

3. **Analyze** -- Apply Aqua-specific reasoning. Aqua's strength is the combination of developer-first open source tools (Trivy) with enterprise runtime protection (Enforcer + vShield + DTA).

4. **Recommend** -- Provide specific Aqua platform guidance with configuration examples.

## Aqua Platform Components

### Overview

Aqua Security provides end-to-end container lifecycle security:

```
Source Code                CI/CD Pipeline              Production Runtime
     │                          │                              │
Trivy/Checkov          Aqua Scanner + Trivy          Aqua Enforcer
(IaC + SCA)            (Image scanning,              (Runtime protection,
                         secrets, misconfigs)          drift prevention)
                               │                              │
                        Image Assurance Policy        Runtime Policy
                        (block/allow/warn)             (allow/alert/block)
                               │                              │
                        Aqua Console (unified visibility, policy management, compliance)
                               │
                        KSPM (Kubernetes Security Posture Management)
                        (kube-bench, CIS benchmark, config assessment)
```

### Aqua Console

Central management and visibility platform:
- SaaS or self-hosted (on Kubernetes)
- Aggregates all scan results, runtime events, and compliance data
- Policy management (image assurance, runtime, container firewall, host compliance)
- RBAC for multi-team environments
- API for programmatic access and SIEM/SOAR integration

### Trivy (Open Source Scanner)

Trivy is Aqua's open-source vulnerability scanner — the most widely adopted container scanner:

**Trivy scan targets:**
```bash
# Container image (local or remote)
trivy image python:3.11-slim

# Filesystem / source code directory
trivy fs /path/to/project

# Git repository
trivy repo https://github.com/myorg/myapp

# Kubernetes cluster
trivy k8s cluster --report summary

# Kubernetes specific namespace
trivy k8s --namespace production --report all

# Specific SBOM file
trivy sbom myapp-sbom.spdx.json
```

**Trivy scanner types (`--scanners` flag):**
- `vuln` — Vulnerability detection (CVEs) — default
- `secret` — Hardcoded secrets (API keys, passwords, tokens)
- `config` — Misconfigurations in Docker, Kubernetes, Terraform, CloudFormation
- `license` — License compliance
- `sbom` — SBOM generation

**Trivy vulnerability databases:**
- OS packages: GitHub Advisory Database + OS vendor advisories (Ubuntu USN, RedHat RHSAs, Alpine SecDB, etc.)
- Language packages: GitHub Advisory Database, PyPI, NPM, Maven, NuGet, Cargo, Go

**Trivy CI/CD integration:**
```yaml
# GitHub Actions: Scan and upload to GitHub Security tab
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH

- name: Upload Trivy scan results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: trivy-results.sarif
```

**Aqua Enterprise Scanner:**
Built on Trivy but adds:
- Policy enforcement (Image Assurance Policies)
- Results stored in Aqua Console with history
- Advanced secrets detection
- Malware detection
- DTA (Dynamic Threat Analysis) integration
- SLA tracking

### Image Assurance Policies

Aqua's policy framework for determining whether an image is allowed to run:

**Policy checks:**
- CVE severity thresholds (block on CRITICAL, warn on HIGH)
- CVE fix availability (block only if a fix is available)
- Sensitive data (secrets, PII) in the image
- Malware detected
- Base image age (block images older than X days)
- Root user check (block images running as root)
- Trusted base image (must be from approved base image list)
- Image registry (must be from approved registries only)
- Image signing (must have valid signature from trusted key)
- Custom compliance checks

**Policy enforcement actions:**
- `Warn` — Log the violation; allow deployment
- `Block` — Prevent deployment (CI/CD gate or admission controller)
- `Audit` — Allow but log all violations for review

```yaml
# Example Image Assurance Policy (via Aqua API or UI)
name: "Production Policy"
enforce: true
checks:
  - type: vulnerability
    value:
      maximum_severity: "high"         # block on CRITICAL, warn on HIGH
      only_fix_available: true         # only block if fix exists
  - type: sensitive_data
    value:
      block_malware: true
      block_credentials: true
  - type: trusted_base_images
    value:
      trusted_images:
        - "registry.company.com/base/*"
  - type: runs_as_root
    value:
      block: true                      # block images that run as root
```

## Aqua Enforcer (Runtime Agent)

### Architecture

The Aqua Enforcer is a DaemonSet (one pod per Kubernetes node) that provides:

**Kubernetes deployment:**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: aqua-agent
  namespace: aqua
spec:
  selector:
    matchLabels:
      app: aqua-agent
  template:
    spec:
      hostPID: true       # Required for process monitoring
      hostIPC: true       # Required for IPC monitoring
      serviceAccountName: aqua-sa
      containers:
      - name: aqua-agent
        image: registry.aquasec.com/enforcer:2024.x
        securityContext:
          privileged: true    # Required for kernel-level monitoring
        volumeMounts:
        - name: var-run
          mountPath: /var/run
        - name: sys
          mountPath: /sys
        - name: etc
          mountPath: /host/etc
          readOnly: true
```

**What the Enforcer monitors:**
- Process execution in all containers (using eBPF or kernel module)
- Network connections (outbound and inbound)
- File system access (reads/writes to sensitive paths)
- System calls (via seccomp integration)
- Container lifecycle (start/stop events)

### Runtime Policies

Runtime policies define what is allowed/blocked during container execution:

**Policy types:**

**Container Runtime Policy:**
```
Processes:
  - Allowed processes: ["python3", "gunicorn", "uvicorn"]  # allowlist
  - Block: shell execution (bash, sh, zsh, ksh)
  - Block: package manager execution (pip, apt, yum)

Network:
  - Outbound: allow to *.company.com, api.stripe.com
  - Block: outbound to known malicious IPs (TI feed)
  - Block: DNS for known malicious domains

File System:
  - Block writes to /usr, /bin, /sbin (OS binaries)
  - Read-only: /etc/passwd, /etc/shadow
  - Allow writes to /tmp, /var/log/app

System Calls:
  - Custom seccomp profile (or use Aqua's generated profile)

Volume Mounts:
  - Block: mounting /var/run/docker.sock
  - Block: hostPath mounts to sensitive paths
```

**Behavioral learning mode:**
Aqua Enforcer has a learning/monitoring mode that observes normal behavior and auto-generates allowlist policies:
1. Deploy Enforcer in `monitoring` mode
2. Run application through normal workflows (1-7 days recommended)
3. Aqua generates a suggested runtime policy based on observed behavior
4. Review and adjust the suggested policy
5. Switch to `enforce` mode

**Enforcement actions:**
- `Monitor` — Log events; do not block
- `Enforce (Block)` — Block violations and kill the container process
- `Alert` — Log and send alert; do not block

### Drift Prevention

Drift prevention is one of Aqua's most powerful runtime security capabilities:

**The problem:**
Containers are meant to be immutable — identical to the image they were built from. But attackers (and sometimes developers) may attempt to modify running containers (install tools, modify scripts, add backdoors).

**How drift detection works:**
1. At container start, Aqua creates a cryptographic baseline of the container filesystem (from the image)
2. During runtime, any modification to files that exist in the original image triggers a drift event
3. Any new file created in read-write locations (but outside designated writable paths) triggers drift

**Drift policy enforcement:**
```
Drift Prevention:
  - Block execution of new files not in the original image
  - Block modification of existing executable files
  - Exception: allow writes to /tmp, /var/log/app (expected writable paths)
```

**Impact:** An attacker who uploads a web shell or installs a new binary in the container will be blocked from executing it — even if the file successfully lands on the filesystem.

## vShield (Virtual Patching)

### Purpose

vShield provides runtime protection against specific vulnerabilities without applying the software patch:

**The problem vShield solves:**
A critical CVE (e.g., Log4Shell, Spring4Shell) is disclosed. Your container images contain the vulnerable library. The vendor patch is not yet available, or the patch cannot be applied immediately due to testing requirements. What do you do?

**How vShield works:**
- Aqua ships virtual patches for specific high-severity CVEs
- The patch is applied as a runtime rule in the Enforcer
- The rule blocks the exploitation technique for that specific CVE
- The underlying vulnerability remains (unfixed software) but cannot be exploited
- When the real patch is applied, the virtual patch is automatically removed

**vShield coverage:**
- High-profile CVEs with known exploitation techniques (Log4Shell, Spring4Shell, Shellshock, etc.)
- OS-level vulnerabilities with known exploitation patterns
- Container-specific vulnerabilities

**Key distinction from general runtime rules:**
vShield rules are CVE-specific — they are precisely crafted to block the specific exploitation technique for each CVE, minimizing false positives while maximizing protection.

### vShield vs. Just Fixing the Vulnerability

| Approach | Time to Protect | Residual Risk | Complexity |
|---|---|---|---|
| Apply software patch | Days to weeks (test + deploy) | Zero (vulnerability removed) | Medium |
| vShield + patch later | Hours (auto-deploy via policy) | Low (exploitation blocked, vuln present) | Low |
| Accept risk + monitor | Zero effort | Full CVE risk | Low |

vShield is a bridge — use it to buy time while the proper patch is prepared and tested.

## Dynamic Threat Analysis (DTA)

### Purpose

DTA is Aqua's sandbox capability — it dynamically executes unknown or suspicious container images in an isolated environment to detect behavioral threats that static scanning cannot find.

**Use cases:**
- Third-party images from public registries (Docker Hub, etc.) before allowing them into production
- Images that fail static scanning but have mitigating factors
- Unknown/obfuscated threats that evade signature-based detection
- Malware that is packed or encrypted and only reveals itself at runtime

### How DTA Works

1. Container image is submitted to DTA (manual or automatically via policy)
2. DTA runs the image in an isolated, instrumented sandbox environment
3. Sandbox monitors all runtime behavior: process execution, network calls, filesystem changes, syscalls
4. DTA analyzes behavior and generates a detailed threat report
5. Report includes: network connections made, files created/modified, processes spawned, suspicious indicators

**Behavioral indicators DTA detects:**
- Crypto mining (CPU usage pattern + network to mining pools)
- Backdoors (outbound C2 connections on unusual ports)
- Persistence mechanisms (cron job creation, init.d modifications)
- Data exfiltration (large outbound transfers, DNS exfiltration)
- Privilege escalation attempts
- Lateral movement patterns

### DTA Integration with Image Assurance

DTA can be set as a required check in Image Assurance Policies:
```
Image Assurance Policy (Critical Images):
  checks:
    - type: DTA
      value:
        block_on_severity: HIGH    # Block image if DTA finds high severity behavior
        timeout: 300               # Wait up to 5 minutes for DTA results
```

## Kubernetes Security Posture Management (KSPM)

Aqua KSPM assesses Kubernetes cluster configurations against security benchmarks:

**kube-bench (open source):**
```bash
# Run CIS Kubernetes Benchmark checks
kube-bench run --config-dir /etc/kube-bench/cfg --config /etc/kube-bench/cfg/config.yaml

# Run specific checks
kube-bench run --check 1.1.1,1.1.2,1.2.1

# Run for specific platform
kube-bench run --benchmark eks-1.4.0
kube-bench run --benchmark aks-1.0
kube-bench run --benchmark gke-1.2.0

# Output: JSON for integration
kube-bench run --json --outputfile kube-bench-results.json
```

**KSPM coverage in Aqua platform:**
- CIS Kubernetes Benchmark (all versions)
- CIS EKS, AKS, GKE Benchmarks
- NSA/CISA Kubernetes Hardening Guidance
- NIST 800-190 (Application Container Security Guide)
- Custom compliance checks

**Configuration assessments:**
- API server configuration (anonymous auth, audit logging, encryption)
- etcd security (TLS, authentication)
- Kubelet configuration (read-only port, anonymous auth)
- RBAC audit (overprivileged roles, cluster-admin usage)
- Network policy coverage
- Pod security configuration
- Secret management practices

## Supply Chain Security

**Image signing with cosign (Sigstore):**
Aqua integrates with Sigstore for supply chain security:
```bash
# Sign image after building and scanning
cosign sign --key cosign.key registry.company.com/myapp:v1.0.0

# Aqua Image Assurance Policy: require valid signature
checks:
  - type: image_signature
    value:
      require_signature: true
      trusted_keys:
        - name: "company-signing-key"
          public_key: "-----BEGIN PUBLIC KEY-----\n..."
```

**SBOM integration:**
```bash
# Generate SBOM with Trivy
trivy image --format cyclonedx --output sbom.json myapp:v1.0.0

# Upload SBOM to Aqua
aquasec scan --image myapp:v1.0.0 --sbom sbom.json
```

## Integration Patterns

### CI/CD Integration

```bash
# aquasec CLI in CI pipeline
aquasec scan --checkonly --registry registry.company.com \
  --image myapp:v1.0.0 \
  --registry-user $REGISTRY_USER \
  --registry-password $REGISTRY_PASS

# Exit code: 0 = pass, 1 = fail (block the build)
```

### SIEM Integration

Aqua forwards security events (image scan results, runtime violations, audit events) to:
- Splunk (Aqua Splunk app available on Splunkbase)
- Sumo Logic
- Elasticsearch
- Syslog (any SIEM with syslog input)
- Webhooks (generic SOAR integration)
- JIRA (ticketing for vulnerability findings)

### Kubernetes Admission Control

Aqua can enforce Image Assurance Policies as a Kubernetes admission controller:
```bash
# Deploy Aqua admission controller webhook
kubectl apply -f aqua-webhook.yaml

# All pod creation requests validated against Aqua Image Assurance Policy
# Pod creation blocked if image fails policy
```

## Reference Files

Load these when you need deep architectural knowledge:

- `references/architecture.md` -- Aqua platform architecture: Aqua Console deployment, Enforcer DaemonSet details, vShield implementation, DTA sandbox architecture, MicroEnforcer for VM/bare-metal, Aqua Gateway (relay between Enforcer and Console in restricted networks).
