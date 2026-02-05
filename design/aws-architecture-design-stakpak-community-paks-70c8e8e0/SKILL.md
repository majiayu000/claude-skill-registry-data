---
name: aws-architecture-design
description: |
  Purpose: Standardize how stakpak designs and optimizes AWS architectures.
  Scope:
  Greenfield: design new infrastructure.
  Brownfield: analyze existing architectures and propose improvements.
license: MIT
tags:
  - aws
  - architecture
  - design aws architecture
  - optimize aws architecture
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# Designing & Optimizing AWS Architectures Rule Book

# Overview

**Purpose:** Standardize how the agent designs and optimizes AWS architectures.

**Scope:**

* **Greenfield:** design new infrastructure.
* **Brownfield:** analyze existing architectures and propose improvements.

**Reference Frameworks:**

* AWS Well-Architected Framework (WAF)
* Well-Architected Lenses (Serverless, SaaS, ML, etc.)

# Phases

1. **Discover**: gather requirements / current context.
2. **Design**: propose new architecture.
3. **Review**: map an existing system against Well-Architected.
4. **Optimize**: recommend improvements.

# Workflow

## Step 1: Context Gathering

* Start by clarifying whether the goal is to **design a new infrastructure** or **optimize an existing one**.
* If it's new, focus first on the **core objective** (what the system needs to achieve). Other details like constraints and workloads can be explored gradually as the design unfolds.
* For existing environments, first locate the infrastructure (accounts, regions, IaC repositories). From there, review the supporting assets such as IaC definitions, diagrams, monitoring data, and cost reports.

## Step 2: Requirements Definition

* Functional (APIs, batch jobs, analytics).
* Non-functional (availability, performance, security, compliance, cost).

## Step 3: Architecture Mapping

* Match requirements to AWS services (compute, storage, networking, database).

* Consider **Serverless-first** designs when applicable:

  * Compute → Lambda, Step Functions, Fargate

  * API → API Gateway + AppSync

  * Storage → S3, DynamoDB

  * Messaging → SNS, SQS, EventBridge

  * Security → IAM, Cognito, WAF, KMS

#### **Step 4: Well-Architected Review**

* **5 Pillars Checklist**

  * **Operational Excellence**: monitoring, IaC, automation.

  * **Security**: IAM least privilege, encryption, threat detection.

  * **Reliability**: HA, backup/restore, fault isolation.

  * **Performance Efficiency**: caching, scaling, right-sizing.

  * **Cost Optimization**: Spot, RIs, lifecycle rules, serverless.

* **Serverless Lens Focus**:

  * Minimize undifferentiated ops.

  * Event-driven orchestration (Step Functions/EventBridge).

  * Use managed data stores (DynamoDB, Aurora Serverless).

  * Secure with IAM boundaries, managed identity (Cognito).

#### **Step 5: Proposal / Optimization**

* Draft architecture diagram.

* For existing → generate **recommendations table**: Pillar, Current Gap, Recommendation, Expected Impact

#### **Step 6: Validation**

* Risks & mitigations.

* Cost estimates (before/after).

* Load test strategy

#### **Step 7: Report**

* Write everything into **Markdown architecture file**.

* Include: Overview, Requirements, Architecture, Diagrams, Well-Architected Review, Optimizations, Risks, Costs.

# Security References

### **1. Identity & Access**

* Enforce **least privilege** IAM policies.

* Prefer **IAM roles over static keys**.

* Use **ABAC or RBAC** (tags, groups, accounts) for scalable access control.

* Require **MFA** for privileged accounts.

* Use **AWS SSO / IAM Identity Center** for central identity management.

### **2. Data Protection**

* Encrypt **all data at rest** (S3, EBS, RDS, DynamoDB, etc.) with KMS CMKs.

* Encrypt **all data in transit** (TLS 1.2+).

* Enable **S3 Block Public Access** and least privilege bucket policies.

* Use **Secrets Manager / Parameter Store** — no hardcoded credentials.

### **3. Network Security**

* Use **VPC with private subnets** for workloads.

* Restrict inbound/outbound traffic with **Security Groups and NACLs**.

* Use **VPC Endpoints** for private service access (no public internet).

* Add **WAF/Shield** for public-facing endpoints.

* Prefer **ALB/NLB with TLS termination** over exposing EC2 directly.

### **4. Monitoring & Logging**

* Enable **CloudTrail** in all regions and send logs to a centralized S3 bucket.

* Enable **Config Rules** for compliance enforcement.

* Integrate **GuardDuty, Security Hub, Inspector** for threat detection.

* Centralize logs (CloudWatch Logs / OpenSearch) and set retention policies.

* Use **CloudWatch alarms** for anomalies, cost spikes, security events.

### **5. Resilience & Recovery**

* Apply **multi-AZ deployments** for critical data stores.

* Enforce **automated backups** with retention policies.

* Test **disaster recovery scenarios** (RTO/RPO compliance).

* Use **infrastructure as code** (Terraform/CDK/CloudFormation) to rebuild environments securely.

### **6. Governance & Compliance**

* Apply **service control policies (SCPs)** with AWS Organizations.

* Enforce **tagging standards** for resources (cost, owner, env).

* Align with compliance frameworks (ISO, SOC2, HIPAA, GDPR) when required.

* Use **Trusted Advisor** and **Well-Architected Tool** for regular reviews.

# Cost References

1. **Native Cost Tools First**: Use cloud provider billing tools as primary source
2. **Credits Excluded**: Always exclude credits unless analyzing discount impact
3. **Comprehensive Discovery**: Identify ALL infrastructure components
4. **Current Pricing**: Research real-time standard pricing only
5. **Python Calculations**: Use Python for ALL numeric operations

NOTE: Dont implement anything until you generate the report and ask for my permission
