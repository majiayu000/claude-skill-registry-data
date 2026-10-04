---
name: infra-kit.workflow.audit
description: Review infrastructure-as-code, DevOps pipelines, and platform controls for security, reliability, compliance, and delivery hygiene using cloud well-architected baselines.
---

# Infrastructure Review & DevOps Auditor

Use this skill when the user wants a holistic infrastructure and DevOps audit that spans repositories, IaC directories, CI/CD workflows, runtime configurations, or platform guardrails. This skill combines lessons from AWS Well-Architected, Azure Well-Architected, Google Cloud Architecture Center/DORA guidance, and Google SRE practices.

## Outcomes

- Produce code-review style findings that cite the exact file/line, risk, and fix
- Check pipelines, IaC, and runtime manifests for least-privilege IAM and secure defaults
- Highlight OWASP Top 10 issues when pipelines or infrastructure touch application security controls (e.g., ingress, WAF, secrets flows)
- Validate that infrastructure aligns with cloud well-architected pillars: security, reliability, operational excellence, performance, cost, and sustainability
- Explain the DevOps maturity gaps (observability, release safety, incident response) with pragmatic next steps

## Where This Fits In The Flow

- Use near the end (pre-merge/release) as a cross-cutting quality gate.
- Use earlier when you need an initial baseline audit to inform `infra-kit.workflow` `plan.md` risk/mitigation sections.

## Workflow

1. Gather scope: repos or directories, environments, clouds, and compliance goals.
2. Pull the latest context locally: prefer `gh pr checkout <id>` for remote reviews so diffs match reality.
3. Map components to pillars:
   - Security/IAM, network, secrets
   - Reliability/SLOs, failover, chaos tests
   - Cost/efficiency (e.g., Spot usage, autoscaling)
   - Operational excellence (runbooks, incident hygiene)
4. Review IaC/manifest files first, then CI/CD workflows, then runtime policies.
5. Trace data, identity, and release paths end-to-end to uncover hidden privilege or compliance drift.
6. Evaluate application-facing controls with an OWASP Top 10 lens (injection, auth, secrets storage, logging, SSRF, etc.).
7. Classify each issue by severity, impact, and remediation. Reference the source framework (AWS/Azure/GCP/SRE/OWASP) when relevant.
8. Summarize open risks plus the validation commands or evidence collected.

## Hallucination Guardrails

- Tie every finding to the exact file, line, or command output inspected so audits stay rooted in real evidence instead of hypothetical configurations.
- Cite the specific framework (AWS Well-Architected pillar, Azure equivalent, Google SRE, OWASP) that backs guidance; do not invoke generic "best practice" without attribution.
- Call out missing data—repos, environments, credentials, runtime visibility—and either pause for clarification or mark the assumption rather than filling gaps with invented architecture details.
- List every tool or command that actually ran and explicitly state when something (tflint, checkov, kubeconform, etc.) could not execute so the user knows the review relied on static analysis.

## Authoring Rules

- Link every finding to a concrete location and show failing configuration snippets.
- Default IAM advice to least privilege across AWS IAM, GCP IAM, Kubernetes RBAC, GitHub permissions, and CI tokens.
- Prefer automated guardrails (policy-as-code, OPA, pre-commit, `pre-commit run --all-files`, `tflint`, `kubeconform`, `actionlint`) over manual review checklists.
- Require reproducible security controls for secrets (sealed secrets, Secret Manager, HashiCorp Vault) rather than inline credentials.
- Enforce strong supply-chain controls: pinned action SHAs, verified OCI/Helm signatures, artifact attestations where possible.
- Highlight OWASP Top 10 categories explicitly when findings map to them.
- Note cost levers such as Spot/preemptible GKE node pools for non-prod, autoscaler limits, and idle resource cleanup.

## Review Priorities

1. **Identity & Access**: orphaned admin roles, broad service accounts, missing workload identity bindings.
2. **Secrets & Supply Chain**: plaintext secrets, missing rotation, unsigned artifacts, unpinned actions/modules.
3. **Network & Data Protection**: open ingress, missing TLS, unrestricted egress, weak transit/storage encryption.
4. **Pipeline Safety**: missing required checks, lack of `concurrency`, env approvals, or artifact promotion steps.
5. **Reliability & Observability**: absent SLOs, no health checks, flaky rollouts without canaries, no incident process.
6. **Cost & Sustainability**: unused resources, oversized instances, no Spot/preemptible usage for test/non-prod, missing cleanup automation.
7. **OWASP Alignment**: SSRF risk via metadata exposure, broken auth/session handling, insecure deserialization, insufficient logging/monitoring, etc.

## Validation Loop

Use repo-specific tooling first. Otherwise consider:

```bash
terraform fmt -recursive && terraform validate
terragrunt hcl fmt && terragrunt validate
kubeconform -strict <rendered-manifests>
helm lint <chart>
actionlint .github/workflows/*.yml
gh workflow view <workflow>
pre-commit run --all-files
trivy config .
checkov -d .
``` 

When tooling cannot run (missing creds, network), explain what was skipped and rely on static inspection.

## Best-Practice References

- AWS Well-Architected Framework (security, reliability, performance, cost, sustainability)
- Azure Well-Architected Framework pillars
- Google Cloud Architecture Center DevOps/DORA technical capabilities
- Google SRE Book (SLOs, incident response, postmortems, automation)
- OWASP Top 10 (injection, auth failures, sensitive data exposure, SSRF, etc.)

## Delivery Standard

Always provide:

- Audit scope and assumptions
- Files or workflows reviewed and validation commands executed
- Findings grouped by severity with OWASP/WAF pillar references where applicable
- Actionable remediation steps and remaining risks if the user cannot implement certain changes immediately
