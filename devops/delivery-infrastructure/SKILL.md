---
name: delivery-infrastructure
description: "Design CI/CD, container topology, cloud or homelab deployment, migrations, telemetry, backups and rollback."
---

# Delivery and infrastructure
- Start with uptime, traffic, hosting policy, geography, data sensitivity, monthly budget and team on-call capacity.
- Compare single host/Docker Compose, managed PaaS, Kubernetes only where justifiable. Include network trust diagram and cost buckets.
- Specify Build→Tests→Scans→Artifact→Staging→Approval→Production→Smoke→Rollback pipeline.
- Cover multi-stage nonroot images, configuration/secrets, ingress/TLS, DNS, health probes, resource limits and graceful shutdown.
- Design safe DB migration (expand/contract) and actual backup/restore test. Reversible deploy plan mandatory.
- Instrument OpenTelemetry, correlation, dashboard, actionable alerts, tracing for queue/HTTP/SQL and operational runbooks.
- If homelab selected: Ansible provisioning + Jenkins CI/CD + Gitea control, optionally Cloudflare Tunnel/Access and WireGuard; protect private endpoints.
- Do not execute changes to cloud/prod/CI secrets/migrations without approval; plan and diff first.
- Reference `knowledge/DEVOPS_INFRA.md`.
