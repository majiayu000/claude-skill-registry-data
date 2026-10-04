---
name: AWS | Amazon Web Services
slug: aws
version: 1.0.7
description: Architects, debugs, secures, and cost-optimizes AWS infrastructure — EC2, Lambda, RDS, VPC, IAM, ECS, CloudFront. Use when deploying or reviewing anything on AWS, when a bill jumps or spend has to come down, when an AccessDenied, throttle, timeout, 502/503/504, or unreachable-database error has no obvious cause, when choosing between Lambda, Fargate, EC2, RDS, DynamoDB, SQS, or EventBridge, when hardening IAM policies, S3 exposure, security groups, or secrets, when writing Terraform/CloudFormation/CDK against AWS, when auditing an account you inherited, or when a service quota, cold start, connection limit, or failover is the thing that broke. Covers VPC and subnet design, NAT versus VPC endpoints, Organizations and cross-account roles, backups and disaster recovery, and CLI/SSO profiles. Not for object-storage patterns in depth (`s3`), DynamoDB key modeling (`dynamodb`), Kubernetes manifest authoring (`k8s`), or Terraform language mechanics (`terraform`).
homepage: https://clawic.com/skills/aws
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: ☁️
    requires:
      bins:
      - aws
    install:
    - id: brew
      kind: brew
      formula: awscli
      bins:
      - aws
      label: Install AWS CLI (Homebrew)
    os:
    - linux
    - darwin
    - win32
    displayName: AWS | Amazon Web Services
    configPaths:
    - ~/Clawic/data/aws/
    - ~/Clawic/data/servers/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/aws/
      - ~/Clawic/data/servers/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/aws/config.yaml` (what the user declared) and `~/Clawic/data/aws/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/servers/servers.md` before any deploy, sizing, or "what do I have" question. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a host created, resized, discovered or retired; an inventory pass; a spend number or a saving; a budget or alert; an account and its owner; a deploy or a timed DR drill; or something the user will want to read again — a runbook, a policy that finally worked, an architecture decision. `memory-template.md` has every destination, format and threshold, and is the only file you open to write.

**Hosts go to the shared inventory `~/Clawic/data/servers/servers.md`**, not here: the same file holds machines from every provider, so a question about "my servers" answers itself whichever cloud they live in. One row per host, identified by `Name` + `Provider` — update your own row in place, never append a second one: `name | provider (aws) | account/project | region | type | role | monthly cost with currency | access reference`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in these files, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `ssm:/prod/db/password`, `env:AWS_PROFILE`, `keychain:aws-prod`, `profile:prod`.

AWS has hundreds of services; this user needs three of them and a bill that surprises nobody. Cut through the catalog, name the monthly number, and say what the blast radius is. Reach for the cheapest thing that meets the requirement, and say when a cheaper thing would not. Work from defaults immediately: never open with questions about their account, their budget, or how proactive to be. The one exception to silence is `default_region` — while it is unset, state which region you are assuming before acting (Rule 7). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale) → the Configuration table default.

## When To Use

- Architecting or deploying on AWS: service selection, VPC layout, account layout, infrastructure as code
- Diagnosing an AWS failure whose cause is not obvious: AccessDenied, throttling, 502/503/504, a database that will not accept connections, a task that never starts
- A bill that jumped, or spend that has to come down without breaking anything
- Security work: IAM policies, S3 exposure, network isolation, secrets, credential hygiene, auditing an inherited account
- Operating what is already live: scaling, failover, backups, upgrades, quotas, deploy and rollback
- Not for Kubernetes manifest authoring (`k8s`), Terraform language mechanics (`terraform`), object-storage patterns in depth (`s3`), or DynamoDB key modeling (`dynamodb`) — this covers the AWS-account side of all four

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "My bill exploded" | Cost Explorer by service, then by usage type; the delta's start date maps to a deploy | `costs.md` |
| Fresh account, nothing deployed yet | Budget + anomaly alert before the first resource, then the Rule 3 stage table | `costs.md` |
| Inherited or unknown account | Inventory (Rule 1), then the audit checklist top to bottom | `security.md` |
| `AccessDenied` on a call that should work | Classify first: identity policy, resource policy, SCP, boundary, or trust policy | `iam.md` |
| Cannot reach RDS, EC2, or an endpoint | Walk the path in order: SG → route table → NACL → subnet type → DNS | `networking.md` |
| 502/503/504 from a load balancer, or requests that hang | Timeout ladder and target health — the status code names the layer | `debug.md` |
| Lambda slow, throttled, or timing out | Memory-CPU coupling, concurrency model, VPC egress, event-source retries | `lambda.md` |
| ECS/Fargate task never becomes healthy | Stopped reason → image pull path → health-check grace period | `containers.md` |
| Database out of connections, failing over, or out of disk | Connection formula, RDS Proxy, storage rules, PITR | `databases.md` |
| S3/EBS/EFS surprises: cost, permissions, throughput | Request pricing, lifecycle interplay, prefix throughput, access precedence | `storage.md` |
| Choosing between two services | Decide by hard limit and break-even, never by feature list | `services.md` |
| Stack stuck, state drifted, or an import to do | CloudFormation failure states, Terraform drift and import | `iac.md` |
| Second account, SSO, or cross-account access | Organizations, SCPs, role chaining, consolidated billing | `accounts.md` |
| Taking it to production | Multi-AZ, backups and DR drills, scaling, quotas, deploy and rollback | `production.md` |
| Need the exact CLI invocation | Profiles, SSO login, JMESPath, pagination, dry-run, assume-role | `commands.md` |
| Anything else AWS | Answer directly, then state the monthly cost and the blast radius of what you recommended | — |

Coverage map: `debug.md` symptom→cause · `iam.md` permissions · `networking.md` VPC and connectivity · `costs.md` bill control · `security.md` hardening · `services.md` selection thresholds · `lambda.md` serverless · `databases.md` RDS/Aurora/DynamoDB · `storage.md` S3/EBS/EFS · `containers.md` ECS/Fargate/EKS/ECR · `iac.md` Terraform/CloudFormation/CDK · `accounts.md` Organizations and SSO · `production.md` reliability · `commands.md` CLI toolkit.

## Core Rules

1. **Inventory before architecture.** Never propose infrastructure into an unknown account — and never rediscover an account you already mapped. Read the stored inventory first: `## Current Infrastructure` in `memory.md`, whatever its `## Boxes` line points to, and `~/Clawic/data/servers/servers.md`. Then run discovery only for what is missing or older than the last recorded pass, and write the result back. Minimum discovery: `aws sts get-caller-identity`, `aws ec2 describe-vpcs`, and 30 days of Cost Explorer grouped by service (`commands.md`). The spend report maps the account faster than any console tour, because anything real costs something.
2. **Billing alarm before the first resource.** On a fresh account the first deploy is a budget plus an anomaly subscription, not an EC2 instance. Thresholds: alert at 80% of budget actual and 100% forecast; set the anomaly threshold near *daily* spend — `monthly_budget_usd ÷ 30`, so a $100/mo budget alerts at $3, not $50 — because anomalies are daily events and a monthly-sized threshold never fires. Commands, in order (monitor first, then subscription): `costs.md`.
3. **A monthly number with every recommendation.** Rough stages (us-east-1, on-demand — verify current pricing before committing):

   | Stage | Recommended stack | Monthly |
   |-------|-------------------|---------|
   | MVP (<1k users) | Single EC2 + RDS single-AZ | ~$50 |
   | Growth (1-10k) | ALB + ASG + RDS Multi-AZ | ~$200 |
   | Scale (10k+) | ECS/EKS + Aurora + ElastiCache | $500+ |

   Default to the smallest viable instance: scaling up takes two minutes, an oversized fleet bleeds silently. Right-sizing heuristic (canonical for this skill): avg CPU <20% over 14 days → step down one size (each step ≈ halves compute cost); sustained >70% → step up or scale out. CPU alone under-diagnoses memory-bound workloads — check memory before downsizing a JVM or a database.
4. **Smallest blast radius, decided at creation.** Least-privilege IAM scoped to resource ARNs not `*`; databases in private subnets; security groups referencing other security groups instead of CIDRs; encryption on by default. RDS and EBS encryption are creation-time only — retrofitting means snapshot → encrypted copy → restore with downtime, so "later" is a decision to never do it.
5. **Everything in code, nothing console-only.** Console is for exploration; anything that survives the session goes into the tool named by `iac_tool`. Drift check before any change: the plan must come back clean first, or you are about to codify someone's console hotfix as an accident (`iac.md`).
6. **Tag at creation, never retroactively.** Cost allocation tags report only from activation forward — tagging later never backfills, so an untagged month is unattributable forever. Minimum set: `Environment`, `Project`, `Owner`.
7. **Region is a decision, not a default.** State the region in every command and price quote. us-east-1 is usually the cheapest and is where CloudFront certificates, Organizations, and billing APIs genuinely must live — but quoting a us-east-1 price for a workload running in Frankfurt or Sydney is a wrong number, not a rounded one. When `default_region` is unset, say which region you are assuming before acting.
8. **Name the first quota and the first timeout.** Every scaling design states which limit it hits first and its current value (`aws service-quotas get-service-quota`). Defaults that bite earliest: 1,000 concurrent Lambda executions per region, 5 Elastic IPs per region, 60 inbound + 60 outbound rules per security group, 5 security groups per network interface. A design that has not named its ceiling has not been designed.

## Failure Signatures

Decode rule: the layer that emits the error names the subsystem. A load balancer status code is about the *connection*; an API error string is about *permissions or quota*; a bare timeout is about *routing*.

| Signature | Most likely cause | First move |
|---|---|---|
| ALB 502 | Target closed a keep-alive connection the ALB was about to reuse | Set the app's idle/keep-alive timeout above the ALB idle timeout (60s default) — 65-75s is the standard fix |
| ALB 503 | No healthy targets registered | Target-group health, then health-check path/port/matcher, then the SG rule from ALB to target |
| ALB 504 | Target slower than the ALB idle timeout | 504 is a timeout, 502 is a broken connection — fix the slow path before touching timeouts |
| API Gateway 504 at ~29s | Integration timeout ceiling | Make the work asynchronous; raising the quota treats the symptom (`lambda.md`) |
| `AccessDenied` on a policy that looks right | Explicit deny, SCP, permissions boundary, session policy, or a resource policy | Evaluation order in `iam.md` — never widen the identity policy first |
| `not authorized to perform: iam:PassRole` | The caller may create the resource but not hand it that role | Grant `iam:PassRole` scoped to the exact role ARN |
| `Connection timed out` to a database | Network path, not credentials | Timeout = SG/route/subnet; `Access denied` or `password authentication failed` = credentials |
| `CannotPullContainerError` | Private subnet with no NAT and no ECR/S3 endpoints | Pull path in `containers.md` |
| `ThrottlingException` / `Rate exceeded` | API-rate quota, not capacity | Exponential backoff with jitter, then request a quota increase (Rule 8) |
| Instance or task vanishes ~2 minutes after a warning | Spot interruption | Spot gives a 2-minute notice — move un-checkpointed state off Spot |
| Alarm never fired during a real outage | `TreatMissingData: missing` and the metric stopped publishing | Set `notBreaching`/`breaching` deliberately (`production.md`) |
| Anything else | Find the exact API call and error in CloudTrail, then match it here | `debug.md` |

## Limits That Force Designs

These are architecture constraints, not trivia: each one has killed a design that was already half-built.

| Service | Limit that decides the design |
|---|---|
| Lambda | 15 min max execution · 6 MB synchronous payload (256 KB async) · 250 MB unzipped package, 10 GB as a container image · 10 GB max memory · 1,000 concurrent executions per region by default |
| API Gateway | ~29s integration timeout · 10 MB payload |
| SQS | 256 KB message — bigger payloads go to S3 with a pointer · FIFO 300 msg/s per API action, 3,000 with batching |
| DynamoDB | 400 KB item · 3,000 RCU / 1,000 WCU per partition before throttling |
| S3 | 5 TB object, but 5 GB max single PUT (above that, multipart) · 5,500 GET / 3,500 PUT per second per prefix · strong read-after-write consistency since 2020, so eventual-consistency workarounds are now dead code |
| RDS | Storage grows and never shrinks · one storage modification per volume per 6 hours · connection ceiling derives from instance memory, not a lookup table (`databases.md`) |
| EBS | One `modify-volume` per volume per 6 hours |
| ALB / NLB | ALB idle timeout 60s (configurable) · NLB **TLS** listener idle timeout is fixed at 350s — TCP/UDP listeners default to 350s but are tunable, so raise the attribute before designing around keepalives (`networking.md`) |
| CloudFormation | 500 resources per stack — the real reason to split by lifecycle |
| VPC | The primary CIDR is immutable (secondary blocks can be added); a subnet can never be resized |

## Cost Reflexes

The ten line items that produce most surprise bills. Prices: us-east-1, on-demand, recorded early 2026 — the ratios are stable, the absolute numbers need verifying (`costs.md` has the commands and the savings playbook).

| Driver | Why it bites | Do instead |
|------|--------------|------------|
| NAT Gateway | $0.045/hr (~$33/mo) + $0.045/GB processed; S3 and DynamoDB traffic through NAT is pure waste | Gateway VPC endpoints for S3/DynamoDB — free (`networking.md`) |
| CloudWatch Logs ingestion | $0.50/GB ingested, 16× the $0.03/GB-mo storage price; retention caps only the cheap part | Fix the log level first: 1 GB/day of debug logs ≈ $15/mo per log group before a byte is stored |
| Public IPv4 addresses | ~$0.005/hr (~$3.6/mo) each since 2024, attached or not | Count them; release idle EIPs, prefer private subnets behind an ALB |
| Cross-AZ traffic | $0.01/GB each way, so $0.02 per round trip; chatty services pay per hop | Co-locate chatty pairs in one AZ; spend cross-AZ money on replicas, not RPC |
| Idle load balancers | ALB ~$16/mo minimum at zero traffic | Weekly sweep for zero-request ALBs (`costs.md`) |
| gp2 volumes | gp3 is ~20% cheaper ($0.08 vs $0.10/GB-mo) with 3,000 baseline IOPS and no burst cliff | `modify-volume` to gp3 — live, no downtime |
| Snapshots and orphaned EBS | Terminating an instance leaves volumes behind unless DeleteOnTermination was set | DLM lifecycle policy; sweep volumes in `status=available` |
| Secrets Manager by default | $0.40/secret/mo adds up across environments | SSM Parameter Store SecureString unless you need rotation or cross-account (`security.md`) |
| Egress from EC2 | $0.09/GB to the internet | Serve assets via CloudFront — first 1 TB/mo free |
| t3 unlimited mode | Sustained CPU above baseline bills credit overage silently | Watch `CPUSurplusCreditsCharged`; sustained load means a bigger instance, not more credits |

## Security Baseline

Non-negotiables. Anything unchecked here outranks whatever feature work is in flight; commands and the full audit are in `security.md`.

| Check | Passing looks like |
|---|---|
| Root account | MFA on, zero access keys, never used for daily work — a root access key bypasses every policy you write |
| Human access | Identity Center / SSO or IAM roles; no long-lived user keys older than 90 days |
| Workload credentials | Instance/task/function roles — never keys in code, env files, or AMIs |
| IMDS | IMDSv2 required on every instance (`--http-tokens required`) — IMDSv1 turns any SSRF into credential theft |
| S3 | Account-level Block Public Access on; exceptions served by CloudFront + Origin Access Control, not a public bucket |
| Inbound | No 0.0.0.0/0 on SSH or database ports; shell access via SSM Session Manager, which needs no inbound port at all |
| Data at rest | EBS encryption-by-default on account-wide; RDS `--storage-encrypted` at creation (Rule 4) |
| Audit trail | A multi-region CloudTrail exists — the first trail's management events are free, so there is no reason to skip it |

## Service Defaults

One default per need, with the escape hatch. Thresholds and break-evens: `services.md`.

| Need | Default | Switch when |
|------|---------|-------------|
| Static site | S3 + CloudFront | Never — direct public buckets have no advantage |
| API backend | Lambda + API Gateway HTTP API | Duty cycle >~40%, or a request exceeds 15 min / 29s (→ Fargate) |
| Container app | ECS Fargate | The team already runs Kubernetes or needs its ecosystem (→ EKS) |
| Database | RDS PostgreSQL | Every access pattern is a known key lookup and scale is the constraint (→ DynamoDB) |
| Cache / sessions | ElastiCache | Sub-ms is not required and idle cost matters more (→ DynamoDB) |
| Queue | SQS | Multiple independent consumers of one event (→ SNS→SQS fan-out) or replay/ordering (→ Kinesis) |
| Cross-service routing | EventBridge | Latency-sensitive push with no filtering needs (→ SNS) |
| Secrets | SSM Parameter Store SecureString | Automatic rotation or cross-account access required (→ Secrets Manager) |
| Config/IaC | Whatever `iac_tool` says | — |

## Output Gates

Before delivering an architecture, a policy, or a command:

- Did I state the monthly cost of what I recommended, in the region it will actually run?
- Did I check the stored inventory *and* the live account before proposing something new?
- Is anything holding data reachable from the public internet?
- Does this design name the first quota and the first timeout it will hit (Rule 8)?
- Is anything that cannot be retrofitted — encryption, CIDR, DynamoDB keys, subnet size — set correctly at creation?
- Is any command destructive (delete, terminate, modify, force)? Then it ships with an explicit confirmation step, never inside a copy-paste block of read-only commands.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/aws/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| default_region | text (region id) | none | Region assumed by every command and price quote; while unset, name the assumed region out loud before acting (Rule 7) |
| cli_profile | text (profile name) | none | Adds `--profile <name>` to CLI examples; unset means examples assume `AWS_PROFILE` is already exported (`commands.md`) |
| iac_tool | terraform \| cloudformation \| cdk \| sam \| none | terraform | Language of every generated infrastructure artifact and the drift-check command in `iac.md` (Rule 5) |
| monthly_budget_usd | number (USD) | 100 | Budget and anomaly thresholds in `costs.md` (Rule 2) and the bar for calling a recommendation expensive |
| account_model | single \| organization | single | Whether guidance uses one account plus budgets, or Organizations, SCPs, and cross-account roles (`accounts.md`) |
| compliance_regime | none \| hipaa \| pci \| soc2 | none | Restricts selection to eligible services and forces the logging, encryption, and retention defaults that regime requires |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — IaC dialect details (module registry vs local modules, CDK language), SSO vs static profiles, console vs CLI for exploration — affects every command example
- **Conventions** — tag keys beyond the required three, resource and account naming, environment separation, CIDR allocation scheme — affects generated resources and the `networking.md` address plan
- **Platform** — home region and multi-region posture, instance families the org standardizes on, Graviton/arm64 vs x86 — affects sizing advice and price quotes
- **Safety posture** — whether destructive commands are emitted at all, deletion protection and MFA-delete default-on, appetite for blast radius — affects Output Gates and `production.md`
- **Cost reporting** — review cadence, whether every answer carries a monthly number, currency for quotes — affects `costs.md`
- **Service preferences** — the standing pick where this skill offers a default (RDS vs DynamoDB, ECS vs EKS, Parameter Store vs Secrets Manager) — affects Service Defaults and `services.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| "We'll tighten IAM later" | By the time later arrives, every app depends on the wide policy and nobody knows which permission is load-bearing | Generate the policy from observed CloudTrail calls (`iam.md`) |
| Console hotfix on IaC-managed resources | The next apply silently reverts it, usually mid-incident | Fix in code; drift check before every change (Rule 5) |
| Reserved Instances or Savings Plans before right-sizing | Locks the oversized fleet in for 1-3 years — the discount is real, the waste is bigger | Right-size (Rule 3), observe two weeks, then commit (`costs.md`) |
| Multi-AZ treated as a backup | Multi-AZ replicates your `DROP TABLE` in under a second | Multi-AZ is availability; PITR and snapshots are recovery (`databases.md`) |
| Deleting an RDS instance without a final snapshot | Automated backups are deleted with the instance — the data is simply gone | `--final-db-snapshot-identifier` always; deletion protection at creation |
| Reading spend from the Billing console's current month | It lags and hides the usage-type breakdown that names the cause | Cost Explorer grouped by service, then by usage type (`costs.md`) |
| One giant stack or one giant state file | 500-resource ceiling, and one bad change blocks every unrelated deploy | Split by lifecycle: network, data, application (`iac.md`) |
| Public subnet chosen because "it needs internet" | A public IP is not required for outbound traffic | Private subnet + NAT, or VPC endpoints where they exist (`networking.md`) |
| Testing disaster recovery by reading the runbook | Restores fail on details nobody wrote down: KMS grants, parameter groups, DNS | Restore a snapshot into a scratch instance quarterly and time it (`production.md`) |
| Quota increase requested during the incident | Approvals for regional capacity quotas are not instant | Request headroom before the launch, not during it (Rule 8) |
| Sizing a design from an architecture diagram | Diagrams omit quotas, timeouts, retries, and cold paths | Walk Limits That Force Designs against the diagram before building |
| Enabling every AWS security service on day one | GuardDuty + Config + Inspector + WAF on a small account can outspend the workload | Baseline table first (free or near-free), managed detection when there is something worth detecting |

## Where Experts Disagree

- **Lambda-first vs containers-first.** Spiky or low traffic → Lambda wins on idle cost; duty cycle above ~40% or a strict p99 requirement → Fargate/ECS. The break-even math, not the preference, decides (`services.md`).
- **Multi-account from day one.** Solo builder → one account plus budgets is fine; any team, or any compliance regime → Organizations now, because moving live resources between accounts later is a migration project, not a setting (`accounts.md`).
- **NACLs.** Most practitioners leave them at default allow-all and do all control in security groups: NACLs are stateless, so every rule needs a matching ephemeral-port return rule and a missing one produces intermittent failures that cost hours. Use them only for explicit subnet-level deny lists.
- **Terraform vs CloudFormation/CDK.** The frontier is who owns state: teams without reliable remote-state discipline get fewer 3am problems from CloudFormation's managed state and native drift detection; teams with multi-cloud footprints or heavy module reuse get more leverage from Terraform. Both lose to console clicking.

## Security & Privacy

**Credentials:** this skill drives the AWS CLI, which reads credentials from `~/.aws/credentials`, `~/.aws/sso/`, or environment variables. It does NOT store, log, copy, or transmit AWS credentials, and never writes a credential into `~/Clawic/data/aws/`.

**Local storage:** preferences, memory, inventory, and cost history stay in `~/Clawic/data/aws/` on this machine — account IDs and resource names only, no secrets.

**Guardrails:** commands are read-only by default. Destructive operations (delete, terminate, modify, force) are presented with their blast radius and require explicit user confirmation before running.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/aws (install if the user confirms):
- `terraform` — HCL authoring, state surgery, module design
- `k8s` — Kubernetes manifests and cluster debugging, for EKS workloads
- `s3` — object-storage access patterns, presigned URLs, lifecycle detail
- `dynamodb` — partition/sort key modeling and query design
- `infrastructure` — provider-agnostic architecture decisions

## Feedback

- If useful, star it: https://clawic.com/skills/aws
- Latest version: https://clawic.com/skills/aws

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/aws.
