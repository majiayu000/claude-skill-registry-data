---
name: gcp-pro
description: Google Cloud guidance — core services, IAM, VPC networking, GKE/Cloud Run choices, BigQuery, and cost control.
category: development
---

## Overview

Google Cloud Platform combines Google's infrastructure heritage (global networking, Kubernetes origins, BigQuery) with a developer-friendly service set. Its networking model is distinctive — a single global VPC rather than per-region networks — and its IAM, while powerful, has its own learning curve around hierarchy and organization policies.

GCP rewards understanding a few core ideas: projects as the isolation boundary, IAM's resource hierarchy, the global VPC, and choosing between GCE/GKE/Cloud Run/Cloud Functions for compute. This skill covers those fundamentals, the key services, and cost control.

## When to use

- Designing architecture on GCP (choosing services).
- Setting up IAM (hierarchy, roles, service accounts, least privilege).
- Building VPC networking (subnets, firewall rules, Private Google Access).
- Choosing compute (GCE, GKE, Cloud Run, Cloud Functions).
- Using BigQuery for analytics (modeling, partitioning, cost control).
- Controlling GCP costs (budgets, committed use, BigQuery slot pricing).
- Securing a GCP organization (baseline, auditing).

## Core concepts

- **Resource hierarchy.** Organization → folders → projects. Projects are the isolation and billing boundary — one per environment/team/service. IAM policies inherit downward; organization policies constrain what children can do.
- **IAM.** Members (users, groups, service accounts) get roles (predefined, custom) on resources. Prefer predefined roles, then custom roles with minimal permissions; avoid primitive roles (Owner/Editor) beyond break-glass. Service accounts are the workload identity — use them, not user credentials.
- **Service account impersonation.** Short-lived credentials via impersonation instead of downloadable keys. Keys that exist get leaked — design so they don't need to exist.
- **Global VPC.** One VPC spans all regions with regional subnets — no peering needed for cross-region traffic. Firewall rules (stateful, deny-by-default posture available) and hierarchical firewall policies for org-wide rules.
- **Private Google Access.** Reach Google APIs from private subnets without NAT — keeps traffic on Google's network and avoids NAT costs.
- **Compute choices.** GCE (VMs, full control), GKE (managed Kubernetes — Autopilot for hands-off, Standard for control), Cloud Run (serverless containers, scales to zero, the default for services), Cloud Functions (event-driven snippets). Cloud Run is the sweet spot for most services.
- **Cloud Run well.** Concurrency per instance, CPU allocation (always-allocated for background work), min instances for latency-sensitive paths, max instances to bound cost, VPC connectors only when needed.
- **GKE.** Autopilot removes node management; workload identity binds K8s service accounts to GCP service accounts (no keys). Use it when you need Kubernetes semantics, not by default.
- **Cloud SQL / AlloyDB.** Managed Postgres/MySQL (Cloud SQL) with HA and backups; AlloyDB for high-performance Postgres-compatible workloads. Private IP, no public exposure.
- **BigQuery.** Serverless data warehouse: columnar storage, SQL interface, partitioning + clustering for performance and cost. On-demand vs flat-rate/slot pricing — understand which fits your query pattern before the bill arrives.
- **GCS.** Object storage with storage classes (Standard/Nearline/Coldline/Archive), lifecycle policies, versioning, and uniform bucket-level access (prefer over fine-grained ACLs).
- **Pub/Sub.** Managed messaging: topics, subscriptions (push/pull), exactly-once delivery options, dead-letter topics, ordering keys. The decoupling primitive for event-driven GCP.
- **Cloud Armor.** WAF + DDoS protection at the edge, integrated with load balancers — rate limiting, geo-blocking, and managed OWASP rules.
- **Operations suite.** Cloud Logging/Monitoring/Trace/Profiler — the default observability stack. Structured JSON logs, log-based metrics, SLO monitoring with alerting.
- **Budgets and cost control.** Budgets with alert thresholds, committed use discounts for steady workloads, BigQuery cost controls (query quotas, custom quotas), and regular rightsizing.
- **Cloud Run jobs.** Run-to-completion container tasks (batch, migrations) — the serverless answer to one-off jobs without standing up GKE.
- **VPC Service Controls.** A data-exfiltration perimeter around GCP resources — complexity worth paying for regulated workloads.

## Practical workflow

1. **Set up the hierarchy.** Organization → folders (prod/non-prod) → projects per service/environment; organization policies (allowed regions, no public IPs, OS Login) as guardrails.
2. **Configure IAM.** Groups for humans (never individual bindings at scale), service accounts per workload, least-privilege custom roles where predefined are too broad; workload identity for GKE, impersonation elsewhere.
   ```hcl
   # least-privilege binding sketch
   resource "google_project_iam_member" "api_reader" {
     project = var.project_id
     role    = "roles/pubsub.subscriber"
     member  = "serviceAccount:${google_service_account.api.email}"
   }
   ```
3. **Build the VPC.** Shared VPC for multi-project networking or per-project VPCs; private subnets for workloads, Private Google Access on, firewall rules deny-by-default with explicit allows, Cloud NAT only where public egress is needed.
4. **Choose compute per workload.** Services → Cloud Run (scale-to-zero, concurrency tuned); event handlers → Cloud Functions/Eventarc; Kubernetes needs → GKE Autopilot; VMs → GCE with managed instance groups.
5. **Put data on managed services.** Cloud SQL private-IP with automated backups and point-in-time recovery; GCS with lifecycle policies; BigQuery datasets with partitioned tables.
6. **Decouple with Pub/Sub.** Events between services via topics; pull subscriptions for workers with dead-letter topics; ordering keys only where order truly matters.
7. **Protect the edge.** Global load balancer + Cloud Armor policies (rate limits, WAF rules); Cloud CDN for static content; IAP (Identity-Aware Proxy) for internal apps instead of VPNs.
8. **Observe and control cost.** Cloud Monitoring dashboards + SLO alerts; budgets at project/folder level with webhook notifications; BigQuery slot/quota monitoring; committed use discounts after baselines stabilize.

   ```hcl
   resource "google_compute_firewall" "deny_all_ingress" {
     name    = "deny-all-ingress"
     network = google_compute_network.main.name
     deny { protocol = "all" }
     source_ranges = ["0.0.0.0/0"]
     priority      = 65535 # last-resort deny; explicit allows take precedence
   }
   ```

## Common pitfalls

- **Primitive roles (Owner/Editor)** — org-wide blast radius; use granular roles.
- **Downloaded service account keys** — leaked credentials; impersonation and workload identity instead.
- **Public Cloud SQL** — databases with public IPs; private IP + authorized networks only.
- **BigQuery cost surprise** — unpartitioned full-table scans on terabytes; partition, cluster, and set quotas.
- **Cloud Run max instances unset** — runaway scaling bills; always bound max instances.
- **Flat project structure** — everything in one project; use folders and per-service projects.
- **No organization policies** — no guardrails on regions, public IPs, or external sharing; set them early.
- **NAT for Google API traffic** — paying NAT data-processing for API calls; Private Google Access instead.
- **Ignoring budgets** — cost alerts configured but unmonitored; budgets need owners and runbooks.
- **GKE by default** — Kubernetes operational overhead for services Cloud Run would handle; choose the simplest compute that fits.
- **Uniform bucket access ignored** — legacy ACL sprawl; enable uniform access on new buckets.
- **No dead-letter on Pub/Sub** — poison messages redelivering forever; configure dead-letter topics.
- **Firewall rules wide open** — `0.0.0.0/0` ingress left from debugging; audit and restrict.
