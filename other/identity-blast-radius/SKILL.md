---
name: identity-blast-radius
description: Analyses the maximum damage a compromised IAM identity can cause. Maps effective permissions across data, identity, detection, compute, and network categories, translates them into real-world business consequences (data exposure, compliance impact, attack narratives), then classifies overall risk. Use when the user asks "what if this role is compromised?", "blast radius", "what can this identity do?", or "identity risk assessment".
---

# Identity Blast Radius

Answers: **"If this identity is compromised, what is the maximum damage?"**

Takes a single IAM principal (user, role, or instance profile) and maps everything it can reach — across all service categories — then translates technical permissions into real-world business consequences and classifies the combined risk level.

---

## Table of Contents

- [When to Trigger](#when-to-trigger)
- [Input Requirements](#input-requirements)
- [Analysis Process](#analysis-process)
- [Impact Categories](#impact-categories)
- [Risk Classification](#risk-classification)
- [Output Format](#output-format)
- [Output Storage](#output-storage)
- [Integration with Pipeline](#integration-with-pipeline)

---

## When to Trigger

The Director triggers this skill when the user asks:
- "What if this role/user is compromised?"
- "Blast radius of X"
- "What can this identity do?"
- "Identity risk assessment"
- "What's the damage if X is compromised?"
- "How dangerous is this role?"
- "Impact analysis for X"

This skill can run standalone (user names a specific identity) or as a follow-up after the pipeline confirms a finding involving an identity (e.g., after PMapper identifies an escalation target).

---

## Input Requirements

One of:
- IAM role ARN: `arn:aws:iam::123456789012:role/app-server-role`
- IAM user ARN: `arn:aws:iam::123456789012:user/deploy-bot`
- IAM user name or role name (resolved via `aws iam get-role` / `aws iam get-user`)
- Instance profile name (resolved to its associated role)

If the user says "blast radius of my EC2 instance", resolve the instance → instance profile → role first.

---

## Analysis Process

All `aws` and `pmapper` commands run during analysis MUST be displayed inline using the mandatory CLI format in `CLAUDE.md`. This skill runs real commands — full visibility applies.

### Step 1: Resolve the identity

```bash
# For a role
aws iam get-role --role-name {{role_name}} --query 'Role.{Arn:Arn,Path:Path,Boundary:PermissionsBoundary.PermissionsBoundaryArn}'

# For a user
aws iam get-user --user-name {{user_name}} --query 'User.{Arn:Arn,Path:Path,Boundary:PermissionsBoundary.PermissionsBoundaryArn}'

# For an instance profile → role
aws iam get-instance-profile --instance-profile-name {{profile}} --query 'InstanceProfile.Roles[0].RoleName'
```

### Step 2: Enumerate effective permissions

Collect ALL policies attached to the identity:

```bash
# Attached managed policies
aws iam list-attached-role-policies --role-name {{role_name}} --query 'AttachedPolicies[].PolicyArn'

# Inline policies
aws iam list-role-policies --role-name {{role_name}} --query 'PolicyNames'

# For each managed policy — get the active version
aws iam get-policy --policy-arn {{policy_arn}} --query 'Policy.DefaultVersionId'
aws iam get-policy-version --policy-arn {{policy_arn}} --version-id {{version}} --query 'PolicyVersion.Document'

# For each inline policy
aws iam get-role-policy --role-name {{role_name}} --policy-name {{policy_name}} --query 'PolicyDocument'

# Permission boundary (if present)
aws iam get-policy-version --policy-arn {{boundary_arn}} --version-id {{version}} --query 'PolicyVersion.Document'
```

Combine all Allow statements. Apply permission boundary intersection if one exists. Note any Deny statements — they restrict the blast radius.

### Step 3: Map access by impact category

For each category, check whether the identity's effective permissions grant access, then enumerate which specific resources are reachable.

**Data Access**
```bash
# S3 — which buckets can it read/write/delete?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names s3:GetObject s3:PutObject s3:DeleteObject s3:ListBucket \
  --resource-arns "arn:aws:s3:::*"

# Cross-reference with actual buckets
aws s3api list-buckets --query 'Buckets[].Name'

# DynamoDB
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names dynamodb:GetItem dynamodb:PutItem dynamodb:DeleteTable \
  --resource-arns "arn:aws:dynamodb:*:*:table/*"

# RDS
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names rds:DeleteDBInstance rds:ModifyDBInstance rds:CreateDBSnapshot \
  --resource-arns "arn:aws:rds:*:*:db:*"

# Secrets Manager
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names secretsmanager:GetSecretValue secretsmanager:DeleteSecret \
  --resource-arns "arn:aws:secretsmanager:*:*:secret:*"
```

**Identity Access**
```bash
# Can it modify IAM?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names iam:PassRole iam:CreateRole iam:AttachRolePolicy iam:PutRolePolicy \
  iam:CreateUser iam:CreateAccessKey iam:UpdateAssumeRolePolicy \
  --resource-arns "arn:aws:iam::*:role/*" "arn:aws:iam::*:user/*"

# Can it assume other roles?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names sts:AssumeRole \
  --resource-arns "arn:aws:iam::*:role/*"

# PMapper — transitive escalation paths
pmapper query "preset privesc {{arn}}"
```

**Detection Access**
```bash
# Can it blind the defenders?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names cloudtrail:StopLogging cloudtrail:DeleteTrail \
  guardduty:DeleteDetector guardduty:UpdateDetector \
  securityhub:DisableSecurityHub \
  config:StopConfigurationRecorder config:DeleteConfigurationRecorder \
  logs:DeleteLogGroup logs:DeleteLogStream \
  --resource-arns "*"
```

**Compute Access**
```bash
# Can it run code or modify running services?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names ec2:RunInstances ec2:TerminateInstances \
  lambda:CreateFunction lambda:UpdateFunctionCode lambda:InvokeFunction \
  ecs:RunTask ecs:StopTask \
  --resource-arns "*"
```

**Network Access**
```bash
# Can it modify network controls?
aws iam simulate-principal-policy --policy-source-arn {{arn}} \
  --action-names ec2:AuthorizeSecurityGroupIngress ec2:RevokeSecurityGroupEgress \
  ec2:CreateSecurityGroup ec2:DeleteSecurityGroup \
  ec2:ModifyVpcAttribute ec2:CreateVpcEndpoint \
  --resource-arns "*"
```

### Step 4: Count reachable resources

For each "allowed" action, enumerate the actual resources that exist:

```bash
# Example: identity can s3:GetObject on * — how many buckets exist?
aws s3api list-buckets --query 'Buckets[].Name' --output text | wc -w

# How many roles can it assume?
# Use PMapper if available, otherwise:
aws iam list-roles --query 'Roles[?AssumeRolePolicyDocument.Statement[?Principal.AWS==`{{arn}}`]].RoleName'
```

The blast radius is permissions × resources. `s3:*` on a policy means nothing if there are zero buckets. `iam:PassRole` scoped to one specific role is lower risk than `iam:PassRole` on `*` with 50 Lambda-assumable roles.

### Step 5: Check SCP and boundary constraints

If `SCP_STATUS = AVAILABLE` or `USER_PROVIDED`, cross-reference the identity's effective permissions against SCPs. An SCP Deny overrides IAM Allow — it shrinks the blast radius.

If a permission boundary exists, note it and intersect with the Allow statements. Report both the raw permissions and the boundary-constrained permissions.

### Step 6: Contextualise real-world impact

Technical permissions alone don't tell the story. This step translates enumerated access into **business consequences** — what an auditor or manager needs to understand.

For every reachable resource from Steps 3–4, inspect metadata to determine what's actually at stake:

**Infer data sensitivity from resource metadata**

```bash
# S3 — bucket names, tags, encryption, public access status
aws s3api get-bucket-tagging --bucket {{bucket_name}} 2>/dev/null
aws s3api get-bucket-encryption --bucket {{bucket_name}} 2>/dev/null
aws s3api get-public-access-block --bucket {{bucket_name}} 2>/dev/null

# Sample object keys to infer content type (first 20 keys only)
aws s3api list-objects-v2 --bucket {{bucket_name}} --max-keys 20 --query 'Contents[].Key'

# DynamoDB — table names and tags
aws dynamodb describe-table --table-name {{table}} --query 'Table.{Name:TableName,ItemCount:ItemCount,SizeBytes:TableSizeBytes}'
aws dynamodb list-tags-of-resource --resource-arn {{table_arn}}

# RDS — engine, multi-AZ, tags
aws rds describe-db-instances --db-instance-identifier {{instance}} --query 'DBInstances[0].{Engine:Engine,MultiAZ:MultiAZ,PubliclyAccessible:PubliclyAccessible}'
aws rds list-tags-for-resource --resource-name {{db_arn}}

# Secrets Manager — secret names and tags (NOT values)
aws secretsmanager describe-secret --secret-id {{secret_name}} --query '{Name:Name,Tags:Tags,Description:Description}'
```

**Classify each resource using available signals:**

| Signal | How to interpret |
|:-------|:-----------------|
| Bucket/table name contains `billing`, `customer`, `user`, `payment`, `pii`, `prod`, `backup` | Likely contains sensitive business data |
| Tags: `classification:confidential`, `data-type:pii`, `environment:production` | Explicit sensitivity markers |
| RDS `PubliclyAccessible: true` | Database already exposed — compromise amplifies risk |
| Secrets named `prod-db-password`, `api-key-*`, `stripe-*` | Credential access enables lateral movement beyond AWS |
| Unencrypted S3 bucket or DynamoDB table | Data at rest is unprotected — exfiltration is trivial |
| Object keys like `exports/customers-*.csv`, `backups/*.sql` | Direct evidence of data type |

**Map to business consequences:**

For each category, state the real-world outcome in plain language:

- **Data**: "Customer PII in `prod-billing-data` bucket (23,847 objects) is readable and exfiltrable" — not just "s3:GetObject allowed on 1 bucket"
- **Identity**: "Can create backdoor admin access that survives credential rotation" — not just "iam:CreateUser allowed"
- **Detection**: "Can delete CloudTrail logs, making attacker activity undetectable — incident response team would be blind" — not just "cloudtrail:DeleteTrail allowed"
- **Compute**: "Can inject code into `payment-processor` Lambda, intercepting every transaction" — not just "lambda:UpdateFunctionCode allowed"
- **Network**: "Can open security group `sg-0abc` to 0.0.0.0/0, exposing internal database to the internet" — not just "ec2:AuthorizeSecurityGroupIngress allowed"

**Map to compliance frameworks:**

| Data type found | Compliance impact |
|:----------------|:------------------|
| Customer PII (names, emails, addresses) | GDPR Article 33 breach notification (72h), potential fines up to 4% annual revenue |
| Payment card data | PCI-DSS Requirement 7 violation, potential loss of card processing capability |
| Health records | HIPAA breach, mandatory HHS notification |
| Authentication credentials | SOC2 CC6.1 logical access controls failure |
| Financial records | SOX compliance gap if publicly traded |
| Any production data | CIS Benchmark failures, SOC2 CC6.3 (least privilege) |

Only cite frameworks where the data type is confirmed or strongly inferred — never speculate.

**Construct the worst-case narrative:**

Write a 2–3 sentence attack story that chains the categories together. This is the "headline" — what would the incident report say?

Example: *"An attacker compromising `app-server-role` could exfiltrate the entire customer database from `prod-billing-data` (est. 500K records including PII), establish persistent access via a new IAM user, then delete CloudTrail logs to cover their tracks. The organisation would likely not detect the breach until customer data appeared on the dark web. This would trigger GDPR mandatory notification and estimated regulatory exposure of €2–10M."*

### Step 7: Classify risk level

Apply the risk matrix from the Risk Classification section below. The real-world impact from Step 6 informs severity — a CRITICAL technical finding on a dev sandbox with no real data may warrant downgrading, while a MEDIUM technical finding on production PII may warrant upgrading.

---

## Impact Categories

| Category | What it covers | Key actions to check | Why it matters |
|:---------|:---------------|:---------------------|:---------------|
| **Data** | S3, DynamoDB, RDS, Secrets Manager, KMS | Get/Put/Delete on data stores, GetSecretValue, Decrypt | Data exfiltration and destruction |
| **Identity** | IAM users, roles, policies, STS | PassRole, CreateRole, AttachPolicy, AssumeRole, CreateAccessKey | Persistence and lateral movement |
| **Detection** | CloudTrail, GuardDuty, Security Hub, Config, CloudWatch Logs | StopLogging, DeleteDetector, DisableSecurityHub, DeleteLogGroup | Covering tracks |
| **Compute** | EC2, Lambda, ECS, EKS | RunInstances, CreateFunction, UpdateFunctionCode, RunTask | Code execution and resource abuse |
| **Network** | VPC, Security Groups, NACLs, Endpoints | AuthorizeIngress, ModifyVpc, CreateEndpoint | Opening attack surface |

---

## Risk Classification

### Risk Level Matrix

The risk level is determined by the **combination** of categories, not any single one:

| Risk Level | Criteria |
|:-----------|:---------|
| **CRITICAL** | Identity + Detection (can escalate AND cover tracks), OR Data(write/delete) + Detection (can exfil AND cover tracks), OR admin-equivalent access (`*` on `*`) |
| **HIGH** | Identity(PassRole/AssumeRole) + Compute (can pivot to other roles via code execution), OR Data(write/delete) on sensitive resources without Detection access, OR Identity + Data(read) on 10+ resources |
| **MEDIUM** | Data(read-only) across multiple services, OR Compute without Identity access, OR Network modification without Compute |
| **LOW** | Single-service read-only access, OR scoped write access to non-sensitive resources |
| **INFORMATIONAL** | No meaningful access beyond describe/list on non-sensitive services |

### Amplifying Factors (raise by one level)

- Wildcarded resource (`*`) on sensitive actions
- No permission boundary
- Can assume cross-account roles
- Access to KMS Decrypt on customer-managed keys
- SCP coverage unknown (`SCP_STATUS = UNKNOWN`)

### Mitigating Factors (lower by one level)

- Permission boundary constrains effective permissions
- SCPs deny critical actions (confirmed, not assumed)
- All access scoped to specific resource ARNs (not wildcarded)
- Identity tagged `environment: dev/test/sandbox`
- MFA required for sensitive actions (and MFA condition uses `BoolIfExists`)

---

## Output Format

The blast radius report uses the output skill's structure with a dedicated Blast Radius section:

```markdown
---
## Results

### Identity Blast Radius: {{identity_name}}
Identity Blast Radius | {{YYYY-MM-DD}} | {{account_id}} | SCP: {{status}}

**Identity:** `{{full_arn}}`
**Type:** {{IAM Role | IAM User | Instance Profile → Role}}
**Permission Boundary:** {{boundary_arn | None}}

### Access Summary

| Category | Access Level | Resources Reachable | Key Actions |
|:---------|:-------------|:--------------------|:------------|
| Data | {{Read/Write/Delete/None}} | {{count + types}} | {{top actions}} |
| Identity | {{Modify/Assume/None}} | {{count roles/users}} | {{top actions}} |
| Detection | {{Disable/Modify/None}} | {{count services}} | {{top actions}} |
| Compute | {{Execute/Modify/None}} | {{count resources}} | {{top actions}} |
| Network | {{Modify/None}} | {{count SGs/VPCs}} | {{top actions}} |

### Risk Level: {{CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL}}

**Why:** {{one paragraph explaining the risk — which combination of categories drives the classification}}

**Amplifying:** {{factors that increase risk, or None}}
**Mitigating:** {{factors that decrease risk, or None}}

### Worst-Case Scenario

{{2–3 sentence attack narrative chaining categories together — what would the incident report headline say? Written in plain language for a non-technical audience. Include estimated data exposure scope and compliance consequences.}}

### Real-World Impact

| Category | Technical Access | Business Consequence | Data at Risk | Compliance |
|:---------|:----------------|:---------------------|:-------------|:-----------|
| Data | {{actions + resource count}} | {{plain-language outcome, e.g. "Customer PII exfiltrable from prod-billing-data (23K records)"}} | {{data types: PII, credentials, financial, health, none}} | {{GDPR, PCI-DSS, HIPAA, SOC2, SOX, CIS, or N/A}} |
| Identity | {{actions + resource count}} | {{e.g. "Backdoor admin user survives credential rotation"}} | {{credentials, policies}} | {{SOC2, CIS}} |
| Detection | {{actions + resource count}} | {{e.g. "CloudTrail deletion blinds incident response"}} | {{audit logs}} | {{SOC2, CIS}} |
| Compute | {{actions + resource count}} | {{e.g. "Code injection into payment-processor Lambda"}} | {{varies by function}} | {{varies}} |
| Network | {{actions + resource count}} | {{e.g. "Internal DB exposed to internet via SG change"}} | {{varies by exposure}} | {{CIS}} |

### Detailed Access

#### Data Access
{{list every reachable resource with action level — complete enumeration applies}}
{{for each resource: include inferred data type and sensitivity based on name, tags, and object key sampling}}

#### Identity Access
{{list assumable roles, passable roles, modifiable policies}}
{{include PMapper escalation paths if PMAPPER_STATUS = AVAILABLE}}

#### Detection Access
{{list which detection services can be disabled/modified}}
{{note: time-to-blindness — how quickly could an attacker erase evidence?}}

#### Compute Access
{{list which compute resources can be created/modified/invoked}}
{{for Lambda/ECS: note what each function/task does based on name and tags}}

#### Network Access
{{list which security groups/VPCs/endpoints can be modified}}
{{note: what services are behind each SG — would opening it expose a database, API, etc.?}}

### Recommendations
| Priority | Action | Effort | Risk Reduction |
|:---------|:-------|:-------|:---------------|
| P0 | {{most impactful reduction}} | Low/Med/High | {{what it eliminates}} |

### Confidence: {{N}}/5
{{gaps — e.g., SCP unknown, resource policies not checked, cross-account not evaluated}}
```

**Complete enumeration applies** — every reachable resource listed with full ARN. No "and 30 more".

---

## Output Storage

Reports are saved to `data/identity-blast-radius/reports/`:

```
data/identity-blast-radius/reports/
└── {account_id}-{date}-{identity_name}.md
```

Example: `123456789012-2026-03-24-app-server-role.md`

---

## Integration with Pipeline

### As a standalone query

User asks "blast radius of role X" → Director triggers this skill directly. No pipeline needed — this is an analysis skill, not a claim validation.

### As a follow-up

After the pipeline confirms an escalation finding (e.g., PMapper shows `dev-role` can reach `admin-role`), the Director can trigger blast radius analysis on the escalation target to quantify the impact:

1. Pipeline confirms: `dev-role` can escalate to `admin-role` (Score 5)
2. Director triggers blast radius on `admin-role` — "what does the attacker get after escalating?"
3. Blast radius output feeds into the Impact section of the finding

### With PMapper

When `PMAPPER_STATUS = AVAILABLE`, the Identity Access section MUST include PMapper's transitive analysis — not just direct AssumeRole permissions, but the full escalation graph from this identity. This is the key differentiator: IAM policy says what the identity is *allowed* to do; PMapper says what it can *actually reach*.

### With PoC Generator

After blast radius identifies high-risk access paths, the user can ask for PoC playbooks for specific paths. The blast radius report provides the input (identity + reachable targets) and the PoC generator produces the reproduction steps.
