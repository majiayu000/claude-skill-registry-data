---
name: Google Cloud
slug: gcp
version: 1.0.2
description: Architects, debugs, secures, and cost-optimizes Google Cloud — Cloud Run, GKE, Compute Engine, BigQuery, Cloud SQL, IAM, VPC. Use when deploying or reviewing anything on GCP, when a bill jumps or BigQuery scan cost has to come down, when a 403 PERMISSION_DENIED, a SERVICE_DISABLED, a RESOURCE_EXHAUSTED quota error, a 502/503/504, or an unreachable Cloud SQL instance has no obvious cause, when choosing between compute (Cloud Run, GKE, Cloud Functions) or databases (Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable), when hardening service accounts, org policies, firewall rules, public buckets, or secrets, when writing Terraform against the google provider, or when auditing an inherited project. Covers VPC/subnet design, Private Google Access, Vertex AI/GPU quota, Pub/Sub/Dataflow, backups/DR, and gcloud. Not for Kubernetes manifest authoring (`k8s`), Terraform language mechanics (`terraform`), or PostgreSQL tuning inside Cloud SQL (`pg`).
homepage: https://clawic.com/skills/gcp
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🌐
    requires:
      anyBins:
      - gcloud
    os:
    - linux
    - darwin
    - win32
    displayName: Google Cloud
    configPaths:
    - ~/Clawic/data/gcp/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/domains/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/gcp/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/domains/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/gcp/config.yaml` (what the user declared) and `~/Clawic/data/gcp/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before any deploy, sizing, or "what do I have" question. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a VM or cluster created, resized, discovered or retired; an inventory pass; a spend number or a saving; a budget or a billing export; a project and its owner; a quota that was raised; a service account and what it is for; a BigQuery dataset and its scan baseline; a DNS zone; a deploy or a timed restore drill; or something the user will want to read again — a runbook, an IAM policy that finally worked, an architecture decision. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**Four boxes are shared with other skills, not private to GCP.** Hosts — Compute Engine VMs and GKE node pools — go to `~/Clawic/data/servers/servers.md`, one row per host identified by `Name` + `Provider`, so a question about "my servers" answers itself whichever cloud they live in. DNS zones and registered domains go to `~/Clawic/data/domains/domains.md`, identified by the domain name. A client or colleague who owns a project goes to `~/Clawic/data/contacts/contacts.md`, identified by **email or handle**, and is referenced here by name only. Work the user tracks as a project of their own goes to `~/Clawic/data/projects/<project>.md`, one file per project named after it. Read the box before adding: if the entity is already there, update that row or file in place, never append a second one, and never touch a row another source wrote. Retirement is part of the row-based boxes — when a host, domain or contact is gone, delete its row and note the date in `memory.md`; a finished project instead keeps its file with `status: closed`. Identity key, scale cut and the foreign-columns rule for each box are in `memory-template.md`, which travels with this skill because the user may not have the owning skill installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `gcp-sm:projects/acme/secrets/db-password`, `env:GOOGLE_APPLICATION_CREDENTIALS`, `keychain:gcp-prod`, `file:~/.config/gcloud/application_default_credentials.json`.

Google Cloud is two products wearing one console: an IaaS that behaves like a worse-documented AWS, and a data/ML platform that is the actual reason to be here. Route accordingly, name the monthly number, and say what the blast radius is. Reach for the managed thing that scales to zero before the thing with a node floor, and say when the floor is worth paying. Work from defaults immediately: never open with questions about their project, their budget, or how proactive to be. The one exception to silence is `default_project` and `default_region` — while either is unset, state what you are assuming before acting (Rule 7). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale) → the Configuration table default.

## When To Use

- Architecting or deploying on GCP: service selection, VPC layout, project and folder layout, infrastructure as code
- Diagnosing a GCP failure whose cause is not obvious: 403 on a call that should work, a quota error, a 502/503/504, a container that never becomes ready, a database that will not accept connections
- A bill that jumped, or spend that has to come down — including a BigQuery query that scanned more than anyone expected
- Security work: service accounts, IAM roles and deny policies, org policies, public buckets, private IP, key hygiene, auditing an inherited project
- Data and ML work on the platform: BigQuery modeling and cost, Pub/Sub and Dataflow pipelines, Vertex AI endpoints and GPU quota
- Operating what is already live: scaling, GKE upgrades, backups and restore drills, quotas, deploy and rollback
- Not for Kubernetes manifest authoring (`k8s`), Terraform language mechanics (`terraform`), or PostgreSQL query and index tuning (`pg`) — this covers the GCP-platform side of all three

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "My bill exploded" | Billing export in BigQuery by service, then by SKU; the delta's start date maps to a deploy | `costs.md` |
| Fresh project, nothing deployed yet | Billing export + budget alerts before the first resource, then the Rule 3 stage table | `costs.md` |
| Inherited or unknown project | Asset Inventory sweep (Rule 1), then the audit checklist top to bottom | `security.md` |
| 403 `PERMISSION_DENIED` on a call that should work | Check API enablement first, then role binding, then deny policy, then VPC-SC — in that order | `iam.md` |
| Which role grants this, and who has too much | Policy Troubleshooter, then IAM Recommender for the over-grant | `iam.md` |
| Cannot reach Cloud SQL, a VM, or a Google API | Walk the path in order: firewall → route → Private Google Access → PSC/peering → DNS | `networking.md` |
| 502/503/504 from a load balancer, or requests that hang | Backend service timeout and health-check source ranges — the status code names the layer | `debug.md` |
| Cloud Run revision will not go live, or is slow and cold | PORT contract, startup probe, concurrency, min instances, CPU allocation mode | `run.md` |
| GKE pod unschedulable, node pool churning, upgrade due | Autopilot constraints, node pool sizing, release channels, surge upgrades | `gke.md` |
| Database out of connections, failing over, or out of disk | Connection ceiling, Auth Proxy, HA vs read replica, PITR, storage that never shrinks | `databases.md` |
| BigQuery query too slow or too expensive | Bytes scanned, not rows: partitioning, clustering, column pruning, on-demand vs editions | `bigquery.md` |
| Streaming or batch pipeline to build or debug | Pub/Sub delivery semantics, Dataflow autoscaling, Composer's floor, Datastream CDC | `pipelines.md` |
| Cloud Storage surprises: cost, permissions, retrieval fees | Storage classes, early-deletion and retrieval charges, versioning, uniform access | `storage.md` |
| Vertex AI endpoint, GPU quota, or model serving cost | Quota starts at zero, endpoints bill while idle, batch beats online for offline work | `vertex.md` |
| Choosing between two services | Decide by hard limit, node floor, and break-even, never by feature list | `services.md` |
| Second project, folders, org policies, billing accounts | Organization hierarchy, Shared VPC, quotas, landing zone | `organization.md` |
| Terraform state, drift, or an import to do | google provider gotchas, drift, import, Config Connector, Cloud Build/Deploy | `iac.md` |
| Taking it to production | SLOs, alerting that fires, backups and timed restores, deploy and rollback | `production.md` |
| Need the exact gcloud invocation | Configurations, ADC vs user login, impersonation, `--format`/`--filter`, dry runs | `commands.md` |
| Anything else GCP | Answer directly, then state the monthly cost and the blast radius of what you recommended | — |

Coverage map: `debug.md` symptom→cause · `iam.md` identity and permissions · `networking.md` VPC and connectivity · `costs.md` bill control · `security.md` hardening and leak response · `services.md` selection thresholds · `run.md` Cloud Run and functions · `gke.md` Kubernetes on GCP · `databases.md` Cloud SQL/AlloyDB/Spanner/Firestore/Bigtable · `bigquery.md` warehouse cost and design · `pipelines.md` Pub/Sub, Dataflow, Composer · `storage.md` Cloud Storage and disks · `vertex.md` AI platform · `organization.md` projects, folders, billing · `iac.md` Terraform and delivery · `production.md` reliability · `commands.md` gcloud toolkit.

## Core Rules

1. **Inventory before architecture.** Never propose infrastructure into an unknown project — and never rediscover a project you already mapped. Read the stored inventory first: `## Current Infrastructure` in `memory.md`, whatever its `## Boxes` line points to, and `~/Clawic/data/servers/servers.md`. Then discover only what is missing or older than the last recorded pass, and write the result back. Minimum discovery: `gcloud config list`, `gcloud projects list`, `gcloud asset search-all-resources --scope=projects/<id>`, and 30 days of cost grouped by service. Asset Inventory is the one GCP tool with no AWS equivalent worth envying — it answers "what exists here" across every API in one call, including resources whose API you never thought to check.
2. **Billing export and a budget before the first resource.** On a fresh project the first deploy is a Cloud Billing export to BigQuery plus a budget, not a VM. The export is the only source of SKU-level detail and **it reports forward only** — a month without it is unanalyzable forever, exactly like an untagged month. Budget thresholds: alert at 50%, 90%, and 100% of actual plus 100% of forecast. **A budget does not cap spend**; capping requires a Pub/Sub-triggered function that detaches the billing account, which stops every resource in the project (`costs.md`).
3. **A monthly number with every recommendation.** Rough stages (us-central1, on-demand, early 2026 — verify current pricing before committing):

   | Stage | Recommended stack | Monthly |
   |-------|-------------------|---------|
   | MVP (<1k users) | Cloud Run scaling to zero + smallest Cloud SQL, no HA | ~$30 |
   | Growth (1-10k) | Cloud Run with min-instances 1 + Cloud SQL HA + Memorystore | ~$250 |
   | Scale (10k+) | GKE Autopilot or Cloud Run + AlloyDB/Cloud SQL HA + global ALB + Cloud CDN | $600+ |

   Default to the smallest viable machine: scaling up is a restart, an oversized fleet bleeds silently. Right-sizing heuristic (canonical for this skill): read `gcloud recommender` before guessing — GCP computes idle-VM, idle-disk, idle-IP and machine-type recommendations from 8 days of observed usage and they are usually right. Where there is no recommendation, avg CPU <20% over 14 days → step down one size (each step ≈ halves compute cost); sustained >70% → step up or scale out. CPU alone under-diagnoses memory-bound workloads.
4. **Smallest blast radius, decided at creation.** One dedicated service account per workload — never the default Compute Engine service account, which carries Editor unless the org policy that stops it is enforced. Databases on private IP; buckets with uniform bucket-level access and public access prevention; CMEK chosen at creation. Retrofits that do not exist: a bucket's location, a Cloud SQL instance's private-IP network, a subnet's primary range shrinking, a project ID.
5. **Everything in code, nothing console-only.** Console is for exploration; `gcloud` is imperative and forgets. Anything that survives the session goes into the tool named by `iac_tool`. Plan must come back clean before any change, or you are about to codify someone's console hotfix as an accident (`iac.md`).
6. **Label at creation, and only after the export exists.** Labels reach the billing export from the moment both the label and the export exist — never backfilled. Keys are lowercase, and a resource cannot carry more than 64 of them. Minimum set: `env`, `team`, `service`. Untagged spend is next month's argument.
7. **Project and region are decisions, not defaults.** State both in every command and price quote. A project ID is globally unique and permanent — it cannot be renamed, and after deletion it can never be reused by anyone. Region matters twice in GCP: for price, and because a VPC is global while every subnet, disk, and Cloud SQL instance is not. When `default_project` or `default_region` is unset, say what you are assuming before acting.
8. **Name the first quota and the first timeout.** Quotas in GCP are per project **and** per region, and several start at zero rather than at a generous default — GPUs, TPUs, and some newer machine families are zero until requested, and approval takes days, not minutes. Every scaling design states which limit it hits first and its current value (`gcloud alpha quotas list` or the Quotas page). A design that has not named its ceiling has not been designed.

## Failure Signatures

Decode rule: in GCP the error string names the subsystem more reliably than the status code. A 403 is three unrelated problems wearing one number; a "quota" message may be capacity, not quota.

| Signature | Most likely cause | First move |
|---|---|---|
| 403 `SERVICE_DISABLED` / "API has not been used in project…" | The API is simply not enabled — not a permissions problem at all | Enable the service; this is the single most common false IAM alarm in GCP |
| 403 `PERMISSION_DENIED` with the right role granted | Binding on the wrong resource level, propagation lag, a deny policy, or VPC Service Controls | Policy Troubleshooter with the exact principal, resource and permission (`iam.md`) |
| 403 mentioning `VPC Service Controls` or a unique request id | A perimeter blocked the call, and the message is deliberately vague | Read the VPC-SC audit log entry — it names the perimeter and the service (`security.md`) |
| `caller does not have permission … iam.serviceAccounts.actAs` | The caller may create the resource but not attach that service account | Grant `roles/iam.serviceAccountUser` on the exact service account, not project-wide (`iam.md`) |
| 429 `RESOURCE_EXHAUSTED` | Rate quota, per project per region | Backoff with jitter, then request the quota; check whether the default is zero (Rule 8) |
| `ZONE_RESOURCE_POOL_EXHAUSTED` | Google has no capacity in that zone right now — this is not a quota | Try another zone, a different machine family, or a reservation. Raising quota changes nothing |
| Cloud Run "container failed to start and listen on the port" | The app is not listening on `$PORT` (8080) on `0.0.0.0`, or it is slower than the startup probe | The PORT contract in `run.md` — this is the top Cloud Run deploy failure |
| LB 502 with healthy-looking backends | Backend closed a keep-alive connection, or the backend service timeout (30s default) fired | Raise backend keep-alive above the LB's, then the timeout (`networking.md`) |
| LB 503 "no healthy upstream" | Health checks blocked: `35.191.0.0/16` and `130.211.0.0/22` must be allowed in the firewall | Health-check source ranges in `networking.md` — the most-missed firewall rule in GCP |
| `Connection timed out` to Cloud SQL | Network path, not credentials | Timeout = firewall/private-IP/peering; `password authentication failed` = credentials (`databases.md`) |
| Cloud SQL "remaining connection slots are reserved" | Connection ceiling, usually from serverless fan-out | Auth Proxy plus a pooler; the ceiling derives from tier memory (`databases.md`) |
| BigQuery query costs 100× the estimate | `SELECT *`, no partition filter, or a filter the pruner cannot use | Dry-run every query before running it (`bigquery.md`) |
| GKE pod `Unschedulable` on Autopilot | Requested a CPU:memory ratio or a feature Autopilot rounds or rejects | Autopilot's resource rules in `gke.md` |
| VM vanishes ~30 seconds after a notice | Spot preemption — GCP gives 30 seconds, not AWS's two minutes | Handle `SIGTERM` fast, or leave Spot (`services.md`) |
| Alert never fired during a real outage | The metric stopped publishing, so the condition never evaluated | Alert on absence of data explicitly (`production.md`) |
| Anything else | Find the exact method and error in Cloud Audit Logs, then match it here | `debug.md` |

## Limits That Force Designs

These are architecture constraints, not trivia: each one has killed a design that was already half-built.

| Service | Limit that decides the design |
|---|---|
| Cloud Run | 60 min max request timeout · default concurrency 80 per instance, max 1000 · max instances default 100 · request payload limits far below a file-upload service's needs — stream to Cloud Storage instead |
| Cloud Run functions | Gen1 caps at 9 min; gen2 HTTP functions reach 60 min. Gen1 is the reason to migrate, and gen2 *is* Cloud Run under a different UI |
| Pub/Sub | Ack deadline 10s default, 600s max · message retention up to 31 days · ordering keys serialize a key's throughput — ordering and scale are traded, not combined |
| BigQuery | On-demand billing is bytes **scanned**, never rows returned · `LIMIT` does not reduce it · streaming inserts cost far more per GB than batch loads, which are free |
| Firestore | Sustained writes to a single document cap around 1/s · sequential document IDs hotspot the index · ramp new traffic gradually rather than launching at full rate |
| Bigtable | One-node floor (hundreds of dollars a month) · the row key is the only index you get, and it cannot be changed later |
| Spanner | Priced from 100 processing units, so the floor is real · schema interleaving is a creation-time decision |
| Cloud SQL | Storage grows and never shrinks · HA failover is a zone-level standby, not a backup · connection ceiling derives from tier memory (`databases.md`) |
| VPC | Global, and a subnet's primary range **can be expanded** but never shrunk · secondary ranges for GKE pods/services are sized at cluster creation and constrain maximum pods forever |
| VPC peering | Non-transitive. Two peered networks do not reach each other's peers — this is why Private Service Connect exists |
| Load balancing | Backend service timeout defaults to 30s · global external ALB requires Premium network tier |
| Projects | Project ID globally unique and permanently unreusable · deletion has a 30-day recovery window · quotas are per project, which makes the project the real isolation unit |
| Cloud KMS | Key rings and keys cannot be deleted, ever — only key versions are destroyed, after a scheduled delay. Plan the naming, because it is permanent |

## Cost Reflexes

The ten line items that produce most surprise bills. Prices: us-central1, on-demand, recorded early 2026 — the ratios are stable, the absolute numbers need verifying (`costs.md` has the commands and the savings playbook).

| Driver | Why it bites | Do instead |
|------|--------------|------------|
| BigQuery on-demand scans | ~$6.25 per TiB scanned, and a `SELECT *` on a wide table scans every column even if you read one | Partition, cluster, select columns, dry-run first; move to editions when monthly scan cost passes a stable baseline (`bigquery.md`) |
| Cloud NAT | Hourly gateway charge plus ~$0.045/GB processed; traffic to Google APIs through NAT is pure waste | Private Google Access on the subnet — free — and Private Service Connect for the rest (`networking.md`) |
| Cloud Logging ingestion | ~$0.50/GiB after the free monthly allowance per project; Data Access audit logs enabled org-wide are the usual cause | Exclusion filters at the sink, and enable Data Access logs only on the datasets and buckets that matter (`security.md`) |
| External IPv4 addresses | Billed per hour whether attached or not, and a reserved-but-unused address bills at a higher rate than an attached one | Count them; release the orphans; put workloads behind a load balancer with no public IP on the VM |
| Idle Vertex AI endpoints | A deployed endpoint bills per node-hour at zero traffic, and GPU node-hours are the expensive kind | Undeploy between experiments; use batch prediction for anything not interactive (`vertex.md`) |
| E2 machines chosen for the list price | E2 is cheap per hour but earns **no** sustained-use discount; N2/N2D/C-series discount automatically toward month-end | For an always-on workload compare the *discounted* N-series price, not the list price (`costs.md`) |
| Orphaned disks and snapshot chains | Deleting a VM leaves its disks unless auto-delete was set; snapshots are incremental but the chain keeps the deleted data alive | Sweep disks with no users; give snapshots a retention policy (`storage.md`) |
| Cross-zone and internet egress | Same-zone traffic is free, cross-zone is not, internet egress is the expensive tier | Co-locate chatty pairs in one zone; serve public assets through Cloud CDN |
| Cloud Composer | A small Airflow environment has a floor in the hundreds per month, running or idle | Cloud Scheduler + Workflows for anything short of real DAGs with backfills (`pipelines.md`) |
| Bigtable and Spanner floors | Both bill from a minimum capacity, so a small workload pays a subscription rather than a usage bill | Firestore or Cloud SQL until the access pattern genuinely demands them (`services.md`) |

## Security Baseline

Non-negotiables. Anything unchecked here outranks whatever feature work is in flight; commands and the full audit are in `security.md`.

| Check | Passing looks like |
|---|---|
| Domain-restricted sharing | `constraints/iam.allowedPolicyMemberDomains` enforced — without it, one `roles/viewer` grant to a personal Gmail address is a valid, silent, permanent export path |
| Default service account | Workloads run as dedicated service accounts; the default Compute Engine account has no Editor and ideally no bindings at all |
| Service account keys | None created; `constraints/iam.disableServiceAccountKeyCreation` enforced, CI authenticated with Workload Identity Federation |
| Primitive roles | No `roles/owner` or `roles/editor` on humans or workloads outside break-glass; predefined or custom roles instead |
| Buckets | `constraints/storage.publicAccessPrevention` enforced org-wide; uniform bucket-level access on; public content served by a load balancer with Cloud CDN |
| Databases | Cloud SQL on private IP only, `constraints/sql.restrictPublicIp` enforced |
| VM access | No external IPs (`constraints/compute.vmExternalIpAccess`), OS Login instead of metadata SSH keys, shell via IAP TCP forwarding — which needs no open inbound port |
| Audit trail | Admin Activity logs are always on and free; Data Access logging deliberately enabled where the data is, with a retention that matches the compliance regime |
| Data residency | `constraints/gcp.resourceLocations` set when a regime or a contract names allowed regions |

## Service Defaults

One default per need, with the escape hatch. Thresholds and break-evens: `services.md`.

| Need | Default | Switch when |
|------|---------|-------------|
| Static site | Cloud Storage behind a global external ALB + Cloud CDN | Never — a public bucket as origin gives up caching, TLS control, and Cloud Armor |
| API backend | Cloud Run | Node-level control, sidecar-heavy meshes, or an existing Kubernetes ecosystem (→ GKE Autopilot) |
| Event handler | Cloud Run function triggered by Eventarc | The work exceeds the HTTP ceiling (→ Cloud Run job or Batch) |
| Container orchestration | GKE Autopilot | Privileged pods, custom kernel settings, or fine-grained GPU packing (→ GKE Standard) |
| Relational database | Cloud SQL for PostgreSQL | Global writes with strong consistency (→ Spanner); heavy analytics against live OLTP (→ AlloyDB) |
| Document database | Firestore in Native mode | Petabyte scale with a single known row-key access pattern (→ Bigtable) |
| Cache / sessions | Memorystore | Idle cost matters more than sub-ms latency (→ Firestore) |
| Messaging | Pub/Sub | Per-task scheduling, retries and rate control (→ Cloud Tasks); multi-step state machines (→ Workflows) |
| Warehouse | BigQuery | — |
| Job orchestration | Cloud Scheduler + Workflows | Real DAGs with dependencies and backfills (→ Composer, with its floor priced in) |
| Secrets | Secret Manager | — |
| Container images | Artifact Registry | — (`gcr.io` addresses now resolve to Artifact Registry) |
| Config/IaC | Whatever `iac_tool` says | — |

## Output Gates

Before delivering an architecture, a policy, or a command:

- Did I state the monthly cost of what I recommended, in the region it will actually run?
- Did I check the stored inventory *and* the live project before proposing something new?
- Is anything holding data reachable from the public internet, or shared outside the org's domain?
- Does this design name the first quota and the first timeout it will hit (Rule 8)?
- Is anything that cannot be retrofitted — bucket location, private-IP network, secondary ranges, KMS naming, project ID — set correctly at creation?
- Is any command destructive (delete, detach billing, destroy key version, drop dataset)? Then it ships with an explicit confirmation step, never inside a copy-paste block of read-only commands.
- **Did anything durable come out of this session — a host, a project, a quota grant, a spend number, a service account, a dataset, a DNS zone, a runbook, a decision? Then it is written to its box before I finish, and any new box has its `## Boxes` line in the same turn (`memory-template.md`).**

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/gcp/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_project | text (project id) | none | Project assumed by every command and price quote; while unset, name the assumed project out loud before acting (Rule 7) |
| default_region | text (region id) | none | Region and zone assumed for placement and quotes; drives which zonal capacity advice applies (Rule 7) |
| gcloud_configuration | text (configuration name) | none | Adds `--configuration <name>` to CLI examples; unset means examples assume the active configuration (`commands.md`) |
| iac_tool | terraform \| config-connector \| gcloud \| none | terraform | Language of every generated infrastructure artifact and the drift-check command in `iac.md` (Rule 5) |
| monthly_budget_usd | number (USD) | 100 | Budget alert thresholds in `costs.md` (Rule 2) and the bar for calling a recommendation expensive |
| org_model | single-project \| organization | single-project | Whether guidance uses one project plus budgets, or folders, org policies, Shared VPC and per-project billing (`organization.md`) |
| bq_billing_model | on-demand \| editions | on-demand | Whether BigQuery advice optimizes bytes scanned or slot utilization, and which break-even applies (`bigquery.md`) |
| compliance_regime | none \| hipaa \| pci \| soc2 \| gdpr-eu | none | Restricts selection to eligible services and forces the logging, CMEK, residency and retention defaults that regime requires |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — Terraform module style vs Config Connector, Cloud Build vs GitHub Actions, console vs CLI for exploration, ADC vs impersonation for local auth — affects every command example
- **Conventions** — label keys beyond the required three, project ID and network naming scheme, environment separation (project per env vs folder per env), CIDR allocation and secondary-range plan — affects generated resources and the `networking.md` address plan
- **Platform** — home region and multi-region posture, machine family standard (E2 vs N2 vs C3 vs Arm-based T2A/C4A), Autopilot vs Standard for GKE, Premium vs Standard network tier — affects sizing advice and every price quote
- **Safety posture** — whether destructive commands are emitted at all, deletion protection and project liens default-on, appetite for Spot in production — affects Output Gates and `production.md`
- **Cost reporting** — review cadence, whether every answer carries a monthly number, currency for quotes, who receives budget alerts — affects `costs.md`
- **Data platform** — BigQuery dataset location and naming, on-demand vs editions posture, whether streaming ingestion is permitted at all — affects `bigquery.md` and `pipelines.md`
- **Service preferences** — the standing pick where this skill offers a default (Cloud Run vs GKE, Firestore vs Bigtable, Workflows vs Composer) — affects Service Defaults and `services.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Treating a budget as a spending cap | Budgets only notify. Spend continues past 100% with no brake | Alerts at 50/90/100%, and if a hard cap is genuinely required, understand that it works by detaching billing and stopping everything (`costs.md`) |
| Enabling billing export "when we need it" | The export has no history — it starts the day you turn it on, so the expensive month is the unanalyzable one | Enable on day one, before the first resource (Rule 2) |
| Running workloads as the default Compute Engine service account | It carries Editor on the whole project, so any compromised container is a project takeover | One service account per workload with only the roles it uses (`iam.md`) |
| Fixing a 403 by granting a broader role | Most GCP 403s are a disabled API or a deny policy; the wider role does not fix them and never gets narrowed again | Diagnose with Policy Troubleshooter first — the API-enablement check takes ten seconds (`iam.md`) |
| Creating a service account key because the tutorial did | A JSON key is a permanent credential with no expiry, and it ends up in a repository | Workload Identity Federation for CI, impersonation locally, attached service accounts on GCP (`iam.md`) |
| `SELECT *` in a BigQuery notebook | Columnar storage means you pay for every column you name, and a wide table is mostly columns you did not want | Name columns, filter the partition, dry-run before running (`bigquery.md`) |
| Committed use discounts before right-sizing | Locks the oversized fleet in for one to three years — the discount is real, the waste is bigger | Right-size from Recommender (Rule 3), observe two weeks, then commit (`costs.md`) |
| HA treated as a backup | A regional Cloud SQL failover replicates your `DROP TABLE` to the standby instantly | HA is availability; PITR and exports are recovery (`databases.md`) |
| Sizing GKE secondary ranges "generously later" | Pod and service ranges are fixed at cluster creation and cap the cluster's maximum pods permanently | Size the secondary ranges against the three-year node count before creating the cluster (`gke.md`) |
| Assuming VPC peering is transitive | Peering does not chain, so the hub-and-spoke design silently loses half its paths | Private Service Connect, or a full mesh, decided before the second spoke (`networking.md`) |
| Reading spend from the Billing console's reports page | It rounds, lags, and hides the SKU breakdown that names the cause | Query the billing export in BigQuery, grouped by service then SKU (`costs.md`) |
| One project for everything | Quotas, IAM blast radius, and cost attribution are all per project — the single project makes every one of them worse at once | Project per environment at minimum, folders once there is a team (`organization.md`) |
| Deleting a project to clean up | The ID is burned globally and forever, and the 30-day window hides live dependencies until they break | Delete the resources, keep the project, or set a lien if it must never be deleted (`organization.md`) |
| Turning on every security service on day one | Security Command Center Premium, org-wide Data Access logs, and full VPC-SC on a small footprint can outspend the workload | Free baseline first (org policies, Admin Activity logs), paid detection when there is something worth detecting (`security.md`) |

## Where Experts Disagree

- **Cloud Run vs GKE.** Request-shaped work with variable traffic → Cloud Run wins on idle cost and operational surface. A platform team, service meshes, operators, or per-node GPU packing → GKE. The honest frontier: GKE Autopilot removed most of the node toil that used to make this obvious, so the question is now "do you need Kubernetes APIs", not "do you need containers" (`services.md`).
- **Project per environment vs folder per team.** Solo builder → one project per environment is enough and folders are ceremony. Any team, or any regime requiring demonstrable isolation → folders with inherited org policies now, because reorganizing a live hierarchy later means re-granting every binding (`organization.md`).
- **BigQuery on-demand vs editions.** On-demand rewards unpredictable, sparse querying and punishes a heavy dashboard refreshing hourly. Editions rewards steady load and punishes idle slots. The break-even is a monthly scan number, not a preference (`bigquery.md`).
- **Terraform vs Config Connector.** Teams already fluent in Terraform get more leverage keeping GCP in the same workflow as everything else. Teams whose primary interface is Kubernetes get real value from managing cloud resources as CRDs with the same reconciliation loop. Both lose to console clicking.
- **Spot in production.** One camp says a 30-second preemption notice is too short for anything stateful and Spot belongs in batch only. The other runs Spot node pools behind a Standard baseline pool and treats preemption as ordinary autoscaling. The dividing line is whether the workload can drain in 30 seconds — measure it before choosing a side.

## Security & Privacy

**Credentials:** this skill drives the `gcloud` CLI, which reads credentials from `~/.config/gcloud/`, from Application Default Credentials, or from environment variables. It does NOT store, log, copy, or transmit GCP credentials, and never writes a credential into `~/Clawic/data/gcp/`.

**Local storage:** preferences, memory, inventory, quota grants, and cost history stay in `~/Clawic/data/gcp/` on this machine — project IDs, resource names and service account emails only, no secrets.

**Guardrails:** commands are read-only by default. Destructive operations (deleting a project or dataset, destroying a key version, detaching a billing account, removing a node pool) are presented with their blast radius and require explicit user confirmation before running.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/gcp (install if the user confirms):
- `terraform` — HCL authoring, state surgery, module design
- `k8s` — Kubernetes manifests and cluster debugging, for GKE workloads
- `pg` — PostgreSQL query, index and vacuum tuning inside Cloud SQL and AlloyDB
- `aws` — the same architecture questions on the other provider, and cross-cloud comparisons
- `infrastructure` — provider-agnostic architecture decisions

## Feedback

- If useful, star it: https://clawic.com/skills/gcp
- Latest version: https://clawic.com/skills/gcp

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/gcp.
